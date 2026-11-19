# DECISIONS.md — Decision Log

Tracking ID: `shopnow047c-20`. This log records the decisions taken for the Countercraft build and
the decisions that are still open. "Open" items are published on the **Suggestions** page with a
recommended path; none are decided without the information listed.

## Taken

| ID | Decision | Rationale | Source |
| --- | --- | --- | --- |
| D-01 | Brand name: **Countercraft** | Reads like a shop and a publication; ties to the kitchen-counter theme. | S-15 |
| D-02 | Lead with products, data below the fold | Front page is a publication front page; the register sits after the shop content. | "Lead with the products" |
| D-03 | Single navigation group; all dashboard surfaces in the footer | Every page (Research Desk, Suggestions, Flagged, About) reachable from one nav and the footer. | "keep every dashboard surface reachable" |
| D-04 | Disclosure strip under the masthead on every page + footer | Above-the-fold disclosure on every page, including the front page. | FTC S07/S24; Operating Agreement |
| D-05 | Every outbound product link `rel="sponsored"` | Paid/commission links must be marked. Enforced by build + gate. | Google S11 |
| D-06 | Ratings shown only where captured; uncaptured left blank + flagged | Never infer a value. 4 of 5 ratings not captured from the listing extraction. | "never infer or fill in values" |
| D-07 | Prices shown "as listed" with a date and a live link; no cross-retailer price comparison | Program Policies 2(b): prices only via Amazon-served link or Creators/PA API. | Program Policies 2(b) |
| D-08 | Product-intent record keeps intended vs. observed in separate fields | Intent and observation are different facts; never merged. | "Build a product-intent confirmation record" |
| D-09 | Submitted short links published as the source, compliance status flagged unresolved | Not declared invalid; 6(w) status unresolved. Recommend Special Links before scaling. | Program Policies 6(w) |
| D-10 | Eight question-shaped guides, one page per question | Publish the questions buyers type; internally link to comparison + categories. | S-07, S-13 |
| D-11 | Counter-space analysis published with the formula; depth figures flagged | Capacity per unit of counter depth; depth inputs must come from official listings, not guessed. | S-23 |
| D-12 | Privacy-preserving click counter, no cookies, five events | Automate measurement without third-party tracking. | "Turn on click and conversion measurement" |
| D-13 | Campaign ledger starts empty and well-defined | No conversion score or forecast without an authorized first-party report. | Priority 4 |
| D-14 | Compliance gate in the publishing workflow | Checklist before publish: disclosure, rel=sponsored, price label, no inferred values. | Priority 5 |
| D-15 | Sitemap, RSS, robots, unique meta, structured data, OG/Twitter cards | One site for engines to index, with a reason to rank it. | S-04, S-09 |
| D-16 | Text-led imagery; no generated or copied product photography | Operating Agreement §1 treats images as Program Content; S-18 needs a decision first. | Operating Agreement; S-18 |

## Open (need information before deciding)

| ID | Question | What's missing | Recommended path |
| --- | --- | --- | --- |
| D-20 | Replace short links with tagged Special Links? | Enrolled Associates account + ability to generate Special Links for the five ASINs. | Generate Special Links, test one per product, confirm destination + tracking report. |
| D-21 | Pull ratings via Creators/PA API? | API access status. | If granted, pull ratings through the API; otherwise keep blank + flagged. |
| D-22 | Where does the `/collect` analytics endpoint run? | Hosting choice for the self-hosted endpoint. | Serverless function at `/collect` alongside the static site. |
| D-23 | Which imagery channel is permitted? | Confirmation of which imagery is allowed under the Agreement. | Stay text-led until confirmed; then use only permitted imagery. |
| D-24 | Publishing cadence and topic order? | Measured query data (analytics + Search Console). | Weekly cadence; reorder next topics from measured queries. |

## Notes on the reference items (S-04 … S-25)

The source brief lists items S-04 through S-25 with priorities and implementation statuses. This
build implements the reader-facing and machinery items directly (unique meta S-04, rel=sponsored
S-05, question-shaped guides S-07, structured data + social preview S-09, docs-in-line S-10,
review-page split S-11, voice/rewrite S-12, topic calendar S-13, design brief S-14, brand S-15,
evidence rule for "trending" S-16, editorial homepage S-17, chooser S-19, counter-space S-23,
internal linking S-24). S-06 (original "live with" reviews) and S-18 (real product photography)
are **not adopted / need a decision** and are recorded here and on the Suggestions page rather
than implemented, because they require first-person experience or permitted imagery that we do
not have. S-20 (mobile-first pass) is implemented in the CSS. S-25 (organic traffic on the
verification angle) is addressed by the question-shaped guides + sitemap + RSS + analytics, with
topics chosen from measured queries once analytics are live.
