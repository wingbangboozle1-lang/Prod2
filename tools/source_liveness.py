#!/usr/bin/env python3
"""source_liveness.py — the register of official sources, with a dated reachability read.

Why this exists
---------------
`data/p2/sources.json` records *what* each source said and the dates it was read, and
`data/p2/verification-<date>.json` carries dated live reads for the five product
listings. What no file recorded was whether the *non-product* citations still resolve —
a compliance page or a USDA factsheet that moves or disappears changes what the site may
keep asserting, and an editorial pass that only re-reads listings would never notice.

Why the results are stored instead of fetched here
--------------------------------------------------
This repository's sandbox has no general HTTPS egress: a direct request to
amazon.com, fsis.usda.gov or the Pages host all fail at the TLS handshake
(`URLError: TLS/SSL connection has been closed`), measured 2026-11-20. Reads therefore
happen through the agent's fetch tool, one URL per call, and a whole-register sweep is
dozens of calls — which is exactly why it has to be a checklist a session can run in
stages rather than a gate that fails on a network it does not have.

What this script does
---------------------
* `--report` (default, and what the gate calls): coverage table — how many sources have
  a liveness read inside the freshness window, which are stale, which were never read,
  and which are already known dead.
* `--pending`: the URLs still needing a read, one per line, in priority order
  (dead > stale > never-read > fresh), so a session can consume them as fetches and
  paste the results back in.
* `--record HOST PATH STATUS [CHECKED_UTC] [NOTE]`: append one observation.

Findings land in `data/p2/source-liveness-{date}.json`, one row per source:
`{"id","url","host","status","checked_utc","evidence","note"}` where status is
`live` / `moved` / `dead` / `blocked`.

Usage
-----
    python3 tools/source_liveness.py --report
    python3 tools/source_liveness.py --pending
    python3 tools/source_liveness.py --record amazon.com /dp/B0CDY277D3 live 2026-11-20 "page title matched register"
    python3 tools/source_liveness.py --derive-from-verification 2026-11-20
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "p2"
WINDOW_DAYS = 45  # a quarter is too slow for a citation that backs published copy

# Hosts where a non-200 or a TLS failure is the sandbox's fault, not the source's.
# Marking them `blocked` (rather than `dead`) keeps a local environment from writing a
# false finding into the register; the row then says who can confirm it.
def today() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def out_path(date: str) -> pathlib.Path:
    return DATA / f"source-liveness-{date}.json"


def load_sources() -> list[dict]:
    reg = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    return reg["sources"]


def load_rows(date: str) -> list[dict]:
    p = out_path(date)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("checks", [])


def url_of(src: dict) -> str | None:
    u = src.get("url") or ""
    return u or None


def days_since(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        d = dt.date.fromisoformat(iso[:10])
    except ValueError:
        return None
    return (dt.datetime.now(dt.timezone.utc).date() - d).days


def build_manifest(date: str) -> list[dict]:
    """One row per source: the URL, the last read the register has, the liveness state."""
    rows = {r["id"]: r for r in load_rows(date)}
    out = []
    for src in load_sources():
        url = url_of(src) or ""
        host = urlparse(url).netloc if url else ""
        reads = src.get("read") or ([] if not src.get("read_utc") else [src["read_utc"]])
        last_read = max(reads) if reads else None
        lr = rows.get(src["id"])
        state = (lr or {}).get("status") or "never-checked"
        checked = (lr or {}).get("checked_utc")
        out.append({
            "id": src["id"], "host": host, "url": url,
            "kind": src.get("kind") or "", "title": (src.get("title") or "")[:90],
            "register_last_read": last_read,
            "register_read_age_days": days_since(last_read),
            "liveness": state, "liveness_checked_utc": checked,
            "liveness_age_days": days_since(checked),
            "note": (lr or {}).get("note", ""),
        })
    # Priority: known-dead first, then stale-registered citations, then never-checked.
    def rank(r: dict) -> tuple[int, int]:
        if r["liveness"] in ("dead", "moved"):
            return (0, -(r["liveness_age_days"] or 0))
        if r["register_read_age_days"] is None:
            return (1, 0)
        if r["register_read_age_days"] > WINDOW_DAYS:
            return (2, -r["register_read_age_days"])
        if r["liveness"] == "never-checked":
            return (3, 0)
        return (4, 0)
    return sorted(out, key=rank)


def derive_from_verification(date: str) -> int:
    """Fold the dated listing re-reads into the liveness file.

    Every product page was fetched live on <date> and its observed title recorded in
    `verification-<date>.json`, which *is* a reachability read for those five URLs. Not
    recording it would leave the coverage number lying about how current they are.
    """
    vf = DATA / f"verification-{date}.json"
    if not vf.exists():
        print(f"no verification record for {date}; nothing derived")
        return 0
    prods = json.loads(vf.read_text(encoding="utf-8"))["products"]
    srcs = {s["id"]: s for s in load_sources()}
    rows = load_rows(date)
    by_url = {r["url"]: r for r in rows}
    added = 0
    for p in prods:
        sid = f"S-{p['id']}"
        src = srcs.get(sid)
        if not src:
            continue
        url = url_of(src)
        observed = bool(p.get("title_observed"))
        row = {"id": sid, "url": url, "host": urlparse(url).netloc,
               "status": "live" if observed else "blocked",
               "checked_utc": date,
               "evidence": f"data/p2/verification-{date}.json",
               "note": ("title fetched and compared verbatim against the register in the "
                        f"{date} pass — a live read of this URL, not an assumption")
                       if observed else "verification record has no observed title for this product"}
        if by_url.get(url, {}).get("status") == row["status"]:
            continue
        rows = [r for r in rows if r["url"] != url] + [row]
        added += 1
    out_path(date).write_text(json.dumps({
        "_meta": {"date_utc": date, "window_days": WINDOW_DAYS,
                  "description": ("Reachability state for every URL the source register cites. "
                                  "Statuses are live / moved / dead / blocked; `blocked` means this "
                                  "sandbox could not complete a TLS handshake and is not a finding about "
                                  "the source. See tools/source_liveness.py for why reads are recorded "
                                  "rather than fetched at build time."),
                  "derived_rows": added},
        "checks": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"recorded {added} row(s) from verification-{date}.json into {out_path(date).name}")
    return added


def record(host: str, path: str, status: str, checked: str, note: str) -> int:
    if status not in ("live", "moved", "dead", "blocked"):
        print("status must be live / moved / dead / blocked")
        return 2
    date = today()
    url = f"https://{host.lstrip('/')}{path if path.startswith('/') else '/' + path}"
    rows = [r for r in load_rows(date) if r["url"] != url]
    sid = next((s["id"] for s in load_sources() if (s.get("url") or "") == url), None)
    rows.append({"id": sid or f"external:{host}{path}", "url": url, "host": host,
                 "status": status, "checked_utc": checked or date, "evidence": "live fetch this pass",
                 "note": note})
    out_path(date).write_text(json.dumps({
        "_meta": {"date_utc": date, "window_days": WINDOW_DAYS,
                  "description": "Reachability state for every URL the source register cites."},
        "checks": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"recorded {status} for {url}" + (f" [{sid}]" if sid else " [not in register]"))
    return 0


def report() -> int:
    date = today()
    manifest = build_manifest(date)
    if not manifest:
        print("no sources in the register")
        return 0
    counts: dict[str, int] = {}
    for r in manifest:
        counts[r["liveness"]] = counts.get(r["liveness"], 0) + 1
    stale = [r for r in manifest if (r["register_read_age_days"] or 0) > WINDOW_DAYS]
    dead = [r for r in manifest if r["liveness"] in ("dead", "moved")]
    never = [r for r in manifest if r["liveness"] == "never-checked"]
    print(f"{len(manifest)} cited sources — " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    print(f"freshness window {WINDOW_DAYS} days; {len(stale)} register row(s) past it; "
          f"{len(dead)} moved/dead; {len(never)} with no liveness read yet")
    for r in dead[:10]:
        print(f"  {r['liveness']:>6}  {r['id']}  {r['url'][:70]}  ({r['note'][:60]})")
    for r in stale[:10]:
        print(f"  STALE   {r['id']}  last read {r['register_last_read']} ({r['register_read_age_days']}d ago)")
    unregistered = [r for r in load_rows(date) if str(r["id"]).startswith("external:")]
    for r in unregistered:
        print(f"  note: {r['url'][:70]} was checked but is not a register row "
              "(add it to sources.json if a page starts citing it)")
    return 0


def pending() -> int:
    for r in build_manifest(today()):
        if r["liveness"] != "live":
            print(r["url"])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--pending", action="store_true")
    ap.add_argument("--record", nargs="*", help="HOST PATH [STATUS [CHECKED [NOTE]]]")
    ap.add_argument("--derive-from-verification", metavar="DATE")
    a = ap.parse_args()
    if a.record:
        vals = a.record + [""] * (5 - len(a.record))
        return record(*vals[:5])
    if a.derive_from_verification:
        return derive_from_verification(a.derive_from_verification)
    if a.pending:
        return pending()
    return report()


if __name__ == "__main__":
    sys.exit(main())
