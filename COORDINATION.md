# COORDINATION: shared task board

Repository: `wingbangboozle1-lang/Prod2` · Base commit: `c6dc49a` (main)
Working branch for this session: `arena/f2613c86-prod2` (the branch is fixed for the session; the `session-<id>/<task>` naming in the brief is not used here).

Statuses: `unclaimed` · `in progress` · `done` · `needs review`. Items marked `needs review` are published on the Flagged for Review page and do not block anything.

## Task board

| Task | Status | Owner (session) | Files in scope | Notes |
|---|---|---|---|---|
| T1 Repo review and flags | done | f2613c86 | `COORDINATION.md`, `data/products.json` (flags) | 18 flags, FR-01 to FR-18. See Flagged page. |
| T2 Verify the five supplied links | done | f2613c86 | `data/products.json` | 5 of 5 resolve. Intended ASIN not confirmed (FR-02). |
| T3 Product register (air fryers, thermometers) | done | f2613c86 | `data/products.json`, `docs/products.html`, `docs/air-fryers.html`, `docs/meat-thermometers.html` | Prices and ratings left blank (FR-05). |
| T4 Site build (landing, subpages, guides, feeds) | done | f2613c86 | `scripts/build_site.py`, `scripts/assets/*`, `docs/**` | Static build into `docs/`. |
| T5 Compliance: disclosure, sponsored links, tracking tag | done | f2613c86 | `scripts/verify_site.py`, `docs/**` | Disclosure wording verified (Operating Agreement §5). |
| T6 Outbound-click counter (privacy-preserving) | needs review | f2613c86 | `scripts/assets/tracker.js` | Only `outbound_click` is built. Nothing is transmitted (FR-09). |
| T7 Self-hosted analytics endpoint | needs review | f2613c86 | none | Not possible on GitHub Pages; decision D-43 open (FR-09). T14 adds a locally tested optional Node host, but no public API host is deployed. |
| T8 Suggestions and open questions | done | f2613c86 | `docs/suggestions.html`, `docs/questions.html` | Nothing implemented before a choice is made. |
| T9 Executive summary, analysis, sources | done | f2613c86 | `docs/executive-summary.html`, `docs/analysis.html`, `docs/sources.html` | |
| T10 Verification gate and CI | done | f2613c86 | `scripts/verify_site.py`, `.github/workflows/verify.yml` | Runs on push and pull request. |
| T11 Publish to GitHub Pages | in progress | f2613c86 | repo Pages setting (source: main `/docs`) | Pages deploy job succeeds, but API still reports legacy source `main /`; live root serves the rendered README, not the publication, and several root routes 404. Current product site is available at `/docs/`. Admin setting change was denied; see current-session log. |
| T12 Integration with PR #1 (session d12d2304): one site, one brand, one Pages source | done | f2613c86 | all | PR #2 is merged as `77d154e`; a root-versus-`docs/` Pages source mismatch remains open under T11. |
| T13 Port the four PR #1 guides into the generated site | done | f2613c86 | `archive/counter-notes-v1/`, `scripts/build_site.py`, `docs/guides/` | Texts kept; two sentences about the short links updated to match the 2026-11-19 resolution. Original root site archived, not deleted. |
| T14 Optional self-hosted analytics endpoint and five-event aggregate collector | done | `arena/3f1d9d65-prod2` | `server.mjs`, `analytics-client.js`, `package.json`, `.gitignore`, `tests/server.test.mjs`, `.github/workflows/analytics-tests.yml`, `ANALYTICS-ENDPOINT.md` | Local self-host mode and five-event aggregation verified. Not deployed publicly; GitHub Pages remains static and owner host is not available. |

## Sources (official unless labelled)

