#!/usr/bin/env python3
"""Build The Crisp Counter from the data registers into public/.

Reads only data/*.json and content/guides/*.html; writes the complete static
site (29 HTML pages, RSS feed, sitemap, robots.txt, assets). Standard library
only. See ENGINE.md.
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"
ASSETS_SRC = ROOT / "assets"
SITE = json.loads((DATA / "site.json").read_text(encoding="utf-8"))
BASE = SITE["base_url"]
PUB_DATE = "2026-11-19"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


PRODUCTS = load("products.json")
INTENT = load("intent-links.json")
ASSOC = load("associates.json")
SOURCES = load("sources.json")
FLAGS = load("flags.json")
DECISIONS = load("decisions.json")
SUGGESTIONS = load("suggestions.json")
QUESTIONS = load("open-questions.json")
GUIDES = load("guides.json")
CALENDAR = load("calendar.json")
EVENTS = load("events.json")
LEDGER = load("ledger.json")

PRODUCTS_BY_ID = {p["id"]: p for p in PRODUCTS["products"]}
GUIDES_BY_SLUG = {g["slug"]: g for g in GUIDES["guides"]}
PUBLISHED_INTENT_ASINS = {l["intended_asin"] for l in INTENT["links"] if l["published_outbound_url"]}
HELD_ASINS = {l["intended_asin"] for l in INTENT["links"] if not l["published_outbound_url"]}

AMAZON_DOMAINS = ("amazon.com", "amzn.to", "link.amazon")


def esc(s):
    return html.escape(str(s), quote=True)


def depth_of(path):
    return path.count("/") + 1


def rel_prefix(path):
    d = depth_of(path)
    return "" if d == 1 else "../" * (d - 1)


def canon(path):
    if path == "index.html":
        return BASE
    if path.endswith("index.html"):
        return BASE + path[: -len("index.html")] + "/"
    return BASE + path


def amazon_anchor(url, text, cls=""):
    """An outbound Amazon anchor: tagged, rel=sponsored, new tab.

    Per Participation Requirements 2(b) the site's conservative rule is that
    every link placed to an Amazon site carries the tag parameter. Held
    products and submitted short-link paths are never rendered as anchors
    (see no_held_anchors below)."""
    tag = ASSOC["tracking_id"]["value"]
    if "?" in url:
        url_t = url + "&tag=" + tag
    else:
        url_t = url + "?tag=" + tag
    clsattr = ' class="%s"' % cls if cls else ""
    return '<a href="%s" rel="sponsored noopener" target="_blank"%s>%s</a>' % (
        esc(url_t), clsattr, esc(text))


def text_url(url):
    """A URL shown as plain text (evidence), never an anchor."""
    return '<code class="urltext">%s</code>' % esc(url)


def amazon_link_or_text(url, text, cls=""):
    """Render an Amazon URL as a tagged anchor, or as plain text when it must
    never be linked (submitted short-link paths, held product ASINs)."""
    if url.startswith("https://link.amazon/"):
        return text_url(url) + " <span class=\"microbadge\">recorded verbatim - not linked</span>"
    for held in HELD_ASINS:
        if held in url:
            return text_url(url) + ' <span class="microbadge">held - not linked</span>'
    return amazon_anchor(url, text, cls)


def buy_button(product):
    return amazon_anchor(
        product["special_link_published"],
        "Check the listing",
        "btn btn-buy product-link")


def cited_dims(p):
    return esc(p["dimensions"])


def fmt_features(p):
    return ", ".join(p["special_features"])


L_PER_QT = 0.946
IN_CM = 2.54


def depth_cm(dims):
    # dims like: 13.38"D x 11.81"W x 10.63"H  (depth first, as listed)
    first = dims.split('"')[0]
    return float(first) * IN_CM


def capacity_l(p):
    cap = p["capacity"].lower()
    if "liter" in cap or "litre" in cap:
        return float(cap.split()[0])
    if "quart" in cap:
        return float(cap.split()[0]) * L_PER_QT
    raise ValueError(p["capacity"])


def cpd(p):
    return capacity_l(p) / depth_cm(p["dimensions"])


# ---------------------------------------------------------------- templates

def head_block(path, title, desc, extra_head="", jsonld=""):
    rp = rel_prefix(path)
    og = BASE + "assets/og-image.png"
    parts = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>%s</title>" % esc(title),
        '<meta name="description" content="%s">' % esc(desc),
        '<link rel="canonical" href="%s">' % esc(canon(path)),
        '<meta property="og:title" content="%s">' % esc(title),
        '<meta property="og:description" content="%s">' % esc(desc),
        '<meta property="og:type" content="website">',
        '<meta property="og:url" content="%s">' % esc(canon(path)),
        '<meta property="og:image" content="%s">' % og,
        '<meta property="og:site_name" content="%s">' % esc(SITE["brand"]["name"]),
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % esc(title),
        '<meta name="twitter:description" content="%s">' % esc(desc),
        '<meta name="twitter:image" content="%s">' % og,
        '<link rel="icon" type="image/svg+xml" href="%sassets/favicon.svg">' % rp,
        '<link rel="alternate" type="application/rss+xml" title="%s" href="%sfeed.xml">' % (
            esc(SITE["brand"]["name"]), BASE),
        '<link rel="stylesheet" href="%sassets/css/main.css">' % rp,
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap">',
    ]
    if extra_head:
        parts.append(extra_head)
    if jsonld:
        parts.append('<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False))
    return "\n".join(parts)


def nav_block(path):
    rp = rel_prefix(path)
    items = []
    for n in SITE["nav_group"]:
        items.append('<a href="%s%s">%s</a>' % (rp, n["href"], esc(n["label"])))
    return ('<nav class="site-nav" aria-label="Primary">%s</nav>' % "\n".join(items))


def disclosure_strip(path):
    rp = rel_prefix(path)
    return (
        '<div id="disclosure-strip" class="disclosure-strip" role="note">'
        '<span>%s</span> <a href="%sabout.html#disclosure">What this means</a>'
        "</div>" % (esc(SITE["disclosure"]["strip"]), rp)
    )


def footer_block(path):
    rp = rel_prefix(path)
    dir_links = []
    for l in SITE["footer_directory"]["links"]:
        dir_links.append('<a href="%s%s">%s</a>' % (rp, l["href"], esc(l["label"])))
    return (
        '<footer class="site-footer">'
        '<div class="footer-brand"><span class="wordmark">%s</span><p>%s</p></div>'
        '<div class="footer-directory"><h3>%s</h3><div class="footer-links">%s</div></div>'
        '<div id="footer-disclosure" class="footer-disclosure">'
        "<p>%s</p><p class='ip-notice'>%s</p>"
        "</div>"
        '<div class="footer-meta"><span>&copy; 2026 %s. %s</span></div>'
        "</footer>"
    ) % (
        esc(SITE["brand"]["name"]),
        esc(SITE["brand"]["tagline"]),
        esc(SITE["footer_directory"]["title"]),
        "".join(dir_links),
        esc(SITE["disclosure"]["footer_note"]),
        esc(SITE["disclosure"]["amazon_ip_notice"]),
        esc(SITE["brand"]["name"]),
        esc("Built from registers; see the source register for every citation."),
    )


def page_shell(path, title, desc, body, body_class="", extra_head="", jsonld=""):
    rp = rel_prefix(path)
    return """<!DOCTYPE html>
<html lang="en">
<head>
%s</head>
<body class="%s">
<a class="skip-link" href="#main">Skip to content</a>
<header class="masthead">
  <div class="masthead-inner">
    <a class="brand" href="%sindex.html"><svg class="brand-glyph" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h16l-1.6 8.4a3 3 0 0 1-3 2.6H8.6a3 3 0 0 1-3-2.6L4 9Zm3.5-4h9l1.2 3H6.3l1.2-3Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg><span class="wordmark">%s</span></a>
    %s
  </div>
