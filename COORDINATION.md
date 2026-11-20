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

---

## ACTIVE CLAIM — session arena/7cec0d73-prod2 (2026-11-20, final integration: CSS repair + live re-verification + site polish)

**Status: active.** Branch `arena/7cec0d73-prod2` (platform-assigned; the `session-<id>/<task>` naming
in the brief is therefore not used, and no other branch is created or pushed). Base: `0a4b573`
(main after PR #46).

### Why this session exists — one defect found that no open PR covers

**The published stylesheet contains unresolved merge-conflict markers.** `assets/css/site.css` on
`main` opens with literal `<<<<<<< HEAD` / `=======` / `>>>>>>> origin/main` lines (lines 1, 48 and
75), and the file is **one brace short** (278 `{`, 277 `}`). This is not theoretical: the live host
serves the markers. Verified by reading
`https://wingbangboozle1-lang.github.io/Prod2/assets/css/site.css` on 2026-11-20 — the first
lines of the served stylesheet are `<<<<<<< HEAD` and `=======`. Every reader loads a stylesheet
whose first rule is a syntax error, and the `@font-face` block that follows it is malformed. The
two candidate resolutions both exist as complete, valid CSS (PR #45 carries the variable-font
resolution; `origin/main` carries the static-subset resolution).

PR #45 (`arena/19fb7064-prod2`) is the only open PR that fixes this file, but it is CONFLICTING
against `main` and its base predates PRs #42–#46. This session takes over the repair rather than
rebasing a stale branch.

### Scope (this session only)

| Task | Status | Session | Scope (files) |
| --- | --- | --- | --- |
| X-01 Repair the conflicted stylesheet and pick one font resolution | in progress | arena/7cec0d73-prod2 | `assets/css/site.css`, `assets/fonts/` |
| X-02 Gate: fail the build on conflict markers in any published artifact | unclaimed | arena/7cec0d73-prod2 | `tools/checks.py` |
| X-03 Live re-read of the five `/dp/` listings (2026-11-20, this session) | unclaimed | arena/7cec0d73-prod2 | `data/p2/verification-2026-11-20-7cec0d73.json` (new) |
| X-04 Carry forward the un-merged register rows from the open PRs, renumbered | unclaimed | arena/7cec0d73-prod2 | `data/p2/{flags,questions,decisions,suggestions}.json` |
| X-05 Reader-facing polish + site surface check | unclaimed | arena/7cec0d73-prod2 | `content/pages/*`, `assets/css/site.css` |
| X-06 Integration: rebuild, re-verify, PR to main, merge, Pages live check | unclaimed | arena/7cec0d73-prod2 | `docs/`, root mirror, `COORDINATION.md` |

### Non-overlap statement

No other session has a live claim on `assets/css/site.css` in `COORDINATION.md`. PR #45's branch
owns the same file, so this session **does not rebase or edit that branch**; the repair is
re-derived here against current `main` and PR #45 is left for its owner to close or supersede.
Register rows from PRs #43, #45, #47 and #41 are **carried forward by content, renumbered**, never
copied with colliding ids (see X-04).

### Verification boundary for this session (recorded honestly)

`curl` to `www.amazon.com` and `link.amazon` fails from this sandbox (`http 000`,
`SSL_ERROR_SYSCALL`), so the **fetch tool** is used for every external read, and each row records
which tool produced it. Amazon listing pages return a "Product summary" variant to the fetch tool:
the listing **title** and **breadcrumb** are readable and are the values the register publishes.
Prices and ratings on these fetches appear inside "customers also viewed" carousels and
protection-plan blocks, which belong to **other ASINs** — except where the target product's own
price is rendered in the buy box, which is recorded but still not published (F-02, D-P10).

## X-01–X-06 final integration record — arena/7cec0d73-prod2 (2026-11-20)

All six claimed tasks are done in this session's commits; the PR to `main` and the
Pages check follow this record (the PR link is appended below once created).

### Sources and verification performed

| Read | Tool | Result | Recorded in |
| --- | --- | --- | --- |
| Five `/dp/` listings, 2026-11-20 | fetch tool (curl is blocked from this sandbox) | all five titles + breadcrumbs match `data/p2/products.json` exactly | `data/p2/verification-2026-11-20.json`, commit history |
| Five `link.amazon` short links, 2026-11-20 | fetch tool | P1 and P5 reached their intended listings; P2 and P3 resolved to the Amazon homepage; P4 returned HTTP 500 twice | `data/p2/intent-links.json` observed history (dated, per link), F-P24/F-P27/F-P28 |
| Associates Program Policies | fetch tool | qualifying-purchase attribution starts with a Special Link click; policies updated 2026-04-14 | D-P11, compliance page |
| GitHub API: PR #16 state | `gh pr view` | CLOSED, not merged | Q-P30 answered in the register |
| PR branches #41/#43/#47 | `git fetch` + content diffs | register rows ported by content with renumbering; no products.json change in any of them | X-04 below |

### X-04 — register reconciliation (content-keyed, not id-keyed)

`tools/reconcile_registers.py` (kept in the repo, one-shot, refuses to write on
unmapped collisions) carried the open branches' rows onto main:

- flags: +F-P25…F-P28 (PR #43), +F-P29 (PR #47's F-P25, renumbered — main's
  F-P25 was a different row). F-P19/F-P20 detail extended from PR #43. F-P23's
  older "open" state from PR #47 skipped: main resolved it (collector fix, PR #44).
- questions: +Q-P18 (PR #43), +Q-P12, Q-P13 and Q-P30…Q-P39 (PR #41, renumbered —
  main had used those ids for different rows).
- suggestions: +SG-18…SG-26 (PR #41), +SG-48 (PR #47's SG-45, renumbered — main's
  SG-45 is a different row). PR #47's reviewer status pass applied to the 18
  matching rows, with one refused regression: SG-41 stays `shipped` (main's gate
  exists; PR #47's base predates it).
- decisions: +D-P22, D-P23 (PR #47, renumbered), +D-P24 (PR #41's handoff record).
- Cross-references inside every carried row and in PR #41's data files were
  rewritten to the new ids; each renumbered row records its former id in its own
  renumber note (the gate treats those provenance notes as history, not citations).

### X-01/X-02/X-05 — stylesheet repair, new gate, reader-facing port

- `assets/css/site.css`: conflict markers removed; the variable-font `@font-face`
  resolution chosen (weights 550/650/750/800 require it); braces balance 272/272.
- `tools/checks.py` now fails on any merge marker in a published artifact and on
  unbalanced CSS braces (both paths injection-tested). The gate also grew PR #41's
  editorial voice lint and read-date checks during the port.
- PR #41's reader-facing additions are live: two question-shaped guides
  (`guide-dual-vs-single`, `guide-probe-in-air-fryer`), the plain-language
  `analysis` page and the `design-prompt` page, with their data files
  (`design-prompts.json`, `decision-priority.json`, `verification-log.json`).
  PR #41's stale claim that all five short links resolve was rewritten to the
  dated, disagreement-aware finding the register actually records.
- PR #43's executive-summary correction is carried: all five displayed prices
  become `withheld (F-02)`; the "all five links resolved" claim becomes the dated
  wording; register counts updated to the post-reconciliation state.
- The intent record now carries the 2026-11-20 reads per link (dated history,
  latest-observation field updated, intent fields untouched). P4 has no recorded
  target — HTTP 500 twice — and the build renders that as "no target observed"
  instead of inferring one.

### Build state at this record

34 pages built; all 14 release checks pass (validity, facts, claims, chrome, seo,
publication, longreads, shop, conflicts, exposition, measurement, freshness,
editorial, plus the endpoint test suite: 3/3). The sitemap and feed include the
new pages. `git pull --rebase` run before every push; no conflicts encountered.

### PR and deployment result

(appended after the pull request is created and merged)