Fetched in this session on 2026-11-19:
- Associates Program Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement (§1 Special Links and Program Content; §5 disclosure wording)
- Associates Program Policies: https://affiliate-program.amazon.com/help/operating/policies (Commission Income Statement; Participation Requirements 2(g))
- Google Search Central, qualify outbound links: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- FTC, Disclosures 101 for Social Media Influencers (dated November 2019): https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- GitHub Docs, configuring a publishing source for GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Docs, what GitHub Pages is and its visitor data collection: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- GitHub REST API, Pages settings and build types (`legacy` / `workflow`): https://docs.github.com/en/rest/pages/pages
- Supplied short links (5): https://link.amazon/B04G1MEwY · https://link.amazon/B02NbDxp3 · https://link.amazon/B00hJ57DV · https://link.amazon/B0c8moW59 · https://link.amazon/B0f3GKalj
- Amazon listing pages (5): https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH · https://www.amazon.com/dp/B0DHZTCNR5 · https://www.amazon.com/dp/B0DZFD6R9Z

Internal register (not an official source; labelled as such): Zone4 decision log, https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html (fetched).

Cited in the brief but not fetched: Google snippet guidance, creating helpful content, page experience, Creators API introduction, Zone3 FLG-003. They are labelled "not fetched" on the Sources page.

## Verification performed

- Each short link followed to its redirect target; observed ASIN recorded in its own field.
- Each listing title read; spec values quoted "as listed" only. Prices, ratings and commission rates not copied.
- Disclosure wording compared word for word against Operating Agreement §5.
- `scripts/verify_site.py` on every build: titles and meta descriptions unique; disclosure under the masthead and in the footer; every Amazon link `rel="sponsored"`; tracking tag correct; internal links and anchors resolve; every data row has an official source link; every unverified cell names a flag; banned promotional words absent; sitemap complete; feed well-formed.

## Irregularities

See the Flagged for Review page (`docs/flagged.html`) for the full list with sources. Headline items:
- FR-01: supplied tokens are 9 characters, not ASIN format, and each resolves to a different ASIN.
- FR-02: no intended ASIN confirmed.
- FR-03: Special Link test not performed (needs owner Associates account).
- FR-09: GitHub Pages cannot host the analytics endpoint; only one of five events is defined in the materials.
- FR-15: files named in the brief are not in this repository.

## Handoffs and conflicts

- **Conflict, 2026-11-19:** session `arena/d12d2304-prod2` merged PR #1 to `main` while this session was working. It had published a product-free site ("Counter Notes") at the repository root and a Pages workflow for `main`. The overlap was in `COORDINATION.md` and `README.md` (add/add conflicts).
- **Resolution:** nothing was discarded. (a) Their root site moved, unchanged, to `archive/counter-notes-v1/` (`git mv`, history kept). (b) Their four guide texts were ported into the generated site with their wording; only two sentences that predated the 2026-11-19 link resolution were updated. (c) Their brand "Counter Notes" was kept, so the site has one name. (d) Their `pages.yml` was kept and changed to publish only the generated `docs/` folder, after the verify gate. (e) Their board and log are reproduced verbatim below.
- **Superseded in part:** their `evidence.html` says the five short links were not yet resolved. That was accurate before this session. The generated `products.html`, `analysis.html` and `flagged.html` replace it.
- **Disclosure line:** their header said product links are published "only after destination and tracking checks". Product buttons on the generated site go live before the Special Link test (FR-03). The generated disclosure does not repeat that promise. Owner decision: SUG-02.
- The brief's `session-<id>/<task>` branch naming conflicts with the session branch rule; the session branch is used.
- **Tracking ID (FR-19):** see the Log. The tagged links use `shopnow047c-20` as the brief requires. Session d12d2304 did not use it in links. This is an unresolved difference, and the owner decides (SUG-02).

## Pull request and merge

- PR: https://github.com/wingbangboozle1-lang/Prod2/pull/2 (opened by f2613c86, base `main`)
- Merge result: _recorded in the final commit on this branch after the merge_
- Pages: _recorded in the final commit on this branch after the deploy check_

## Log

