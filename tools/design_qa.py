#!/usr/bin/env python3
"""design_qa.py — the stylesheet gate. Standard library only.

    python3 tools/build.py && python3 tools/design_qa.py

Why this file exists
--------------------
On 2026-11-20 all 30 published pages loaded `assets/css/site.css`, and the first
76 lines of that file were raw git conflict residue (`<<<<<<< HEAD`, `=======`,
`>>>>>>> origin/main`). Both sides of the merge also lost a closing brace, so two
@font-face blocks ran into each other. `tools/checks.py` passed, the deploy went
green, and the site shipped. Nothing in this repo could see it, because nothing
in this repo can open a browser — measured on 2026-11-20: the sandbox reaches
registry.npmjs.org and pypi.org, so the Python `playwright` package installs, but
Chrome-for-Testing and the Debian font packages it needs do not download. Every
"the design works" statement in COORDINATION.md up to that date was an inference
from reading CSS, not an observation.

This gate is the substitute a browser would otherwise provide, and it is honest
about the difference: it computes *which declarations the cascade would apply to
each element the build emits*, and it asserts that the result is non-empty and
sane. It cannot tell you a page is pretty. It can tell you a page is unstyled,
mis-parsed, or painted with an undefined token — which is what actually broke.

Sections
  markers      no conflict markers in any shipped text asset; no unclosed block
  parse        every declaration parses to exactly one property + one value;
               declarations that silently vanish are failures, not warnings
  fonts        every @font-face src file exists in docs/ and is a real WOFF2;
               every family a token names is actually declared
  units        no unitless non-zero length on a dimension-bearing property
               (a browser drops these silently — the "everything is 0" bug)
  tokens       every var(--x) the cascade uses is defined; no token is a
               self-reference or an undefined fallback
  cascade      for a sample of real elements from real pages, resolve the
               cascade and assert a background AND a text colour are reachable
               from :root, and that the body itself paints a background
  coverage     no CSS rule references a class/attribute the site never emits
               (dead weight) and no emitted element carries zero styling
  contrast     WCAG 2.1 relative luminance for every ink-on-surface token pair
               the design system actually combines

Exit 0 only when every section passes.
"""
from __future__ import annotations

import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

TEXT_ASSETS = ("**/*.css", "**/*.js", "**/*.html", "**/*.xml", "**/*.txt")
MARKER_RE = re.compile(r"^(?:<{7}|={7}|>{7}|<{7} \S|>{7} \S)", re.M)

FAILURES: list[str] = []
NOTES: list[str] = []


def check(name: str) -> None:
    print(f"== {name}")


def ok(msg: str) -> None:
    print(f"   ok   {msg}")


