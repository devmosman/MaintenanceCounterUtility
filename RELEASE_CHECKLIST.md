# Release Checklist — Waste Ink Maintenance Counter Utility

**Product:** Waste Ink Maintenance Counter Utility
**Executable:** `MaintenanceCounterUtility.exe`
**Version:** 1.0.0
**License:** EUPL-1.2 (`LICENSE.txt`)
**Platform:** Windows 64-bit, USB connection only

This checklist is **maintenance-focused** and **compliance-oriented**. It is **not legal advice**. Anti-circumvention, repair, warranty, consumer-protection, product-liability and trademark laws **vary by jurisdiction**. Any paid distribution **requires legal review before paid distribution** by a qualified local IP/product lawyer.

> **Non-affiliation notice:** This project is not affiliated with, endorsed by, sponsored by, or approved by Epson. Epson is a trademark of its respective owner. Product names are used only to describe compatibility with selected printer models.

---

## 1. Source code and licensing (EUPL copyleft)

- [ ] Corresponding source code is published with the binary release (EUPL-1.2 copyleft requirement: source MUST accompany any binary release).
- [ ] All source files are present in the published tree: `maintenance_counter_app.py`, `printer_core.py`, `epson_d4.py`, `model_db.py`, `eeprom_io.py`, `operations.py`, `oplog.py`, `gen_model_db.py`, and the `tests/` directory.
- [ ] `LICENSE.txt` (EUPL-1.2) is included in the repository and in the packaged binary.
- [ ] Third-party license review is complete and documented.
- [ ] Attribution recorded for model-database content derived from `epson_print_conf` (EUPL-1.2, Copyright (c) 2024-2025 Ircama).
- [ ] `epson_d4.py` confirmed to be an independent USB + IEEE-1284.4 (D4) + control-channel layer written from public specifications and documented protocol/API facts — not copied from any third party.

## 2. Database and artifact hygiene

- [ ] Embedded model database contains exactly the 108 compatible models and is built only from EUPL-derived data plus the on-hardware-verified L3250/L3251/L3253/L3255 family.
- [ ] No proprietary, vendor, or unlicensed database is included.
- [ ] No reverse-engineered vendor database is included.
- [ ] The previously removed larger unlicensed database is confirmed absent from the source tree and the build artifacts.
- [ ] No unused legacy files and no legally risky files are present in the build artifacts.
- [ ] No Epson logo, artwork, or misleading branding appears anywhere in the source, the app UI, the icon, the installer, or marketing text. Any mention of Epson is plain-text compatibility wording only.

## 3. Notices and disclosures

- [ ] Non-affiliation notice (verbatim, above) is visible **in the app** (e.g., About / first-run screen).
- [ ] Non-affiliation notice (verbatim, above) is visible **in the README**.
- [ ] `NOTICE`, `DISCLAIMER`, `PRIVACY`, and `TERMS_OF_USE` documents are present and current.
- [ ] Documentation states clearly that the utility performs **no physical maintenance** and is **not** a way to avoid service requirements.

## 4. Safety behaviour — tested before release

- [ ] First-run Terms-of-Use acceptance is shown and required.
- [ ] Mandatory pre-reset warning (all 8 points) is displayed and tested.
- [ ] Required checkbox tested: "I confirm that the waste ink pad has been inspected, cleaned, replaced, or an external waste ink tank is installed and functioning."
- [ ] Required second confirmation tested: "I understand this action modifies printer maintenance counters and I accept full responsibility for ensuring physical maintenance has been completed."
- [ ] Automatic EEPROM backup is taken **before every reset** — tested.
- [ ] Backup-failure-stops-reset behaviour tested: the reset halts if the backup fails, unless the user explicitly overrides with a warning.
- [ ] Restore-from-backup is documented and tested.
- [ ] Local operation log creation tested. Logs record model, transport, counter values, backup path, confirmation flags, and errors — and do **not** record serial numbers or personal data.
- [ ] Low-counter caution is displayed and tested.
- [ ] Power-cycle reminder is shown after a reset.
- [ ] Confirmed: no telemetry; nothing is transmitted off the device.

## 5. Models, provenance, and documentation accuracy

- [ ] `SUPPORTED_MODELS` list is accurate (108 compatible models).
- [ ] Verification status is correct: L3250 / L3251 / L3253 / L3255 = **Verified on hardware (June 2026)**; all other models = **Experimental (EUPL-derived data, not verified by this project on hardware)**.
- [ ] `DATA_PROVENANCE.md` is updated and reflects the current database sources and verification status.
- [ ] Build instructions and reproducibility are documented (commands below).

## 6. Build and reproducibility reference

- [ ] Runtime dependencies confirmed: **none** (Python standard library + `ctypes`). Build dependency: **PyInstaller only**.

```text
Create venv:          python -m venv .venv
Activate (Windows):   .venv\Scripts\activate
Install build tool:   pip install pyinstaller
Run app:              python maintenance_counter_app.py
Run tests:            python -m unittest discover -s tests -v
Build binary:         pyinstaller --onefile --windowed --clean --noconfirm --name MaintenanceCounterUtility --hidden-import epson_d4 --hidden-import model_db --hidden-import printer_core --hidden-import eeprom_io --hidden-import operations --hidden-import oplog maintenance_counter_app.py
```

- [ ] Automated test suite passes (`python -m unittest discover -s tests -v`).

## 7. Packaging contents

- [ ] The packaged binary ships with all of: `README`, `LICENSE`, `NOTICE`, `DISCLAIMER`, `PRIVACY`, `TERMS_OF_USE`, `SUPPORTED_MODELS`, `DATA_PROVENANCE`.

## 8. Legal review and release notes

- [ ] Legal review completed **before paid distribution** by a qualified local IP/product lawyer. (This is **not legal advice**; **laws vary by jurisdiction**, covering anti-circumvention, repair, warranty, consumer-protection, product-liability, and trademark.)
- [ ] Release notes include a legal caution: this is a **risk-reduced**, **compliance-oriented**, **maintenance-focused** utility; it is **not legal advice**; **laws vary by jurisdiction**; paid distribution **requires legal review before paid distribution**.
- [ ] Release notes include the safety warning: the utility reads approximate waste-ink maintenance counters and can reset them **only after** the owner has physically inspected, cleaned, replaced, or redirected the waste-ink pad/tank; it performs no physical maintenance.
- [ ] Release notes include the verbatim non-affiliation notice.
