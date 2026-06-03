# Final Compliance Report

_Project: Waste Ink Maintenance Counter Utility (v1.0.0). Date: June 2026._

## 1. Executive Summary

This work moved the project to an independent code base, an embedded EUPL-derived
model database, neutral (non-Epson) branding, and a maintenance-first reset flow
with mandatory acknowledgements, automatic pre-reset backup, local logging, and a
full open-source documentation set.

- This work reduces compliance and user-safety risk but does not constitute legal advice.
- Paid distribution should still be reviewed by a qualified local IP/product lawyer.
- The project should not be described as fully legal or risk-free; remaining risks are listed in sections 15–16.

## 2. Scope of Review

- Source code (entry, backend, USB/D4 layer, embedded database, backup/restore, reset controller, logging).
- UI reset flow (terms gate, warning, acknowledgement checkbox, second confirmation, low-counter caution).
- Documentation and licensing files.
- Supported-model data and its provenance.
- Build/packaging scripts and binary distribution contents.
- Legacy files from earlier ez-reset-based versions.
- Release readiness.

## 3. Files Changed

| File | Change Summary | Reason |
|------|----------------|--------|
| maintenance_counter_app.py | New neutral-named GUI entry (replaces epson_waste_reset.py); non-affiliation footer + About; mandatory warning + physical-maintenance checkbox + second confirmation; low-counter caution; maintenance-focused wording; wired to operations controller | Trademark/affiliation, anti-circumvention wording, reset-safety flow |
| printer_core.py | Backend over independent D4 stack + embedded DB; status/waste/usage; verified vs experimental flag | Independent implementation |
| epson_d4.py | Independent USB + IEEE-1284.4 + control-channel layer (ctypes; no third-party code) | Remove unlicensed-code dependency |
| model_db.py | Embedded model database (108 models), EUPL-derived + verified L3250 family; usage multi-group fix | License-clean, single-file distribution |
| eeprom_io.py | Self-contained backup/restore + app/data/backups path helpers | Decouple from removed modules |
| gen_model_db.py | Build-time generator from EUPL epson_print_conf data + verified L3250 | Documented provenance |
| LICENSE.txt | EUPL-1.2 text with project + upstream attribution header | EUPL compliance |

## 4. New Files Added

| File | Purpose |
|------|---------|
| operations.py | GUI-agnostic, unit-testable reset controller (confirmations, backup-before-reset, fail-stop, logging, low-counter) |
| oplog.py | Local operation logging (no serial/PII; no network) |
| tests/test_operations.py | Automated tests for the safety controller + model DB |
| README.md | Project overview, non-affiliation, supported models, build/usage, legal caution |
| NOTICE.md | Attribution, trademark, third-party components, data provenance |
| DISCLAIMER.md | As-is, no warranty, user responsibility, jurisdiction caution |
| CONTRIBUTING.md | "How to add and verify a new printer model legitimately" |
| PRIVACY.md | No telemetry; local logs/backups; what is/ isn't collected |
| TERMS_OF_USE.md | Use-at-own-risk terms that defer to EUPL for licensed code |
| RELEASE_CHECKLIST.md | Pre-release verification checklist |
| DATA_PROVENANCE.md | Model-data sources, licensing, verification status |
| SUPPORTED_MODELS.md | Per-model operations + verification status |
| TEST_PLAN.md | Automated + manual test cases |
| FINAL_COMPLIANCE_REPORT.md | This report |
| .gitignore | Exclude build/venv/clones/local runtime data |

## 5. UI/UX Safety Controls Implemented