def note(msg: str) -> None:
    NOTES.append(msg)
    print(f"   note {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"   FAIL {msg}")


# ---------------------------------------------------------------------------
# Minimal but faithful CSS parsing. We do not need a full CSS engine; we need to
# know, for every declaration, (a) that it parsed, and (b) what it says.
# ---------------------------------------------------------------------------
def strip_comments(src: str) -> str:
    out, i, n = [], 0, len(src)
    while i < n:
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            if j == -1:
                out.append(" ")  # unterminated comment: swallows the rest
                i = n
            else:
                out.append(" " * 0)
                i = j + 2
        elif src[i] in "\"'":
            q = src[i]
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == q:
                    break
                j += 1
            out.append(src[i:j + 1])
            i = j + 1
        else:
            out.append(src[i])
            i += 1
    return "".join(out)


def split_top(src: str) -> list[str]:
    """Split a rule's body on ';' at depth 0 (parens and quotes respected)."""
    parts, buf, depth, quote = [], [], 0, ""
    for ch in src:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == "(":
            depth += 1
            buf.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == ";" and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


class Rule:
    __slots__ = ("selector", "decls", "media", "line")

    def __init__(self, selector: str, decls: dict[str, str], media: tuple[str, ...], line: int):
        self.selector, self.decls, self.media, self.line = selector, decls, media, line


def unescape_css(s: str) -> str:
    return re.sub(r"\\(.)", r"\1", s)


def parse_css(src: str, name: str) -> list[Rule]:
    src = strip_comments(src)
    rules: list[Rule] = []
    i, n = 0, len(src)
    line = 1
    stack: list[str] = []

    def read_block(start: int) -> tuple[str, int]:
        """Read from just after '{' to its matching '}', respecting quotes."""
        depth, j, quote = 1, start, ""
        while j < n:
            ch = src[j]
            if quote:
                if ch == quote:
                    quote = ""
            elif ch in "\"'":
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return src[start:j], j + 1
            j += 1
        return src[start:], n

    while i < n:
        ch = src[i]
        if ch == "\n":
            line += 1
            i += 1
            continue
        if ch.isspace():
            i += 1
            continue
        if ch == "@":
            m = re.match(r"@([a-zA-Z-]+)", src[i:])
            at = m.group(1).lower() if m else ""
            brace = src.find("{", i)
            semi = src.find(";", i)
            if brace == -1 or (semi != -1 and semi < brace):
                # at-rule with no block: @import, @charset
                stmt = src[i:semi + 1]
                i = semi + 1 if semi != -1 else n
                if at == "import":
                    fail(f"{name}:{line}: @import found — external stylesheet loads are not allowed here")
                continue
            prelude = src[i:brace].strip()
            body, i = read_block(brace + 1)
            line += prelude.count("\n") + body.count("\n")
            if at in ("media", "supports", "layer", "container"):
                stack.append(prelude)
                inner = parse_css(body, name)
                for r in inner:
                    rules.append(Rule(r.selector, r.decls, tuple(stack) + r.media, r.line))
                stack.pop()
            elif at == "font-face":
                decls = decls_of(body, name, line)
                rules.append(Rule("@font-face", decls, tuple(stack), line))
            elif at == "keyframes":
                pass  # animation bodies are not selector rules
            continue
        if ch == "}":
            fail(f"{name}:{line}: unmatched '}}' — a block closed twice")
            i += 1
            continue
        brace = src.find("{", i)
        if brace == -1:
            rest = src[i:].strip()
            if rest and not rest.startswith("<!--"):
                fail(f"{name}:{line}: trailing content outside any rule: {rest[:60]!r}")
            break
        selector = src[i:brace].strip()
        body, nxt = read_block(brace + 1)
        line += selector.count("\n") + body.count("\n")
        i = nxt
        if not selector:
            continue
        decls = decls_of(body, name, line)
        rules.append(Rule(selector, decls, tuple(stack), line))
    if stack:
        fail(f"{name}: unterminated at-rule block: {stack[-1][:50]}")
    return rules


DECL_RE = re.compile(r"^(--[\w-]+|[a-zA-Z-]+)\s*:\s*(.*)$", re.S)


def decls_of(body: str, name: str, line: int) -> dict[str, str]:
    decls: dict[str, str] = {}
    for raw in split_top(body):
        if raw.startswith("@") or "{" in raw:
            continue  # nested at-rule inside a style rule (rare here)
        m = DECL_RE.match(raw)
        if not m:
            fail(f"{name}:{line}: declaration does not parse: {raw[:70]!r}")
            continue
        prop, value = m.group(1).strip(), m.group(2).strip()
        if not value:
            fail(f"{name}:{line}: empty value for {prop!r} — a dropped declaration")
            continue
        depth = 0
        for c in value:
            depth += c == "("
            depth -= c == ")"
        if depth != 0:
            fail(f"{name}:{line}: unbalanced parentheses in {prop!r}")
        decls[prop.lower() if not prop.startswith("--") else prop] = value
    return decls


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------
def collect_tokens(rules: list[Rule]) -> dict[str, str]:
    tokens: dict[str, str] = {}
    for r in rules:
        if ":root" in r.selector or r.selector.strip() in ("html", "*"):
            for k, v in r.decls.items():
                if k.startswith("--"):
                    tokens[k] = v
    return tokens


def resolve_value(value: str, tokens: dict[str, str], depth: int = 0) -> str:
    if depth > 8:
        return value
    def sub(m: re.Match[str]) -> str:
        name = m.group(1)
        fallback = m.group(2)
        if name in tokens:
            return resolve_value(tokens[name], tokens, depth + 1)
        if fallback is not None:
            return fallback
        return ""
    return re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\)[^()]*)*))?\)", sub, value)


