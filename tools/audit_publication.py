#!/usr/bin/env python3
"""Audit the published publication (root mirror = what legacy Pages serves, plus docs/)
line by line against the brief's hard reader-facing rules:

  A. disclosure strip under the masthead on every page (above the fold);
  B. disclosure repeated in the footer of every page;
  C. product-link contract: every outbound product link (/dp/, link.amazon, tag=)
     carries rel="sponsored" and the enrolled tag; no non-product Amazon link
     carries the tag (an undisclosed affiliate link); every external link opened
     in a new tab carries rel="noopener";
  D. every table row that states a figure carries a source link to an official page
     (in-row <a> or a visible official URL), or is explicitly marked with a
     register id (F-/D-/Q-/SG-/S-) or blank/unverified wording;
  E. every internal link resolves (file + fragment) inside the published tree;
  F. every page has a canonical URL pointing at its own published URL;
  G. titles and meta descriptions are present (uniqueness is checked site-wide);
  H. JSON-LD blocks parse;
  I. findings: published links that point into the source tree (docs/, site/,
     content/, data/, …) — printed, never a gate failure (the Flagged page uses
     some as evidence links);
  J. one site to index: robots.txt disallows every source/duplicate tree, and
     sitemap.xml lists only published root pages that exist.

This is a read-only reviewer instrument: it prints a report and exits non-zero when
a hard rule (A, B, C, F, J) fails. Rule D prints an adjudication list so a human
can look at rows that mix prose and figures.

    python3 tools/audit_publication.py [--root DIR] [--json OUT]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://wingbangboozle1-lang.github.io/Prod2"
OFFICIAL_HOSTS = (
    "www.amazon.com", "amazon.com", "link.amazon",
    "www.usda.gov", "usda.gov", "www.fsis.usda.gov", "fsis.usda.gov",
    "www.foodsafety.gov", "foodsafety.gov",
    "www.fda.gov", "fda.gov",
    "www.ftc.gov", "ftc.gov",
    "www.extension.unl.edu", "extension.unl.edu", "food.unl.edu",
    "affiliate-program.amazon.com", "www.affiliate-program.amazon.com",
    "sellercentral.amazon.com", "sell.amazon.com",
    "developers.google.com", "support.google.com",
)
CITE_HOSTS = ("affiliate-program.amazon.com", "www.affiliate-program.amazon.com",
              "sell.amazon.com", "sellercentral.amazon.com")
BLANK_MARKERS = ("unverified", "flagged", "not published", "not confirmed",
                 "no source", "blank", "left blank", "unknown", "—", "–")
REG_ID_RE = re.compile(r"\b(?:F-P?\d+|D-P?\d+|Q-P?\d+|SG-\d+|S-[A-Z][A-Z0-9-]*)\b")
URL_IN_TEXT_RE = re.compile(r"https?://[^\s\"'<>]+")
SOURCE_DIRS = {"docs", "site", "content", "data", "tools", "scripts", "tests",
               "archive", "var", "npm", ".arena-import", ".git"}

A_RE = re.compile(r"<a\b[^>]*>", re.S | re.I)
HREF_RE = re.compile(r'href="([^"]+)"', re.I)
REL_RE = re.compile(r'rel="([^"]+)"', re.I)
TARGET_RE = re.compile(r'target="([^"]+)"', re.I)
CANON_RE = re.compile(r'<link rel="canonical" href="([^"]+)"', re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
TABLE_RE = re.compile(r"<table\b[^>]*>(.*?)</table>", re.S | re.I)
TR_RE = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>", re.S)
JSONLD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S | re.I)
SITEMAP_LOC_RE = re.compile(r"<loc>([^<]+)</loc>")


def official(url: str) -> bool:
    host = url.split("/", 3)[2].lower() if url.startswith("http") else ""
    return any(host == h or host.endswith("." + h) for h in OFFICIAL_HOSTS)


def text_of(fragment: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", fragment)).strip()


def audit(root: pathlib.Path) -> dict:
    pages = sorted(p for p in root.glob("*.html"))
    report = {"pages": len(pages), "violations": [], "row_findings": [], "source_tree_links": [],
              "counts": {}}
    titles: dict[str, str] = {}
    descs: dict[str, str] = {}

    for page in pages:
        html = page.read_text(encoding="utf-8")
        name = page.name
        lower = html.lower()

        # A. disclosure strip under the masthead, above the fold (before <main)
        head_part = lower.split("<main", 1)[0]
        if 'class="disclosure"' not in head_part and "class='disclosure'" not in head_part:
            report["violations"].append((name, "A", "no disclosure strip before <main>"))

        # B. footer disclosure
        foot = lower.rsplit("<footer", 1)
        footer_html = foot[1] if len(foot) > 1 else ""
        if "as an amazon associate i earn from qualifying purchases" not in footer_html:
            report["violations"].append((name, "B", "no Associate statement in footer"))

        for tag in A_RE.finditer(html):
            a = tag.group(0)
            href_m = HREF_RE.search(a)
            if not href_m:
                continue
            href = href_m.group(1)
            rel_m = REL_RE.search(a)
            rel = (rel_m.group(1).lower() if rel_m else "")
            tgt_m = TARGET_RE.search(a)
            is_product = ("amazon.com/dp/" in href or "link.amazon/" in href or "tag=" in href)
            if "amazon.com" in href or "link.amazon" in href:
                if is_product:
                    # C1: product links are sponsored and tagged
                    if "sponsored" not in rel:
                        report["violations"].append((name, "C", f"product link without rel=sponsored: {href[:90]}"))
                    if "amazon.com/dp/" in href and "tag=shopnow047c-20" not in href:
                        report["violations"].append((name, "C", f"product link without enrolled tag: {href[:90]}"))
                else:
                    # C2: citations must not look like affiliate links
                    if "tag=" in href:
                        report["violations"].append((name, "C", f"non-product amazon link carries tag=: {href[:90]}"))
                    # C3: no redirecting shorteners as live hrefs (F-03 contract)
                    if "link.amazon" in href:
                        report["violations"].append((name, "C", f"live short-link href published: {href[:90]}"))
            if tgt_m and tgt_m.group(1).lower() == "_blank" and "noopener" not in rel:
                report["violations"].append((name, "C", f"target=_blank without noopener: {href[:90]}"))

            # E. internal links resolve (files + fragments)
            if href.startswith(("http://", "https://", "mailto:", "data:", "javascript:")):
                if href.startswith(BASE + "/"):
                    rel_path = href[len(BASE) + 1:].split("#", 1)[0]
                    top = rel_path.split("/", 1)[0]
                    if top in SOURCE_DIRS:
                        report["source_tree_links"].append((name, href[:110]))
                continue
            if href.startswith("#"):
                frag = href[1:]
                if frag and f'id="{frag}"' not in html and f"id='{frag}'" not in html:
                    report["violations"].append((name, "E", f"broken fragment #{frag}"))
                continue
            path, _, frag = href.partition("#")
            target = (root / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
            top = path.split("/", 1)[0]
            if top in SOURCE_DIRS:
                report["source_tree_links"].append((name, href[:110]))
            if path and not target.exists():
                report["violations"].append((name, "E", f"broken link {href}"))
            elif frag and path:
                tgt_html = target.read_text(encoding="utf-8") if target.exists() else ""
                if f'id="{frag}"' not in tgt_html and f"id='{frag}'" not in tgt_html:
                    report["violations"].append((name, "E", f"broken fragment {href}"))

        # F. canonical points at this page's published URL
        can_m = CANON_RE.search(html)
        want = f"{BASE}/{name}"
        if not can_m:
            report["violations"].append((name, "F", "no canonical URL"))
        elif can_m.group(1) != want:
            report["violations"].append((name, "F", f"canonical {can_m.group(1)} != {want}"))

        # G. title / description present (uniqueness recorded site-wide)
        t_m = TITLE_RE.search(html)
        d_m = DESC_RE.search(html)
        if not t_m or not t_m.group(1).strip():
            report["violations"].append((name, "G", "empty <title>"))
        else:
            titles.setdefault(t_m.group(1).strip(), []).append(name)
        if not d_m or not d_m.group(1).strip():
            report["violations"].append((name, "G", "empty meta description"))
        else:
            descs.setdefault(d_m.group(1).strip(), []).append(name)

        # H. JSON-LD parses
        for m in JSONLD_RE.finditer(html):
            try:
                json.loads(m.group(1))
            except Exception as exc:  # noqa: BLE001
                report["violations"].append((name, "H", f"JSON-LD parse error: {exc}"))

        # D. table rows that state figures need a source or an explicit flag
        for tm in TABLE_RE.finditer(html):
            for rm in TR_RE.finditer(tm.group(1)):
                row = rm.group(1)
                cells = [text_of(c) for c in re.findall(r"<td\b[^>]*>(.*?)</td>", row, re.S | re.I)]
                if not cells:
                    continue
                body = " ".join(cells)
                states_figure = bool(re.search(r"\d", body)) or bool(
                    re.search(r"\b(quart|qt|inch|inches|°|degrees|pound|lb|ounce|oz|watt)\b", body, re.I))
                if not states_figure:
                    continue
                has_source = any(official(h) for h in HREF_RE.findall(row)) or any(
                    official(u.rstrip(".,);")) for u in URL_IN_TEXT_RE.findall(row))
                flagged = bool(REG_ID_RE.search(body)) or any(m in body.lower() for m in BLANK_MARKERS)
                if has_source:
                    report["counts"]["rows_sourced"] = report["counts"].get("rows_sourced", 0) + 1
                elif flagged:
                    report["counts"]["rows_flagged_blank"] = report["counts"].get("rows_flagged_blank", 0) + 1
                else:
                    report["row_findings"].append((name, body[:150]))

    dup_t = [f"{v[0]} (dup of {v[1]})" for v in titles.values() if len(v) > 1]
    dup_d = [f"{v[0]} (dup of {v[1]})" for v in descs.values() if len(v) > 1]
    for d in dup_t:
        report["violations"].append((d, "G", "duplicate <title>"))
    for d in dup_d:
        report["violations"].append((d, "G", "duplicate meta description"))

    # J. one site to index: robots policy + sitemap purity
    robots_path = root / "robots.txt"
    if not robots_path.exists():
        report["violations"].append(("robots.txt", "J", "missing"))
    else:
        robots = robots_path.read_text(encoding="utf-8")
        for d in ("docs", "site", "content", "data", "tools", "scripts", "tests", "archive"):
            if f"Disallow: /Prod2/{d}/" not in robots:
                report["violations"].append(("robots.txt", "J", f"missing Disallow for /Prod2/{d}/"))
        if f"Sitemap: {BASE}/sitemap.xml" not in robots:
            report["violations"].append(("robots.txt", "J", "missing Sitemap: line"))
    sm_path = root / "sitemap.xml"
    if not sm_path.exists():
        report["violations"].append(("sitemap.xml", "J", "missing"))
    else:
        locs = SITEMAP_LOC_RE.findall(sm_path.read_text(encoding="utf-8"))
        if not locs:
            report["violations"].append(("sitemap.xml", "J", "no <loc> entries"))
        for loc in locs:
            if not loc.startswith(BASE + "/"):
                report["violations"].append(("sitemap.xml", "J", f"loc outside site: {loc}"))
                continue
            rel = loc[len(BASE) + 1:].split("#", 1)[0]
            top = rel.split("/", 1)[0]
            if top in SOURCE_DIRS or "/" in rel:
                report["violations"].append(("sitemap.xml", "J", f"loc is not a published root page: {loc}"))
            elif rel and not (root / rel).exists():
                report["violations"].append(("sitemap.xml", "J", f"loc has no file: {loc}"))
        sm_pages = {loc.rsplit("/", 1)[-1] for loc in locs}
        for p in pages:
            if p.name not in sm_pages and p.name != "404.html":
                report["violations"].append(("sitemap.xml", "J", f"published page missing from sitemap: {p.name}"))

    report["counts"].setdefault("rows_sourced", 0)
    report["counts"].setdefault("rows_flagged_blank", 0)
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT), help="published tree (default: repo root mirror)")
    ap.add_argument("--json", help="also write machine-readable findings here")
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    rep = audit(root)
    print(f"publication audit — {rep['pages']} pages in {root}")
    if rep["violations"]:
        print(f"\nVIOLATIONS ({len(rep['violations'])}):")
        for name, rule, msg in rep["violations"]:
            print(f"  [{rule}] {name}: {msg}")
    else:
        print("\nno violations: disclosure, product-link contract, canonical, links, "
              "JSON-LD, robots policy and sitemap all pass")
    if rep["source_tree_links"]:
        print(f"\nFINDINGS — links into the source tree ({len(rep['source_tree_links'])}):")
        for name, href in rep["source_tree_links"]:
            print(f"  {name}: {href}")
    if rep["row_findings"]:
        print(f"\nROWS STATING FIGURES WITH NO SOURCE AND NO FLAG MARKER ({len(rep['row_findings'])}):")
        for name, body in rep["row_findings"]:
            print(f"  {name}: {body}")
    print(f"\nrows with source link: {rep['counts']['rows_sourced']}; "
          f"rows flagged/blank: {rep['counts']['rows_flagged_blank']}")
    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(rep, indent=1), encoding="utf-8")
    return 1 if rep["violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
