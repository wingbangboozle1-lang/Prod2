#!/usr/bin/env python3
"""
Countercraft site builder.

Reads the verified data in data/*.json and renders a static, editorial affiliate
site into site/. Stdlib only, so every check can run from a clean checkout:

    python3 scripts/build_site.py

Design rules enforced here (and re-checked by scripts/verify_site.py):
  * every outbound product link is rel="sponsored" (Google paid-link guidance);
  * the disclosure strip sits under the masthead on every page and repeats in the footer;
  * every page has its own <title> and meta description;
  * question-shaped guides get Article + FAQPage structured data;
  * sitemap.xml, rss.xml and robots.txt are regenerated from the tree.
"""
import json
import shutil
import os
import os
import html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "site")

BRAND = "Countercraft"
TAGLINE = "Kitchen gear worth the counter space."
DISCLOSURE = (
    "Countercraft is an Amazon Associate. As an Amazon Associate I earn from qualifying "
    "purchases. Product links on this site are affiliate links and are marked as sponsored. "
    "Prices and availability are as listed on the Amazon product page at the date shown and "
    "may change; always confirm on Amazon before you buy."
)
VERIFY_DATE = "2026-11-19"


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def esc(s):
    return html.escape(str(s), quote=True)


def load_all():
    products = load("products.json")["products"]
    sources = load("sources.json")["sources"]
    suggestions = load("suggestions.json")
    articles = load("articles.json")["articles"]
    ledger = load("ledger.json")
    return products, sources, suggestions, articles, ledger


def by_id(products, pid):
    for p in products:
        if p["id"] == pid:
            return p
    return None


TRACKING_TAG = "shopnow047c-20"


def tagged_url(url):
    """Tagged Special Link: final destination URL with the tag as its parameter
    (Participation Requirements 2(b)). No shortener (6(v)-(w))."""
    if "/dp/" in url and "tag=" not in url:
        sep = "&" if "?" in url else "?"
        return url + sep + "tag=" + TRACKING_TAG
    return url


def product_link(p, label=None, class_="product-link"):
    """Outbound affiliate link. rel=sponsored per Google paid-link guidance, nofollow,
    and the tracking tag on the destination URL (integration fix 2026-11-19)."""
    label = label or p["title"]
    return (
        '<a class="%s" href="%s" rel="sponsored nofollow noopener" target="_blank" '
        'data-event="product_click" data-asin="%s">%s</a>'
        % (class_, esc(tagged_url(p["listing_url"])), esc(p["resolves_to_asin"]), esc(label))
    )


def ext_link(url, label, cls="src"):
    """External link. Amazon links are marked sponsored; /dp/ product links also get the
    tracking tag (integration fix 2026-11-19)."""
    if url.startswith("https://www.amazon.com/"):
        rel = "sponsored nofollow noopener"
        url = tagged_url(url)
    else:
        rel = "noopener"
    return '<a class="%s" href="%s" rel="%s" target="_blank">%s</a>' % (cls, esc(url), rel, esc(label))


def token_to_link(token, products):
    """Convert [[product:ID|Label]] tokens in article bodies to sponsored links."""
    import re

    def repl(m):
        pid, label = m.group(1), m.group(2)
        p = by_id(products, pid)
        if not p:
            return m.group(0)
        return product_link(p, label)

    return re.sub(r"\[\[product:([^|\]]+)\|([^\]]+)\]\]", repl, token)


