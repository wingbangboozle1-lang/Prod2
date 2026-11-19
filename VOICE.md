# VOICE.md — how this site speaks

Every reader-facing sentence on this site is written to this standard. The
anti-slop lint in `check.py` enforces the banned patterns on reader-facing
pages; a build that breaks voice fails its own checks.

## The voice in one paragraph

A practical friend who reads spec sheets for fun and refuses to be sold to.
Specific over generic, numbers over adjectives, trade-offs over verdicts.
Says plainly what is known, where it came from, and what is not known.
Second person. Short sentences. Everyday American English.

## Rules

1. **Answer first.** The question is the title; the answer starts the first
   screen. No wind-up paragraphs.
2. **Name the source.** A product fact appears only with its register citation
   ("as listed on the official page, read 2026-11-16").
3. **Admit the limit.** "We haven't lab-tested this" is allowed and used. No
   invented authority, no fake hands-on anecdotes, no fabricated personas.
4. **No hype.** Banned on reader-facing pages: trending, best-selling, most
   popular, top-rated, viral, #1, game-changer, must-have, ultimate guide,
   seamless, cutting-edge, elevate, unleash, supercharge, revolutionary,
   "look no further", "in today's fast-paced", "delve", "whether you're a",
   "let's dive", "buckle up".
5. **No popularity claims without a dated official source** (decision D-08).
   None exists for these products, so none appears.
6. **Trade-offs over verdicts.** Where the data can't rank products, say so
   and give the reader the comparison that can.
7. **Questions are titles.** Guides answer one question each; the title asks
   it.
8. **Compliance copy is human copy.** Disclosures are one plain sentence, not
   legal wallpaper: the Associates statement above the fold, the sponsored
   link note next to every product link.
9. **Do not reproduce Amazon listing prose.** Facts are re-stated in original
   words; listing titles appear verbatim only inside the product register
   where they are quoted as data.

## Anti-slop checklist (what "AI slop" looks like, and what ships instead)

| Pattern | Ships instead |
|---|---|
| "In today's fast-paced world..." | The answer, first sentence. |
| "Whether you're a beginner or a pro..." | The specific reader situation with numbers. |
| Rule-of-three adjective stacks ("crispy, convenient, cost-effective") | One concrete detail the reader can check. |
| "Unlock / elevate / unleash your kitchen" | The actual instruction or trade-off. |
| Invented statistics ("up to 85% faster!") | Nothing - unverified numbers never ship. |
| Fake enthusiasm ("This will change your life!") | The honest limit of the claim. |
| Em-dash confetti and bold-everything | Punctuation that carries meaning. |
| "As an AI language model" disclaimers | The site's real method, on the Methodology page. |
