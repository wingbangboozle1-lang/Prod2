# Analytics endpoint contract

`assets/analytics.js` posts privacy-preserving events to an endpoint whose URL
is configured in one place (see `ENDPOINT` at the top of that file). The
endpoint is **not provisioned yet** — until it is, events stay in the browser
and are never transmitted.

## Request

```
POST /e
Content-Type: application/json

{"events": [ {"name": "...", "session_id": "...", "path": "...", "ts": 1773900000, ...} ]}
```

- Batches of 1–20 events, sent with `navigator.sendBeacon` when available.
- `session_id` is a random 16-hex string created per browser tab
  (`sessionStorage`); it is not derived from any personal data.
- No cookies, no IP logging requested, no user-agent parsing requested.

## Event names (exactly five — see data/events.json)

| name | emitted when |
|---|---|
| `page_view` | page finished loading in a foreground tab |
| `product_impression` | a product card/row ≥50% visible for 1 s |
| `outbound_click` | a `rel=sponsored` product link was clicked (ASIN only, no query strings) |
| `guide_read` | an article was scrolled to ≥75%, once per session per article |
| `chooser_result` | the three-question chooser on comparison.html produced a verdict |

## Server requirements

- Accept `POST /e`, respond `204`, ignore unknown fields.
- Do not store IP addresses or user agents.
- Aggregate counts by `name` (+ `asin` for `outbound_click`); expose a daily
  rollup that can be appended to `data/campaign-ledger.csv` **only** from
  authorized first-party reports (timestamp, source, channel, eligible
  sessions, outbound clicks, reported orders, provenance).
- Suggested minimal implementations: a Cloudflare Worker writing to KV, or a
  20-line Flask app behind your own domain. Both are listed as options on
  suggestions.html (S-04).
