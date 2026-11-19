# Imported register archive — kanlerxz87-cyber/Zone4

These files are the predecessor repository's registers, fetched read-only from
the public GitHub API (`api.github.com/repos/kanlerxz87-cyber/Zone4/contents/...`)
on **2026-11-19** and stored verbatim. They are an archive, not a live input:
the site generator reads the canonical registers in `data/*.json`, which cite
this archive where a value is carried forward.

| File | What it is |
|---|---|
| `z4-products.json` | Verified product records for P1–P3 as read from the official Amazon listing pages, with dated re-verification entries and session records |
| `z4-intent.json` | Product-intent confirmation record for all five submitted links (intended ASIN, official listing URL, confirmation date and source, observed redirect kept in its own field) |
| `z4-associates.json` | The owner-supplied tracking ID `shopnow047c-20` and the tagged Special Link record |
| `z4-sources.json` | The source register (S-IDs) with official URLs |
| `z4-flags.json` | The 67-item flag register (F-IDs) with statuses |
| `z4-decisions.json` | 45 decision rows (D-IDs) with recorded statuses |
| `z4-suggestions.json` | 46 suggestion rows (S-IDs) |
| `z4-questions.json` | 50 question rows (Q-IDs) |
| `z4-guides.json` | The published guide register |
| `z4-ledger.json` | The empty campaign ledger and five-event definitions |
| `z4-publishing.json` | Publishing cadence |
| `z4-content.json` | Disclosure wording, executive summary and the Amazon IP notice (Section 2(k) conservative reading) |
| `z4-marketing.json` | Marketing content kit with per-fact source rows |
| `z4-requirements.json` | The requirements register |

**What this session did and did not do:** this environment cannot reach
amazon.com or the Associates pages (egress allowlist), so no carried value was
re-derived here. Anything Prod2 re-states cites the official page it came from
plus the dated Zone4 record; unverified or owner-action items are flagged on
the site's Flagged for Review page with their official links.
