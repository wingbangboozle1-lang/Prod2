# Counter Notes

A static, editorial-style Amazon Associates publication starter for practical kitchen-appliance decision guides. The site prioritizes reader questions and makes product uncertainty, measurement gaps, and review gates visible.

## Preview locally

Open `index.html` in a browser, or run a static server from the repository root, for example:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`. No build dependencies are required.

## Pages

- `index.html` — editorial front page and category entry points.
- `guides/` — four question-led guides. They are decision frameworks, not hands-on product reviews or product claims.
- `evidence.html` — user-submitted product-link register, separate intent/redirect fields, measurement plan, and flagged items.
- `suggestions.html` — executive summary, decision sequence, options for review, and known/unknown questions with discovery steps.
- `feed.xml`, `sitemap.xml`, `robots.txt` — publication discovery files.

## Evidence and affiliate-link boundary

The five `https://link.amazon/...` URLs provided to the project have not been resolved or tested here. Their intended products, ASINs, official listing URLs, current destinations, Special Link status, and tracking reports remain unverified. The submitted strings are not treated as ASINs. No product-specific claims, ratings, prices, trend claims, commissions, or performance forecasts are made. Each product-intent row intentionally leaves unconfirmed values blank, and observed redirects are stored separately from intended product data.

Before promoting a product, verify intended ASIN and official listing URL, record source and confirmation date, then test one enrolled Associates Special Link per product and confirm destination and tracking report. Keep the disclosure visible and qualify affiliate links with `rel="sponsored"`. Review current official Amazon Associates and FTC guidance; linked references are in the site footer and review pages.

## Measurement boundary

No analytics endpoint, Amazon report importer, or Search Console connection is implemented. The campaign ledger is empty. The five event names on `evidence.html` are a proposal only; no browser events are currently sent or stored. A privacy-reviewed server endpoint and data-retention/access policy are needed before collection. Do not scrape or automate product data without confirming current authorized access and policy.

## GitHub Pages

`.github/workflows/pages.yml` publishes the static site artifact on pushes and manual workflow dispatch. It requires GitHub Pages to be enabled for the repository with GitHub Actions as the source and the workflow's Pages permissions available. Canonical URLs currently target `https://wingbangboozle1-lang.github.io/Prod2/`; verify the actual Pages URL and update canonical URLs, sitemap, RSS, and robots URL if the repository uses a custom domain or different Pages origin. The workflow run and Pages deployment must be checked in GitHub before calling the site live.

## Official references for manual review

- [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement)
- [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies)
- [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
- [FTC endorsements and reviews guidance](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews)
- [Google Search Central: helpful, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Central: qualifying outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
