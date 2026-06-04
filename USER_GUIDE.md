# User Guide — Waste Ink Maintenance Counter Utility

A maintenance-support utility for selected compatible inkjet printers (Windows,
USB). It reads waste-ink maintenance counters, backs up the relevant printer
memory, and can reset those counters **after** you have physically serviced the
waste-ink pad/tank. It does **not** perform physical maintenance and is **not** a
way to avoid service requirements.

> Not affiliated with, endorsed by, sponsored by, or approved by Epson. Epson is a
> trademark of its respective owner; product names indicate compatibility only.

![Main window](docs/img/screenshot.png)

---

## 1. Before you start

You need:
- A Windows PC (64-bit).
- A **supported** printer connected by **USB cable** and powered on.
- The downloaded app (`MaintenanceCounterUtility.exe`).

**Most important principle:** a counter reset clears only a *software* counter.
The physical waste-ink pad is still full. **Inspect, clean, replace the pad, or
install/verify an external waste-ink tank first** — otherwise ink can overflow
inside the printer.

## 2. Launch the app

1. Unzip the download and double-click `MaintenanceCounterUtility.exe`.
2. The app is unsigned, so Windows SmartScreen may show *"Windows protected your
   PC"* → click **More info → Run anyway**.
3. On first launch, read and **accept the Terms of Use**.

## 3. Read the counters

- Connect the printer by USB and power it on, then click **Refresh**.
- The window shows:
  - **Model** and a **Verified / Experimental** badge.
  - **Waste ink maintenance counters** — each as `current / maximum (percent)`.
    (The pad names are approximate.)
  - **Usage counters** — total printed pages, scans, cleaning cycles, head passes.
- If you see **"No Epson USB printer detected"**, check the USB cable and that the
  printer is on, then click **Refresh** again.

## 4. Back up (recommended)

Click **Backup** to save a snapshot of the relevant printer memory to a local
`backups` folder next to the app. A backup is **also taken automatically before
every reset**, so a change can be reversed.

## 5. Reset the maintenance counters (after physical service)

1. Make sure you have **physically serviced** the waste-ink pad/tank.
2. Click **Reset Maintenance Counters**.
3. If the counters are low, you'll get a caution (resetting low counters is
   usually unnecessary).
4. Read the **warning**, then tick the box:
   *"I confirm that the waste ink pad has been inspected, cleaned, replaced, or an
   external waste ink tank is installed and functioning."*
   The **Continue** button stays disabled until you tick it.
5. Click **Continue**, then confirm the **second prompt** accepting responsibility.
6. The app takes a backup, performs the reset, and shows the backup location.
   *(If the backup fails, the reset stops unless you explicitly override it.)*

## 6. Power-cycle the printer

After a reset you **must turn the printer off** with its physical power button,
wait a few seconds, and turn it back on. This commits the change.

## 7. Restore from a backup (if needed)

Click **Restore…**, choose a backup file from the `backups` folder, confirm, then
power-cycle the printer. This writes the saved values back.

## 8. Where things are stored

Next to the application:
- `backups\` — EEPROM backup files (JSON).
- `logs\operations.log` — local operation log (model, counters, backup path,
  confirmation flags, errors). **No serial numbers or personal data; no telemetry.**
- `data\settings.json` — your Terms acceptance.

See `PRIVACY.md` for full details.

## 9. Buttons reference

| Button | What it does |
|--------|--------------|
| Refresh | Re-read counters from the printer |
| Backup | Save a memory snapshot now |
| Reset Maintenance Counters | Reset after the confirmation flow (backup taken first) |
| Restore… | Write a previous backup back to the printer |
| About | Version, license, links |
| 🌐 Website | Open the project website |
| ❤ Support on Ko-fi | Optional donation to support the project |

## 10. Troubleshooting

- **No window appears, but it's in Task Manager:** update to the latest version;
  if it persists, look for `startup_error.log` next to the app and report it.
- **"…is not in the database":** your exact model isn't supported yet. See
  `SUPPORTED_MODELS.md` and `CONTRIBUTING.md`.
- **Experimental model warning:** that model's data hasn't been verified on
  hardware by this project — proceed with extra caution; a backup is always taken.
- **Antivirus flags the .exe:** PyInstaller executables are sometimes false-
  flagged. You can verify the SHA-256 against `SHA256SUMS.txt`, or build from
  source.

## 11. Safety & legal

- Resetting clears only the software counter; the physical pad must be serviced
  separately, or ink can overflow.
- Anti-circumvention, repair, warranty, consumer-protection, and trademark laws
  **vary by jurisdiction**. This is **not legal advice**.
- Licensed under EUPL-1.2. Source: https://github.com/devmosman/MaintenanceCounterUtility
