"""Data-room pages: dashboard, requirements, decisions, flagged, suggestions,
open questions, metrics, sources. Every row carries a source link; unverifiable
values render as explicit blanks."""
import json
import datetime
from helpers import PRODUCTS, u, official, TAG, VERIFY_DATE  # noqa: F401 (TAG used in sources_body)

DOCS_NAV = [
    ("Dashboard", "/docs/index.html"),
    ("Requirements", "/docs/requirements.html"),
    ("Decisions", "/docs/decisions.html"),
    ("Flagged", "/docs/flagged.html"),
    ("Suggestions", "/docs/suggestions.html"),
    ("Open questions", "/docs/open-questions.html"),
    ("Metrics", "/docs/metrics.html"),
    ("Sources", "/docs/sources.html"),
]


def docs_subnav(current):
    links = "".join(
        f'<a href="{u(href)}" style="text-decoration:none;{"font-weight:700;color:var(--brand-deep);" if label == current else "color:var(--ink-soft);"}">{label}</a>'
        for label, href in DOCS_NAV
    )
    return f'<div style="display:flex;gap:14px;flex-wrap:wrap;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 16px;margin:18px 0 26px;font-size:0.88rem;box-shadow:var(--shadow);">{links}</div>'


def docs_head(kicker, title, lede):
    return f"""<div class="wrap"><section class="page-head" style="padding-bottom:0;">
      <p class="kicker">{kicker}</p>
      <h1 style="font-family:var(--font-display);font-weight:640;font-size:clamp(1.8rem,4vw,2.5rem);margin:0 0 10px;">{title}</h1>
      <p class="lede">{lede}</p>
    </section></div>"""


def _table(headers, rows):
    ths = "".join(f"<th>{h}</th>" for h in headers)
    if isinstance(rows, str):
        body = rows
    else:
        body = "".join(f"<tr>{''.join(f'<td>{c}</td>' for c in row)}</tr>" for row in rows)
    return f'<div class="data-table-wrap"><table class="data"><thead><tr>{ths}</tr></thead><tbody>{body}</tbody></table></div>'


P = {
    "shop": "https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html",
    "policies": "https://affiliate-program.amazon.com/help/operating/policies",
    "agreement": "https://affiliate-program.amazon.com/help/operating/agreement",
    "ftc101": "https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers",
    "ftcend": "https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews",
    "snippet": "https://developers.google.com/search/docs/appearance/snippet",
    "sponsored": "https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links",
    "spam": "https://developers.google.com/search/docs/essentials/spam-policies",
    "helpful": "https://developers.google.com/search/docs/fundamentals/creating-helpful-content",
    "pageexp": "https://developers.google.com/search/docs/appearance/page-experience",
}


