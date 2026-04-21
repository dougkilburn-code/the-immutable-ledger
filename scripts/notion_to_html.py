#!/usr/bin/env python3
"""
notion_to_html.py — The Immutable Ledger publishing script
-----------------------------------------------------------
Reads articles from Notion with Status = "In progress" (Ready to Publish),
generates article-{slug}.html files in the site root, prepends a card to the
correct category section in index.html, then marks articles as Done in Notion.

Usage:
    python3 scripts/notion_to_html.py

Requirements:
    pip3 install notion-client python-dotenv
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip3 install notion-client python-dotenv")
    sys.exit(1)

try:
    from notion_client import Client
except ImportError:
    print("ERROR: notion-client not installed. Run: pip3 install notion-client python-dotenv")
    sys.exit(1)

# ── Configuration ─────────────────────────────────────────────────────────────

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID  = os.getenv("NOTION_DATABASE_ID")
SITE_ROOT    = Path(__file__).parent.parent  # repo root

# Map Category values to homepage section anchor IDs
CATEGORY_ANCHORS = {
    "Payments":   "payments",
    "Technology": "technology",
    "Agentic AI": "agentic",
    "Crypto":     "crypto",
    "Regulation": "regulation",
    "Consumer":   "consumer",
    "Conferences":"conferences",
}

# ── Notion helpers ────────────────────────────────────────────────────────────

def get_plain_text(rich_text_array):
    return "".join(t.get("plain_text", "") for t in (rich_text_array or []))


def get_property(props, name, fallback=""):
    prop = props.get(name)
    if not prop:
        return fallback
    t = prop.get("type")
    if t == "title":
        return get_plain_text(prop.get("title", []))
    if t == "rich_text":
        return get_plain_text(prop.get("rich_text", []))
    if t == "select":
        sel = prop.get("select")
        return sel["name"] if sel else fallback
    if t == "date":
        d = prop.get("date")
        return d["start"] if d else fallback
    if t == "status":
        s = prop.get("status")
        return s["name"] if s else fallback
    if t == "url":
        return prop.get("url") or fallback
    return fallback


def fetch_all_blocks(notion, block_id):
    """Fetch all child blocks, handling pagination."""
    results = []
    cursor = None
    while True:
        resp = notion.blocks.children.list(block_id=block_id, start_cursor=cursor)
        results.extend(resp["results"])
        if not resp.get("has_more"):
            break
        cursor = resp["next_cursor"]
    return results


def blocks_to_html(blocks):
    """Convert Notion blocks to HTML for article body."""
    html_parts = []
    in_list = False
    list_type = None

    def close_list():
        nonlocal in_list, list_type
        if in_list:
            html_parts.append(f"</{list_type}>")
            in_list = False
            list_type = None

    def rich_text_to_html(rt_array):
        out = []
        for rt in (rt_array or []):
            text = rt.get("plain_text", "")
            # Escape HTML
            text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            ann = rt.get("annotations", {})
            if ann.get("bold"):
                text = f"<strong>{text}</strong>"
            if ann.get("italic"):
                text = f"<em>{text}</em>"
            if ann.get("code"):
                text = f"<code>{text}</code>"
            link = rt.get("href")
            if link:
                text = f'<a href="{link}">{text}</a>'
            out.append(text)
        return "".join(out)

    for block in blocks:
        btype = block.get("type")
        val   = block.get(btype, {})
        rt    = val.get("rich_text", [])
        text  = rich_text_to_html(rt)

        if btype == "paragraph":
            close_list()
            if text.strip():
                html_parts.append(f"<p>{text}</p>")
        elif btype == "heading_1":
            close_list()
            html_parts.append(f"<h2>{text}</h2>")
        elif btype == "heading_2":
            close_list()
            html_parts.append(f"<h3>{text}</h3>")
        elif btype == "heading_3":
            close_list()
            html_parts.append(f"<h4>{text}</h4>")
        elif btype == "bulleted_list_item":
            if not in_list or list_type != "ul":
                close_list()
                html_parts.append("<ul>")
                in_list = True
                list_type = "ul"
            html_parts.append(f"<li>{text}</li>")
        elif btype == "numbered_list_item":
            if not in_list or list_type != "ol":
                close_list()
                html_parts.append("<ol>")
                in_list = True
                list_type = "ol"
            html_parts.append(f"<li>{text}</li>")
        elif btype == "quote":
            close_list()
            html_parts.append(f"<blockquote>{text}</blockquote>")
        elif btype == "divider":
            close_list()
            html_parts.append("<hr>")
        elif btype == "code":
            close_list()
            code_text = get_plain_text(rt).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_parts.append(f"<pre><code>{code_text}</code></pre>")
        elif btype == "image":
            close_list()
            img_url = (val.get("file") or val.get("external") or {}).get("url", "")
            caption = rich_text_to_html(val.get("caption", []))
            html_parts.append(f'<figure><img src="{img_url}" alt="{caption}"><figcaption>{caption}</figcaption></figure>')
        # skip unsupported block types silently

    close_list()
    return "\n".join(html_parts)


# ── HTML template ─────────────────────────────────────────────────────────────

def format_display_date(iso_date):
    """Convert 2026-04-18 → APRIL 18, 2026"""
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y").upper()
    except Exception:
        return iso_date.upper()


def build_article_html(title, slug, date_iso, category, summary, author, hero_image, body_html):
    category_upper  = category.upper()
    anchor          = CATEGORY_ANCHORS.get(category, category.lower().replace(" ", "-"))
    display_date    = format_display_date(date_iso)
    hero_src        = f"img/clean_images/{hero_image}" if hero_image else "img/clean_images/article-ai.jpg"
    title_escaped   = title.replace('"', '&quot;')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title} – The Immutable Ledger</title>
<meta content="The Immutable Ledger — Subject to change. Fintech and payments news. All content fictional." name="description"/>
<link href="style.css?v=4" rel="stylesheet"/>
<script>history.scrollRestoration = 'manual'; window.scrollTo(0, 0);</script>
</head>
<body>
<!-- UTIL BAR -->
<div class="util-bar">
<div class="util-date">{datetime.now().strftime("%B %-d, %Y")}</div>
<div class="util-right">
<button class="util-btn">Subscribe</button>
<a class="util-btn util-btn-red" href="donate.html">Support Us</a>
</div>
</div>
<!-- MASTHEAD -->
<header class="masthead">
<div class="masthead-logo"><a href="index.html">THE IMMUTABLE LEDGER</a></div>
<div class="masthead-tagline">Subject to change</div>
</header>
<!-- NAV -->
<div class="nav-bar">
<nav>
<a href="index.html#payments">PAYMENTS</a>
<a href="index.html#technology">TECHNOLOGY</a>
<a href="index.html#agentic">AGENTIC AI</a>
<a href="index.html#crypto">CRYPTO</a>
<a href="index.html#regulation">REGULATION</a>
<a href="index.html#consumer">CONSUMER</a>
<a href="index.html#conferences">CONFERENCES</a>
<a href="people.html">PEOPLE</a>
</nav>
</div>
<!-- AD LEADERBOARD -->
<div class="ad-leaderboard">
<div class="ad-leaderboard-inner">970×90 · Advertisement</div>
</div>
<!-- ARTICLE PAGE -->
<div class="article-page">
<div class="article-inner">
<div class="article-breadcrumb"><a href="index.html">Home</a>  /  <a href="index.html#{anchor}">{category_upper}</a>  /  Article</div>
<div class="article-kicker">{category_upper}</div>
<h1 class="article-headline">{title}</h1>
<p class="article-deck">{summary}</p>
<div class="article-byline">
<div class="byline-info">
<div class="byline-name">{author}</div>
<div class="byline-meta">{category_upper} · {display_date}</div>
</div>
</div>
<img alt="" class="article-hero-img" src="{hero_src}"/>
<p class="article-caption"></p>
<div class="article-body">
{body_html}
</div>
<p class="article-signoff"><em>The Immutable Ledger</em></p>
</div>
<aside class="article-sidebar">
<div class="sidebar-sponsor">
<div class="sb-eyebrow">Presenting Sponsor</div>
<div class="sidebar-sponsor-logo">Your Logo Here</div>
<h4>Sponsor This Space</h4>
<p>Reach payments &amp; fintech professionals. Enquire about article-level sponsorship.</p>
<a class="btn-sponsor" href="mailto:advertising@theimmutableledger.com" style="font-size:11px;padding:8px 18px;">Enquire</a>
</div>
<div style="margin-bottom:12px;">
<span class="ad-label">Advertisement</span>
<div class="sidebar-ad-box" style="min-height:250px;">300×250 · AdSense slot</div>
</div>
<div>
<span class="ad-label">Advertisement</span>
<div class="sidebar-ad-box" style="min-height:300px;">300×600 · AdSense slot</div>
</div>
</aside>
</div>
<footer>
<div class="footer-logo">THE IMMUTABLE LEDGER</div>
<div class="footer-tagline">Subject to change</div>
<nav class="footer-nav-desktop">
<a href="index.html#payments">Payments</a>
<a href="index.html#technology">Technology</a>
<a href="index.html#agentic">Agentic AI</a>
<a href="index.html#crypto">Crypto</a>
<a href="index.html#regulation">Regulation</a>
<a href="index.html#consumer">Consumer</a>
<a href="index.html#conferences">Conferences</a>
<a href="people.html">Our Team</a>
<a href="donate.html">Support Us</a>
</nav>
<nav class="footer-nav-mobile">
<a href="index.html">Home</a>
<a href="people.html">Our Team</a>
<a href="donate.html">Support Us</a>
</nav>
<p class="footer-disclaimer">Satirical publication. All content fictional. Any resemblance to actual events, institutions, or persons is coincidental.</p>
<p class="footer-copy">&#169; {datetime.now().year} The Immutable Ledger.</p>
</footer>
<button class="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">&#8679;</button>
</body>
</html>
"""


