# 🧠 AI Radar Wiki — AI 产品设计雷达

> 面向 AI 产品经理的自动知识库 · 4 大支柱体系

## 4 大知识支柱

| Pillar | 关注点 | 示例 |
|--------|--------|------|
| 🤖 **Capabilities** | Context, Latency, Cost, Multimodal | vLLM, GGUF, RLHF |
| 📱 **Patterns** | Chat, Copilot, Agent Workflow | AutoGen, CrewAI |
| 🔧 **Ecosystem** | Orchestration, VectorDB, Eval | LangGraph, Chroma |
| 💰 **Business** | Funding, Moat, Growth, Ethics | 商业化分析、竞品对比 |

## 数据源
| 来源 | 说明 | 频率 |
|------|------|------|
| GitHub | AI 高星项目（stars > 100） | 每4小时 |
| arXiv | 最新 cs.AI/cs.LG 论文 | 每4小时 |
| Hacker News | AI 热门讨论（score > 30） | 每4小时 |
| Product Hunt | 新 AI 产品 | 每4小时 |

## 知识库结构
```
ai-radar-wiki/
├── entities/        # 项目、公司、讨论、产品
├── concepts/        # 技术概念、论文
├── comparisons/     # 横向对比
├── timelines/       # 时间线
├── raw/             # 原始数据
├── graph.json       # 知识图谱数据
├── graph.html       # 交互式可视化
├── index.md         # 按支柱分类的索引
├── SCHEMA.md        # 标签体系
├── feedback.json    # 用户互动反馈
└── evolution.md     # 自进化日志
```

## 使用方式

### 1. 在线图谱
- [知识图谱可视化](https://ttmens.github.io/ai-radar-wiki/graph.html) — 点击节点查看详情

### 2. 本地 Obsidian
```bash
git clone https://github.com/ttmens/ai-radar-wiki.git
# Obsidian 打开 → Graph View 可视化
```

## 图谱统计
| 指标 | 数值 |
|------|------|
| 节点数 | 22 |
| 边数 | 39 |
| Schema | 4-pillar-pm-focused |
| 最后更新 | 2026-05-07 12:24 |

## 自进化机制
- **pm_score**: 基于信号强度 + 时效性 + 用户反馈的动态权重
- **内容淘汰**: 90天无更新 + 低分自动降权
- **趋势检测**: 新标签涌现自动上报

---
*AI Radar Explorer v3 | 4-Pillar PM System | Last: 2026-05-07 12:24*