def dashboard_body():
    intent_rows = []
    for pid in ["P1", "P2", "P3", "P4", "P5"]:
        pr = PRODUCTS[pid]
        intent_rows.append(
            f'<tr><td><strong>{pid}</strong></td>'
            f'<td><a href="{pr["submitted"]}" rel="nofollow noopener" target="_blank">{pr["submitted"].replace("https://", "")}</a></td>'
            f'<td><code>{pr["submitted"].rsplit("/", 1)[-1]}</code></td>'
            f'<td class="muted">404 (observed {VERIFY_DATE})</td>'
            f'<td><code>{pr["observed_asin"]}</code></td>'
            f"<td>{official(pid)}</td></tr>"
        )
    events_rows = [
        ("E1", "page_view", "any page load", "shipped &mdash; browser queue; endpoint optional"),
        ("E2", "outbound_product_click", "click on any marked Amazon link", "shipped"),
        ("E3", "chooser_completed", "three-question chooser submit", "shipped"),
        ("E4", "article_half_read", "scroll crosses 50% / 100% of article body", "shipped"),
        ("E5", "disclosure_viewed", "disclosure strip enters viewport", "shipped"),
    ]
    return f"""{docs_head("Data room", "The dashboard", "Everything the machinery knows, in one page: what is verified, what is measured, what is open. Reader-facing pages live one click from the masthead; this room is the paper trail.")}
  <div class="wrap">{docs_subnav("Dashboard")}
  <div class="metric-grid" style="margin-bottom:30px;">
    <div class="metric"><div class="m-value">5 / 5</div><div class="m-label">Products verified against official listings</div><div class="m-note">Live fetches dated {VERIFY_DATE}; sources on the <a href="{u('/docs/sources.html')}">source register</a>.</div></div>
    <div class="metric"><div class="m-value">4</div><div class="m-label">Question-shaped guides published</div><div class="m-note"><a href="{u('/guides/index.html')}">Read them</a> &middot; one per week cadence.</div></div>
    <div class="metric"><div class="m-value">0</div><div class="m-label">Campaign ledger rows &mdash; by design</div><div class="m-note">Rows enter only from authorized first-party reports with provenance (<a href="{u('/docs/metrics.html')}">rules</a>).</div></div>
    <div class="metric"><div class="m-value">5</div><div class="m-label">Measurement events shipped</div><div class="m-note">Privacy-preserving; no cookies, no third parties (<a href="{u('/docs/metrics.html')}">spec</a>).</div></div>
    <div class="metric"><div class="m-value">10</div><div class="m-label">Flags tracked</div><div class="m-note"><a href="{u('/docs/flagged.html')}">Flagged for Review</a> &mdash; none block publication.</div></div>
    <div class="metric"><div class="m-value">2</div><div class="m-label">Owner actions open</div><div class="m-note">Search Console (T-10) &amp; Associates console link test (T-09).</div></div>
  </div>

  <div class="section-head"><h2>Executive summary</h2></div>
  <div class="prose" style="max-width:none;">
    <p><strong>What this is.</strong> An Amazon Associates publication (tracking ID <code>{TAG}</code>) built around five
    products whose submitted short links were resolved live to official listings on {VERIFY_DATE}: three air fryers
    (CHEFMAN 6 Qt dual basket, Emeril Lagasse 26 QT french-door oven, Chefman 8 Qt TurboFry) and two meat thermometers
    (ThermoMaven instant-read, CHEF iQ Sense wireless). The site is a publication that reads like a shop: four
    question-shaped guides, a three-question chooser, a five-product comparison, and a product shelf &mdash; with the
    entire verification apparatus reachable from the footer instead of in the reader&rsquo;s face.</p>
    <p><strong>What is verified.</strong> Every product fact shown on reader pages was read from the product&rsquo;s
    official Amazon listing (title, category path) on {VERIFY_DATE}. The submitted ASIN strings do not resolve as
    direct <code>amazon.com/dp/</code> paths (404 observed); the <code>link.amazon</code> short links do resolve, and
    their observed destinations are recorded in a separate field &mdash; never merged with the intended ASIN. The
    compliance status of the short links themselves is <em>unresolved</em> (<a href="{u('/docs/flagged.html')}#F-02">F-02</a>);
    reader-facing links therefore use tagged <code>amazon.com/dp/</code> Special Links built from the observed ASINs.</p>
    <p><strong>What is deliberately blank.</strong> Prices, star ratings, dimensions and warranty terms. Prices and
    ratings change daily (flag F-05); dimensions and warranty have not been verified from official sources (F-04, F-06).
    The capacity-per-centimetre analysis (S-23) publishes its methodology now and its numbers when the inputs verify.</p>
    <p><strong>What is measured.</strong> Five privacy-preserving events (page views, outbound product clicks,
    chooser completions, half-reads, disclosure views) queue locally in the browser; a self-hosted aggregate endpoint
    can be attached later via one config value. No conversion scores, rankings or revenue forecasts exist anywhere in
    this project (decision <a href="{u('/docs/decisions.html')}#D-07">D-07</a>) &mdash; conversion rows enter the
    <a href="https://github.com/wingbangboozle1-lang/Prod2/blob/main/data/ledger.csv" rel="nofollow noopener" target="_blank">campaign ledger</a>
    only from authorized first-party reports with a provenance note.</p>
    <p><strong>What needs a human.</strong> Two owner actions unlock the next stage: verifying the site in Google
    Search Console (T-10) so topic selection switches from instinct to measured queries, and testing one Special Link
    per product in the Associates console (T-09) to confirm destination and tracking reporting before scale. Two
    decisions are reserved for the owner: the brand name (T-11) and the photography policy (T-12) &mdash; both are
    staged on the <a href="{u('/docs/suggestions.html')}">suggestions page</a> with the evidence for each path.</p>
  </div>

  <div class="section-head" style="margin-top:34px;"><h2>Product-intent confirmation record</h2><span class="badge badge-new">intended vs observed &mdash; never merged</span></div>
  {_table(["ID", "Submitted link", "Intended ASIN (as submitted)", "Intended ASIN as direct dp path", "Observed redirect target", "Official listing (source)"], intent_rows)}
  <p class="hero-note">Verification method: live fetch of each submitted short link on {VERIFY_DATE}; the destination
  and listing title were read from the resulting official page. Direct dp paths built from the submitted strings were
  also fetched (404 observed). Machine-readable version:
  <a href="https://github.com/wingbangboozle1-lang/Prod2/blob/main/data/product-intent.json" rel="nofollow noopener" target="_blank">data/product-intent.json</a>.</p>

  <div class="section-head" style="margin-top:34px;"><h2>Event inventory</h2></div>
  {_table(["Event", "Name", "Trigger", "Status"], [list(r) for r in events_rows])}

  <div class="section-head" style="margin-top:34px;"><h2>Campaign ledger</h2><span class="badge badge-warn">empty by design</span></div>
  <div class="empty-note">The ledger (<code>data/ledger.csv</code>) has columns
  <code>timestamp, source, channel, eligible_sessions, clicks, reported_orders, provenance</code> and zero rows.
  A row is written only when an authorized first-party report (Associates console, Search Console) provides the
  numbers, with the exact tool and export date in <code>provenance</code>. No derived scores or forecasts &mdash;
  see <a href="{u('/docs/metrics.html')}">the metrics plan</a> and flag <a href="{u('/docs/flagged.html')}#F-09">F-09</a>.</div>

  <div class="section-head" style="margin-top:34px;"><h2>Recent verification log</h2></div>
  {_table(["When (UTC)", "What was verified", "Result"], [
      [f"{VERIFY_DATE} 12:45", "<code>amazon.com/dp/B04G1MEwY</code> (submitted ASIN as direct path)", "404 &mdash; page not found (observed)"],
      [f"{VERIFY_DATE} 12:50", "<code>link.amazon/B04G1MEwY</code> &rarr; official listing B0CDY277D3", "Resolved; CHEFMAN 6 Qt dual basket; Air Fryers node"],
      [f"{VERIFY_DATE} 12:50", "<code>link.amazon/B02NbDxp3</code> &rarr; B09B7SB46R", "Resolved; Emeril Lagasse 26QT; Air Fryers node"],
      [f"{VERIFY_DATE} 12:51", "<code>link.amazon/B00hJ57DV</code> &rarr; B08DKYBTPH", "Resolved; Chefman 8 Qt TurboFry; Air Fryers node"],
      [f"{VERIFY_DATE} 12:51", "<code>link.amazon/B0c8moW59</code> &rarr; B0DHZTCNR5", "Resolved; ThermoMaven instant-read; Meat Thermometers node"],
      [f"{VERIFY_DATE} 12:51", "<code>link.amazon/B0f3GKalj</code> &rarr; B0DZFD6R9Z", "Resolved; CHEF iQ Sense wireless; Meat Thermometers node"],
      [f"{VERIFY_DATE} 12:55", "Associates Program Policies page", "Live; Special Link framework read verbatim"],
  ])}
  </div>"""


