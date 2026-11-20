#!/usr/bin/env python3
"""build.py — renders the published site in docs/ from data/*.json + content/pages/*.html.

Stdlib only. Run from a clean checkout:

    python3 tools/build.py

The build is deterministic: same inputs -> same output. tools/checks.py gates the
result; nothing is published without passing it (see ENGINE.md).
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "p2"
CONTENT = ROOT / "content"
ASSETS_SRC = ROOT / "assets"
DOCS = ROOT / "docs"

BUILD_DATE = "2026-11-20"  # set on each publishing pass


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SETTINGS = load("settings.json")
PRODUCTS = load("products.json")["products"]
INTENTS = load("intent-links.json")["links"]
SOURCES = load("sources.json")["sources"]
FLAGS = load("flags.json")["flags"]
QUESTIONS = load("questions.json")["questions"]
SUGGESTIONS = load("suggestions.json")["suggestions"]
DECISIONS = load("decisions.json")["decisions"]
LEDGER = load("ledger.json")
EVENTS = load("events.json")
CALENDAR = load("calendar.json")
COMMISSION = load("commission.json")

BRAND = SETTINGS["brand"]["name"]
DESCRIPTOR = SETTINGS["brand"]["descriptor"]
TAGLINE = SETTINGS["brand"]["tagline"]
BASE = SETTINGS["base_url"].rstrip("/")
DISCLOSURE = SETTINGS["disclosure_sentence"]
PAID_LABEL = SETTINGS["paid_link_label"]

PROD_BY_ID = {p["id"]: p for p in PRODUCTS}

# ---------------------------------------------------------------------------
# Page registry: id -> (path, title, description, jsonld kind, nav section)
# ---------------------------------------------------------------------------
PAGES = [
    ("index", "index.html",
     f"Air fryers and thermometers by format | {BRAND}",
     "Three air fryers in three formats and two meat thermometers, compared by capacity, counter fit and cleanup. Every figure cites the official listing it came from.",
     "home"),
    ("shop", "shop.html",
     f"Shop: the five kitchen tools we follow | {BRAND}",
     "One shelf: three air fryer formats and two thermometer workflows, filtered by what you cook and how much counter you can spare. Paid links, marked.",
     "shop"),
    ("about", "about.html",
     f"About this site: who writes it, how we check | {BRAND}",
     "Who edits this site, the four rules every page follows, how figures are read and dated, and exactly what we cannot tell you yet.",
     "about"),
    ("compare", "compare.html",
     f"Compare the five products side by side | {BRAND}",
     "One sourced comparison table: format, capacity, dimensions, counter depth and listed features — plus a three-question chooser and the counter-space analysis.",
     "compare"),
    ("products", "products.html",
     f"The five products, spec by spec | {BRAND}",
     "Full listed specifications with read dates and source links, plus the product-intent confirmation record for every submitted link. Blank means unverified.",
     "products"),
    ("buying-guide", "buying-guide.html",
     f"Buying guide: format, capacity and counter fit | {BRAND}",
     "A buying guide that starts from your kitchen, not a brand: format first, then capacity, then counter depth, then cleanup — with the questions that decide each.",
     "guides"),
    ("guide-basket-vs-oven", "guide-basket-vs-oven.html",
     f"Basket or oven-style air fryer: what to compare | {BRAND}",
     "Basket-style or oven-style? Compare the right things: footprint, food shape, capacity zones, cleanup. With the listed values for each format, sourced.",
     "guides"),
    ("guide-capacity", "guide-capacity.html",
     f"A no-hype checklist for air-fryer capacity | {BRAND}",
     "Quarts, litres and basket counts don't compare themselves. A five-minute checklist for comparing air-fryer capacity honestly, with listed values.",
     "guides"),
    ("guide-cleanup-counter-space", "guide-cleanup-counter-space.html",
     f"Cleanup and counter-space trade-offs, assessed | {BRAND}",
     "What listed dimensions, materials and dishwasher-safe parts say about cleanup and counter space — and how to weigh the trade-off before buying.",
     "guides"),
    ("guide-multifunction", "guide-multifunction.html",
     f"Questions to ask before buying multi-function gear | {BRAND}",
     "Air fry, bake, dehydrate, rotisserie: which functions will you actually use? The questions that separate a worktop workhorse from a cupboard-filler.",
     "guides"),
    ("article-air-fryer-doneness", "article-air-fryer-doneness.html",
     f"Did the air fryer work? One number decides | {BRAND}",
     "Capacity, drawers and wattage do not tell you whether dinner is safe. USDA and extension guidance on the one number that does, applied to the three air fryers we track.",
     "guides"),
    ("article-thermometer-placement", "article-thermometer-placement.html",
     f"Where to put the probe: placement beats precision | {BRAND}",
     "USDA guidance on where a thermometer probe actually belongs, set against the two thermometers we follow. What the official pages say, and what they do not.",
     "guides"),
    ("guide-thermometer-accuracy", "guide-thermometer-accuracy.html",
     f"How accurate does a meat thermometer need to be? | {BRAND}",
     "±0.5°F vs ±1°F, instant-read vs leave-in wireless: what accuracy claims on the listing mean and which thermometer fits which cook.",
     "guides"),
    ("guide-how-many-quarts", "guide-how-many-quarts.html",
     f"How many quarts do you actually need? | {BRAND}",
     "Quarts on a listing describe volume, not people. A serving-count sanity check built from the listed capacities of the three air fryers, each sourced.",
     "guides"),
    ("guide-two-baskets-or-one", "guide-two-baskets-or-one.html",
     f"Two baskets or one: when two drawers earn it | {BRAND}",
     "Dual-zone or one big basket? The batch math and the listed specs that decide it: sync finish, shake reminders, and who cooks two dishes at once.",
     "guides"),
    ("guide-holiday-hosting", "guide-holiday-hosting.html",
     f"Holiday hosting: which format earns the counter? | {BRAND}",
     "Big meals, borrowed counter space, eat-in waves. Which air-fryer format and which thermometer workflow fit holiday hosting, from listed specs only.",
     "guides"),
    ("guide-instant-vs-leave-in", "guide-instant-vs-leave-in.html",
     f"Instant-read vs leave-in: which one fits you | {BRAND}",
     "Spot-check in a second, or watch a long cook from your phone? How an instant-read and a wireless leave-in thermometer differ by workflow, with listed specs.",
     "guides"),
    ("guide-gift-guide", "guide-gift-guide.html",
     f"Gift guide: which of the five fits which cook? | {BRAND}",
     "Match each of the five machines to the cook who would actually use it: weeknight juggling, from-scratch roasting, small kitchens, grill-side checks, long smokes.",
     "guides"),
    ("guide-preheat-shake", "guide-preheat-shake.html",
     f"Preheat, shake, or don’t: which rituals matter | {BRAND}",
     "Which air-fryer steps are worth learning, from the listings we track and extension guidance: preheat, the mid-cook shake, the no-overfill rule, the probe.",
     "guides"),
    ("guides", "guides.html",
     f"Guides: one buyer question per page | {BRAND}",
     "Every buying guide on this site, grouped by cluster and season, each answering a single question with sourced figures. A new guide every two weeks.",
     "guides"),
    ("category-air-fryers", "category-air-fryers.html",
     f"Air fryers: the three formats compared | {BRAND}",
     "Three air-fryer formats compared by the decision that matters — how they fit your counter and your cooking. Listed specs only, each with its source.",
     "categories"),
    ("category-thermometers", "category-thermometers.html",
     f"Meat thermometers: instant-read vs leave-in | {BRAND}",
     "Two thermometers compared: a one-second instant-read with certified accuracy claims, and a wireless leave-in probe set. Listed specs only, sourced.",
     "categories"),
    ("executive-summary", "executive-summary.html",
     f"Executive summary | {BRAND}",
     "What this project is, what is verified, what is missing, and what decisions are open — the reviewer's one-page overview.",
     "work"),
    ("method", "method.html",
     f"Method and source register | {BRAND}",
     "How every figure on this site is checked against official sources, with the full source register and read dates.",
     "work"),
    ("flagged", "flagged.html",
     f"Flagged for review | {BRAND}",
     "Open, resolved and standing items with evidence links: the irregularities and unverified values a reviewer should see.",
     "work"),
    ("before-you-decide", "before-you-decide.html",
     f"Before you decide anything: the eleven open calls | {BRAND}",
     "Eleven decisions waiting on facts only the owner can obtain: what is known, what is missing, how it gets found, and what changes when it lands.",
     "work"),
    ("questions", "questions.html",
     f"Open questions and missing information | {BRAND}",
     "What we know, what we don't, and how to find out — the register that must be answered before certain decisions can be made.",
     "work"),
    ("suggestions", "suggestions.html",
     f"Suggestion queue: choose the path before we build | {BRAND}",
     "Proposed improvements with evidence, impact, effort and risk. Nothing here is implemented until a reviewer picks a path.",
     "work"),
    ("decisions", "decisions.html",
     f"Decision log | {BRAND}",
     "Every recorded decision, its question, its outcome and its sources — carried decisions keep their original dates.",
     "work"),
    ("measurement", "measurement.html",
     f"Measurement: events, clicks, campaign ledger | {BRAND}",
     "The privacy-preserving click counter, the five defined events with attribution windows, the analytics endpoint, and the empty campaign ledger.",
     "work"),
    ("compliance", "compliance.html",
     f"Compliance gate: disclosures and link policy | {BRAND}",
     "How the Associates disclosure, sponsored-link marking and FTC endorsement guidance are enforced in the publishing workflow.",
     "work"),
    ("privacy", "privacy.html",
     f"Privacy | {BRAND}",
     "What this site collects (almost nothing), what the click counter does, and what the self-hosted analytics endpoint stores.",
     "work"),
]

GUIDE_IDS = ["guide-basket-vs-oven", "guide-capacity", "guide-cleanup-counter-space",
             "guide-multifunction", "guide-thermometer-accuracy", "guide-how-many-quarts",
             "guide-two-baskets-or-one", "guide-holiday-hosting", "guide-instant-vs-leave-in",
             "guide-gift-guide", "guide-preheat-shake"]
GUIDE_TITLES = {g: dict((p[0], p[2]) for p in PAGES)[g] for g in GUIDE_IDS}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def esc(s) -> str:
    return html.escape(str(s), quote=True)


def amazon_link(url: str, label: str, extra_class: str = "") -> str:
    cls = ("aff-link " + extra_class).strip()
    return (f'<a class="{cls}" href="{esc(url)}" rel="sponsored nofollow noopener" '
            f'target="_blank" data-affiliate="1">{esc(label)}</a>')


def src_link(sid: str) -> str:
    for s in SOURCES:
        if s["id"] == sid:
            return (f'<a class="src" href="{esc(s["url"])}" rel="noopener" target="_blank" '
                    f'title="{esc(s["title"])}">{esc(sid)}</a>')
    return f'<span class="src-missing">{esc(sid)} (missing)</span>'


def listing_link(p: dict, label: str = "listing") -> str:
    return (f'<a class="src" href="https://www.amazon.com/dp/{esc(p["asin"])}" '
            f'rel="noopener" target="_blank">{esc(label)}</a>')


def buy_link(p: dict, text: str | None = None, cls: str = "btn btn-buy") -> str:
    label = text or f"See the {p['name_short']} on Amazon"
    return amazon_link(p["buy_url"], label, cls) + f' <span class="paid">{esc(PAID_LABEL)}</span>'


# ---------------------------------------------------------------------------
# Layout chrome
# ---------------------------------------------------------------------------
# Reader navigation: what a shopper needs. Six links, one group.
# D-06 (2026-11-20): the previous nav carried eleven links, five of which were
# dashboard surfaces. Those move to the footer's "The work behind it" directory,
# which the gate still requires on every page.
NAV_READER = [
    ("shop.html", "Shop"),
    ("category-air-fryers.html", "Air fryers"),
    ("category-thermometers.html", "Thermometers"),
    ("guides.html", "Guides"),
    ("compare.html", "Compare"),
    ("about.html", "About"),
]
# Everything an owner, reviewer or search engine needs, reachable from every page.
NAV_WORK = [
    ("before-you-decide.html", "Before you decide"),
    ("about.html", "About &amp; standards"),
    ("executive-summary.html", "Executive summary"),
    ("method.html", "Method &amp; sources"),
    ("flagged.html", "Flagged for review"),
    ("questions.html", "Open questions"),
    ("suggestions.html", "Suggestions"),
    ("decisions.html", "Decisions"),
    ("measurement.html", "Measurement"),
    ("compliance.html", "Compliance"),
    ("privacy.html", "Privacy"),
]
GUIDE_LINKS = [
    ("guide-basket-vs-oven.html", "Basket or oven-style air fryer?"),
    ("guide-capacity.html", "The capacity checklist"),
    ("guide-cleanup-counter-space.html", "Cleanup &amp; counter space"),
    ("guide-multifunction.html", "Before buying multi-function"),
    ("guide-thermometer-accuracy.html", "Thermometer accuracy"),
    ("guide-how-many-quarts.html", "How many quarts do you need?"),
    ("guide-two-baskets-or-one.html", "Two baskets or one?"),
    ("guide-holiday-hosting.html", "Holiday hosting formats"),
    ("guide-instant-vs-leave-in.html", "Instant-read vs leave-in"),
    ("guide-gift-guide.html", "The gift guide"),
    ("guides.html", "All guides"),
]


def build_nav(current: str) -> str:
    links = []
    for href, label in NAV_READER:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    work_items = ""
    for href, label in NAV_WORK:
        cur = ' aria-current="page"' if href == current else ""
        work_items += f'<a href="{href}"{cur}>{label}</a>'
    work_cur = " current" if current in [h for h, _ in NAV_WORK] else ""
    return (
        '<nav class="nav" aria-label="Site">'
        + "".join(links)
        + f'<details class="nav-work{work_cur}"><summary>The work behind it</summary>'
        f'<div class="nav-work-menu">{work_items}</div></details>'
        + '</nav>'
    )


def build_footer() -> str:
    def lis(items):
        return "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in items)
    guides = lis(GUIDE_LINKS)
    shop = lis([("shop.html", "Shop the shelf"), ("compare.html", "Compare the five"),
                ("products.html", "Products &amp; specs"), ("category-air-fryers.html", "Air fryers"),
                ("category-thermometers.html", "Thermometers"), ("buying-guide.html", "Buying guide")])
    read = lis([("guides.html", "All guides"), ("buying-guide.html", "Buying guide"),
                ("guides.html#subscribe", "Follow the feed"), ("guides.html#ask", "Ask a question"),
                ("about.html", "Who writes this")])
    work = lis(NAV_WORK)
    return f"""
