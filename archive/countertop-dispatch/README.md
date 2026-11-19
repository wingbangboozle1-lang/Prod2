# archive/countertop-dispatch — preserved build from PR #16 (arena/30a7028a-prod2)

This directory is a verbatim snapshot of the tree at commit
`d77bb9f95b9d6db3e54dd74886bd7b9126ef2a19` — the "Countertop Dispatch" build,
a complete parallel implementation (28 HTML pages, its own registers at
`data/{products,product-intent,submitted-links,events}.json`, `data/campaign-ledger.csv`,
its own `tools/build_site.py` + `tools/check_site.py` gate, four question-shaped guides,
suggestions/flags/summary pages).

**Why it is archived and not deployed:** the standing one-site rule (INT-06, adopted at
the 2026-11-19 consolidation) keeps exactly one deployed publication so search engines
index one site. The canonical deployed publication is the Prod2 publication in `docs/`
(built by `tools/build.py`, gated by `tools/checks.py`, mirrored to the repo root for
legacy Pages serving).

**Nothing is discarded:**

- The snapshot here is complete and self-contained (it can be rebuilt/run from this
  directory; its README and COORDINATION board are included as published).
- The original branch `arena/30a7028a-prod2` remains on the remote with its full history
  (15 commits; PR #16 shows the complete diff).
- Its session record is preserved in `COORDINATION.md`.

Snapshot taken 2026-11-19 by session arena/9f84489c-prod2 under the handoff rule
(the claim was >60 minutes old with no commits and its stated merge plan never ran;
PR #16 was closed unmerged at 2026-11-19T21:51Z).
