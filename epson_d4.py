"""Independent Epson USB control stack.

Implemented from public specifications and documented facts:
  * IEEE 1284.4 (ISO/IEC 19500-style transaction/packet layer over a byte channel)
  * Epson "EPSON-CTRL" remote-mode command framing (cc + little-endian length +
    payload), as documented in epson-reversing notes and the EUPL-licensed
    epson_print_conf project.
  * Windows usbprint.sys device-interface access (Win32 CreateFile / ReadFile /
    WriteFile / DeviceIoControl) per Microsoft documentation.

This module is an independent implementation; it does not copy third-party code.
Only the protocol/API facts (which are not copyrightable) are used.
"""
import ctypes
import struct
import time
import winreg
from ctypes import wintypes

# --------------------------------------------------------------------------
# Win32 USBPRINT transport
# --------------------------------------------------------------------------
GUID_USBPRINT = "{28d78fad-5a12-11d1-ae5b-0000f803a8c2}"
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_RW = 0x03
OPEN_EXISTING = 3
FILE_FLAG_NO_BUFFERING = 0x20000000
FILE_FLAG_WRITE_THROUGH = 0x80000000
INVALID_HANDLE = wintypes.HANDLE(-1).value

# usbprint IOCTLs (Microsoft documented control codes)
IOCTL_USBPRINT_GET_1284_ID = 0x220034
IOCTL_USBPRINT_SOFT_RESET = 0x220040

_k32 = ctypes.WinDLL("kernel32", use_last_error=True)
_k32.CreateFileW.restype = wintypes.HANDLE
_k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                             ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
_PDWORD = ctypes.POINTER(wintypes.DWORD)
_k32.ReadFile.restype = wintypes.BOOL
_k32.ReadFile.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, _PDWORD, ctypes.c_void_p]
_k32.WriteFile.restype = wintypes.BOOL
_k32.WriteFile.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD, _PDWORD, ctypes.c_void_p]
_k32.DeviceIoControl.restype = wintypes.BOOL
_k32.DeviceIoControl.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD,
                                 ctypes.c_void_p, wintypes.DWORD, _PDWORD, ctypes.c_void_p]
_k32.CloseHandle.restype = wintypes.BOOL
_k32.CloseHandle.argtypes = [wintypes.HANDLE]


def enumerate_epson_usb():
    """Return CreateFile device paths for connected Epson (VID_04B8) USBPRINT
    interfaces, discovered via the device-interface class registry key."""
    paths = []
    key_path = r"SYSTEM\CurrentControlSet\Control\DeviceClasses\%s" % GUID_USBPRINT
    try:
        root = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
    except OSError:
        return paths
    try:
        i = 0
        while True:
            try:
                sub = winreg.EnumKey(root, i)
            except OSError:
                break
            i += 1
            # sub looks like: ##?#USB#VID_04B8&PID_118A&MI_01#...#{guid}
            if "VID_04B8" not in sub.upper():
                continue
            path = sub
            if path.startswith("##?#"):
                path = "\\\\?\\" + path[4:]
            paths.append(path)
    finally:
        winreg.CloseKey(root)
    return paths


