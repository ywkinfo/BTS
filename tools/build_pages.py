#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = "https://bts-volvio.example"
TEXT_FILES = {
    ".html",
    ".xml",
    ".txt",
    ".json",
    ".webmanifest",
    ".css",
    ".js",
    ".svg",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a GitHub Pages-ready static bundle for BTS volvió."
    )
    parser.add_argument(
        "--site-url",
        required=True,
        help="Absolute production URL, for example https://owner.github.io/repo",
    )
    parser.add_argument(
        "--output-dir",
        default="_site",
        help="Directory where the built site will be written",
    )
    return parser.parse_args()


def copy_tree(src: Path, dest: Path) -> None:
    shutil.copytree(src, dest, dirs_exist_ok=True)


def replace_placeholder_in_text_files(output_dir: Path, site_url: str) -> None:
    for path in output_dir.rglob("*"):
      if not path.is_file():
        continue
      if path.suffix not in TEXT_FILES:
        continue

      text = path.read_text(encoding="utf-8")
      updated = text.replace(PLACEHOLDER, site_url.rstrip("/"))
      if updated != text:
        path.write_text(updated, encoding="utf-8")


def write_nojekyll(output_dir: Path) -> None:
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = (ROOT / args.output_dir).resolve()

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    for file_name in ("index.html", "404.html", "robots.txt", "sitemap.xml", "site.webmanifest"):
        shutil.copy2(ROOT / file_name, output_dir / file_name)

    for dir_name in ("assets", "pages", "scripts", "styles"):
        copy_tree(ROOT / dir_name, output_dir / dir_name)

    replace_placeholder_in_text_files(output_dir, args.site_url)
    write_nojekyll(output_dir)

    print(f"Built site in {output_dir}")
    print(f"Site URL: {args.site_url.rstrip('/')}")


if __name__ == "__main__":
    main()
