"""Local operation logging.

Writes maintenance-operation records to a local log file next to the application.
Privacy-by-default: records the printer MODEL, transport, counter values, backup
path, user-confirmation flags and errors -- but NOT printer serial numbers or any
personal identifiers. Nothing is transmitted off the device.
"""
import os
import time

import eeprom_io


def logs_dir():
    d = os.path.join(eeprom_io.app_dir(), "logs")
    os.makedirs(d, exist_ok=True)
    return d


def log_path():
    return os.path.join(logs_dir(), "operations.log")


def log_event(event, **fields):
    """Append one structured, human-readable line to the local operation log.

    Do not pass serial numbers or personal identifiers as fields.
    """
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    parts = [f"{ts}", f"event={event}"]
    for k, v in fields.items():
        parts.append(f"{k}={v}")
    line = " | ".join(parts)
    try:
        with open(log_path(), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        # logging must never crash the application
        pass
    return line
