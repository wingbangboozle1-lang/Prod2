#!/usr/bin/env python3
"""publish_surface.py — decides which paths the *served* site may contain, and writes
the root `_config.yml` that enforces that decision on GitHub Pages.

Why this file exists
-------------------
This repository's Pages site is in **legacy** mode with the source set to
`main /` — the *repository root* (Pages API read 2026-11-20: `build_type=legacy`,
`source={branch: main, path: /}`). A `PUT` to `build_type=workflow` returns
**403 "Resource not accessible by integration"** for the token available to these
sessions, so the setting itself is an owner action (flags F-P19 / F-P20).

While the root is the source, whatever is committed at the root is fetchable by an
anonymous reader. Measured, not assumed: on 2026-11-20 a cache-busting read of
`https://wingbangboozle1-lang.github.io/Prod2/data/p2/settings.json` returned the
current settings register, `tracking_id` included.

There is one lever left inside the repository. A legacy Pages build runs **Jekyll**
unless a `.nojekyll` file is present, and Jekyll does not build paths named in the
`exclude` setting of `_config.yml` (GitHub Docs, "About GitHub Pages and Jekyll":
*"By default, Jekyll doesn't build files or folders that … are excluded by the
`exclude` setting in your configuration file"*,
https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll).
So the root can hold the whole working repository for the build *and* publish only
the publication, by deleting the root `.nojekyll` and shipping an `_config.yml`
whose exclusion list is derived from the tree itself.

Rules
-----
* The publication is exactly what `docs/` contains — the generator writes `docs/`,
  then `tools/build.py` mirrors it to the root for legacy mode. The public set is
  therefore derived from `docs/`, never hand-maintained.
* Everything else tracked at the root (`data/`, `content/`, `tools/`, `scripts/`,
  `tests/`, `site/`, `archive/`, `docs/` itself, the `.md` records, `package.json`,
  `server.mjs`, …) is excluded from the served output.
* `.github/`, `.gitignore` and anything starting with `_`, `.` or `#` is not built by
  Jekyll anyway (same GitHub Docs paragraph); they are listed as a belt-and-braces
  measure because `jekyll-optional-front-matter` treats every Markdown file as a page.

Usage
-----
    python3 tools/publish_surface.py            # write _config.yml (+ report)
    python3 tools/publish_surface.py --check    # is the committed config current?
    python3 tools/publish_surface.py --report   # print the served / excluded split
"""
from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Files Jekyll's own defaults already keep out of the build; they are written into the
# config anyway so the intent survives a change of generator, and so a reviewer can
# read one list and see the whole served surface.
DOT_PREFIX_NOTE = (
    "# Jekyll's own defaults already keep these out of the build, so they are not named\n"
    "# below: any path starting with '_', '.' or '#', anything ending in '~', and the\n"
    "# node_modules/ and vendor/ directories (docs.github.com, 'About GitHub Pages and\n"
    "# Jekyll', read 2026-11-20). This file is called _config.yml, which is one reason\n"
    "# that rule is load-bearing rather than a convenience.\n"
)

HEADER = """# _config.yml — GitHub Pages build settings for the REPOSITORY ROOT. Generated file:
# do not hand-edit; regenerate with `python3 tools/build.py` (or
# `python3 tools/publish_surface.py`). tools/checks.py fails the build if this file
# disagrees with the tree, so a new directory cannot become public by accident.
#
# The publication is the root mirror of docs/ (index.html and the other generated
# pages, plus assets/, feed.xml, sitemap.xml, robots.txt). Pages serves this
# repository's ROOT in legacy mode, so every other path here is a file an anonymous
# reader could fetch — which is why the list below is a deny-list of the working
# source, not a theme configuration. Flags F-P19 / F-P20 carry the measurement;
# decision D-P24 carries the reasoning. One caveat for anyone reading this file in
# the repository: the root .nojekyll file must stay deleted, or Jekyll never runs
# and this exclusion list is ignored. The docs/ artifact keeps its own .nojekyll
# because an Actions upload must not be re-processed.
"""


def published_names() -> list[str]:
    """The served surface is whatever docs/ holds, mirrored to the root by build.py."""
    if not DOCS.is_dir():
        raise SystemExit(
            "publish_surface: docs/ is missing — run `python3 tools/build.py` first "
            "(the exclusion list is derived from the built publication, so the "
            "publication has to exist)."
        )
    return sorted(p.name for p in DOCS.iterdir() if p.name != ".nojekyll")


