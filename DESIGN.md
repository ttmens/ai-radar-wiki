# AI Radar 系统设计文档 (System Design Document)

> **版本**: v3.0.0  
> **最后更新**: 2026-05-07  
> **维护者**: Hermes Agent  
> **在线地址**: https://ttmens.github.io/ai-radar-wiki/graph.html

---

## 1. 系统概述

AI 产品设计雷达是一个自动化 AI 技术情报系统，通过**采集 → 分析 → 可视化 → 推送**的完整链路，持续追踪 AI 领域的开源项目、学术论文、商业动态和研发效能工具，帮助 AI 产品经理和开发者快速获取高价值情报。

### 核心价值主张
- 🎯 **AI PM 视角**：按“技术/模式/生态/商业”四大维度评估项目
- ⏱️ **自动化**：每日自动采集、分析、生成报告，无需人工干预
- 🔗 **可交互**：知识图谱支持点击、搜索、筛选，一目了然

---

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    数据采集层 (Scraper)                   │
│  GitHub Trending  │  ArXiv API  │  Tech Blogs  │  RSS   │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   智能分析层 (LLM Agent)                  │
│  标题/摘要翻译  │  4-Pillar 分类  │  PM Score 计算  │  关键词提取  │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    数据生成层 (Explorer)                  │
│  graph.json (节点/边)  │  wiki/  (Markdown 知识库)        │
│  daily-digest/ (日报)  │  ai-readable.jsonl (原始数据)     │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    前端展示层 (Frontend)                  │
│  graph.html (交互式图谱)  │  Template-Data 分离架构        │
│  左侧仪表盘 │ 右侧详情面板 │ 图例 │ 搜索框                  │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    分发推送层 (Delivery)                  │
│  GitHub Pages (公开)  │  Feishu Bot (群聊/个人)           │
│  Cron 定时推送        │  RSS/Atom Feed                   │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 数据流水线 (Data Pipeline)

### 3.1 两阶段架构
| 阶段 | 职责 | 执行频率 | 工具 |
|------|------|----------|------|
| **Stage 1: 数据采集** | 从 GitHub/ArXiv/Blogs 抓取原始数据 | 每 4 小时 | `explorer.py` (Python) |
| **Stage 2: 智能分析** | LLM 翻译、分类、评分、摘要生成 | 每 6 小时 | Claude/GPT API |

### 3.2 数据 Schema
```json
{
  "id": "unique_node_id",
  "label": "项目/论文名称",
  "group": "capabilities|patterns|ecosystem|business",
  "pillar": "capabilities|patterns|ecosystem|business",
  "summary": "中文摘要（必填，200-500 字）",
  "date": "YYYY-MM-DD",
  "pm_score": 0.0-10.0,
  "source_url": "https://...",
  "keywords": ["LLM", "Agent", "RAG"],
  "type": "github|paper|blog|product"
}
```

### 3.3 四象限分类体系 (4-Pillar Framework)
| Pillar | 中文 | 颜色 | 覆盖范围 |
|--------|------|------|----------|
| `capabilities` | 🤖 技术能力 | `#FF6B6B` (红) | 新模型、算法、工具、技术突破 |
| `patterns` | 📱 模式/范式 | `#4ECDC4` (青) | 新交互方式、工作流、AI 应用模式 |
| `ecosystem` | 🔧 开发生态 | `#45B7D1` (蓝) | 框架、SDK、库、平台、开源社区 |
| `business` | 💰 商业动态 | `#F9CA24` (黄) | 融资、产品发布、公司战略、市场 |

### 3.4 PM Score 计算逻辑
```python
pm_score = (
    novelty_weight * (0-10) +      # 新颖度：技术突破/模式创新
    impact_weight * (0-10) +       # 影响力：Star 数/引用数/讨论热度
    relevance_weight * (0-10) +    # 相关性：对 AI PM 的参考价值
    timeliness_weight * (0-10)     # 时效性：发布时间衰减
) / 4.0
```

---

## 4. 前端设计规范 (Frontend Design)

### 4.1 核心架构原则
> **模板与数据分离 (Template-Data Separation)**

- `graph_template.html`: 纯静态前端模板（HTML/CSS/JS），不含任何业务数据
- `graph.json`: 独立数据文件，包含所有节点/边信息
- Python 脚本仅负责将 JSON 数据注入到模板的 `{{DATA}}` 占位符

### 4.2 页面布局
```
┌─────────────────────────────────────────────────────┐
│ [🔍 搜索框]          [📅 日报开关]  [🌐 语言切换]       │
├────────────┬────────────────────────────┬───────────┤
│            │                            │           │
│  📊 仪表盘 │                            │  📋 详情   │
│  (左侧面板) │                            │  (右侧面板) │
│            │     交互式知识图谱           │           │
│  • 今日 Top │     (vis-network.js)       │  点击节点 │
│  • 高价值   │     - 力导向图              │  显示详情 │
│  • 新发现   │     - 可拖拽/缩放           │           │
│            │     - 节点高亮              │           │
│            │                            │           │
├────────────┴────────────────────────────┴───────────┤
│  🟥 技术能力  🟩 模式范式  🟦 开发生态  🟨 商业动态   │
│                     (左下角图例)                      │
└─────────────────────────────────────────────────────┘
```

