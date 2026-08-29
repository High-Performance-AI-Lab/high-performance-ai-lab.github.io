#!/usr/bin/env python3
"""Fail if any generated page lacks the Lab's production social metadata."""

from __future__ import annotations

import argparse
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path


SITE_URL = "https://highperformanceailab.com"
CARD_URL = f"{SITE_URL}/social-card.png"
REQUIRED_META = {
    "og:title",
    "og:description",
    "og:type",
    "og:url",
    "og:site_name",
    "og:locale",
    "og:image",
    "og:image:secure_url",
    "og:image:type",
    "og:image:width",
    "og:image:height",
    "og:image:alt",
    "twitter:card",
    "twitter:title",
    "twitter:description",
    "twitter:url",
    "twitter:image",
    "twitter:image:alt",
}


class HeadMeta(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.canonical: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "meta":
            key = values.get("property") or values.get("name")
            content = values.get("content")
            if key and content is not None:
                self.meta[key] = content
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href")


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"{path} is not a PNG with an IHDR header")
    return struct.unpack(">II", data[16:24])


def check_page(path: Path) -> list[str]:
    parser = HeadMeta()
    parser.feed(path.read_text(encoding="utf-8"))
    errors = [
        f"{path}: missing {key}"
        for key in sorted(REQUIRED_META - parser.meta.keys())
    ]
    expected = {
        "og:image": CARD_URL,
        "og:image:secure_url": CARD_URL,
        "og:image:type": "image/png",
        "og:image:width": "1200",
        "og:image:height": "630",
        "twitter:card": "summary_large_image",
        "twitter:image": CARD_URL,
    }
    for key, value in expected.items():
        if parser.meta.get(key) != value:
            errors.append(f"{path}: {key} is not {value!r}")
    for key in ("og:url", "twitter:url"):
        value = parser.meta.get(key, "")
        if not value.startswith(f"{SITE_URL}/"):
            errors.append(f"{path}: {key} is not on the production origin")
    if not parser.canonical or not parser.canonical.startswith(f"{SITE_URL}/"):
        errors.append(f"{path}: canonical is not on the production origin")
    if parser.meta.get("og:url") != parser.canonical:
        errors.append(f"{path}: og:url and canonical differ")
    if parser.meta.get("twitter:url") != parser.canonical:
        errors.append(f"{path}: twitter:url and canonical differ")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("build_dir", nargs="?", default="dist")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    build_dir = (root / args.build_dir).resolve()
    cards = [
        root / "assets" / "social-card.png",
        root / "public" / "social-card.png",
        build_dir / "social-card.png",
    ]
    errors: list[str] = []
    for card in cards:
        if not card.is_file():
            errors.append(f"missing social card: {card}")
        elif png_dimensions(card) != (1200, 630):
            errors.append(f"{card}: expected 1200x630 PNG")
    if all(card.is_file() for card in cards):
        expected = cards[0].read_bytes()
        for card in cards[1:]:
            if card.read_bytes() != expected:
                errors.append(f"social card differs: {card}")

    pages = sorted(build_dir.rglob("*.html"))
    if not pages:
        errors.append(f"no generated HTML pages below {build_dir}")
    for page in pages:
        errors.extend(check_page(page))

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(pages)} pages carry complete Open Graph and X card metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
