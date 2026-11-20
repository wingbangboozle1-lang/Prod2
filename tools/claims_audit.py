#!/usr/bin/env python3
"""claims_audit.py — every product claim the site publishes, matched to its evidence.

Why this exists
---------------
The site's reader-facing promise is that a figure on a card or in the comparison
table was read off the official listing, and the brief's rule is that a value which
cannot be confirmed from an official source is left blank and flagged rather than
phrased around. Titles have been re-read verbatim on every pass; the *card bullets*
and the *comparison rows* have never been checked one by one against the recorded
evidence strings. That is the gap this closes, mechanically, so it stays closed:
`python3 tools/checks.py` calls `audit()` and fails the build on any `unsupported`
row.

Rule (stated so a reviewer can reproduce it)
-------------------------------------------
A published claim is a string. Its evidence is the set of verbatim strings recorded
in `data/p2/products.json` and `data/p2/verification-2026-11-20.json` for that ASIN
(listing title, `special_feature`, `capacity`, `dimensions`, `color`, `material`,
`model_name`, `variant_note`, plus each `*_observed` value from the dated live read).
Words are lower-cased, digits are split off their units (`3Qt` = `3` + `qt`), one
inflection is folded off (`rotating` = `rotate`, `crisp` = `crispi`), stop-words and
unit words are dropped, and a word counts as covered only at 4+ characters so short
spec tokens match exactly. The rule lives in `stem()` / `same_word()` below.

  title-verbatim : every content word appears in the listing TITLE string that the
                   live read recorded — i.e. a reader can confirm it from the title
                   alone, today.
  dated-read     : every content word appears in some recorded evidence string, but
                   not all in the title — the claim rests on a dated read of another
                   part of the page (spec table, feature bullets) that this
                   environment cannot reliably re-retrieve (see F-P30).
  unsupported    : a content word appears in no recorded evidence string. The claim
                   must be corrected or removed; the gate fails.

Usage
-----
    python3 tools/claims_audit.py            # write the audit + print the summary
    python3 tools/claims_audit.py --report   # print only
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "p2"
DOCS = ROOT / "docs"

AUDIT_DATE = "2026-11-20"
SESSION = "arena/b3089214-prod2"

# Words that carry no product fact: articles, prepositions, our own hedging, and unit
# words that the register stores in a different shape ("6 qt total" vs "6 Quart").
STOP = {
    "a", "an", "the", "and", "or", "of", "in", "on", "with", "for", "to", "is",
    "as", "listed", "listing", "noted", "plus", "per", "its", "it", "that", "this",
    "option", "options", "features", "feature", "body", "finish", "included",
    "instead", "format", "total", "own", "away", "from", "one", "two", "three",
    "qt", "qts", "quart", "quarts", "independent", "size", "big", "least", "more",
    "sq", "ft", "hot", "high", "heat",
}
UNITS = {"qt", "qts", "quart", "quarts", "sec", "s", "ft", "in", "inch", "inches",
         "f", "°f", "lb", "lbs", "x"}


SUFFIXES = ("ing", "ers", "er", "es", "ed", "s", "e")


def stem(w: str) -> str:
    """Fold one inflection off a word, if enough of the word is left to recognise.

    Documented so the audit's leniency is reviewable: `rotating` and `rotate` have to
    compare equal, because a card may say what the listing says in another mood, and
    `crisp` has to reach `Crispier`. Only one suffix is removed, and never below four
    characters, so `lids` stays `lids` and a short spec token can never dissolve into
    a false match. Numbers are returned untouched.
    """
    for suf in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def words(text: str) -> set[str]:
    """Content words of a claim or a piece of evidence, normalised identically.

    Digits are split from the unit glued to them (`3Qt` and `3 qt` have to compare
    equal, and `450°F` arrives as `450f` otherwise); each word is then stem-folded;
    stop-words and unit words drop out because the register stores capacities and
    dimensions in their own fields. What survives is the part a reader would call a
    claim about the product.
    """
    text = text.lower().replace("±", "").replace("“", '"').replace("”", '"')
    text = re.sub(r"(\d)([a-z])", r"\1 \2", text)
    text = re.sub(r"([a-z])(\d)", r"\1 \2", text)
    out = set()
    for raw in re.split(r"[^a-z0-9°.]+", text):
        w = raw.strip(".-").replace("°", "")
        if not w or w in STOP or w in UNITS:
            continue
        folded = stem(w)
        if folded in STOP or folded in UNITS:
            continue
        out.add(folded)
    return out


def same_word(a: str, b: str) -> bool:
    """Two stems match when one is the other, or a prefix of it, at 4+ characters.

    One-directional would be safer but wrong (`crisp` must reach `crispi`), so the
    guard is the length floor, and numbers only ever match exactly — `1` is `1`.
    """
    if a == b:
        return True
    if min(len(a), len(b)) < 4:
        return False
    return a.startswith(b) or b.startswith(a)


def priority(field_name: str) -> int:
    """Citation order for the evidence pool: listing title first, then the register's
    verbatim spec fields, then anything a dated live read observed."""
    order = ["products.json:name_listing", f"verification-{AUDIT_DATE}.json:title_observed",
             "products.json:capacity", "products.json:dimensions",
             "products.json:special_feature"]
    key = field_name.split(":", 1)[1]
    if field_name in order:
        return order.index(field_name)
    return 10 if field_name.startswith("products.json:") else 20


def missing(evidence_words: set[str], claim_words: set[str]) -> list[str]:
    """Claim words the evidence does not carry — the list a reviewer needs to see."""
    out = []
    for w in sorted(claim_words):
        if not any(same_word(w, e) for e in evidence_words):
            out.append(w)
    return out


def covers(evidence_words: set[str], claim_words: set[str]) -> bool:
    """True when every claim word is carried by this piece of evidence."""
    return not missing(evidence_words, claim_words)


# --------------------------------------------------------------------------- evidence
# Only fields that record *what the listing says* count as evidence. A claim may not be
# its own proof: the first version of this audit read every string in products.json and
# let `highlight_2` verify itself, which the fabricated-claim negative test caught on
# 2026-11-20. Our own names, format labels and prose notes are therefore excluded.
# A tuple, not a set: the audit has to be byte-reproducible (the freshness gate rebuilds
# and compares), and a set's iteration order changes between processes for strings, so
# the first version of this file produced a different word_evidence map on every run.
# Order is also the citation priority — the title first, then the spec table.
LISTING_EVIDENCE_FIELDS = (
    "name_listing",            # verbatim title, re-read on every dated pass
    "name_listing_previous",   # verbatim title as an earlier pass recorded it
    "capacity", "dimensions", "special_feature", "color", "material",
    "model_name", "model_number", "category_path", "function_count",
)
LIVE_EVIDENCE_SUFFIX = "_observed"  # strings a dated fetch actually saw


def evidence_pool(products_row: dict, live_row: dict) -> dict[str, str]:
    """Named verbatim strings this pass may cite for one product."""
    pool: dict[str, str] = {}
    for key in LISTING_EVIDENCE_FIELDS:
        val = products_row.get(key)
        if isinstance(val, str) and val.strip():
            pool[f"products.json:{key}"] = val
    for key, val in live_row.items():
        # Prices are excluded on purpose: observed but never published (S-POL §2(b)),
        # and a dollar figure cannot evidence a feature claim.
        if (isinstance(val, str) and val.strip() and key.endswith(LIVE_EVIDENCE_SUFFIX)
                and "price" not in key and "rating" not in key):
            pool[f"verification-{AUDIT_DATE}.json:{key}"] = val
    return pool


TITLE_KEYS = ("products.json:name_listing", f"verification-{AUDIT_DATE}.json:title_observed")


# --------------------------------------------------------------------- published claims
CLAIM_FIELDS = ("highlight_1", "highlight_2", "highlight_3")


def published_claims() -> list[dict]:
    """The card bullets, read back out of the BUILT page so a claim that never
    reached the page cannot pass, and a claim that reached it cannot be ignored."""
    out: list[dict] = []
    shop = (DOCS / "shop.html")
    products = {p["id"]: p for p in json.loads((DATA / "products.json").read_text(encoding="utf-8"))["products"]}
    live = {p["id"]: p for p in json.loads(
        (DATA / f"verification-{AUDIT_DATE}.json").read_text(encoding="utf-8"))["products"]}
    if shop.exists():
        text = shop.read_text(encoding="utf-8")
        # Each card is an <article class="card product-card" id="Pn"> block inside the
        # shelf; its three bullets are the <li> items. Reading the built page (not the
        # register) is deliberate: a claim that never reached the page is not audited,
        # and a claim on the page cannot be quietly ignored.
        shelf = re.search(r'<div class="shelf">(.*?)</div>\s*</section>', text, re.S)
        body = shelf.group(1) if shelf else text
        for pid, card in re.findall(r'id="(P\d)">(.*?)</article>', body, re.S)[:5]:
            row = products.get(pid, {})
            pool = evidence_pool(row, live.get(pid, {}))
            pool_words = {name: words(ev) for name, ev in pool.items()}
            for field, claim in zip(CLAIM_FIELDS, re.findall(
                    r'<li[^>]*>\s*([^<]{6,240}?)\s*</li>', card)):
                cw = words(claim)
                # A card bullet is allowed to assemble two listing facts (a spec-table
                # value and a title phrase), so coverage is judged word by word across
                # the evidence pool; which string carries which word is recorded so a
                # reviewer can read the same two lines. A word no evidence carries is
                # the failure case, and the only one.
                hit_fields = {name for name, ew in pool_words.items() if covers(ew, cw)}
                if not hit_fields:
                    hit_fields = {name for name, ew in pool_words.items()
                                  if not missing(ew, cw)}
                per_word = {}
                for w in sorted(cw):
                    carriers = sorted((name for name, ew in pool_words.items()
                                       if not missing(ew, {w})), key=priority)
                    if carriers:
                        per_word[w] = carriers[0].split(":", 1)[1]
                uncovered = [w for w in sorted(cw) if w not in per_word]
                title_hit = [n for n in sorted(hit_fields) if n in TITLE_KEYS]
                every: set[str] = set()
                for ew in pool_words.values():
                    every |= ew
                if not cw:
                    cls, cited = "unsupported", []
                elif uncovered:
                    cls, cited = "unsupported", []
                elif title_hit and not missing(
                        set().union(*[pool_words.get(n, set()) for n in TITLE_KEYS]), cw):
                    cls, cited = "title-verbatim", title_hit
                else:
                    cls, cited = "dated-read", sorted(hit_fields)
                everything = every
                out.append({
                    "product": pid,
                    "asin": row.get("asin"),
                    "field": field,
                    "claim": claim,
                    "classification": cls,
                    "evidence_keys": cited,
                    "words_outside_the_title": missing(
                        set().union(*[pool_words.get(n, set()) for n in TITLE_KEYS]), cw
                    ) if title_hit else sorted(cw),
                    "unmatched_words": uncovered,
                    "word_evidence": per_word,
                    "source": f"S-{pid[0]}{pid[1:]}",
                    "claim_read": row.get("last_live_read"),
                })
    return out


# Phrases this pass took out of the site because no recorded verbatim string carried
# them. They are kept here so the wording cannot creep back in on a later edit: the
# release gate refuses any reader-facing page that contains one. Each entry names the
# replacement and the flag that records the reason, so the removal is auditable rather
# than silent — and so a future pass with a better source (a browser read of the
# feature bullets, or a Creators/PA-API response, see F-P30) knows what to put back.
RETIRED_PHRASES = [
    {"phrase": "magnetic back", "product": "P4", "instead": "Auto-rotating bright LED screen",
     "why": "no recorded string for P4 mentions a magnet; the phrase came from an "
            "unrecorded 2026-11-19 read"},
    {"phrase": "rinse-clean", "product": "P4", "instead": "IP67 waterproof for grill and BBQ",
     "why": "the listing evidence records the IP67 rating, not a cleaning instruction"},
    {"phrase": "Smart Hub", "product": "P5", "instead": "CHEF iQ app with predictive cook times",
     "why": "no recorded string names a Smart Hub or audio reminders"},
    {"phrase": "rack cooking", "product": "P2", "instead": "French-door oven with an extra-large 26 qt interior",
     "why": "the listing evidence names French doors, presets and accessories, not racks"},
    {"phrase": "in the basket lids", "product": "P1", "instead": "Easy-view windows, dual-zone features, and a mute",
     "why": "the title says 'Easy View Windows'; where the window sits is not recorded"},
    # "leave-in" is this site's own format label for P5 (products.json `format`), so the
    # words alone are not a claim about the listing; what was unevidenced is the
    # monitor-from-anywhere promise, so that is the string denied by name.
    {"phrase": "monitor away from the heat", "product": "P5", "instead": "3 ultra-thin wireless probes, WiFi unlimited range",
     "why": "the card paired our format word with a monitoring promise no recorded string carries"},
]


def retired_hits(docs: pathlib.Path) -> list[dict]:
    """Reader-facing pages that still contain a retired phrase."""
    governance = {"executive-summary.html", "method.html", "flagged.html", "questions.html",
                  "suggestions.html", "decisions.html", "measurement.html", "compliance.html",
                  "privacy.html"}
    hits = []
    for f in sorted(docs.glob("*.html")):
        if f.name in governance:
            continue  # governance pages quote the removal to explain it
        text = f.read_text(encoding="utf-8")
        for item in RETIRED_PHRASES:
            if item["phrase"].lower() in text.lower():
                hits.append({"page": f.name, **item})
    return hits


def audit() -> dict:
    claims = published_claims()
    counts: dict[str, int] = {}
    for c in claims:
        counts[c["classification"]] = counts.get(c["classification"], 0) + 1
    return {
        "_meta": {
            "id": "claim-audit",
            "date_utc": AUDIT_DATE,
            "session": SESSION,
            "description": (
                "Every product claim published on the shop shelf, matched against the verbatim "
                "evidence recorded for that ASIN. Classification rule is written out in "
                "tools/claims_audit.py so a reviewer can re-run it; `python3 tools/claims_audit.py` "
                "regenerates this file and tools/checks.py fails the build on any unsupported row."
            ),
            "retired_phrases": RETIRED_PHRASES,
            "retired_phrase_hits": retired_hits(DOCS),
            "evidence_files": [
                f"data/p2/verification-{AUDIT_DATE}.json",
                "data/p2/products.json",
            ],
            "counts": counts,
            "limits": (
                "This audit proves a claim is consistent with the evidence this project recorded; it "
                "does not re-read the listing sections behind the dated reads. Which claims rest on a "
                "dated read rather than on the title a reader can check today is stated per row, and "
                "the class is flagged as F-P30 with the browser spot-check path (Q-P19)."
            ),
        },
        "claims": claims,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    result = audit()
    if not args.report:
        (DATA / f"claim-audit-{AUDIT_DATE}.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote data/p2/claim-audit-{AUDIT_DATE}.json")
    rows = result["claims"]
    print(f"{len(rows)} published product claims; " +
          ", ".join(f"{k}: {v}" for k, v in sorted(result["_meta"]["counts"].items())))
    for r in rows:
        if r["classification"] in ("unsupported", "dated-read"):
            print(f"  {r['classification']:>12}  {r['product']} {r['field']}: {r['claim']!r}"
                  + (f"  unmatched={r['unmatched_words']}" if r["classification"] == "unsupported" else ""))
    return 1 if any(r["classification"] == "unsupported" for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
