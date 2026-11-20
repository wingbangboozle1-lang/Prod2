# DECISIONS.md — Decision Log

Tracking ID: `shopnow047c-20`. Domain: `https://wingbangboozle1-lang.github.io/Prod2`.

This file mirrors `data/p2/decisions.json`, which is what the site renders on the
**Decisions** page. The register is authoritative; this file is the reviewer's summary.

> **Corrected 2026-11-20 (D-P15):** this file previously carried a decision table that no
> longer described the shipped site — it named the brand **Countercraft**, said prices were
> published "as listed with a date", and said ratings were shown where captured. None of
> those is true of the live publication, which publishes no prices and no ratings and uses
> the `Prod2` wordmark. The table below was rebuilt from `data/p2/decisions.json` on
> 2026-11-20. The stale table was wrong, not the site.

## Taken — foundational

| ID | Decision | Rationale | Source |
| --- | --- | --- | --- |
| D-01 | Five supplied short links resolved to five official listings, which are the products covered | Owner-supplied catalogue | `data/p2/intent-links.json` |
| D-05 | Every outbound product link is a tagged Special Link with `rel="sponsored"` | Program Policies §2(b); Google outbound-link guidance | S-POL, S-GOUT |
| D-06 | No hands-on testing is claimed; the site is an edited buying guide | Nothing was purchased or tested | Brief |
| D-12 | Privacy-preserving click counter: no cookies, five defined events | Measurement without third-party tracking | Brief |
| D-14 | Compliance checks are automated in the release gate, not remembered | A rule that is not enforced is a rule that lapses | Brief |
| D-17 | One canonical published site; parallel builds are archived | Avoid duplicate content | INT-06 |
| D-18 | Keep the `Prod2` wordmark until name clearance is settled | Naming is a legal question (Q-19) | Q-19 |
| D-19 | No popularity, sales-volume or ranking claim without a dated official snapshot | Google spam policies; Program Policies | S-GSPAM |
| D-21 | No published star ratings | Ratings require the licensed API | S-POL |
| D-22 | Campaign ledger starts empty; only authorized first-party rows | No forecast without a report | Brief |
| D-23 | Three-question chooser routes to a format, never to a checkout | Uses published listed values only | Brief |
| D-26 | Counter-space analysis is published as a formula, not a score | A ratio a reader can check | Brief |
| D-27 | Guides are question-shaped, one question per page | Search intent | S-GHELP |

## Taken — publication and design passes

| ID | Date | Decision |
| --- | --- | --- |
| D-P07 | 2026-11-19 | Publication pass: shop-first front page, guides hub, eight-topic calendar, seasonal desks, clusters, RSS, Search Console readiness, consent-gated capture form |
| D-P08 | 2026-11-19 | Reader-capture form ships disconnected: nothing is transmitted until a consent basis exists |
| D-P09 | 2026-11-19 | Root mirror retained because Pages serves the repository root in legacy mode |
| D-P10 | 2026-11-20 | **Shop-first design rebuild.** New design system, drawn format illustrations, front page led by products, new `shop.html` shelf with filters and chooser, new `about.html` with authorship and four rules, reader nav cut from 11 links to 6, gate extended to protect all of it |
| D-P11 | 2026-11-20 | **The dated-snapshot price policy (SG-05) is refused by the policy text.** Program Policies §2(b) permits published prices only when Amazon serves them or they arrive via the Creators/PA API. Dated snapshots are neither, so prices stay unpublished. Closes Q-27 |
| D-P12 | 2026-11-20 | No Amazon listing photography. Illustrations are drawn for the site, generic to the product format, and captioned as such |
| D-P13 | 2026-11-20 | Disclosure adopts the prescribed first-person sentence from Operating Agreement §5 |
| D-P14 | 2026-11-20 | The thermometer guide publishes USDA/FoodSafety.gov safe-temperature, storage and power-outage data, quoted with last-reviewed dates |
| D-P15 | 2026-11-20 | This file rebuilt from the register after drifting from the shipped site (see the note above) |

## Open — a choice is waiting

| ID | Question | What is missing | Recommended path |
| --- | --- | --- | --- |
| Q-01 | Is the Associates account enrolled under `shopnow047c-20`, and has each link been validated in it? | Access to Associates Central | Owner: generate one Special Link, test one click, read the report |
| Q-19 | Is the site's trade name cleared, and does it contain an Amazon Mark? | Trademark search | Clear a name before renaming (SG-01) |
| Q-23 | Where can the self-hosted analytics endpoint run? | Hosting choice | Any Node host; GitHub Pages cannot run it |
| Q-27 | May the site publish prices under a dated-snapshot rule? | — | **Answered: no.** See D-P11 |
| Q-31 | Is P2's preset count 24 or 25? | The listing body copy | The title states 24; the body was not captured in enough detail to settle it |
| Q-47 | May the site collect an email address, and on what consent text? | A privacy decision | Settle before enabling the capture form |
| Q-P02 | Which question-shaped guide comes next, chosen on evidence? | 14 days of search data | Search Console first (SG-29) |
| Q-P05 | Is any product imagery usable, and through which official channel? | The IP Licence read for imagery | Stay with drawn illustrations until read |
| Q-P06 | Does the owner control a domain? | Owner answer | Needed for Search Console and the endpoint |
| Q-P08 | Who verifies the site in Search Console, and when? | Owner action | Owner adds the token to `settings.json`; the build emits the meta tag |
| Q-P09 | Which design direction ships? | — | **Answered: the editorial shop direction.** See D-P10 |

## Standing rules (not up for a vote)

1. Disclosure under the masthead on every page, repeated in the footer.
2. Every outbound product link carries `rel="sponsored"` and the Associates tag.
3. No published price or star rating.
4. No value is inferred. A blank plus a flag beats a guess.
5. A build that fails the gate does not deploy.

## See also

- `data/p2/decisions.json` — the register the site renders.
- `data/p2/flags.json` — every irregularity, with an evidence link.
- `data/p2/verification-2026-11-20.json` — the live re-verification records.
- The **Flagged for review**, **Open questions** and **Suggestions** pages on the site.
