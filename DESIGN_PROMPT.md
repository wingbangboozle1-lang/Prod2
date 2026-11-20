# DESIGN_PROMPT.md — the visual brief for Prod2

Reconciled 2026-11-20 against the live registers and the shipped theme
(`assets/css/site.css`). This is the brief a designer — or a rebuild of this site —
should implement. Compliance constraints are non-negotiable and are listed at the end.

**Reconciliation note (closes F-P12).** The earlier version of this file was adopted from the
predecessor "The Crisp Counter" registers and cited ids that do not exist on the live site
(D-01/D-02 as brand decisions, D-15, Q-05, Q-10). On the live registers the wordmark decision is
**D-P03**, name clearance is **Q-19**, the photography question is **Q-P05** with decision
**D-22**, and the visual-direction decision is **D-18**. The ids below now point at the live
register. Where the shipped theme has already moved past this brief, the brief records the
shipped behaviour instead of the older ambition.

## Brand

- **Name:** Prod2 — decision **D-P03** (the project's established name is kept deliberately; a
  consumer-facing rename is queued as **SG-01** and is blocked on clearance, **Q-19**)
- **Descriptor:** Kitchen notes & buying guides
- **Tagline:** What to compare before you buy
- **Promise line (front-page hero):** Three air fryers and two thermometers, chosen by format.
- **Method line:** one sentence stating that every published figure was read from an official
  listing page on a dated pass, and that the receipts stay visible.

## Direction: warm editorial (kitchen magazine that shows its sources)

The shipped theme implements this direction with a single token layer in `assets/css/site.css`.
The values below are the **shipped** ones — a rebuild should reproduce them, not the earlier
ambition of this file.

- **Display type: Fraunces — SHIPPED 2026-11-20**, self-hosted variable woff2
  (`assets/fonts/fraunces-var.woff2`, SIL OFL 1.1, preloaded). Fallback chain:
  'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif.
- **Body type: Inter 17px / 1.65 — SHIPPED** as a self-hosted variable woff2
  (`assets/fonts/inter-var.woff2`). Fallback: system-ui, -apple-system, sans-serif.
- **No font CDN.** A CDN request would contradict the site's own privacy statement; the
  gate now fails on any third-party host in a built page. The typography gap this file used
  to carry (**SG-15**) is closed on the fonts side; the brief itself was reconciled against
  the live registers in the same pass (**F-P12**).

- **Palette tokens** (`--*` in `:root`):
  - surface: `--paper #FBF8F3`, `--paper-deep #F4EDE2`, `--paper-card #FFFFFF`, `--cream #EFE4D4`
  - ink: `--ink #1C1613`, `--ink-soft #3F352E`, `--muted #6E6259`, `--faint #93877C`
  - accent: `--terracotta #C2552F`, `--terracotta-deep #9E3F1F`, `--terracotta-wash #FBEDE6`,
    `--sage #5E7256`, `--sage-deep #44543E`, `--sage-wash #EEF2EA`, `--gold #B08A28`
  - lines: `--rule #E6DACB`, `--rule-strong #D6C6B2`, with three shadow steps
- **Geometry:** `--radius-sm 6px`, `--radius 12px`, `--radius-lg 18px`; content width `--wrap
  74rem`, narrow measure `--wrap-narrow 48rem`. The earlier "8px radius max" rule is superseded
  by the shipped token layer (**SG-16**).
- **Headings:** serif, tight leading, generous top space. **Body:** sans, 17–18px.
- **Hero:** a drawn kitchen illustration (`assets/img/hero-kitchen.png`), the promise line, the
  method line, and two side-by-side calls to action. The image is captioned as an illustration,
  not a product photo.
- **Cards:** white surface, hairline rule border, soft shadow. **Tables:** rule-separated rows,
  tabular numerals, sticky header on mobile.
- **Disclosure strip:** a paper-on-rule strip directly under the masthead on every page, repeated
  in the footer. Never inside a link list.
- **Buttons:** terracotta fill for primary CTAs, outlined for secondary; 44px minimum tap target
  on mobile.
- **Status badges:** sage "verified", amber "unverified/held", muted outline "carried".
- **Imagery:** **drawn, not photographed**, until the photography decision (**Q-P05**, **D-22**).
  Six format illustrations plus the typographic social card are the only graphics. Amazon listing
  photography is Program Content and needs a licence review first.

## Navigation and page order

