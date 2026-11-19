#!/usr/bin/env python3
"""Build the static site in docs/ from data/products.json and the page definitions below.

Standard library only. Run:  python3 scripts/build_site.py
"""
import datetime
import html
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
DATA = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))

BASE = "https://wingbangboozle1-lang.github.io/Prod2/"
TRACK = DATA["tracking_id"]
FETCHED = DATA["fetched_on"]
SITE_NAME = "Countertop Journal"  # working name (FR-12)
PRODUCTS = DATA["products"]
FLAGS = DATA["flags"]
BY_ID = {p["id"]: p for p in PRODUCTS}
FLAG_IDS = {f["id"] for f in FLAGS}

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
NOT_ENDORSED = "This site is not endorsed by or affiliated with Amazon."

NAV = [
    ("index.html", "Home"),
    ("air-fryers.html", "Air fryers"),
    ("meat-thermometers.html", "Meat thermometers"),
    ("guides/index.html", "Guides"),
    ("products.html", "Products"),
    ("analysis.html", "Analysis"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged for review"),
    ("about.html", "About"),
]
FOOTER_SURFACES = [
    ("executive-summary.html", "Executive summary"),
    ("products.html", "Full product table"),
    ("analysis.html", "Analysis and build status"),
    ("questions.html", "Open questions"),
    ("suggestions.html", "Suggestions for review"),
    ("ledger.html", "Campaign ledger"),
    ("sources.html", "Source register"),
    ("flagged.html", "Flagged for review"),
    ("about.html", "About and method"),
    ("feed.xml", "RSS feed"),
    ("sitemap.xml", "Sitemap"),
]

PAGES = []  # (path, title, description, body_html, jsonld_obj_or_None, kind)


def esc(value):
    return html.escape(str(value), quote=True)


def prefix_for(path):
    return "../" * path.count("/")


def buy_url(p):
    return f"https://www.amazon.com/dp/{p['observed_redirect_asin']}?tag={TRACK}"


def buy_link(p, label="View on Amazon"):
    return (f'<a class="buy" href="{esc(buy_url(p))}" rel="sponsored noopener" '
            f'data-outbound data-product="{p["id"]}">{esc(label)}</a>')


def source_link(p):
    return (f'<a href="{esc(p["official_listing_url"])}" rel="sponsored noopener">'
            f'Amazon listing</a>')


def link(url, label):
    if "amazon.com" in url or "link.amazon" in url:
        return f'<a href="{esc(url)}" rel="sponsored noopener">{esc(label)}</a>'
    return f'<a href="{esc(url)}">{esc(label)}</a>'


def flag_ref(fid):
    assert fid in FLAG_IDS, fid
    return f'<a href="flagged.html#{fid}">{fid}</a>'


def sources_cell(sources):
    return "<br>".join(link(s["url"], s["label"]) for s in sources)


def product_table(products, extended=False):
    head = ["Product", "Observed ASIN (redirect target)", "Intended ASIN", "Spec as listed",
            "Price", "Rating", "Source", "Status"]
    if extended:
        head.insert(1, "Supplied link token")
    rows = []
    for p in products:
        cells = [f'<td><strong>{esc(p["display_name"])}</strong><br>{buy_link(p)}</td>']
        if extended:
            cells.append(f'<td><code>{esc(p["supplied_token"])}</code><br>'
                         f'<a href="{esc(p["supplied_link"])}" rel="sponsored noopener">supplied link</a></td>')
        cells.append(f'<td><code>{esc(p["observed_redirect_asin"])}</code></td>')
        cells.append(f'<td class="unverified">Unverified (FR-02)</td>')
        cells.append(f'<td>{esc(p["spec_as_listed"])}</td>')
        cells.append('<td class="unverified">Unverified: left blank (FR-05)</td>')
        cells.append('<td class="unverified">Unverified: left blank (FR-05)</td>')
        cells.append(f'<td>{source_link(p)}</td>')
        cells.append(f'<td>Redirect ASIN observed {esc(FETCHED)}. Special Link test pending ({flag_ref("FR-03")}).</td>')
        rows.append(f'<tr data-row="{p["id"]}">' + "".join(cells) + "</tr>")
    thead = "".join(f"<th>{esc(h)}</th>" for h in head)
    return ('<div class="table-wrap"><table class="data"><thead><tr>' + thead +
            '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")


def simple_table(headers, rows, caption=None):
    """rows: list of lists of cell HTML strings (already escaped where needed)."""
    cap = f"<caption>{esc(caption)}</caption>" if caption else ""
    thead = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<div class="table-wrap"><table class="data">{cap}<thead><tr>{thead}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def product_card(p):
    cat = "Air fryers" if p["category"] == "air-fryers" else "Meat thermometers"
    return f"""<article class="card">
  <p class="card-kicker">{esc(cat)} · Amazon listing</p>
  <h3>{esc(p["display_name"])}</h3>
  <p class="spec"><span>As listed:</span> {esc(p["spec_as_listed"])}</p>
  <p class="meta">Observed ASIN <code>{esc(p["observed_redirect_asin"])}</code> · Intended ASIN <span class="unverified">unverified</span></p>
  <p class="meta">Listing checked {esc(FETCHED)} · {source_link(p)}</p>
  {buy_link(p)}
</article>"""


def guide_card(path, title, blurb):
    return f"""<article class="card guide-card">
  <p class="card-kicker">Working title</p>
  <h3><a href="{path}">{esc(title)}</a></h3>
  <p>{esc(blurb)}</p>
</article>"""


def jsonld_article(title, desc, path, date):
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "datePublished": date,
        "dateModified": date,
        "url": BASE + path,
        "author": {"@type": "Organization", "name": "Editorial team (no named author supplied)"},
        "publisher": {"@type": "Organization", "name": SITE_NAME},
    }


def render(path, title, desc, body, jsonld=None):
    pre = prefix_for(path)
    canonical = BASE + path
    nav_items = ""
    for href, label in NAV:
        current = ' aria-current="page"' if href == path else ""
        nav_items += f'<li><a href="{pre}{href}"{current}>{esc(label)}</a></li>'
    foot_items = "".join(f'<li><a href="{pre}{href}">{esc(label)}</a></li>' for href, label in FOOTER_SURFACES)
    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{pre}assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE_NAME)} guides" href="{pre}feed.xml">
{ld}
</head>
<body data-analytics-endpoint="">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap">
    <a class="brand" href="{pre}index.html">{esc(SITE_NAME)}</a>
    <p class="tagline">Working name · Air fryers and meat thermometers, with the listing behind every row</p>
  </div>
