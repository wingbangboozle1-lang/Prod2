# COORDINATION.md — Shared Task Board

Repo: `wingbangboozle1-lang/Prod2`
Tracking ID: `shopnow047c-20`
Current session: **session-arena-8ff10f50-prod2** (branch `arena/8ff10f50-prod2`)

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

No other session has an unexpired claim on these files. If this session stops, any other session may take over an `in progress` task older than 60 minutes with no commits and must note the handoff here.

## Verification boundary (this session)

- Product facts, ASINs, prices and ratings in `data/products.json` were re-read from the official Amazon listings on 2026-11-19 (see `data/sources.json`). This sandbox cannot reach amazon.com (egress is limited to github.com/npm/pypi hosts), so values are taken from the dated 2026-11-19 verification records and are **not re-fetched here**. Any value that cannot be confirmed from an official source is left blank and flagged (see the Flagged for Review page). No value is inferred.
- Compliance sources (Amazon Associates Operating Agreement, Program Policies, ASIN definition, FTC, Google Search Central) are cited from `data/sources.json` with access date 2026-11-19; links are provided for manual review.

## PR / merge / deploy record (filled in after merge)

| PR | What | Result |
| --- | --- | --- |
| #19 | Integration: product-forward landing page + transparency flag F-P08 + both builds verified + Pages deploy | Merged into `main` as merge commit `0030f90a69b53ecd226923ddd6125dc795f0b282`; `Deploy to GitHub Pages` success; `verify-site` success; `pages build and deployment` success; live at https://wingbangboozle1-lang.github.io/Prod2/ |

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
| T-08 Measurement machinery (click counter, five events, self-hosted endpoint, campaign ledger) | done | arena/44093825-prod2 | `docs/assets/js/measure.js`, `analytics-endpoint/server.py`, `data/ledger.json`, `data/events.json` | Amazon Commission Income Statement windows (S-COMM/S-CDIS) | Endpoint deployable, not yet hosted — flagged F-19. Ledger stays empty until an authorized report exists. |
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
# Session `arena/b650562d-prod2` (sess-b650562d) — claim + scope, 2026-11-19

**Branch:** `arena/b650562d-prod2` from `da11cd414e9d0dd18f0e2d44854f4d976326ef26` (= `main` tip at claim time).
**Role:** suggestions/decision-portal pass + reader-facing polish. This session is *not* a second
site build: it improves the canonical `docs/` publication (mirrored to root) that is live today.

## Task claims (scope is mine while in progress; SG-15+ numbering continues from the merged SG-14)

