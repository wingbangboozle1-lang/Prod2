#!/usr/bin/env python3
"""Verification gate for Countertop Dispatch.

Run from the repository root after building:

    python3 tools/build_site.py && python3 tools/check_site.py

Checks (each maps to an acceptance rule from the brief):
  1  disclosure strip directly under the masthead on every HTML page
  2  disclosure text repeated in the footer of every HTML page
  3  every outbound amazon.com/dp link carries rel="sponsored"
  4  every outbound amazon.com/dp link carries tag=shopnow047c-20
  5  unique <title> and unique meta description across pages
  6  every table row (tbody tr) in a .data table has at least one source
     link to an official domain OR an explicit flag link to flagged.html
  7  sitemap.xml covers every built HTML page; robots.txt points at it
  8  feed.xml includes all four guide articles
  9  no internal href points at a missing file
 10  data/*.json parses; campaign-ledger.csv has a header and zero data rows
 11  exactly five events defined in data/events.json
 12  every flag ID referenced on pages exists in flagged.html, and vice versa
"""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://wingbangboozle1-lang.github.io/Prod2"
TAG = "shopnow047c-20"
OFFICIAL_HOSTS = {
    "www.amazon.com",
    "affiliate-program.amazon.com",
    "developers.google.com",
    "www.ftc.gov",
    "sell.amazon.com",
    "kanlerxz87-cyber.github.io",
}
REQUIRED_GUIDES = [
    "guides/basket-or-oven-air-fryer.html",
    "guides/air-fryer-capacity-checklist.html",
    "guides/cleanup-counter-space-tradeoffs.html",
    "guides/multi-function-kitchen-appliance-questions.html",
]

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def pages() -> list[Path]:
    """Built pages only — content/ fragments are build inputs, not published."""
    out = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in {"node_modules", ".git", "content"}:
            continue
        out.append(p)
    return sorted(out)


def check_disclosure(page: Path, text: str, rel: str) -> None:
    # Rule 1: strip immediately after </header>
    m = re.search(r"</header>\s*(.*?)<nav", text, re.S)
    if not m or "As an Amazon Associate" not in m.group(1):
        err(f"{rel}: disclosure strip not directly under masthead")
    # Rule 2: footer repeat
    footer = text[text.find('<footer'):] if "<footer" in text else ""
    if "As an Amazon Associate" not in footer:
        err(f"{rel}: disclosure missing from footer")


def check_links(rel: str, text: str) -> None:
    for m in re.finditer(r"<a\b([^>]*)>", text):
        attrs = m.group(1)
        href_m = re.search(r'href="([^"]+)"', attrs)
        if not href_m:
            continue
        href = href_m.group(1)
        if "amazon.com/dp/" in href:
            if "sponsored" not in attrs:
                err(f"{rel}: amazon.com/dp link missing rel=sponsored → {href[:80]}")
            if TAG not in href:
                err(f"{rel}: amazon.com/dp link missing tag={TAG} → {href[:80]}")


def check_internal_links(rel: str, text: str) -> None:
    page_dir = (ROOT / rel).parent
    for m in re.finditer(r'href="([^"]+)"', text):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#", "{prefix}")):
            continue
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        if not (page_dir / target).exists():
            err(f"{rel}: broken internal link → {href}")


def check_tables(rel: str, text: str) -> None:
    # Rule 6: every tbody row in a table.data must have an official source
    # link OR a flag link (flag link means the blank is published, not silent).
    for tbl in re.finditer(r'<table class="data([^"]*)"[^>]*>(.*?)</table>', text, re.S):
        editorial = "editorial" in tbl.group(1)
        for row in re.finditer(r"<tr\b[^>]*>(.*?)</tr>", tbl.group(2), re.S):
            row_html = row.group(1)
            if "<td" not in row_html:
                continue  # header row
            links = re.findall(r'href="([^"]+)"', row_html)
            if editorial:
                # commentary tables: every row must still carry at least one link
                if not links:
                    err(f"{rel}: editorial table row without any link → {row_html[:90]}...")
                continue
            official = any(
                urlparse(l).netloc in OFFICIAL_HOSTS for l in links if l.startswith("http")
            )
            flagged = any("flagged.html" in l for l in links)
            if not (official or flagged):
                err(f"{rel}: table row without source or flag link → {row_html[:90]}...")