- **Reader nav (six links, D-10):** Shop · Air fryers · Thermometers · Guides · Compare · About.
- **Owner and reviewer surfaces** live in the single "The work behind it" group and in the footer
  directory: executive summary, method, flagged, questions, suggestions, decisions, measurement,
  compliance, privacy. The release gate fails if the reader nav exceeds seven links.
- **Page order that earns its place:** shop first, then guides, then the register — in that order.

## Mobile-first rules

- Fluid type with `clamp()`; nothing below 16px in body copy.
- Tap targets ≥44px; the nav collapses to a stacked row, not a burger menu of nested groups.
- The comparison table keeps a sticky header row and a sticky anchor bar.
- No horizontal scroll traps: tables scroll inside their own card.

## Anti-slop design constraints

- No badge strips, no fake countdowns, no "X people bought this".
- No star ratings or prices anywhere (F-02; Amazon's Program Policies §2(b) permits a published
  price only when Amazon serves it or it arrives through the Creators/PA API — **D-P11**).
- No stock-collage hero and no product photography in the hero.
- Every figure on a page carries its source and read date.

## Compliance block (do not design around)

1. Disclosure strip above the fold on every page (FTC placement and Associates identification),
   repeated in the footer with the Amazon IP notice (**F-P15**, **D-P13**).
2. Every outbound Amazon link: final destination URL with `tag=shopnow047c-20`,
   `rel="sponsored nofollow noopener"`, no shortener, no redirect wrapper.
3. No price, availability, rating, review count or popularity badge.
4. Every product in the register renders with its destination — there is no "held" state. The
   earlier rule that P4 and P5 never render as links or cards belonged to the predecessor
   registers; both thermometers ship as normal cards on this build.
5. No "trending" or popularity claims anywhere reader-facing (**D-19**).

## Marketing conversion layer (shipped 2026-11-20, D-P10)

The front page reads like a shop, not an audit. Product cards lead the fold above any register or
process explanation. Each product card carries:

- A drawn format illustration with the format label, linked to the official listing
- A "Best for:" line in plain language
- The short listing title and the ASIN in a muted line
- Three listed-feature bullets, each traceable to its source
- A primary CTA button to the official listing (`rel="sponsored"`, `tag=shopnow047c-20`)
- A source line naming the official listing and the re-check date, captioned "Illustration, not the
  product photo"

## Editorial hooks for the guide calendar

Working titles for the question-shaped guide calendar — each is a buyer question, not a claim
about search volume or product superiority. These are the nine guides that ship today:

- "Basket or oven-style air fryer: what to compare" (format decision, decoded)
- "A no-hype checklist for air-fryer capacity" (quarts across formats, made comparable)
- "Cleanup and counter-space trade-offs, assessed" (dimensions and dishwasher-safe parts, before
  the box arrives)
- "Questions to ask before buying multi-function gear" (24 presets, 24 reasons to buy? Count them
  down)
- "How accurate does a meat thermometer need to be?" (±0.5°F vs ±1°F, check-it vs watch-it)
- "How many quarts do you actually need?" (batch math from the listed capacities — not a serving
  count, which no listing states)
- "Two baskets or one: when do two drawers earn their space?" (batch math meets listed specs)
- "Holiday hosting: which format earns the counter?" (big meals, borrowed counter space, eat-in
  waves)
- "Instant-read vs leave-in: which thermometer for which cook" (spot-check vs watch-a-roast)

## Organic traffic hooks

Every guide page is built for search: unique `<title>` and meta description, Article structured
data, canonical URL, and inclusion in both `sitemap.xml` and `feed.xml` by the same build. Search
Console verification meta is emitted when the owner supplies the token (`settings.json`). The feed
covers every guide so subscribers get each new question-shaped article the day it publishes.

## Queued inputs

- **SG-15** — the type gap is closed on the fonts side: Fraunces + Inter are self-hosted
  (variable woff2, SIL OFL 1.1, preloaded, no CDN), shipped 2026-11-20. Marked shipped; the
  brief itself was reconciled against the live registers (**F-P12**) in the same pass.
- **SG-16** — design-token conformance pass against the brief's non-negotiables. Shipped: the
  token layer in `assets/css/site.css` is the record of what conformed.
- **SG-17** — seasonal front-page merchandising scaffolding (grilling, gifting), gated on the
  seasonal-window question **Q-P07**; calendar-based framing only, per the evidence rule
  **D-19**.
- **SG-31** — three fully specified directions for the next visual pass, shipped.
