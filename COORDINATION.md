# COORDINATION — shared task board

This file is the coordination point for any session working in this repository.
Read it before starting work. Claim a task by writing your session ID and file
scope here, then commit and push that claim immediately. Never start a task
another session has claimed. Record sources, verification performed and any
irregularities when a task is finished, and mark it done.

---

## Session model note (recorded 2026-11-19)

The Arena platform pins this session to the single working branch
`arena/cd3cddd6-prod2` (branched from `c6dc49a` on `main`); it cannot create or
push the per-task `session-<id>/<task>` branches the coordination protocol
describes. All tasks are therefore consolidated on this one branch by one
session, with non-overlapping file scopes per task recorded below. If other
sessions join, they must re-claim free tasks here and follow the branch
constraint that applies to them, or log a handoff request in the log section.

## Session ID

`arena/cd3cddd6-prod2`

## Carried state (imported verbatim from kanlerxz87-cyber/Zone4)

Zone4 is the predecessor repository. Its registers were fetched read-only via
the GitHub API on 2026-11-19 and archived under `data/imported/zone4/`
(unmodified, with provenance README). Prod2's canonical registers carry the
verified records forward and cite the archive. Nothing in the archive was
re-derived or edited; anything Prod2 re-states is marked with the date and
record it came from.

## Task board

| Task | Scope (files) | Status | Owner session | Notes |
|---|---|---|---|---|
| T1 Governance & docs | `COORDINATION.md`, `README.md`, `ENGINE.md`, `DESIGN_PROMPT.md`, `VOICE.md`, `.gitignore` | done | arena/cd3cddd6-prod2 | Board created and claimed before any other work; docs finished with the build |
| T2 Data registers | `data/*.json` (canonical), `data/imported/zone4/**` (archive) | done | arena/cd3cddd6-prod2 | Products, intent links, associates, sources, flags, decisions, suggestions, open questions, guides, calendar, events, ledger |
| T3 Site generator & checks | `build.py`, `check.py`, `assets/**`, `collector/**`, `.github/workflows/**` | done | arena/cd3cddd6-prod2 | Static generator, 30 self-checks, CI workflow, self-hosted collector reference |
| T4 Editorial content | `content/**`, guides + category/pillar copy in `data/` | done | arena/cd3cddd6-prod2 | Eight question-shaped guides, four category pages, front page, comparison page |
| T5 Dashboard & review pages | pages under `data/`, `review/`, `suggestions.html`, `open-questions.html`, `executive-summary.html` | done | arena/cd3cddd6-prod2 | Rendered from the T2 registers by T3 |
| T6 Integration & publish | branch `arena/cd3cddd6-prod2`, PR to `main`, GitHub Pages | done | arena/cd3cddd6-prod2 | See log entries below for PR link, merge result and deploy status |

No task is free to claim while this row shows `in progress` for the owning
session. Check the log for freshness; a claim older than 60 minutes with no
commit may be taken over with a logged handoff.

## Verification performed (T2/T4)

- Product facts for P1–P3 (ASINs B0CDY277D3, B09B7SB46R, B08DKYBTPH) are carried
  from the Zone4 register, which reads them from the official Amazon listing
  pages; the archive keeps the dated session records
  (`data/imported/zone4/verification-session-*.json` in Zone4, listed in
  `data/imported/zone4/README.md`). **This environment cannot reach amazon.com**
  (egress allowlist), so no value was re-derived here; every carried value keeps
  its original citation and the register states the last-read date. This is
  recorded as flag FLG-05 on the site's Flagged for Review page, with the
  official listing URLs supplied for manual re-check.
- P4–P5 remain held (provisional intended ASINs B0DHZTCNR5 / B0DZFD6R9Z, meat
  thermometers, out of the air-fryer scope): no product page, no outbound link,
  no published fact. Carried under FLG-06.
- The Associates tracking ID `shopnow047c-20` is owner-supplied input recorded
  verbatim; its active/registered status can only be confirmed inside
  Associates Central (flag FLG-04, owner action).
- Published outbound Special Links for P1–P3 match the carried product-intent
  record (`?tag=shopnow047c-20`, destination ASIN observed 2026-11-17);
  attribution remains unverified until the one-link-per-product test in the
  enrolled Associates workflow passes (flag FLG-07, owner action).
- Policy/legal sources (Amazon Associates Operating Agreement, Program
  Policies, FTC guidance, Google Search Central) are cited link-only in
  `data/sources.json`; no wording is quoted as verified in this environment
  (flag FLG-05 lists them for manual review).
- Everything produced in this session is checked by `check.py` (30 checks) in
  CI on every push.

## Irregularities observed

1. The five supplied short links use path codes nine characters long
   (`B04G1MEwY` etc.); the intended ASINs are ten characters. Zone4 resolved
   this: the codes are short-link path codes, not ASINs. Recorded, not judged
   valid or invalid (Zone3 FLG-003 unresolved).
2. P4/P5 listings are meat thermometers, outside the air-fryer scope of the
   brief (Zone4 F-56). They are registered and held, not published.
3. No authorised first-party performance report exists, so the campaign
   ledger ships empty and no conversion score, traffic figure or revenue
   forecast appears anywhere on the site.

## Log

- 2026-11-19 — arena/cd3cddd6-prod2 created the board and claimed T1–T6 before
  starting any other work.
- 2026-11-19 — arena/cd3cddd6-prod2 imported the Zone4 registers read-only
  (archive under `data/imported/zone4/`), wrote the canonical registers,
  generator, checks, collector, content and pages; `python3 build.py` and
  `python3 check.py` pass (30/30) locally.
- 2026-11-19 — arena/cd3cddd6-prod2 opened PR to `main`, merged it, confirmed
  the Pages deployment via the GitHub API, and recorded the results in the
  session log on the branch after the merge. PR: see `PULL_REQUEST.md` and the
  GitHub repository's merged PR list (PR #1, merged 2026-11-19). Pages deploy
  run: GitHub Actions "Build checks and deploy site" on `main` — status
  confirmed via `gh api repos/wingbangboozle1-lang/Prod2/pages/builds/latest`.
  Live URL: https://wingbangboozle1-lang.github.io/Prod2/
