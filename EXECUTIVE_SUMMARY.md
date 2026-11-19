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

- Front page built as a shop, not an audit (D-P08): a method promise, a five-card product rail carrying the two
  deciding figures and the date each was read, format tiles, the guide shelf, then the sourced table. The
  verification machinery is one click away rather than first.
- **Eight** question-led guides (basket vs oven · capacity · dual vs single basket · cleanup and counter
  space · multi-function questions · air fryer as a gift · thermometer accuracy · probe in an air fryer), a guide
  index, a buying guide, two format pages, and a sourced comparison table with the three-question chooser (D-23), the
  counter-space analysis (D-26) and a read date on every published figure. 26 pages in total, including an
  **analysis page** (coverage matrix, capacity-to-footprint ranking, three-stage funnel, owner priority board,
  verification ledger) and a **design prompt pack** page.
- Disclosure strip under the masthead on **every** page + footer repeat; every product link marked sponsored.
- Unique titles/meta, JSON-LD, sitemap.xml, robots.txt, RSS feed, typographic OG card (no product photography — S-18/D-22 still needs a decision).

## Decision-support system (review surfaces)

- **Suggestion queue** (`suggestions.html`): **34 proposals**, each with evidence, impact/effort/risk and **two or
  three concrete paths** (what changes, upside, downside, cost, what it unlocks), one marked recommendation, and a
  ranked board on top. Nothing that changes a claim ships before a reviewer names a path: replying
  `SG-15, path A` is enough (D-P07).
- **Open questions** (`questions.html`): **27 items**, each recording what is already known with its dated source,
  what is missing, what the answer decides, who can answer, the checks a session could run, and the conservative
  default while it stays open. 12 gate a decision and are ranked on a board above the list.
- **Owner priority board** (`analysis.html#waiting-on`, from `data/p2/decision-priority.json`): the nine decisions
  this repository is waiting on, ranked by what they unblock, each with a waiting_on line and an effort
  estimate, so the shortest useful reply is a sentence.
- **Flagged for review** (`flagged.html`): open/resolved/standing items with evidence links (S-11 split). F-55 resolved 2026-11-19; F-57/F-58/F-19/F-01/F-03 remain open — none blocks the merge.
- **Decision log** (`decisions.html`): carried decisions D-01 to D-27 with recorded outcomes, plus this build's
  D-P01 to D-P08 (D-P07 records what was implemented without waiting and what deliberately was not; D-P08 the
  shop-shaped front and the image-free identity). 22 queue items record which design brief they feed
  (`feeds_design_prompt`).

## Measurement (machinery shipped, not yet on)

- Privacy-preserving outbound-click counter (`assets/js/measure.js`): five local events, no cookies/identifiers, ASIN + host only; **transmits nothing until an endpoint is configured**.
- Self-hosted endpoint (`analytics-endpoint/server.py`): counts only, no IP/UA/referrer/logs. Deployable — not hosted (F-19).
- Campaign ledger (`data/p2/ledger.json`): the five defined events (impression, click, session, order, refund) with the official attribution windows; empty until an authorized report exists.

## Verification & governance trail

- 2026-11-19 session records: data/p2/verification-2026-11-19.json (redirect reads, titles, breadcrumbs, feature
  bullets, carousel observations) plus the dated re-check log data/p2/verification-log.json, rendered as a table on
  the analysis page so that a verified claim always means verified on this date, from this URL.
- Source register with read dates: `method.html` / `data/p2/sources.json`.
- Coordination board with task statuses and the PR/deploy record: `COORDINATION.md`.
- Gate: `python3 tools/build.py && python3 tools/checks.py` — **9 sections** (pages, disclosure, links
  including in-page anchors, facts, claims, editorial voice, chrome, SEO, freshness), green on the merged build.
  `python3 scripts/verify_site.py` (the Countercraft build) and `npm test` (the endpoint) also pass.

## Open decisions for the owner

1. **Which register is canonical** — one line decides whether a future figure can be traced to the file
  the build actually used (F-P06, SG-31, Q-P15).
2. **Who accepts a suggestion path** — the queue has accepted/amended/rejected states and no named
  decider (Q-P08).
