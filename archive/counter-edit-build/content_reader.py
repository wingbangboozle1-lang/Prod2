"""Reader-facing pages: front page, guides, comparison, shelf, about, disclosure, 404.

Editorial voice (decision D-12): plain-spoken, source-first, zero hype. Sentences
vary in length. No "in today's fast-paced world". Claims that come from a listing
say so. Claims that are opinion are framed as opinion. Blank beats invented.
"""
from helpers import PRODUCTS, u, aff, official, VERIFY_DATE

GUIDES = [
    {
        "slug": "basket-or-oven-style-air-fryer",
        "title": "Basket or oven-style air fryer: what should you compare?",
        "short": "Basket or oven style?",
        "standfirst": "Two very different machines share one name. The fastest way to choose is to answer three questions about how you actually cook.",
        "img": "g-basket.jpg",
        "kicker": "Choosing a type",
        "minutes": "6 min read",
        "badge": "Start here",
        "badge_class": "badge-hot",
        "date": "2026-11-19",
    },
    {
        "slug": "air-fryer-capacity-checklist",
        "title": "A no-hype checklist for comparing air fryer capacity",
        "short": "Capacity, minus the hype",
        "standfirst": "Quarts are a marketing unit. Five checks tell you what a fryer will actually hold — before the box lies to you.",
        "img": "g-capacity.jpg",
        "kicker": "Capacity",
        "minutes": "7 min read",
        "badge": "Most practical",
        "badge_class": "badge-new",
        "date": "2026-11-19",
    },
    {
        "slug": "cleanup-and-counter-space-trade-offs",
        "title": "How to assess cleanup and counter-space trade-offs",
        "short": "Cleanup & counter space",
        "standfirst": "The two costs an appliance keeps charging after the receipt: sink minutes and square centimetres. Here is how to price both.",
        "img": "g-cleanup.jpg",
        "kicker": "Living with it",
        "minutes": "5 min read",
        "badge": "New",
        "badge_class": "badge-new",
        "date": "2026-11-19",
    },
    {
        "slug": "multi-function-appliance-questions",
        "title": "Questions to ask before buying a multi-function kitchen appliance",
        "short": "Multi-function reality check",
        "standfirst": "\u201cAir fryer\u201d has become a feature, not a category. Nine questions separate a workhorse from a drawer-filler.",
        "img": "g-multi.jpg",
        "kicker": "Reality check",
        "minutes": "6 min read",
        "badge": "",
        "badge_class": "",
        "date": "2026-11-19",
    },
]


def guide_url(g):
    return u(f"/guides/{g['slug']}.html")


def _card(g, with_badge=True):
    badge = (
        f'<span class="badge {g["badge_class"]}">{g["badge"]}</span>' if with_badge and g["badge"] else ""
    )
    return f"""<article class="card">
  <a class="card-media" href="{guide_url(g)}" aria-hidden="true" tabindex="-1"><img src="{u('/assets/img/')}{g['img']}" alt="Illustration for the guide: {esc_attr(g['short'])}" loading="lazy"></a>
  <div class="card-body">
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">{badge}<span class="kicker" style="margin:0;">{g['kicker']}</span></div>
    <h3><a href="{guide_url(g)}">{g['title']}</a></h3>
    <p>{g['standfirst']}</p>
    <div class="card-meta"><span>{g['date']}</span><span>{g['minutes']}</span></div>
  </div>
</article>"""


def esc_attr(s):
    return s.replace('"', "&quot;")