- [x] Non-affiliation notice visible in app — Status: Complete — Evidence: `maintenance_counter_app.py` footer label + `show_about()` (NON_AFFILIATION).
- [x] No Epson logo/artwork used — Status: Complete — Evidence: text-only UI; no image assets in repo.
- [x] Reset warning appears before reset — Status: Complete — Evidence: `reset_consent()` 8-point `RESET_WARNING`.
- [x] Physical maintenance checkbox required — Status: Complete — Evidence: `reset_consent()` `ACK_PHYSICAL` checkbox.
- [x] Reset/Continue disabled until acknowledgement — Status: Complete — Evidence: `reset_consent()` `cont_btn.state(["disabled"])` until checkbox set.
- [x] Second confirmation required — Status: Complete — Evidence: `reset_consent()` `messagebox.askyesno(ACK_RESPONSIBILITY)`.
- [x] Backup before reset by default — Status: Complete — Evidence: `operations.perform_reset()` calls `eeprom_io.backup()` before `backend.reset()`; test `test_backup_runs_before_reset`.
- [x] Reset stops or warns if backup fails — Status: Complete — Evidence: `operations.BackupFailed` + GUI override prompt; test `test_backup_failure_stops_reset`.
- [x] Operation logs created — Status: Complete — Evidence: `oplog.log_event()`; events in `operations.perform_reset()`.
- [x] Low-counter warning implemented — Status: Complete — Evidence: `operations.counters_are_low()` + GUI caution in `reset_action()`.
- [x] Offline warnings available — Status: Complete — Evidence: all warnings are in-app strings + packaged docs.

## 6. Documentation Compliance

- [x] README.md — Status: Complete — Notes: created via doc workflow.
- [x] LICENSE present and EUPL-compatible — Status: Complete — Notes: LICENSE.txt (EUPL-1.2).
- [x] NOTICE.md — Status: Complete.
- [x] DISCLAIMER.md — Status: Complete.
- [x] CONTRIBUTING.md — Status: Complete.
- [x] PRIVACY.md — Status: Complete.
- [x] TERMS_OF_USE.md — Status: Complete.
- [x] RELEASE_CHECKLIST.md — Status: Complete.
- [x] DATA_PROVENANCE.md — Status: Complete.
- [x] SUPPORTED_MODELS.md — Status: Complete.
- [x] TEST_PLAN.md — Status: Complete.

Remaining gaps: SUPPORTED_MODELS.md lists ~104 models as "Experimental" (EUPL-derived, not verified by this project on hardware); broader verification is an ongoing contributor task.

## 7. Licensing and EUPL Readiness

- Source distribution is ready (8 source modules + tests + docs; no external runtime dependencies).
- The EUPL-1.2 licence text is included (LICENSE.txt).
- Additional terms (TERMS_OF_USE.md) explicitly defer to the EUPL for licensed code and do not restrict EUPL freedoms.
- Third-party provenance is documented (NOTICE.md, DATA_PROVENANCE.md): model data derived from epson_print_conf (EUPL-1.2); build tool PyInstaller; Python standard library; no proprietary code/data.
- The binary distribution folder includes the licence and notice files.

"Distribution under EUPL requires publishing the corresponding source code with the binary release. This report does not replace legal review."

## 8. Trademark and Branding Review

- App name reviewed: "Waste Ink Maintenance Counter Utility" (neutral; no "Epson").
- Window title reviewed: same neutral title.
- About screen reviewed: states "not an official Epson product" + non-affiliation notice.
- README wording reviewed: includes non-affiliation notice.
- Packaging metadata reviewed: executable `MaintenanceCounterUtility.exe` (no "Epson").
- Epson logo/artwork check: none present (text-only UI).
- Non-affiliation wording check: present in app footer, About, README, NOTICE.

Remaining trademark risk: the word "Epson" appears as plain-text compatibility wording and as the printer-reported model string (e.g. "L3250 Series"). This is nominative use; marketing copy should remain factual and avoid implying endorsement. Risk reduced, not eliminated.

## 9. Anti-Circumvention Risk Mitigation

- Risky/ambiguous wording removed; replaced with maintenance-oriented wording.
- Reset is framed as a maintenance-support step that requires explicit acknowledgement that physical pad/tank service was completed.
- Documentation states that laws vary by jurisdiction and that paid distribution requires legal review before paid distribution.

