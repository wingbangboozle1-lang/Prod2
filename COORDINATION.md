# Coordination

This repository initially contained only a minimal README and no prior coordination board. Work was performed on the Arena-assigned branch `arena/d12d2304-prod2`; branch names are fixed by the workspace. No other session claims were present at initial inspection.

| Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|
| Create a publication-style, evidence-conscious affiliate site and decision-support pages | done | arena/d12d2304-prod2 | `index.html`, `suggestions.html`, `evidence.html`, `guides/`, `assets/`, `.github/workflows/`, `README.md`, `COORDINATION.md`, `feed.xml`, `sitemap.xml`, `robots.txt` | Static publication, decision room, source register, feed, sitemap, and Pages workflow added. Deployment still requires checking GitHub Pages settings and workflow. |

## Verification / handoff log

### Evidence boundaries and irregularities

- The five user-provided `https://link.amazon/...` URLs are opaque short links. Their intended products, ASINs, official listing URLs, destination behavior, Special Link compliance, and tracking report status have not been verified. Their path tokens are not treated as ASINs; the submitted URL/source, intended product fields, and observed redirect field are separate. No conclusion that the supplied links are invalid is made.
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
- Link/source validation is not a substitute for checking actual hosted Pages deployment, Search Console, or Associates link reports. Those remain flagged, not marked verified.
