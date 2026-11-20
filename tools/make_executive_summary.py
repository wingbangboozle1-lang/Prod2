#!/usr/bin/env python3
"""make_executive_summary.py — render the review-ready executive summary.

The canonical source is `data/p2/executive-summary.md`. This module turns that
Markdown into the HTML fragment the publication serves, and `tools/build.py`
calls it while rendering `content/pages/executive-summary.html`, so the page
can never drift from its source.

Standard library only.

    python3 tools/make_executive_summary.py          # preview the fragment
"""
from __future__ import annotations

import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "p2" / "executive-summary.md"

CODE_PLACEHOLDER = "\x00CODE{}\x00"
LINK_PLACEHOLDER = "\x00LINK{}\x00"
HARD_BREAK = "\x01"


def _format_inline(text: str) -> str:
    """Escape text, then apply code, link, bold and italic markup."""
    placeholders: list[str] = []

    def stash(markup: str) -> str:
        placeholders.append(markup)
        return CODE_PLACEHOLDER.format(len(placeholders) - 1)

    # Code spans first: their contents are literal, never markup.
    text = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{html.escape(m.group(1))}</code>"), text)

    # Links: the label is formatted recursively, the destination is escaped.
    def link(m: "re.Match[str]") -> str:
        label = _format_inline(m.group(1))
        target = html.escape(m.group(2), quote=True)
        return stash(f'<a href="{target}">{label}</a>')

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)

    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    for index, markup in enumerate(placeholders):
        text = text.replace(CODE_PLACEHOLDER.format(index), markup)
        text = text.replace(LINK_PLACEHOLDER.format(index), markup)
    return text.replace(HARD_BREAK, "<br>")


def _table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(set(cell) <= {"-", ":", " "} and cell for cell in cells)


def render(markdown: str) -> str:
    """Render the summary Markdown into an HTML fragment."""
    out: list[str] = []
    paragraph: list[str] = []
    table: list[list[str]] = []
    list_items: list[str] = []
    list_tag = ""

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            body = "".join(paragraph).strip()
            if body:
                out.append(f"<p>{_format_inline(body)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items, list_tag
        if list_items:
            out.append(f"<{list_tag}>")
            out.extend(f"<li>{_format_inline(item)}</li>" for item in list_items)
            out.append(f"</{list_tag}>")
            list_items = []
            list_tag = ""

    def flush_table() -> None:
        nonlocal table
        if not table:
            return
        out.append('<div class="table-wrap"><table>')
        for index, row in enumerate(table):
            tag = "th" if index == 0 else "td"
            cells = "".join(f"<{tag}>{_format_inline(cell)}</{tag}>" for cell in row)
            out.append(f"<tr>{cells}</tr>")
        out.append("</table></div>")
        table = []

    def flush_all() -> None:
        flush_paragraph()
        flush_list()
        flush_table()

    for raw in markdown.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            cells = _table_row(stripped)
            if not _is_separator(cells):
                table.append(cells)
            continue
        if table:
            flush_table()

        if not stripped:
            flush_all()
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            flush_all()
            level = len(heading.group(1))
            if level == 1:
                continue  # the page template already carries the document title
            out.append(f"<h{min(level, 4)}>{_format_inline(heading.group(2))}</h{min(level, 4)}>")
            continue

        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet:
            flush_paragraph()
            if list_tag != "ul":
                flush_list()
                list_tag = "ul"
            list_items.append(bullet.group(1))
            continue

        numbered = re.match(r"^\d+[.)]\s+(.*)$", stripped)
        if numbered:
            flush_paragraph()
            if list_tag != "ol":
                flush_list()
                list_tag = "ol"
            list_items.append(numbered.group(1))
            continue

        flush_list()
        # Two trailing spaces are a Markdown hard line break; keep them apart.
        hard_break = raw.endswith("  ")
        paragraph.append(line.strip() + (HARD_BREAK if hard_break else " "))

    flush_all()
    return "\n".join(out) + "\n"


def render_source() -> str:
    return render(SOURCE.read_text(encoding="utf-8"))


def main() -> int:
    print(render_source(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
