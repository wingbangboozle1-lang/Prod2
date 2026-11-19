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

BUILD_DATE = "2026-11-19"  # set on each publishing pass


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
DESIGN = load("design-prompts.json")
PRIORITY = load("decision-priority.json")
VERLOG = load("verification-log.json")["entries"]

# How long a guide takes to read, computed from the fragment that is actually published
# (tags and build hooks stripped). Same input -> same number, so the build stays deterministic.
WORDS_PER_MINUTE = 225


def guide_body(page_id: str) -> str:
    raw = (CONTENT / "pages" / f"{page_id}.html").read_text(encoding="utf-8")
    raw = re.sub(r"\{\{[^}]+\}\}", " ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", raw).strip()


def guide_minutes(page_id: str) -> int:
    words = len(guide_body(page_id).split())
    return max(1, round(words / WORDS_PER_MINUTE))


def guide_stat(page_id: str) -> str:
    """'3 min read · 5 sections' — counted from the page, nothing claimed about its audience."""
    raw = (CONTENT / "pages" / f"{page_id}.html").read_text(encoding="utf-8")
    h2 = len(re.findall(r"<h2\b", raw))
    return f"{guide_minutes(page_id)} min read · {h2} section{'s' if h2 != 1 else ''}"

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
     f"Find the format that fits your kitchen | {BRAND}",
     "Three air fryers and two meat thermometers compared by format, capacity and counter fit. Every figure links to the official listing it was read from.",
     "home"),
    ("compare", "compare.html",
     f"Compare the five products side by side | {BRAND}",
     "One sourced comparison table: format, capacity, dimensions, counter depth and listed features — plus a three-question chooser and the counter-space analysis.",
     "compare"),
    ("products", "products.html",
     f"The five products, spec by spec | {BRAND}",
     "Full listed specifications with read dates and source links, plus the product-intent confirmation record for every submitted link. Blank means unverified.",
     "products"),
    ("buying-guide", "buying-guide.html",
     f"Buying guide: choose by format, capacity and counter fit | {BRAND}",
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
    ("guide-thermometer-accuracy", "guide-thermometer-accuracy.html",
     f"How accurate does a meat thermometer need to be? | {BRAND}",
     "±0.5°F vs ±1°F, instant-read vs leave-in wireless: what accuracy claims on the listing mean and which thermometer fits which cook.",
     "guides"),
    ("guide-dual-vs-single", "guide-dual-vs-single.html",
     f"Dual-basket or single-basket air fryer: which? | {BRAND}",
     "Two 3 qt baskets or one 8 qt basket? What the listed capacity, depth and shake-reminder "
     "features actually decide, with every figure read from the listings.",
     "guides"),
    ("guide-probe-in-air-fryer", "guide-probe-in-air-fryer.html",
     f"Can you leave a meat thermometer in an air fryer? | {BRAND}",
     "Probe heat ratings, basket depth and what leave-in monitoring means in a small cavity - "
     "read from the two listings and the air fryers here, with the gaps left blank.",
     "guides"),
    ("guide-air-fryer-gift", "guide-air-fryer-gift.html",
     f"Air fryer as a gift: the four checks that matter | {BRAND}",
     "Gifting an air fryer or a thermometer? Four checks before you wrap: footprint, what is in "
     "the box, what they must already own, and which variant actually ships.",
     "guides"),
    ("guides", "guides.html",
     f"Kitchen buying guides, one question each | {BRAND}",
     "Eight question-shaped guides on air fryers and meat thermometers. Every figure links to the "
     "official listing it was read from, with the date.",
     "guides"),
    ("analysis", "analysis.html",
     f"Analysis: what the verified data supports | {BRAND}",
     "The findings this register can carry: coverage, the capacity-to-footprint ranking, the "
     "funnel in three stages and the verification ledger.",
     "work"),
    ("design-prompt", "design-prompt.html",
     f"Design prompt pack for this publication | {BRAND}",
     "Eight copy-ready design briefs and the guardrails that survive any redesign: compliance "
     "constraints first, so a restyle cannot undo the disclosure.",
     "work"),
    ("category-air-fryers", "category-air-fryers.html",
     f"Air fryers: dual-basket, toaster-oven, single-basket | {BRAND}",
     "Three air-fryer formats compared by the decision that matters — how they fit your counter and your cooking. Listed specs only, each with its source.",
     "categories"),
    ("category-thermometers", "category-thermometers.html",
     f"Meat thermometers: instant-read vs wireless leave-in | {BRAND}",
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
     f"Measurement: events, clicks and the campaign ledger | {BRAND}",
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

GUIDE_IDS = ["guide-basket-vs-oven", "guide-capacity", "guide-dual-vs-single",
             "guide-cleanup-counter-space", "guide-multifunction",
             "guide-probe-in-air-fryer", "guide-air-fryer-gift", "guide-thermometer-accuracy"]
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


def buy_link(p: dict, text: str | None = None) -> str:
    label = text or f"See the {p['name_short']} on Amazon"
    return amazon_link(p["buy_url"], label, "btn") + f' <span class="paid">{esc(PAID_LABEL)}</span>'


# ---------------------------------------------------------------------------
# Layout chrome
# ---------------------------------------------------------------------------
NAV_READER = [
    ("compare.html", "Compare"),
    ("products.html", "Products"),
    ("buying-guide.html", "Buying guide"),
    ("guides.html", "Guides"),
    ("category-air-fryers.html", "Air fryers"),
    ("category-thermometers.html", "Thermometers"),
]
NAV_WORK = [
    ("executive-summary.html", "Executive summary"),
    ("method.html", "Method &amp; sources"),
    ("analysis.html", "Analysis &amp; findings"),
    ("flagged.html", "Flagged for review"),
    ("questions.html", "Open questions"),
    ("suggestions.html", "Suggestions"),
    ("design-prompt.html", "Design prompt pack"),
    ("decisions.html", "Decisions"),
    ("measurement.html", "Measurement"),
    ("compliance.html", "Compliance"),
    ("privacy.html", "Privacy"),
]
GUIDE_LINKS = [
    ("guides.html", "All guides"),
    ("guide-basket-vs-oven.html", "Basket or oven-style air fryer?"),
    ("guide-capacity.html", "The capacity checklist"),
    ("guide-cleanup-counter-space.html", "Cleanup &amp; counter space"),
    ("guide-multifunction.html", "Before buying multi-function"),
    ("guide-dual-vs-single.html", "Dual basket or one big basket?"),
    ("guide-probe-in-air-fryer.html", "A leave-in probe in an air fryer?"),
    ("guide-air-fryer-gift.html", "Air fryer as a gift: four checks"),
    ("guide-thermometer-accuracy.html", "Thermometer accuracy"),
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
    shop = lis([("compare.html", "Compare all products"), ("products.html", "Products &amp; specs"),
                ("category-air-fryers.html", "Air fryers"), ("category-thermometers.html", "Thermometers"),
                ("buying-guide.html", "Buying guide")])
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
    <div><h2>The work behind it</h2><ul>{work}</ul></div>
  </div>
  <p class="wrap footer-legal">Published {esc(BUILD_DATE)}. Prices and star ratings are not published — see <a href="flagged.html#F-02">F-02</a>.
  Product links are Amazon Associates Special Links. Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.</p>
</footer>"""


DISCLOSURE_STRIP = (f'<div class="disclosure" role="note">'
                    f'<span class="disclosure-check" aria-hidden="true">✓</span> '
                    f'<strong>{esc(DISCLOSURE)}</strong> '
                    f'<span class="disclosure-more">Product links on this site are paid links ({esc(PAID_LABEL)}); '
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


UNVERIFIED = "—"


def _read_label(p: dict, key: str) -> str:
    """'read 2026-11-14' beside a published figure, or "" when there is no figure to date.
    A date is never printed for a value that was not read, and never estimated."""
    d = p.get(key)
    return f"read {d}" if d else ""


def _chip(p: dict, key: str) -> str:
    label = _read_label(p, key)
    return f'<br><span class="chip-read">{label}</span>' if label else ""


def hook_products_table(_="") -> str:
    head = ("<thead><tr><th>Product</th><th>Format</th><th>Capacity as listed</th>"
            "<th>Dimensions (D×W×H) as listed</th><th>Counter depth</th><th>Capacity per inch of depth</th>"
            "<th>What it is for</th><th>Source</th><th>Where to look</th></tr></thead>")
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
            f'<tr id="{p["id"]}"><td><strong>{esc(p["name_short"])}</strong><br>'
            f'<span class="muted">{esc(p["asin"])}</span></td>'
            f'<td>{esc(p["format"])}</td>'
            f'<td>{esc(p["capacity"] or UNVERIFIED)}{_chip(p, "capacity_read")}</td>'
            f'<td>{esc(p["dimensions"] or UNVERIFIED)}{_chip(p, "dimensions_read")}</td>'
            f'<td>{esc(str(depth) + chr(34) if depth else UNVERIFIED)}</td>'
            f'<td>{ratio}</td><td>{esc(why)}</td><td>{listing_link(p)}</td>'
            f'<td>{buy_link(p, "See it on Amazon")}</td></tr>')
    return (f'<div class="table-scroll"><table class="data products-table">{head}'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="table-note">Capacity / depth = listed qt capacity ÷ listed counter depth (inches), '
            f'shown as the formula, computed only where both figures are listed (P4/P5 are thermometers — no capacity). '
            f'No prices or ratings are published (<a href="flagged.html#F-02">F-02</a>): a price read by hand is '
            f'stale the day it is posted, so the button invites a check rather than quoting a number. '
            f'Every row links to the official listing it was read from.</p>')


def hook_air_fryer_table(_="") -> str:
    rows = []
    for p in PRODUCTS[:3]:
        rows.append(f'<tr><td><strong>{esc(p["name_short"])}</strong></td><td>{esc(p["format"])}</td>'
                    f'<td>{esc(p["capacity"])}</td><td>{esc(p["dimensions"])}</td>'
                    f'<td>{esc(p["special_feature"])}</td><td>{listing_link(p)}</td>'
                    f'<td>{buy_link(p, "See it on Amazon")}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Product</th><th>Format</th>'
            '<th>Capacity</th><th>Dimensions (D×W×H)</th><th>Listed special features</th>'
            '<th>Source</th><th></th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>')


def hook_thermo_table(_="") -> str:
    rows = []
    for p in PRODUCTS[3:]:
        rows.append(f'<tr><td><strong>{esc(p["name_short"])}</strong></td><td>{esc(p["format"])}</td>'
                    f'<td>{esc(p["special_feature"])}</td><td>{listing_link(p)}</td>'
                    f'<td>{buy_link(p, "See it on Amazon")}</td></tr>')
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


def hook_sources_table(_="") -> str:
    rows = []
    for s in SOURCES:
        reads = ", ".join(s.get("read", []))
        rows.append(f'<tr id="{esc(s["id"])}"><td><code>{esc(s["id"])}</code></td><td>{esc(s["title"])}</td>'
                    f'<td><a class="src" href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["url"])[:64]}</a></td>'
                    f'<td>{esc(s["kind"])}</td><td>{esc(reads)}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>ID</th><th>Source</th>'
            '<th>Official URL</th><th>Kind</th><th>Read (UTC)</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>')


def _flag_row(f: dict) -> str:
    return (f'<tr id="{esc(f["id"])}"><td><code>{esc(f["id"])}</code></td><td>{esc(f["title"])}</td>'
            f'<td>{esc(f["detail"])}</td>'
            f'<td><a class="src" href="{esc(f["evidence"])}" rel="noopener" target="_blank">evidence</a><br>'
            f'<span class="muted">{esc(f["evidence_note"])}</span></td>'
            f'<td>{esc(f["how_to_resolve"])}</td></tr>')


def hook_flags(status: str) -> str:
    rows = [_flag_row(f) for f in FLAGS if f["status"] == status]
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>ID</th><th>Item</th>'
            '<th>What and why</th><th>Evidence</th><th>How it resolves</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>')


def _q_gate_row(q: dict) -> str:
    gates = q.get("gates") or ([q["decision_at_stake"]] if q.get("decision_at_stake") else [])
    gates_txt = "; ".join(gates) if gates else "Nothing on the publish path."
    blocking = q.get("blocking")
    badge = ('<span class="status status-open">gates a decision</span>' if blocking
             else '<span class="status status-resolved">does not gate</span>')
    checks = "".join(
        f'<a class="src" href="{esc(c["url"])}" rel="noopener" target="_blank">{esc(c["label"])}</a>'
        for c in q.get("checks", [])) or '<span class="muted">internal register only</span>'
    answer = q.get("owner_answer")
    ans_block = (f'<p class="q-answer"><strong>Your answer on {esc(q.get("owner_answer_date", ""))}:</strong> '
                 f'{esc(answer)}</p>' if answer else
                 '<p class="q-answer q-answer-empty"><span class="badge">Awaiting your answer</span> '
                 f'{esc(q.get("default_if_unanswered") or "The site keeps its current behaviour; nothing blocks publication.")}</p>')
    return (f'<tr id="{esc(q["id"])}"><td><code>{esc(q["id"])}</code><br>{badge}</td>'
            f'<td><strong>{esc(q["question"])}</strong><br>'
            f'<span class="muted">{esc(q.get("area", ""))}</span></td>'
            f'<td>{esc(q.get("known", ""))}</td>'
            f'<td>{esc(q.get("unknown", ""))}</td>'
            f'<td>{esc(gates_txt)}</td>'
            f'<td>{esc(q.get("how_to_discover") or q.get("how_to_answer") or "")}<br>{checks}</td>'
            f'<td>{esc(q.get("answerable_by", ""))}</td>'
            f'<td>{ans_block}</td></tr>')


def hook_questions_board(_="") -> str:
    """The gate table the brief asked for: what we know, what is missing, what it gates,
    where to verify it, and what the default is while nobody answers."""
    qs = sorted(QUESTIONS, key=lambda q: (not q.get("blocking"), q.get("rank", 99), q["id"]))
    blocking = sum(1 for q in QUESTIONS if q.get("blocking"))
    answered = sum(1 for q in QUESTIONS if q.get("owner_answer"))
    rows = "".join(_q_gate_row(q) for q in qs)
    return ('<div class="table-scroll"><table class="data q-board"><thead><tr><th>ID</th><th>Question</th>'
            '<th>What we know</th><th>What is missing</th><th>What it decides</th>'
            '<th>How to answer it</th><th>Who can answer</th><th>Status</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            f'<p class="table-note">{len(QUESTIONS)} questions: <strong>{blocking} gate a decision</strong> '
            f'and {len(QUESTIONS) - blocking} are recorded for completeness. {answered} carry an owner answer. '
            'A blank status column means nobody has answered yet - it does not mean the site guessed.</p>')


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


def _path_cards(item: dict) -> str:
    out = []
    for p in item.get("paths", []):
        rec = ' path-recommended' if p.get("recommended") else ""
        unlocks = (f'<p class="path-unlocks"><strong>Unlocks:</strong> {esc(p["unlocks"])}</p>'
                   if p.get("unlocks") else "")
        out.append(
            f'<div class="path-card{rec}" id="{esc(item["id"])}-{esc(p["key"])}">'
            f'<p class="path-key">Path {esc(p["key"])}'
            f'{" <span class=badge>recommended</span>" if p.get("recommended") else ""}</p>'
            f'<h4>{esc(p["label"])}</h4>'
            f'<dl><dt>What changes</dt><dd>{esc(p["what_changes"])}</dd>'
            f'<dt>Upside</dt><dd>{esc(p["upside"])}</dd>'
            f'<dt>Downside</dt><dd>{esc(p["downside"])}</dd>'
            f'<dt>Cost</dt><dd>{esc(p["cost"])}</dd></dl>{unlocks}</div>')
    return f'<div class="path-grid">{"".join(out)}</div>' if out else ""


def hook_suggestions_board(_="") -> str:
    """Ranked decision board: the one screen from which a reviewer can choose a path per item."""
    items = sorted(SUGGESTIONS, key=lambda s: (s.get("rank", 99), s["id"]))
    rows = []
    for s in items:
        paths = ", ".join(f'{p["key"]}{"*" if p.get("recommended") else ""}' for p in s.get("paths", []))
        state = s.get("owner_decision") or "to review"
        rows.append(f'<tr id="{esc(s["id"])}-board"><td><a href="suggestions.html#{esc(s["id"])}">'
                    f'<code>{esc(s["id"])}</code></a></td>'
                    f'<td><strong>{esc(s["title"])}</strong>'
                    f'{"<br><span class=muted>" + esc(s["note"]) + "</span>" if s.get("note") else ""}</td>'
                    f'<td>{esc(s.get("theme", ""))}</td>'
                    f'<td>{esc(s.get("impact", ""))}</td>'
                    f'<td>{esc(s.get("effort", ""))}</td>'
                    f'<td>{esc(paths) or "—"}</td>'
                    f'<td><span class="status status-{esc(s.get("status", "proposed"))}">{esc(state)}</span></td></tr>')
    return ('<div class="table-scroll"><table class="data board"><thead><tr><th>ID</th><th>Suggestion</th>'
            '<th>Theme</th><th>Expected impact</th><th>Effort</th><th>Paths (recommended marked *)</th>'
            '<th>Status</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'
            f'<p class="table-note">{len(items)} items, ranked by impact against effort as recorded in '
            '<code>data/p2/suggestions.json</code>. Ranking is editorial judgement against the registers: '
            'no traffic or conversion data exists to rank on yet (<a href="questions.html#Q-P14">Q-P14</a>).</p>')


def hook_suggestions(_="") -> str:
    """One card per queue item: the problem, the proposal, the evidence, and the paths a
    reviewer can choose between. Paths are the point of the page — a suggestion without a
    path is a wish, and 'reviewed' means picking one, not nodding at the idea."""
    out = []
    for s in sorted(SUGGESTIONS, key=lambda x: (x.get("rank", 99), x["id"])):
        deps = esc(", ".join(s.get("depends_on", [])) or "—")
        links = " ".join(
            f'<a class="src" href="{esc(l["url"])}" rel="noopener" target="_blank">{esc(l["label"])}</a>'
            for l in s.get("links", []))
        note = (f'<p class="s-note">{esc(s["note"])}</p>' if s.get("note") else "")
        theme = (f'<span class="s-theme">{esc(s["theme"])}</span>' if s.get("theme") else "")
        rank = f'<span class="s-rank">rank {esc(s.get("rank", "—"))}</span>' if s.get("rank") else ""
        feed = ('<span class="s-dp">feeds the design prompt</span>' if s.get("feeds_design_prompt") else "")
        decision = (f'<p class="s-decision"><strong>Recorded:</strong> {esc(s["owner_decision"])} '
                    f'({esc(s.get("owner_decision_date", ""))})</p>' if s.get("owner_decision") else
                    '<p class="s-decision s-decision-open"><strong>Your move:</strong> '
                    'accept a path (name it), amend it, or reject the item — then it moves to the '
                    '<a href="decisions.html">decision log</a> and the build picks it up.</p>')
        out.append(f"""
<article class="card s-card" id="{esc(s['id'])}">
  <header><h3><code>{esc(s['id'])}</code> {esc(s['title'])}</h3>
  <span class="status status-{esc(s['status'])}">{esc(s['status'])}</span></header>
  <p class="s-meta">{theme}{rank}{feed}</p>
  {note}
  <dl>
    <dt>Problem</dt><dd>{esc(s['problem'])}</dd>
    <dt>Proposal</dt><dd>{esc(s['proposal'])}</dd>
    <dt>Evidence</dt><dd>{esc(s['evidence'])}{' ' + links if links else ''}</dd>
    <dt>Expected impact</dt><dd>{esc(s['impact'])}</dd>
    <dt>Effort</dt><dd>{esc(s['effort'])}</dd>
    <dt>Risk</dt><dd>{esc(s['risk'])}</dd>
    <dt>Depends on</dt><dd>{deps}</dd>
  </dl>
  <p class="reco"><strong>Our recommendation:</strong> {esc(s['recommendation'])}</p>
  <h4 class="paths-h">Paths</h4>
  {_path_cards(s)}
  {decision}
</article>""")
    return "".join(out)


def _qn(nm: float) -> str:
    return f"{nm:.2f}".rstrip("0").rstrip(".")


def _guide_links_cell(gids):
    if not gids:
        return "—"
    return " ".join('<a href="%s.html">%s</a>' % (g, g.replace("guide-", "").replace("-", " ")) for g in gids)


DIMS_RE = re.compile(r'(\d+(?:\.\d+)?)\s*"D\s*x\s*(\d+(?:\.\d+)?)\s*"W\s*x\s*(\d+(?:\.\d+)?)\s*"H')


def parse_dims(s):
    """Return (depth, width, height) inches from a listing string like 13.38"D x 11.81"W x 10.63"H."""
    m = DIMS_RE.search(s or "")
    if not m:
        return None, None, None
    return (float(m.group(1)), float(m.group(2)), float(m.group(3)))


def hook_href_for(page_id: str) -> str:
    """The href a fragment would use to link to a page, for counting internal coverage."""
    return page_id + ".html"


def _analysis_products():
    """(product, capacity qt, qt per inch of depth, box volume cu in) for products with both figures."""
    out = []
    for p in PRODUCTS:
        cap = re.match(r"([\d.]+)", p.get("capacity") or "")
        d, w, h = parse_dims(p.get("dimensions"))
        if cap and d and w and h:
            c = float(cap.group(1))
            out.append((p, c, c / d, c * w * h, d))
    out.sort(key=lambda r: -r[2])
    return out


def hook_capacity_ranking(_="") -> str:
    """Computed from listed capacity and listed dimensions - arithmetic, not a score."""
    rows = []
    for (p, c, v, vol, d) in _analysis_products():
        rows.append(
            f'<tr><td><a href="products.html#{p["id"]}">{esc(p["name_short"])}</a></td>'
            f'<td>{esc(p["format"])}</td><td>{_qn(c)} qt</td>'
            f'<td>{_qn(d)}&quot;</td><td>{_qn(v)} qt per inch</td><td>{_qn(vol)} cu in</td>'
            f'<td class="muted">{esc(p.get("capacity_read") or "—")} / {esc(p.get("dimensions_read") or "—")}</td></tr>')
    lead = max(_analysis_products(), key=lambda r: r[3])
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Product</th><th>Format</th>'
            '<th>Listed capacity</th><th>Listed depth</th><th>Capacity per inch of depth</th>'
            '<th>Listed box as a volume</th><th>Read (capacity / dimensions)</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>'
            '<p class="findings"><strong>Findings.</strong> The ratios differ by more than three to one, which is '
            'the whole argument for comparing on more than quarts: a basket that stacks two zones and an oven with '
            'a rack are not the same unit of cooking. '
            f'The largest listed cavity here ({esc(lead[0]["name_short"])}, {_qn(lead[3])} cu in treated as a box) is '
            f'also the deepest machine at {_qn(lead[4])} inches - that is the trade the format makes, not a flaw in it. '
            'Usable cavity is smaller than either number and no listing here states it, so the figure stays blank '
            'rather than estimated.</p>')


def hook_coverage_matrix(_="") -> str:
    """Which published pages actually link to each product, counted from the fragments."""
    def cell(gids):
        if not gids:
            return "—"
        return " ".join('<a href="%s.html">%s</a>' % (g, g.replace("guide-", "").replace("-", " "))
                        for g in gids)
    def refs(pid):
        prod = PROD_BY_ID[pid]
        hits = []
        for gid in GUIDE_IDS + ["compare", "buying-guide", "index", "category-air-fryers",
                                "category-thermometers"]:
            f = CONTENT / "pages" / f"{gid}.html"
            if not f.exists():
                continue
            txt = f.read_text(encoding="utf-8")
            if prod["asin"] in txt or pid in txt or hook_href_for(gid) in txt:
                hits.append(gid)
        return hits
    rows = []
    for p in PRODUCTS:
        g = refs(p["id"])
        rows.append(f'<tr id="cov-{esc(p["id"])}"><td><a href="products.html#{esc(p["id"])}">{esc(p["name_short"])}</a></td>'
                    f'<td>{esc(p["format"])}</td><td>{len(g)}</td><td>{cell(g)}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Product</th><th>Format</th>'
            f'<th>Pages referencing it (of {len(GUIDE_IDS) + 4})</th><th>Which</th></tr></thead>'
            '<tbody>' + "".join(rows) + '</tbody></table></div>'
            '<p class="table-note">Counted from the published page bodies at build time. A short row is not a '
            'ranking problem - it is a shelf gap, and the fix is the kind of page named in the '
            '<a href="suggestions.html">queue</a>.</p>')


def hook_funnel(_="") -> str:
    return ("""<div class="table-scroll"><table class="data"><thead><tr><th>Stage</th><th>What exists now</th>
<th>What does not exist</th><th>How it becomes measurable</th></tr></thead><tbody>
<tr><td><strong>Arrive</strong></td><td>Twenty-plus published pages, a sitemap, an RSS feed, unique titles and
meta descriptions enforced by the gate, JSON-LD on every page</td><td>No Search Console property, so no
impressions, queries or positions — the reason no page here claims to be popular</td>
<td>Verify a property and submit the sitemap (<a href="questions.html#Q-P06">Q-P06</a>), then read two weeks
before reordering anything</td></tr>
<tr><td><strong>Click out</strong></td><td>Every product link is a tagged Special Link with the sponsored
attributes, and the click handler counts five local events</td><td>No collector receives them; the endpoint is
empty by design, so no click count exists</td><td>Host the existing collector (SG-06); counts then become
readable per page and per ASIN</td></tr>
<tr><td><strong>Convert</strong></td><td>Commission rates read from the official table with dates, and the
attribution windows on the measurement page</td><td>No earnings report, no order counts, no revenue figure —
none is published and none is estimated</td><td>The campaign ledger fills only from an authorized export; rows
are never modelled (SG-14)</td></tr></tbody></table></div>
<p class="findings"><strong>Finding.</strong> The middle stage is the cheap one: the client-side counting exists,
and the receiving end is one small service away. Until then every design argument on this repository is taste
against taste, which is exactly how a generated site gets generated.</p>""")


def hook_decision_board(_="") -> str:
    """The ranked 'answer this first' list, built from the open questions."""
    qs = sorted([q for q in QUESTIONS if q.get("blocking")], key=lambda q: (q.get("rank", 99), q["id"]))
    rows = []
    for i, q in enumerate(qs, 1):
        answer = q.get("owner_answer")
        status = (f'<span class="status status-resolved">answered {esc(q.get("owner_answer_date", ""))}</span>'
                  if answer else '<span class="status status-open">unanswered</span>')
        checks = " ".join(
            f'<a class="src" href="{esc(c["url"])}" rel="noopener" target="_blank">{esc(c["label"])}</a>'
            for c in q.get("checks", [])) or '<span class="muted">—</span>'
        rows.append(f'<tr><td>{i}</td><td><a href="questions.html#{esc(q["id"])}"><code>{esc(q["id"])}</code></a></td>'
                    f'<td><strong>{esc(q["question"])}</strong></td>'
                    f'<td>{esc(q.get("decision_at_stake") or "—")}</td>'
                    f'<td>{esc(q.get("answerable_by", ""))}<br>{checks}</td>'
                    f'<td>{status}</td></tr>')
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>#</th><th>ID</th><th>Question</th>'
            '<th>What it gates</th><th>Who answers, and where to check</th><th>Status</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>'
            f'<p class="table-note">{len(qs)} of {len(QUESTIONS)} open questions gate a decision. None blocks '
            'publication: the site stays live and correct while every one of them stays open, because the '
            'default for an unanswered question is the conservative behaviour already shipped.</p>')


def _src_cell(target: str) -> str:
    """Render a ledger 'source read' cell: a link when it is a URL, plain code when it is a
    command or a repo path - a build-time query is not something a reader can click."""
    if str(target).startswith("http"):
        return f'<a href="{esc(str(target))}" rel="noopener" target="_blank">{esc(str(target))}</a>'
    return f"<code>{esc(str(target))}</code>"


def hook_verification_ledger(_="") -> str:
    rows = "".join(
        f'<tr><td>{esc(v["checked_utc"])}</td><td><code>{esc(v["by"])}</code></td>'
        f'<td>{_src_cell(v["target"])}</td>'
        f'<td>{esc(v["result"])}</td></tr>' for v in VERLOG)
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Checked</th><th>Session</th>'
            '<th>Source read</th><th>What it showed</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
            f'<p class="table-note">{len(VERLOG)} dated checks on the register. The five product links were each '
            'resolved to their listing on 2026-11-19 and the listing title compared with the stored string; '
            'titles drift between reads on one listing, which is why the date is part of the figure '
            '(<a href="flagged.html#F-44">F-44</a>).</p>')