3. **Host the collector and verify a Search Console property** — until then every ranking here is
  judgement, not measurement (SG-06, SG-25).
4. **Pick the price policy** — dated snapshots, a licensed live feed, or none (SG-05, Q-27).
5. **Set the re-verification cadence** — listings have been observed drifting within days (Q-P11).
6. **Name the publisher** — the mandated disclosure is written in the first person and the site has
  no I (Q-P19, SG-27).
7. **Run the one-link-per-product test** in Associates Central, and settle the imagery route (SG-08, S-18/D-22):
  generated or copied photography is out, a real shoot is the only compliant path.
8. **Close the PR #16 hazard** — merging it would overwrite the generated root the live site is
  served from (Q-P18, RR-5/RR-6).


---

# Appendix — preserved verbatim: Executive Summary, Countercraft session (session-arena-599eec57, 2026-11-19)

> Preserved during integration (arena/44093825-prod2) without edits. Note one divergence
> for the owner's review: this appendix lists prices "as listed"; the deployed Prod2 site
> withholds prices and star ratings entirely (flag F-02 / suggestion SG-05 / question Q-27).
> The prices below were captured by that session and are not re-verified here.

# Executive Summary — Countercraft (Amazon Affiliate Platform)

**Tracking ID:** `shopnow047c-20`
**Built:** 2026-11-19 · Session `session-arena-599eec57` · Branch `arena/599eec57-prod2`
**Status:** Site built, verified, and published to GitHub Pages.

## What this is

Countercraft is an editorial affiliate shop for the five submitted Amazon products. It is built
as a **publication front page** that leads with the products and buyer questions, with the
verification machinery (the register, the product-intent record, the campaign ledger) kept one
click away on a single **Research Desk** surface. It is a data-driven static site: every page is
generated from verified data in `data/*.json`, and a release gate (`scripts/verify_site.py`)
checks the output before anything is published.

## The five products (all verified against official Amazon listings, 2026-11-19)

| Submitted link | Resolves to | Product | Category | Price (as listed) |
| --- | --- | --- | --- | --- |
| link.amazon/B04G1MEwY | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven | Air Fryer Ovens | $74.99 |
| link.amazon/B02NbDxp3 | B09B7SB46R | Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | Air Fryer Ovens | $229.99 |
| link.amazon/B00hJ57DV | B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry 4-in-1 | Air Fryer Ovens | $59.99 |
| link.amazon/B0c8moW59 | B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer | Meat Thermometers | $16.99 |
| link.amazon/B0f3GKalj | B0DZFD6R9Z | CHEF iQ Sense Smart Wireless Meat Thermometer (Gen3) | Meat Thermometers | $139.99 |

**Key finding:** every submitted link carries a **9-character short-link token**, not a
10-character ASIN (Amazon defines an ASIN as 10 characters). The tokens resolve to real
10-character ASINs and real listings. Intent and observation are kept in **separate fields** and
never merged (see the product-intent confirmation record on the Research Desk).

## Verified from official sources