# ── index.html injection ──────────────────────────────────────────────────────

def make_desktop_card(title, slug, date_iso, category, summary, hero_image):
    """Build an sg-card div for the desktop category section."""
    display_date = format_display_date(date_iso)
    category_upper = category.upper()
    hero_src = f"img/clean_images/{hero_image}" if hero_image else "img/clean_images/article-ai.jpg"
    return (
        f'\n<div class="sg-card">\n'
        f'<img alt="" src="{hero_src}"/>\n'
        f'<span class="s-kicker">{category_upper}</span>\n'
        f'<h3><a href="article-{slug}.html">{title}</a></h3>\n'
        f'<p>{summary}</p>\n'
        f'<span class="s-meta">{display_date}</span>\n'
        f'</div>'
    )


def make_mobile_card(title, slug, date_iso, category, hero_image):
    """Build a mobile-card anchor for the mobile category section."""
    display_date = format_display_date(date_iso)
    category_upper = category.upper()
    hero_src = f"img/clean_images/{hero_image}" if hero_image else "img/clean_images/article-ai.jpg"
    return (
        f'\n<a class="mobile-card" href="article-{slug}.html">\n'
        f'<img alt="" src="{hero_src}"/>\n'
        f'<div class="mobile-card-body">\n'
        f'<span class="s-kicker">{category_upper}</span>\n'
        f'<h3>{title}</h3>\n'
        f'<span class="s-meta">{display_date}</span>\n'
        f'</div>\n'
        f'</a>'
    )


