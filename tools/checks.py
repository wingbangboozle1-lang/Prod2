#!/usr/bin/env python3
"""checks.py — the publish gate. Run from a clean checkout:

    python3 tools/build.py && python3 tools/checks.py

Standard library only. Exits non-zero on the first failing section; every
section name is printed. Nothing is published while a check fails.

Sections:
  pages        every registered page built; unique <title> + meta description
  disclosure   disclosure sentence on every page (strip + footer repeat)
  links        Amazon link policy (sponsored rel, tag on /dp/); internal links
               resolve; no broken in-site references
  facts        each product's listed facts appear with a citation; null values
               are published blank + marked unverified, never filled in
  claims       banned popularity words on reader-facing pages; no published
               prices or star ratings anywhere
  chrome       one nav group ("The work behind it") + footer directory present
  seo          canonical/og:image/JSON-LD parse; sitemap covers every page;
               robots.txt points at the sitemap; feed items resolve
  freshness    docs/ matches a rebuild from data/ + content/ (no stale output)
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = ROOT / "data" / "p2"

# The disclosure sentence is not hardcoded here: the gate reads the settings file the build
# reads, so the mandated wording and the enforced wording cannot drift apart. Dropped the
# old hardcoded string (it had drifted from the statement Amazon prescribes — F-P09/D-P07).
_settings = json.loads((DATA / "settings.json").read_text(encoding="utf-8"))
DISCLOSURE = _settings["disclosure_sentence"]
PAID_LABEL = _settings["paid_link_label"]
TRACKING_TAG = "tag=shopnow047c-20"

GOVERNANCE = {"executive-summary.html", "method.html", "flagged.html", "questions.html",
              "suggestions.html", "decisions.html", "measurement.html", "compliance.html",
              "privacy.html", "analysis.html", "design-prompt.html"}
BANNED_CLAIM_WORDS = ["trending", "best-selling", "best selling", "hottest", "viral",
                      "everyone is buying", "must-have", "amazon's choice"]
# Reader-facing pages only: the voice rules in data/p2/design-prompts.json (DP-8) and VOICE.md.
# Governance pages may quote the blocklist to explain it, so they are exempt like the rest.
EDITORIAL_BLOCKLIST = [
    "in today's fast-paced", "in today's busy kitchen", "look no further", "game-changer",
    "game changer", "elevate your", "unleash", "delve", "whether you're a beginner",
    "whether you are a beginner", "a world of", "revolutionize", "seamlessly",
    "the perfect gift for", "you won't want to miss", "don't miss out",
]
READ_DATE_RE = re.compile(r"read \d{4}-\d{2}-\d{2}")
PRICE_RE = re.compile(r"\$\s?\d")
RATING_RE = re.compile(r"out of 5 stars")

FAILURES: list[str] = []
SECTION = ""


def check(name: str) -> None:
    global SECTION
    SECTION = name
    print(f"== {name}")


def fail(msg: str) -> None:
    FAILURES.append(f"[{SECTION}] {msg}")
    print(f"   FAIL {msg}")


def ok(msg: str) -> None:
    print(f"   ok   {msg}")


def pages() -> list[pathlib.Path]:
    return sorted(DOCS.glob("*.html"))


def main() -> int:
    html_files = pages()
    if not html_files:
        print("no built pages found — run tools/build.py first")
        return 1

    # ------------------------------------------------------------------ pages
    check("pages")
    sys.path.insert(0, str(ROOT / "tools"))
    import build  # noqa: E402
    registered = {p[1] for p in build.PAGES}
    built = {p.name for p in html_files}
    missing = registered - built
    if missing:
        fail(f"registered pages missing from docs/: {sorted(missing)}")
    titles: dict[str, str] = {}
    descs: dict[str, str] = {}
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        mt = re.search(r"<title>(.*?)</title>", text, re.S)
        md = re.search(r'<meta name="description" content="(.*?)">', text, re.S)
        if not mt:
            fail(f"{f.name}: no <title>")
            continue
        if not md:
            fail(f"{f.name}: no meta description")
            continue
        t, d = mt.group(1).strip(), md.group(1).strip()
        if len(t) > 70:
            fail(f"{f.name}: title longer than 70 chars ({len(t)})")
        if len(d) > 170 or len(d) < 50:
            fail(f"{f.name}: meta description length {len(d)} (want 50-170)")
        if t in titles:
            fail(f"{f.name}: title duplicates {titles[t]}")
        titles[t] = f.name
        if d in descs:
            fail(f"{f.name}: meta description duplicates {descs[d]}")
        descs[d] = f.name
    if not FAILURES:
        ok(f"{len(html_files)} pages, unique titles + descriptions")

    # ------------------------------------------------------------- disclosure
    check("disclosure")
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        n = text.count(DISCLOSURE)
        if n < 2:
            fail(f"{f.name}: disclosure sentence appears {n}x (need strip + footer)")
        if 'class="disclosure"' not in text:
            fail(f"{f.name}: no disclosure strip under the masthead")
        if "footer-disclosure" not in text:
            fail(f"{f.name}: no footer disclosure")
    if not FAILURES:
        ok("disclosure strip + footer repeat on every page")

    # ------------------------------------------------------------------ links
    check("links")
    anchor_re = re.compile(r'<a\b[^>]*>')
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        for tag in anchor_re.findall(text):
            hm = re.search(r'href="([^"]+)"', tag)
            if not hm:
                continue
            href = hm.group(1)
            if href.startswith("https://www.amazon.com/dp/"):
                if TRACKING_TAG not in href:
                    fail(f"{f.name}: product link without {TRACKING_TAG}: {href}")
                if 'rel="sponsored' not in tag:
                    fail(f"{f.name}: product link without rel=sponsored: {href}")
            elif href.startswith("https://link.amazon/"):
                if 'rel="sponsored' not in tag:
                    fail(f"{f.name}: short product link without rel=sponsored: {href}")
            elif href.startswith("https://www.amazon.com/"):
                if "nofollow" not in tag:
                    fail(f"{f.name}: amazon link without nofollow: {href}")
        # internal links resolve
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http", "mailto:", "#")) or href.endswith(".xml"):
                continue
            target = href.split("#")[0]
            if target and not (DOCS / target).exists():
                fail(f"{f.name}: broken internal link -> {href}")

    # In-page anchors resolve. A register id that scrolls nowhere is not a typo, it is a broken
    # promise to a reviewer who was told to jump to SG-24 and lands at the top of the page.
    anchors = {f.name: set(re.findall(r'id="([^"]+)"', f.read_text(encoding="utf-8"))) for f in html_files}
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        for page, frag in re.findall(r'href="([a-zA-Z0-9._\-]+\.html)#([^"#]+)"', text):
            if page not in anchors:
                fail(f"{f.name}: in-page link to a page that does not exist -> {page}#{frag}")
            elif frag not in anchors[page]:
                fail(f"{f.name}: broken anchor -> {page}#{frag}")
        for frag in re.findall(r'href="#([^"#]+)"', text):
            if frag not in anchors[f.name]:
                fail(f"{f.name}: broken same-page anchor -> #{frag}")
    if not FAILURES:
        ok("amazon link policy holds; internal links and in-page anchors resolve")

    # ------------------------------------------------------------------ facts
    check("facts")
    products = json.loads((DATA / "products.json").read_text(encoding="utf-8"))["products"]
    intents = json.loads((DATA / "intent-links.json").read_text(encoding="utf-8"))["links"]
    prod_html = (DOCS / "products.html").read_text(encoding="utf-8")
    compare_html = (DOCS / "compare.html").read_text(encoding="utf-8")
    for p in products:
        if p["buy_url"] not in prod_html:
            fail(f"{p['id']}: buy URL {p['buy_url']} not published on products.html")
        if f"https://www.amazon.com/dp/{p['asin']}" not in prod_html:
            fail(f"{p['id']}: listing citation missing on products.html")
        if p["asin"] not in compare_html:
            fail(f"{p['id']}: ASIN missing from the comparison table")
        if not p.get("name_listing_read"):
            fail(f"{p['id']}: listing title has no read date")
    if "— unverified" not in prod_html:
        fail("products.html: no unverified markers (expected blank commission/price rows)")
    for l in intents:
        for field in ("intended_asin", "official_listing_url", "confirmation_date_utc",
                      "confirmation_source", "observed_redirect"):
            if not l.get(field):
                fail(f"{l['product_id']}: intent record missing {field}")
        if l["intended_asin"] in (l.get("observed_redirect") or {}).get("final_url_without_query", ""):
            pass  # fine — fields are separate JSON keys even when values agree
        if l["intended_asin"] and not re.fullmatch(r"B[0-9A-Z]{9}", l["intended_asin"]):
            fail(f"{l['product_id']}: intended_asin not a 10-char ASIN: {l['intended_asin']}")
    for l in intents:
        if l["link_path_code"] == l["intended_asin"]:
            fail(f"{l['product_id']}: path code merged into intended_asin (must stay separate)")
    if not FAILURES:
        ok("product facts cited; nulls blank + marked; intent fields separate")

    # ----------------------------------------------------------------- claims
    check("claims")
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        if PRICE_RE.search(text):
            fail(f"{f.name}: published price pattern found (F-02 forbids prices)")
        if RATING_RE.search(text):
            fail(f"{f.name}: published star-rating pattern found (F-02)")
        if f.name not in GOVERNANCE:
            low = text.lower()
            for w in BANNED_CLAIM_WORDS:
                if w in low:
                    fail(f"{f.name}: banned popularity claim word '{w}' (D-19)")
    if not FAILURES:
        ok("no prices, ratings or banned popularity claims")

    # --------------------------------------------------------------- editorial
    # The voice rules the project wrote for itself (VOICE.md, design prompt DP-8) are worth
    # nothing if they live only in a document: an unadopted style guide decays within two
    # passes. This section enforces the narrow, checkable part. Exemptions are printed in the
    # run log so a deliberate exception stays visible in review rather than silent.
    check("editorial")
    exempt_file = ROOT / "data" / "p2" / "editorial-exemptions.json"
    exempt = {}
    if exempt_file.exists():
        exempt = json.loads(exempt_file.read_text(encoding="utf-8"))
    exempt_pages = set(exempt.get("pages", []))
    lint_pages = [f for f in html_files
                  if f.name not in GOVERNANCE and f.name not in exempt_pages]
    for f in lint_pages:
        low = f.read_text(encoding="utf-8").lower()
        for w in EDITORIAL_BLOCKLIST:
            if w in low:
                fail(f"{f.name}: throat-clearing / filler phrase '{w}' (VOICE.md, DP-8)")
    for name in ("products.html", "compare.html"):
        text = (DOCS / name).read_text(encoding="utf-8")
        if not READ_DATE_RE.search(text):
            fail(f"{name}: no 'read YYYY-MM-DD' date next to published figures (G8/SG-22)")
    if not FAILURES:
        if exempt_pages:
            print(f"   note: editorial lint exemptions active for {sorted(exempt_pages)}")
        ok(f"voice lint on {len(lint_pages)} reader pages; read dates present on register tables")

    # ------------------------------------------------------------------ chrome
    check("chrome")
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        if 'class="nav"' not in text or "nav-work" not in text:
            fail(f"{f.name}: missing single navigation group")
        if text.count("The work behind it") < 2:
            fail(f"{f.name}: dashboard surfaces not reachable via nav group + footer")
        if "<footer" not in text:
            fail(f"{f.name}: no footer")
    if not FAILURES:
        ok("nav group + footer directory on every page")

    # -------------------------------------------------------------------- seo
    check("seo")
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        if 'rel="canonical"' not in text:
            fail(f"{f.name}: no canonical")
        if 'property="og:image"' not in text:
            fail(f"{f.name}: no og:image")
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
        if not m:
            fail(f"{f.name}: no JSON-LD")
        else:
            try:
                json.loads(m.group(1))
            except Exception as e:  # noqa: BLE001
                fail(f"{f.name}: JSON-LD does not parse ({e})")
    if not (DOCS / "assets" / "img" / "og-card.png").exists():
        fail("og-card.png missing")
    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    for f in html_files:
        if f"/{f.name}</loc>" not in sitemap:
            fail(f"{f.name}: missing from sitemap.xml")
    for loc in re.findall(r"<loc>(.*?)</loc>", sitemap):
        name = loc.rsplit("/", 1)[-1]
        if not (DOCS / name).exists():
            fail(f"sitemap lists missing page {name}")
    robots = (DOCS / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap:" not in robots:
        fail("robots.txt has no Sitemap line")
    feed = (DOCS / "feed.xml").read_text(encoding="utf-8")
    if feed.count("<item>") < 5:
        fail("feed.xml has fewer than 5 items")
    for link in re.findall(r"<link>(.*?)</link>", feed):
        name = link.rsplit("/", 1)[-1]
        if name and name.endswith(".html") and not (DOCS / name).exists():
            fail(f"feed links missing page {name}")
    if not FAILURES:
        ok("meta/JSON-LD/sitemap/robots/feed consistent")

    # -------------------------------------------------------------- freshness
    check("freshness")
    with tempfile.TemporaryDirectory() as td:
        import importlib
        importlib.reload(build)
        build.DOCS = pathlib.Path(td)
        build.main()
        rebuilt = {p.relative_to(td).as_posix(): p for p in pathlib.Path(td).rglob("*") if p.is_file()}
        current = {p.relative_to(DOCS).as_posix(): p for p in DOCS.rglob("*") if p.is_file()}
        for rel, p in rebuilt.items():
            if rel not in current:
                fail(f"stale build: {rel} missing from docs/ (rebuild)")
            elif p.read_bytes() != current[rel].read_bytes():
                fail(f"stale build: {rel} differs from a fresh render (rebuild)")
        for rel in current:
            if rel not in rebuilt:
                fail(f"unexpected file in docs/: {rel} (remove or add to the build)")
    if not FAILURES:
        ok("docs/ matches a fresh render from data/ + content/")

    print()
    if FAILURES:
        print(f"CHECKS FAILED — {len(FAILURES)} problem(s):")
        for f in FAILURES:
            print("  -", f)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
