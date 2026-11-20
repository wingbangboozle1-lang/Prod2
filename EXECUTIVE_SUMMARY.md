# Executive summary — The Crisp Counter (Prod2 affiliate publication)

**What this is:** a small Amazon-affiliate publication (working brand: **The Crisp Counter — Kitchen notes & buying guides**; formal clearance still open, F-P21/Q-P10) built around five owner-supplied products. Since the 2026-11-20 pass it reads as a shop first: a product shelf, drawn illustrations, buy buttons and question-shaped guides, with the verification machinery one click behind it rather than in front of it.
**Live site:** https://wingbangboozle1-lang.github.io/Prod2/ (GitHub Pages, this repository's `docs/`).
**Source of truth:** `data/*.json` + `content/pages/*.html` → `docs/` via `tools/build.py`; gated by `tools/checks.py`. See `ENGINE.md`.

## The five products (tracking ID `shopnow047c-20`)

| # | Product | Format | ASIN | Submitted short link | Status |
|---|---|---|---|---|---|
| P1 | Chefman 6 qt dual basket air fryer oven | Dual-basket | B0CDY277D3 | link.amazon/B04G1MEwY | Live re-read 2026-11-20 (title matched) |
| P2 | Emeril Lagasse 26 qt French door air fryer toaster oven | Oven-style | B09B7SB46R | link.amazon/B02NbDxp3 | Live re-read 2026-11-20 (title matched; preset count still open, Q-31) |
| P3 | Chefman 8 qt TurboFry air fryer | Single-basket | B08DKYBTPH | link.amazon/B00hJ57DV | Live re-read 2026-11-20 (title matched) |
| P4 | ThermoMaven 1-second meat thermometer | Instant-read | B0DHZTCNR5 | link.amazon/B0c8moW59 | Live re-read 2026-11-20 (title, ±0.5℉/NIST, IP67 matched) |
| P5 | CHEF iQ Sense Gen3 wireless thermometer | Wireless leave-in | B0DZFD6R9Z | link.amazon/B0f3GKalj | Live re-read 2026-11-20 (title, 3 probes, 1000°F matched) |

- All five short links resolved to the ASINs above **with no `tag=` parameter** (F-03). The supplied short links are recorded verbatim and not judged (FLG-003 unresolved).
- **Every listing was re-fetched live on 2026-11-20** and each observed string is recorded in `data/p2/verification-2026-11-20.json`. Prior records stated this environment could not reach Amazon; that was wrong (F-P18).
- The site publishes tagged Special Links `https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20` with `rel="sponsored"` and the required disclosure on every page (decisions D-01/D-14, D-P06).
- **No revenue is claimed.** Tag registration and click attribution are confirmable only inside Associates Central (F-57, F-58) — the one-link-per-product test is the owner's next step.

## What is deliberately absent

- **Prices and star ratings** (F-02) — now a policy requirement, not a preference: Program Policies §2(b) (updated 2026-04-14, read 2026-11-20) permits published prices only when Amazon serves them or they arrive via the Creators/PA API. Dated snapshots are neither (D-P11).
- **Product-level commission figures** (F-01) — the official rate table's category bands (Kitchen 4.50%, Home 3.00%) don't map to these ASINs; product rates stay blank.
- **Hands-on testing** (D-06) — a specification publication until real usage exists (queued as suggestion SG-07).
- **Forecasts** — no conversion score or revenue forecast anywhere; the campaign ledger starts empty by rule and fills only from authorized first-party reports.

## The site

