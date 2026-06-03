# How to add and verify a new printer model legitimately

Thank you for helping improve the **Waste Ink Maintenance Counter Utility**
(`MaintenanceCounterUtility.exe`, version 1.0.0). This project is a
maintenance-focused, open-source utility for selected compatible inkjet
printers. It reads approximate waste-ink maintenance counters, creates a local
backup, and can reset those counters **only after** the owner has physically
inspected, cleaned, replaced, or redirected the waste-ink pad/tank. The utility
performs **no** physical maintenance and is **not** a way to avoid service
requirements.

This document explains how to add and verify a new printer model in a way that
is honest, legally careful, and consistent with the project's EUPL-1.2 license.

> **This is not legal advice.** Anti-circumvention, repair, warranty,
> consumer-protection, product-liability, and trademark laws **vary by
> jurisdiction**. Nothing here guarantees any legal outcome. This project is a
> risk-reduced, compliance-oriented effort, but any paid distribution
> **requires legal review before paid distribution** by a qualified local
> IP/product lawyer.

> **Non-affiliation notice.** This project is not affiliated with, endorsed by,
> sponsored by, or approved by Epson. Epson is a trademark of its respective
> owner. Product names are used only to describe compatibility with selected
> printer models.

---

## License and data provenance context

- The project is licensed under **EUPL-1.2** (see `LICENSE.txt`).
- EUPL-1.2 is a copyleft license: the **corresponding source code MUST be
  published with any binary release**. If you build and distribute a binary,
  you must also publish the source it was built from.
- The embedded model database currently contains **108 compatible models**.
  That data was converted from **`epson_print_conf`** (EUPL-1.2, Copyright (c)
  2024-2025 Ircama), plus the **L3250 / L3251 / L3253 / L3255** family, which
  was verified on real hardware.
- There is **no** unlicensed database, **no** proprietary or vendor data, and
  **no** reverse-engineered vendor database in this project. A previous larger
  unlicensed database was removed and **must not** be reintroduced.
- **Verification status:**
  - **L3250 / L3251 / L3253 / L3255 — Verified on hardware (June 2026).**
  - **All other models — Experimental** (EUPL-derived data, *not* verified by
    this project on hardware).

When you contribute a model, you are adding to a data set that other people
will rely on while servicing their own equipment. Please be accurate and
conservative.

---

## (A) General principles

Read these before contributing any model data.

1. **Do not copy from prohibited sources.** Do **not** copy data from
   proprietary or unlicensed databases, vendor tools, or closed-source
   commercial tools **unless that data is legally licensed for
   redistribution** and that license is compatible with EUPL-1.2.
2. **Use only legitimate data sources.** Acceptable sources are:
   - data that is **legally shareable** (for example, EUPL-1.2 or otherwise
     redistribution-compatible licensed data, with attribution preserved);
   - your own **independent testing** on hardware you own or are authorized to
     service;
   - **user-submitted verification** from owners who tested their own printers;
   - other **properly licensed sources** whose terms allow redistribution under
     this project's license.
3. **Certify your data.** Every contributor **must certify** that the submitted
   data is original (produced by their own independent testing) or otherwise
   legally shareable, and that it was **not** taken from a proprietary,
   unlicensed, or redistribution-incompatible source.
4. **Preserve attribution.** If data derives from a licensed upstream source
   (such as `epson_print_conf`), keep the required copyright and license notices
   and record the provenance in `DATA_PROVENANCE.md`.
5. **No personal data.** Do not submit serial numbers, names, or other personal
   data. The application's local operation logs already exclude serial numbers
   and personal data, and contributions must do the same.
6. **Be honest about verification.** Only mark a model as **Verified on
   hardware** if it was actually tested on real hardware as described below.
   Everything else stays **Experimental**.

---

## (B) Required verification data per model

When you submit a model, include the following fields. Use plain text and omit
anything you cannot confirm rather than guessing.

| Field | Description |
|---|---|
| **Exact model** | The precise model designation (e.g. `L3250`). No abbreviations. |
| **Region variant** | The regional/market variant, if the model has one. |
| **Connection method** | How the printer was connected. This project supports **Windows 64-bit, USB connection only.** |
| **Firmware version** | The printer firmware version, if available. |
| **OS** | The operating system used for the test (Windows 64-bit). |
| **Counter read result** | What the approximate waste-ink maintenance counter read returned (success/failure and observed values). |
| **Reset test result** | Whether the counter reset completed as expected after physical maintenance. |
| **Backup created before test** | Confirmation that an automatic EEPROM backup was created **before** the reset, and the local backup path. |
| **User confirmation of physical pad/tank service** | Confirmation that the waste-ink pad/tank was physically inspected, cleaned, replaced, or an external waste-ink tank was installed and is functioning. |
| **Date** | The date of the verification test. |
| **Contributor handle or anonymous verification ID** | Your handle, or an anonymous verification ID. Do not include personal data. |
| **Evidence / notes** | Relevant notes and evidence, **with no personal data and no serial numbers**. |