</header>
<div class="disclosure-strip" id="disclosure" role="note">
  <div class="wrap"><strong>Disclosure:</strong> {esc(DISCLOSURE)} {esc(NOT_ENDORSED)} Product links are marked sponsored.</div>
</div>
<nav class="nav" aria-label="Main">
  <div class="wrap"><ul>{nav_items}</ul></div>
</nav>
<main id="main" class="wrap">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <p class="footer-disclosure" id="footer-disclosure"><strong>Disclosure:</strong> {esc(DISCLOSURE)} {esc(NOT_ENDORSED)}</p>
    <nav aria-label="Site map"><ul class="footer-links">{foot_items}</ul></nav>
    <p class="fine">Every page is dated by its source fetch. Product data was checked on {esc(FETCHED)}. Editorial byline: “Editorial team” (no named author supplied, see <a href="{pre}flagged.html#FR-11">FR-11</a>). Brand name is a working name (<a href="{pre}flagged.html#FR-12">FR-12</a>).</p>
  </div>
</footer>
<script src="{pre}assets/tracker.js" defer></script>
</body>
</html>
"""


def write_page(path, title, desc, body, jsonld=None):
    PAGES.append(path)
    full = OUT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(render(path, title, desc, body, jsonld), encoding="utf-8")


# ---------------------------------------------------------------- content

AIR = [p for p in PRODUCTS if p["category"] == "air-fryers"]
THERMO = [p for p in PRODUCTS if p["category"] == "meat-thermometers"]

GUIDES = [
    {
        "slug": "basket-or-oven-style-air-fryer-what-to-compare",
        "title": "Basket or oven-style air fryer: what should you compare?",
        "desc": "Working-title guide: the questions to answer before choosing between a basket air fryer and an oven-style air fryer, with the listing spec each product states.",
        "blurb": "Two designs show up in the listings we checked. This guide lists what to compare before choosing.",
        "body": """
<p>Two designs show up in the listings we checked: a basket air fryer, and a countertop air-fryer oven with a door. The listing titles name the form. They do not say which one suits a given kitchen, and this guide does not rank them.</p>
<h2>What the listings say</h2>
<ul>
  <li><strong>{P01}</strong>: “2 Independent 3Qt” baskets, as printed in the title.</li>
  <li><strong>{P02}</strong>: “24 One-Touch Preset Options” and “Six Cooking Accessories Included”, as printed.</li>
  <li><strong>{P03}</strong>: “4-in-1” with a “450°F Hi-Fry Option”, as printed.</li>
</ul>
<h2>Questions to answer before you compare</h2>
<ol>
  <li>How many people do you cook for, and do you cook two dishes at once? Two baskets and a single chamber are different layouts, and we have not tested either.</li>
  <li>How much counter depth and door clearance do you have? We did not extract listing dimensions (<a href="flagged.html#FR-08">FR-08</a>), so measure your space and read the dimensions section on each listing yourself.</li>
  <li>Which functions do you actually use: air fry, bake, broil, dehydrate, toast? Check the function list on each listing, not the number of presets.</li>
  <li>Who will clean it, and which parts does the listing describe as dishwasher-safe?</li>
</ol>
<h2>What we cannot tell you</h2>
<p>We have not tested these appliances, and no ratings or performance results appear on this site. Anything printed on a listing is the seller’s or manufacturer’s statement, not ours.</p>
""",
        "links": ["air-fryers.html", "products.html", "guides/air-fryer-capacity-checklist.html",
                  "guides/cleanup-and-counter-space-tradeoffs.html",
                  "guides/multi-function-kitchen-appliance-questions.html"],
    },
    {
        "slug": "air-fryer-capacity-checklist",
        "title": "A no-hype checklist for comparing air fryer capacity",
        "desc": "Working-title guide: a plain checklist for reading air fryer capacity figures as listed, with the capacity printed on each listing we checked.",
        "blurb": "A checklist for reading capacity figures as the listing states them.",
        "body": """
<p>Capacity figures are the first thing people compare, and they are easy to misread. This checklist keeps to what the listings state.</p>
<h2>How the listings state capacity</h2>
<ul>
  <li><strong>{P01}</strong>: “6 Quart Dual Basket” in the title, with “2 Independent 3Qt” baskets. The title gives a total figure and a per-basket figure. Read both as stated.</li>
  <li><strong>{P02}</strong>: “26QT” in the title.</li>
  <li><strong>{P03}</strong>: “8 Qt” in the title.</li>
</ul>
<h2>Checklist</h2>
<ol>
  <li>Use one unit. Compare quarts with quarts, not with litres from another listing.</li>
  <li>Check whether a figure is per basket or total.</li>
  <li>Compare the figure each listing states. Do not assume two brands measure capacity the same way.</li>
  <li>Think about the food you cook most, and how many batches you would need.</li>
  <li>Check the dimensions on the listing (we did not extract them; <a href="flagged.html#FR-08">FR-08</a>) before you assume a larger number fits your counter.</li>
</ol>
<h2>What this guide does not do</h2>
<p>It does not say a capacity is “enough” for any household, and it does not rank these products.</p>
""",
        "links": ["air-fryers.html", "products.html", "guides/basket-or-oven-style-air-fryer-what-to-compare.html",
                  "guides/cleanup-and-counter-space-tradeoffs.html",
                  "guides/multi-function-kitchen-appliance-questions.html"],
    },
    {
        "slug": "cleanup-and-counter-space-tradeoffs",
        "title": "How to assess cleanup and counter-space trade-offs",
        "desc": "Working-title guide: questions for weighing cleanup and counter space before buying an air fryer, with the cleanup features each listing prints.",
        "blurb": "Cleanup and counter space: the trade-offs to write down before you buy.",
        "body": """
<p>Cleanup and counter space decide whether an appliance gets used. This guide lists what to check, and what the listings say.</p>
<h2>Cleanup, as the listings state it</h2>
<ul>
  <li><strong>{P01}</strong>: “Dishwasher Safe Frying Baskets” in the title.</li>
  <li><strong>{P03}</strong>: “XL Nonstick Dishwasher-Safe Basket” in the title.</li>
  <li><strong>{P02}</strong>: “Six Cooking Accessories Included” in the title. The title does not say the accessories are dishwasher-safe, so check the listing before you assume it.</li>
