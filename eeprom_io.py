"""EEPROM backup & restore. Before any write we snapshot every address a reset
will touch (plus the waste-counter addresses) to a timestamped JSON file, so a bad
reset can be reversed. Works with any backend exposing all_addresses()/read_byte/
write_byte/model/transport.
"""
import json
import os
import sys
import time


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def backups_dir():
    d = os.path.join(app_dir(), "backups")
    os.makedirs(d, exist_ok=True)
    return d


def settings_path():
    d = os.path.join(app_dir(), "data")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "settings.json")


def backup(backend, note="pre-reset"):
    addrs = backend.all_addresses()
    values = {a: backend.read_byte(a) for a in addrs}
    stamp = time.strftime("%Y%m%d-%H%M%S")
    safe = "".join(ch if ch.isalnum() else "_" for ch in (backend.model or "printer"))
    path = os.path.join(backups_dir(), f"{safe}_{stamp}.json")
    payload = {
        "model": backend.model, "transport": backend.transport,
        "note": note, "timestamp": stamp,
        "eeprom": {str(a): v for a, v in values.items()},
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path


def list_backups():
    d = backups_dir()
    return sorted((os.path.join(d, f) for f in os.listdir(d) if f.endswith(".json")), reverse=True)


def load_backup(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def restore(backend, path):
    data = load_backup(path)
    eeprom = data.get("eeprom", {})
    written = 0
    for addr_s, value in eeprom.items():
        backend.write_byte(int(addr_s), int(value))
        written += 1
    return written, len(eeprom)
