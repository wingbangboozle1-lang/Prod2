# REPO_AUDIT.md — line-by-line repo review, 2026-11-20

Session `arena/86206fb3-prod2` · branch `arena/86206fb3-prod2` · tracking ID `shopnow047c-20`

This is the repo-review half of the brief: what was checked, what was found, what was fixed, and what
is published for human review. Every finding carries an evidence link. Nothing is inferred — where a
value could not be confirmed from an official source it is left blank and flagged. The reader-facing
version of this page is **Flagged for review** on the live site (`flagged.html`), generated from
`data/p2/flags.json`. Flag IDs here are the live register's IDs; they are not renumbered by this pass.

---

## 1. What was reviewed

| Layer | Files | How it was checked |
| --- | --- | --- |
| Product facts and identity | `data/p2/products.json`, `data/p2/intent-links.json` | Every ASIN and submitted short link re-read; title, spec table and breadcrumb compared with the register |
| Policy sources | `data/p2/sources.json` | Each official URL re-read on its stated date (Operating Agreement §5, Program Policies, Commission Income Statement, ASIN definition, FTC, Google Search Central) |
| Generated site | `docs/*.html` (27 pages) | Automated gate (`tools/checks.py`, 12 sections) plus independent scans for broken links, duplicate ids, heading order, missing `alt`, third-party requests and link policy |
| Generator and gate | `tools/build.py`, `tools/checks.py` | Read line by line; two gate sections added (`exposition`, plus the short-link rule) |
| Registers | `data/p2/{flags,questions,suggestions,decisions,events,settings,calendar,editorial}.json` | Cross-reference sweep: every `F-`/`Q-`/`SG-`/`D-` id cited on a page must exist in its register — enforced by the gate |
| Measurement machinery | `assets/js/measure.js`, `server.mjs`, `ANALYTICS-ENDPOINT.md`, `data/p2/events.json` | Event vocabularies compared name by name; endpoint claims traced to a file that exists |
| Deploy configuration | `.github/workflows/pages.yml`, Pages API | Publishing root and what it exposes to the public internet |
| Archived builds | `archive/**` | Reachability from the live host |

## 2. Findings fixed in this pass