- **Front page rebuilt 2026-11-20 as a shop front** (D-P10): illustrated hero, the full shelf of five cards with best-for lines and buy buttons, then question-led guide entry points, the seasonal desk and clusters. The method moved into a short byline strip near the foot of the page.
- **New `shop.html`**: the whole catalogue in one filterable shelf (format and category), the three-question chooser, and a shortlist comparison.
- **New `about.html`**: who writes this, the four editorial rules, a "what we cannot tell you" table with a flag link on every row, and a plain statement of the commission relationship.
- **Navigation cut from eleven links to six** (Shop · Air fryers · Thermometers · Guides · Compare · About). All dashboard surfaces remain in the footer directory, and the gate now fails if the reader nav exceeds seven links.
- **Imagery**: six illustrations drawn for the site, generic to the format, captioned "illustration, not the product photo" (D-P12). No Amazon photography is copied.
- Ten question-shaped guides on a fortnightly cadence, plus two long reads (see below), a buying guide, two category pages, and a sourced comparison table with the three-question chooser (D-23) and the counter-space analysis (D-26).
- The thermometer guide now leads with the **official USDA safe-minimum temperatures** and the cold-storage and power-outage limits, quoted with their last-reviewed dates (D-P14). This gives a reader an independent reason to care about accuracy instead of restating a marketing claim.
- Disclosure strip under the masthead on **every** page + footer repeat; every product link marked sponsored.
- Unique titles/meta, JSON-LD, sitemap.xml, robots.txt, RSS feed, typographic OG card (no product photography — S-18/D-22 still needs a decision).

## Reader-facing work in the latest pass (2026-11-20, session arena/644d217b-prod2)

The prior passes made the site correct and made it look like a shop. This pass answered the harder
question — *why would anyone read it?* — with depth, and fixed the machinery that would have hidden
whether it worked.

- **Two long reads, sourced to official guidance rather than to the listings.**
  `article-thermometer-placement.html` (1,295 words) argues that probe placement matters more than
  stated precision, from the USDA FSIS Food Thermometers factsheet and the FSIS Safe Minimum Internal
  Temperature Chart (both read 2026-11-20). `article-air-fryer-doneness.html` (1,212 words) argues
  that internal temperature, not capacity or wattage, is the number that decides whether an air fryer
  worked, from Nebraska Extension's peer-reviewed air-fryer food-safety guidance plus the same FSIS
  chart. Both name what they could not verify.
- **The measurement defect that would have hidden all of it is fixed.** The published contract named
  five events; the only collector in the repo answered 400 to three of them, so two thirds of the
  site's measurement would have been dropped silently the moment an endpoint was hosted. The collector
  now accepts all five, a regression test reads the five names out of `measure.js`, and the gate fails
  the build on any divergence (F-P23 resolved, Q-P14 answered, D-P21).
- **The long reads are measured too.** The depth event fired only on pages whose build id starts with
  `guide`, so both new articles would have been invisible. Fixed and gated.
- **A ranked short list now opens the suggestion queue**, because 38 proposals with no ordering is not
  a decision surface. Ranked by unblocked work per hour of owner time: Pages source (one dropdown),
  analytics + Search Console, name clearance, the email-consent question, then the payoff step.
- **Three new open questions** (Q-P15 length standard, Q-P16 whether real product photography is
  obtainable at all, Q-P17 where the endpoint runs and who pays), each with the cheapest route to the
  answer.
- **New gate section `longreads`** enforces what the two new pieces do by hand: inline sources, the
  unverified block, allow-listed official hosts, presence in sitemap and feed.

## Decision-support system (review surfaces)

- **Suggestion queue** (`suggestions.html`): 38 proposals, opened by a ranked five-row short list of the only items that change what happens next, now grouped into **three decision paths** (prove the traffic / consolidate the shop / rebrand and expand) with a four-step walkthrough, so a reviewer can choose a direction in one sitting. Recommended: **Path A**, starting with SG-06 (endpoint) and SG-29 (Search Console).
- **Open questions** (`questions.html`): 21 items, now with a **discovery-method table** that names the cheapest route to each answer (re-read the official page · log in to Associates Central · run a controlled test · ask a lawyer · read the licence · ask the reader) and what it closes. Q-27 is newly answered by D-P11.
- **Flagged for review** (`flagged.html`): 37 items, open/resolved/standing, each with an evidence link. Four added 2026-11-20: F-P15 (disclosure wording), F-P16 (misleading CTA), F-P17 (neighbouring-ASIN prices), F-P18 (egress boundary).
- **Decision log** (`decisions.html`): 32 recorded decisions, including D-P21 (which event vocabulary is authoritative) from the latest pass.

## Measurement (machinery shipped, not yet on)

- Privacy-preserving outbound-click counter (`assets/js/measure.js`): five local events, no cookies/identifiers, ASIN + host only; **transmits nothing until an endpoint is configured**.
- Self-hosted endpoint (`server.mjs`): counts only, no IP/UA/referrer/logs. Deployable — not hosted (F-19).
- Campaign ledger (`data/p2/ledger.json`): the five defined events (impression, click, session, order, refund) with the official attribution windows; empty until an authorized report exists.

