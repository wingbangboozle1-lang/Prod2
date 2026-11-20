# Executive summary: Prod2 affiliate publication

**Review prepared:** 2026-11-20  
**Publication:** [Prod2 product guides and kitchen-tool comparisons](https://wingbangboozle1-lang.github.io/Prod2/)  
**Tracking ID in published product links:** `shopnow047c-20`  
**Status:** the static publication, its release gates and its live GitHub Pages deployment were checked on 2026-11-20 and are described below. The Associates account state, tagged-link attribution, Search Console indexing and performance, product price and availability, hands-on product testing, sales, commissions and revenue were **not** verified in this review and are not claimed anywhere on the site.

## What this publication is

Prod2 is a reader-facing static publication about air fryers and kitchen thermometers. It puts product comparisons and question-led buying and usage guides first, and keeps the research trail — method, flagged items, open questions, suggestions, decisions, compliance and measurement — reachable from one navigation group and every footer. Product details come from the source records in this repository and carry their verification dates and limits; anything unconfirmed stays blank or flagged rather than filled in.

A product listing is not a hands-on test. A listed capacity or a listed dimension does not by itself establish serving size, whether a real piece of food will fit, how fast a machine cooks, how popular it is, or that one product is better than another. Where the site compares two products, it compares the values that were actually read, and it names the trade-off instead of declaring a winner ([D-23](decisions.html#D-23)).

Every outbound Amazon product link is a tagged Special Link marked `rel="sponsored"`, and each page carries the Associates disclosure directly beneath the masthead with a repeat in the footer. The owner-supplied short links are kept in intent records beside any redirect observation; this summary does not declare them compliant or non-compliant. The campaign ledger is empty by rule: a local click count is not an order, a commission or a revenue record.

## The five products and what is verified

| # | Product | Format | ASIN | What is verified | What is not |
|---|---|---|---|---|---|
| P1 | Chefman 6 qt dual basket air fryer oven | Dual-basket | `B0CDY277D3` | Listing title, capacity, dimensions and feature bullets read 2026-11-20 | Price, rating, hands-on results |
| P2 | Emeril Lagasse 26 qt French door air fryer toaster oven | Oven-style | `B09B7SB46R` | Listing title, capacity and dimensions read 2026-11-20 | The preset-count discrepancy is still open ([F-26](flagged.html#F-26), [Q-31](questions.html#Q-31)) |
| P3 | Chefman 8 qt TurboFry air fryer | Single-basket | `B08DKYBTPH` | Listing title, capacity and dimensions read 2026-11-20 | The size-variant family is still open ([F-08](flagged.html#F-08)) |
| P4 | ThermoMaven 1-second digital meat thermometer | Instant-read | `B0DHZTCNR5` | Listing title, accuracy claim and IP rating read 2026-11-20 | Accuracy as experienced; no calibration test was run |
| P5 | CHEF iQ Sense Gen3 wireless meat thermometer | Wireless leave-in | `B0DZFD6R9Z` | Listing title, probe count and temperature range read 2026-11-20 | Range and accuracy as experienced |

All five listings were re-fetched live on 2026-11-20 and every observed string is recorded in `data/p2/verification-2026-11-20.json`, including the values that were *not* observed. Three of the five listings show a neighbouring product's price or rating in the visible page; none of those was mistaken for the target product ([F-P17](flagged.html#F-P17)). No price and no star rating is published anywhere on the site ([F-02](flagged.html#F-02)), and no product-level commission rate is published ([F-01](flagged.html#F-01)).

## What is deliberately absent

- **Prices and star ratings** — withheld by policy, not by oversight ([F-02](flagged.html#F-02), [D-P11](decisions.html#D-P11)).
- **Hands-on testing claims** — nobody here has cooked with these machines, so the site is a specification publication until real usage exists ([D-06](decisions.html#D-06), queued as [SG-07](suggestions.html#SG-07)).
- **Forecasts and conversion scores** — the campaign ledger starts empty and fills only from authorized first-party reports.
- **Popularity claims** — a "best" or "most popular" statement needs a dated official snapshot, which the site does not have ([D-19](decisions.html#D-19)).

## Measurement: five local events, two deployment roles

The browser client (`assets/js/measure.js`) declares exactly five local events — `page_view`, `outbound_click`, `guide_read_75`, `category_click`, `feed_click` — and carries no visitor identity: no cookies, no identifiers, no referrer capture, and only the ASIN and target host on an outbound click. While `settings.analytics_endpoint` is empty, nothing leaves the browser; events are counted in the reader's own local storage, for the reader's own view.

The two deployment roles are different things and are not interchangeable:

- **Static publication (what is live).** GitHub Pages serves files. It exposes no API, so the live site collects nothing and the configured endpoint attribute is deliberately empty. The client can emit events; nothing is receiving them.
- **Optional self-hosted endpoint (not hosted).** `server.mjs` is a dependency-free Node server that accepts the same five events over `POST /api/events`, validates each body against the published contract, and stores daily aggregate counts per event and path in a single JSON file. It stores no IP address, user agent, referrer, cookie, timestamp or visitor identifier, and writes no request log. It is deployable on any owner-controlled host; it is not deployed ([F-19](flagged.html#F-19), [Q-23](questions.html#Q-23)).

The campaign ledger's five events (`impression`, `click`, `session`, `order`, `refund`) are a third, separate, report-only system ([D-P05](decisions.html#D-P05)). A ledger row appears only when the owner exports an authorized report.

## AI answer platforms: a measurement question, not an optimisation target

Google's own guidance, read on 2026-11-20, sets the boundary. There are **no additional technical
requirements** to appear as a supporting link in AI Overviews or AI Mode: a page must be indexed
and eligible for a snippet, which is the same requirement as ordinary Search. The generative AI
features retrieve from the Search index with query fan-out, so eligibility follows ordinary
indexing rather than a separate application. A site must be **included in Search generative AI
features in Search Console** to be eligible for display, and AI-feature traffic is reported **only
inside the "Web" search type** of the Performance report — so AI visibility cannot be separated out
at all until the property is verified, which it is not.

Two further constraints shape the roadmap. Producing content for every query variation, including
fan-out queries, violates Google's scaled content abuse spam policy, so this site's fourteen-day
editorial cadence stands and no query-farmed pages are written. And Google's documented lever is
non-commodity content: for this site that means the dated verification register and its published
limits — not first-hand reviews, which nobody here can honestly write.

The evidence-gated roadmap is published as [SG-42](suggestions.html#SG-42), with the two missing
inputs recorded as [Q-P15](questions.html#Q-P15) and [Q-P16](questions.html#Q-P16) and the stance
as [D-P16](decisions.html#D-P16). No `llms.txt`, no AI-only structured data and no machine-generated
summaries of listings are added: the guidance documents no such requirement, and Amazon listing
photography stays unpublished until the Program Content licence review closes
([Q-P05](questions.html#Q-P05)).

## What the local gates prove, and what they cannot prove

`python3 tools/build.py && python3 tools/checks.py` renders the publication and runs the release gate over the result: unique titles and meta descriptions, disclosure placement, the Amazon link policy, internal link integrity, markup validity, register cross-references, sourced product facts, banned claims, site chrome, SEO metadata, sitemap and feed coverage, the shop shelf, publication consistency and build freshness. `npm test` adds the endpoint's own contract test.

Passing those gates proves that the code and the repository data meet those checks on the commit that was checked. It does not prove live deployment success, legal approval, search visibility, affiliate acceptance, sales or revenue. Live deployment was confirmed separately for this review: the repository's Pages API reported the site built and serving from branch `main` at the repository root, and the published sitemap, feed and robots file were fetched successfully.

## Open items for a decision-maker

1. Run the one-link-per-product test in Associates Central — it gates every attribution claim ([F-57](flagged.html#F-57), [F-58](flagged.html#F-58), [Q-01](questions.html#Q-01)).
2. Host the endpoint and verify the property in Search Console — everything downstream depends on it ([SG-06](suggestions.html#SG-06), [SG-29](suggestions.html#SG-29), [F-P13](flagged.html#F-P13), [Q-P08](questions.html#Q-P08)).
3. Settle the reader-capture consent basis before the question form is connected ([Q-47](questions.html#Q-47), [F-P14](flagged.html#F-P14)).
4. Decide whether to adopt a dated-snapshot price policy, and only with automation ([SG-05](suggestions.html#SG-05)).
5. Decide the product-photography question; Amazon listing photography is Program Content ([D-12](decisions.html#D-12), [D-22](decisions.html#D-22)).

## Official sources for reviewer use

| Topic | Official reference | Review note |
|---|---|---|
| Amazon Associates operating requirements, disclosures, links, product-content licence and current policies | [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Amazon states that policy versions may change; recheck before launch and whenever the program changes. The page showed an update date of April 14, 2026 when it was read on November 20, 2026. |
| Amazon Associates linking tools and product-link creation | [Associates Central linking tools](https://affiliate-program.amazon.com/welcome/topic/tools) | Generate and validate product links through the authorized account; confirm real link tags and destinations there. |
| Amazon product-data access options | [Creators API information](https://affiliate-program.amazon.com/creatorsapi) | The public page redirected to sign-in during this review, so eligibility, credentials, current terms and approval remain account-dependent and are not asserted here. |
| FTC endorsement and affiliate disclosure guidance | [FTC: Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | Plain, clear disclosure is useful guidance; obtain legal review where appropriate. |
| Google Search people-first content guidance | [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | Focus on useful original content and transparent authorship and process; no ranking guarantee. |
| Google Search Essentials and spam policies | [Search Essentials](https://developers.google.com/search/docs/essentials) · [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Avoid thin affiliate pages, scaled low-value content and unsupported search-manipulation tactics. |
| Google Search Console setup and monitoring | [Get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start) | Ownership verification and authorized account access are required for site-specific indexing and performance data. |
| GitHub Pages publishing source | [Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) · [Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source) | Confirm the repository's Pages settings and the latest successful deployment; a workflow file alone does not prove the live source. |
| Google guidance on AI answer platforms | [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) · [Optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Both read 2026-11-20. The guidance is versioned and has changed in 2025 and 2026; re-read it on every verification pass before acting on it. |

## Known omissions

No externally verified redirect target, Associates account state, Search Console measurement, product price or availability, hands-on product test, campaign result, conversion, commission or revenue is included. This summary is prepared for a human reviewer and is not a substitute for the current Associates Agreement, applicable law, or professional legal advice. The live governance pages carry the detail: [method](method.html), [flagged items](flagged.html), [open questions](questions.html), [suggestions](suggestions.html), [decisions](decisions.html), [measurement](measurement.html) and [compliance](compliance.html).