def never_built(name: str) -> bool:
    """True for paths Jekyll does not build on its own, exclusion list or not.

    GitHub Docs, "About GitHub Pages and Jekyll" (read 2026-11-20): the default build
    skips files and folders that "start with `_`, `.`, or `#`" or "end with `~`", as
    well as `node_modules/` and `vendor/`. Naming those in `exclude` would be a no-op —
    and `_config.yml` in particular cannot be listed by the file that generates itself,
    because it does not exist on the first render. They are recorded in the config's
    comment instead, so a reviewer sees the whole rule in one place.
    """
    return name.startswith(("_", ".", "#")) or name.endswith("~") or name in {"node_modules", "vendor"}


def excluded_top_level() -> list[str]:
    """Every top-level path in the repo that is not the publication and that Jekyll
    would otherwise build — i.e. exactly what `_config.yml` must name."""
    keep = set(published_names())
    out: list[str] = []
    for p in sorted(ROOT.iterdir(), key=lambda x: x.name):
        name = p.name
        if name in keep or never_built(name):
            continue
        out.append(name)
    return out


def render_config() -> str:
    excluded = excluded_top_level()
    dirs = [n + "/" for n in excluded if (ROOT / n).is_dir()]
    globs = [
        # Every Markdown record is a working document, not a page. Listed as patterns
        # as well as names so a file added between regenerations is still not served
        # even before the next build — the gate catches the staleness either way.
        "*.md",
        "**/*.md",
    ]
    lines = [HEADER, DOT_PREFIX_NOTE, "# Paths excluded from the Pages build (derived from the repository tree):",
             "exclude:"]
    for d in dirs:
        lines.append(f"  - {d[:-1]}")
    for g in globs:
        lines.append(f"  - \"{g}\"")
    for f in [n for n in excluded if not (ROOT / n).is_dir()]:
        lines.append(f"  - {f}")
    lines += [
        "",
        "# jekyll-readme-index and jekyll-default-layout are enabled by GitHub Pages and",
        "# cannot be switched off (see the GitHub Docs page quoted in the header), so the",
        "# exclusion above is what stops README.md or COORDINATION.md becoming a page.",
        "# This key is a second lock: if a README ever reached the build, it must not",
        "# replace the front page.",
        "readme_index:",
        "  enabled: false",
        "",
        "# No theme and no Markdown pipeline are configured on purpose: every published",
        "# file is already rendered HTML with no YAML front matter, so Jekyll copies it",
        "# as a static file instead of converting it (jekyllrb.com/docs/front-matter,",
        "# read 2026-11-20). Setting `markdown` or `highlighter` here could only drift",
        "# from the values Pages forces anyway, so they are left out.",
        "",
    ]
    return "\n".join(lines)


def config_path() -> pathlib.Path:
    return ROOT / "_config.yml"


def write() -> str:
    """Write the root _config.yml for the current tree. Called by tools/build.py after
    the docs/ -> root mirror, so the served surface can never lag behind the build."""
    path = config_path()
    text = render_config()
    path.write_text(text, encoding="utf-8")
    return text


def read_excludes(text: str) -> list[str]:
    """Parse the exclude list back out of the config, for the gate and for --check."""
    out: list[str] = []
    inside = False
    for raw in text.splitlines():
        if raw.startswith("exclude:"):
            inside = True
            continue
        if inside:
            s = raw.strip()
            if s.startswith("- "):
                out.append(s[2:].strip().strip('"'))
            elif s == "" or s.startswith("#"):
                continue
            else:
                break
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if the committed _config.yml is stale")
    ap.add_argument("--report", action="store_true", help="print the served / excluded split, change nothing")
    args = ap.parse_args()

    want = render_config()
    path = config_path()
    have = path.read_text(encoding="utf-8") if path.exists() else ""

    if args.report or args.check:
        pub = published_names()
        exc = excluded_top_level()
        print(f"served by the root build : {len(pub)} top-level paths")
        print(f"excluded from the build  : {len(exc)} top-level paths")
        if args.report:
            print("\nserved : " + ", ".join(pub))
            print("\nexcluded: " + ", ".join(exc))
            nojekyll = (ROOT / ".nojekyll").exists()
            print(f"\nroot .nojekyll present : {nojekyll}"
                  + ("   <-- Jekyll is disabled, so the exclusion list is IGNORED" if nojekyll else ""))
        if args.check and have != want:
            print("\n_config.yml is stale: regenerate with `python3 tools/build.py`")
            missing = sorted(set(exc) - {e.rstrip("/") for e in read_excludes(have)} - {""})
            if missing:
                print("  not excluded by the committed config: " + ", ".join(missing))
            return 1
        if args.check:
            print("\n   ok   _config.yml matches the tree")
        return 0

    path.write_text(want, encoding="utf-8")
    print(f"wrote _config.yml ({len(excluded_top_level())} top-level paths excluded, "
          f"{len(published_names())} served)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