def index_body():
    g1, g2, g3, g4 = GUIDES
    featured = _card(g1) + _card(g2) + _card(g3)
    tiles = f"""
    <div class="grid grid-2" style="margin-top:18px;">
      <div class="tile"><div class="tile-icon">&#127919;</div><h3>Not sure which one fits?</h3>
        <p>Three questions, one honest recommendation &mdash; including &ldquo;none of these, buy a thermometer first.&rdquo;</p>
        <div class="tile-link"><a href="{u('/compare.html')}#chooser">Take the chooser &rarr;</a></div></div>
      <div class="tile"><div class="tile-icon">&#9878;&#65039;</div><h3>The side-by-side</h3>
        <p>Five products, one table. Facts only from official listings; everything unverified stays blank and flagged.</p>
        <div class="tile-link"><a href="{u('/compare.html')}">Open the comparison &rarr;</a></div></div>
      <div class="tile"><div class="tile-icon">&#128230;</div><h3>The Shelf</h3>
        <p>All five products with their verification record: what we confirmed, when, and from which listing.</p>
        <div class="tile-link"><a href="{u('/products.html')}">Browse the shelf &rarr;</a></div></div>
      <div class="tile"><div class="tile-icon">&#128202;</div><h3>The data room</h3>
        <p>Decisions, flags, open questions and an empty campaign ledger &mdash; the machinery, in public.</p>
        <div class="tile-link"><a href="{u('/docs/index.html')}">Inspect the machinery &rarr;</a></div></div>
    </div>"""
    glance = ""
    for pid in ["P1", "P2", "P3", "P4", "P5"]:
        p = PRODUCTS[pid]
        glance += (
            f'<tr><td><span class="rowlabel">{p["short"]}</span><br><span class="muted">{p["type"]}</span></td>'
            f"<td>{p['best_for']}</td>"
            f'<td>{aff(pid, "home_glance", "View on Amazon")}</td></tr>'
        )
    glance_table = f"""
    <div class="section-head"><h2>The five, at a glance</h2><a class="more" href="{u('/compare.html')}">Full comparison &rarr;</a></div>
    <div class="table-scroll"><table class="compare" style="min-width:520px;">
      <thead><tr><th>Product</th><th>Best for (our opinion)</th><th>Link</th></tr></thead>
      <tbody>{glance}</tbody>
    </table></div>
    <p class="hero-note" style="margin-top:10px;">Product identities above are verified from each official Amazon listing on {VERIFY_DATE}; &ldquo;best for&rdquo; is our opinion, labeled as such. Dimensions and prices are deliberately blank &mdash; <a href="{u('/docs/flagged.html')}">here is why</a>.</p>"""
    trust = f"""
    <div class="section-head"><h2>How we say what we say</h2></div>
    <div class="grid grid-3">
      <div class="tile"><div class="tile-icon">&#128279;</div><h3>Every claim carries its source</h3>
        <p>Product facts link straight to the official Amazon listing they came from. If we can&rsquo;t verify it, the cell stays blank.</p></div>
      <div class="tile"><div class="tile-icon">&#9888;&#65039;</div><h3>No invented numbers</h3>
        <p>Prices and star ratings change daily. We never copy them into a page and pretend they&rsquo;re stable.</p></div>
      <div class="tile"><div class="tile-icon">&#128161;</div><h3>Opinions are labeled</h3>
        <p>&ldquo;Best for&rdquo; is our editorial judgment. It says so, every time it appears.</p></div>
    </div>"""
    return f"""<section class="hero"><div class="wrap"><div class="hero-grid">
      <div>
        <p class="kicker">Kitchen counter intelligence</p>
        <h1>Air-fryer decisions, <em>minus the noise</em>.</h1>
        <p class="lede">Question-shaped guides to the three air fryers and two thermometers on our counter &mdash;
        what the listings can&rsquo;t tell you, and what the spec sheets argue about. Sourced, dated, and honest
        about what we don&rsquo;t know.</p>
        <div class="hero-cta">
          <a class="btn btn-primary" href="{u('/compare.html')}#chooser">Find your fit in 3 questions <span class="arrow">&rarr;</span></a>
          <a class="btn btn-ghost" href="{u('/guides/index.html')}">Read the guides</a>
        </div>
        <p class="hero-note">Five products verified against their official Amazon listings on {VERIFY_DATE}. Every outbound product link is a paid affiliate link, marked and disclosed above.</p>
      </div>
      <div class="hero-media"><img src="{u('/assets/img/hero-front.jpg')}" alt="Line-art illustration of a tidy kitchen counter with an air fryer, thermometer and cutting board" fetchpriority="high"></div>
    </div></div></section>
    <section class="section"><div class="wrap">
      <div class="section-head"><h2>Start with your question</h2><a class="more" href="{u('/guides/index.html')}">All guides &rarr;</a></div>
      <div class="grid grid-3">{featured}</div>
      {tiles}
    </div></section>
    <section class="section"><div class="wrap">{glance_table}</div></section>
    <section class="section"><div class="wrap">{trust}</div></section>"""


def guides_hub_body():
    cards = "".join(_card(g) for g in GUIDES)
    upcoming = "".join(
        f'<li><strong>{t}</strong> <span class="badge badge-warn">In the calendar</span><br>'
        f'<span style="color:var(--ink-soft);font-size:0.9rem;">{d}</span></li>'
        for t, d in [
            ("&ldquo;450&deg;F claims, tested against what the listings promise&rdquo;", "Working title &mdash; spec-backed, needs verified temperature data before publication."),
            ("&ldquo;Smart thermometers: is app range worth the drawer space?&rdquo;", "Working title &mdash; waiting on owner confirmation of the WiFi-range claims in the CHEF iQ manual."),
            ("&ldquo;The two-basket week: cooking a whole meal in a dual fryer&rdquo;", "Working title &mdash; recipe-first piece; needs our own kitchen tests, not listing claims."),
        ]
    )
    return f"""<div class="wrap-narrow"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{u('/index.html')}">Home</a></li><li>Guides</li></ol></nav></div>
    <section class="article-head"><div class="wrap-narrow">
      <p class="kicker">The guide shelf</p>
      <h1>Buyer guides that answer real questions</h1>
      <p class="standfirst">One page per question. Written for people standing in a kitchen holding a credit card,
      not for search engines holding a keyword list.</p>
    </div></section>
    <section class="section" style="padding-top:10px;"><div class="wrap">
      <div class="grid grid-3">{cards}</div>
    </div></section>
    <section class="section" style="padding-top:0;"><div class="wrap-narrow">
      <h2 class="section-head" style="font-family:var(--font-display);">Next in the pipeline</h2>
      <ul class="prose" style="list-style:none;padding:0;">{upcoming}</ul>
      <div class="empty-note">Cadence: one new guide per week, Tuesday mornings. Every new guide enters
      <a href="{u('/sitemap.xml')}">the sitemap</a> and <a href="{u('/rss.xml')}">the feed</a> the day it publishes.
      Topic choice is driven by measured arrivals &mdash; see <a href="{u('/docs/metrics.html')}">the metrics plan</a>.</div>
    </div></section>"""