</ul>
<h2>Counter space</h2>
<p>We did not extract listing dimensions (<a href="flagged.html#FR-08">FR-08</a>), so no size comparison is made here. Measure your counter depth and the clearance the appliance needs, then compare with the dimensions section of each listing.</p>
<h2>Trade-offs to write down</h2>
<ol>
  <li>How often will you use it? Daily use changes how much cleaning effort matters.</li>
  <li>Where will it live? A permanent spot and a cupboard-stored appliance need different footprints.</li>
  <li>Will accessories fit in your dishwasher, and will they fit in a cupboard once stored?</li>
  <li>Does the manufacturer’s manual ask for clear space around the appliance? Check the manual, not only the listing.</li>
</ol>
""",
        "links": ["air-fryers.html", "products.html", "guides/basket-or-oven-style-air-fryer-what-to-compare.html",
                  "guides/air-fryer-capacity-checklist.html",
                  "guides/multi-function-kitchen-appliance-questions.html"],
    },
    {
        "slug": "multi-function-kitchen-appliance-questions",
        "title": "Questions to ask before buying a multi-function kitchen appliance",
        "desc": "Working-title guide: questions to ask before buying a multi-function kitchen appliance, using the function, preset and accessory claims printed on the listings.",
        "blurb": "Function lists, presets and accessories: the questions to ask before you buy.",
        "body": """
<p>Multi-function appliances list many functions. The useful question is which of them you will use. This guide shows the claims printed on the listings so you can check them.</p>
<h2>Claims printed on the listings</h2>
<ul>
  <li><strong>{P02}</strong>: “24 One-Touch Preset Options” and “Six Cooking Accessories Included”.</li>
  <li><strong>{P03}</strong>: “Bake, Dehydrate, Frozen” and a “450°F Hi-Fry Option”.</li>
</ul>
<h2>Questions to ask</h2>
<ol>
  <li>Which functions will you use each week? Write them down before you look at preset counts.</li>
  <li>Does the maximum temperature on the listing cover the dishes you cook? Check the number on the listing.</li>
  <li>Which accessories come in the box, and which would you have to buy separately?</li>
  <li>What does the warranty cover? We did not verify warranty terms; read the manufacturer’s statement on the listing.</li>
  <li>Does the appliance fit your counter and your storage space? See <a href="guides/cleanup-and-counter-space-tradeoffs.html">the cleanup and counter-space guide</a>.</li>
</ol>
<h2>On claims</h2>
<p>A printed claim is a claim, not a test result. We have not verified the functions, temperatures or accessory counts beyond what the listing titles state.</p>
""",
        "links": ["air-fryers.html", "products.html", "guides/basket-or-oven-style-air-fryer-what-to-compare.html",
                  "guides/air-fryer-capacity-checklist.html",
                  "guides/cleanup-and-counter-space-tradeoffs.html"],
    },
]

GUIDE_TOKENS = {"{P01}": "Chefman 6-quart dual-basket air fryer",
                "{P02}": "Emeril Lagasse 26QT French door air fryer toaster oven",
                "{P03}": "Chefman 8-quart TurboFry air fryer"}


def fix_guide_paths(fragment):
    """Guides live in guides/, so root-relative links need a ../ prefix (or a sibling name)."""
    def repl(m):
        href = m.group(1)
        if href.startswith(("http", "#", "../", "mailto:")):
            return m.group(0)
        if href.startswith("guides/"):
            href = href[len("guides/"):]
        else:
            href = "../" + href
        return f'href="{href}"'
    return re.sub(r'href="([^"]+)"', repl, fragment)


def guide_body(g):
    body = g["body"]
    for tok, name in GUIDE_TOKENS.items():
        pid = {"{P01}": "P01", "{P02}": "P02", "{P03}": "P03"}[tok]
        p = BY_ID[pid]
        body = body.replace(tok, f'<a href="{esc(p["official_listing_url"])}" rel="sponsored noopener">{esc(name)}</a>')
    return fix_guide_paths(body)


def guide_href(target):
    """Target is a root-relative site path; convert it for a page inside guides/."""
    if target.startswith("guides/"):
        return target[len("guides/"):]
    return "../" + target


def related(links, depth_prefix=""):
    items = "".join(
        f'<li><a href="{guide_href(l)}">{esc(l.replace(".html", "").replace("guides/", "").replace("-", " "))}</a></li>'
        for l in links)
    return f'<aside class="related"><h2>Keep reading</h2><ul>{items}</ul></aside>'


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "assets").mkdir()
    shutil.copy(ROOT / "scripts" / "assets" / "style.css", OUT / "assets" / "style.css")
    shutil.copy(ROOT / "scripts" / "assets" / "tracker.js", OUT / "assets" / "tracker.js")

    # ---------------- Home (front page)
    cards = "".join(product_card(p) for p in PRODUCTS)
    guide_cards = "".join(guide_card("guides/" + g["slug"] + ".html", g["title"], g["blurb"]) for g in GUIDES)
    home = f"""
<section class="hero">
  <p class="kicker">Front page · working edition</p>
  <h1>Five products, each tied to the Amazon listing it was checked against</h1>
  <p class="dek">Air fryers and meat thermometers. For every product: the listing’s own title and spec, the ASIN the supplied link resolves to, and what we have not verified yet.</p>
  <div class="cta-row">
    <a class="btn" href="air-fryers.html">Air fryers (3)</a>
    <a class="btn alt" href="meat-thermometers.html">Meat thermometers (2)</a>
  </div>
</section>

<section aria-labelledby="products-h">
  <h2 id="products-h" class="section-h">The products</h2>
  <div class="grid">{cards}</div>
  <p class="note">Prices and ratings are left blank: they change, and Creators API access is not in place (<a href="flagged.html#FR-05">FR-05</a>). Intended ASINs are unverified (<a href="flagged.html#FR-02">FR-02</a>).</p>
</section>