## Verification & governance trail

- 2026-11-20 session record: `data/p2/verification-2026-11-20.json` — every observed string, every non-observation, and five findings (V-01…V-05).
- 2026-11-19 session record: `data/p2/verification-2026-11-19.json` (redirect reads, titles, breadcrumbs, feature bullets, carousel observations).
- Source register with read dates: `method.html` / `data/p2/sources.json`.
- Coordination board with task statuses and the PR/deploy record: `COORDINATION.md`.
- Gate: `python3 tools/build.py && python3 tools/checks.py` — **13 sections** (pages, disclosure, links, validity, facts, claims, chrome, seo, publication, longreads, shop, exposition, measurement, freshness), green on this build. The `shop` section is new: it fails if the shelf loses a card, a buy button, an image file or the About page, if a referenced asset is missing, or if any page implies hands-on testing.

## The publication passes (2026-11-20 — three sessions, reconciled)

Three parallel sessions executed the owner's standing directive — the site must read as a polished,
branded publication with timely articles, not generated output — and this merge reconciles all three:

- **Shop-front design rebuild** (arena/70b2b9f7-prod2, D-P10…D-P14): shipped design system (drawn
  format illustrations, product shelf, `shop.html`, `about.html`, reader nav cut to six links), all
  five listings re-read live with verbatim records, disclosure corrected to the Operating Agreement
  §5 first-person sentence (D-P13), dated-snapshot price policy refused on the Program Policies
  §2(b) read (D-P11, closes Q-27), drawn-only imagery (D-P12), USDA/FoodSafety.gov temperature
  guidance in the thermometer guide (D-P14).
- **Anti-slop brand + typography + seasonal pass** (arena/f55b5827-prod2, D-P18…D-P20): the working
  brand **"The Crisp Counter"** on every reader-facing surface (preliminary name search clean;
  formal clearance open as Q-19/Q-P10, flag F-P21), the design brief's Fraunces + Inter shipped
  self-hosted (SIL OFL 1.1, no third-party font requests) with mobile token conformance (44px tap
  targets, sticky comparison anchors, amber unverified states), and the December gifting window
  opened with `guide-gift-guide.html` plus four new hypothesis queue slots.
- **Event-vocabulary pass** (arena/86206fb3-prod2, D-P15, F-P22/F-P23, Q-P14, SG-41): measured the
  root-mode Pages exposure, rewrote F-P19/F-P20 with evidence, added root-mirror canaries, and
  published (rather than silently fixed) the site/endpoint event-vocabulary mismatch.
- **Register ID collisions were remapped and documented**: the anti-slop pass's rows now live at
  D-P18…D-P20 (twice remapped; see the decision log meta) and its runbook suggestion at SG-44;
  nothing from any session was discarded.

## The publication pass (2026-11-19, arena/9f84489c-prod2)

The reader-facing site now reads like a shop, not an audit (decision D-P07): the front page leads
with the five product cards before any data table; a guides hub groups eight question-shaped guides
into two clusters (air fryers, meat thermometers) with pillar pages; a seasonal desk (holiday
hosting live, grilling season staged) rotates from `data/p2/calendar.json`; the reader nav carries
clear labels (Compare · Products · Guides · Buying guide · Air fryers · Thermometers) while every
dashboard surface stays in the footer and the single "The work behind it" group; the RSS feed ships
with subscribe affordances; Search Console readiness ships with a verification-token slot and an
owner checklist (F-P06 / Q-P05); and a consent-gated "What should we answer next?" form ships dark
until its privacy basis exists (F-P07 / Q-47). Three new guides (how many quarts; two baskets or
one; holiday hosting) complete the eight-topic calendar on a 14-day cadence. The suggestion queue
grew SG-11…SG-17 — including three fully specified design directions that feed DESIGN_PROMPT.md —
and the questions register gained a scannable status table plus Q-P05/Q-P06.

## Open decisions for the owner

