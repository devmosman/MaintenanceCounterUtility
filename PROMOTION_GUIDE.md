# Promotion / distribution guide (step by step)

This is the human checklist for spreading the project. The repository already
contains the non-human assets: landing page, FAQ, an SEO guide, a social-preview
image, sitemap/robots, README badges, and ready-to-post templates
(`promo/launch-templates.md`).

Keep everything **maintenance-focused** and **honest**: disclose you are the
author, don't imply Epson affiliation, avoid "bypass/crack/unlock" wording. This
is not legal/marketing-compliance advice; platform rules and laws vary by
jurisdiction.

---

## Phase 0 — Make it live (do first)

1. **Push** your commits and tag (PowerShell, PAT as password):
   ```
   cd "D:\AI_Demos\EPSON"
   git push origin main
   git push origin v1.0.0
   ```
2. **Create the GitHub Release** (Releases → Draft new release → tag `v1.0.0`),
   paste `RELEASE_NOTES_v1.0.0.md`, attach `dist\MaintenanceCounterUtility-v1.0.0.zip`,
   `dist\MaintenanceCounterUtility.exe`, `dist\SHA256SUMS.txt`, publish.
3. **Enable GitHub Pages:** Settings → Pages → Deploy from a branch →
   `main` / `/docs` → Save. Wait ~1–2 min, then open
   `https://devmosman.github.io/MaintenanceCounterUtility/`.
4. **Add a screenshot:** save your app screenshot as `docs\img\screenshot.png`,
   commit and push. (It then shows on the site and README.)
5. **Record a short demo** (optional but high-impact): a 30–60s screen capture or
   GIF of reading + the reset confirmation flow. Add it to the README and site.

## Phase 1 — GitHub presence

6. **About box** (repo home, gear icon): add the description and **topics**:
   `epson ecotank waste-ink maintenance-tool windows usb eupl open-source printer`.
   Add the website URL.
7. **Social preview:** Settings → General → Social preview → upload
   `docs/og-image.png` (so shared repo links show the card).
8. **Enable Issues and Discussions** for support and model reports.

## Phase 2 — Software directories (evergreen traffic)

9. Submit to:
   - **AlternativeTo** (alternativeto.net) — use the description in `promo/launch-templates.md`.
   - **Softpedia**, **MajorGeeks** (submit-software pages).
   - Optionally mirror on **SourceForge** as a download host.
   Use the maintenance-focused description; link the GitHub release.

## Phase 3 — Communities (initial spike)

10. Post the **guide** (not a bare "download my app") using the templates:
    - Reddit: r/printers, r/fixit, r/right_to_repair, r/Epson (check each rule).
    - Printer/repair **forums** (e.g. tech/printer repair boards).
    - **Facebook groups** for printer repair / your printer model (large globally).
    - **Discord/Telegram** repair servers.
    Always disclose authorship and follow each community's self-promo rules.

## Phase 4 — Search & content (the compounding engine)

11. **Google Search Console:** add the site, verify, and submit
    `https://devmosman.github.io/MaintenanceCounterUtility/sitemap.xml`.
12. **Write more guides** (one per popular model / error variant), same structure
    as `docs/guide-fix-epson-l3250-waste-ink.html`. This is what ranks over time.
13. **Translate** the best guide into 2–3 languages your audience uses
    (e.g. Indonesian, Spanish, Arabic, Hindi) as additional pages.
14. Answer related questions on **Quora / Stack Exchange / GitHub issues** of
    similar tools, helpfully, with a link (use the reply template).

## Phase 5 — Measure & iterate

15. **Analytics (privacy-friendly):** create a free **GoatCounter** site, then in
    `docs/index.html` (and the other pages) uncomment the analytics snippet and
    replace `YOURCODE`. (Or use Cloudflare Web Analytics.)
16. Watch **Release download counts**, **GitHub stars**, and analytics by
    **UTM source** (below). Double down on whatever channel converts.

---

## UTM link convention

Append to the site URL so you can see where visitors come from:
```
https://devmosman.github.io/MaintenanceCounterUtility/?utm_source=<reddit|forum|facebook|youtube|twitter>&utm_medium=<post|comment|video>
```
The templates in `promo/launch-templates.md` already include these.

## Etiquette / compliance reminders
- Disclose authorship everywhere.
- Lead with help; respect each community's promo rules (avoid bans).
- Maintenance framing only; keep the non-affiliation notice.
- No Epson logos/branding. Plain-text compatibility wording only.
- Don't ship or link the previously-removed unlicensed data.

## Launch checklist
- [ ] Commits + tag pushed
- [ ] GitHub Release published (zip + exe + SHA256SUMS)
- [ ] GitHub Pages live; screenshot added
- [ ] Repo description, topics, social preview set
- [ ] Issues/Discussions enabled
- [ ] Submitted to 2–3 directories
- [ ] Posted the guide to 3–5 communities (rules followed, author disclosed)
- [ ] Search Console verified; sitemap submitted
- [ ] Analytics enabled (UTM tracking)
- [ ] At least one extra guide / one translation drafted