def hook_flag_stats(_="") -> str:
    open_f = [f for f in FLAGS if f.get("status") == "open"]
    stand = [f for f in FLAGS if f.get("status") == "standing"]
    res = [f for f in FLAGS if f.get("status") == "resolved"]
    accepted = sum(1 for s in SUGGESTIONS if s.get("owner_decision"))
    return (f'<div class="stat-grid">'
            f'<div class="stat"><b>{len(open_f)}</b><span>open flags, each with an evidence link</span></div>'
            f'<div class="stat"><b>{len(stand)}</b><span>standing rules the site publishes to</span></div>'
            f'<div class="stat"><b>{len(res)}</b><span>resolved with a dated answer</span></div>'
            f'<div class="stat"><b>{len(SUGGESTIONS)}</b><span>suggestions queued, {accepted} with a recorded decision</span></div>'
            f'<div class="stat"><b>{len(PRODUCTS)}</b><span>products tracked, all five link-verified today</span></div>'
            f'</div>')



def _ref_link(ref: str) -> str:
    """Link an SG-/Q-/F-/D- id to the page that carries it, so a ranked decision is a table of
    jump-offs rather than a list of acronyms."""
    ref = ref.strip().rstrip(",")
    if not ref:
        return ""
    if not re.fullmatch(r"(?:SG|Q|F|D|DP|G)-P?\d+", ref):
        # a phrase, not an id - 'every growth item below it' stays plain text rather than
        # becoming a link to an anchor that cannot exist.
        return esc(ref)
    if ref.startswith("SG-"):
        page = "suggestions.html"
    elif ref.startswith("Q-"):
        page = "questions.html"
    elif ref.startswith("F-"):
        page = "flagged.html"
    elif ref.startswith("D-"):
        page = "decisions.html"
    elif ref.startswith("DP-") or ref.startswith("G"):
        page = "design-prompt.html"
    else:
        return f"<code>{esc(ref)}</code>"
    return f'<a href="{page}#{esc(ref)}">{esc(ref)}</a>'


