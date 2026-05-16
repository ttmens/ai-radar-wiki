#!/usr/bin/env python3
"""
Build articles.html — scan daily-articles/ and embed full article content into the archive page.
Run after each new article is generated.
"""
import json
import os
import re
import base64
from datetime import datetime, timezone, timedelta

BJ_TZ = timezone(timedelta(hours=8))
WIKI_DIR = os.path.expanduser("~/ai-radar-wiki")
ARTICLES_DIR = os.path.join(WIKI_DIR, "daily-articles")
TEMPLATE = os.path.join(WIKI_DIR, "articles_template.html")
OUTPUT = os.path.join(WIKI_DIR, "articles.html")


def extract_article_info(filepath):
    """Extract metadata and content from an article HTML file."""
    fname = os.path.basename(filepath)

    # Parse date from filename: YYYY-MM-DD-title.html
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', fname)
    date_str = date_match.group(1) if date_match else ""

    # Parse title from filename
    title_match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.html', fname)
    title_from_file = title_match.group(1).replace('-', ' ').strip() if title_match else fname

    # Try to extract from HTML content
    title = title_from_file
    overview = ""
    content_html = ""

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to find <h1> tag
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        if h1_match:
            title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
            if not title:
                title = title_from_file

        # Try to find overview from first meaningful paragraph after h1
        if h1_match:
            after_h1 = content[h1_match.end():]
            p_match = re.search(r'<p[^>]*>(.*?)</p>', after_h1, re.DOTALL)
            if p_match:
                overview = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
                if len(overview) > 120:
                    overview = overview[:120] + "..."

        # Embed full content as base64 to avoid escaping issues
        content_html = base64.b64encode(content.encode('utf-8')).decode('ascii')

    except Exception as e:
        print(f"  ⚠️ Error reading {fname}: {e}")

    # File size
    size = os.path.getsize(filepath)
    size_str = f"{size / 1024:.1f}KB" if size > 1024 else f"{size}B"

    return {
        "id": date_str + "-" + re.sub(r'[^a-z0-9\u4e00-\u9fff]', '', fname.replace('.html', '').lower())[:40],
        "file": fname,
        "date": date_str,
        "title": title,
        "overview": overview,
        "size": size_str,
        "isLatest": False,
        "content": content_html  # Base64 encoded HTML content
    }


def main():
    print("🔨 Building articles.html...")

    # Scan articles directory
    if not os.path.exists(ARTICLES_DIR):
        print("  ⚠️ No articles directory found")
        articles = []
    else:
        files = sorted(
            [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html')],
            reverse=True  # Newest first
        )
        articles = []
        for i, fname in enumerate(files):
            filepath = os.path.join(ARTICLES_DIR, fname)
            info = extract_article_info(filepath)
            info["isLatest"] = (i == 0)
            articles.append(info)
            print(f"  📄 {info['date']} — {info['title'][:50]}...")

    # Sort by date descending
    articles.sort(key=lambda a: a["date"], reverse=True)
    if articles:
        articles[0]["isLatest"] = True

    # Read template
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()

    # Generate articles data as JavaScript
    articles_js = f"const ARTICLES = {json.dumps(articles, ensure_ascii=False, indent=2)};"

    # Replace placeholder
    output_html = template.replace("// {{ARTICLES_DATA}}", articles_js)

    # Write output
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(output_html)

    print(f"\n✅ Generated {OUTPUT}")
    print(f"   {len(articles)} articles")
    print(f"   Size: {os.path.getsize(OUTPUT) / 1024:.1f}KB")


if __name__ == "__main__":
    main()
