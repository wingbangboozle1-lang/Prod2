#!/usr/bin/env python3
"""make_art.py — deterministic brand artwork for the publication.

The site carries NO product photography. Amazon's IP License restricts Program
Content (including product images) to specific uses we have not been granted,
and inventing a photograph of a product we have not handled would break the
site's own evidence rule (D-06). What the site CAN honestly show is its own
editorial identity, so every image here is typographic or diagrammatic brand
art drawn from the site's own palette and its own verified facts.

Run once and commit the output; the build copies assets/ into docs/:

    python3 tools/make_art.py

Requires Pillow (not required at runtime by the site itself).
"""
from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

FONT_DIR = pathlib.Path("/usr/share/fonts/truetype/dejavu")
SERIF = FONT_DIR / "DejaVuSerif.ttf"
SERIF_B = FONT_DIR / "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_B = FONT_DIR / "DejaVuSans-Bold.ttf"

# Palette — kept in step with assets/css/site.css
PAPER = (251, 247, 241)
PAPER_DEEP = (244, 237, 227)
INK = (36, 28, 23)
INK_SOFT = (74, 62, 53)
MUTED = (107, 96, 88)
TERRA = (196, 97, 60)
TERRA_DEEP = (166, 77, 45)
SAGE = (111, 127, 99)
RULE = (231, 221, 209)