class UsbTransport:
    """Bidirectional byte pipe to the printer's usbprint interface."""
    MAX_READ = 0x100000

    def __init__(self, path):
        self.path = path
        self.h = None
        self._buf = b""

    def open(self):
        self.h = _k32.CreateFileW(self.path, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_RW,
                                  None, OPEN_EXISTING,
                                  FILE_FLAG_NO_BUFFERING | FILE_FLAG_WRITE_THROUGH, None)
        if not self.h or self.h == INVALID_HANDLE:
            raise OSError(f"Cannot open USB device (err {ctypes.get_last_error()})")
        self._ioctl(IOCTL_USBPRINT_SOFT_RESET)  # best-effort reset of the printer channel
        return self

    def close(self):
        if self.h and self.h != INVALID_HANDLE:
            _k32.CloseHandle(self.h)
        self.h = None

    def __enter__(self):
        return self.open()

    def __exit__(self, *exc):
        self.close()
        return False

    def _ioctl(self, code, out_size=1024):
        out = ctypes.create_string_buffer(out_size)
        returned = wintypes.DWORD(0)
        ok = _k32.DeviceIoControl(self.h, code, None, 0, out, out_size,
                                  ctypes.byref(returned), None)
        if not ok:
            return None
        return out.raw[:returned.value]

    def get_1284_id(self):
        raw = self._ioctl(IOCTL_USBPRINT_GET_1284_ID)
        if not raw:
            return ""
        # first two bytes are a big-endian length prefix
        return raw[2:].split(b"\x00")[0].decode("ascii", "replace")

    def write(self, data):
        written = wintypes.DWORD(0)
        if not _k32.WriteFile(self.h, data, len(data), ctypes.byref(written), None):
            raise OSError(f"WriteFile failed (err {ctypes.get_last_error()})")

    def _pull(self):
        buf = ctypes.create_string_buffer(self.MAX_READ)
        nread = wintypes.DWORD(0)
        if not _k32.ReadFile(self.h, buf, self.MAX_READ, ctypes.byref(nread), None):
            raise OSError(f"ReadFile failed (err {ctypes.get_last_error()})")
        return buf.raw[:nread.value]

    def read(self, n, timeout=8.0):
        deadline = None
        while len(self._buf) < n:
            chunk = self._pull()
            if chunk:
                self._buf += chunk
                deadline = None
            else:
                # nothing yet; arm a timeout so we never hang forever
                if deadline is None:
                    deadline = _mono() + timeout
                elif _mono() > deadline:
                    raise TimeoutError("USB read timed out")
                time.sleep(0.01)
        out, self._buf = self._buf[:n], self._buf[n:]
        return out

    def drain(self):
        # discard any queued/unsolicited bytes
        for _ in range(8):
            if not self._pull():
                break
        self._buf = b""


def _mono():
    # Date/clock helpers used only for relative timeouts.
    return time.perf_counter()


# --------------------------------------------------------------------------
# IEEE 1284.4 (D4) transaction layer
# --------------------------------------------------------------------------
_CMD_INIT = 0x00
_CMD_OPEN = 0x01
_CMD_CLOSE = 0x02
_CMD_CREDIT = 0x03
_CMD_CREDIT_REQ = 0x04
_CMD_GET_SOCKET = 0x09


class D4Error(RuntimeError):
    pass


