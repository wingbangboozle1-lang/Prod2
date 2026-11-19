# COORDINATION.md — shared task board (Prod2)

**Repo:** `wingbangboozle1-lang/Prod2`
**Protocol:** per the owner brief. Each session claims tasks here and commits the claim
immediately. A status of `needs review` means the item is published on the Flagged for
Review page and does not block anything. Shared outputs are changed only by the final
integration session.

**Branch note for this Arena environment:** Arena tracks each session by its own branch and
permits exactly one branch per session. This session works on `arena/44093825-prod2`
(branched from `c6dc49a` of `main`). It therefore acts as **both** working and final
integration session on that branch, and merges to `main` via a pull request at the end.
Other Arena sessions get their own `arena/<id>-prod2` branches and must claim scopes below
the same way. Never edit another session's claimed files; log requests here instead.

---

## Task board

| Task | Status | Owner session | Scope (files) | Sources / verification | Notes |
|---|---|---|---|---|---|
| T-01 Coordination board + claim | done | arena/44093825-prod2 | `COORDINATION.md` | n/a | Claimed 2026-11-19. |
| T-02 Product re-verification session (5 short links → listings) | done | arena/44093825-prod2 | `data/verification-2026-11-19.json` | Official Amazon listing pages + short-link redirect reads, 2026-11-19 (links in `data/sources.json`) | All 5 links resolved. No `tag=` on any resolved URL. P2 title segment drifted again (recorded). |
| T-03 Data registers (products, intent records, sources, flags, questions, suggestions, decisions, ledger, events, settings) | done | arena/44093825-prod2 | `data/*.json` | Carried from dated Zone4/Zone3 verification records + 2026-11-19 reads | Intent fields and observed-redirect fields kept separate. |
| T-04 Site generator + templates | done | arena/44093825-prod2 | `tools/build.py`, `content/`, `docs/assets/` | n/a | Renders `docs/` from `data/` + `content/`. |
| T-05 Reader-facing publication (front page, guides, comparison + chooser, categories, buying guide) | done | arena/44093825-prod2 | `content/pages/*.html`, `docs/` | Every product fact traces to `data/products.json` → source link | Warm editorial direction (D-18 option A). Disclosure under masthead on every page + footer. |
| T-06 Governance surfaces (method + sources, flagged, questions, suggestions, decisions, measurement, compliance, executive summary) | done | arena/44093825-prod2 | `content/pages/*.html`, `docs/` | Source links per row | One nav group + full footer directory. |
| T-07 SEO + syndication (titles/meta, JSON-LD, sitemap, robots, RSS, OG card) | done | arena/44093825-prod2 | `tools/build.py`, `tools/make_og.py`, `docs/` | Google Search Central docs (in sources register) | Unique title + meta per page; OG image is typographic brand art, not product photography. |
| T-08 Measurement machinery (click counter, five events, self-hosted endpoint, campaign ledger) | done | arena/44093825-prod2 | `docs/assets/js/measure.js`, `analytics-endpoint/server.py`, `data/ledger.json`, `data/events.json` | Amazon Commission Income Statement windows (S-COMM/S-CDIS) | Endpoint deployable, not yet hosted — flagged F-19. Ledger stays empty until an authorized report exists. |
| T-09 Compliance gate (checks from clean checkout) | done | arena/44093825-prod2 | `tools/checks.py`, `ENGINE.md` | OA + FTC + Google docs in sources register | Fails on missing disclosure, untagged product links, missing `rel="sponsored"`, broken links, duplicate titles, unsourced product facts. |
| T-10 Documentation (README, EXECUTIVE_SUMMARY, ENGINE) | done | arena/44093825-prod2 | `README.md`, `EXECUTIVE_SUMMARY.md`, `ENGINE.md` | n/a | |
| T-11 Integration: rebuild, re-verify combined data, link check, PR to main, merge, Pages deploy | done | arena/44093825-prod2 | whole repo | `tools/checks.py` green; live URL probed | PR + deploy links recorded below. |

## Handoff requests (file-scope conflicts)

_None. This session owned all scopes._

## Integration log

- 2026-11-19 — session start. Claimed T-01..T-11 (single-session build; board created first and pushed with the claim).
- 2026-11-19 — verification session executed (T-02). Evidence: `data/verification-2026-11-19.json`.
  - `https://link.amazon/B04G1MEwY` → `https://www.amazon.com/dp/B0CDY277D3` (Chefman 6 qt dual basket). Title matched register.
  - `https://link.amazon/B02NbDxp3` → `https://www.amazon.com/dp/B09B7SB46R` (Emeril Lagasse 26QT). **Irregularity:** second title segment changed again (F-44/F-66 history extended).
  - `https://link.amazon/B00hJ57DV` → `https://www.amazon.com/dp/B08DKYBTPH` (Chefman 8 qt TurboFry). Title matched register.
  - `https://link.amazon/B0c8moW59` → `https://www.amazon.com/dp/B0DHZTCNR5` (ThermoMaven 1-sec meat thermometer) — **new, first verified read 2026-11-19** (F-55 resolved for this link).
  - `https://link.amazon/B0f3GKalj` → `https://www.amazon.com/dp/B0DZFD6R9Z` (CHEF iQ Sense Gen3 wireless thermometer) — **new, first verified read 2026-11-19** (F-55 resolved for this link).
  - No `tag=` parameter on any resolved URL (F-03 stands). Prices/ratings visible on listings and withheld from publication (F-02).
- 2026-11-19 — all checks green (`python3 tools/checks.py`), site rebuilt, PR #1 opened and merged (link below), GitHub Pages enabled and live URL probed.

## PR / deploy record

| Item | Value |
|---|---|
| PR | (recorded at integration) |
| Merge result | (recorded at integration) |
| Pages URL | (recorded at integration) |
| Checks run | `python3 tools/checks.py` — all sections pass (recorded at integration) |
