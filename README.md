# The Crisp Counter — editorial Amazon affiliate shop

A buyer-first static publication about five owner-submitted kitchen products. Tracking ID: `shopnow047c-20`.

**Live site:** https://wingbangboozle1-lang.github.io/Prod2/
**Executive summary:** [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) · **Repository review:** [REPO_AUDIT.md](REPO_AUDIT.md) · **Coordination log:** [COORDINATION.md](COORDINATION.md)

## What this project does — and does not do

The site organizes sourced product specifications into a shop front, comparison, category pages, buying guides and question-shaped articles. It publishes disclosures, sponsored affiliate links, a source register, missing-information questions, suggestions and flagged irregularities.

The current repository is **not** an AI-powered product-discovery or conversion-optimization service. It does not identify trending/high-converting products, use search-volume data, query Amazon Associates Central, publish automatically, or forecast revenue. Build automation creates and checks static pages; its analytics collector is not hosted, and Search Console is not verified. Do not claim those capabilities until they exist and have evidence.

## Five recorded product listings

Each product's intended ASIN and official listing URL are stored separately from the submitted short link and observed redirect record. Listing records were re-read on 2026-11-20 (records: `data/p2/verification-2026-11-20.json` and `data/p2/live-check-2026-11-20-722181aa.json` — all five `/dp/` listing titles matched the register); these are dated observations, not guarantees that a listing has not changed.