def font(path: pathlib.Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def text(d: ImageDraw.ImageDraw, xy, s, f, fill=INK, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def wrap(d: ImageDraw.ImageDraw, s: str, f, width: int) -> list[str]:
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def canvas(w: int, h: int, bg=PAPER) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def grain(d: ImageDraw.ImageDraw, w: int, h: int, step: int = 7) -> None:
    """A faint paper tooth so flat colour reads as stock, not as a screenshot."""
    for y in range(0, h, step):
        for x in range(0, w, step):
            if (x * 31 + y * 17) % 23 == 0:
                d.point((x, y), fill=(238, 231, 221))


# ---------------------------------------------------------------------------
# 1. Wordmark / masthead mark (square, used as the site icon and in the header)
# ---------------------------------------------------------------------------
def wordmark() -> None:
    S = 512
    img, d = canvas(S, S, TERRA_DEEP)
    d.rectangle([0, 0, S, S], fill=TERRA_DEEP)
    d.ellipse([-120, -160, 300, 260], fill=TERRA)
    d.ellipse([300, 330, 640, 670], fill=(139, 62, 36))
    # a counter-top line and three "pan" bars: the publication's own diagram
    d.rectangle([96, 300, S - 96, 312], fill=PAPER)
    for i, height in enumerate((78, 118, 58)):
        x = 118 + i * 100
        d.rounded_rectangle([x, 300 - height, x + 64, 300], radius=12, fill=PAPER)
    f = font(SERIF_B, 116)
    text(d, (S // 2, 392), "P2", f, PAPER, anchor="ma")
    f2 = font(SANS_B, 30)
    text(d, (S // 2, 452), "KITCHEN NOTES", f2, PAPER, anchor="ma")
    img.save(OUT / "mark.png", optimize=True)


# ---------------------------------------------------------------------------
# 2. Hero card (the front-page image: the five formats, drawn as shapes)
# ---------------------------------------------------------------------------
def hero() -> None:
    W, H = 1200, 900
    img, d = canvas(W, H, PAPER_DEEP)
    grain(d, W, H)
    d.rectangle([0, 0, W, H], outline=RULE, width=2)

    # header rule + eyebrow
    text(d, (72, 76), "THE SHELF, DRAWN TO SCALE OF PURPOSE", font(SANS_B, 22), TERRA_DEEP)
    d.line([72, 116, W - 72, 116], fill=RULE, width=2)
    f_head = font(SERIF_B, 62)
    for i, line in enumerate(("Five machines.", "Three formats.", "One counter.")):
        text(d, (72, 150 + i * 74), line, f_head, INK)

    # five diagram tiles: dual basket, oven, single basket, instant-read, probe
    tiles = [
        ("Dual basket", "6 qt · 2 × 3 qt"),
        ("Toaster oven", "26 qt · French doors"),
        ("Single basket", "8 qt · one drawer"),
        ("Instant-read", "1-second probe"),
        ("Wireless probe", "leave-in · 1000°F"),
    ]
    tw, th = 196, 196
    gap = 22
    x0, y0 = 72, 404
    for i, (label, sub) in enumerate(tiles):
        x = x0 + i * (tw + gap)
        d.rounded_rectangle([x, y0, x + tw, y0 + th], radius=14, fill=PAPER, outline=RULE, width=2)
        cx, cy = x + tw // 2, y0 + 74
        if i == 0:  # dual basket
            d.rounded_rectangle([cx - 62, cy - 26, cx - 8, cy + 34], radius=6, outline=TERRA, width=4)
            d.rounded_rectangle([cx + 8, cy - 26, cx + 62, cy + 34], radius=6, outline=TERRA, width=4)
            d.line([cx - 54, cy - 40, cx - 16, cy - 40], fill=TERRA, width=4)
            d.line([cx + 16, cy - 40, cx + 54, cy - 40], fill=TERRA, width=4)
        elif i == 1:  # oven with french doors
            d.rounded_rectangle([cx - 66, cy - 40, cx + 66, cy + 40], radius=6, outline=TERRA, width=4)
            d.line([cx, cy - 40, cx, cy + 40], fill=TERRA, width=4)
            d.line([cx - 66, cy - 14, cx + 66, cy - 14], fill=TERRA, width=3)
            for k in (-44, -18, 18, 44):
                d.ellipse([cx + k - 4, cy + 8, cx + k + 4, cy + 16], fill=TERRA)
        elif i == 2:  # single basket
            d.rounded_rectangle([cx - 56, cy - 34, cx + 56, cy + 42], radius=10, outline=TERRA, width=4)
            d.line([cx - 34, cy - 48, cx + 34, cy - 48], fill=TERRA, width=4)
            d.line([cx - 56, cy - 6, cx + 56, cy - 6], fill=TERRA, width=3)
        elif i == 3:  # instant read
            d.line([cx, cy - 48, cx, cy + 18], fill=TERRA, width=6)
            d.ellipse([cx - 18, cy + 4, cx + 18, cy + 44], outline=TERRA, width=5)
            d.line([cx + 8, cy - 34, cx + 26, cy - 34], fill=TERRA, width=4)
            d.line([cx + 8, cy - 20, cx + 20, cy - 20], fill=TERRA, width=4)
        else:  # wireless probe + hub
            d.line([cx - 46, cy + 10, cx + 6, cy + 10], fill=TERRA, width=6)
            d.ellipse([cx - 58, cy + 2, cx - 46, cy + 18], outline=TERRA, width=3)
            d.rounded_rectangle([cx + 10, cy - 30, cx + 62, cy + 30], radius=8, outline=TERRA, width=4)
            for r in (8, 16, 24):
                d.arc([cx + 34 - r, cy - r, cx + 34 + r, cy + r], 200, 340, fill=TERRA, width=3)
        text(d, (x + tw // 2, y0 + 136), label, font(SANS_B, 20), INK, anchor="ma")
        text(d, (x + tw // 2, y0 + 164), sub, font(SANS, 17), MUTED, anchor="ma")

    # footer note: the honest line
    d.line([72, 664, W - 72, 664], fill=RULE, width=2)
    f_note = font(SANS, 21)
    for i, line in enumerate(wrap(
        d,
        "Specifications read from the official listings and dated. No product photography: "
        "these are the site's own diagrams, not the manufacturer's images.",
        f_note, W - 144,
    )):
        text(d, (72, 692 + i * 30), line, f_note, INK_SOFT)
    text(d, (72, H - 76), "wingbangboozle1-lang.github.io/Prod2", font(SANS_B, 19), TERRA_DEEP)

    img.save(OUT / "hero-shelf.png", optimize=True)


# ---------------------------------------------------------------------------
# 3. Guide cards — one diagram per guide topic (no stock photos, no product art)
# ---------------------------------------------------------------------------
def guide_card(name: str, title_lines: list[str], kicker: str, draw_fn) -> None:
    W, H = 800, 500
    img, d = canvas(W, H, PAPER_DEEP)
    grain(d, W, H)
    d.rectangle([0, 0, W, H], outline=RULE, width=2)
    d.rectangle([0, 0, 10, H], fill=TERRA)
    text(d, (52, 48), kicker.upper(), font(SANS_B, 19), TERRA_DEEP)
    f = font(SERIF_B, 47)
    for i, line in enumerate(title_lines):
        text(d, (50, 92 + i * 56), line, f, INK)
    draw_fn(d, W, H)
    img.save(OUT / f"{name}.png", optimize=True)


def draw_two_baskets(d, W, H):
    y = 356
    for i, (w, label) in enumerate(((150, "basket A"), (150, "basket B"))):
        x = 84 + i * 176
        d.rounded_rectangle([x, y - 70, x + w, y + 40], radius=12, outline=TERRA, width=5)
        text(d, (x + w // 2, y + 58), label, font(SANS, 18), MUTED, anchor="ma")
    d.line([84, y + 22, 410, y + 22], fill=SAGE, width=4)
    text(d, (438, y - 6), "sync finish", font(SANS_B, 20), SAGE)
    text(d, (438, y + 22), "two clocks, one stop", font(SANS, 18), MUTED)


def draw_capacity(d, W, H):
    y = 352
    for i, (h, label) in enumerate(((58, "2 qt"), (96, "6 qt"), (128, "8 qt"), (164, "26 qt"))):
        x = 90 + i * 118
        d.rectangle([x, y + 60 - h, x + 78, y + 60], fill=None, outline=TERRA, width=4)
        text(d, (x + 39, y + 74), label, font(SANS_B, 19), INK, anchor="ma")
    text(d, (90, y - 44), "Quarts, drawn as volume — not as servings.", font(SANS, 19), MUTED)


def draw_counter_space(d, W, H):
    y = 320
    d.line([70, y + 118, W - 60, y + 118], fill=INK_SOFT, width=6)
    text(d, (70, y + 128), "counter front edge", font(SANS, 17), MUTED)
    boxes = ((150, 96, 'oven 16.9"'), (128, 74, 'dual 13.4"'), (112, 66, 'single 12.8"'))
    for i, (w, h, label) in enumerate(boxes):
        x = 80 + i * 200
        top = y + 118 - h
        d.rectangle([x, top, x + w, y + 118], outline=TERRA, width=4)
        d.line([x, top, x + w, top], fill=TERRA, width=4)
        text(d, (x, top - 30), label, font(SANS_B, 18), INK)
        # depth / width guide lines
        d.line([x + w + 6, y + 118, x + w + 6, top - 6], fill=SAGE, width=2)
        d.line([x, y + 118 - h - 6, x + w, y + 118 - h - 6], fill=SAGE, width=2)
    text(d, (80, y - 52), "Depth (vertical) and width (horizontal), to one scale.", font(SANS, 19), MUTED)


def draw_multifunction(d, W, H):
    y = 330
    funcs = ("air fry", "bake", "broil", "dehydrate", "roast", "reheat")
    for i, f in enumerate(funcs):
        x = 76 + (i % 3) * 210
        yy = y + (i // 3) * 74
        d.rounded_rectangle([x, yy, x + 186, yy + 56], radius=10, outline=TERRA, width=3)
        text(d, (x + 93, yy + 28), f, font(SANS_B, 20), INK, anchor="mm")
    text(d, (76, y - 46), "Six of the listed functions. Which will you use?", font(SANS, 19), MUTED)


def draw_thermometer(d, W, H):
    y = 300
    d.line([120, y, 120, y + 130], fill=TERRA, width=10)
    d.ellipse([96, y + 118, 144, y + 166], outline=TERRA, width=6)
    for i, t in enumerate(("165°F", "145°F", "135°F")):
        yy = y + 10 + i * 40
        d.line([112, yy, 136, yy], fill=SAGE, width=4)
        text(d, (152, yy - 12), t, font(SANS_B, 20), INK_SOFT)
    text(d, (250, y + 10), "±0.5°F claimed accuracy", font(SANS_B, 21), INK)
    text(d, (250, y + 44), "reads in 1 second, per the listing", font(SANS, 19), MUTED)
    text(d, (250, y + 92), "What matters is where you put it,", font(SANS, 19), MUTED)
    text(d, (250, y + 116), "not how many decimals it shows.", font(SANS, 19), MUTED)


def draw_quarts(d, W, H):
    y = 330
    for i in range(8):
        x = 86 + i * 78
        d.rounded_rectangle([x, y, x + 54, y + 54], radius=8,
                            fill=PAPER if i < 6 else None, outline=TERRA, width=4)
    text(d, (86, y - 46), "One quart, one square: eight of them, six used.", font(SANS, 19), MUTED)
    text(d, (86, y + 78), "Capacity is volume. Servings are a decision.", font(SANS, 19), MUTED)


def draw_instant_vs_leavein(d, W, H):
    y = 340
    d.line([110, y - 60, 110, y + 60], fill=TERRA, width=8)
    d.ellipse([92, y + 50, 128, y + 86], outline=TERRA, width=5)
    text(d, (110, y + 108), "instant-read", font(SANS_B, 19), INK, anchor="ma")
    d.rounded_rectangle([330, y - 50, 470, y + 60], radius=10, outline=TERRA, width=5)
    d.line([470, y + 5, 560, y + 5], fill=TERRA, width=5)
    for r in (14, 26, 38):
        d.arc([330 + 70 - r, y + 5 - r, 330 + 70 + r, y + 5 + r], 200, 340, fill=SAGE, width=4)
    text(d, (400, y + 84), "wireless leave-in", font(SANS_B, 19), INK, anchor="ma")
    text(d, (590, y - 4), "check it", font(SANS_B, 20), INK_SOFT)
    text(d, (590, y + 26), "or watch it", font(SANS_B, 20), SAGE)


def draw_holiday(d, W, H):
    y = 336
    for i, (w, label) in enumerate(((170, "oven: the bird"), (140, "dual: the sides"),
                                    (120, "single: the reheat"))):
        x = 84 + i * 210
        d.rounded_rectangle([x, y, x + w, y + 92], radius=12, outline=TERRA, width=4)
        text(d, (x + w // 2, y + 46), f"wave {i + 1}", font(SANS_B, 19))
        text(d, (x, y + 108), label, font(SANS, 18), MUTED)
    text(d, (84, y - 44), "Three waves of food, one counter.", font(SANS, 19), MUTED)


def guides() -> None:
    guide_card("g-basket-vs-oven", ["Basket or oven:", "what to compare"], "Format", draw_two_baskets)
    guide_card("g-capacity", ["A no-hype", "capacity checklist"], "Capacity", draw_capacity)
    guide_card("g-counter-space", ["Cleanup and", "counter space"], "Counter fit", draw_counter_space)
    guide_card("g-multifunction", ["Before you buy", "multi-function gear"], "Features", draw_multifunction)
    guide_card("g-thermometer", ["How accurate must", "a thermometer be?"], "Thermometers", draw_thermometer)
    guide_card("g-quarts", ["How many quarts", "do you need?"], "Sizing", draw_quarts)
    guide_card("g-two-baskets", ["Two baskets", "or one?"], "Format", draw_two_baskets)
    guide_card("g-instant-vs-leavein", ["Instant-read", "or leave-in?"], "Thermometers", draw_instant_vs_leavein)
    guide_card("g-holiday", ["Holiday hosting", "formats"], "Seasonal", draw_holiday)


# ---------------------------------------------------------------------------
# 4. Social card (1200×630), the one image that travels off-site
# ---------------------------------------------------------------------------
def social() -> None:
    W, H = 1200, 630
    img, d = canvas(W, H, INK)
    d.rectangle([0, 0, 14, H], fill=TERRA)
    text(d, (72, 70), "PROD2 · KITCHEN NOTES & BUYING GUIDES", font(SANS_B, 22), TERRA)
    f = font(SERIF_B, 84)
    for i, line in enumerate(("Find the format", "that fits", "your kitchen.")):
        text(d, (72, 130 + i * 100), line, f, PAPER)
    text(d, (72, 470), "Air fryers and meat thermometers, compared by format —",
         font(SANS, 26), (222, 212, 200))
    text(d, (72, 508), "every figure dated and sourced to its official listing.",
         font(SANS, 26), (222, 212, 200))
    d.line([72, 560, W - 72, 560], fill=(90, 78, 68), width=2)
    text(d, (72, 578), "As an Amazon Associate we earn from qualifying purchases.",
         font(SANS, 20), (200, 190, 178))
    img.save(OUT / "social.png", optimize=True)
    img.save(OUT / "og-card.png", optimize=True)  # og:image, same design


def main() -> None:
    wordmark()
    hero()
    guides()
    social()
    for p in sorted(OUT.glob("*.png")):
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