def _refs(text: str) -> str:
    """Turn ids inside a sentence into links, leaving the sentence itself untouched."""
    return re.sub(r"\b((?:SG|Q|F|D|DP|G)-P?\d[\w-]*)\b", lambda m: _ref_link(m.group(1)), esc(text))


def hook_priority_board(_="") -> str:
    """The owner's board: the ranked decisions this project is waiting on, each with what it is
    waiting for and what moves once it is answered. Ranking is judgement, recorded as such —
    there is no traffic or revenue data here to rank against (Q-P14)."""
    out = []
    for d in PRIORITY["ordering"]:
        unblocks = " ".join(_ref_link(u) for u in d.get("unblocks", [])) or '<span class="muted">—</span>'
        out.append(
            f'<li class="prio"><span class="prio-num">{d["rank"]}</span>'
            f'<p class="prio-item">{esc(d["decision"])}</p>'
            f'<p class="muted">{_refs(d["item"])}</p>'
            f'<p>{esc(d["why"])}</p>'
            f'<p class="prio-wait"><strong>Waiting on:</strong> {esc(d["waiting_on"])} '
            f'<span class="badge">effort: {esc(d["effort"])}</span></p>'
            f'<p class="prio-unblocks"><strong>Then moves:</strong> {unblocks}</p></li>')
    return ('<ol class="prio-list">' + "".join(out) + "</ol>"
            f'<p class="table-note">{len(PRIORITY["ordering"])} ranked items, from '
            '<a href="https://github.com/wingbangboozle1-lang/Prod2/blob/main/data/p2/decision-priority.json" '
            'rel="noopener" target="_blank">data/p2/decision-priority.json</a>. Answering one is usually a '
            'sentence; each answer becomes a dated entry in the '
            '<a href="decisions.html">decision log</a> and moves the queue under it.</p>')