| ID | Finding | Evidence | Status |
| --- | --- | --- | --- |
| **F-P22** | Eight files described the analytics endpoint as `analytics-endpoint/server.py`. **No such file has ever been committed.** The only endpoint is `server.mjs`. | [server.mjs](https://github.com/wingbangboozle1-lang/Prod2/blob/main/server.mjs) · [ANALYTICS-ENDPOINT.md](https://github.com/wingbangboozle1-lang/Prod2/blob/main/ANALYTICS-ENDPOINT.md) | **Resolved**: every reference now names `server.mjs`; flag F-19's evidence URL repointed; a gate rule fails the build on any page citing a non-existent local path |
| **Short links as clickable anchors** | `method.html` (5) and `flagged.html` (1) rendered `https://link.amazon/…` as `<a href>` with `rel="sponsored"`. Those codes are *evidence of what the owner submitted*, not the site's product destination, and their compliance status is unresolved (**F-03**/FLG-003). Rendering them as clickable sponsored links implied the site endorses them as the buy path. | [tools/build.py](https://github.com/wingbangboozle1-lang/Prod2/blob/main/tools/build.py) — `normalize_amazon_links` | **Fixed at the generator**: a short-link anchor now renders as inert `<code>`, and the new `exposition` gate section fails the build if one ever comes back |
| **The site shipped no fonts** | `DESIGN_PROMPT.md` specified Fraunces and Inter. Neither was in the repo: `--serif` and `--sans` fell through to `ui-serif`/`-apple-system`, so every page rendered in a system font on every machine. | [assets/css/site.css](https://github.com/wingbangboozle1-lang/Prod2/blob/main/assets/css/site.css) | **Fixed**: both families self-hosted as variable woff2 with their OFL licences, `@font-face` declared, preloaded, and the existing `shop` gate section now checks the files exist |
| **Root-mode publishing** | The Pages API returned `build_type: legacy, source: main, /` — the repository **root** was the publish root, so `data/`, `content/`, `tools/`, `scripts/` and every archived build were readable by anyone who typed the path. | `gh api repos/wingbangboozle1-lang/Prod2/pages` → `"build_type":"legacy","source":{"branch":"main","path":"/"}` | **Mitigated in-repo**: the workflow publishes the `docs/` artifact only, and the new `exposition` gate section fails the build if a source directory, manifest or endpoint file appears inside `docs/`. Flipping the repository setting is a one-time owner action on the next deploy (**F-P19**, **F-P20**) |
| **F-P12** | `DESIGN_PROMPT.md` cited a different register lineage than the live site. | [DESIGN_PROMPT.md](https://github.com/wingbangboozle1-lang/Prod2/blob/main/DESIGN_PROMPT.md) | **Resolved**: design doc synced to the shipped stack |

## 3. Findings published for review, not fixed here

These are open in the register and on `flagged.html`. None of them blocks publication, and each one
names the action that closes it.

| ID | Finding | Why it matters | Evidence |
| --- | --- | --- | --- |
| **F-P23** | The site's five events (`page_view`, `outbound_click`, `guide_read_75`, `category_click`, `feed_click`) and the repo's only endpoint vocabulary do not match — **three would be rejected** by `server.mjs` as written. | Connecting them unchanged would silently under-count. Nothing is lost today because the endpoint is not hosted. Choosing the vocabulary is a decision, not a typo. | [server.mjs](https://github.com/wingbangboozle1-lang/Prod2/blob/main/server.mjs) vs [events.json](https://github.com/wingbangboozle1-lang/Prod2/blob/main/data/p2/events.json) |
| **F-19** | The endpoint is deployable but not hosted. | No click figure on this site is a measurement yet. | [ANALYTICS-ENDPOINT.md](https://github.com/wingbangboozle1-lang/Prod2/blob/main/ANALYTICS-ENDPOINT.md) |
| **F-01** | No official source maps these ASINs to a commission category. | Every product-level rate is published blank, never inferred from the Kitchen/Home band. | [Commission Income Statement](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |
| **F-03** | The supplied short links carry no `tag=` parameter. | Clicks through them cannot be attributed; the site publishes tagged Special Links built from verified ASINs instead. | [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) |
| **F-57 / F-58** | Tracking-ID registration and the one-link-per-product test are confirmable only inside Associates Central. | The site claims no revenue, no ranking and no attribution. | [Amazon tag help](https://www.amazon.com/b?ie=UTF8&node=51812349011) |
| **F-13 / F-14** | Search Console verification and the reader-capture consent basis are owner actions. | The capture form ships dark and sends nothing. | [settings.json](https://github.com/wingbangboozle1-lang/Prod2/blob/main/data/p2/settings.json) |
| **F-08 · F-26 · F-44 · F-66** | P2 and P3 listings state a value two ways (functions, title segments, size-family variants). | The site publishes one string with its read date and keeps the history; it never synthesizes an average. | [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) · [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) |
| **F-49 · F-29 · F-17** | Default offers can be used items; carousel membership changes between reads; carousel prices belong to neighbouring ASINs. | Standing buyer warnings, published rather than smoothed away. | [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) |

Standing rules that are **not** defects, published so a reviewer sees them: **F-02** (prices and
ratings are never published), **F-15** (no popularity claims without a dated official snapshot),
**F-67** (short-link codes are not ASINs), **F-17** (imagery/price context on listings).

## 4. Link and compliance audit of the built site

| Check | Result |
| --- | --- |
| Outbound `/dp/` product links carrying `tag=shopnow047c-20` | all of them — 0 untagged |
| Product links without `rel="sponsored"` | 0 |
| `link.amazon` short links rendered as a clickable destination | **0** (was 6) — all quoted as inert `<code>` |
| Amazon links to non-product pages | `rel="nofollow noopener"` |
| Broken internal links | 0 across all published pages |
| Third-party requests (font CDN, analytics, social) | 0 |
| Pages missing the disclosure strip or its footer repeat | 0 |
| Duplicate `id` / nested `<p>` / dangling flag references | 0 |
| Source directories reachable inside the published artifact | 0 (new gate section) |
| Images without `alt` | 0 |

## 5. How to reproduce every check

```bash
python3 tools/build.py     # render docs/ from data/p2/ + content/pages/
python3 tools/checks.py    # 12-section publish gate
npm test                   # endpoint tests
```

## 6. What this audit does **not** claim

- It does not claim these products are good. Nobody here has cooked with them (**D-06**).
- It does not claim any click, order or commission. No Associates report has been read (**F-57**).
- It does not claim prices or ratings. They are deliberately unpublished (**F-02**).
- It does not claim the imagery is the product. It is illustration (**F-17** lineage).
- It does not claim the short links are invalid. Their compliance status is unresolved (**F-03**).
