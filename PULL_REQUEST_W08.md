## What this PR does

The site was already correct and already looked like a shop. This pass answers the question the last
two passes left open: **why would anyone read it?** It ships two long-form pieces that carry an
argument instead of repeating the method, and it fixes the measurement machinery that would have
hidden whether those pieces worked.

**Gates, all green from this branch:** `tools/build.py && tools/checks.py` → **ALL CHECKS PASSED**
(30 pages, 13 sections) · `scripts/build_site.py && scripts/verify_site.py` → **VERIFY OK, 18 pages**
· `npm test` → **3/3** · root mirror byte-identical to `docs/` (30/30 files, same hashes).

---

### 1. A real defect, fixed rather than disclosed

The site publishes a five-event measurement contract. The only collector in this repo —
`server.mjs` — answered **400** to three of those five (`guide_read_75`, `category_click`,
`feed_click`) and keyed every page view as `page_view|/unknown`. Hosting it unchanged would have
silently dropped two thirds of the site's measurement, with no error any reader could see.

The previous gate printed this as a **note** and passed the build.

| Before | After |
| --- | --- |
| 3 of 5 events rejected; page views collapse to `/unknown` | All 5 accepted and correctly keyed |
| Gate prints a warning, build passes | Gate **fails** on any divergence |
| Nothing prevents the two lists drifting | A test reads the five names out of `assets/js/measure.js` |

The site's events win, not the collector's: renaming them would have made the published register
wrong. The collector keeps its older Countercraft names so no existing client breaks, and now bounds
every value it stores (10-character ASIN pattern, slug-validated category, cleaned path).

`F-P23` resolved · `Q-P14` answered · `D-P21` recorded · `SG-41` shipped.

### 2. Two long reads, sourced to guidance the listings do not carry

The ten guides run 436–814 words and each ends by restating the same rule: every figure is sourced.
That is a method, not a reason to visit. Both new pieces make a claim a buyer cannot get from a
listing.

| Piece | Words | Spine | Official sources (all read 2026-11-20) |
| --- | --- | --- | --- |
| `article-thermometer-placement.html` | 1,295 | Probe **placement** matters more than stated precision — a ±0.5 °F probe in the wrong spot is a precise wrong answer | USDA FSIS *Food Thermometers*; FSIS *Safe Minimum Internal Temperature Chart* (updated 2025-04-14) |
| `article-air-fryer-doneness.html` | 1,212 | Internal temperature, not capacity or wattage, decides whether an air fryer worked — and a bigger basket is **not** a bigger batch | Nebraska Extension *Food Safety Tips for Air Fryers* (peer-reviewed, updated 2025); same FSIS chart |

Both carry the site's mandatory "what we could not verify" block (real-world accuracy of either unit,
currency of the NIST/NSF certification claim, cooking times, accessory care instructions), are in the
sitemap, the feed and JSON-LD, and are linked from both category pillars and three guides.

New source ids: `S-FSIS-CHART`, `S-FSIS-THERMO`, `S-UNL-AIRFRYER`.

### 3. Decision surfaces a reviewer can actually act on

- **The suggestions page now opens with five ranked rows**, not 38 proposals in registry order. Ranked
  by unblocked-work-per-hour: **Pages source (one dropdown)** → analytics + Search Console → name
  clearance → the email-consent question → the payoff step. Each row states the cost, whether it is
  reversible, and the exact owner action.
- **Three new open questions** with the cheapest route to each answer: `Q-P15` (is there a length
  standard — and is length even the right control?), `Q-P16` (can this project show a real product
  photo at all? one test settles it), `Q-P17` (where does the endpoint run, and who pays).
- **`SG-46` is now the top recommendation on the board.** Flipping Pages to the Actions artifact is a
  single dropdown, closes `F-P19`/`F-P20`, and removes the duplicate copy of every page that this repo
  commits on every pass. It was buried at position 30-something.

### 4. Line-by-line re-verification (2026-11-20)

All five listings re-fetched and compared field by field against the register.

- **Titles: verbatim match for P1–P5** — including ThermoMaven, whose second segment `F-P01` had
  recorded as differing; it now reads exactly as the register has it.
- **Breadcrumbs: match for P1, P3, P4, P5.** P2's breadcrumb did not appear in the fetched variant and
  **stays null** — not inferred.
- **Every published dimension** cross-checked programmatically against the register: `13.38 / 11.81 /
  10.63` (P1), `16.9 / 15.8 / 14.8` (P2), `12.75 / 13.5 / 10` (P3). No unexplained inch value appears
  on any page.
- **No published value changed.**

**One thing worth flagging to the owner:** on these fetches, the `$` figures on an Amazon listing page
belong to *other* ASINs in "customers also viewed" carousels and protection-plan blocks. That is
exactly the attribution trap `F-P17` records, and a live demonstration of why prices and ratings stay
blank (`F-02`, `D-P10`). Any future pass that copies a price string from a fetched listing would
publish a competitor's price as this product's.

### 5. Gate additions

New **`longreads`** section: the registered piece must exist, show ≥3 inline source markers, carry its
unverified block, cite only allow-listed official hosts, and appear in both sitemap and feed.
The **`measurement`** section additionally asserts that the depth event covers `article-*` pages — the
old check silently ignored them, so both new pieces would have been unmeasured.

Also fixed: the executive summary carried counts from two passes ago (28/15/32/27/9) and still named
the project by its codename. Corrected to the rendered values (38/21/37/32, 10 guides + 2 long reads,
13 gate sections).

---

## Sources used

[USDA FSIS — Food Thermometers](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/kitchen-thermometers) ·
[USDA FSIS — Safe Minimum Internal Temperature Chart](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart) ·
[Nebraska Extension — Food Safety Tips for Air Fryers](https://food.unl.edu/free-resources/newsletters/food-safety-tips-electric-air-fryers/) ·
[The five Amazon listings](https://www.amazon.com/dp/B0CDY277D3) ·
[Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies)

## Flagged irregularities (published, non-blocking)

Published on the [Flagged for review](https://wingbangboozle1-lang.github.io/Prod2/flagged.html) page
with source links, per the standing rule:

1. **`F-P23`** — the collector rejected three of five published events. Fixed and resolved this pass.
2. The depth event did not cover `article-*` pages. Fixed; now gated.
3. The executive summary drifted two passes out of date. Corrected.
4. Amazon fetches misattribute neighbouring ASINs' prices. Recorded; the site keeps prices blank.

## Coordination

`COORDINATION.md` carries the full claim (W-01…W-08), the results, the files touched and the handoff
note. **Open PR #35 was logged, not touched**: still `CONFLICTING` at 06:45 UTC with its last commit at
06:27 UTC — inside its own claim window. Its scope overlaps every reader-facing surface here, so its
author must rebase and reconcile by hand; the board quotes the exact time the handoff rule makes it
available (07:27 UTC).
