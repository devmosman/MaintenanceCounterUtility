# Terms of Use

**Product:** Waste Ink Maintenance Counter Utility (`MaintenanceCounterUtility.exe`)
**Version:** 1.0.0
**License:** EUPL-1.2 (see `LICENSE.txt`)

> This is not legal advice. These terms describe the conditions under which you may use this utility. Laws vary by jurisdiction. If you are uncertain about your rights or obligations, consult a qualified local legal professional.

---

## 1. Not an official Epson product

This project is not affiliated with, endorsed by, sponsored by, or approved by Epson. Epson is a trademark of its respective owner. Product names are used only to describe compatibility with selected printer models.

This is an independent, open-source, maintenance-focused utility. It is not an Epson product and is not distributed on behalf of any printer manufacturer.

## 2. What this utility does (and does not do)

This utility reads approximate waste-ink maintenance counters for selected compatible inkjet printers, creates a local backup, and can reset those counters **only after** the owner has physically inspected, cleaned, replaced, or redirected the waste-ink pad or tank.

It performs **no** physical maintenance. Resetting a counter does not empty, clean, replace, or repair any physical component. This utility is **not** a substitute for the maintenance and service requirements that apply to your hardware.

## 3. Your responsibility: complete physical maintenance first

By using this utility you accept that you are solely responsible for completing the required physical maintenance **before** resetting any counter. Specifically, you confirm that, before each reset, you have inspected, cleaned, replaced, or installed and verified a functioning external waste-ink tank as appropriate for your printer.

Resetting a maintenance counter without performing the corresponding physical maintenance may allow waste ink to overflow, which can damage the printer, surrounding property, or cause other harm. You accept full responsibility for ensuring physical maintenance has been completed.

The application includes safeguards to support careful use, including a first-run Terms-of-Use acceptance, a mandatory pre-reset warning, two required confirmations, an automatic local backup taken before every reset, restore-from-backup, local operation logging, a low-counter caution, and a reminder to power-cycle the printer after a reset. These safeguards are aids only and do not transfer responsibility away from you.

## 4. Use at your own risk; no warranty

You use this utility entirely at your own risk. To the maximum extent permitted by applicable law, and consistent with the disclaimers in the EUPL-1.2, the software is provided "as is" and "as available", without warranty of any kind, whether express or implied, including but not limited to fitness for a particular purpose. The authors and contributors are not liable for any loss or damage arising from use of this utility, to the extent the law allows.

## 5. No guarantee of compatibility

There is no guarantee that this utility will work with any particular printer.

The embedded model database contains 108 compatible models. Only the **L3250, L3251, L3253, and L3255** family has been verified on real hardware (June 2026). **All other models are Experimental**: their data is EUPL-derived and has **not** been verified on hardware by this project. Behaviour on unverified models may be incorrect or incomplete.

This is Windows 64-bit, USB-connection software only. Other platforms and connection types are not supported.

## 6. Laws vary by country

Anti-circumvention, repair, warranty, consumer-protection, product-liability, and trademark laws vary by jurisdiction. Whether and how you may use a tool of this kind, and what obligations apply, depends on where you are and how you use it. This document is not legal advice. It is your responsibility to understand and comply with the laws that apply to you.

## 7. Commercial use and distribution

This utility is intended as a risk-reduced, compliance-oriented, maintenance-focused tool. Commercial use or distribution should be reviewed by a qualified legal professional. In particular, this project **requires legal review before paid distribution** by a qualified local IP or product-liability lawyer in your jurisdiction.

Because the software is licensed under the EUPL-1.2 (a copyleft license), the corresponding source code **must** be published with any binary release you distribute. See `LICENSE.txt` for the full terms.

## 8. Relationship to the EUPL (the EUPL controls)

These Terms of Use are intended to describe responsible use and do **not** remove, restrict, or override any rights granted to you by the EUPL-1.2 for the licensed code. Nothing in this document is intended to reduce the freedoms the EUPL grants, including the rights to use, study, modify, and redistribute the source code under the conditions of that license.

If any conflict exists between these Terms of Use and the EUPL-1.2, **the EUPL-1.2 controls for the licensed code.**

## 9. Privacy

This utility contains no telemetry and transmits nothing off your device. Local operation logs record model, transport, counter values, backup path, confirmation flags, and errors, but do **not** record serial numbers or personal data.

---

*This document is not legal advice. Laws vary by jurisdiction.*