<footer class="footer">
  <div class="wrap footer-grid">
    <div>
      <p class="footer-brand">{esc(BRAND)} <span>· {esc(DESCRIPTOR)}</span></p>
      <p class="footer-disclosure">{esc(DISCLOSURE)} Product links on this site are paid links. <a href="compliance.html">How we handle disclosures</a>.</p>
    </div>
    <div><h2>Guides</h2><ul>{guides}</ul></div>
    <div><h2>Compare &amp; shop</h2><ul>{shop}</ul></div>
    <div><h2>Read &amp; follow</h2><ul>{read}</ul></div>
    <div><h2>The work behind it</h2><ul>{work}</ul></div>
  </div>
  <p class="wrap footer-legal">Published {esc(BUILD_DATE)}. Prices and star ratings are not published — see <a href="flagged.html#F-02">F-02</a>.
  Product links are Amazon Associates Special Links. Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.</p>
</footer>"""


DISCLOSURE_STRIP = (f'<div class="disclosure" role="note">'
                    f'<span class="disclosure-check" aria-hidden="true">✓</span> '
                    f'<strong>{esc(DISCLOSURE)}</strong> '
                    f'<span class="disclosure-more">Product links on this site are paid links, marked {esc(PAID_LABEL)}; '
                    f'we may earn a commission on qualifying purchases. <a href="compliance.html">Details</a></span>'
                    f'</div>')

# ---------------------------------------------------------------------------
# Data-rendering hooks
# ---------------------------------------------------------------------------
def spec_rows(p: dict) -> str:
    """Fact rows for a product register table: fact | value | read | source."""
    rows = []

    def row(fact, value, read, sid, flag=None):
        if value in (None, ""):
            flag_html = f'<a href="flagged.html#{flag}">{flag}</a>' if flag else ''
            rows.append(f'<tr><td>{esc(fact)}</td><td class="unverified">— unverified</td>'
                        f'<td></td><td>{flag_html}</td></tr>')
        else:
            rows.append(f'<tr><td>{esc(fact)}</td><td>{esc(value)}</td>'
                        f'<td>{esc(read or "")}</td><td>{src_link(sid)}</td></tr>')

    sid = f'S-{p["id"]}'
    row("Listing title", p["name_listing"], p.get("name_listing_read"), sid)
    row("Brand", p.get("brand"), p.get("brand_read"), sid)
    row("Manufacturer", p.get("manufacturer"), p.get("item_details_read"), sid)
    row("Model name", p.get("model_name"), p.get("item_details_read"), sid)
    row("Model number", p.get("model_number"), p.get("item_details_read"), sid)
    row("Category path", p.get("category_path"), p.get("category_read"), sid)
    row("Capacity", p.get("capacity"), p.get("capacity_read"), sid)
    row("Dimensions (D×W×H)", p.get("dimensions"), p.get("dimensions_read"), sid)
    row("Color", p.get("color"), p.get("spec_table_read"), sid)
    row("Material", p.get("material"), p.get("spec_table_read"), sid)
    row("Listed special features", p.get("special_feature"), p.get("spec_table_read"), sid)
    row("Function count", p.get("function_count"), p.get("name_listing_read"), sid,
        "F-26" if "function_count" in p else None)
    row("Commission rate", None, None, "S-COMM", "F-01")
    row("Price", None, None, sid, "F-02")
    row("Star rating", None, None, sid, "F-02")
    return "".join(rows)


def hook_products_table(_="") -> str:
    head = ("<thead><tr><th>Product</th><th>Format</th><th>Capacity</th>"
            "<th>Dimensions (D×W×H)</th><th>Counter depth</th><th>Capacity / depth</th>"
            "<th>Why it exists</th><th>Source</th><th></th></tr></thead>")
    rows = []
    for p in PRODUCTS:
        depth = None
        m = re.match(r'([\d.]+)"D', p.get("dimensions") or "")
        if m:
            depth = float(m.group(1))
        cap_qt = {"P1": 6.0, "P2": 26.0, "P3": 8.0}.get(p["id"])
        ratio = f"{cap_qt / depth:.2f} qt/in" if (cap_qt and depth) else '<span class="unverified">—</span>'
        why = {"P1": "Two dishes at once, synced", "P2": "Rack cooking, sheet-pan meals",
               "P3": "Big single basket, small footprint", "P4": "Fast doneness checks",
               "P5": "Cook away from the heat"}[p["id"]]
        rows.append(
            f'<tr id="row-{p["id"]}"><td><strong>{esc(p["name_short"])}</strong><br>'
            f'<span class="muted">{esc(p["asin"])}</span></td>'
            f'<td>{esc(p["format"])}</td><td>{esc(p["capacity"] or "—")}</td>'
            f'<td>{esc(p["dimensions"] or "—")}</td><td>{esc(str(depth) + chr(34) if depth else "—")}</td>'
            f'<td>{ratio}</td><td>{esc(why)}</td><td>{listing_link(p)}</td>'
            f'<td>{buy_link(p, "See price")}</td></tr>')
    return (f'<div class="table-scroll"><table class="data products-table">{head}'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="table-note">Capacity / depth = listed qt capacity ÷ listed counter depth (inches), '
            f'shown as the formula, computed only where both figures are listed (P4/P5 are thermometers — no capacity). '
            f'No prices or ratings are published (<a href="flagged.html#F-02">F-02</a>). '
            f'Every row links to the official listing it was read from.</p>')


def hook_air_fryer_table(_="") -> str:
    rows = []
    for p in PRODUCTS[:3]:
        rows.append(f'<tr><td><strong>{esc(p["name_short"])}</strong></td><td>{esc(p["format"])}</td>'
                    f'<td>{esc(p["capacity"])}</td><td>{esc(p["dimensions"])}</td>'
                    f'<td>{esc(p["special_feature"])}</td><td>{listing_link(p)}</td>'
                    f'<td>{buy_link(p, "See price")}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Product</th><th>Format</th>'
            '<th>Capacity</th><th>Dimensions (D×W×H)</th><th>Listed special features</th>'
            '<th>Source</th><th></th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>')


def hook_thermo_table(_="") -> str:
    rows = []
    for p in PRODUCTS[3:]:
        rows.append(f'<tr><td><strong>{esc(p["name_short"])}</strong></td><td>{esc(p["format"])}</td>'
                    f'<td>{esc(p["special_feature"])}</td><td>{listing_link(p)}</td>'
                    f'<td>{buy_link(p, "See price")}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Product</th><th>Format</th>'
            '<th>Listed features</th><th>Source</th><th></th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>')


def hook_counter_space(_="") -> str:
    rows = []
    for p in PRODUCTS[:3]:
        depth = float(re.match(r'([\d.]+)"D', p["dimensions"]).group(1))
        width = float(re.search(r'x ([\d.]+)"W', p["dimensions"]).group(1))
        cap_qt = {"P1": 6.0, "P2": 26.0, "P3": 8.0}[p["id"]]
        footprint = depth * width
        rows.append(f'<tr><td>{esc(p["name_short"])}</td><td>{esc(p["capacity"])}</td>'
                    f'<td>{depth}"</td><td>{width}"</td><td>{footprint:.0f} in²</td>'
                    f'<td><strong>{cap_qt / footprint:.3f}</strong> qt / in²</td>'
                    f'<td>{listing_link(p)}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Product</th><th>Listed capacity</th>'
            '<th>Counter depth</th><th>Width</th><th>Footprint (D×W)</th><th>Capacity per in²</th>'
            '<th>Source</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'
            '<p class="table-note">Capacity per in² = listed qt ÷ (listed depth × listed width). '
            'A derived value, not a manufacturer figure — the formula is the point (decision D-26). '
            'It answers: how much cooking space do I get per square inch of counter surrendered?</p>')


def hook_chooser(_="") -> str:
    return """