### 4.3 核心 UI 组件

#### 左侧仪表盘 (Dashboard)
- **默认状态**: 展开
- **内容**: 今日 Top 10 高价值情报（按 PM Score 排序）
- **每条情报显示**:
  - 标题 (中文)
  - 分类标签 (颜色对应 pillar)
  - PM Score (0-10)
  - 摘要预览 (前 100 字)
- **交互**: 点击条目 → 图谱聚焦到该节点 + 右侧面板弹出详情
- **折叠**: 点击 Header 按钮切换显示/隐藏

#### 右侧详情面板 (Detail Panel)
- **触发**: 点击图谱节点
- **内容**:
  - 标题 (中文)
  - 分类标签 + 颜色标识
  - 日期 (YYYY-MM-DD)
  - PM Score (0-10)
  - 完整中文摘要 (200-500 字)
  - 🔗 查看原文按钮 (跳转 source_url)
- **回退机制**: 若无摘要，显示对应类型的中文提示文案
- **关闭**: 点击空白区域或 X 按钮

#### 图例 (Legend)
- **位置**: 左下角固定
- **内容**: 四大分类的颜色标识 + 中文说明
- **样式**: 半透明背景，不遮挡图谱

#### 搜索框
- **功能**: 按标题/关键词/日期过滤节点
- **交互**: 实时过滤，匹配节点高亮，不匹配节点变暗

### 4.4 节点样式规范
| 属性 | 规则 |
|------|------|
| **形状** | 统一圆形 (`shape: 'dot'`) |
| **大小** | 根据 PM Score 映射: `r = 10 + pm_score * 3` |
| **颜色** | 按 `group` 映射到四象限颜色 |
| **字体** | 白色/浅灰，字号 12-14px |
| **边** | 灰色半透明，不显示标签 |

### 4.5 技术约束
- **零外部依赖**: 所有库必须本地化 (如 `vis-network.min.js`)
- **单文件部署**: `graph.html` 自包含，适合 GitHub Pages
- **响应式**: 适配桌面端，移动端基础可用
- **暗色主题**: 背景 `#1a1a2e`，节点发光效果

---

## 5. 定时任务系统 (Cron Jobs)

### 5.1 任务矩阵
| 任务名称 | 频率 | 职责 | 交付目标 |
|----------|------|------|----------|
| `ai-radar-explorer` | 每 4h | 数据采集 + 分析 + 生成 graph.json/wiki | 本地文件 + Git Push |
| `ai-radar-data-sync` | 每日 06:00 | 同步数据到飞书 Bitable | Feishu Bitable |
| `ai-daily-briefing` | 每日 08:00 | 生成并推送早报 | Feishu 群聊 |
| `ai-radar-weekly-digest` | 每周一 10:00 | 生成周报 | Feishu + 本地文件 |
| `github-ai-trending-digest` | 每周一 09:00 | GitHub 趋势分析 | 本地文件 |
| `ai-radar-rss-feed` | 每 4h | 生成 RSS Feed | feed.xml + Git Push |

---

## 5.5 订阅系统 (Subscription)

### 5.5.1 RSS 订阅
- **Feed 地址**: `https://ttmens.github.io/ai-radar-wiki/feed.xml`
- **格式**: RSS 2.0 标准格式
- **内容**: Top 50 最新情报，包含标题、摘要、分类、PM Score、原文链接
- **更新频率**: 每 4 小时自动生成
- **兼容**: Feedly, Inoreader, Reeder, Tiny Tiny RSS 等所有标准 RSS 阅读器

### 5.5.2 邮件订阅
- **订阅页面**: `https://ttmens.github.io/ai-radar-wiki/subscribe.html`
- **表单后端**: Formspree (需配置 FORM_ID)
- **推送频率**: 可选每日 (08:00) 或每周 (周一)
- **待集成**: 配置 Formspree 或 Resend API Key 后激活

### 5.5.3 RSS 生成脚本
- **路径**: `~/.hermes/scripts/generate_rss.py`
- **输入**: `~/ai-radar-wiki/graph.json`
- **输出**: `~/ai-radar-wiki/feed.xml`
- **Cron**: `ai-radar-rss-feed` (每 4h)

### 5.2 飞书集成
- **文档结构**:
  ```
  📁 AI 产品设计雷达
  ├── 📁 00-每日情报 → 📄 AI 雷达早报
  ├── 📁 10-开源生态 → 📄 GitHub 开源项目追踪
  ├── 📁 20-学术前沿 → 📄 学术论文前沿
  ├── 📁 30-商业动态 → 📄 AI 商业动态
  ├── 📁 40-研发效能 → 📄 AI 研发效能工具库
  └── 📁 90-综合报告 → 📄 综合周报
  ```
