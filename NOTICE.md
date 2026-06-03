# NOTICE

This file accompanies the **Waste Ink Maintenance Counter Utility**
(executable: `MaintenanceCounterUtility.exe`, version 1.0.0). It records
attribution, licensing, third-party components, and data-source provenance.

This document is **not legal advice**. Anti-circumvention, repair, warranty,
consumer-protection, product-liability, and trademark laws **vary by
jurisdiction**. This utility is provided as a maintenance-focused,
compliance-oriented tool; it is risk-reduced, not risk-free. Any paid
distribution **requires legal review before paid distribution** by a qualified
local intellectual-property / product lawyer.

---

## 1. Non-Affiliation and Trademark Notice

This project is not affiliated with, endorsed by, sponsored by, or approved by
Epson. Epson is a trademark of its respective owner. Product names are used
only to describe compatibility with selected printer models.

All other product names, brand names, and trademarks referenced anywhere in
this project remain the property of their respective owners. Their use is for
plain-text compatibility identification only and does not imply any
affiliation, endorsement, or sponsorship.

---

## 2. No Logos or Artwork Included

This project includes **no Epson logo, no Epson artwork, and no vendor-supplied
graphics or branding of any kind**. Where a manufacturer or product name
appears, it appears only as plain text for the purpose of identifying which
printer models the utility is compatible with.

Product names are used **only for compatibility identification**. They do not
indicate that this utility originates from, is licensed by, or is in any way
connected to the named manufacturer.

---

## 3. License of This Project

This project is licensed under the **European Union Public Licence v1.2
(EUPL-1.2)**. The full text is in `LICENSE.txt`.

The EUPL-1.2 is a copyleft licence. **The corresponding source code MUST be
published with any binary release.** If you distribute
`MaintenanceCounterUtility.exe` (or any modified build), you must make the
corresponding source code available under the same terms.

Source files covered by this licence include:

- `maintenance_counter_app.py` (entry point / GUI)
- `printer_core.py` (backend)
- `epson_d4.py` (independent USB + IEEE-1284.4 (D4) + control-channel layer,
  written from public specifications and documented protocol/API facts — not
  copied from any third party)
- `model_db.py` (embedded model database)
- `eeprom_io.py` (backup/restore and paths)
- `operations.py` (reset safety controller)
- `oplog.py` (local operation logging)
- `gen_model_db.py` (build-time database generator)
- the automated tests in `tests/`

---

## 4. Third-Party Components and Licenses

### 4.1 Runtime dependencies — NONE

The application has **no runtime dependencies** beyond what ships with the
Python interpreter. It uses only the **Python standard library** and `ctypes`.
There are no bundled third-party runtime libraries.

### 4.2 Python Standard Library

The application relies on the **Python standard library**, which is
distributed under the **Python Software Foundation License (PSF License)**.
The standard library is the property of the Python Software Foundation and its
contributors.

### 4.3 Build dependency — PyInstaller

The only build-time dependency is **PyInstaller**, used to produce the
`--onefile --windowed` binary. PyInstaller is distributed under its own
license (the **GNU General Public License with a special bootloader
exception**, which permits using the PyInstaller bootloader to package and
distribute applications regardless of their own license). PyInstaller is the
property of its respective authors and contributors.

PyInstaller is required only to build the binary; it is **not** required to run
the application from source, and **no** PyInstaller source code is included in
this project's repository.

---

## 5. Data-Source Provenance Statement

The embedded model database contains **108 compatible models** and is embedded
directly in the binary. Its provenance is as follows:

- **Converted from `epson_print_conf`**, which is licensed under
  **EUPL-1.2**, Copyright (c) 2024-2025 Ircama. The model data used by this
  project was converted from that EUPL-licensed source under the terms of the
  EUPL-1.2.
- **Plus the L3250 / L3251 / L3253 / L3255 family**, which was **verified on
  real hardware** by this project.

There is **no unlicensed database**, **no proprietary or vendor data**, and
**no reverse-engineered vendor database** in this project. A previously used
larger unlicensed database has been **removed** and must not be reintroduced or
used.

### 5.1 Verification status

| Models | Status |
|---|---|
| L3250 / L3251 / L3253 / L3255 | **Verified on hardware** (June 2026) |
| All other models | **Experimental** — EUPL-derived data, **not** verified by this project on hardware |

Experimental entries are provided on a best-effort, maintenance-focused basis.
Counter readings and addresses for experimental models are approximate and have
not been confirmed on physical hardware by this project.

### 5.2 Requirement for future model data

Any supported-model data added to this project in the future **must come only
from legally usable sources or from independent verification on hardware**.
Acceptable sources are limited to:

- data that is itself available under a license compatible with EUPL-1.2
  (with proper attribution recorded in this file), or
- values independently verified on real hardware by this project.

Proprietary, vendor-confidential, or unlicensed data **must not** be added.

---

## 6. Purpose, Scope, and Safety Statement

The **Waste Ink Maintenance Counter Utility** is an open-source,
maintenance-focused utility for selected compatible inkjet printers on
**Windows 64-bit over a USB connection only**. It reads approximate waste-ink
maintenance counters, creates a local backup, and can reset those counters
**only after** the owner has physically inspected, cleaned, replaced, or
redirected the waste-ink pad/tank.

The utility **performs no physical maintenance** and is **not** a way to avoid
service requirements. Resetting a counter does not address the underlying
physical condition of the waste-ink pad or tank; physical maintenance remains
the owner's responsibility.

The application includes safety behaviour intended to keep its use
maintenance-focused and compliance-oriented:

- first-run Terms-of-Use acceptance;
- a mandatory pre-reset warning (8 points);
- a required checkbox: *"I confirm that the waste ink pad has been inspected,
  cleaned, replaced, or an external waste ink tank is installed and
  functioning"*;
- a required second confirmation: *"I understand this action modifies printer
  maintenance counters and I accept full responsibility for ensuring physical
  maintenance has been completed"*;
- an automatic EEPROM backup taken **before every reset** (the reset stops if
  the backup fails, unless the user explicitly overrides with a warning);
- restore-from-backup;
- local operation logs that record model, transport, counter values, backup
  path, confirmation flags, and errors, but **not** serial numbers or personal
  data;
- a low-counter caution; and
- a reminder to power-cycle the printer after a reset.

There is **no telemetry**; nothing is transmitted off the device.

---

## 7. Disclaimer

This NOTICE is provided for attribution and transparency. It is **not legal
advice**. Because anti-circumvention, repair, warranty, consumer-protection,
product-liability, and trademark laws **vary by jurisdiction**, distributing
this software — and especially any paid distribution — **requires legal review
before paid distribution** by a qualified local intellectual-property /
product lawyer.
