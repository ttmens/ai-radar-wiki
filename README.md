# 🧠 AI Radar Wiki

> AI 产品设计雷达 · 自动构建的知识库

## 数据源
| 来源 | 说明 | 频率 |
|------|------|------|
| GitHub | AI 高星项目（stars > 100, 30天内创建） | 每4小时 |
| arXiv | 最新 cs.AI/cs.LG 论文 | 每4小时 |
| Hacker News | AI 热门讨论（score > 30） | 每4小时 |
| Product Hunt | 新 AI 产品 | 每4小时 |

## 知识库结构
```
ai-radar-wiki/
├── entities/        # 项目、公司、人物
├── concepts/        # 技术概念、论文
├── comparisons/     # 横向对比
├── timelines/       # 时间线
├── raw/             # 原始数据（不可变）
├── graph.json       # 知识图谱数据
├── graph.html       # 交互式可视化（浏览器打开）
├── index.md         # 总索引
└── SCHEMA.md        # 标签体系 + 结构规则
```

## 使用方式

### 1. 在线浏览
- [知识图谱可视化](https://ttmens.github.io/ai-radar-wiki/graph.html) — 交互式图谱
- [总索引](index.md) — 所有页面导航

### 2. 本地使用（Obsidian）
```bash
git clone https://github.com/ttmens/ai-radar-wiki.git
# 用 Obsidian 打开 ai-radar-wiki 目录
# Graph View 自动可视化知识图谱
```

### 3. Clone 使用
```bash
git clone https://github.com/ttmens/ai-radar-wiki.git
```

## 图谱统计
| 指标 | 数值 |
|------|------|
| 节点数 | 0 |
| 边数 | 0 |
| 最后更新 | 2026-05-07 09:37 |

## 自动化
- 数据采集：Python 爬虫（每4小时）
- Wiki 构建：自动提取实体/概念
- 图谱生成：规则提取 + LLM 推断（Stage 2）
- GitHub 推送：自动 commit + push

---
*由 AI Radar Explorer 自动生成 | 最后更新: 2026-05-07 09:37*