def _guide_shell(g, body, aside_extra=""):
    aside = f"""
    <aside>
      <div class="aside-box">
        <h3>Still deciding?</h3>
        <p style="color:var(--ink-soft);margin:0 0 10px;">The three-question chooser gives a recommendation in under a minute &mdash; and it will happily tell you a thermometer beats a second appliance.</p>
        <a class="btn btn-primary" style="width:100%;" href="{u('/compare.html')}#chooser">Take the chooser</a>
      </div>
      <div class="aside-box">
        <h3>Jump to</h3>
        <ul>
          <li><a href="{u('/compare.html')}">The five, side by side</a></li>
          <li><a href="{u('/guides/air-fryer-capacity-checklist.html')}">Capacity checklist</a></li>
          <li><a href="{u('/guides/cleanup-and-counter-space-trade-offs.html')}">Cleanup trade-offs</a></li>
          <li><a href="{u('/guides/basket-or-oven-style-air-fryer.html')}">Basket vs oven style</a></li>
          <li><a href="{u('/products.html')}">The Shelf (all five)</a></li>
        </ul>
      </div>
      <div class="aside-box">
        <h3>Sources on this page</h3>
        <ul>
          <li>{official('P1')}</li>
          <li>{official('P2')}</li>
          <li>{official('P3')}</li>
          <li>{official('P4')}</li>
          <li>{official('P5')}</li>
          <li><a href="{u('/docs/sources.html')}">Full source register</a></li>
        </ul>
      </div>
      {aside_extra}
    </aside>"""
    return f"""<div class="wrap-narrow"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{u('/index.html')}">Home</a></li><li><a href="{u('/guides/index.html')}">Guides</a></li><li>{g['short']}</li></ol></nav></div>
    <section class="article-head"><div class="wrap-narrow">
      <p class="kicker">{g['kicker']}</p>
      <h1>{g['title']}</h1>
      <p class="standfirst">{g['standfirst']}</p>
      <div class="article-meta"><span>{g['date']}</span><span>{g['minutes']}</span><span>By the {esc_attr('Counter Edit')} desk</span><span>Facts verified {VERIFY_DATE}</span></div>
    </div></section>
    <div class="wrap-narrow">
      <div class="article-hero"><img src="{u('/assets/img/')}{g['img']}" alt="Editorial illustration accompanying the guide {esc_attr(g['short'])}" fetchpriority="high"></div>
      <p class="illustration-note">Illustration: The Counter Edit. Not a photograph of any product &mdash; see <a href="{u('/docs/decisions.html')}">decision D-22</a>.</p>
      <div class="toc"><h2>On this page</h2><ol>
        {body_toc(body)}
      </ol></div>
    </div>
    <section class="section" style="padding-top:0;"><div class="wrap"><div class="two-col">
      <div class="prose" data-article-body>{body}</div>
      {aside}
    </div></div></section>
    <div class="sticky-bar"><div class="wrap">
      <span class="bar-label">Keep going</span>
      <a href="{u('/compare.html')}">Comparison table</a>
      <a href="{u('/guides/air-fryer-capacity-checklist.html')}">Capacity</a>
      <a href="{u('/products.html')}">The Shelf</a>
      <span class="bar-out">{aff('P1', 'sticky_bar', 'Check prices on Amazon')}</span>
    </div></div>"""


def body_toc(body):
    import re
    out, i = [], 1
    for m in re.finditer(r'<h2 id="([^"]+)">([^<]+)</h2>', body):
        out.append(f'<li><a href="#{m.group(1)}">{m.group(2)}</a></li>')
        i += 1
    return "".join(out)


def guide1_body():
    return f"""
<h2 id="not-the-same">They are not the same appliance</h2>
<p>A basket air fryer is a fast little convection pit: it heats in minutes, wants a shake halfway through,
and rewards you with weeknight speed. An oven-style air fryer is a small second oven with a door, racks and
patience &mdash; it preheats slower, holds more, and can toast a bagel while it&rsquo;s at it.</p>
<p>Neither is &ldquo;better.&rdquo; They fail differently. A basket fails when you feed more than two people
or cook in courses. An oven-style fails when your counter is shallow or your patience is short. That is why
the first question isn&rsquo;t <em>which brand</em> &mdash; it&rsquo;s <em>which failure can you live with</em>.</p>
<h2 id="five-things">Compare these five things, in this order</h2>
<ol>
<li><strong>Counter depth, including the door.</strong> Measure the space and add the door swing. Oven-style
french-door units open outward; a basket needs pull-out room and shake clearance. The <a href="{u('/guides/cleanup-and-counter-space-trade-offs.html')}">cleanup and counter-space guide</a> has the measuring routine.</li>
<li><strong>What you cook on weeknights.</strong> Two things at once? A dual-basket format exists for exactly
that &mdash; the Chefman 6 Qt below is literally two independent 3-quart baskets with a sync-finish mode, per its
official listing. One big tray of vegetables? That&rsquo;s oven-style territory.</li>
<li><strong>Geometry beats marketing.</strong> &ldquo;6 quarts&rdquo; over two baskets is two 3-quart pits, not
one 6-quart pit. Read the basket count before the headline number. Our <a href="{u('/guides/air-fryer-capacity-checklist.html')}">capacity checklist</a> runs this trap down properly.</li>
<li><strong>Preheat patience.</strong> Basket: fast, but you shake. Oven: slower, but you walk away. Honest
question: which ritual will you still be doing in February?</li>
<li><strong>Cleanup surfaces.</strong> Count the washable parts before you buy, not after. More accessories
equals more sink time &mdash; the trade-off guide makes the math explicit.</li>
</ol>
<h2 id="picks">Our picks in each camp</h2>
<p><em>Editorial opinion below &mdash; the facts in brackets come from each official listing title, verified {VERIFY_DATE}.</em></p>
<div class="callout"><h4>Dual-basket pick: Chefman 6 Qt Dual Basket Air Fryer <span class="badge badge-hot">Our dual pick</span></h4>
<p>For two-dish weeknights. [6-quart dual-basket format; two independent 3-quart nonstick baskets; baskets
listed as dishwasher safe; sync-finish and hi-fry modes named in the listing.] {aff('P1', 'guide1_pick', 'Check price on Amazon')}</p></div>
<div class="callout"><h4>Oven-style pick: Emeril Lagasse 26 QT French Door <span class="badge badge-hot">Our oven pick</span></h4>
<p>For batch cooks and toaster-oven replacers. [26-quart cavity; french-door opening; 24 one-touch presets;
six cooking accessories included &mdash; which is also six things in the sink someday.] {aff('P2', 'guide1_pick', 'Check price on Amazon')}</p></div>
<div class="callout"><h4>Single-basket middle ground: Chefman 8 Qt TurboFry</h4>
<p>Smallest fuss at the sink, one big basket. [8-quart basket; 4-in-1 function set; 450&deg;F hi-fry option;
XL nonstick dishwasher-safe basket.] {aff('P3', 'guide1_pick', 'Check price on Amazon')}</p></div>
<h2 id="thermometer">The add-on nobody regrets</h2>
<p>Whichever box you buy, an instant-read thermometer is the cheapest upgrade to every meal it cooks. Air-fryer
recipes lie about doneness the same way grill recipes do. The <a href="{u('/products.html')}">Shelf</a> carries
two verified options: a <a href="{u('/products.html')}#P4">sub-second instant read</a> and a
<a href="{u('/products.html')}#P5">wireless multi-probe</a> for long cooks.</p>
<h2 id="next">Where to go next</h2>
<ul>
<li>Undecided between the two formats? <a href="{u('/compare.html')}#chooser">The three-question chooser</a> settles it in a minute.</li>
<li>Worried about the number on the box? <a href="{u('/guides/air-fryer-capacity-checklist.html')}">The capacity checklist</a>.</li>
<li>Worried about the counter? <a href="{u('/guides/cleanup-and-counter-space-trade-offs.html')}">Cleanup and counter-space trade-offs</a>.</li>
</ul>"""


