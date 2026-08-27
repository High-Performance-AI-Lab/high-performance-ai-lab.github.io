#!/usr/bin/env python3
"""Generate the site's social preview card.

One deterministic render, no randomness, no external inputs, written to
two committed copies:

- assets/social-card.png   uploaded manually as the repo's social preview
- public/social-card.png   served by the site and referenced as og:image

The mark is the lab's memory-page grid in its light-surface palette —
site teal -> cobalt ramp, oxide decode head — the same geometry as
public/favicon.svg and the dark-surface twin in the .github org repo.

    python3 scripts/generate_social_card.py --check   # verify committed files
    python3 scripts/generate_social_card.py           # regenerate
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# src/styles/global.css values
BG = (250, 249, 247)       # --bg paper
INK = (28, 25, 23)         # --ink
MUTED = (87, 83, 78)       # --muted
OXIDE = (194, 65, 12)      # --accent
TEAL = (15, 118, 110)      # --teal
COBALT = (37, 99, 235)     # --cobalt
PAGE_DIM = (232, 231, 229) # unlit memory page (8% ink over paper)

FONT_PATHS = [
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SUPPLEMENTARY/Arial Bold.ttf",
]

GRID_N = 4                 # pages per side
CELL = 140                 # page size (mark coordinates, 1024x1024)
GAP = 32                   # gap between pages
RADIUS = 29                # page corner radius
HEIGHTS = [1, 3, 2, 4]     # lit pages per column, left to right


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_mark(img: Image.Image, scale: float = 1.0) -> Image.Image:
    """Memory-page grid with the lit measured series, centered onto `img`."""
    size = img.size[0]
    d = ImageDraw.Draw(img)
    cell, gap = CELL * scale, GAP * scale
    total = GRID_N * cell + (GRID_N - 1) * gap
    x0 = y0 = (size - total) / 2
    for c in range(GRID_N):
        for r in range(GRID_N):        # r = 0 is the bottom row
            x = x0 + c * (cell + gap)
            y = y0 + (GRID_N - 1 - r) * (cell + gap)
            if r >= HEIGHTS[c]:
                color = PAGE_DIM
            elif c == GRID_N - 1 and r == HEIGHTS[c] - 1:
                color = OXIDE          # the decode head, the hot page
            else:
                color = lerp(TEAL, COBALT, (c + r) / (2 * (GRID_N - 1)))
            d.rounded_rectangle([x, y, x + cell, y + cell],
                                radius=RADIUS * scale, fill=color)
    return img


def render_card() -> Image.Image:
    img = Image.new("RGB", (1200, 630), BG)
    mark = draw_mark(Image.new("RGB", (1024, 1024), BG), scale=0.78)
    mark = mark.resize((635, 635), Image.LANCZOS)
    img.paste(mark, (-60, 0))
    d = ImageDraw.Draw(img)
    x = 540
    d.text((x, 190), "High Performance", font=font(78), fill=INK)
    d.text((x, 280), "AI Lab", font=font(78), fill=INK)
    d.text((x, 420), "Open systems for local inference,", font=font(40), fill=OXIDE)
    d.text((x, 472), "proofs, and measured intelligence.", font=font(40), fill=OXIDE)
    d.text((x, 552), "highperformanceailab.com", font=font(28), fill=MUTED)
    return img


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify committed assets match a fresh render")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    paths = [root / "assets" / "social-card.png",
             root / "public" / "social-card.png"]
    fresh = render_card()

    if args.check:
        ok = True
        for path in paths:
            if not path.exists():
                print("FAIL: committed asset missing:", path)
                ok = False
            elif Image.open(path).convert("RGB").tobytes() != fresh.tobytes():
                print("FAIL: committed asset differs from fresh render:", path)
                ok = False
        print("PASS: social card matches render" if ok else "FAIL: see above")
        return 0 if ok else 1

    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        fresh.save(path, format="PNG", optimize=True)
        print("wrote", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