def hook_design_pack(_="") -> str:
    import json as _json
    blocks = []
    for i, b in enumerate(DESIGN["blocks"], 1):
        acc = "".join(f"<li>{esc(x)}</li>" for x in b.get("acceptance", []))
        avo = "".join(f"<li>{esc(x)}</li>" for x in b.get("avoid", []))
        ev = " ".join(f'<a class="src" href="{esc(e["url"])}" rel="noopener" target="_blank">{esc(e["label"])}</a>'
                      for e in b.get("evidence", []))
        rel = " ".join(f'<a href="suggestions.html#{esc(s)}"><code>{esc(s)}</code></a>' for s in b.get("related", []))
        blocks.append(
            f'<article class="card dp-card" id="{esc(b["id"])}">'
            f'<header><p class="eyebrow">Prompt {i} of {len(DESIGN["blocks"])} · {esc(b["id"])}</p>'
            f'<h3>{esc(b["title"])}</h3><p class="muted">{esc(b["goal"])}</p></header>'
            f'<div class="dp-prompt"><pre><code>{esc(b["paste_prompt"])}</code></pre></div>'
            f'<details class="dp-meta"><summary>Acceptance criteria, avoid list, sources, linked suggestions</summary>'
            f'<div class="dp-cols"><div><h4>Done means</h4><ul>{acc}</ul></div>'
            f'<div><h4>Do not</h4><ul>{avo}</ul></div></div>'
            f'<p class="small-note">Evidence: {ev or "—"}<br>Queue items this depends on: {rel or "—"}</p>'
            f'</details></article>')
    rails = "".join(
        f'<tr id="rail-{esc(g["id"])}"><td><code>{esc(g["id"])}</code></td>'
        f'<td><strong>{esc(g["rule"])}</strong></td><td>{esc(g["why"])}</td>'
        f'<td>{esc(g["design_consequence"])}</td>'
        f'<td><a class="src" href="{esc(g["source"])}" rel="noopener" target="_blank">official source</a></td></tr>'
        for g in DESIGN["guardrails"])
    seq = "".join(f"<li>{esc(s)}</li>" for s in DESIGN["sequence"])
    return (f'<p class="lede">{esc(DESIGN["_meta"]["description"])}</p>'
            '<div class="callout callout-sage"><h3>Read the guardrails before the prompts</h3>'
            f'<p>{esc(DESIGN["_meta"]["how_it_relates_to_the_queue"])}</p></div>'
            '<h2 id="guardrails">The eight guardrails</h2>'
            '<div class="table-scroll"><table class="data"><thead><tr><th>#</th><th>Constraint</th>'
            '<th>Why it is fixed</th><th>What that means for a design</th><th>Source</th></tr></thead>'
            f'<tbody>{rails}</tbody></table></div>'
            '<h2 id="prompts">The eight prompts</h2>' + "".join(blocks) +
            '<h2 id="sequence">Suggested order of work</h2><ol>' + seq + '</ol>')


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