def inject_into_index(index_path, title, slug, date_iso, category, summary, hero_image):
    """
    Prepend new article cards into the appropriate sections of index.html.
    Touches two places:
      1. The desktop category section: <!-- PAYMENTS SECTION -->, etc.
      2. The mobile section strip for the same category.
    """
    html = index_path.read_text(encoding="utf-8")

    # Skip if article already present
    if f"article-{slug}.html" in html:
        print(f"  index.html already contains article-{slug}.html — skipping injection")
        return

    anchor = CATEGORY_ANCHORS.get(category, category.lower().replace(" ", "-"))

    # ── Desktop category section ──────────────────────────────────────────────
    # Find the <div class="story-grid-4"> immediately inside the <div id="{anchor}"> section
    desktop_pattern = re.compile(
        r'(<div id="' + re.escape(anchor) + r'"[^>]*>.*?<div class="story-grid-\d+">)',
        re.DOTALL
    )
    desktop_card = make_desktop_card(title, slug, date_iso, category, summary, hero_image)
    html, n_desktop = desktop_pattern.subn(r'\1' + desktop_card, html, count=1)
    if n_desktop == 0:
        print(f"  WARNING: Could not find desktop section for category '{category}' in index.html")

    # ── Mobile section strip ──────────────────────────────────────────────────
    category_upper = category.upper()
    mobile_pattern = re.compile(
        r'(<span class="mobile-section-label">' + re.escape(category_upper) + r'</span>\s*<div class="mobile-strip">)',
        re.DOTALL
    )
    mobile_card = make_mobile_card(title, slug, date_iso, category, hero_image)
    html, n_mobile = mobile_pattern.subn(r'\1' + mobile_card, html, count=1)
    if n_mobile == 0:
        print(f"  WARNING: Could not find mobile section for category '{category}' in index.html")

    index_path.write_text(html, encoding="utf-8")
    print(f"  Updated index.html with article-{slug} in {category} section")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not NOTION_TOKEN:
        print("ERROR: NOTION_TOKEN not set. Create a .env file — see .env.example")
        sys.exit(1)
    if not DATABASE_ID:
        print("ERROR: NOTION_DATABASE_ID not set. Create a .env file — see .env.example")
        sys.exit(1)

    notion = Client(auth=NOTION_TOKEN)
    index_path = SITE_ROOT / "index.html"

    print("Querying Notion for articles with Status = In progress (Ready to Publish)…")

    response = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "Status",
            "status": {"equals": "In progress"}
        }
    )

    pages = response.get("results", [])
    if not pages:
        print("No articles ready to publish. Set Status to 'In progress' in Notion.")
        return

    print(f"Found {len(pages)} article(s) to publish.\n")

    for page in pages:
        props = page["properties"]

        title      = get_property(props, "Title")
        slug       = get_property(props, "Slug")
        date_iso   = get_property(props, "Date")
        category   = get_property(props, "Category")
        summary    = get_property(props, "Summary")
        author     = get_property(props, "Author", "The Immutable Ledger")
        hero_image = get_property(props, "HeroImage")

        if not title:
            print(f"  SKIP: Page {page['id']} has no Title — skipping")
            continue
        if not slug:
            # Derive slug from title if not set
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            print(f"  WARNING: No Slug set for '{title}' — using derived slug: {slug}")
        if not date_iso:
            date_iso = datetime.now().strftime("%Y-%m-%d")
            print(f"  WARNING: No Date set for '{title}' — using today: {date_iso}")
        if not category:
            category = "Payments"
            print(f"  WARNING: No Category set for '{title}' — defaulting to Payments")

        print(f"Processing: {title} ({slug})")

        # Fetch body blocks
        blocks    = fetch_all_blocks(notion, page["id"])
        body_html = blocks_to_html(blocks)

        # Generate article HTML
        article_html = build_article_html(
            title, slug, date_iso, category, summary, author, hero_image, body_html
        )

        out_path = SITE_ROOT / f"article-{slug}.html"
        out_path.write_text(article_html, encoding="utf-8")
        print(f"  Created {out_path.name}")

        # Update index.html
        if index_path.exists():
            inject_into_index(index_path, title, slug, date_iso, category, summary, hero_image)

        # Mark as Done in Notion
        notion.pages.update(
            page_id=page["id"],
            properties={"Status": {"status": {"name": "Done"}}}
        )
        print(f"  Marked '{title}' as Done in Notion\n")

    print("Done. Review the new files, then run: git add . && git commit -m 'Publish new article' && git push")


if __name__ == "__main__":
    main()
