# AI Radar 系统设计文档 (System Design Document)

> **版本**: v3.2.0  
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
┌─────────────────────────────────────────────────────────────────┐
│ [🧠 AI Radar]        [📅 收起] [📡 RSS] [nodes] [edges]         │
├─────────────────────┬─────────────────────────┬───────────────┤
│                     │                         │               │
│ 📅 今日情报摘要  [✕]│                         │ [✕] 详情面板   │
│ ─────────────────── │                         │               │
│ ▌ Headline          │                         │ 标题 + 标签    │
│                     │                         │               │
│ 🎯 值得关注         │    交互式知识图谱         │ 📝 摘要总结   │
│ · Design Conductor  │    (vis-network.js)       │ (120字精炼)   │
│ · SQLite...         │    - 力导向图             │               │
│                     │    - 可拖拽/缩放           │ 📄 原文       │
│ 📊 Stats            │    - 节点颜色=分类        │ 来源 日期 类型 │
│                     │                         │ [原文预览框]   │
│ 📊 趋势洞察         │                         │               │
│ ▼ LLM 可靠性        │                         │ [🔗查看原文]   │
│   · 说明文字         │                         │ [📋完整原文]   │
│   ↗ 文章1/2/3       │                         │               │
│ ▼ AI Agent          │                         │               │
│   · 说明文字         │                         │               │
│   ↗ 文章1/2/3       │                         │               │
│                     │                         │               │
│ ┌─────────────────┐ │                         │               │
│ │ 🔵 技术能力      │ │                         │               │
│ │ 🟢 产品模式      │ │                         │               │
│ │ 🟣 工具生态      │ │                         │               │
│ │ 🟠 商业趋势      │ │                         │               │
│ └─────────────────┘ │                         │               │
└─────────────────────┴─────────────────────────┴───────────────┘
```

### 4.3 核心 UI 组件

#### 左侧仪表盘 (Dashboard)
- **默认状态**: 展开，**撑满窗口高度** (`top: 56px; bottom: 12px`)
- **宽度**: 340px
- **内容顺序** (从上到下):
  1. **Headline**: 一句话总结今日核心趋势 (渐变背景 + 左边框)
  2. **Watch List**: 值得关注的单个项目 (可点击 → 聚焦节点)
  3. **Stats**: 一句话数据概览
  4. **趋势洞察**: 按分类的可折叠洞察区域，**默认全部展开**
     - 每个洞察含：标题 + 说明文字 + 佐证文章链接
     - 点击文章链接自动聚焦到图谱对应节点
- **折叠**: 点击 Header 按钮 `📅 收起/展开` 或面板内 `✕` 按钮

#### 图例 (Legend)
- **位置**: 画布上（非固定），跟随面板滑动
- **面板展开时**: `left: 372px`（与面板有间距）
- **面板收起时**: `left: 12px`（滑动画布左下角）
- **过渡动画**: `transition: left 0.3s ease`
- **内容**: 四大分类的颜色标识 + 中文说明
- **样式**: 半透明背景，圆角，不遮挡图谱

#### 右侧详情面板 (Detail Panel)
- **触发**: 点击图谱节点
- **宽度**: 460px
- **内容**:
  - **标题**: 完整节点名称
  - **标签行**: 分类 + 日期 + PM Score + 类型
  - **📝 摘要总结**: 精炼版 (120字以内，超过截断)
  - **📄 原文**: 
    - 来源信息: 域名 + 日期 + 类型
    - 原文预览框: 完整原文内容 (保持原始语种)
  - **🔗 查看原文**: 直接跳转 URL 按钮 (Primary)
  - **📋 完整原文**: 切换显示完整原文 vs 精炼摘要 (Secondary)
- **回退机制**: 若无摘要，显示对应类型的中文提示文案
- **关闭**: 点击面板内 `✕` 按钮或点击图谱空白区域

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

### 5.5.4 结构化摘要生成
- **路径**: `~/.hermes/scripts/generate_daily_summary.py`
- **输入**: `~/ai-radar-wiki/graph.json` (今日数据)
- **输出**: `~/ai-radar-wiki/daily_summary.json`
- **LLM**: DashScope qwen-plus
- **生成时机**: explorer.py 运行后 / cron 调用
- **格式**: JSON (headline, insights, watch_list, stats)

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
| v3.1.0 | 2026-05-07 | 结构化摘要 + 图例跟随：图例放画布上跟随面板滑动 + 左侧面板改为 LLM 结构化摘要（headline → insights → watch list）+ 摘要和预览区分内容 |
| v3.2.0 | 2026-05-07 | Linear 风格重构：面板撑满高度 + 内容重排 (Headline → Watch → Stats → 洞察) + 图例间距 + 右侧详情增加来源/日期 + 摘要精炼版 vs 完整原文 |