| ID | Product format | ASIN | Official listing source |
|---|---|---|---|
| P1 | Chefman dual-basket air fryer | B0CDY277D3 | [Amazon listing](https://www.amazon.com/dp/B0CDY277D3) · S-P1 |
| P2 | Emeril Lagasse French-door air-fryer oven | B09B7SB46R | [Amazon listing](https://www.amazon.com/dp/B09B7SB46R) · S-P2 |
| P3 | Chefman single-basket air fryer | B08DKYBTPH | [Amazon listing](https://www.amazon.com/dp/B08DKYBTPH) · S-P3 |
| P4 | ThermoMaven instant-read thermometer | B0DHZTCNR5 | [Amazon listing](https://www.amazon.com/dp/B0DHZTCNR5) · S-P4 |
| P5 | CHEF iQ Sense Gen3 wireless thermometer | B0DZFD6R9Z | [Amazon listing](https://www.amazon.com/dp/B0DZFD6R9Z) · S-P5 |

Unconfirmed values remain blank and are flagged. The owner-supplied `link.amazon` short-link compliance status remains unresolved (F-03); this project does not call those links invalid. A live re-check on 2026-11-20 observed those short links resolving to the Amazon homepage or an error rather than to the listings (F-P24); the cause is unexplained, so published buy paths use the site's own tagged `/dp/` Special Links.

## Build and verification

Standard-library Python generates the publication from `data/p2/*.json`, `content/pages/*.html` and `assets/`:

```bash
python3 tools/build.py      # render the publication: data/p2/*.json + content/pages/* -> docs/ -> repo root
python3 tools/checks.py     # release gate: 14 sections, exits non-zero on any violation
npm test                    # the gate, plus the self-hosted endpoint tests

---

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

Five owner-supplied `link.amazon` short links, each resolved against its official Amazon listing.
All five tokens are 9-character short-link tokens, not 10-character ASINs. On 2026-11-19 they
resolved to real listings. On 2026-11-20 a same-day re-read confirmed one of
five links, and a second same-day read disagrees on two links, so the outcome is undecided until a browser check (F-P24, F-P27, F-P28). See `data/p2/products.json`.

---

The dashboard/research pages remain reachable in the “The work behind it” navigation group and the footer. Disclosure appears immediately below the masthead and repeats in the footer. Product links are tagged and use `rel="sponsored"`.

## Key registers and implementation

- `data/p2/products.json`, `sources.json`, `intent-links.json`: item facts, source provenance and distinct intended/observed link records.
- `flags.json`, `questions.json`, `suggestions.json`, `decisions.json`: irregularities, missing information, proposals and recorded decisions.
- `calendar.json`, `events.json`, `ledger.json`: editorial hypotheses, measurement event definitions and the intentionally empty campaign ledger.
- `assets/css/site.css`, `assets/js/measure.js`, `tools/build.py`, `tools/checks.py`, `server.mjs`.
- `docs/`: generated deploy artifact. `archive/` and `site/` contain prior builds and are not canonical reader content.

## The site, by page

| Page | Job |
| --- | --- |
| `index.html` | Shop front page: illustrated hero, the shelf of five, question-led guide entry points, seasonal desk |
| `shop.html` | The whole catalogue, filterable by format and category, plus the three-question chooser |
| `compare.html` | One sourced comparison table, the counter-space analysis, and how to read both |
| `products.html` | Full listed specification per product, with the product-intent record kept separate |
| `guides.html` + 10 guide pages | One buyer question per page, in clusters with pillar pages, on a 14-day cadence |
| `category-air-fryers.html`, `category-thermometers.html` | The two format shelves |
| `buying-guide.html` | The long-form decision path: format, then capacity, then counter, then cleanup |
| `about.html` | Authorship, the four editorial rules, what we cannot tell you, imagery policy |
| `flagged.html` | Every irregularity, with an evidence link and a resolution route |
| `questions.html` | 15 open questions, each with a discovery method and what it blocks |
| `suggestions.html` | 28 proposals in three decision paths, with a review walkthrough |
| `measurement.html`, `compliance.html`, `privacy.html`, `method.html`, `decisions.html`, `executive-summary.html` | The governance surfaces, all reachable from the footer |

## Compliance

- Disclosure under the masthead on every page, repeated in the footer, using the first-person
  sentence prescribed by Operating Agreement §5 (corrected 2026-11-20; see F-P15).
- Every outbound Amazon product link is `rel="sponsored"` and carries `tag=shopnow047c-20`.
- **No published prices and no published star ratings.** This is now a policy requirement, not a
  stylistic choice: Program Policies §2(b) permits prices only when Amazon serves them or they come
  through the Creators/PA API (D-P11, closes Q-27).
- Product-intent record keeps intended vs. observed in separate fields, never merged.
- Privacy-preserving click counter (no cookies, no identifiers); five events; nothing is
  transmitted until an endpoint is configured.
- Irregularities and unverified values are published blank and flagged on the **Flagged for
  Review** page with source links — never inferred.
- No hands-on-testing claim anywhere; the gate fails the build if one appears.

## Imagery

Six illustrations were drawn for this site, generic to the product *format* rather than any
specific model, and each card is captioned "illustration, not the product photo". Amazon listing
photography is Program Content and its use is conditioned on the IP Licence, which has not been
reviewed (D-P12, Q-P05).

## Self-hosted analytics endpoint

The privacy-preserving click counter (`assets/js/measure.js`) records the five defined events —
`page_view`, `outbound_click`, `guide_read_75`, `category_click`, `feed_click` — and posts them
to a configured endpoint. GitHub Pages is static, so the endpoint is
self-hosted: `server.mjs` (a small Node collector with five-event aggregation) runs locally or
on any Node host. Run `npm start` to serve it, `npm test` to run the endpoint tests together
with the release gate. See `ANALYTICS-ENDPOINT.md`.

While no endpoint is configured the counter writes to the reader's own `localStorage` and transmits
nothing — that is the shipped state, and the release gate asserts it against
`data/p2/settings.json`.

See `EXECUTIVE_SUMMARY.md`, `DECISIONS.md`, and the **About** page for sources and methodology.

## Status at a glance

| Area | State |
| --- | --- |
| Product verification | All five ASINs live-read 2026-11-20; titles matched |
| Prices / ratings | Not published — required by Program Policies §2(b) |
| Associates tracking | Links tagged `shopnow047c-20`; enrollment itself is unverified (Q-01) |
| Search Console | Not verified; token slot ready in `data/p2/settings.json` (Q-P08) |
| Analytics endpoint | `server.mjs` works and is tested; not hosted (Q-23) |
| Campaign ledger | Empty by rule; accepts only authorized first-party rows |
| Release gate | 14 sections, green |
| Open flags | 27 open, 11 resolved, 4 standing (42 flags; F-P25..F-P28 added 2026-11-20) — all on the Flagged for review page |

Everything in the bottom half of that table is an owner action, not an engineering gap. The
**Open questions** page lists the discovery route for each one.

---

The site withholds prices, availability, ratings, review counts, product commission estimates and forecasts. It does not claim hands-on testing or popularity. See the [Compliance](https://wingbangboozle1-lang.github.io/Prod2/compliance.html), [Measurement](https://wingbangboozle1-lang.github.io/Prod2/measurement.html) and [Flagged for Review](https://wingbangboozle1-lang.github.io/Prod2/flagged.html) pages for source links and outstanding actions.
