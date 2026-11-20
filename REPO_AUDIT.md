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
| **Root-mode publishing** | The Pages site is in *legacy* mode with the source set to the repository **root** (`build_type: legacy`, `source: main /`). Measured on 2026-11-20: `data/` 42 files, `content/` 27, `tools/` 5, `scripts/` 4, `tests/` 1, `archive/` 121 — **196 source files** reachable by an anonymous reader who types the path. Verified by fetching `https://…/Prod2/data/p2/settings.json`, which returned the register as JSON. `robots.txt` is a crawler convention, not access control. | `gh api repos/wingbangboozle1-lang/Prod2/pages`; `python3 tools/root_mirror.py --report`; the live GET above | **Mitigated in-repo, not solved**: the workflow publishes the `docs/` artifact only; a new `exposition` gate section refuses any source directory inside `docs/`; `tools/root_mirror.py` writes a canary into each source directory and prints the exact exposure count. **The fix is one owner setting** — Settings → Pages → Source: GitHub Actions. A token-scoped `PUT` to `build_type: workflow` returns 403, so this session cannot flip it (**F-P19**, **F-P20**) |
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
| Source files reachable on the live host (root mode) | **196 — open, F-P19/F-P20**, owner setting |
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

---

# Addendum — session arena/e1dbef32-prod2 (2026-11-20, editorial sourcing + gate additions)

Same rule as the audit above: everything checked, nothing inferred, and the
reader-facing copy of every finding lives on `flagged.html`. Permalinks below are
to `main` so a reviewer can click them after the merge.

## 1. What was read, and what it produced

| Official source (read 2026-11-20) | What was checked | Where it landed |
| --- | --- | --- |
| [USDA FSIS — Safe Minimum Internal Temperature Chart](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart) (page dated Apr 14, 2025) | Every row of the table transcribed verbatim, including the "Ground Poultry 165 degrees F" row that carries no Celsius figure, and the four standing guidelines (Clean, Separate, Cook, Chill) | `guide-safe-temp-chart.html`, `S-FSIS-CHART`, `data/p2/verification-2026-11-20-e1dbef32.json` (V-READ-3) |
| [USDA FSIS — Leftovers and Food Safety](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety) (page dated Jul 31, 2020) | Both chunks of the factsheet; the 3–4 day / 3–4 month storage figures, the two named causes of foodborne illness, cool-rapidly and refreezing conditions, the reheat-to-165°F instruction, and the fact that it names a saucepan, a microwave and an oven — and no air fryer | `guide-leftovers.html`, `article-danger-zone.html`, `S-FSIS-LEFTOVERS` (V-READ-2) |
| [USDA FSIS — "Danger Zone" (40°F - 140°F)](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/danger-zone-40f-140f) (page dated Jun 28, 2023) | The 40–140°F band and the 20-minute doubling sentence, the 2-hour / 1-hour rule, the hot-holding device list, the 325°F oven statement, the 165°F reheat line | `article-danger-zone.html`, `S-FSIS-DANGER` (V-READ-1) |
| [Nebraska Extension — Food Safety Tips for Air Fryers](https://food.unl.edu/free-resources/newsletters/food-safety-tips-electric-air-fryers/) (peer-reviewed, updated 2025) | Convection definition, overfill warning, thermometer-only sentence, placement sentence, cleaning sentence, the "check the operator's manual" instruction, its temperature table | three new pages, `S-UNL-AIRFRYER` (V-READ-4) |
| [Google Search Central blog, 2023-08-08](https://developers.google.com/search/blog/2023/08/howto-faq-changes), [structured-data gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery), [documentation changelog](https://developers.google.com/search/updates#removing-faq-rich-result) | Whether FAQ rich results are still a thing for a site like this, and what Google's own list of supported features says today | `D-P23`, `F-P27`, `Q-P20`, `SG-48`, corrected `DESIGN_PROMPT.md` |

**Secondary-source material kept out of the site.** The May 7, 2026 date and the
Search Console/API phase-out dates for FAQ rich results appear only in trade
coverage; no official Google page in this sandbox states them, so nothing on the
site asserts them. What the site asserts is what the three Google pages above
actually say (V-READ-7 `not_observed`).

## 2. Defects found in the repo this pass

| ID | Finding | Status |
| --- | --- | --- |
| **F-P25** | `content/pages/guides.html` closed its lede and continued the sentence outside the paragraph with a stray `</p>`. No gate counted paragraph balance, so a broken first screen shipped unnoticed. | **Resolved** — fragment fixed, and `validity` now compares `<p>` openings with `</p>` closings on all 33 pages (the rule reproduced the defect before the fix) |
| **F-P27** | `DESIGN_PROMPT.md` promised "FAQPage + Article structured data" on every guide. The generator emitted Article only, and nothing noticed — documentation asserting a shipped state the code does not have (the F-P12 class). | **Resolved** — markup now derived from visible blocks and gated against them; the brief rewritten to state what ships and what the search benefit is not |
| **F-P29** | The Product node hard-coded `"gtin13": null` and filled a missing brand with the literal string `"unknown"`. An invented value inside machine-readable data. Latent today (all five brands were read), a defect the first time a read came back empty. | **Resolved** — unread fields are omitted; the evidence rule now covers JSON-LD (D-P24) |
| **F-P28** | `site/` (25 tracked files, titled "Countercraft …") and `archive/countertop-dispatch/` remain reachable by URL while Pages serves the repository root, with no canonical pointing at this site. A recursive grep for a currency pattern found no prices there, so this is brand and index dilution, not a disclosure breach. | **Open** — mitigated by a `robots.txt` disallow for both prefixes; the real fix is the owner's Pages-source action (F-P19), or a recorded decision to keep them reachable (Q-P21, SG-52) |
| **F-P30** | The 14-day cadence was unauditable: six reader pages shipped on 2026-11-19/20 while `next_due_utc` stayed at 2026-12-03, and queue slot 1 promised to answer a ritual question from a source (the listings) that states features, not rituals. | **Resolved as machinery** — a `cadence` gate section now fails an overdue slot, a dangling cluster reference, a stale long-read word count, or a publish that does not advance the schedule; slot 1 is marked blocked on Q-P18 instead of pretending to be on time |

Cross-check that no prior claim was broken: `data/p2/products.json` was not edited;
no price, rating or commission value was added anywhere; the five intent records
keep intended-ASIN and observed-redirect fields separate; `link.amazon` strings are
still rendered as inert `<code>` (the `exposition` section enforces it).

## 3. Gates and commands a reviewer can run

```bash
python3 tools/build.py      # 33 pages -> docs/, mirrored to the root for legacy Pages mode
python3 tools/checks.py     # 16 sections: pages, disclosure, links, validity, facts, claims,
                            # chrome, seo, faq, publication, longreads, cadence, shop,
                            # exposition, measurement, freshness
python3 scripts/verify_site.py
npm test                    # endpoint tests
```

## 4. What this addendum does **not** claim

- It does not claim the five listings were re-read by this session; two parallel
  sessions did that on 2026-11-20 and their records stand (F-P24).
- It does not claim any traffic, click, order or commission: the endpoint is still
  unhosted and Search Console is still unverified.
- It does not claim the new pages make these products good — no unit has been used
  (D-06), and the pages say so in their own text.
- It does not claim the extension's Celsius figure is a typo; it claims only that
  two official pages disagree and that this site publishes the figure they share.
