"""Automated tests for the maintenance-reset safety controller (operations.py).

Run:  python -m unittest discover -s tests -v
These tests use a fake backend and do NOT touch any real printer.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import operations
import eeprom_io
import oplog


class FakeBackend:
    model = "TEST Model"
    transport = "USB (D4)"

    def __init__(self, waste=None):
        self._waste = waste if waste is not None else [
            ("Main waste ink pad", 6000, 6346, 94.5),
            ("Platen / borderless pad", 100, 3416, 2.9),
            ("Flushing / cleaning pad", 50, 1300, 3.8),
        ]
        self.reset_called = False
        self.order = []

    def read_waste(self):
        return list(self._waste)

    def all_addresses(self):
        return [0x30, 0x31]

    def read_byte(self, a):
        return 0

    def write_byte(self, a, v):
        pass

    def reset(self):
        self.reset_called = True
        self.order.append("reset")


class OperationsTest(unittest.TestCase):
    def setUp(self):
        # capture log events instead of writing to disk
        self.events = []
        self._orig_log = oplog.log_event
        operations.oplog.log_event = lambda ev, **kw: self.events.append((ev, kw))
        # default: backup succeeds and records ordering
        self._orig_backup = eeprom_io.backup

    def tearDown(self):
        operations.oplog.log_event = self._orig_log
        eeprom_io.backup = self._orig_backup

    def _patch_backup(self, fail=False):
        def fake_backup(backend, note="pre-reset"):
            backend.order.append("backup")
            if fail:
                raise OSError("simulated backup failure")
            return "C:/backups/test.json"
        operations.eeprom_io.backup = fake_backup

    def test_requires_both_confirmations(self):
        self._patch_backup()
        be = FakeBackend()
        with self.assertRaises(operations.ConfirmationRequired):
            operations.perform_reset(be, acknowledged_physical=True, accepted_responsibility=False)
        self.assertFalse(be.reset_called)
        self.assertTrue(any(ev == "reset_blocked" for ev, _ in self.events))

    def test_backup_runs_before_reset(self):
        self._patch_backup()
        be = FakeBackend()
        res = operations.perform_reset(be, acknowledged_physical=True, accepted_responsibility=True)
        self.assertTrue(be.reset_called)
        self.assertEqual(be.order, ["backup", "reset"])  # backup strictly before reset
        self.assertTrue(res["backup_ok"])
        self.assertEqual(res["backup_path"], "C:/backups/test.json")

    def test_backup_failure_stops_reset(self):
        self._patch_backup(fail=True)
        be = FakeBackend()
        with self.assertRaises(operations.BackupFailed):
            operations.perform_reset(be, acknowledged_physical=True, accepted_responsibility=True)
        self.assertFalse(be.reset_called)
        self.assertTrue(any(ev == "backup_failed" for ev, _ in self.events))

    def test_backup_failure_override_proceeds(self):
        self._patch_backup(fail=True)
        be = FakeBackend()
        res = operations.perform_reset(be, acknowledged_physical=True, accepted_responsibility=True,
                                       override_backup_failure=True)
        self.assertTrue(be.reset_called)
        self.assertFalse(res["backup_ok"])

    def test_logging_attempt_and_success(self):
        self._patch_backup()
        be = FakeBackend()
        operations.perform_reset(be, acknowledged_physical=True, accepted_responsibility=True)
        names = [ev for ev, _ in self.events]
        self.assertIn("reset_attempt", names)
        self.assertIn("reset_success", names)

    def test_low_counter_detection(self):
        low = [("A", 10, 6346, 0.2), ("B", 0, 3416, 0.0)]
        high = [("A", 6000, 6346, 94.5)]
        self.assertTrue(operations.counters_are_low(low))
        self.assertFalse(operations.counters_are_low(high))


class ModelDbTest(unittest.TestCase):
    def test_resolve_l3250(self):
        import printer_core
        key, entry = printer_core.resolve("L3250 Series")
        self.assertEqual(key, "L3250")
        self.assertEqual(len(entry["counters"]), 3)
        self.assertTrue(len(entry["reset"]) >= 10)

    def test_model_count_nonzero(self):
        import printer_core
        self.assertGreater(printer_core.model_count(), 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
