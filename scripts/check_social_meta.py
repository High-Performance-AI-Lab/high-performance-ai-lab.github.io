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
ARTICLE_CARD_PATH = Path("img/articles/evals-as-theory-building/map-becomes-territory-social.jpg")
ARTICLE_CARD_URL = f"{SITE_URL}/{ARTICLE_CARD_PATH.as_posix()}"
ARTICLE_PAGE = "articles/evals-as-theory-building/index.html"
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
    "twitter:image:width",
    "twitter:image:height",
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


def image_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        offset = 2
        start_of_frame = {
            0xC0, 0xC1, 0xC2, 0xC3,
            0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB,
            0xCD, 0xCE, 0xCF,
        }
        while offset + 8 < len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            while offset < len(data) and data[offset] == 0xFF:
                offset += 1
            marker = data[offset]
            offset += 1
            if marker in start_of_frame:
                height = int.from_bytes(data[offset + 3:offset + 5], "big")
                width = int.from_bytes(data[offset + 5:offset + 7], "big")
                return width, height
            if marker == 0x01 or 0xD0 <= marker <= 0xD9:
                continue
            segment_length = int.from_bytes(data[offset:offset + 2], "big")
            if segment_length < 2:
                break
            offset += segment_length
    raise ValueError(f"{path} is not a supported PNG or JPEG")


def check_page(path: Path, build_dir: Path) -> list[str]:
    parser = HeadMeta()
    parser.feed(path.read_text(encoding="utf-8"))
    errors = [
        f"{path}: missing {key}"
        for key in sorted(REQUIRED_META - parser.meta.keys())
    ]
    is_featured_article = path.relative_to(build_dir).as_posix() == ARTICLE_PAGE
    image_url = ARTICLE_CARD_URL if is_featured_article else CARD_URL
    image_type = "image/jpeg" if is_featured_article else "image/png"
    expected = {
        "og:image": image_url,
        "og:image:secure_url": image_url,
        "og:image:type": image_type,
        "og:image:width": "1200",
        "og:image:height": "630",
        "twitter:card": "summary_large_image",
        "twitter:image": image_url,
        "twitter:image:width": "1200",
        "twitter:image:height": "630",
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
    card_sets = [
        [
            root / "assets" / "social-card.png",
            root / "public" / "social-card.png",
            build_dir / "social-card.png",
        ],
        [
            root / "public" / ARTICLE_CARD_PATH,
            build_dir / ARTICLE_CARD_PATH,
        ],
    ]
    errors: list[str] = []
    for cards in card_sets:
        for card in cards:
            if not card.is_file():
                errors.append(f"missing social card: {card}")
            elif image_dimensions(card) != (1200, 630):
                errors.append(f"{card}: expected 1200x630 image")
        if all(card.is_file() for card in cards):
            expected_bytes = cards[0].read_bytes()
            for card in cards[1:]:
                if card.read_bytes() != expected_bytes:
                    errors.append(f"social card differs: {card}")

    pages = sorted(build_dir.rglob("*.html"))
    if not pages:
        errors.append(f"no generated HTML pages below {build_dir}")
    for page in pages:
        errors.extend(check_page(page, build_dir))

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(pages)} pages carry complete Open Graph and X card metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