<div class="chooser" id="chooser">
  <h2>Which one is for you? Three questions.</h2>
  <p class="muted">Built only from the published listed values (decision D-23). It routes to a format, not to a checkout.</p>
  <fieldset>
    <legend>1. How many people do you usually cook for?</legend>
    <label><input type="radio" name="q1" value="s"> One or two</label>
    <label><input type="radio" name="q1" value="m"> Three or four</label>
    <label><input type="radio" name="q1" value="l"> Five or more</label>
  </fieldset>
  <fieldset>
    <legend>2. How much counter depth can you spare?</legend>
    <label><input type="radio" name="q2" value="shallow"> Under about 13 inches</label>
    <label><input type="radio" name="q2" value="medium"> 13 to 16 inches</label>
    <label><input type="radio" name="q2" value="deep"> More than 16 inches</label>
  </fieldset>
  <fieldset>
    <legend>3. Do you cook two different dishes at the same time?</legend>
    <label><input type="radio" name="q3" value="yes"> Most meals</label>
    <label><input type="radio" name="q3" value="sometimes"> Sometimes</label>
    <label><input type="radio" name="q3" value="no"> Rarely</label>
  </fieldset>
  <button type="button" class="btn" id="chooser-run">Show my answer</button>
  <div id="chooser-out" class="chooser-out" aria-live="polite"></div>
