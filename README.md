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
server.mjs       optional self-hosted aggregate-only event endpoint (serves site/; not deployed publicly)
tests/           Node integration tests for the endpoint (npm test)
.github/workflows/pages.yml   deploy to GitHub Pages on push to main
.github/workflows/verify.yml  build + release gate + reproducibility check on every push/PR
archive/counter-notes-v1/     the root-level site from PR #1 (kept unchanged; not published)
archive/counter-notes-docs/   the generated "Counter Notes" site from PRs #2-#5 (archived at consolidation; not published)
archive/counter-edit-build/   a parallel "The Counter Edit" build from session sess-prod2-a1 (archived at consolidation; not published)
COORDINATION.md  shared task board
EXECUTIVE_SUMMARY.md  executive summary
DECISIONS.md     decision log (taken + open)
```

**What GitHub Pages serves:** the repository **root**, in legacy "main /" mode. The build mirrors
`docs/` to the root, so the live URL (https://wingbangboozle1-lang.github.io/Prod2/) serves exactly
the gated publication. `tools/checks.py` fails if the mirror drifts from `docs/` by a single byte,
because a stale root page would be the page readers actually see.

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

## Design and imagery

The publication is styled by a single stylesheet (`assets/css/site.css`) and illustrated entirely
with its own generated artwork (`tools/make_art.py`). There is no product photography: Amazon's IP
License governs listing images, and a photograph the site did not take would break its evidence
rule. `DESIGN_PROMPT.md` records the shipped system (palette, type stack, page types, and the five
things a future pass must not undo).

## The products

Five submitted `link.amazon` short links, each resolved against its official Amazon listing.
All five tokens are 9-character short-link tokens, not 10-character ASINs; they resolve to real
listings. See `data/p2/products.json` and the **Research Desk** page.

## Compliance

- Disclosure strip under the masthead on every page, repeated in the footer.
- Every outbound Amazon product link is `rel="sponsored"`.
- Product-intent record keeps intended vs. observed in separate fields.
- Privacy-preserving click counter (no cookies); five events; self-hosted `/collect` endpoint.
- **Prices and star ratings are not published.** This is a checked rule, not caution: Associates
  Program Policies 2(b) permits prices only when Amazon serves the link displaying them or via
  Creators/PA API, and Participation Requirements 6(t) permits ratings only via Creators/PA API.
  Re-read 2026-11-20; recorded as decision D-P10; a gate check fails the build if either appears.
- Irregularities and unverified values are published blank + flagged on the **Flagged for
  Review** page with source links — never inferred.

## Self-hosted analytics endpoint

The privacy-preserving click counter (`site/assets/analytics.js`) records the five defined
events and POSTs them to a `/collect` endpoint. GitHub Pages is static, so the endpoint is
self-hosted: `server.mjs` (a small Node collector with five-event aggregation) runs locally or
on any Node host. Run `npm start` to serve it, `npm test` to run the endpoint tests together
with the release gate. See `ANALYTICS-ENDPOINT.md`.

See `EXECUTIVE_SUMMARY.md`, `DECISIONS.md`, and the **About** page for sources and methodology.

## Live site — Prod2 publication (`docs/`)

GitHub Pages serves the `docs/` folder of `main`, so this publication **is the live site**
(generated by `tools/build.py`, gated by `tools/checks.py` — 9 sections). It carries the deeper review registers
(`data/p2-*.json` + `data/{intent-links,flags,questions,decisions,events,settings}.json`):
intent records with dated redirect histories, flags split open/resolved/standing, question
and suggestion registers with recommendations, and the five-event campaign ledger with the
official attribution windows. The 2026-11-19 publication pass (D-P07) rebuilt the reader-facing
site as a shop-first publication: product cards before data on the front page, a guides hub with
two clusters and a seasonal desk (`data/p2/calendar.json`), eight question-shaped guides on a
14-day cadence, RSS subscribe affordances, Search Console readiness (token slot in `settings.json`),
and a consent-gated question form that ships dark until its privacy basis exists (F-P07).
The Countercraft `site/` build is preserved and deployable via the Actions workflow. See the
integration addendum in `COORDINATION.md`.
