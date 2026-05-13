#!/usr/bin/env python3
"""Generate RSS 2.0 feed from graph.json data."""

import json
import os
from datetime import datetime
from xml.sax.saxutils import escape

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
GRAPH_JSON = os.path.join(os.path.expanduser("~/ai-radar-wiki"), "graph.json")
RSS_OUTPUT = os.path.join(os.path.expanduser("~/ai-radar-wiki"), "feed.xml")

SITE_URL = "https://ttmens.github.io/ai-radar-wiki"
FEED_TITLE = "AI Radar - 每日情报摘要"
FEED_DESCRIPTION = "AI 产品设计雷达 - 自动化追踪 AI 领域最新技术、产品、商业动态"
FEED_LANGUAGE = "zh-CN"

PILLAR_NAMES = {
    "capabilities": "🤖 技术能力",
    "patterns": "📱 产品模式",
    "ecosystem": "🔧 工具生态",
    "business": "💰 商业趋势",
}


def generate_rss():
    """Generate RSS 2.0 XML from graph.json."""
    if not os.path.exists(GRAPH_JSON):
        print(f"Error: {GRAPH_JSON} not found")
        return

    with open(GRAPH_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    # Filter out concept nodes, only keep real items
    items = [n for n in nodes if n.get("type") != "concept"]
    # Sort by date descending, then by pm_score
    items.sort(key=lambda x: (x.get("date", ""), x.get("pm_score", 0)), reverse=True)
    # Take top 50 for feed
    items = items[:50]

    now = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        f'    <title>{escape(FEED_TITLE)}</title>',
        f'    <link>{SITE_URL}/graph.html</link>',
        f'    <description>{escape(FEED_DESCRIPTION)}</description>',
        f'    <language>{FEED_LANGUAGE}</language>',
        f'    <lastBuildDate>{now}</lastBuildDate>',
        f'    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>',
        '    <image>',
        f'      <url>{SITE_URL}/og-image.png</url>',
        f'      <title>{escape(FEED_TITLE)}</title>',
        f'      <link>{SITE_URL}/graph.html</link>',
        '    </image>',
    ]

    for item in items:
        node_id = item.get("id", "")
        title = escape(item.get("label", "Untitled"))
        date = item.get("date", "")
        summary = escape(item.get("summary", "暂无摘要"))
        url = item.get("url", "")
        pillar = item.get("pillar", "unknown")
        pm_score = item.get("pm_score", 0)
        node_type = item.get("type", "")

        link = url if url else f"{SITE_URL}/graph.html"
        pub_date = f"{date}T00:00:00+00:00" if date else now

        # Build description with metadata
        pillar_name = PILLAR_NAMES.get(pillar, pillar)
        description = (
            f"<p><strong>分类:</strong> {pillar_name}</p>"
            f"<p><strong>PM Score:</strong> {pm_score:.1f}/10</p>"
            f"<p><strong>类型:</strong> {node_type}</p>"
            f"<hr/><p>{summary}</p>"
        )

        xml_parts.extend([
            '    <item>',
            f'      <title>{title}</title>',
            f'      <link>{escape(link)}</link>',
            f'      <guid isPermaLink="false">{escape(node_id)}</guid>',
            f'      <pubDate>{pub_date}</pubDate>',
            f'      <description>{description}</description>',
            f'      <category>{escape(pillar_name)}</category>',
            '    </item>',
        ])

    xml_parts.extend([
        '  </channel>',
        '</rss>',
    ])

    rss_xml = "\n".join(xml_parts)

    with open(RSS_OUTPUT, "w", encoding="utf-8") as f:
        f.write(rss_xml)

    print(f"RSS feed generated: {RSS_OUTPUT}")
    print(f"Items: {len(items)}")


if __name__ == "__main__":
    generate_rss()
