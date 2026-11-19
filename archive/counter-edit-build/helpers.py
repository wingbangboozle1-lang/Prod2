"""Shared helpers for The Counter Edit site build.

Rules encoded here:
- Every outbound Amazon link is tagged with the Associates tracking ID and carries
  rel="sponsored nofollow noopener" (S-05) and data-outbound attributes (event E2).
- Every page gets a unique title + meta description (S-04), canonical URL, and OG/Twitter cards.
- The disclosure strip sits under the masthead region on every page (FTC clear-and-conspicuous).
- Blank-by-design: prices, ratings and dimensions are never invented (F-04/F-05).
"""
import html as _html

TAG = "shopnow047c-20"
BASE = "https://wingbangboozle1-lang.github.io/Prod2"
PREFIX = "/Prod2"
SITE_NAME = "The Counter Edit"
TAGLINE = "Air-fryer decisions, minus the noise."
VERIFY_DATE = "2026-11-19"
# Owner action T-10: replace this with the real Search Console meta tag.
SEARCH_CONSOLE_META = ""


def u(path: str) -> str:
    return PREFIX + path


def esc(s: str) -> str:
    return _html.escape(s, quote=False)


def amz_url(asin: str, tag: bool = True) -> str:
    base = f"https://www.amazon.com/dp/{asin}"
    return f"{base}?tag={TAG}" if tag else base


def aff(pid: str, position: str, label: str = "Check price on Amazon") -> str:
    """Tagged Special Link. rel=sponsored nofollow noopener + measurement attrs."""
    p = PRODUCTS[pid]
    return (
        f'<a href="{amz_url(p["asin"])}" rel="sponsored nofollow noopener" target="_blank" '
        f'data-outbound data-product="{pid}" data-position="{position}">{label}<span class="arrow"> ↗</span></a>'
    )


def official(pid: str) -> str:
    """Reference link to the official listing — also tagged and sponsored:
    the site's single invariant is that EVERY outbound Amazon link is a tagged,
    marked affiliate link (R-09), including citations."""
    p = PRODUCTS[pid]
    return (
        f'<a href="{amz_url(p["asin"])}" rel="sponsored nofollow noopener" target="_blank" '
        f'data-outbound data-product="{pid}" data-position="citation">amazon.com/dp/{p["asin"]} ↗</a>'
    )


PRODUCTS = {
    "P1": {
        "asin": "B0CDY277D3",
        "brand": "CHEFMAN",
        "short": "Chefman 6 Qt Dual Basket",
        "type": "Dual-basket air fryer",
        "kind_icon": "🧺🧺",
        "title": "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black",
        "verified_facts": [
            "6-quart dual-basket format",
            "two independent 3-quart nonstick baskets",
            "baskets listed as dishwasher safe",
            "sync-finish and hi-fry modes named in the listing title",
        ],
        "best_for": "Cooking two dishes at once that finish together",
        "submitted": "https://link.amazon/B04G1MEwY",
        "observed_asin": "B0CDY277D3",
    },
    "P2": {
        "asin": "B09B7SB46R",
        "brand": "Emeril Lagasse",
        "short": "Emeril Lagasse 26 QT French Door",
        "type": "Oven-style air fryer toaster oven",
        "kind_icon": "🚪",
        "title": "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included",
        "verified_facts": [
            "26-quart oven-style cavity",
            "french-door opening",
            "24 one-touch preset options",
            "six cooking accessories included",
        ],
        "best_for": "Batch cooking, roasting and replacing a toaster oven",
        "submitted": "https://link.amazon/B02NbDxp3",
        "observed_asin": "B09B7SB46R",
    },
    "P3": {
        "asin": "B08DKYBTPH",
        "brand": "Chefman",
        "short": "Chefman 8 Qt TurboFry",
        "type": "Single-basket air fryer",
        "kind_icon": "🧺",
        "title": "Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel",
        "verified_facts": [
            "8-quart single basket",
            "4-in-1 function set",
            "450°F hi-fry option",
            "XL nonstick basket listed as dishwasher safe",
        ],
        "best_for": "One big basket with the smallest fuss at the sink",
        "submitted": "https://link.amazon/B00hJ57DV",
        "observed_asin": "B08DKYBTPH",
    },
    "P4": {
        "asin": "B0DHZTCNR5",
        "brand": "ThermoMaven",
        "short": "ThermoMaven 1-Sec Instant Read",
        "type": "Instant-read thermometer",
        "kind_icon": "🌡️",
        "title": "ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy | NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black",
        "verified_facts": [
            "1-second read claimed in the listing title",
            "±0.5°F accuracy claimed",
            "NIST and NSF certified (per listing title)",
            "IP67 waterproof rating",
        ],
        "best_for": "Fast doneness checks without app setup",
        "submitted": "https://link.amazon/B0c8moW59",
        "observed_asin": "B0DHZTCNR5",
    },
    "P5": {
        "asin": "B0DZFD6R9Z",
        "brand": "CHEF iQ",
        "short": "CHEF iQ Sense Gen3 Wireless",
        "type": "Wireless smart thermometer",
        "kind_icon": "📡",
        "title": "CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi Unlimited Range | 1000°F Heat Safe | 5 Sensors | BBQ, Grill, Oven, Smoker, Air Fryer | Gen3",
        "verified_facts": [
            "wireless with WiFi unlimited range (per listing title)",
            "three ultra-thin probes included",
            "five sensors",
            "1000°F heat-safe claim",
        ],
        "best_for": "Long cooks where you want range and app alerts",
        "submitted": "https://link.amazon/B0f3GKalj",
        "observed_asin": "B0DZFD6R9Z",
    },
}


