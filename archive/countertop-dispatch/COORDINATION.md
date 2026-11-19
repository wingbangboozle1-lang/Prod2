# COORDINATION.md — shared task board

Repo: `wingbangboozle1-lang/Prod2` · Site: https://wingbangboozle1-lang.github.io/Prod2/
Created: 2026-11-19 (session `arena-30a7028a`)

## How to claim

1. Add or update a row below with your session ID, status, and file scope.
2. Commit and push the claim **before** starting work.
3. Status values: `unclaimed` · `in progress` · `done` · `needs review`
   (`needs review` = item is published on the Flagged for Review page; it does not block anything).
4. Keep scopes non-overlapping. If you must touch a file another session owns, log a
   request in the Request log instead of editing it.
5. Never mark anything `verified` without an official source link.

## Sessions

| Session ID | Branch | Notes |
| --- | --- | --- |
| `arena-30a7028a` | `arena/30a7028a-prod2` | Single integration session for this run (all tasks below). Arena sessions run on their own fixed branch; this session owns the whole tree and integrates to `main` via PR. |

## Task board

| Task | Status | Owning session | Files |
| --- | --- | --- | --- |
| T1 · Create COORDINATION.md task board, claim all tasks | done | `arena-30a7028a` | COORDINATION.md |
| T2 · Verify the five submitted link.amazon tokens (length, live resolution) against Amazon's official ASIN definition | done | `arena-30a7028a` | data/submitted-links.json, flagged.html |
| T3 · Build product-intent confirmation register (intended ASIN / listing URL / date / source; observed redirects in a separate field) | done | `arena-30a7028a` | data/product-intent.json |
| T4 · Build the site: landing page (publication front page), product table, analysis, executive summary, suggestions, flagged-for-review, article/guide subpages | done | `arena-30a7028a` | *.html, assets/* |
| T5 · Disclosure strip under masthead on every page + footer repeat; `rel="sponsored"` + Associates tag `shopnow047c-20` on every outbound product link | done | `arena-30a7028a` | *.html, assets/site.js |
| T6 · SEO: unique title + meta description per page, sitemap.xml, robots.txt, RSS feed, JSON-LD structured data | done | `arena-30a7028a` | *.html, sitemap.xml, robots.txt, feed.xml |
| T7 · Privacy-preserving click/conversion measurement: five defined events, client-side counter, configurable self-hosted endpoint (empty campaign ledger) | done | `arena-30a7028a` | assets/analytics.js, data/campaign-ledger.csv, data/events.json |
| T8 · Question-shaped guide articles (4 working titles) added to sitemap + feed | done | `arena-30a7028a` | articles/*.html, sitemap.xml, feed.xml |
| T9 · Line-by-line verification pass: every table row carries an official source link; unverifiable values left blank and flagged | done | `arena-30a7028a` | flagged.html, all data tables |
| T10 · Suggestions & decision-support section (open questions, missing information, options) | done | `arena-30a7028a` | suggestions.html |
| T11 · Link check (no broken internal links), sitemap coverage, clean-checkout verification scripts | done | `arena-30a7028a` | tools/check_site.py |
| T12 · Integration: PR to `main`, merge, confirm GitHub Pages deploy, record PR link + merge result here | done | `arena-30a7028a` | COORDINATION.md |

## Source register (official sources used)

| ID | Source | URL | Used for | Read on |
| --- | --- | --- | --- | --- |
| S01 | Amazon Associates Program Operating Agreement | https://affiliate-program.amazon.com/help/operating/agreement | Special Link definition, disclosure obligations | 2026-11-19 |
| S02 | Amazon Associates Program Policies | https://affiliate-program.amazon.com/help/operating/policies | Participation requirements, link marking | 2026-11-19 |
| S03 | Amazon Services Associates Program — Operating Agreement (public copy, Section 1) | https://affiliate-program.amazon.com/help/operating/agreement | Program Content, Special Links | 2026-11-19 |
| S04 | Amazon help: What is an ASIN? | https://www.amazon.com/gp/help/customer/display.html?nodeId=201188900 | ASIN = 10-character identifier | 2026-11-19 |
| S05 | Google Search Central — qualify outbound links | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` guidance | 2026-11-19 |
| S06 | Google Search Central — create unique descriptions | https://developers.google.com/search/docs/appearance/snippet | per-page meta descriptions | 2026-11-19 |
| S07 | FTC — Disclosures 101 for social media influencers | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | disclosure placement | 2026-11-19 |
| S24 | FTC — Guides Concerning the Use of Endorsements and Testimonials | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | endorsement context review | 2026-11-19 |
| S08 | GitHub Pages documentation | https://docs.github.com/en/pages | deploy verification | 2026-11-19 |
| S09 | Amazon Associates — link creation tools (SiteStripe / Special Links) | https://affiliate-program.amazon.com/help/topic/linking.html | Special Link format with `tag=` | 2026-11-19 |

## Verification log

| Date | What was checked | Method | Result |
| --- | --- | --- | --- |
| 2026-11-19 | Five submitted tokens length (B04G1MEwY, B02NbDxp3, B00hJ57DV, B0c8moW59, B0f3GKalj) | counted characters; compared against Amazon ASIN definition (S04) | all five are 9 characters; Amazon defines an ASIN as 10 characters → tokens are not ASINs (irregularity, published on flagged.html) |
| 2026-11-19 | Live resolution of each link.amazon token | HTTP fetch of each submitted URL, redirect target recorded verbatim | recorded in data/submitted-links.json as *observed* targets, kept separate from *intended* values |
| 2026-11-19 | Product rows (title, price, rating, category) for each resolved listing | fetched official amazon.com listing pages | only values visible on the official listing are published; anything not shown left blank and flagged |
| 2026-11-19 | Associates tag `shopnow047c-20` embedded in every outbound product link | grep over rendered HTML | pass (tools/check_site.py) |
| 2026-11-19 | Disclosure strip present under masthead on every page, repeated in footer | tools/check_site.py | pass |
| 2026-11-19 | Every `<td>` in published data tables carries a source link | tools/check_site.py | pass; unverifiable cells are blank + flagged |
| 2026-11-19 | Internal links + sitemap coverage | tools/check_site.py | pass |

## Request log (cross-scope changes)

| Date | Requesting session | File owned by | Request | Status |
| --- | --- | --- | --- | --- |
| — | — | — | none | — |

## Merge / deploy record

| Item | Value |
| --- | --- |
| Integration branch | `arena/30a7028a-prod2` |
| PR | #1 https://github.com/wingbangboozle1-lang/Prod2/pull/1 |
| Merge | merged to `main` (squash) 2026-11-19 |
| GitHub Pages | https://wingbangboozle1-lang.github.io/Prod2/ — status `built` after merge |
| Irregularities blocking merge | none (flagged items published on flagged.html) |

## Handoffs / conflicts

| Date | What happened | Resolution |
| --- | --- | --- |
| — | none | — |
