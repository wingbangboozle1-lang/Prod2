# Optional self-hosted event endpoint

The public GitHub Pages site remains static. It cannot run this API. This opt-in Node server is a separate, same-origin mode that serves the existing generated `docs/` site and the event endpoint together; use it only on an API-capable host/reverse proxy. It is not connected to Amazon conversion/order reporting.

## Run and test

Requires Node.js 20+ and Python 3 for the existing site verification gate. There are no npm runtime dependencies.

```sh
npm test
npm start
# open http://localhost:4173
```

The self-host server serves the checked-in `docs/` tree, opts in the existing `data-analytics-endpoint` click tracker, and injects a small first-party client for the other event types. The GitHub Pages build does not run this server or injected client, so the published Pages site has no app-level event collection unless the owner chooses and deploys an API-capable same-origin host.

## Event dictionary

| Event | Collected detail | What it does not mean |
|---|---|---|
| `page_view` | Path only; no query string or fragment | Not a unique visitor or eligible affiliate session |
| `outbound_click` | Product register ID only | Not an Amazon-attributed click or order |
| `guide_open` | One of the four published guide slugs | Not a search impression or ranking signal |
| `category_open` | `air-fryers` or `meat-thermometers` | Not purchase intent or product preference by a known person |
| `rss_feed_click` | Feed link click | Not a completed RSS subscription |

The service validates event names and dimensions, then keeps counts only. It does not persist raw events, timestamps, query terms, email addresses, cookie IDs, referrers, user agents, or IP addresses. Product clicks are not conversions. Conversion/order data remains an empty campaign ledger until the authorized Associates report is supplied and reconciled separately.

## Storage and privacy boundary

By default, aggregate counts are stored in ignored `var/events-aggregate.json`. The file has no per-event timestamp or identifier. Counts accumulate until the operator deletes the file; choose and document a retention/reset schedule before production deployment. Restrict filesystem access and secure the host, HTTPS, reverse proxy, and backups. The application does not log request metadata. However, hosting/network providers may process connection metadata. GitHub specifically documents that GitHub Pages logs visitor IP addresses for security; this remains true for the static Pages host, independently of this endpoint’s event store: [GitHub Pages data collection](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

The endpoint intentionally does not accept conversions, revenue, email signup, free-form search text, or arbitrary dimensions. Do not add those without an authorized data source, privacy/retention review, and explicit consent design where required.

## Deployment limits

- This server must be hosted on Node or another API-capable same-origin runtime. A static GitHub Pages deployment cannot execute it.
- No hosting account, API-capable provider, Search Console property, or Amazon Associates account was available/verified in this task, so public production collection is not enabled.
- Do not infer affiliate attribution from the event counts. Use only authorized Amazon first-party reports for eligible sessions, clicks, orders, and commissions.
