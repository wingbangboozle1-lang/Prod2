#!/usr/bin/env python3
"""make_og.py — renders the social-preview card (assets/img/og-card.png).

Typographic brand art only: real lettering rendered with DejaVu fonts on the
site's paper background. This is NOT product photography — generated or copied
product photography is banned (decision D-22 / S-18, still awaiting a decision).

    python3 tools/make_og.py

Requires Pillow (pip install pillow). The output is committed so a clean
checkout does not need Pillow unless the card is being changed.
"""
from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "og-card.png"

W, H = 1200, 630
PAPER = (251, 247, 241)
PAPER_DEEP = (244, 237, 227)
INK = (36, 28, 23)
TERRACOTTA = (196, 97, 60)
SAGE = (111, 127, 99)
MUTED = (107, 96, 88)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_brand = ImageFont.truetype(SERIF, 58)
    f_desc = ImageFont.truetype(SANS_B, 24)
    f_head = ImageFont.truetype(SERIF, 78)
    f_sub = ImageFont.truetype(SANS, 34)
    f_foot = ImageFont.truetype(SANS_B, 26)

    # top rule + brand row (working brand — D-P10; see DESIGN_PROMPT.md)
    brand = "The Crisp Counter"
    d.rectangle([0, 0, W, 14], fill=TERRACOTTA)
    d.text((72, 56), brand, font=f_brand, fill=INK)
    d.text((72 + d.textlength(brand, font=f_brand) + 22, 76),
           "KITCHEN NOTES & BUYING GUIDES", font=f_desc, fill=MUTED)

    # headline (auto-fit to the column left of the chips)
    head_lines = ["Find the format", "that fits your kitchen."]
    size = 84
    max_w = 660  # headline column: x 72..732, chips start at 810
    while size > 40:
        f_try = ImageFont.truetype(SERIF, size)
        if max(d.textlength(t, font=f_try) for t in head_lines) <= max_w:
            break
        size -= 2
    f_head = ImageFont.truetype(SERIF, size)
    y = 190
    for t in head_lines:
        d.text((72, y), t, font=f_head, fill=INK)
        y += size + 18

    # method line
    d.line([72, y + 28, 420, y + 28], fill=TERRACOTTA, width=5)
    d.text((72, y + 56), "Every figure read from its official listing.", font=f_sub, fill=SAGE)

    # right-side format chips (short strings, clear of the headline block)
    x = 810
    chips = ["DUAL-BASKET", "OVEN-STYLE", "SINGLE-BASKET", "THERMOMETERS"]
    y = 180
    for c in chips:
        w = d.textlength(c, font=f_desc) + 44
        d.rounded_rectangle([x, y, x + w, y + 54], radius=27, outline=INK, width=3, fill=PAPER_DEEP)
        d.text((x + 22, y + 14), c, font=f_desc, fill=INK)
        y += 76

    # footer strip (disclosure only — it is the line that must always be legible)
    d.rectangle([0, H - 72, W, H], fill=INK)
    d.text((72, H - 50), "As an Amazon Associate we earn from qualifying purchases.",
           font=f_foot, fill=PAPER)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
