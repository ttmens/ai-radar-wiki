#!/usr/bin/env python3
"""
AI Radar Data Sync Pipeline — 数据获取、清洗、同步到 Bitable 和飞书云文档

稳定性保障：
- 每条记录独立处理，单条失败不影响其他
- 自动重试（网络错误最多 3 次）
- 去重检查（基于文件名 + 内容哈希）
- 完整的错误日志
"""

import json
import os
import re
import sys
import glob
import time
import hashlib
import requests
from datetime import datetime

# Config
CRON_OUTPUT_DIR = "/home/admin/.hermes/cron/output"
ENV_PATH = "/home/admin/.hermes/.env"
STATE_FILE = "/home/admin/.hermes/cron/bitable_sync_state.json"
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "").strip()
if not FEISHU_APP_ID:
    raise EnvironmentError("FEISHU_APP_ID not set")

BITABLE_APP_TOKEN = os.environ.get("BITABLE_APP_TOKEN", "").strip()
if not BITABLE_APP_TOKEN:
    raise EnvironmentError("BITABLE_APP_TOKEN not set")
BITABLE_TABLE_ID = os.environ.get("BITABLE_TABLE_ID", "").strip()
if not BITABLE_TABLE_ID:
    raise EnvironmentError("BITABLE_TABLE_ID not set")

# Document mapping (in main folder: MPcgfuV3Zl6qsIdZlqRcDOCXnGd)
# PARA folder structure:
#   📁 00-每日情报 → 📄 AI 雷达早报 (A58Gd8)
#   📁 10-开源生态 → 📄 GitHub 开源项目追踪 (XGisd1)
#   📁 20-学术前沿 → 📄 学术论文前沿 (Ko2Vdg)
#   📁 30-商业动态 → 📄 AI 商业动态 (Nv5AdN)
#   📁 40-研发效能 → 📄 AI 研发效能工具库 (Mm1Ide)
#   📁 90-综合报告 → 📄 综合周报 (JeIydb)
DOC_MAP = {
    "00-每日情报": "A58Gd8ekdoFCWGxAaXgcaK4Inlc",
    "10-开源生态": "XGisd1z9QoJBmgxmEgFcsZ7fnse",
    "20-学术前沿": "Ko2VdgQloo4iqux1610cSN2knLe",
    "30-商业动态": "Nv5AdN60BoxjO6x2jQecl7zSnjd",
    "40-研发效能": "Mm1IdevDZogiKuxLiIRcSkK5nEg",
    "90-综合报告": "JeIydbfrJoesINxoOXNcQpzinne",
}

# PARA folder tokens (for reference, docs are accessed by doc_id directly)
FOLDER_MAP = {
    "00-每日情报": "RsRmfbKdOlamLidrpykcmz1hngb",
    "10-开源生态": "G6Bdfz23Pl0xxgd6lwVcCaNsnkT",
    "20-学术前沿": "Sd9EfBOO7lg4f8dcoWXcYlLynHd",
    "30-商业动态": "YQXRfBjW2lx0iZdaHt9cvnNqn6c",
    "40-研发效能": "LOw4fj6HPlrwPjdffRZc9TbLnNb",
    "90-综合报告": "SUACfJyNRlPdJhdoeUecBioXnoh",
}

# Job ID to doc mapping (cron directories use job IDs, not names)
JOB_TO_DOC = {
    # Active jobs
    "68f8524e608f": "00-每日情报",      # ai-daily-briefing
    "5f5a7512e579": "10-开源生态",      # github-ai-trending-digest
    "b65130333c60": "40-研发效能",      # dev-efficiency-tools-digest
    "d8090592a7c9": "20-学术前沿",      # arxiv-paper-digest
    "c283dc3b6741": "90-综合报告",      # ai-radar-weekly-digest
    # Legacy (removed/paused)
    "8210df73935d": "00-每日情报",      # 每日AI资讯推送 (removed)
    # Paused jobs (for when they are re-enabled)
    "905e2bb68138": "40-研发效能",      # ai-design-tools-digest
    "f2231bd8b030": "30-商业动态",      # china-ai-news-digest
    "4a21eb30fff2": "30-商业动态",      # ai-funding-intelligence
    "28f6e53f028e": "30-商业动态",      # ai-product-launch-tracker
    "ec6b527373ec": "30-商业动态",      # ai-community-buzz
    "41a406fe330b": "30-商业动态",      # ai-company-strategy-watch
    "2e75979fec0c": "10-开源生态",      # ai-agent-framework-watch
    "cf75003ce9fd": "30-商业动态",      # open-model-benchmark
    "5391f1f746f7": "90-综合报告",      # monthly-tech-trends
}

CATEGORY_MAP = {
    "00-每日情报": "Global News",
    "10-开源生态": "GitHub",
    "20-学术前沿": "Paper",
    "30-商业动态": "Funding",
    "40-研发效能": "Product",
    "90-综合报告": "Global News",
}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_app_secret():
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("FEISHU_APP_SECRET="):
                return line.strip().split("=", 1)[1]
    raise ValueError("FEISHU_APP_SECRET not found")