def requirements_body():
    rows = [
        ("R-01", "P1", "Turn a careful source register into a page a buyer can act on &mdash; read like a shop, not an audit.", "Implemented", "Front page is publication-first; data room reachable from footer.", P["helpful"]),
        ("R-02", "P1", "Make it findable: one indexable site with a reason to rank.", "Implemented", "Sitemap, feed, canonicals, robots, unique titles; Search Console pending owner (T-10).", P["snippet"]),
        ("R-03", "P1", "Automate what can be automated; gate what cannot.", "Implemented", "build.py + check.py + CI gate; PA-API automation deferred until enrollment qualifies (F-03).", P["policies"]),
        ("R-04", "P1", "Read like a publication: authorship, navigation, brand, imagery, seasons, clusters (SG-27..SG-30).", "Implemented", "Nav labels shipped; RSS shipped; Search Console pending (T-10); reader capture = E1/E4 events + cadence.", P["helpful"]),
        ("R-05", "P1", "Lead with products, not the verification process.", "Implemented", "Hero, guides and chooser first; verification one footer-click deep.", P["helpful"]),
        ("R-06", "P1", "Publish question-shaped guides; measure arrivals before choosing the next topic.", "Partly", "Four guides live on the suggested hypotheses; arrival measurement blocked on Search Console (F-07).", P["spam"]),
        ("R-07", "P0", "Turn on click and conversion measurement before writing anything else.", "Implemented", "Five events shipped with the first build; ledger contract defined; endpoint optional.", P["policies"]),
        ("R-08", "P0", "Disclosure above the fold on every page, repeated in footer.", "Implemented", "Strip renders on all 20 pages including the data room; asserted by check.py.", P["ftc101"]),
        ("R-09", "P0", "Every outbound product link marked as sponsored.", "Implemented", "rel=\"sponsored nofollow noopener\" + tracking ID on all outbound Amazon links; asserted by check.py.", P["sponsored"]),
        ("R-10", "P0", "Product-intent confirmation record: intended ASIN, official URL, confirmation date, source; observed redirects in a separate field.", "Implemented", "data/product-intent.json + dashboard table; fields never merged.", P["agreement"]),
        ("R-11", "P0", "Replace ambiguous outbound links with validated Special Links; test one per product before scaling.", "Partly", "Tagged dp Special Links shipped; per-product console test pending (T-09); no claim made about short-link validity (F-02).", P["policies"]),
        ("R-12", "P2", "Lead with useful, human-sounding buyer questions.", "Implemented", "Four guides built from the suggested editorial hypotheses; titles are working titles, not popularity claims.", P["helpful"]),
        ("R-13", "P4", "Measure before automating optimization; empty but well-defined ledger with provenance.", "Implemented", "Ledger schema + rules shipped empty; no conversion score or forecast presented.", P["policies"]),
        ("R-14", "P5", "Disclosures and API policy checks in the publishing workflow.", "Implemented", "check.py gates disclosure + sponsored marking before deploy; endorsement-context review checklist in ENGINE.md.", P["ftcend"]),
        ("S-04", "P1", "Give every page its own title and meta description.", "Implemented", "check.py fails the build on duplicates or blanks.", P["snippet"]),
        ("S-05", "P2", "Mark affiliate links rel=\"sponsored\" without breaking the disclosure.", "Implemented", "Shipped site-wide; see decision D-04.", P["sponsored"]),
        ("S-06", "P2", "Add what the appliance is like to live with.", "Implemented", "The cleanup &amp; counter-space guide is that content (D-06).", P["spam"]),
        ("S-07", "P2", "Answer the questions people actually type, one page per question.", "Partly", "Four question pages live; measured-queries loop pending T-10.", P["helpful"]),
        ("S-09", "P2", "Ship social preview + structured data, then measure arrival.", "Partly", "OG/Twitter cards + JSON-LD shipped; traffic measurement pending T-10.", P["pageexp"]),
        ("S-10", "P3", "Documentation in line with code; every published check runs from a clean checkout.", "Implemented", "ENGINE.md mirrors build.py/check.py; CI runs both on every push.", P["helpful"]),
        ("S-11", "P3", "Fix flag cross-references; split open/resolved/historical items.", "Implemented", "Flag page has the three sections; check.py verifies every referenced flag ID exists.", P["helpful"]),
        ("S-12", "P2", "Decide the voice; rewrite articles to it.", "Implemented", "D-12 voice shipped; four guides written in it.", P["helpful"]),
        ("S-13", "P2", "Approve a format-first topic calendar of catchy, spec-backed articles.", "Partly", "Calendar shipped with three working titles; approval is an owner decision.", P["helpful"]),
        ("S-14", "P2", "Adopt the design-prompt draft as the visual overhaul brief.", "Implemented", "DESIGN_PROMPT.md committed and adopted (D-14/D-20).", P["helpful"]),
        ("S-15", "P2", "Choose the visual direction and settle the brand name.", "Partly", "Direction shipped (Warm Counter Editorial); brand name provisional pending T-11.", P["helpful"]),
        ("S-16", "P2", "Written evidence rule for trending/popularity claims.", "Implemented", "D-19: dated snapshot link or silence; enforced in voice and disclosure page.", P["helpful"]),
        ("S-17", "P2", "Rebuild the front page as an editorial homepage.", "Implemented", "Hero &rarr; featured guides &rarr; tools &rarr; glance &rarr; trust (D-13).", P["helpful"]),
        ("S-18", "P2", "Add real product photography; never generated or copied photography.", "Needs decision", "No product imagery shipped; illustrations only (D-15); owner decision T-12.", P["agreement"]),
        ("S-19", "P2", "Three-question chooser above the comparison table.", "Implemented", "Shipped on compare.html; completion measured as event E3.", P["helpful"]),
        ("S-20", "P2", "Mobile-first pass: type scale, tap targets, sticky comparison bar.", "Partly", "Shipped (clamp scale, 44px targets, sticky bars); Lighthouse audit pending live deploy.", P["pageexp"]),
        ("S-23", "P2", "Publish the counter-space analysis: capacity per cm of counter depth.", "Partly", "Methodology published; numbers blank until dimensions verify (F-04).", P["helpful"]),
        ("S-24", "P2", "Every article reaches the comparison, the buying guide and its category pillar.", "Implemented", "Enforced by check.py internal-link rules.", P["policies"]),
        ("S-25", "P3", "Grow organic traffic on the verification angle, not on volume.", "Open", "Blocked on analytics (F-07); angle strategy drafted on the suggestions page.", P["helpful"]),
    ]
    rendered = [
        f'<tr><td><strong>{i}</strong></td><td><span class="badge">{prio}</span></td><td>{req}</td>'
        f'<td><span class="status-pill status-{"done" if s == "Implemented" else ("flag" if s in ("Partly", "Open") else "open")}">{s}</span></td>'
        f"<td>{note}</td><td><a class=\"src-chip\" href=\"{src}\" rel=\"nofollow noopener\" target=\"_blank\">source ↗</a></td></tr>"
        for i, prio, req, s, note, src in rows
    ]
    return f"""{docs_head("Requirements register", "Full list of requirements", "Every requirement from the project register, its priority, and what this build does about it. Implemented does not mean measured &mdash; measurement status is honest and separate.")}
  <div class="wrap">{docs_subnav("Requirements")}
  {_table(["ID", "Priority", "Requirement", "Status", "What this build does", "Source"], rendered)}
  <p class="hero-note">Statuses reflect this repository&rsquo;s build of {VERIFY_DATE}. Prior-session registers
  (Zone2/Zone3/Zone4) recorded parallel work on other sites; nothing here repeats those claims &mdash; each row was
  implemented and checked in <em>this</em> codebase.</p>
  </div>"""