</div>"""


def hook_intent_table(_="") -> str:
    rows = []
    for l in INTENTS:
        p = PROD_BY_ID[l["product_id"]]
        obs = l["observed_redirect"]
        rows.append(
            f'<tr><td>{esc(l["product_id"])} — {esc(p["name_short"])}</td>'
            f'<td><code>{esc(l["submitted_url"])}</code></td>'
            f'<td><code>{esc(l["link_path_code"])}</code></td>'
            f'<td><code>{esc(l["intended_asin"])}</code><br><span class="muted">{esc(l["intent_basis"][:110])}…</span></td>'
            f'<td><code>{esc(l["official_listing_url"])}</code><br>'
            f'<a class="src" href="{esc(l["official_listing_url"])}" rel="noopener" target="_blank">open</a></td>'
            f'<td>{esc(l["confirmation_date_utc"])}</td>'
            f'<td><code>{esc(obs["final_url_without_query"])}</code> <span class="muted">(observed {esc(obs["date_utc"])})</span></td>'
            f'<td>{esc("yes" if l["intent_match"] else "no")}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr>'
            '<th>Product</th><th>Submitted link (verbatim)</th><th>Path code<br><span class="muted">not an ASIN</span></th>'
            '<th>Intended ASIN + basis</th><th>Official listing URL</th><th>Confirmed</th>'
            '<th>Observed redirect (kept separate)</th><th>Match</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>'
            '<p class="table-note">Intent fields and observed-redirect fields are never merged. '
            'The short links are recorded verbatim and are not judged valid or invalid '
            '(<a href="https://github.com/kanlerxz87-cyber/Zone3">FLG-003 unresolved</a>). '
            'Full dated redirect history: <a href="https://github.com/wingbangboozle1-lang/Prod2/blob/main/data/intent-links.json">data/intent-links.json</a>.</p>')


def _source_url_cell(url: str) -> str:
    """Render a source URL. A link.amazon short link is owner-supplied evidence,
    never a clickable destination (F-03/FLG-003, unresolved): show it as inert code."""
    if url.startswith("https://link.amazon"):
        return f'<code>{esc(url)}</code>'
    return (f'<a class="src" href="{esc(url)}" rel="noopener" target="_blank">'
            f'{esc(url)[:64]}</a>')


def hook_trust_row(_="") -> str:
    """The front-page trust row. Every number is derived from the registers at
    build time, so it cannot drift when a guide is added (the counts were
    hardcoded and went stale twice before this hook existed)."""
    formats = {p["format"] for p in PRODUCTS if "thermometer" not in p["format"].lower()}
    reads = len([p for p in PAGES if p[0].startswith("article-")])
    pieces = len(GUIDE_IDS) + reads
    cells = [
        (len(PRODUCTS), "tools followed"),
        (len(formats), "air fryer formats"),
        (pieces, "buyer guides &amp; reads"),
        (0, "made-up specs"),
    ]
    return ('<div class="trust-row">'
            + "".join(f'<div><b>{n}</b><span>{label}</span></div>' for n, label in cells)
            + '</div>')


def hook_sources_table(_="") -> str:
    rows = []
    for s in SOURCES:
        reads = ", ".join(s.get("read", []))
        rows.append(f'<tr id="{esc(s["id"])}"><td><code>{esc(s["id"])}</code></td><td>{esc(s["title"])}</td>'
                    f'<td>{_source_url_cell(s["url"])}</td>'
                    f'<td>{esc(s["kind"])}</td><td>{esc(reads)}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>ID</th><th>Source</th>'
            '<th>Official URL</th><th>Kind</th><th>Read (UTC)</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>')


def hook_commission_table(_="") -> str:
    """Commission potential, from Amazon's own Standard Commission Income
    Statement only. A rate, never a forecast: no order count, no click count,
    no revenue estimate, and no claim that any commission was earned."""
    tbl = COMMISSION["rate_table"]
    rows = []
    for c in COMMISSION["products"]:
        p = PROD_BY_ID[c["product_id"]]
        actual = c.get("actual_rate_percent")
        actual_cell = (f'{actual}%' if actual is not None
                       else '<span class="muted">— unverified</span>')
        rows.append(
            f'<tr id="comm-{esc(c["product_id"])}"><td><strong>{esc(c["product_id"])}</strong></td>'
            f'<td><code>{esc(c["asin"])}</code></td>'
            f'<td>{esc(p["name_short"])}</td>'
            f'<td>{esc(c["listing_department_path"])}<br>'
            f'<span class="muted">{src_link(c["listing_department_source"])}, read {esc(c["listing_department_read"])}</span></td>'
            f'<td>{esc(c["commission_category"])}</td>'
            f'<td>{c["standard_rate_percent"]:.2f}%</td>'
            f'<td>{actual_cell}</td>'
            f'<td>{src_link(c["rate_source"])}</td></tr>')
    head = ('<div class="table-scroll"><table class="data"><thead><tr><th>ID</th><th>ASIN</th>'
            '<th>Product</th><th>Listing department (read from the listing)</th>'
            '<th>Commission category</th><th>Standard rate</th>'
            '<th>This account\'s rate</th><th>Rate source</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>')
    rows_tbl = []
    for r in tbl["rows_used"]:
        rows_tbl.append(
            f'<tr><td>{esc(r["category"])}</td><td><strong>{r["rate_percent"]:.2f}%</strong></td>'
            f'<td><code>{esc(r["row_text"])}</code></td>'
            f'<td>{esc(r["why_it_could_apply"])}</td></tr>')
    rate_tbl = ('<div class="table-scroll"><table class="data"><thead><tr><th>Category</th>'
                '<th>Standard rate</th><th>Row as published</th><th>Why it is or is not a candidate here</th>'
                '</tr></thead><tbody>' + "".join(rows_tbl) + '</tbody></table></div>')
    meta = COMMISSION["_meta"]
    return (
        f'<p class="callout"><strong>What this table is.</strong> {esc(meta["what_this_is"])} '
        f'Rate source: {src_link(tbl["source_id"])} — {esc(tbl["source_title"])}, read {esc(tbl["read_utc"])}. '
        f'Nothing here is a revenue figure.</p>'
        + head
        + '<h3>The rows this site read, and why</h3>' + rate_tbl
        + '<div class="callout"><h3>What we could not verify</h3><ul>'
        + "".join(f'<li>{esc(x)}</li>' for x in meta["not_verified"])
        + f'</ul><p>{esc(COMMISSION["catalogue_summary"]["owner_action"])}</p></div>'
    )


def _flag_row(f: dict) -> str:
    # A resolved flag must SHOW its resolution on the page, not only in the JSON.
    # Fixed 2026-11-20: F-P23 read as open on the Flagged page while the register
    # said resolved, because only the how_to_resolve cell was rendered.
    resolution = f.get("resolution")
    tail = (f'<strong>Resolved {esc(f.get("resolved_utc", ""))}.</strong> {esc(resolution)}'
            if resolution else esc(f["how_to_resolve"]))
    return (f'<tr id="{esc(f["id"])}"><td><code>{esc(f["id"])}</code></td><td>{esc(f["title"])}</td>'
            f'<td>{esc(f["detail"])}</td>'
            f'<td><a class="src" href="{esc(f["evidence"])}" rel="noopener" target="_blank">evidence</a><br>'
            f'<span class="muted">{esc(f["evidence_note"])}</span></td>'
            f'<td>{tail}</td></tr>')


def hook_flags(status: str) -> str:
    rows = [_flag_row(f) for f in FLAGS if f["status"] == status]
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>ID</th><th>Item</th>'
            '<th>What and why</th><th>Evidence</th><th>How it resolves</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>')


def hook_questions(_="") -> str:
    out = []
    for q in QUESTIONS:
        flags = " ".join(f'<a href="flagged.html#{esc(x)}">{esc(x)}</a>' for x in q.get("flags", []))
        blocks = esc(", ".join(q.get("blocks", [])) or "—")
        out.append(f"""
