# Prod2 — Countercraft

An editorial Amazon affiliate shop built from a verified product register. Tracking ID
`shopnow047c-20`.

The site is **data-driven**: every page is generated from the verified data in `data/*.json` by
`scripts/build_site.py`, and `scripts/verify_site.py` is a release gate that fails the build on
any violation (missing disclosure, missing `rel="sponsored"`, duplicate meta, broken links,
sitemap gaps). Standard library only — no dependencies.

## Quick start

```bash
python3 scripts/build_site.py     # render site/ from data/*.json
python3 scripts/verify_site.py    # release gate (exits non-zero on any violation)
```

## Layout

```
data/            verified product data, source register, suggestions, ledger, articles
scripts/         build_site.py (generator), verify_site.py (release gate)
site/            generated static site (served by GitHub Pages)
.github/workflows/pages.yml   deploy to GitHub Pages on push to main
COORDINATION.md  shared task board
EXECUTIVE_SUMMARY.md  executive summary
DECISIONS.md     decision log (taken + open)
```

## The products

Five submitted `link.amazon` short links, each resolved against its official Amazon listing.
All five tokens are 9-character short-link tokens, not 10-character ASINs; they resolve to real
listings. See `data/products.json` and the **Research Desk** page.

## Compliance

- Disclosure strip under the masthead on every page, repeated in the footer.
- Every outbound Amazon product link is `rel="sponsored"`.
- Product-intent record keeps intended vs. observed in separate fields.
- Privacy-preserving click counter (no cookies); five events; self-hosted `/collect` endpoint.
- Irregularities and unverified values are published blank + flagged on the **Flagged for
  Review** page with source links — never inferred.

## Self-hosted analytics endpoint

The privacy-preserving click counter (`site/assets/analytics.js`) records the five defined
events and POSTs them to a `/collect` endpoint. GitHub Pages is static, so the endpoint is
self-hosted: `server.mjs` (a small Node collector with five-event aggregation) runs locally or
on any Node host. Run `npm start` to serve it, `npm test` to run the endpoint tests together
with the release gate. See `ANALYTICS-ENDPOINT.md`.

See `EXECUTIVE_SUMMARY.md`, `DECISIONS.md`, and the **About** page for sources and methodology.