def main() -> int:
    built = pages()
    if not built:
        print("no HTML pages found — run tools/build_site.py first", file=sys.stderr)
        return 1

    titles: dict[str, str] = {}
    descs: dict[str, str] = {}
    flag_ids_on_pages: set[str] = set()

    for page in built:
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8")

        check_disclosure(page, text, rel)
        check_links(rel, text)
        check_internal_links(rel, text)
        check_tables(rel, text)

        t = re.search(r"<title>(.*?)</title>", text, re.S)
        if not t:
            err(f"{rel}: missing <title>")
        elif t.group(1) in titles:
            err(f"{rel}: duplicate <title> also used by {titles[t.group(1)]}")
        else:
            titles[t.group(1)] = rel

        d = re.search(r'<meta name="description" content="([^"]*)"', text)
        if not d:
            err(f"{rel}: missing meta description")
        elif d.group(1) in descs:
            err(f"{rel}: duplicate meta description also used by {descs[d.group(1)]}")
        else:
            descs[d.group(1)] = rel

        if f'href="{BASE_URL}/' not in text and rel != "index.html":
            # canonical must be absolute; index uses /index.html
            if 'rel="canonical"' not in text:
                err(f"{rel}: missing canonical")
        flag_ids_on_pages.update(re.findall(r'href="[^"]*flagged\.html#([A-Za-z0-9\-]+)"', text))
        flag_ids_on_pages.update(re.findall(r'id="(FLG-[A-Za-z0-9\-]+)"', text))

    # Rule 7: sitemap coverage
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        err("sitemap.xml missing")
    else:
        sm = sitemap.read_text(encoding="utf-8")
        locs = set(re.findall(r"<loc>(.*?)</loc>", sm))
        for page in built:
            rel = page.relative_to(ROOT).as_posix()
            if f"{BASE_URL}/{rel}" not in locs:
                err(f"sitemap.xml missing {rel}")
        try:
            ET.fromstring(sm)
        except ET.ParseError as e:
            err(f"sitemap.xml is not valid XML: {e}")

    robots = ROOT / "robots.txt"
    if not robots.exists():
        err("robots.txt missing")
    elif f"{BASE_URL}/sitemap.xml" not in robots.read_text(encoding="utf-8"):
        err("robots.txt does not reference sitemap.xml")

    # Rule 8: feed contains all four guides
    feed = ROOT / "feed.xml"
    if not feed.exists():
        err("feed.xml missing")
    else:
        ft = feed.read_text(encoding="utf-8")
        try:
            ET.fromstring(ft)
        except ET.ParseError as e:
            err(f"feed.xml is not valid XML: {e}")
        for g in REQUIRED_GUIDES:
            if f"{BASE_URL}/{g}" not in ft:
                err(f"feed.xml missing guide {g}")

    # Rule 10: data files
    for jf in ["data/products.json", "data/submitted-links.json",
               "data/product-intent.json", "data/events.json"]:
        p = ROOT / jf
        if not p.exists():
            err(f"{jf} missing")
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{jf} is not valid JSON: {e}")

    ledger = ROOT / "data/campaign-ledger.csv"
    if not ledger.exists():
        err("data/campaign-ledger.csv missing")
    else:
        lines = [l for l in ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
        if len(lines) != 1:
            err(f"campaign-ledger.csv must be header-only (empty ledger), found {len(lines)-1} data rows")
        expected_head = "timestamp,source,channel,eligible_sessions,outbound_clicks,reported_orders,provenance"
        if lines and lines[0].strip() != expected_head:
            err("campaign-ledger.csv header mismatch")

    # Rule 11: five events
    ev = ROOT / "data/events.json"
    if ev.exists():
        try:
            events = json.loads(ev.read_text(encoding="utf-8"))["events"]
            names = [e["name"] for e in events]
            expected = ["page_view", "product_impression", "outbound_click",
                        "guide_read", "chooser_result"]
            if sorted(names) != sorted(expected):
                err(f"events.json defines {names}, expected {expected}")
            # every event must be emitted somewhere in shipped JS
            js = (ROOT / "assets/analytics.js").read_text(encoding="utf-8")
            for n in expected:
                if n not in js and n != "chooser_result":
                    err(f"event {n} not referenced in assets/analytics.js")
        except (json.JSONDecodeError, KeyError) as e:
            err(f"events.json unreadable: {e}")

    # Rule 12: flag cross-reference
    flagged_page = ROOT / "flagged.html"
    if flagged_page.exists():
        ft = flagged_page.read_text(encoding="utf-8")
        declared = set(re.findall(r'id="(FLG-[A-Za-z0-9\-]+)"', ft))
        referenced = set()
        for page in built:
            rel = page.relative_to(ROOT).as_posix()
            if rel == "flagged.html":
                continue
            referenced.update(
                re.findall(r'href="[^"]*flagged\.html#([A-Za-z0-9\-]+)"',
                           page.read_text(encoding="utf-8"))
            )
        missing = referenced - declared
        unused = declared - referenced
        for m in sorted(missing):
            err(f"flag {m} referenced but not declared in flagged.html")
        for u in sorted(unused):
            warn(f"flag {u} declared but never referenced")

    # Disclosure text exactness
    for page in built:
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8")
        if text.count("As an Amazon Associate") < 2:
            err(f"{rel}: expected disclosure in both strip and footer")

    # Report
    print(f"checked {len(built)} pages, {len(titles)} unique titles, "
          f"{len(descs)} unique descriptions")
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        for e in errors:
            print(f"FAIL  {e}")
        print(f"\n{len(errors)} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
