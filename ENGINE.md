# Engine guide

The machinery behind this site: a deterministic static-site build plus a
publish gate. The central guarantee is simple — **an unverified fact cannot
reach a published page, and a page that breaks the disclosure or link rules
cannot ship.**

```
data/*.json  ──►  tools/build.py  ──►  docs/            (the published site)
content/pages/*.html ─┘                  │
assets/ (css/js/img) ────────────────────┤
                                         ▼
                               tools/checks.py  ──►  gate: fail = do not publish
```

## Commands (clean checkout, standard-library Python 3.11+)

```bash
python3 tools/build.py     # render docs/ from data/ + content/ + assets/
python3 tools/checks.py    # the publish gate; exit 0 = green
```

Optional (only when changing the social-preview card; needs Pillow):

```bash
python3 tools/make_og.py   # re-render assets/img/og-card.png (typographic brand art)
```

Self-hosted analytics endpoint (deployable, not yet hosted — flag F-19):

```bash
python3 analytics-endpoint/server.py --port 8787
# then set analytics_endpoint in data/p2/settings.json and rebuild
```

## What the gate checks (tools/checks.py)

| Section | Enforced |
|---|---|
| `pages` | every registered page is built; each has a unique `<title>` (≤ 70 chars) and unique meta description (50–170 chars) |
| `disclosure` | the Associates sentence appears on every page twice — the strip under the masthead and the footer repeat |
| `links` | every `amazon.com/dp/` product link carries `tag=shopnow047c-20` **and** `rel="sponsored nofollow noopener"`; `link.amazon` short links carry `rel="sponsored"` and are never query-stripped or tag-appended; other Amazon links carry `nofollow`; every internal link resolves **and** every `page.html#anchor` points at an id that exists on that page |
| `editorial` | reader pages are linted for filler/boilerplate phrasing and for hedging that reads as AI copy; the two register tables that publish dated figures (`products.html`, `compare.html`) must carry a literal `read YYYY-MM-DD` next to them |
| `facts` | every product's buy URL and listing citation is published; blanks are rendered `— unverified`; intent records keep `intended_asin` and `observed_redirect` as separate fields and the path code is never treated as an ASIN |
| `claims` | no price patterns (`$…`) and no star-rating patterns anywhere (F-02); no banned popularity words ("trending", "best-selling", …) on reader-facing pages (D-19) |
| `chrome` | the single navigation group ("The work behind it") and the footer directory appear on every page |
| `seo` | canonical + og:image + parseable JSON-LD per page; sitemap covers exactly the built pages; robots.txt points at the sitemap; feed items resolve |
| `freshness` | `docs/` byte-matches a fresh render from `data/` + `content/` — no stale output can ship |

## How the "no hallucination" rule is enforced

| Layer | Enforcement |
|---|---|
| `data/p2/products.json` | every published value carries `*_source` (register id) and `*_read` (UTC date); nulls are null, never guessed |
| `data/p2/intent-links.json` | intent fields (`intended_asin`, `official_listing_url`, `confirmation_date_utc`, `confirmation_source`) and observation fields (`observed_redirect`, `observed_redirect_history`) are separate structures and are never merged |
| `data/p2/flags.json` | anything unconfirmed is blank on the page **and** flagged with an evidence link |
| `data/p2/verification-log.json` | each dated re-check (who ran it, what it read, what it showed) is published on the analysis page, so a "verified" claim is always a dated one |
| `data/p2/suggestions.json` | proposals carry 2–3 `paths` (change / upside / downside / cost / unlocks) plus one marked recommendation, and **no** owner field is invented — `owner_decision` stays absent until a human sets it |
| `data/p2/questions.json` | each open question records what is known, what is missing, what it gates, who can answer and the conservative default while it stays unanswered |
| `tools/checks.py` | `facts` and `claims` sections fail the build when a cited value disappears, a blank gets filled without a source, or a banned claim slips into copy |
| content rule | manufacturer claims ("±0.5°F", "NIST-certified") are quoted as the listing's statements with dates — never adopted as the site's own |

## Adding a page

1. Add its fragment to `content/pages/<id>.html` (hooks available: `{{products_table}}`,
   `{{product_cards}}`, `{{guide_shelf}}`, `{{categories_row}}`, `{{trust_rail}}`,
   `{{facts:P1}}`, `{{buy:P1}}`, `{{chooser}}`, `{{comparison_cta}}`, `{{flags_open}}`,
   `{{questions}}`, `{{questions_board}}`, `{{suggestions}}`, `{{suggestions_board}}`,
   `{{priority_board}}`, `{{capacity_ranking}}`, `{{coverage_matrix}}`, `{{funnel}}`,
   `{{decision_board}}`, `{{verification_ledger}}`, `{{flag_stats}}`, `{{design_pack}}`, … —
   see `tools/build.py` HOOKS).
2. Register it in `PAGES` in `tools/build.py` (id, file, title, description, nav section). A
   guide additionally goes in `GUIDE_IDS` / `GUIDE_LINKS`; the guide shelf renders from those
   lists and fails the build if the fragment file is missing, so a page and its entry point cannot
   drift apart.
3. Run the two commands above. The sitemap, feed (for guides), nav, the mobile comparison bar and
   the footer pick it up automatically or fail the gate.

## Test count

`tools/checks.py` runs **9 check sections** covering 70+ individual assertions across
27 pages. The engine has no other entry points; everything the site publishes flows
through the build and the gate. The build also mirrors `docs/` to the repository root because
this repo's Pages is in legacy root mode (INT-07) — the mirror is purged and rewritten on every
build, so hand-edits to root copies of generated pages are lost by design.