<section class="tiles" aria-label="Categories">
  <a class="tile" href="air-fryers.html"><span class="tile-n">3</span><span class="tile-t">Air fryers</span><span class="tile-s">Basket and oven-style, as listed</span></a>
  <a class="tile" href="meat-thermometers.html"><span class="tile-n">2</span><span class="tile-t">Meat thermometers</span><span class="tile-s">Probes and response time, as printed</span></a>
  <a class="tile" href="guides/index.html"><span class="tile-n">4</span><span class="tile-t">Guides</span><span class="tile-s">Questions to answer before you buy</span></a>
</section>

<section aria-labelledby="guides-h">
  <h2 id="guides-h" class="section-h">Guides <span class="pill">working titles</span></h2>
  <div class="grid">{guide_cards}</div>
</section>

<section aria-labelledby="data-h">
  <h2 id="data-h" class="section-h">Where the numbers stand</h2>
  {simple_table(["Measure", "Value", "Source", "Status"], [
    ["Supplied links that resolved to an Amazon listing", "5 of 5", f'<a href="https://link.amazon/B04G1MEwY" rel="sponsored noopener">link.amazon/B04G1MEwY</a> (and the other four)', "Checked " + esc(FETCHED)],
    ["Intended ASINs confirmed by the owner", "0 of 5", f'<a href="flagged.html#FR-02">FR-02</a>', "Open"],
    ["Special Link tests completed in the Associates workflow", "0 of 5", f'<a href="flagged.html#FR-03">FR-03</a>', "Open"],
    ["Prices or ratings published", "0 of 5", f'<a href="flagged.html#FR-05">FR-05</a>', "Blank by design"],
    ["Clicks recorded by a server", "Not available", f'<a href="flagged.html#FR-09">FR-09</a>', "No endpoint hosted"],
  ])}
  <p class="note"><a href="analysis.html">Full analysis and build status</a> · <a href="products.html">full product table</a> · <a href="executive-summary.html">executive summary</a></p>
</section>
"""
    write_page("index.html", "Countertop Journal: air fryers and meat thermometers, with listing sources",
               "Five Amazon products for air fryers and meat thermometers, each with its listing source, observed ASIN, and what is still unverified.",
               home,
               {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": BASE,
                "description": "Air fryers and meat thermometers, each tied to its Amazon listing."})

    # ---------------- Category pages
    air_body = f"""
<section class="hero compact">
  <p class="kicker">Category</p>
  <h1>Air fryers</h1>
  <p class="dek">Three products, from basket designs to an oven-style air fryer. Each row shows the spec the listing states and the source it came from.</p>
</section>
<section>
  <h2 class="section-h">Comparison table</h2>
  {product_table(AIR)}
  <p class="note">Spec column is quoted from the listing title. Nothing here is a performance or ranking claim.</p>
</section>
<section>
  <h2 class="section-h">Questions before you choose</h2>
  <ul class="plain">
    <li><a href="guides/basket-or-oven-style-air-fryer-what-to-compare.html">Basket or oven-style: what should you compare?</a></li>
    <li><a href="guides/air-fryer-capacity-checklist.html">A checklist for comparing capacity</a></li>
    <li><a href="guides/cleanup-and-counter-space-tradeoffs.html">Cleanup and counter-space trade-offs</a></li>
    <li><a href="guides/multi-function-kitchen-appliance-questions.html">Questions before a multi-function appliance</a></li>
  </ul>
</section>
"""
    air_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Air fryers",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["display_name"],
                                   "url": p["official_listing_url"]} for i, p in enumerate(AIR)]}
    write_page("air-fryers.html", "Air fryers: three listings compared by stated spec",
               "Three Amazon air fryer listings compared by the spec each title states, with the observed ASIN and the source for every row.",
               air_body, air_ld)

    th_body = f"""
<section class="hero compact">
  <p class="kicker">Category</p>
  <h1>Meat thermometers</h1>
  <p class="dek">Two digital thermometers: one listed with a “1 Sec” response, and one smart wireless model with three probes. Specs are the figures each listing title prints; we have not tested accuracy.</p>
</section>
<section>
  <h2 class="section-h">Comparison table</h2>
  {product_table(THERMO)}
  <p class="note">“As printed” means the claim comes from the listing title and has not been verified against a certificate or a test.</p>
</section>
<section>
  <h2 class="section-h">Questions before you choose</h2>
  <ul class="plain">
    <li>How many probes do you need, and at what cooking temperatures?</li>
    <li>Do you need a wireless app connection? Check whether the listing requires one.</li>
    <li>Which waterproof and heat-safety ratings matter to you? Check the rating’s issuing body, not only the printed number.</li>
    <li>Is a printed certification (for example NIST) something you want to verify yourself? Check the certifying body’s own records.</li>
  </ul>
</section>
"""
    th_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Meat thermometers",
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["display_name"],
                                  "url": p["official_listing_url"]} for i, p in enumerate(THERMO)]}
    write_page("meat-thermometers.html", "Meat thermometers: two listings with printed specs",
               "Two Amazon meat thermometer listings with the specs printed in each title, the observed ASIN and the source for every row.",
               th_body, th_ld)

    # ---------------- Full product table
    prod_body = f"""
<section class="hero compact">
  <p class="kicker">Data</p>
  <h1>All products</h1>
  <p class="dek">The full register: the supplied link, the ASIN it redirects to, the intended ASIN (unverified), and the source for each row.</p>
</section>
<section>
  {product_table(PRODUCTS, extended=True)}
  <p class="note">Observed ASIN and intended ASIN are kept in separate columns on purpose. Observed values come from the redirect; intended values come from the owner and are not yet confirmed.</p>
</section>
"""
    write_page("products.html", "All products: full register with supplied links and sources",
               "Full register of the five supplied Amazon links: supplied token, observed redirect ASIN, unverified intended ASIN, spec as listed, and source.",
               prod_body)

    # ---------------- Guides
    gcards = "".join(guide_card(g["slug"] + ".html", g["title"], g["blurb"]) for g in GUIDES)
    write_page("guides/index.html", "Guides: questions to answer before buying an air fryer",
               "Four working-title guides on air fryer comparison, capacity, cleanup and multi-function appliances, each linked to its category and product table.",
               f"""<section class="hero compact"><p class="kicker">Guides</p><h1>Questions to answer before you buy</h1>
<p class="dek">Four working-title guides. Each lists what to compare, quotes what the listings state, and says what we have not verified.</p></section>
<section><div class="grid">{gcards}</div></section>
<section><p class="note">Working titles are editorial hypotheses, not claims about popularity or search volume (<a href="../flagged.html#FR-13">FR-13</a>).</p></section>""")

    for g in GUIDES:
        path = "guides/" + g["slug"] + ".html"
        body = f"""
