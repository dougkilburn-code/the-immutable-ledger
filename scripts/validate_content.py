#!/usr/bin/env python3
"""
validate_content.py — The Immutable Ledger content validator
-------------------------------------------------------------
Checks all article-*.html files in the site root for:
  - Required content (headline, article body)
  - Duplicate slugs
  - Missing hero images

Usage:
    python3 scripts/validate_content.py
"""

import re
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent

REQUIRED_PATTERNS = {
    "headline":   re.compile(r'<h1[^>]*class="article-headline"[^>]*>.+?</h1>', re.DOTALL),
    "article body": re.compile(r'<div class="article-body">\s*.+?\s*</div>', re.DOTALL),
    "category kicker": re.compile(r'<div class="article-kicker">.+?</div>'),
    "byline":     re.compile(r'<div class="article-byline">'),
}


def extract_slug(filename):
    """article-bnpl.html → bnpl"""
    return re.sub(r'^article-(.+)\.html$', r'\1', filename)


def validate_article(path):
    errors = []
    html = path.read_text(encoding="utf-8")

    for field, pattern in REQUIRED_PATTERNS.items():
        if not pattern.search(html):
            errors.append(f"missing {field}")

    # Check hero image src exists on disk
    hero_match = re.search(r'<img[^>]+class="article-hero-img"[^>]+src="([^"]+)"', html)
    if hero_match:
        hero_src = hero_match.group(1)
        hero_path = SITE_ROOT / hero_src
        if not hero_path.exists():
            errors.append(f"hero image not found: {hero_src}")
    else:
        errors.append("missing hero image tag")

    return errors


def main():
    article_files = sorted(SITE_ROOT.glob("article-*.html"))

    if not article_files:
        print("No article-*.html files found in repo root.")
        sys.exit(1)

    print(f"Validating {len(article_files)} article(s)…\n")

    seen_slugs = {}
    has_errors = False

    for path in article_files:
        slug   = extract_slug(path.name)
        errors = validate_article(path)

        # Check for duplicate slugs
        if slug in seen_slugs:
            errors.append(f"duplicate slug '{slug}' (also in {seen_slugs[slug]})")
        else:
            seen_slugs[slug] = path.name

        if errors:
            has_errors = True
            for err in errors:
                print(f"  FAIL  {path.name}: {err}")
        else:
            print(f"  OK    {path.name}")

    print()
    if has_errors:
        print("Validation failed. Fix the errors above before publishing.")
        sys.exit(1)
    else:
        print(f"All {len(article_files)} articles passed validation.")


if __name__ == "__main__":
    main()
