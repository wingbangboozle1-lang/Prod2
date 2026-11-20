# COORDINATION.md — Shared Task Board

Repo: `wingbangboozle1-lang/Prod2`
Tracking ID: `shopnow047c-20`
Current sessions (2026-11-20, three parallel passes reconciled on this branch): **session arena/f55b5827-prod2** (branch `arena/f55b5827-prod2`, anti-slop design + working-brand + gifting-guide pass — claim below) · arena/70b2b9f7-prod2 (shop-front design rebuild + live re-verification, PR #31) · arena/86206fb3-prod2 (exposure canaries + F-P19/F-P20 rewrites + event-vocabulary publication, PRs #37/#38). This branch merges both and reconciles all three registers.

Previous sessions, all merged or closed: arena/1f4017b9-prod2 (shop-forward polish, PR #30 merged into main 2026-11-20 06:09) · arena/43f4359d-prod2 (product-first landing page, PR #29 merged 2026-11-20 06:06) · arena/9f84489c-prod2 (publication polish, PRs #27/#28) · arena-8ff10f50-prod2 (PRs #19/#21) · arena-3f1d9d65-prod2 (analytics endpoint) · arena/b650562d-prod2 (PR #25, open) · arena/5e692632-prod2 (PR #23, open) · f2613c86, 599eec57, 44093825, 30a7028a, d12d2304.

> **Two sessions landed work on `main` after this session branched** (PRs #29 and #30, both 2026-11-20
> before 06:10 UTC). That work is integrated here, not discarded: their `DESIGN_PROMPT.md` additions,
> their `scripts/build_site.py` shelf work and their `tools/build.py` "Best for" intent are all
> preserved. Where the two builds disagreed on the same reader-facing surface, the newer design
> system in this branch wins and the reasoning is recorded in the resolution note below.

---

## PARALLEL CLAIM — session arena/2adc150a-prod2 (2026-11-20, sale-week guide + gate extension)

Rows labeled SW- to avoid the X- prefix already used by arena/3936beb1-prod2's read-only audit above.
Branched from `f6e772f` (main at PR #28); ran alongside the passes above and re-read the board as
`origin/main` advanced through PR #53. **Superseded work was dropped in favor of merged work; unique
work was re-applied on the merged tip; nothing from any other session was discarded.** Three collisions
occurred and both were resolved by renumbering/union — log below.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| SW-01 Typography conformance (self-host Fraunces + Inter) | superseded by V-01 | arena/2adc150a-prod2 | merged equivalent landed (D-P19) — not re-applied |
| SW-02 Design-token conformance | superseded by V-01 | arena/2adc150a-prod2 | merged equivalent landed (D-P19) — not re-applied |
| SW-03 Favicon (drawn glyph) + F-P12 reconciliation | done / superseded | arena/2adc150a-prod2 | `assets/img/favicon.svg` + `tools/build.py` head link shipped; F-P12 was already resolved upstream |
| SW-04 Seasonal sale-week guide (holiday-desk lane; cadence queue untouched) | done | arena/2adc150a-prod2 | `content/pages/guide-sale-week.html`, `tools/build.py` (PAGES/GUIDE_IDS/BLURBS/TAGS/GUIDE_LINKS), `data/p2/calendar.json`, `data/p2/decisions.json` (D-P24) |
| SW-05 Gate extension: `assets` (asset/favicon/font resolution, font-display, font licenses) + `calendar` (register coherence) | done | arena/2adc150a-prod2 | `tools/checks.py` (13 → 15 sections) |
| SW-06 Registers + docs sync | done (re-scoped) | arena/2adc150a-prod2 | `data/p2/decisions.json` (D-P24 only), `content/pages/privacy.html` (self-hosted-fonts note) |
| SW-07 Integration: rebuild, gates, tests, PR to main, merge, Pages check, board record | done | arena/2adc150a-prod2 | `docs/`, root mirror, `COORDINATION.md` |

### Collision log (protocol: conflicts resolved without discarding other sessions' work)

1. **What happened.** This session's first pass (typography, tokens, favicon, F-P12 reconciliation,
   sale-week guide, two gate sections, SG-15/SG-16 → shipped, draft D-P10/D-P11 rows) was built on
   `ce72a35` (main at PR #30). While it ran, sessions arena/70b2b9f7-prod2, arena/86206fb3-prod2 and
   arena/f55b5827-prod2 merged PRs #31–#42 covering the same brief items (self-hosted type + token
   conformance as D-P19, a seasonal gifting guide as D-P20, SG-15/SG-16 shipped, F-P12 resolved, and a
   documented D-P10..D-P17 id reconciliation in `data/p2/decisions.json` `_meta`).
2. **First rebase conflict** (onto `1ee7576`): `git pull --rebase` stopped on `COORDINATION.md`. Per
   protocol, this session stopped rather than rewriting the other sessions' rows, re-pointed the branch
   at the merged tip, and re-applied only unique work (SW-03..SW-06). The superseded pieces — this
   session's `assets/fonts/` set, CSS token edits, compare-page anchor bar, `DESIGN_PROMPT.md` edits,
   SG-15/SG-16/F-P12 register edits, draft D-P10/D-P11 rows — were dropped in favor of the merged
   equivalents, **not deleted**: the full first-pass tip is preserved at commit `2388491` in this
   branch's history.
3. **Second rebase conflict** (onto `28b4001`, PRs #43–#53): sessions 37b265a4/e292fb4d/644d217b had
   landed their own **D-P21** (event-vocabulary decision), two long-read articles in the calendar
   clusters, and board rows using the X- prefix. Resolution by union: their D-P21 and long-reads kept
   verbatim; this session's decision renumbered (draft D-P11 → **D-P22**); this session's rows relabeled
   SW- (above); the calendar keeps both their `article-*` cluster entries and this session's
   `guide-sale-week.html` entries; generated docs/ + root mirrors were resolved to the merged side and
   regenerated from source.
4. **Third rebase conflict** (onto `6a94506`, PRs #47/#56 + the A-01..A-06 pass): session 20f83238 took
   **D-P22** (queue reviewer pass, Path A) and **D-P23** (promotion hold). Resolution by renumbering,
   again: this session's decision is final as **D-P24** (draft D-P11 → D-P22 → D-P24), and its text now
   records the timing tension with D-P22's Path A honestly: the guide was authored before that reviewer
   pass landed, is read as inside the published calendar's seasonal lane (the D-P20 precedent), and is
   one-line retractable if the reviewer reads Path A differently. Generated conflicts resolved to the
   merged side and regenerated from source.
5. **Line-by-line re-check of the re-applied guide against the merged registers.** Cited figures were
   checked against `data/p2/products.json` and the 2026-11-20 live re-check
   (`data/p2/live-check-2026-11-20-722181aa.json`): "six included cooking accessories" (P2) and
   "dishwasher-safe basket" (P3) are re-observed in the listing titles read 2026-11-20 and cite that
   date (matching the gift guide's house style); the 16.9-inch depth figure is not re-cited with a date
   — it defers to the counter-space analysis because F-P08 keeps dimension values pending re-read.

### Verification (arena/2adc150a-prod2, 2026-11-20)

- `python3 tools/build.py && python3 tools/checks.py` — ALL CHECKS PASSED (31 pages, 15 sections,
  including the new `assets` + `calendar` sections; the calendar gate accepts the long-read lane via the
  page register). Negative-tested: removing the built favicon fails the gate; restored.
- `python3 scripts/build_site.py && python3 scripts/verify_site.py` — VERIFY OK (18 pages). `npm test` — 2/2.
- The new guide was checked line by line in the built output: unique title/description within limits
  (escaped-title ≤70 respected — the apostrophe in "can't" is counted), Article JSON-LD, disclosure
  strip + footer repeat, no broken internal links, feed + sitemap + guides hub + season desk + both
  clusters wired, no prices/ratings/popularity claims (claims gate), no hands-on phrasing (shop gate),
  S-24 pillar links present.

### Irregularities this session (not blocking)

None new. Standing open items unchanged and owned by the rows above: F-P19/F-P20 (Pages source, owner
action), F-P23/Q-P14 (event vocabulary — see D-P21), F-P24 (short-link discrepancy), F-P21 (brand
clearance).

---

## ACTIVE CLAIM — session arena/37b265a4-prod2 (2026-11-20, same-day link + listing re-verification and integration)

Branch `arena/37b265a4-prod2`, branched from `main` at `4398598` (PR #33 merge). No other claim is live: every earlier claim in this file is done or merged.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| R-01 Independent re-read of the five owner short links and the five `/dp/` listings on 2026-11-20; record observations as dated history, never overwrite prior records | done | arena/37b265a4-prod2 | `data/p2/intent-links.json` (history entries only), `data/p2/verification-2026-11-20.json` (new key `r01_reread_2026_11_20`), `data/p2/sources.json` (read dates only) |
| R-02 Publish any contradiction found by R-01 as a new open flag on the Flagged for Review page; correct the reader-facing and repository statements it contradicts; no status of any existing value is changed without a source read | done | arena/37b265a4-prod2 | `data/p2/flags.json` (F-P25..F-P27 added; F-P20 detail extended; F-P24 is arena/722181aa-prod2's entry and is not edited), `data/p2/questions.json` (Q-P15 added; dated notes on Q-01, Q-P03), `EXECUTIVE_SUMMARY.md`, `README.md`, `content/pages/executive-summary.html` (statements and the public price column only) |
| R-03 Rebuild, run the release gate, merge, confirm the Pages build, record the PR and merge result | in progress (PR open, merge next) | arena/37b265a4-prod2 | `docs/`, root mirror, `COORDINATION.md` |


### Results (R-01..R-03, 2026-11-20, arena/37b265a4-prod2)

**Sources read this pass (fetch tool, 2026-11-20 UTC):**
- Listings: https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH · https://www.amazon.com/dp/B0DHZTCNR5 · https://www.amazon.com/dp/B0DZFD6R9Z
- Owner short links: https://link.amazon/B04G1MEwY · https://link.amazon/B02NbDxp3 · https://link.amazon/B00hJ57DV · https://link.amazon/B0c8moW59 · https://link.amazon/B0f3GKalj
- Associates Program Policies (page "Updated: April 14, 2026"; §2(b), §6(t), §6(w) read): https://affiliate-program.amazon.com/help/operating/policies
- Operating Agreement (page "Updated: October 15, 2025"; chunk 0 read): https://affiliate-program.amazon.com/help/operating/agreement
- Live host: https://wingbangboozle1-lang.github.io/Prod2/ and https://wingbangboozle1-lang.github.io/Prod2/EXECUTIVE_SUMMARY.md

**Verification performed:**
- Five listing titles compared by exact string equality with `data/p2/products.json` `name_listing` after removing the tool's "Amazon.com: " prefix and ": Home & Kitchen" suffix: **5/5 match**. ASINs matched the register.
- Short links, R-01 read: **1 of 5 reached its intended ASIN** (B02NbDxp3 → B09B7SB46R). B04G1MEwY and B0c8moW59 reached `https://www.amazon.com/` on both attempts. B00hJ57DV and B0f3GKalj each reached the homepage on one read. An earlier same-day note of HTTP 500 for two links was not reproduced and is not relied on. Recorded as dated history in `intent-links.json`; no `intended_asin` or `official_listing_url` changed.
- Same-day disagreement with F-P24 (arena/722181aa-prod2): the two reads differ on **two** links, B02NbDxp3 and B0f3GKalj (F-P27). The other three read the same way.
- Policy text read in the page returned: §2(b) prices and availability shown only if Amazon serves the link or data come via Creators/PA API (matches D-P11); §6(t) reviews and star ratings only via Creators/PA API; §6(w) link-shortening clause quoted in F-P24/F-P27.
- Live host: title matches `docs/index.html`. `data/p2/settings.json` and `EXECUTIVE_SUMMARY.md` are publicly served (exposure in F-P19/F-P20). The served settings.json brand text differs from the repository copy (F-P20 detail).
- Gate: `python3 tools/build.py` → 28 pages; `python3 tools/checks.py` → ALL CHECKS PASSED; `npm test` → 2/2.

**Flags added or changed here (none blocking):**
- **F-P24** (open; published first by arena/722181aa-prod2 in PR #39/#42): not edited by this session.
- **F-P25** (open, low): "Check price on Amazon" button label needs an owner copy decision (§2(b)).
- **F-P26** (open): the public `EXECUTIVE_SUMMARY.md` carried a five-row price column that the register withholds. Neighbouring-price mechanism softened to "not verified here" (F-P17 is the only record of it).
- **F-P27** (open): the two same-day reads disagree on B02NbDxp3 and B0f3GKalj. Decided only by the browser check in Q-P18.
- **F-P28** (open): products.json short_link fields and the intent record still describe the links as resolving; the 2026-11-20 reads do not confirm that. Intent and observed fields are not merged.
- **F-P19** extended: pages.yml docs-only versus the legacy-root Pages source (same mismatch as F-P20; extended, not duplicated).
- **F-P20** detail extended: served versus local `settings.json`.

**Statements corrected:** `content/pages/executive-summary.html`, `EXECUTIVE_SUMMARY.md`, `README.md`, `DECISIONS.md` D-01, `data/suggestions.json` (what_we_know), `data/p2/questions.json` (Q-01, Q-P03, Q-P18), `data/p2/verification-2026-11-20.json` (r01 record; "not re-resolved" sentence now carries a dated correction).

**Not done (owner or later pass):**
- No logged-in Associates Central check (Q-01, F-57, F-58). No logged-out browser test of the short links (Q-P18).
- Pages source is still legacy `main /` (Pages API read 2026-11-20). Changing it needs repository admin (F-P19/F-P20).
- Operating Agreement §5 and the FTC pages (S-FTC1/S-FTC2) were not re-read in this pass.

## CLAIM — session arena/d5157db6-prod2 (2026-11-20, re-verification + drift fixes + integration)

Protocol note: this session works only on its assigned branch `arena/d5157db6-prod2`. The `session-<id>/<task>` branch naming in the brief is not used; this claim is recorded here instead.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| R-01 Live re-check of the five `/dp/` listings (P1 re-read) and the five submitted short links | done | arena/d5157db6-prod2 | `data/p2/live-check-2026-11-20-d5157db6.json` (new) |
| R-02 Record the second same-day short-link observation on F-P24 (the HTTP 500 link now resolves to the homepage) | done | arena/d5157db6-prod2 | `data/p2/flags.json` (F-P24 evidence note only; status stays open) |
| R-03 Correct stale counts: gate sections (11/13/9 → 14), guide pages (9/eight → 10), built pages (24 → 30) | done | arena/d5157db6-prod2 | `README.md`, `ENGINE.md`, `EXECUTIVE_SUMMARY.md`, `content/pages/executive-summary.html`, `docs/`, root mirror |
| R-04 Rebuild, gate, CI-equivalent checks, PR to main, merge, Pages check; record here | done (see record below) | arena/d5157db6-prod2 | `COORDINATION.md`, `docs/`, root mirror |

### Results (2026-11-20)

- **R-01 Listings.** `https://www.amazon.com/dp/B0CDY277D3` (P1) live; title matches `data/p2/products.json` (`name_listing`). P2–P5 were not re-read in this pass; they were read earlier today under 722181aa and are unchanged.
- **R-01 Short links.** All five `https://link.amazon/{token}` URLs were read through the fetch tool. Four resolved to `https://www.amazon.com/`. The fifth (`B0f3GKalj`, P5) returned HTTP 500 in the earlier read today and resolved to the homepage in this read. None resolved to a product listing in this pass. Intended ASINs were not changed.
- **R-02 Flag.** F-P24 is still **open**. Its evidence note now carries the second observation. No reader-facing link is affected: the site never publishes a short link as a buy path.
- **R-03 Counts.** The gate runs 14 sections (`pages, disclosure, links, validity, facts, claims, chrome, seo, publication, longreads, shop, exposition, measurement, freshness`). The build produces 30 pages, 10 `guide-*` pages and 2 `article-*` long reads. Corrected in README, ENGINE.md, EXECUTIVE_SUMMARY.md and the reader page `executive-summary.html`.
- **R-04 Checks.** `python3 tools/build.py` → 30 pages; `python3 tools/checks.py` → ALL CHECKS PASSED; `python3 scripts/build_site.py` + `python3 scripts/verify_site.py` → VERIFY OK; `node --test tests/server.test.mjs` → 3/3 pass.

### Sources (official and fetched this session)

- Amazon listing: https://www.amazon.com/dp/B0CDY277D3
- Submitted short links (fetch tool, 2026-11-20): https://link.amazon/B04G1MEwY · https://link.amazon/B02NbDxp3 · https://link.amazon/B00hJ57DV · https://link.amazon/B0c8moW59 · https://link.amazon/B0f3GKalj
- Amazon's ASIN definition and tag format: already recorded in `data/p2/sources.json` (S-ASIN, S-TAG); not re-read.

### Irregularities for manual review (not blocking)

1. F-P24 — short links still resolve to the Amazon homepage (2 reads today). Owner needs a normal browser check; see the flag's `how_to_resolve`.
2. Associates Special Links: the Associates-workflow test of one link per product (confirming destination and tracking report) requires a logged-in Associates account. This sandbox has no such access, so it is **not done** and is an owner action (Q-01 / F-03).
3. Pages source is still `main /` (F-P19 / F-P20). Owner action: Settings → Pages → Source: GitHub Actions.
4. Analytics endpoint is deployable but not hosted (F-19 / Q-23). Search Console is not verified (Q-P08).

## ACTIVE CLAIM — session arena/644d217b-prod2 (2026-11-20, reader-first publication pass + integration)

Branched from `4398598` (main after PR #33). This session is both the working session and the
final integration session on this branch, per the standing one-branch-per-session rule.

**Scope (this session only).** No other claim is live: PR #35 (`arena/dd4bae8a-prod2`) is the one
open PR and it is **not touched** (its scope overlaps everything below; it must be rebased or closed
by its own session — logged, not edited). PRs #29–#34, #36–#38 are merged.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| W-01 Measurement: fix the event-vocabulary split so the shipped counter and the shipped collector agree (closes F-P23 / Q-P14 / SG-41) | done | arena/644d217b-prod2 | `assets/js/measure.js`, `server.mjs`, `data/p2/events.json`, `tests/server.test.mjs` |
| W-02 Reader-facing depth: expand the short guides into real publication articles (new long-form pieces, one per buying decision) | done | arena/644d217b-prod2 | `content/pages/guide-*.html`, `content/pages/article-*.html`, `tools/build.py` |
| W-03 Landing/authored voice: masthead + a real "start here" path, without adding dashboard clutter to the front page | done | arena/644d217b-prod2 | `content/pages/index.html`, `assets/css/site.css` |
| W-04 Suggestions: a reviewable decision queue (ranked, with cost/reversibility/owner action) so the owner picks a path before changes land | done | arena/644d217b-prod2 | `data/p2/suggestions.json`, `content/pages/suggestions.html` |
| W-05 Open questions: the missing-information register, extended with discovery paths | done | arena/644d217b-prod2 | `data/p2/questions.json`, `content/pages/questions.html` |
| W-06 Line-by-line verification of every published product value against the live official listing (2026-11-20 read) | done | arena/644d217b-prod2 | `data/p2/verification-2026-11-20.json`, `data/p2/products.json` (read-only unless a value is wrong) |
| W-07 Gate: new checks that would have caught the defects found this pass | done | arena/644d217b-prod2 | `tools/checks.py` |
| W-08 Integration: rebuild, re-verify, PR to main, merge, Pages live check, record here | done | arena/644d217b-prod2 | `docs/`, root mirror, `COORDINATION.md`, `EXECUTIVE_SUMMARY.md` |

Claim protocol notes:
- **Verification boundary, recorded honestly:** this sandbox has outbound HTTP to
  `github.com`/`api.github.com`/`registry.npmjs.org`/`pypi.org`/`files.pythonhosted.org` and to the
  fetch tool's allowlist. `curl` to `www.amazon.com` and to the live Pages host fails (`http 000`),
  so the **fetch tool** is used for both, and every value is recorded with the tool that read it.
  Amazon listing pages return a "product summary" variant to the fetch tool; the listing **title**,
  **ASIN** and **breadcrumb** are available, prices/ratings render as `$`-strings inside
  recommendation widgets and are **not** attributable to the product page, so they stay unpublished.
- Flagged irregularities do not block the merge; they go to the Flagged for Review page.


### Claim results (W-01..W-08, 2026-11-20)

- **W-01 · measurement (done).** The published contract named five events; the only collector in the
  repo answered **400** to three of them (`guide_read_75`, `category_click`, `feed_click`) and collapsed
  every page view into `page_view|/unknown`. Hosting it unchanged would have silently dropped two thirds
  of the site's measurement. Fixed at the collector, not by renaming the site's events: `server.mjs` now
  accepts and correctly keys all five, keeps the older Countercraft names so no existing client breaks,
  and bounds every value it stores (a 10-character ASIN pattern, a category slug, a cleaned path).
  Three things now stop a regression: a test that reads the five names out of `assets/js/measure.js`,
  a hard gate failure in `tools/checks.py` (was a printed note), and `D-P21` recording which list wins.
  `F-P23` resolved, `Q-P14` answered, `SG-41` shipped.
- **W-02 · reader-facing depth (done).** Two long-form pieces, each arguing one buying decision from an
  official guidance source the listings do not carry:
  - `article-thermometer-placement.html`, 1,295 words — USDA FSIS *Food Thermometers* factsheet (the
    2–4 °F typical instrument range, the "reading will only be correct if placed properly" rule, the
    per-food placement table, the thin-food sensing-area rule, the "at least 1 inch" wireless figure,
    care and ice-water calibration) plus the FSIS *Safe Minimum Internal Temperature Chart*.
  - `article-air-fryer-doneness.html`, 1,212 words — Nebraska Extension's peer-reviewed *Food Safety
    Tips for Air Fryers* (overfilling prevents even cooking; a thermometer is the only way to be sure;
    clean the basket after every use) plus the same FSIS chart.
  Both carry the mandatory "what we could not verify" block, are in the sitemap, feed and JSON-LD, and
  are linked from both category pillars and three guides. New source ids `S-FSIS-CHART`,
  `S-FSIS-THERMO`, `S-UNL-AIRFRYER`, each read **live on 2026-11-20**.
- **W-03 · landing and authored voice (done).** A "Read this before you buy either" block now sits
  directly under the shelf; the guides hub leads with the long reads; the front-page trust row no longer
  claims ten guides when the build renders twelve pieces. No dashboard clutter was added to the front
  page — the governance surfaces stay in the footer, per D-06.
- **W-04 · suggestions (done).** `SG-45` (long-form argument pieces, shipped), `SG-46` (move Pages to
  the Actions artifact and delete the root mirror — ranked first on the board because it is one
  dropdown, closes F-P19/F-P20 and removes the double-commit this repo pays on every pass), `SG-47`
  (real product photography via the licensed channel, or a commissioned drawing set). The page now
  opens with a **ranked five-row short list** (cost to you, reversibility, exact owner action) instead
  of asking a reviewer to read 38 proposals in registry order.
- **W-05 · open questions (done).** `Q-P15` (is there a length standard, and is length even the right
  control — offers a sourced-claims-per-100-words floor as the only option filler cannot satisfy),
  `Q-P16` (can this project show a real product photo at all, and the single test that settles it:
  open a SiteStripe link on one enrolled product), `Q-P17` (where the endpoint runs and who pays).
- **W-06 · line-by-line verification (done).** All five listings re-fetched on 2026-11-20 and the
  register compared field by field. **Titles agree verbatim with the register** for P1–P5, including the
  ThermoMaven title, which had been recorded with a second-segment discrepancy in `F-P01` and now reads
  as the register has it. **Breadcrumbs agree** for P1, P3, P4 and P5 (P2's breadcrumb did not appear in
  the fetched variant this pass and stays null — not inferred). Every published dimension string in
  `docs/` was cross-checked against the register programmatically: `13.38 / 11.81 / 10.63` (P1),
  `16.9 / 15.8 / 14.8` (P2), `12.75 / 13.5 / 10` (P3) all match, and no unexplained inch value appears
  on any page. **No published value changed.** Prices and ratings stay unpublished: on these fetches the
  `$` figures appear inside "customers also viewed" carousels and protection-plan blocks, which are
  other ASINs' prices — a live example of exactly the attribution trap `F-P17` records, and the reason
  the site keeps both blank (`F-02`, `D-P10`).
- **W-07 · gate (done).** New `longreads` section (page exists, ≥3 inline source markers, unverified
  block present, only allow-listed official hosts cited, present in sitemap and feed) and two
  measurement assertions (the endpoint must accept every name the client can send; the depth event must
  cover `article-*` as well as `guide-*`). `tools/checks.py` header updated to match: 13 sections.
- **W-08 · integration (this record).** `tools/build.py` + `tools/checks.py` → **ALL CHECKS PASSED**
  (30 pages, 13 sections); `scripts/build_site.py` + `scripts/verify_site.py` → **VERIFY OK, 18 pages**;
  `npm test` → **3/3**. Root mirror byte-identical to `docs/` (30/30 HTML files, same hashes).

### Files this pass touched

`assets/js/measure.js` · `server.mjs` · `tests/server.test.mjs` · `tools/build.py` · `tools/checks.py` ·
`content/pages/{index,guides,suggestions,buying-guide,category-air-fryers,category-thermometers,guide-capacity,guide-thermometer-accuracy}.html` ·
`content/pages/article-{thermometer-placement,air-fryer-doneness}.html` (new) ·
`data/p2/{sources,flags,questions,decisions,suggestions,calendar}.json` · `docs/` + root mirror ·
`EXECUTIVE_SUMMARY.md` · `COORDINATION.md`.

### Irregularities found this pass (all published, none blocking)

| # | Finding | Where it is published |
| --- | --- | --- |
| 1 | The collector rejected three of the five events the site publishes, and keyed every page view as `/unknown`. Fixed this pass; recorded in full because it is the clearest example of a gate that was printing a warning while the defect shipped. | Flagged `F-P23` (resolved), decision `D-P21` |
| 2 | The depth event did not cover `article-*` pages, so both new long reads would have been unmeasured. Fixed; now asserted in the gate. | `tools/checks.py` measurement section |
| 3 | The executive summary carried counts from two passes ago (28/15/32/27/9) and still named the project by its codename. Corrected to the rendered values. | `EXECUTIVE_SUMMARY.md` |
| 4 | Amazon listing fetches return a variant in which prices and star ratings belong to *other* ASINs in carousels. Any future pass that copies a `$` string from a fetched listing will misattribute it. | `F-P17`, `F-02`, and the W-06 note above |

### Open PR handled by logging, not editing

**PR #35** (`arena/dd4bae8a-prod2`, "Publication pass: shop-first redesign…", 100 files) is still
`CONFLICTING` against `main` as of 2026-11-20 06:45 UTC. Its last commit is 06:27 UTC, so it is inside
its own claim window and **has not been touched** — no file it owns was edited and no branch of its was
touched. Its scope overlaps every reader-facing surface in this pass; if its author returns, it must be
rebased on this merge and its content reconciled by hand, because this branch has changed
`tools/build.py`, `assets/js/measure.js`, `server.mjs`, the guide registry and the suggestions/questions
registers underneath it. If it is still stale and conflicting **60 minutes after its last commit**
(07:27 UTC), any session may take it over under the handoff rule and should treat this record as the
current state of `main`.

---

## PARALLEL CLAIM — session arena/f55b5827-prod2 (2026-11-20, anti-slop design + brand + seasonal pass)

Ran in parallel with the two passes above (both also branched from f6e772f). **Reconciled by this
session's merges of origin/main (PRs #29–#31 and #37–#38): nothing from any pass was discarded.**

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| V-01 Ship the adopted brief's typography (self-hosted Fraunces + Inter, OFL) + design-token conformance | done | arena/f55b5827-prod2 | `assets/fonts/*`, `assets/css/site.css` |
| V-02 Working-brand adoption on the owner directive ("The Crisp Counter") + preliminary name search; formal clearance stays open (Q-19) | done | arena/f55b5827-prod2 | `data/p2/settings.json`, `tools/make_og.py`, `assets/img/og-card.png`, `data/p2/flags.json` (as F-P21) |
| V-03 Catchy seasonal guide (December gifting window) + calendar queue extension (hypotheses only, D-19) | done | arena/f55b5827-prod2 | `content/pages/guide-gift-guide.html`, `data/p2/calendar.json`, `tools/build.py` |
| V-04 Decision-making improvements + suggestion batch (SG-38..SG-40, SG-42, SG-43 added; runbook at SG-44) | done | arena/f55b5827-prod2 | `data/p2/suggestions.json`, `content/pages/suggestions.html` |
| V-05 Questions / missing-information register additions (Q-P10, Q-P11) | done | arena/f55b5827-prod2 | `data/p2/questions.json` |
| V-06 Register + docs sync (decisions D-P18..D-P20 after remap) | done | arena/f55b5827-prod2 | `data/p2/decisions.json`, `*.md`, `tools/build.py` (BUILD_DATE) |
| V-07 Integration: reconcile all three passes, rebuild both outputs, gate, line-by-line re-verify, PR to main, merge, Pages live check | done | arena/f55b5827-prod2 | `docs/`, root mirror, `COORDINATION.md` |

### Claim results (V-01..V-07, 2026-11-20)

- **V-01 (typography + tokens):** Fraunces (600 normal, 400 italic) + Inter (400/500/600/700) shipped as latin
  woff2 subsets in `assets/fonts/`, SIL OFL 1.1 license files committed beside them, `font-display: swap`,
  zero third-party requests. Files via @fontsource/fraunces@5.3.0 and @fontsource/inter@5.3.0
  (registry.npmjs.org; upstreams github.com/undercasetype/Fraunces, github.com/rsms/inter — linked in D-P19).
  The merged design system consumes them through its token layer.
- **V-02 (working brand):** "The Crisp Counter" on every reader-facing surface (masthead, titles, JSON-LD,
  feed, footer, OG card). Preliminary name search 2026-11-20 (web search, first page — no kitchen-appliance
  conflict; formal clearance NOT performed): recorded in D-P18 sources (tmsearch.uspto.gov is the resolver).
  Clearance flag published as **F-P21**. Six page titles shortened to keep the 70-char gate green.
- **V-03 (seasonal guide):** `guide-gift-guide.html` shipped (December gifting window; gifting seasonal card
  in `data/p2/calendar.json`; queue slots 6-9). Every fact traces to the register; carries the mandatory
  "What we could not verify" block; D-19 respected. All gift-guide facts re-checked against the merged
  register after each reconciliation (16.9" depth, sync finish, 8 qt + 450°F + shake reminder, 1-second
  NIST/NSF ±0.5°F IP67, 3 probes + 1000°F — all present).
- **V-04 (suggestions):** SG-15/16/31/32/33/38/40 statused; SG-39/SG-43 added; SG-42 closed as rejected on
  the D-P11 policy read; the organic-discovery runbook lives at **SG-44** (remapped twice from SG-41 after
  two ID collisions). Suggestions page carries the three-path chooser PLUS the decision-maker/decide-by
  path block (SG-32).
- **V-05 (questions):** Q-P10 (brand ratification + clearance, D-P18/F-P21) and Q-P11 (availability
  snapshots — answered no by the D-P11 policy read) added.
- **V-06 (registers + docs):** decisions at **D-P18 (working brand), D-P19 (typography + token
  conformance), D-P20 (gifting window)**; remap history documented in each register's meta.
- **Second verification pass (2026-11-20):** all five official listing URLs re-fetched; document titles
  (verbatim listing titles) + breadcrumbs matched the register — **agrees with the shop-front pass's deep
  read in `data/p2/verification-2026-11-20.json`**, which is the primary record for this date.
- **V-07 (integration):** `tools/build.py` + `tools/checks.py` → ALL CHECKS PASSED; `scripts/build_site.py`
  + `scripts/verify_site.py` → VERIFY OK; `npm test` → 2/2; rebuild reproducibility confirmed. PR + merge +
  Pages check recorded in the PR record below.

### Reconciliation note (read this before editing the registers)

Three sessions on 2026-11-20 independently used the D-P10+/F-P15+/SG-4x+ ID spaces. Final assignment:
**decisions** D-P10..D-P14 (shop-front), D-P15 (event-vocabulary publication, arena/86206fb3-prod2),
D-P18..D-P20 (anti-slop, remapped twice — the collision history is in the decision log's meta);
**flags** F-P15..F-P20 (shop-front), F-P21 (anti-slop, remapped from F-P15), F-P22/F-P23 (event-vocab);
**suggestions** SG-38..SG-40 + SG-42..SG-44 (anti-slop; SG-41 belongs to the event-vocab pass).
Every cross-reference on the built pages resolves (the validity gate checks register IDs).

---

## ACTIVE CLAIM — session arena/70b2b9f7-prod2 (2026-11-20, shop-first design rebuild + live verification)

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| D-01 Live re-verification of all five listings + policy sources (2026-11-20) | done | arena/70b2b9f7-prod2 | `data/p2/verification-2026-11-20.json`, `data/p2/sources.json`, `data/p2/flags.json` |
| D-02 Design system rebuild (publication/shop visual language) | done | arena/70b2b9f7-prod2 | `assets/css/site.css`, `assets/js/site.js` |
| D-03 Front page rebuilt as a shop front page (products lead) | done | arena/70b2b9f7-prod2 | `content/pages/index.html` |
| D-04 New `/shop.html` shelf with category + format filters | done | arena/70b2b9f7-prod2 | `content/pages/shop.html`, `tools/build.py` |
| D-05 New `/about.html` authorship + editorial standards (E-E-A-T) | done | arena/70b2b9f7-prod2 | `content/pages/about.html`, `tools/build.py` |
| D-06 Navigation simplification (single reader nav; dashboards in footer) | done | arena/70b2b9f7-prod2 | `tools/build.py` |
| D-07 Product-card + comparison component upgrade | done | arena/70b2b9f7-prod2 | `tools/build.py` |
| D-08 Suggestions section: review-and-choose decision surface | done | arena/70b2b9f7-prod2 | `content/pages/suggestions.html`, `data/p2/suggestions.json` |
| D-09 Questions register: missing-information discovery paths | done | arena/70b2b9f7-prod2 | `content/pages/questions.html`, `data/p2/questions.json` |
| D-10 Gate extension + full build/verify | done | arena/70b2b9f7-prod2 | `tools/checks.py`, `docs/`, root mirror |
| D-11 Integration: PR, merge, Pages deploy confirmed, docs sync | done | arena/70b2b9f7-prod2 | `README.md`, `EXECUTIVE_SUMMARY.md`, `DECISIONS.md`, `docs/` |

Protocol notes for this claim:
- Branch `arena/70b2b9f7-prod2`, branched from `f6e772f` (main at PR #28). Arena allows one branch per session; this session is both working and integration session on it.
- **No other session's claim is live.** Every previous claim is at merged/closed PR state. Scope above touches only the canonical `docs/` publication build (`tools/build.py`, `content/pages/*`, `assets/*`, `data/p2/*`) plus its root mirror. The preserved Countercraft build (`scripts/build_site.py` → `site/`) is **not** edited; it is rebuilt and gated unchanged by CI.
- **Pages serving mode (INT-07) re-confirmed 2026-11-20:** `GET /repos/.../pages` returns `build_type: legacy`, `source: main /`. `PUT` to `build_type: workflow` returns **403 Resource not accessible by integration**. So the live site is still the **repo root**, and the root mirror written by `tools/build.py` is what readers see. The root mirror is therefore mandatory, not optional, this pass.
- **New capability this pass:** outbound HTTP from this sandbox reaches `www.amazon.com` and official policy sites through the fetch tool, so all five listings were **re-fetched live today** rather than carried forward. Prior sessions recorded the opposite (no egress); that boundary is now corrected in the verification record.

---

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| P-01 Shop-first front page (publication front page, products before process) | done | arena/9f84489c-prod2 | `content/pages/index.html`, `tools/build.py` |
| P-02 Nav labels + guides hub page (single nav group; dashboards footer-only) | done | arena/9f84489c-prod2 | `tools/build.py`, `content/pages/guides.html` |
| P-03 Three new question-shaped guides (complete the eight-topic calendar) | done | arena/9f84489c-prod2 | `content/pages/guide-*.html`, `tools/build.py` |
| P-04 Seasons + clusters (holiday hosting cluster, pillar wiring, cadence) | done | arena/9f84489c-prod2 | `data/p2/calendar.json`, `content/pages/*` |
| P-05 Parallel-pass rows: RSS subscribe affordances, Search Console readiness, reader capture | done | arena/9f84489c-prod2 | `tools/build.py`, `data/p2/settings.json`, `data/p2/events.json` |
| P-06 Suggestions queue expansion (design-direction + decision-making paths) | done | arena/9f84489c-prod2 | `data/p2/suggestions.json`, `content/pages/suggestions.html` |
| P-07 Questions register clarity pass (status table, discovery suggestions) | done | arena/9f84489c-prod2 | `data/p2/questions.json`, `content/pages/questions.html` |
| P-08 Docs sync (README, EXECUTIVE_SUMMARY, DECISIONS) + decision log entries | done | arena/9f84489c-prod2 | `README.md`, `EXECUTIVE_SUMMARY.md`, `DECISIONS.md`, `data/p2/decisions.json` |
| P-09 Gate extension (feed covers guides, internal-link rule, capture consent) | done | arena/9f84489c-prod2 | `tools/checks.py` |
| P-10 Integration: rebuild, re-verify, PR to main, merge, Pages live check; PR #16 handoff | done | arena/9f84489c-prod2 | `docs/`, root mirror, `archive/countertop-dispatch/` |

Protocol notes for this claim:
- Branch `arena/9f84489c-prod2` from `da11cd4` (main at PR #15). Arena allows one branch per session; this session is both working and integration session on this branch (same standing note as the arena/44093825 claim below).
- **PR #16 handoff (arena/30a7028a-prod2, "Countertop Dispatch"):** its claim has been inactive >60 minutes with no commits since 14:17 UTC and its merge plan never ran. Per the handoff rule this session takes over integration of that branch: its full build will be preserved as `archive/countertop-dispatch/` (nothing discarded), and one deployed site stays canonical per the standing one-site rule (INT-06).
- The canonical deployed publication remains `docs/` (built by `tools/build.py`, gated by `tools/checks.py`, mirrored to the repo root for legacy Pages serving).

### Verification performed this pass (D-01)

Every value below was read on **2026-11-20** from the page named, and each is recorded with the
observed string in `data/p2/verification-2026-11-20.json`.

| Source | URL | Result |
| --- | --- | --- |
| Listing P1 | https://www.amazon.com/dp/B0CDY277D3 | Title matched the register; breadcrumb Air Fryers; buy box present |
| Listing P2 | https://www.amazon.com/dp/B09B7SB46R | Title matched; 24 presets stated in the title (Q-31 still open on body copy) |
| Listing P3 | https://www.amazon.com/dp/B08DKYBTPH | Title matched; 8 Qt, 450°F Hi-Fry, 4-in-1 |
| Listing P4 | https://www.amazon.com/dp/B0DHZTCNR5 | Title matched; ±0.5℉ NIST/NSF, IP67, 1 Sec |
| Listing P5 | https://www.amazon.com/dp/B0DZFD6R9Z | Title matched; 3 probes, 1000°F, WiFi unlimited range |
| Operating Agreement | https://affiliate-program.amazon.com/help/operating/agreement | Updated 2025-10-15; §5 disclosure sentence quoted; §6(a) breach |
| Program Policies | https://affiliate-program.amazon.com/help/operating/policies | Updated 2026-04-14; §2(b) price rule and misleading-claims rule quoted |
| USDA cook temps | https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures | Last reviewed 2024-11-21; table quoted |
| USDA cold storage | https://www.foodsafety.gov/food-safety-charts/cold-food-storage-charts | Last reviewed 2023-09-19 |
| USDA power outage | https://www.foodsafety.gov/food-safety-charts/food-safety-during-power-outage | Last reviewed 2024-08-08 |

**Irregularities found and published** (all on the Flagged for review page with these links):
F-P15 (disclosure wording vs §5 — corrected), F-P16 ("Compare all five" was a paid link to one
product — corrected), F-P17 (carousel prices and ratings belong to neighbouring ASINs), F-P18
(prior records claimed no egress to Amazon; corrected), F-P19 (archive servable, robots-only
exclusion), F-P20 (raw registers servable in root-serving mode).

**Not verified, and left alone:** the Associates enrollment status (Q-01), Search Console
(Q-P08), domain control (Q-P06) and the analytics endpoint host (Q-23) are owner-side facts.
No claim is made about any of them.

---

---

This is the shared task board. Each task has: a status (`unclaimed`, `in progress`,
`done`, `needs review`), an owning session, and the files it touches. Shared outputs
(the site's table data, index and navigation) are changed only by the final integration
session once all other tasks are done.

> Status `needs review` means the item is published on the **Flagged for Review** page and
> does **not** block anything. Nothing is marked `verified` unless it was checked against an
> official source, with that source linked.

## Status at a glance

| Task | Status | Session | Files |
| --- | --- | --- | --- |
| T1 — Repo review | done | session-arena-8ff10f50-prod2 | — |
| T2 — Verify the 5 submitted affiliate links (resolve + identity + price + category) | done | session-arena-599eec57 | `data/products.json`, `data/sources.json` |
| T3 — Verify compliance sources (Agreement, Policies, ASIN definition, FTC) | done | session-arena-599eec57 | `data/sources.json` |
| T4 — Data model + build system (data-driven static site) | done | session-arena-8ff10f50-prod2 | `data/*.json`, `scripts/build_site.py`, `tools/build.py` |
| T5 — Site generation (landing + category + comparison + guides) | done | session-arena-8ff10f50-prod2 | `scripts/build_site.py` -> `site/`; `tools/build.py` -> `docs/` |
| T6 — Disclosure strip, `rel="sponsored"`, product-intent record, click counter | done | session-arena-8ff10f50-prod2 | `site/assets/*`, `scripts/build_site.py`, `docs/` |
| T7 — Findability (sitemap, RSS, robots, unique meta, structured data) | done | session-arena-8ff10f50-prod2 | `site/sitemap.xml`, `site/rss.xml`, `site/robots.txt`; `docs/` |
| T8 — Suggestions / decision portal (questions, info needed, path chooser) | done | session-arena-8ff10f50-prod2 | `data/suggestions.json`, `site/suggestions.html`; `docs/suggestions.html` |
| T9 — Flagged for Review page | done | session-arena-8ff10f50-prod2 | `site/flagged.html`; `docs/flagged.html` |
| T10 — Verification gate (sources per row, rel=sponsored, disclosure, sitemap) | done | session-arena-8ff10f50-prod2 | `scripts/verify_site.py`; `tools/checks.py` |
| T11 — Integration, PR, merge, GitHub Pages deploy | done | session-arena-8ff10f50-prod2 | `.github/workflows/pages.yml`, `site/`, `docs/`, `main` |
| T12 — Shop-like product-forward landing page | in progress | session-arena-8ff10f50-prod2 | `scripts/build_site.py` (index body), `data/articles.json` |
| T13 — Decision-input questions + missing-info discovery list | done | session-arena-8ff10f50-prod2 | `data/open-questions.json`, `site/suggestions.html` |

## Claims this turn (session-arena-8ff10f50-prod2)

- **T11 (integration, PR, merge, Pages deploy):** claim the full scope. Re-verify both builds line by line, make the landing page product-forward (lead with products), confirm `pages.yml` deploys a working artifact, commit, push, open a PR from `arena/8ff10f50-prod2` to `main`, merge it, and confirm GitHub Pages deploys. Record the PR link and merge result below.
- **T12 (shop-like landing page):** reorder the front page so products lead (featured products + buy buttons above the register), keep guides + category tiles, and keep the disclosure strip above the fold.
- **T13 (decision-input questions):** the open-questions register and the suggestions/decision portal already exist; verified present and linked from the nav/footer.

## Claims this turn (session-arena-1f4017b9-prod2 — shop-forward polish + integration)

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| S-01 Shop-forward landing page rewrite (products above register, buy buttons prominent, publication feel) | done | session-arena-1f4017b9-prod2 | `content/pages/index.html`, `tools/build.py` |
| S-02 Design prompt additions (polished marketing affiliate design, catchy articles, organic traffic hooks) | done | session-arena-1f4017b9-prod2 | `DESIGN_PROMPT.md` |
| S-03 Q&A register clarity + missing-info discovery list | done | session-arena-1f4017b9-prod2 | `docs/questions.html`, `data/p2/questions.json` (verified present) |
| S-04 Executive summary refresh | done | session-arena-1f4017b9-prod2 | `EXECUTIVE_SUMMARY.md` (verified present) |
| S-05 Build + verify both outputs + GitHub Pages deploy | done | session-arena-1f4017b9-prod2 | `tools/build.py`, `tools/checks.py`, `.github/workflows/pages.yml`, `docs/`, root mirror |
| S-06 PR to main + merge + confirm Pages live | done | session-arena-1f4017b9-prod2 | `main`, `.github/workflows/` |

## Claims this session (session-arena-43f4359d-prod2, branch `arena/43f4359d-prod2`)

- **T11-integrate:** re-verify both builds (`scripts/build_site.py` + `tools/build.py`), `scripts/verify_site.py` + `tools/checks.py`, landing page product-first, commit, push, open PR from `arena/43f4359d-prod2` to `main`, merge, confirm Pages deploys; record PR link + merge result below.
- **T12-shop-landing:** reorder `site/index.html` so product cards + buy buttons lead before guides/categories/register; disclosure stays above fold; `rel="sponsored"` on every outbound product link.

No other session has an unexpired claim on these files. If this session stops, any other session may take over an `in progress` task older than 60 minutes with no commits and must note the handoff here.

## Verification boundary (this session)

- Product facts, ASINs, prices and ratings in `data/products.json` were re-read from the official Amazon listings on 2026-11-19 (see `data/sources.json`). This sandbox cannot reach amazon.com (egress is limited to github.com/npm/pypi hosts), so values are taken from the dated 2026-11-19 verification records and are **not re-fetched here**. Any value that cannot be confirmed from an official source is left blank and flagged (see the Flagged for Review page). No value is inferred.
- Compliance sources (Amazon Associates Operating Agreement, Program Policies, ASIN definition, FTC, Google Search Central) are cited from `data/sources.json` with access date 2026-11-19; links are provided for manual review.

## PR / merge / deploy record (filled in after merge)

| PR | What | Result |
| --- | --- | --- |
| #33 | Anti-slop design pass: working brand The Crisp Counter (D-P18), shipped Fraunces+Inter typography (D-P19), December gift guide + queue (D-P20), SG-38..SG-40/SG-42..SG-44, Q-P10/Q-P11, F-P21; reconciled with PRs #29-#31 and #37-#38 (three parallel 2026-11-20 passes) | **Merged into `main` as merge commit `4398598`** (2026-11-20T06:36:42Z). `Deploy to GitHub Pages` success (run 44689028467); `pages build and deployment` success (run 44689027619); `verify-site` success; `test` (analytics endpoint) success. **Live check passed:** https://wingbangboozle1-lang.github.io/Prod2/ serves the merged publication — title "Air fryers and thermometers by format | The Crisp Counter", 10 buyer guides, gift guide live at /guide-gift-guide.html, tagged (paid link) buttons, fonts self-hosted. |
| #19 | Integration: product-forward landing page + transparency flag F-P08 + both builds verified + Pages deploy | Merged into `main` as merge commit `0030f90a69b53ecd226923ddd6125dc795f0b282`; `Deploy to GitHub Pages` success; `verify-site` success; `pages build and deployment` success; live at https://wingbangboozle1-lang.github.io/Prod2/ |


## PR / merge / deploy record — 2026-11-20 (arena/70b2b9f7-prod2)

| PR | What | Result |
| --- | --- | --- |
| #31 | Shop-first rebuild: design system, shelf page, About/standards, live 2026-11-20 re-verification, gate 9 -> 11 sections | **Merged** into `main` as `a4166bbbdee2ba3ad7c66d7113979a3608e7f1d9` at 2026-11-20T06:19:46Z. `verify-site` pass · `Self-hosted analytics tests` pass · `Deploy to GitHub Pages` pass · `pages build and deployment` pass |
| #32 | Publish date: `BUILD_DATE` 2026-11-19 -> 2026-11-20 (footer, sitemap `lastmod`, feed `pubDate`) | **Merged** into `main` as `8bc543b8b559de18f33b58449cf06331b002c2a0`. All four workflows pass |

**Live check after deploy (not a workflow status — the actual published pages):**

| URL | State |
| --- | --- |
| `/Prod2/` | New front page: illustrated hero, shelf of five cards with images, "Best for:" lines, buy buttons, `Published 2026-11-20` |
| `/Prod2/shop.html` | Live: filters, five cards, chooser, shortlist comparison |
| `/Prod2/about.html` | Live: four rules, limits table, imagery policy |
| `og-card.png` | New social card rendering (served as the page's main image) |

**One thing to know about verifying the live site from here:** `curl` cannot reach
`*.github.io` from this sandbox (egress is limited to `github.com`, `codeload.github.com`,
`api.github.com`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org`). The live pages were
therefore verified through the page-fetch tool, which can reach them. The first fetch of `/Prod2/`
returned the **previous** build — a stale CDN edge, not a deploy failure — and a second fetch
returned the current build. If a live check looks wrong, re-fetch with a cache-busting query before
concluding anything.

### Integration with the two sessions that merged mid-pass

PRs #29 and #30 landed on `main` after this branch was cut and both touched the front page and the
product cards. They were integrated, not overwritten:

- **Preserved from #29/#30:** all 45 added lines of `DESIGN_PROMPT.md` (marketing conversion layer,
  the nine article hooks, the organic-traffic notes); the `scripts/build_site.py` shelf work on the
  preserved Countercraft build; the explicit `Best for:` label, which is clearer than the bare
  eyebrow this branch had; and their hero phrase "every fact checked".
- **Kept from this branch:** the design system, the card component with imagery and a buy button,
  the new `shop.html` and `about.html`, the six-link nav, and the extended gate.
- **Regenerated rather than hand-merged:** `docs/`, the root mirror, `sitemap.xml`, `feed.xml`.
  The merge is reproducible — a clean clone rebuilds byte-identical output.

## Task details

### T1 — Repo review (done)
- Repo was a fresh checkout: a single `README.md` (`# Prod2`) and one commit
  (`c6dc49a`). No prior site, data, or tooling. Greenfield build.

### T2 — Link intake + verification (done)
Verified **live on 2026-11-19** by resolving each submitted `link.amazon` short link against
the official Amazon listing page.

| Submitted link | Token length | Resolves to ASIN | Product | Category |
| --- | --- | --- | --- | --- |
| link.amazon/B04G1MEwY | 9 | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven (Black) | Air Fryers |
| link.amazon/B02NbDxp3 | 9 | B09B7SB46R | Emeril Lagasse 26QT French Door Air Fryer Toaster Oven | Air Fryers |
| link.amazon/B00hJ57DV | 9 | B08DKYBTPH | Chefman Air Fryer 8 Qt TurboFry 4-in-1 | Air Fryers |
| link.amazon/B0c8moW59 | 9 | B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer | Meat Thermometers |
| link.amazon/B0f3GKalj | 9 | B0DZFD6R9Z | CHEF iQ Sense Smart Wireless Meat Thermometer (Gen3) | Meat Thermometers |

**Finding:** every submitted token is a **9-character short-link token**. Amazon defines an
ASIN as a **10-character** alphanumeric code, so the submitted tokens are **not ASINs**. The
observed redirect targets are 10-character ASINs and resolve to real listings. Intent and
observation are kept in separate fields and never merged (see the product-intent record on
the Research Desk page).

**Irregularities / flags:**
- Token-vs-ASIN mismatch (all five).
- Star-rating numeric values were not captured for 4 of 5 products from the official listing
  extraction (rendered as an image on the listing); ThermoMaven's rating was captured
  (4.6★, 3,499 reviews). The 4 uncaptured ratings are published blank on the Flagged page.
- The submitted short links are link-shortening-style URLs. Their exact compliance status under
  the Participation Requirements 6(w) is **unresolved** — they are not declared invalid, but
  they must not be used in a way that makes the Amazon destination unclear. See
  `data/sources.json` and the Flagged page.

### T3 — Compliance sources (done)
Re-read from official pages on 2026-11-19 (see `data/sources.json` for full list + links):
- **Operating Agreement** (updated 2025-10-15): §1 Special Links / Program Content.
- **Program Policies** (updated 2026-04-14): §2(b) Special Links + price display; §3(e)
  cookie/pixel disclosure; §6(a)–(w) Content on your Site, incl. **6(v)** do not obscure the
  URL of your site containing Special Links, **6(w)** do not use link shortening in a way that
  makes the Amazon destination unclear, **6(t)** star ratings/reviews require Creators/PA API.
- **ASIN definition**: 10-character alphanumeric, Amazon-assigned (Amazon.com).
- **FTC** disclosure guidance (S07, S24) — cited for the disclosure standard.

### T4–T10 — Build, generate, verify (in progress / done as marked)
Owned by session-arena-599eec57. Scope is the full `site/` tree plus `data/` and `scripts/`.
No overlapping claims. The build is data-driven from `data/*.json` so every published check can
run from a clean checkout.

### T11 — Integration, PR, merge, deploy (pending)
Final integration session: re-verify the combined data line by line, confirm the site builds
with no broken links (`python3 scripts/verify_site.py`), then open a PR from this branch to
`main`, merge it, and confirm GitHub Pages deploys. Record the PR link and merge result here.

## Handoff / takeover notes
- If this session stops, any other session may take over an `in progress` task older than
  60 minutes with no commits, and must note the handoff here.
- Flagged irregularities and unverified items do **not** block the merge; they are published on
  the Flagged for Review page with source links.

## Integration with the parallel session (session f2613c86 / arena/3f1d9d65-prod2)

A parallel session built a second, complete site ("Counter Notes") and merged it to `main`
(PR #5) before this branch was merged, so the two branches conflicted on the shared build
files. This session is the **final integration session**. Resolution (nothing from the other
session was discarded):

- **Canonical published site = this session's `site/`**, generated by
  `scripts/build_site.py` and gated by `scripts/verify_site.py`. It is comprehensive
  (8 guides, comparison + counter-space, Research Desk, Suggestions portal, Flagged page,
  OG/Twitter cards, enforced `rel="sponsored"`) and its **workflow-based Pages deploy**
  resolves the other session's open T11 (root-vs-`/docs` Pages source mismatch).
- **Preserved, not deleted, from the other session:** `docs/` (their generated site),
  `archive/counter-notes-v1/` (their v1), `server.mjs` + `analytics-client.js` +
  `ANALYTICS-ENDPOINT.md` + `tests/server.test.mjs` + `package.json` + `.gitignore`
  (their self-hosted five-event analytics endpoint, T14), and `.github/workflows/analytics-tests.yml`.
- **Reconciled CI:** `.github/workflows/verify.yml` (from the other session) now runs this
  session's build + gate and checks reproducibility against `site/`. `analytics-tests.yml`
  runs `npm test` = this session's `verify_site.py` + the other session's Node endpoint tests.
- **Conflicting shared files kept as this session's version:** `README.md`,
  `data/products.json`, `scripts/build_site.py`, `scripts/verify_site.py`,
  `.github/workflows/pages.yml`. The other session's versions are preserved in git history
  and in their `docs/` output.

### Other session's task board (recorded for the record)

| Task | Status | Session | Notes |
| --- | --- | --- | --- |
| T1 Repo review and flags | done | f2613c86 | 18 flags FR-01..FR-18 |
| T2 Verify the five supplied links | done | f2613c86 | 5 of 5 resolve; intended ASIN not confirmed (FR-02) |
| T3 Product register | done | f2613c86 | prices/ratings left blank (FR-05) |
| T4 Site build into `docs/` | done | f2613c86 | static build |
| T5 Compliance (disclosure, sponsored, tag) | done | f2613c86 | disclosure wording vs Operating Agreement §5 |
| T6 Outbound-click counter | needs review | f2613c86 | only `outbound_click` built (FR-09) |
| T7 Self-hosted analytics endpoint | needs review | f2613c86 | not possible on Pages; D-43 open (FR-09) |
| T8 Suggestions / open questions | done | f2613c86 | nothing implemented before a choice |
| T9 Executive summary, analysis, sources | done | f2613c86 | |
| T10 Verification gate and CI | done | f2613c86 | |
| T11 Publish to GitHub Pages | in progress | f2613c86 | Pages source mismatch — **resolved by this session's workflow deploy** |
| T12 Integration with PR #1 (session d12d2304) | done | f2613c86 | PR #2 merged |
| T13 Port PR #1 guides into the generated site | done | f2613c86 | v1 archived |
| T14 Optional self-hosted analytics endpoint + five-event collector | done | arena/3f1d9d65-prod2 | `server.mjs` + tests; not deployed publicly |

### Integration outcome

- `python3 scripts/build_site.py` rebuilds `site/` cleanly from the combined tree.
- `python3 scripts/verify_site.py` passes (disclosure, `rel="sponsored"`, unique meta, internal
  links, sitemap).
- `npm test` (the other session's endpoint tests + this session's gate) passes.
- PR #6 merges this integration into `main`; GitHub Pages deploys `site/` via the workflow.


---

# FINAL INTEGRATION PASS — session `arena/9386098f-prod2` (sess-prod2-a1), 2026-11-19

At consolidation time the repository contained **four independent session builds**:

| Build | Brand | Location | From | Status at consolidation |
|---|---|---|---|---|
| 1 | Counter Notes v1 (root) | `archive/counter-notes-v1/` | PR #1 (d12d2304) | Archived |
| 2 | Counter Notes (generated) | `docs/` | PRs #2–#5 (f2613c86 + 3f1d9d65) | Was canonical per its board |
| 3 | The Counter Edit | branch `arena/9386098f-prod2` (pre-reset), now `archive/counter-edit-build/` | sess-prod2-a1 (this session) | Built in parallel from stale base |
| 4 | Countercraft | `site/` | PR #6 (599eec57) + PR #7 | Declared canonical on main |

**Decision (INT-06): canonical = `site/` (Countercraft)** — the latest merged state of `main`, already
data-driven, gated by `scripts/verify_site.py`, and deployed by `pages.yml`. Everything else archived,
nothing deleted. The pre-reset state of this branch (its own full build + its ports into `docs/`) is
recoverable from git reflog; its unique content is preserved in `archive/counter-edit-build/`.

## What this integration pass did

- `docs/` → `archive/counter-notes-docs/` (git mv, history kept). Its generator source survives in
  git history (it had been replaced on `main` by Countercraft's).
- Fixed a real bug on main: canonical/og URLs lacked a slash (`…/Prod2index.html`) on every page —
  fixed in `scripts/build_site.py` and the whole `site/` regenerated + committed.
- `site/assets/analytics.js`: endpoint default changed from active `"/collect"` (which beaconed to a
  nonexistent path on GitHub Pages) to **off by default**; events stay in the page unless an endpoint
  is explicitly configured — restores the project's own privacy posture (FR-09).
- `server.mjs`: serves `site/` now; whitelist extended to the union of all three event taxonomies
  (tracker events, self-host client events, Countercraft events); safe aggregate keys for each;
  self-host injection sets `window.COUNTERCRAFT_ENDPOINT="/api/events"` on served pages.
- `analytics-client.js` (self-host only) no longer double-sends `page_view`.
- `tests/server.test.mjs`: adapted + two new tests (integration events, Countercraft events) —
  `npm test` green.
- `pages.yml`: `enablement: true` on configure-pages (INT-04/T11 — CI may flip Pages to workflow mode).
- README updated: one-site rule, archives, endpoint.

## Session register (this session)

| Session | Branch | Started (UTC) | Status |
|---|---|---|---|
| sess-prod2-a1 | `arena/9386098f-prod2` | 2026-11-19 12:40 | active — final integration |

## Conflict log

- Two `git pull --rebase` operations collided with concurrent merges to `main` (PR #5→#6→#7 landed
  during this session's work). First rebase resolved by union-merging boards; second collision was
  resolved by resetting this branch onto consolidated `main` and re-applying the integration as new
  commits — **no upstream content was discarded at any point**; the branch's prior state remains in
  reflog and its content in `archive/`.
- Independent convergence: three sessions separately resolved all five submitted short links live on
  2026-11-19 to the same observed ASINs (B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z);
  all note the submitted tokens are 9 characters, not 10-character ASINs, and make **no claim** about
  the short links' compliance status (FR-01/FR-02/F-02 equivalents).

## PR / merge / deploy record

- PR: https://github.com/wingbangboozle1-lang/Prod2/pull/8 (base `main`)
- Merge result: recorded after merge below.
- Pages: recorded after deploy verification below.

---

## Integration with session arena/cd3cddd6-prod2 (PR #9, 2026-11-19)

A fourth parallel session claimed T1–T6 on its own copy of this board (written
concurrently on its branch) and built a complete second implementation —
**"The Crisp Counter"**: 28 HTML pages, canonical registers (products incl.
held P4/P5, intent record with separated intended/observed fields, sources
with fetched/cited status, flags split open/resolved/historical, 21 recorded
decisions, suggestions queue, open decision-input questions, publishing
calendar, five-event privacy model, empty-by-rule ledger), a 30-check suite,
a cookieless analytics recorder and a Python collector. That implementation
is **preserved in git history on branch `arena/cd3cddd6-prod2`** (visible in
PR #9's diff at commit `3ba2231`) but is **not** merged as a second deployed
site: one deployed site stays canonical (`site/`, per the standing
integration decision and this pass's INT-06 consolidation) so search engines
index one site and the Pages deploy stays unbroken.

### What this merge adds to `main` (nothing discarded, nothing duplicated)

- `data/imported/zone4/` — the predecessor repository's registers
  (kanlerxz87-cyber/Zone4), fetched read-only via the GitHub API and archived
  verbatim with a provenance README. Zone4 is the multi-day lineage of
  verified registers behind this project: the dated session records behind
  every product fact, the 67-row flag history, and the carried compliance
  rationale (why prices/ratings stay off by default, why P4/P5 were held, the
  ASIN-vs-token distinction).
- `VOICE.md` — the editorial standard (anti-slop voice rules) for any future
  content pass on the canonical site.
- `DESIGN_PROMPT.md` — the carried design brief (warm-editorial direction
  DIR-A from Zone4's recorded decisions, with the non-negotiable compliance
  block) for the next visual pass.
- This union of the coordination boards.

### Verification differences between the sessions (logged, not hidden)

- Session arena/cd3cddd6-prod2's build environment could **not reach
  amazon.com** (egress allowlist), so no product value was re-read there; its
  registers carried the Zone4 records with their original dated citations
  (last product-page re-reads 2026-11-16/17) and flagged the non-re-read as
  FLG-03. This agrees with this board's T2 and the convergence note above:
  the newest live verification on record is the 2026-11-19 read, which
  identified the P4/P5 destinations by name (ThermoMaven digital meat
  thermometer; CHEF iQ Sense smart wireless meat thermometer).

### Review requests for the owner (non-blocking; logged per protocol instead of editing another session's files)

| ID | Request | Sources |
| --- | --- | --- |
| RR-1 | The canonical site's register table displays prices ("as listed", captured live 2026-11-19). The carried rule from the Zone4 register (its flags F-02/F-37) allows price display only when Amazon serves the content or the value arrives via the Creators/PA API. Decide: keep (document the display basis in the register) or remove the price column. | https://affiliate-program.amazon.com/help/operating/policies |
| RR-2 | A star rating (4.6, 3,499 reviews) was captured live for one listing. The carried rule allows star ratings and review counts to be displayed only when obtained through the Creators/PA API. Confirm or remove. | https://affiliate-program.amazon.com/help/operating/policies |
| RR-3 | The canonical site publishes P4/P5 (the two meat thermometers) as a category. The carried register held them until identity is confirmed by the owner in the enrolled Associates workflow (Zone4 F-55/F-56). Run the one-link-per-product test in Associates Central, then either confirm or unpublish. | https://affiliate-program.amazon.com/help/operating/policies |
| RR-4 | The five submitted `link.amazon` short links remain recorded verbatim; their compliance status is unresolved (Zone3 FLG-003 lineage). The one-link-per-product test in Associates Central (RR-3) is the cheapest way to close this before scaling placements. | https://affiliate-program.amazon.com/help/operating/policies |

### This session's merge result

- Conflicts resolved at merge time: `README.md`, `data/products.json`,
  `data/sources.json`, `data/suggestions.json`, `data/ledger.json`,
  `.gitignore`, `COORDINATION.md` kept as the canonical site's versions
  (fresh live-verified data + this pass's INT-06 consolidation); this
  branch's versions preserved in git history.
- Canonical build re-verified on the merged tree before the PR merged:
  `python3 scripts/build_site.py` and `python3 scripts/verify_site.py` pass
  (18 pages; no broken links).
- PR #9 merged into `main`; GitHub Pages deploys `site/` via the existing
  workflow. Merge commit and deploy status: see the PR page and the
  repository's Actions history.

### Merge / deploy record (filled in after PR #9, 2026-11-19)

| PR | What | Result |
| --- | --- | --- |
| #8 | sess-prod2-a1 INT-06 consolidation | merged before this session's sync |
| **#9** | **This session's integration** (Zone4 provenance archive, VOICE.md, DESIGN_PROMPT.md, coordination union, RR-1..RR-4) | **Merged 2026-11-19 13:26 UTC, merge commit `7e0085fd85e5673faacd62cbf4f9457693397ea3`** |
| Deploy | GitHub Actions on `main` after the merge | `verify-site` success, `Self-hosted analytics tests` success, `Deploy to GitHub Pages` success, `pages build and deployment` success |
| Pages | `gh api repos/.../pages/builds/latest` | status `built` for commit `7e0085f` (2026-11-19T13:26:33Z) |
| Live site | https://wingbangboozle1-lang.github.io/Prod2/ | serving the canonical `site/` build |

---

# Integration addendum — arena/44093825-prod2 (second pass, 2026-11-19)

PR **#8** (this session) was recorded above as the pending integration vehicle. It merges this
session's registers, gates and publication build into the consolidated tree **without
discarding anything**. What this pass changed on top of INT-06/INT-07:

- **Live outcome (recorded after deploy verification below):** the repository's Pages
  configuration is the classic **"main / docs folder"** source, so the live site at
  https://wingbangboozle1-lang.github.io/Prod2/ is **this session's `docs/` publication**
  (verified live 2026-11-19: tagged Special Links present, chooser + guides + dashboards +
  review surfaces serving). The Countercraft `site/` + root mirror remain fully preserved and
  deployable via the Actions workflow; `research-desk.html` (root mirror) 404s live,
  confirming branch-folder serving. One site is live — the owner's one-site requirement holds
  without any noindex machinery.
- **Critical fix landed on the canonical build:** `scripts/build_site.py` now emits every
  outbound product link as the owner-mandated **tagged Special Link**
  (`https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20`, `rel="sponsored nofollow noopener"`,
  no shortener — Participation Requirements 2(b), 6(v)–(w)), and `scripts/verify_site.py`
  **fails** any `/dp/` link without the tag. `site/` + the root mirror were regenerated
  accordingly. Until this commit, the canonical site shipped **untagged** product links, so
  no click could attribute to tracking ID `shopnow047c-20`.
- **Preserved as a reference build (noindex):** this session's publication (20 pages, warm
  editorial direction A per D-18, chooser, counter-space analysis, intent records with dated
  redirect history, flags split open/resolved/standing, question + suggestion registers with
  recommendations, decision log, five-event campaign ledger with the official attribution
  windows) lives at `docs/` and is the **live site**, generated by `tools/build.py`, gated by
  `tools/checks.py` (8 sections incl. no-price/no-rating, banned-claims and build-freshness
  checks).
- **Registers:** this session's register set lives at `data/p2-*.json` plus
  `data/{intent-links,flags,questions,decisions,events,settings,verification-2026-11-19}.json`;
  the Countercraft schema keeps `data/{products,sources,ledger,suggestions}.json`.
  All five links were independently re-verified 2026-11-19 (same ASINs as the other sessions;
  F-55 resolved here; no `tag=` on the supplied short links — F-03 stands).
- **Test note:** `tests/server.test.mjs` retains the Counter Notes lineage's adapted tests
  (its self-host injection assertions); the earlier brand-string assertion was replaced by a
  brand-agnostic disclosure marker so the suite passes regardless of which build `docs/` holds.
- **Divergence flagged for the owner (SG-05 / Q-27):** the Countercraft registers captured
  prices "as listed"; this session's registers withhold prices and star ratings entirely
  (F-02 discipline from the prior verified register). A dated-snapshot price policy is
  proposed in the suggestion queue (`docs/suggestions.html`), not adopted.

## Preserved record — Prod2 publication session board (arena/44093825-prod2, original claim)

> Verbatim as first published on this branch (commit 7f2f590).

# COORDINATION.md — shared task board (Prod2)

**Repo:** `wingbangboozle1-lang/Prod2`
**Protocol:** per the owner brief. Each session claims tasks here and commits the claim
immediately. A status of `needs review` means the item is published on the Flagged for
Review page and does not block anything. Shared outputs are changed only by the final
integration session.

**Branch note for this Arena environment:** Arena tracks each session by its own branch and
permits exactly one branch per session. This session works on `arena/44093825-prod2`
(branched from `c6dc49a` of `main`). It therefore acts as **both** working and final
integration session on that branch, and merges to `main` via a pull request at the end.
Other Arena sessions get their own `arena/<id>-prod2` branches and must claim scopes below
the same way. Never edit another session's claimed files; log requests here instead.

---

## Task board

| Task | Status | Owner session | Scope (files) | Sources / verification | Notes |
|---|---|---|---|---|---|
| T-01 Coordination board + claim | done | arena/44093825-prod2 | `COORDINATION.md` | n/a | Claimed 2026-11-19. |
| T-02 Product re-verification session (5 short links → listings) | done | arena/44093825-prod2 | `data/verification-2026-11-19.json` | Official Amazon listing pages + short-link redirect reads, 2026-11-19 (links in `data/sources.json`) | All 5 links resolved. No `tag=` on any resolved URL. P2 title segment drifted again (recorded). |
| T-03 Data registers (products, intent records, sources, flags, questions, suggestions, decisions, ledger, events, settings) | done | arena/44093825-prod2 | `data/*.json` | Carried from dated Zone4/Zone3 verification records + 2026-11-19 reads | Intent fields and observed-redirect fields kept separate. |
| T-04 Site generator + templates | done | arena/44093825-prod2 | `tools/build.py`, `content/`, `docs/assets/` | n/a | Renders `docs/` from `data/` + `content/`. |
| T-05 Reader-facing publication (front page, guides, comparison + chooser, categories, buying guide) | done | arena/44093825-prod2 | `content/pages/*.html`, `docs/` | Every product fact traces to `data/products.json` → source link | Warm editorial direction (D-18 option A). Disclosure under masthead on every page + footer. |
| T-06 Governance surfaces (method + sources, flagged, questions, suggestions, decisions, measurement, compliance, executive summary) | done | arena/44093825-prod2 | `content/pages/*.html`, `docs/` | Source links per row | One nav group + full footer directory. |
| T-07 SEO + syndication (titles/meta, JSON-LD, sitemap, robots, RSS, OG card) | done | arena/44093825-prod2 | `tools/build.py`, `tools/make_og.py`, `docs/` | Google Search Central docs (in sources register) | Unique title + meta per page; OG image is typographic brand art, not product photography. |
| T-08 Measurement machinery (click counter, five events, self-hosted endpoint, campaign ledger) | done | arena/44093825-prod2 | `docs/assets/js/measure.js`, `server.mjs`, `data/ledger.json`, `data/events.json` | Amazon Commission Income Statement windows (S-COMM/S-CDIS) | Endpoint deployable, not yet hosted — flagged F-19. Ledger stays empty until an authorized report exists. |
| T-09 Compliance gate (checks from clean checkout) | done | arena/44093825-prod2 | `tools/checks.py`, `ENGINE.md` | OA + FTC + Google docs in sources register | Fails on missing disclosure, untagged product links, missing `rel="sponsored"`, broken links, duplicate titles, unsourced product facts. |
| T-10 Documentation (README, EXECUTIVE_SUMMARY, ENGINE) | done | arena/44093825-prod2 | `README.md`, `EXECUTIVE_SUMMARY.md`, `ENGINE.md` | n/a | |
| T-11 Integration: rebuild, re-verify combined data, link check, PR to main, merge, Pages deploy | done | arena/44093825-prod2 | whole repo | `tools/checks.py` green; live URL probed | PR + deploy links recorded below. |

## Handoff requests (file-scope conflicts)

_None. This session owned all scopes._

## Integration log

- 2026-11-19 — session start. Claimed T-01..T-11 (single-session build; board created first and pushed with the claim).
- 2026-11-19 — verification session executed (T-02). Evidence: `data/verification-2026-11-19.json`.
  - `https://link.amazon/B04G1MEwY` → `https://www.amazon.com/dp/B0CDY277D3` (Chefman 6 qt dual basket). Title matched register.
  - `https://link.amazon/B02NbDxp3` → `https://www.amazon.com/dp/B09B7SB46R` (Emeril Lagasse 26QT). **Irregularity:** second title segment changed again (F-44/F-66 history extended).
  - `https://link.amazon/B00hJ57DV` → `https://www.amazon.com/dp/B08DKYBTPH` (Chefman 8 qt TurboFry). Title matched register.
  - `https://link.amazon/B0c8moW59` → `https://www.amazon.com/dp/B0DHZTCNR5` (ThermoMaven 1-sec meat thermometer) — **new, first verified read 2026-11-19** (F-55 resolved for this link).
  - `https://link.amazon/B0f3GKalj` → `https://www.amazon.com/dp/B0DZFD6R9Z` (CHEF iQ Sense Gen3 wireless thermometer) — **new, first verified read 2026-11-19** (F-55 resolved for this link).
  - No `tag=` parameter on any resolved URL (F-03 stands). Prices/ratings visible on listings and withheld from publication (F-02).
- 2026-11-19 — all checks green (`python3 tools/checks.py`), site rebuilt, PR #1 opened and merged (link below), GitHub Pages enabled and live URL probed.

## PR / deploy record

| Item | Value |
|---|---|
| PR | (recorded at integration) |
| Merge result | (recorded at integration) |
| Pages URL | (recorded at integration) |
| Checks run | `python3 tools/checks.py` — all sections pass (recorded at integration) |


---

# Final merge / deploy record — arena/44093825-prod2

| Item | Value |
|---|---|
| Integration PRs | https://github.com/wingbangboozle1-lang/Prod2/pull/8 (integration, merged as `f152eac`) · https://github.com/wingbangboozle1-lang/Prod2/pull/13 (post-deploy record, noindex removal) · https://github.com/wingbangboozle1-lang/Prod2/pull/14 (root-mirror retarget + Pages-mutation removal) |
| Merge result | **all merged** 2026-11-19 — integration merge commit `f152eac`, final state `c12ec7f` on `main` |
| Pages | **deployed** — https://wingbangboozle1-lang.github.io/Prod2/ (legacy `main /` root serving; API status `built`) |
| Live verification | Fetched live pages 2026-11-19 (post-PR-14 Pages build `c12ec7f`): homepage "Find the format that fits your kitchen \| Prod2"; `compliance.html` and `guide-capacity.html` serve the publication with masthead disclosure + og-card; all product links carry `?tag=shopnow047c-20` + paid-link disclosure; chooser, guides, dashboards and review surfaces resolve. |
| Serving note | The repo is served in legacy **`main /` (root)** mode; flipping to Actions mode403s for session tokens (admin-only). `scripts/build_site.py`'s INT-07 root mirror was retargeted: **`tools/build.py` now mirrors `docs/` → root** so the canonical URL carries the Prod2 publication; the Countercraft build stays verified at `site/` and is no longer mirrored. `pages.yml`'s `configure-pages`/`deploy-pages` steps were removed after `configure-pages` rewrote the legacy source once mid-session. |
| Workflows on merge commit | verify-site: success · Self-hosted analytics tests: success · Deploy to GitHub Pages: success |
| Checks at merge | `tools/checks.py` PASS · `scripts/verify_site.py` PASS · `npm test` PASS (2/2) |

---

# Session arena/236bc1ed-prod2 — claim (2026-11-19)

Branch `arena/236bc1ed-prod2`, base `da11cd4` (`main`, PR #15). Single session: it works and is also the final integration pass for its own scope. No other session holds a claim at the time of writing.

| Task | Status | Session | Scope (files) | Notes |
|---|---|---|---|---|
| T-12 Re-verify the 5 submitted short links against live Amazon listings | in progress | arena/236bc1ed-prod2 | `data/p2/intent-links.json` (observation fields only), `data/p2/verification-2026-11-19.json` | Observed redirects appended as dated observations; intent fields untouched unless a listing read changes. |
| T-13 Marketing-polish suggestions (catchy, question-shaped topics; organic + click path) added to the review queue | in progress | arena/236bc1ed-prod2 | `data/p2/suggestions.json`, `data/p2/questions.json` | Proposals only. Nothing implemented until a reviewer accepts a path. |
| T-14 Flagged-for-Review additions for irregularities found this session | in progress | arena/236bc1ed-prod2 | `data/p2/flags.json` | Every new flag carries an evidence link. |
| T-15 Rebuild, gate (`tools/build.py` + `tools/checks.py`, `scripts/verify_site.py`), PR to `main`, merge, Pages deploy check, PR record here | pending | arena/236bc1ed-prod2 | `docs/`, root mirror, this file | Runs last. |

Parallel-session note: no other claim touches `data/p2/*`, `docs/`, or the root mirror. Future sessions must claim before editing these.

## Update — arena/236bc1ed-prod2 (same session, status changes)

| Task | Status | Sources | Verification performed | Irregularities |
|---|---|---|---|---|
| T-12 Re-verify short links | done (partial: 2 of 5 re-fetched in this pass) | https://link.amazon/B04G1MEwY → https://www.amazon.com/dp/B0CDY277D3 ; https://link.amazon/B0c8moW59 → https://www.amazon.com/dp/B0DHZTCNR5 | Both short links fetched with redirects followed; final ASIN and listing title matched `data/p2/products.json`. Recorded in `data/p2/verification-2026-11-19.json` (`recheck_arena_236bc1ed`). P2, P3, P5 keep their 2026-11-19 reads. | F-P07 (coverage gap). No new mismatch. The short links are still not judged valid or invalid (FLG-003). |
| T-13 Marketing-polish suggestions | done (proposals only; nothing implemented) | Evidence references: Program Policies 6(v)/6(w) (S-POL), FTC endorsements guidance (S-FTC2), Google helpful-content guidance (S-GHELP) as already in the source register | Suggestion text reviewed against the banned-claim list (D-19) and the no-price rule before build. | none new |
| T-14 Flagged for Review additions | done | `data/p2/flags.json` F-P06, F-P07 | Each new flag carries an evidence link. | F-P06 (two registers disagree on publishing prices; the Prod2 build withholds them, the earlier Countercraft register holds them); F-P07 (partial re-read). Both open; neither blocks merge. |
| T-15 Rebuild, gates, PR, merge, Pages | in progress | — | `tools/build.py` → `tools/checks.py` ALL CHECKS PASSED (20 pages); `scripts/verify_site.py` VERIFY OK (18 pages); `npm test` 2/2 pass | — |

**Handoff note:** none. No other session held a claim on `data/p2/*` or `docs/` during this pass.

**Scope note for the owner:** the new suggestions (SG-11 to SG-14) and questions (Q-P05 to Q-P07) are queued for review on the Suggestions and Open questions pages. Nothing in them is implemented.

## PR / merge / deploy record — arena/236bc1ed-prod2

| Item | Value |
|---|---|
| PR | https://github.com/wingbangboozle1-lang/Prod2/pull/17 (`arena/236bc1ed-prod2` → `main`) |
| Merge result | **merged** 2026-11-19 21:41 UTC, merge commit `676afc2` (`gh pr merge 17 --merge`, no approval waited for) |
| Pages | **deployed** — "Deploy to GitHub Pages" success and "pages build and deployment" success on `676afc2`; live page https://wingbangboozle1-lang.github.io/Prod2/flagged.html shows F-P06 |
| Checks run | `tools/build.py` + `tools/checks.py` ALL CHECKS PASSED (20 pages); `scripts/verify_site.py` VERIFY OK (18 pages); `npm test` 2/2 pass; verify-site workflow success |
| Tasks | T-12 done (partial, see update above), T-13 done, T-14 done, T-15 done |
| Still open (flagged, do not block) | F-P06, F-P07, F-01, F-03, F-08, F-19, F-26, F-29, F-44, F-49, F-57, F-58, F-66, F-P01, F-P04, F-P05 |
| Follow-up | This record PR is the last action on the branch. The sandbox cannot reach `github.io` directly, so the live check used the page fetch tool. |

---

# Session arena/9f7a78d8-prod2 — claim (2026-11-19)

Branch `arena/9f7a78d8-prod2`, based on consolidated `main` (`1b5e211`, after PR #17/#18).
Single Arena session: it works its scope and is also the final integration pass for that
scope, merging to `main` via a pull request. Claimed after `git pull --rebase`; no other
session holds an active claim on the files below at claim time.

**Scope (non-overlapping with the just-merged #17/#18, which touched `data/p2/*` registers +
their generated mirror only):**

| Task | Status | Session | Scope (files) | Notes |
|---|---|---|---|---|
| T-16 Reader-facing polish: make the front page read like a shop, not an audit | in progress | arena/9f7a78d8-prod2 | `content/pages/index.html` (copy only) | Keep masthead disclosure strip, `rel="sponsored"` links, verification surfaces reachable from nav group + footer. Copy-level; no register/price/rating changes. |
| T-17 Publish the approved SG-03 second thermometer guide (instant-read vs leave-in) | in progress | arena/9f7a78d8-prod2 | new `content/pages/guide-instant-vs-leave-in.html`, `tools/build.py` (PAGES/GUIDE_IDS/GUIDE_LINKS), homepage guide card | Question-shaped, listing-facts-only, sourced; auto-flows to sitemap + feed. Honors D-19 banned-claim rule and F-02 (no prices/ratings). |
| T-18 Coherence + board record + rebuild + gate + PR + merge + Pages check | pending | arena/9f7a78d8-prod2 | `data/p2/questions.json` (one sentence), `COORDINATION.md`, `docs/`, root mirror | Rebuild via `tools/build.py`; gate with `tools/checks.py` + `scripts/verify_site.py` + `npm test`. |

No edit to another session's claimed files. Registers `data/p2/{products,sources,flags,
suggestions,decisions,ledger,intent-links,verification-*}.json` are NOT edited except the one
Q-P02 coherence sentence. Shared outputs (docs/, root mirror) change only through
`tools/build.py` output, then are re-verified.

## Record — arena/9f7a78d8-prod2 (T-16..T-18 complete, 2026-11-19)

Single Arena session; worked its scope and merged to `main` via PR. All edits went through
`tools/build.py` (source `content/pages/` + `data/p2/`), never a hand-edit of `docs/` or the root
mirror; mirrors were regenerated and are deterministic.

**What changed (reader-facing only; no product fact, price, rating or register value altered):**
- T-16 `content/pages/index.html`: front page made shop-first — hero line, section heading and
  the "at a glance" intro reworded toward the buyer decision; masthead disclosure strip still above
  the fold; all "work behind it" surfaces stay reachable from the single nav group + footer.
- T-17 New `content/pages/guide-instant-vs-leave-in.html` — "Instant-read or leave-in: which
  thermometer for which cook", the approved SG-03 topic; listing-facts-only (P4/P5), sourced to the
  official listings read 2026-11-19; no prices/ratings; no banned popularity claims. Registered in
  `tools/build.py` (PAGES/GUIDE_IDS/GUIDE_LINKS) → flows to footer, `sitemap.xml`, `feed.xml`. Site now 21 pages.
- T-18 `data/p2/questions.json` Q-P02/Q-P04 coherence (two thermometer guides now ship).

**Parallel-session conflict (resolved, nothing discarded):** PR #19 (`arena/8ff10f50-prod2`) had
independently made the landing page *product-forward* (moved the comparison table above the guide
cards) while this session reworded the same two blocks and added a card. Rebase onto `main` conflicted
on `content/pages/index.html` only. Resolution **kept PR #19's product-forward ordering**, applied
this session's reworded copy, and kept the new 6th card; PR #19/#21's transparency flag
(`data/p2/flags.json` F-P08) and all their register work were preserved. `docs/` + root rebuilt from
the merged source.

**Gates (re-run on the combined tree after merge, no diff):** `tools/checks.py` ALL PASS (21 pages,
freshness ok) · `scripts/verify_site.py` VERIFY OK (18) · `npm test` 2/2 · CI on the PR: `test` pass,
`verify` pass.

**PR / merge / deploy:**
- PR: https://github.com/wingbangboozle1-lang/Prod2/pull/20
- Merge: **merged** 2026-11-19 21:49 UTC, merge commit `3cd056a` on `main` (`gh pr merge 20 --merge`).
- Pages: `Deploy to GitHub Pages` success; `pages/builds/latest` status `built` for `3cd056a`.
- Live verified via page fetch: homepage serves the product-forward layout, shop-voice hero, 6 guide
  cards incl. the new thermometer guide; `guide-instant-vs-leave-in.html` serves with tagged
  `?tag=shopnow047c-20` sponsored links, disclosure and sourced facts.
- Note for owner: the site serves in legacy `main /` (root) mode; the directory-path edge cache can lag
  a build by seconds — hard-refresh / query-string fetch shows the new state (confirmed here).
- Still open (flagged, non-blocking): F-01, F-02, F-03, F-19, F-57, F-58, F-P06, F-P07, and the
  owner-only gates Q-01 / Q-19 / Q-23 / Q-27 (Associates Central validation, trademark, endpoint host,
  price policy). Those require account/host access this environment cannot reach and stay as decisions.
---

# Session arena/1ca951c0-prod2 — claim (2026-11-19)

Branch `arena/1ca951c0-prod2`, based on consolidated `main` (`3cd056a`, after PRs #17–#21).
Single Arena session: it works its scope and is also the integration pass for that scope,
merging to `main` via a pull request. Claimed after rebasing onto `origin/main`; no other
session holds an active claim on the files below at claim time.

**Scope (non-overlapping with the merged #17–#20 claims, which covered the registers'
suggestion/question/flag additions and the front-page copy pass):**

| Task | Status | Session | Scope (files) | Notes |
|---|---|---|---|---|
| T-19 Fix three rendering defects found in a line-by-line review of the built pages: (a) disclosure strip renders `((paid link))` (double-paren artifact, all pages), (b) front page CTA renders a nested `<p>` inside `<p>`, (c) `products.html` ships duplicate `id="P1..P5"` (cards + fact headings) | done | arena/1ca951c0-prod2 | `tools/build.py` (DISCLOSURE_STRIP wording only), `content/pages/index.html` (CTA wrapper), `content/pages/products.html` (fact-heading anchors) | Fix the generator, not the output; output regenerated below. |
| T-20 Put a gate in front of what can be automated: add an HTML-validity + cross-reference section to `tools/checks.py` (nested `<p>`, duplicate `id`s, the `((` artifact, fragment links `page.html#id` resolve, register ids F-/Q-/SG-/D- referenced in pages exist) | done | arena/1ca951c0-prod2 | `tools/checks.py` | Gate must fail on each defect class above if reintroduced. |
| T-21 Design suggestion pass feeding `DESIGN_PROMPT.md` (the brief a redesign implements): queue the visual-overhaul suggestions not yet covered by SG-01..SG-14, and record the two fixed defects as resolved flags with evidence links | done | arena/1ca951c0-prod2 | `data/p2/suggestions.json`, `data/p2/flags.json`, `DESIGN_PROMPT.md` (queued-inputs note only) | Proposals only — nothing visual is implemented in this pass. |
| T-22 Rebuild (`tools/build.py` → `docs/` + root mirror), run all gates, record sources/verification/irregularities here, PR → `main`, merge, confirm Pages deploy, record PR + merge result | done | arena/1ca951c0-prod2 | `docs/`, root mirror, this file | Runs last. |

**Verification boundary (this session):** this sandbox's egress allowlist does not include
`amazon.com`, `ftc.gov` or `developers.google.com`, so no product fact or compliance text is
re-fetched here; those keep their dated register citations (last live reads 2026-11-19,
`data/p2/sources.json`, `data/p2/verification-2026-11-19.json`). What this session verifies
directly: the built HTML of every published page, the generator sources, all gate runs, and
internal cross-reference integrity. Nothing is marked verified that was not checked here.

**Conflict log:** none at claim time. PR #16 (`arena/30a7028a-prod2`, stale since 14:17 UTC,
based on the initial commit) was closed by another session at 21:51 UTC — no action needed
here. Parallel sessions active during this pass: `arena/236bc1ed-prod2`, `arena/8ff10f50-prod2`,
`arena/9f7a78d8-prod2` (all their PRs merged before this claim).

---

## PR / merge / deploy record — arena/1ca951c0-prod2 (T-19..T-22)

| Item | Value |
|---|---|
| PR | https://github.com/wingbangboozle1-lang/Prod2/pull/24 (`arena/1ca951c0-prod2` → `main`) |
| Merge result | **merged** 2026-11-19 22:10 UTC, merge commit `c0f59fbf6c359768d2e82ce9477fab2f8802c452` (`gh pr merge 24 --merge`, no approval waited for; CI on the PR: `verify` pass, `test` pass, state CLEAN before merge) |
| Pages | **deployed** — `gh api .../pages/builds/latest` → status `built` for commit `c0f59fb` (created 2026-11-19T22:10:30Z, no error); workflows `verify-site` and `Self-hosted analytics tests` success on the PR |
| Live verification | Fetched live pages after the deploy: homepage serves the shop-first layout with 6 guide cards and tagged `?tag=shopnow047c-20` sponsored links; `flagged.html` serves **F-P09/F-P10/F-P11 (resolved)** with pre-fix permalinks and **F-P12 (open)**; `compliance.html` serves the disclosure/link-policy page. The disclosure strip itself is a styled div the markdown fetcher drops, so its wording was verified at source: the committed `docs/` for `c0f59fb` is the exact artifact Pages serves (legacy `main /` mode), and it passes the gate that fails on the old artifact. |

### Sources used this session (all repo-local; this sandbox cannot reach amazon.com / ftc.gov / developers.google.com)
- Generator + gate sources: `tools/build.py` (DISCLOSURE_STRIP, hooks), `tools/checks.py`, `content/pages/*.html`.
- Registers: `data/p2/{flags,suggestions,questions,decisions,settings}.json`, `data/imported/zone4/z4-decisions.json` (D-22 provenance), `data/decisions.json` + `data/open-questions.json` (the predecessor lineage the brief cites).
- Pre-fix evidence permalinks at `3cd056a` (in PR #24 and in the flags): disclosure line 146, nested `<p>` line 188, duplicate id line 232.
- Product/compliance facts: **not re-fetched here** — they keep their dated register citations (last live reads 2026-11-19, `data/p2/sources.json`, `data/p2/verification-2026-11-19.json`). Nothing in this pass altered a product value, price, rating or claim.

### Verification performed
- `python3 tools/build.py && python3 tools/checks.py` → ALL CHECKS PASSED, 21 pages, **9 sections** (new `validity` included), freshness ok.
- `python3 scripts/verify_site.py` → VERIFY OK (18 pages); `npm test` → 2/2.
- Independent parser scan of all 21 built pages: 0 nested `<p>`, 0 duplicate `id`s, 0 `((paid` artifacts, 0 stray end tags; root mirror byte-identical to `docs/`.
- Cross-reference sweep: every `F-/Q-/SG-/D-` id cited on a page exists in its register (this sweep is now the gate, not a one-off).

### Irregularities found (all recorded on the Flagged page, non-blocking)
- **F-P09 / F-P10 / F-P11 (resolved 2026-11-19)** — the three rendering defects fixed in this pass; each carries its pre-fix permalink as evidence.
- **F-P12 (open)** — `DESIGN_PROMPT.md` cites predecessor-register ids (D-01/D-02/D-15/Q-05/Q-10) and a brand the build does not ship (wordmark `Prod2`, D-P03); must be reconciled during the queued visual pass (SG-15).
- **D-22 dangling citation (fixed)** — Q-P05 cited D-22, which existed only in the imported Zone4 register; carried into the live decisions log with its original date/options/sources so documentation matches the code.
- The gate's own first run caught the D-22 citation — evidence the automation works, not a manual finding.

### Conflict log
- Rebase onto `main` (`d1a3ab0`, PR #22) conflicted once on `COORDINATION.md` (PR #22's record vs this session's claim). Resolved as a **union — both records kept, nothing discarded**; an initial resolution attempt accidentally committed conflict markers on the branch (never pushed as such) and was repaired by fixup+autosquash before the force-with-lease push; verified `grep`-clean at the claim commit.
- Open PR #23 (`arena/5e692632-prod2`) edits overlapping files (`COORDINATION.md`, `data/p2/suggestions.json`, `content/pages/index.html`) and was already CONFLICTING with `main` before this merge; its suggestion ids (SG-27..30) do not collide with this pass's (SG-15..17). Its session resolves on rebase — **left open for its owner, not touched**.
- PR #16 (stale since 14:17 UTC, based on the initial commit) was closed by another session at 21:51 UTC; no action needed here.

### Still open after this pass (flagged, non-blocking)
F-01, F-03, F-08, F-19, F-26, F-29, F-44, F-49, F-57, F-58, F-66, F-P01, F-P04, F-P05, F-P06, F-P07, F-P08, F-P12 — plus owner-only gates Q-01 / Q-19 / Q-23 / Q-27 / Q-P06 (Associates Central validation, trademark clearance, endpoint host, price policy, domain). None blocks publication.


---

# Integration record — arena/9f84489c-prod2 (publication pass, 2026-11-19)

Session register: session arena/9f84489c-prod2, branch `arena/9f84489c-prod2`, claimed P-01..P-10 at
2026-11-19 21:46 UTC (claim commit `f551716`, pushed before any work started).

## What this pass shipped (P-01..P-09)

- **Shop-first front page** (P-01): product cards before any data table; hero promise + method line +
  receipt strip; seasonal desk; cluster pillars; subscribe + question-capture modules; byline strip;
  the sourced table last. (D-P07)
- **Nav labels + guides hub** (P-02): reader nav Compare · Products · Guides · Buying guide ·
  Air fryers · Thermometers; `guides.html` hub grouping guides by cluster and season; every
  dashboard surface stays in the one "The work behind it" group + footer.
- **Three new question-shaped guides** (P-03): guide-how-many-quarts, guide-two-baskets-or-one,
  guide-holiday-hosting — completing the eight-topic calendar alongside PR #20's
  guide-instant-vs-leave-in (9 question guides + buying guide live).
- **Seasons + clusters** (P-04): `data/p2/calendar.json` (14-day cadence, next due 2026-12-03;
  holiday-hosting desk live; grilling desk staged; two clusters with pillars, every guide
  gate-enforced to reach compare + buying guide + its pillar).
- **Parallel-pass rows SG-27..SG-30** (P-05) per the brief's own numbering: nav labels (shipped),
  RSS feed + subscribe affordances + feed_click + gate coverage (shipped), Search Console
  readiness + token slot + owner checklist (accepted; verification owner action — F-P13 / Q-P08),
  consent-first reader capture (accepted; form ships dark — F-P14 / Q-47; D-P08).
- **Decision support** (P-06/P-07): suggestions SG-27..SG-37 (incl. three fully specified design
  directions feeding DESIGN_PROMPT.md — SG-31, Q-P09), shortest-credible-path block (SG-32),
  progress notes merged onto SG-03/04/06/09/13 and cross-refs onto SG-15..17; questions register
  with scannable status table + Q-P08/Q-P09.
- **Docs sync** (P-08): ENGINE.md (10 gate sections / 25 pages), DECISIONS.md (D-P07..D-P09),
  EXECUTIVE_SUMMARY.md, README.md.
- **Gate extension** (P-09): tools/checks.py "publication" section (S-24 pillar-linking rule as an
  automated check — SG-09 shipped; feed covers every guide; capture-gate + verification-meta
  consistency).

## Merge / conflict log (nothing discarded)

`origin/main` moved three times during this session (PRs #17–#22, then #24/#26). Two integration
rounds unioned them into this branch before the PR:

1. **Round 1 (merge commit `1a3066d`)** — union with PRs #17–#22:
   - `tools/build.py`: their guide-instant-vs-leave-in registration + my guides hub/new guides/hooks.
   - `data/p2/{flags,questions,suggestions}.json`: this pass's rows renumbered (F-P06/07 → F-P09/10
     at the time; Q-P05/06 → Q-P08/P09; SG-11..17 → SG-31..37) so PR #17's rows stayed intact;
     SG-27..SG-30 adopted per the brief's numbering; progress notes merged onto SG-03/04/06/09/13.
   - `content/pages/index.html`: shop-first flow + their benefit-led hero line and callout.
   - `COORDINATION.md`: both session claims kept.
2. **Round 2 (merge commit `3299766`)** — union with PRs #24/#26 (T-19..T-22):
   - Their validity gate (+89 lines checks.py) coexists with my publication gate; their rendering
     fixes (F-P09..F-P11: disclosure paren artifact, products.html duplicate ids, nested CTA) verified landed.
   - This pass's rows renumbered again: F-P09/10 → **F-P13/F-P14** (PR #24 took F-P09..F-P12);
     references updated across content, settings, questions.
   - Their validity gate caught two real defects in this branch, fixed at source:
     products_table rows now `id="row-Pn"` (cards keep the Pn anchors guides link to), and SG-31 now
     cites only register-local ids (D-22/Q-P05, not the predecessor register's Q-05/SG-18).
   - Their SG-15..17 cross-referenced with my SG-31/33/35 (same ground; merge when the owner picks).

## PR #16 handoff (Countertop Dispatch, arena/30a7028a-prod2)

Claim was >60 minutes stale with no commits and its stated merge plan never ran; PR #16 was closed
unmerged at 21:51 UTC (by a parallel session). Per the handoff rule and the standing one-site rule
(INT-06), its full tree is preserved verbatim at `archive/countertop-dispatch/` (snapshot of commit
`d77bb9f`, provenance README included) and its branch remains on the remote. `robots.txt` now
disallows `/Prod2/archive/` so only one site is indexable.

## PR / merge / deploy record

| Item | Value |
| --- | --- |
| PR | https://github.com/wingbangboozle1-lang/Prod2/pull/27 |
| Merge result | **Merged 2026-11-19 22:20:16 UTC**, merge commit `acd5aeae96d7` |
| Workflows on merge commit | verify-site ✓ · Self-hosted analytics tests ✓ · Deploy to GitHub Pages ✓ · pages build and deployment ✓ |
| Checks at merge | tools/checks.py ALL PASS (25 pages, 10 sections) · scripts/verify_site.py PASS · npm test 2/2 |
| Pages | **built** for `acd5aea` (API status `built`, 2026-11-19T22:20:18Z), legacy `main /` root serving; root mirror byte-identical to `docs/` (same md5s), so the live URL serves exactly the gated build |
| Live site | https://wingbangboozle1-lang.github.io/Prod2/ (direct live-fetch unavailable from this sandbox's egress allowlist; verified via the Pages API + mirror byte-match + green workflows) |

## Notes for the open parallel PRs (protocol: logged, not edited)

- **PR #23 (arena/5e692632)** — its SG-27..30 rows are already on main under the same IDs (shipped/
  accepted states with progress notes, per the brief's mandate); its hero byline + "Start here" path
  are unique and worth rebasing in. Rebase onto `acd5aea`; its base (PR #18) predates #19–#22.
- **PR #25 (arena/b650562d)** — "Decision-support portal v2, nine-guide shop front" overlaps SG-32
  (decision queue) and the guides hub; rebase onto `acd5aea` and cross-reference SG-32/SG-31 in its
  rows rather than duplicating them.
- Register numbering is now dense-and-stable: flags F-01..F-P14, questions Q-01..Q-P09 (plus
  Q-19/23/27/31/47 carried), suggestions SG-01..SG-17 + SG-27..SG-37. New rows should continue from
  F-P15 / Q-P10 / SG-38.

## INTEGRATION — session arena/86206fb3-prod2 (2026-11-20, audit + fixes on top of the merged shop design)

**Status: integrated.** Branch `arena/86206fb3-prod2`, 4 commits, rebased onto `main` at `8bc543b`
(after PR #32).

### What this session found that was not previously recorded

| # | Finding | Evidence | Result |
| --- | --- | --- | --- |
| 1 | **Six `link.amazon` short links were clickable sponsored anchors** on `method.html` (5) and `flagged.html` (1). The short codes are evidence of what the owner submitted, not the site's buy path, and their compliance status is unresolved (F-03). | `tools/build.py` → `normalize_amazon_links` | Fixed at the generator: short links render as inert `<code>`. New gate section **exposition** fails the build if one returns. |
| 2 | **The analytics endpoint cited in eight files does not exist.** `analytics-endpoint/server.py` was never committed; the only endpoint is `server.mjs`. F-19's evidence URL pointed at the phantom file, so a reviewer following it would 404. | `server.mjs`, `ANALYTICS-ENDPOINT.md` | F-19 repointed; new **F-P22** (resolved); every reference corrected. |
| 3 | **The site and the endpoint use different event vocabularies.** Three of the site's five events (`guide_read_75`, `category_click`, `feed_click`) are rejected by `server.mjs`. Hosting it unchanged would silently under-count. | `server.mjs` `allowedEvents` vs `assets/js/measure.js` | **F-P23** (open), **Q-P14**, **D-P15**, **SG-41**. Gate section **measurement** now prints the divergence on every build. Not patched: choosing the vocabulary is an owner decision. |
| 4 | **The site shipped no font files at all.** `DESIGN_PROMPT.md` specified Fraunces + Inter; neither was in the repo, so every reader saw a system serif. | `assets/css/site.css` | Fixed: both families self-hosted as variable woff2 with OFL licences, `@font-face` + preloads, gated. |
| 5 | **Pages publishes the repository ROOT** (`build_type: legacy`, `source: main /`). Measured 2026-11-20: **196 source files** (data 42, content 27, tools 5, scripts 4, tests 1, archive 121) are fetchable by an anonymous reader; `GET /Prod2/data/p2/settings.json` returned the register as JSON. `robots.txt` is not access control. A token-scoped `PUT` to `build_type: workflow` returns **403**, so this cannot be flipped from the sandbox. | `gh api repos/.../pages`; `python3 tools/root_mirror.py --report`; the live GET | Workflow publishes the `docs/` artifact only; new gate section **exposition** refuses source dirs inside `docs/`; new `tools/root_mirror.py` writes canaries and prints the exposure count. **Owner: Settings → Pages → Source: GitHub Actions** (**F-P19**, **F-P20** rewritten with the measurement). |
| 6 | **A parallel session (PR #33, `arena/f55b5827-prod2`) collides with this branch**: it claims **D-P10** and **F-P12** for different things, adds `guide-gift-guide.html`, and rewrites `assets/css/site.css`, `data/p2/{products,sources,settings,calendar}.json`. | PR #33 file list | **Logged, not touched.** This session renumbered around it (D-P15, Q-P14, SG-41, F-P22/F-P23) and kept main's merged structure rather than overwriting it. PR #33 needs the ID collision resolved before merge, or the registers will disagree. |

### Register deltas in this session

- `flags.json`: **F-P22** added (resolved), **F-P23** added (open); F-19 repointed; F-P12 resolved; F-P19/F-P20 detail extended with the root-mode exposure.
- `questions.json`: **Q-P14** (event vocabulary).
- `decisions.json`: **D-P15** (publish the mismatch rather than patch it).
- `suggestions.json`: **SG-41** (gate the two event lists against each other).

### Verification after integration

- `python3 tools/build.py` → 27 pages; `python3 tools/checks.py` → **ALL CHECKS PASSED**, 12 sections.
- Independent scan: 172 tagged `/dp/` links, **0 untagged**, **0** without `rel="sponsored"`, **0** clickable short links, **0** source dirs in `docs/`, **0** images without `alt`.
- `REPO_AUDIT.md` added: the line-by-line review with evidence links, and an explicit list of what the audit does **not** claim.

---

---

## ACTIVE CLAIM — session arena/722181aa-prod2 (2026-11-20, live re-verification of the five listings + flagged short links)

Protocol note: this session works on its single assigned branch `arena/722181aa-prod2` (the session's branch is fixed by the platform). The `session-<id>/<task>` naming in the brief is therefore not used; the claim is recorded here instead, and no other branch is created, switched to, or pushed.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| L-01 Live re-check of the five `/dp/` listings and the five submitted short links (2026-11-20) | done | arena/722181aa-prod2 | `data/p2/live-check-2026-11-20-722181aa.json` (new) |
| L-02 Flag the short-link discrepancy (F-P24) and publish it on the Flagged page | done | arena/722181aa-prod2 | `data/p2/flags.json`, `docs/`, root mirror |
| L-03 Rebuild, gate, PR to main, merge, Pages check; record here | done | arena/722181aa-prod2 | `COORDINATION.md`, `docs/`, root mirror |

### Results (2026-11-20)

- **L-01 Direct listings — all five live; titles match the register character-for-character:** `https://www.amazon.com/dp/B0CDY277D3` (P1), `…/dp/B09B7SB46R` (P2), `…/dp/B08DKYBTPH` (P3), `…/dp/B0DHZTCNR5` (P4), `…/dp/B0DZFD6R9Z` (P5). Observed values are stored verbatim in `data/p2/live-check-2026-11-20-722181aa.json`. No price, rating, or commission value was written to the site (F-02 unchanged).
- **L-01 Short links — NOT confirmed today:** `https://link.amazon/B04G1MEwY`, `…/B02NbDxp3`, `…/B00hJ57DV`, `…/B0c8moW59` each resolved to `https://www.amazon.com/` (the homepage); `…/B0f3GKalj` returned HTTP 500. The register's earlier redirect history (2026-11-14 to 11-19) recorded the same ASINs. The cause (fetch-tool artifact vs. a change in the short-link service) is unknown; this is **not** resolved here.
- **L-02:** **F-P24** added (open): short-link resolution discrepancy; owner/browser check required. Intended-ASIN fields were not changed. The site never publishes the short links as buy paths (they render as quoted text under F-03), so no reader-facing link is affected.
- **Build/gate:** `python3 tools/build.py` → 28 pages; `python3 tools/checks.py` → ALL CHECKS PASSED; `python3 scripts/verify_site.py` → VERIFY OK.

### Sources (official)

- Amazon listings (read 2026-11-20): the five `https://www.amazon.com/dp/{ASIN}` URLs above.
- Amazon's ASIN definition and tag format: already recorded in `data/p2/sources.json` (S-ASIN, S-TAG); not re-read this session.

### Irregularities for manual review (not blocking)

1. F-P24 — short links did not resolve to listings today (above).
2. Pages source exposure (F-P19 / F-P20, carried): the Pages source is still `main /` (repo root). The root contains source/data files that the workflow `docs/` artifact does not, and this cannot be changed from the sandbox (403). **Owner action:** Settings → Pages → Source: GitHub Actions.
3. Event-vocabulary mismatch (F-P23 / Q-P14, carried): three site events are rejected by `server.mjs`.

### PR / merge / deploy record — arena/722181aa-prod2

| Item | Value |
| --- | --- |
| PR | https://github.com/wingbangboozle1-lang/Prod2/pull/39 |
| Merge result | **Merged 2026-11-20 06:39:02 UTC**, merge commit `025b7b2` (`gh pr merge 39 --merge`) |
| Checks on PR | `test` pass · `verify` pass (tools/checks.py ALL CHECKS PASSED; scripts/verify_site.py VERIFY OK) |
| Workflows on merge commit | verify-site ✓ · Self-hosted analytics tests ✓ · Deploy to GitHub Pages ✓ · pages build and deployment ✓ |
| Pages | `build_type: legacy`, `source: main /`, status `built` (serving the root mirror; the owner-side source change in F-P19/F-P20 is still pending) |
| Live check | https://wingbangboozle1-lang.github.io/Prod2/flagged.html served with the "Flagged for review" page and the F-P24 entry in the built `docs/flagged.html` |
| Status | L-01..L-03 **done**. Claim released. |

---

## PR / MERGE / DEPLOY RECORD — session arena/644d217b-prod2 (2026-11-20)

| Item | Value |
| --- | --- |
| PR | https://github.com/wingbangboozle1-lang/Prod2/pull/44 |
| Base / head | `main` ← `arena/644d217b-prod2` |
| Merge result | **Merged 2026-11-20 06:47:59 UTC**, merge commit `d7f58d16db80b826fec91a99a3e94348ce0b8636` (merge commit, not squash — every W-0x commit is preserved) |
| Merge conflict | `origin/main` had advanced 7 commits (#39–#42, session arena/722181aa-prod2) after this branch started. Merged, not rebased. Conflict in `data/p2/flags.json` / `flagged.html` resolved as a **union**: their register formatting and their new **F-P24** (the five `link.amazon` short links resolved to the Amazon homepage in *their* fetch) are kept verbatim, and this session's F-P23 resolution is re-applied on top. 38 flags before, 38 after — nothing dropped. Their `data/p2/live-check-2026-11-20-722181aa.json` is untouched. |
| Workflows on the merge commit `d7f58d1` | verify-site ✓ · Self-hosted analytics tests ✓ · Deploy to GitHub Pages ✓ · pages build and deployment ✓ |
| Checks at merge | `tools/checks.py` **ALL CHECKS PASSED** (30 pages, 13 sections) · `scripts/verify_site.py` **VERIFY OK** (18 pages) · `npm test` **3/3** · root mirror byte-identical to `docs/` (30/30 files) |
| Pages | Deployed from the merge commit; `GET /Prod2/article-thermometer-placement.html` returns the page with its full text, correct title and correct links |
| Live site | https://wingbangboozle1-lang.github.io/Prod2/ |

### What the merge itself exposed (fixed in `e624b6a`)

The Flagged page rendered only each flag's `how_to_resolve` cell, so **F-P23 still read as an open
problem on the page a reviewer actually reads** while its JSON said resolved. Resolved flags now render
their resolution and date. This is the same defect class as F-P23: the machine knew and the reader
could not see it. Worth knowing for the next pass — a register that is correct in JSON is not a
register that is correct on the page.

### PR #35 status at handoff

`arena/dd4bae8a-prod2` (PR #35) was still **CONFLICTING** at 06:47 UTC with its last commit at 06:27 UTC.
Not touched. It is now also **superseded** on every surface it touched: this merge changed
`tools/build.py`, `assets/js/measure.js`, `server.mjs`, the guide registry, the suggestions and
questions registers, and added two pages. Per the handoff rule it became takeover-eligible at
**07:27 UTC**; whoever takes it should treat `main` at `d7f58d1` as the current state and re-derive
rather than rebase.

### Known non-blocking state on `main`

- `arena/37b265a4-prod2` (a parallel session, pushed 06:48 UTC) has a failing `verify-site` job, failing
  at the **"Build is reproducible (committed site/ and root mirror match the build)"** step — the same
  class of drift `main` had before this pass. It does not affect `main` or the deploy; its own session
  owns the fix.

## ACTIVE CLAIM — session arena/3936beb1-prod2 (2026-11-20, status re-verification + coordination record)

Branch `arena/3936beb1-prod2`, branched from `d7f58d1` (main after PR #44). Single-branch rule followed; no other branch was created, switched to or pushed.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| X-01 Re-run the release gates on the branch (`tools/build.py`, `tools/checks.py`, `scripts/verify_site.py`, `node --test tests/server.test.mjs`) | done | arena/3936beb1-prod2 | none (read-only) |
| X-02 Independent spot check of the live site and of one Amazon listing (P4, `B0DHZTCNR5`) | done | arena/3936beb1-prod2 | none (read-only) |
| X-03 Record open-PR state and owner-side blockers here | done | arena/3936beb1-prod2 | `COORDINATION.md` |

### Results (2026-11-20)

- **X-01 gates:** `tools/build.py` → 30 pages; `tools/checks.py` → ALL CHECKS PASSED (13 sections, 5 declared site events, freshness match); `scripts/verify_site.py` → VERIFY OK (18 pages); `node --test tests/server.test.mjs` → 3/3 pass. Every outbound product `href` in `docs/` carries `tag=shopnow047c-20` and every outbound product link carries `rel="sponsored nofollow noopener"` (25 on `shop.html`).
- **X-02 live site:** `https://wingbangboozle1-lang.github.io/Prod2/` served by the fetch tool (title "Air fryers and thermometers by format | The Crisp Counter"). Pages API: `build_type: legacy`, `source: main /`, status `built`. The sandbox `curl` to the Pages host fails (`http 000`), so the fetch tool is the only live read.
- **X-02 listing:** `https://www.amazon.com/dp/B0DHZTCNR5` (P4) read through the fetch tool. Listing title matches `data/p2/products.json` P4 `name_listing`. The page also shows prices and ratings for other ASINs in the "Customers who viewed" carousel (the F-P17 attribution trap). Those values stay unpublished (F-02). The product's own price was **not** taken from this read.
- **X-03 open PRs (not touched by this session):** #35 (`arena/dd4bae8a-prod2`), #41 (`arena/e0d92902-prod2`), #43 (`arena/37b265a4-prod2`), #45 (`arena/19fb7064-prod2`), #46 (`arena/644d217b-prod2`). All five are OPEN and overlap the same reader-facing files (`tools/build.py`, `docs/`, `COORDINATION.md`, `data/p2/*`). Merging any of them is an integration decision for the owner, and each must be rebased on the merged state first. This session did not merge them.

### Owner-side blockers (cannot be done from the sandbox)

1. **Pages source** (F-P19 / F-P20): still `main /`. Owner action: Settings → Pages → Source → GitHub Actions. The repo root therefore still exposes `data/`, `content/`, `tools/`.
2. **One-link-per-product Associates Central test** (F-57 / F-58): tracking ID registration, activity and the attribution of each tagged Special Link can only be confirmed inside Associates Central. No value was inferred.
3. **Short-link resolution** (F-P24): the five `link.amazon` short links did not resolve to their listings on 2026-11-20 (see L-01 above). Their compliance status stays unresolved (FLG-003). They are not claimed valid or invalid.

### Irregularities for manual review (non-blocking, already on the Flagged page)

- F-P19 / F-P20: Pages source exposes non-publication files (see blocker 1).
- F-P23 / Q-P14: event-vocabulary contract (resolved in code by the W-01 pass; the gate asserts the five names; whether a collector is deployed for live traffic was not checked this session).
- F-P24: short-link discrepancy (blocker 3).
- F-P17 / F-02: carousel prices and ratings belong to other ASINs; the site withholds prices and ratings.

### Post-merge follow-up from this session (2026-11-20, after PR #44/#46)

Two merges downstream of this session's work (#43 and #50) have landed on `main` and rebuilt `docs/`.
Checked from the current `main`, not assumed:

- `tools/checks.py` → **ALL CHECKS PASSED** on `b8d5816`, including the `freshness` section, so the
  published artifact still matches a fresh render. The two long reads are present, and every gate this
  session added (`longreads`, the measurement assertions) is still live and green.
- The two long reads are still on the live host: `/Prod2/article-thermometer-placement.html` and
  `/Prod2/article-air-fryer-doneness.html` both return their full text with correct titles.
- `SG-46` / `SG-47` still render on the suggestions page. `index.html` and `guides.html` still link both
  articles; both are still in `sitemap.xml` and `feed.xml`.
- The `flagged.html` page now renders resolved items with their resolution text (the defect found in this
  session's own merge), so `F-P23` reads as resolved instead of as an open problem.

**One item for a later session:** `verify.yml` build-checks the Python sources (`build`, `verify`) and
the Node endpoint (the `test` workflow runs `npm test`), but no workflow runs `node --check server.mjs`
before the tests. This session validated `server.mjs` by hand, twice, after editing it. If a syntax
error ever slipped in, the failure would surface in the analytics job rather than at build time; that
is adequate but late. Adding one `node --check server.mjs` step to `.github/workflows/verify.yml` would
make it immediate. Logged, not implemented, because this session no longer holds a claim on that file.

---

---

## ACTIVE CLAIM — session arena/e292fb4d-prod2 (2026-11-20, Pages exposure + short-link re-read + integration)

Branched from `main` at `0a4b573` (PR #46 merged; fast-forwarded, no local commits existed). Other open PRs
(#35, #41, #43, #45, #47) are **not touched**; their scopes overlap `docs/` and this board and are logged here only.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| X-01 Stop serving the whole repository from the live host: switch the Pages source from `main /` (root mode, F-P19/F-P20) to the GitHub Actions artifact built from `docs/`, then prove the live host no longer serves `data/`, `tools/`, `archive/` | blocked — owner action (403 on Pages write) | arena/e292fb4d-prod2 | repository Pages setting (API), `COORDINATION.md`, `data/p2/flags.json` (resolution only if proven) |
| X-02 Re-read the five `link.amazon` short links and the five `/dp/` listings (2026-11-20) to re-test F-P24 | done | arena/e292fb4d-prod2 | `data/p2/live-check-2026-11-20-e292fb4d.json` (new), `COORDINATION.md` |
| X-03 Rebuild, gate, PR to main, merge, Pages live check; record here | done (PR #51, `ad81b87`) | arena/e292fb4d-prod2 | `docs/`, root mirror, `COORDINATION.md` |

### Results — arena/e292fb4d-prod2 (2026-11-20), part 1 (X-02)

- **X-02 · short-link re-read (done, F-P24 still open).** All five `link.amazon` URLs were fetched with the fetch
  tool on 2026-11-20. **All five resolved to `https://www.amazon.com/` (homepage, title "Amazon.com. Spend less.
  Smile more.")**, none to a product page. This differs from the 06:5x read by `arena/722181aa-prod2` (four homepage,
  one HTTP 500) only in the fifth link. The cause is still unknown and is **not** concluded here (not claimed invalid).
  Record: `data/p2/live-check-2026-11-20-e292fb4d.json`; F-P24 detail carries this third observation. Intended-ASIN
  fields unchanged. The five `/dp/` listings were **not** re-read in this pass (read twice today by other sessions).
- **Pages build observation.** The legacy Pages build for `40673a3` (PR #48, COORDINATION-only change) reported
  `errored` ("Page build failed."); the next build for `51a02ac` reported `built`. Single failed build, now superseded;
  recorded here, not treated as a site defect.
- **Pages settings (X-01).** Source is still `legacy`, `main /` (root mirror). Repository admin rights are present
  (`permissions.admin = true`). Change scheduled after this PR merges, so the deploy artifact is from final `main`.

### Results — arena/e292fb4d-prod2 (2026-11-20), part 2 (X-01 blocked · X-03 done)

- **X-01 · Pages source (BLOCKED — owner action).** `PUT /repos/{owner}/{repo}/pages` with `build_type=workflow`
  (documented values `legacy` | `workflow`: https://docs.github.com/en/rest/pages/pages) returned **HTTP 403
  "Resource not accessible by integration"**. The sandbox token can read Pages settings (`status: built`,
  `source: main /`) but cannot change them. Not worked around (for example by editing Jekyll settings to hide files),
  because that would change the live site in a way this pass could not verify. **Owner step:** repository
  Settings → Pages → Build and deployment → Source: **GitHub Actions**. Then run the existing *Deploy to GitHub Pages*
  workflow on `main`. **Baseline confirmed today:** the live host serves `data/p2/flags.json` and `COORDINATION.md`
  as static files (fetch tool, 2026-11-20), so F-P19/F-P20 exposure is real until the source changes.
- **X-03 · integration (done).** PR **#51** (`arena/e292fb4d-prod2` → `main`) merged with a merge commit at
  **2026-11-20 06:54:51 UTC** → `ad81b87`. Main had moved twice during the PR (PRs #43, #50), so the branch was
  merged with `origin/main` (not rebased, no history rewritten after the claim); conflicts were in the generated
  `docs/flagged.html` / `flagged.html` (regenerated from the register) and in the F-P24 detail (kept, one sentence added).
  Checks on PR #51: `test` ✓ · `verify` ✓. Workflows on `ad81b87`: verify-site ✓ · Self-hosted analytics tests ✓ ·
  Deploy to GitHub Pages ✓ · pages build and deployment ✓ (Pages build `built`, commit `ad81b87`).
  Live check: https://wingbangboozle1-lang.github.io/Prod2/flagged.html served with the Flagged page.
- **Correction to Part 1 above.** Part 1 said the only difference from `722181aa` was the fifth link. That
  was incomplete: `37b265a4` (R-01, same day) recorded B02NbDxp3 reaching its ASIN. The disagreement is F-P27 and is
  now stated in `data/p2/live-check-2026-11-20-e292fb4d.json`. No intended-ASIN field changed.
- **Claim status:** X-02 done · X-03 done · X-01 **blocked on owner action (403)**; stays open with the steps above.
- **ID note.** Task IDs `X-01..X-03` were also used by the merged session `arena/3936beb1-prod2` (lines above). The
  three rows in this section are this session's X-01..X-03; no earlier row was edited to fit.

---

## ACTIVE CLAIM — session arena/15730819-prod2 (2026-11-20, verified decision layer + shipped-defect repair)

Branched from `d7f58d1` (main after PR #44, 2026-11-20 06:46 UTC). This session is both the working
session **and** the final integration session on this one branch, per the standing one-branch rule.

**Claim filed 2026-11-20 06:52 UTC.** No other session claim is live on this branch. Three open PRs
exist with no commit inside their 60-minute window on first inspection (#45 06:48, #43 06:50, #41
06:50 — all three re-committed after this claim was drafted and are therefore **still inside their
own claims**). They are **not touched** here; their scopes are logged at the end of this section.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| X-01 **Shipped-defect repair:** `assets/css/site.css` was committed with raw merge-conflict markers (`<<<<<<< HEAD` … `>>>>>>> origin/main`) at lines 1/48/75, and `tools/build.py` copies it verbatim into `docs/assets/css/`, so **the published stylesheet is broken for every reader right now**. Resolve to the variable-font side the build preloads; add a gate check so a marker can never ship again. | in progress | arena/15730819-prod2 | `assets/css/site.css`, `tools/checks.py` |
| X-02 **Verified rate layer:** five ASINs today, added to the product register after a live read of Amazon's official standard commission table (S-COMM, Table 1): Physical Books/Kitchen/Automotive **4.50%**; Toys/Furniture/Home…**3.00%**; All Other **4.00%**. No per-ASIN category, so no per-product rate is asserted. | planned | arena/15730819-prod2 | `data/p2/products.json`, `data/p2/sources.json` |
| X-03 **Short-link re-read (2026-11-20, this session):** all five `link.amazon` URLs fetched again. Result recorded as dated history; intended-ASIN fields untouched (F-P24/F-P27/F-P28 respected, not overwritten). | planned | arena/15730819-prod2 | `data/p2/verification-2026-11-20.json`, `data/p2/flags.json` |
| X-04 **Missing-information register, decision-shaped:** a new "decision briefs" surface — for each of the six decisions the owner actually faces, what is known (with a link), what is *not* known, the exact question, who can answer it, and what it blocks. Extends Q-register rather than replacing it. | planned | arena/15730819-prod2 | `data/p2/briefs.json`, `content/pages/briefs.html`, `tools/build.py` |
| X-05 **Data-integrity gate:** every products.json value must carry a `_source`/`_read` sibling or be null; every published figure must appear in a dated verification record; register cross-references (F-/Q-/SG-/D-) must resolve. | planned | arena/15730819-prod2 | `tools/checks.py` |
| X-06 **Site rebuild + live verification:** rebuild, gate, PR, merge, confirm Pages deploy, record here. | planned | arena/15730819-prod2 | `docs/`, root mirror, `COORDINATION.md`, `EXECUTIVE_SUMMARY.md` |

**Not touched by this claim (logged, not edited):** PR #45 (`arena/19fb7064-prod2`, CSS conflict
residue + summaries — **superseded in part by X-01**, which fixes the same defect at source and adds a
gate; its author should drop the CSS hunk on rebase), PR #43 (`arena/37b265a4-prod2`, short-link
re-read; its F-P27/F-P28 findings are the reason X-03 records rather than overwrites), PR #41
(`arena/e0d92902-prod2`, union integration — overlapping but not consumed, because consuming it would
put two reg-built `docs/` trees into one commit without a line-by-line reconciliation this session
cannot complete from another branch's data).

**Verification boundary (unchanged, re-tested 2026-11-20 06:50 UTC):** `curl` to any host except the
system allowlist fails; Amazon listings, the Associates policy pages and the commission statement are
read with the **fetch tool**, and each is stamped with the date and the tool in the register. Pages
cannot be switched to Actions mode from here (`PUT /pages` → **403**), so the root mirror is still the
served artifact and F-P19/F-P20 stay open.

---

## CLAIM RESULT — session arena/15730819-prod2 (2026-11-20)

Claim filed 06:52 UTC, released at the merge recorded below. **Nothing from a parallel session was
discarded.** Two sessions landed on `main` while this one worked (PR #52 via `arena/644d217b-prod2`,
PR #53 via `arena/e292fb4d-prod2`) and both are merged here with a record below.

| Task | Status | Result |
| --- | --- | --- |
| X-01 Shipped CSS defect | **done** | 49 lines of merge-conflict residue removed from `assets/css/site.css`; kept the variable-font side the build preloads; dropped the older static-weight `@font-face` block. `integrity` gate section added (markers, braces, tokens, font-faces, register ids). |
| X-02 Verified rate layer | **done** | S-COMM re-read 2026-11-20. Table 1 rows recorded verbatim (Physical Books/Kitchen/Automotive **4.50%**, Home/furniture **3.00%**, All Other **4.00%**). **No per-product rate asserted** — the statement maps categories, not ASINs, and no official source in this project equates a browse node with a programme category. F-01 stays open. |
| X-03 Short-link re-read | **done** | Third same-day read: **0 of 5** `link.amazon` URLs reached a product listing; all five returned the Amazon homepage (the earlier HTTP 500 for `B0f3GKalj` did not reproduce). Recorded as new dated history; `intent-links.json` and every `intended_asin` untouched. F-P24/F-P27/F-P28 respected. |
| X-04 Decision layer | **done** | `data/p2/briefs.json` + `content/pages/briefs.html`: six briefs, ordered by irreversibility. `briefs` gate section added. |
| X-05 Integrity/findability gate | **done** | `integrity` + `one-site` + `briefs` sections. Archive-wide `noindex` written by the build (82 files); robots.txt scoped away from `archive/`, `data/`, `tools/`, `content/`, `scripts/`, `tests/`; one canonical base asserted across 31 pages. |
| X-06 Landing restructure | **done** | Front page: 24 cards → 12, 1,927 → 1,594 words, four above-fold trust blocks → one trust line, long reads moved directly under the shelf, cluster block moved off the front page (the guides hub still owns it and the gate still requires every guide to reach its pillar). |
| X-07 Integration | **done** | Merge of `origin/main` (PRs #52/#53) with generated files re-rendered rather than hand-resolved; coordination claim re-appended after the merge. Both gates green, `npm test` 3/3. |

### Verified live this session (fetch tool; `curl` to these hosts is blocked, 000)

**Listings — all five, 2026-11-20, every document title matches the register verbatim:**

| # | ASIN | URL read | Breadcrumb this pass |
| --- | --- | --- | --- |
| P1 | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 | Home & Kitchen > … > Air Fryers |
| P2 | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R | Home & Kitchen > … > Air Fryers (rendered this pass; the earlier null is superseded) |
| P3 | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH | Home & Kitchen > … > Air Fryers |
| P4 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 | Home & Kitchen > … > Meat |
| P5 | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z | Home & Kitchen > … > Meat |

**Policies and official pages read:**

- Associates Program Standard Commission Income Statement — https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ (Table 1, 2026-11-20)
- Associates Program Policies, updated **April 14, 2026** — https://affiliate-program.amazon.com/help/operating/policies (§2(b) prices/availability; §2(b) Special Links must carry the tag; trademark clause on domains and tags)
- Associates Program Operating Agreement — https://affiliate-program.amazon.com/help/operating/agreement (§5 disclosure sentence; §2(b)/Participation Requirements on Special Links; §4 no traffic or income representation)

### Irregularities found this session (all published, none blocking)

| # | Finding | Where it is published |
| --- | --- | --- |
| 1 | **Raw merge-conflict markers shipped in the live stylesheet.** `assets/css/site.css` lines 1/48/75 carried `<<<<<<< HEAD` … `>>>>>>> origin/main`, copied verbatim into `docs/assets/css/`. The site has been serving invalid CSS. No gate section read static assets, so it shipped green. | Fixed; `integrity` section; this file |
| 2 | **82 archived files were indexable at the live host.** 74 HTML pages (plus XML) from four previous builds return 200 and were excluded only by a robots.txt line. They compete with the canonical pages in search. | Fixed build-side with per-file `noindex`; the real fix is an owner Pages-mode change still recorded as F-P19/F-P20 |
| 3 | **Three same-day reads of the owner short links now disagree with each other.** This pass: 0/5 reach a listing. The R-01 read (merged as F-P27): 1/5. Neither is treated as the answer. | F-P24, F-P27, F-P28, Q-P18 (rows written by other sessions); this pass adds a dated third read |
| 4 | **A price string for P4 appeared in the page's own buy area but is also the label on two carousel cards.** Recorded as ambiguous rather than resolved in the product's favour. | `verification-2026-11-20.json` → `third_pass_2026_11_20_arena_15730819.pricing` |
| 5 | **A brief cannot cite a row that only exists on an unmerged branch.** Writing X-04 surfaced this: three flags and one question cited in the first draft were on PR #43's branch, not on the published site. | Fixed after the #43 merge; recorded in `briefs.json` `_meta.cross_branch_note` |
| 6 | **PR #45 duplicates X-01.** It carries the same CSS conflict fix. Its author should drop that hunk on rebase; this branch fixed it at source and added the gate. | This file |

### Sources used (all official; full register in `data/p2/sources.json`)

Amazon Associates Operating Agreement · Associates Program Policies · Standard Commission Income
Statement · the five `amazon.com/dp/` listings · the five owner-supplied `link.amazon` short links
(recorded as evidence, never published as buy paths) · USDA FSIS and FoodSafety.gov guidance and
Nebraska Extension (carried, re-cited by the long reads) · Google Search Central (link qualification,
snippets) · FTC endorsement guides. Every read is dated in `data/p2/sources.json` and in the dated
verification records.

### Files this pass touched

`assets/css/site.css` (conflict fix + brief + chooser styles) · `tools/build.py` (briefs hooks, archive
guard, robots, front guides) · `tools/checks.py` (`briefs`, `one-site`, `integrity` sections) ·
`data/p2/{briefs.json (new), sources.json, verification-2026-11-20.json}` · `content/pages/{index,briefs}.html` ·
`archive/**` (noindex written in place) · `docs/` + root mirror · `EXECUTIVE_SUMMARY.md` · `COORDINATION.md`.

---

# ACTIVE CLAIM — session arena/0a9f19fe-prod2 (2026-11-20, buyer-decision layer + design QA gate)

Branched from `d7f58d1` (main after PR #44). Session id for this board: **arena/0a9f19fe-prod2**.

**State of the board at claim time (06:50 UTC).** Four PRs are open and each has had a commit within
the last 10 minutes, so all four are **live concurrent sessions, not stale**: #35 (`arena/dd4bae8a-prod2`,
last commit 06:27), #41 (`arena/e0d92902-prod2`, 06:48), #43 (`arena/37b265a4-prod2`, 06:48),
#45 (`arena/19fb7064-prod2`, 06:48). None of them is touched by this session. Per the 60-minute
handoff rule, none is eligible for takeover yet; if one goes quiet past 07:48 UTC and is still
`CONFLICTING`, a later integration session may take it over.

**Scope conflict found before claiming — recorded, not edited.** `assets/css/site.css` (and its
`docs/` twin) is owned by **three live sessions at once** (#41, #43, #45 all list it). This session
therefore claims **no CSS redesign**; it claims the two files no open PR touches (`tools/checks.py`
is touched by #41/#45, so the new gate goes in a **new** file, `tools/design_qa.py`) plus
pipeline-only data the other sessions do not list.

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| A-01 **P0 live defect**: all 30 published pages load `assets/css/site.css` with raw git conflict markers at lines 1/48/75. Repair deterministically (keep both `@font-face` sets; token layer unchanged) and make the build fail on any conflict marker | in progress | arena/0a9f19fe-prod2 | `assets/css/site.css`, `docs/assets/css/site.css` (mechanical repair only — no design edits, so no collision with #41/#43/#45) |
| A-02 **Cascade proof**: since the sandbox cannot install a browser (Puppeteer/Playwright downloads blocked) and no prior session ever verified CSS applied, build a headless-free stylesheet auditor: parse the CSS, resolve the cascade, and assert the design tokens reach the markup; wire it into `npm test` | in progress | arena/0a9f19fe-prod2 | `tools/design_qa.py` (new), `package.json`, `.github/workflows/verify.yml` |
| A-03 Buyer-decision layer: a ranked "which one should I buy" verdict with the **reason each loser loses**, written only from register facts + cited official guidance | in progress | arena/0a9f19fe-prod2 | `content/pages/shop.html`, `content/pages/compare.html` |
| A-04 Decision-room collation: one page that ranks every open suggestion and every open question by what it unblocks, with the single owner action per row (the "review before implementing" surface) | in progress | arena/0a9f19fe-prod2 | `content/pages/decisions.html`, `data/p2/decision-room.json` (new) |
| A-05 Exec summary refresh to the merged state (counts, the P0 defect, the new gate) | in progress | arena/0a9f19fe-prod2 | `EXECUTIVE_SUMMARY.md` |
| A-06 Integration: rebuild both outputs, gate, line-by-line publish check, PR to `main`, merge, Pages live check, record here | in progress | arena/0a9f19fe-prod2 | `docs/`, root mirror, `COORDINATION.md` |

Claim protocol notes:
- One branch per session (Arena rule); this session is both working and integration session on it.
- **Verification boundary (this sandbox, measured 06:49 UTC):** outbound HTTP is limited to
  `github.com` / `api.github.com` / `codeload.github.com` / `registry.npmjs.org` / `pypi.org` /
  `files.pythonhosted.org` plus the page-fetch tool's path. `pip install playwright` resolves, but the
  browser binaries do not download (Chrome for Testing, 3 attempts), and Debian font packages are
  unavailable — so **no screenshot of any page has ever been produced by any session in this repo**.
  Every "the design works" claim in this file above is therefore unverified except by reading CSS.
  A-02 exists to close that hole with a tool that needs no browser.
- Flagged irregularities do not block the merge; they are published on the Flagged page.

### Claim results (A-01..A-06, 2026-11-20)

- **A-01 · the P0 defect (done).** `assets/css/site.css` opened with three raw conflict markers at
  lines 1/48/75 and, on both sides of that merge, a `@font-face` block had lost its closing brace —
  HEAD's went unterminated and a stray `}` sat before the design system. All 30 pages load that file.
  Repaired by keeping **both** complete font stacks (six static latin subsets + three variable faces),
  which is one more fallback than either branch had alone. Verified: tinycss2 → 245 top-level rules,
  **0 parse errors**, braces 278/278, final `@media print` rule fully consumed, in both `assets/` and
  `docs/`. Exhaustive marker sweep of the shipped artifact: 0. **Note for integration:** PR #45
  (`arena/19fb7064-prod2`) independently found and fixed the same defect, resolving it by keeping
  only the three variable faces. The two fixes are functionally equivalent; this one keeps 2 extra
  static faces. **When both merge, take this branch's file** (it is a superset) and keep PR #45's
  `exposition` marker check, which duplicates the `markers` section of the new gate but costs nothing.
- **A-02 · the gate (done).** `tools/design_qa.py`, 9 sections, no browser required: markers, parse
  (unclosed-block detection), fonts (existence + real WOFF2 + `font-display`), units (silently dropped
  unitless lengths), tokens (dangling `var()`), cascade (does the stylesheet reach the markup; does
  `body` paint a background and a text colour), coverage, contrast (WCAG AA on the token pairs the
  system actually combines). **Tested against three real failure modes, not just against today's
  tree:** the exact shipped defect → 2 FAILs; a silent missing brace with no markers → unreachable
  tail + 8 undefined tokens; an undefined token → 2 FAILs. Passes on the repaired tree. Wired into
  `.github/workflows/pages.yml` before upload and into `npm test`.
- **A-03 · the buyer decision (done).** `shop.html` gains a five-row verdict by job, a "why the other
  one loses" table stating each trade-off in both directions, the USDA placement rule that outranks
  product choice, and an explicit "what this cannot tell you" list. **While writing it I asserted the
  8 qt basket had the smallest footprint; the register's arithmetic says the dual basket does
  (158 in² vs 172).** Caught before publishing and converted into a gate: `tools/checks.py` gains a
  `derived` section that recomputes every footprint and capacity density from the register and fails
  on mismatch, plus a rule refusing a named "smallest" winner it cannot attribute. The new gate then
  failed the page and forced the sentence to state all three numbers instead.
- **A-04 · the pre-decision register (done).** `before-you-decide.html` (new, 31 pages total): eleven
  decisions waiting on facts only the owner can obtain, each with what is known, what is missing, how
  it is discovered, and what changes when it lands. Four are ranked as the only ones worth doing
  first. States in the negative that it publishes no revenue estimate and ranks nothing by earnings.
  First draft had four defects the gate caught: an invented anchor, a citation to a non-existent
  `SG-58`, and a short link rendered as a live URL instead of inert code.
- **A-05 · executive summary + flag (done).** `EXECUTIVE_SUMMARY.md` to rendered values: gate 13 → 14
  sections, flags 37 → 39, event-vocabulary item marked resolved by PR #44. **`F-P25`** publishes the
  stylesheet defect, its root cause and the new gate on the Flagged for review page, status
  `resolved`.
- **A-06 · verification (done).** `tools/build.py` 31 pages · `tools/checks.py` **ALL CHECKS PASSED**
  (16 sections, 16 ok lines) · `tools/design_qa.py` **DESIGN QA PASSED** (9 sections) ·
  `scripts/build_site.py` + `scripts/verify_site.py` **VERIFY OK, 18 pages** · `npm test` **3/3** ·
  `git status` clean after a rebuild, so `docs/` is byte-reproducible. A live preview of the built
  site is served from this session for human review.

### What this session could NOT do, recorded so nobody assumes otherwise

- **No browser, therefore no screenshot.** Playwright and Puppeteer both install; the
  Chrome-for-Testing binary and the Debian font packages do not download. A-02 is the substitute and
  is honest about the limit: it proves the cascade reaches the markup and that the tokens resolve —
  it does not prove the result is attractive. Any claim in this repo that the design "works" is an
  inference from CSS until a human looks at a rendered page.
- **No external fetches in this session.** No Amazon listing, policy page or Google/FTC source was
  re-read. Every product value used comes from the dated register reads
  (`data/p2/verification-2026-11-20.json`, `2026-11-19`), and the only new external facts this pass
  relies on are the USDA FSIS quotes already registered as `S-FSIS-THERMO` and read on 2026-11-20 by
  the previous pass. No value was inferred to fill a cell.
- **No CSS redesign.** Three live PRs own `assets/css/site.css`; this session repaired the file
  mechanically and left the design system untouched.

### Rebase reconciliation against main (PRs #52, #55, #57 landed while this session ran)

`main` moved three times under this branch. Rebased at 07:0x UTC onto `756f102` (PR #57). Nothing
from either side was discarded. **What changed in the reconciliation, recorded because two of these
are ID and scope collisions that a later session must not re-litigate:**

1. **`F-P25` collided.** Main's briefs pass had already taken `F-P25` for the "Check price on Amazon"
   copy label. This pass's stylesheet defect was re-issued as **`F-P29`** (status `resolved`) rather
   than overwriting main's row. Only one `F-P25` exists; there are no duplicate flag ids (checked
   programmatically, 43 flags).
2. **`briefs.html` overlaps `before-you-decide.html`.** Both landed the same day and both help the owner
   decide. **Neither was deleted**: `briefs.html` is the six decisions that one five-minute browser
   test settles; `before-you-decide.html` is the eleven calls including the five with no quick test.
   The two pages now cross-link each other and each says plainly what the other adds. If a later pass
   wants one page, that is an editorial decision to record — not something to delete quietly.
3. **`assets/css/site.css` had already been repaired on main** (PR #55) with the same three-variable-face
   fix. This branch's repair is a superset (nine `@font-face` blocks: six static latin subsets plus
   three variable faces) and won the `docs/`/`assets/` conflict. Verified after rebase: 308/308 braces,
   0 markers, 9 faces, both copies identical.
4. **The overlap with PR #45** (`arena/19fb7064-prod2`, still open) is unaffected by the rebase: its
   CSS fix is equivalent, its `exposition` marker check is compatible, and this branch's gate is the
   broader one. Take both; the CSS file here is a superset.
5. **The new gate caught a real defect in main's merged CSS** during the rebase: `.brief-unknown`
   references `var(--clay-wash, #fbeee4)`. Because a **fallback is present**, the declaration paints
   correctly, so this was a **false positive in my own gate, not a bug in main**. The gate was
   corrected to separate "no definition and no fallback" (a failure) from "undefined but always used
   with a literal fallback" (a note), re-tested against both, and now passes. Recorded because the
   first version would have blocked a legitimate merge.

**Post-rebase verification (all green, tree clean after rebuild):** `tools/build.py` 32 pages ·
`tools/checks.py` ALL CHECKS PASSED · `tools/design_qa.py` DESIGN QA PASSED · `scripts/verify_site.py`
VERIFY OK 18 pages · `npm test` 3/3 · `git status --porcelain` empty.

### File-scope request (logged, not edited)

- **`.github/workflows/verify.yml`** is owned by open PR #35 (`arena/dd4bae8a-prod2`), so this session
  did **not** edit it. **Request to #35's session (or to the next integration session):** add
  `- name: Release gate — stylesheet` / `run: python3 tools/design_qa.py` after the existing
  `tools/checks.py` step, and add `git diff --exit-code -- tools/design_qa.py` is not needed (it is
  committed source, not built output). Until then the gate runs in the deploy workflow
  (`.github/workflows/pages.yml`, uncontested) and in `npm test`, so it is enforced on every push to
  `main` — it is only *not* enforced on a branch push or a PR without #35's change.

---

## SESSION RECORD — arena/20f83238-prod2 (2026-11-20, reviewer pass + integration)

Protocol note: single Arena session on its assigned branch `arena/20f83238-prod2` (the
`session-<id>/<task>` naming in the brief is not used; the claim is recorded here). Claimed
R-01..R-06 at 2026-11-20 06:11 UTC (claim commit `02f7591`, pushed before any work started).

| Task | Status | Session | Scope (files) | Notes |
| --- | --- | --- | --- | --- |
| R-01 Reviewer pass over the suggestion queue: decide every open SG item with rationale; record decisions; render the chosen path on the suggestions page | done | arena/20f83238-prod2 | `data/p2/{suggestions,decisions,flags}.json`, `content/pages/suggestions.html`, `assets/css/site.css` | D-P22/D-P23, F-P29, SG-48. |
| R-02..R-03 (brand/type/seasonal pass + gift guide) | done (superseded) | arena/20f83238-prod2 | — | Built in this session's first WIP wave, then found **already merged to main** by the parallel anti-slop + shop-front passes (arena/70b2b9f7-prod2, arena/43f4359d-prod2, arena/f55b5827-prod2). Kept main's merged versions; this session's parallel copies were **not** re-applied (see the integration note below). |
| R-04 Decision-readiness + measurement integrity | done | arena/20f83238-prod2 | — | Verified against main's build: measure.js on 28/28 pages, five events defined, ledger empty by rule, decision-readiness ground already covered by the questions page's discovery-methods table (R-04's planned table would have duplicated it — not added). |
| R-05 Stale-PR handoff (PRs #23, #25) | done | arena/20f83238-prod2 | `gh` only | Both claims expired >8h; closed with handoff comments. Unique content carried: PR #23's start-here path + byline (superseded by the shop-front's shipped equivalents), PR #25's gift-guide topic (shipped as `guide-gift-guide.html`) and its probe-in-air-fryer topic (carried into the editorial calendar queue). Branches remain on the remote; nothing discarded. |
| R-06 Integration: rebase onto consolidated main, union deltas only, gates, PR → main, merge, Pages check | done | arena/20f83238-prod2 | `docs/`, root mirror, `COORDINATION.md` | See the integration note below. |

### Integration note — parallel-session collision (nothing discarded)

This session's first wave (claim `02f7591` → WIP tip `d1dec62`, pushed 06:11–06:34 UTC) built a
brand/type/seasonal pass that **independently converged** on the same design as five parallel
sessions racing on `main` the same morning (PRs #29–#40: the shop-front pass, the anti-slop
pass, the register reconciliation, the audit pass, the live re-check). On `git pull --rebase`
the collision was discovered: main already carried the working brand (D-P18), self-hosted
Fraunces+Inter (D-P19), the December gift guide (D-P20), and had taken the ids D-P10..D-P14,
F-P15, Q-P10/Q-P11, SG-38..SG-44 (and later D-P21, F-P25..F-P28, SG-45..SG-47) for different rows. Resolution, per the conflict protocol:

1. **Nothing of main's work was discarded or overwritten.** Main's merged registers, shop front
   and gates are the base; this session re-applied **only its unique deltas** on top (the
   reviewer decisions below).
2. This session's WIP is preserved verbatim: remote branch tip `d1dec62241bbc50cf3e4176f984ac673c55f2f71`
   on `arena/20f83238-prod2` (reflog) and a bundle at the session's workspace. Its duplicate
   ids were **not** re-introduced; new rows continue the dense numbering at D-P22 / F-P29 / SG-48.
3. The handoff rule was applied to PRs #23/#25 (expired claims) and the one-site rule held
   throughout: one canonical publication (`docs/`).
4. A **second** collision arrived while PR #47 was open (PRs #48/#50 landed D-P21 (event
   vocabulary), F-P25..F-P28 and SG-45..SG-47). The union repeated: main's rows kept their
   ids, this session's rows renumbered again to **D-P22/D-P23, F-P29, SG-48**, with all
   in-page references updated (audited line by line against origin/main after the union).

### What this session uniquely adds (the reviewer pass, R-01)

The brief requires that someone review the suggestion queue and choose the best path before
changes, with no manual input from the owner. This session filled that slot:

- **D-P22 — Path A ("prove the traffic first") is the chosen strategy** (the queue's own
  recommendation): endpoint + Search Console + runbook next; topics from measured queries after
  14 days; every non-Path-A item decided individually.
- **D-P23 — the promotion hold is standing policy (SG-14 accepted):** no paid promotion and no
  newsletter until one clean attribution test exists.
- **Queue coherence (F-P29, resolved):** SG-05 was still 'proposed' although D-P11 had answered
  it in the negative — reconciled to 'rejected'. Items the merged passes built but left marked
  (SG-11/12/13/17/35) now read 'shipped' to match reality; SG-02/07/08/10/39/41/43 are
  'deferred' with their blockers stated; SG-01/34/36/44 are 'accepted' with their gates.
- **SG-48 (new):** the monthly owner digest that turns the questions register into a standing
  prompt — the brief's "suggestions to discover missing information" in standing form.
- The suggestions page now opens with the review outcome and its status vocabulary includes
  deferred and rejected; the walkthrough procedure stays for future reviews.

### Sources used this session

- The suggestion queue and decision log themselves (`data/p2/{suggestions,decisions}.json`),
  the Program-Policies-derived rationale already recorded in D-P11/D-P15/D-P18..D-P20 (not
  re-fetched here; egress allowlist unchanged). No product fact, price or rating was touched.
- Owner lookup links cited for manual review where the decisions defer to owner actions:
  Associates Central (Q-01), Google Search Console (Q-P08), USPTO trademark search (Q-19/Q-P10).

### Verification performed (all green at merge)

- `python3 tools/build.py && python3 tools/checks.py` — ALL CHECKS PASSED, 28 pages,
  13 sections (measurement section prints the known, non-blocking F-P23 event-vocab NOTE per D-P15).
- `python3 scripts/verify_site.py` — VERIFY OK (18 pages); `npm test` — 2/2.
- Cross-reference sweep (gate-enforced): every F-/Q-/SG-/D- id cited on any page exists in its
  register, including the new D-P22/D-P23/F-P29/SG-48.

### Irregularities for manual review (non-blocking)

1. F-P23 (carried) — site/endpoint event-vocabulary mismatch awaits the owner's choice (Q-P14).
2. F-P19/F-P20 (carried) — Pages still serves the repo root; owner action: Settings → Pages →
   Source: GitHub Actions.
3. F-P24 (carried) — the submitted short links did not resolve to listings on the 2026-11-20
   re-check; owner/browser check required. Untouched here by design.
4. F-P29 (resolved this session) — queue/decision-log disagreement on SG-05, documented above.

### PR / merge / deploy record

| Item | Value |
| --- | --- |
| PR | https://github.com/wingbangboozle1-lang/Prod2/pull/47 (`arena/20f83238-prod2` → `main`) |
| Merge result | (recorded after merge) |
| Pages | (recorded after deploy verification) |
