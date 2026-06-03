"""Maintenance-operation orchestration (GUI-agnostic, unit-testable).

Encapsulates the compliance-oriented reset flow so it can be tested without a UI:
  * both user confirmations are required,
  * a backup is attempted before any write,
  * if the backup fails the reset is stopped unless the caller explicitly
    overrides (with a warning recorded in the log),
  * every attempt/success/failure is recorded in the local operation log.

The waste-ink counter reset is a maintenance-support function intended for use
only after the physical waste-ink pad/tank has been inspected, cleaned, replaced,
or redirected. It does not perform any physical maintenance itself.
"""
import eeprom_io
import oplog

LOW_COUNTER_PCT = 50.0  # below this, resetting is usually unnecessary


class ConfirmationRequired(Exception):
    """Raised when the required user acknowledgements were not both given."""


class BackupFailed(Exception):
    """Raised when the pre-reset backup could not be created and was not overridden."""


def counters_are_low(waste_rows, threshold=LOW_COUNTER_PCT):
    """waste_rows: list of (name, raw, max, pct). True if the highest pad is low."""
    pcts = [pct for (_n, _r, _m, pct) in waste_rows] or [0.0]
    return max(pcts) < threshold


def perform_reset(backend, *, acknowledged_physical, accepted_responsibility,
                  override_backup_failure=False):
    """Run the maintenance-counter reset with safety preconditions.

    Returns a result dict: {backup_path, backup_ok, before, after}.
    Raises ConfirmationRequired or BackupFailed on guarded conditions.
    """
    model = getattr(backend, "model", "?")
    transport = getattr(backend, "transport", "?")

    if not (acknowledged_physical and accepted_responsibility):
        oplog.log_event("reset_blocked", model=model, transport=transport,
                        ack_physical=bool(acknowledged_physical),
                        ack_responsibility=bool(accepted_responsibility),
                        reason="confirmations_not_given")
        raise ConfirmationRequired(
            "Both the physical-maintenance acknowledgement and the responsibility "
            "confirmation are required before a counter reset.")

    # snapshot counter values before (for the log / troubleshooting)
    try:
        before = [(n, raw, mx) for (n, raw, mx, _pct) in backend.read_waste()]
    except Exception:
        before = []

    oplog.log_event("reset_attempt", model=model, transport=transport,
                    ack_physical=True, ack_responsibility=True,
                    counters_before=";".join(f"{n}:{r}/{m}" for n, r, m in before) or "n/a")

    # backup before write
    backup_path, backup_ok = None, False
    try:
        backup_path = eeprom_io.backup(backend, note="pre-reset")
        backup_ok = True
        oplog.log_event("backup_ok", model=model, path=backup_path)
    except Exception as e:
        oplog.log_event("backup_failed", model=model, error=repr(e),
                        override=bool(override_backup_failure))
        if not override_backup_failure:
            raise BackupFailed(
                f"Backup before reset failed: {e}. Reset stopped. You may retry, "
                f"or explicitly override to proceed without a backup (not recommended).")

    # perform the reset
    try:
        backend.reset()
    except Exception as e:
        oplog.log_event("reset_failed", model=model, transport=transport,
                        backup_path=backup_path, error=repr(e))
        raise

    # verify after
    try:
        after = [(n, raw, mx, pct) for (n, raw, mx, pct) in backend.read_waste()]
    except Exception:
        after = []

    oplog.log_event("reset_success", model=model, transport=transport,
                    backup_path=backup_path, backup_ok=backup_ok,
                    counters_after=";".join(f"{n}:{r}/{m}" for n, r, m, _p in after) or "n/a")

    return {"backup_path": backup_path, "backup_ok": backup_ok,
            "before": before, "after": after}
