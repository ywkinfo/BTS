#!/usr/bin/env python3

from __future__ import annotations

import argparse
from html import escape
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
    parser.add_argument(
        "--search-console-verification",
        default="",
        help="Optional Google Search Console verification token for the homepage",
    )
    parser.add_argument(
        "--ga4-measurement-id",
        default="",
        help="Optional GA4 measurement ID, for example G-XXXXXXXXXX",
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


def insert_before_head_close(content: str, snippet: str) -> str:
    marker = "  </head>"
    if marker not in content:
        raise ValueError("Expected closing </head> tag was not found in HTML output.")
    return content.replace(marker, f"{snippet}\n{marker}", 1)


def make_search_console_meta(token: str) -> str:
    escaped = escape(token, quote=True)
    return f'    <meta name="google-site-verification" content="{escaped}" />'


def make_ga4_snippet(measurement_id: str) -> str:
    escaped = escape(measurement_id, quote=True)
    return "\n".join(
        [
            f'    <script async src="https://www.googletagmanager.com/gtag/js?id={escaped}"></script>',
            "    <script>",
            "      window.dataLayer = window.dataLayer || [];",
            "      function gtag(){dataLayer.push(arguments);}",
            '      gtag("js", new Date());',
            f'      gtag("config", "{escaped}");',
            "    </script>",
        ]
    )


def inject_optional_html_tags(
    output_dir: Path,
    search_console_verification: str,
    ga4_measurement_id: str,
) -> None:
    for path in output_dir.rglob("*.html"):
        content = path.read_text(encoding="utf-8")
        snippets: list[str] = []

        if path.name == "index.html" and search_console_verification:
            snippets.append(make_search_console_meta(search_console_verification))

        if ga4_measurement_id:
            snippets.append(make_ga4_snippet(ga4_measurement_id))

        if not snippets:
            continue

        updated = insert_before_head_close(content, "\n".join(snippets))
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
    inject_optional_html_tags(
        output_dir,
        args.search_console_verification.strip(),
        args.ga4_measurement_id.strip(),
    )
    write_nojekyll(output_dir)

    print(f"Built site in {output_dir}")
    print(f"Site URL: {args.site_url.rstrip('/')}")
    print(
        "Search Console verification: "
        + ("enabled" if args.search_console_verification.strip() else "disabled")
    )
    print("GA4: " + ("enabled" if args.ga4_measurement_id.strip() else "disabled"))


if __name__ == "__main__":
    main()