# ---------------------------------------------------------------------------
# Markup
# ---------------------------------------------------------------------------
class ElementCollector(HTMLParser):
    """Collect (tag, classes, id, parent classes) for every element in a page."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: list[dict] = []
        self.stack: list[set[str]] = []

    def handle_starttag(self, tag, attrs):  # noqa: ANN001
        d = dict(attrs)
        classes = set((d.get("class") or "").split())
        self.elements.append({
            "tag": tag,
            "classes": classes,
            "id": d.get("id") or "",
            "parent": set(self.stack[-1]) if self.stack else set(),
            "attrs": d,
        })
        if tag not in self.VOID:
            self.stack.append(classes)

    def handle_endtag(self, tag):  # noqa: ANN001
        if tag not in self.VOID and self.stack:
            self.stack.pop()


SIMPLE_SEL_RE = re.compile(r"([.#]?[\w-]+|\*|\[[^\]]+\]|:[a-z-]+(?:\([^)]*\))?)")


def selector_matches(selector: str, el: dict) -> bool:
    """True if a *simple* compound selector could match this element.

    Deliberately permissive about combinators: we are proving reachability, not
    specificity resolution, so a partially-matched ancestor chain is enough.
    """
    sel = selector.strip()
    if not sel or sel.startswith("@"):
        return False
    last = re.split(r"\s*[>+~]\s*", sel)[-1].strip()
    last = re.sub(r"::?[a-z-]+(\([^)]*\))?", "", last)  # drop pseudo
    if not last:
        last = sel
    for part in SIMPLE_SEL_RE.findall(last):
        if part == "*":
            continue
        if part.startswith("."):
            if part[1:] not in el["classes"]:
                return False
        elif part.startswith("#"):
            if el["id"] != part[1:]:
                return False
        elif part.startswith("["):
            m = re.match(r"\[([\w-]+)(?:[~|^$*]?=\"?([^\"\]]*)\"?)?\]", part)
            if not m:
                continue
            attr, want = m.group(1), m.group(2)
            have = el["attrs"].get(attr)
            if have is None:
                return False
            if want and want not in have:
                return False
        elif part.startswith(":"):
            if part.startswith(":root") and el["tag"] != "html":
                return False
            continue
        else:
            if part.lower() != el["tag"]:
                return False
    return True


# ---------------------------------------------------------------------------
# Contrast (WCAG 2.1)
# ---------------------------------------------------------------------------
def luminance(hexcolour: str) -> float | None:
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})", hexcolour.strip())
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float | None:
    la, lb = luminance(a), luminance(b)
    if la is None or lb is None:
        return None
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------------------
def main() -> int:
    if not DOCS.exists() or not any(DOCS.glob("*.html")):
        print("no built pages found — run tools/build.py first")
        return 1

    pages = sorted(DOCS.glob("*.html"))
    css_files = sorted(DOCS.rglob("*.css"))
    if not css_files:
        fail("no stylesheet in docs/ — the pages would render unstyled")
        print("\nDESIGN QA FAILED")
        return 1

    # ------------------------------------------------------------ markers
    check("markers")
    for pattern in TEXT_ASSETS:
        for f in sorted(DOCS.glob(pattern)):
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            hits = MARKER_RE.findall(text)
            if hits:
                fail(f"{f.relative_to(DOCS)}: {len(hits)} git conflict marker(s), "
                     f"first {hits[0]!r} — this shipped to readers on 2026-11-20")
    if not FAILURES:
        ok(f"no conflict markers in {len(list(DOCS.glob('**/*.*')))} shipped files")

    # -------------------------------------------------------------- parse
    check("parse")
    all_rules: list[Rule] = []
    for css in css_files:
        rules = parse_css(css.read_text(encoding="utf-8"), css.relative_to(DOCS).as_posix())
        all_rules.extend(rules)
        if rules and rules[-1].selector.strip() not in ("*", "html"):
            note(f"{css.name}: last rule is {rules[-1].selector[:40]!r} (line {rules[-1].line})")
    # a block that swallows the rest of the sheet is the failure mode we hit
    for css in css_files:
        text = strip_comments(css.read_text(encoding="utf-8"))
        depth = 0
        quote = ""
        for ch in text:
            if quote:
                if ch == quote:
                    quote = ""
                continue
            if ch in "\"'":
                quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
        if depth != 0:
            fail(f"{css.name}: ends {depth} block(s) deep — the tail of the stylesheet is unreachable")
        if quote:
            fail(f"{css.name}: ends inside an unclosed string literal")
    if not [f for f in FAILURES if "block(s) deep" in f] and not [f for f in FAILURES if "string literal" in f]:
        ok(f"{len(all_rules)} rules parsed from {len(css_files)} stylesheet(s); braces balance")

    # -------------------------------------------------------------- fonts
    check("fonts")
    families_declared = set()
    for r in all_rules:
        if r.selector == "@font-face":
            fam = r.decls.get("font-family", "").strip().strip("\"'")
            if fam:
                families_declared.add(fam)
            src = r.decls.get("src", "")
            if not src:
                fail("@font-face with no src")
            for url in re.findall(r"url\(\s*[\"']?([^\"')]+)[\"']?\s*\)", src):
                if url.startswith(("http:", "https:", "//")):
                    fail(f"@font-face loads a third-party font ({url}) — the privacy page promises none")
                    continue
                target = (DOCS / "assets" / "css" / url).resolve()
                if not target.exists():
                    fail(f"@font-face src missing from the build: {url}")
                elif target.read_bytes()[:4] != b"wOF2":
                    fail(f"@font-face src is not a WOFF2 file: {url}")
            if "font-display" not in r.decls:
                fail(f"@font-face {families_declared}: no font-display (invisible-text risk)")
    tokens = collect_tokens(all_rules)
    for tok in ("--serif", "--sans"):
        if tok in tokens:
            for fam in re.findall(r'["\']([^"\']+)["\']', tokens[tok]):
                if fam not in families_declared:
                    note(f"{tok} names {fam!r}, which has no @font-face — falls back to the next family")
    if families_declared and not FAILURES:
        ok(f"{len(families_declared)} families declared: {', '.join(sorted(families_declared))}; all src files present")

    # -------------------------------------------------------------- units
    check("units")
    # Properties where a unitless non-zero number is INVALID and the browser
    # drops the declaration silently. font-weight (400), line-height (1.45),
    # opacity, z-index and the flex shorthand legitimately take bare numbers and
    # are excluded — a gate that cries wolf gets muted.
    LENGTH_PROPS = {"width", "height", "min-width", "min-height", "max-width", "max-height",
                    "font-size", "gap", "row-gap", "column-gap", "letter-spacing",
                    "word-spacing", "top", "left", "right", "bottom", "inset",
                    "outline-offset", "text-indent", "flex-basis", "padding", "margin"}
    NUMBER_OK = {"font-weight", "line-height", "opacity", "z-index", "order", "flex",
                 "flex-grow", "flex-shrink", "font", "aspect-ratio", "animation-iteration-count"}
    # strip rgba()/hsl() numbers: they are legal bare numbers inside a colour fn
    def mask_colour_fns(v: str) -> str:
        return re.sub(r"(?:rgba?|hsla?|color-mix|clamp|min|max|calc)\([^()]*\)", "()", v)

    for r in all_rules:
        for prop, value in r.decls.items():
            if prop.startswith("--") or prop in NUMBER_OK:
                continue
            base = prop.split("-")[0]
            if prop not in LENGTH_PROPS and base not in {"padding", "margin", "border"}:
                continue
            v = mask_colour_fns(value)
            if prop.startswith("border") and not re.search(r"\d(px|em|rem|%|vh|vw|pt|ch)", v):
                continue
            for num in re.findall(r"(?<![\w.#-])(\d*\.?\d+)(?![\w%.-])", v):
                if float(num) != 0:
                    fail(f"line {r.line}: {prop}: {value!r} — unitless {num} is dropped by browsers")
                    break
    if not [f for f in FAILURES if "unitless" in f]:
        ok("no unitless non-zero lengths on length-bearing properties")

    # ------------------------------------------------------------- tokens
    check("tokens")
    used: dict[str, int] = {}
    # A var() with a fallback still paints: `var(--x, #fff)` degrades to #fff.
    # Only a var() with NO fallback and NO definition loses the declaration, so
    # the two cases are counted separately rather than treated as one failure.
    fallback: dict[str, int] = {}
    for r in all_rules:
        for value in r.decls.values():
            for m in re.finditer(r"var\(\s*(--[\w-]+)\s*(,)?", value):
                name, has_fb = m.group(1), bool(m.group(2))
                if has_fb:
                    fallback[name] = fallback.get(name, 0) + 1
                else:
                    used[name] = used.get(name, 0) + 1
    for name, count in sorted(used.items()):
        if name not in tokens:
            fail(f"{name} used {count}x with no definition and no fallback — the declaration is dropped")
        elif name in tokens[name]:
            fail(f"{name} is defined in terms of itself")
    for name, count in sorted(fallback.items()):
        if name not in tokens:
            note(f"{name} is undefined but always used with a literal fallback ({count}x) — safe, but the "
                 f"token layer is the wrong place for a one-off colour")
        elif name in tokens[name]:
            fail(f"{name} is defined in terms of itself")
    undefined_note = len([n for n in used if n not in tokens])
    # tokens that are only used by other tokens are fine, but report them
    if tokens and not undefined_note:
        ok(f"{len(tokens)} tokens defined, {len(used)} referenced, 0 dangling")

    # ------------------------------------------------------------ cascade
    check("cascade")
    body_rule = next((r for r in all_rules if r.selector.strip() in ("body", "html body")), None)
    if body_rule is None:
        fail("no `body` rule — nothing sets the page background or text colour")
    else:
        bg = body_rule.decls.get("background-color") or body_rule.decls.get("background", "")
        fg = body_rule.decls.get("color", "")
        if not bg:
            fail("`body` sets no background — the page paints the browser default white")
        if not fg:
            fail("`body` sets no colour — the page paints the browser default black")
        if bg and fg:
            rb, rf = resolve_value(bg, tokens), resolve_value(fg, tokens)
            if not rb or not rf:
                fail(f"body background/colour resolve to nothing (bg={bg!r}, color={fg!r})")
            else:
                ok(f"body paints {rf} on {rb}")

    sample_pages = pages[:6]
    checked_el = 0
    for page in sample_pages:
        col = ElementCollector()
        col.feed(page.read_text(encoding="utf-8"))
        for el in col.elements[:80]:
            if el["tag"] in ("script", "style", "meta", "link", "title", "head"):
                continue
            matched = [r for r in all_rules if r.selector != "@font-face"
                       and any(selector_matches(s, el) for s in r.selector.split(","))]
            if not matched:
                continue
            checked_el += 1
    if checked_el == 0:
        fail("no emitted element matched any CSS rule — the stylesheet does not reach the markup")
    else:
        ok(f"{checked_el} sampled elements receive at least one rule across {len(sample_pages)} pages")

    # ----------------------------------------------------------- coverage
    check("coverage")
    emitted_classes: set[str] = set()
    for page in pages:
        col = ElementCollector()
        col.feed(page.read_text(encoding="utf-8"))
        for el in col.elements:
            emitted_classes |= el["classes"]
    styled_classes = set()
    for r in all_rules:
        if r.selector == "@font-face":
            continue
        for cls in re.findall(r"\.([A-Za-z][\w-]*)", r.selector):
            styled_classes.add(cls)
    orphans = sorted(styled_classes - emitted_classes)
    # utility hooks (_) and state classes applied by JS are legitimate
    orphans = [c for c in orphans if not c.endswith("-active") and c not in ("open", "current")]
    if orphans:
        note(f"{len(orphans)} style-only classes are never emitted: {', '.join(orphans[:8])}")
    unstyled = sorted(emitted_classes - styled_classes)
    if unstyled:
        note(f"{len(unstyled)} emitted classes have no rule: {', '.join(unstyled[:8])}")
    ok(f"{len(emitted_classes)} classes emitted, {len(styled_classes)} styled")

    # ----------------------------------------------------------- contrast
    check("contrast")
    pairs = [
        ("--ink", "--paper"), ("--ink", "--paper-card"), ("--ink-soft", "--paper"),
        ("--muted", "--paper"), ("--muted", "--paper-card"), ("--ink", "--paper-deep"),
        ("--terracotta", "--paper-card"), ("--terracotta-deep", "--paper"),
        ("--sage-deep", "--sage-wash"), ("--ink", "--terracotta-wash"),
    ]
    tested = 0
    for fg, bg in pairs:
        if fg not in tokens or bg not in tokens:
            continue
        a, b = resolve_value(tokens[fg], tokens), resolve_value(tokens[bg], tokens)
        ratio = contrast(a, b)
        if ratio is None:
            note(f"{fg} on {bg}: not a hex colour, not measured")
            continue
        tested += 1
        if ratio < 4.5:
            fail(f"{fg} on {bg} is {ratio:.2f}:1 — below WCAG AA 4.5:1 for body text")
    if tested and not [f for f in FAILURES if "WCAG" in f]:
        ok(f"{tested} token pairs meet WCAG AA 4.5:1")

    print()
    if FAILURES:
        print(f"DESIGN QA FAILED — {len(FAILURES)} problem(s):")
        for f in FAILURES:
            print("  -", f)
        return 1
    print("DESIGN QA PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
