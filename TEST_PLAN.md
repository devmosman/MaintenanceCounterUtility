# Test Plan — Waste Ink Maintenance Counter Utility

**Product:** Waste Ink Maintenance Counter Utility
**Executable:** `MaintenanceCounterUtility.exe`
**Version:** 1.0.0
**License:** EUPL-1.2 (see `LICENSE.txt`)
**Platform:** Windows 64-bit, USB connection only

> This document is **not legal advice**. Anti-circumvention, repair, warranty, consumer-protection, product-liability and trademark laws vary by jurisdiction. This utility is a maintenance-focused, compliance-oriented tool intended to read approximate waste-ink maintenance counters, create a local backup, and reset those counters **only after** the owner has physically inspected, cleaned, replaced, or redirected the waste-ink pad/tank. It performs no physical maintenance and is not a substitute for service requirements. Any plan to charge for distribution **requires legal review before paid distribution** by a qualified local IP/product lawyer.

> **Non-affiliation notice:** This project is not affiliated with, endorsed by, sponsored by, or approved by Epson. Epson is a trademark of its respective owner. Product names are used only to describe compatibility with selected printer models.

---

## 1. Scope and objectives

This test plan covers the verification of the Waste Ink Maintenance Counter Utility across two layers:

1. **Automated unit/integration tests** for the reset safety controller, backup ordering, logging, low-counter detection, and the embedded model database. These live in `tests/` and exercise the backend modules (`operations.py`, `eeprom_io.py`, `oplog.py`, `model_db.py`, `printer_core.py`, `epson_d4.py`).
2. **Manual UI tests** for behaviours that depend on the GUI (`maintenance_counter_app.py`), on operator interaction, on packaging, and on the absence of any network/telemetry activity.

The runtime has **no third-party runtime dependencies** (Python standard library plus `ctypes`). PyInstaller is the only build dependency.

### Verification status of model data

- **L3250 / L3251 / L3253 / L3255** — Verified on real hardware (June 2026).
- **All other models (108 total in the embedded database)** — Experimental. The data is EUPL-derived (converted from `epson_print_conf`, EUPL-1.2, Copyright (c) 2024-2025 Ircama) and has **not** been verified on hardware by this project.

---

## 2. Test environment

| Item | Value |
| --- | --- |
| Operating system | Windows 64-bit |
| Connection | USB only |
| Python (source runs) | Standard library + `ctypes` only |
| Build tool | PyInstaller (build-time only) |
| Source under test | `maintenance_counter_app.py`, `printer_core.py`, `epson_d4.py`, `model_db.py`, `eeprom_io.py`, `operations.py`, `oplog.py`, `gen_model_db.py` |
| Automated tests | `tests/` |

### Setup commands

```bat
python -m venv .venv
.venv\Scripts\activate
pip install pyinstaller
```

### Run the application (from source)

```bat
python maintenance_counter_app.py
```

### Run the automated tests

```bat
python -m unittest discover -s tests -v
```

### Build the binary

```bat
pyinstaller --onefile --windowed --clean --noconfirm --name MaintenanceCounterUtility --hidden-import epson_d4 --hidden-import model_db --hidden-import printer_core --hidden-import eeprom_io --hidden-import operations --hidden-import oplog maintenance_counter_app.py
```

---

## 3. Automated tests

The automated suite is run with:

```bat
python -m unittest discover -s tests -v
```

The cases below are implemented in `tests/test_operations.py` and supporting test modules. They are designed so that the safety-critical ordering (confirmations, backup-before-reset, logging) is enforced regardless of the GUI layer.

| # | Automated test | What it verifies | Module exercised |
| --- | --- | --- | --- |
| A1 | Reset blocked unless both confirmations given | A reset request is rejected unless **both** required confirmations are present: the physical-maintenance checkbox confirmation **and** the second "I accept full responsibility" confirmation. With either flag missing, the controller refuses to proceed. | `operations.py` |
| A2 | Backup runs strictly before reset | The reset safety controller takes the EEPROM backup **before** any counter write occurs. The test asserts call ordering so that no reset can happen before a successful backup (or an explicit override). | `operations.py`, `eeprom_io.py` |
| A3 | Backup failure stops reset | When the automatic backup fails and no override is supplied, the reset is aborted and no counter is modified. | `operations.py`, `eeprom_io.py` |
| A4 | Backup-failure override proceeds | When the backup fails **and** the operator has explicitly supplied the override, the controller proceeds with the reset. The override path is recorded as a warning condition. | `operations.py` |
| A5 | Reset attempt and success are logged | A reset attempt is logged, and on success a corresponding success entry is recorded. Logs capture model, transport, counter values, backup path, confirmation flags and errors — but **not** serial numbers or personal data. | `operations.py`, `oplog.py` |
| A6 | Low-counter detection | The controller detects and flags low counter values so that a caution can be raised (a low reading may indicate the counters do not need resetting). | `operations.py` |
| A7 | `model_db` resolves L3250 | The embedded model database resolves the verified model `L3250` to a valid record. | `model_db.py` |
| A8 | Model count > 50 | The embedded database exposes more than 50 compatible models (the shipped database contains 108). | `model_db.py` |

### Expected automated outcome

All of the above cases should report `ok`. A failure in A1–A5 is treated as a **safety-blocking** defect and must halt release: these cases guarantee that confirmations are mandatory, that a backup is taken before any write, that a failed backup stops the reset unless explicitly overridden, and that operations are logged without personal data.

---

## 4. Manual UI test cases

