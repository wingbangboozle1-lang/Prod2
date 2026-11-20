# Engine guide

The machinery behind this site: a deterministic static-site build plus a
publish gate. The central guarantee is simple — **an unverified fact cannot
reach a published page, and a page that breaks the disclosure or link rules
cannot ship.**

```
data/p2/*.json  ──►  tools/build.py  ──►  docs/            (the published site)
content/pages/*.html ─┘                  │                  │
assets/ (css/js/img) ────────────────────┤                  ▼
data/p2/executive-summary.md ────────────┘         tools/checks.py ──► gate: fail = do not publish
                                                         │
data/p2/executive-summary.md ──► tools/make_executive_summary.py ──► content/pages/executive-summary.html
```

## Commands (clean checkout, standard-library Python 3.11+)

```bash
python3 tools/build.py     # render docs/ from data/ + content/ + assets/, then mirror to the root
python3 tools/checks.py    # the publish gate; exit 0 = green
npm test                   # build + gate + legacy verifier + the endpoint's own contract test
```

Optional (only when changing the social-preview card; needs Pillow):

```bash
python3 tools/make_og.py   # re-render assets/img/og-card.png (typographic brand art)
```

Self-hosted analytics endpoint (deployable, not yet hosted — flag F-19):

```bash
node server.mjs            # serves docs/ and accepts POST /api/events
# then set analytics_endpoint in data/p2/settings.json and rebuild
```

## What the gate checks (tools/checks.py)

| Section | Enforced |
|---|---|
| `pages` | every registered page is built; each has a unique `<title>` (≤ 70 chars) and unique meta description (50–170 chars) |
| `disclosure` | the Associates sentence appears on every page twice — the strip under the masthead and the footer repeat |
| `links` | every `amazon.com/dp/` product link carries `tag=shopnow047c-20` **and** `rel="sponsored nofollow noopener"`; `link.amazon` short links carry `rel="sponsored"` and are never query-stripped or tag-appended; other Amazon links carry `nofollow`; every internal link resolves |
| `facts` | every product's buy URL and listing citation is published; blanks are rendered `— unverified`; intent records keep `intended_asin` and `observed_redirect` as separate fields and the path code is never treated as an ASIN |
| `claims` | no price patterns (`$…`) and no star-rating patterns anywhere (F-02); no banned popularity words ("trending", "best-selling", …) on reader-facing pages (D-19) |
| `copy` | no serving count, footprint claim, speed generalization, cabinet-clearance conclusion or unstated cleaning method that no listing supports; the dishwasher-safe claims name both baskets that carry one |
| `chrome` | the single navigation group ("The work behind it") and the footer directory appear on every page |
| `seo` | canonical + og:image + parseable JSON-LD per page; sitemap covers exactly the built pages; robots.txt points at the sitemap; feed items resolve |
| `publication` | every guide reaches the comparison, the buying guide and its cluster pillars (S-24 rule, automated); the feed covers every guide; the reader-capture form's consent checkbox and gate state match `settings.json`; the Search Console verification meta appears only while a token is configured |
| `endpoint` | the five-event contract agrees across `data/p2/events.json`, `assets/js/measure.js` and `server.mjs`; no superseded or report-only event is accepted; no file names a repository path that does not exist |
| `summary` | `docs/executive-summary.html` is generated from `data/p2/executive-summary.md`; the root `EXECUTIVE_SUMMARY.md` carries the same official sources and the same gate size |
| `mirror` | the repository root byte-matches `docs/` — the tree GitHub Pages serves in legacy "main /" mode |
| `freshness` | `docs/` byte-matches a fresh render from `data/` + `content/` — no stale output can ship |

## How the "no hallucination" rule is enforced

| Layer | Enforcement |
|---|---|
| `data/p2/products.json` | every published value carries `*_source` (register id) and `*_read` (UTC date); nulls are null, never guessed |
| `data/p2/intent-links.json` | intent fields (`intended_asin`, `official_listing_url`, `confirmation_date_utc`, `confirmation_source`) and observation fields (`observed_redirect`, `observed_redirect_history`) are separate structures and are never merged |
| `data/p2/flags.json` | anything unconfirmed is blank on the page **and** flagged with an evidence link |
| `tools/checks.py` | `facts` and `claims` sections fail the build when a cited value disappears, a blank gets filled without a source, or a banned claim slips into copy |
| content rule | manufacturer claims ("±0.5°F", "NIST-certified") are quoted as the listing's statements with dates — never adopted as the site's own |

## Adding a page

1. Add its fragment to `content/pages/<id>.html` (hooks available: `{{products_table}}`,
   `{{facts:P1}}`, `{{buy:P1}}`, `{{chooser}}`, `{{flags_open}}`, `{{questions}}`,
   `{{executive_summary}}`, … — see `tools/build.py` HOOKS).
2. Register it in `PAGES` in `tools/build.py` (path, title, description, section).
3. Run the two commands above. The sitemap, feed (for guides), nav and footer pick it up
   automatically or fail the gate.

## Test count

`tools/checks.py` runs **15 check sections** across the 27 published pages. The engine has no
other entry points; everything the site publishes flows through the build and the gate, and the
optional endpoint has its own contract test in `tests/server.test.mjs`.