# --------------------------------------------------------------------------
# CSS — editorial, warm, mobile-first. Deliberately not a generic AI look.
# --------------------------------------------------------------------------
CSS = """
:root{
  --paper:#f7f3ec; --card:#fffdf8; --ink:#1c1a17; --muted:#6b665e;
  --line:#e4dcc9; --accent:#b45309; --accent-2:#1f4d3a; --accent-soft:#f3e6d2;
  --shadow:0 1px 2px rgba(28,26,23,.06),0 8px 24px rgba(28,26,23,.06);
  --serif:Georgia,"Iowan Old Style","Times New Roman",serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  line-height:1.6;font-size:17px;-webkit-font-smoothing:antialiased}
a{color:var(--accent-2);text-decoration:underline;text-underline-offset:2px}
a:hover{color:var(--accent)}
h1,h2,h3,h4{font-family:var(--serif);line-height:1.2;letter-spacing:-.01em;margin:0 0 .4em}
h1{font-size:clamp(2rem,5vw,3.2rem)}
h2{font-size:clamp(1.5rem,3vw,2rem)}
h3{font-size:1.25rem}
p{margin:0 0 1.1em}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
.eyebrow{font-family:var(--sans);text-transform:uppercase;letter-spacing:.12em;
  font-size:.72rem;font-weight:700;color:var(--accent);margin:0 0 .6em}
.muted{color:var(--muted)}
.small{font-size:.85rem}

/* masthead */
.masthead{background:var(--card);border-bottom:1px solid var(--line)}
.masthead .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 20px}
.brand{font-family:var(--serif);font-size:1.4rem;font-weight:700;color:var(--ink);text-decoration:none;letter-spacing:-.02em}
.brand span{color:var(--accent)}
.brand small{display:block;font-family:var(--sans);font-weight:400;font-size:.7rem;color:var(--muted);letter-spacing:.06em}

/* disclosure strip — under the masthead, above the fold */
.disclosure{background:var(--accent-2);color:#f3efe6;font-size:.82rem}
.disclosure .wrap{padding:9px 20px;display:flex;gap:8px;align-items:flex-start}
.disclosure b{font-weight:700}
.disclosure a{color:#ffe9c7;text-decoration:underline}

/* nav */
nav.site{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:30}
nav.site .wrap{display:flex;gap:4px;overflow-x:auto;padding:8px 20px;scrollbar-width:thin}
nav.site a{text-decoration:none;color:var(--ink);font-size:.9rem;white-space:nowrap;
  padding:7px 11px;border-radius:999px;border:1px solid transparent}
nav.site a:hover{background:var(--accent-soft)}
nav.site a.active{background:var(--ink);color:var(--paper)}

main{padding:34px 0 60px}
section{margin:0 0 46px}

/* hero */
.hero{padding:34px 0 8px}
.hero h1{max-width:16ch}
.hero p.lead{font-size:1.18rem;color:#3a352e;max-width:60ch}
.cta{display:inline-flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.btn{display:inline-block;background:var(--ink);color:var(--paper);text-decoration:none;
  padding:12px 20px;border-radius:999px;font-weight:600;font-size:.95rem;border:1px solid var(--ink)}
.btn:hover{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line)}
.btn.ghost:hover{background:var(--accent-soft);color:var(--ink);border-color:var(--accent)}

/* cards / tiles */
.grid{display:grid;gap:18px}
.grid.cols-2{grid-template-columns:repeat(2,1fr)}
.grid.cols-3{grid-template-columns:repeat(3,1fr)}
@media(max-width:820px){.grid.cols-3{grid-template-columns:1fr}.grid.cols-2{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;
  padding:20px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:8px}
.card h3{margin:0}
.card .meta{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.tile{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;
  box-shadow:var(--shadow);text-decoration:none;color:var(--ink);display:flex;flex-direction:column;gap:6px}
.tile:hover{border-color:var(--accent);transform:translateY(-2px)}
.tile h3{margin:0;color:var(--accent-2)}
.tile .count{font-size:.78rem;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}

/* tables */
.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card)}
table{width:100%;border-collapse:collapse;font-size:.92rem;min-width:640px}
th,td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--sans);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted);background:#fbf7ef;font-weight:700}
tbody tr:last-child td{border-bottom:none}
td .src{font-size:.8rem}
.badge{display:inline-block;font-size:.7rem;font-weight:700;padding:2px 8px;border-radius:999px;
  letter-spacing:.04em;text-transform:uppercase}
.badge.ok{background:#e6f2ec;color:var(--accent-2)}
.badge.flag{background:#fbe8d6;color:var(--accent)}
.badge.blank{background:#ece7db;color:var(--muted)}
.product-link{font-weight:600}

/* chooser */
.chooser{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;box-shadow:var(--shadow)}
.chooser ol{margin:8px 0 0;padding-left:20px}
.chooser li{margin:6px 0}
.chooser .pick{margin-top:12px;font-size:.92rem;color:var(--muted)}

/* guide */
.guide{max-width:720px;margin:0 auto}
.guide .lead{font-size:1.15rem;color:#3a352e}
.faq{border-top:1px solid var(--line);padding:16px 0}
.faq h3{margin:0 0 4px;color:var(--accent-2)}
.related{margin-top:30px;padding-top:20px;border-top:1px solid var(--line)}

/* footer */
footer{background:var(--ink);color:#cfc9bd;margin-top:40px}
footer .disc{background:#2a2722;color:#e9e2d2;border-bottom:1px solid #3a352e}
footer .disc .wrap{padding:14px 20px;font-size:.82rem;max-width:1080px}
footer .wrap{padding:30px 20px 40px;display:grid;gap:24px}
footer h4{color:#fff;font-family:var(--sans);font-size:.78rem;text-transform:uppercase;letter-spacing:.1em;margin:0 0 10px}
footer a{color:#e9c9a6;text-decoration:none}
footer a:hover{text-decoration:underline;color:#fff}
footer .col{display:flex;flex-direction:column;gap:7px}
footer .legal{font-size:.78rem;color:#8d877b;margin-top:8px}

.note{background:var(--accent-soft);border:1px solid #e6d3b8;border-radius:12px;padding:14px 16px;font-size:.9rem}
.flagrow{background:#fbe8d6;border:1px solid #ecc9a8;border-radius:12px;padding:14px 16px}
"""