def decisions_body():
    rows = [
        ("D-01", VERIFY_DATE, "Intended ASIN and observed redirect target are recorded in separate fields, never merged.", "Product-intent record requirement; a merged field would launder an unverified identity into a fact.", "Adopted", "Official listings fetched live"),
        ("D-02", VERIFY_DATE, f"Tracking ID <code>{TAG}</code> applied to every outbound Amazon link site-wide.", "Associates attribution requires the tag on all links we intend to monetize.", "Adopted", "<a href='https://affiliate-program.amazon.com/help/operating/policies' rel='nofollow noopener' target='_blank'>Program Policies</a>"),
        ("D-03", VERIFY_DATE, "Disclosure strip above the fold on every page, repeated in footer.", "FTC clear-and-conspicuous placement; Associates statement requirement.", "Adopted", "<a href='https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers' rel='nofollow noopener' target='_blank'>FTC Disclosures 101</a>"),
        ("D-04", VERIFY_DATE, "rel=\"sponsored nofollow noopener\" on all outbound Amazon links.", "Machine-readable paid-link marking that coexists with the visible disclosure.", "Adopted", "<a href='https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links' rel='nofollow noopener' target='_blank'>Google: qualify outbound links</a>"),
        ("D-05", VERIFY_DATE, "Reader-facing links use tagged amazon.com/dp/ Special Links built from observed ASINs; submitted short links are not used for readers until their compliance status resolves.", "The short links resolve (observed live) but their policy status is unresolved; readers get links built from listings we have actually read.", "Adopted", "<a href='https://affiliate-program.amazon.com/help/operating/policies' rel='nofollow noopener' target='_blank'>Special Link requirements</a>"),
        ("D-06", VERIFY_DATE, "S-06 adopted: the cleanup &amp; counter-space guide is the &lsquo;what it is like to live with&rsquo; content.", "Listing specs cannot carry lived-in judgment; Google&rsquo;s thin-affiliation guidance asks for meaningful content.", "Adopted", "<a href='https://developers.google.com/search/docs/essentials/spam-policies' rel='nofollow noopener' target='_blank'>Google: spam policies</a>"),
        ("D-07", VERIFY_DATE, "Conversion facts enter the ledger only from authorized first-party reports with a provenance string; no scores, rankings or forecasts are derived.", "Analytics must be evidence before optimization; fabricated baselines poison every later decision.", "Adopted", "<a href='https://affiliate-program.amazon.com/help/operating/policies' rel='nofollow noopener' target='_blank'>Associates reporting</a>"),
        ("D-08", VERIFY_DATE, "Five events (E1&ndash;E5) shipped; privacy-preserving by construction; endpoint optional via one config value.", "Measurement before content decisions; privacy as a design constraint, not a policy page.", "Adopted", "data/events.schema.json"),
        ("D-09", VERIFY_DATE, "Prices and ratings are never published as stable facts; cells stay blank with a flag.", "Both change daily; a copied number is a defect the day after publish.", "Adopted", "Observed dynamic values on listings"),
        ("D-10", VERIFY_DATE, "Dimensions and warranty terms blank until verified from official sources; S-23 methodology published ahead of its numbers.", "Verification-before-values rule; methodology transparency keeps the eventual table checkable.", "Adopted", "Listing spec tables pending fetch"),
        ("D-11", VERIFY_DATE, "Brand name provisional: &lsquo;The Counter Edit&rsquo;.", "A name is an owner-level decision (T-11); the build needs a consistent placeholder that survives replacement.", "Open &mdash; owner decision", "Suggestions page"),
        ("D-12", VERIFY_DATE, "Voice: plain-spoken, source-first, labeled opinions; guides written to it once, deliberately.", "A consistent voice is the difference between a publication and a content farm.", "Adopted", "<a href='https://developers.google.com/search/docs/fundamentals/creating-helpful-content' rel='nofollow noopener' target='_blank'>Google: people-first content</a>"),
        ("D-13", VERIFY_DATE, "Front page rebuilt as editorial homepage: hero, featured guides, tools, glance table, trust strip.", "Products lead; verification is one footer-click deep.", "Adopted", "site/index.html"),
        ("D-14", VERIFY_DATE, "Visual direction &lsquo;Warm Counter Editorial&rsquo; (cream ground, paprika ink, Fraunces + Inter), implemented from the adopted design brief.", "A decided direction prevents per-page style drift.", "Adopted", "DESIGN_PROMPT.md"),
        ("D-15", VERIFY_DATE, "Illustration-only imagery, labeled as illustration; no generated or copied product photography (photography policy decision recorded as <strong id=\"D-22\">D-22</strong>).", "Program Content rules and the S-18 decision make photography an owner call; illustrations are safe and ownable.", "Adopted &mdash; pending T-12", "<a href='https://affiliate-program.amazon.com/help/operating/agreement' rel='nofollow noopener' target='_blank'>Operating Agreement (Program Content)</a>"),
        ("D-16", VERIFY_DATE, "One page per question; four guides built from the suggested hypotheses; titles carry no popularity claim.", "Question-shaped content matches buyer intent without pretending to keyword data we do not have.", "Adopted", "<a href='https://developers.google.com/search/docs/fundamentals/creating-helpful-content' rel='nofollow noopener' target='_blank'>Google: people-first content</a>"),
        ("D-17", VERIFY_DATE, "Publishing cadence: one guide per week (Tuesday); each new guide enters sitemap and feed the day it publishes.", "Cadence is a promise to readers and a measurable habit for the desk.", "Adopted", "rss.xml / sitemap.xml"),
        ("D-18", VERIFY_DATE, "Internal-linking rule: every guide links the comparison, the capacity pillar, the shelf and the category hub; enforced by check.py.", "S-24 compliance becomes a machine-checked invariant instead of a memory task.", "Adopted", "scripts/check.py"),
        ("D-19", VERIFY_DATE, "Evidence rule for trending/popularity claims: a dated link to the snapshot that showed it, or silence.", "Unverifiable popularity claims are a compliance and trust hazard.", "Adopted", "disclosure.html"),
        ("D-20", VERIFY_DATE, "Publishing workflow gates: build &rarr; check (titles, sponsored rel, disclosure, link integrity, flag cross-refs) &rarr; deploy; human endorsement-context review checklist in ENGINE.md.", "Automate the checkable, gate the judgment.", "Adopted", "ENGINE.md"),
        ("D-22", VERIFY_DATE, "Photography policy (S-18): no product photography until the owner picks a rights-safe path; illustration-only until then.", "Program Content includes images; generated or copied photography risks a policy breach and misleads readers.", "Open &mdash; owner decision T-12", "<a href='https://affiliate-program.amazon.com/help/operating/agreement' rel='nofollow noopener' target='_blank'>Operating Agreement (Program Content)</a>"),
    ]
    rendered = "".join(
        f'<tr><td><strong id="{did}">{did}</strong></td><td>{dt}</td><td>{dec}</td><td>{why}</td>'
        f'<td><span class="status-pill status-{"done" if st.startswith("Adopted") else "open"}">{st}</span></td><td>{src}</td></tr>'
        for did, dt, dec, why, st, src in rows
    )
    return f"""{docs_head("Decision log", "Decisions", "Every structural decision, its rationale, and its status. The gate rule: suggestions are reviewed here before code changes &mdash; not after.")}
  <div class="wrap">{docs_subnav("Decisions")}
  {_table(["ID", "Date", "Decision", "Rationale", "Status", "Source"], rendered)}
  </div>"""


