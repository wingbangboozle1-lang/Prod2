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
  validity     no nested <p>, no duplicate id attributes, no disclosure
               label artifact; fragment links (page.html#id) resolve; every
               F-/Q-/SG-/D- reference in a page exists in its register
  facts        each product's listed facts appear with a citation; null values
               are published blank + marked unverified, never filled in
  claims       banned popularity words on reader-facing pages; no published
               prices or star ratings anywhere
  copy         no unsupported serving counts, footprint claims, speed
               generalizations or cleaning/cabinet conclusions; the
               dishwasher-safe claims name both baskets that carry one
  chrome       one nav group ("The work behind it") + footer directory present
  seo          canonical/og:image/JSON-LD parse; sitemap covers every page;
               robots.txt points at the sitemap; feed items resolve
  shop         one shelf page with all five cards, buy buttons, imagery that
               exists, an About page, and no hands-on-testing claim
  publication  guides reach compare + buying guide + their cluster pillars (S-24);
               feed covers every guide; reader-capture gate consistent with
               settings; Search Console verification meta matches the token slot
  endpoint     the five-event contract agrees across events.json, measure.js and
               server.mjs; no superseded or campaign-ledger event is accepted;
               no reference to a file that does not exist
  summary      the executive summary is generated from data/p2/executive-summary.md
               and the repository's own summary carries the same official sources
  mirror       the repository root mirrors docs/ byte for byte (Pages serves the
               root in legacy "main /" mode)
  exposition   the publish artifact is docs/ only; source is never servable;
               link.amazon short links are quoted evidence, never clickable
  measurement  the site's event list vs the endpoint's accepted names; a
               divergence fails the build (the vocabulary was reconciled in
               M-01; F-P23)
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

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
TRACKING_TAG = "tag=shopnow047c-20"

GOVERNANCE = {"executive-summary.html", "method.html", "flagged.html", "questions.html",
              "suggestions.html", "decisions.html", "measurement.html", "compliance.html",
              "privacy.html"}
BANNED_CLAIM_WORDS = ["trending", "best-selling", "best selling", "hottest", "viral",
                      "everyone is buying", "must-have", "amazon's choice"]
PRICE_RE = re.compile(r"\$\s?\d")
RATING_RE = re.compile(r"out of 5 stars")

# Copy the publication must not make. Each pattern is a claim a listing cannot
# support: no source states a serving count, a heat-up time, a required cabinet
# clearance or a cleaning method for parts a listing does not name.
BANNED_COPY = [
    ("serving count",
     re.compile(r"\b\d\s*[-–]\s*\d+\s+people\b"
                r"|\b(one|two|three|four|five|six|1|2|3|4|5|6)\s*(?:[-–]\s*(?:or|to)\s*"
                r"|\s+(?:or|to)\s+)(two|three|four|five|six|\d)[\s-]*(person|people)\b"
                r"|\b(for|serves?|feeds?|cooks? for)\s+(?:a\s+)?(one|two|three|four|five|six|\d+)"
                r"\s+(?:person|people|servings?)\b", re.I)),
    ("serving count",
     re.compile(r"\bfor\s+(?:a\s+)?(?:one|two|three|four|five|six|\d+)"
                r"(?:\s+(?:or|to)\s+(?:one|two|three|four|five|six|\d+))?"
                r"\s*(?:,|\.|;|<|\s+(?:people|persons?|servings?|crowd)\b)", re.I)),
    ("serving count", re.compile(r"\bfamily of (?:four|4)\b", re.I)),
    ("footprint claim",
     re.compile(r"\b(?:smallest|shallowest|least)\s+footprint\b", re.I)),
    ("generalization about other machines or kitchens",
     re.compile(r"\bmost (?:machines|air fryers|kitchens|models)\b", re.I)),
    ("speed claim",
     re.compile(r"\b(?:heats? up faster|heat faster|preheat(?:s)? faster|cooks? faster"
                r"|runs? hot and fast|warms? up faster)\b", re.I)),
    ("cabinet-clearance conclusion",
     re.compile(r"\b(?:fits under (?:standard )?(?:upper )?cabinets|wants a clear wall"
                r"|will fit in your cabinet|standard upper cabinets)\b", re.I)),
    ("unstated cleaning method",
     re.compile(r"\bhand[- ]wash(?:es|ing)?\s+(?:six|its|the|their)\b", re.I)),
    ("part that no listing names",
     re.compile(r"\bcrisper tray in most\b", re.I)),
]
QUOTED_RE = re.compile(r'"[^"]*"')

# The superseded twelve-event family and the report-only campaign-ledger
# events must never be accepted by the local endpoint.
SUPERSEDED_EVENTS = ["guide_open", "category_open", "rss_feed_click", "chooser_completed",
                     "article_half_read", "disclosure_viewed", "cta_click", "product_click",
                     "filter_apply", "guide_read"]
LEDGER_EVENTS = ["impression", "click", "session", "order", "refund"]

# Directories that hold preserved earlier generations. They are not the active
# publication, so the active-tree scans below skip them.
HISTORICAL_DIRS = {"archive", "site", ".git", ".arena-import", "node_modules", "var",
                   "__pycache__", "docs"}

FAILURES: list[str] = []
SECTION = ""


def check(name: str) -> None:
    global SECTION
    SECTION = name
    print(f"== {name}")


def fail(msg: str) -> None:
    FAILURES.append(f"[{SECTION}] {msg}")
    print(f"   FAIL {msg}")


def note(msg: str) -> None:
    """A published irregularity, not a gate failure. Prints and continues."""
    print(f"   NOTE  {msg}")


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
    if not FAILURES:
        ok("amazon link policy holds; internal links resolve")

    # --------------------------------------------------------------- validity
    check("validity")
    from html.parser import HTMLParser

    class PageParser(HTMLParser):
        VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                "link", "meta", "param", "source", "track", "wbr"}

        def __init__(self) -> None:
            super().__init__(convert_charrefs=True)
            self.p_depth = 0
            self.nested_p: list[int] = []
            self.ids: dict[str, int] = {}
            self.dup_ids: list[tuple[str, int, int]] = []

        def handle_starttag(self, tag, attrs):  # noqa: ANN001
            if tag == "p":
                self.p_depth += 1
                if self.p_depth > 1:
                    self.nested_p.append(self.getpos()[0])
            for key, value in attrs:
                if key == "id" and value:
                    if value in self.ids:
                        self.dup_ids.append((value, self.ids[value], self.getpos()[0]))
                    else:
                        self.ids[value] = self.getpos()[0]

        def handle_endtag(self, tag):  # noqa: ANN001
            if tag == "p":
                self.p_depth = max(0, self.p_depth - 1)

    page_ids: dict[str, set[str]] = {}
    parsed: dict[str, PageParser] = {}
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(text)
        parsed[f.name] = parser
        page_ids[f.name] = set(parser.ids)
        for line in parser.nested_p:
            fail(f"{f.name}:{line}: nested <p> (invalid markup)")
        for dup, first, line in parser.dup_ids:
            fail(f'{f.name}:{line}: duplicate id="{dup}" (first seen line {first})')
        # The Flagged page exists to describe irregularities: it may quote the
        # defective string and name ids from other registers. Every other page
        # must be clean (the disclosure template is shared, so the artifact
        # pattern is still caught on the other 20 pages).
        if f.name != "flagged.html" and re.search(r"\(\(paid", text):
            fail(f"{f.name}: disclosure label artifact '((paid' rendered")
    # fragment links resolve (relative or on-site absolute)
    base = json.loads((DATA / "settings.json").read_text(encoding="utf-8"))["base_url"].rstrip("/")
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(base + "/"):
                href = href[len(base) + 1:]
            if "#" not in href:
                continue
            page_part, frag = href.split("#", 1)
            if not frag:
                continue
            target = page_part or f.name
            if target.endswith(".html") and target in page_ids:
                if frag not in page_ids[target]:
                    fail(f"{f.name}: fragment {target}#{frag} has no matching id")
            elif target == f.name and frag not in page_ids[f.name]:
                fail(f"{f.name}: fragment #{frag} has no matching id")
    # register cross-references: every F-/Q-/SG-/D- id cited on a page exists
    registers = {
        "F": {x["id"] for x in json.loads((DATA / "flags.json").read_text(encoding="utf-8"))["flags"]},
        "Q": {x["id"] for x in json.loads((DATA / "questions.json").read_text(encoding="utf-8"))["questions"]},
        "SG": {x["id"] for x in json.loads((DATA / "suggestions.json").read_text(encoding="utf-8"))["suggestions"]},
        "D": {x["id"] for x in json.loads((DATA / "decisions.json").read_text(encoding="utf-8"))["decisions"]},
    }
    ref_re = re.compile(r"\b(F|Q|SG|D)-(?:P)?\d+\b")
    for f in html_files:
        if f.name == "flagged.html":
            continue  # may name out-of-register ids when that is the irregularity
        text = f.read_text(encoding="utf-8")
        for m in ref_re.finditer(text):
            rid = m.group(0)
            if rid not in registers[m.group(1)]:
                fail(f"{f.name}: cites {rid} which is not in the register")
    if not FAILURES:
        ok("valid markup; fragments and register cross-references resolve")

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

    # -------------------------------------------------------------------- copy
    check("copy")
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        # A quoted string may name a phrase the site refuses to publish
        # ("never estimated for a family of four"), so scan around them.
        scannable = QUOTED_RE.sub('""', text)
        for label, pattern in BANNED_COPY:
            m = pattern.search(scannable)
            if m:
                fail(f"{f.name}: unsupported {label} — {m.group(0)!r}")
    # P1's and P3's baskets are both listed dishwasher-safe; the register and
    # the format page must keep saying so.
    products_data = json.loads((DATA / "products.json").read_text(encoding="utf-8"))["products"]
    for pid in ("P1", "P3"):
        record = next(p for p in products_data if p["id"] == pid)
        if "dishwasher" not in (record.get("name_listing") or "").lower():
            fail(f"{pid}: register no longer lists a dishwasher-safe basket")
    categories = (DOCS / "category-air-fryers.html").read_text(encoding="utf-8").lower()
    if categories.count("dishwasher-safe") < 2:
        fail("category-air-fryers.html: the dishwasher-safe claim must name both P1 and P3")
    if not FAILURES:
        ok("no unsupported serving, footprint, speed or cleaning claims")

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
        # D-06: dashboard surfaces belong in the footer directory, never the reader nav.
        # The reader nav must stay short enough to read at a glance.
        # The reader nav is an inline-flex row of bare <a> siblings followed by the
        # single "The work behind it" <details> group. Slice to the details tag so
        # the footer's links cannot be miscounted as nav links.
        start = text.find('<nav class="nav"')
        if start == -1:
            fail(f"{f.name}: no reader nav")
        else:
            head = text[start:text.find("</nav>", start)]
            reader_part = head.split('<details class="nav-work', 1)[0]
            links = len(re.findall(r"<a\b", reader_part))
            if links > 7:
                fail(f"{f.name}: reader nav has {links} links (max 7; move dashboards to the footer)")
            if links < 4:
                fail(f"{f.name}: reader nav has only {links} links")
        # the wordmark is the home link on every page
        if 'class="wordmark"' not in text:
            fail(f"{f.name}: no wordmark home link")
    if not FAILURES:
        ok("nav group + footer directory on every page; reader nav within budget")

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

    # ----------------------------------------------------------- publication
    check("publication")
    cal = json.loads((DATA / "calendar.json").read_text(encoding="utf-8"))
    guide_ids = [g for g in build.GUIDE_IDS]
    # every guide reaches the comparison, the buying guide and its cluster pillars
    pillars: dict[str, set[str]] = {}
    for cl in cal["clusters"]:
        for g in cl["guides"]:
            pillars.setdefault(g, set()).add(cl["pillar"])
    for gid in guide_ids:
        f = DOCS / f"{gid}.html"
        if not f.exists():
            fail(f"guide page missing: {gid}.html")
            continue
        text = f.read_text(encoding="utf-8")
        for need in ("compare.html", "buying-guide.html"):
            if f'href="{need}' not in text:
                fail(f"{gid}.html: does not reach {need} (S-24 internal-link rule)")
        for pillar in pillars.get(f"{gid}.html", set()):
            if f'href="{pillar}"' not in text:
                fail(f"{gid}.html: does not reach its pillar {pillar} (S-24)")
    # feed covers every guide
    feed = (DOCS / "feed.xml").read_text(encoding="utf-8")
    for gid in guide_ids:
        if f"/{gid}.html" not in feed:
            fail(f"feed.xml: guide {gid}.html not in the feed")
    # reader-capture form: present, consent required, state matches settings
    settings = json.loads((DATA / "settings.json").read_text(encoding="utf-8"))
    cap = settings.get("reader_capture", {}) or {}
    endpoint = cap.get("endpoint", "") or ""
    expect_state = "live" if endpoint else "disconnected"
    for name in ("index.html", "guides.html"):
        text = (DOCS / name).read_text(encoding="utf-8")
        if "data-capture=" not in text or 'name="consent"' not in text:
            fail(f"{name}: reader-capture form or consent checkbox missing")
        if f'data-capture="{expect_state}"' not in text:
            fail(f"{name}: data-capture state != '{expect_state}' (settings.reader_capture)")
        if endpoint and f'data-capture-endpoint="{endpoint}"' not in text:
            fail(f"{name}: capture endpoint not wired from settings")
    # Search Console verification meta matches the settings token
    token = (settings.get("search_console", {}) or {}).get("verification_token", "") or ""
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        has_meta = 'name="google-site-verification"' in text
        if token and not has_meta:
            fail(f"{f.name}: verification token set but meta missing")
        if not token and has_meta:
            fail(f"{f.name}: verification meta present but settings token empty")
    if not FAILURES:
        ok("guides link their pillars; feed covers guides; capture gate and verification meta consistent")

    # ---------------------------------------------------------------- endpoint
    check("endpoint")
    events_doc = json.loads((DATA / "events.json").read_text(encoding="utf-8"))
    declared = [event["name"] for event in events_doc["events"]]
    contract = events_doc["endpoint_contract"]
    if len(declared) != 5:
        fail(f"events.json declares {len(declared)} local events (the contract is exactly five)")
    if sorted(contract["accepted_events"]) != sorted(declared):
        fail("events.json endpoint_contract.accepted_events does not match the declared events")
    if contract.get("method") != "POST":
        fail(f"endpoint contract method is {contract.get('method')!r} (expected POST)")
    if "/api/events" not in str(contract.get("url", "")):
        fail(f"endpoint contract url is {contract.get('url')!r} (expected the /api/events path)")
    # The browser client emits exactly the declared events.
    measure_path = ROOT / "assets" / "js" / "measure.js"
    if not measure_path.exists():
        fail("assets/js/measure.js missing: the five-event client must ship with the site")
    else:
        measure = measure_path.read_text(encoding="utf-8")
        block = measure.split("var EVENTS = [", 1)[-1].split("]", 1)[0]
        client_events = set(re.findall(r'"([a-z_0-9]+)"', block))
        if client_events != set(declared):
            fail(f"measure.js emits {sorted(client_events)}; the contract declares {sorted(declared)}")
    # The endpoint accepts exactly the declared events and nothing else.
    server_path = ROOT / "server.mjs"
    if not server_path.exists():
        fail("server.mjs missing: the optional self-hosted endpoint must ship with the site")
    else:
        server = server_path.read_text(encoding="utf-8")
        for name in declared:
            if name not in server:
                fail(f"server.mjs never names the declared event {name}")
        for name in SUPERSEDED_EVENTS + LEDGER_EVENTS:
            if re.search(rf"""["']{re.escape(name)}["']""", server):
                fail(f"server.mjs accepts the superseded or report-only event {name!r}")
        if "'docs'" not in server and '"docs"' not in server:
            fail("server.mjs does not serve the generated publication in docs/")
        for probe in ("user-agent", "x-forwarded-for", "remoteaddress"):
            if probe in server.lower():
                fail(f"server.mjs reads request metadata ({probe}); it must store counts only")
    # The operator contract names the five events and the endpoint path.
    doc_path = ROOT / "ANALYTICS-ENDPOINT.md"
    if not doc_path.exists():
        fail("ANALYTICS-ENDPOINT.md missing: the endpoint has no operator contract")
    else:
        doc = doc_path.read_text(encoding="utf-8")
        for name in declared:
            if f"`{name}`" not in doc:
                fail(f"ANALYTICS-ENDPOINT.md does not document the event {name}")
        if "/api/events" not in doc:
            fail("ANALYTICS-ENDPOINT.md does not document the POST /api/events path")
    # No active file may point at a repository path that does not exist.
    blob_re = re.compile(r"https://github\.com/wingbangboozle1-lang/Prod2/blob/[^/]+/([^)\s\"'#]+)")
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] in HISTORICAL_DIRS or rel.parts[0] == "data" and rel.parts[1:2] == ("imported",):
            continue
        if path.suffix not in (".md", ".json", ".html", ".py", ".mjs", ".js", ".yml"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for m in blob_re.finditer(text):
            if not (ROOT / m.group(1)).exists():
                fail(f"{rel.as_posix()}: links to {m.group(1)}, which is not in this repository")
    # The endpoint path that never existed must not be named as a file to run.
    # COORDINATION.md and EXECUTIVE_SUMMARY.md are records and name it on purpose.
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] in HISTORICAL_DIRS or rel.as_posix() in (
                "COORDINATION.md", "EXECUTIVE_SUMMARY.md", "tools/checks.py"):
            continue
        if rel.parts[0] == "data" and rel.parts[1:2] == ("imported",):
            continue
        if path.suffix not in (".md", ".json", ".html", ".py", ".mjs", ".js", ".yml"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "analytics-endpoint/server.py" in text:
            # A resolved flag may quote the phantom path as evidence of the
            # defect it records (F-P22). Only a live presentation of the path —
            # one that does not also record that the file never existed — fails.
            historical = ("never committed", "has never existed", "not in this repository",
                          "F-P22")
            if not any(h in text for h in historical):
                fail(f"{rel.as_posix()}: names analytics-endpoint/server.py, "
                     "which is not in this repository")
    if not FAILURES:
        ok("the five-event contract agrees across events.json, measure.js, server.mjs and the docs")

    # ----------------------------------------------------------------- summary
    check("summary")
    summary_source = DATA / "executive-summary.md"
    if not summary_source.exists():
        fail("data/p2/executive-summary.md missing: the executive summary needs a source")
        summary_markdown = ""
    else:
        summary_markdown = summary_source.read_text(encoding="utf-8")
        if "## Official sources for reviewer use" not in summary_markdown:
            fail("executive-summary.md has no official-source section")
        if "## Known omissions" not in summary_markdown:
            fail("executive-summary.md has no known-omissions section")
    summary_page = DOCS / "executive-summary.html"
    if summary_page.exists():
        page = summary_page.read_text(encoding="utf-8")
        for url in re.findall(r"https?://[^\s\"')]+", summary_markdown):
            if url not in page:
                fail(f"executive-summary.html: official source {url} is missing from the page")
    # The repository's own summary must carry the same official sources.
    root_summary = ROOT / "EXECUTIVE_SUMMARY.md"
    if not root_summary.exists():
        fail("EXECUTIVE_SUMMARY.md missing at the repository root")
    else:
        root_text = root_summary.read_text(encoding="utf-8")
        for url in re.findall(r"https?://[^\s\"')|]+", summary_markdown):
            if url not in root_text:
                fail(f"EXECUTIVE_SUMMARY.md: official source {url} is not carried over")
        # The stated gate size must match the gate this file implements.
        stated = re.search(r"\*\*(\d+) sections\*\*", root_text)
        actual = len(re.findall(r'^\s{4}check\("', (ROOT / "tools" / "checks.py").read_text(
            encoding="utf-8"), re.M))
        if stated and int(stated.group(1)) != actual:
            fail(f"EXECUTIVE_SUMMARY.md states {stated.group(1)} gate sections; checks.py has {actual}")
        # The register sizes the summary quotes must match the registers.
        register_sizes = [
            (r"\*\*Flagged for review\*\* \(`flagged\.html`\): (\d+) items",
             len(json.loads((DATA / "flags.json").read_text(encoding="utf-8"))["flags"]), "flags"),
            (r"\*\*Open questions\*\* \(`questions\.html`\): (\d+) items",
             len(json.loads((DATA / "questions.json").read_text(encoding="utf-8"))["questions"]),
             "questions"),
            (r"\*\*Suggestion queue\*\* \(`suggestions\.html`\): (\d+) proposals",
             len(json.loads((DATA / "suggestions.json").read_text(encoding="utf-8"))["suggestions"]),
             "suggestions"),
            (r"\*\*Decision log\*\* \(`decisions\.html`\): (\d+) recorded decisions",
             len(json.loads((DATA / "decisions.json").read_text(encoding="utf-8"))["decisions"]),
             "decisions"),
        ]
        for pattern, expected, label in register_sizes:
            found = re.findall(pattern, root_text)
            if not found:
                fail(f"EXECUTIVE_SUMMARY.md does not state the {label} register size")
            for value in found:
                if int(value) != expected:
                    fail(f"EXECUTIVE_SUMMARY.md states {value} {label}; the register holds {expected}")
    # DECISIONS.md must mirror the decision register exactly, both ways.
    decisions_path = ROOT / "DECISIONS.md"
    if not decisions_path.exists():
        fail("DECISIONS.md missing at the repository root")
    else:
        decisions_text = decisions_path.read_text(encoding="utf-8")
        register = {d["id"] for d in json.loads(
            (DATA / "decisions.json").read_text(encoding="utf-8"))["decisions"]}
        cited = set(re.findall(r"\bD-(?:P)?\d+\b", decisions_text))
        for stale in sorted(cited - register):
            fail(f"DECISIONS.md cites {stale}, which is not in the decision register")
        for missing in sorted(register - cited):
            fail(f"DECISIONS.md does not record {missing} from the decision register")
    if not FAILURES:
        ok("the executive summary is generated from its source and reconciled with the root record")

    # ------------------------------------------------------------------ mirror
    check("mirror")
    for path in sorted(DOCS.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(DOCS)
        twin = ROOT / rel
        if not twin.is_file():
            fail(f"root mirror missing {rel.as_posix()} (legacy Pages serves the repository root)")
        elif twin.read_bytes() != path.read_bytes():
            fail(f"root mirror differs from docs/ for {rel.as_posix()} (rebuild and mirror)")
    root_pages = {p.name for p in ROOT.glob("*.html")}
    docs_pages = {p.name for p in DOCS.glob("*.html")}
    for stale in sorted(root_pages - docs_pages):
        fail(f"root carries {stale}, which is not part of the generated publication")
    if not FAILURES:
        ok(f"the repository root mirrors docs/ ({len(list(DOCS.rglob('*')))} entries)")

    # ------------------------------------------------------------ shop surface
    check("shop")
    if not (DOCS / "shop.html").exists():
        fail("shop.html missing: the site needs one shelf a reader can act on")
    if not (DOCS / "about.html").exists():
        fail("about.html missing: authorship and editorial standards need a home")
    for name in ("index.html", "shop.html"):
        text = (DOCS / name).read_text(encoding="utf-8")
        n_cards = text.count('class="card product-card"')
        if n_cards < 5:
            fail(f"{name}: {n_cards} product cards on the shop surface (want all 5)")
        if text.count('btn-buy') < 5:
            fail(f"{name}: fewer than 5 buy buttons on the shop surface")
        if "assets/img/" not in text:
            fail(f"{name}: no product or hero imagery")
    # every referenced local image must exist in the build
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        for rel in re.findall(r'src="(?:https://[^"]*?/Prod2/)?(assets/img/[^"]+)"', text):
            if not (DOCS / rel).exists():
                fail(f"{f.name}: image {rel} missing from docs/")
        for rel in re.findall(r'<link rel="stylesheet" href="(?:https://[^"]*?/Prod2/)?([^"]+)"', text):
            if not (DOCS / rel).exists():
                fail(f"{f.name}: stylesheet {rel} missing from docs/")
    # the docs must not claim a hands-on test
    for f in html_files:
        text = f.read_text(encoding="utf-8").lower()
        for phrase in ("we tested", "our testing", "hands-on review", "we cooked"):
            if phrase in text:
                fail(f"{f.name}: implies hands-on testing ({phrase!r}) — no unit was tested")
    if not FAILURES:
        ok("one shelf, full cards, real imagery, no hands-on claim")

    # ----------------------------------------------------------- exposition
    check("exposition")
    # The deploy artifact is docs/ alone. Nothing a reader can fetch may expose
    # the registers, the page sources or the generator (flags F-P19/F-P20).
    for stray in ("data", "content", "tools", "scripts", "tests"):
        if (DOCS / stray).exists():
            fail(f"docs/{stray}/ exists in the published artifact — source must not be servable")
    for name in ("COORDINATION.md", "package.json", "server.mjs", ".env"):
        if (DOCS / name).exists():
            fail(f"docs/{name} would be published — source must not be servable")
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        for bad in re.findall(r'href="(?:\.\./|/)(?:data|content|tools|scripts)/[^"]*"', text):
            fail(f"{f.name}: links into the source tree ({bad})")
        for bad in re.findall(r'src="(?:\.\./|/)(?:data|content|tools|scripts)/[^"]*"', text):
            fail(f"{f.name}: embeds a source-tree asset ({bad})")
    # a short link is evidence of what the owner submitted, never a clickable
    # destination: its status is unresolved (F-03/FLG-003) and the site's own
    # outbound hrefs are the tagged /dp/ URLs.
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r'<a\b[^>]*href="https://link\.amazon/[^"]*"', text):
            fail(f"{f.name}: link.amazon short link rendered as a clickable anchor")
            break
        if "link.amazon" in text and "<code>https://link.amazon" not in text:
            fail(f"{f.name}: cites a short link without rendering it as inert code")
        # a doubled string means a renderer emitted the URL twice (label + href)
        for dup in re.findall(r'https://link\.amazon/[A-Za-z0-9]{2,}(https://link\.amazon/)', text):
            fail(f"{f.name}: short-link URL rendered twice in one cell")
    if not FAILURES:
        ok("artifact is docs/ only; short links are quoted, never clickable")

    # ---------------------------------------------------------- measurement
    check("measurement")
    # The site's five events and the endpoint's accepted names must be the same
    # list. They were not (F-P23, published by D-P15 rather than patched); the
    # M-01 rewrite of server.mjs reconciled them, so a divergence now fails the
    # build instead of printing a note.
    server = (ROOT / "server.mjs")
    site_js = (DOCS / "assets" / "js" / "measure.js")
    if server.exists() and site_js.exists():
        m = re.search(r"ACCEPTED_EVENTS\s*=\s*new Set\(\[(.*?)\]\)",
                      server.read_text(encoding="utf-8"), re.S)
        server_events = set(re.findall(r"'([a-z_0-9]+)'", m.group(1))) if m else set()
        js_text = site_js.read_text(encoding="utf-8")
        site_events = set(re.findall(r"name:\s*'([a-z_0-9]+)'", js_text))
        if not site_events:
            m2 = re.search(r'EVENTS\s*=\s*\[(.*?)\]', js_text, re.S)
            site_events = set(re.findall(r'"([a-z_0-9]+)"', m2.group(1))) if m2 else set()
        events_doc = json.loads((ROOT / "data" / "p2" / "events.json").read_text(encoding="utf-8"))
        declared = {e["name"] for e in events_doc["events"]}
        if not server_events:
            fail("server.mjs does not declare an ACCEPTED_EVENTS set the gate can read")
        if site_events != declared:
            fail(f"measure.js events {sorted(site_events)} != events.json {sorted(declared)}")
        rejected = sorted(e for e in declared if e not in server_events)
        if rejected:
            fail(f"endpoint would reject: {', '.join(rejected)} — F-P23")
        ok(f"{len(declared)} site events; endpoint accepts exactly the same {len(server_events)}")
    else:
        note("server.mjs or measure.js missing — vocabulary cross-check skipped")

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