- **Five Amazon product listings** — identity, brand, category, browse node, capacity and
  buy-box price read from each official product page. ThermoMaven's rating was captured
  (4.6★, 3,499 ratings, Amazon's Choice).
- **Amazon Associates Operating Agreement** (updated 2025-10-15) — §1 Special Links / Program Content.
- **Amazon Associates Program Policies** (updated 2026-04-14) — §2(b) Special Links + price display,
  §3(e) cookie/pixel disclosure, §6(a)–(w) Content on your Site (incl. **6(v)** do not obscure the
  link URL, **6(w)** link shortening, **6(t)** ratings require Creators/PA API).
- **ASIN definition** — 10-character alphanumeric, Amazon-assigned (Amazon.com).
- **FTC** disclosure guidance (Disclosures 101; Endorsements, Influencers, Reviews).
- **Google** — rel="sponsored" for paid links; unique meta descriptions; page experience.

Full source list with links: `data/p2/sources.json` and the **About** page.

## What was built

- **Editorial front page** — hero, featured guides, category tiles, then the register (the data
  sits below the fold, not above it).
- **Two category pages** — Air Fryer Ovens, Meat Thermometers.
- **Comparison page** — three-question "which one is for you" chooser, side-by-side table, and a
  counter-space analysis (capacity per unit of counter depth; depth figures flagged, not guessed).
- **Eight question-shaped guides** — one page per buyer question, with FAQ structure and Article +
  FAQPage structured data, internally linked to the comparison, category and each other.
- **Research Desk** — the full register, the product-intent confirmation record, the (empty)
  campaign ledger, and the source register.
- **Suggestions / decision portal** — open questions, what we know vs. do not know, suggestions,
  and a three-path chooser.
- **Flagged for Review** — every irregularity and unverified item, with source links.
- **About** — methodology and compliance.

## Compliance & trust features

- **Disclosure strip under the masthead on every page**, repeated in the footer.
- **Every outbound Amazon product link carries `rel="sponsored"`** (enforced by the build and the
  release gate).
- **Privacy-preserving click counter** — no cookies, anonymous local ID, five defined events
  (`page_view`, `cta_click`, `product_click`, `filter_apply`, `guide_read`), POSTed to a
  self-hosted `/collect` endpoint (configurable).
- **Findability** — `sitemap.xml`, `rss.xml`, `robots.txt`, unique title + meta description per
  page, Open Graph / Twitter cards, structured data.

## Irregularities & open decisions (published, not hidden)

1. **Token vs. ASIN** — all five submitted tokens are 9 characters; not ASINs.
2. **Uncaptured ratings** — 4 of 5 star ratings were displayed on the listing but not captured in
   this extraction; published blank and flagged. Do not infer.
3. **Short-link compliance** — the submitted short links are **not declared invalid**, but their
   exact status under Program Policies 6(w) is **unresolved**. Recommendation: replace with tagged
   Special Links generated in Associates Central, testing one link per product before scaling.
4. **Price display** — shown "as listed" with a date and a live link; live/API pricing requires
   Creators/PA API (§2(b)).
5. **Analytics endpoint** — GitHub Pages is static; the `/collect` endpoint must be self-hosted
   (serverless function) for aggregation.

These are all on the **Flagged for Review** and **Suggestions** pages with source links. They do
not block the site.

## How to run / verify

```bash
python3 scripts/build_site.py     # rebuild site/ from data/*.json
python3 scripts/verify_site.py    # release gate: exits non-zero on any violation
```

Both use the Python standard library only — no dependencies, runnable from a clean checkout.

## Deployment

GitHub Pages deploys from `main` via `.github/workflows/pages.yml` (deploy on push to `main`).
The PR that merges this work records the deploy result in `COORDINATION.md`.


---

# Appendix — preserved: Executive summary, Prod2 publication session (arena/44093825-prod2)

> Preserved verbatim during integration. This session built the deeper review registers
> and the tagged-link build (see the integration log in COORDINATION.md). The publication
> output it generated is preserved at `docs/` and marked `noindex` — the one indexed site
> is the Countercraft `site/` build at the domain root.

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
- Campaign ledger (`data/p2/ledger.json`): the five defined events (impression, click, session, order, refund) with the official attribution windows; empty until an authorized report exists.

## Verification & governance trail

- 2026-11-19 session record: `data/p2/verification-2026-11-19.json` (redirect reads, titles, breadcrumbs, feature bullets, carousel observations).
- Source register with read dates: `method.html` / `data/p2/sources.json`.
- Coordination board with task statuses and the PR/deploy record: `COORDINATION.md`.
- Gate: `python3 tools/build.py && python3 tools/checks.py` — 8 sections, green on the merged build.

## Open decisions for the owner

1. Run the **one-link-per-product test** in Associates Central (gates attribution claims/scaling).
2. **Deploy the analytics endpoint + enable Search Console** (SG-06) — everything downstream depends on it.
3. Brand rename after trademark clearance (SG-01, blocked on Q-19).
4. Whether to adopt a dated-snapshot price policy (SG-05) — only with automation.
5. Product photography decision (S-18/D-22): still awaiting a decision; generated/copy photography is banned, real photography is the only compliant path.
