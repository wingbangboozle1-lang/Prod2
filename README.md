# The Crisp Counter

A source-checked Amazon Associates publication for countertop air fryers,
built in the `Prod2` repository. Every published product fact was read from an
official Amazon listing page by the predecessor register (archived verbatim at
`data/imported/zone4/`), and the site ships its receipts: a product register,
a source register, an open flag list, a suggestions queue and a decision log —
all reachable from the footer of every page.

**Live site:** https://wingbangboozle1-lang.github.io/Prod2/

## What ships

- A storefront front page (shop, guides, method — dashboards live in the footer)
- Three shop category pages covering the three verified products
- Eight question-shaped buying guides written to `VOICE.md`
- A comparison page with a three-question chooser and the verified fact table
- The counter-space method (capacity per centimetre of counter depth)
- Dashboard & governance pages: product register, source register, campaign
  ledger (empty by rule), five-event privacy model, flagged-for-review page,
  decision log, methodology, suggestions, open questions, executive summary
- RSS feed, sitemap, robots.txt, unique titles/descriptions, JSON-LD,
  `rel="sponsored"` outbound links, above-the-fold disclosure on every page

## Compliance posture

- Tracking ID `shopnow047c-20` (owner-supplied; active status unconfirmed)
- Outbound Special Links: final destination + tag, `rel="sponsored"`, no
  shorteners; held products (P4/P5) are never published
- Disclosure above the fold on every page; Amazon IP notice in every footer
- No prices, ratings, review counts or popularity claims anywhere
- Campaign ledger stays empty until an authorised first-party report exists;
  no conversion scores or revenue forecasts are published

## Build & check

```bash
python3 build.py     # build the site into public/
python3 check.py     # run all 30 checks (exit non-zero on failure)
```

Standard library only. CI runs both on every push and deploys `public/` to
GitHub Pages on `main`. `ENGINE.md` documents the pipeline; `DESIGN_PROMPT.md`
and `VOICE.md` are the design and editorial briefs; `COORDINATION.md` is the
multi-session task board.

## Repository layout

```
build.py  check.py           generator + check suite
data/                        canonical registers (products, sources, flags, …)
data/imported/zone4/         predecessor registers, verbatim archive
content/guides/*.html        article bodies
assets/                      css, js, og-image, favicon
collector/                   self-hosted analytics endpoint (reference)
.github/workflows/site.yml   CI: checks + Pages deploy
```
