"""Clean printer backend: independent D4 stack (epson_d4) + embedded DB (model_db).
No third-party runtime code; database is compiled in (single-file distribution).
"""
import re
import struct

import epson_d4
from model_db import MODELS

VALIDATED = {"l3250", "l3251", "l3253", "l3255"}  # verified on real hardware

# minimal status decode (codes are documented facts from the BDC/ST2 status block)
_STATE = {0x00: "ERROR", 0x01: "SELF_PRINTING", 0x02: "BUSY", 0x03: "WAITING",
          0x04: "IDLE", 0x05: "PAUSE", 0x06: "INK_DRYING", 0x07: "CLEANING",
          0x08: "FACTORY", 0x0A: "SHUTDOWN"}
_ERROR = {0x00: "FATAL", 0x05: "INK_OUT", 0x06: "PAPER_OUT", 0x10: "SERVICE_REQUIRED",
          0x25: "COVER_OPEN", 0x22: "NO_MAINTENANCE_BOX"}


def _norm(name):
    n = (name or "").lower().strip()
    n = re.sub(r"\bseries\b", "", n)
    return re.sub(r"[^a-z0-9]", "", n)


def resolve(mdl):
    """Return (key, entry) for a printer MDL string, or (None, None)."""
    target = _norm(mdl)
    if not target:
        return None, None
    for key, entry in MODELS.items():
        if _norm(key) == target or target in entry.get("names", []):
            return key, entry
    return None, None


def model_count():
    return len(MODELS)


def parse_status(resp):
    """Decode @BDC ST2 payload -> (state_name, error_name, serial)."""
    state, error, serial = "UNKNOWN", "NONE", ""
    head = b"@BDC ST2\r\n"
    if not resp.startswith(head):
        return state, error, serial
    data = resp[len(head):]
    if len(data) < 2:
        return state, error, serial
    length = int.from_bytes(data[0:2], "little")
    i, end = 2, min(len(data), length + 2)
    while i + 2 <= end:
        hdr = data[i]; n = data[i + 1]; body = data[i + 2:i + 2 + n]; i += 2 + n
        if hdr == 0x01 and body:
            state = _STATE.get(body[0], f"0x{body[0]:02X}")
        elif hdr == 0x02 and body:
            error = _ERROR.get(body[0], f"0x{body[0]:02X}") if body[0] != 0xFF else "NONE"
        elif hdr == 0x40:
            serial = body.decode("ascii", "replace")
    return state, error, serial


class UsbBackend:
    transport = "USB (D4)"

    def __init__(self, path=None):
        self.path = path
        self.model = None
        self.key = None
        self.entry = None
        self.experimental = True
        self._t = None
        self._ctrl = None

    def __enter__(self):
        paths = [self.path] if self.path else epson_d4.enumerate_epson_usb()
        if not paths or not paths[0]:
            raise RuntimeError("No Epson USB printer detected. Connect it by USB and power it on.")
        self.path = paths[0]
        self._t = epson_d4.UsbTransport(self.path).open()
        ident = {}
        for field in self._t.get_1284_id().split(";"):
            if ":" in field:
                k, v = field.split(":", 1)
                ident[k.strip()] = v.strip()
        mdl = ident.get("MDL", "")
        self.key, self.entry = resolve(mdl)
        if self.entry is None:
            self._t.close()
            raise RuntimeError(f"Printer model '{mdl}' is not in the database.")
        self.model = mdl or self.key
        self.experimental = _norm(self.key) not in VALIDATED
        self._ctrl = epson_d4.EpsonControl(self._t, self.entry)
        return self

    def __exit__(self, *exc):
        try:
            if self._ctrl:
                self._ctrl.close()
        finally:
            if self._t:
                self._t.close()
        return False

    # primitives
    def read_byte(self, addr):
        return self._ctrl.read_byte(addr)

    def write_byte(self, addr, value):
        return self._ctrl.write_byte(addr, value)

    # derived data
    @property
    def reset_pairs(self):
        return [(int(a), int(v)) for a, v in self.entry["reset"]]

    def all_addresses(self):
        addrs = {a for a, _ in self.reset_pairs}
        for c in self.entry["counters"]:
            addrs.update(int(a) for a in c["addresses"])
        return sorted(addrs)

    def read_waste(self):
        rows = []
        for c in self.entry["counters"]:
            raw = int.from_bytes(bytes(self.read_byte(a) for a in c["addresses"]), "little")
            mx = c.get("max") or 0
            pct = (raw / mx * 100) if mx else 0.0
            rows.append((c.get("name", "Waste pad"), raw, mx, pct))
        return rows

    def read_usage(self):
        rows = []
        for name, groups in self.entry.get("usage", []):
            total, ok = 0, True
            for regs in groups:
                val = 0
                for a in regs:
                    try:
                        val = (val << 8) | self.read_byte(a)
                    except Exception:
                        ok = False
                total += val
            rows.append((name, total if ok else None))
        return rows

    def read_status(self):
        try:
            state, error, _ = parse_status(self._ctrl.get_status())
            return f"{state} / {error}"
        except Exception:
            return "unknown"

    def read_state(self):
        return {
            "model": self.model, "transport": self.transport,
            "experimental": self.experimental, "status": self.read_status(),
            "waste": self.read_waste(), "usage": self.read_usage(),
            "ink": [], "ink_reported": False,
        }

    def reset(self):
        for addr, value in self.reset_pairs:
            self.write_byte(addr, value)
