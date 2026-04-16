#!/usr/bin/env python3
"""
Batch update all article HTML files with new header/footer structure.
Preserves existing article content while updating surrounding HTML.
"""

import os
import re
from pathlib import Path

# List of all article files
ARTICLES = [
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
]

ARTICLE_SIDEBAR = '''<aside class="article-sidebar">
  <div class="sidebar-sponsor">
    <div class="sb-eyebrow">Presenting Sponsor</div>
    <div class="sidebar-sponsor-logo">Your Logo Here</div>
    <h4>Sponsor This Space</h4>
    <p>Reach payments &amp; fintech professionals. Enquire about article-level sponsorship.</p>
    <a href="mailto:advertising@theimmutableledger.com" class="btn-sponsor" style="font-size:11px;padding:8px 18px;">Enquire</a>
  </div>
  <div style="margin-bottom:12px;">
    <span class="ad-label">Advertisement</span>
    <div class="sidebar-ad-box" style="min-height:250px;">300×250 · AdSense slot</div>
  </div>
  <div>
    <span class="ad-label">Advertisement</span>
    <div class="sidebar-ad-box" style="min-height:300px;">300×600 · AdSense slot</div>
  </div>
</aside>'''

FOOTER = '''<footer>
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
  <p class="footer-copy">&copy; 2026 The Immutable Ledger.</p>
</footer>
<button class="back-top" onclick="window.scrollTo({top:0,behavior:'smooth'})">&#8679;</button>'''

def extract_article_content(html):
    """Extract the article content from existing HTML."""
    # Extract headline
    headline_match = re.search(r'<h1[^>]*class="article-headline"[^>]*>(.*?)</h1>', html, re.DOTALL)
    headline = headline_match.group(1) if headline_match else ''

    # Extract deck/subtitle
    deck_match = re.search(r'<p[^>]*class="article-sub"[^>]*>(.*?)</p>', html, re.DOTALL)
    deck = deck_match.group(1) if deck_match else ''

    # Extract byline info
    byline_match = re.search(r'<div class="article-byline">(.*?)</div>', html, re.DOTALL)
    byline = byline_match.group(1) if byline_match else ''

    # Extract hero image
    hero_match = re.search(r'<img[^>]*class="article-hero-img"[^>]*>', html)
    hero_img = hero_match.group(0) if hero_match else ''

    # Extract image caption
    caption_match = re.search(r'<p class="article-img-caption">(.*?)</p>', html, re.DOTALL)
    caption = caption_match.group(1) if caption_match else ''

    # Extract article body (everything inside article-body div)
    body_match = re.search(r'<div class="article-body">(.*?)</div>\s*<p class="article-signoff"', html, re.DOTALL)
    body = body_match.group(1) if body_match else ''

    # Extract signoff
    signoff_match = re.search(r'<p class="article-signoff">(.*?)</p>', html, re.DOTALL)
    signoff = signoff_match.group(1) if signoff_match else ''

    # Extract tags
    tags_match = re.search(r'<div class="article-tags">(.*?)</div>', html, re.DOTALL)
    tags = tags_match.group(1) if tags_match else ''

    # Extract related section
    related_match = re.search(r'<div class="article-related">(.*?)</div>\s*</div><!--\s*/article-main', html, re.DOTALL)
    related = related_match.group(1) if related_match else ''

    return {
        'headline': headline,
        'deck': deck,
        'byline': byline,
        'hero_img': hero_img,
        'caption': caption,
        'body': body,
        'signoff': signoff,
        'tags': tags,
        'related': related,
    }

def build_new_article_html(filename, content):
    """Build new article HTML with new structure."""
    # Determine a kicker based on filename
    kicker_map = {
        'best-sleep': 'CONFERENCES',
        'surcharge': 'PAYMENTS',
        'agentpay': 'AGENTIC AI',
        'agentic': 'AGENTIC AI',
        'becs': 'PAYMENTS',
        'cloud': 'TECHNOLOGY',
        'stablecoin': 'CRYPTO',
        'acacia': 'CRYPTO',
        'austrac': 'REGULATION',
        'bitcoin': 'CRYPTO',
        'conference': 'CONFERENCES',
        'summit': 'CONFERENCES',
        'readiness': 'TECHNOLOGY',
        'ai': 'REGULATION',
        'bnpl': 'CONSUMER',
    }

    slug = filename.replace('article-', '').replace('.html', '')
    kicker = kicker_map.get(slug, 'NEWS')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{content['headline'].replace('<a href=', '').replace('</a>', '').strip()} – The Immutable Ledger</title>
  <meta name="description" content="The Immutable Ledger — Subject to change. Fintech and payments news. All content fictional.">
  <link rel="stylesheet" href="style.css">
  <script>history.scrollRestoration = 'manual'; window.scrollTo(0, 0);</script>
</head>
<body>

<!-- UTIL BAR -->
<div class="util-bar">
  <div class="util-date">April 16, 2026</div>
  <div class="util-right">
    <button class="util-btn">Subscribe</button>
    <a href="donate.html" class="util-btn util-btn-red">Support Us</a>
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
    <div class="article-breadcrumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="index.html#{kicker.lower().replace(' ', '-')}">{kicker}</a> &nbsp;/&nbsp; Article</div>
    <div class="article-kicker">{kicker}</div>
    <h1 class="article-headline">{content['headline']}</h1>
    {f'<p class="article-deck">{content["deck"]}</p>' if content['deck'] else ''}
    {content['byline']}
    {content['hero_img']}
    {f'<p class="article-caption">{content["caption"]}</p>' if content['caption'] else ''}
    <div class="article-body">
{content['body']}
    </div>
    {f'<p class="article-signoff">{content["signoff"]}</p>' if content['signoff'] else ''}
    {f'<div class="article-tags">{content["tags"]}</div>' if content['tags'] else ''}
  </div>

  {ARTICLE_SIDEBAR}
</div>

{f'<div class="article-related">{content["related"]}</div>' if content['related'] else ''}

{FOOTER}

</body>
</html>
'''
    return html

def update_article(filepath):
    """Update a single article file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        old_html = f.read()

    content = extract_article_content(old_html)
    new_html = build_new_article_html(os.path.basename(filepath), content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return True

def main():
    article_dir = Path('/sessions/trusting-gallant-thompson/mnt/Cowork/The Immutable Ledger')

    for article_file in ARTICLES:
        filepath = article_dir / article_file
        if filepath.exists():
            try:
                update_article(filepath)
                print(f'✓ Updated {article_file}')
            except Exception as e:
                print(f'✗ Error updating {article_file}: {e}')
        else:
            print(f'! File not found: {article_file}')

    print('\nArticle update complete.')

if __name__ == '__main__':
    main()
