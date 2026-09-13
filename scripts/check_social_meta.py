#!/usr/bin/env python3
"""Fail if any generated page lacks the Lab's production social metadata."""

from __future__ import annotations

import argparse
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


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
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X" and len(data) >= 30:
            return (
                1 + int.from_bytes(data[24:27], "little"),
                1 + int.from_bytes(data[27:30], "little"),
            )
        if chunk == b"VP8 " and len(data) >= 30 and data[23:26] == b"\x9d\x01\x2a":
            width, height = struct.unpack("<HH", data[26:30])
            return width & 0x3FFF, height & 0x3FFF
        if chunk == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
            bits = int.from_bytes(data[21:25], "little")
            return 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)
    raise ValueError(f"{path} is not a supported PNG, JPEG, or WebP")


def check_page(path: Path, build_dir: Path, root: Path) -> list[str]:
    parser = HeadMeta()
    parser.feed(path.read_text(encoding="utf-8"))
    errors = [
        f"{path}: missing {key}"
        for key in sorted(REQUIRED_META - parser.meta.keys())
    ]
    image_url = parser.meta.get("og:image", "")
    parsed_image = urlparse(image_url)
    if f"{parsed_image.scheme}://{parsed_image.netloc}" != SITE_URL:
        errors.append(f"{path}: og:image is not on the production origin")
    elif not parsed_image.path.startswith("/") or ".." in Path(parsed_image.path).parts:
        errors.append(f"{path}: og:image has an invalid path")
    else:
        relative_image = Path(unquote(parsed_image.path.lstrip("/")))
        built_image = build_dir / relative_image
        source_image = root / "public" / relative_image
        if not built_image.is_file():
            errors.append(f"{path}: social image does not exist in build: {relative_image}")
        else:
            try:
                width, height = image_dimensions(built_image)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                if (width, height) != (1200, 630):
                    errors.append(f"{built_image}: expected 1200x630 image")
                for prefix in ("og:image", "twitter:image"):
                    if parser.meta.get(f"{prefix}:width") != str(width):
                        errors.append(f"{path}: {prefix}:width does not match the image")
                    if parser.meta.get(f"{prefix}:height") != str(height):
                        errors.append(f"{path}: {prefix}:height does not match the image")
        if not source_image.is_file():
            errors.append(f"{path}: social image is not tracked below public/: {relative_image}")
        elif built_image.is_file() and source_image.read_bytes() != built_image.read_bytes():
            errors.append(f"{path}: built social image differs from public source: {relative_image}")

    suffix_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(Path(parsed_image.path).suffix.lower())
    if suffix_type and parser.meta.get("og:image:type") != suffix_type:
        errors.append(f"{path}: og:image:type does not match the image extension")
    for key in ("og:image:secure_url", "twitter:image"):
        if parser.meta.get(key) != image_url:
            errors.append(f"{path}: {key} differs from og:image")
    if parser.meta.get("og:image:alt") != parser.meta.get("twitter:image:alt"):
        errors.append(f"{path}: Open Graph and X image alt text differ")
    if parser.meta.get("twitter:card") != "summary_large_image":
        errors.append(f"{path}: twitter:card is not 'summary_large_image'")
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
        errors.extend(check_page(page, build_dir, root))

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(pages)} pages carry complete Open Graph and X card metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
