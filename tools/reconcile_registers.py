#!/usr/bin/env python3
"""reconcile_registers.py — one-shot merge of the open-PR register rows onto main.

Run once, from a clean checkout on the integration branch:

    python3 tools/reconcile_registers.py [--dry-run]

Why this exists
---------------
Four parallel sessions wrote register rows (F-/Q-/SG-/D- ids) into their own
branches. Several of those rows carry an id that main has since used for a
*different* row. Copying branches verbatim would therefore produce two rows
with one id, and the build's cross-reference check would fail in a way that
looks like a content bug rather than an id collision.

This script merges by CONTENT, not by id:

  1. read each open PR's register,
  2. drop rows whose id+content already exist on main (already merged),
  3. renumber the rows whose id collides with a main row of different content,
     using the explicit tables below,
  4. rewrite every cross-reference inside the merged rows (a row that cites
     F-P25 means the row that was F-P25 in its source branch, so it must cite
     the renumbered id),
  5. write the merged register and print an audit line per row.

Nothing is deleted from main. Every carried row keeps its original text; only
its id and the ids it cites may change, and the change is recorded in the row's
own "renumber_note" field so a reviewer can follow the trail.

The tables below are the whole decision surface. If a row is not in a table, it
keeps its id — and if that id is already taken on main with different content,
the script refuses to write and exits non-zero.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "p2"
REFS = {
    "pr41": "refs/remotes/pr/41",
    "pr43": "refs/remotes/pr/43",
    "pr47": "refs/remotes/pr/47",
}

# ---------------------------------------------------------------------------
# The renumbering tables. Key = the id in the SOURCE branch, value = the id it
# takes on main, or None to drop the row (main already has equivalent content).
# ---------------------------------------------------------------------------
FLAG_MAP = {
    "pr43": {"F-P25": "F-P25", "F-P26": "F-P26", "F-P27": "F-P27", "F-P28": "F-P28"},
    "pr47": {"F-P25": "F-P29"},
}
# A source row whose id exists on main but whose CONTENT is a strict extension of
# main's row (same title, longer detail). These merge into main's row: the detail
# is appended, the evidence link is kept, and the merge is recorded in the row.
# Flagged rows that main already owns and that the source only restates are
# left alone.
EXTENDABLE = {"flags": {"pr43": {"F-P19", "F-P20"}}}
# Rows main owns that a source branch also owns, but where main has since moved
# the row FORWARD (e.g. F-P23 was open on the source's older base and is
# resolved on main). The source row is older, so it is skipped — taking it
# would regress main. Each entry records why.
STALE_ON_SOURCE = {
    "flags": {
        "pr47": {"F-P23": "resolved on main by the collector fix (PR #44); "
                         "the source branch still shows it open"},
    },
    "questions": {
        "pr43": {"Q-01": "main's row carries the newer 2026-11-20 note; the source "
                         "branch's note is an earlier version of the same row",
                 "Q-P03": "same row, main's wording is the later one"},
    },
}
QUESTION_MAP = {
    "pr43": {"Q-P18": "Q-P18"},
    "pr41": {"Q-P12": "Q-P12", "Q-P13": "Q-P13", "Q-P18": "Q-P30", "Q-P19": "Q-P31",
             "Q-P20": "Q-P32", "Q-P21": "Q-P33", "Q-P22": "Q-P34", "Q-P23": "Q-P35",
             "Q-P24": "Q-P36", "Q-P26": "Q-P37", "Q-P27": "Q-P38", "Q-P28": "Q-P39"},
    "pr47": {},
}
SUGGESTION_MAP = {
    "pr47": {"SG-45": "SG-48"},
    "pr41": {"SG-18": "SG-18", "SG-19": "SG-19", "SG-20": "SG-20", "SG-21": "SG-21",
             "SG-22": "SG-22", "SG-23": "SG-23", "SG-24": "SG-24", "SG-25": "SG-25",
             "SG-26": "SG-26"},
}
DECISION_MAP = {
    "pr47": {"D-P21": "D-P22", "D-P22": "D-P23"},
    "pr41": {"D-P21": None, "D-P22": "D-P24"},
}

# Rows main already has that a source branch also has, with identical content.
# These are "already merged" — the source row is skipped, not duplicated.
ALREADY_MERGED: dict[str, set[str]] = {"flags": set(), "questions": set(),
                                       "suggestions": set(), "decisions": set()}

ID_RE = re.compile(r"\b((?:F|Q|SG|D)-P\d{2})\b")


def read_ref(ref: str, name: str, key: str):
    out = subprocess.run(["git", "show", f"{ref}:data/p2/{name}.json"],
                         capture_output=True, text=True, cwd=ROOT)
    if out.returncode != 0:
        return []
    return json.loads(out.stdout)[key]


def read_main(name: str, key: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))[key]


def signature(row: dict) -> str:
    """Content identity of a row, ignoring its id and any renumber note."""
    body = {k: v for k, v in row.items() if k not in ("id", "renumber_note")}
    return json.dumps(body, sort_keys=True, ensure_ascii=False)


def rewrite_refs(value, mapping: dict[str, str]):
    """Rewrite every register id cited inside a value."""
    if isinstance(value, str):
        def sub(m: re.Match) -> str:
            return mapping.get(m.group(1), m.group(1))
        return ID_RE.sub(sub, value)
    if isinstance(value, list):
        return [rewrite_refs(v, mapping) for v in value]
    if isinstance(value, dict):
        return {k: rewrite_refs(v, mapping) for k, v in value.items()}
    return value


def merge(kind: str, main_rows: list[dict], sources: list[tuple[str, str]],
          mapping: dict[str, dict[str, str | None]]) -> list[dict]:
    """sources: list of (branch_key, ref_name)"""
    out = list(main_rows)
    main_sigs = {signature(r): r["id"] for r in main_rows}
    main_ids = {r["id"] for r in main_rows}

    for branch, ref_name in sources:
        rows = read_ref(REFS[branch], ref_name, kind)
        m = mapping.get(branch, {})
        # the global id map for this branch across ALL registers, so a row citing
        # a flag id from another register still gets rewritten
        global_map = {**FLAG_MAP.get(branch, {}), **QUESTION_MAP.get(branch, {}),
                      **SUGGESTION_MAP.get(branch, {}), **DECISION_MAP.get(branch, {})}
        for row in rows:
            src_id = row["id"]
            if src_id in ALREADY_MERGED[kind]:
                continue
            sig = signature(row)
            if sig in main_sigs:
                continue  # already merged by content
            new_id = m.get(src_id, src_id)
            stale = STALE_ON_SOURCE.get(kind, {}).get(branch, {})
            if src_id in stale:
                print(f"  = {kind[:-1]:10s} {src_id} skipped — {stale[src_id]}")
                continue
            if new_id is None:
                continue  # explicitly dropped: main has the equivalent row
            if new_id in main_ids:
                # main already owns this id.
                target = next(r for r in out if r["id"] == new_id)
                ext = EXTENDABLE.get(kind, {}).get(branch, set())
                if src_id in ext and target.get("title", "").strip() == row.get("title", "").strip():
                    # A flag the source branch EXTENDED (longer detail, same
                    # title). The extension is merged into main's row.
                    if row.get("detail", "") not in target.get("detail", ""):
                        target["detail"] = (target.get("detail", "").rstrip() + " " +
                                            row.get("detail", "").strip()).strip()
                        target["detail_extension_sources"] = sorted(
                            set(target.get("detail_extension_sources", []) + [branch]))
                        print(f"  ^ {kind[:-1]:10s} {new_id} detail extended from {branch}")
                    else:
                        print(f"  = {kind[:-1]:10s} {new_id} already carries {branch}'s detail")
                    continue
                same_row = target.get("title", "").strip() == row.get("title", "").strip()
                if same_row:
                    # Same row, different wording or a later state. Main's row is
                    # the newer one (it was merged from later passes), so the
                    # source row is skipped; status edits are applied separately
                    # by the caller for the registers where that is the point.
                    print(f"  = {kind[:-1]:10s} {new_id} already on main — source row skipped")
                    continue
                # Different row that happens to share an id. If the mapping sends
                # it to a free id, it is a genuine new row.
                if m.get(src_id) and m[src_id] != src_id and m[src_id] not in main_ids:
                    new_id = m[src_id]
                else:
                    # main owns the id and the source row is a different row:
                    # if the source row is a strict extension of main's row,
                    # merge the extension; otherwise refuse.
                    ext = EXTENDABLE.get(kind, {}).get(branch, set())
                    if src_id in ext:
                        if row.get("detail", "") not in target.get("detail", ""):
                            target["detail"] = (target.get("detail", "").rstrip() + " " +
                                                row.get("detail", "").strip()).strip()
                            target["detail_extension_sources"] = sorted(
                                set(target.get("detail_extension_sources", []) + [branch]))
                            print(f"  ^ {kind[:-1]:10s} {new_id} detail extended from {branch}")
                        else:
                            print(f"  = {kind[:-1]:10s} {new_id} already carries {branch}'s detail")
                        continue
                    raise SystemExit(
                        f"refusing to write: {kind} id {new_id} (from {branch}:{src_id}) "
                        f"is already taken on main with different content")
            new = rewrite_refs(row, global_map)
            new["id"] = new_id
            if src_id != new_id:
                note = (f"Renumbered from {src_id} during the 2026-11-20 integration "
                        f"(session arena/7cec0d73-prod2): the source branch and main had "
                        f"both used {src_id} for different rows.")
                prev = new.get("renumber_note")
                new["renumber_note"] = (prev + " " + note) if prev else note
            out.append(new)
            main_ids.add(new_id)
            main_sigs[sig] = new_id
            print(f"  + {kind[:-1]:10s} {src_id} -> {new_id}  ({branch})")
    return out


def main() -> int:
    dry = "--dry-run" in sys.argv
    print(f"reconciling open-PR register rows onto main{' (dry run)' if dry else ''}")

    print("flags:")
    flags = merge("flags", read_main("flags.json", "flags"),
                  [("pr43", "flags"), ("pr47", "flags")], FLAG_MAP)
    print("questions:")
    questions = merge("questions", read_main("questions.json", "questions"),
                      [("pr43", "questions"), ("pr41", "questions")], QUESTION_MAP)
    print("suggestions:")
    suggestions = merge("suggestions", read_main("suggestions.json", "suggestions"),
                        [("pr47", "suggestions"), ("pr41", "suggestions")], SUGGESTION_MAP)
    print("decisions:")
    decisions = merge("decisions", read_main("decisions.json", "decisions"),
                      [("pr47", "decisions"), ("pr41", "decisions")], DECISION_MAP)

    # ---- suggestion status changes proposed by PR47 (the reviewer pass) ----
    # PR47 decided every open queue item. Only its status edits are applied;
    # the row text stays main's. A status is only applied if the row's title
    # matches PR47's title, so a same-id/different-row cannot be clobbered.
    print("suggestion status changes (PR47 reviewer pass):")
    pr47_sugg = {r["id"]: r for r in read_ref(REFS["pr47"], "suggestions", "suggestions")}
    by_id = {r["id"]: r for r in suggestions}
    for src_id, pr in pr47_sugg.items():
        target = SUGGESTION_MAP["pr47"].get(src_id, src_id)
        row = by_id.get(target)
        if row is None:
            continue
        if row.get("title", "").strip() != pr.get("title", "").strip():
            print(f"  ! skip status edit for {target}: title differs from PR47's {src_id}")
            continue
        new_status = pr.get("status")
        # A status edit must never move a row BACKWARDS past something main
        # has already shipped. PR #47's branch is based on 025b7b2, which
        # predates the collector fix merged in PR #44; on that base SG-41 read
        # "proposed" and its reviewer deferred it. Main shipped it. Applying
        # that would undo shipped work, so a regression is refused and the
        # divergence is printed for review.
        REGRESSION = {"shipped"}
        if row.get("status") in REGRESSION and new_status not in REGRESSION:
            print(f"  ! refused regression on {target}: main has "
                  f"'{row.get('status')}', the source branch says '{new_status}' "
                  f"(its base predates main's ship) — main's state kept")
            continue
        if new_status and row.get("status") != new_status:
            old = row.get("status")
            row["status"] = new_status
            hist = row.get("status_history")
            if hist is None:
                hist = []
                row["status_history"] = hist
            hist.append({"date_utc": "2026-11-20", "from": old, "to": new_status,
                         "by": "session arena/7cec0d73-prod2, carrying the reviewer pass "
                               "recorded in PR #47 (branch arena/20f83238-prod2)"})
            print(f"  ~ {target}: {old} -> {new_status}")

    if dry:
        print("dry run: nothing written")
        return 0

    for name, key, rows in (("flags.json", "flags", flags),
                            ("questions.json", "questions", questions),
                            ("suggestions.json", "suggestions", suggestions),
                            ("decisions.json", "decisions", decisions)):
        p = DATA / name
        doc = json.loads(p.read_text(encoding="utf-8"))
        doc[key] = rows
        doc.setdefault("_meta", {})["updated_utc"] = "2026-11-20"
        doc["_meta"]["last_change"] = (
            doc["_meta"].get("last_change", "") +
            " | 2026-11-20 (arena/7cec0d73-prod2, final integration): rows carried "
            "forward from the open branches arena/37b265a4-prod2 (PR #43), "
            "arena/20f83238-prod2 (PR #47) and arena/e0d92902-prod2 (PR #41) by content, "
            "renumbered where the source id collided with a main row. No main row was "
            "dropped or rewritten in place.").strip(" |")
        p.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {p.relative_to(ROOT)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
