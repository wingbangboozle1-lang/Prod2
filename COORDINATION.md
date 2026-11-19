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
| T7 Self-hosted analytics endpoint | needs review | f2613c86 | none | Not possible on GitHub Pages; decision D-43 open (FR-09). |
| T8 Suggestions and open questions | done | f2613c86 | `docs/suggestions.html`, `docs/questions.html` | Nothing implemented before a choice is made. |
| T9 Executive summary, analysis, sources | done | f2613c86 | `docs/executive-summary.html`, `docs/analysis.html`, `docs/sources.html` | |
| T10 Verification gate and CI | done | f2613c86 | `scripts/verify_site.py`, `.github/workflows/verify.yml` | Runs on push and pull request. |
| T11 Publish to GitHub Pages | in progress | f2613c86 | repo Pages setting (source: main `/docs`) | Set after merge. Status recorded below. |
| T12 Integration: merge, re-verify, PR, merge to main | in progress | f2613c86 | all | PR and merge result recorded below. |

## Sources (official unless labelled)

Fetched in this session on 2026-11-19:
- Associates Program Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement (§1 Special Links and Program Content; §5 disclosure wording)
- Associates Program Policies: https://affiliate-program.amazon.com/help/operating/policies (Commission Income Statement; Participation Requirements 2(g))
- Google Search Central, qualify outbound links: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- FTC, Disclosures 101 for Social Media Influencers (dated November 2019): https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- GitHub Docs, configuring a publishing source for GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
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

- No other session has claimed a task on this repository. No merge conflicts occurred.
- The brief's `session-<id>/<task>` branch naming conflicts with the session branch rule; the session branch is used.

## Pull request and merge

- PR: _to be recorded after creation_
- Merge result: _to be recorded after merge_
- Pages: _to be recorded after deploy_

## Log

- 2026-11-19: Claimed T1 to T12 (session f2613c86). Repository contained only README.md; all content built in this session.
