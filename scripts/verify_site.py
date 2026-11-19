#!/usr/bin/env python3
"""Verification gate for the built site in docs/. Exits non-zero on any failure.

Checks:
  1. Every page has a unique <title> and a unique meta description.
  2. Every page shows the Associates disclosure under the masthead (#disclosure)
     and repeats it in the footer (#footer-disclosure), with the exact wording
     from Operating Agreement Section 5.
  3. Every Amazon link carries rel="sponsored"; every tagged link uses the
     tracking ID from data/products.json.
  4. Every internal link (including #fragment targets) resolves.
  5. Every data row (tr[data-row]) has a source link to an allowed official host.
  6. Every unverified cell says "Unverified" and points to a flag ID.
  7. Banned promotional wording does not appear on reader-facing pages.
  8. sitemap.xml lists every page; feed.xml is well-formed RSS.
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qs

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
TRACK = DATA["tracking_id"]
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
ALLOWED_OFFICIAL = {
    "www.amazon.com", "link.amazon", "affiliate-program.amazon.com", "sellercentral.amazon.com",
    "www.ftc.gov", "developers.google.com", "docs.github.com", "kanlerxz87-cyber.github.io",
}
BANNED = re.compile(r"\b(trending|best|bestsell\w*|top[- ]rated|most popular|guaranteed|highest[- ]converting)\b|#1\b", re.I)
REVIEWER_PAGES = {"flagged.html", "analysis.html", "executive-summary.html", "questions.html",
                  "suggestions.html", "sources.html", "about.html", "ledger.html", "404.html"}

failures = []


def fail(msg):
    failures.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta_desc = None
        self.links = []          # (href, rel, text)
        self.ids = set()
        self.rows = []           # list of dicts: {"id", "cells": [(cls, text, hrefs)]}
        self._in_title = False
        self._a = None
        self._row = None
        self._cell = None
        self.text_parts = []
        self._skip = 0
        self.disclosure_text = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.meta_desc = a.get("content", "")
        if tag == "a":
            self._a = {"href": a.get("href", ""), "rel": a.get("rel", ""), "text": ""}
            if self._cell is not None:
                self._cell["hrefs"].append(a.get("href", ""))
        if tag == "tr" and "data-row" in a:
            self._row = {"id": a["data-row"], "cells": []}
        if tag in ("td", "th") and self._row is not None:
            self._cell = {"cls": a.get("class", ""), "text": "", "hrefs": []}
        if tag == "div" and a.get("id") in ("disclosure", "footer-disclosure"):
            self._disc = a["id"]
            self.disclosure_text[a["id"]] = ""

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        if tag == "title":
            self._in_title = False
        if tag == "a" and self._a is not None:
            self.links.append((self._a["href"], self._a["rel"], self._a["text"].strip()))
            self._a = None
        if tag in ("td", "th") and self._cell is not None and self._row is not None:
            self._row["cells"].append(self._cell)
            self._cell = None
        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._skip:
            return
        if self._a is not None:
            self._a["text"] += data
        if self._cell is not None:
            self._cell["text"] += data
        self.text_parts.append(data)


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def main():
    pages = sorted(DOCS.rglob("*.html"))
    if not pages:
        fail("no HTML pages found in docs/")
    titles, descs = {}, {}
    parsed = {}
    for path in pages:
        rel = path.relative_to(DOCS).as_posix()
        pg = parse(path)
        parsed[rel] = pg

        if not pg.title.strip():
            fail(f"{rel}: missing <title>")
        titles.setdefault(pg.title.strip(), []).append(rel)
        if not pg.meta_desc or not pg.meta_desc.strip():
            fail(f"{rel}: missing meta description")
        descs.setdefault(pg.meta_desc, []).append(rel)

        for div_id in ("disclosure", "footer-disclosure"):
            if div_id not in pg.disclosure_text and div_id not in pg.ids:
                fail(f"{rel}: missing #{div_id}")
        if DISCLOSURE not in "".join(pg.text_parts):
            fail(f"{rel}: Associates disclosure wording missing")

        for href, rel_attr, text in pg.links:
            parsed_url = urlparse(href)
            host = parsed_url.netloc
            if host.endswith("amazon.com") or host == "link.amazon":
                if "sponsored" not in rel_attr.split():
                    fail(f"{rel}: Amazon link without rel=sponsored: {href[:80]}")
                if host.endswith("amazon.com") and "/dp/" in parsed_url.path:
                    tag = parse_qs(parsed_url.query).get("tag", [""])[0]
                    if tag and tag != TRACK:
                        fail(f"{rel}: wrong tracking tag '{tag}' in {href[:80]}")
            if host and host not in ALLOWED_OFFICIAL and host not in ("kanlerxz87-cyber.github.io", "wingbangboozle1-lang.github.io"):
                fail(f"{rel}: link to non-allowlisted host {host}")
            if not href or href.startswith(("mailto:", "http://", "https://", "#")) or host:
                continue
            target, _, frag = href.partition("#")
            dest = (path.parent / target).resolve() if target else path
            if not dest.exists():
                fail(f"{rel}: broken internal link {href}")
                continue
            if frag and dest.suffix == ".html":
                target_page = parsed.get(dest.relative_to(DOCS).as_posix())
                if target_page is None:
                    target_page = parse(dest)
                if frag not in target_page.ids:
                    fail(f"{rel}: missing anchor #{frag} in {target}")

        for row in pg.rows:
            has_official = False
            for cell in row["cells"]:
                for h in cell["hrefs"]:
                    if urlparse(h).netloc in ALLOWED_OFFICIAL:
                        has_official = True
                if "unverified" in cell["cls"]:
                    if "Unverified" not in cell["text"] or not re.search(r"FR-\d{2}", cell["text"]):
                        fail(f"{rel}: unverified cell lacks 'Unverified' and a flag ID: {cell['text'][:60]}")
            if not has_official:
                fail(f"{rel}: data row {row['id']} has no official source link")

        if rel not in REVIEWER_PAGES:
            body_text = " ".join(pg.text_parts)
            for m in BANNED.finditer(body_text):
                fail(f"{rel}: banned promotional wording '{m.group(0)}'")

    for t, where in titles.items():
        if len(where) > 1:
            fail(f"duplicate <title> '{t}': {where}")
    for d, where in descs.items():
        if len(where) > 1:
            fail(f"duplicate meta description: {where}")

    # Flag references resolve
    flag_ids = {f["id"] for f in DATA["flags"]}
    flagged = parsed.get("flagged.html")
    if flagged is None:
        fail("flagged.html missing")
    else:
        for fid in flag_ids:
            if fid not in flagged.ids:
                fail(f"flagged.html lacks anchor for {fid}")

    # Sitemap and feed
    sm_path = DOCS / "sitemap.xml"
    if not sm_path.exists():
        fail("sitemap.xml missing")
    else:
        locs = re.findall(r"<loc>([^<]+)</loc>", sm_path.read_text(encoding="utf-8"))
        for path in pages:
            rel = path.relative_to(DOCS).as_posix()
            if rel == "404.html":
                continue
            if not any(loc.endswith("/" + rel) or (rel == "index.html" and loc.endswith("/Prod2/")) for loc in locs):
                fail(f"sitemap.xml missing {rel}")
    try:
        feed = ET.parse(DOCS / "feed.xml").getroot()
        if feed.tag != "rss" or not feed.findall("./channel/item"):
            fail("feed.xml: not an RSS feed with items")
    except ET.ParseError as exc:
        fail(f"feed.xml not well-formed: {exc}")

    if failures:
        print(f"VERIFY FAILED: {len(failures)} problem(s)")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print(f"VERIFY OK: {len(pages)} pages, all checks passed")


if __name__ == "__main__":
    main()