| Risky Wording | Replacement Wording |
|---------------|---------------------|
| "Reset tool" / "EpsonWasteReset" | "Waste Ink Maintenance Counter Utility" |
| "Reset Waste Counters" (button) | "Reset Maintenance Counters" (after maintenance acknowledgement) |
| "clears the Service Required error" | "maintenance-support step after physical pad/tank service" |
| implied "fix/avoid service" framing | "does not perform physical maintenance; not a way to avoid service requirements" |
| (implied open-ended-printing framing) | "software counter reset does not replace physical maintenance" |

Risk reduced, not eliminated.

## 10. Liability and User Safety Controls

- Physical-maintenance warning (8 points) + mandatory acknowledgement checkbox + second confirmation.
- Automatic EEPROM backup before every reset; reset stops on backup failure unless explicitly overridden.
- Local operation logs (model, counters, backup path, confirmation flags, errors; no serial/PII).
- Restore-from-backup available and documented.
- Low-counter caution.
- No-warranty disclaimer and explicit user-responsibility language in app + docs.

Remaining product-liability risk: misuse (resetting without real service) can still cause ink overflow/leakage or hardware damage; experimental-model data is unverified; outcomes vary by printer/firmware. Risk reduced, not eliminated.

## 11. Data Provenance Review

| Data/File | Source/Provenance | License/Permission | Status | Notes |
|-----------|-------------------|--------------------|--------|-------|
| model_db.py (L3250/L3251/L3253/L3255) | Hardware-verified values | Facts verified independently | Verified | Read/reset confirmed on real hardware (June 2026) |
| model_db.py (other ~104 models) | Converted from epson_print_conf | EUPL-1.2 (c) Ircama | Experimental | Not verified on hardware by this project |
| gen_model_db.py | Converter script | This project (EUPL) | Included | Documents conversion; needs epson_print_conf clone to regenerate |
| Previous large database | ez-reset / unlicensed | No usable licence | Removed | Deleted; must not be used |
| ez-reset/ clone | Third-party, unlicensed | None | Removed | Deleted from working tree |

No proprietary/unlicensed database is bundled in the source or the binary.

## 12. Legacy File Cleanup

| File | Used by App? | Included in Build? | Risk Level | Action Taken |
|------|--------------|--------------------|------------|--------------|
| device_db.py | No | No | High (imported unlicensed ez_reset) | Removed |
| backends.py | No | No | High (imported unlicensed ez_reset) | Removed |
| epc_merge.py | No | No | High (imported unlicensed ez_reset) | Removed |
| usb_read_waste.py / usb_reset_waste.py / probe_info.py | No | No | High (imported unlicensed ez_reset) | Removed |
| usb_probe.py / usb_winusb_probe.py / usb_if2_char.py / probe_eeprom.py | No | No | Medium (dev scratch) | Removed |
| epson_waste_reset.py + EpsonWasteReset.spec | Superseded | No | Medium (old "Epson" naming) | Removed |
| ez-reset/ clone | No | No | High (unlicensed) | Removed |
| reinkpy/ clone | No | No | Medium (unused) | Removed |
| epson_print_conf/ clone | Build-time only (gen_model_db) | No | Low (EUPL) | Kept locally, git-ignored |

## 13. Packaging and Binary Distribution Readiness

- Required docs included with the binary: README, LICENSE, NOTICE, DISCLAIMER, PRIVACY, TERMS_OF_USE, SUPPORTED_MODELS, DATA_PROVENANCE (copied into `dist/`).
- Risky files excluded: no clones, no unlicensed database, no logs/backups/keys in the binary build.
- Source release prepared alongside the binary (all source modules + tests + docs).
- Build command documented and reproducible (below). Version visible in About + footer.
- Release checklist available (RELEASE_CHECKLIST.md).

Recommended build commands:
```
python -m venv .venv
.venv\Scripts\activate
pip install pyinstaller
python -m unittest discover -s tests -v
pyinstaller --onefile --windowed --clean --noconfirm --name MaintenanceCounterUtility ^
  --hidden-import epson_d4 --hidden-import model_db --hidden-import printer_core ^
  --hidden-import eeprom_io --hidden-import operations --hidden-import oplog ^
  maintenance_counter_app.py
```