1. Run the **one-link-per-product test** in Associates Central (gates attribution claims/scaling).
2. **Deploy the analytics endpoint + verify Search Console** (SG-06, runbook SG-44) — everything downstream depends on it; the checklist is on the measurement page.
3. **Ratify the working brand and run formal clearance** (SG-38, Q-P10/Q-19) — "The Crisp Counter" ships as the working wordmark; the USPTO/state/common-law search is the missing evidence.
4. **Settle the reader-capture consent text** (Q-47) — the form ships dark until then.
5. Price-policy and availability-policy questions are answered for now (D-P11: both out, per Program Policies §2(b)) — revisit only if Creators/PA API access arrives (D-21).
6. Settle the event-vocabulary fix (SG-41/F-P23/Q-P14) — an owner decision recorded as open in D-P15.
7. Product photography decision (S-18/D-22/Q-P05): still awaiting the IP-licence read; drawn illustrations are the shipped interim (D-P12), with seasonal hero-art extension queued (SG-39).



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

**What this is:** a small Amazon-affiliate publication (working brand: **The Crisp Counter — Kitchen notes & buying guides**; formal clearance still open, F-P21/Q-P10) built around five owner-supplied products. Since the 2026-11-20 pass it reads as a shop first: a product shelf, drawn illustrations, buy buttons and question-shaped guides, with the verification machinery one click behind it rather than in front of it.
**Live site:** https://wingbangboozle1-lang.github.io/Prod2/ (GitHub Pages, this repository's `docs/`).
**Source of truth:** `data/*.json` + `content/pages/*.html` → `docs/` via `tools/build.py`; gated by `tools/checks.py`. See `ENGINE.md`.

## The five products (tracking ID `shopnow047c-20`)

| # | Product | Format | ASIN | Submitted short link | Status |
|---|---|---|---|---|---|
| P1 | Chefman 6 qt dual basket air fryer oven | Dual-basket | B0CDY277D3 | link.amazon/B04G1MEwY | Live re-read 2026-11-20 (title matched) |
| P2 | Emeril Lagasse 26 qt French door air fryer toaster oven | Oven-style | B09B7SB46R | link.amazon/B02NbDxp3 | Live re-read 2026-11-20 (title matched; preset count still open, Q-31) |
| P3 | Chefman 8 qt TurboFry air fryer | Single-basket | B08DKYBTPH | link.amazon/B00hJ57DV | Live re-read 2026-11-20 (title matched) |
| P4 | ThermoMaven 1-second meat thermometer | Instant-read | B0DHZTCNR5 | link.amazon/B0c8moW59 | Live re-read 2026-11-20 (title, ±0.5℉/NIST, IP67 matched) |
| P5 | CHEF iQ Sense Gen3 wireless thermometer | Wireless leave-in | B0DZFD6R9Z | link.amazon/B0f3GKalj | Live re-read 2026-11-20 (title, 3 probes, 1000°F matched) |

- All five short links resolved to the ASINs above **with no `tag=` parameter** (F-03). The supplied short links are recorded verbatim and not judged (FLG-003 unresolved).
- **Every listing was re-fetched live on 2026-11-20** and each observed string is recorded in `data/p2/verification-2026-11-20.json`. Prior records stated this environment could not reach Amazon; that was wrong (F-P18).
- The site publishes tagged Special Links `https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20` with `rel="sponsored"` and the required disclosure on every page (decisions D-01/D-14, D-P06).
- **No revenue is claimed.** Tag registration and click attribution are confirmable only inside Associates Central (F-57, F-58) — the one-link-per-product test is the owner's next step.

## What is deliberately absent

- **Prices and star ratings** (F-02) — now a policy requirement, not a preference: Program Policies §2(b) (updated 2026-04-14, read 2026-11-20) permits published prices only when Amazon serves them or they arrive via the Creators/PA API. Dated snapshots are neither (D-P11).
- **Product-level commission figures** (F-01) — the official rate table's category bands (Kitchen 4.50%, Home 3.00%) don't map to these ASINs; product rates stay blank.
- **Hands-on testing** (D-06) — a specification publication until real usage exists (queued as suggestion SG-07).
- **Forecasts** — no conversion score or revenue forecast anywhere; the campaign ledger starts empty by rule and fills only from authorized first-party reports.

## The site