</header>
%s
<main id="main">
%s
</main>
%s
<script src="%sassets/js/analytics.js" defer></script>
</body>
</html>""" % (
        head_block(path, title, desc, extra_head, jsonld),
        esc(body_class),
        rp,
        esc(SITE["brand"]["name"]),
        nav_block(path),
        disclosure_strip(path),
        body,
        footer_block(path),
        rp,
    )


def breadcrumb(path, trail):
    rp = rel_prefix(path)
    parts = ['<nav class="crumbs" aria-label="Breadcrumb"><a href="%sindex.html">Home</a>' % rp]
    for label, href in trail[1:-1]:
        parts.append('<span class="crumb-sep" aria-hidden="true">/</span><a href="%s%s">%s</a>' % (rp, href, esc(label)))
    parts.append('<span class="crumb-sep" aria-hidden="true">/</span><span aria-current="page">%s</span>' % esc(trail[-1][0]))
    parts.append("</nav>")
    return "".join(parts)


def status_badge(status):
    label = {
        "verified-carried": "verified (carried)",
        "held-unpublished": "held",
        "unverified": "unverified",
    }.get(status, status)
    cls = "verified" if status == "verified-carried" else ("held" if status == "held-unpublished" else "unverified")
    return '<span class="badge badge-%s">%s</span>' % (cls, esc(label))


def fact_table(p):
    rows = [
        ("Brand", p["brand"]),
        ("Model", "%s (%s)" % (p["model_name"], p["model_number"])),
        ("Format", p["category"]),
        ("Capacity, as listed", p["capacity"]),
        ("Dimensions, as listed", "%s inches" % cited_dims(p)),
        ("Colour / finish", p["color"]),
        ("Materials", p["material"]),
        ("Special features, as listed", fmt_features(p)),
        ("Facts read from", amazon_link_or_text(p["official_listing_url"], "the official listing page")),
        ("Last read", p["facts_last_read_utc"]),
        ("Attribution", p["attribution_status"]),
    ]
    trs = "".join(
        "<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (esc(k), v)
        for k, v in rows
    )
    return '<table class="fact-table"><tbody>%s</tbody></table>' % trs


def verified_three_module(current_path, heading="The verified three"):
    rp = rel_prefix(current_path)
    rows = []
    for pid in ("P1", "P2", "P3"):
        p = PRODUCTS_BY_ID[pid]
        rows.append(
            "<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td class=\"cell-cta\">%s <span class=\"microbadge\">sponsored</span></td></tr>" % (
                esc(p["name_short"]), esc(p["category"]), esc(p["capacity"]), buy_button(p))
        )
    return (
        '<section class="verified-three" aria-label="The verified three">'
        "<h2>%s</h2>"
        '<p class="module-note">Every figure in this table was read from the official Amazon listing page '
        "(last read 2026-11-16; see the <a href=\"%sdata/products.html\">product register</a> for the receipts). "
        "Links marked sponsored are Amazon Associate links: buying through them can earn this site a commission.</p>"
        '<table class="vt-table"><thead><tr><th scope="col">Product</th><th scope="col">Format</th><th scope="col">Capacity, as listed</th><th scope="col">Listing</th></tr></thead><tbody>%s</tbody></table>'
        '<p class="module-cta"><a class="btn btn-secondary" data-cc="guide-to-compare" href="%scompare/index.html">Compare all three side by side</a></p>'
        "</section>"
    ) % (esc(heading), rp, "".join(rows), rp)


def guide_card(g, path):
    rp = rel_prefix(path)
    return (
        '<a class="card guide-card" href="%sguides/%s.html"><span class="chip">%s</span>'
        "<h3>%s</h3><p>%s</p></a>" % (
            rp, esc(g["slug"]), esc(g["cluster"]), esc(g["title"]), esc(g["description"]))
    )


# ------------------------------------------------------------------ pages

PAGES = []


def add(path, title, desc, body, body_class="", extra_head="", jsonld=""):
    if not jsonld:
        jsonld = {"@context": "https://schema.org", "@type": "WebPage", "name": title,
                  "description": desc, "url": canon(path),
                  "isPartOf": {"@type": "WebSite", "name": SITE["brand"]["name"], "url": BASE}}
    PAGES.append((path, title, desc, page_shell(path, title, desc, body, body_class, extra_head, jsonld)))


def write_all():
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)
    for path, _t, _d, html_text in PAGES:
        out = PUBLIC / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_text, encoding="utf-8")
    (PUBLIC / ".nojekyll").write_text("", encoding="utf-8")


# ------------------------------------------------------------ index

def build_index():
    path = "index.html"
    hero = """
<section class="hero">
  <p class="kicker">A source-checked kitchen publication</p>
  <h1>%s</h1>
  <p class="hero-method">%s</p>
  <div class="hero-ctas">
    <a class="btn btn-primary" href="%scompare/index.html">Compare the three</a>
    <a class="btn btn-secondary" href="%sguides/index.html">Read the guides</a>
  </div>
</section>""" % (
        esc(SITE["brand"]["promise"]),
        esc(SITE["brand"]["method_line"]),
        rel_prefix(path), rel_prefix(path),
    )

    cat_page_for = {
        "Dual-basket air fryers": "shop/dual-basket-air-fryers.html",
        "Air fryer toaster ovens": "shop/air-fryer-toaster-ovens.html",
        "Single-basket air fryers": "shop/single-basket-air-fryers.html",
    }
    cards = []
    for pid in ("P1", "P2", "P3"):
        p = PRODUCTS_BY_ID[pid]
        cards.append("""
<article class="product-card">
  <div class="product-card-head"><h2>%s</h2>%s</div>
  <p class="product-format">%s &middot; %s</p>
  <dl class="product-specs">
    <div><dt>Capacity</dt><dd>%s</dd></div>
    <div><dt>Footprint</dt><dd>%s</dd></div>
  </dl>
  <div class="product-ctas">
    %s <span class="microbadge">sponsored</span>
    <a class="textlink" href="%s%s">Facts &amp; receipts</a>
  </div>
</article>""" % (
            esc(p["name_short"]), status_badge(p["status"]), esc(p["brand"]), esc(p["category"]),
            esc(p["capacity"]), cited_dims(p), buy_button(p), rel_prefix(path),
            esc(cat_page_for[p["category"]]),
        ))

    guide_cards = "".join(guide_card(g, path) for g in GUIDES["guides"][:6])

    tiles = []
    for c in PRODUCTS["categories"]:
        tiles.append(
            '<a class="tile" href="%s%s"><h3>%s</h3><p>%s</p></a>' % (
                rel_prefix(path),
                {"Dual-basket air fryers": "shop/dual-basket-air-fryers.html",
                 "Air fryer toaster ovens": "shop/air-fryer-toaster-ovens.html",
                 "Single-basket air fryers": "shop/single-basket-air-fryers.html"}[c["name"]],
                esc(c["name"]), esc(c["summary"])))

    body = """
%s
%s
<section class="strip-section">
  <div class="section-head"><h2>The verified three</h2><p>Three formats, one standard: every published figure comes from the official listing page, and the receipts are one click away.</p></div>
  <div class="product-grid">%s</div>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>Guides that answer one question each</h2><p>No top-ten lists. Each guide asks the question you actually have and answers it with checkable comparisons.</p></div>
  <div class="card-grid">%s</div>
  <p class="more-link"><a class="textlink" href="%sguides/index.html">All eight guides</a></p>
</section>
<section class="strip-section">
  <div class="section-head"><h2>Shop by format</h2><p>Every product sits in one of three countertop formats. Start with the format, then compare the numbers.</p></div>
  <div class="tile-grid">%s</div>
</section>
<section class="strip-section alt method-strip">
  <div class="section-head"><h2>The method, in one minute</h2><p>Every product fact on this site was read from an official Amazon listing page. The product register keeps the receipts: what was read, when, and from where. When something is unverified, the page says so instead of guessing.</p></div>
  <p><a class="btn btn-secondary" href="%sreview/methodology.html">How we check facts</a> <a class="btn btn-secondary" href="%sreview/flagged.html">What is still open</a></p>