<article class="card q-card" id="{esc(q['id'])}">
  <h3><code>{esc(q['id'])}</code> {esc(q['question'])}</h3>
  <dl>
    <dt>What we know</dt><dd>{esc(q['known'])}</dd>
    <dt>What is missing</dt><dd>{esc(q['unknown'])}</dd>
    <dt>How to discover it</dt><dd>{esc(q['how_to_discover'])}</dd>
    <dt>Answerable by</dt><dd>{esc(q['answerable_by'])}</dd>
    <dt>Blocks</dt><dd>{blocks}</dd>
    <dt>Flags</dt><dd>{flags or '—'}</dd>
  </dl>
</article>""")
    return "".join(out)


def hook_suggestions(_="") -> str:
    out = []
    for s in SUGGESTIONS:
        deps = esc(", ".join(s.get("depends_on", [])) or "—")
        progress = s.get("progress")
        progress_html = (f"<dt>Progress</dt><dd>{esc(progress)}</dd>" if progress else "")
        out.append(f"""
<article class="card s-card" id="{esc(s['id'])}">
  <header><h3><code>{esc(s['id'])}</code> {esc(s['title'])}</h3>
  <span class="status status-{esc(s['status'])}">{esc(s['status'])}</span></header>
  <dl>
    <dt>Problem</dt><dd>{esc(s['problem'])}</dd>
    <dt>Proposal</dt><dd>{esc(s['proposal'])}</dd>
    <dt>Evidence</dt><dd>{esc(s['evidence'])}</dd>
    <dt>Expected impact</dt><dd>{esc(s['impact'])}</dd>
    <dt>Effort</dt><dd>{esc(s['effort'])}</dd>
    <dt>Risk</dt><dd>{esc(s['risk'])}</dd>
    {progress_html}
    <dt>Depends on</dt><dd>{deps}</dd>
  </dl>
  <p class="reco"><strong>Our recommendation:</strong> {esc(s['recommendation'])}</p>
</article>""")
    return "".join(out)


def hook_decisions(_="") -> str:
    out = []
    for d in DECISIONS:
        srcs = "".join(f'<a class="src" href="{esc(u)}" rel="noopener" target="_blank">source</a> ' for u in d.get("sources", []))
        out.append(f"""
<article class="card d-card" id="{esc(d['id'])}">
  <h3><code>{esc(d['id'])}</code> {esc(d['question'])}</h3>
  <p class="status status-recorded">{esc(d['status'])}</p>
  <p>{esc(d['recorded_choice'])}</p>
  <p>{srcs}</p>
</article>""")
    return "".join(out)


def hook_ledger_events(_="") -> str:
    rows = "".join(f'<tr><td><strong>{esc(e["event"])}</strong></td><td>{esc(e["definition"])}</td>'
                   f'<td>{esc(e["window"])}</td></tr>' for e in LEDGER["five_events"])
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Event</th><th>Definition</th>'
            '<th>Attribution window (official)</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
            f'<p class="table-note">Windows as stated in the Commission Income Statement ({src_link("S-COMM")}). '
            'This ledger starts empty and is filled only from authorized first-party reports.</p>')


def hook_ledger_table(_="") -> str:
    head = "".join(f'<th>{esc(c)}</th>' for c in LEDGER["columns"])
    return (f'<div class="table-scroll"><table class="data"><thead><tr>{head}</tr></thead>'
            f'<tbody></tbody></table></div>'
            f'<p class="table-note"><strong>{esc(LEDGER["status"])}</strong> '
            'A row is added only from an authorized first-party report (for example an Associates Central export). '
            'No row is estimated, and the site\'s own click counter is never a reported order.</p>')


def hook_local_events(_="") -> str:
    rows = "".join(f'<tr><td><code>{esc(e["name"])}</code></td><td>{esc(e["definition"])}</td>'
                   f'<td><code>{esc(e["fields"])}</code></td></tr>' for e in EVENTS["events"])
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Event</th><th>Definition</th>'
            '<th>Fields</th></tr></thead><tbody>' + rows + '</tbody></table></div>')


# Product imagery: drawn, ours, and deliberately generic. No Amazon product
# photography is copied onto this site; each card is a format illustration so a
# reader sees the shape of the appliance, not a brand's asset (see about.html).
PRODUCT_IMAGES = {
    "P1": ("assets/img/fmt-dual-basket.png", "Two-basket air fryer, drawn from the format"),
    "P2": ("assets/img/fmt-toaster-oven.png", "French-door air fryer toaster oven, drawn from the format"),
    "P3": ("assets/img/fmt-single-basket.png", "Single-basket air fryer, drawn from the format"),
    "P4": ("assets/img/fmt-instant-read.png", "Folding instant-read thermometer, drawn from the format"),
    "P5": ("assets/img/fmt-wireless-probe.png", "Wireless leave-in probe and hub, drawn from the format"),
}
# Plain-English positioning. Every claim here restates a listed feature that is
# already published on the card; these are the "who is this for" line, not a ranking.
PRODUCT_BEST_FOR = {
    "P1": "Two dishes, one finish time",
    "P2": "Sheet-pan meals and rack cooking",
    "P3": "One big basket, the least counter",
    "P4": "A one-second spot check",
    "P5": "Long cooks, watched from away",
}
PRODUCT_BUY_LABEL = {
    "P1": "Check price on Amazon",
    "P2": "Check price on Amazon",
    "P3": "Check price on Amazon",
    "P4": "Check price on Amazon",
    "P5": "Check price on Amazon",
}


def hook_product_cards(_="") -> str:
    cards = []
    for p in PRODUCTS:
        src, alt = PRODUCT_IMAGES[p["id"]]
        cards.append(f"""
<article class="card product-card" id="{esc(p['id'])}">
  <a class="thumb" href="{esc(p['buy_url'])}" rel="sponsored nofollow noopener" target="_blank"
     data-affiliate="1" tabindex="-1" aria-hidden="true">
    <img src="{esc(BASE)}/{src}" alt="" loading="lazy" width="1200" height="900">
    <span class="rank">{esc(p['format'])}</span>
  </a>
  <div class="body">
    <p class="eyebrow">Best for: {esc(PRODUCT_BEST_FOR[p['id']])}</p>
    <h3><a href="products.html#{esc(p['id'])}" style="color:inherit;text-decoration:none">{esc(p['name_short'])}</a></h3>
    <p class="muted asin">{esc(p['asin'])}</p>
    <ul>
      <li>{esc(p.get('highlight_1') or '')}</li>
      <li>{esc(p.get('highlight_2') or '')}</li>
      <li>{esc(p.get('highlight_3') or '')}</li>
    </ul>
    <p class="buy-row">{buy_link(p, PRODUCT_BUY_LABEL[p['id']])}</p>
    <p class="source-line">Listed facts sourced to {listing_link(p, 'the official listing')}; listing re-checked {esc(p.get('last_live_read') or p.get('name_listing_read') or '')}. Illustration, not the product photo.</p>
  </div>
