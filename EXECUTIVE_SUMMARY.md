# Executive summary — Prod2 affiliate publication

**What this is:** a small Amazon-affiliate publication (brand: **Prod2 — Kitchen notes & buying guides**) built around five owner-supplied products, with the verification machinery kept visible and reviewable behind it.
**Live site:** https://wingbangboozle1-lang.github.io/Prod2/ (GitHub Pages, this repository's `docs/`).
**Source of truth:** `data/*.json` + `content/pages/*.html` → `docs/` via `tools/build.py`; gated by `tools/checks.py`. See `ENGINE.md`.

## The five products (tracking ID `shopnow047c-20`)

| # | Product | Format | ASIN | Submitted short link | Status |
|---|---|---|---|---|---|
| P1 | Chefman 6 qt dual basket air fryer oven | Dual-basket | B0CDY277D3 | link.amazon/B04G1MEwY | Verified since 2026-11-14; re-read 2026-11-19 |
| P2 | Emeril Lagasse 26 qt French door air fryer toaster oven | Oven-style | B09B7SB46R | link.amazon/B02NbDxp3 | Verified since 2026-11-14; re-read 2026-11-19 (title drift — F-44) |
| P3 | Chefman 8 qt TurboFry air fryer | Single-basket | B08DKYBTPH | link.amazon/B00hJ57DV | Verified since 2026-11-14; re-read 2026-11-19 |
| P4 | ThermoMaven 1-second meat thermometer | Instant-read | B0DHZTCNR5 | link.amazon/B0c8moW59 | **First verified 2026-11-19** (resolves F-55) |
| P5 | CHEF iQ Sense Gen3 wireless thermometer | Wireless leave-in | B0DZFD6R9Z | link.amazon/B0f3GKalj | **First verified 2026-11-19** (resolves F-55) |

- All five short links resolved to the ASINs above on 2026-11-19 **with no `tag=` parameter** (F-03). The supplied short links are recorded verbatim and not judged (FLG-003 unresolved).
- The site publishes tagged Special Links `https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20` with `rel="sponsored"` and the required disclosure on every page (decisions D-01/D-14, D-P06).
- **No revenue is claimed.** Tag registration and click attribution are confirmable only inside Associates Central (F-57, F-58) — the one-link-per-product test is the owner's next step.

## What is deliberately absent

- **Prices and star ratings** (F-02) — they drift faster than honest re-verification; the site compares formats and listed specs instead.
- **Product-level commission figures** (F-01) — the official rate table's category bands (Kitchen 4.50%, Home 3.00%) don't map to these ASINs; product rates stay blank.
- **Hands-on testing** (D-06) — a specification publication until real usage exists (queued as suggestion SG-07).
- **Forecasts** — no conversion score or revenue forecast anywhere; the campaign ledger starts empty by rule and fills only from authorized first-party reports.

## The site

- Front page built as a publication front (D-21): hero, question-led guides, category tiles, then the data.
- Five question-shaped guides (basket vs oven · capacity checklist · cleanup & counter space · multi-function questions · thermometer accuracy), a buying guide, two category pages, and a sourced comparison table with the three-question chooser (D-23) and the counter-space analysis (D-26).
- Disclosure strip under the masthead on **every** page + footer repeat; every product link marked sponsored.
- Unique titles/meta, JSON-LD, sitemap.xml, robots.txt, RSS feed, typographic OG card (no product photography — S-18/D-22 still needs a decision).

## Decision-support system (review surfaces)

- **Suggestion queue** (`suggestions.html`): 10 proposals with evidence/impact/effort/risk and recommendations — nothing implemented until a reviewer picks a path. Recommended first move: **SG-06** (deploy the analytics endpoint + Search Console).
- **Open questions** (`questions.html`): what is known/missing/how to discover, per item — including Q-01 (Associates enrollment) and Q-19 (name clearance).
- **Flagged for review** (`flagged.html`): open/resolved/standing items with evidence links (S-11 split). F-55 resolved 2026-11-19; F-57/F-58/F-19/F-01/F-03 remain open — none blocks the merge.
- **Decision log** (`decisions.html`): carried decisions D-01…D-27 with recorded outcomes, plus this build's D-P01…D-P06.

## Measurement (machinery shipped, not yet on)

- Privacy-preserving outbound-click counter (`assets/js/measure.js`): five local events, no cookies/identifiers, ASIN + host only; **transmits nothing until an endpoint is configured**.
- Self-hosted endpoint (`analytics-endpoint/server.py`): counts only, no IP/UA/referrer/logs. Deployable — not hosted (F-19).
- Campaign ledger (`data/ledger.json`): the five defined events (impression, click, session, order, refund) with the official attribution windows; empty until an authorized report exists.

## Verification & governance trail

- 2026-11-19 session record: `data/verification-2026-11-19.json` (redirect reads, titles, breadcrumbs, feature bullets, carousel observations).
- Source register with read dates: `method.html` / `data/sources.json`.
- Coordination board with task statuses and the PR/deploy record: `COORDINATION.md`.
- Gate: `python3 tools/build.py && python3 tools/checks.py` — 8 sections, green on the merged build.

## Open decisions for the owner

1. Run the **one-link-per-product test** in Associates Central (gates attribution claims/scaling).
2. **Deploy the analytics endpoint + enable Search Console** (SG-06) — everything downstream depends on it.
3. Brand rename after trademark clearance (SG-01, blocked on Q-19).
4. Whether to adopt a dated-snapshot price policy (SG-05) — only with automation.
5. Product photography decision (S-18/D-22): still awaiting a decision; generated/copy photography is banned, real photography is the only compliant path.