- **Front page rebuilt 2026-11-20 as a shop front** (D-P10): illustrated hero, the full shelf of five cards with best-for lines and buy buttons, then question-led guide entry points, the seasonal desk and clusters. The method moved into a short byline strip near the foot of the page.
- **New `shop.html`**: the whole catalogue in one filterable shelf (format and category), the three-question chooser, and a shortlist comparison.
- **New `about.html`**: who writes this, the four editorial rules, a "what we cannot tell you" table with a flag link on every row, and a plain statement of the commission relationship.
- **Navigation cut from eleven links to six** (Shop · Air fryers · Thermometers · Guides · Compare · About). All dashboard surfaces remain in the footer directory, and the gate now fails if the reader nav exceeds seven links.
- **Imagery**: six illustrations drawn for the site, generic to the format, captioned "illustration, not the product photo" (D-P12). No Amazon photography is copied.
- Ten question-shaped guides on a fortnightly cadence, plus two long reads (see below), a buying guide, two category pages, and a sourced comparison table with the three-question chooser (D-23) and the counter-space analysis (D-26).
- The thermometer guide now leads with the **official USDA safe-minimum temperatures** and the cold-storage and power-outage limits, quoted with their last-reviewed dates (D-P14). This gives a reader an independent reason to care about accuracy instead of restating a marketing claim.
- Disclosure strip under the masthead on **every** page + footer repeat; every product link marked sponsored.
- Unique titles/meta, JSON-LD, sitemap.xml, robots.txt, RSS feed, typographic OG card (no product photography — S-18/D-22 still needs a decision).

## Decision-support system (review surfaces)

- **Suggestion queue** (`suggestions.html`): 38 proposals, opened by a ranked five-row short list of the only items that change what happens next, now grouped into **three decision paths** (prove the traffic / consolidate the shop / rebrand and expand) with a four-step walkthrough, so a reviewer can choose a direction in one sitting. Recommended: **Path A**, starting with SG-06 (endpoint) and SG-29 (Search Console).
- **Open questions** (`questions.html`): 21 items, now with a **discovery-method table** that names the cheapest route to each answer (re-read the official page · log in to Associates Central · run a controlled test · ask a lawyer · read the licence · ask the reader) and what it closes. Q-27 is newly answered by D-P11.
- **Flagged for review** (`flagged.html`): 37 items, open/resolved/standing, each with an evidence link. Four added 2026-11-20: F-P15 (disclosure wording), F-P16 (misleading CTA), F-P17 (neighbouring-ASIN prices), F-P18 (egress boundary).
- **Decision log** (`decisions.html`): 32 recorded decisions, including D-P21 (which event vocabulary is authoritative) from the latest pass.

## Measurement (machinery shipped, not yet on)

- Privacy-preserving outbound-click counter (`assets/js/measure.js`): five local events, no cookies/identifiers, ASIN + host only; **transmits nothing until an endpoint is configured**.
- Self-hosted endpoint (`server.mjs`): counts only, no IP/UA/referrer/logs. Deployable — not hosted (F-19).
- Campaign ledger (`data/p2/ledger.json`): the five defined events (impression, click, session, order, refund) with the official attribution windows; empty until an authorized report exists.

## Verification & governance trail

- 2026-11-20 session record: `data/p2/verification-2026-11-20.json` — every observed string, every non-observation, and five findings (V-01…V-05).
- 2026-11-19 session record: `data/p2/verification-2026-11-19.json` (redirect reads, titles, breadcrumbs, feature bullets, carousel observations).
- Source register with read dates: `method.html` / `data/p2/sources.json`.
- Coordination board with task statuses and the PR/deploy record: `COORDINATION.md`.
- Gate: `python3 tools/build.py && python3 tools/checks.py` — **13 sections** (pages, disclosure, links, validity, facts, claims, chrome, seo, publication, longreads, shop, exposition, measurement, freshness), green on this build. The `shop` section is new: it fails if the shelf loses a card, a buy button, an image file or the About page, if a referenced asset is missing, or if any page implies hands-on testing.

## Open decisions for the owner

