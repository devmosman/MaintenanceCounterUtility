# Data Provenance

This document explains the origin, licensing, and verification status of the
supported-model data bundled with the **Waste Ink Maintenance Counter Utility**
(`MaintenanceCounterUtility.exe`, version 1.0.0).

This utility is a maintenance-focused, open-source tool that reads approximate
waste-ink maintenance counters, creates a local backup, and can reset those
counters **only after** the owner has physically inspected, cleaned, replaced,
or redirected the waste-ink pad/tank. It performs no physical maintenance and is
not a substitute for service requirements.

> This document is **not legal advice**. Anti-circumvention, repair, warranty,
> consumer-protection, product-liability, and trademark laws **vary by
> jurisdiction**. Any paid distribution **requires legal review before paid
> distribution** by a qualified local IP/product lawyer.

---

## Non-affiliation notice

This project is not affiliated with, endorsed by, sponsored by, or approved by
Epson. Epson is a trademark of its respective owner. Product names are used only
to describe compatibility with selected printer models.

---

## Summary

- The supported-model database contains **108 compatible models** and is
  **embedded** in the binary.
- The data has **two provenance streams**:
  1. **EUPL-derived data** converted from
     [`epson_print_conf`](https://github.com/Ircama/epson_print_conf)
     (EUPL-1.2, Copyright (c) 2024-2025 Ircama) by the build-time generator
     `gen_model_db.py`.
  2. **Hardware-verified data** for the **L3250 / L3251 / L3253 / L3255**
     family, verified on real hardware by this project in **June 2026**.
- **No proprietary, unlicensed, vendor, or reverse-engineered vendor database is
  bundled.** A previously bundled larger unlicensed database was **removed** and
  **must not be used**.

---

## Data sources

### 1. EUPL-derived model data (`epson_print_conf`)

The majority of the embedded model entries (approximately **104** of the 108
models) were converted from the open-source project `epson_print_conf`:

- **Upstream project:** `epson_print_conf`
- **License:** EUPL-1.2 (compatible with this project's EUPL-1.2 license)
- **Copyright:** (c) 2024-2025 Ircama
- **Conversion tool:** `gen_model_db.py` (build-time database generator)
- **Output:** `model_db.py` (embedded model database)

Because both `epson_print_conf` and this project are licensed under **EUPL-1.2**,
the converted data is **license-compatible**. Under the EUPL-1.2 copyleft
obligation, the **corresponding source code MUST be published with any binary
release**, including the generator (`gen_model_db.py`) and the generated
database (`model_db.py`).

These EUPL-derived models are marked **Experimental**: their counter addresses
and reset parameters are derived from EUPL-licensed public data and have **not
been verified by this project on real hardware**.

### 2. Hardware-verified model data (L3250 family)

The **L3250 / L3251 / L3253 / L3255** family was independently verified on real
hardware by this project in **June 2026**. These models are marked **Verified**.

The protocol layer used to communicate with these printers
(`epson_d4.py` — an independent USB + IEEE-1284.4 (D4) + control-channel layer)
was written from public specifications and documented protocol/API facts and was
**not copied from any third party**.

---

## Verification method and evidence

Verification for the L3250 family was performed by reading and resetting the
waste-ink maintenance counters on physical hardware over a USB connection
(Windows 64-bit), following the application's full safety workflow:

- First-run Terms-of-Use acceptance.
- Mandatory pre-reset warning (8 points).
- Required confirmation checkbox: *"I confirm that the waste ink pad has been
  inspected, cleaned, replaced, or an external waste ink tank is installed and
  functioning."*
- Required second confirmation: *"I understand this action modifies printer
  maintenance counters and I accept full responsibility for ensuring physical
  maintenance has been completed."*
- An automatic EEPROM backup taken **before** every reset (the reset **stops**
  if the backup fails, unless the user explicitly overrides with a warning).

**Evidence location:** the local operation logs produced by `oplog.py` plus the
EEPROM backup files produced by `eeprom_io.py`. The operation logs record model,
transport, counter values, backup path, confirmation flags, and errors, but
**not serial numbers or personal data**. There is **no telemetry**; nothing is
transmitted off the device.

A model is considered **Verified** by this project only when:

1. The counters were successfully **read** from the physical printer, and
2. A counter **reset** was successfully applied and confirmed on the physical
   printer (with the EEPROM backup taken first), and
3. The above are reflected in the local operation logs and backup files.

All models that have **not** met these criteria remain **Experimental**.

---

## Data that MUST NOT be used

To preserve the project's compliance-oriented, risk-reduced posture, the
following data sources **must not** be added to or bundled with this project:

- Any **proprietary** or **vendor** database or data file.
- Any **unlicensed** database (no clear, compatible open-source license).
- Any **reverse-engineered vendor database**.
- The **previously-removed large unlicensed database** — it was removed and must
  not be reintroduced under any name.

Only data that is **license-compatible** (e.g., EUPL-1.2 data such as
`epson_print_conf`) or **independently verified on hardware by this project**
may be included.

---

## Provenance table

| Model | Region/Variant | Support status | Data source | License/provenance | Verification date | Verification method | Evidence/log reference | Notes |
|-------|----------------|----------------|-------------|--------------------|-------------------|---------------------|------------------------|-------|
| L3250 | Global / EcoTank | Verified | Hardware verification by this project | EUPL-1.2 (project) | June 2026 | USB read + reset of waste-ink counters via `epson_d4.py`, with pre-reset EEPROM backup | Local `oplog.py` operation logs + `eeprom_io.py` backup files | Verified on real hardware |
| L3251 | Global / EcoTank | Verified | Hardware verification by this project | EUPL-1.2 (project) | June 2026 | USB read + reset of waste-ink counters via `epson_d4.py`, with pre-reset EEPROM backup | Local `oplog.py` operation logs + `eeprom_io.py` backup files | Verified on real hardware |
| L3253 | Global / EcoTank | Verified | Hardware verification by this project | EUPL-1.2 (project) | June 2026 | USB read + reset of waste-ink counters via `epson_d4.py`, with pre-reset EEPROM backup | Local `oplog.py` operation logs + `eeprom_io.py` backup files | Verified on real hardware |
| L3255 | Global / EcoTank | Verified | Hardware verification by this project | EUPL-1.2 (project) | June 2026 | USB read + reset of waste-ink counters via `epson_d4.py`, with pre-reset EEPROM backup | Local `oplog.py` operation logs + `eeprom_io.py` backup files | Verified on real hardware |
| ~104 remaining compatible models | Various | Experimental | `epson_print_conf` converted by `gen_model_db.py` | EUPL-1.2, (c) 2024-2025 Ircama | Not verified by this project | EUPL-derived public data; not read/reset-verified on hardware by this project | None (no project hardware log) | Experimental; EUPL-derived data, not verified by this project on hardware. Use with caution. |

> The total embedded database contains **108 compatible models**: the 4 verified
> L3250-family models above plus approximately 104 Experimental, EUPL-derived
> models. **No proprietary or unlicensed database is bundled.**

---

## Adding new model data

New model data may be contributed, but only from **license-compatible** or
**independently hardware-verified** sources. The process is:

1. **Confirm the source is permitted.** It must be either:
   - EUPL-1.2-compatible open data (and clearly attributed), or
   - Data you verified yourself on real hardware.
   Data from proprietary, unlicensed, vendor, or reverse-engineered vendor
   databases is **not accepted** (see *Data that MUST NOT be used*).
2. **Generate, do not hand-edit, EUPL-derived entries.** EUPL-derived data is
   produced by `gen_model_db.py`, which writes `model_db.py`. Update the
   generator/input and regenerate so provenance stays reproducible.
3. **Mark the support status honestly.** New entries default to **Experimental**
   unless they meet the hardware **Verified** criteria above.
4. **Record provenance.** Add a row to the table in this file with the model,
   region/variant, support status, data source, license/provenance, and (if
   applicable) verification date, method, and evidence/log reference.
5. **For Verified status, attach evidence.** Provide the local `oplog.py`
   operation-log details and confirm an EEPROM backup was taken before the
   reset (with serial numbers and personal data excluded).
6. **Preserve copyleft.** Ensure the corresponding source (generator + generated
   database) is published with any binary release, as required by EUPL-1.2.

For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

This project is licensed under the **EUPL-1.2** (see `LICENSE.txt`). The EUPL-1.2
copyleft requires that the corresponding source code be published with any binary
release. EUPL-derived model data originates from `epson_print_conf` (EUPL-1.2,
Copyright (c) 2024-2025 Ircama).
