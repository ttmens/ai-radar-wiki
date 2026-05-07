# 🧠 AI Radar Wiki — AI 产品设计雷达

> **Automated AI Knowledge Base for Product Managers** — 自动构建 · 4 大支柱体系 · 自进化图谱

[![Knowledge Graph](https://img.shields.io/badge/📊_Graph-Live-blue)](https://ttmens.github.io/ai-radar-wiki/graph.html)
[![Auto Updated](https://img.shields.io/badge/🔄_Update-Every_4h-green)]()
[![Pillars](https://img.shields.io/badge/🏗️_Pillars-4-orange)](https://ttmens.github.io/ai-radar-wiki/index.md)
[![License](https://img.shields.io/badge/📄_License-MIT-lightgrey)]()
[![AI Agent Ready](https://img.shields.io/badge/🤖_Agent-Ready-9cf)](https://ttmens.github.io/ai-radar-wiki/ai-agent.json)

## 🎯 What is this?

一个面向 AI 产品经理的**自动知识雷达系统**，每 4 小时从 GitHub、arXiv、Hacker News、Product Hunt 采集数据，自动分类到 4 大知识支柱，构建交互式知识图谱。

An **automated AI knowledge radar** that collects data every 4 hours, classifies into 4 pillars, and builds an interactive knowledge graph.

## 🏗️ 4-Pillar Knowledge System

| Pillar | 关注点 | 示例 |
|--------|--------|------|
| 🤖 **Capabilities** | Context, Latency, Cost, Multimodal | vLLM, GGUF, RLHF |
| 📱 **Patterns** | Chat, Copilot, Agent Workflow | AutoGen, CrewAI |
| 🔧 **Ecosystem** | Orchestration, VectorDB, Eval | LangGraph, Chroma |
| 💰 **Business** | Funding, Moat, Growth, Ethics | 商业化分析、竞品对比 |

## 📡 Quick Access

| What | Link | Format |
|------|------|--------|
| 📊 **Interactive Graph** | [Open →](https://ttmens.github.io/ai-radar-wiki/graph.html) | HTML/JS |
| 📋 **Knowledge Graph Data** | [graph.json →](https://ttmens.github.io/ai-radar-wiki/graph.json) | JSON |
| 📚 **Wiki Index** | [index.md →](https://ttmens.github.io/ai-radar-wiki/index.md) | Markdown |
| 🤖 **Agent Discovery** | [ai-agent.json →](https://ttmens.github.io/ai-radar-wiki/ai-agent.json) | JSON |
| 📐 **Schema** | [SCHEMA.md →](https://ttmens.github.io/ai-radar-wiki/SCHEMA.md) | Markdown |

## 🤖 For AI Agents

This repo is **agent-discoverable** and **machine-readable**:

```bash
# Clone the full knowledge base
git clone https://github.com/ttmens/ai-radar-wiki.git

# Or fetch just the graph data
curl https://ttmens.github.io/ai-radar-wiki/graph.json

# Agent discovery endpoint
curl https://ttmens.github.io/ai-radar-wiki/.well-known/ai-agent.json

# Read individual pages (YAML frontmatter + markdown)
cat ai-radar-wiki/entities/*.md
```

**Schema:** Every page has structured YAML frontmatter:
```yaml
title: "Project Name"
type: entity | concept
pillar: capabilities | patterns | ecosystem | business
pm_score: 0.0-1.0  # Dynamic importance score
tags: ["array", "of", "tags"]
```

## 📁 Repository Structure

```
ai-radar-wiki/
├── entities/              # 项目、公司、讨论、产品
├── concepts/              # 技术概念、论文
├── comparisons/           # 横向对比
├── timelines/             # 时间线
├── raw/                   # 原始数据（不可变）
├── graph.json             # 知识图谱数据
├── graph.html             # 交互式可视化（GitHub Pages）
├── index.md               # 按支柱分类的索引
├── SCHEMA.md              # 标签体系 + 结构规则
├── ai-agent.json          # 🤖 Agent 发现端点
├── .well-known/ai-agent.json  # 🤖 标准发现端点
├── robots.txt             # 🕷️ 搜索引擎爬取规则
└── sitemap.xml            # 🗺️ 站点地图
```

## 🔄 How It Works

```
Data Sources (GitHub, arXiv, HN, PH)
         ↓
  Python Scraper (every 4h)
         ↓
  AI Classification → 4 Pillars + pm_score
         ↓
  Wiki Pages (Markdown) + Knowledge Graph (JSON)
         ↓
  Auto Git Push → GitHub Pages (Live)
```

### Self-Evolution
- **pm_score**: 基于信号强度 + 时效性 + 反馈的动态权重
- **Content Pruning**: 90 天无更新 + 低分自动降权
- **Trend Detection**: 新标签涌现自动上报

## 📊 Live Stats

| 指标 | 数值 |
|------|------|
| Nodes | 34+ (auto-growing) |
| Edges | 51+ (auto-growing) |
| Update Cycle | Every 4 hours |
| Schema | 4-Pillar PM System v3 |

## 🚀 Use Cases

- **AI PM**: 追踪技术趋势、产品模式、商业动态
- **Researchers**: 发现相关论文和研究方向
- **Developers**: 了解高星 AI 项目和工具生态
- **AI Agents**: 结构化知识图谱，可编程访问
- **Investors**: 监控 AI 领域创新信号

## 📬 Connect

- 🐛 Issues: [Report a bug](https://github.com/ttmens/ai-radar-wiki/issues)
- 💡 Ideas: [Request a feature](https://github.com/ttmens/ai-radar-wiki/issues)
- 📖 Docs: [SCHEMA.md](https://github.com/ttmens/ai-radar-wiki/blob/main/SCHEMA.md)

---

*Built by AI Radar Explorer v3 · Self-evolving knowledge base · Last update: 2026-05-07*