1. Run the **one-link-per-product test** in Associates Central (gates attribution claims/scaling).
2. **Deploy the analytics endpoint + enable Search Console** (SG-06) — everything downstream depends on it.
3. Brand rename after trademark clearance (SG-01, blocked on Q-19).
4. Whether to adopt a dated-snapshot price policy (SG-05) — only with automation.
5. Product photography decision (S-18/D-22): still awaiting a decision; generated/copy photography is banned, real photography is the only compliant path.

## The 2026-11-20 shop-first pass (arena/70b2b9f7-prod2)

The brief for this pass was blunt: it should look and read like a polished affiliate shop, not an
audit, and it should earn organic traffic. What shipped, and why each change is defensible:

| Change | Why it exists | Decision |
| --- | --- | --- |
| New design system with a single token layer | A shop needs one coherent look; tokens keep a future rename or palette change reversible | D-P10, D-P11 |
| Front page led by an illustrated hero and the product shelf | The first screen should sell and orient, not explain the checking process | D-P10 |
| New `shop.html` filterable shelf + chooser | One place where a reader can actually act, filtered by what they cook | D-P10 |
| New `about.html` with four rules and a limits table | Authorship and standards build trust; burying them helps nobody, leading with them loses the reader | D-P10 |
| Reader nav cut 11 → 6 | Eleven links is a dashboard; six is a shop | D-P10 |
| Six drawn format illustrations | Product photography is Program Content and needs a licence review first | D-P12 |
| USDA temperature, storage and outage data in the thermometer guide | The reader's real question is "what am I aiming for", not "what does the listing claim" | D-P14 |
| Disclosure changed to the prescribed first-person sentence | Operating Agreement §5 prescribes it; §6(a) makes a violation a material breach | D-P13 |
| "Compare all five" CTA repointed at `compare.html` | It used to be a paid link to one product — a label that did not match its destination | F-P16 |

**What this pass did not change, deliberately.** No price was published. No rating was published.
No popularity claim was made. No value was inferred. No hands-on testing is implied. Those five
absences are what make the rest of the page credible, and the release gate now enforces four of them
mechanically.

## The 2026-11-20 handoff-integration pass (arena/e0d92902-prod2)

Two parallel sessions (PRs #23 and #25) had been inactive for over eight hours; the coordination
protocol's handoff rule let this session take their work over. Their unique content was
union-merged into the consolidated tree (decision D-P16), conflicts resolved at source, nothing
discarded, both branches preserved on the remote:

| Change | Why it exists | Decision / source |
| --- | --- | --- |
| Redirect-level re-verification of all five short links + same-day re-reads of the compliance pages | Their 2026-11-20 pass verified listing content; this pass verified the redirect chain and the policy pages, so every citation in the register now has a same-day read | `data/p2/verification-2026-11-20.json` (sessions section), F-P07 resolved |
| Three question-shaped guides (dual-vs-single capacity math · leave-in probe in an air fryer · air-fryer gift checks) | More organic entry points, same evidence rules | PR #25 content, D-P16 |
| Analysis page (capacity-to-depth ranking, coverage matrix, funnel, verification ledger) + Design prompt pack page | The brief's decision-support requirement: reviewers see what the data supports and the design briefs before choosing a path | PR #25 content, D-P16 |
| Registers: decision-priority, design-prompts, verification-log; Q-P10..Q-P21 + SG-18..SG-26 rows | Review-gated queues grow; nothing in them is implemented | PR #25 registers, D-P16 |
| Editorial voice-lint gate + settings-derived disclosure sentence in the gate + read-date chips in the register table | Voice rules decay unless enforced; mandated wording and enforced wording cannot drift | PR #25 gates, D-P16 |

ID collisions were resolved by renumbering, not overwriting: PR #25's Q-P14 became **Q-P22**
(main already carried a different Q-P14 from PR #36) and its D-P10 became **D-P16** (main
consumed D-P10..D-P15). Still queued, not implemented: the mobile compare bar (SG-23) and the
portal-v2 board hooks — both stay on the source branches pending an owner decision.

**What is still missing before this can earn money.** The Associates account is unverified (Q-01),
so nothing is known about whether clicks track. Search Console is unverified (Q-P08), so topic
selection has no data behind it. The analytics endpoint has no host (Q-23), so the five event
counters stay in the reader's browser. All three are owner actions, listed on the **Open questions**
page with the discovery route for each.