<article class="article">
  <p class="kicker">Guide · working title · added {esc(FETCHED)}</p>
  <h1>{esc(g["title"])}</h1>
  <p class="byline">By the Editorial team (no named author supplied, <a href="../flagged.html#FR-11">FR-11</a>)</p>
  {guide_body(g)}
  <p class="note">Product names link to the Amazon listing they describe. Data as checked {esc(FETCHED)}.</p>
  {related(g["links"])}
</article>"""
        write_page(path, g["title"], g["desc"], body,
                   jsonld_article(g["title"], g["desc"], path, FETCHED))

    # ---------------- Analysis
    findings = [
        ["Supplied short links that resolved to an Amazon product page", "5 of 5", link("https://link.amazon/B0c8moW59", "link.amazon (5 tokens)"), "Verified " + FETCHED],
        ["Distinct observed redirect ASINs", "5", link("https://www.amazon.com/dp/B0CDY277D3", "B0CDY277D3 listing"), "Verified " + FETCHED],
        ["Supplied tokens in the 10-character ASIN format", "0 of 5", link("https://sellercentral.amazon.com/seller-forums/discussions/t/736a09d1-bb16-4add-bb57-229805c9f2d9", "Amazon Seller Central forum (secondary)"), "Irregular: see FR-01"],
        ["Intended ASINs confirmed", "0 of 5", link("https://www.amazon.com/dp/B0CDY277D3", "B0CDY277D3 listing"), "Unverified: FR-02"],
        ["Prices and ratings published", "0 of 5", link("https://www.amazon.com/dp/B0CDY277D3", "B0CDY277D3 listing"), "Blank by design: FR-05"],
        ["Associates disclosure wording", "“As an Amazon Associate I earn from qualifying purchases.”", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 5"), "Verified verbatim"],
        ["Special Link tests in the Associates workflow", "0 of 5", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 1"), "Open: FR-03"],
        ["Guide topics backed by measured demand data", "0 of 4", link("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google: creating helpful content"), "Open: FR-13"],
        ["Outbound product links marked rel=\"sponsored\"", "All product links", link("https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links", "Google: qualify outbound links"), "Enforced by verify script"],
    ]
    status_rows = [
        ["Product pages with titles and meta descriptions (S-04)", "Implemented; checked by the verify script", link("https://developers.google.com/search/docs/appearance/snippet", "Google: snippet guidance (cited, not fetched)")],
        ["Outbound product links marked sponsored (S-05)", "Implemented", link("https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links", "Google: qualify outbound links")],
        ["Disclosure under the masthead and in the footer, every page", "Implemented", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 5")],
        ["Product-intent record with separate observed and intended fields", "Implemented (intended fields unverified)", link("https://sellercentral.amazon.com/seller-forums/discussions/t/736a09d1-bb16-4add-bb57-229805c9f2d9", "ASIN description (secondary)")],
        ["Special Link validation per product (brief)", "Not done: owner test required (FR-03)", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 1")],
        ["Privacy-preserving outbound-click counter", "Partial: client-side event, nothing transmitted (FR-09)", link("https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html", "Zone4 decision log (internal)")],
        ["Self-hosted analytics endpoint and five defined events", "Not implemented: no server on GitHub Pages; 1 of 5 events defined (FR-09)", link("https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html", "Zone4 decision log (internal)")],
        ["Question-shaped guides (S-07, S-13)", "Partial: four working titles", link("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google: creating helpful content")],
        ["Sitemap and RSS feed for each guide", "Implemented; search-console submission owner action (FR-10)", link("https://developers.google.com/search/docs/appearance/page-experience", "Google: page experience (cited)")],
        ["Structured data (S-09)", "Partial: JSON-LD on category and guide pages; no social preview image", link("https://developers.google.com/search/docs/appearance/page-experience", "Google: page experience (cited)")],
        ["Product photography (S-18)", "Not implemented: decision needed (FR-07)", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 1")],
        ["Three-question chooser above the table (S-19)", "Not implemented: awaiting option choice (SUG-07)", link("https://www.amazon.com/dp/B0CDY277D3", "B0CDY277D3 listing")],
        ["Counter-space analysis (S-23)", "Not implemented: dimensions not extracted (FR-08)", link("https://www.amazon.com/dp/B0CDY277D3", "B0CDY277D3 listing")],
        ["Authorship, navigation and brand (publication polish)", "Partial: navigation and footer done; no named author; brand working name (FR-11, FR-12)", link("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google: creating helpful content")],
        ["Measurement ledger, empty until first-party reports exist", "Implemented as empty", link("https://affiliate-program.amazon.com/help/operating/policies", "Associates Program Policies (Commission Income Statement)")],
        ["Verification gate in the workflow (disclosure, sponsored links, links, claims)", "Implemented: scripts/verify_site.py; GitHub Actions workflow", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 5")],
    ]
    analysis_body = f"""
<section class="hero compact"><p class="kicker">Data · analysis</p><h1>Analysis and build status</h1>
<p class="dek">What the verified data shows, what it does not show, and where each requirement stands.</p></section>
<section><h2 class="section-h">Findings</h2>
{simple_table(["Finding", "Value", "Source", "Status"], findings)}
<p class="note">No conversion score, revenue forecast, or ranking is presented. The campaign ledger is empty by design (<a href="ledger.html">ledger</a>).</p></section>
<section><h2 class="section-h">Build status against the requirements</h2>
{simple_table(["Requirement", "Status", "Source"], status_rows)}
</section>
<section><h2 class="section-h">Reading the findings</h2>
<ul class="plain">
  <li>The five supplied links all resolve, so the links work. We cannot say they are the intended products until the owner confirms it (<a href="flagged.html#FR-02">FR-02</a>).</li>
  <li>Every product row links to its Amazon listing; nothing on the site is copied from a listing except the title spec, marked “as listed”.</li>
  <li>The strongest next step is confirmation, not content: intended ASINs and one Special Link test per product. See <a href="suggestions.html">Suggestions</a>.</li>
