# Changelog

All notable changes to this project are documented here.
This project follows semantic versioning where practical.

## [1.0.0] — 2026-06-04

First public release.

### Added
- Independent USB + IEEE-1284.4 (D4) + control-channel stack (`epson_d4.py`),
  written from public specifications and documented protocol/API facts.
- Embedded model database (`model_db.py`, 108 compatible models); build-time
  generator `gen_model_db.py`.
- Read approximate waste-ink maintenance counters and usage counters
  (printed pages, scans, cleaning cycles) over USB.
- Automatic EEPROM backup before every reset, with restore-from-backup.
- Maintenance-focused reset safety flow: first-run Terms acceptance, mandatory
  pre-reset warning, required physical-maintenance acknowledgement checkbox,
  required second confirmation, and a low-counter caution.
- Local operation logging (no serial numbers, no personal data, no telemetry).
- tkinter GUI with non-affiliation notice and About dialog.
- Automated tests (`tests/`) for the reset safety controller and model database.
- Full documentation set (README, NOTICE, DISCLAIMER, CONTRIBUTING, PRIVACY,
  TERMS_OF_USE, SUPPORTED_MODELS, DATA_PROVENANCE, RELEASE_CHECKLIST, TEST_PLAN).

### Verification status
- Verified on hardware (June 2026): `L3250`, `L3251`, `L3253`, `L3255`.
- All other models are experimental (EUPL-derived data, not verified on
  hardware by this project).

### Licensing
- Licensed under EUPL-1.2. Corresponding source is published with the release.

### Notes
- Not affiliated with Epson; "Epson" and model names are trademarks of their
  respective owner and are used only for compatibility identification.
- This is not legal advice; laws vary by jurisdiction.