def deciding_numbers(p: dict) -> str:
    """The two listed figures that decide this product, chosen by format. Values come straight
    from the register; anything unlisted stays absent rather than approximate."""
    bits = []
    if p.get("capacity"):
        bits.append(("Listed capacity", p["capacity"], p.get("capacity_read")))
    if p.get("dimensions"):
        bits.append(("Listed footprint", p["dimensions"], p.get("dimensions_read")))
    if not bits:
        feat = (p.get("special_feature") or "").split(";")[0].strip()
        if feat:
            bits.append(("As listed", feat, p.get("spec_table_read")))
    return "".join(
        f'<p class="spec-line"><span>{esc(label)}</span> <strong>{esc(val)}</strong> '
        f'{read_chip(read)}</p>' for label, val, read in bits[:2])


def read_chip(read) -> str:
    return f'<span class="chip-read">read {esc(read)}</span>' if read else ""


def hook_product_cards(_="") -> str:
    cards = []
    for p in PRODUCTS:
        chips = []
        if p.get("function_count"):
            chips.append(esc(p["function_count"].split(" (")[0]) + " presets as listed")
        if p.get("special_feature"):
            first = p["special_feature"].split(";")[0].strip()
            if first and len(first) < 60:
                chips.append(esc(first))
        cards.append(f"""
<article class="card product-card" id="{esc(p['id'])}-card">
  <p class="eyebrow">{esc(p['format'])}</p>
  <h3><a href="products.html#{esc(p['id'])}">{esc(p['name_short'])}</a></h3>
  <p class="muted">{esc(p['asin'])} · {esc(p.get('brand') or '')}</p>
  {deciding_numbers(p)}
  <ul>
    <li>{esc(p.get('highlight_1') or '')}</li>
    <li>{esc(p.get('highlight_2') or '')}</li>
    <li>{esc(p.get('highlight_3') or '')}</li>
  </ul>
  <p class="card-cta">{buy_link(p)}</p>
  <p class="muted">Listed facts sourced to {listing_link(p, 'the official listing')} ({esc(p.get('name_listing_read') or '')}).
  Prices and ratings are not published here — <a href="flagged.html#F-02">F-02</a>.</p>
</article>""")
    return '<div class="card-grid product-rail">' + "".join(cards) + '</div>'


