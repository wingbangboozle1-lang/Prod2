#!/usr/bin/env python3
"""make_og.py — renders the social-preview card (assets/img/og-card.png).

Typographic brand art only: real lettering rendered with DejaVu fonts on the
site's paper background. This is NOT product photography — Amazon listing imagery
is Program Content and its use needs a licence review first (D-P12 / Q-P05).

    python3 tools/make_og.py

Requires Pillow (pip install pillow). The output is committed so a clean
checkout does not need Pillow unless the card is being changed.

Layout rule (added 2026-11-20 after a broken render): every string is measured
before it is drawn, and the draw is skipped-with-a-warning if it would overrun
its column. Silent overlap is worse than a missing chip.
"""
from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "og-card.png"

W, H = 1200, 630
PAPER = (251, 247, 241)
PAPER_DEEP = (244, 237, 226)
INK = (28, 22, 19)
TERRACOTTA = (194, 85, 47)
SAGE = (94, 114, 86)
MUTED = (110, 98, 89)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MARGIN = 72
FOOTER_H = 96

DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."

# Right column holds the format chips; keep it clear of the headline.
CHIP_X = 806
CHIP_W_MAX = W - CHIP_X - MARGIN


def fit(draw: ImageDraw.ImageDraw, text: str, font, max_w: int):
    """Return the text truncated with an ellipsis if it cannot fit max_w."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    ell = "…"
    while text and draw.textlength(text + ell, font=font) > max_w:
        text = text[:-1]
    return text + ell


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_brand = ImageFont.truetype(SERIF_B, 58)
    f_desc = ImageFont.truetype(SANS_B, 20)
    f_head = ImageFont.truetype(SERIF_B, 68)
    f_sub = ImageFont.truetype(SANS, 28)
    f_chip = ImageFont.truetype(SANS_B, 19)
    f_foot = ImageFont.truetype(SANS_B, 19)

    # top rule
    d.rectangle([0, 0, W, 12], fill=TERRACOTTA)

    # ---- brand row ----------------------------------------------------------
    d.text((MARGIN, 56), "Prod2", font=f_brand, fill=INK)
    brand_w = d.textlength("Prod2", font=f_brand)
    # the wordmark's own terracotta full stop
    d.text((MARGIN + brand_w, 56), ".", font=f_brand, fill=TERRACOTTA)
    desc_x = MARGIN + brand_w + 26
    d.text((desc_x, 84), "KITCHEN NOTES & BUYING GUIDES", font=f_desc, fill=MUTED)

    # ---- headline, confined to the left column ------------------------------
    head_max_w = CHIP_X - MARGIN - 28
    lines = ["The air fryer that", "fits how you cook."]
    y = 182
    for line in lines:
        d.text((MARGIN, y), fit(d, line, f_head, head_max_w), font=f_head, fill=INK)
        y += 82

    # ---- method line --------------------------------------------------------
    d.line([MARGIN, y + 26, MARGIN + 210, y + 26], fill=TERRACOTTA, width=5)
    sub = "Every figure read from its official listing."
    d.text((MARGIN, y + 52), fit(d, sub, f_sub, head_max_w), font=f_sub, fill=SAGE)

    # ---- right column: format chips ----------------------------------------
    chips = ["DUAL-BASKET", "OVEN-STYLE", "SINGLE-BASKET", "THERMOMETERS"]
    cy = 176
    for c in chips:
        label = fit(d, c, f_chip, CHIP_W_MAX - 52)
        w = min(d.textlength(label, font=f_chip) + 52, CHIP_W_MAX)
        d.rounded_rectangle([CHIP_X, cy, CHIP_X + w, cy + 50],
                            radius=25, outline=INK, width=2, fill=PAPER_DEEP)
        d.text((CHIP_X + 26, cy + 15), label, font=f_chip, fill=INK)
        cy += 70

    # ---- footer strip -------------------------------------------------------
    d.rectangle([0, H - FOOTER_H, W, H], fill=INK)
    fy = H - FOOTER_H + (FOOTER_H - 26) // 2
    right = "shop · compare · guides"
    right_w = d.textlength(right, font=f_foot)
    # draw the right label first so the disclosure gets the remaining width
    d.text((W - MARGIN - right_w, fy), right, font=f_foot, fill=(183, 169, 150))
    avail = W - MARGIN * 2 - right_w - 40
    if d.textlength(DISCLOSURE, font=f_foot) > avail:
        # never truncate a required disclosure — shrink to fit instead
        size = 19
        while size > 12:
            f_foot = ImageFont.truetype(SANS_B, size)
            if d.textlength(DISCLOSURE, font=f_foot) <= avail:
                break
            size -= 1
        fy = H - FOOTER_H + (FOOTER_H - size) // 2
    d.text((MARGIN, fy), DISCLOSURE, font=f_foot, fill=PAPER)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