def flagged_body():
    open_flags = [
        ("F-01", "No conversion scores or forecasts exist anywhere in the project.", "Informational", "The measurement plan forbids derived scores until authorized first-party data exists.", "Unblocks itself: first authorized report writes the first ledger row.", "<a href='https://affiliate-program.amazon.com/help/operating/policies' rel='nofollow noopener' target='_blank'>Associates reporting</a>"),
        ("F-02", "Compliance status of the submitted <code>link.amazon</code> short links is unresolved.", "High", "All five resolve live to official listings (observed 2026-11-19), but no policy source consulted confirms or denies their validity as Special Links. No claim is made either way. Reader-facing links use tagged dp Special Links instead.", "Owner tests one link per product in the Associates console and confirms destination + tracking report (T-09).", "<a href='https://affiliate-program.amazon.com/help/operating/policies' rel='nofollow noopener' target='_blank'>Participation Requirements</a>"),
        ("F-03", "PA-API automation not yet possible for this account stage.", "Medium", "Product data was verified by live fetches with dates instead. No fabricated API fields appear anywhere.", "Enrollment qualifies after sales; then automate price/availability refresh.", "<a href='https://affiliate-program.amazon.com/help/operating/policies' rel='nofollow noopener' target='_blank'>PA-API policy</a>"),
        ("F-04", "Product dimensions unverified &mdash; blank cells where numbers would normally go.", "Medium", "Listing spec tables were not part of the verified fetch set.", "Verification session against official listing spec sheets; then S-23 table publishes.", "Official listing pages"),
        ("F-05", "Prices and ratings deliberately absent.", "Informational", "Dynamic values; publishing them creates same-day defects.", "Permanent policy (D-09); no action expected.", "<a href='https://affiliate-program.amazon.com/help/operating/policies' rel='nofollow noopener' target='_blank'>Associates policies</a>"),
        ("F-06", "Warranty terms unverified &mdash; blank in comparison.", "Low", "Manufacturer warranty pages not yet fetched.", "Fetch + verify; then fill the column.", "Manufacturer sites (pending)"),
        ("F-07", "Search Console not yet verified; arrival measurement blocked.", "High", "The meta-tag/DNS token requires site-owner action.", "Owner verifies property (T-10); then measured-query loop starts.", "<a href='https://search.google.com/search-console' rel='nofollow noopener' target='_blank'>Google Search Console</a>"),
        ("F-08", "No named human author yet.", "Low", "Desk byline used; no invented person.", "Owner assigns a real editor; bio + byline then ship.", "About page"),
        ("F-09", "Campaign ledger empty by design.", "Informational", "Rows require authorized first-party provenance.", "First report arrives with provenance; row enters.", "data/ledger.csv"),
        ("F-10", "Live price/availability pipeline absent.", "Medium", "Requires PA-API or approved automation (F-03).", "After enrollment; never scraped client-side.", "<a href='https://affiliate-program.amazon.com/help/operating/policies' rel='nofollow noopener' target='_blank'>PA-API policy</a>"),
    ]
    resolved_flags = [
        ("F-20", "Thin-affiliation risk (ex-flag F-11/F-31 class).", "Resolved 2026-11-19", "Four original guides with editorial voice and lived-in content shipped (D-06, D-12, D-16).", "<a href='https://developers.google.com/search/docs/essentials/spam-policies' rel='nofollow noopener' target='_blank'>Google: spam policies</a>"),
        ("F-21", "Front-page audit-dump risk (ex-flag F-46 class).", "Resolved 2026-11-19", "Editorial homepage rebuilt; data room moved behind footer (D-13).", "site/index.html"),
        ("F-22", "Flag cross-reference integrity (ex-flag F-29/F-35 class).", "Resolved 2026-11-19", "check.py now fails the build if any F-xx/D-xx reference points to an ID that does not exist.", "scripts/check.py"),
    ]
    historical_flags = [
        ("F-90", "Parallel-session registers (Zone2/Zone3/Zone4) describe work on other sites with overlapping item numbers.", "Archived", "Kept as historical context only. This repo&rsquo;s registers were rebuilt from its own verification; item IDs here do not map 1:1 to prior sites.", "COORDINATION.md"),
    ]
    def render(fs, status_cls):
        out = ""
        for entry in fs:
            fid, title, sev, body, src = entry[0], entry[1], entry[2], entry[3], entry[-1]
            unblock = entry[4] if len(entry) == 6 else ""
            out += f'<div class="flag" id="{fid}"><h3>{fid} &mdash; {title}</h3><p>{body}</p>'
            if unblock:
                out += f'<p><strong>What would resolve it:</strong> {unblock}</p>'
            out += f'<div class="f-meta"><span class="status-pill status-{status_cls}">{sev}</span> &nbsp; {src}</div></div>'
        return out
    return f"""{docs_head("Flagged for review", "Flagged for Review", "Open items first, resolved items for context, historical items for the record. Flags do not block publication &mdash; they are the honest boundary of what this build verified.")}
  <div class="wrap">{docs_subnav("Flagged")}
  <div class="section-head"><h2>Open</h2><span class="badge badge-warn">10 open</span></div>
  {render(open_flags, "flag")}
  <div class="section-head" style="margin-top:30px;"><h2>Resolved</h2></div>
  {render(resolved_flags, "done")}
  <div class="section-head" style="margin-top:30px;"><h2>Historical</h2></div>
  {render(historical_flags, "open")}
  </div>"""