- **API 能力边界**:
  - ✅ 读取文件夹、创建文档、写入 Bitable、移动文件
  - ❌ 创建文件夹 (CDN 404)、删除文档 (无权限)

---

## 6. 需求清单 (Requirements Checklist)

### 6.1 已实现 ✅
- [x] 四象限分类体系 (Capabilities/Patterns/Ecosystem/Business)
- [x] PM Score 评分系统
- [x] 交互式知识图谱 (vis-network + 力导向布局)
- [x] 模板与数据分离架构
- [x] 中文摘要生成 (LLM)
- [x] 左侧仪表盘 (今日 Top 10)
- [x] 右侧详情面板 (完整摘要 + 原文链接)
- [x] 图例 (左下角固定)
- [x] 搜索/过滤功能
- [x] 节点统一圆形 + 大小映射 PM Score
- [x] 暗色主题
- [x] 零外部依赖 (本地 vis-network)
- [x] GitHub Pages 部署
- [x] 定时数据采集 (每 4h)
- [x] 飞书早报推送 (每日 08:00)
- [x] 飞书 Bitable 同步 (每日 06:00)
- [x] 周报生成 (每周一)

### 6.2 待实现/优化 🚧
- [ ] 移动端适配优化 (触摸手势、响应式布局)
- [ ] 节点时间轴过滤 (按日期范围筛选)
- [ ] 多语言切换 (中/英)
- [ ] 导出功能 (PNG/SVG 图谱截图)
- [ ] 节点关系强度可视化 (边的粗细/颜色)
- [ ] 历史版本对比 (本周 vs 上周)
- [ ] 用户收藏/书签功能
- [ ] 邮件订阅后端集成 (Formspree/Resend)
- [ ] 更多数据源接入 (HackerNews, ProductHunt, arXiv daily)

### 6.3 已知问题/限制 ⚠️
- 飞书 API 无法创建文件夹和删除文档
- GitHub Pages 屏蔽外部 CDN，必须本地化所有依赖
- LLM 分析有 Token 成本，需控制频率
- 中文摘要质量依赖 Prompt 设计

---

## 7. 开发规范 (Development Guidelines)

### 7.1 前端修改流程
1. 修改 `graph_template.html` (纯 HTML/CSS/JS)
2. 本地测试: `cd ~/ai-radar-wiki && python3 -m http.server 8080`
3. 运行数据注入: `python3 explorer.py --inject-only`
4. 验证 `graph.html` 输出
5. Git Commit + Push

### 7.2 数据 Pipeline 修改流程
1. 修改 `explorer.py` 采集/分析逻辑
2. 本地运行: `python3 explorer.py --full-run`
3. 验证 `graph.json` 和 `wiki/` 输出
4. Git Commit + Push
5. 观察 Cron 下次执行结果

### 7.3 需求变更管理
- 所有需求变更需更新本文档 (版本递增)
- 前端需求 → 更新 Section 4
- 数据需求 → 更新 Section 3
- 定时任务 → 更新 Section 5
- 需求清单 → 更新 Section 6

---

## 8. 技术栈

| 层级 | 技术 |
|------|------|
| **数据采集** | Python 3.10+, Requests, BeautifulSoup, ArXiv API |
| **智能分析** | Claude API / OpenAI API (LLM) |
| **数据格式** | JSON, Markdown, JSONL |
| **前端渲染** | vis-network.js (本地化), Vanilla JS, CSS3 |
| **部署** | GitHub Pages (Static Hosting) |
| **定时任务** | Cron (Linux), Hermes Agent Cron Jobs |
| **消息推送** | Feishu/Lark Bot API |
| **版本控制** | Git, GitHub |

---

## 9. 文件索引

```
~/ai-radar-wiki/
├── graph.html              # 最终部署文件 (数据已注入)
├── graph_template.html     # 前端模板 (开发用)
├── graph.json              # 图谱数据 (节点/边)
├── explorer.py             # 数据采集 + 分析 + 注入脚本
├── vis-network.min.js      # 本地化图谱渲染库
├── wiki/                   # Markdown 知识库
│   ├── capabilities/       # 技术能力
│   ├── patterns/           # 模式范式
│   ├── ecosystem/          # 开发生态
│   └── business/           # 商业动态
├── daily-digest/           # 每日情报 Markdown
├── ai-readable.jsonl       # 原始数据 (JSON Lines)
├── ai-agent.json           # AI Agent 发现配置
├── .well-known/            # 标准发现端点
└── DESIGN.md               # 本文档
```

---

## 10. 变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0.0 | 2026-05-06 | 初始版本：基础图谱 + 飞书集成 + Cron 任务 |
| v2.0.0 | 2026-05-07 | 架构重构：模板分离 + 四象限分类 + 左侧仪表盘 + 右侧详情面板 + 图例恢复 + 节点圆形化 + 中文摘要回退 |
| v3.0.0 | 2026-05-07 | UI 重构 + 订阅功能：仓库根目录整理 + 图例随滑窗移动 + 摘要按钮移至左侧 + 右侧显示原文预览 + RSS Feed 生成 + 邮件订阅页面 |
