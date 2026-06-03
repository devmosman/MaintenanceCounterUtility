# Privacy Policy

**Product:** Waste Ink Maintenance Counter Utility (`MaintenanceCounterUtility.exe`)
**Version:** 1.0.0
**License:** EUPL-1.2 (see `LICENSE.txt`)

This document describes how the Waste Ink Maintenance Counter Utility handles data. It is written to be honest and maintenance-focused. It is **not legal advice**, and data-protection, consumer-protection and related laws vary by jurisdiction.

---

## Summary

> This application does not include telemetry and does not transmit usage data to the developer by default. Logs and backups are stored locally on the user's device.

The Waste Ink Maintenance Counter Utility is an open-source, maintenance-focused utility for selected compatible inkjet printers connected over USB on Windows 64-bit. It reads approximate waste-ink maintenance counters, creates a local backup, and can reset those counters only after the owner has physically inspected, cleaned, replaced, or redirected the waste-ink pad/tank. It performs no physical maintenance.

This privacy policy reflects the behaviour of version 1.0.0 as shipped.

---

## No telemetry, no transmission

- The application **does not include telemetry**.
- The application **does not transmit usage data to the developer** by default.
- Nothing is sent off the device. There is no analytics service, no crash-reporting service, and no network reporting of any kind built into the application.
- All data the application produces (logs, backups, settings) is stored **locally on the user's device**.

The application connects only to the printer over **USB**. It does not initiate network connections to deliver usage data to the developer or to any third party.

---

## What is stored locally

The application keeps a local operation log so that the owner has a record of maintenance actions and can troubleshoot problems. Local logs may contain the following:

- **Event** — the maintenance action or step that occurred.
- **Timestamp** — the date and time of the event.
- **Printer model** — the compatible model selected or detected.
- **Transport / connection method** — for example, the USB connection used.
- **Counter values before and after** — the approximate waste-ink maintenance counter readings around an operation.
- **Backup path** — the local file path of the EEPROM backup taken before a reset.
- **User-confirmation flags (true/false)** — whether the required confirmations and checkbox were accepted.
- **Error messages** — diagnostic information when an operation fails.

These logs are intended for the owner's own use and for local troubleshooting.

---

## What is NOT collected

The application is designed so that it should **not collect personal data unless strictly necessary**. In particular, the following are **not** collected:

- **Printer serial numbers.**
- **Personal identifiers** (names, email addresses, account details, location, and similar).
- **Unnecessary device identifiers** that are not required for the maintenance operation.

The local logs record the model, transport, counter values, backup path, confirmation flags and error messages described above, but **not** serial numbers or personal data.

---

## Where data is stored

All data is stored locally, next to the application:

- **Logs:** a `logs` folder next to the application.
- **Backups:** a `backups` folder next to the application.
- **Settings:** a `data` folder.

Because these files are stored locally on the user's device, the owner remains in control of them and can inspect, retain, or delete them. Backups should be kept safe, because the restore-from-backup feature relies on them.

---

## Future changes

If telemetry or any off-device data transmission is ever added in a future version:

- It must be **opt-in**.
- It must be clearly **documented**.

The application should continue to avoid collecting personal data unless strictly necessary, and any change to this behaviour should be reflected in this document.

---

## Non-affiliation notice

This project is not affiliated with, endorsed by, sponsored by, or approved by Epson. Epson is a trademark of its respective owner. Product names are used only to describe compatibility with selected printer models.

---

*This document is provided for transparency and is not legal advice. Privacy, data-protection and consumer-protection laws vary by jurisdiction. This project is compliance-oriented and risk-reduced in its handling of data, but it requires legal review before paid distribution by a qualified local lawyer.*
