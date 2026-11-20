#!/usr/bin/env python3
"""
Countercraft release gate.

Runs from a clean checkout against the generated site/ and exits non-zero on any
violation. Checks:
  1. every page has a disclosure strip under the masthead AND a disclosure in the footer;
  2. every page has a unique, non-empty <title> and a meta description;
  3. every outbound Amazon product link carries rel="sponsored";
  4. every internal link resolves to a real file (no broken links);
  5. sitemap.xml lists every published .html page.

    python3 scripts/verify_site.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

errors = []
warnings = []


def html_files():
    out = []
    for dirpath, _, files in os.walk(SITE):
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def rel_path(abs_path):
    return os.path.relpath(abs_path, SITE)


def main():
    pages = html_files()
    if not pages:
        errors.append("No HTML pages found under site/.")

    titles = {}
    amazon_link_re = re.compile(r"<a\b[^>]*href=['\"](https://www\.amazon\.com/[^'\"]+)['\"][^>]*>", re.I)
    any_link_re = re.compile(r"<a\b[^>]*href=['\"]([^'\"]+)['\"]", re.I)
    rel_re = re.compile(r"\brel=\"([^\"]*)\"", re.I)

    sitemap = ""
    sm_path = os.path.join(SITE, "sitemap.xml")
    if os.path.exists(sm_path):
        sitemap = read(sm_path)

    for p in pages:
        rp = rel_path(p)
        doc = read(p)

        # 1. disclosure
        if "class='disclosure'" not in doc and 'class="disclosure"' not in doc:
            errors.append("%s: missing disclosure strip under the masthead." % rp)
        if "class='disc'" not in doc and 'class="disc"' not in doc:
            errors.append("%s: missing disclosure in the footer." % rp)

        # 2. unique title + meta description
        tm = re.search(r"<title>([^<]*)</title>", doc, re.I)
        title = tm.group(1).strip() if tm else ""
        if not title:
            errors.append("%s: missing <title>." % rp)
        elif title in titles:
            errors.append("%s: duplicate title '%s' (also on %s)." % (rp, title, titles[title]))
        else:
            titles[title] = rp
        md = re.search(r"<meta name=['\"]description['\"] content=['\"]([^'\"]*)['\"]", doc, re.I)
        if not md or not md.group(1).strip():
            errors.append("%s: missing or empty meta description." % rp)

        # 3b. every /dp/ product link carries the tracking tag (integration fix 2026-11-19)
        for href in amazon_link_re.findall(doc):
            if "/dp/" in href and "tag=shopnow047c-20" not in href:
                errors.append("%s: product link missing tag=shopnow047c-20: %s" % (rp, href))
        # 3. every outbound Amazon product link is rel="sponsored"
        for href in amazon_link_re.findall(doc):
            tag_start = doc.find('href="%s"' % href)
            seg = doc[tag_start:tag_start + 400]
            rel = rel_re.search(seg)
            if not rel or "sponsored" not in rel.group(1).lower():
                errors.append("%s: outbound Amazon link not marked rel=\"sponsored\": %s" % (rp, href))

        # 4. internal links resolve (relative to the page's own directory)
        page_dir = os.path.dirname(p)
        for href in any_link_re.findall(doc):
            if href.startswith(("http://", "https://", "//", "mailto:", "data:", "#")):
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            if target.startswith("/"):
                # site-root-absolute link: resolve against the site root
                resolved = os.path.normpath(os.path.join(SITE, target.lstrip("/")))
            else:
                resolved = os.path.normpath(os.path.join(page_dir, target))
            if os.path.exists(resolved):
                continue
            if os.path.exists(os.path.join(resolved, "index.html")):
                continue
            errors.append("%s: broken internal link -> %s" % (rp, href))

    # 5. sitemap coverage
    if sitemap:
        for p in pages:
            rp = rel_path(p)
            if rp == "404.html":
                continue  # the 404 page is not a content page and is not sitemapped
            if "<loc>" + "https://wingbangboozle1-lang.github.io/Prod2/" + rp + "</loc>" not in sitemap:
                errors.append("%s: not listed in sitemap.xml." % rp)
    else:
        errors.append("sitemap.xml is missing.")

    # 6. publication audit (root mirror = what legacy Pages serves) + docs/ mirror.
    #    Rules: disclosure above the fold and in the footer, the product-link
    #    contract (rel="sponsored" + enrolled tag on /dp/ links, no tag= on
    #    citations), canonical self-links, resolvable internal links, JSON-LD,
    #    robots policy and sitemap purity. Run by tools/audit_publication.py.
    #    Added by session arena/4fef743e-prod2 (tasks X-01/X-02).
    import subprocess
    auditor = os.path.join(ROOT, "tools", "audit_publication.py")
    for tree, label in ((ROOT, "root mirror"), (os.path.join(ROOT, "docs"), "docs/")):
        if not os.path.isdir(tree):
            errors.append("publication tree missing: %s" % tree)
            continue
        res = subprocess.run([sys.executable, auditor, "--root", tree],
                             capture_output=True, text=True)
        if res.returncode != 0:
            errors.append("publication audit failed for %s:\n%s" % (label, res.stdout))
    root_robots = os.path.join(ROOT, "robots.txt")
    docs_robots = os.path.join(ROOT, "docs", "robots.txt")
    if os.path.exists(root_robots) and os.path.exists(docs_robots):
        if read(root_robots) != read(docs_robots):
            errors.append("robots.txt at the root mirror and in docs/ disagree.")
    else:
        errors.append("robots.txt missing at the root mirror or in docs/.")

    # summary
    for w in warnings:
        print("WARN:", w)
    if errors:
        print("VERIFY FAILED — %d problem(s):" % len(errors))
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("VERIFY OK — %d pages checked. Disclosure, rel=\"sponsored\", unique meta, "
          "internal links and sitemap coverage all pass." % len(pages))


if __name__ == "__main__":
    main()