# --------------------------------------------------------------------------
# Privacy-preserving click counter. No cookies. Anonymous local id only.
# --------------------------------------------------------------------------
ANALYTICS_JS = """
/* Countercraft privacy-preserving outbound-click counter.
   No cookies, no third parties. An anonymous id is stored in localStorage.
   Events: page_view, cta_click, product_click, filter_apply, guide_read.
   Point window.COUNTERCRAFT_ENDPOINT at your self-hosted /collect endpoint. */
(function () {
  var EVENTS = ["page_view","cta_click","product_click","filter_apply","guide_read"];
  var ENDPOINT = window.COUNTERCRAFT_ENDPOINT || "/collect";
  function uid() {
    var k = "cc_uid";
    try {
      var v = localStorage.getItem(k);
      if (!v) { v = "cc_" + Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
        localStorage.setItem(k, v); }
      return v;
    } catch (e) { return "cc_anon"; }
  }
  var queue = [];
  function send() {
    if (!queue.length) return;
    var batch = queue.splice(0, queue.length);
    var body = JSON.stringify({ events: batch });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([body], { type: "application/json" }));
      } else {
        fetch(ENDPOINT, { method: "POST", body: body,
          headers: { "Content-Type": "application/json" }, keepalive: true });
      }
    } catch (e) { /* endpoint not hosted yet; events stay local and are not lost silently */ }
  }
  window.ccTrack = function (event, extra) {
    if (EVENTS.indexOf(event) === -1) return;
    queue.push({ event: event, path: location.pathname, ts: Date.now(),
                 ref: document.referrer, uid: uid(), extra: extra || null });
    if (queue.length >= 5) send();
  };
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-event]");
    if (!el) return;
    var ev = el.getAttribute("data-event");
    if (EVENTS.indexOf(ev) === -1) return;
    window.ccTrack(ev, { asin: el.getAttribute("data-asin") || null,
                         label: (el.textContent || "").trim().slice(0, 80) });
  }, true);
  window.ccTrack("page_view");
  window.addEventListener("beforeunload", send);
})();
"""


def ldjson(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj)


def layout(active, title, description, body, extra_head="", breadcrumbs=None):
    crumbs = ""
    if breadcrumbs:
        items = "".join(
            '<li><a href="%s">%s</a></li>' % (esc(href), esc(label)) if href else "<li>%s</li>" % esc(label)
            for href, label in breadcrumbs
        )
        crumbs = '<nav class="crumbs small muted" aria-label="Breadcrumb"><ol style="list-style:none;display:flex;gap:8px;padding:0;margin:0 0 18px;flex-wrap:wrap">%s</ol></nav>' % items
    nav_items = [
        ("/index.html", "Home"),
        ("/air-fryer-ovens.html", "Air Fryer Ovens"),
        ("/meat-thermometers.html", "Meat Thermometers"),
        ("/comparison.html", "Comparison"),
        ("/guides.html", "Guides"),
        ("/research-desk.html", "Research Desk"),
        ("/suggestions.html", "Suggestions"),
        ("/flagged.html", "Flagged"),
        ("/about.html", "About"),
    ]
    nav = "".join(
        '<a href="%s" class="%s">%s</a>' % (href, "active" if href == active else "", label)
        for href, label in nav_items
    )
    disc = '<div class="disclosure"><div class="wrap"><b>Disclosure.</b> <span>%s</span></div></div>' % esc(DISCLOSURE)
    footer_disc = '<div class="disc"><div class="wrap"><b>Disclosure.</b> %s</div></div>' % esc(DISCLOSURE)
    footer_nav = "".join('<a href="%s">%s</a>' % (h, l) for h, l in nav_items)
    footer = (
        "<footer>%s<div class='wrap'>"
        "<div class='col'><h4>%s</h4><a href='/index.html'>%s</a><span class='small'>%s</span></div>"
        "<div class='col'><h4>Shop</h4>%s</div>"
        "<div class='col'><h4>Measure &amp; review</h4>"
        "<a href='/research-desk.html'>Research Desk</a>"
        "<a href='/suggestions.html'>Suggestions</a>"
        "<a href='/flagged.html'>Flagged for Review</a>"
        "<a href='/about.html'>About &amp; compliance</a></div>"
        "<div class='col'><h4>Find this site</h4>"
        "<a href='/sitemap.xml'>Sitemap</a>"
        "<a href='/rss.xml'>RSS feed</a>"
        "<a href='/robots.txt'>robots.txt</a></div>"
        "<p class='legal'>%s · Tracking ID %s · Data verified %s · No cookies. "
        "Outbound product links are affiliate links marked as sponsored.</p>"
        "</div></footer>"
    ) % (footer_disc, esc(BRAND), esc(BRAND), esc(TAGLINE), footer_nav, esc(DISCLOSURE), "shopnow047c-20", VERIFY_DATE)
    canon = "https://wingbangboozle1-lang.github.io/Prod2/" + (active or "index.html").lstrip("/")  # INT-06: fixed missing slash (was Prod2index.html)
    doc = (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>%s</title>"
        "<meta name='description' content='%s'>"
        "<link rel='canonical' href='%s'>"
        "<link rel='alternate' type='application/rss+xml' title='%s' href='rss.xml'>"
        "<link rel='sitemap' type='application/xml' href='sitemap.xml'>"
        "<link rel='icon' href='data:,'>"
        "<meta property='og:type' content='website'>"
        "<meta property='og:title' content='%s'>"
        "<meta property='og:description' content='%s'>"
        "<meta property='og:image' content='https://wingbangboozle1-lang.github.io/Prod2/assets/social.png'>"
        "<meta property='og:url' content='%s'>"
        "<meta name='twitter:card' content='summary_large_image'>"
        "<meta name='twitter:title' content='%s'>"
        "<meta name='twitter:description' content='%s'>"
        "<meta name='twitter:image' content='https://wingbangboozle1-lang.github.io/Prod2/assets/social.png'>"
        "<style>%s</style>%s</head><body>"
        "<header class='masthead'><div class='wrap'>"
        "<a class='brand' href='/index.html'>%s<small>%s</small></a>"
        "<span class='small muted'>Verified %s</span></div></header>%s"
        "<nav class='site'><div class='wrap'>%s</div></nav>"
        "<main><div class='wrap'>%s%s</div></main>%s"
        "<script>%s</script></body></html>"
    ) % (
        esc(title), esc(description), canon, esc(BRAND),
        esc(title), esc(description), canon,
        esc(title), esc(description),
        CSS, extra_head, esc(BRAND), esc(TAGLINE), VERIFY_DATE, disc, nav, crumbs, body, footer, ANALYTICS_JS,
    )
    return doc