</ul></section>
"""
    write_page("analysis.html", "Analysis: what the verified data shows and where each requirement stands",
               "Verified findings for the five supplied Amazon links, with source links, and the build status of each requirement.",
               analysis_body)

    # ---------------- Questions
    qrows = [
        ["Q-01", "Are the five supplied links the intended products?", "Each link resolves to one Amazon listing (observed ASIN).", "Owner confirmation of intended ASIN for each link.", "Owner confirms against the product they meant; the listing is the reference.", link("https://www.amazon.com/dp/B0CDY277D3", "P01 listing (example)"), "FR-02"],
        ["Q-02", "Do tagged product links track as Special Links?", "Standard tagged format is used on the site.", "A test per product in the enrolled Associates workflow.", "One test link per product; confirm destination and the tracking report.", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 1"), "FR-03, FR-04"],
        ["Q-03", "What is the commission rate for each product?", "Standard commission is a percentage of qualifying revenue.", "Per-product or per-category rate.", "Associates rate card and Commission Income Statement, read against each product’s category.", link("https://affiliate-program.amazon.com/help/operating/policies", "Associates Program Policies"), "FR-06"],
        ["Q-04", "Can prices and ratings be shown?", "Visible on listings on 2026-11-19.", "Permission and access route for price and rating data.", "Creators API introduction and prerequisites.", link("https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction", "Creators API introduction"), "FR-05"],
        ["Q-05", "What are the listing dimensions, and does the appliance fit?", "Capacity as stated in titles.", "Dimensions, extracted from each listing.", "Read the dimensions section of each listing on a dated snapshot.", link("https://www.amazon.com/dp/B0CDY277D3", "P01 listing"), "FR-08"],
        ["Q-06", "Which guide topics do people search for?", "Working titles only.", "Measured query data from first-party sources.", "Search Console queries after verification, and site analytics once the endpoint decision is made.", link("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google: creating helpful content"), "FR-10, FR-13"],
        ["Q-07", "Where will analytics run, and what do the five events mean?", "One event (outbound_click) is built, with nothing sent.", "Hosting decision and the definitions of the other four events.", "Owner names the events; hosting is chosen; a consent review is done.", link("https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html", "Zone4 decision log (internal)"), "FR-09"],
        ["Q-08", "Who is the author?", "Byline is “Editorial team”.", "A named person, or a decision to publish as a team.", "Owner decision.", link("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google: creating helpful content"), "FR-11"],
        ["Q-09", "What is the brand name?", "Working name: Countertop Journal.", "Decision.", "Owner decision; check trademark availability before adoption.", link("https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html", "Zone4 decision log (internal)"), "FR-12"],
        ["Q-10", "Are product photos allowed, and from where?", "No photos used.", "Image source and licence.", "Owner decision; Program Content terms apply to Amazon images.", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement, Section 1"), "FR-07"],
        ["Q-11", "Does the disclosure wording meet current FTC guidance?", "Associates wording verified verbatim; FTC page checked (dated November 2019).", "Counsel review of current FTC guidance and placement.", "Counsel review.", link("https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers", "FTC: Disclosures 101"), "FR-14"],
        ["Q-12", "How often should new guides be published?", "No cadence has been set.", "Owner choice of cadence.", "Decision recorded in Suggestions.", link("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Google: creating helpful content"), "SUG-05"],
    ]
    q_body = f"""
<section class="hero compact"><p class="kicker">Decisions</p><h1>Open questions</h1>
<p class="dek">What must be answered before a decision can reasonably be made. For each: what we have, what is missing, and where to find it.</p></section>
<section>{simple_table(["ID", "Question", "What we have", "What is missing", "How to find it", "Source", "Flag"], qrows)}</section>
"""
    write_page("questions.html", "Open questions: what must be answered before each decision",
               "The open questions behind the site: what the verified data answers, what it does not, and how each gap can be closed from an official source.",
               q_body)

    # ---------------- Suggestions
    sugs = [
        ("SUG-01", "Confirm the intended ASIN for each supplied link", [
            ("A", "Owner confirms each product against the one they meant; the site updates the intended-ASIN field."),
            ("B", "Keep the observed ASIN only, and label the link as the redirect target."),
        ], "Argument: A first. It is the only way to close FR-02, and it costs one check per link."),
        ("SUG-02", "Run the Special Link test before scaling", [
            ("A", "Test one link per product now, then record destination and tracking report."),
            ("B", "Replace the product buttons with the supplied short links until the test is done."),
        ], "Argument: A. The brief requires the test before scaling, and the supplied short links’ status is unresolved (FLG-003)."),
        ("SUG-03", "Price and rating display", [
            ("A", "Keep both blank until API access is in place."),
            ("B", "Apply for Creators API access, then publish prices and ratings from it."),
        ], "Argument: A now, B when access is confirmed. Observed listing values change and are not safe to copy."),
        ("SUG-04", "Where the analytics endpoint runs", [
            ("A", "Keep it client-only; nothing is sent until an endpoint is chosen."),
            ("B", "Host a first-party endpoint outside GitHub Pages, after a consent and privacy review."),
        ], "Argument: A until the consent review (D-41) is done. The endpoint is not hosted on GitHub Pages either way."),
        ("SUG-05", "Publishing cadence for new guides", [
            ("A", "Two guides per month, one per product category."),
            ("B", "One guide per month, added only when a measured query supports it."),
            ("C", "No fixed cadence; publish when a question is confirmed by first-party data."),
        ], "Argument: C until Search Console data exists (FR-10). A fixed cadence would be a choice, not evidence."),
        ("SUG-06", "Brand name", [
            ("A", "Keep “Countertop Journal”."),
            ("B", "Choose a new name, after a trademark check."),
        ], "Argument: decide after the trademark check. The name is a working name only (FR-12)."),
        ("SUG-07", "Three-question chooser above the comparison tables (S-19)", [
            ("A", "Add the chooser, with each answer pointing to a listing spec."),
            ("B", "Skip it until dimensions are extracted (FR-08)."),
        ], "Argument: A for the air fryers page only, using capacity and function as listed."),
        ("SUG-08", "Add a fifth guide for meat thermometers", [
            ("A", "Write a guide on probe count and printed specs."),
            ("B", "Keep the category questions on the category page only."),
        ], "Argument: B until a question is confirmed by first-party data (FR-13)."),
        ("SUG-09", "Product photography (S-18)", [
            ("A", "No photography; typographic cards only."),
            ("B", "Owner-supplied photographs with written licence."),
        ], "Argument: A. Amazon images are Program Content under the Operating Agreement (FR-07)."),
        ("SUG-10", "Search Console", [
            ("A", "Owner verifies the site and submits sitemap.xml and feed.xml."),
            ("B", "Defer until the analytics decision is made."),
        ], "Argument: A. It is the only source of measured queries, and it is an owner action (FR-10)."),
    ]
    sug_html = ""
    for sid, title, opts, arg in sugs:
        opt_items = "".join(f'<li><strong>{oid}.</strong> {esc(text)}</li>' for oid, text in opts)
        sug_html += f"""<article class="card sug" id="{sid}">
  <p class="card-kicker">{sid} · awaiting choice</p>
  <h3>{esc(title)}</h3>
  <ul class="plain">{opt_items}</ul>
  <p class="meta"><em>{esc(arg)}</em></p>
