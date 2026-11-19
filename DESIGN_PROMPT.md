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
4. No "trending"/popularity claims anywhere reader-facing.
5. Prices and star ratings are not published (F-02), so no design element may imply them.
6. A module that states a figure must carry the date it was read and the listing it came
   from; the build can render both, so no design may drop them.

## Status against the published build (updated 2026-11-19)

Implemented in the `docs/` publication (the live site): the warm-editorial tokens are the
stylesheet (`assets/css/site.css`, token-first, fluid `clamp()` type, 44px tap targets, one
terracotta accent reserved for interaction); the front page leads with a product rail, format
tiles, the guide shelf and then the sourced table; the mobile sticky comparison bar ships on
every reader page (SG-23 path A) and is dismissible; read-date chips appear on product cards and
in the comparison table (SG-22). One deliberate deviation: an unverified value
renders as a muted italic em dash with a link to its flag, not an amber badge —
a badge implies a queue someone is working, and nobody is on payroll here.

Changed since this brief was written: **P4 and P5 are published** — both thermometers were
destination-verified on 2026-11-19 and render as cards and table rows with tagged Special Links
(decision D-P06), so the "held products" constraint above no longer applies to them. The hero
promise line is "Three air fryers, two thermometers, zero guesswork." and the primary CTA is
"Compare all five".

Not adopted, still awaiting a named path in the queue: brand rename (SG-01), verdict/ranking
modules (SG-24), price display (SG-05), product photography (SG-08), seasonal framing (SG-28).

The eight machine-ready design briefs that the queue feeds live in
`data/p2/design-prompts.json` and are published as a page — **Design prompt pack**
(`design-prompt.html`) — with each suggestion's `feeds_design_prompt` field recording which brief
it unblocks. Regenerating a page from a brief must keep the compliance block above intact: the
gate (`tools/checks.py`) is what makes that claim checkable rather than aspirational.
