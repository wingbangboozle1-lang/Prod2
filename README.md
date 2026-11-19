# Countertop Dispatch — Prod2

An AI-built Amazon affiliate publication for kitchen appliances: five products
checked line by line against official Amazon listings, question-shaped buying
guides, category dashboards, and a public flag list for everything that could
not be verified.

**Live site:** https://wingbangboozle1-lang.github.io/Prod2/

## What is here

| Area | Files | Purpose |
|---|---|---|
| Pages | `index.html`, `products.html`, `comparison.html`, `analysis.html`, `suggestions.html`, `flagged.html`, `compliance.html`, `summary.html`, `guides/`, `category/` | The publication (built output) |
| Content source | `content/**` | Page bodies with front matter — edit these, not the built HTML |
| Build | `tools/build_site.py` | Wraps content fragments in shared chrome (masthead, disclosure strip, nav, footer); emits `sitemap.xml` + `feed.xml` |
| Verification gate | `tools/check_site.py` | 12 checks: disclosure placement, `rel="sponsored"` + tag on every product link, unique titles/descriptions, source-or-flag link in every data-table row, sitemap/feed coverage, internal links, JSON validity, empty campaign ledger, five defined events, flag cross-references |
| Data | `data/*.json`, `data/campaign-ledger.csv` | Machine-readable source of truth: products, submitted links, product-intent (intended vs observed, never merged), events, empty ledger |
| Analytics | `assets/analytics.js`, `tools/analytics-endpoint.md` | Five-event privacy-preserving counter; endpoint not provisioned (events stay local) |
| Policy sources | `content/compliance.html`, `content/flagged.html` | Where each rule and each flag is published |

## Build and check

```bash
python3 tools/build_site.py && python3 tools/check_site.py
```

Both use only the Python standard library. The site is served by GitHub Pages
from the repository root (legacy Pages, `main` branch, `/`).

## House rules (enforced by the gate)

1. **Disclosure strip** sits directly under the masthead on every page and is
   repeated in the footer.
2. **Every** `amazon.com/dp/…` link carries `rel="sponsored"` and
   `?tag=shopnow047c-20` (85 links, all tested live 2026-11-19).
3. **No value without a source.** Every data-table row links to an official
   source or to its flag on `flagged.html`. Blanks stay blank.
4. **Prices, ratings, per-product commission** are withheld by policy and
   flagged (`FLG-P03`–`FLG-P05`) — never inferred.
5. **Intended ≠ observed.** `data/product-intent.json` keeps `intended.*`
   (owner-confirmation only, currently null) separate from `observed.*`.

## Open flags

Eight flags are published on [Flagged for Review](https://wingbangboozle1-lang.github.io/Prod2/flagged.html),
two of them blocking on owner input (FLG-P01 intended-product confirmation,
FLG-P02 short-link compliance status). See `content/suggestions.html` for the
decision menu. Nothing on the site is blocked by them; the site publishes them
instead of hiding them.