</section>""" % (
        hero,
        "",
        "".join(cards),
        guide_cards,
        rel_prefix(path),
        "".join(tiles),
        rel_prefix(path), rel_prefix(path),
    )

    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE["brand"]["name"],
        "url": BASE,
        "description": desc_index,
        "publisher": {"@type": "Organization", "name": SITE["brand"]["name"], "url": BASE},
    }
    add(path, title_index, desc_index, body, body_class="home", jsonld=jsonld)


title_index = "The Crisp Counter - air fryer decisions, minus the hype"
desc_index = ("A source-checked guide to three countertop air fryers: dual-basket, French-door oven and "
              "single-basket. Every figure was read from an official Amazon listing page.")


# ------------------------------------------------------------ guides

def build_guides():
    # hub
    path = "guides/index.html"
    cards = "".join(guide_card(g, path) for g in GUIDES["guides"])
    body = """
%s
<section class="page-head"><h1>Guides</h1>
<p>One question per guide, answered with checkable comparisons and none of the hype. Product facts are cited to the official listing pages; where something is unknown, the guide says so.</p></section>
<div class="card-grid">%s</div>
<section class="strip-section alt">
  <div class="section-head"><h2>What comes next</h2><p>The queue below is the publishing cadence - one new guide every 14 days. Topics switch to measured search queries once Search Console and the collector have 14 days of data.</p></div>
  <table class="data-table"><thead><tr><th scope="col">Due</th><th scope="col">Planned guide</th></tr></thead><tbody>%s</tbody></table>
</section>""" % (
        breadcrumb(path, [("Home", ""), ("Guides", "")]),
        cards,
        "".join("<tr><td>%s</td><td>%s</td></tr>" % (esc(q["due_utc"]), esc(q["title"])) for q in CALENDAR["queue"]),
    )
    add(path, "Guides - one question per guide - The Crisp Counter",
        "Eight question-shaped buying guides for countertop air fryers: format, capacity, cleanup and the "
        "multi-function question. Answers first, hype nowhere, facts cited.",
        body, body_class="hub")

    # articles
    for g in GUIDES["guides"]:
        gp = "guides/%s.html" % g["slug"]
        body_html = (CONTENT / ("guides/%s.html" % g["slug"])).read_text(encoding="utf-8")
        module = verified_three_module(gp)
        related = []
        for slug in g["sibling_links"]:
            s = GUIDES_BY_SLUG.get(slug)
            if s:
                related.append(guide_card(s, gp))
        catpage = g["category_page"]
        related_note = '<p class="module-note">Start with the <a href="%s%s" data-cc="guide-to-compare">side-by-side comparison</a>, or browse <a href="%s%s">the shop</a>.</p>' % (
            rel_prefix(gp), "compare/index.html", rel_prefix(gp), catpage)
        body = """
%s
<article class="article">
  <header class="article-head">
    <p class="kicker">%s guide</p>
    <h1>%s</h1>
    <p class="article-meta">By The Crisp Counter editors &middot; %s &middot; facts cited to official listing pages</p>
  </header>
  <div class="article-body">
  %s
  </div>
  %s
  %s
  <section class="related"><h2>Keep going</h2><div class="card-grid">%s</div>%s</section>
</article>""" % (
            breadcrumb(gp, [("Home", ""), ("Guides", "guides/index.html"), (g["title"], "")]),
            esc(g["cluster"]), esc(g["title"]), PUB_DATE,
            body_html,
            module,
            related_note,
            "".join(related),
            "",
        )
        jsonld = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": g["title"],
            "description": g["description"],
            "datePublished": PUB_DATE,
            "dateModified": PUB_DATE,
            "author": {"@type": "Organization", "name": "The Crisp Counter editors"},
            "publisher": {"@type": "Organization", "name": SITE["brand"]["name"], "url": BASE},
            "mainEntityOfPage": canon(gp),
            "image": BASE + "assets/og-image.png",
        }
        add(gp, "%s - The Crisp Counter" % g["title"], g["description"], body,
            body_class="article-page", jsonld=jsonld)


# ------------------------------------------------------------ shop

CAT_SLUGS = {
    "Dual-basket air fryers": ("dual-basket-air-fryers", ["basket-or-oven-style-air-fryer-what-to-compare", "how-much-air-fryer-capacity-does-a-family-of-four-need"]),
    "Air fryer toaster ovens": ("air-fryer-toaster-ovens", ["questions-before-a-multi-function-kitchen-appliance", "air-fryer-accessories-which-extras-earn-their-drawer-space"]),
    "Single-basket air fryers": ("single-basket-air-fryers", ["air-fryer-capacity-checklist", "counter-space-and-cleanup-trade-offs"]),
}


def build_shop():
    path = "shop/index.html"
    tiles = []
    for c in PRODUCTS["categories"]:
        slug, _ = CAT_SLUGS[c["name"]]
        tiles.append('<a class="tile" href="%s"><h2>%s</h2><p>%s</p><span class="tile-meta">%d verified product%s</span></a>' % (
            esc(slug + ".html"), esc(c["name"]), esc(c["summary"]),
            len(c["products"]), "" if len(c["products"]) == 1 else "s"))
    held_note = """
<aside class="note-card held-note">
<h2>Why only three products are here</h2>
<p>Five product links were submitted to this project. Three resolve to the verified air-fryer listings above. The other two (P4, P5) were observed to open to listings outside the air-fryer scope, and their identity was never confirmed in an enrolled Associates workflow - so they are registered but never published here. See <a href="%sreview/flagged.html">Flagged for review</a> and the <a href="%sdata/products.html">product register</a> for the full record.</p>
</aside>""" % (rel_prefix(path), rel_prefix(path))
    body = """
%s
<section class="page-head"><h1>Shop the verified three</h1>
<p>Each listing below was checked line by line against its official Amazon page. Prices and star ratings are deliberately absent: those may only be shown when Amazon serves the content or it arrives through the Amazon API - neither is connected here, so we show the facts we can cite.</p></section>
<div class="tile-grid">%s</div>
%s""" % (breadcrumb(path, [("Home", ""), ("Shop", "")]), "".join(tiles), held_note)
    add(path, "Shop the verified three - The Crisp Counter",
        "Three countertop air fryers, every fact read from its official Amazon listing page: a dual-basket "
        "model, a French-door multi-function oven and a single-basket classic.",
        body, body_class="shop-hub")

    for name, (slug, guide_slugs) in CAT_SLUGS.items():
        cpath = "shop/%s.html" % slug
        cat = next(c for c in PRODUCTS["categories"] if c["name"] == name)
        prods = [PRODUCTS_BY_ID[pid] for pid in cat["products"]]
        prod_html = ""
        for p in prods:
            prod_html += """
<article class="product-detail">
  <div class="product-card-head"><h2>%s</h2>%s</div>
  <p class="product-format">%s &middot; model %s</p>
  <p class="listing-title">&ldquo;%s&rdquo;</p>
  %s
  <div class="product-ctas">
    %s <span class="microbadge">sponsored</span>
    <span class="microbadge">earnings notice: as an Amazon Associate we earn from qualifying purchases</span>
  </div>
  <p class="fact-note">Facts last read from the official listing page on %s. The <a href="%sdata/products.html">product register</a> holds the receipt; prices and ratings are not shown (see the <a href="%sreview/methodology.html">method</a>).</p>
</article>""" % (
                esc(p["name_short"]), status_badge(p["status"]), esc(p["brand"]), esc(p["model_number"]),
                esc(p["name_listing"]), fact_table(p), buy_button(p),
                esc(p["facts_last_read_utc"]), rel_prefix(cpath), rel_prefix(cpath))
        related = "".join(guide_card(GUIDES_BY_SLUG[s], cpath) for s in guide_slugs if s in GUIDES_BY_SLUG)
        desc = "%s: verified facts, the official listing and the guides that answer the buying questions." % name
        body = """
