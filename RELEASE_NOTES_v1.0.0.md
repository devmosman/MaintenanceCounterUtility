# Waste Ink Maintenance Counter Utility — v1.0.0

First public release. An open-source, maintenance-focused utility for selected
**compatible** inkjet printers (Windows, USB).

## What it does
- Reads approximate **waste-ink maintenance counters** and usage counters
  (printed pages, scans, cleaning cycles) over USB.
- Creates an automatic **EEPROM backup before every reset** (with restore).
- Resets the maintenance counters **only after** you confirm the physical
  waste-ink pad/tank has been inspected, cleaned, replaced, or redirected.

## What it does not do
- It does **not** clean, empty, repair, or replace the waste-ink pad/tank.
- It is **not** a way to avoid service requirements, and it is **not** an
  official Epson product.

## Supported models
- **Verified on hardware (June 2026):** L3250 / L3251 / L3253 / L3255.
- **Experimental (EUPL-derived, unverified):** all other models — use extra
  caution. See `SUPPORTED_MODELS.md` and `DATA_PROVENANCE.md`.

## Install
1. Download `MaintenanceCounterUtility-v1.0.0.zip`, unzip, run the `.exe`.
2. Accept the Terms on first run. Connect the printer by USB and use the app.
3. After a reset, **power-cycle the printer** to commit the change.

## Verify the download
Compare the SHA-256 of the files against `SHA256SUMS.txt`:
```
Get-FileHash .\MaintenanceCounterUtility.exe -Algorithm SHA256
```

## Notes
- The `.exe` is **unsigned**: Windows SmartScreen may warn → *More info → Run anyway*.
- Licensed under **EUPL-1.2**; full source is in this repository.
- Resetting clears only the **software** counter — the physical pad is still
  full and must be serviced separately, or ink can overflow.
- Anti-circumvention, repair, warranty, consumer-protection, and trademark laws
  **vary by jurisdiction**. This is **not legal advice**; paid/ad-supported
  distribution **requires legal review before paid distribution**.

**Not affiliated with, endorsed by, sponsored by, or approved by Epson.** Epson
is a trademark of its respective owner; product names indicate compatibility only.
