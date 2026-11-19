#!/usr/bin/env python3
"""Build the Countertop Dispatch static site from content/ fragments.

Every page is assembled from one shared chrome (masthead, disclosure strip,
navigation, footer) so that the disclosure gate in tools/check_site.py can
rely on identical markup everywhere. Run from the repo root:

    python3 tools/build_site.py

Outputs HTML pages, sitemap.xml and feed.xml at the repository root, which is
where GitHub Pages (legacy, main branch, root) serves from.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
BASE_URL = "https://wingbangboozle1-lang.github.io/Prod2"
BUILD_DATE = date.today().isoformat()

NAV = [
    ("index.html", "Home"),
    ("guides/index.html", "Guides"),
    ("products.html", "Products"),
    ("comparison.html", "Comparison"),
    ("analysis.html", "Analysis"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged"),
]

FOOTER_READ = [
    ("guides/index.html", "All guides"),
    ("products.html", "Product table"),
    ("comparison.html", "Comparison & chooser"),
    ("category/air-fryers.html", "Air fryers"),
    ("category/meat-thermometers.html", "Meat thermometers"),
]
FOOTER_DASH = [
    ("summary.html", "Executive summary"),
    ("analysis.html", "Analysis & findings"),
    ("suggestions.html", "Suggestions & decisions"),
    ("flagged.html", "Flagged for Review"),
    ("compliance.html", "Disclosure & compliance"),
]
FOOTER_DATA = [
    ("data/products.json", "products.json"),
    ("data/submitted-links.json", "submitted-links.json"),
    ("data/product-intent.json", "product-intent.json"),
    ("data/events.json", "events.json"),
    ("data/campaign-ledger.csv", "campaign-ledger.csv"),
    ("feed.xml", "RSS feed"),
    ("sitemap.xml", "Sitemap"),
    ("robots.txt", "robots.txt"),
    ("https://github.com/wingbangboozle1-lang/Prod2", "Source repo"),
]

DISCLOSURE_STRIP = (
    '<div class="disclosure-strip" role="note">'
    "As an Amazon Associate we earn from qualifying purchases. "
    '<a href="{p}compliance.html">How this site makes money &amp; how sources are checked</a>'
    "</div>"
)

DISCLOSURE_FOOTER = (
    '<p class="footer-disclosure">'
    "<strong>Disclosure:</strong> As an Amazon Associate we earn from qualifying purchases. "
    "Every product link on this site is a Special Link tagged with our Associates ID "
    '<span class="mono">shopnow047c-20</span> and marked <span class="mono">rel=&quot;sponsored&quot;</span>. '
    "Prices, ratings and commission rates are withheld wherever Amazon&rsquo;s Program Policies "
    "restrict how they may be shown &mdash; see "
    '<a href="{p}flagged.html">Flagged for Review</a> and '
    '<a href="{p}compliance.html">Compliance</a>.'
    "</p>"
)


def prefix_for(page_path: str) -> str:
    """Relative prefix from a page to the repository root ('' or '../')."""
    depth = page_path.count("/")
    return "../" * depth


def parse_fragment(raw: str) -> dict:
    """Parse 'key: value' front matter delimited by a line containing only ---."""
    if not raw.startswith("title:"):
        raise ValueError("fragment must start with front matter (title: ...)")
    head, _, body = raw.partition("\n---\n")
    meta: dict[str, str] = {}
    for line in head.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    for required in ("title", "description", "nav"):
        if required not in meta:
            raise ValueError(f"front matter missing '{required}'")
    meta["body"] = body
    return meta


def nav_html(current: str, prefix: str) -> str:
    items = []
    for href, label in NAV:
        attr = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{prefix}{href}"{attr}>{label}</a></li>')
    return '<nav class="mainnav" aria-label="Primary"><ul>' + "".join(items) + "</ul></nav>"


def footer_links(pairs: list[tuple[str, str]], prefix: str) -> str:
    out = []
    for href, label in pairs:
        if href.startswith("http"):
            out.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            out.append(f'<li><a href="{prefix}{href}">{label}</a></li>')
    return "<ul>" + "".join(out) + "</ul>"


def build_page(page_path: str, meta: dict) -> str:
    prefix = prefix_for(page_path)
    title = meta["title"]
    description = meta["description"]
    canonical = f"{BASE_URL}/{page_path}"
    nav = nav_html(meta["nav"], prefix)
    body = meta["body"].replace("{prefix}", prefix)

    jsonld = ""
    if page_path == "index.html":
        data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Countertop Dispatch",
            "url": f"{BASE_URL}/index.html",
            "description": description,
            "inLanguage": "en",
        }
        jsonld = '<script type="application/ld+json">' + json.dumps(data) + "</script>"
    elif page_path.startswith("guides/") and page_path != "guides/index.html":
        data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "datePublished": BUILD_DATE,
            "dateModified": BUILD_DATE,
            "inLanguage": "en",
            "image": f"{BASE_URL}/assets/og-cover.png",
            "author": {"@type": "Organization", "name": "Countertop Dispatch"},
            "publisher": {"@type": "Organization", "name": "Countertop Dispatch"},
            "mainEntityOfPage": canonical,
        }
        jsonld = '<script type="application/ld+json">' + json.dumps(data) + "</script>"

    og_type = meta.get("og_type", "article" if page_path.startswith("guides/") else "website")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}/assets/og-cover.png">
<meta property="og:site_name" content="Countertop Dispatch">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Countertop Dispatch guides" href="{prefix}feed.xml">
<link rel="stylesheet" href="{prefix}assets/style.css">
{jsonld}
<script src="{prefix}assets/analytics.js" defer></script>
</head>
<body>
<header class="masthead">
  <div class="wrap">
    <a class="wordmark" href="{prefix}index.html">Countertop Dispatch</a>
    <p class="tagline">Kitchen appliance buying guides, checked line by line</p>
    <span class="issue-line">Verified 19 Nov 2026</span>
  </div>
</header>
{DISCLOSURE_STRIP.format(p=prefix)}
{nav}
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    {DISCLOSURE_FOOTER.format(p=prefix)}
    <div class="footer-grid">
      <div>
        <h4>Read</h4>
        {footer_links(FOOTER_READ, prefix)}
      </div>
      <div>
        <h4>Dashboards</h4>
        {footer_links(FOOTER_DASH, prefix)}
      </div>
      <div>
        <h4>Data &amp; feeds</h4>
        {footer_links(FOOTER_DATA, prefix)}
      </div>
    </div>
    <div class="colophon">
      <span>Countertop Dispatch &mdash; published from a checked build. Prices change; the listing is the source of truth.</span>
      <span>Built {BUILD_DATE}</span>
    </div>
  </div>
</footer>
<script src="{prefix}assets/site.js" defer></script>
</body>
</html>
"""