%s
<section class="page-head"><h1>%s</h1><p>%s</p></section>
%s
<section class="related"><h2>Guides for this format</h2><div class="card-grid">%s</div></section>
<p class="module-cta"><a class="btn btn-secondary" data-cc="guide-to-compare" href="%scompare/index.html">Compare all three side by side</a></p>""" % (
            breadcrumb(cpath, [("Home", ""), ("Shop", "shop/index.html"), (name, "")]),
            esc(name), esc(cat["summary"]), prod_html, related, rel_prefix(cpath))
        add(cpath, "%s - verified facts - The Crisp Counter" % name, desc, body, body_class="shop-cat")


# ------------------------------------------------------------ compare

def build_compare():
    path = "compare/index.html"
    rows = []
    for pid in ("P1", "P2", "P3"):
        p = PRODUCTS_BY_ID[pid]
        rows.append(
            "<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td>%s in</td><td>%s</td><td class=\"cell-cta\">%s <span class=\"microbadge\">sponsored</span></td></tr>" % (
                esc(p["name_short"]), esc(p["category"]), esc(p["capacity"]), cited_dims(p),
                "%.2f L/cm" % cpd(p), buy_button(p))
        )
    chooser_data = {
        "questions": [
            {"id": "depth", "q": "How much counter depth can you give it?",
             "options": [{"label": "Under 14 inches", "key": "shallow"}, {"label": "14-17 inches", "key": "mid"}, {"label": "More than 17 inches", "key": "deep"}, {"label": "It lives in a cupboard", "key": "stored"}]},
            {"id": "cook", "q": "What do you cook most weeks?",
             "options": [{"label": "Snacks and sides for one or two", "key": "snacks"}, {"label": "Full meals for a family", "key": "family"}, {"label": "Batch prep and big trays", "key": "batch"}]},
            {"id": "cleanup", "q": "How do you feel about washing up?",
             "options": [{"label": "Two basket parts, quick rinse", "key": "rinse"}, {"label": "Dishwasher everything", "key": "dishwasher"}, {"label": "Fewer parts, whatever the size", "key": "fewparts"}]},
        ]
    }
    body = """
%s
<div class="sticky-compare-bar" aria-label="Comparison page sections"><a href="#chooser">Chooser</a><a href="#table">Table</a><a href="#howto">How to read</a><a href="#status">Status</a></div>
<section class="page-head"><h1>Compare the verified three</h1>
<p>Three formats that cover the countertop range: a 6-litre dual-basket, a 24.6-litre French-door oven and an 8-quart single basket. The table holds only what their official listing pages state - read 2026-11-16, receipts in the product register.</p></section>
<section id="chooser" class="strip-section">
  <div class="section-head"><h2>Which one fits your kitchen?</h2><p>Three questions. The chooser names the spec priorities to look for - it recommends formats, never products, because attribution and performance claims stay unverified by design.</p></div>
  <div class="chooser" id="chooser-app" aria-live="polite"></div>
  <script type="application/json" id="chooser-data">%s</script>
</section>
<section id="table" class="strip-section alt">
  <div class="section-head"><h2>The verified fact table</h2><p>Capacity is listed exactly as each listing states it. Footprint is the listed depth &times; width &times; height. The last column is the listing's own capacity divided by its listed depth in centimetres - the arithmetic is shown in the <a href="%scounter-space.html">counter-space method</a>.</p></div>
  <div class="table-scroll"><table class="data-table compare-table"><thead><tr><th scope="col">Product</th><th scope="col">Format</th><th scope="col">Capacity, as listed</th><th scope="col">Footprint (D &times; W &times; H)</th><th scope="col">Capacity per cm of depth</th><th scope="col">Listing</th></tr></thead><tbody>%s</tbody></table></div>
</section>
<section id="howto" class="strip-section">
  <div class="section-head"><h2>How to read this table</h2></div>
  <ul class="prose-list">
    <li><strong>Format first.</strong> A drawer and a door-front oven are different tools; the <a href="%sguides/basket-or-oven-style-air-fryer-what-to-compare.html">format guide</a> walks the trade-offs.</li>
    <li><strong>Capacity labels are marketing territory.</strong> "Serves X" hides batch logic; the <a href="%sguides/air-fryer-capacity-checklist.html">capacity checklist</a> gives you the five checks that survive.</li>
    <li><strong>Depth is the quiet constraint.</strong> The tallest capacity means nothing if the body eats your counter; compare capacity per centimetre of depth and read the <a href="%scounter-space.html">method</a>.</li>
    <li><strong>No prices, no stars.</strong> Those appear only when Amazon serves the content or the API is connected; today neither is. The listing links take you to the live page for the price.</li>
  </ul>
</section>
<section id="status" class="strip-section alt">
  <div class="section-head"><h2>What is verified, and what is not</h2></div>
  <ul class="prose-list">
    <li>Listing titles, brands, models, capacities, dimensions and listed features: <span class="badge badge-verified">verified (carried)</span> - read from the official pages, last read 2026-11-16.</li>
    <li>Click attribution: <span class="badge badge-unverified">unverified</span> - the one-link-per-product test in Associates Central has not been run yet (FLG-07).</li>
    <li>Two submitted products (P4, P5): <span class="badge badge-held">held</span> - outside the air-fryer scope and unconfirmed, so they appear nowhere on this page.</li>
    <li>Prices, ratings and popularity: <span class="badge badge-held">not shown by rule</span> - see the <a href="%sreview/methodology.html">methodology</a>.</li>
  </ul>
</section>""" % (
        breadcrumb(path, [("Home", ""), ("Compare", "")]),
        json.dumps(chooser_data, ensure_ascii=False),
        rel_prefix(path), "".join(rows),
        rel_prefix(path), rel_prefix(path), rel_prefix(path),
        rel_prefix(path),
    )
    add(path, "Compare the verified three - The Crisp Counter",
        "Side-by-side facts for three air fryer formats: listed capacity, footprint, capacity per centimetre "
        "of depth, plus a chooser that names your spec priorities.",
        body, body_class="compare-page",
        extra_head='<script src="%sassets/js/chooser.js" defer></script>' % rel_prefix(path),
        jsonld={"@context": "https://schema.org", "@type": "WebPage", "name": "Compare the verified three",
                "description": "Side-by-side verified facts and a three-question chooser for three air fryer formats.",
                "url": canon(path), "isPartOf": {"@type": "WebSite", "name": SITE["brand"]["name"], "url": BASE}})


# ------------------------------------------------------------ counter-space

def build_counter_space():
    path = "counter-space.html"
    rows = []
    for pid in ("P1", "P2", "P3"):
        p = PRODUCTS_BY_ID[pid]
        cap = capacity_l(p)
        dcm = depth_cm(p["dimensions"])
        cap_disp = p["capacity"]
        if "quart" in p["capacity"].lower():
            cap_disp = "%s (listed) = %.2f L" % (p["capacity"], cap)
        rows.append(
            "<tr><th scope=\"row\">%s</th><td>%s</td><td>%.2f cm (%s in)</td><td><strong>%.2f L/cm</strong></td><td class=\"arith\">%.2f &divide; %.2f</td></tr>" % (
                esc(p["name_short"]), esc(cap_disp), dcm, cited_dims(p).split('"')[0], cap / dcm, cap, dcm)
        )
    body = """
%s
<section class="page-head"><h1>Counter-space math: capacity per centimetre of depth</h1>
<p>Counter depth is the constraint nobody puts on the box. Kitchens typically give you about 60 to 65&nbsp;cm of counter depth before the backsplash, and an air fryer that needs breathing room at the wall eats into that fast. This page turns capacity and footprint into one number you can compare honestly.</p></section>
<section class="strip-section">
  <div class="section-head"><h2>The method</h2></div>
  <p class="formula">capacity per cm of depth = listed capacity in litres &divide; listed depth in centimetres</p>
  <ul class="prose-list">
    <li>Capacity and depth come straight from the official listing - no rounding, no reinterpretation. Where the listing states quarts, the conversion is shown (1&nbsp;qt&nbsp;=&nbsp;0.946&nbsp;L).</li>
    <li>Depth is the first dimension in every listing's footprint line. Centimetres come from inches at 2.54 exactly.</li>
    <li>Higher is better: more litres of listed capacity per centimetre of counter depth consumed.</li>
    <li>The number is a space proxy, not a performance claim. It says nothing about how fast or evenly anything cooks.</li>
  </ul>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>The verified three, computed</h2><p>Every input below was read from an official listing page (last read 2026-11-16); the division is shown so you can check the arithmetic.</p></div>
  <div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">Product</th><th scope="col">Capacity</th><th scope="col">Depth</th><th scope="col">Capacity per cm</th><th scope="col">Shown as</th></tr></thead><tbody>%s</tbody></table></div>
  <p class="module-note">What the table says in practice: the French-door format trades a deep body for sheet-pan capacity, which is why its litres-per-centimetre leads while its listed footprint is the largest. The single basket's square drawer buys height instead of depth. Whether that trade suits your counter is what the <a data-cc="guide-to-compare" href="%scompare/index.html">comparison table</a> is for - measure first, then compare.</p>