def guide2_body():
    return f"""
<h2 id="quarts-lie">Why &ldquo;quarts&rdquo; tells you less than you think</h2>
<p>The quart number on the box is a volume rating for the machine&rsquo;s chamber, not a promise about dinner.
What matters is usable volume: baskets have walls, racks steal height, and air needs room to move or you
steam instead of crisp. Two machines with the same quart rating can hold very different meals.</p>
<p>So run the checklist below before you trust any capacity claim &mdash; including ours. Everything we state
about the five products here comes from their official Amazon listing titles, verified {VERIFY_DATE}; where the
listing doesn&rsquo;t state something, we leave it blank rather than guess.</p>
<h2 id="checklist">The capacity checklist</h2>
<ol>
<li><strong>Count the baskets.</strong> A &ldquo;6-quart dual basket&rdquo; is two 3-quart pits. That&rsquo;s
the Chefman 6 Qt&rsquo;s honest geometry &mdash; its listing title says <em>two independent 3-quart baskets</em>,
not one big one. Great for two dishes, limiting for one huge tray.</li>
<li><strong>Prefer stated dimensions to stated quarts.</strong> Dimensions are the number you can actually
measure your counter against. We do not copy dimension claims into our comparison table yet &mdash; our fetches
verified the listings but not their spec tables &mdash; so the table shows blanks with a flag instead. When
dimension values are verified from the official listings, our
<a href="{u('/guides/cleanup-and-counter-space-trade-offs.html')}">counter-space analysis</a> will publish the
methodology and the numbers together.</li>
<li><strong>Match the fryer to your food, not to your family size.</strong> Family-size claims are
unstandardized. A portion of fries that overlaps barely crisps &mdash; surface area matters more than depth.
Think about the widest single thing you cook, then compare basket floor space.</li>
<li><strong>For oven-style, check rack reality.</strong> The Emeril Lagasse 26 QT lists a 26-quart cavity and
six included accessories. Accessories change what &ldquo;26 quarts&rdquo; means in practice &mdash; racks split
the cavity; a rotisserie setup eats clearance. Count what&rsquo;s included before imagining the load.</li>
<li><strong>Beware &ldquo;serves N&rdquo; claims.</strong> There is no official standard behind them. Treat any
&ldquo;serves 6&rdquo; as marketing until you have read the basket dimensions.</li>
</ol>
<h2 id="counter-depth">Capacity per centimetre of counter depth</h2>
<p>This is the number a listing cannot give you: usable quarts divided by the counter depth the machine actually
occupies, including door swing and shake clearance. Our methodology is fixed and published &mdash;
<a href="{u('/guides/cleanup-and-counter-space-trade-offs.html')}">see the trade-off guide</a> &mdash; but the
table itself is blank today because the dimension inputs are not yet verified from the official listings.</p>
<div class="empty-note"><strong>Deliberately blank:</strong> the capacity-per-centimetre table publishes when
dimensions are verified from official listing spec sheets (flag <a href="{u('/docs/flagged.html')}#F-04">F-04</a>).
We would rather show you nothing than a number we cannot source. Track progress on the
<a href="{u('/docs/index.html')}">dashboard</a>.</div>
<h2 id="serves">Read this before trusting a &ldquo;best seller&rdquo; badge</h2>
<p>Popularity badges are snapshots, not measurements &mdash; they change by the hour and mean different things
in different categories. Our evidence rule for any trending or popularity claim (decision
<a href="{u('/docs/decisions.html')}#D-19">D-19</a>): we repeat one only with a dated link to the page that
showed it. Anything less stays off the page.</p>
<h2 id="picks">The three formats, in one line each</h2>
<ul>
<li><strong>Dual basket (Chefman 6 Qt):</strong> two independent 3-quart baskets &mdash; {aff('P1', 'guide2_pick', 'check price')}</li>
<li><strong>Oven-style (Emeril Lagasse 26 QT):</strong> 26-quart cavity, six accessories included &mdash; {aff('P2', 'guide2_pick', 'check price')}</li>
<li><strong>Single basket (Chefman 8 Qt TurboFry):</strong> one 8-quart XL basket, 4-in-1 &mdash; {aff('P3', 'guide2_pick', 'check price')}</li>
</ul>
<p>Then pair whichever you choose with a thermometer &mdash; doneness is the one spec a fryer can&rsquo;t carry
on its box. See <a href="{u('/products.html')}">the Shelf</a> for the two verified options.</p>"""


