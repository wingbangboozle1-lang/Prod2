#!/usr/bin/env python3
"""Build The Counter Edit site: one command regenerates site/ from content modules.

Usage: python3 scripts/build.py
Writes:
  site/*.html, site/guides/*.html, site/docs/*.html   (20 pages)
  site/rss.xml, site/sitemap.xml, site/robots.txt
"""
import json
import os
import sys
from email.utils import format_datetime
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers import shell, BASE, PREFIX, SITE_NAME, TAG, TAGLINE, u  # noqa: E402
import content_reader  # noqa: E402
import content_docs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

LASTMOD = "2026-11-19"


def jsonld_for(path: str) -> str:
    """Minimal structured data. No Product schema (no verified offers data to attach)."""
    base = BASE + PREFIX
    org = {
        "@type": "Organization",
        "name": SITE_NAME,
        "url": base + "/",
    }
    if path.startswith("/guides/") and path != "/guides/index.html":
        g = next(x for x in content_reader.GUIDES if path.endswith(x["slug"] + ".html"))
        return json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": g["title"],
            "description": g["standfirst"],
            "image": f"{base}/assets/img/{g['img']}",
            "datePublished": g["date"],
            "dateModified": LASTMOD,
            "inLanguage": "en",
            "author": org,
            "publisher": org,
        })
    if path == "/index.html":
        return json.dumps({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "alternateName": TAGLINE,
            "url": base + "/",
        })
    return ""


def _jsonld_compare_products():
    base = BASE + PREFIX
    items = []
    for i, pid in enumerate(["P1", "P2", "P3", "P4", "P5"], 1):
        from helpers import PRODUCTS
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": PRODUCTS[pid]["short"],
            "url": f"{base}/products.html#{pid}",
        })
    return items


def write(path: str, content: str) -> None:
    full = os.path.join(SITE, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    pages = {}
    for path, (active, title, desc, body) in content_reader.pages().items():
        pages[path] = shell(active, title, desc, path, body)
    for path, (active, title, desc, body) in content_docs.pages().items():
        pages[path] = shell(active, title, desc, path, body)

    for path, html in sorted(pages.items()):
        ld = jsonld_for(path)
        if path in ("/compare.html", "/products.html"):
            ld = json.dumps({
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": "The Counter Edit shelf",
                "itemListElement": _jsonld_compare_products(),
            })
        if ld:
            html = html.replace("</head>", f'<script type="application/ld+json">{ld}</script>\n</head>')
        write(path, html)

    # ---- rss.xml ----
    import content_reader as cr
    items = []
    for g in cr.GUIDES:
        pub = format_datetime(datetime(2026, 11, 19, 9, 0, tzinfo=timezone.utc))
        url = BASE + u(f"/guides/{g['slug']}.html")
        items.append(f"""<item>
      <title>{g['title']}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{pub}</pubDate>
      <description>{g['standfirst']}</description>
    </item>""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_NAME}</title>
    <link>{BASE}{PREFIX}/</link>
    <atom:link href="{BASE}{PREFIX}/rss.xml" rel="self" type="application/rss+xml"/>
    <description>{TAGLINE} Question-shaped buyer guides with every claim sourced.</description>
    <language>en</language>
    <lastBuildDate>{format_datetime(datetime(2026, 11, 19, 9, 0, tzinfo=timezone.utc))}</lastBuildDate>
    {chr(10).join('    ' + i for i in items)}
  </channel>
</rss>
"""
    write("/rss.xml", rss)

    # ---- sitemap.xml ----
    urls = []
    pri = {
        "/index.html": "1.0",
        "/guides/index.html": "0.8",
        "/compare.html": "0.9",
        "/products.html": "0.9",
        "/about.html": "0.5",
        "/disclosure.html": "0.4",
        "/docs/index.html": "0.4",
    }
    for path in sorted(pages):
        if path == "/404.html":
            continue
        url = f"{BASE}{path if path == '/index.html' else path}"
        urls.append(
            f"<url><loc>{url}</loc><lastmod>{LASTMOD}</lastmod>"
            f"<changefreq>weekly</changefreq><priority>{pri.get(path, '0.6')}</priority></url>"
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    write("/sitemap.xml", sitemap)

    # ---- robots.txt ----
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}{PREFIX}/sitemap.xml\n")

    print(f"Built {len(pages)} pages + rss.xml + sitemap.xml + robots.txt into site/")


if __name__ == "__main__":
    main()