def suggestions_body():
    cards = [
        ("SG-01", "Verify the five listing spec sheets, then publish the capacity-per-cm table", "Unblocks S-23 with real inputs and turns a blank into the site&rsquo;s most checkable original analysis.", "Effort: one verification session (fetch 5 spec tables). Risk: low. Evidence: methodology already published.", "Decision: approve the verification session (no owner input needed beyond go-ahead).", "Open for review"),
        ("SG-02", "Brand name: keep &lsquo;The Counter Edit&rsquo; or pick from alternatives", "Alternatives: &lsquo;The Counter Test&rsquo;, &lsquo;Crisp &amp; Counter&rsquo;, &lsquo;Two Baskets&rsquo;. A name that survives scale matters before more content ships.", "Effort: zero until chosen (build.py single source of truth). Risk: renaming after indexation.", "Decision: owner picks (T-11) &mdash; one-line answer.", "Owner decision &mdash; T-11"),
        ("SG-03", "Photography policy (S-18/D-22): license CC0 kitchen photography, request manufacturer images, or stay illustration-only", "Illustrations are shipped and labeled; real product photography would raise trust but requires rights diligence (Program Content rules).", "Effort: low (CC0) / medium (permissions). Risk: rights errors are a policy breach.", "Decision: owner picks a path (T-12). Default if unanswered: illustration-only.", "Owner decision &mdash; T-12"),
        ("SG-04", "Search Console verification, then a weekly measured-query review that feeds the topic calendar", "Switches topic selection from instinct to measured queries (the S-07 loop).", "Effort: owner verifies property once; desk reviews weekly. Risk: none.", "Decision: owner action (T-10).", "Owner action &mdash; T-10"),
        ("SG-05", "Associates console test: one Special Link per product, confirm destination + tracking", "The single fastest compliance win; resolves F-02 or documents its scope.", "Effort: minutes in the console. Risk: none.", "Decision: owner action (T-09).", "Owner action &mdash; T-09"),
        ("SG-06", "Extend structured data: FAQPage on guides matching visible questions", "Complements shipped Article/ItemList JSON-LD. Must mirror visible content exactly or risk manual-action penalty.", "Effort: low. Risk: medium if mismatched.", "Decision: approve with rule &lsquo;FAQ markup only where the guide visibly asks and answers the question&rsquo;.", "Open for review"),
        ("SG-07", "Reader capture: privacy-preserving newsletter vs RSS-first", "SG-30 without trackers: a self-hosted aggregate subscribe box, or promote RSS and skip email entirely.", "Effort: medium (self-host) / zero (RSS-first). Risk: email vendor = third-party dependency.", "Decision: pick RSS-first (recommended default) or approve a provider.", "Open for review"),
        ("SG-08", "Add a monthly &lsquo;Counter Notes&rsquo; short post format", "Keeps the weekly cadence honest when no guide is ready; dated snapshots of verified facts (fits D-19).", "Effort: low. Risk: dilutes cluster depth if overused.", "Decision: approve as format or keep guides-only.", "Open for review"),
        ("SG-09", "Seasonal refresh calendar (January reset &middot; September back-to-routine &middot; November gift-doneness angle)", "Seasons requirement; refreshes existing guides rather than spawning thin new pages.", "Effort: low. Risk: none.", "Decision: approve calendar dates.", "Open for review"),
        ("SG-10", "Per-claim verification dates (upgrade from page-level &lsquo;verified {VERIFY_DATE}&rsquo;)", "Prevents a single stale date laundering old facts; each fact carries its own fetch date.", "Effort: medium (data model change). Risk: none.", "Decision: approve before the first content refresh, not after.", "Open for review"),
    ]
    rendered = "".join(
        f'<div class="suggestion"><h3>{sid} &mdash; {title}</h3><p>{what}</p><p>{ev}</p>'
        f'<p><strong>Decision needed:</strong> {dec}</p>'
        f'<div class="s-meta"><span class="status-pill status-{"open" if "Owner" in st else "flag"}">{st}</span></div></div>'
        for sid, title, what, ev, dec, st in cards
    )
    paths = f"""
<div class="tile" style="border-left:5px solid var(--brand);"><h3>Path A &mdash; Depth first (recommended default)</h3>
<p>Verify spec sheets (SG-01), fill S-23, extend structured data (SG-06), keep cadence. Traffic follows the
verification angle once Search Console lands. Nothing new ships until F-04 resolves.</p></div>
<div class="tile" style="border-left:5px solid var(--gold);"><h3>Path B &mdash; Reach first</h3>
<p>Prioritize Search Console + newsletter (SG-04, SG-07) and publish two more guides before filling blanks.
Faster top-line growth; leaves visible blanks for another cycle.</p></div>
<div class="tile" style="border-left:5px solid var(--accent);"><h3>Path C &mdash; Trust first</h3>
<p>Resolve F-02 (SG-05) and D-22 photography before any new content. Slowest; makes every later page
unimpeachable.</p></div>"""
    return f"""{docs_head("Suggestions &amp; direction", "Suggestions", "A dedicated review surface: every proposal sits here with evidence, effort and risk until a decision is recorded in the decision log. Nothing below has been implemented; choosing is the whole point of this page.")}
  <div class="wrap">{docs_subnav("Suggestions")}
  <div class="section-head"><h2>How to use this page</h2></div>
  <div class="prose" style="max-width:none;"><p>Review the suggestion cards, pick the best path below, and record the
  choice in <a href="{u('/docs/decisions.html')}">the decision log</a>. &lsquo;Owner decision&rsquo; cards cannot be
  implemented by any session &mdash; they are deliberately gated. Questions the owner will likely ask are pre-answered
  on the <a href="{u('/docs/open-questions.html')}">open questions page</a>.</p></div>
  <div class="section-head" style="margin-top:26px;"><h2>Suggestion cards</h2></div>
  {rendered}
  <div class="section-head" style="margin-top:26px;"><h2>Three paths, one choice</h2></div>
  <div class="grid grid-3">{paths}</div>
  </div>"""