---

## (C) Model verification checklist

A model may only be promoted from **Experimental** to **Verified on hardware**
when **every** item below is satisfied. Copy this checklist into your pull
request and tick each box.

- [ ] **Model identified exactly** (exact model and region variant recorded).
- [ ] **No proprietary or unlicensed source used** for the data.
- [ ] **Counters read** successfully via the utility.
- [ ] **Backup created** automatically before any reset (reset stops if the
      backup fails, unless explicitly overridden with a warning).
- [ ] **Physical maintenance confirmed** — the waste-ink pad/tank was inspected,
      cleaned, replaced, or an external waste-ink tank was installed and is
      functioning.
- [ ] **Reset tested** only after physical maintenance was confirmed, with both
      required confirmations and the mandatory pre-reset warning acknowledged.
- [ ] **Printer restarted** (power-cycled) after the reset, as the app reminds.
- [ ] **Counter re-read verified** after the restart to confirm the expected
      result.
- [ ] **Logs reviewed** — local operation logs reviewed (they record model,
      transport, counter values, backup path, confirmation flags, and errors,
      but **not** serial numbers or personal data).
- [ ] **Docs updated** (`SUPPORTED_MODELS.md` and any related notes).
- [ ] **`DATA_PROVENANCE.md` updated** to record the source and license of the
      data and the verification status.

If any item cannot be honestly checked, the model remains **Experimental**.

---

## (D) Pull-request requirements

Each pull request that adds or verifies a model **must** include all of the
following:

1. **Update `SUPPORTED_MODELS.md`** — add or update the model entry, and set its
   status honestly (**Verified on hardware** only when the checklist in section
   (C) is fully satisfied; otherwise **Experimental**).
2. **Update `DATA_PROVENANCE.md`** — record where the data came from, its
   license, the required attribution (for example, EUPL-1.2 upstream such as
   `epson_print_conf`, Copyright (c) 2024-2025 Ircama, where applicable), and
   the verification status.
3. **Add test notes** — include the required verification data from section (B)
   and the completed checklist from section (C), with no personal data and no
   serial numbers.
4. **Include a no-proprietary-data certification** — add the following
   statement to the pull request:

   > I certify that the model data in this contribution is original (from my own
   > independent testing) or otherwise legally shareable, that it was **not**
   > copied from any proprietary, unlicensed, vendor, or closed-source
   > commercial source that is not licensed for redistribution under EUPL-1.2,
   > and that it contains no personal data or serial numbers.

---

## Building and testing locally

If you want to reproduce a build or run the test suite while preparing a
contribution:

```bat
:: Create a virtual environment
python -m venv .venv

:: Activate it (Windows)
.venv\Scripts\activate

:: Install the build tool (PyInstaller is the only build dependency)
pip install pyinstaller

:: Run the app
python maintenance_counter_app.py

:: Run the tests
python -m unittest discover -s tests -v

:: Build the binary
pyinstaller --onefile --windowed --clean --noconfirm --name MaintenanceCounterUtility --hidden-import epson_d4 --hidden-import model_db --hidden-import printer_core --hidden-import eeprom_io --hidden-import operations --hidden-import oplog maintenance_counter_app.py
```

The application has **no runtime dependencies** (Python standard library plus
`ctypes`); **PyInstaller is only a build dependency**.

### Where the relevant code lives

- `maintenance_counter_app.py` — entry point and GUI.
- `printer_core.py` — backend.
- `epson_d4.py` — independent USB + IEEE-1284.4 (D4) + control-channel layer,
  written from public specifications and documented protocol/API facts (not
  copied from any third party).
- `model_db.py` — embedded model database.
- `gen_model_db.py` — build-time database generator.
- `eeprom_io.py` — backup/restore and paths.
- `operations.py` — reset safety controller.
- `oplog.py` — local operation logging.
- `tests/` — automated tests.

---

## A note on responsible use

This utility exists to support honest maintenance. It does **not** perform
physical maintenance and is **not** a way to avoid service requirements. The
application already enforces first-run Terms-of-Use acceptance, a mandatory
pre-reset warning, a required physical-maintenance confirmation checkbox, a
required second confirmation of responsibility, an automatic pre-reset backup,
restore-from-backup, local operation logs (without serial numbers or personal
data), a low-counter caution, and a post-reset power-cycle reminder. There is
**no telemetry**; nothing is transmitted off the device. Please keep
contributions aligned with that maintenance-focused, cautious approach.