def guide3_body():
    return f"""
<h2 id="real-estate">The real estate audit</h2>
<p>An appliance keeps two ledgers after the receipt: sink minutes and square centimetres. Most regret reviews
(&ldquo;it just sits in the cupboard&rdquo;) are one of those two ledgers going unpaid. Run this audit before
buying anything with a heating element:</p>
<ol>
<li><strong>Measure the landing zone</strong> &mdash; width, depth, and the vertical clearance above it.</li>
<li><strong>Add the door story.</strong> French doors swing wide (that is the design &mdash; the Emeril Lagasse
26 QT&rsquo;s listing leads with its french-door opening). Baskets pull out; add their travel.</li>
<li><strong>Add the ritual space.</strong> Baskets want shake room; ovens want rack-pull room. Nobody plans
this and everybody needs it.</li>
<li><strong>Check the heat bubble.</strong> Keep clearance above and behind per the manual&rsquo;s safety pages
&mdash; we link listings, we don&rsquo;t restate their safety numbers.</li>
</ol>
<h2 id="sink-math">Sink math</h2>
<p>Count washable surfaces like a cost, because they are one. From the official listing titles, verified
{VERIFY_DATE}:</p>
<ul>
<li><strong>Chefman 6 Qt dual:</strong> two dishwasher-safe baskets <em>(plus any trays the listing describes
&mdash; we haven&rsquo;t verified the full accessory list, so we don&rsquo;t count it)</em>. Two baskets also
means two things to dry.</li>
<li><strong>Chefman 8 Qt TurboFry:</strong> one XL nonstick dishwasher-safe basket. One surface. This is the
sink-minimum pick.</li>
<li><strong>Emeril Lagasse 26 QT:</strong> six cooking accessories included. Six objects that will, some night,
all be in the sink &mdash; plus the cavity. The flexibility is real; so is the wash count.</li>
</ul>
<p><em>Opinion:</em> if you already resent dishes, optimize for the single basket. If you batch-cook on
Sundays and wash once, the oven-style&rsquo;s accessory ecosystem pays for itself.</p>
<h2 id="dishwasher">Dishwasher claims, translated</h2>
<p>&ldquo;Dishwasher-safe&rdquo; on a listing is the manufacturer&rsquo;s statement, verified here only as far
as the listing title goes. Two practical notes, offered as opinion: nonstick coatings live longer when they
skip the hot dry cycle; and a quick hand-wash of a still-warm basket often takes less time than loading the
dishwasher at all. Check each product&rsquo;s manual page for care specifics &mdash; and if it matters to you,
verify the coating claims on the listing before purchase.</p>
<h2 id="cheat-sheet">The trade-off cheat sheet</h2>
<table>
<thead><tr><th>If you&hellip;</th><th>Then look at</th><th>Trade you&rsquo;re accepting</th></tr></thead>
<tbody>
<tr><td>Hate doing dishes</td><td>Chefman 8 Qt TurboFry (one basket) &mdash; {aff('P3', 'guide3_table', 'link')}</td><td>No two-dish cooking; smaller batch ceiling</td></tr>
<tr><td>Cook two things at once on weeknights</td><td>Chefman 6 Qt dual &mdash; {aff('P1', 'guide3_table', 'link')}</td><td>Two baskets to wash; two pits, not one big one</td></tr>
<tr><td>Batch-cook or want a toaster-oven replacement</td><td>Emeril Lagasse 26 QT &mdash; {aff('P2', 'guide3_table', 'link')}</td><td>Deep counter footprint; six accessories in the sink</td></tr>
</tbody>
</table>
<h2 id="counter-ledger">The counter-space ledger</h2>
<p>Our capacity-per-centimetre analysis (S-23) will publish here once machine dimensions are verified from the
official listings&rsquo; spec sheets. The methodology is already fixed: usable quarts &divide; occupied counter
depth including door swing and ritual clearance, calculated identically for every product, sources linked for
every input. Until then the table stays blank &mdash; see flag <a href="{u('/docs/flagged.html')}#F-04">F-04</a>
and the <a href="{u('/docs/index.html')}">dashboard</a> for status.</p>
<p>One thing we can say today: whichever machine you pick, a
<a href="{u('/products.html')}#P4">fast instant-read thermometer</a> occupies almost none of the counter and
upgrades every meal it touches.</p>"""


def guide4_body():
    return f"""
<h2 id="drawer-filler">The drawer-filler problem</h2>
<p>Every kitchen has one: the machine that promised seven appliances and became one, used lazily, taking the
counter of three. Multi-function isn&rsquo;t a feature &mdash; it&rsquo;s a bet that you will actually change
modes. These nine questions are how you price that bet before you make it.</p>
<h2 id="nine-questions">Nine questions to ask</h2>
<ol>
<li><strong>Which three functions would you genuinely use weekly?</strong> Name them. If you can&rsquo;t name
three, you&rsquo;re buying a demo, not a tool.</li>
<li><strong>Does the primary function still excel?</strong> A combo unit that toasts brilliantly but air-fries
meekly fails the main job it was bought for. Reviews matter here; specs don&rsquo;t tell you.</li>
<li><strong>What does each mode cost in time?</strong> Preheat and mode-switch add minutes. A basket fryer
wins partly because it skips ceremony.</li>
<li><strong>Does it replace something you own &mdash; really?</strong> The Emeril Lagasse 26 QT&rsquo;s listing
positions it as a countertop convection cooker with 24 presets. If it retires your toaster oven, its footprint
debt is partly repaid. If it doesn&rsquo;t, it isn&rsquo;t.</li>
<li><strong>Can you operate it half-asleep?</strong> Controls you can use at 6:50 a.m. without glasses count
more than a mode list you&rsquo;ll read once.</li>
<li><strong>What&rsquo;s included versus sold later?</strong> Six accessories come included with the 26 QT,
per its listing. What comes extra on other units is a real cost difference.</li>
<li><strong>How many washable surfaces?</strong> Functions multiply sink count &mdash; the
<a href="{u('/guides/cleanup-and-counter-space-trade-offs.html')}">trade-off guide</a> makes this math explicit.</li>
<li><strong>What does it replace in footprint terms?</strong> Measure twice. The
<a href="{u('/guides/cleanup-and-counter-space-trade-offs.html')}">real-estate audit</a> applies doubly here.</li>
<li><strong>What&rsquo;s the warranty and support story?</strong> We haven&rsquo;t verified warranty terms for
any of the five products &mdash; that field stays blank in our comparison (flag
<a href="{u('/docs/flagged.html')}#F-06">F-06</a>). Check the listing&rsquo;s warranty section and the
manufacturer&rsquo;s site before purchase; a multi-function machine has more parts to be covered.</li>
</ol>
<h2 id="oven-stress-test">Oven-style units: the multi-function stress test</h2>
<p>Oven-style air fryers are where multi-function promises concentrate. The 26 QT lists
<em>24 one-touch presets</em> &mdash; and here&rsquo;s the honest reading, offered as opinion: presets are
starting points, not functions. Count <em>functions</em> (air fry, bake, roast, toast, broil, dehydrate&hellip;)
and ask which ones you&rsquo;d use weekly. Twenty-four presets over two real functions is a worse deal than
six presets over five functions you actually cook.</p>
<h2 id="thermometer-trap">Thermometers: the same trap in reverse</h2>
<p>The multi-function question cuts both ways. On the Shelf you&rsquo;ll find two verified thermometers that
illustrate the fork: the <a href="{u('/products.html')}#P4">ThermoMaven instant-read</a> does one job
[1-second read, &plusmn;0.5&deg;F accuracy, NIST &amp; NSF certified, IP67 waterproof &mdash; per listing title],
while the <a href="{u('/products.html')}#P5">CHEF iQ Sense</a> adds wireless range, app alerts, three probes
and five sensors. Neither is better in the abstract. The question is the same nine, shortened: what will you
use weekly &mdash; a two-second doneness check, or leave-the-house brisket monitoring?</p>
<h2 id="shortcut">The decision shortcut</h2>
<p>If the nine questions tire you, the <a href="{u('/compare.html')}#chooser">three-question chooser</a> does
the short version &mdash; and the <a href="{u('/compare.html')}">comparison table</a> shows which claims on
each machine are verified versus still blank. Buying slowly is a feature.</p>"""