def open_questions_body():
    qa = [
        ("Q-01", "Are the five submitted short links compliant as Special Links?", "Unresolved. They resolve live to official listings (observed 2026-11-19), but no consulted policy text confirms their validity. Reader links use tagged dp Special Links; owner console test (T-09) settles it.", "Open &mdash; needs owner action"),
        ("Q-02", "What are the dimensions of each product?", "Not verified. Listing spec tables were not in the verified fetch set. Blank cells everywhere; verification session proposed as SG-01.", "Open"),
        ("Q-03", "What do the products cost?", "Deliberately unpublished. Prices change daily; publishing them creates same-day defects (D-09).", "Answered &mdash; policy"),
        ("Q-04", "Who owns the byline?", "No invented person. Desk byline until a real editor is assigned (F-08).", "Open &mdash; owner decision"),
        ("Q-05", "What is the commission rate per product?", "Not published. The fee schedule must be read in the Associates console by the account holder; rates are category-dependent and account-specific.", "Open &mdash; needs owner data"),
        ("Q-06", "Is the brand name final?", "Provisional: The Counter Edit. Owner decision T-11; build.py single source of truth makes renaming a one-line change.", "Open &mdash; owner decision"),
        ("Q-07", "Can we show live prices from Amazon?", "Not yet. PA-API requires enrollment with qualifying sales (F-03). Until then, no price display at all &mdash; no client-side scraping.", "Answered &mdash; blocked on enrollment"),
        ("Q-08", "Do we have permission for product photography?", "No photographs used. Illustration-only until D-22 path is chosen (T-12).", "Open &mdash; owner decision"),
        ("Q-09", "What analytics endpoint will we use?", "None yet. Events queue in-browser; window.TCE_ENDPOINT attaches a self-hosted, aggregate-only collector when the owner provides one.", "Open"),
        ("Q-10", "How will organic traffic be measured?", "Search Console (pending T-10) + event E1 page views. Nothing measured yet by design &mdash; no synthetic baselines (F-07).", "Open &mdash; blocked on T-10"),
        ("Q-11", "Which products convert best?", "Unknown, and unknowable until authorized first-party reports exist (D-07, F-09). No scores are presented.", "Answered &mdash; by design"),
        ("Q-12", "What topic is next?", "Working titles on the guides page; final choice switches to measured queries once Q-10 resolves.", "Open"),
        ("Q-13", "Are manufacturer claims like &lsquo;1-second read&rsquo; independently tested?", "No. Facts shown are listing-stated and dated. Independent testing is proposed as a future editorial format &mdash; it must be honest about being our own tests.", "Open &mdash; editorial decision"),
        ("Q-14", "Do guides include recipes or how-to cookware content?", "Not yet. Proposed as &lsquo;Counter Notes&rsquo; (SG-08); kept out of buying guides to preserve question-shaped intent.", "Open &mdash; review"),
        ("Q-15", "Is there an email capture?", "Not yet. SG-07 stages the privacy-preserving options; RSS exists today.", "Open &mdash; review"),
        ("Q-16", "What happens when a listed product is discontinued?", "Shelf cards carry the verified date; a dead listing link is a build-time check failure, forcing review rather than silent deletion.", "Answered &mdash; process"),
        ("Q-17", "How are corrections handled?", "Corrections ship with a note in the flagged page&rsquo;s resolved section; the RSS feed announces material changes.", "Answered &mdash; process"),
        ("Q-18", "What is the publishing cadence?", "One guide per week, Tuesdays (D-17). New guides enter sitemap + feed the day they publish.", "Answered"),
        ("Q-19", "Is the comparison table sortable?", "Not yet; mobile-first sticky table shipped. Sortable columns proposed after Lighthouse baseline (S-20 note).", "Open &mdash; low priority"),
        ("Q-20", "Who deploys and how often?", "GitHub Actions on every push to main (deploy-pages.yml); check.py gates the deploy. Site rebuilds on content change.", "Answered"),
    ]
    rendered = "".join(
        f'<div class="qa-item"><p class="qq">{qid} &mdash; {q}</p><p class="qa-ans">{a}</p>'
        f'<p class="qa-status"><span class="status-pill status-{"done" if st.startswith("Answered") else "open"}">{st}</span></p></div>'
        for qid, q, a, st in qa
    )
    return f"""{docs_head("Open questions", "Open questions &mdash; and the answers we have", "The decision gate needs inputs. This is the question list a reviewer can work through, with our current best answer and its status.")}
  <div class="wrap">{docs_subnav("Open questions")}
  {rendered}
  </div>"""