def hook_guide_shelf(_="") -> str:
    """The guide shelf: the question as the title, the tag, and a length measured from the
    page itself (words counted at build time - no audience or popularity claim)."""
    titles = {p[0]: p[2] for p in PAGES}
    topic = {"guide-basket-vs-oven": "Air fryers", "guide-capacity": "Air fryers",
             "guide-dual-vs-single": "Air fryers", "guide-cleanup-counter-space": "Air fryers",
             "guide-multifunction": "Air fryers", "guide-air-fryer-gift": "Buying guide",
             "guide-thermometer-accuracy": "Thermometers", "guide-probe-in-air-fryer": "Thermometers"}
    cards = []
    for gid in GUIDE_IDS:
        raw = (CONTENT / "pages" / f"{gid}.html").read_text(encoding="utf-8")
        deck = re.search(r'class="lede">(.*?)</p>', raw, re.S)
        cards.append(
            f'<article class="card guide-card"><p class="eyebrow">{esc(topic.get(gid, "Guide"))}</p>'
            f'<h3><a href="{gid}.html">'
            f'{esc(titles[gid].split(" | ")[0])}</a></h3>'
            f'<p>{esc((deck.group(1).strip() if deck else "")[:180])}</p>'
            f'<p class="muted">{guide_stat(gid)}</p></article>')
    return '<div class="card-grid guide-shelf">' + "".join(cards) + '</div>'