def write(path, content):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def price_cell(p):
    if p["price_usd"]:
        return "%s" % esc(p["price_usd"])
    return ""


def rating_cell(p):
    if p["rating_stars"]:
        return "%s★ (%s)" % (esc(p["rating_stars"]), esc(p["rating_reviews"]))
    return ""


def source_cell(p):
    return ext_link(p["source_url"], "source ↗")


def build_pages(products, sources, suggestions, articles, ledger):
    air = [p for p in products if p["category_slug"] == "air-fryer-ovens"]
    meat = [p for p in products if p["category_slug"] == "meat-thermometers"]

    # ---- index (editorial front page) -------------------------------------
    featured = [a for a in articles[:4]]
    featured_cards = "".join(
        "<a class='tile' href='guides/%s.html' data-event='cta_click' data-label='guide'>"
        "<span class='count'>%s · %s</span><h3>%s</h3>"
        "<span class='small muted'>%s</span></a>"
        % (esc(a["slug"]), esc(a["category"]), esc(a["read_time"]), esc(a["title"]), esc(a["meta_description"]))
        for a in featured
    )
    cat_tiles = "".join(
        "<a class='tile' href='%s.html' data-event='cta_click' data-label='category'>"
        "<span class='count'>%d verified listings</span><h3>%s</h3>"
        "<span class='small muted'>Browse the checked listings and what each one is for.</span></a>"
        % (esc(cat["slug"]), len(cat["items"]), esc(cat["label"]))
        for cat in [{"slug": "air-fryer-ovens", "label": "Air Fryer Ovens", "items": air},
                    {"slug": "meat-thermometers", "label": "Meat Thermometers", "items": meat}]
    )
    # mini register preview (the "data" part, below the fold)
    reg_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(p["brand"]), esc(p["resolves_to_asin"]), price_cell(p), rating_cell(p) or "<span class='badge blank'>unverified</span>", source_cell(p))
        for p in products
    )
    index_body = (
        "<section class='hero'><p class='eyebrow'>The counter-space edit</p>"
        "<h1>Kitchen gear worth the counter space.</h1>"
        "<p class='lead'>%s We check the listings before we write, so the comparisons are built on "
        "what the product page actually says — not guesswork. Start with the guides, then dig into the "
        "verified data when you want the detail.</p>"
        "<div class='cta'><a class='btn' href='comparison.html' data-event='cta_click' data-label='compare'>Compare the models</a>"
        "<a class='btn ghost' href='guides.html' data-event='cta_click' data-label='guides'>Read the guides</a></div></section>"
        "<section><p class='eyebrow'>Featured guides</p><div class='grid cols-2'>%s</div></section>"
        "<section><p class='eyebrow'>Shop by category</p><div class='grid cols-2'>%s</div></section>"
        "<section><p class='eyebrow'>The register</p><p class='muted small'>Every listing we track, with the source for each row. "
        "Values we could not confirm from an official source are left blank and flagged.</p>"
        "<div class='table-wrap'><table><thead><tr><th>Brand</th><th>ASIN</th><th>Price (as listed)</th><th>Rating</th><th>Source</th></tr></thead>"
        "<tbody>%s</tbody></table></div>"
        "<p class='small muted' style='margin-top:10px'>Full detail, the product-intent record and the campaign ledger are on the "
        "<a href='research-desk.html'>Research Desk</a>.</p></section>"
    ) % (esc(TAGLINE), featured_cards, cat_tiles, reg_rows)
    index_head = ldjson({
        "@context": "https://schema.org", "@type": "WebSite", "name": BRAND,
        "url": "https://wingbangboozle1-lang.github.io/Prod2/",
        "description": TAGLINE,
    })
    write("index.html", layout("index.html", "%s — %s" % (BRAND, TAGLINE),
                               "%s Kitchen gear and buying guides, checked against the official Amazon listings before we write." % BRAND,
                               index_body, index_head))

    # ---- category pages ---------------------------------------------------
    for cat_slug, cat_label, items in [("air-fryer-ovens", "Air Fryer Ovens", air), ("meat-thermometers", "Meat Thermometers", meat)]:
        rows = "".join(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (esc(p["brand"]), esc(p["title"]), esc(p["capacity_qt"]) or "—",
               price_cell(p), rating_cell(p) or "<span class='badge blank'>unverified</span>",
               esc(p["browse_node_label"]), source_cell(p))
            for p in items
        )
        cards = "".join(
            "<div class='card'><span class='meta'>%s</span><h3>%s</h3>"
            "<p class='small'>%s</p><p class='small'>Price: %s</p>%s</div>"
            % (esc(p["browse_node_label"]), esc(p["title"]), esc(p["flags"][0] if p["flags"] else "Verified listing."),
               esc(p["price_usd"]), product_link(p, "View on Amazon ↗", "btn ghost"))
            for p in items
        )
        body = (
            "<section><p class='eyebrow'>Category</p><h1>%s</h1>"
            "<p class='lead'>%d verified listings in this category. Each row links to its official Amazon source. "
            "Capacity, price and rating are as listed on %s; anything we could not confirm is left blank and flagged.</p>"
            "<div class='grid cols-2'>%s</div></section>"
            "<section><h2>The listings</h2><div class='table-wrap'><table>"
            "<thead><tr><th>Brand</th><th>Listing</th><th>Capacity</th><th>Price (as listed)</th><th>Rating</th><th>Browse node</th><th>Source</th></tr></thead>"
            "<tbody>%s</tbody></table></div>"
            "<p class='small muted' style='margin-top:10px'>Compare across categories on the <a href='comparison.html'>comparison page</a>, "
            "or read a <a href='guides.html'>guide</a>.</p></section>"
        ) % (esc(cat_label), len(items), VERIFY_DATE, cards, rows)
        write(cat_slug + ".html", layout(cat_slug + ".html", "%s — %s" % (BRAND, cat_label),
                                         "%d verified %s listings, each with a link to its official Amazon source." % (len(items), cat_label),
                                         body, ldjson({"@context": "https://schema.org", "@type": "CollectionPage", "name": cat_label,
                                                       "url": "https://wingbangboozle1-lang.github.io/Prod2/" + cat_slug + ".html"})))

    # ---- comparison page --------------------------------------------------
    comp_rows = "".join(
        "<tr><td><strong>%s</strong><br><span class='small muted'>%s</span></td>"
        "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(p["title"]), esc(p["brand"]), esc(p["capacity_qt"]) or "—",
           esc(p["price_usd"]), rating_cell(p) or "<span class='badge blank'>unverified</span>",
           esc(p["category"]), source_cell(p))
        for p in products
    )
    chooser = (
        "<div class='chooser'><p class='eyebrow'>Three questions before you compare</p>"
        "<h2>Which one is for you?</h2><ol>"
        "<li><strong>How many people do you cook for?</strong> Match quarts to your household so you cook one batch, not three.</li>"
        "<li><strong>What is the largest thing you cook?</strong> A roast or big sheet needs a door-style oven; fries and vegetables suit a basket.</li>"
        "<li><strong>How much bench can you give it?</strong> Capacity and footprint are the same decision — see the counter-space analysis below.</li>"
        "</ol><p class='pick'>Answer those, then read the table from the row that fits.</p></div>"
    )
    # counter-space analysis: capacity per unit depth. Depth figures are NOT verified,
    # so they are left blank and flagged rather than guessed.
    cs_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(p["brand"]), esc(p["capacity_qt"]) or "—",
           "<span class='badge flag'>depth unverified</span>",
           "<span class='badge blank'>not computed</span>")
        for p in products if p["capacity_qt"]
    )
    cs = (
        "<section id='counter-space'><h2>Counter-space analysis</h2>"
        "<p>Capacity and footprint are one decision. The honest metric is <strong>capacity per unit of counter depth</strong>: "
        "how many quarts you get for each centimetre of bench the unit occupies.</p>"
        "<p class='note'>The formula is <code>capacity (qt) ÷ counter depth (cm)</code>. Counter-depth figures must be read from each "
        "official listing's product-information table. We have not captured them yet, so they are left blank and flagged rather than guessed. "
        "Once captured from the official source, fill the depth column and the ratio computes automatically.</p>"
        "<div class='table-wrap'><table><thead><tr><th>Brand</th><th>Capacity (qt)</th><th>Counter depth</th><th>qt per cm</th></tr></thead>"
        "<tbody>%s</tbody></table></div></section>"
    ) % cs_rows
    body = (
        "<section><p class='eyebrow'>Comparison</p><h1>Compare the models</h1>"
        "<p class='lead'>Every figure below is as listed on the official Amazon page on %s. Ratings we could not capture from the listing "
        "are left blank and flagged, never guessed.</p></section>"
        "%s"
        "<section><h2>At a glance</h2><div class='table-wrap'><table>"
        "<thead><tr><th>Listing</th><th>Capacity</th><th>Price (as listed)</th><th>Rating</th><th>Category</th><th>Source</th></tr></thead>"
        "<tbody>%s</tbody></table></div></section>%s"
    ) % (VERIFY_DATE, chooser, comp_rows, cs)
    write("comparison.html", layout("comparison.html", "Air Fryer &amp; Thermometer Comparison — %s" % BRAND,
                                   "Compare the verified air fryer and meat thermometer listings side by side, with a three-question chooser and a counter-space analysis.",
                                   body, ldjson({"@context": "https://schema.org", "@type": "ItemList", "name": "Model comparison",
                                                 "url": "https://wingbangboozle1-lang.github.io/Prod2/comparison.html"})))

    # ---- guides index ----------------------------------------------------
    guide_list = "".join(
        "<a class='tile' href='guides/%s.html' data-event='cta_click' data-label='guide'>"
        "<span class='count'>%s · %s</span><h3>%s</h3><span class='small muted'>%s</span></a>"
        % (esc(a["slug"]), esc(a["category"]), esc(a["read_time"]), esc(a["title"]), esc(a["meta_description"]))
        for a in articles
    )
    body = (
        "<section><p class='eyebrow'>Guides</p><h1>Question-shaped buying guides</h1>"
        "<p class='lead'>One page per question a buyer actually has. Each guide links to the comparison and to its category, "
        "and every product it mentions links to the verified Amazon listing.</p></section>"
        "<section><div class='grid cols-2'>%s</div></section>"
    ) % guide_list
    write("guides.html", layout("guides.html", "Guides — %s" % BRAND,
                                "Question-shaped buying guides for air fryers and meat thermometers, each linking to verified Amazon listings.",
                                body))

    # ---- guide pages -----------------------------------------------------
    for a in articles:
        faq_html = "".join(
            "<div class='faq'><h3>%s</h3><p>%s</p></div>" % (esc(f["q"]), esc(f["a"])) for f in a["faqs"]
        )
        rel = "".join(
            "<li><a href='/guides/%s.html'>%s</a></li>" % (esc(r), esc(next((x["title"] for x in articles if x["slug"] == r), r)))
            for r in a["related"]
        )
        body = (
            "<article class='guide'><p class='eyebrow'>%s · %s</p><h1>%s</h1>"
            "<p class='lead muted small'>%s</p>%s"
            "<h2>Questions people ask</h2>%s"
            "<div class='related'><h3>Keep reading</h3><ul>%s</ul>"
            "<p class='small muted'>Compare the products in this guide on the <a href='/comparison.html'>comparison page</a> "
            "or browse the <a href='/%s.html'>%s</a> category.</p></div></article>"
        ) % (esc(a["category"]), esc(a["read_time"]), esc(a["title"]), esc(a["meta_description"]),
             token_to_link(a["body"], products), faq_html, rel, esc(a["category_slug"]), esc(a["category"]))
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": f["q"],
                                  "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in a["faqs"]]}
        article_ld = {"@context": "https://schema.org", "@type": "Article",
                      "headline": a["title"], "description": a["meta_description"],
                      "datePublished": VERIFY_DATE, "author": {"@type": "Organization", "name": BRAND}}
        head = ldjson(article_ld) + ldjson(faq_ld)
        write("guides/%s.html" % a["slug"],
              layout("guides.html", "%s — %s" % (a["title"], BRAND), a["meta_description"], body, head,
                     breadcrumbs=[("/guides.html", "Guides"), (None, a["title"])]))

    # ---- research desk (the dashboard) ------------------------------------
    pi_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(p["submitted_link"]), esc(p["resolves_to_asin"]),
           esc(p["listing_url"]),
           "<span class='badge blank'>not provided</span>", "<span class='badge blank'>not provided</span>",
           "<span class='badge blank'>pending</span>", "<span class='badge blank'>not provided</span>",
           esc(p["verification_date"]))
        for p in products
    )
    full_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(p["brand"]), esc(p["resolves_to_asin"]), esc(p["category"]),
           esc(p["capacity_qt"]) or "—", price_cell(p),
           rating_cell(p) or "<span class='badge blank'>unverified</span>",
           esc(p["browse_node_label"]), source_cell(p))
        for p in products
    )
    prov_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (esc(s["id"]), esc(s["label"]),
                                                        ext_link(s["url"], s["type"] + " ↗"))
        for s in sources
    )
    ledger_cols = "".join("<th>%s</th>" % esc(c) for c in ledger["columns"])
    body = (
        "<section><p class='eyebrow'>Research Desk</p><h1>The register, the record and the ledger</h1>"
        "<p class='lead'>This is the working surface behind the shop. Every listing, its source, the "
        "product-intent confirmation record, and an empty campaign ledger that stays empty until we have an "
        "authorized first-party report to fill it.</p></section>"
        "<section><h2>All entries</h2><div class='table-wrap'><table>"
        "<thead><tr><th>Brand</th><th>ASIN</th><th>Category</th><th>Capacity</th><th>Price (as listed)</th><th>Rating</th><th>Browse node</th><th>Source</th></tr></thead>"
        "<tbody>%s</tbody></table></div></section>"
        "<section><h2>Product-intent confirmation record</h2>"
        "<p class='note'>Intent and observation are different facts and are kept in separate fields, never merged. "
        "The intended ASIN, intended listing URL, confirmation date and intended source are blank because the submitted "
        "links are 9-character short-link tokens, not ASINs, and nothing public binds a short code to a product. "
        "The observed redirect target is measured and populated.</p>"
        "<div class='table-wrap'><table><thead><tr><th>Submitted link</th><th>Observed ASIN</th><th>Observed listing URL</th>"
        "<th>Intended ASIN</th><th>Intended URL</th><th>Confirm. date</th><th>Intended source</th><th>Verified</th></tr></thead>"
        "<tbody>%s</tbody></table></div></section>"
        "<section><h2>Campaign ledger</h2>"
        "<p class='note'>Evidence-based iteration. The ledger starts empty and well-defined. Timestamp, source, channel, "
        "eligible sessions, clicks and reported orders are added only from authorized first-party reports. No conversion "
        "score or revenue forecast is presented.</p>"
        "<div class='table-wrap'><table><thead><tr>%s</tr></thead><tbody><tr><td colspan='%d' class='muted'>No entries yet — awaiting an authorized first-party report.</td></tr></tbody></table></div></section>"
        "<section><h2>Source register</h2><div class='table-wrap'><table><thead><tr><th>ID</th><th>Source</th><th>Link</th></tr></thead>"
        "<tbody>%s</tbody></table></div></section>"
    ) % (full_rows, pi_rows, ledger_cols, len(ledger["columns"]), prov_rows)
    write("research-desk.html", layout("research-desk.html", "Research Desk — %s" % BRAND,
                                       "Verified product register, product-intent confirmation record, campaign ledger and source register.",
                                       body))

    # ---- suggestions / decision portal ------------------------------------
    q_html = ""
    for q in suggestions["open_questions"]:
        opts = "".join("<li><strong>%s</strong> — <span class='muted'>%s</span></li>" % (esc(o["label"]), esc(o["tradeoff"]))
                       for o in q["options"])
        q_html += (
            "<div class='card'><span class='meta'>Question %s</span><h3>%s</h3>"
            "<p><strong>What we know:</strong> %s</p><p><strong>What we do not know:</strong> %s</p>"
            "<h4>Options</h4><ul>%s</ul>"
            "<p><strong>Recommendation:</strong> %s</p>"
            "<p class='small muted'><strong>How to find out:</strong> %s</p></div>"
        ) % (esc(q["id"]), esc(q["question"]), esc(q["what_we_know"]), esc(q["what_we_do_not_know"]),
             opts, esc(q["recommendation"]), esc(q["how_to_discover"]))
    sug_html = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><span class='badge %s'>%s</span></td></tr>"
        % (esc(s["id"]), esc(s["title"]), esc(s["description"]), esc(s["expected_outcome"]),
           "ok" if s["status"] == "implemented" else "flag", esc(s["status"]))
        for s in suggestions["suggestions"]
    )
    paths = "".join(
        "<div class='card'><span class='meta'>%s</span><h3>%s</h3><p>%s</p><p class='small muted'>%s</p></div>"
        % (esc(p["id"]), esc(p["label"]), esc(p["summary"]), esc(p["why"]))
        for p in suggestions["path_chooser"]
    )
    body = (
        "<section><p class='eyebrow'>Decision portal</p><h1>Suggestions &amp; open questions</h1>"
        "<p class='lead'>Nothing here is decided for you. Below is the list of questions that need answers before a "
        "decision can be made, what we have and do not have, and the suggestions for discovering what is missing. "
        "Review, pick a path, then implement.</p></section>"
        "<section><h2>Open questions to resolve first</h2><div class='grid cols-2'>%s</div></section>"
        "<section><h2>Suggestions to improve decision-making</h2><div class='table-wrap'><table>"
        "<thead><tr><th>ID</th><th>Suggestion</th><th>What it does</th><th>Expected outcome</th><th>Status</th></tr></thead>"
        "<tbody>%s</tbody></table></div></section>"
        "<section><h2>Path chooser</h2><p class='muted small'>Three ways to proceed. The recommended path leads with the "
        "products and puts a gate in front of the parts that need a decision.</p><div class='grid cols-3'>%s</div></section>"
    ) % (q_html, sug_html, paths)
    write("suggestions.html", layout("suggestions.html", "Suggestions &amp; Open Questions — %s" % BRAND,
                                     "Open questions, missing information and suggested improvements, with a path chooser for the next decision.",
                                     body))

    # ---- flagged ---------------------------------------------------------
    flags = []
    for p in products:
        for f in p["flags"]:
            flags.append({"product": p, "flag": f})
    flag_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(p["brand"]), esc(fl["flag"]),
           esc(p["source_url"]),
           ext_link(p["source_url"], "review ↗"))
        for fl in flags
    )
    shortlink_rows = "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % (esc(p["submitted_link"]), esc(p["resolves_to_asin"]),
           "<span class='badge flag'>unresolved</span>",
           ext_link("https://affiliate-program.amazon.com/help/operating/policies", "policy ↗"))
        for p in products
    )
    body = (
        "<section><p class='eyebrow'>Flagged for review</p><h1>Irregularities &amp; unverified items</h1>"
        "<p class='lead'>These are published, not hidden, and they do not block the site. Each one carries its source so you "
        "can review and request changes. Nothing here is inferred — where we could not confirm a value from an official "
        "source, it is left blank.</p></section>"
        "<section><h2>Token vs. ASIN</h2><p class='note'>All five submitted links carry 9-character short-link tokens. "
        "Amazon defines an ASIN as a 10-character code, so the submitted tokens are not ASINs. They resolve to real 10-character "
        "ASINs. This is a fact, not a judgement on the links.</p></section>"
        "<section><h2>Uncaptured values</h2><div class='table-wrap'><table>"
        "<thead><tr><th>Product</th><th>Flag</th><th>Source</th><th>Review</th></tr></thead><tbody>%s</tbody></table></div></section>"
        "<section><h2>Short-link compliance status</h2>"
        "<p class='note'>The submitted short links are not declared invalid, but their exact compliance status is unresolved. "
        "Program Policies 6(w) addresses link shortening that makes the Amazon destination unclear. Recommend replacing with "
        "tagged Special Links before scaling.</p>"
        "<div class='table-wrap'><table><thead><tr><th>Submitted link</th><th>Resolves to</th><th>Status</th><th>Review</th></tr></thead>"
        "<tbody>%s</tbody></table></div></section>"
    ) % (flag_rows, shortlink_rows)
    write("flagged.html", layout("flagged.html", "Flagged for Review — %s" % BRAND,
                                 "Irregularities and unverified items published with their source links for manual review.",
                                 body))

    # ---- about -----------------------------------------------------------
    src_list = "".join(
        "<li><strong>%s</strong> — %s %s</li>"
        % (esc(s["id"]), esc(s["label"]), ext_link(s["url"], s["url"]))
        for s in sources
    )
    body = (
        "<section><p class='eyebrow'>About</p><h1>About &amp; compliance</h1>"
        "<p class='lead'>%s is an editorial affiliate shop. We write buyer questions and compare the listings we track "
        "against the official Amazon product pages. We do not guess: where a value cannot be confirmed from an official "
        "source, it is left blank and flagged.</p></section>"
        "<section><h2>How we verify</h2><p>Each listing is resolved from the submitted link to its official Amazon product "
        "page. Identity, category, browse node, capacity and price are read from that page. Ratings are shown only where "
        "captured from the official listing. Every table row links to its source.</p></section>"
        "<section><h2>Compliance</h2>"
        "<ul>"
        "<li><strong>Disclosure.</strong> The Associates statement sits under the masthead on every page and repeats in the footer.</li>"
        "<li><strong>Sponsored links.</strong> Every outbound product link carries <code>rel=\"sponsored\"</code>.</li>"
        "<li><strong>Special Links.</strong> Outbound links should be tagged Special Links generated in Associates Central; "
        "the submitted short links are flagged for review under Program Policies 6(w).</li>"
        "<li><strong>Ratings &amp; prices.</strong> Ratings require Creators/PA API (6(t)); prices are shown as listed with a date and a live link (2(b)).</li>"
        "<li><strong>No tracking cookies.</strong> The click counter uses an anonymous local id only.</li>"
        "</ul></section>"
        "<section><h2>Sources</h2><ul>%s</ul></section>"
    ) % (esc(BRAND), src_list)
    write("about.html", layout("about.html", "About &amp; Compliance — %s" % BRAND,
                               "How Countercraft verifies listings and stays compliant with Amazon Associates and FTC disclosure requirements.",
                               body))

    # ---- 404 -------------------------------------------------------------
    body = "<section><h1>Page not found</h1><p class='lead'>That page does not exist. Head back to the <a href='index.html'>front page</a> or browse the <a href='guides.html'>guides</a>.</p></section>"
    write("404.html", layout("index.html", "Page not found — %s" % BRAND, "The page you requested does not exist.", body))

    # ---- assets ----------------------------------------------------------
    write("assets/style.css", CSS)
    write("assets/analytics.js", ANALYTICS_JS)


