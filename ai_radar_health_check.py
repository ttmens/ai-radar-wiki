#!/usr/bin/env python3
"""
AI Radar 保活监控脚本
- 检查数据采集是否停滞
- 检查关键 cron 任务状态
- 自动恢复失败的组件
- 发送告警到飞书
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WIKI_DIR = "/home/admin/ai-radar-wiki"
GRAPH_JSON = f"{WIKI_DIR}/graph.json"
HEALTH_LOG = f"{WIKI_DIR}/health_log.json"
STAGNATION_THRESHOLD_HOURS = 12  # 超过12小时无更新视为停滞
ZERO_NEW_THRESHOLD = 3  # 连续3次零新增视为异常

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def check_graph_stagnation():
    """检查 graph.json 是否停滞"""
    if not os.path.exists(GRAPH_JSON):
        return {"status": "CRITICAL", "message": "graph.json 不存在！"}
    
    mtime = os.path.getmtime(GRAPH_JSON)
    age_hours = (time.time() - mtime) / 3600
    
    if age_hours > STAGNATION_THRESHOLD_HOURS:
        return {
            "status": "WARNING",
            "message": f"graph.json 已 {age_hours:.1f} 小时未更新 (阈值:{STAGNATION_THRESHOLD_HOURS}h)",
            "age_hours": age_hours
        }
    
    return {"status": "OK", "message": f"graph.json 更新正常 ({age_hours:.1f}h前)"}

def check_node_growth():
    """检查节点增长情况"""
    data = load_json(GRAPH_JSON)
    if not data:
        return {"status": "CRITICAL", "message": "无法读取 graph.json"}
    
    nodes = data.get("nodes", [])
    total = len(nodes)
    
    # 检查最近日期的节点数
    dates = [n.get("date", "") for n in nodes if n.get("date")]
    if not dates:
        return {"status": "WARNING", "message": "没有日期信息的节点"}
    
    from collections import Counter
    date_counts = Counter(dates)
    latest_date = max(dates)
    latest_count = date_counts[latest_date]
    
    # 检查健康日志中的连续零新增记录
    health = load_json(HEALTH_LOG) or {"zero_new_streak": 0, "last_check": None}
    
    # 如果最新日期的节点数很少（<5），且不是今天
    today = datetime.now().strftime("%Y-%m-%d")
    if latest_date < today and latest_count < 5:
        health["zero_new_streak"] = health.get("zero_new_streak", 0) + 1
    else:
        health["zero_new_streak"] = 0
    
    health["last_check"] = datetime.now().isoformat()
    health["total_nodes"] = total
    health["latest_date"] = latest_date
    health["latest_count"] = latest_count
    save_json(HEALTH_LOG, health)
    
    if health["zero_new_streak"] >= ZERO_NEW_THRESHOLD:
        return {
            "status": "WARNING",
            "message": f"连续 {health['zero_new_streak']} 次检查无显著新增 (最新:{latest_date} {latest_count}个)"
        }
    
    return {
        "status": "OK",
        "message": f"节点总数:{total}, 最新数据:{latest_date} ({latest_count}个)"
    }

def check_cron_jobs():
    """检查关键 cron 任务状态"""
    critical_jobs = {
        "ai-radar-explorer": "数据采集核心",
        "ai-radar-data-sync": "飞书同步",
        "ai-daily-briefing": "每日早报"
    }
    
    # 直接从 jobs.json 读取状态（Hermes cron 子系统存储格式）
    try:
        jobs_file = "/home/admin/.hermes/cron/jobs.json"
        if not os.path.exists(jobs_file):
            return {"status": "WARNING", "message": "jobs.json 不存在，cron 子系统未初始化"}
        
        with open(jobs_file) as f:
            data = json.load(f)
        
        jobs = data.get("jobs", [])
        issues = []
        ok_count = 0
        
        for j in jobs:
            name = j.get("name", "")
            if name in critical_jobs:
                enabled = j.get("enabled", False)
                last_status = j.get("last_status", "")
                last_run = j.get("last_run_at", "")
                
                if not enabled:
                    issues.append(f"❌ {name}: 已暂停")
                elif last_status == "error":
                    issues.append(f"❌ {name}: 最近运行失败 (last_run: {last_run})")
                elif not last_run:
                    issues.append(f"⚠️ {name}: 从未运行过")
                else:
                    ok_count += 1
        
        if issues:
            return {"status": "WARNING", "message": "; ".join(issues)}
        if ok_count > 0:
            return {"status": "OK", "message": f"所有关键任务正常运行 ({ok_count}/{len(critical_jobs)})"}
        return {"status": "OK", "message": "所有关键任务正常运行"}
        
    except Exception as e:
        return {"status": "ERROR", "message": f"检查 cron 任务失败：{str(e)}"}

def check_data_sources():
    """检查各数据源健康度"""
    data = load_json(GRAPH_JSON)
    if not data:
        return {"status": "CRITICAL", "message": "无法读取 graph.json"}
    
    nodes = data.get("nodes", [])
    sources = {}
    for n in nodes:
        src = n.get("source_type", "unknown")
        sources[src] = sources.get(src, 0) + 1
    
    # 检查主要数据源
    issues = []
    if sources.get("github", 0) == 0:
        issues.append("GitHub 源无数据")
    if sources.get("papers", 0) == 0:
        issues.append("arXiv 论文源无数据")
    
    total = sum(sources.values())
    if total < 100:
        issues.append(f"总节点数过低 ({total})")
    
    if issues:
        return {"status": "WARNING", "message": "; ".join(issues)}
    
    return {
        "status": "OK",
        "message": f"数据源正常: {', '.join(f'{k}:{v}' for k,v in sorted(sources.items(), key=lambda x:-x[1]))}"
    }

def auto_recover():
    """自动恢复尝试"""
    recovery_actions = []
    
    # 1. 检查 concepts 目录
    concepts_dir = f"{WIKI_DIR}/wiki/concepts"
    if not os.path.exists(concepts_dir):
        os.makedirs(concepts_dir, exist_ok=True)
        recovery_actions.append("✅ 创建 wiki/concepts 目录")
    
    # 2. 检查 vis-network.min.js
    vis_js = f"{WIKI_DIR}/assets/vis-network.min.js"
    if not os.path.exists(vis_js):
        recovery_actions.append("❌ vis-network.min.js 缺失，需要手动恢复")
    
    # 3. 尝试运行一次 explorer
    graph_mtime = os.path.getmtime(GRAPH_JSON) if os.path.exists(GRAPH_JSON) else 0
    age_hours = (time.time() - graph_mtime) / 3600
    
    if age_hours > STAGNATION_THRESHOLD_HOURS:
        recovery_actions.append("⚠️ 数据停滞超过阈值，建议手动触发 explorer")
        # 可以尝试运行
        try:
            subprocess.run(
                ["python3", "/home/admin/.hermes/scripts/ai_radar_explorer.py"],
                cwd=WIKI_DIR, timeout=600, capture_output=True
            )
            recovery_actions.append("✅ 已触发 explorer 运行")
        except Exception as e:
            recovery_actions.append(f"❌ explorer 运行失败：{str(e)}")
    
    return recovery_actions

def send_feishu_alert(title, content):
    """发送飞书告警（如果配置了 webhook）"""
    # 这里可以集成飞书 webhook
    # 暂时只打印
    print(f"[FEISHU ALERT] {title}: {content}")

def main():
    print(f"🔍 AI Radar 保活检查 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    checks = []
    
    # 执行检查
    checks.append(("图谱停滞", check_graph_stagnation()))
    checks.append(("节点增长", check_node_growth()))
    checks.append(("Cron任务", check_cron_jobs()))
    checks.append(("数据源", check_data_sources()))
    
    # 输出结果
    has_warning = False
    for name, result in checks:
        status = result["status"]
        msg = result["message"]
        icon = {"OK": "✅", "WARNING": "⚠️", "CRITICAL": "❌", "ERROR": "❌"}.get(status, "❓")
        print(f"{icon} {name}: {msg}")
        if status in ("WARNING", "CRITICAL", "ERROR"):
            has_warning = True
    
    # 自动恢复
    print("\n🔧 自动恢复:")
    recoveries = auto_recover()
    for action in recoveries:
        print(f"  {action}")
    
    # 发送告警
    if has_warning:
        alert_title = "AI Radar 数据异常告警"
        alert_content = "\n".join(f"{c[0]}: {c[1]['message']}" for c in checks if c[1]["status"] != "OK")
        send_feishu_alert(alert_title, alert_content)
    
    print("\n" + "=" * 60)
    print("检查完成")

if __name__ == "__main__":
    main()