GUIDE_BODIES = {
    "basket-or-oven-style-air-fryer": guide1_body,
    "air-fryer-capacity-checklist": guide2_body,
    "cleanup-and-counter-space-trade-offs": guide3_body,
    "multi-function-appliance-questions": guide4_body,
}


def compare_body():
    rows = ""
    for pid in ["P1", "P2", "P3", "P4", "P5"]:
        p = PRODUCTS[pid]
        rows += (
            f'<tr id="{pid}"><td><span class="rowlabel">{p["short"]}</span><br>'
            f'<span class="muted">{p["type"]}</span></td>'
            f'<td>{aff(pid, "compare_row", "Check price")}</td>'
            f'<td>{official(pid)}</td>'
            f"<td>{p['best_for']} <em>(opinion)</em></td>"
            f"<td>{'; '.join(p['verified_facts'])}</td>"
            f'<td class="spec-unverified">blank &mdash; unverified (F-04)</td>'
            f'<td class="spec-unverified">blank &mdash; dynamic (F-05)</td>'
            f'<td class="spec-unverified">blank &mdash; dynamic (F-05)</td>'
            f'<td class="spec-unverified">blank &mdash; unverified (F-06)</td></tr>'
        )
    chooser = f"""
<div class="chooser" id="chooser">
  <h2>Which one is for you?</h2>
  <p class="chooser-sub">Three questions. A recommendation in one minute &mdash; no email, no scorekeeping.</p>
  <form id="chooser-form">
    <div class="q"><span class="q-label">1. Who are you cooking for, most nights?</span>
      <div class="seg">
        <label><input type="radio" name="c-people" value="solo" checked> Just me (maybe two)</label>
        <label><input type="radio" name="c-people" value="family"> A family table</label>
      </div></div>
    <div class="q"><span class="q-label">2. How much counter can you give up?</span>
      <div class="seg">
        <label><input type="radio" name="c-space" value="tight" checked> Tight &mdash; every centimetre counts</label>
        <label><input type="radio" name="c-space" value="roomy"> Roomy &mdash; footprint is fine</label>
      </div></div>
    <div class="q"><span class="q-label">3. What job is this appliance really for?</span>
      <div class="seg">
        <label><input type="radio" name="c-goal" value="twoatonce" checked> Two dishes at once</label>
        <label><input type="radio" name="c-goal" value="bigbatches"> Big batches &amp; roasting</label>
        <label><input type="radio" name="c-goal" value="smallcounter"> Small meals, small counter</label>
        <label><input type="radio" name="c-goal" value="doneness"> Doneness, not volume</label>
      </div></div>
    <button class="btn btn-primary" type="submit">Show my match <span class="arrow">&rarr;</span></button>
  </form>
  <div class="chooser-result" id="chooser-result">
    <p class="verdict"></p>
    <p class="why"></p>
    <a class="btn btn-affiliate" href="#P1">See the match in the table</a>
  </div>
</div>"""
    return f"""<div class="wrap-narrow"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{u('/index.html')}">Home</a></li><li>Compare</li></ol></nav></div>
    <section class="page-head"><div class="wrap">
      <p class="kicker">Side by side</p>
      <h1>Five products, one honest table</h1>
      <p class="lede">Facts come only from official Amazon listings, verified {VERIFY_DATE}. Cells we can&rsquo;t
      verify stay blank and flagged &mdash; no guessed numbers, no frozen prices, no copied ratings.</p>
    </div></section>
    <section class="section" style="padding-top:6px;"><div class="wrap">
      {chooser}
      <div class="table-scroll"><table class="compare">
        <thead><tr><th>Product</th><th>Our link</th><th>Official listing</th><th>Best for</th>
        <th>Listing-stated facts (verified {VERIFY_DATE})</th><th>Dimensions</th><th>Price</th><th>Rating</th><th>Warranty</th></tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
      <p class="hero-note"><strong>Blank cells are a policy, not an omission.</strong> Dimensions and warranty
      pending verification (flags <a href="{u('/docs/flagged.html')}#F-04">F-04</a>,
      <a href="{u('/docs/flagged.html')}#F-06">F-06</a>); prices and ratings change daily and are never published
      as stable facts (<a href="{u('/docs/flagged.html')}#F-05">F-05</a>). Submitted ASINs vs observed redirect
      targets are tracked separately in the <a href="{u('/docs/index.html')}">product-intent register</a>.</p>
    </div></section>
    <div class="sticky-bar"><div class="wrap">
      <span class="bar-label">Compare</span>
      <a href="#P1">Dual basket</a><a href="#P2">Oven style</a><a href="#P3">Single basket</a>
      <a href="#P4">Instant read</a><a href="#P5">Wireless</a>
      <span class="bar-out">{aff('P1', 'sticky_bar', 'Check prices on Amazon')}</span>
    </div></div>"""