</section>
<section class="strip-section">
  <div class="section-head"><h2>Run it on your shortlist</h2></div>
  <ol class="prose-list">
    <li>Write down the capacity exactly as listed (quarts or litres).</li>
    <li>Write down the depth exactly as listed (the first number in the footprint).</li>
    <li>Convert: litres = quarts &times; 0.946; centimetres = inches &times; 2.54.</li>
    <li>Divide. Now compare across your whole shortlist - including models that are not on this site.</li>
    <li>Then add the human factors the number cannot see: door or drawer swing, the clearance the manual requires at the back, and whether the thing lives on the counter or in a cupboard. The <a href="%sguides/will-it-fit-measuring-your-counter-for-an-air-fryer.html">five-minute measuring routine</a> covers all three.</li>
  </ol>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>Why no illustrative made-up numbers?</h2><p>Because a fabricated example is how a fact-checked site starts lying. Every number on this page is an input from an official listing, and the only arithmetic is division you can redo in your head. When more products are verified, they join the table with the same inputs - nothing else changes.</p></div>
</section>""" % (
        breadcrumb(path, [("Home", ""), ("Counter-space math", "")]),
        "".join(rows),
        "", rel_prefix(path),
    )
    add(path, "Counter-space math: capacity per centimetre of depth - The Crisp Counter",
        "Compare air fryer footprints honestly: listed capacity divided by listed depth for the verified "
        "three, arithmetic shown, plus the routine to run it on any shortlist.",
        body, body_class="method-page",
        jsonld={"@context": "https://schema.org", "@type": "WebPage", "name": "Counter-space math",
                "description": "Capacity per centimetre of counter depth for the verified three, with the method shown.",
                "url": canon(path), "isPartOf": {"@type": "WebSite", "name": SITE["brand"]["name"], "url": BASE}})


# ------------------------------------------------------------ data pages

def build_data_pages():
    # products
    path = "data/products.html"
    rows = []
    for p in PRODUCTS["products"]:
        rows.append(
            "<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                esc(p["id"]),
                esc(p.get("name_short") or "-"),
                esc(p.get("asin") or p.get("intended_asin_provisional") or "-"),
                status_badge(p["status"]),
                amazon_link_or_text(p["official_listing_url"], "official listing") if p.get("official_listing_url") else "-",
                esc(p.get("facts_last_read_utc") or "-"),
            ))
    held_rows = []
    for l in INTENT["links"]:
        if not l["published_outbound_url"]:
            held_rows.append(
                "<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    esc(l["product_id"]), text_url(l["submitted_url"]),
                    esc(l["intended_asin"]) + " (provisional)",
                    esc(l["confirmation_date_utc"]), esc(l["attribution_status"])))
    body = """
%s
<section class="page-head"><h1>Product register</h1>
<p>The canonical record of every product this project has been given, verified or held. Values were read from official Amazon listing pages by the predecessor register (last re-read 2026-11-16/17) and carried with their citations; this build environment cannot reach Amazon, so nothing was re-derived here - flagged as <a href="%sreview/flagged.html#FLG-03">FLG-03</a>.</p></section>
<section class="strip-section">
  <div class="section-head"><h2>The verified three</h2></div>
  <div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">ID</th><th scope="col">Product</th><th scope="col">ASIN</th><th scope="col">Status</th><th scope="col">Source</th><th scope="col">Last read</th></tr></thead><tbody>%s</tbody></table></div>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>Held and never published</h2><p>These two submitted links were observed to open to listings outside the air-fryer scope. Their intended ASINs are provisional; the owner has not confirmed identity in an enrolled Associates workflow, so they have no product page, no outbound link and no published fact.</p></div>
  <div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">ID</th><th scope="col">Submitted link</th><th scope="col">Intended ASIN</th><th scope="col">Recorded</th><th scope="col">Status</th></tr></thead><tbody>%s</tbody></table></div>
</section>
<section class="strip-section">
  <div class="section-head"><h2>Product-intent confirmation record</h2><p>For each submitted link, the intended ASIN, the official listing URL, the confirmation date and its source - and, in a field that is never merged with them, the observed redirect target. The short-link path codes are not ASINs; both identifier kinds are kept apart.</p></div>
  <div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">ID</th><th scope="col">Intended ASIN</th><th scope="col">Official listing URL</th><th scope="col">Confirmed</th><th scope="col">Confirmation source</th><th scope="col">Observed redirect (separate field)</th></tr></thead><tbody>%s</tbody></table></div>
</section>""" % (
        breadcrumb(path, [("Home", ""), ("Product register", "")]),
        rel_prefix(path), "".join(rows), "".join(held_rows),
        "".join(
            "<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s on %s &rarr; %s</td></tr>" % (
                esc(l["product_id"]), esc(l["intended_asin"]),
                text_url(l["official_listing_url"]),
                esc(l["confirmation_date_utc"]), esc(l["confirmation_source"]),
                esc(l["observed_redirect"]["observed_asin"]),
                esc(l["observed_redirect"]["date_utc"]),
                text_url(l["observed_redirect"]["final_url_without_query"]))
            for l in INTENT["links"]),
    )
    add(path, "Product register - The Crisp Counter",
        "Every product received, verified or held: identifiers, official listing URLs, confirmation dates "
        "and sources, observed redirects kept in separate fields.",
        body, body_class="dashboard")

    # sources
    path = "data/sources.html"
    srows = "".join(
        "<tr><th scope=\"row\">%s</th><td>%s</td><td>%s</td><td><span class=\"badge badge-%s\">%s</span></td><td>%s</td></tr>" % (
            esc(s["id"]), esc(s["title"]),
            (amazon_link_or_text(s["url"], "link") if any(d in s["url"] for d in AMAZON_DOMAINS)
             else '<a href="%s" rel="noopener" target="_blank">link</a>' % esc(s["url"])),
            "verified" if s["status"] == "fetched" else "unverified", esc(s["status"]),
            esc(s["use"]))
        for s in SOURCES["sources"])
    body = """