</article>""")
    return '<div class="shelf">' + "".join(cards) + '</div>'


def hook_facts(pid: str) -> str:
    p = PROD_BY_ID[pid]
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Fact</th><th>Value as listed</th>'
            '<th>Read (UTC)</th><th>Source</th></tr></thead><tbody>' + spec_rows(p) + '</tbody></table></div>')


def hook_guide_links(_="") -> str:
    items = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in GUIDE_LINKS)
    return f'<ul class="guide-links">{items}</ul>'


def hook_comparison_cta(_="") -> str:
    # Fixed 2026-11-20: this used to be a paid Amazon link labelled "Compare all
    # five", which pointed at P1's listing. A comparison call to action must lead
    # to the comparison, not to one product (misleading-label risk under
    # Program Policies §2(b)).
    return ('<p class="cta-row"><a class="btn" href="compare.html">Compare all five side by side</a>'
            ' <a class="btn btn-ghost" href="buying-guide.html">Read the buying guide</a></p>')


GUIDE_BLURBS = {
    "guide-basket-vs-oven": "The format decision, decoded: food shape, preheat patience, cleanup.",
    "guide-capacity": "Quarts lie when you compare across formats. Make them mean the same thing.",
    "guide-cleanup-counter-space": "What listed dimensions and dishwasher-safe parts tell you before it arrives.",
    "guide-multifunction": "Twenty-four presets, twenty-four reasons to buy? The questions that count them down.",
    "guide-thermometer-accuracy": "±0.5°F versus ±1°F, check-it versus watch-it: what the claims really say.",
    "guide-how-many-quarts": "A serving-count sanity check from the listed capacities, not the marketing.",
    "guide-two-baskets-or-one": "Batch math meets listed specs: when two drawers beat one big basket.",
    "guide-holiday-hosting": "Big meals, borrowed counter space, eat-in waves: the format that holds up.",
    "guide-instant-vs-leave-in": "Check at the counter in a second, or watch a long roast from your phone.",
    "guide-gift-guide": "Five machines, five kinds of cooks: match the gift to the person, from listed specs.",
    "guide-preheat-shake": "Which air-fryer steps are worth learning, and which the machine does for you.",
}
GUIDE_TAGS = {
    "guide-basket-vs-oven": "Format",
    "guide-capacity": "Capacity",
    "guide-cleanup-counter-space": "Counter space",
    "guide-multifunction": "Multi-function",
    "guide-thermometer-accuracy": "Thermometers",
    "guide-how-many-quarts": "Capacity",
    "guide-two-baskets-or-one": "Format",
    "guide-holiday-hosting": "Seasonal",
    "guide-instant-vs-leave-in": "Thermometers",
    "guide-gift-guide": "Seasonal",
    "guide-preheat-shake": "Using it",
}


def _guide_card(gid: str) -> str:
    title = GUIDE_TITLES[gid].split(" | ")[0]
    return f"""
  <article class="card guide-card">
    <span class="tag">{esc(GUIDE_TAGS.get(gid, "Guide"))}</span>
    <h3><a href="{gid}.html">{esc(title)}</a></h3>
    <p>{esc(GUIDE_BLURBS.get(gid, ""))}</p>
    <a class="more" href="{gid}.html">Read the guide</a>
  </article>"""


def hook_guide_cards(_="") -> str:
    return '<div class="card-grid">' + "".join(_guide_card(g) for g in GUIDE_IDS) + "</div>"


def hook_subscribe(_="") -> str:
    return f"""
<div class="card subscribe-card" id="subscribe">
  <h3>Follow the feed</h3>
  <p>Every new guide lands in <a href="feed.xml" data-feed="1">the RSS feed</a> the day it publishes. It is the reader channel on this site that collects nothing at all: no sign-up, no address, no tracking.</p>
  <p class="muted">Feed address: <code>{esc(BASE)}/feed.xml</code> — paste it into any feed reader.</p>
</div>"""


def hook_reader_capture(_="") -> str:
    consent = esc(SETTINGS.get("reader_capture", {}).get("consent_checkbox_text",
                                                          "Use my question only to answer it on the site."))
    endpoint = SETTINGS.get("reader_capture", {}).get("endpoint", "") or ""
    state = "live" if endpoint else "disconnected"
    return f"""
<div class="card capture-card" id="ask">
  <h3>What should we answer next?</h3>
  <p>Every guide here starts from a real buyer question. Ask yours in one line — if it fits the five products we follow, it enters the <a href="guides.html">guide queue</a>.</p>
  <form class="capture-form" data-capture="{esc(state)}" data-capture-endpoint="{esc(endpoint)}">
    <label for="capture-question">Your question</label>
    <textarea id="capture-question" name="question" rows="3" required
      placeholder="e.g. Can two baskets really finish dinner at the same time?"></textarea>
    <label for="capture-email">Email <span class="muted">(optional — only to tell you when the answer publishes)</span></label>
    <input id="capture-email" name="email" type="email" autocomplete="email">
    <label class="capture-consent"><input type="checkbox" name="consent" required> {consent}</label>
    <button type="submit" class="btn">Send the question</button>
    <p class="capture-note" data-capture-note hidden></p>
    <p class="muted small-note">This form is currently <strong>disconnected on purpose</strong>: nothing is sent anywhere until the privacy basis for holding an email is settled (<a href="questions.html#Q-47">Q-47</a>) and an endpoint is configured (<a href="flagged.html#F-P14">F-P14</a>). Until then your question stays in your own browser.</p>
  </form>
</div>"""


def hook_byline(_="") -> str:
    return f"""
<div class="byline-strip" id="byline">
  <div>
    <h3>Who writes this</h3>
    <p>{esc(BRAND)} is an edited buying guide, not a store and not a lab. Every figure was read from an official listing or an official policy page on a dated pass, and the citation sits next to it. Nobody here has cooked with these machines (<a href="decisions.html#D-06">D-06</a>), so nothing pretends otherwise. <a href="about.html">Read the four rules every page follows</a>, or go straight to the <a href="method.html">receipts</a>.</p>
  </div>
  <p class="byline-meta">Published {esc(BUILD_DATE)} · <a href="feed.xml" data-feed="1">RSS</a> · <a href="https://github.com/wingbangboozle1-lang/Prod2" rel="noopener" target="_blank">Source register on GitHub</a></p>