</article>"""
    s_body = f"""
<section class="hero compact"><p class="kicker">Suggestions</p><h1>Choose the path before anything changes</h1>
<p class="dek">Each item lists the options. Nothing here is implemented until an option is chosen. The recommendation is an argument, not a decision.</p></section>
<section><div class="grid">{sug_html}</div></section>
<section><p class="note">To choose, reply with the suggestion ID and option letter (for example “SUG-01 A”). Decisions are recorded in the flags and questions pages.</p></section>
"""
    write_page("suggestions.html", "Suggestions: choose the path before any change",
               "Ten suggestions with options, each awaiting a choice. Nothing is implemented until an option is picked.",
               s_body)

    # ---------------- Executive summary
    es_body = f"""
<article class="article">
  <p class="kicker">Executive summary · as of {esc(FETCHED)}</p>
  <h1>Executive summary</h1>
  <h2>What the site is</h2>
  <p>A static, text-first product site for five Amazon products in two categories: air fryers and meat thermometers. It is published from this repository through GitHub Pages.</p>
  <h2>What is verified</h2>
  <ul>
    <li>All five supplied short links resolve to Amazon product pages. The observed ASINs are in the product table (<a href="products.html">products</a>).</li>
    <li>The Associates disclosure wording is taken verbatim from Section 5 of the Operating Agreement (<a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="sponsored noopener">source</a>).</li>
    <li>Every product link is marked sponsored, and the verify script checks it on every build.</li>
  </ul>
  <h2>What is not verified, and why it matters</h2>
  <ul>
    <li>The intended ASIN for each link is not confirmed (<a href="flagged.html#FR-02">FR-02</a>). The site shows the observed redirect target and keeps the intended field blank.</li>
    <li>Special Link tests have not been run (<a href="flagged.html#FR-03">FR-03</a>). This needs the owner’s Associates account.</li>
    <li>No price, rating, commission rate or dimension is published (<a href="flagged.html#FR-05">FR-05</a>, <a href="flagged.html#FR-06">FR-06</a>, <a href="flagged.html#FR-08">FR-08</a>).</li>
    <li>No server-side analytics runs; GitHub Pages cannot host the endpoint (<a href="flagged.html#FR-09">FR-09</a>).</li>
  </ul>
  <h2>Decisions the owner needs to make</h2>
  <p>Ten items are on the <a href="suggestions.html">suggestions page</a>. The first three decide whether the product links can be relied on: confirm intended ASINs, run the Special Link test, and decide on price display.</p>
  <h2>What the site does not claim</h2>
  <p>No ranking, no performance result, no ‘trending’ or popularity claim, no conversion score, and no revenue forecast. The campaign ledger is empty (<a href="ledger.html">ledger</a>).</p>
  <h2>Flagged for review</h2>
  <p>There are {len(FLAGS)} flagged items, with sources, on the <a href="flagged.html">Flagged for Review page</a>. Flags do not block publication.</p>
</article>"""
    write_page("executive-summary.html", "Executive summary: five Amazon products, what is verified, and what is not",
               "Executive summary of the site: the five supplied products, what is verified from official sources, what is not, and the decisions still open.",
               es_body)

    # ---------------- Ledger
    ledger_body = f"""
<section class="hero compact"><p class="kicker">Measurement</p><h1>Campaign ledger</h1>
<p class="dek">Empty by design. Rows are added only from authorised first-party reports. No estimates, forecasts or scores are shown.</p></section>
<section>
  <p class="empty">No entries yet. No first-party report has been added. Clicks recorded in a browser are not counted here.</p>
  <h2 class="section-h">Fields a row must carry</h2>
  <div class="table-wrap"><table class="data"><thead><tr><th>Timestamp (UTC)</th><th>Source (first-party report)</th><th>Channel</th><th>Eligible sessions</th><th>Clicks</th><th>Reported orders</th><th>Provenance note</th></tr></thead><tbody></tbody></table></div>
  <p class="note">Source requirements: <a href="https://affiliate-program.amazon.com/help/operating/policies" rel="sponsored noopener">Associates Program Policies (Commission Income Statement)</a>. Measurement decisions are open (<a href="flagged.html#FR-09">FR-09</a>).</p>
