# The Crisp Counter — editorial Amazon affiliate shop

A buyer-first static publication about five owner-submitted kitchen products. Tracking ID: `shopnow047c-20`.

**Live site:** https://wingbangboozle1-lang.github.io/Prod2/
**Executive summary:** [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) · **Repository review:** [REPO_AUDIT.md](REPO_AUDIT.md) · **Coordination log:** [COORDINATION.md](COORDINATION.md)

## What this project does — and does not do

The site organizes sourced product specifications into a shop front, comparison, category pages, buying guides and question-shaped articles. It publishes disclosures, sponsored affiliate links, a source register, missing-information questions, suggestions and flagged irregularities.

The current repository is **not** an AI-powered product-discovery or conversion-optimization service. It does not identify trending/high-converting products, use search-volume data, query Amazon Associates Central, publish automatically, or forecast revenue. Build automation creates and checks static pages; its analytics collector is not hosted, and Search Console is not verified. Do not claim those capabilities until they exist and have evidence.

## Five recorded product listings

Each product's intended ASIN and official listing URL are stored separately from the submitted short link and observed redirect record. Listing records were re-read on 2026-11-20 (record: `data/p2/verification-2026-11-20.json`); these are dated observations, not guarantees that a listing has not changed.

| ID | Product format | ASIN | Official listing source |
|---|---|---|---|
| P1 | Chefman dual-basket air fryer | B0CDY277D3 | [Amazon listing](https://www.amazon.com/dp/B0CDY277D3) · S-P1 |
| P2 | Emeril Lagasse French-door air-fryer oven | B09B7SB46R | [Amazon listing](https://www.amazon.com/dp/B09B7SB46R) · S-P2 |
| P3 | Chefman single-basket air fryer | B08DKYBTPH | [Amazon listing](https://www.amazon.com/dp/B08DKYBTPH) · S-P3 |
| P4 | ThermoMaven instant-read thermometer | B0DHZTCNR5 | [Amazon listing](https://www.amazon.com/dp/B0DHZTCNR5) · S-P4 |
| P5 | CHEF iQ Sense Gen3 wireless thermometer | B0DZFD6R9Z | [Amazon listing](https://www.amazon.com/dp/B0DZFD6R9Z) · S-P5 |

Unconfirmed values remain blank and are flagged. The owner-supplied `link.amazon` short-link compliance status remains unresolved (F-03); this project does not call those links invalid.

## Build and verification

Standard-library Python generates the publication from `data/p2/*.json`, `content/pages/*.html` and `assets/`:

```bash
python3 tools/build.py
python3 tools/checks.py
npm test
```

`tools/build.py` writes the intended publication to `docs/` and currently also mirrors generated pages to the repository root for legacy Pages compatibility. `tools/checks.py` is the build gate; `npm test` additionally tests the optional Node analytics endpoint. CI runs site build and verification workflows in `.github/workflows/`.

## Important live-host warning — flagged, not concealed

As checked on 2026-11-20, GitHub Pages reports `build_type=legacy`, source `main /`. Therefore GitHub Pages serves the **repository root**, and source files, data registers and archives are accessible by URL. `robots.txt` cannot prevent direct access. The Pages workflow builds `docs/` but does not change the active source setting. An API attempt to switch to workflow publishing returned HTTP 403.

**Required administrator action:** GitHub repository Settings → Pages → Source → **GitHub Actions**. Then verify `https://wingbangboozle1-lang.github.io/Prod2/data/p2/settings.json` and `/tools/build.py` return 404. Until that verification, flags F-P19 and F-P20 stay open. Do not treat a green workflow as proof this repository exposure is fixed.

## Main site pages

- `index.html`, `shop.html`, `products.html`, `compare.html`
- `guides.html`, `buying-guide.html`, question-shaped guide pages
- `category-air-fryers.html`, `category-thermometers.html`
- `about.html`, `method.html`, `flagged.html`, `questions.html`, `suggestions.html`, `decisions.html`
- `measurement.html`, `compliance.html`, `privacy.html`, `executive-summary.html`

The dashboard/research pages remain reachable in the “The work behind it” navigation group and the footer. Disclosure appears immediately below the masthead and repeats in the footer. Product links are tagged and use `rel="sponsored"`.

## Key registers and implementation

- `data/p2/products.json`, `sources.json`, `intent-links.json`: item facts, source provenance and distinct intended/observed link records.
- `flags.json`, `questions.json`, `suggestions.json`, `decisions.json`: irregularities, missing information, proposals and recorded decisions.
- `calendar.json`, `events.json`, `ledger.json`: editorial hypotheses, measurement event definitions and the intentionally empty campaign ledger.
- `assets/css/site.css`, `assets/js/measure.js`, `tools/build.py`, `tools/checks.py`, `server.mjs`.
- `docs/`: generated deploy artifact. `archive/` and `site/` contain prior builds and are not canonical reader content.

The site withholds prices, availability, ratings, review counts, product commission estimates and forecasts. It does not claim hands-on testing or popularity. See the [Compliance](https://wingbangboozle1-lang.github.io/Prod2/compliance.html), [Measurement](https://wingbangboozle1-lang.github.io/Prod2/measurement.html) and [Flagged for Review](https://wingbangboozle1-lang.github.io/Prod2/flagged.html) pages for source links and outstanding actions.
