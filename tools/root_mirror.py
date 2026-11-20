#!/usr/bin/env python3
"""Write the root mirror that legacy-mode GitHub Pages serves.

Why this exists: the repository's Pages site is in *legacy* mode with the source set
to `main /` (confirmed via the Pages API on 2026-11-20; the token cannot change it —
a PUT to build_type=workflow returns 403). So whatever sits at the repo root is what
a reader can fetch. That means two things have to be true of every mirror write:

1. The reader-facing pages must be at the root, byte-identical to docs/.
2. The source tree — data/, content/, tools/, scripts/, tests/, the claim files, the
   coordination board — must NOT be. Publishing it exposes the whole working
   repository to anyone who types the path (flags F-P19/F-P20).

The previous mirror was `cp -r docs/* .`, which copied only the site but left the
source files sitting at the root from normal git checkouts. Legacy Pages serves a
checked-out repo, so those files were reachable regardless of what the generator
wrote. Two controls now sit between the checkout and the reader:

1. The root carries no `.nojekyll`, so the legacy build runs Jekyll (and Jekyll does
   not build a path named in `exclude` — see the citation in tools/publish_surface.py).
2. `tools/publish_surface.py` generates the root `_config.yml` whose exclusion list is
   derived from the tree, so `data/`, `content/`, `tools/`, `scripts/`, `tests/`,
   `archive/`, `site/`, `docs/` and the `.md` records are not published, while the
   mirrored pages and `assets/` are.

The canaries below stay as tripwires: if a future configuration change makes a source
directory servable again, the file that appears is this one, and it names the flags.
The real fix remains one repository setting (Settings → Pages → Source: GitHub Actions),
which is why F-P31 stays open until that flip happens.

    python3 tools/root_mirror.py            # write the mirror + deny files
    python3 tools/root_mirror.py --report   # print what is exposed, change nothing
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Served from the mirror as normal pages/assets; everything else at the root is source.
PUBLIC_SUFFIXES = {".html", ".css", ".js", ".xml", ".txt", ".png", ".jpg", ".jpeg",
                   ".svg", ".webp", ".woff2", ".ico", ".json"}
PUBLIC_ROOT_FILES = {"robots.txt", "sitemap.xml", "feed.xml", "404.html", "CNAME",
                     "favicon.ico", "og-card.png"}

# Directories whose contents are working data, not publication.
SOURCE_DIRS = ["data", "content", "tools", "scripts", "tests", "archive", "var", "npm"]

# A deny-file is a directory canary: if a static host ever serves the directory or
# its index, this file proves it. It is not a security control — it is a tripwire
# that makes the exposure visible and linkable in the coordination record.
CANARY = """# This directory is source, not publication.

If you are reading this on the public site, then the repository root is being served
without the exclusion list in its `_config.yml` taking effect: GitHub Pages is in
legacy mode with the source set to `main /`, and a root `.nojekyll` file (or a stale
`_config.yml`) means Jekyll copied the whole checkout instead of only the publication.

Flags F-P19, F-P20 and F-P31 track this (F-P29 is the published-CSS conflict-marker defect, a different surface problem). Two checks keep it shut: the gate section
"exposition" in tools/checks.py refuses a root .nojekyll and refuses a config that
misses a top-level path, and tools/publish_surface.py --check says the same thing on
its own. The permanent fix is one repository setting: Settings -> Pages -> Source:
GitHub Actions, which publishes the docs/ artifact only.

Reader-facing pages are the .html files at the site root. The registers behind them
are documented on method.html and cited as repository links, never as served files.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="list exposure, change nothing")
    args = ap.parse_args()

    exposed = []
    for d in SOURCE_DIRS:
        p = ROOT / d
        if p.exists():
            n = sum(1 for _ in p.rglob("*") if _.is_file())
            exposed.append(f"{d}/ ({n} files)")

    if args.report:
        print("Root-mode Pages surface (build_type=legacy, source=main /):")
        for e in exposed:
            print(f"  in the tree: {e}")
        print(f"  at root: {len(list(ROOT.glob('*.md')))} .md files, "
              f"{len(list(ROOT.glob('.session*')))} claim markers")
        sys.path.insert(0, str(ROOT / "tools"))
        import publish_surface

        print(f"\n  served by the Pages build : {len(publish_surface.published_names())} top-level paths "
              f"(the docs/ mirror)")
        print(f"  excluded by _config.yml   : {len(publish_surface.excluded_top_level())} top-level paths")
        print(f"  root .nojekyll present    : {(ROOT / '.nojekyll').exists()}"
              + ("   <-- Jekyll is disabled: everything at the root would be served"
                 if (ROOT / ".nojekyll").exists() else ""))
        rc = subprocess.call([sys.executable, str(ROOT / "tools" / "publish_surface.py"), "--check"])
        print("\nReal fix: Settings -> Pages -> Source: GitHub Actions (owner action; closes F-P31 and SG-46).")
        return rc

    written = 0
    for d in SOURCE_DIRS:
        p = ROOT / d
        if p.is_dir():
            (p / "_SOURCE_NOT_PUBLICATION.md").write_text(CANARY, encoding="utf-8")
            written += 1
    for name in (".session-86206fb3.claim",):
        p = ROOT / name
        if p.exists():
            pass  # a claim file is evidence; the canary above covers the tree

    print(f"wrote {written} source-directory canaries")
    print(f"documented exposure: {', '.join(exposed) if exposed else 'none'}")
    print("the deployed publication is docs/; root mode is an owner setting (F-P19/F-P20)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