</section>
"""
    write_page("ledger.html", "Campaign ledger: empty until first-party reports are added",
               "The campaign ledger is empty by design. It will hold only rows drawn from authorised first-party reports, with provenance.",
               ledger_body)

    # ---------------- Sources
    src_rows = [
        ["GitHub Docs: configuring a publishing source for GitHub Pages", "Publishing from a branch and /docs folder (FR-18)", FETCHED, "Fetched", link("https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site", "GitHub Docs: publishing source")],
        ["Associates Program Operating Agreement", "Disclosure wording (Section 5), Special Links (Section 1), Program Content (Section 1)", FETCHED, "Fetched", link("https://affiliate-program.amazon.com/help/operating/agreement", "Operating Agreement")],
        ["Associates Program Policies", "Commission Income Statement, Participation Requirements, link formatting (2(g))", FETCHED, "Fetched (chunks 0–2 of 11)", link("https://affiliate-program.amazon.com/help/operating/policies", "Program Policies")],
        ["Google: qualify outbound links (rel=sponsored)", "Link attribute for paid links", FETCHED, "Fetched", link("https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links", "Qualify outbound links")],
        ["FTC: Disclosures 101 for Social Media Influencers", "Disclosure placement principles (dated November 2019)", FETCHED, "Fetched", link("https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers", "Disclosures 101")],
        ["link.amazon short links (5)", "Supplied links and redirect targets", FETCHED, "Fetched", link("https://link.amazon/B04G1MEwY", "link.amazon/B04G1MEwY")],
        ["Amazon listing pages (5)", "Titles, observed ASIN and spec as listed", FETCHED, "Fetched (title and first chunk)", link("https://www.amazon.com/dp/B0CDY277D3", "P01 listing")],
        ["Zone4 decision log (internal register)", "Open decisions (D-02, D-13, D-40, D-41, D-42, D-43); not an official source", FETCHED, "Fetched", link("https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html", "Zone4 decisions")],
        ["Amazon Seller Central forum (ASIN description)", "10-character ASIN description (secondary, Amazon-hosted)", "Search result", "Not the formal help page", link("https://sellercentral.amazon.com/seller-forums/discussions/t/736a09d1-bb16-4add-bb57-229805c9f2d9", "Seller Central forum")],
        ["Google: snippet guidance", "Titles and descriptions (S-04)", "Cited in brief", "Not fetched", link("https://developers.google.com/search/docs/appearance/snippet", "Snippet guidance")],
        ["Google: creating helpful content", "Editorial standard (cited in brief)", "Cited in brief", "Not fetched", link("https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "Creating helpful content")],
        ["Google: page experience", "Mobile presentation (cited in brief)", "Cited in brief", "Not fetched", link("https://developers.google.com/search/docs/appearance/page-experience", "Page experience")],
        ["Creators API introduction", "Prerequisites for price and rating data (cited in register)", "Cited in register", "Not fetched", link("https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction", "Creators API")],
    ]
    src_body = f"""
<section class="hero compact"><p class="kicker">Data · sources</p><h1>Source register</h1>
<p class="dek">Every source used, what it was used for, and whether it was fetched in this session or only cited.</p></section>
<section>{simple_table(["Source", "Used for", "Date", "Status", "Link"], src_rows)}</section>
"""
    write_page("sources.html", "Source register: official sources and how each was checked",
               "Source register for the Amazon affiliate site: each official source, what it supports, and whether it was fetched or only cited.",
               src_body)

    # ---------------- Flagged
    frows = []
    for f in FLAGS:
        frows.append([f'<span id="{f["id"]}"><strong>{f["id"]}</strong></span>', esc(f["severity"]),
                      f'<strong>{esc(f["title"])}</strong><br><span class="small">{esc(f["detail"])}</span>',
                      sources_cell(f["sources"]), esc(f["status"])])
    flag_rows = "".join(f'<tr data-row="flag">' + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in frows)
    flagged_body = f"""
<section class="hero compact"><p class="kicker">Flagged for review</p><h1>Flagged for review</h1>
<p class="dek">Irregularities, unverified values and open items. Each carries its source. Flags do not block publication; they are here so you can review them and ask for changes.</p></section>
<section>
  <div class="table-wrap"><table class="data"><thead><tr><th>ID</th><th>Severity</th><th>Issue</th><th>Sources</th><th>Status</th></tr></thead><tbody>
  {flag_rows}
  </tbody></table></div>
</section>
"""
    write_page("flagged.html", "Flagged for review: irregularities and unverified items with sources",
               "Flagged for review: irregularities, unverified values and open items, each with its source, for the owner to review.",
               flagged_body)

    # ---------------- About
    about_body = f"""
<article class="article">
  <p class="kicker">About</p>
  <h1>About this site and how it is checked</h1>
  <h2>Who writes it</h2>
  <p>The Editorial team. No named author has been supplied (<a href="flagged.html#FR-11">FR-11</a>). The brand name is a working name (<a href="flagged.html#FR-12">FR-12</a>).</p>
  <h2>Affiliate relationship</h2>
  <p>{esc(DISCLOSURE)} {esc(NOT_ENDORSED)} Product links go to Amazon and carry the Associates tracking tag. They are marked sponsored.</p>
  <h2>How a product row is checked</h2>
  <ol>
    <li>The supplied short link is followed to the Amazon product page it redirects to. That ASIN is recorded as the observed redirect target.</li>
    <li>The intended ASIN is recorded separately and left unverified until the owner confirms it.</li>
    <li>Spec values are quoted from the listing title, marked “as listed”. Prices, ratings and commission rates are left blank.</li>
    <li>Every row carries a link to its official source. The verify script checks this on each build.</li>
  </ol>
  <h2>Reader data</h2>
  <p>The site sets no cookies and loads no third-party analytics or tracking script. Outbound clicks are counted only in the page’s own memory and sent nowhere until an endpoint is chosen (<a href="flagged.html#FR-09">FR-09</a>). Our hosting provider, GitHub Pages, keeps its own standard server logs, which we do not control.</p>
</article>"""
    write_page("about.html", "About Countertop Journal: editorial team, affiliate disclosure and checking method",
               "About the site: who writes it, the Associates disclosure, how each product row is checked, and what reader data is collected.",
               about_body)

    # ---------------- 404
    write_page("404.html", "Page not found: Countertop Journal",
               "This page does not exist. Return to the Countertop Journal front page.",
               '<section class="hero compact"><h1>Page not found</h1><p class="dek">Try the <a href="index.html">front page</a>, or see the <a href="products.html">product table</a>.</p></section>')

    write_feeds_and_sitemap()


def write_feeds_and_sitemap():
    today_rfc = "Wed, 19 Nov 2026 00:00:00 +0000"
    items = ""
    for g in GUIDES:
        items += f"""  <item>
    <title>{esc(g["title"])}</title>
    <link>{BASE}guides/{g["slug"]}.html</link>
    <guid isPermaLink="true">{BASE}guides/{g["slug"]}.html</guid>
    <pubDate>{today_rfc}</pubDate>
    <description>{esc(g["desc"])}</description>
  </item>
"""
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>{esc(SITE_NAME)} guides</title>
  <link>{BASE}</link>
  <description>Working-title guides on air fryers and meat thermometers.</description>
  <language>en-us</language>
  <lastBuildDate>{today_rfc}</lastBuildDate>
{items}</channel>
</rss>
"""
    (OUT / "feed.xml").write_text(feed, encoding="utf-8")
    urls = sorted(set(PAGES))
    sm = "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{FETCHED}</lastmod></url>\n" for u in urls if u != "404.html")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + sm + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    build()
    print(f"built {len(set(PAGES))} pages into {OUT}")