- 2026-11-19: Claimed T1 to T12 (session f2613c86). Repository contained only README.md at base; all content built in this session.
- 2026-11-19: PR #2 opened from `arena/f2613c86-prod2`. Merge refused (conflict) because PR #1 (session d12d2304) had been merged to `main` in the meantime. Resolved as above; see Handoffs.
- 2026-11-19: CI `verify-site` passed on the pre-merge commit. It is re-run on the resolved branch.
- 2026-11-19: `main` advanced again while PR #2 was open (PR #3 and PR #4 from session d12d2304: deployment record, and the tracking ID recorded as unverified input). Merged into this branch. Their edits to `evidence.html`, `suggestions.html` and the board were applied to the archived copies and to the history section below. Nothing was dropped.
- 2026-11-19: Position difference recorded (FR-19). Session d12d2304 did not use `shopnow047c-20` in links. This session uses it in tagged product links, as the brief's "Selected Tracking ID" requires. Enrollment of the ID is unverified, so the owner must confirm it in the account.

---

## History: session arena/d12d2304-prod2 (verbatim from `main` at commit 7e39a59, PR #1)


This repository initially contained only a minimal README and no prior coordination board. Work was performed on the Arena-assigned branch `arena/d12d2304-prod2`; branch names are fixed by the workspace. No other session claims were present at initial inspection.

| Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|
| Create a publication-style, evidence-conscious affiliate site and decision-support pages | done | arena/d12d2304-prod2 | `index.html`, `suggestions.html`, `evidence.html`, `guides/`, `assets/`, `.github/workflows/`, `README.md`, `COORDINATION.md`, `feed.xml`, `sitemap.xml`, `robots.txt` | Published via PR #1; GitHub Pages deployment succeeded on main. Hosted site verified at the expected Pages origin. |

## Verification / handoff log

### Evidence boundaries and irregularities

- The five user-provided `https://link.amazon/...` URLs are opaque short links. Their intended products, ASINs, official listing URLs, destination behavior, Special Link compliance, and tracking report status have not been verified. Their path tokens are not treated as ASINs; the submitted URL/source, intended product fields, and observed redirect field are separate. No conclusion that the supplied links are invalid is made.
- The project supplied tracking ID `shopnow047c-20`; it is recorded as user input only. Its Associates account status and relation to tested Special Links are not verified, and it was not appended to or used to generate links.
- No product-level specifications, pricing, ratings, reviews, popularity, commission, conversion, or revenue assertions are included. Guides are decision frameworks, not hands-on testing or product recommendations.
- No analytics endpoint, Search Console property, or report data exists in this repository. The five event names are proposed only; the campaign ledger remains empty. A privacy-reviewed backend and account/property setup are required.
- Site canonical URLs target the expected GitHub Pages project address `https://wingbangboozle1-lang.github.io/Prod2/`; this is a deployment assumption pending confirmation of the actual Pages origin/custom domain.
- Original product photos were not available. No stock, copied, or generated product photography was used; the front-page abstract editorial illustration is CSS.

### Official-source checks performed 2026-11-19

- Amazon Associates Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement — fetched current page; it states the Associates links must use provided tagged Special Link formats and section 5 gives the Associate identification statement. Page indicated updated October 15, 2025.
- Amazon Associates Program Policies: https://affiliate-program.amazon.com/help/operating/policies — fetched current page; page indicated updated April 14, 2026. It incorporates the policies by reference into the Agreement.
- FTC Disclosures 101: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers — fetched official FTC page, including disclosure visibility/clarity and no claims about experiences with products not tried.
- Google Search Central outbound-link qualification: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links — fetched; specifies `rel="sponsored"` for advertising or paid placements.
- Google Search Central people-first content guidance: https://developers.google.com/search/docs/fundamentals/creating-helpful-content — fetched; supports original, useful, non-search-engine-first editorial standards.
- Source links are provided on `evidence.html` and `suggestions.html` for manual review. No official product-specific sources could be checked because the products themselves remain unidentified.

### Checks performed

- `git diff --check` passed.
- HTML check covered all 7 HTML pages: unique page titles present; descriptions and disclosure strips present; local links resolve; the five product URLs carry `rel="sponsored"` (also `nofollow`); sitemap and RSS XML parse successfully.
- First Pages workflow attempt failed because `upload-pages-artifact` was given a multiline path list; fixed by assembling an explicit `_site` artifact. The artifact upload/build then passed, but deployment from the feature branch was blocked by GitHub Pages environment protection. The workflow now deploys only from `main`; verify the post-merge main-branch run and hosted site before calling it live.
- Link/source validation is not a substitute for checking actual hosted Pages deployment, Search Console, or Associates link reports. Those remain flagged, not marked verified.

