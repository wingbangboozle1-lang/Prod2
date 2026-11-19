# Prod2 — Kitchen notes & buying guides

A small Amazon-affiliate **publication** (not a dashboard): five checked kitchen
products — three air fryers and two meat thermometers — presented as question-led
buying guides with every figure sourced to the official listing it was read from.

**Live site:** https://wingbangboozle1-lang.github.io/Prod2/
**Tracking ID:** `shopnow047c-20` (owner-supplied; attribution pending — see F-57)
**Disclosure:** *As an Amazon Associate we earn from qualifying purchases.* — on every page.

## Repository layout

```
data/            source registers: products, intent records, sources, flags,
                 questions, suggestions, decisions, ledger, events, settings
content/pages/   page content fragments (hooks pull data tables in)
assets/          css / js / og-card.png (source; copied into docs/ at build)
tools/build.py   renders docs/ (static site served by GitHub Pages)
tools/checks.py  the publish gate (see ENGINE.md)
tools/make_og.py renders the social-preview card (typographic brand art)
analytics-endpoint/  privacy-preserving self-hosted event counter (deployable)
docs/            the published site (generated; committed; Pages source)
```

## Build & check (clean checkout, stdlib Python)

```bash
python3 tools/build.py && python3 tools/checks.py
```

## Review surfaces

- `EXECUTIVE_SUMMARY.md` — the one-page overview for a reviewer.
- Site pages: **Flagged for review**, **Open questions**, **Suggestion queue** (choose a
  path before anything is implemented), **Decision log**, **Method & sources**,
  **Measurement**, **Compliance** — all under "The work behind it" in the nav/footer.
- `COORDINATION.md` — the shared task board (multi-session protocol) and the PR/deploy record.

## What this site never publishes

Prices, star ratings, product-level commission rates, revenue forecasts — and any
claim without a dated official source. See `flagged.html` for why.
