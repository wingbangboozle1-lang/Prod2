# PR: The Crisp Counter — affiliate publication site

## Summary of changes

Builds the complete Amazon Associates publication in this repository:

- **28-page static site** (`build.py` → `public/`, deployed to GitHub Pages):
  storefront front page, shop by format (3 category pages), eight
  question-shaped guides, comparison page with a three-question chooser,
  counter-space method page, four data pages (product register, source
  register, campaign ledger, events & privacy), four review pages (flagged,
  decisions, methodology), suggestions, open questions, executive summary,
  about & disclosure, 404.
- **Canonical registers** (`data/*.json`) carrying the predecessor Zone4
  records verbatim-cited: three verified products with published Special
  Links (`?tag=shopnow047c-20`), two held products (P4/P5, never published),
  intent record with intended/observed fields kept separate, empty-by-rule
  campaign ledger, five-event privacy model, flag register split
  open/resolved/historical, suggestion queue, open decision-input questions.
- **Compliance machinery**: disclosure strip above the fold on every page
  (repeated in footer with the Amazon IP notice), every outbound Amazon link
  `rel="sponsored"` + tag parameter, no shorteners, no held-ASIN or
  short-link anchors, no prices/ratings/popularity claims anywhere, unique
  titles + meta descriptions, JSON-LD, sitemap, RSS feed, robots.txt.
- **Measurement**: cookieless first-party recorder wired for the five defined
  events, live local counts on the events page, dependency-free
  self-hosted collector (smoke-tested).
- **30-check suite** (`check.py`) run in CI before the Pages deploy; docs
  (ENGINE.md) assert the check count against the code.
- **Coordination**: COORDINATION.md task board claimed before work began;
  Zone4 registers imported read-only as a provenance archive.

## Sources used

Official citations only, listed in `data/sources.json` and shown with
fetched/cited status on the site's Source register page: the three official
Amazon listing pages (S-P1..S-P3), the held listings (S-P4/S-P5), the five
submitted short links recorded verbatim (S-L1..S-L5), the Associates Operating
Agreement (S-OA), Program Policies (S-POL), FTC guidance (S-FTC, S-FTC-END),
Google Search Central docs (S-SNIP, S-OUTL, S-SPAM, S-HELP, S-PEXP), Amazon's
ASIN guide (S-ASIN), the commission table (S-COMM), and the predecessor
register archive (S-Z4).

## Flagged irregularities (published on review/flagged.html; non-blocking)

- FLG-03: no fact re-read in this environment (egress allowlist excludes
  amazon.com); carried values keep their original dated citations.
- FLG-04: tracking ID active status unconfirmed (Associates Central only).
- FLG-07: click attribution unverified until the one-link-per-product test.
- FLG-06: P4/P5 held — observed listings outside the air-fryer scope,
  identity unconfirmed; registered, never published.
- FLG-01/02: short links recorded verbatim; path codes are not ASINs;
  compliance status unresolved (never judged valid or invalid).
- FLG-05: policy pages cited, not re-quoted, in this environment.
- FLG-08: collector shipped but not hosted (Pages is static).
- FLG-09: Search Console property needs owner verification.
- FLG-10: photography path undecided; site ships non-photographic.

## Verification performed

`python3 build.py` then `python3 check.py` (30/30) on this branch before the
PR; CI re-runs both on the merge. Collector smoke-tested locally
(health, accept, reject, count). Spot checks: disclosure strip above `<main>`
on all 28 pages, sponsored+tagged anchors only on published ASINs, guide
internal linking complete.
