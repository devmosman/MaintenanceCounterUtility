# Disclaimer

**Waste Ink Maintenance Counter Utility** (executable: `MaintenanceCounterUtility.exe`), Version 1.0.0
License: EUPL-1.2 (see `LICENSE.txt`)

This document is **not legal advice**. Please read it in full before downloading, building, running, or distributing this software.

---

## 1. Provided As-Is, No Warranty

This software is provided **"AS IS"**, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. The authors and contributors accept no liability for any claim, damages, or other liability arising from, out of, or in connection with the software or its use. You use this software entirely at your own risk. Use of the software is governed by the terms of the EUPL-1.2 license in `LICENSE.txt`.

## 2. No Guarantee of Compatibility

This is a maintenance-focused, open-source utility for a limited set of **compatible** inkjet printer models. The embedded model database contains 108 models.

- **L3250 / L3251 / L3253 / L3255** — Verified on real hardware (June 2026).
- **All other models** — **Experimental.** The data for these models is EUPL-derived and has **not** been verified by this project on hardware.

There is no guarantee that any model — verified or experimental — will be detected, read, or operated correctly. Counter values are **approximate**. Behaviour may differ between firmware revisions, regional variants, and individual units. The utility supports **Windows 64-bit** over a **USB connection only**.

## 3. Not Affiliated With Epson

This project is not affiliated with, endorsed by, sponsored by, or approved by Epson. Epson is a trademark of its respective owner. Product names are used only to describe compatibility with selected printer models.

## 4. The Utility Performs No Physical Maintenance

This utility reads approximate waste-ink maintenance counters, creates a local backup, and can reset those counters. **It performs no physical maintenance of any kind.** It does not inspect, clean, replace, drain, or redirect the waste-ink pad or tank. It is **not** a substitute for required service and is **not** a way to avoid service requirements.

A counter reset only changes a stored value. It does nothing to the physical condition of the printer.

## 5. Risks of Incorrect Reset Use

Resetting maintenance counters without first completing the corresponding physical maintenance is dangerous and may cause, among other things:

- **Ink leakage** from a saturated waste-ink pad.
- **Overflow** of waste ink inside or outside the printer.
- **Printer damage**, including damage to internal components and surrounding surfaces.
- **Mess** and staining of the printer, work area, and nearby property.
- **Data loss**, including loss or corruption of stored counter data.

These outcomes can be permanent and are not covered by any warranty from the authors of this software.

## 6. You Are Responsible for Physical Maintenance First

**You — the printer owner or operator — are solely responsible for ensuring that the required physical waste-ink maintenance has actually been completed before performing any reset.** A reset must only ever follow the owner having physically inspected, cleaned, replaced, or redirected the waste-ink pad/tank.

To support a careful, maintenance-focused workflow, the application already includes:

- First-run Terms-of-Use acceptance.
- A mandatory pre-reset warning (8 points).
- A required checkbox: *"I confirm that the waste ink pad has been inspected, cleaned, replaced, or an external waste ink tank is installed and functioning."*
- A required second confirmation: *"I understand this action modifies printer maintenance counters and I accept full responsibility for ensuring physical maintenance has been completed."*
- An automatic EEPROM backup taken **before every reset** — the reset stops if the backup fails, unless you explicitly override it with a warning.
- Restore-from-backup.
- Local operation logs recording model, transport, counter values, backup path, confirmation flags, and errors — but **not** serial numbers or personal data.
- A low-counter caution.
- A reminder to power-cycle the printer after a reset.

There is **no telemetry**, and nothing is transmitted off the device. These safeguards reduce risk but **do not remove your responsibility**. Confirming the on-screen prompts does not mean the physical work was done; only you can ensure that.

## 7. Legal Considerations

This section is **not legal advice**, and the authors are not your lawyers.

**Laws vary by jurisdiction.** Anti-circumvention, repair, warranty, consumer-protection, product-liability, and trademark laws differ significantly from one country and region to another, and they change over time. Whether and how you may use, build, modify, or distribute this software — and what obligations and risks attach to doing so — depends on your local law and your specific circumstances.

You should **consult local legal and technical professionals** before relying on this software in any context where the legal or technical consequences matter to you.

This is a copyleft (EUPL-1.2) project: corresponding source code **must** be published with any binary release.

### Paid Distribution

This software is offered as a risk-reduced, compliance-oriented, maintenance-focused tool, but no such description is a guarantee of legality. **Paid distribution requires legal review before paid distribution** by a qualified local intellectual-property and product-liability lawyer. Do not sell, bundle for sale, or otherwise commercially distribute this software without first obtaining that review for your jurisdiction.

## 8. Summary

By downloading, building, running, or distributing this software you acknowledge that you have read and understood this disclaimer, that the software is provided as-is with no warranty and no guarantee of compatibility, that it performs no physical maintenance, that incorrect reset use may cause ink leakage, overflow, printer damage, mess, and data loss, that you alone are responsible for ensuring physical waste-ink maintenance is completed first, that laws vary by jurisdiction, and that this document is not legal advice.