These behaviours depend on the GUI, on operator interaction, on packaging, or on observing that nothing is transmitted off the device, and are therefore verified manually. Record results in the **Actual result** and **Pass/Fail** columns during each test pass.

| Test ID | Test name | Preconditions | Steps | Expected result | Actual result | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- |
| M01 | Terms gate appears on first run | Fresh install / first launch with no prior acceptance stored | 1. Launch `MaintenanceCounterUtility.exe` for the first time. 2. Observe the initial screen. | The first-run Terms-of-Use acceptance gate is shown and must be accepted before any other function is reachable. The application does not expose reset functionality until terms are accepted. | _(placeholder)_ | _(placeholder)_ |
| M02 | Reset "Continue" disabled until physical-maintenance checkbox ticked | Terms accepted; a compatible printer connected via USB; reset dialog reached | 1. Open the reset flow. 2. Leave the checkbox "I confirm that the waste ink pad has been inspected, cleaned, replaced, or an external waste ink tank is installed and functioning" unticked. 3. Observe the Continue control. 4. Tick the checkbox. | While the physical-maintenance checkbox is unticked, the Continue control is disabled. After ticking it, the control becomes available. | _(placeholder)_ | _(placeholder)_ |
| M03 | Mandatory 8-point warning appears before reset | Terms accepted; reset flow started | 1. Proceed through the reset flow toward the reset action. 2. Observe the pre-reset warning. | The mandatory pre-reset warning is shown and lists 8 points before any reset can proceed. | _(placeholder)_ | _(placeholder)_ |
| M04 | Second confirmation required | Terms accepted; physical-maintenance checkbox ticked; 8-point warning shown | 1. Continue past the first checkbox. 2. Attempt to perform the reset without the second confirmation. 3. Provide the second confirmation "I understand this action modifies printer maintenance counters and I accept full responsibility for ensuring physical maintenance has been completed". | The reset cannot proceed until the second confirmation is given. Once both confirmations are present, the reset is allowed to continue. | _(placeholder)_ | _(placeholder)_ |
| M05 | Backup path shown after reset | Terms accepted; both confirmations given; backup succeeds | 1. Complete a reset on a connected printer (or a supported test path). 2. Observe the result screen. | An automatic EEPROM backup is taken before the reset, and the backup file path is displayed to the operator after the reset completes. | _(placeholder)_ | _(placeholder)_ |
| M06 | Low-counter caution appears for low values | A printer/state reporting low counter values | 1. Read the counters for a printer that reports low values. 2. Observe any caution shown. | A low-counter caution is displayed, indicating the counters may not need resetting. | _(placeholder)_ | _(placeholder)_ |
| M07 | Non-affiliation notice visible in footer and About | Application launched | 1. Inspect the main window footer. 2. Open the About dialog. | The non-affiliation notice is visible in both the footer and the About dialog, as plain-text compatibility wording: "This project is not affiliated with, endorsed by, sponsored by, or approved by Epson. Epson is a trademark of its respective owner. Product names are used only to describe compatibility with selected printer models." No Epson logos or artwork are present. | _(placeholder)_ | _(placeholder)_ |
| M08 | Experimental-model caution appears | A model other than L3250/L3251/L3253/L3255 selected | 1. Select an Experimental (EUPL-derived, not hardware-verified) model. 2. Observe the model status shown. | A caution is shown indicating the model is Experimental and has not been verified on hardware by this project. Verified status appears only for L3250 / L3251 / L3253 / L3255. | _(placeholder)_ | _(placeholder)_ |
| M09 | Restore from backup works | A previously created backup file exists | 1. Open the restore-from-backup function. 2. Select a valid backup file. 3. Apply the restore to the connected printer. | The restore completes and the previously backed-up counter values are written back. The operation is logged. | _(placeholder)_ | _(placeholder)_ |
| M10 | No network or telemetry call | Network monitoring tool available (e.g. OS firewall log or a local packet/connection monitor) | 1. Launch the utility and exercise read, backup, reset, and restore flows while monitoring outbound connections. | No outbound network connections are made; no telemetry is transmitted. Nothing is sent off the device. | _(placeholder)_ | _(placeholder)_ |
| M11 | Packaged binary includes required documents | A built `MaintenanceCounterUtility.exe` and its release package | 1. Inspect the release package. 2. Confirm the presence of `LICENSE.txt` (EUPL-1.2). 3. Confirm corresponding source code is published alongside the binary. 4. Confirm the non-affiliation notice is present in distributed documentation. | The release includes `LICENSE.txt`, the corresponding source code is published (EUPL-1.2 copyleft requires source with any binary release), and the non-affiliation notice is present. | _(placeholder)_ | _(placeholder)_ |

---

## 5. Power-cycle reminder check (manual, supplementary)

After any successful reset, the application should display a reminder to power-cycle the printer. Verify during M05 that this reminder is shown. Record any deviation as a defect.

---

## 6. Release gating

A release is **maintenance-ready** only when:

- All automated cases A1–A8 report `ok` (A1–A5 are safety-blocking).
- All manual cases M01–M11 are marked **Pass**.
- The embedded model database is the EUPL-derived 108-model database only. No unlicensed, proprietary, vendor, or reverse-engineered vendor database is present. The previously removed larger unlicensed database must not be reintroduced.
- The non-affiliation notice and `LICENSE.txt` are present in the package, and corresponding source code is published with the binary.

This plan is compliance-oriented and risk-reduced; it is **not legal advice**, and laws vary by jurisdiction. Any paid distribution **requires legal review before paid distribution** by a qualified local IP/product lawyer.
