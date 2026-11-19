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

Full source list with links: `data/sources.json` and the **About** page.

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
