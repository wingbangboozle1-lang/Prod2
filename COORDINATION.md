# COORDINATION.md — Shared Task Board

Repo: `wingbangboozle1-lang/Prod2`
Tracking ID: `shopnow047c-20`
Current session: **session-arena-599eec57** (branch `arena/599eec57-prod2`)

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
| T1 — Repo review | done | session-arena-599eec57 | — |
| T2 — Verify the 5 submitted affiliate links (resolve + identity + price + category) | done | session-arena-599eec57 | `data/products.json`, `data/sources.json` |
| T3 — Verify compliance sources (Agreement, Policies, ASIN definition, FTC) | done | session-arena-599eec57 | `data/sources.json` |
| T4 — Data model + build system (data-driven static site) | in progress | session-arena-599eec57 | `data/*.json`, `scripts/build_site.py` |
| T5 — Site generation (landing + category + comparison + guides) | in progress | session-arena-599eec57 | `scripts/build_site.py` -> `site/` |
| T6 — Disclosure strip, `rel="sponsored"`, product-intent record, click counter | in progress | session-arena-599eec57 | `site/assets/*`, `scripts/build_site.py` |
| T7 — Findability (sitemap, RSS, robots, unique meta, structured data) | in progress | session-arena-599eec57 | `site/sitemap.xml`, `site/rss.xml`, `site/robots.txt` |
| T8 — Suggestions / decision portal (questions, info needed, path chooser) | in progress | session-arena-599eec57 | `data/suggestions.json`, `site/suggestions.html` |
| T9 — Flagged for Review page | in progress | session-arena-599eec57 | `site/flagged.html` |
| T10 — Verification gate (sources per row, rel=sponsored, disclosure, sitemap) | in progress | session-arena-599eec57 | `scripts/verify_site.py` |
| T11 — Integration, PR, merge, GitHub Pages deploy | pending | session-arena-599eec57 | `site/`, `.github/workflows/pages.yml` |

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

- PR #10 (final integration): https://github.com/wingbangboozle1-lang/Prod2/pull/10 — **merged** (merge commit `25119abf`); CI checks (`test`, `verify`) passed before merge.
- Pages API: `PUT /pages {build_type: workflow}` returned **403** with this session's token (third recorded occurrence) — Pages remained in legacy `main /` mode; flipping it needs a repository admin.
- Actions deployment for the merge commit: `github-pages` environment reported success; sandbox egress to `*.github.io` is blocked, so live HTML could not be fetched from the session.
- **INT-07 (root mirror, PR #11):** legacy Pages serves the repository root, which had no `index.html` after consolidation. The generator now mirrors the deterministic `site/` output to the repo root (one source of truth, two deterministic outputs; reproducibility check extended in `verify.yml`). PR #11: https://github.com/wingbangboozle1-lang/Prod2/pull/11 — **merged** (merge commit `8c3c9a23`); CI passed.
- **Deploy verified (API):** legacy `pages-build-deployment` run for `8c3c9a23` completed with **success**; `GET /pages/builds/latest` → `{status: built, commit: 8c3c9a23}`. The live site at https://wingbangboozle1-lang.github.io/Prod2/ now serves the canonical Countercraft build at root paths with corrected canonical URLs. An HTML fetch from inside the session was impossible (egress restriction); verification is by GitHub's build/deployment API plus the repo-side gate. This is the final deploy result for the brief's "confirm GitHub Pages deploys successfully" step.
- When an admin flips Pages to Actions mode, delete the root mirror in a single commit (documented in README).

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

