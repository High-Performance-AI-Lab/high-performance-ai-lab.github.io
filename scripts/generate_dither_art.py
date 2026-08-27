#!/usr/bin/env python3
"""Generate the site's dithered photography plates.

Deterministic: reads the committed source photos in assets/photos/ and a
fixed seed; writes 1-bit Floyd-Steinberg ALPHA MASKS (opaque dots on
transparency) to public/img/. The page recolors them with CSS mask-image,
so one asset serves ink, oxide, and paper knockout treatments, and the
paper background shows through the holes.

Every mask is exported nearest-neighbour doubled from its dither width so
the dot stays a crisp ~2 device px square (mask-image ignores
image-rendering, so the doubling must be baked in).

Plates per subject:
  <name>-solo.png   1-bit plate (full tonal range) — single-plate uses
  <name>-ink.png    dark plate  (shadows + dark mids) — duotone base
  <name>-ox.png     light-mid plate — duotone accent (scarce)

Photo sources and licenses: assets/photos/credits.json (Wikimedia
Commons, all Public Domain / CC0 / CC BY; attribution in the colophon).

    python3 scripts/generate_dither_art.py          # regenerate
    python3 scripts/generate_dither_art.py --check  # verify committed files
"""

import argparse
import random
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "photos"
OUT = ROOT / "public" / "img"

GRAIN_SEED = 20260827
GRAIN_DENSITY = 0.055


def levels(img: Image.Image, n: int) -> Image.Image:
    """FS-dither a grayscale image to n evenly spaced levels; return P image."""
    pal = Image.new("P", (1, 1))
    grays = [round(i * 255 / (n - 1)) for i in range(n)]
    pal.putpalette(sum(([g, g, g] for g in grays), []) + [0, 0, 0] * (256 - n))
    return img.convert("RGB").quantize(palette=pal, dither=Image.FLOYDSTEINBERG)


def prep(name: str, width: int, aspect: float, focus=(0.5, 0.5), contrast=1.15) -> Image.Image:
    """Crop to `aspect` (w/h) around `focus` (fractions), enhance, resize."""
    img = Image.open(SRC / f"{name}.jpg").convert("L")
    w, h = img.size
    if w / h > aspect:              # too wide: crop width
        cw, ch = round(h * aspect), h
    else:                           # too tall: crop height
        cw, ch = w, round(w / aspect)
    cx = min(max(round(focus[0] * w - cw / 2), 0), w - cw)
    cy = min(max(round(focus[1] * h - ch / 2), 0), h - ch)
    img = img.crop((cx, cy, cx + cw, cy + ch))
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    return img.resize((width, round(width / aspect)), Image.LANCZOS)


def mask_from(q: Image.Image, lit: set) -> Image.Image:
    """Alpha mask: indices in `lit` become opaque black dots, rest transparent."""
    w, h = q.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    qp, op = q.load(), out.load()
    for y in range(h):
        for x in range(w):
            if qp[x, y] in lit:
                op[x, y] = (0, 0, 0, 255)
    return out.resize((w * 2, h * 2), Image.NEAREST)


def plates(name: str, out_stem: str, width: int, aspect: float, focus=(0.5, 0.5), contrast=1.15):
    img = prep(name, width, aspect, focus, contrast)
    q2 = levels(img, 2)                    # solo plate: classic 1-bit
    q4 = levels(img, 4)                    # duotone plates from 4 levels
    yield f"{out_stem}-solo.png", mask_from(q2, {0})
    yield f"{out_stem}-ink.png", mask_from(q4, {0, 1})
    yield f"{out_stem}-ox.png", mask_from(q4, {2})


def grain() -> Image.Image:
    rng = random.Random(GRAIN_SEED)
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    px = img.load()
    for y in range(256):
        for x in range(256):
            if rng.random() < GRAIN_DENSITY:
                px[x, y] = (28, 25, 23, 255)
    return img


def render_all() -> dict:
    out = {"grain-256.png": grain()}
    jobs = [
        # hero: the road to Fitz Roy, portrait 3:4
        ("fitzroy-tall", "hero-fitzroy", 720, 3 / 4, (0.5, 0.45), 1.15),
        # horizon bands, 21:5 — one Swiss, one Patagonian
        ("matterhorn", "band-matterhorn", 1600, 21 / 5, (0.5, 0.42), 1.2),
        ("paine-wide", "band-paine", 1600, 21 / 5, (0.5, 0.34), 1.25),
        # founder places, square
        ("lauterbrunnen", "place-zurich", 240, 1.0, (0.45, 0.5), 1.2),
        ("fitzroy-wide", "place-patagonia", 240, 1.0, (0.5, 0.45), 1.2),
    ]
    for name, stem, width, aspect, focus, c in jobs:
        for fname, img in plates(name, stem, width, aspect, focus, c):
            out[fname] = img
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    rendered = render_all()
    if args.check:
        ok = True
        for fname, fresh in rendered.items():
            p = OUT / fname
            if not p.exists():
                print("FAIL missing:", p)
                ok = False
            elif Image.open(p).convert("RGBA").tobytes() != fresh.tobytes():
                print("FAIL differs:", fname)
                ok = False
        print("PASS: dither art matches" if ok else "FAIL: see above")
        return 0 if ok else 1
    OUT.mkdir(parents=True, exist_ok=True)
    for fname, img in rendered.items():
        img.save(OUT / fname, optimize=True)
        print("wrote", OUT / fname, img.size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