## 14. Tests Performed

| Test ID | Test Description | Result | Evidence/Notes |
|---------|------------------|--------|----------------|
| T1 | Reset blocked unless both confirmations given | Pass | test_requires_both_confirmations |
| T2 | Backup runs strictly before reset | Pass | test_backup_runs_before_reset (order == [backup, reset]) |
| T3 | Backup failure stops reset | Pass | test_backup_failure_stops_reset |
| T4 | Backup-failure override proceeds | Pass | test_backup_failure_override_proceeds |
| T5 | Reset attempt + success logged | Pass | test_logging_attempt_and_success |
| T6 | Low-counter detection | Pass | test_low_counter_detection |
| T7 | Model DB resolves L3250 | Pass | test_resolve_l3250 |
| T8 | Model count > 50 | Pass | test_model_count_nonzero |
| H1 | Independent stack reads real L3250 (status/waste/usage) | Pass | `--check`: IDLE/NONE, 42/0/10, pages 59, scans 88 |
| H2 | Frozen exe reads real L3250 | Pass | `MaintenanceCounterUtility.exe --check` |
| H3 | GUI constructs + first refresh, closes cleanly | Pass | EWR_GUI_SELFTEST run |
| M* | Manual UI behaviours (warning/checkbox/2nd confirm/low-counter/About) | Manual | See TEST_PLAN.md (require human clicks) |

## 15. Remaining Legal Risks

- Anti-circumvention laws may vary by country and remain an unsettled area for counter resets.
- Repair / right-to-repair exceptions may not apply in every jurisdiction.
- Trademark use still requires careful, factual marketing that avoids implying endorsement.
- Product-liability risk remains if the reset is misused without physical maintenance.
- Warranty implications may vary by region and printer.
- Paid distribution should be reviewed by a qualified local IP/product lawyer. This is not legal advice; laws vary by jurisdiction.

## 16. Remaining Technical Risks

- Unsupported models (only 108 are in the database; many printers are not covered).
- Failed backups (rare) would block a reset by design (override available with warning).
- Printer communication errors / USB driver variations.
- Firmware variations may change behaviour or block access.
- Incorrect model detection if a printer reports an unexpected MDL string.
- Restore depends on a valid prior backup; partial writes are possible on communication errors.
- User misuse (resetting without service).
- Log-privacy considerations (model + counters are logged locally; no serial/PII).

## 17. Commercial Distribution Recommendations

- Form a legal entity before selling.
- Publish the corresponding source with every binary release (EUPL requirement).
- Keep any paid offer positioned as convenience/support/build service, not proprietary access to the code.
- Avoid official Epson-like branding; do not use Epson logos.
- Obtain local legal review before selling in the US/EU or internationally (anti-circumvention, repair, consumer protection, trademark, product liability).
- Maintain an issue tracker and a clear support policy.
- Keep model-support evidence (verification logs/notes).
- Consider insurance or a product-liability review if revenue grows.

## 18. Final Acceptance Checklist

- [x] Source code ready for publication
- [x] Binary release includes required documents
- [x] EUPL license included
- [x] No proprietary/unlicensed database bundled
- [x] No Epson logo/artwork included
- [x] Non-affiliation notice visible
- [x] Reset cannot proceed without acknowledgement
- [x] Backup behavior implemented/tested
- [x] Logs implemented/tested
- [x] Supported models list accurate
- [x] Data provenance documented
- [x] Release checklist completed
- [x] Legal review still recommended before paid distribution

## 19. Final Conclusion

The project is now more compliance-oriented and safer for responsible maintenance
use. However, this does not eliminate all legal or product-liability risk. The
project should still receive qualified legal review before paid distribution,
especially for jurisdictions with anti-circumvention, repair, consumer protection,
trademark, and product liability rules.