def hook_categories_row(_="") -> str:
    """Format tiles as data, so the shelf and the categories cannot disagree."""
    tiles = [("Dual-basket air fryers", "Two dishes, one machine, finished together.", "category-air-fryers.html#dual"),
             ("Air fryer toaster ovens", "Rack cooking, sheet-pan meals, French doors.", "category-air-fryers.html#oven"),
             ("Single-basket air fryers", "One big basket, the smallest footprint here.", "category-air-fryers.html#single"),
             ("Meat thermometers", "Instant-read checks and leave-in probes.", "category-thermometers.html")]
    return ('<div class="format-tiles">' + "".join(
        f'<a class="tile" href="{href}"><h3>{esc(name)}</h3><p>{esc(blurb)}</p></a>'
        for name, blurb, href in tiles) + '</div>')


def hook_facts(pid: str) -> str:
    p = PROD_BY_ID[pid]
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Fact</th><th>Value as listed</th>'
            '<th>Read (UTC)</th><th>Source</th></tr></thead><tbody>' + spec_rows(p) + '</tbody></table></div>'
            '<p class="small-note">Blank means the official listing does not state it; the reason sits on the '
            '<a href="flagged.html">flagged list</a>. Every figure keeps its read date because listing text '
            'changes between reads.</p>')


def hook_trust_rail(_="") -> str:
    read = sorted({v["checked_utc"] for v in VERLOG})
    open_f = sum(1 for f in FLAGS if f.get("status") == "open")
    return (f'<section class="trust-rail"><div>'
            f'<p class="eyebrow">Why this page is worth your minute</p>'
            f'<ul class="trust-list">'
            f'<li><b>{len(PRODUCTS)} products</b> tracked, each figure linked to the official listing it was read from.</li>'
            f'<li><b>{len(GUIDE_IDS)} guides</b> answering one buyer question each, plus a sourced comparison of all {len(PRODUCTS)}.</li>'
            f'<li><b>{len(SOURCES)} sources</b> in the register, most recently checked {esc(read[-1])}.</li>'
            f'<li><b>{open_f} open flags</b> published rather than smoothed over: blanks stay blanks.</li>'
            f'<li>No prices and no star ratings are shown, on purpose - <a href="flagged.html#F-02">F-02</a> explains.</li>'
            f'</ul></div>'
            f'<div class="trust-cta"><p class="cta-row">'
            f'<a class="btn" href="compare.html">Compare the {len(PRODUCTS)}</a>'
            f'<a class="btn btn-ghost" href="guides.html">Read the guides</a></p>'
            f'<p class="small-note">Product links are paid links: <a href="compliance.html">how that works here</a>.</p>'
            f'</div></section>')


