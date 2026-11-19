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

- Display type: **Fraunces** (optical size 96, soft), fallback Georgia,
  'Iowan Old Style', 'Palatino Linotype', serif
- Body type: **Inter** 17px / 1.65, fallback system-ui, sans-serif
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
- Cards: white surface, 1px rule border, 8px radius max (editorial, not SaaS).
- Tables: rule-separated rows, tabular numerals, sticky header on mobile.
- Disclosure strip: paper-on-rule strip directly under the masthead on every
  page, 15px, ink on paper; repeats in the footer. Never inside a link list.
- Buttons: terracotta fill for primary CTAs; outlined for secondary. 44px
  minimum tap target on mobile.
- Status badges: sage "verified", amber "unverified/held", muted outline
  "carried".
- Imagery: **drawn, not photographed** until the photography decision (Q-05).
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
