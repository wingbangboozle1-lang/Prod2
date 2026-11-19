# Archived: "The Counter Edit" parallel build (session sess-prod2-a1)

This is a complete parallel site build created from the pre-merge base `c6dc49a` and archived
unchanged during the integration pass (INT-02, 2026-11-19), because the canonical site is the
generated `docs/` tree ("Counter Notes") — see COORDINATION.md.

Kept for traceability, mirroring the repo's own `archive/counter-notes-v1/` convention:

- `scripts/` (helpers.py, content_reader.py, content_docs.py, build.py, check.py) — the content
  modules, design tokens, product register, decision/flag/suggestion datasets, and the checker
  that asserted titles, sponsored links, disclosure, link integrity and cross-references.
- `site/` — the generated output (19 pages + feeds), with its illustration set.

Its unique value was ported into the canonical site (INT-03): illustrations and og-image,
guide heroes, og:image/Twitter cards, the three-question chooser, and the five-event tracker.
Paths inside `build.py` no longer resolve from this location (it assumed the repo root); run
nothing here. The four guide texts here were superseded by the canonical guides to avoid
duplicate-topic pages.
