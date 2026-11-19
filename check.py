#!/usr/bin/env python3
"""The Crisp Counter — check suite. 30 checks over public/ and data/.

Exit code 0 only when every check passes. CI runs build.py then check.py on
every push; the deploy is blocked on any failure. ENGINE.md documents this
count and the count is asserted here (check 29): edit both together.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
DATA = ROOT / "data"
BASE = json.loads((DATA / "site.json").read_text(encoding="utf-8"))["base_url"]

FAILURES = []
CHECKS_RUN = 0


def check(name):
    global CHECKS_RUN
    CHECKS_RUN += 1
    idx = CHECKS_RUN

    def deco(fn):
        def wrapped():
            try:
                ok, detail = fn()
            except Exception as e:  # noqa: BLE001
                ok, detail = False, "raised %r" % (e,)
            if not ok:
                FAILURES.append("#%d %s — %s" % (idx, name, detail))
            return ok
        wrapped.__name__ = name
        return wrapped
    return deco


def all_html():
    return sorted(p for p in PUBLIC.rglob("*.html"))


def rel(p):
    return str(p.relative_to(PUBLIC))


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


site = load("site.json")
products = load("products.json")
intent = load("intent-links.json")
ledger = load("ledger.json")
events = load("events.json")
guides = load("guides.json")
flags = load("flags.json")

AMAZON_RE = re.compile(r"https?://(?:www\.)?amazon\.com|https?://link\.amazon|https?://(?:www\.)?amzn\.to")
TAG = site and "shopnow047c-20"
PUBLISHED_ASINS = {l["intended_asin"] for l in intent["links"] if l["published_outbound_url"]}
HELD_ASINS = {l["intended_asin"] for l in intent["links"] if not l["published_outbound_url"]}
EXPECTED_PAGES = {
    "index.html", "about.html", "404.html", "counter-space.html",
    "executive-summary.html", "suggestions.html", "open-questions.html",
    "shop/index.html", "shop/dual-basket-air-fryers.html",
    "shop/air-fryer-toaster-ovens.html", "shop/single-basket-air-fryers.html",
    "compare/index.html", "guides/index.html",
    "data/products.html", "data/sources.html", "data/ledger.html", "data/events.html",
    "review/flagged.html", "review/decisions.html", "review/methodology.html",
} | {"guides/%s.html" % g["slug"] for g in guides["guides"]}


class P(HTMLParser):
    """Minimal per-page extractor."""

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.anchors = []
        self.imgs = []
        self.metas = {}
        self.title = None
        self._in_title = False
        self._buf = []
        self.jsonld_raw = []
        self._in_ld = False
        self._ld_buf = []
        self._frag_ids = set()
        self.head_closed = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title" and not self.head_closed:
            self._in_title = True
            self._buf = []
        elif tag == "meta":
            if a.get("name"):
                self.metas.setdefault(a["name"], a.get("content", ""))
            elif a.get("property"):
                self.metas.setdefault(a["property"], a.get("content", ""))
        elif tag == "a" and a.get("href"):
            self.anchors.append((a.get("href", ""), a.get("rel", "")))
        elif tag == "img":
            self.imgs.append(a.get("alt", "__MISSING__"))
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self._ld_buf = []
        elif tag == "head":
            pass
        elif a.get("id"):
            self._frag_ids.add(a["id"])

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self.title = "".join(self._buf).strip()
            self._in_title = False
        elif tag == "script" and self._in_ld:
            self._in_ld = False
            self.jsonld_raw.append("".join(self._ld_buf))
        elif tag == "head":
            self.head_closed = True

    def handle_data(self, data):
        if self._in_title:
            self._buf.append(data)
        if self._in_ld:
            self._ld_buf.append(data)


def parse_page(p):
    text = p.read_text(encoding="utf-8")
    parser = P(text)
    parser.feed(text)
    return text, parser


# ---------------------------------------------------------------- checks

@check("all expected pages generated")
def c01():
    got = {rel(p) for p in all_html()}
    missing = EXPECTED_PAGES - got
    extra = got - EXPECTED_PAGES
    if missing or extra:
        return False, "missing=%s extra=%s" % (sorted(missing), sorted(extra))
    return True, ""


@check("unique <title> per page")
def c02():
    titles = {}
    for p in all_html():
        _, pr = parse_page(p)
        titles.setdefault(pr.title, []).append(rel(p))
    dups = {t: v for t, v in titles.items() if len(v) > 1}
    if dups or any(not t for t in titles):
        return False, "dups=%s empty=%s" % (dups, [k for k, v in titles.items() if not t])
    return True, ""


@check("unique meta description per page (40-170 chars)")
def c03():
    descs = {}
    for p in all_html():
        _, pr = parse_page(p)
        d = pr.metas.get("description", "")
        if len(d) < 40 or len(d) > 170:
            return False, "%s has %d-char description" % (rel(p), len(d))
        descs.setdefault(d, []).append(rel(p))
    dups = {d: v for d, v in descs.items() if len(v) > 1}
    if dups:
        return False, "duplicate descriptions: %s" % list(dups.values())
    return True, ""


@check("disclosure strip above the fold on every page")
def c04():
    for p in all_html():
        text, _ = parse_page(p)
        if 'id="disclosure-strip"' not in text:
            return False, rel(p)
    return True, ""


@check("footer disclosure on every page")
def c05():
    for p in all_html():
        text, _ = parse_page(p)
        if 'id="footer-disclosure"' not in text:
            return False, rel(p)
    return True, ""


@check("Amazon IP notice on every page")
def c06():
    needle = "CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON"
    for p in all_html():
        text, _ = parse_page(p)
        if needle not in text:
            return False, rel(p)
    return True, ""


@check("canonical URL on every page")
def c07():
    for p in all_html():
        text, _ = parse_page(p)
        m = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        if not m or not m.group(1).startswith(BASE):
            return False, rel(p)
    return True, ""


@check("Open Graph + Twitter card tags on every page")
def c08():
    for p in all_html():
        _, pr = parse_page(p)
        for k in ("og:title", "og:image", "twitter:card", "twitter:title"):
            if not pr.metas.get(k):
                return False, "%s missing %s" % (rel(p), k)
    return True, ""


@check("JSON-LD parses on every page")
def c09():
    for p in all_html():
        _, pr = parse_page(p)
        if not pr.jsonld_raw:
            return False, rel(p)
        for raw in pr.jsonld_raw:
            try:
                json.loads(raw)
            except Exception as e:
                return False, "%s: %r" % (rel(p), e)
    return True, ""


@check("guides carry BlogPosting structured data")
def c10():
    for g in guides["guides"]:
        p = PUBLIC / "guides" / ("%s.html" % g["slug"])
        _, pr = parse_page(p)
        types = []
        for raw in pr.jsonld_raw:
            types.append(json.loads(raw).get("@type"))
        if "BlogPosting" not in types:
            return False, rel(p)
    return True, ""


@check("front page carries WebSite structured data")
def c11():
    _, pr = parse_page(PUBLIC / "index.html")
    types = [json.loads(raw).get("@type") for raw in pr.jsonld_raw]
    if "WebSite" not in types:
        return False, "types=%s" % types
    return True, ""


@check("sitemap.xml lists exactly the public pages")
def c12():
    sm = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
    locs = set(re.findall(r"<loc>(.*?)</loc>", sm))
    expect = set()
    for p in all_html():
        r = rel(p)
        if r == "404.html":
            continue
        if r.endswith("index.html"):
            expect.add(BASE + (r[:-len("index.html")] + "/" if r != "index.html" else ""))
        else:
            expect.add(BASE + r)
    if locs != expect:
        return False, "missing=%s extra=%s" % (sorted(expect - locs), sorted(locs - expect))
    return True, ""


@check("feed.xml is valid RSS 2.0 and lists all eight guides")
def c13():
    feed = (PUBLIC / "feed.xml").read_text(encoding="utf-8")
    if "<rss" not in feed or "<channel>" not in feed:
        return False, "not RSS"
    titles = re.findall(r"<item><title>(.*?)</title>", feed)
    want = {g["title"] for g in guides["guides"]}
    got = set(titles)
    if got != want or len(titles) != len(want):
        return False, "items=%d want=%d diff=%s" % (len(titles), len(want), want ^ got)
    return True, ""


@check("robots.txt references the sitemap")
def c14():
    robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: %ssitemap.xml" % BASE not in robots:
        return False, robots
    return True, ""


@check("every internal link resolves")
def c15():
    pages = {rel(p) for p in all_html()}
    files = {p.name for p in PUBLIC.iterdir() if p.is_file() and p.suffix in (".xml", ".txt")}
    for p in all_html():
        _, pr = parse_page(p)
        base_dir = rel(p).rsplit("/", 1)[0] if "/" in rel(p) else ""
        for href, _rel in pr.anchors:
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target = href.split("#", 1)[0]
            if target:
                resolved = Path(base_dir, target).as_posix() if base_dir else target
                # normalize ../
                parts = []
                for seg in resolved.split("/"):
                    if seg == "..":
                        if parts:
                            parts.pop()
                    elif seg not in (".", ""):
                        parts.append(seg)
                resolved = "/".join(parts)
                if resolved not in pages and resolved not in files:
                    return False, "%s -> %s" % (rel(p), href)
    return True, ""


@check("every internal fragment target exists")
def c16():
    page_ids = {}
    for p in all_html():
        page_ids[rel(p)] = set(re.findall(r'id="([^"]+)"', p.read_text(encoding="utf-8")))
    for p in all_html():
        _, pr = parse_page(p)
        base_dir = rel(p).rsplit("/", 1)[0] if "/" in rel(p) else ""
        r = rel(p)
        for href, _relattr in pr.anchors:
            if href.startswith(("http://", "https://")):
                continue
            if "#" in href:
                target_page, frag = href.split("#", 1)
                if not frag:
                    continue
                if not target_page:
                    ids = page_ids[r]
                else:
                    resolved = Path(base_dir, target_page).as_posix() if base_dir else target_page
                    parts = []
                    for seg in resolved.split("/"):
                        if seg == "..":
                            if parts:
                                parts.pop()
                        elif seg not in (".", ""):
                            parts.append(seg)
                    resolved = "/".join(parts)
                    ids = page_ids.get(resolved)
                if ids is None or frag not in ids:
                    return False, "%s missing #%s (from %s)" % (resolved if target_page else r, frag, r)
    return True, ""


@check('every Amazon-domain anchor is rel="sponsored"')
def c17():
    for p in all_html():
        _, pr = parse_page(p)
        for href, relattr in pr.anchors:
            if AMAZON_RE.search(href):
                if "sponsored" not in relattr.split():
                    return False, "%s -> %s rel=%r" % (rel(p), href, relattr)
    return True, ""


@check("every tagged anchor is a published intended ASIN or a policy citation")
def c18():
    for p in all_html():
        _, pr = parse_page(p)
        for href, _relattr in pr.anchors:
            if "tag=shopnow047c-20" in href:
                m = re.search(r"amazon\.com/dp/([A-Z0-9]{10})", href)
                if not m:
                    continue  # policy/help pages may carry the tag too
                if m.group(1) not in PUBLISHED_ASINS:
                    return False, "%s -> %s" % (rel(p), href)
    return True, ""


@check("held ASINs and link.amazon paths never appear as anchors")
def c19():
    for p in all_html():
        _, pr = parse_page(p)
        for href, _relattr in pr.anchors:
            if href.startswith("https://link.amazon/"):
                return False, "%s anchors a submitted short link: %s" % (rel(p), href)
            for held in HELD_ASINS:
                if held in href:
                    return False, "%s anchors held ASIN %s" % (rel(p), held)
    return True, ""


@check("product register keeps intended/observed fields separate")
def c20():
    for l in intent["links"]:
        obs = l.get("observed_redirect", {})
        if "intended_asin" not in l or "observed_asin" not in obs:
            return False, l["product_id"]
        if not l.get("confirmation_date_utc") or not obs.get("date_utc"):
            return False, "%s missing dated fields" % l["product_id"]
    return True, ""


@check("ledger is empty, schema-exact, forecast-free")
def c21():
    if ledger["rows"]:
        return False, "ledger has rows"
    cols = ["timestamp_utc", "source", "channel", "eligible_sessions", "clicks", "reported_orders", "report_reference", "obtained_by"]
    if ledger["columns"] != cols:
        return False, "columns drifted"
    if "no_forecast_rule" not in ledger.get("_meta", {}):
        return False, "no-forecast rule missing"
    banned = ("conversion score", "projected revenue", "expected earnings", "revenue estimate")
    text = json.dumps(ledger["rows"]) + json.dumps(ledger["status"]).lower()
    for b in banned:
        if b in text:
            return False, "contains %r" % b
    return True, ""


@check("exactly five events defined and wired in analytics.js")
def c22():
    names = [e["name"] for e in events["events"]]
    if len(names) != 5 or len(set(names)) != 5:
        return False, str(names)
    js = (ROOT / "assets" / "js" / "analytics.js").read_text(encoding="utf-8")
    for n in ("page_view", "product_link_click", "chooser_step", "article_read", "guide_to_compare_click"):
        if n not in js:
            return False, "analytics.js missing %s" % n
    return True, ""


@check("no popularity claims on reader-facing pages")
def c23():
    reader = [p for p in all_html() if not rel(p).startswith(("data/", "review/"))
              and rel(p) not in ("suggestions.html", "open-questions.html")]
    banned = ["trending", "best-selling", "bestseller", "most popular", "top-rated", "viral", "number one", "#1 "]
    for p in reader:
        text = p.read_text(encoding="utf-8").lower()
        body = re.sub(r"<script.*?</script>", "", text, flags=re.S)
        for b in banned:
            if b in body:
                return False, "%s contains %r" % (rel(p), b)
    return True, ""


@check("no slop phrases on reader-facing pages")
def c24():
    reader = [p for p in all_html() if not rel(p).startswith(("data/", "review/"))
              and rel(p) not in ("suggestions.html", "open-questions.html")]
    banned = ["in today's fast-paced", "whether you're a", "let's dive", "buckle up",
              "game-changer", "must-have", "ultimate guide", "look no further",
              "unleash", "supercharge", "elevate your", "seamless", "cutting-edge", "revolutionary", "delve"]
    for p in reader:
        body = re.sub(r"<script.*?</script>", "", p.read_text(encoding="utf-8").lower(), flags=re.S)
        for b in banned:
            if b in body:
                return False, "%s contains %r" % (rel(p), b)
    return True, ""


@check("guide internal linking (comparison + category + two siblings)")
def c25():
    for g in guides["guides"]:
        p = PUBLIC / "guides" / ("%s.html" % g["slug"])
        _, pr = parse_page(p)
        hrefs = [h for h, _r in pr.anchors]
        joined = " ".join(hrefs)
        if "compare/index.html" not in joined:
            return False, "%s missing comparison link" % g["slug"]
        if g["category_page"] not in joined:
            return False, "%s missing category page link" % g["slug"]
        for s in g["sibling_links"]:
            if "guides/%s.html" % s not in joined:
                return False, "%s missing sibling %s" % (g["slug"], s)
    return True, ""


@check("header nav is the single configured group")
def c26():
    want = [n["label"] for n in site["nav_group"]]
    for p in all_html():
        _, pr = parse_page(p)
        nav = re.search(r'<nav class="site-nav"[^>]*>(.*?)</nav>', p.read_text(encoding="utf-8"), re.S)
        if not nav:
            return False, rel(p)
        labels = re.findall(r">([^<]+)</a>", nav.group(1))
        if labels != want:
            return False, "%s has %s" % (rel(p), labels)
    return True, ""


@check("footer directory contains every configured surface")
def c27():
    want = [l["href"] for l in site["footer_directory"]["links"]]
    for p in all_html():
        text = p.read_text(encoding="utf-8")
        for h in want:
            rp = ("../" * (rel(p).count("/"))) + h
            if rp not in text:
                return False, "%s missing %s" % (rel(p), h)
    return True, ""


@check("every image has alt text")
def c28():
    for p in all_html():
        _, pr = parse_page(p)
        for alt in pr.imgs:
            if alt == "__MISSING__" or not str(alt).strip():
                return False, rel(p)
    return True, ""


@check("ENGINE.md check count matches the code")
def c29():
    engine = (ROOT / "ENGINE.md").read_text(encoding="utf-8")
    m = re.search(r"Checks:\s*(\d+)", engine)
    if not m:
        return False, "no count line in ENGINE.md"
    if int(m.group(1)) != len(CHECKS):
        return False, "ENGINE.md says %s, code defines %d" % (m.group(1), len(CHECKS))
    return True, ""


@check("every page parses as HTML")
def c30():
    for p in all_html():
        text = p.read_text(encoding="utf-8")
        parser = HTMLParser()
        try:
            parser.feed(text)
        except Exception as e:
            return False, "%s: %r" % (rel(p), e)
        if not text.rstrip().endswith("</html>"):
            return False, "%s truncated" % rel(p)
    return True, ""


CHECKS = [c01, c02, c03, c04, c05, c06, c07, c08, c09, c10,
          c11, c12, c13, c14, c15, c16, c17, c18, c19, c20,
          c21, c22, c23, c24, c25, c26, c27, c28, c29, c30]


def main():
    if not PUBLIC.exists():
        print("public/ missing — run build.py first", file=sys.stderr)
        return 2
    results = [fn() for fn in CHECKS]
    total = len(CHECKS)
    passed = sum(1 for r in results if r)
    print("checks: %d/%d passed" % (passed, total))
    for f in FAILURES:
        print("FAIL", f)
    return 0 if not FAILURES and passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