def metrics_body():
    return f"""{docs_head("Measurement", "The metrics plan", "Five events, one empty ledger, strict provenance rules, and a permanent ban on invented baselines.")}
  <div class="wrap">{docs_subnav("Metrics")}
  <div class="prose" style="max-width:none;">
  <div class="section-head"><h2>The five events</h2></div>
  {_table(["Event", "Name", "Trigger", "Payload", "Feeds"], [
      ["E1", "page_view", "any page load", "path, same-origin referrer", "arrival measurement per page"],
      ["E2", "outbound_product_click", "click on a marked Amazon link", "product id, position, host, page", "ledger &lsquo;clicks&rsquo; column per product"],
      ["E3", "chooser_completed", "chooser submit", "answers, recommendation", "which buyer paths are taken"],
      ["E4", "article_half_read", "scroll crosses 50% / 100%", "guide path, depth bucket", "arrivals vs actual readers"],
      ["E5", "disclosure_viewed", "disclosure enters viewport", "path", "FTC clear-and-conspicuous evidence"],
  ])}
  <p>Implementation: <code>site/assets/js/tce.js</code>. Events queue in <code>localStorage</code> (last 200)
  and beacon only to a self-hosted endpoint set via <code>window.TCE_ENDPOINT</code> &mdash; unset by default, so
  nothing leaves the browser today. No cookies, no third-party scripts, no identifiers.</p>

  <div class="section-head" style="margin-top:30px;"><h2>Ledger rules</h2></div>
  <ol>
    <li>One row per authorized first-party report; the report tool and export date go in <code>provenance</code>.</li>
    <li>Rows without provenance are invalid and must be removed.</li>
    <li><code>clicks</code> may be reconciled against E2 aggregates; <code>reported_orders</code> comes only from the Associates console.</li>
    <li>No conversion score, ranking or revenue forecast is derived &mdash; ever (<a href="{u('/docs/decisions.html')}#D-07">D-07</a>).</li>
  </ol>

  <div class="section-head" style="margin-top:30px;"><h2>Why the ledger starts empty</h2></div>
  <p>Because every number in it must be authorized and provenanced. An empty, well-defined ledger is honest; a
  seeded one is fiction that later optimization will trust. The first row arrives with the first real report.</p>

  <div class="section-head" style="margin-top:30px;"><h2>Search Console loop (once T-10 lands)</h2></div>
  <p>Weekly: export measured queries &rarr; log with provenance &rarr; compare against the working calendar &rarr;
  next guide topic follows the strongest measured question, recorded in the decision log. Instinct retires.</p>
  </div>
  </div>"""


def sources_body():
    with open("data/sources.json", "r", encoding="utf-8") as f:
        reg = json.load(f)
    rows = []
    kind_label = {"O": "Official policy / search guidance", "L": "Official product listing", "P": "Project record"}
    for s in reg["sources"]:
        url = s["url"]
        is_product = "amazon.com/dp/" in url
        if is_product:
            href = f"{url}{'&' if '?' in url else '?'}tag={TAG}"
            attrs = 'rel="sponsored nofollow noopener" target="_blank" data-outbound data-position="source_register"'
        else:
            href = url
            attrs = 'rel="nofollow noopener" target="_blank"'
        rows.append(
            f'<tr><td><strong>{s["id"]}</strong></td><td>{kind_label.get(s["kind"], s["kind"])}</td>'
            f"<td>{s['title']}</td>"
            f'<td><a href="{href}" {attrs}>{url.replace("https://", "").replace("http://", "")}</a></td>'
            f"<td>{s.get('verified_live', '&mdash;')}</td><td>{s.get('used_for', '')}</td></tr>"
        )
    return f"""{docs_head("Sources", "Source register", "Every claim on this site resolves to one of these sources. Official sources are the only kind used for product facts and policy statements.")}
  <div class="wrap">{docs_subnav("Sources")}
  {_table(["ID", "Kind", "Title", "URL", "Verified", "Used for"], rows)}
  <div class="section-head" style="margin-top:30px;"><h2>Verification method</h2></div>
  <div class="prose" style="max-width:none;">
  <p>Product facts: live fetch of each submitted short link and the resulting official listing page on {VERIFY_DATE};
  title, breadcrumb and category node read from the page itself. Submitted ASIN strings were additionally fetched as
  direct <code>amazon.com/dp/</code> paths (404 observed) so the intended-vs-observed distinction is documented, not
  assumed. Policy sources: the Associates Program Policies page was fetched live; other official pages were supplied
  in the task register and are cited by their official URLs for manual review.</p>
  <p><strong>Manual review links:</strong>
  <a href="https://affiliate-program.amazon.com/help/operating/policies" rel="nofollow noopener" target="_blank">Associates Program Policies</a> &middot;
  <a href="https://affiliate-program.amazon.com/help/operating/agreement" rel="nofollow noopener" target="_blank">Operating Agreement</a> &middot;
  <a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers" rel="nofollow noopener" target="_blank">FTC Disclosures 101</a> &middot;
  <a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews" rel="nofollow noopener" target="_blank">FTC Endorsements</a> &middot;
  <a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="nofollow noopener" target="_blank">Google rel=sponsored</a></p>
  </div>
  </div>"""


def pages() -> dict:
    return {
        "/docs/index.html": (
            "home",
            "Dashboard \u2014 The Counter Edit data room",
            "The full picture: product-intent record, event inventory, campaign ledger status and the verification log.",
            dashboard_body(),
        ),
        "/docs/requirements.html": (
            "home",
            "Requirements register \u2014 The Counter Edit",
            "Every project requirement with priority, implementation status and source.",
            requirements_body(),
        ),
        "/docs/decisions.html": (
            "home",
            "Decision log \u2014 The Counter Edit",
            "Twenty structural decisions with rationale and status; the gate before implementation.",
            decisions_body(),
        ),
        "/docs/flagged.html": (
            "home",
            "Flagged for Review \u2014 The Counter Edit",
            "Open, resolved and historical flags: what this build verified, and the honest boundary of what it did not.",
            flagged_body(),
        ),
        "/docs/suggestions.html": (
            "home",
            "Suggestions \u2014 The Counter Edit direction page",
            "Ten suggestion cards with evidence, effort and risk, three paths, and the owner decisions that gate them.",
            suggestions_body(),
        ),
        "/docs/open-questions.html": (
            "home",
            "Open questions \u2014 The Counter Edit",
            "Twenty questions a reviewer can work through, with current answers and status.",
            open_questions_body(),
        ),
        "/docs/metrics.html": (
            "home",
            "Metrics plan \u2014 The Counter Edit",
            "Five privacy-preserving events, ledger provenance rules, and the ban on invented baselines.",
            metrics_body(),
        ),
        "/docs/sources.html": (
            "home",
            "Source register \u2014 The Counter Edit",
            "Every claim on the site resolves to a source here; official sources only for product facts.",
            sources_body(),
        ),
    }
