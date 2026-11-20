# DESIGN_PROMPT.md — the visual brief for The Crisp Counter

Adopted 2026-11-19 (decisions D-01/D-02), carrying the predecessor register's
warm-editorial direction (DIR-A, data/design.json there). This file is the
brief a designer (or a rebuild of this site) should implement. Compliance
constraints are non-negotiable and listed at the end.

## Brand

- **Name:** The Crisp Counter (decision D-01; clearance check open as Q-10)
- **Tagline:** Air fryer decisions, minus the hype.
- **Promise line (front-page hero, ≤9 words):** Three air fryers. Every fact checked.
- **Method line:** one sentence under the promise stating that every published
  figure was read from an official listing page and the receipts stay visible.

## Direction: warm editorial (kitchen magazine that shows its sources)

- Display type: **Fraunces** — SHIPPED 2026-11-20, self-hosted variable woff2
  (`assets/fonts/fraunces-var.woff2`, SIL OFL 1.1, preloaded). Fallback chain:
  'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif.
- Body type: **Inter** 17px / 1.65 — SHIPPED as a self-hosted variable woff2
  (`assets/fonts/inter-var.woff2`). Fallback: system-ui, -apple-system, sans-serif.
- **No font CDN.** A CDN request would contradict the site's own privacy statement; the
  gate now fails on any third-party host in a built page.
- Palette tokens:
  - ink `#241C17` (text)
  - paper `#FBF7F1` (page background)
  - card `#FFFFFF` (surfaces)
  - terracotta `#C4613C` (accent, links, CTAs)
  - sage `#6F7F63` (verified/positive states)
  - rule `#E7DDD1` (hairlines, table rules)
  - muted `#6B6058` (secondary text)
  - amber `#B98A2F` (unverified/attention states)
- Headings: serif, tight leading, generous top space. Body: sans, 17–18px.
- Hero: paper background, no photography tint, promise + method line + two
  side-by-side calls to action ("Compare the three", "Read the guides").
- Cards: white surface, 1px rule border, restrained radius (editorial, not SaaS).
- Tables: rule-separated rows, tabular numerals, sticky header on mobile.
- Disclosure strip: paper-on-rule strip directly under the masthead on every
  page, 15px, ink on paper; repeats in the footer. Never inside a link list.
- Buttons: terracotta fill for primary CTAs; outlined for secondary. 44px
  minimum tap target on mobile.
- Status badges: sage "verified", amber "unverified/held", muted outline
  "carried".
- Imagery: **illustration and drawn glyphs, never manufacturer photography** (standing rule
  F-P17/F-P18 lineage; decision pending Q-P05).
  Line-art air-fryer glyphs, the og-image card, and the favicon are the only
  graphics.

## Mobile-first rules (D-15)

- Fluid type with `clamp()`; nothing below 16px in body copy.
- Tap targets ≥44px; nav collapses to a simple stacked row, not a burger menu
  of nested groups.
- The comparison table keeps a sticky header row and a sticky anchor bar
  (Chooser · Table · How to read · Statuses).
- No horizontal scroll traps: tables scroll inside their own card.

## Anti-slop design constraints

- No badge strips, no fake countdowns, no "X people bought this".
- No star ratings or prices anywhere (register rule - carried, F-02/6(t)).
- No stock-collage hero. The hero is type on paper.
- Every module earns its place: shop, guides, method, data - in that order.

## Compliance block (do not design around)

1. Disclosure strip above the fold on every page (FTC placement + Associates
   identification), repeated in the footer with the Amazon IP notice.
2. Every outbound Amazon link: final destination URL + `tag=shopnow047c-20`,
   `rel="sponsored"`, no shortener, no redirect wrapper.
3. No price, availability, rating, review count or popularity badge.
4. Held products (P4/P5) never render as links, cards or rows with destinations.
5. No "trending"/popularity claims anywhere reader-facing.

## Marketing conversion layer (added 2026-11-20 — shop-forward polish)

The front page must read like a shop, not an audit. Product cards lead the
fold above any register or process explanation. Each product card carries:

- A human-readable format label ("Dual-basket air fryer", not "P1")
- The short listing title (no price, no rating — compliance rule)
- Three listed-feature bullets, each traceable to its source
- A primary CTA button to the official listing (`rel="sponsored"`,
  `tag=shopnow047c-20`, destination URL — no shortener)