### Pull request and deployment result

- PR #1: https://github.com/wingbangboozle1-lang/Prod2/pull/1 — merged with a merge commit on 2026-11-19 (`7e39a599a1d87db5107ed132fa347728642a9655`).
- Successful main-branch Pages workflow run: https://github.com/wingbangboozle1-lang/Prod2/actions/runs/44526867564 — build artifact and deploy jobs both succeeded.
- Live site verified at https://wingbangboozle1-lang.github.io/Prod2/; fetched the homepage, evidence page, suggestions page, RSS feed, and sitemap after deployment.
- Main branch is the authorized Pages deployment source; feature-branch build passes and deploy is skipped by design because environment protection rejects feature branches.
- Note: GitHub's Pages API reported `build_type: legacy` / source `main` while the Actions deployment job also succeeded. The live files at the expected origin were fetched successfully; check the repository Pages settings if deployment mode is later changed.

## Current Arena session handoff — `arena/3f1d9d65-prod2`

- The current checkout started from `c6dc49a`, before the coordination board and publication work landed on `main`. While preparing a separate full-site build, `git pull --rebase origin main` exposed the intervening PR #1–#4 work and the merged PR #2 integration. No files from `origin/main` were discarded.
- The full-site duplicate generated from the stale checkout was not applied over the merged `docs/` site and is not included in this PR. This session will work only on the separate self-hosted event endpoint in T14.
- Request to T6/T7 integration owner: please review whether the existing `docs/assets/tracker.js` should send the documented five event types when served by an API-capable host. This session will not edit that existing tracker/build scope; the new Node server can optionally inject its own event client at response time.
- Official source additionally checked: GitHub Docs, https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages — GitHub Pages is a static hosting service; its documentation also says visitor IP addresses are logged for security. This host-level collection is distinct from the app's aggregate endpoint.
- Rebase conflict handled without discarding upstream work: `COORDINATION.md` was resolved by retaining the complete `origin/main` board/history and appending this session's T14 claim/handoff. The stale duplicate site build remains in a local stash only; it is not part of this PR.
- T14 implementation: optional `server.mjs` serves existing `docs/` and enables the existing click tracker plus a separate client for `page_view`, `outbound_click`, `guide_open`, `category_open`, and `rss_feed_click`. The endpoint accepts only those event types and safe dimensions, stores aggregate counts only, rejects foreign Origins, and ignores timestamps and extra fields. GitHub Pages remains unchanged/static; this endpoint has not been deployed to a public Node host.
- Verification: `npm test` passed (`scripts/verify_site.py`: 18 pages OK; Node event endpoint integration test passed). `git diff --check` passed. Local HTTP smoke test returned 200 for `/`, products, a guide, suggestions, flagged page, RSS, sitemap and `/api/client.js`; live preview runs in self-host mode.
- Live Pages check before and after PR #5: `gh api repos/wingbangboozle1-lang/Prod2/pages` reported `build_type=legacy`, source `main /`. Main Pages Actions run 44529573813, verify run 44529573975, and analytics test run 44529573780 all succeeded. The live root now renders the repository README rather than the publication; `/executive-summary.html`, `/flagged.html`, and `/products.html` return 404, while `/docs/index.html`, `/docs/executive-summary.html`, and `/docs/flagged.html` return the current product site. The intended single root site is not confirmed live despite successful workflow jobs.
- Attempted to switch Pages to `build_type=workflow` through the Pages REST API; GitHub returned HTTP 403 `Resource not accessible by integration`. The API documentation says updating Pages requires a repository administrator/maintainer or the `manage GitHub Pages settings` permission. No setting was changed; retain T11 as open and do not claim the root deployment is fixed.
- PR #5: https://github.com/wingbangboozle1-lang/Prod2/pull/5 — merged with merge commit `bebb5cbb2c2ad9ef8b5746fc486dc25e6c61dcf2` on 2026-11-19. PR checks and post-merge workflows passed. Public endpoint deployment remains unconfigured; GitHub Pages stays static.
