# Supported Models

This document lists the compatible inkjet printer models recognised by the
**Waste Ink Maintenance Counter Utility** (`MaintenanceCounterUtility.exe`,
version 1.0.0). It is generated to match the embedded model database in
`model_db.py`.

The utility is an open-source, maintenance-focused tool. It reads approximate
waste-ink maintenance counters, creates a local backup, and can reset those
counters **only after** the owner has physically inspected, cleaned, replaced,
or redirected the waste-ink pad/tank. It performs **no** physical maintenance
and is **not** a way to avoid service requirements.

> This project is not affiliated with, endorsed by, sponsored by, or approved
> by Epson. Epson is a trademark of its respective owner. Product names are
> used only to describe compatibility with selected printer models.

## How to read this list

- **Platform / connection:** Windows 64-bit, **USB connection only**.
- Every model listed below supports **Read counters**, **Backup**, **Reset**,
  and **Restore** over USB.
- A backup is **always taken before a reset**. The reset stops if the backup
  fails, unless the owner explicitly overrides with a warning.
- The model database contains **108 compatible models**, embedded in the
  binary. It was converted from `epson_print_conf`
  (EUPL-1.2, Copyright (c) 2024-2025 Ircama) **plus** the
  L3250 / L3251 / L3253 / L3255 family, which was verified on real hardware.
  There is no unlicensed, proprietary, vendor, or reverse-engineered database.

## Legend

| Status | Meaning |
| --- | --- |
| **Verified** | Confirmed on real hardware by this project (June 2026). |
| **Experimental** | EUPL-derived data (from `epson_print_conf`); **not** verified on hardware by this project. Treat with extra caution. |

> **Extra caution for Experimental entries.** Counter addresses for
> Experimental models come from EUPL-licensed community data and have not been
> validated on physical hardware by this project. Values shown may be
> approximate or incorrect for your specific unit. Because a backup is always
> taken before any reset, you can restore the previous counter state from the
> local backup if a result looks wrong. This is not legal advice; anti-circumvention,
> repair, warranty, consumer-protection, product-liability and trademark laws
> vary by jurisdiction.

## Compatible models

The L3250 / L3251 / L3253 / L3255 family is represented in the database by a
single verified entry (`L3250`), which also matches the `L3251`, `L3253`, and
`L3255` variants. All other entries are Experimental.

| Model | Read counters | Backup | Reset | Restore | Verification status | Notes |
| --- | :---: | :---: | :---: | :---: | --- | --- |
| Artisan 720 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| Artisan 730 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2400 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2401 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2403 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2405 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2500 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2550 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2600 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2650 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2700 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2701 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2703 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2705 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2714 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2720 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2721 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2723 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2725 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2750 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2751 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2756 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2800 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2801 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2803 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2805 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2810 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2811 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2812 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2813 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2814 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2815 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2816 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-2818 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-4700 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| ET-4800 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L3060 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L3150 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L3151 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L3160 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L3166 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L3168 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L3250 | Yes | Yes | Yes | Yes | **Verified** | Hardware-verified (June 2026); also matches L3251 / L3253 / L3255; USB only |
| L355 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L366 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L386 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L395 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L405 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4150 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4152 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4154 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4156 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4158 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4160 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4162 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4164 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4166 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| L4168 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| PX720WD | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| PX730WD | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| R2000 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| Stylus Photo PX720WD | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| Stylus Photo PX730 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| Stylus Photo PX730WD | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| TX720WD | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| TX730WD | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| WF-7515 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| WF-7525 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-200 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-205 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-207 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-2100 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-2150 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-2151 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-2155 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-2200 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-2205 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-225 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-235 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-312 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-313 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-315 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-342 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-343 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-345 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-422 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-423 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-425 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-432 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-433 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-435 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-540 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-610 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-611 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-615 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-620 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-621 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-625 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-700 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-701 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-702 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-7100 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-760 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-820 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-821 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-830 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-850 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |
| XP-960 | Yes | Yes | Yes | Yes | Experimental | EUPL-derived data; USB only |

## Counts

- Database entries: **108**.
- Hardware-verified: **L3250** (covering the L3250 / L3251 / L3253 / L3255
  family).
- Experimental (EUPL-derived, not verified on hardware by this project): all
  remaining entries.

## Before resetting any counter

The reset workflow is intentionally cautious and compliance-oriented:

1. First-run Terms-of-Use acceptance.
2. A mandatory pre-reset warning.
3. A required checkbox: *"I confirm that the waste ink pad has been inspected,
   cleaned, replaced, or an external waste ink tank is installed and
   functioning."*
4. A required second confirmation: *"I understand this action modifies printer
   maintenance counters and I accept full responsibility for ensuring physical
   maintenance has been completed."*
5. An automatic EEPROM backup taken **before** every reset. The reset stops if
   the backup fails, unless the owner explicitly overrides with a warning.
6. A low-counter caution and a reminder to power-cycle the printer after a
   reset.

Local operation logs record the model, transport, counter values, backup path,
confirmation flags, and errors, but **not** serial numbers or personal data.
There is no telemetry; nothing is transmitted off the device.

## Notes on accuracy and risk

This is a risk-reduced, maintenance-focused tool, but it is **not legal
advice**. Anti-circumvention, repair, warranty, consumer-protection,
product-liability, and trademark laws vary by jurisdiction. This project
**requires legal review before paid distribution** by a qualified local
IP/product lawyer. The utility is licensed under the EUPL-1.2 (see
`LICENSE.txt`); corresponding source code must be published with any binary
release.