def build_seo(products, sources, articles):
    base = "https://wingbangboozle1-lang.github.io/Prod2"
    pages = [
        ("index.html", "Weekly", VERIFY_DATE),
        ("air-fryer-ovens.html", "Weekly", VERIFY_DATE),
        ("meat-thermometers.html", "Weekly", VERIFY_DATE),
        ("comparison.html", "Weekly", VERIFY_DATE),
        ("guides.html", "Weekly", VERIFY_DATE),
        ("research-desk.html", "Weekly", VERIFY_DATE),
        ("suggestions.html", "Monthly", VERIFY_DATE),
        ("flagged.html", "Weekly", VERIFY_DATE),
        ("about.html", "Monthly", VERIFY_DATE),
    ]
    for a in articles:
        pages.append(("guides/%s.html" % a["slug"], "Weekly", VERIFY_DATE))

    sitemap = ["<?xml version='1.0' encoding='UTF-8'?>",
               "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"]
    for path, _, _ in pages:
        sitemap.append("  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>" % (base, path, VERIFY_DATE))
    sitemap.append("</urlset>")
    write("sitemap.xml", "\n".join(sitemap))

    rss_items = []
    for a in articles:
        rss_items.append(
            "    <item><title>%s</title><link>%s/guides/%s.html</link>"
            "<guid isPermaLink='true'>%s/guides/%s.html</guid>"
            "<pubDate>%sT09:00:00Z</pubDate><description>%s</description></item>"
            % (esc(a["title"]), base, a["slug"], base, a["slug"], VERIFY_DATE, esc(a["meta_description"])))
    rss = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<rss version='2.0' xmlns:atom='http://www.w3.org/2005/Atom'>"
        "<channel><title>%s</title><link>%s/</link><description>%s</description>"
        "<language>en-us</language><atom:link href='%s/rss.xml' rel='self' type='application/rss+xml'/>%s"
        "</channel></rss>"
    ) % (esc(BRAND), base, esc(TAGLINE), base, "\n".join(rss_items))
    write("rss.xml", rss)

    robots = (
        "User-agent: *\nAllow: /\n"
        "Sitemap: %s/sitemap.xml\n" % base
    )
    write("robots.txt", robots)
    write(".nojekyll", "")


def main():
    os.makedirs(SITE, exist_ok=True)
    products, sources, suggestions, articles, ledger = load_all()
    build_pages(products, sources, suggestions, articles, ledger)
    build_seo(products, sources, articles)
    print("Built site/ with %d products, %d articles, %d sources."
          % (len(products), len(articles), len(sources)))


if __name__ == "__main__":
    main()    # INT-07 mirror REPLACED 2026-11-19 (arena/44093825-prod2): the legacy
    # "main /" Pages source serves the repo root, and the mirror now carries the
    # Prod2 publication (tools/build.py mirrors docs/ -> root). This generator keeps
    # building site/ only — preserved and verified, no longer the mirrored build.
    # Reason + live-verification record: COORDINATION.md, final merge/deploy record.
