#!/usr/bin/env python3
"""Verify the illustrated Article 2, its provenance, and bundled receipts."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from check_social_meta import image_dimensions


ROOT = Path(__file__).resolve().parent.parent
SLUG = "what-survives-the-next-model"
ARTICLE = ROOT / "src/content/articles" / f"{SLUG}.md"
ARTICLE_PAGE = ROOT / "dist/articles" / SLUG / "index.html"
HOME_PAGE = ROOT / "dist/index.html"
PROVENANCE = ROOT / "art-direction" / SLUG / "provenance.json"
RECEIPTS = ROOT / "public/receipts" / SLUG
RECEIPTS_PAGE = ROOT / "dist/receipts" / SLUG / "RECEIPTS.html"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_repo_path(value: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(f"path escapes repository: {value!r}")
    resolved = (ROOT / relative).resolve()
    if ROOT.resolve() not in resolved.parents:
        raise RuntimeError(f"path escapes repository: {value!r}")
    return resolved


def check_file_record(record: dict, *, dimensions: bool = True) -> Path:
    path = resolve_repo_path(record["path"])
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"missing or linked declared file: {path}")
    if path.stat().st_size != record["bytes"]:
        raise RuntimeError(f"size mismatch: {path}")
    if sha256(path) != record["sha256"]:
        raise RuntimeError(f"digest mismatch: {path}")
    if dimensions and image_dimensions(path) != (record["width"], record["height"]):
        raise RuntimeError(f"dimension mismatch: {path}")
    return path


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.figure_stack: list[dict] = []
        self.figures: list[dict] = []
        self.caption_depth = 0
        self.links: list[str] = []
        self.meta: dict[str, str] = {}
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta":
            key = values.get("property") or values.get("name")
            content = values.get("content")
            if key and content is not None:
                self.meta[str(key)] = str(content)
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))
        if tag == "figure":
            classes = str(values.get("class", "")).split()
            figure = {"article": "article-illustration" in classes, "images": [], "caption": []}
            self.figure_stack.append(figure)
            self.figures.append(figure)
        elif tag == "figcaption" and self.figure_stack:
            self.caption_depth += 1
        elif tag == "img" and self.figure_stack:
            self.figure_stack[-1]["images"].append(values)

    def handle_endtag(self, tag: str) -> None:
        if tag == "figcaption" and self.caption_depth:
            self.caption_depth -= 1
        elif tag == "figure":
            if not self.figure_stack:
                raise RuntimeError("unmatched closing figure")
            self.figure_stack.pop()

    def handle_data(self, data: str) -> None:
        if self.caption_depth and self.figure_stack:
            self.figure_stack[-1]["caption"].append(data)


def built_target(page: Path, reference: str) -> Path | None:
    split = urlsplit(reference)
    if split.scheme or split.netloc or reference.startswith("#"):
        return None
    if split.path.startswith("/"):
        target = ROOT / "dist" / unquote(split.path.lstrip("/"))
    else:
        target = page.parent / unquote(split.path)
    if split.path.endswith("/"):
        target /= "index.html"
    target = target.resolve()
    if (ROOT / "dist").resolve() not in target.parents:
        raise RuntimeError(f"local reference escapes build: {reference!r}")
    return target


def verify_article(provenance: dict) -> None:
    parser = ArticleParser()
    parser.feed(ARTICLE_PAGE.read_text(encoding="utf-8"))
    parser.close()
    figures = [figure for figure in parser.figures if figure["article"]]
    if parser.h1_count != 1:
        raise RuntimeError(f"article page must contain one h1, found {parser.h1_count}")
    if len(figures) != 4:
        raise RuntimeError(f"expected four article illustrations, found {len(figures)}")
    expected_social = (
        "https://highperformanceailab.com/img/articles/"
        f"{SLUG}/silent-provider-worlds-social.jpg"
    )
    for key in ("og:image", "og:image:secure_url", "twitter:image"):
        if parser.meta.get(key) != expected_social:
            raise RuntimeError(f"article {key} does not use the opening illustration social crop")
    if parser.meta.get("og:image:type") != "image/jpeg":
        raise RuntimeError("article social image does not declare image/jpeg")
    for key in ("og:image:width", "twitter:image:width"):
        if parser.meta.get(key) != "1200":
            raise RuntimeError(f"article {key} is not 1200")
    for key in ("og:image:height", "twitter:image:height"):
        if parser.meta.get(key) != "630":
            raise RuntimeError(f"article {key} is not 630")
    if parser.meta.get("twitter:card") != "summary_large_image":
        raise RuntimeError("article does not request a large social card")
    if parser.meta.get("robots") != "noindex, nofollow":
        raise RuntimeError("unlisted article lacks noindex, nofollow metadata")
    declared = {resolve_repo_path(row["public"]["path"]).resolve() for row in provenance["assets"]}
    used: set[Path] = set()
    for figure in figures:
        if len(figure["images"]) != 1:
            raise RuntimeError("each article figure must contain exactly one image")
        image = figure["images"][0]
        alt = str(image.get("alt", "")).strip()
        if not alt:
            raise RuntimeError("article image lacks meaningful alt text")
        if not "".join(figure["caption"]).strip():
            raise RuntimeError("article figure lacks a caption")
        src = str(image.get("src", ""))
        built = built_target(ARTICLE_PAGE, src)
        if built is None or not built.is_file():
            raise RuntimeError(f"article image is missing from build: {src}")
        public = ROOT / "public" / unquote(urlsplit(src).path.lstrip("/"))
        used.add(public.resolve())
        width, height = image_dimensions(public)
        if str(image.get("width")) != str(width) or str(image.get("height")) != str(height):
            raise RuntimeError(f"article markup dimensions do not match {public}")
    if used != declared:
        raise RuntimeError("article figures and provenance public assets differ")
    for link in parser.links:
        target = built_target(ARTICLE_PAGE, link)
        if target is not None and not target.exists():
            raise RuntimeError(f"broken local article link: {link}")

    homepage = ArticleParser()
    homepage.feed(HOME_PAGE.read_text(encoding="utf-8"))
    homepage.close()
    article_path = f"/articles/{SLUG}"
    if any(urlsplit(link).path.rstrip("/") == article_path for link in homepage.links):
        raise RuntimeError("unlisted article is linked from the public homepage")


def verify_receipts() -> None:
    manifest = json.loads((RECEIPTS / "evidence-manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "hpal-evidence-manifest/v1":
        raise RuntimeError("unsupported evidence manifest")
    for record in manifest["files"]:
        relative = Path(record["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"unsafe evidence path: {record['path']}")
        path = (RECEIPTS / relative).resolve()
        if RECEIPTS.resolve() not in path.parents or not path.is_file() or path.is_symlink():
            raise RuntimeError(f"missing or linked evidence file: {path}")
        if path.stat().st_size != record["size_bytes"] or sha256(path) != record["sha256"]:
            raise RuntimeError(f"evidence manifest mismatch: {path}")

    receipt_parser = ArticleParser()
    receipt_parser.feed(RECEIPTS_PAGE.read_text(encoding="utf-8"))
    receipt_parser.close()
    for link in receipt_parser.links:
        target = built_target(RECEIPTS_PAGE, link)
        if target is not None and not target.exists():
            raise RuntimeError(f"broken local receipts link: {link}")

    finite = RECEIPTS / "evidence/finite-assay"
    review = RECEIPTS / "evidence/review"
    with tempfile.TemporaryDirectory(prefix="hpal-article2-") as directory:
        temp = Path(directory)
        finite_output = temp / "finite.json"
        subprocess.run(
            [sys.executable, str(finite / "run.py"), "--output", str(finite_output)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        if finite_output.read_bytes() != (finite / "result.json").read_bytes():
            raise RuntimeError("finite refund result does not reproduce byte-identically")

        anchor = temp / "anchor"
        anchor.mkdir()
        shutil.copy2(review / "cbc-anchor-check.py", anchor)
        shutil.copy2(review / "cbc-anchor-sample.csv", anchor)
        subprocess.run([sys.executable, str(anchor / "cbc-anchor-check.py")], check=True, stdout=subprocess.DEVNULL)
        if (anchor / "cbc-anchor-check.json").read_bytes() != (review / "cbc-anchor-check.json").read_bytes():
            raise RuntimeError("judge-calibration anchor result does not reproduce byte-identically")

        panel_output = temp / "panel.json"
        subprocess.run(
            [sys.executable, str(review / "cbc-panel-bundle-check.py"), "--output", str(panel_output)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        if panel_output.read_bytes() != (review / "cbc-panel-bundle-check.json").read_bytes():
            raise RuntimeError("judge-calibration panel result does not reproduce byte-identically")


def main() -> int:
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    if provenance.get("schema_version") != "hpal-illustration-provenance/v1":
        raise RuntimeError("unsupported illustration provenance")
    if provenance.get("claim_boundary") != "All images are conceptual editorial artwork, not research evidence.":
        raise RuntimeError("illustration claim boundary is missing")
    for reference in provenance["style_references"]:
        path = resolve_repo_path(reference["path"])
        if not path.is_file() or sha256(path) != reference["sha256"]:
            raise RuntimeError(f"style reference mismatch: {path}")
    for asset in provenance["assets"]:
        check_file_record(asset["source"])
        check_file_record(asset["public"])
        if "social" in asset:
            check_file_record(asset["social"])
        if not asset.get("generation_prompt") or not asset.get("qa"):
            raise RuntimeError(f"incomplete illustration provenance: {asset.get('name')}")
    verify_article(provenance)
    verify_receipts()
    css = (ROOT / "src/styles/editorial-article.css").read_text(encoding="utf-8")
    if "@media (max-width: 640px)" not in css:
        raise RuntimeError("article illustration styles lack the mobile breakpoint")
    print("PASS: Article 2 images, provenance, links, responsive styles, and evidence reruns verify")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