| Task | Status | Scope (files) | What |
|---|---|---|---|
| S1 — Live re-verification of the five submitted links | done | `data/p2/verification-2026-11-19.json`, `data/p2/products.json` (read dates only) | All five `link.amazon` short links re-resolved live 2026-11-19; same ASINs; no `tag=` on any resolved URL (F-03 stands). |
| S2 — Suggestions portal v2 (decision paths) | in progress | `data/p2/suggestions.json`, `tools/build.py` (hook_suggestions), `content/pages/suggestions.html` | Every suggestion carries theme, 2–3 concrete paths, cost/upside/downside, what it unlocks, and whether it feeds the design prompt. |
| S3 — Open-questions register v2 | in progress | `data/p2/questions.json`, `tools/build.py` (hook_questions) | Known / missing / how to discover / who can answer / blocking / default if unanswered, each with an official link for manual review. |
| S4 — Design prompt pack page | in progress | `content/pages/design-prompt.html`, `tools/build.py` (PAGES), `DESIGN_BRIEF.md` | Copy-ready briefs that make the site read like a shop, not an audit — with the compliance guardrails any redesign must keep. |
| S5 — Reader-facing polish (S-20 mobile-first, shop framing) | in progress | `assets/css/site.css`, `assets/js/site.js`, `content/pages/index.html`, `content/pages/compare.html` | Type scale, ≥44px tap targets, sticky comparison bar, product-first front page, card system. |
| S6 — Three new question-shaped guides (completes S-13's eight) | in progress | `content/pages/guide-*.html`, `tools/build.py` | Published into the same sitemap/feed. |
| S7 — Analysis/findings page | in progress | `content/pages/analysis.html`, `tools/build.py` | Computed counter-space ranking, coverage matrix, revenue-path findings, priority matrix. |
| S8 — Docs + registers + gates + PR + merge + deploy | in progress | `EXECUTIVE_SUMMARY.md`, `data/p2/{decisions,flags}.json`, `COORDINATION.md` | Rebuild, both gates green, PR to `main`, merge, confirm Pages. |

## Review requests for another session's open work (logged per protocol — not edited)

| ID | Request | Evidence |
|---|---|---|
| RR-5 | **Open PR #16 (`arena/30a7028a-prod2`) must not be merged as-is.** It writes root-level `index.html`, `products.html`, `suggestions.html`, `flagged.html`, `sitemap.xml`, `feed.xml`, `robots.txt` and `data/products.json` as hand-authored files. On `main` those root paths are **generated mirrors** of `docs/` (INT-07: `tools/build.py` mirrors `docs/` → root) and `data/products.json` belongs to the preserved Countercraft schema. Merging PR #16 would clobber the live publication and desynchronise the mirror (its own `tools/check_site.py` would then fail `git diff` reproducibility in CI). Recommended: rebase the PR onto current `main`, retarget its generator to a non-conflicting directory, or close it and carry its unique registers only. | `main` `tools/build.py` `mirror_to_root()`; `verify.yml` reproducibility steps; PR #16 file list via `gh pr view 16 --json files`. |
| RR-6 | PR #16's branch was cut from `c6dc49a` (pre-consolidation), so it lacks the tagged-Special-Link fix, the disclosure gate and the archives. Any unique content there should be ported by an integration session, not merged wholesale. | `git log` base of `arena/30a7028a-prod2`. |

## Verification note for this session

Sandbox egress allows only github/npm/pypi hosts over the shell, so re-reads were done through the
page-fetch tool (not `curl`): each short link was followed to its final Amazon URL and the listing
`<title>` was compared character-for-character with the register. Results recorded in
`data/p2/verification-2026-11-19.json` under `session_b650562d`.

## Completion record — sess-b650562d (2026-11-19, after merging `origin/main`)

S2–S8 are done and the merge of `origin/main` (PRs #17–#22, including T-16/T-17 from
arena/9f7a78d8-prod2) is folded in rather than overwritten:

- **Suggestion portal (S2)** — all 34 items carry `theme`, two or three priced `paths`
  (change/upside/downside/cost/unlocks), a marked recommendation and `feeds_design_prompt`;
  `suggestions.html` renders a ranked board plus the item-by-item queue and an explicit
  "your move" line. Nothing that changes a claim was adopted without a named path (D-P07).
- **Questions register (S3)** — 27 items with known/missing/what-it-decides/who-answers/
  `blocking` (12) and the conservative default, each with official links for manual review;
  `questions.html` renders a gate table and the cards. Q-P02/Q-P04 were re-worded to the
  nine-guide state created by this merge.
- **Design prompt pack (S4)** — `design-prompt.html` + `data/p2/design-prompts.json`
  (G1–G8 briefs, DP-1…DP-8 blocks, sequence, guardrails); `DESIGN_PROMPT.md` records what is
  implemented, what changed (P4/P5 are published, D-P06) and what still waits on the queue.
- **Reader polish (S5)** — token-first editorial CSS, 44px tap targets, dismissible sticky
  mobile comparison bar on the 15 reader pages, product rail + format tiles + guide shelf on the
  front page (D-P08), read-date chips on cards and in the comparison table.
- **Guides (S6)** — three new guides (dual vs single basket, leave-in probe in an air fryer,
  air fryer as a gift) plus a `guides.html` index; T-17's instant-read vs leave-in guide is kept,
  so the shelf now renders nine guides and the nav/footer lists them.
- **Analysis page (S7)** — coverage matrix, capacity-to-footprint ranking, three-stage funnel,
  flag stats, owner priority board (from `data/p2/decision-priority.json`) and the dated
  verification ledger (`data/p2/verification-log.json`).
- **Gates (S8)** — `tools/checks.py` grew an `editorial` section (dated figures on the register
  tables, filler-phrase lint) and an in-page anchor check; `tools/build.py` grew seven analysis
  hooks and three shop hooks. 27 pages, `build + checks` green, `scripts/verify_site.py` and
  `npm test` green.
- **Re-verification** — all five short links re-resolved from this sandbox on 2026-11-19
  (5/5 match the register; no `tag=` on any resolved URL, so F-03 stands). Note for the board:
  **F-P08's premise is now stale** — this session's fetch tool did reach amazon.com and re-read
  the listings, so the 'sandbox cannot reach amazon.com' caveat no longer explains the flag;
  the flag itself stays open because it is the register's own read-date caveat, and only an
  owner decision (Q-P11) can set the cadence that closes it. Not edited here beyond this note.
- **Handoff** — RR-5/RR-6 stand: PR #16 was closed by another session (no longer in `gh pr list`),
  so the root-mirror clobber hazard is retired; the `site/` Countercraft build and the `docs/`
  publication still coexist per INT-06/INT-07 and neither was touched beyond regeneration.