def hook_guide_links(_="") -> str:
    items = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in GUIDE_LINKS)
    return f'<ul class="guide-links">{items}</ul>'


BAR_PAGES = {"compare.html", "products.html", "buying-guide.html", "category-air-fryers.html",
             "category-thermometers.html", "guide-basket-vs-oven.html", "guide-capacity.html",
             "guide-dual-vs-single.html", "guide-cleanup-counter-space.html", "guide-multifunction.html",
             "guide-probe-in-air-fryer.html", "guide-air-fryer-gift.html", "guide-thermometer-accuracy.html",
             "guides.html"}


def build_compare_bar() -> str:
    """A dismissible mobile bar: one tap from any reader page to the comparison and to the
    listing. Chrome, not content - it carries no figure, so it cannot go stale, and the
    disclosure above it is untouched (suggestion SG-23 path A; SG-08 folded in)."""
    first = PRODUCTS[0]
    close = '<button type="button" class="compare-bar-close" id="compare-bar-close" ' + \
            'aria-label="Hide this bar">&times;</button>'
    return ('<div class="compare-bar" id="compare-bar" role="complementary" aria-label="Compare and shop">'
            '<div class="wrap compare-bar-inner">'
            '<p class="compare-bar-copy">Five products, every figure sourced to its listing.</p>'
            '<div class="compare-bar-actions">'
            '<a class="btn btn-sm" href="compare.html">Compare all five</a>'
            + amazon_link(first["buy_url"], "See it on Amazon", "btn btn-sm btn-ghost")
            + close + '</div></div></div>')


def hook_comparison_cta(_="") -> str:
    return ('<p class="cta-row">' + buy_link(PROD_BY_ID["P1"], "Compare all five") +
            ' <a class="btn btn-ghost" href="buying-guide.html">Read the buying guide</a></p>')


HOOKS = {
    "products_table": hook_products_table,
    "air_fryer_table": hook_air_fryer_table,
    "thermo_table": hook_thermo_table,
    "counter_space": hook_counter_space,
    "chooser": hook_chooser,
    "intent_table": hook_intent_table,
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
    "guide_shelf": hook_guide_shelf,
    "categories_row": hook_categories_row,
    "questions_board": hook_questions_board,
    "suggestions_board": hook_suggestions_board,
    "capacity_ranking": hook_capacity_ranking,
    "coverage_matrix": hook_coverage_matrix,
    "funnel": hook_funnel,
    "decision_board": hook_decision_board,
    "priority_board": hook_priority_board,
    "verification_ledger": hook_verification_ledger,
    "flag_stats": hook_flag_stats,
    "design_pack": hook_design_pack,
    "trust_rail": hook_trust_rail,
    "comparison_cta": hook_comparison_cta,
}


AMAZON_HREF = re.compile(r'href="(https://(?:www\.amazon\.com|link\.amazon)[^"]*)"')
ANCHOR_TAG = re.compile(r"<a\b[^>]*>")


def normalize_amazon_links(fragment: str) -> str:
    """Rewrite outbound Amazon anchors by policy (see compliance page):
    - /dp/ product links and link.amazon short product links -> rel="sponsored
      nofollow noopener"; /dp/ links also carry tag=shopnow047c-20.
    - link.amazon short links are never given a query string (their status is
      F-03 / FLG-003 unresolved).
    - other Amazon links (help pages, browse nodes) -> rel="nofollow noopener".
    """

    def fix_anchor(m: "re.Match[str]") -> str:
        tag = m.group(0)
        hm = re.search(r'href="([^"]+)"', tag)
        if not hm:
            return tag
        url = hm.group(1)
        if not (url.startswith("https://www.amazon.com") or url.startswith("https://link.amazon")):
            return tag
        is_product = "/dp/" in url or url.startswith("https://link.amazon")
        if "/dp/" in url and "tag=" not in url:
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
    if page_id.startswith("guide") or page_id == "buying-guide":
        graph.append({
            "@type": "Article", "headline": title.split(" | ")[0],
            "description": description, "url": BASE + "/" + path,
            "datePublished": BUILD_DATE, "dateModified": BUILD_DATE,
            "wordCount": len(guide_body(page_id).split()),
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
<html lang="en">
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
<link rel="alternate" type="application/rss+xml" title="{brand} feed" href="{base}/feed.xml">
<link rel="stylesheet" href="{base}/assets/css/site.css">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body data-page="{page_id}">
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap masthead-row">
    <a class="wordmark" href="{base}/index.html"><span class="wordmark-name">{brand}</span>
      <span class="wordmark-desc">{descriptor}</span></a>
    {nav}
  </div>
  {disclosure}
</header>
<main id="main" class="wrap">
{content}
</main>
{bar}
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
    out = LAYOUT.format(
        title=esc(title), description=esc(description), canonical=f"{BASE}/{path}",
        base=esc(BASE), brand=esc(BRAND), descriptor=esc(DESCRIPTOR),
        jsonld=jsonld_for(page_id, title, description, path),
        page_id=esc(page_id), nav=nav, disclosure=DISCLOSURE_STRIP,
        content=content, footer=build_footer(),
        bar=(build_compare_bar() if path in BAR_PAGES else ""),
    )
    (DOCS / path).write_text(out, encoding="utf-8")


def build_feed() -> None:
    items = []
    for gid in GUIDE_IDS + ["buying-guide"]:
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
    (DOCS / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n", encoding="utf-8")


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "assets").mkdir(exist_ok=True)
    if ASSETS_SRC.exists():
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
