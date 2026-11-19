# Prod2 · Counter Notes

A static, editorial-style Amazon Associates publication for practical kitchen-appliance decision guides. It covers five supplied Amazon products (air fryers and meat thermometers), each shown with its listing source, the ASIN its link resolves to, and what is still unverified.

Brand: "Counter Notes" (adopted from PR #1; owner to confirm, see Flagged FR-12).

## Layout

- `data/products.json`: the product register. Supplied link, observed redirect ASIN and intended ASIN (unverified) are separate fields. Also holds the flags with their sources.
- `scripts/build_site.py`: generates every page in `docs/` from the register and the four guides in `archive/`. Standard library only.
- `scripts/verify_site.py`: the verification gate (disclosure, sponsored links, tracking tag, links and anchors, source link on every data row, unverified cells, banned promotional words, sitemap, feed).
- `scripts/assets/`: stylesheet and the outbound-click counter (`tracker.js`).
- `docs/`: the generated site, published by GitHub Pages. Do not edit by hand; change the source and rebuild.
- `archive/counter-notes-v1/`: the root-level site published by PR #1, kept unchanged for traceability. Not published.
- `COORDINATION.md`: shared task board, log and handoffs.
- `.github/workflows/verify.yml`: runs the build, the gate, and a check that the committed `docs/` matches a rebuild, on every push and pull request.
- `.github/workflows/pages.yml`: rebuilds, verifies, and deploys `docs/` to GitHub Pages on pushes to `main`.

## Rebuild and verify

```sh
python3 scripts/build_site.py
python3 scripts/verify_site.py
```

## Evidence and affiliate-link boundary

The five `https://link.amazon/...` URLs were resolved on 2026-11-19. Each one redirects to an Amazon product page. The observed ASIN is recorded in its own field. The site does not treat the short-link token as an ASIN; the tokens are 9 characters, not the 10-character ASIN format (FR-01).

Intended products are not confirmed (FR-02). Special Link validation has not been done. It needs the owner's Associates account. Until it is done, product buttons use the standard tagged format `https://www.amazon.com/dp/ASIN?tag=shopnow047c-20` and are marked `rel="sponsored"` (FR-03, FR-04).

No price, rating, commission rate, popularity, trend, conversion or revenue figure is published. Prices and ratings change, and Creators API access is not in place (FR-05, FR-06). Spec values are quoted from listing titles and marked "as listed".

Before promoting a product, confirm the intended ASIN and official listing URL, record the source and confirmation date, then test one enrolled Associates Special Link per product and confirm the destination and tracking report. Keep the disclosure visible.

## Measurement boundary

The site has no server. The self-hosted analytics endpoint cannot run on GitHub Pages (FR-09). The page carries one client-side event, `outbound_click`, which pushes to `window.dataLayer` and sends nothing unless an endpoint is set. The brief names five events, but their definitions were not supplied, so only one is built. The campaign ledger is empty by design (`docs/ledger.html`).

## Disclosure

As an Amazon Associate I earn from qualifying purchases. This site is not endorsed by or affiliated with Amazon. The wording is taken from Section 5 of the Associates Operating Agreement.

## GitHub Pages

Pages publishes the generated `docs/` folder through the `pages.yml` workflow (Pages source: GitHub Actions). Canonical URLs, the sitemap, the feed and robots.txt use `https://wingbangboozle1-lang.github.io/Prod2/`. If the site moves to a custom domain, update `BASE` in `scripts/build_site.py` and rebuild.

## Official references for manual review

- [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement)
- [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies)
- [FTC Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) (dated November 2019)
- [FTC endorsements and reviews guidance](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews)
- [Google Search Central: helpful, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Central: qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
- [GitHub Docs: configuring a publishing source for GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