%s
<section class="page-head"><h1>Source register</h1>
<p>Every published value points at one of these sources. A source marked <span class="badge badge-verified">fetched</span> was actually retrieved and read. A source marked <span class="badge badge-unverified">cited</span> is supplied for manual review: this build environment's network allowlist excludes the official pages, so their wording was not re-verified here (<a href="%sreview/flagged.html#FLG-05">FLG-05</a>).</p></section>
<div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">URL</th><th scope="col">Status</th><th scope="col">Used for</th></tr></thead><tbody>%s</tbody></table></div>""" % (
        breadcrumb(path, [("Home", ""), ("Source register", "")]),
        rel_prefix(path), srows,
    )
    add(path, "Source register - The Crisp Counter",
        "The citation backbone of the site: official Amazon, FTC and Google Search Central sources with "
        "fetched/cited status for every published value.",
        body, body_class="dashboard")

    # ledger
    path = "data/ledger.html"
    cols = "".join("<th scope=\"col\">%s</th>" % esc(c) for c in LEDGER["columns"])
    body = """
%s
<section class="page-head"><h1>Campaign ledger</h1>
<p>Defined on 2026-11-19 and empty on purpose. A row is added only from an authorised first-party report - for example an Associates Central report the owner exports - with the report reference and who obtained it. Nothing estimated, nothing copied from third parties, and the site's own click counter is never a reported order.</p></section>
<section class="strip-section">
  <div class="table-scroll"><table class="data-table"><thead><tr>%s</tr></thead><tbody></tbody></table></div>
  <p class="module-note">%s</p>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>Why there is no forecast on this page</h2></div>
  <p>The Associates Operating Agreement states that Amazon makes no representation about the traffic or commission income an Associate can expect. This site goes further: until an authorised report lands, the ledger has no rows, no conversion score and no revenue projection - and when rows land, they carry their report reference so every number keeps a receipt.</p>
  <p>What is measured today, honestly and separately: the <a href="%sdata/events.html">five first-party events</a> (no cookies, aggregated in the visitor's browser).</p>
</section>""" % (
        breadcrumb(path, [("Home", ""), ("Campaign ledger", "")]),
        cols, esc(LEDGER["status"]), rel_prefix(path),
    )
    add(path, "Campaign ledger - The Crisp Counter",
        "An empty-by-rule ledger: rows are added only from authorised first-party Associates reports with "
        "references. No estimates, no forecasts, no third-party figures.",
        body, body_class="dashboard")

    # events
    path = "data/events.html"
    erows = "".join(
        "<tr><th scope=\"row\">%s <code>%s</code></th><td>%s</td><td>%s</td></tr>" % (
            esc(e["id"]), esc(e["name"]), esc(e["definition"]), esc(e["privacy"]))
        for e in EVENTS["events"])
    pl = "".join("<li>%s</li>" % esc(x) for x in EVENTS["privacy_commitments"])
    body = """
%s
<section class="page-head"><h1>Events &amp; privacy</h1>
<p>Five defined events, recorded first-party and cookieless. The counter aggregates in the visitor's browser; the optional collector ships as runnable reference code for whatever host is chosen (see <a href="%ssuggestions.html">suggestion SG-02</a>).</p></section>
<section class="strip-section">
  <div class="section-head"><h2>The five events</h2></div>
  <div class="table-scroll"><table class="data-table"><thead><tr><th scope="col">Event</th><th scope="col">Definition</th><th scope="col">Privacy</th></tr></thead><tbody>%s</tbody></table></div>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>Privacy commitments</h2></div>
  <ul class="prose-list">%s</ul>
  <p class="module-note">Live, local-only counts from this browser (nothing leaves your machine unless a collector URL is configured):</p>
  <pre id="cc-live-counts" class="codeblock">(no events recorded yet in this browser)</pre>
</section>
<section class="strip-section">
  <div class="section-head"><h2>Self-hosting the collector</h2></div>
  <p>The endpoint is a dependency-free Python file in the repository at <code>collector/app.py</code>. Run it, point <code>window.CC_COLLECT_URL</code> at it, and events flow as anonymous JSON lines with a 90-day default rotation. Hosting decision: open question <a href="%sopen-questions.html#Q-06">Q-06</a>.</p>
</section>""" % (
        breadcrumb(path, [("Home", ""), ("Events & privacy", "")]),
        rel_prefix(path), erows, pl, rel_prefix(path),
    )
    add(path, "Events and privacy - The Crisp Counter",
        "The five first-party events, their privacy rules, and the self-hosted collector contract. "
        "No cookies, no fingerprinting, aggregation in the visitor's browser.",
        body, body_class="dashboard", extra_head='<script src="%sassets/js/livecounts.js" defer></script>' % rel_prefix(path),
        jsonld={"@context": "https://schema.org", "@type": "WebPage", "name": "Events and privacy",
                "description": "Five first-party events, privacy rules and the collector contract.",
                "url": canon(path), "isPartOf": {"@type": "WebSite", "name": SITE["brand"]["name"], "url": BASE}})


# ------------------------------------------------------------ review pages

def build_review_pages():
    # flagged
    path = "review/flagged.html"
    def flag_card(f, status_cls=""):
        ev = []
        for e in f.get("evidence", []):
            if e.startswith("http"):
                if any(d in e for d in AMAZON_DOMAINS):
                    ev.append("<li>%s</li>" % amazon_link_or_text(e, "official source" if "amazon.com/dp" in e or "affiliate-program" in e or "sell.amazon" in e else e))
                else:
                    ev.append('<li><a href="%s" rel="noopener" target="_blank">%s</a></li>' % (esc(e), esc(e)))
            else:
                ev.append("<li><code>%s</code> (repository record)</li>" % esc(e))
        return """
<article class="flag-card %s" id="%s">
  <div class="flag-head"><h3>%s %s</h3>%s</div>
  <p><strong>What:</strong> %s</p>
  %s
  <p><strong>Evidence:</strong></p><ul class="evidence">%s</ul>
  <p><strong>Unblocks by:</strong> %s</p>
</article>""" % (
            status_cls, esc(f["id"]), esc(f["id"]), esc(f["title"]), "",
            esc(f.get("what", f.get("resolution", f.get("note", "")))),
            ("<p><strong>Why it matters:</strong> %s</p>" % esc(f["why_it_matters"])) if f.get("why_it_matters") else "",
            "".join(ev) or "<li>Recorded in the registers; see the links above.</li>",
            esc(f.get("unblock_action", f.get("date_utc", "-"))),
        )
    open_cards = "".join(flag_card(f) for f in FLAGS["open"])
    res_cards = "".join(
        "<article class='flag-card resolved'><div class='flag-head'><h3>%s %s</h3></div><p>%s</p><p class='flag-date'>Resolved %s.</p></article>" % (
            esc(f["id"]), esc(f["title"]), esc(f["resolution"]), esc(f["date_utc"]))
        for f in FLAGS["resolved"])
    hist_cards = "".join(
        "<article class='flag-card historical'><div class='flag-head'><h3>%s</h3></div><p>%s</p></article>" % (
            esc(f["title"]), esc(f["note"]))
        for f in FLAGS["historical"])
    body = """
%s
<section class="page-head"><h1>Flagged for review</h1>
<p>Open items do not block publication; they are published so they can be reviewed with their sources attached. Resolved items keep their receipts. Historical records live in the imported predecessor archive. Unverified things never silently fill in.</p></section>
<section class="strip-section"><div class="section-head"><h2>Open (%d)</h2></div>%s</section>
<section class="strip-section alt"><div class="section-head"><h2>Resolved</h2></div>%s</section>
<section class="strip-section"><div class="section-head"><h2>Historical</h2></div>%s</section>""" % (
        breadcrumb(path, [("Home", ""), ("Flagged for review", "")]),
        len(FLAGS["open"]), open_cards, res_cards, hist_cards,
    )
    add(path, "Flagged for review - The Crisp Counter",
        "The open, resolved and historical flag register: what is unverified, why it matters, the evidence "
        "links and the action that unblocks each item.",
        body, body_class="dashboard")

    # decisions
    path = "review/decisions.html"
    drows = "".join(
        "<tr><th scope=\"row\">%s</th><td>%s</td><td><span class=\"badge badge-%s\">%s</span></td><td>%s</td><td>%s</td></tr>" % (
            esc(d["id"]), esc(d["title"]),
            "verified" if d["status"] == "Recorded" else "held", esc(d["status"]),
            esc(d["date_utc"]), esc(d["rationale"]))
        for d in DECISIONS["decisions"])
    body = """
%s
<section class="page-head"><h1>Decision log</h1>
<p>Every design, editorial and compliance decision this build made, with its rationale and date. Where a decision carries a predecessor register's call, it says so. Partly-recorded rows name the open part instead of pretending it is settled.</p></section>
<div class="table-scroll"><table class="data-table decisions-table"><thead><tr><th scope="col">ID</th><th scope="col">Decision</th><th scope="col">Status</th><th scope="col">Date</th><th scope="col">Rationale</th></tr></thead><tbody>%s</tbody></table></div>""" % (
        breadcrumb(path, [("Home", ""), ("Decision log", "")]), drows)
    add(path, "Decision log - The Crisp Counter",
        "Twenty-one recorded decisions with rationale and dates: brand, voice, link rules, the evidence "
        "rule, measurement design and the publication structure.",
        body, body_class="dashboard")

    # methodology
    path = "review/methodology.html"
    body = """
%s
<section class="page-head"><h1>Methodology: how every fact gets published</h1>
<p>This site's only edge is that it does not guess. Here is the discipline, line by line.</p></section>
<section class="strip-section">
  <div class="section-head"><h2>The rules</h2></div>
  <ol class="prose-list">
    <li><strong>One value, one source.</strong> A product fact is published only with the official listing page it was read from and the date it was read. The product register keeps that pair for every field.</li>
    <li><strong>Blank beats invented.</strong> If a value cannot be confirmed from an official source, the field stays blank and a flag explains why. Nothing is inferred to make a table look complete.</li>
    <li><strong>Identifiers are typed.</strong> The intended ASIN, the short-link path code and the observed redirect target are three different things and live in three different fields. They are never merged.</li>
    <li><strong>Carried values keep their provenance.</strong> Facts read by the predecessor register were imported verbatim with their session records; this environment cannot reach Amazon, so the carried values cite their original reads instead of pretending to be re-verified (FLG-03).</li>
    <li><strong>Withheld stays withheld.</strong> Prices, availability, star ratings, review counts and popularity badges are displayed only when Amazon serves the content or the Amazon API supplies it. Neither is connected, so none appear.</li>
    <li><strong>Measurement is separated by kind.</strong> First-party click counts, authorised Associates reports and anything else each keep their own store. The site's counter is never presented as a reported order.</li>
    <li><strong>Claims need evidence.</strong> No trending, popularity or superiority claims anywhere reader-facing. Guides compare checkable fields; the chooser recommends formats, never products.</li>
    <li><strong>Compliance gates run in the build.</strong> The generator adds the disclosure, the sponsored rel and the tag parameter; the check suite fails the build if any page loses them.</li>
  </ol>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>Reproducibility</h2></div>
  <p>The whole site is two standard-library scripts: <code>build.py</code> renders from the registers, <code>check.py</code> verifies the output. CI runs both on every push, and the deployment only happens after the checks pass on a clean checkout. The registers are plain JSON - a reviewer can diff a claim against its source line by line.</p>
  <p>The imported predecessor archive (verbatim, with a provenance README) is at <code>data/imported/zone4/</code> in the repository; its dated verification session records back every carried fact.</p>
</section>""" % breadcrumb(path, [("Home", ""), ("Methodology", "")])
    add(path, "Methodology - how every fact is checked - The Crisp Counter",
        "The line-by-line verification rules: one value one source, blank beats invented, typed identifiers, "
        "carried provenance, withheld values and build-time compliance gates.",
        body, body_class="method-page")