</div>"""


def hook_season_desk(_="") -> str:
    blocks = []
    for s in CALENDAR["seasons"]:
        links = "".join(
            f'<li><a href="{esc(g)}">{esc(GUIDE_TITLES.get(g[:-5], g).split(" | ")[0])}</a></li>'
            for g in s["guides"])
        blocks.append(f"""
  <div class="card season-card">
    <p class="eyebrow">{esc(s["window"])} · {esc(s["status"])}</p>
    <h3>{esc(s["name"])}</h3>
    <p>{esc(s["line"])}</p>
    <ul class="season-guides">{links}</ul>
  </div>""")
    return ('<div class="card-grid season-grid">' + "".join(blocks) + "</div>"
            + '<p class="table-note">Seasons follow the US calendar (the marketplace is amazon.com). '
            "They are an editorial rotation, not a demand claim — no season is chosen from a trend figure "
            '(<a href="flagged.html#F-15">F-15</a>). Rotation register: '
            '<a href="https://github.com/wingbangboozle1-lang/Prod2/blob/main/data/p2/calendar.json" rel="noopener" target="_blank">data/p2/calendar.json</a>.</p>')


def hook_clusters(_="") -> str:
    blocks = []
    for c in CALENDAR["clusters"]:
        links = "".join(
            f'<li><a href="{esc(g)}">{esc(GUIDE_TITLES.get(g[:-5], g).split(" | ")[0])}</a></li>'
            for g in c["guides"])
        blocks.append(f"""
  <div class="card cluster-card">
    <p class="eyebrow">Cluster · {len(c["guides"])} guides</p>
    <h3><a href="{esc(c["pillar"])}">{esc(c["name"])}</a></h3>
    <p>{esc(c["line"])}</p>
    <ul class="cluster-guides">{links}</ul>
    <p><a class="more" href="{esc(c["pillar"])}">The {esc(c["name"].lower())} pillar page</a></p>
  </div>""")
    return '<div class="card-grid cluster-grid">' + "".join(blocks) + "</div>"


def hook_queue(_="") -> str:
    rows = "".join(
        f'<tr><td>{esc(q["due_utc"])}</td><td>{esc(q["title"])}</td><td>{esc(q["answers_with"])}</td></tr>'
        for q in CALENDAR["queue"])
    return (f'<div class="table-scroll"><table class="data"><thead><tr><th>Due (UTC)</th>'
            f"<th>Working title — a hypothesis, not a popularity claim</th>"
            f"<th>Answerable from</th></tr></thead><tbody>{rows}</tbody></table></div>"
            f'<p class="table-note">Cadence: {esc(CALENDAR["cadence"]["unit"])}, every '
            f'{esc(str(CALENDAR["cadence"]["interval_days"]))} days; next due '
            f'{esc(CALENDAR["cadence"]["next_due_utc"])}. {esc(CALENDAR["cadence"]["rule"])}</p>')


def hook_questions_summary(_="") -> str:
    rows = []
    for q in QUESTIONS:
        state = "owner action" if "account holder" in q.get("answerable_by", "").lower() else "open"
        rows.append(f'<tr><td><a href="#{esc(q["id"])}"><code>{esc(q["id"])}</code></a></td>'
                    f'<td>{esc(q["area"])}</td><td>{esc(q["question"])}</td>'
                    f'<td>{esc(state)}</td><td>{esc(", ".join(q.get("blocks", [])) or "—")}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>ID</th><th>Area</th>'
            '<th>The question</th><th>State</th><th>What it blocks</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>"
            + '<p class="table-note">The full register below answers each row in five fields: '
            "what we know, what is missing, how to discover it, who can answer it, and what it blocks.</p>")


def hook_guides_index(_="") -> str:
    out = []
    for c in CALENDAR["clusters"]:
        items = "".join(_guide_card(g[:-5]) for g in c["guides"] if g[:-5] in GUIDE_TITLES)
        out.append(f'<h2 class="cluster-head">Cluster: {esc(c["name"])}</h2>'
                   f'<p class="lede">{esc(c["line"])} Start at the '
                   f'<a href="{esc(c["pillar"])}">{esc(c["name"].lower())} pillar</a> or pick a question.</p>'
                   f'<div class="card-grid">{items}</div>')
    return "".join(out)


def hook_shop_grid(_="") -> str:
    """The shelf with filter chips. Filters are progressive enhancement: with no
    JavaScript every card is simply visible, so the page still sells."""
    groups = [
        ("af", "Air fryers", [p for p in PRODUCTS if p["format"].lower().find("thermometer") == -1]),
        ("th", "Thermometers", [p for p in PRODUCTS if p["format"].lower().find("thermometer") != -1]),
    ]
    chips = ['<a class="chip is-active" href="shop.html" aria-pressed="true">All <span class="count">5</span></a>']
    for pid, label, members in groups:
        chips.append(f'<button type="button" class="chip" data-filter="{pid}" aria-pressed="false">'
                     f'{esc(label)} <span class="count">{len(members)}</span></button>')
    # format-level filters, one per distinct listed format
    fmt_chips = []
    seen = set()
    for p in PRODUCTS:
        f = p["format"]
        if f in seen:
            continue
        seen.add(f)
        slug = f.lower().replace(" ", "-").replace("&", "and")
        fmt_chips.append(f'<button type="button" class="chip" data-format="{esc(slug)}" aria-pressed="false">'
                         f'{esc(f)}</button>')
    cards = hook_product_cards("")
    return (f'<div class="filter-bar" role="group" aria-label="Filter the shelf">'
            f'<span class="label">Show</span>{"".join(chips)}</div>'
            f'<div class="filter-bar" role="group" aria-label="Filter by format">'
            f'<span class="label">Format</span>{"".join(fmt_chips)}</div>'
            f'{cards}'
            '<p class="filter-status" id="filter-status" role="status" aria-live="polite"></p>')


def hook_compare_table(_="") -> str:
    """The decision-grade comparison table: attributed columns, sourced cells,
    blanks that stay blank. Wraps the existing products_table output."""
    return hook_products_table("")


HOOKS = {
    "products_table": hook_products_table,
    "air_fryer_table": hook_air_fryer_table,
    "thermo_table": hook_thermo_table,
    "counter_space": hook_counter_space,
    "chooser": hook_chooser,
    "intent_table": hook_intent_table,
    "commission_table": hook_commission_table,
    "trust_row": hook_trust_row,
    "sources_table": hook_sources_table,
    "flags_open": lambda _: hook_flags("open"),
    "flags_resolved": lambda _: hook_flags("resolved"),
    "flags_standing": lambda _: hook_flags("standing"),
    "questions": hook_questions,
    "suggestions": hook_suggestions,
    "decisions": hook_decisions,
    "ledger_events": hook_ledger_events,
    "ledger_table": hook_ledger_table,
    "local_events": hook_local_events,
    "product_cards": hook_product_cards,
    "guide_links": hook_guide_links,
    "comparison_cta": hook_comparison_cta,
    "guide_cards": hook_guide_cards,
    "subscribe": hook_subscribe,
    "reader_capture": hook_reader_capture,
    "byline": hook_byline,
    "season_desk": hook_season_desk,
    "clusters": hook_clusters,
    "queue": hook_queue,
    "questions_summary": hook_questions_summary,
    "guides_index": hook_guides_index,
    "shop_grid": hook_shop_grid,
    "compare_table": hook_compare_table,
}


AMAZON_HREF = re.compile(r'href="(https://www\.amazon\.com[^"]*)"')
ANCHOR_TAG = re.compile(r"<a\b[^>]*>")


def normalize_amazon_links(fragment: str) -> str:
    """Rewrite outbound Amazon anchors by policy (see compliance page):
    - /dp/ product links -> rel="sponsored nofollow noopener", tag=shopnow047c-20.
    - other Amazon links (help pages, browse nodes) -> rel="nofollow noopener".
    - link.amazon short links are NEVER a clickable destination. They are quoted
      evidence of what the owner submitted, their status is unresolved (F-03 /
      FLG-003), and the site's own outbound product hrefs are the tagged /dp/
      URLs. Any remaining short-link anchor is rendered as inert text.
    """

    def fix_anchor(m: "re.Match[str]") -> str:
        tag = m.group(0)
        hm = re.search(r'href="([^"]+)"', tag)
        if not hm:
            return tag
        url = hm.group(1)
        if url.startswith("https://link.amazon"):
            return f'<code>{url}</code>'
        if not url.startswith("https://www.amazon.com"):
            return tag
        is_product = "/dp/" in url
        if is_product and "tag=" not in url:
            sep = "&" if "?" in url else "?"
            url = url + sep + "tag=shopnow047c-20"
        tag = tag[:hm.start(1)] + url + tag[hm.end(1):]
        rel = 'rel="sponsored nofollow noopener"' if is_product else 'rel="nofollow noopener"'
        if re.search(r'\brel="[^"]*"', tag):
            tag = re.sub(r'\brel="[^"]*"', rel, tag)
        else:
            tag = tag.replace("<a ", "<a " + rel + " ", 1)
        return tag

    return ANCHOR_TAG.sub(fix_anchor, fragment)


def render_fragment(text: str) -> str:
    def repl(m):
        key = m.group(1)
        if ":" in key:
            name, arg = key.split(":", 1)
            if name == "facts":
                return hook_facts(arg)
            if name == "buy":
                return buy_link(PROD_BY_ID[arg])
            raise KeyError(key)
        if key in HOOKS:
            return HOOKS[key]("")
        if key == "brand":
            return esc(BRAND)
        if key == "descriptor":
            return esc(DESCRIPTOR)
        if key == "tagline":
            return esc(TAGLINE)
        if key == "disclosure":
            return esc(DISCLOSURE)
        if key == "paid_label":
            return esc(PAID_LABEL)
        if key == "base_url":
            return esc(BASE)
        raise KeyError(key)
    return normalize_amazon_links(re.sub(r"\{\{([a-zA-Z0-9_:]+)\}\}", repl, text))


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------
def jsonld_for(page_id: str, title: str, description: str, path: str) -> str:
    graph = [{
        "@type": "WebSite", "name": f"{BRAND} — {DESCRIPTOR}", "url": BASE + "/",
        "description": TAGLINE,
        "publisher": {"@type": "Organization", "name": BRAND, "url": BASE + "/"},
    }]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
    if page_id != "index":
        crumbs.append({"@type": "ListItem", "position": 2, "name": title.split(" | ")[0],
                       "item": BASE + "/" + path})
        graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    if page_id in ("index", "compare", "products"):
        items = []
        for i, p in enumerate(PRODUCTS, 1):
            items.append({
                "@type": "ListItem", "position": i,
                "url": BASE + "/products.html#" + p["id"],
                "name": p["name_short"],
                "item": {
                    "@type": "Product",
                    "name": p["name_listing"],
                    "sku": p["asin"],
                    "gtin13": None,
                    "brand": {"@type": "Brand", "name": p.get("brand") or "unknown"},
                    "category": p.get("category_path"),
                    "url": "https://www.amazon.com/dp/" + p["asin"],
                    "description": p.get("special_feature"),
                },
            })
        graph.append({"@type": "ItemList", "name": "Products compared on " + BRAND,
                      "itemListElement": items})
    if (page_id.startswith(("guide", "article")) and page_id != "guides") or page_id == "buying-guide":
        graph.append({
            "@type": "Article", "headline": title.split(" | ")[0],
            "description": description, "url": BASE + "/" + path,
            "datePublished": BUILD_DATE, "dateModified": BUILD_DATE,
            "author": {"@type": "Organization", "name": BRAND},
            "publisher": {"@type": "Organization", "name": BRAND},
            "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + "/" + path},
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=1)


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
LAYOUT = """<!DOCTYPE html>
<html lang="en" data-endpoint="{endpoint}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{base}/assets/img/og-card.png">
<meta property="og:site_name" content="{brand} — {descriptor}">
<meta name="twitter:card" content="summary_large_image">
{site_verification}<link rel="alternate" type="application/rss+xml" title="{brand} feed" href="{base}/feed.xml">
<link rel="preload" href="{base}/assets/fonts/fraunces-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}/assets/css/site.css">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body data-page="{page_id}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap masthead-row">
    <a class="wordmark" href="{base}/index.html"><span class="wordmark-name">{brand}<span class="wordmark-dot">.</span></span>
      <span class="wordmark-desc">{descriptor}</span></a>
    {nav}
  </div>
  {disclosure}