- A secondary "see specs" link to the products page

## Catchy trendy article hooks (editorial hypotheses, not popularity claims)

Working titles for the question-shaped guide calendar — each is a buyer
question, not a claim about search volume or product superiority:

- "Basket or oven-style air fryer: what should you compare?" (format
  decision, decoded)
- "A no-hype checklist for comparing air fryer capacity" (quarts lie across
  formats — make them mean the same thing)
- "How to assess cleanup and counter-space trade-offs" (dimensions +
  dishwasher-safe parts, before it arrives)
- "Questions to ask before buying a multi-function kitchen appliance" (24
  presets, 24 reasons to buy? Count them down)
- "How many quarts do you actually need?" (serving-count sanity check from
  listed capacities)
- "Two baskets or one: when do two drawers earn their space?" (batch math
  meets listed specs)
- "How accurate does a meat thermometer need to be?" (±0.5°F vs ±1°F,
  check-it vs watch-it)
- "Instant-read vs leave-in: which thermometer for which cook" (spot-check
  vs watch-a-roast-from-your-phone)
- "Holiday hosting: which format earns the counter?" (big meals, borrowed
  counter space, eat-in waves)

## Organic traffic hooks

Every guide page is built for search: unique `<title>` + meta description,
FAQPage + Article structured data, canonical URL, and inclusion in both
`sitemap.xml` and `feed.xml` by the same build. Search Console verification
meta is emitted when the owner supplies the token (settings.json). The feed
covers every guide so subscribers get each new question-shaped article the
day it publishes.

## Queued inputs (2026-11-19)

The suggestion queue now carries three design items that feed this brief
(proposed only — pick a path on the Suggestions page before anything here
is built):

- **SG-15** — close the type gap: ship Fraunces + Inter self-hosted, or
  record a substitution decision. Reconcile this brief's cross-references
  first: flag **F-P12** records that the ids cited above (D-01/D-02, D-15,
  Q-05, Q-10) belong to the predecessor registers, not the live ones — on
  the live site D-01 is the Special Links decision, name clearance is Q-19,
  the photography question is Q-P05 with decision D-22 (carried, open), and
  the shipped wordmark is "Prod2" (D-P03) while clearance is open.
- **SG-16** — design-token conformance pass: audit this brief line by line
  against the shipped theme (card radius, 44px tap targets, sticky mobile
  anchors, disclosure-strip treatment) and conform or amend, once, recorded
  as a decision.
- **SG-17** — seasonal front-page merchandising scaffolding (grilling,
  gifting), gated on the seasonal-window question Q-P07; calendar-based
  framing only, per the evidence rule D-19.

## Marketing inputs — session arena/44af3083-prod2 (2026-11-20)

Proposals only. Each is queued on the Suggestions page (SG-49, SG-50, SG-51); pick a path
there before anything in this section is built.

1. **"The newest question" slot (SG-49).** One module above the shelf on the front page:
   the latest published guide's question headline, its one-sentence answer, one link.
   Rotates from the build's guide order — no new data, no publish-time editorial work. It
   gives the front page the pulse of a publication with a cadence instead of a fixed catalogue.
2. **CTA language for the no-price world (SG-51).** With prices and ratings withheld (F-02),
   the buy button copy is the entire conversion layer. Specify three compliant label variants
   ("See today's price on Amazon" is truthful under Program Policies 2(b) — Amazon shows the
   price), keep the paid-link label attached, and rotate behind the outbound_click event once
   the measurement gate (SG-06) opens. No variant may imply a price, rating or availability
   the site cannot see.
3. **Re-verification as a trust signal (SG-50).** The dated-read discipline is the site's
   stated differentiator (SG-37). The design should surface it: a "last checked" date on
   product cards is already rendered (`last_live_read`) — keep it prominent in any card
   redesign, and give the verification record a visible home on the Method page.

Article-template shape to preserve in any redesign (two guides shipped this session proved
it repeatable at cadence): question as the title, the answer in the first screen, listed
facts each carrying its source and read date, a "What we could not verify" callout, a
one-sentence-answer callout, and a short "Keep reading" list that reaches the comparison,
the buying guide and the cluster pillar.
