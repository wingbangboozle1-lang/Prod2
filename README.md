# Prod2 — The Crisp Counter (editorial Amazon affiliate shop)

Five kitchen tools (three air fryers in three formats, two meat thermometers), written up as a
buying guide and sold through Amazon Associates. Tracking ID `shopnow047c-20`. The reader-facing
publication ships under the working brand **The Crisp Counter** (decision D-P18, 2026-11-20, on the
owner's anti-slop directive; formal name clearance open as Q-19/F-P21).

**Live site:** https://wingbangboozle1-lang.github.io/Prod2/

**Read this first if you are picking the project up:** the reader-facing site is the editorial
shop build described below. The `Countercraft` `site/` build further down is a preserved earlier
generation, kept deployable and gated, but it is **not** what readers see.

The site is **data-driven**: every page is generated from the verified data in `data/*.json` by
`scripts/build_site.py`, and `scripts/verify_site.py` is a release gate that fails the build on
any violation (missing disclosure, missing `rel="sponsored"`, duplicate meta, broken links,
sitemap gaps). Standard library only — no dependencies.

## Quick start

```bash
python3 tools/build.py      # render the publication: data/p2/*.json + content/pages/* -> docs/ -> repo root
python3 tools/checks.py     # release gate: 27 sections, exits non-zero on any violation
npm test                    # the gate, plus the self-hosted endpoint tests
```

`tools/build.py` writes `docs/` and then mirrors it to the repository root, because GitHub Pages
serves this repository in legacy "main /" mode. That is not a preference: the Pages API reports
`build_type: legacy` and returns **403** to the session token on any attempt to switch to Actions
mode, so the root mirror is what readers actually get (INT-07, re-confirmed 2026-11-20).

## Layout

```
data/p2/          the registers the site renders: products, sources, flags, questions,
                  suggestions, decisions, intent-links, events, ledger, calendar, settings,
                  and the dated verification records
content/pages/    one file per page, with {{placeholders}} for data-rendered blocks
assets/           the design system (css/site.css), interactions (js/site.js), measurement
                  (js/measure.js) and six drawn illustrations
tools/            build.py (generator), checks.py (release gate), make_og.py (social card)
docs/             generated output -> published (also mirrored to the repo root)
server.mjs        optional self-hosted aggregate-only event endpoint (not deployed publicly)
scripts/ + site/  the preserved Countercraft build (earlier generation, still gated in CI)
archive/          every previous build, kept and excluded from indexing by robots.txt
COORDINATION.md   shared task board
EXECUTIVE_SUMMARY.md, DECISIONS.md   reviewer-facing records
```

**Root mirror (INT-07):** GitHub Pages for this repo is in legacy "serve the repository root"
mode, which only a repository admin can switch to Actions mode (the REST API returns 403 to the
session token — recorded three times). The generator therefore mirrors the deterministic `site/`
output to the repository root, so the live site is correct in both Pages modes. One source of truth
(`data/*.json`), two deterministic outputs. When an admin flips Pages to Actions mode, delete the
root mirror in a single commit.

**One site rule (INT-06, 2026-11-19):** four independent session builds existed at peak. The
consolidated, canonical site is the data-driven `site/` build. Everything else lives in `archive/`.
The optional `server.mjs` endpoint serves `site/` and accepts all event families in aggregate-only
form; the page tracker transmits nothing unless an endpoint is explicitly configured.

## The products

Five owner-supplied `link.amazon` short links, each resolved against its official Amazon listing.
All five tokens are 9-character short-link tokens, not 10-character ASINs. On 2026-11-19 they
resolved to real listings. On 2026-11-20 a same-day re-read confirmed one of
five links, and a second same-day read disagrees on two links, so the outcome is undecided until a browser check (F-P24, F-P27, F-P28). See `data/p2/products.json`.

| # | Product | Format | ASIN |
| --- | --- | --- | --- |
| P1 | Chefman 6 qt dual basket air fryer oven | Dual-basket | B0CDY277D3 |
| P2 | Emeril Lagasse 26 qt French door air fryer toaster oven | Oven-style | B09B7SB46R |
| P3 | Chefman 8 qt TurboFry air fryer | Single-basket | B08DKYBTPH |
| P4 | ThermoMaven 1-second digital meat thermometer | Instant-read | B0DHZTCNR5 |
| P5 | CHEF iQ Sense Gen3 wireless meat thermometer | Wireless leave-in | B0DZFD6R9Z |

All five were **re-fetched live on 2026-11-20**; every observed string is recorded in
`data/p2/verification-2026-11-20.json`, including the values that were *not* observed. Three of the
five listings show a neighbouring product's price or rating in the visible page; none of those were
mistaken for the target product (F-P17).

## The site, by page

| Page | Job |
| --- | --- |
| `index.html` | Shop front page: illustrated hero, the shelf of five, question-led guide entry points, seasonal desk |
| `shop.html` | The whole catalogue, filterable by format and category, plus the three-question chooser |
| `compare.html` | One sourced comparison table, the counter-space analysis, and how to read both |
| `products.html` | Full listed specification per product, with the product-intent record kept separate |
| `guides.html` + 12 guide pages | One buyer question per page, in clusters with pillar pages, on a 14-day cadence; 3 long reads registered in `data/p2/calendar.json` |
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
| Release gate | 27 sections, green |
| Open flags | 28 open, 20 resolved, 5 standing (53 flags) — all on the Flagged for review page |


Everything in the bottom half of that table is an owner action, not an engineering gap. The
**Open questions** page lists the discovery route for each one.