# ------------------------------------------------------------ suggestions & questions

def build_suggestions():
    path = "suggestions.html"
    order = {"adopted": 0, "needs a decision": 1, "needs a decision (owner action)": 1, "under review": 2, "proposed": 3}
    groups = {}
    for s in SUGGESTIONS["suggestions"]:
        groups.setdefault(s["status"], []).append(s)
    status_order = sorted(groups.keys(), key=lambda k: order.get(k, 9))
    sections = []
    for st in status_order:
        cls = "verified" if st == "adopted" else ("unverified" if st == "proposed" else "held")
        cards = []
        for s in groups[st]:
            ev = "".join('<li><a href="%s" rel="noopener" target="_blank">%s</a></li>' % (esc(e), esc(e))
                         if e.startswith("http") and not any(d in e for d in AMAZON_DOMAINS)
                         else ("<li>%s</li>" % text_url(e) if any(d in e for d in AMAZON_DOMAINS)
                               else "<li><code>%s</code> (repository record)</li>" % esc(e))
                         for e in s["evidence"])
            cards.append("""
<article class="suggestion-card" id="%s">
  <div class="flag-head"><h3>%s %s</h3><span class="badge badge-%s">%s</span></div>
  <p><strong>What:</strong> %s</p>
  <p><strong>Why:</strong> %s</p>
  <p class="sugg-meta"><strong>Effort:</strong> %s &middot; <strong>Risk:</strong> %s &middot; <strong>Category:</strong> %s</p>
  <p><strong>Decision needed:</strong> %s</p>
  <p><strong>Evidence:</strong></p><ul class="evidence">%s</ul>
</article>""" % (
                esc(s["id"]), esc(s["id"]), esc(s["title"]),
                cls, esc(s["status"]), esc(s["what"]), esc(s["why"]),
                esc(s["effort"]), esc(s["risk"]), esc(s["category"]),
                esc(s["decision_needed"]), ev))
        sections.append(
            '<section class="strip-section%s"><div class="section-head"><h2>%s</h2></div>%s</section>' % (
                " alt" if len(sections) % 2 else "", esc(st), "".join(cards)))
    body = """
%s
<section class="page-head"><h1>Suggestions</h1>
<p>This page is the review queue. Every proposed change lands here first - what it is, why it matters, what it costs, what could go wrong, and the decision it needs. <strong>Nothing is implemented from a suggestion until someone reviews it and picks a path.</strong> To act on one: check its evidence, set its status to &ldquo;under review&rdquo; in <code>data/suggestions.json</code>, record the choice in <code>data/decisions.json</code>, and move the row to adopted or declined with a reason.</p></section>
%s""" % (breadcrumb(path, [("Home", ""), ("Suggestions", "")]), "".join(sections))
    add(path, "Suggestions - review before we build - The Crisp Counter",
        "The suggestion queue: each proposal with evidence, effort, risk and the decision it needs, "
        "grouped by status so a reviewer picks the path before anything changes.",
        body, body_class="dashboard")


def build_open_questions():
    path = "open-questions.html"
    qrows = []
    for q in QUESTIONS["questions"]:
        qrows.append("""
<article class="suggestion-card" id="%s">
  <div class="flag-head"><h3>%s</h3></div>
  <p class="q-title">%s</p>
  <p><strong>Blocks:</strong> %s</p>
  <p><strong>What we have:</strong> %s</p>
  <p><strong>What is missing:</strong> %s</p>
  <p><strong>How to discover it:</strong> %s</p>
</article>""" % (
            esc(q["id"]), esc(q["id"]), esc(q["question"]), esc(q["why_it_blocks"]),
            esc(q["have"]), esc(q["missing"]), esc(q["discovery"])))
    body = """
%s
<section class="page-head"><h1>Open questions</h1>
<p>The decision inputs: the questions, the information already in hand, the information missing, and how to discover it. <strong>No decision downstream of a question moves until the question is answered and recorded in the decision log.</strong> This is the list to work through before choosing paths on the suggestions page.</p></section>
%s""" % (breadcrumb(path, [("Home", ""), ("Open questions", "")]), "".join(qrows))
    add(path, "Open questions - what we need answered before deciding - The Crisp Counter",
        "Twelve decision-input questions: what blocks each decision, what information exists, what is "
        "missing, and the concrete step that discovers it.",
        body, body_class="dashboard")


# ------------------------------------------------------------ exec summary & about & 404

