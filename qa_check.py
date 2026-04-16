#!/usr/bin/env python3
"""
QA script for The Immutable Ledger website.
Checks: link resolution, metadata, structure, content requirements.
"""

import os
import re
from pathlib import Path

# Define all valid HTML files
VALID_FILES = {
    'index.html',
    'people.html',
    'donate.html',
    'style.css',
    'article-best-sleep.html',
    'article-surcharge.html',
    'article-agentpay.html',
    'article-agentic.html',
    'article-becs.html',
    'article-cloud.html',
    'article-stablecoin.html',
    'article-acacia.html',
    'article-austrac.html',
    'article-bitcoin.html',
    'article-conference.html',
    'article-summit.html',
    'article-readiness.html',
    'article-ai.html',
    'article-bnpl.html',
}

ARTICLE_DIR = Path('/sessions/trusting-gallant-thompson/mnt/Cowork/The Immutable Ledger')
FAILURES = []
WARNINGS = []

def check_file_exists(filepath):
    """Check if file exists."""
    if not filepath.exists():
        FAILURES.append(f"FILE MISSING: {filepath.name}")
        return False
    return True

def check_charset(content):
    """Check for UTF-8 charset declaration."""
    if '<meta charset="UTF-8">' not in content and '<meta charset=UTF-8>' not in content:
        return False
    return True

def check_viewport(content):
    """Check for viewport meta tag."""
    if 'viewport' not in content:
        return False
    return True

def check_title(content):
    """Check for title tag."""
    if '<title>' not in content or '</title>' not in content:
        return False
    return True

def check_description(content):
    """Check for meta description."""
    if 'name="description"' not in content:
        return False
    return True

def check_stylecss(content):
    """Check for style.css link."""
    if 'href="style.css"' not in content:
        return False
    return True

def check_satirical_disclaimer(content):
    """Check for satirical publication disclaimer."""
    if 'Satirical publication' not in content:
        return False
    return True

def check_subject_to_change(content):
    """Check for 'Subject to change' tagline."""
    if 'Subject to change' not in content:
        return False
    return True

def extract_href_links(content):
    """Extract all href links from content."""
    pattern = r'href=["\']([^"\']+)["\']'
    return re.findall(pattern, content)

def check_href_links(filepath, content, filename):
    """Check that href links point to valid files."""
    links = extract_href_links(content)
    for link in links:
        # Skip external URLs, anchor links
        if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
            continue
        # Check if file exists
        link_file = link.split('#')[0]  # Remove anchor
        if link_file and link_file not in VALID_FILES:
            FAILURES.append(f"INVALID HREF in {filename}: {link}")

def check_no_empty_href(content, filename):
    """Check that no href="#" exists (except section anchors)."""
    # Find href="#" that are not valid section anchors
    pattern = r'href="#([^"]*)"'
    matches = re.findall(pattern, content)
    for match in matches:
        anchor = match
        # Valid anchors: payments, technology, agentic, crypto, regulation, consumer, conferences, global, people
        valid_anchors = {
            '', 'payments', 'technology', 'agentic', 'crypto', 'regulation',
            'consumer', 'conferences', 'global', 'people', 'payment'
        }
        if anchor not in valid_anchors:
            WARNINGS.append(f"UNUSUAL ANCHOR in {filename}: #{anchor}")

def check_mobile_feed_unique(content, filename):
    """Check that #mobile-feed only exists in index.html."""
    if 'id="mobile-feed"' in content:
        if filename != 'index.html':
            FAILURES.append(f"MOBILE FEED in {filename}: #mobile-feed should only exist in index.html")

def check_style_css_exists():
    """Check that style.css exists."""
    css_file = ARTICLE_DIR / 'style.css'
    if not css_file.exists():
        FAILURES.append("FILE MISSING: style.css")
        return False
    return True

def check_media_query_exists():
    """Check that @media (max-width: 600px) exists in style.css."""
    css_file = ARTICLE_DIR / 'style.css'
    if not css_file.exists():
        return False
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    if '@media (max-width: 600px)' not in css_content and '@media (max-width:600px)' not in css_content:
        FAILURES.append("MISSING MOBILE MEDIA QUERY in style.css")
        return False
    return True

def check_no_editorial_calendar(content, filename):
    """Check that no reference to editorial-calendar.html exists."""
    if 'editorial-calendar.html' in content:
        FAILURES.append(f"INVALID REFERENCE in {filename}: editorial-calendar.html should not be referenced")

def run_checks():
    """Run all QA checks."""
    print("=" * 70)
    print("THE IMMUTABLE LEDGER — QA CHECKS")
    print("=" * 70)

    # Check style.css
    print("\n1. Checking style.css...")
    if check_style_css_exists():
        if check_media_query_exists():
            print("   ✓ style.css exists and has @media query")
        else:
            print("   ✗ style.css missing mobile media query")
    else:
        print("   ✗ style.css not found")

    # Check each HTML file
    print("\n2. Checking HTML files...")
    for filename in sorted([f for f in VALID_FILES if f.endswith('.html')]):
        filepath = ARTICLE_DIR / filename
        if not check_file_exists(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Run checks
        checks = {
            'charset': check_charset(content),
            'viewport': check_viewport(content),
            'title': check_title(content),
            'description': check_description(content),
            'style.css': check_stylecss(content),
            'satirical disclaimer': check_satirical_disclaimer(content),
            'Subject to change': check_subject_to_change(content),
        }

        failed_checks = [k for k, v in checks.items() if not v]
        if failed_checks:
            print(f"   ✗ {filename}: missing {', '.join(failed_checks)}")
        else:
            print(f"   ✓ {filename}")

        # Additional checks
        check_href_links(filepath, content, filename)
        check_no_empty_href(content, filename)
        check_mobile_feed_unique(content, filename)
        check_no_editorial_calendar(content, filename)

    # Print results
    print("\n" + "=" * 70)
    if FAILURES:
        print("FAILURES:")
        for failure in FAILURES:
            print(f"  ✗ {failure}")
    else:
        print("✓ ALL CRITICAL CHECKS PASSED")

    if WARNINGS:
        print("\nWARNINGS:")
        for warning in WARNINGS:
            print(f"  ⚠ {warning}")

    print("=" * 70)
    return len(FAILURES) == 0

if __name__ == '__main__':
    success = run_checks()
    exit(0 if success else 1)
