#!/usr/bin/env python3
"""
AI Radar 每日公众号深度文章生成器
- 围绕每日简报的"核心观点"生成一篇完整的公众号文章
- 结合当天的AI新闻和证据
- 自动推送到 Git 仓库的 daily-articles/ 文件夹
- 文件命名：YYYY-MM-DD-核心观点.md

用法：python3 daily_article.py [--date YYYY-MM-DD]
"""

import json
import os
import re
import sys
import subprocess
import argparse
from datetime import datetime, timezone, timedelta

BJ_TZ = timezone(timedelta(hours=8))

WIKI_DIR = os.path.expanduser("~/ai-radar-wiki")
ARTICLES_DIR = os.path.join(WIKI_DIR, "daily-articles")
DAILY_SUMMARY = os.path.join(WIKI_DIR, "daily_summary.json")
GRAPH_JSON = os.path.join(WIKI_DIR, "graph.json")

# 添加脚本目录到路径
sys.path.insert(0, os.path.expanduser("~/.hermes/scripts"))
try:
    from ai_model_router import call_llm as router_call_llm
    HAS_MODEL_ROUTER = True
except ImportError:
    HAS_MODEL_ROUTER = False

def log(msg):
    ts = datetime.now(BJ_TZ).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def load_data():
    """加载每日摘要和图谱数据。"""
    with open(DAILY_SUMMARY) as f:
        data = json.load(f).get("daily_summary", {})
    
    # 加载今日情报详情
    items = []
    if os.path.exists(GRAPH_JSON):
        with open(GRAPH_JSON) as f:
            graph = json.load(f)
        today = datetime.now(BJ_TZ).strftime("%Y-%m-%d")
        for node in graph.get("nodes", []):
            if node.get("date", "").startswith(today) and node.get("type") != "concept":
                items.append(node)
    
    return data, sorted(items, key=lambda x: x.get("pm_score", 0), reverse=True)

def sanitize_filename(name):
    """清理文件名，移除非法字符。"""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r'\s+', '-', name)
    name = name.strip('-')
    return name[:60]  # 限制长度

def build_article_prompt(summary, items):
    """构建公众号文章生成 prompt。"""
    date = summary.get("date", datetime.now(BJ_TZ).strftime("%Y-%m-%d"))
    overview = summary.get("overview", "")
    narratives = summary.get("narratives", [])
    insights = summary.get("insights", [])
    
    # 构建新闻列表
    news_items = ""
    for i, item in enumerate(items[:15], 1):
        pillar = item.get("pillar", "")
        score = item.get("pm_score", 0)
        title = item.get("label", "")[:70]
        summary_text = (item.get("summary", "") or "")[:150]
        news_items += f"{i}. [{pillar}] {title} (PM {score:.2f})\n   {summary_text}\n\n"
    
    # 构建叙事信息
    narrative_info = ""
    for n in narratives:
        narrative_info += f"- **{n.get('title', '')}** ({n.get('type', '')})\n  {n.get('body', '')}\n\n"
    
    return f"""你是AI领域的资深产品分析师和公众号主笔，面向AI产品经理和创业者读者。

## 任务
围绕今日AI情报的**核心观点**，撰写一篇有深度、有洞察的公众号文章。

## 今日核心观点
{overview}

## 关键叙事
{narrative_info}

## 今日AI新闻素材
{news_items}

## 文章要求

**标题**：
- 吸引眼球，有悬念或冲突感
- 20-30字，适合公众号推送
- 不要使用"日报""简报"等字样

**结构**：
1. **开篇引子**（200字）：用一个具体的新闻事件或现象切入，引出核心观点，制造阅读悬念
2. **深度分析**（400-600字）：围绕核心观点展开分析，结合多条新闻素材，指出背后的趋势和逻辑
3. **关键案例**（300-400字）：选取2-3个最有代表性的项目/事件详细解读，说明对产品/行业的影响
4. **PM启示**（200-300字）：给AI产品经理的具体建议，可操作的洞察
5. **结尾展望**（100-150字）：前瞻性判断，留下思考空间

**写作风格**：
- 像36氪/晚点LatePost的科技分析文章，不是新闻汇总
- 有观点、有态度，不要中立客观的流水账
- 用具体数据和案例支撑观点
- 语言精炼，段落短小（每段不超过5行）
- 适当使用emoji增加可读性（但不要过多）
- 重要观点/数据可以用**加粗**突出

**字数**：1200-1800字

**输出格式**：
先输出标题（以 # 开头），然后是正文。不要输出其他内容。"""

def generate_article(prompt):
    """调用 LLM 生成文章。"""
    if HAS_MODEL_ROUTER:
        return router_call_llm(
            prompt=prompt,
            system_prompt="你是资深科技公众号主笔，擅长写出有深度、有传播力的AI行业分析文章。",
            scene="analysis",
        )
    else:
        log("⚠️ ai_model_router 不可用，尝试直接调用")
        # 备用方案
        import httpx
        ds_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if ds_key:
            url = f"{os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')}/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ds_key}",
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是资深科技公众号主笔。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 3000,
            }
            resp = httpx.post(url, json=payload, headers=headers, timeout=120)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        raise RuntimeError("无可用LLM")

def save_and_push(date, overview, article_content):
    """保存文章并推送到 Git。"""
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    
    # 文件名：日期-核心观点
    topic = sanitize_filename(overview)
    filename = f"{date}-{topic}.md"
    filepath = os.path.join(ARTICLES_DIR, filename)
    
    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(article_content)
    
    log(f"📝 文章已保存: {filename}")
    
    # Git 提交
    os.chdir(WIKI_DIR)
    try:
        subprocess.run(["git", "add", filepath], capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"daily-article: {date} {overview}"],
            capture_output=True, check=True
        )
        subprocess.run(["git", "push"], capture_output=True, check=True)
        log(f"✅ 已推送到 Git 仓库")
    except subprocess.CalledProcessError as e:
        log(f"⚠️ Git 推送失败: {e.stderr.decode('utf-8', errors='ignore')[:200]}")

def main():
    parser = argparse.ArgumentParser(description="生成每日公众号深度文章")
    parser.add_argument("--date", type=str, default=None, help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="只生成不保存")
    args = parser.parse_args()
    
    date = args.date or datetime.now(BJ_TZ).strftime("%Y-%m-%d")
    log(f"📅 生成 {date} 公众号文章...")
    
    # 加载数据
    summary, items = load_data()
    log(f"📊 加载 {len(items)} 条今日情报")
    
    if not items:
        log("❌ 今日无情报数据")
        sys.exit(1)
    
    # 构建 prompt
    prompt = build_article_prompt(summary, items)
    log("🤖 调用 LLM 生成文章...")
    
    # 生成文章
    try:
        article = generate_article(prompt)
        log(f"✅ 文章生成完成 ({len(article)} 字)")
    except Exception as e:
        log(f"❌ 文章生成失败: {e}")
        sys.exit(1)
    
    if args.dry_run:
        log("--- 预览 ---")
        print(article)
        return
    
    # 保存并推送
    overview = summary.get("overview", "AI日报")
    save_and_push(date, overview, article)
    log(f"🎉 完成！文章路径: {ARTICLES_DIR}")

if __name__ == "__main__":
    main()