def products_body():
    cards = ""
    for i, pid in enumerate(["P1", "P2", "P3", "P4", "P5"], 1):
        p = PRODUCTS[pid]
        facts = "".join(f"<li>{f}</li>" for f in p["verified_facts"])
        cards += f"""
<article class="card shelf-card" id="{pid}">
  <span class="p-rank">{i}</span>
  <div class="card-body">
    <span class="badge">{p['type']}</span>
    <h3>{p['short']}</h3>
    <p><strong>Best for:</strong> {p['best_for']} <em>(our opinion)</em></p>
    <ul style="margin:0;padding-left:1.2em;color:var(--ink-soft);font-size:0.9rem;">{facts}</ul>
    <p style="font-size:0.82rem;color:var(--ink-faint);">Verified from the official listing on {VERIFY_DATE}.
    Source: {official(pid)}. Submitted link (pre-verification): <code>{p['submitted']}</code> &mdash;
    compliance status open, see <a href="{u('/docs/flagged.html')}#F-02">F-02</a>.</p>
    <div class="card-meta">{aff(pid, 'shelf_card', 'Check price on Amazon')}</div>
  </div>
</article>"""
    return f"""<div class="wrap-narrow"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{u('/index.html')}">Home</a></li><li>The Shelf</li></ol></nav></div>
    <section class="page-head"><div class="wrap-narrow">
      <p class="kicker">The Shelf</p>
      <h1>Five products, each with its paper trail</h1>
      <p class="lede">Every card carries what we verified, when, and from which official listing. Nothing here
      was inferred; blank means we haven&rsquo;t confirmed it yet.</p>
    </div></section>
    <section class="section" style="padding-top:8px;"><div class="wrap">
      <div class="grid grid-2">{cards}</div>
      <p class="hero-note">Order on this shelf is editorial, based on the guides&rsquo; reasoning &mdash; not a
      popularity claim (decision <a href="{u('/docs/decisions.html')}#D-19">D-19</a>). All outbound Amazon links
      are affiliate links marked rel=&quot;sponsored&quot;.</p>
    </div></section>"""


def about_body():
    return f"""<div class="wrap-narrow"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{u('/index.html')}">Home</a></li><li>About</li></ol></nav></div>
    <section class="page-head"><div class="wrap-narrow">
      <p class="kicker">The desk</p>
      <h1>About The Counter Edit</h1>
      <p class="lede">A small editorial desk covering the air-fryer aisle properly: question-shaped guides,
      sourced facts, and a public ledger of what we don&rsquo;t know.</p>
    </div></section>
    <section class="section" style="padding-top:8px;"><div class="wrap-narrow prose">
      <h2>Why this site exists</h2>
      <p>The air-fryer aisle is loud. Every listing shouts a quart number, a preset count and a badge. We wanted
      the opposite: a quiet page that answers the question you actually have, links every claim to its official
      source, and admits blank cells instead of inventing numbers.</p>
      <h2>Our voice</h2>
      <ul>
        <li><strong>Plain-spoken.</strong> No hype, no urgency theater, no robot prose. If a section reads like
        a human wrote it for a friend, it passed.</li>
        <li><strong>Source-first.</strong> Product facts come from official Amazon listings, verified on a dated
        fetch. Every table row on the data pages carries its source link.</li>
        <li><strong>Opinions labeled.</strong> &ldquo;Best for&rdquo; is editorial judgment and says so.</li>
        <li><strong>Blank beats invented.</strong> Unverifiable values stay empty and are flagged publicly on
        the <a href="{u('/docs/flagged.html')}">Flagged for Review page</a>.</li>
      </ul>
      <h2>Who writes this</h2>
      <p>The Counter Edit desk. We don&rsquo;t put a personal name on these pages yet &mdash; and we won&rsquo;t
      invent one. When a real human takes ownership of the byline, their name goes here with a bio that says
      how they know appliances. Until then, the editorial standards above are the byline.</p>
      <h2>How the site makes money</h2>
      <p>Outbound product links to Amazon.com are affiliate links carrying tracking ID
      <code>shopnow047c-20</code>. When a reader clicks one and buys something, Amazon may pay us a commission.
      The price you pay is never changed by this. Full details on the
      <a href="{u('/disclosure.html')}">disclosure page</a>.</p>
      <h2>What we will never do</h2>
      <ul>
        <li>Publish a price, rating or dimension we cannot verify from an official source.</li>
        <li>Repeat a &ldquo;trending&rdquo; or &ldquo;best seller&rdquo; claim without a dated link to the page
        that showed it.</li>
        <li>Use product photography we did not take or license &mdash; illustrations only until the
        <a href="{u('/docs/decisions.html')}#D-22">photography decision (D-22)</a> is made.</li>
        <li>Publish a conversion score or revenue forecast &mdash; the
        <a href="{u('/docs/metrics.html')}">metrics plan</a> forbids it.</li>
      </ul>
    </div></section>"""


