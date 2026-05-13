#!/usr/bin/env python3
"""
Bitable Sync Pipeline — reads cron outputs and writes structured data to Feishu Bitable.
Runs as a daily cron job at 06:30 (before the morning briefing).
"""

import json
import os
import re
import sys
import glob
import requests
from datetime import datetime, timedelta

# Config
CRON_OUTPUT_DIR = "/home/admin/.hermes/cron/output"
ENV_PATH = "/home/admin/.hermes/.env"
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
BITABLE_APP_TOKEN = os.getenv("BITABLE_APP_TOKEN", "")
BITABLE_TABLE_ID = os.getenv("BITABLE_TABLE_ID", "tblrHRQiNq6gsaJq")
STATE_FILE = "/home/admin/.hermes/cron/bitable_sync_state.json"

# Category mapping (cron job name → Bitable Category)
CATEGORY_MAP = {
    "每日AI资讯推送": "Global News",
    "ai-daily-briefing": "Global News",
    "github-ai-trending-digest": "GitHub",
    "dev-efficiency-tools-digest": "Product",
    "arxiv-paper-digest": "Paper",
    "ai-radar-weekly-digest": "Global News",
    "ai-design-tools-digest": "Design",
    "china-ai-news-digest": "China AI",
    "ai-funding-intelligence": "Funding",
    "ai-product-launch-tracker": "Product",
    "ai-community-buzz": "Community",
    "ai-company-strategy-watch": "Strategy",
    "ai-agent-framework-watch": "Product",
    "open-model-benchmark": "Product",
    "monthly-tech-trends": "Global News",
}

def get_app_secret():
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("FEISHU_APP_SECRET="):
                return line.strip().split("=", 1)[1]
    raise ValueError("FEISHU_APP_SECRET not found")

