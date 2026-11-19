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

    f_brand = ImageFont.truetype(SERIF, 64)
    f_desc = ImageFont.truetype(SANS_B, 26)
    f_head = ImageFont.truetype(SERIF, 88)
    f_sub = ImageFont.truetype(SANS, 34)
    f_foot = ImageFont.truetype(SANS_B, 26)

    # top rule + brand row
    d.rectangle([0, 0, W, 14], fill=TERRACOTTA)
    d.text((72, 64), "Prod2", font=f_brand, fill=INK)
    d.text((72 + d.textlength("Prod2", font=f_brand) + 22, 84),
           "KITCHEN NOTES & BUYING GUIDES", font=f_desc, fill=MUTED)

    # headline
    d.text((72, 210), "Find the format", font=f_head, fill=INK)
    d.text((72, 310), "that fits your kitchen.", font=f_head, fill=INK)

    # method line
    d.line([72, 450, 420, 450], fill=TERRACOTTA, width=5)
    d.text((72, 478), "Every figure read from its official listing.", font=f_sub, fill=SAGE)

    # right-side format chips
    x = 760
    chips = ["DUAL-BASKET", "OVEN-STYLE", "SINGLE-BASKET", "THERMOMETERS"]
    y = 200
    for c in chips:
        w = d.textlength(c, font=f_desc) + 56
        d.rounded_rectangle([x, y, x + w, y + 58], radius=29, outline=INK, width=3, fill=PAPER_DEEP)
        d.text((x + 28, y + 15), c, font=f_desc, fill=INK)
        y += 82

    # footer strip
    d.rectangle([0, H - 88, W, H], fill=INK)
    d.text((72, H - 60), "As an Amazon Associate we earn from qualifying purchases.",
           font=f_foot, fill=PAPER)
    d.text((W - 320, H - 60), "compare · guides · sources", font=f_foot, fill=(183, 169, 150))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