def disclosure_body():
    return f"""<div class="wrap-narrow"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{u('/index.html')}">Home</a></li><li>Disclosure</li></ol></nav></div>
    <section class="page-head"><div class="wrap-narrow">
      <p class="kicker">The deal, in plain words</p>
      <h1>Disclosure policy</h1>
      <p class="lede">How this site earns, what the labels mean, and where our obligations come from &mdash;
      with links to the primary sources so you can read them yourself.</p>
    </div></section>
    <section class="section" style="padding-top:8px;"><div class="wrap-narrow prose">
      <h2>The affiliate relationship</h2>
      <p>The Counter Edit participates in the Amazon Associates Program. Outbound product links to Amazon.com
      carry our Associates tracking ID (<code>shopnow047c-20</code>). If a reader clicks one and makes a
      qualifying purchase, Amazon may pay us a commission from the purchase price. The reader&rsquo;s price is
      never affected. This disclosure appears above the fold on every page of this site and again in the footer.</p>
      <h2>What the labels on our links mean</h2>
      <p>Every outbound Amazon link on this site is marked <code>rel="sponsored nofollow noopener"</code>. The
      <code>sponsored</code> marker is a public, machine-readable statement that the link is paid &mdash; see
      Google&rsquo;s guidance on <a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links" rel="nofollow noopener" target="_blank">qualifying outbound links</a>. For readers, the meaning is simpler: those links are advertising, and they are labeled as such.</p>
      <h2>Where the obligations come from</h2>
      <ul>
        <li><a href="https://affiliate-program.amazon.com/help/operating/policies" rel="nofollow noopener" target="_blank">Amazon Associates Program Policies</a> &mdash; the Special Link, disclosure and participation requirements this site operates under.</li>
        <li><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers" rel="nofollow noopener" target="_blank">FTC: Disclosures 101</a> &mdash; clear-and-conspicuous placement (that is why the strip is above the fold, not buried).</li>
        <li><a href="https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews" rel="nofollow noopener" target="_blank">FTC: Endorsements, Influencers and Reviews</a> &mdash; the endorsement context we review every page against.</li>
      </ul>
      <h2>What we do not claim</h2>
      <ul>
        <li>We do not claim any submitted short link is compliant or non-compliant &mdash; its status is
        unresolved and tracked as flag <a href="{u('/docs/flagged.html')}#F-02">F-02</a>. Reader-facing links
        use tagged <code>amazon.com/dp/</code> Special Links built from observed listing ASINs.</li>
        <li>We do not publish prices, ratings or stock states &mdash; those live on Amazon and change daily.</li>
        <li>We do not claim popularity for any product without a dated snapshot link (decision
        <a href="{u('/docs/decisions.html')}#D-19">D-19</a>).</li>
      </ul>
      <h2>Privacy on this site</h2>
      <p>The measurement layer stores aggregate events in your browser only &mdash; no cookies, no advertising
      identifiers, no third-party scripts. If a self-hosted, aggregate-only analytics endpoint is switched on,
      it receives page-view counts, outbound-click counts and scroll-depth buckets &mdash; never identities.
      The <a href="{u('/docs/metrics.html')}">metrics plan</a> documents every event we collect.</p>
    </div></section>"""


def notfound_body():
    return f"""<section class="page-head"><div class="wrap-narrow" style="text-align:center;padding:40px 0;">
      <p class="kicker">404</p>
      <h1>That page isn&rsquo;t on the counter.</h1>
      <p class="lede">The link may be stale &mdash; we publish corrections openly on the
      <a href="{u('/docs/flagged.html')}">Flagged for Review page</a>.</p>
      <div class="hero-cta" style="justify-content:center;margin-top:18px;">
        <a class="btn btn-primary" href="{u('/index.html')}">Back to the front page</a>
        <a class="btn btn-ghost" href="{u('/guides/index.html')}">Browse the guides</a>
      </div>
    </div></section>"""


def pages() -> dict:
    out = {}
    g1, g2, g3, g4 = GUIDES

    out["/index.html"] = (
        "home",
        "The Counter Edit \u2014 Air-fryer decisions, minus the noise",
        "Question-shaped buyer guides to three air fryers and two meat thermometers, with every claim sourced to official Amazon listings. Take the 3-question chooser or read the guides.",
        index_body(),
    )
    out["/guides/index.html"] = (
        "guides",
        "All buyer guides \u2014 The Counter Edit",
        "Every The Counter Edit guide in one place: basket vs oven style, the capacity checklist, cleanup and counter-space trade-offs, and the multi-function reality check.",
        guides_hub_body(),
    )
    for g in GUIDES:
        out[f"/guides/{g['slug']}.html"] = (
            "guides",
            f"{g['title']} \u2014 The Counter Edit",
            g["standfirst"],
            _guide_shell(g, GUIDE_BODIES[g["slug"]]()),
        )
    out["/compare.html"] = (
        "compare",
        "Compare the five \u2014 dual basket, oven-style, single basket, instant-read, wireless | The Counter Edit",
        "A side-by-side comparison of five verified products with a three-question chooser. Facts from official Amazon listings only; unverified cells stay blank and flagged.",
        compare_body(),
    )
    out["/products.html"] = (
        "products",
        "The Shelf \u2014 all five products with their verification record | The Counter Edit",
        "All five products on one shelf: what we verified, when, and from which official Amazon listing. No invented prices, no copied ratings.",
        products_body(),
    )
    out["/about.html"] = (
        "about",
        "About The Counter Edit \u2014 our voice, standards and limits",
        "Why The Counter Edit exists, the voice it is written in, who writes it, and the four things it will never do.",
        about_body(),
    )
    out["/disclosure.html"] = (
        "home",
        "Disclosure policy \u2014 The Counter Edit",
        "How The Counter Edit earns from Amazon Associates links, what rel=sponsored means for readers, and the FTC and Amazon policies we operate under.",
        disclosure_body(),
    )
    out["/404.html"] = (
        "home",
        "Page not found \u2014 The Counter Edit",
        "The page you asked for is not on The Counter Edit. Start from the front page or browse the guides.",
        notfound_body(),
    )
    return out
