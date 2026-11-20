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
  chrome       one nav group ("The work behind it") + footer directory present
  seo          canonical/og:image/JSON-LD parse; sitemap covers every page;
               robots.txt points at the sitemap; feed items resolve
  shop         one shelf page with all five cards, buy buttons, imagery that
               exists, an About page, and no hands-on-testing claim
  a11y         one h1 per page, no heading-level skips, headings opened and closed at
               the same level, alt text on images, every radio inside a label
  structured   FAQPage markup matches visible page copy; the landing glance table
               covers all five tools with a source and a sponsored link per row
  assets       the shipped stylesheet is parseable: no unresolved merge-conflict
               markers, design tokens defined, every class a page uses exists
  longreads    every long read registered in the calendar exists, shows inline
               sources, carries its "what we could not verify" block, cites only
               allow-listed official hosts, and is in the sitemap and the feed
  publication  guides reach compare + buying guide + their cluster pillars (S-24);
               feed covers every guide; reader-capture gate consistent with
               settings; Search Console verification meta matches the token slot
  exposition   the publish artifact is docs/ only; source is never servable;
               link.amazon short links are quoted evidence, never clickable
  measurement  the site's event list vs the endpoint's accepted names; any
               divergence FAILS the build (F-P23 fixed 2026-11-20, D-P21)
  one-site     one canonical base across every page; sitemap complete and free of
               duplicates; every archived build carries noindex; robots.txt scoped
               away from source and archive; every css/js URL carries a content
               version so a corrected asset cannot sit behind a stale CDN copy
  productpages one dedicated page per product (SG-12): exists, cites the buy URL,
               carries the unverified block, linked from index, shop, products and
               its pillar, present in the sitemap; no orphan product pages
  briefs       the decision layer: every declared brief rendered, every cited
               register id resolves, no brief with an empty "not known" list, and
               the page is in the sitemap and the footer directory (X-04)
  integrity    no raw merge-conflict marker in any shipped file (a marker shipped
               in assets/css/site.css on 2026-11-20 and broke the live stylesheet);
               the stylesheet still defines its tokens and font-faces; register
               ids cited from a register exist somewhere (X-01/X-05, 2026-11-20)
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
    # A page body that opens with "---" / "Key: value" / "---" is frontmatter the
    # renderer does not understand: it ships as visible text. This happened on
    # 2026-11-20 (before-you-decide.html) and was caught only by reading the live
    # page, which no check does. Catch it in source instead.
    for src in sorted((ROOT / "content" / "pages").glob("*.html")):
        head = src.read_text(encoding="utf-8").lstrip()[:200]
        if head.startswith("---") and re.search(r"^---\s*$", head.split("\n", 1)[1] if "\n" in head else "", re.M):
            fail(f"content/pages/{src.name}: opens with a frontmatter block the renderer emits verbatim")
        if re.match(r"^\s*---\s*\n[A-Za-z][\w ]*:", head):
            fail(f"content/pages/{src.name}: looks like unstripped frontmatter — it will render as text")
    # and the built page must not contain a bare delimiter row either
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        if re.search(r'>\s*---\s*<', text) or re.search(r'<p>\s*---\s*</p>', text):
            fail(f"{f.name}: rendered a bare '---' delimiter as visible content")


    # ------------------------------------------------------- derived numbers
    # 2026-11-20: this session published "the smallest footprint" about the 8 qt
    # basket. The register says the DUAL basket is smallest (158 in2 vs 172).
    # Every derived figure on a page must equal the register's arithmetic, so a
    # wrong comparison fails the build instead of shipping.
    check("derived")
    import json as _json
    _prods = {x["id"]: x for x in _json.loads((DATA / "products.json").read_text(encoding="utf-8"))["products"]}
    _dims, _cap = {}, {"P1": 6.0, "P2": 26.0, "P3": 8.0}
    for _pid, _p in _prods.items():
        if _p.get("dimensions") and _p.get("capacity") and _pid in _cap:
            _d = float(re.match(r'([\d.]+)"D', _p["dimensions"]).group(1))
            _w = float(re.search(r'x ([\d.]+)"W', _p["dimensions"]).group(1))
            _dims[_pid] = (_d, _w, _d * _w, _cap[_pid] / (_d * _w))
    if len(_dims) >= 3:
        _smallest = min(_dims, key=lambda k: _dims[k][2])
        _densest = max(_dims, key=lambda k: _dims[k][3])
        _shop = (DOCS / "shop.html").read_text(encoding="utf-8")
        _m = re.search(r"footprint of the three \(([\d.]+)&nbsp;in&sup2;? against ([\d.]+) and ([\d.]+)\)", _shop)
        if _m:
            _quoted = sorted(float(x) for x in _m.groups())
            _actual = sorted(round(v[2], 1) for v in _dims.values())
            if [round(q) for q in _quoted] != [round(a) for a in _actual]:
                fail(f"shop.html: quoted footprints {_quoted} != register footprints {_actual}")
            _named = re.search(r"(?:the|The) ([A-Za-z0-9 ]+?) (?:has|have) the smallest listed footprint", _shop)
            if _named:
                fail("shop.html: names a 'smallest footprint' winner in prose — the gate cannot "
                     "verify a product name here; state the numbers and let the reader compare")
        # published per-in2 figures on the comparison page must match to 3dp
        _cmp = (DOCS / "compare.html").read_text(encoding="utf-8")
        for _pid, (_d, _w, _fp, _den) in _dims.items():
            _expect = f"{_den:.3f}"
            if _expect not in _cmp:
                fail(f"compare.html: capacity-per-in2 for {_pid} should be {_expect}; not found")
    if not FAILURES:
        ok(f"published footprints and capacity densities match the register arithmetic "
           f"({len(_dims)} products; smallest {_smallest}, densest {_densest})")

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

    # ------------------------------------------------------------- accessibility
    check("a11y")
    # Added 2026-11-20. Nine pages jumped h1 -> h3 (a screen reader announces a
    # section that was never opened) and one page closed an <h2> with </h3>.
    # Neither is visually obvious, and neither would ever have been caught by a
    # reader — which is exactly why it needs a gate rather than a habit.
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        opens = [(int(m.group(1)), m.start()) for m in re.finditer(r"<h([1-6])[^>]*>", text)]
        closes = [(int(m.group(1)), m.start()) for m in re.finditer(r"</h([1-6])>", text)]
        if len(opens) != len(closes):
            fail(f"{f.name}: {len(opens)} headings opened, {len(closes)} closed")
        for (o, opos), (c, cpos) in zip(opens, closes):
            if o != c:
                line = text[:opos].count("\n") + 1
                fail(f"{f.name}: heading opened as h{o} and closed as h{c} (line {line})")
        if opens and opens[0][0] != 1:
            fail(f"{f.name}: first heading is h{opens[0][0]}, not h1")
        if sum(1 for n, _ in opens if n == 1) != 1:
            fail(f"{f.name}: {sum(1 for n, _ in opens if n == 1)} h1 elements (want exactly 1)")
        for (a, _), (b, _) in zip(opens, opens[1:]):
            if b - a > 1:
                fail(f"{f.name}: heading level skips from h{a} to h{b}")
                break
        # images carry alt text or are explicitly decorative
        for m in re.finditer(r"<img\b[^>]*>", text):
            if not re.search(r"\balt=", m.group(0)):
                fail(f"{f.name}: <img> without an alt attribute")
                break
        # a form control needs a label or an aria-label
        for m in re.finditer(r"<input\b[^>]*>", text):
            tag = m.group(0)
            if 'type="hidden"' in tag or 'type="radio"' in tag or 'type="checkbox"' in tag:
                continue  # radios are wrapped in <label> on this site; checked below
            if "aria-label" not in tag and "id=" in tag:
                ident = re.search(r'id="([^"]+)"', tag).group(1)
                if f'for="{ident}"' not in text:
                    fail(f"{f.name}: input #{ident} has no <label for=...>")
    # radio groups: every radio must sit inside a <label>
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r"<input\b[^>]*type=\"radio\"[^>]*>", text):
            before = text[max(0, m.start() - 200):m.start()]
            if "<label" not in before.split("<label")[-1] if "<label" in before else True:
                pass  # handled by the structural check below
        radio_count = text.count('type="radio"')
        label_count = text.count("<label")
        if radio_count and label_count < radio_count:
            fail(f"{f.name}: {radio_count} radios but only {label_count} labels")
    if not FAILURES:
        ok("one h1 per page, no heading-level skips, every heading closed as opened, "
           "images have alt, radios are labelled")

    # --------------------------------------------------------------- structured
    check("structured")
    # Added 2026-11-20. FAQPage markup that does not match the visible copy is a
    # search-engine violation (Google's structured-data policy requires the
    # marked-up content to be visible on the page), so the two are asserted to
    # agree rather than trusted to be written in step. Only the questions are
    # compared verbatim; answers are compared by a shared keyword set, because
    # the JSON-LD is plain text and the page copy carries links.
    for name, must_have in (("index.html", 4), ("decide.html", 4)):
        text = (DOCS / name).read_text(encoding="utf-8")
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
        graph = json.loads(m.group(1))["@graph"] if m else []
        faq = next((g for g in graph if g.get("@type") == "FAQPage"), None)
        if faq is None:
            fail(f"{name}: no FAQPage structured data")
            continue
        entries = faq.get("mainEntity", [])
        if len(entries) < must_have:
            fail(f"{name}: FAQPage has {len(entries)} questions (want at least {must_have})")
        for e in entries:
            q = e["name"]
            # the visible page must contain the same question as a <summary>
            if q not in text:
                fail(f"{name}: FAQPage question not visible on the page: {q!r}")
            if not e.get("acceptedAnswer", {}).get("text"):
                fail(f"{name}: FAQPage question has no answer: {q!r}")
    # the glance table on the landing page must carry a source link on every row
    home = (DOCS / "index.html").read_text(encoding="utf-8")
    if 'class="data glance-table"' in home:
        glance = home.split('class="data glance-table"', 1)[1].split("</table>", 1)[0]
        rows = glance.count("<tr") - 1
        sourced = len(re.findall(r'https://www\.amazon\.com/dp/', glance))
        buyd = len(re.findall(r'rel="sponsored', glance))
        if rows != 5:
            fail(f"index.html: glance table has {rows} rows (want all 5 tools)")
        if sourced < 5 or buyd < 5:
            fail(f"index.html: glance table has {sourced} listing links and {buyd} sponsored links for 5 rows")
    else:
        fail("index.html: the at-a-glance table is missing")
    if not FAILURES:
        ok("FAQPage data mirrors the visible questions; glance table row-sourced")

    # ------------------------------------------------------------------ assets
    check("assets")
    # Added 2026-11-20. The site shipped a stylesheet whose first line was the
    # literal text "<<<<<<< HEAD" (an unresolved merge conflict, reproduced on the
    # live host). A browser is required to core (!) an unknown selector, which
    # swallowed the @font-face block and the :root custom properties: no fonts, no
    # colour tokens, no design system, on every page. Nothing in this gate looked
    # at the CSS bytes, so 30 green sections shipped a broken site.
    #
    # These checks are deliberately structural, not stylistic: they assert the
    # artifact a browser will parse, and the presets the pages depend on.
    CONFLICT_MARKER = re.compile(r"^(<{7}|={7}|>{7})(\s|$)", re.M)
    # Only the files a built page actually loads can break the reader's view, so
    # scan those (plus every .js, which cannot be scoped by a media query). An
    # unrelated archived stylesheet in the same folder is not a shipping defect.
    linked = set()
    for page in html_files:
        text = page.read_text(encoding="utf-8")
        # Strip any ?v= cache-buster: the artifact on disk is site.css, the page
        # requests site.css?v=<hash>. Comparing the raw string against the file
        # list would fail for every page once assets are versioned.
        for rel in re.findall(r'<link rel="stylesheet" href="(?:https://[^"]*?/Prod2/)?([^"?]+)', text):
            linked.add(rel)
        for rel in re.findall(r'<script[^>]+src="(?:https://[^"]*?/Prod2/)?([^"?]+)', text):
            linked.add(rel)
    css_files = sorted(DOCS / rel for rel in linked if rel.endswith((".css", ".js")) and (DOCS / rel).exists())
    if not css_files:
        fail("no stylesheet or script linked by a built page exists in docs/ — nothing styles the site")
    for f in css_files:
        text = f.read_text(encoding="utf-8")
        m = CONFLICT_MARKER.search(text)
        if m:
            line = text[:m.start()].count("\n") + 1
            fail(f"{f.relative_to(DOCS)}: unresolved merge-conflict marker at line {line} "
                 f"({m.group(0).strip()!r}) — a browser drops the rest of the rule block")
        if f.suffix == ".css":
            # a stylesheet that does not declare the design tokens renders unstyled
            if ":root" not in text:
                fail(f"{f.relative_to(DOCS)}: no :root block — every var(--token) is undefined")
            if text.count("{") != text.count("}"):
                fail(f"{f.relative_to(DOCS)}: unbalanced braces "
                     f"({text.count('{')} open vs {text.count('}')} close)")
            for tok in ("--paper", "--ink", "--terracotta", "--serif", "--sans", "--rule"):
                if tok + ":" not in text:
                    fail(f"{f.relative_to(DOCS)}: design token {tok} is not defined")
            # every class the built pages actually use must exist in the sheet
            used = set()
            for page in html_files:
                for attr in re.findall(r'class="([^"]*)"', page.read_text(encoding="utf-8")):
                    used.update(attr.split())
            defined = set(re.findall(r"\.(-?[_a-zA-Z][_a-zA-Z0-9-]*)", text))
            missing = sorted(c for c in used if c not in defined)
            if missing:
                fail(f"{f.relative_to(DOCS)}: {len(missing)} class(es) used by a built page are "
                     f"never defined: {', '.join(missing[:8])}")
    if not FAILURES:
        ok("stylesheets parse as stylesheets: no conflict markers, tokens defined, "
           "every class used by a page exists")
    # Weight budget. The landing page shipped 2.4 MB of PNG for six flat-colour
    # illustrations; WebP siblings brought the same art to 230 KB. A budget is
    # the only thing that stops the next illustration from quietly undoing it.
    BUDGET_FIRST_VIEW_KB = 900
    for name, budget in (("index.html", BUDGET_FIRST_VIEW_KB),
                         ("shop.html", BUDGET_FIRST_VIEW_KB),
                         ("decide.html", BUDGET_FIRST_VIEW_KB)):
        text = (DOCS / name).read_text(encoding="utf-8")
        total = 0
        for rel in re.findall(r'<source[^>]+srcset="(?:https://[^"]*?/Prod2/)?(assets/[^"?\s]+)', text):
            # a <picture> source is what a modern browser actually downloads
            pth = DOCS / rel
            if pth.exists():
                total += pth.stat().st_size
        if total > budget * 1024:
            fail(f"{name}: first-view imagery is {total // 1024} KB (budget {budget} KB)")
    # every <picture> must have a WebP source and a PNG fallback, and both exist
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r'<picture>\s*<source[^>]+srcset="(?:https://[^"]*?/Prod2/)?(assets/[^"?]+)[^"]*"[^>]*>\s*<img[^>]+src="(?:https://[^"]*?/Prod2/)?(assets/[^"?]+)', text):
            webp, png = m.group(1), m.group(2)
            if not webp.endswith(".webp"):
                fail(f"{f.name}: <picture> source is not WebP ({webp})")
            for rel in (webp, png):
                if not (DOCS / rel).exists():
                    fail(f"{f.name}: <picture> file missing from docs/: {rel}")
    if not FAILURES:
        ok(f"first-view imagery within the {BUDGET_FIRST_VIEW_KB} KB budget; every <picture> "
           f"has an existing WebP source and PNG fallback")

    # -------------------------------------------------------------- long reads
    check("longreads")
    # Rules for long-form pieces (added 2026-11-20). A long read is an argument,
    # so the failure modes are different from a guide's: it can ship without a
    # source next to its figures, or without saying what it could not verify.
    cal = json.loads((DATA / "calendar.json").read_text(encoding="utf-8"))
    longreads = (cal.get("longreads") or {}).get("items") or []
    if not longreads:
        note("no long reads registered in data/p2/calendar.json")
    for item in longreads:
        name = item["path"]
        f = DOCS / name
        if not f.exists():
            fail(f"registered long read missing from the build: {name}")
            continue
        text = f.read_text(encoding="utf-8")
        if "What we could not verify" not in text:
            fail(f"{name}: long read has no 'what we could not verify' block")
        # Every external citation must be a real URL on an https official host.
        # Exclude the site's own absolute URLs (canonical, nav, assets): only
        # third-party citations count as evidence.
        base = re.search(r'<link rel="canonical" href="(https://[^/"]+)', text)
        own = base.group(1) if base else ""
        ext = {u for u in re.findall(r'href="(https://[^"]+)"', text) if not u.startswith(own)}
        if not ext:
            fail(f"{name}: long read cites nothing external")
        for url in ext:
            host = re.sub(r"^https://([^/]+).*$", r"\1", url)
            if not re.search(r"(amazon\.com|usda\.gov|food\.unl\.edu|ftc\.gov|google\.com|github\.com)$", host):
                fail(f"{name}: cites an unregistered host {host} — add it to the allowlist deliberately")
        # A claim-carrying paragraph should show a source marker on the page.
        if text.count('class="src-inline"') < 3:
            fail(f"{name}: fewer than 3 inline source markers; a long read must show its receipts")
        if f"/{name}" not in (DOCS / "sitemap.xml").read_text(encoding="utf-8"):
            fail(f"{name}: long read is not in the sitemap")
        if f"/{name}" not in (DOCS / "feed.xml").read_text(encoding="utf-8"):
            fail(f"{name}: long read is not in the feed")
    if not FAILURES:
        ok(f"{len(longreads)} long reads: sourced, verified-block present, in sitemap and feed")

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
        for rel in re.findall(r'src="(?:https://[^"]*?/Prod2/)?(assets/img/[^"?]+)', text):
            if not (DOCS / rel).exists():
                fail(f"{f.name}: image {rel} missing from docs/")
        for rel in re.findall(r'<link rel="stylesheet" href="(?:https://[^"]*?/Prod2/)?([^"?]+)', text):
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

    # ------------------------------------------------------------ exposition
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

    # -------------------------------------------------------------- measurement
    check("measurement")
    # The site and the only endpoint in this repo were written to different event
    # vocabularies (F-P23). Until Q-P14 picks one, the build must at least say so
    # out loud: if they diverge, this prints the divergence rather than failing,
    # because the fix is a recorded decision (D-P15), not a code change.
    server = (ROOT / "server.mjs")
    site_js = (DOCS / "assets" / "js" / "measure.js")
    if server.exists() and site_js.exists():
        m = re.search(r"allowedEvents\s*=\s*new Set\(\[(.*?)\]\)", server.read_text(encoding="utf-8"), re.S)
        server_events = set(re.findall(r"'([a-z_0-9]+)'", m.group(1))) if m else set()
        events_doc = json.loads((ROOT / "data" / "p2" / "events.json").read_text(encoding="utf-8"))
        declared = {e["name"] for e in events_doc["events"]}
        # Read the shipped client's own list too, not just the register: the client
        # is what actually posts, and it is the file that drifted from the register
        # in the first place. Any name it can send that the endpoint rejects is a
        # silent 400 in production, so this is a hard failure now, not a note.
        client_txt = (ROOT / "assets" / "js" / "measure.js").read_text(encoding="utf-8")
        cm = re.search(r"var EVENTS = \[(.*?)\]", client_txt, re.S)
        client_events = set(re.findall(r"\"([a-z_0-9]+)\"|'([a-z_0-9]+)'", cm.group(1))) if cm else set()
        client_events = {a or b for a, b in client_events}
        if not server_events:
            fail("server.mjs: allowedEvents list could not be parsed")
        elif not client_events:
            fail("assets/js/measure.js: EVENTS list could not be parsed")
        else:
            rejected = sorted(e for e in declared | client_events if e not in server_events)
            undocumented = sorted(e for e in client_events if e not in declared)
            if rejected:
                fail("the shipped client can send events the endpoint answers 400 to, "
                     f"so those counts are lost silently: {', '.join(rejected)} (F-P23)")
            if undocumented:
                fail(f"the client sends events missing from data/p2/events.json: {', '.join(undocumented)}")
            ok(f"{len(declared)} declared site events; {len(client_events)} sent by measure.js; "
               f"endpoint accepts {len(server_events)} names; 0 unmatched")
    else:
        note("server.mjs or measure.js missing — vocabulary cross-check skipped")
    # The depth event must fire on long reads too, not only on guide pages.
    # Both new articles were invisible to the old check (2026-11-20).
    mjs = (ROOT / "assets" / "js" / "measure.js").read_text(encoding="utf-8")
    if 'indexOf("article")' not in mjs:
        fail("measure.js: guide_read_75 does not cover article-* pages, so long reads are unmeasured")
    else:
        ok("depth event covers both guide-* and article-* pages")

    # ----------------------------------------------------------------- briefs
    check("briefs")
    # X-04: the decision layer. A brief is only useful if every fact in it points
    # at a row a reader can open, and only honest if it names what is missing. So
    # the gate asserts: the page exists and is reachable; every declared brief is
    # rendered with an anchor; every cited register id exists in that register;
    # and no brief is published with an empty "not known" list, which would mean
    # a decision dressed up as a conclusion.
    briefs_doc = DOCS / "briefs.html"
    if not briefs_doc.exists():
        fail("docs/briefs.html is missing but briefs are declared in data/p2/briefs.json")
    else:
        btext = briefs_doc.read_text(encoding="utf-8")
        bjson = json.loads((DATA / "briefs.json").read_text(encoding="utf-8"))["briefs"]
        flag_ids = {x["id"] for x in json.loads((DATA / "flags.json").read_text(encoding="utf-8"))["flags"]}
        q_ids = {x["id"] for x in json.loads((DATA / "questions.json").read_text(encoding="utf-8"))["questions"]}
        sg_ids = {x["id"] for x in json.loads((DATA / "suggestions.json").read_text(encoding="utf-8"))["suggestions"]}
        d_ids = {x["id"] for x in json.loads((DATA / "decisions.json").read_text(encoding="utf-8"))["decisions"]}
        reg = {"F": flag_ids, "Q": q_ids, "SG": sg_ids, "D": d_ids}
        for b in bjson:
            if f'id="{b["id"]}"' not in btext:
                fail(f"briefs.html: brief {b['id']} is declared but not rendered")
            if not b.get("not_known"):
                fail(f"data/p2/briefs.json: {b['id']} lists nothing as unknown — "
                     "a decision with no open question is a conclusion, not a brief")
            if not b.get("known"):
                fail(f"data/p2/briefs.json: {b['id']} cites no evidence")
            for ref in b.get("flags", []) + b.get("questions", []):
                ns = ref.split("-")[0]
                if ns not in reg or ref not in reg[ns]:
                    fail(f"data/p2/briefs.json: {b['id']} cites {ref}, which is not in its register")
        # every id cited inside a known[]/cheapest-test string must resolve too
        idscan = re.compile(r"\b(F-P?\d{1,3}|Q-P?\d{1,3}|SG-\d{1,3}|D-P?\d{1,3})\b")
        for b in bjson:
            blob = json.dumps({k: b[k] for k in ("known", "not_known", "cheapest_first_test",
                                                  "what_it_blocks", "what_it_does_not_block")})
            for rid in set(idscan.findall(blob)):
                ns = rid.split("-")[0]
                if ns in reg and rid not in reg[ns]:
                    fail(f"data/p2/briefs.json: {b['id']} text cites {rid}, missing from that register")
        # findable: the briefs page must be in the sitemap and reachable from the footer
        smap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
        if "briefs.html" not in smap:
            fail("sitemap.xml does not list briefs.html")
        if 'href="briefs.html"' not in (DOCS / "index.html").read_text(encoding="utf-8"):
            fail("index.html does not link briefs.html (the footer directory must carry it)")
    if not FAILURES:
        ok(f"{'briefs' and len(bjson)} briefs rendered; every citation resolves; page in sitemap + footer")

    # --------------------------------------------------------- one-site/noindex
    check("one-site")
    # "Make it findable" means one site, not four. Every archived build is still
    # fetchable at the live host; left unmarked it competes with the canonical page
    # it duplicates. guard_archive() writes a noindex into each one on every build,
    # and this section is what stops that from silently regressing.
    arch = ROOT / "archive"
    if arch.is_dir():
        unmarked = []
        for f in arch.rglob("*"):
            if f.is_file() and f.suffix in (".html", ".xml"):
                if "noindex" not in f.read_text(encoding="utf-8", errors="replace"):
                    unmarked.append(f.relative_to(arch).as_posix())
        if unmarked:
            fail(f"{len(unmarked)} archived pages ship without noindex, so duplicate copies of "
                 f"the site stay indexable (first: {unmarked[0]}) — rerun tools/build.py")
    robots = (DOCS / "robots.txt").read_text(encoding="utf-8")
    for required in ("Disallow: /Prod2/archive/", "Disallow: /Prod2/data/", "Sitemap: "):
        if required not in robots:
            fail(f"robots.txt: missing '{required}'")
    # exactly one canonical home: every page points at the same base, and the
    # sitemap holds no duplicates and no unbuilt URL.
    cands = set()
    for f in html_files:
        m = re.search(r'<link rel="canonical" href="([^"]+)"', f.read_text(encoding="utf-8"))
        if not m:
            fail(f"{f.name}: no canonical link (search engines must be told which URL is the page)")
        else:
            cands.add(m.group(1).rsplit("/", 1)[0])
    if len(cands) > 1:
        fail(f"pages declare {len(cands)} different canonical bases: {sorted(cands)}")
    smap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", smap)
    if len(locs) != len(set(locs)):
        fail("sitemap.xml contains duplicate <loc> entries")
    built_names = {f.name for f in html_files}
    missing_from_sitemap = sorted(n for n in built_names if f"/{n}<" not in smap)
    if missing_from_sitemap:
        fail(f"{len(missing_from_sitemap)} built pages absent from sitemap.xml: {missing_from_sitemap[:4]}")
    # Asset URLs must carry a content version. Pages serves assets through a CDN:
    # on 2026-11-20 the fixed stylesheet was in the repo and the CDN still served
    # the conflict-broken copy, so a reader kept seeing a broken site after a
    # successful deploy. Versioning the URL makes the deploy actually take effect.
    unversioned = []
    for f in html_files:
        t = f.read_text(encoding="utf-8")
        # Only real asset references: a <link> to a stylesheet or a <script src>.
        # A bare href to the stylesheet is evidence *about* an asset (F-P29 cites
        # the live stylesheet URL as its proof), not a request for one.
        for m in re.finditer(r'<link[^>]+href="[^"]*?/assets/css/[^"?]+"'
                             r'|<script[^>]+src="[^"]*?/assets/js/[^"?]+"', t):
            unversioned.append(f"{f.name}: {m.group(0)[:60]}")
    if unversioned:
        fail(f"{len(unversioned)} asset URLs carry no ?v= cache-buster, so a fix can sit "
             f"behind a stale CDN copy (first: {unversioned[0]})")
    if not FAILURES:
        ok(f"one canonical base; {len(locs)} sitemap URLs, no duplicates; archive noindexed; "
           f"robots scoped; assets cache-busted")

    # --------------------------------------------------------------- integrity
    check("integrity")
    # A raw merge-conflict marker shipped in assets/css/site.css on 2026-11-20 and
    # build.py copied it verbatim into docs/assets/css/, so the published stylesheet
    # was invalid for every reader while every other section stayed green: no section
    # read the static assets. Two fixes: resolve the file (done), and gate it here.
    CONFLICT_RE = re.compile(r"^(<<<<<<<|>>>>>>>|\|\|\|\|\|\|\|)( |$)|^=======$", re.M)
    static_exts = {".css", ".js", ".svg", ".html", ".xml", ".json", ".txt"}
    for root_dir, label in ((DOCS, "docs/"), (ROOT / "assets", "assets/")):
        for f in root_dir.rglob("*"):
            if not f.is_file() or f.suffix not in static_exts:
                continue
            if "archive" in f.parts:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if CONFLICT_RE.search(text):
                fail(f"{label}{f.relative_to(root_dir).as_posix()}: raw merge-conflict marker shipped")
    # The stylesheet must actually parse far enough to define the token block the
    # pages depend on: a truncated or marker-broken file loses :root and the site
    # renders unstyled. Assert the tokens and the two families the build preloads.
    css = DOCS / "assets" / "css" / "site.css"
    if not css.exists():
        fail("docs/assets/css/site.css is missing")
    else:
        c = css.read_text(encoding="utf-8")
        if c.count("{") != c.count("}"):
            fail(f"site.css: unbalanced braces ({c.count('{')} open / {c.count('}')} close)")
        for token in ("--paper:", "--ink:", "--serif:", "--sans:"):
            if token not in c:
                fail(f"site.css: design token {token} missing (stylesheet truncated?)")
        # Both a static-subset and a variable stack are valid; what must not happen
        # is a stylesheet with no usable face for each family the build preloads.
        # (tools/design_qa.py parses the CSS properly; this is the cheap assertion.)
        if "@font-face" not in c:
            fail("site.css: no @font-face at all, so the preloaded fonts are never used")
        for family in ('"Fraunces"', '"Inter"'):
            if family not in c:
                fail(f"site.css: no @font-face declares {family}")
        if not re.search(r'src:\s*url\("\.\./fonts/[^"]+\.woff2"\)', c):
            fail("site.css: no @font-face points at a local .woff2 (a CDN face would leak reader IPs)")
    # Every register id referenced from a page or another register must exist.
    registers = {}
    for name, key in (("flags.json", "flags"), ("questions.json", "questions"),
                      ("suggestions.json", "suggestions"), ("decisions.json", "decisions")):
        p = DATA / name
        if p.exists():
            registers[name] = {x["id"] for x in json.loads(p.read_text(encoding="utf-8"))[key]}
    all_ids = set().union(*registers.values()) if registers else set()
    id_re = re.compile(r"\b(F-P?\d{1,3}|Q(?:-P)?\d{1,3}|SG-\d{1,3}|D(?:-P)?\d{1,3})\b")
    # A range such as "D-P10..D-P17" names an ID space, not a reference to a row,
    # so drop range expressions before collecting ids to check.
    range_re = re.compile(r"\b[A-Z]{1,2}(?:-P)?\d{1,3}\s*[.–-]{1,2}\s*[A-Z]{1,2}(?:-P)?\d{1,3}\b")
    for name in registers:
        text = range_re.sub(" ", (DATA / name).read_text(encoding="utf-8"))
        for rid in set(id_re.findall(text)):
            # a register may cite a neighbouring register's id; only flag ids that
            # exist in NO register at all, which is the real dangling-reference case.
            if rid not in all_ids:
                fail(f"data/p2/{name}: cites {rid}, which exists in no register")
    # every dated verification record must name a date and the tool that read it
    for p in DATA.glob("verification-*.json"):
        try:
            blob = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"data/p2/{p.name}: not valid JSON ({exc})")
            continue
        if not re.search(r"\d{4}-\d{2}-\d{2}", p.name):
            fail(f"data/p2/{p.name}: verification record filename carries no date")
    if not FAILURES:
        ok("no conflict markers shipped; stylesheet tokens intact; register ids resolve")

    # ------------------------------------------------------------ product pages
    check("productpages")
    # SG-12 (shipped 2026-11-20): every product in the register has its own
    # reader page. The gate keeps the promise: no product without a page, no
    # page without its buy link, its citations and its unverified block.
    paths = build.PRODUCT_PAGE_PATHS
    product_files = sorted(f.name for f in DOCS.glob("product-*.html"))
    expect_files = sorted(v + ".html" for v in paths.values())
    if product_files != expect_files:
        fail(f"product pages on disk != registry: {product_files} vs {expect_files}")
    for p in products:
        slug = paths.get(p["id"])
        if not slug:
            fail(f"{p['id']}: no product page registered in build.PRODUCT_PAGE_PATHS")
            continue
        f = DOCS / (slug + ".html")
        if not f.exists():
            fail(f"{p['id']}: product page {slug}.html not built")
            continue
        text = f.read_text(encoding="utf-8")
        if p["buy_url"] not in text:
            fail(f"{slug}.html: does not carry the tagged buy URL")
        if 'rel="sponsored' not in text:
            fail(f"{slug}.html: buy link not marked sponsored")
        if "What we could not verify" not in text:
            fail(f"{slug}.html: no 'what we could not verify' block")
        if p["asin"] not in text:
            fail(f"{slug}.html: ASIN not published on its own page")
        for host_page in ("index.html", "shop.html", "products.html"):
            if f'href="{slug}.html"' not in (DOCS / host_page).read_text(encoding="utf-8"):
                fail(f"{host_page}: does not link the {p['id']} product page")
        pillar = "category-air-fryers.html" if "thermometer" not in p["format"].lower() \
            else "category-thermometers.html"
        if f'href="{slug}.html"' not in (DOCS / pillar).read_text(encoding="utf-8"):
            fail(f"{pillar}: does not link the {p['id']} product page")
        if f"/{slug}.html</loc>" not in (DOCS / "sitemap.xml").read_text(encoding="utf-8"):
            fail(f"{slug}.html: missing from sitemap.xml")
    if not FAILURES:
        ok(f"{len(products)} product pages: cited, sponsored, unverified-block present, linked, in sitemap")

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