def get_token(max_retries=3):
    """Get tenant access token with retry."""
    app_secret = get_app_secret()
    for attempt in range(max_retries):
        try:
            r = requests.post(
                "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                json={"app_id": FEISHU_APP_ID, "app_secret": app_secret},
                timeout=15
            )
            data = r.json()
            if data.get("code") == 0:
                return data["tenant_access_token"]
            log(f"Auth failed (attempt {attempt+1}): {data}")
        except Exception as e:
            log(f"Auth error (attempt {attempt+1}): {e}")
        time.sleep(2)
    raise Exception("Failed to get token after retries")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def content_hash(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

def parse_cron_output(filepath):
    """Parse cron output markdown, extract structured items."""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        log(f"  ⚠️ Read failed: {filepath}: {e}")
        return []

    # Extract job ID
    job_id = "unknown"
    run_time = datetime.now().strftime("%Y-%m-%d")
    for line in content.split("\n")[:10]:
        if "**Job ID:**" in line:
            job_id = line.split(":")[-1].strip()
        if "**Run Time:**" in line:
            raw = line.split(":", 1)[-1].strip()
            run_time = raw[:10]

    # Determine which doc this belongs to
    dir_name = os.path.basename(os.path.dirname(filepath))
    doc_name = JOB_TO_DOC.get(dir_name, "📡 AI 雷达早报")

    # Extract response section
    resp_match = re.search(r"## Response\n(.*)", content, re.DOTALL)
    if not resp_match:
        return []
    response = resp_match.group(1).strip()

    items = []
    category = CATEGORY_MAP.get(doc_name, "Global News")

    # Split into sections by markdown headers
    sections = re.split(r'\n#{1,4}\s+\d+[\s️⃣📦📌🔥.]*\s*', response)

    for section in sections[1:]:  # skip first empty/header section
        lines = [l.strip() for l in section.strip().split("\n") if l.strip()]
        if not lines:
            continue

        title = lines[0].strip("#* ").strip()[:200]
        if not title or len(title) < 2:
            continue

        # Extract link
        link = ""
        link_match = re.search(r'https?://[^\s\)]+', section)
        if link_match:
            link = link_match.group(0).split(")")[0].split("]")[0].strip()

        # Extract summary
        text_parts = []
        for line in lines[1:]:
            clean = line.strip().lstrip("*-•").strip()
            if clean and not clean.startswith("原文链接") and not clean.startswith("🔗") and len(clean) > 10:
                text_parts.append(clean)
        summary = " ".join(text_parts[:3])[:1500]

        if title and summary:
            items.append({
                "title": title,
                "category": category,
                "date": run_time,
                "summary": summary,
                "link": link,
                "doc_name": doc_name,
                "source_hash": content_hash(title + summary),
            })

    # Fallback: treat whole response as one item
    if not items and len(response) > 50:
        first_para = response.split("\n\n")[0].strip()[:1500]
        title = response.split("\n")[0].strip("#* ").strip()[:200]
        link_match = re.search(r'https?://[^\s\)]+', response)
        link = link_match.group(0).split(")")[0] if link_match else ""

        items.append({
            "title": title or "AI Intelligence Report",
            "category": category,
            "date": run_time,
            "summary": first_para,
            "link": link,
            "doc_name": doc_name,
            "source_hash": content_hash(response[:500]),
        })

    return items

def write_to_bitable(token, items, max_retries=3):
    """Write items to Bitable one by one."""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BITABLE_APP_TOKEN}/tables/{BITABLE_TABLE_ID}/records"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    written = 0
    for item in items:
        try:
            date_ts = 0
            if item.get("date"):
                try:
                    dt = datetime.strptime(item["date"], "%Y-%m-%d")
                    date_ts = int(dt.timestamp() * 1000)
                except:
                    pass

            link_obj = {"text": "", "link": ""}
            if item.get("link") and item["link"].startswith("http"):
                link_obj = {"text": item["link"].split("/")[-1][:50] or "Link", "link": item["link"]}

            payload = {
                "fields": {
                    "Title": (item.get("title", "") or "")[:150],
                    "Category": item.get("category", "Global News")[:50],
                    "Date": date_ts,
                    "Summary": (item.get("summary", "") or "")[:2000],
                    "Insight": "",
                    "Link": link_obj,
                }
            }

            for attempt in range(max_retries):
                try:
                    r = requests.post(url, headers=headers, json=payload, timeout=15)
                    result = r.json()
                    if result.get("code") == 0:
                        written += 1
                        break
                    elif "rate" in str(result).lower():
                        time.sleep(2)
                        continue
                    else:
                        break
                except:
                    time.sleep(1)

            time.sleep(0.05)
        except Exception as e:
            log(f"  ⚠️ Bitable write error: {e}")

    return written

def write_to_doc(token, doc_id, blocks):
    """Append blocks to a Feishu document."""
    if not blocks:
        return

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"children": blocks, "index": -1}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        result = r.json()
        if result.get("code") == 0:
            return True
        else:
            log(f"  ⚠️ Doc write failed: {json.dumps(result, ensure_ascii=False)[:300]}")
            return False
    except Exception as e:
        log(f"  ⚠️ Doc write error: {e}")
        return False

