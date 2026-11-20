# Optional self-hosted event endpoint

The GitHub Pages publication at `docs/` is static. It does **not** expose an analytics API, and
the deployed `data-endpoint` is intentionally empty. The five-event measurement contract is
documented in `data/p2/events.json`; the static site must not imply that events are being
received merely because its client can emit them.

For an operator who separately chooses to run the opt-in Node endpoint, `server.mjs` serves the
generated `docs/` publication and enables the same-origin `POST /api/events` endpoint. It accepts
exactly the following five local, aggregate events:

- `page_view`: `path`
- `outbound_click`: `path`, allow-listed product `asin`
- `guide_read_75`: `path`
- `category_click`: `path`, allow-listed category `target`
- `feed_click`: `path`

Anything else is rejected with `400`: a sixth event name, a superseded event from the earlier
twelve-event family (`guide_open`, `category_open`, `rss_feed_click`, `chooser_completed`,
`article_half_read`, `disclosure_viewed`, `cta_click`, `product_click`, `filter_apply`,
`guide_read`), and the separate report-only campaign-ledger events (`impression`, `click`,
`session`, `order`, `refund`). A request whose page path is not a built publication page is
counted under `/unknown`; an outbound click whose ASIN is not in `data/p2/products.json` and a
category click whose target is not a published category are refused outright.

## What is stored

The endpoint stores aggregate counts only. The store is a single JSON file:

```json
{
  "page_view": {
    "2026-11-20": {"/index.html": 3}
  },
  "outbound_click": {
    "2026-11-20": {"B0CDY277D3": 1}
  }
}
```

That is daily counts per event and path, exactly as `data/p2/events.json` declares. It holds no
visitor identifier, no IP address, no user agent, no referrer, no cookie, no query string and no
per-event timestamp — the day bucket is a UTC date, not a moment. The server writes no request
log and deliberately logs no request metadata. Counts are not Amazon-reported sales or
attribution and cannot be used to claim orders, commissions, conversion or revenue.

The default local store is `var/events-aggregate.json` (the directory is git-ignored). Set
`EVENT_STORE` to choose another location and `PORT` to choose the listening port. The store
grows one bucket per day; archive or delete it under an explicitly reviewed retention policy, and
`npm run reset-events` clears the local one. Keep the store out of the public static site.

## Request handling

The endpoint accepts same-origin requests only when an `Origin` header is present, caps request
bodies at 2 KB, requires a JSON or plain-text content type, and serves only files inside the
generated `docs/` tree — the preserved legacy `site/` tree is not served.

## Running it

```sh
python3 tools/build.py   # generate docs/ first
npm start                # node server.mjs
```

The server binds to `0.0.0.0` on the chosen port. This repository's GitHub Pages workflow deploys
only static files and does not run this process, and Pages cannot host it. A separate durable,
secure host and any applicable privacy or legal review are required before collecting public
traffic. Never deploy this development endpoint as an implied replacement for Amazon's authorized
reports.

## Test

```sh
npm test   # builds docs/, runs the release gate and the legacy verifier, then the endpoint test
node --test tests/server.test.mjs   # the endpoint contract on its own
```

The endpoint test asserts that all five events are accepted and aggregated, that a superseded or
ledger event is refused, that an unknown ASIN is refused, that a cross-origin request is refused,
that the store carries only dated counts, and that the server serves `docs/` and nothing outside
it.