def get_token():
    app_secret = get_app_secret()
    r = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": app_secret})
    data = r.json()
    if data.get("code") != 0:
        raise Exception(f"Auth failed: {data}")
    return data["tenant_access_token"]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def parse_cron_output(filepath):
    """Parse a cron output markdown file and extract structured data."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Extract job metadata
    job_name = ""
    run_time = ""
    for line in content.split("\n"):
        if line.startswith("**Job ID:**"):
            job_id = line.split(":")[-1].strip()
        elif line.startswith("**Run Time:**"):
            run_time = line.split(":")[-1].strip()
            # Parse: 2026-05-06 07:11:45
            try:
                run_time = run_time.split(".")[0].strip()
            except:
                pass
        elif line.startswith("## Prompt") or line.startswith("## Response"):
            break

    # Extract the response part (after "## Response")
    resp_match = re.search(r"## Response\n(.*)", content, re.DOTALL)
    if not resp_match:
        return []

    response = resp_match.group(1).strip()

    # Determine category from directory
    dir_name = os.path.basename(os.path.dirname(filepath))
    category = CATEGORY_MAP.get(dir_name, "Global News")

    # Try to extract individual items from the response
    items = []

    # Pattern 1: Markdown headers with links
    # Look for patterns like "### 1️⃣ Title" or "#### 1. Title"
    sections = re.split(r"\n#{1,4}\s+\d+[\s️⃣📦📌🔥.]*", response)
    for section in sections[1:]:  # skip first empty section
        lines = section.strip().split("\n")
        title = lines[0].strip() if lines else ""
        if not title or len(title) > 200:
            continue

        # Extract link
        link_match = re.search(r"https?://[^\s\)]+", section)
        link = link_match.group(0) if link_match else ""

        # Extract summary (first 2-3 meaningful sentences)
        text_parts = []
        for line in lines[1:]:
            line = line.strip().lstrip("*-•").strip()
            if line and not line.startswith("原文链接") and not line.startswith("🔗"):
                text_parts.append(line)
        summary = " ".join(text_parts[:3])[:500]

        if title and summary:
            items.append({
                "Title": title[:200],
                "Category": category,
                "Date": run_time[:10] if run_time else datetime.now().strftime("%Y-%m-%d"),
                "Summary": summary,
                "Insight": "",
                "Link": link,
            })

    # If no structured items found, treat the whole response as one entry
    if not items:
        # Extract first meaningful paragraph
        paragraphs = [p.strip() for p in response.split("\n\n") if p.strip() and len(p) > 50]
        if paragraphs:
            first_para = paragraphs[0][:500]
            # Extract title from first line
            title_line = response.split("\n")[0].strip("#* ").strip()[:200]
            link_match = re.search(r"https?://[^\s\)]+", response)
            link = link_match.group(0) if link_match else ""

            items.append({
                "Title": title_line or "AI Intelligence Report",
                "Category": category,
                "Date": run_time[:10] if run_time else datetime.now().strftime("%Y-%m-%d"),
                "Summary": first_para,
                "Insight": "",
                "Link": link,
            })

    return items

def write_to_bitable(token, items):
    """Write items to Bitable one by one with rate limiting."""
    if not items:
        print("No items to write.")
        return 0

    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BITABLE_APP_TOKEN}/tables/{BITABLE_TABLE_ID}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    total_written = 0
    for idx, item in enumerate(items):
        try:
            # Convert date to timestamp
            date_ts = 0
            if item.get("Date"):
                try:
                    dt = datetime.strptime(item["Date"], "%Y-%m-%d")
                    date_ts = int(dt.timestamp() * 1000)
                except:
                    pass

            # Convert link to URL object
            link_obj = {"text": "", "link": ""}
            link_val = item.get("Link", "")
            if link_val and link_val.startswith("http"):
                # Extract clean URL (remove markdown artifacts)
                link_val = link_val.split(")")[0].split("]")[0].strip()
                link_obj = {"text": link_val.split("/")[-1][:50] or "Link", "link": link_val}

            # Truncate fields to safe lengths
            title = (item.get("Title", "") or "")[:150]
            summary = (item.get("Summary", "") or "")[:2000]
            insight = (item.get("Insight", "") or "")[:2000]
            category = (item.get("Category", "") or "Global News")[:50]

            payload = {
                "fields": {
                    "Title": title,
                    "Category": category,
                    "Date": date_ts,
                    "Summary": summary,
                    "Insight": insight,
                    "Link": link_obj,
                }
            }
            r = requests.post(url, headers=headers, json=payload)
            result = r.json()

            if result.get("code") == 0:
                total_written += 1
                if total_written % 10 == 0:
                    print(f"  ✅ {total_written}/{len(items)} written...")
            else:
                msg = result.get("msg", "")
                # Skip silently on validation errors
                if "validation" in msg.lower() or "field" in msg.lower():
                    pass  # skip bad records
                else:
                    print(f"  ⚠️ [{idx+1}] {title[:30]} — {msg}")

            # Rate limit: 50 req/s for Feishu, be conservative
            import time
            time.sleep(0.05)

        except Exception as e:
            print(f"  ⚠️ Error on item {idx+1}: {e}")

    return total_written

def main():
    print(f"🔄 Bitable Sync started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    state = load_state()
    token = get_token()

    all_items = []
    new_files = 0

    # Scan all cron output directories
    for job_dir in sorted(glob.glob(os.path.join(CRON_OUTPUT_DIR, "*"))):
        if not os.path.isdir(job_dir):
            continue

        job_id = os.path.basename(job_dir)
        processed = state.get(job_id, [])

        # Find all .md files
        for md_file in sorted(glob.glob(os.path.join(job_dir, "*.md"))):
            if md_file in processed:
                continue

            try:
                items = parse_cron_output(md_file)
                if items:
                    all_items.extend(items)
                    new_files += 1
                    processed.append(md_file)
                    print(f"  📄 Parsed {md_file}: {len(items)} items")
            except Exception as e:
                print(f"  ⚠️ Failed to parse {md_file}: {e}")

        state[job_id] = processed

    if not all_items:
        print("✅ No new data to sync.")
        return

    print(f"\n📊 Total items to write: {len(all_items)}")
    written = write_to_bitable(token, all_items)

    save_state(state)
    print(f"\n✅ Sync complete: {new_files} files parsed, {written} records written to Bitable")

if __name__ == "__main__":
    main()