def build_sitemap(pages: list[str]) -> str:
    urls = []
    for page in pages:
        loc = f"{BASE_URL}/{page}"
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n"
            f"    <changefreq>weekly</changefreq>\n  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def build_feed() -> str:
    """RSS 2.0 feed: the four question-shaped guides plus the product table."""
    items_spec = [
        ("guides/basket-or-oven-air-fryer.html",
         "Basket or oven-style air fryer: what should you compare?",
         "The two shapes solve different problems. Here is the comparison that actually matters before you measure your counter."),
        ("guides/air-fryer-capacity-checklist.html",
         "A no-hype checklist for comparing air fryer capacity",
         "Quarts, basket depth, and the food you actually cook. A short checklist with no marketing words in it."),
        ("guides/cleanup-counter-space-tradeoffs.html",
         "How to assess cleanup and counter-space trade-offs",
         "Dishwasher-safe parts, wipe-down surfaces, and the maths of what stays on the counter all week."),
        ("guides/multi-function-kitchen-appliance-questions.html",
         "Questions to ask before buying a multi-function kitchen appliance",
         "Twelve questions that separate the functions you will use from the ones printed on the box."),
        ("products.html",
         "All five products, checked against official listings",
         "The full product table: capacity, dimensions, features and a source link on every row."),
    ]
    entries = []
    for path, title, description in items_spec:
        entries.append(
            "  <item>\n"
            f"    <title>{title}</title>\n"
            f"    <link>{BASE_URL}/{path}</link>\n"
            f"    <guid isPermaLink=\"true\">{BASE_URL}/{path}</guid>\n"
            f"    <description>{description}</description>\n"
            f"    <pubDate>{date(2026, 11, 19).strftime('%a, %d %b %Y')} 09:00:00 GMT</pubDate>\n"
            "  </item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "<channel>\n"
        "  <title>Countertop Dispatch</title>\n"
        f"  <link>{BASE_URL}/index.html</link>\n"
        f"  <atom:link href=\"{BASE_URL}/feed.xml\" rel=\"self\" type=\"application/rss+xml\"/>\n"
        "  <description>Question-shaped buying guides for countertop appliances, every claim sourced.</description>\n"
        "  <language>en</language>\n"
        f"  <lastBuildDate>{date(2026, 11, 19).strftime('%a, %d %b %Y')} 09:00:00 GMT</lastBuildDate>\n"
        + "\n".join(entries)
        + "\n</channel>\n</rss>\n"
    )


def main() -> int:
    fragments = sorted(p for p in CONTENT.rglob("*.html"))
    if not fragments:
        print("no content fragments found", file=sys.stderr)
        return 1
    pages: list[str] = []
    titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    for frag in fragments:
        rel = frag.relative_to(CONTENT).as_posix()
        meta = parse_fragment(frag.read_text(encoding="utf-8"))
        if meta["title"] in titles:
            print(f"duplicate title: {meta['title']} ({rel} and {titles[meta['title']]})",
                  file=sys.stderr)
            return 1
        titles[meta["title"]] = rel
        descriptions[meta["description"]] = rel
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_page(rel, meta), encoding="utf-8")
        pages.append(rel)
        print(f"built {rel}")

    # guides/index.html is the hub; ensure feed items reference real pages
    (ROOT / "sitemap.xml").write_text(build_sitemap(pages), encoding="utf-8")
    (ROOT / "feed.xml").write_text(build_feed(), encoding="utf-8")
    print(f"built sitemap.xml ({len(pages)} urls) and feed.xml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
