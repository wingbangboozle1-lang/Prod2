# Self-hosted analytics collector

`app.py` is a dependency-free Python HTTP endpoint that receives the five
defined events (`data/events.json`) from the site's client-side recorder as
anonymous JSON lines. It exists because GitHub Pages cannot host a dynamic
endpoint — hosting it is the open decision behind flag FLG-08 / question Q-06
(see the site's *Suggestions* page, SG-02).

## Run it

```bash
python3 collector/app.py --port 8090
curl -s localhost:8090/health        # {"ok": true, "events": 0}
```

## Wire the site to it

Set the endpoint once, before `analytics.js` loads (e.g. in the page head):

```html
<script>window.CC_COLLECT_URL = "https://collector.example.com/collect";</script>
```

Event lines then arrive at `POST /collect`:

```json
{"event": "product_link_click", "ts": "2026-11-19T12:00:00Z", "path": "/Prod2/compare/index.html", "props": {"href": "https://www.amazon.com/dp/..."}}
```

## Privacy posture (matches data/events.json)

- No cookies, no fingerprinting, no cross-site identifiers.
- No IP logging: `log_message` is disabled; nothing about the request is stored.
- Anonymous event lines only, rotated after 90 days (`RETENTION_DAYS`).
- The click counter is a first-party measurement and is never treated as a
  reported order — orders enter the campaign ledger only from authorised
  Associates Central reports (decision D-10).

## Deployment notes

- Bind to `127.0.0.1` behind a reverse proxy with TLS, or a private network,
  in production; the default `0.0.0.0` is for quick tests and the sandbox preview.
- CORS is open (`*`) because the recorder sends no credentials; tighten it to
  the site origin if you prefer.
- Files written: `events.jsonl` next to the script (git-ignored).
