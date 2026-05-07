# 🧠 AI Radar — AI 产品设计雷达

> 自动化 AI 技术情报系统，面向 AI 产品经理的 4 支柱知识图谱

[![Graph](https://img.shields.io/badge/📊_Knowledge_Graph-Live-blue)](https://ttmens.github.io/ai-radar-wiki/graph.html)
[![Update](https://img.shields.io/badge/🔄_Every_6h-green)]()
[![RSS](https://img.shields.io/badge/📡_RSS_Feed-orange)](https://ttmens.github.io/ai-radar-wiki/feed.xml)
[![Chinese](https://img.shields.io/badge/🇨🇳_178_中文摘要-red)]()

---

## 📊 实时统计

| 指标 | 数值 |
|------|------|
| 总节点 | 257 |
| 总边 | 263 |
| 中文摘要 | 178 (69%) |
| 最后更新 | %Y->- (HEAD -> main, origin/main, origin/HEAD) 52c5905e361318f5d6f2368f0cc0b09f8f1c48cc:%M |

### 四支柱分布

| 支柱 | 节点数 | 说明 |
|------|--------|------|
| 🤖 技术能力 | 79 | 新模型、算法、技术突破 |
| 📱 产品模式 | 86 | 交互方式、工作流、AI 应用 |
| 🔧 工具生态 | 59 | 框架、SDK、库、平台 |
| 💰 商业动态 | 31 | 融资、产品发布、市场 |

### 数据来源

| 来源 | 节点数 | 说明 |
|------|--------|------|
| GitHub | 200 | 高星 AI 开源项目 |
| TechCrunch | 17 | AI 商业新闻 |
| arXiv | 24 | 学术论文 |
| Hacker News | 11 | 社区讨论 |

---

## 🚀 快速访问

| 资源 | 链接 |
|------|------|
| 📊 交互式知识图谱 | [Open Graph](https://ttmens.github.io/ai-radar-wiki/graph.html) |
| 📋 图谱数据 | [graph.json](https://ttmens.github.io/ai-radar-wiki/graph.json) |
| 📚 Wiki 索引 | [index.md](https://ttmens.github.io/ai-radar-wiki/index.md) |
| 📡 RSS 订阅 | [feed.xml](https://ttmens.github.io/ai-radar-wiki/feed.xml) |
| 📅 今日日报 | [daily_summary.json](https://ttmens.github.io/ai-radar-wiki/daily_summary.json) |
| 📖 设计文档 | [DESIGN.md](https://ttmens.github.io/ai-radar-wiki/DESIGN.md) |

---

## 🔄 系统架构

```
数据采集 → LLM 分析 → 图谱生成 → 前端展示
   ↓           ↓           ↓          ↓
 GitHub     中文摘要     graph.json   知识图谱
 ArXiv      四象限       Wiki        RSS Feed
 HN/TC      PM Score     日报        飞书推送
```

- **采集**: GitHub API, ArXiv, Hacker News, TechCrunch, Product Hunt
- **分析**: DashScope qwen3.6-plus (中文摘要翻译、四象限分类、PM Score)
- **展示**: 交互式知识图谱 (vis-network.js) + Wiki + RSS
- **推送**: 飞书早报 (每日 08:00) + 周报 (每周一 10:00)

---

## 🤖 AI Agent 可访问

本仓库为 AI Agent 设计，支持：

- 📊 通过 `graph.json` 获取结构化知识
- 📚 通过 `wiki/` 获取详细 Wiki 页面
- 📡 通过 `feed.xml` 获取 RSS 订阅
- 🤖 通过 `ai-agent.json` 获取 Agent API（即将上线）

---

*AI Radar Explorer v3 · Self-evolving Knowledge Graph · Last updated: %Y->- (HEAD -> main, origin/main, origin/HEAD) 52c5905e361318f5d6f2368f0cc0b09f8f1c48cc:%M*