</header>
<main id="main" class="wrap">
{content}
</main>
{footer}
<script src="{base}/assets/js/site.js" defer></script>
<script src="{base}/assets/js/measure.js" defer></script>
</body>
</html>
"""


def build_page(page_id: str, path: str, title: str, description: str, section: str) -> None:
    frag = (CONTENT / "pages" / f"{page_id}.html").read_text(encoding="utf-8")
    content = render_fragment(frag)
    nav = build_nav(path)
    token = (SETTINGS.get("search_console", {}) or {}).get("verification_token", "") or ""
    site_verification = (f'<meta name="google-site-verification" content="{esc(token)}">\n'
                         if token else "")
    out = LAYOUT.format(
        title=esc(title), description=esc(description), canonical=f"{BASE}/{path}",
        base=esc(BASE), brand=esc(BRAND), descriptor=esc(DESCRIPTOR),
        jsonld=jsonld_for(page_id, title, description, path),
        page_id=esc(page_id), nav=nav, disclosure=DISCLOSURE_STRIP,
        content=content, footer=build_footer(),
        endpoint=esc(SETTINGS.get("analytics_endpoint", "") or ""),
        site_verification=site_verification,
    )
    (DOCS / path).write_text(out, encoding="utf-8")


def build_feed() -> None:
    items = []
    for gid in GUIDE_IDS + ["buying-guide", "article-thermometer-placement", "article-air-fryer-doneness"]:
        p = next(x for x in PAGES if x[0] == gid)
        items.append(f"""    <item>
      <title>{esc(p[2].split(' | ')[0])}</title>
      <link>{BASE}/{p[1]}</link>
      <guid isPermaLink="true">{BASE}/{p[1]}</guid>
      <description>{esc(p[3])}</description>
      <pubDate>{BUILD_DATE}T09:00:00Z</pubDate>
    </item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{esc(BRAND)} — {esc(DESCRIPTOR)}</title>
    <link>{BASE}/</link>
    <description>{esc(TAGLINE)}. Question-shaped kitchen buying guides with every figure sourced.</description>
    <language>en-us</language>
    <lastBuildDate>{BUILD_DATE}T09:00:00Z</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""
    (DOCS / "feed.xml").write_text(feed, encoding="utf-8")


def build_sitemap() -> None:
    urls = "".join(
        f"  <url><loc>{BASE}/{p[1]}</loc><lastmod>{BUILD_DATE}</lastmod></url>\n"
        for p in PAGES)
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls + "</urlset>\n", encoding="utf-8")


def build_robots() -> None:
    # Pages currently serves the repository ROOT (build_type: legacy, source
    # "main /") - see flag F-P19/F-P20. That means the source registers, the
    # content fragments and the build tools are technically fetchable at the
    # public URL. robots.txt is not access control, but disallowing the source
    # directories keeps them out of search results and stops them being read as
    # duplicate content for the publication.
    (DOCS / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n"
        "Disallow: /Prod2/archive/\n"
        "Disallow: /Prod2/data/\n"
        "Disallow: /Prod2/content/\n"
        "Disallow: /Prod2/tools/\n"
        "Disallow: /Prod2/scripts/\n"
        "Disallow: /Prod2/tests/\n"
        "Disallow: /Prod2/site/\n"
        "Disallow: /Prod2/.git/\n"
        "Disallow: /Prod2/.github/\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n", encoding="utf-8")


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "assets").mkdir(exist_ok=True)
    if ASSETS_SRC.exists():
        # Mirror, do not overlay: an asset deleted or replaced in assets/ must
        # disappear from docs/assets/ too, or the freshness check fails forever.
        if (DOCS / "assets").exists():
            shutil.rmtree(DOCS / "assets")
        shutil.copytree(ASSETS_SRC, DOCS / "assets", dirs_exist_ok=True)
    for page_id, path, title, desc, section in PAGES:
        build_page(page_id, path, title, desc, section)
    build_feed()
    build_sitemap()
    build_robots()
    (DOCS / ".nojekyll").write_text("")
    print(f"built {len(PAGES)} pages -> {DOCS}")


def mirror_to_root():
    """Legacy "main /" Pages serves the repo root. Mirror the publication there so
    the canonical URL carries it (INT-07's approach, retargeted to this build).
    Purge artifacts of the previous mirror (site/ output) first so no stale pages
    linger at root. Writes .nojekyll so the root is served as static files."""
    site = ROOT / "site"
    if site.is_dir():
        for src in site.rglob("*"):
            if src.is_file():
                rel = src.relative_to(site)
                dst = ROOT / rel
                if dst.is_file():
                    dst.unlink()
        for src in sorted(site.rglob("*"), reverse=True):
            d = ROOT / src.relative_to(site)
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
    for src in DOCS.rglob("*"):
        if src.is_file():
            dst = ROOT / src.relative_to(DOCS)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    (ROOT / ".nojekyll").write_text("")
    (DOCS / ".nojekyll").write_text("")
    print("mirrored docs/ -> repo root")


if __name__ == "__main__":
    main()
    mirror_to_root()
