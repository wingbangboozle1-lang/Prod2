# Engine guide

The publication is generated from structured registers and page fragments. Build-time validation catches known formatting, link, disclosure, sourcing and SEO failures. It does **not** prove every source remains current, validate Amazon Associates enrollment, supply missing owner-controlled data, or replace editorial/compliance review.

```text
data/p2/*.json + content/pages/*.html + assets/
        └── tools/build.py ──► docs/ (generated publication)
                    └── tools/checks.py ──► release gate
```

## Commands

```bash
python3 tools/build.py
python3 tools/checks.py
npm test
```

Python build and checks use the standard library. `npm test` also runs the independent publication verifier and the self-hosted Node endpoint tests. Optional Open Graph image generation (`python3 tools/make_og.py`) requires Pillow.

The analytics service is Node, not Python. It is tested but is not hosted; do not configure the browser to send data to it until the event vocabulary and hosting/privacy decisions are resolved.

```bash
node server.mjs
```

## Current release-gate sections

`tools/checks.py` reports all sections, accumulates failures, and exits non-zero if any check fails.

| Section | Checks |
|---|---|
| `pages` | All registered pages exist; titles and descriptions are unique and within configured limits. |
| `disclosure` | Associates disclosure strip and footer repeat are present on every page. |
| `links` | Amazon product URLs carry the tracking tag and sponsored relationship; internal references resolve. |
| `validity` | Markup checks, duplicate IDs, fragments and register cross-references. |
| `facts` | Product listings are cited and dated; blanks are marked unverified; intent and observed redirect fields stay separate. |
| `claims` | Prices/ratings are withheld and prohibited popularity claims are absent from reader-facing copy. |
| `chrome` | Reader navigation, one “The work behind it” group and footer directory are present. |
| `seo` | Canonical, social metadata, JSON-LD, sitemap, robots and feed consistency. |
| `shop` | Product shelf, cards, images, About page and absence of hands-on-test claims. |
| `publication` | Guide-cluster/pillar links, RSS coverage, capture gate and Search Console token consistency. |
| `exposition` | `docs/` artifact avoids source directories and clickable submitted short links; source and generated text are checked for conflict markers. |
| `measurement` | Compares event declarations with the endpoint. The current mismatch is deliberately printed as F-P23/Q-P14 rather than concealed. |
| `freshness` | Generated `docs/` matches a fresh build from source inputs. |

A green gate is not proof that a listing has not changed since its recorded read date. Re-fetch official sources before changing factual claims and update the dated verification record. Current product/source records live in `data/p2/products.json`, `data/p2/sources.json` and `data/p2/verification-2026-11-20.json`.

## Product-data rules

- Each factual value should have a source-register ID and read date. Null/unknown values remain blank in reader-facing tables and are flagged; do not infer them.
- `data/p2/intent-links.json` preserves intended ASIN/listing/confirmation provenance separately from the observed redirect and its history.
- The owner-submitted short links are evidence, not confirmed compliant buy paths. Their status remains unresolved (F-03). Published buy paths use the site's tagged Amazon `/dp/` Special Links, with `rel="sponsored"`.
- Keep prices, availability, ratings, review counts, commissions, orders and revenue blank unless a policy-permitted source and dated provenance are recorded. The campaign ledger is intentionally empty until authorized first-party reports exist.

## Known conditions that a green build does not resolve

1. **Pages source mode:** the Pages API reports legacy `main /` root publishing (checked 2026-11-20). The deployment workflow uploads `docs/`, but it does not switch the active Pages source. Repository source and archives remain fetchable by path; see F-P19/F-P20. Repository-admin action is required to select GitHub Actions and verify source URLs return 404.
2. **Analytics vocabulary:** three site events are not accepted by `server.mjs`; F-P23/Q-P14/SG-41. Endpoint is not hosted and the browser sends nothing in the current configuration.
3. **Search Console and Associates Central:** ownership/report data are not available to this build. Search Console property verification, sitemap submission and one-link-per-product tracking tests remain owner-account tasks.
4. **Brand clearance and other open questions:** see Questions and Flagged for Review. Do not treat a provisional name or unresolved item as cleared.

## Adding a page

1. Add its fragment to `content/pages/<id>.html` (hooks available: `{{products_table}}`,
   `{{facts:P1}}`, `{{buy:P1}}`, `{{chooser}}`, `{{flags_open}}`, `{{questions}}`, … —
   see `tools/build.py` HOOKS).
2. Register it in `PAGES` in `tools/build.py` (path, title, description, section).
3. Run the two commands above. The sitemap, feed (for guides), nav and footer pick it up
   automatically or fail the gate.

## Test count

`tools/checks.py` runs **14 check sections** covering 70+ individual assertions across
30 built pages (the core pages, the guides hub, 10 guide pages and 2 long reads). The engine has no other entry points; everything the site publishes flows
through the build and the gate.

---

1. Add reader-facing content under `content/pages/` and register it in `PAGES` in `tools/build.py`.
2. Add source-backed data to `data/p2/` as appropriate; never fabricate missing values.
3. Rebuild and run the complete gate and `npm test`.
4. Review the generated page, navigation, sitemap, feed, disclosure and the relevant source links before publishing.