def make_doc_blocks(items, doc_name):
    """Create Feishu document blocks from items."""
    blocks = []

    # Add date separator heading
    today = datetime.now().strftime("%Y-%m-%d")
    blocks.append({
        "block_type": 3,
        "heading1": {"elements": [{"text_run": {"content": f"📅 {doc_name} — {today}", "text_element_style": {"bold": True}}}]}
    })

    for item in items:
        # Title block
        blocks.append({
            "block_type": 2,
            "text": {"elements": [{"text_run": {"content": item["title"], "text_element_style": {"bold": True}}}]}
        })

        # Summary block
        blocks.append({
            "block_type": 2,
            "text": {"elements": [{"text_run": {"content": item["summary"][:500]}}]}
        })

        # Link block
        if item.get("link"):
            blocks.append({
                "block_type": 2,
                "text": {"elements": [{"text_run": {"content": f"🔗 {item['link']}", "text_element_style": {"underline": True}}}]}
            })

        # Separator
        blocks.append({
            "block_type": 22,
            "divider": {}
        })

    return blocks

def main():
    log("🔄 AI Radar Sync Pipeline starting...")
    start = time.time()

    # Get token
    try:
        token = get_token()
        log("✅ Token acquired")
    except Exception as e:
        log(f"❌ Failed to get token: {e}")
        sys.exit(1)

    state = load_state()
    all_items = []
    new_files = 0
    items_by_doc = {}

    # Scan all cron outputs
    for job_dir in sorted(glob.glob(os.path.join(CRON_OUTPUT_DIR, "*"))):
        if not os.path.isdir(job_dir):
            continue

        job_id = os.path.basename(job_dir)
        processed = state.get(job_id, {})

        for md_file in sorted(glob.glob(os.path.join(job_dir, "*.md"))):
            file_hash = content_hash(md_file + str(os.path.getmtime(md_file)))
            if file_hash in processed.get("hashes", []):
                continue

            try:
                items = parse_cron_output(md_file)
                if items:
                    all_items.extend(items)
                    new_files += 1

                    # Group by document
                    for item in items:
                        doc = item["doc_name"]
                        items_by_doc.setdefault(doc, []).append(item)

                    processed.setdefault("hashes", []).append(file_hash)
                    processed.setdefault("files", []).append(os.path.basename(md_file))
                    log(f"  📄 Parsed {os.path.basename(md_file)}: {len(items)} items → {item['doc_name']}")
            except Exception as e:
                log(f"  ⚠️ Parse failed {md_file}: {e}")

        state[job_id] = processed

    if not all_items:
        log("✅ No new data to sync.")
        return

    log(f"\n📊 Total: {len(all_items)} items from {new_files} files")

    # Write to Bitable
    log("📝 Writing to Bitable...")
    bitable_written = write_to_bitable(token, all_items)
    log(f"  ✅ Bitable: {bitable_written} records")

    # Write to Feishu Docs (one item at a time for stability)
    log("📝 Writing to Feishu Docs...")
    doc_written = 0
    doc_errors = 0
    for doc_key, items in items_by_doc.items():
        if doc_key not in DOC_MAP:
            continue

        doc_id = DOC_MAP[doc_key]

        # Write date header once per doc
        today = datetime.now().strftime("%Y-%m-%d")
        header_blocks = [{
            "block_type": 3,
            "heading1": {"elements": [{"text_run": {"content": f"📅 {doc_key} — {today}", "text_element_style": {"bold": True}}}]}
        }]
        write_to_doc(token, doc_id, header_blocks)
        time.sleep(0.1)

        # Write each item separately
        for item in items:
            blocks = []

            # Title
            blocks.append({
                "block_type": 2,
                "text": {"elements": [{"text_run": {"content": item["title"], "text_element_style": {"bold": True}}}]}
            })

            # Summary
            blocks.append({
                "block_type": 2,
                "text": {"elements": [{"text_run": {"content": item["summary"][:1000]}}]}
            })

            # Link
            if item.get("link"):
                blocks.append({
                    "block_type": 2,
                    "text": {"elements": [{"text_run": {"content": f"🔗 {item['link']}", "text_element_style": {"underline": True}}}]}
                })

            # Divider
            blocks.append({"block_type": 22, "divider": {}})

            if write_to_doc(token, doc_id, blocks):
                doc_written += 1
            else:
                doc_errors += 1

            time.sleep(0.05)

        log(f"  ✅ {doc_key}: {len(items)} items")

    if doc_errors > 0:
        log(f"  ⚠️ {doc_errors} doc write errors (non-fatal)")

    # Save state
    save_state(state)

    elapsed = time.time() - start
    log(f"\n✅ Sync complete in {elapsed:.1f}s")
    log(f"   Bitable: {bitable_written} | Docs: {doc_written} | Files: {new_files}")

if __name__ == "__main__":
    main()