class D4:
    """Minimal 1284.4 transport: socket 0 is the control socket; data channels
    are opened by name (e.g. 'EPSON-CTRL')."""

    def __init__(self, transport: UsbTransport):
        self.t = transport
        self._chan = {}  # psid -> dict(state)
        self.t.drain()
        # leave any prior mode and enter 1284.4 mode
        self.t.write(b"\x00\x00\x00\x1b\x01@EJL 1284.4\n@EJL\n@EJL\n")
        self.t.read(8)
        self._init()

    # --- packet I/O ---
    def _send_packet(self, psid, ssid, credit, control, payload):
        header = struct.pack(">BBHBB", psid, ssid, 6 + len(payload), credit, control)
        self.t.write(header + payload)

    def _recv_packet(self):
        psid, ssid, length, credit, control = struct.unpack(">BBHBB", self.t.read(6))
        payload = self.t.read(length - 6) if length > 6 else b""
        return psid, ssid, credit, control, payload

    # --- control-socket command/reply ---
    def _control(self, cmd, payload=b""):
        self._send_packet(0, 0, 1, 0, bytes([cmd]) + payload)
        psid, ssid, credit, control, reply = self._recv_packet()
        if not reply or reply[0] != (cmd | 0x80):
            raise D4Error(f"D4 command 0x{cmd:02x} failed: {reply!r}")
        return reply[2:]

    def _init(self):
        if self._control(_CMD_INIT, b"\x10") != b"\x10":
            raise D4Error("D4 Init rejected")

    def _socket_id(self, name):
        return self._control(_CMD_GET_SOCKET, name.encode("ascii"))[0]

    def open_channel(self, service_name):
        ssid = self._socket_id(service_name)
        req = struct.pack(">BBHHHH", ssid, ssid, 0xFFFF, 0xFFFF, 0, 0)
        psid, rssid, mtu, _maxc, credit = struct.unpack(">BBHHH", self._control(_CMD_OPEN, req))
        ch = {"psid": psid, "ssid": ssid, "mtu": mtu, "tx": credit, "rx": 0}
        self._chan[psid] = ch
        # grant the printer 1 credit so it can reply
        self._control(_CMD_CREDIT, struct.pack(">BBH", psid, ssid, 1))
        ch["rx"] += 1
        return ch

    def close_channel(self, ch):
        try:
            self._control(_CMD_CLOSE, struct.pack(">BB", ch["psid"], ch["ssid"]))
        except Exception:
            pass
        self._chan.pop(ch["psid"], None)

    def _ensure_tx(self, ch):
        while ch["tx"] < 1:
            resp = self._control(_CMD_CREDIT_REQ, struct.pack(">BBH", ch["psid"], ch["ssid"], 0xFFFF))
            _, _, amount = struct.unpack(">BBH", resp)
            ch["tx"] += amount
            if amount == 0:
                time.sleep(0.05)

    def transact(self, ch, data):
        """Send a command on the channel and return the reply payload bytes."""
        mtu = ch["mtu"] or 512
        view = data
        while view:
            chunk = view[: mtu - 6]
            view = view[len(chunk):]
            grant = max(0, 1 - ch["rx"])
            self._ensure_tx(ch)
            self._send_packet(ch["psid"], ch["ssid"], grant, 0x02, chunk)
            ch["rx"] += grant
            ch["tx"] -= 1
        # read one reply packet addressed to this channel
        while True:
            psid, ssid, credit, control, payload = self._recv_packet()
            if psid in self._chan:
                self._chan[psid]["tx"] += credit
                self._chan[psid]["rx"] -= 1
            if psid == ch["psid"]:
                return payload


# --------------------------------------------------------------------------
# Epson EPSON-CTRL command set
# --------------------------------------------------------------------------
def _action_code(action):
    # documented obfuscation of the action byte
    return bytes((action, action ^ 0xFF, ((action >> 1) & 0x7F) | ((action << 7) & 0x80)))


class EpsonControl:
    """Reads/writes the printer EEPROM and status over the EPSON-CTRL channel."""

    def __init__(self, transport: UsbTransport, model_entry: dict):
        self.t = transport
        self.entry = model_entry
        self.factory = bytes(model_entry["factory"])
        self.keyword = bytes(model_entry.get("keyword", []))
        self._d4 = D4(transport)
        self._ch = self._d4.open_channel("EPSON-CTRL")

    def close(self):
        try:
            self._d4.close_channel(self._ch)
        except Exception:
            pass

    def _command(self, cc: bytes, payload: bytes) -> bytes:
        frame = cc + struct.pack("<H", len(payload)) + payload
        return self._d4.transact(self._ch, frame)

    def read_byte(self, addr: int) -> int:
        payload = self.factory + _action_code(0x41) + struct.pack("<H", addr)
        resp = self._command(b"||", payload)
        if not resp.startswith(b"@BDC PS\r\n"):
            raise D4Error(f"EEPROM read rejected: {resp!r}")
        return int(resp[16:18], 16)

    def write_byte(self, addr: int, value: int):
        payload = self.factory + _action_code(0x42) + struct.pack("<H", addr) + bytes([value & 0xFF]) + self.keyword
        resp = self._command(b"||", payload)
        if b":NA;" in resp:
            raise D4Error(f"EEPROM write refused at 0x{addr:X}: {resp!r}")
        return resp

    def get_status(self) -> bytes:
        resp = self._command(b"st", b"\x01")
        return resp
