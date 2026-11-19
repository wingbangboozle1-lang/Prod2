# Engine guide — how this site is built and checked

This repository is a deterministic static-site pipeline. There is no CMS, no
database and no unverified fact path: the generator reads only the registers
in `data/`, and the check suite fails the build if a published page violates a
register rule.

```
data/*.json ──► build.py ──► public/          (site: 28 HTML pages + feed + sitemap + robots)
                  │
                  ├─► content/guides/*.html   (article bodies, one per guide)
                  └─► assets/                 (css, js, og-image, favicon)

check.py    ──► 30 checks over public/ + data/   (CI runs both on every push)
```

## Commands

```bash
python3 build.py     # build the site into public/
python3 check.py     # run all 30 checks (exit non-zero on failure)
python3 collector/app.py --port 8090   # optional: run the self-hosted collector
python3 -m http.server 8000 --directory public  # preview the built site
```

Both scripts use the Python standard library only - a clean checkout needs
nothing else.

## Pipeline rules

1. **Registers are the only input.** `build.py` reads `data/*.json`; hand-edits
   to `public/` are lost and pointless. Content lives in `data/` (registers)
   and `content/` (article bodies).
2. **A page cannot exist without its register row.** Titles, descriptions,
   internal links, product facts and source links all come from the registers.
3. **Link rules are enforced twice** - by the generator (which adds
   `rel="sponsored"` and the tag parameter) and by the checks (which fail if
   any Amazon-domain anchor is unmarked, untagged, or points at a held ASIN).
4. **Disclosure is structural.** The strip is part of the page template, not
   page content; a page without it cannot be generated.
5. **The ledger is append-only by hand of the owner.** It ships empty
   (`rows: []`) and the checks verify it stays schema-exact.
6. **Docs match code.** The check-count line below is asserted by `check.py`;
   edit both together or the build fails.

## Checks: 30 (see check.py; ENGINE.md and check.py must agree)

1. all expected pages generated
2. unique `<title>` per page
3. unique meta description per page (40–170 chars)
4. disclosure strip above the fold on every page
5. footer disclosure on every page
6. Amazon IP notice on every page
7. canonical URL on every page
8. Open Graph + Twitter card tags on every page
9. JSON-LD parses on every page
10. guides carry BlogPosting structured data
11. front page carries WebSite structured data
12. sitemap.xml lists exactly the public pages
13. feed.xml is valid RSS 2.0 and lists all eight guides
14. robots.txt references the sitemap
15. every internal link resolves
16. every internal fragment target exists
17. every Amazon-domain anchor is rel="sponsored"
18. every tagged anchor is a published intended ASIN or a policy citation
19. held ASINs and link.amazon paths never appear as anchors
20. product register keeps intended/observed fields separate
21. ledger is empty, schema-exact, forecast-free
22. exactly five events defined and wired in analytics.js
23. no popularity claims on reader-facing pages
24. no slop phrases on reader-facing pages
25. guide internal linking (comparison + category + two siblings)
26. header nav is the single configured group
27. footer directory contains every configured surface
28. every image has alt text
29. ENGINE.md check count matches the code
30. every page parses as HTML

## Failure policy

Any failed check exits non-zero and CI blocks the deploy. Fix the register or
the template - never the check.