def build_exec_summary():
    path = "executive-summary.html"
    body = """
%s
<section class="page-head"><h1>Executive summary</h1>
<p>The whole project, stated plainly: what was built, what is verified, what is held, and what happens next.</p></section>
<section class="strip-section">
  <div class="section-head"><h2>The site</h2></div>
  <p><strong>%s</strong> is a source-checked Amazon Associates publication for countertop air fryers, live on GitHub Pages. It reads like a shop, publishes like a magazine and keeps its receipts in the open: every page carries the disclosure above the fold, every outbound Amazon link is a tagged Special Link marked <code>rel="sponsored"</code>, and every dashboard surface is reachable from the footer.</p>
  <ul class="prose-list">
    <li>28 pages: storefront front page, shop by format, eight question-shaped guides, comparison with chooser, counter-space method, five data pages, four review pages, suggestions, open questions, executive summary, about, 404.</li>
    <li>RSS feed, sitemap, robots.txt, unique titles and descriptions, JSON-LD on every page, mobile-first presentation.</li>
    <li>30 self-checks run in CI on every push; the deploy fails if a disclosure, a sponsored mark or a link rule is lost.</li>
  </ul>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>The products</h2></div>
  <ul class="prose-list">
    <li><strong>P1 - %s.</strong> Verified: facts read from the official listing page, last read 2026-11-16. Published Special Link with the selected tracking ID.</li>
    <li><strong>P2 - %s.</strong> Verified the same way, including the function-count discrepancy the register records (listing says 24; the panel shows 25). Published Special Link.</li>
    <li><strong>P3 - %s.</strong> Verified the same way. Published Special Link.</li>
    <li><strong>P4, P5 - held.</strong> The two newest submitted links were observed to open to listings outside the air-fryer scope (meat thermometers) and their identity was never confirmed in an enrolled Associates workflow. Registered, never published: no page, no link, no facts.</li>
    <li><strong>Attribution for all published links is unverified</strong> until the one-link-per-product test passes in Associates Central (FLG-07).</li>
  </ul>
</section>
<section class="strip-section">
  <div class="section-head"><h2>The machinery</h2></div>
  <ul class="prose-list">
    <li><strong>Tracking ID %s</strong> (owner-supplied 2026-11-17; format valid, active status to be confirmed in Associates Central - FLG-04).</li>
    <li><strong>Five defined events</strong> recorded first-party and cookieless (page_view, product_link_click, chooser_step, article_read, guide_to_compare_click), with a runnable self-hosted collector awaiting a hosting decision (Q-06).</li>
    <li><strong>A campaign ledger that starts empty by rule</strong> - rows come only from authorised first-party reports with references. No conversion scores, no revenue forecasts, anywhere (FLG-03 for facts; the ledger rule for figures).</li>
    <li><strong>Product-intent records</strong> keep intended ASIN, official listing URL, confirmation date and source in one set of fields, observed redirects in another, and never merge them.</li>
  </ul>
</section>
<section class="strip-section alt">
  <div class="section-head"><h2>What happens next</h2></div>
  <ol class="prose-list">
    <li>Owner actions from the <a href="%sopen-questions.html">open questions</a>: confirm the tracking ID, run the one-link test per product, decide P4/P5 scope.</li>
    <li>Publishing cadence: one new question-shaped guide every 14 days, each added to the sitemap and feed by the same build; topics switch to measured queries after the gate (SG-06).</li>
    <li>Search Console setup and collector hosting to switch the topic queue from editorial to measured (SG-02, SG-03).</li>
    <li>Photography path decision before any imagery upgrade (Q-05); generated and scraped photos are barred (D-13).</li>
    <li>Everything else goes through the <a href="%ssuggestions.html">suggestions queue</a> first.</li>
  </ol>
</section>""" % (
        breadcrumb(path, [("Home", ""), ("Executive summary", "")]),
        esc(SITE["brand"]["name"]),
        esc(PRODUCTS_BY_ID["P1"]["name_short"]),
        esc(PRODUCTS_BY_ID["P2"]["name_short"]),
        esc(PRODUCTS_BY_ID["P3"]["name_short"]),
        esc(ASSOC["tracking_id"]["value"]),
        rel_prefix(path), rel_prefix(path),
    )
    add(path, "Executive summary - The Crisp Counter",
        "The project in one page: the site, the verified and held products, the tracking ID, the "
        "measurement machinery, and the ordered next steps with their open decisions.",
        body, body_class="summary")


def build_about():
    path = "about.html"
    body = """
%s
<section class="page-head"><h1>About &amp; disclosure</h1></section>
<section class="strip-section">
  <div class="section-head"><h2>What this is</h2></div>
  <p>The Crisp Counter is a small kitchen-technology publication about countertop air fryers. It exists because the listings, the roundups and the review-screamers all skip the same thing: what the facts actually say, and where they came from. The site compares three formats on the figures their official listing pages state, answers the questions a buyer actually asks, and keeps every receipt one click away.</p>
  <p>It is written and maintained by the site's editors. There is no test kitchen behind it - the guides say so when it matters, and the <a href="%sreview/methodology.html">methodology page</a> says exactly what a published fact requires before it ships.</p>
</section>
<section class="strip-section alt" id="disclosure">
  <div class="section-head"><h2>Disclosure</h2></div>
  <p>%s</p>
  <p>Concretely: product links on this site point to Amazon with the site's Associates tag. They are marked <code>rel="sponsored"</code> and labelled in place. The commission never changes the price you pay, and it never changes what the register publishes - the fact tables are written from the listings, not from the commissions.</p>
  <p>Click attribution is not yet verified: the one-link-per-product test in Associates Central has not been run (see <a href="%sreview/flagged.html">the flags</a>). The site publishes no traffic, conversion or revenue figures, and it will not until an authorised report exists.</p>
</section>
<section class="strip-section">
  <div class="section-head"><h2>How the site is made</h2></div>
  <p>Every page is generated from plain JSON registers by two standard-library Python scripts, and 30 self-checks run on every change. The full repository is public: <a href="https://github.com/wingbangboozle1-lang/Prod2" rel="noopener" target="_blank">github.com/wingbangboozle1-lang/Prod2</a>. If something looks wrong, open an issue - the registers make every claim checkable line by line.</p>
</section>""" % (
        breadcrumb(path, [("Home", ""), ("About", "")]),
        rel_prefix(path),
        esc(SITE["disclosure"]["strip"]),
        rel_prefix(path),
    )
    add(path, "About and disclosure - The Crisp Counter",
        "Who writes this site, how it is made, and the plain-words disclosure: Associate links, sponsored "
        "marking, unverified attribution, and the no-figures rule.",
        body, body_class="about-page",
        jsonld={"@context": "https://schema.org", "@type": "WebSite", "name": SITE["brand"]["name"], "url": BASE})


def build_404():
    path = "404.html"
    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE["brand"]["name"],
        "url": BASE,
    }
    body = """
<section class="page-head"><h1>Page not found</h1><p>The page you asked for does not exist. The site map below stays inside what is actually published.</p></section>
<div class="card-grid">
  <a class="card guide-card" href="index.html"><h3>Front page</h3><p>The verified three, the guides and the method.</p></a>
  <a class="card guide-card" href="compare/index.html"><h3>Compare</h3><p>The fact table and the three-question chooser.</p></a>
  <a class="card guide-card" href="guides/index.html"><h3>Guides</h3><p>One question per guide, answers first.</p></a>
  <a class="card guide-card" href="review/flagged.html"><h3>Flagged for review</h3><p>What is unverified, with sources.</p></a>
</div>"""
    add(path, "Page not found - The Crisp Counter",
        "The page does not exist. Start from the front page, the comparison, the guides or the flag page.",
        body, body_class="error-page", jsonld=jsonld)


# ------------------------------------------------------------ feed, sitemap, robots

def build_feed():
    items = []
    for g in GUIDES["guides"]:
        url = canon("guides/%s.html" % g["slug"])
        items.append(
            "<item><title>%s</title><link>%s</link><guid isPermaLink=\"true\">%s</guid>"
            "<pubDate>Wed, 19 Nov 2026 09:00:00 +0000</pubDate>"
            "<description>%s</description></item>" % (
                esc(g["title"]), esc(url), esc(url), esc(g["description"])))
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>%s</title>
<link>%s</link>
<description>%s</description>
<lastBuildDate>Wed, 19 Nov 2026 09:00:00 +0000</lastBuildDate>
<language>en-us</language>
%s
</channel></rss>""" % (
        esc(SITE["brand"]["name"]), esc(BASE), esc(SITE["brand"]["method_line"]), "\n".join(items))
    (PUBLIC / "feed.xml").write_text(xml, encoding="utf-8")


def build_sitemap_robots():
    urls = []
    for path, _t, _d, _h in PAGES:
        if path == "404.html":
            continue
        urls.append("  <url><loc>%s</loc><lastmod>2026-11-19</lastmod></url>" % esc(canon(path)))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>' % "\n".join(urls)
    (PUBLIC / "sitemap.xml").write_text(xml, encoding="utf-8")
    (PUBLIC / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % BASE, encoding="utf-8")


def copy_assets():
    shutil.copytree(ASSETS_SRC, PUBLIC / "assets")


def main():
    build_index()
    build_guides()
    build_shop()
    build_compare()
    build_counter_space()
    build_data_pages()
    build_review_pages()
    build_suggestions()
    build_open_questions()
    build_exec_summary()
    build_about()
    build_404()
    write_all()
    copy_assets()
    build_feed()
    build_sitemap_robots()
    print("built %d pages into %s" % (sum(1 for p, *_ in PAGES), PUBLIC))


if __name__ == "__main__":
    main()