DISCLOSURE_HTML = f"""<div class="disclosure" data-disclosure>
  <div class="wrap"><span class="tag">Affiliate disclosure</span>
  <span>The Counter Edit earns from qualifying purchases as an Amazon Associate. Product links on this site are paid affiliate links to Amazon.com &mdash; the price you pay never changes. <a href="{u('/disclosure.html')}">How this works</a></span></div>
</div>"""


def header(active: str) -> str:
    def nav(label, href, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'

    return f"""<header class="site-head">
  <div class="wrap">
    <a class="wordmark" href="{u('/index.html')}"><span class="dot"></span>{SITE_NAME}</a>
    <nav class="site-nav" aria-label="Primary">
      <ul>
        {nav("Guides", u('/guides/index.html'), "guides")}
        {nav("Compare", u('/compare.html'), "compare")}
        {nav("The Shelf", u('/products.html'), "products")}
        {nav("About", u('/about.html'), "about")}
      </ul>
    </nav>
  </div>
</header>"""


def footer() -> str:
    return f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="foot-brand">{SITE_NAME}</div>
        <p style="margin:0 0 8px; color:#cfc7b8;">Question-shaped buyer guides for air fryers and the
        thermometers that keep them honest. Independent, reader-first, and boring where it matters
        &mdash; every claim carries its source.</p>
        <p style="margin:0; font-size:0.82rem; color:#8a8177;">Provisional brand name &mdash; see the
        <a href="{u('/docs/suggestions.html')}">suggestions page</a> for the open decision.</p>
      </div>
      <div>
        <h4>Read</h4>
        <ul>
          <li><a href="{u('/guides/index.html')}">All guides</a></li>
          <li><a href="{u('/compare.html')}">Compare the five</a></li>
          <li><a href="{u('/products.html')}">The Shelf</a></li>
          <li><a href="{u('/rss.xml')}">RSS feed</a></li>
        </ul>
      </div>
      <div>
        <h4>Data room</h4>
        <ul>
          <li><a href="{u('/docs/index.html')}">Dashboard</a></li>
          <li><a href="{u('/docs/requirements.html')}">Requirements</a></li>
          <li><a href="{u('/docs/decisions.html')}">Decisions</a></li>
          <li><a href="{u('/docs/flagged.html')}">Flagged for review</a></li>
          <li><a href="{u('/docs/suggestions.html')}">Suggestions</a></li>
          <li><a href="{u('/docs/open-questions.html')}">Open questions</a></li>
          <li><a href="{u('/docs/metrics.html')}">Metrics plan</a></li>
          <li><a href="{u('/docs/sources.html')}">Source register</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-disclosure">
      <strong>Disclosure:</strong> As an Amazon Associate, {SITE_NAME} earns from qualifying purchases.
      outbound product links to Amazon.com on this site are marked <code>rel="sponsored"</code> and carry our
      Associates tracking ID (<code>{TAG}</code>). They are advertising, and they are labeled as such above the
      fold on every page. Prices and availability on Amazon change without notice; we do not publish prices
      we cannot verify at the moment you read. This site is independent and is not owned by or endorsed by Amazon.
      Compliance references: <a href="https://affiliate-program.amazon.com/help/operating/policies" rel="nofollow noopener" target="_blank">Associates Program Policies</a>
      &middot; <a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers" rel="nofollow noopener" target="_blank">FTC Disclosures 101</a>.
    </div>
    <div class="foot-legal">
      <span>&copy; 2026 {SITE_NAME}. Illustrations are our own; no product photography is used pending the S-18 decision.</span>
      <span><a href="{u('/disclosure.html')}">Disclosure policy</a> &middot; <a href="{u('/docs/index.html')}">Data room</a></span>
    </div>
  </div>
</footer>"""


def head(title: str, desc: str, canonical_path: str, og_type: str = "website") -> str:
    og_url = BASE + canonical_path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{SITE_NAME} desk">
<link rel="canonical" href="{og_url}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{og_url}">
<meta property="og:image" content="{BASE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/assets/img/og-image.jpg">
<link rel="icon" type="image/svg+xml" href="{u('/favicon.svg')}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME} &mdash; new guides" href="{u('/rss.xml')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('/assets/css/style.css')}">
{SEARCH_CONSOLE_META}
<script>window.TCE_ENDPOINT = "";</script>
<script defer src="{u('/assets/js/tce.js')}"></script>
</head>"""


def shell(active: str, title: str, desc: str, canonical_path: str, body: str, og_type: str = "website") -> str:
    return (
        head(title, desc, canonical_path, og_type)
        + f'<body>\n<a class="skip-link" href="#main">Skip to content</a>\n'
        + DISCLOSURE_HTML
        + "\n"
        + header(active)
        + f'\n<main id="main">\n{body}\n</main>\n'
        + footer()
        + "\n</body>\n</html>\n"
    )
