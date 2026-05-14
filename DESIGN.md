---
name: ai-radar-design
category: devops
description: AI Radar 系统设计文档 v4.0.0 — 架构、数据流水线、前端规范、Schema、订阅系统、公众号文章、开发流程
version: 4.0.0
updated: 2026-05-14
---

# AI Radar 系统设计 (v4.0.0)

## 架构概要

### 系统全貌
AI Radar 是一个自动化 AI 情报知识库系统，面向 AI 产品经理。系统自动采集、分析、聚合全球 AI 领域动态，生成可视化知识图谱和深度分析文章。

- **数据采集**: Python 爬虫 (6 个数据源)，每 6h 运行一次
- **LLM 分析**: 自动翻译、分类、评分、提取概念
- **知识图谱**: graph.json (499 节点, 15072 边) + vis-network 可视化
- **前端**: 模板与数据分离架构 — graph_template.html + graph.json → graph.html
- **部署**: GitHub Pages (archwang.top)，零外部依赖，vis-network 本地化
- **每日摘要**: LLM 生成观点驱动的结构化摘要 (daily_summary.json)
- **公众号文章**: 每日 19:00 自动生成深度分析 HTML 文章，推送飞书聊天
- **飞书集成**: Bitable 多维表格同步 (每日 06:00) + 云文档更新
- **订阅系统**: RSS Feed (每 4h) + 邮件订阅页面

### 仓库结构
```
ai-radar-wiki/
├── graph.html              # 最终部署文件（数据已注入）
├── graph_template.html     # 纯静态模板（{{DATA}} 占位符）
├── graph.json              # 知识图谱数据
├── daily_summary.json      # 每日结构化摘要
├── weekly_trends.json      # 周趋势叙事链
├── feed.xml                # RSS 2.0 Feed
├── index.md                # Wiki 索引
├── README.md               # 项目说明
├── DESIGN.md               # 本设计文档
├── daily-articles/         # 公众号文章归档
├── summary_archive/        # 每日摘要历史
├── wiki/                   # Wiki 页面 (entities + concepts + papers)
├── reports/                # 四象限报告
├── daily-digest/           # 每日情报原始输出
├── data/                   # ai-readable.jsonl, ai-index.json, feedback.json
├── docs/                   # evolution.md, log.md, SCHEMA.md
├── raw/                    # 原始采集数据 (TTL 30天自动清理)
└── assets/                 # vis-network.min.js, 静态资源
```

## 四支柱分类 (4-Pillar)

| Pillar | 颜色 | 覆盖 | 节点数 |
|--------|------|------|--------|
| capabilities | #58a6ff (蓝) | 新模型、算法、技术突破 | ~168 |
| patterns | #3fb950 (绿) | 新交互、工作流、AI 应用模式 | ~128 |
| ecosystem | #a371f7 (紫) | 框架、SDK、库、开源社区 | ~83 |
| business | #f0883e (橙) | 融资、产品发布、市场 | ~120 |

**分类逻辑**: 基于关键词匹配 + LLM 确认。未匹配任何关键词的默认归入 `capabilities`（研究/学术内容）。

## 数据流水线 (Pipeline)

### 数据流
```
采集 (6数据源) → 去重 → LLM 分析 (翻译+分类+评分) → PM Score 计算
  → 生成 graph.json → 生成 wiki 页面 → 生成 daily_summary
  → 生成 graph.html → 生成 index.md → 自我进化 → 生成 digest
  → 保存状态 → 清理过期 raw → 周趋势更新
```

### 执行顺序（严格）
1. `batch_analyze_items()` — LLM 批量分析新采集项
2. `build_wiki_pages()` — 生成 Wiki Markdown 文件
3. `build_graph_json()` — 构建知识图谱 JSON
4. `generate_daily_summary.py` — 生成每日结构化摘要
5. `generate_graph_html()` — 注入数据到模板，生成 graph.html
6. `update_index()` — 更新 Wiki 索引
7. `run_self_evolution()` — 过期节点清理 + 趋势检测
8. `generate_daily_digest()` — 生成每日情报原始文件
9. `save_state()` — 保存采集状态
10. `clean_old_raw()` — TTL 清理过期原始数据
11. `weekly_trends.py` — 更新叙事链趋势

### 关键脚本

| 脚本 | 职责 | 大小 |
|------|------|------|
| `ai_radar_explorer.py` | 主 Pipeline: 采集→去重→LLM→Score→生成 | 84KB (1900行) |
| `generate_daily_summary.py` | 结构化每日摘要 (LLM 调用) | 30KB |
| `generate_rss.py` | RSS 2.0 feed 生成 | 3.8KB |
| `generate_daily_article.py` | 公众号深度文章生成 | 9.5KB |
| `ai_radar_sync.py` | 飞书 Bitable 同步 + 云文档更新 | 16KB |
| `ai_model_router.py` | 统一 LLM 路由（双模型 fallback） | 16.6KB |
| `weekly_trends.py` | 叙事链趋势分析与更新 | 15.9KB |
| `ai_radar_health_check.py` | 系统健康监控 | 8.7KB |
| `chat_health_check.py` | AI Chat Server 健康监控 | 5.1KB |

### 数据源 (6个)
| 数据源 | 类型 | Pillar 倾向 |
|--------|------|-------------|
| GitHub Trending | 开源项目 | ecosystem |
| arXiv (cs.AI/cs.LG/cs.CL) | 学术论文 | capabilities |
| HackerNews (AI 关键词过滤) | 技术讨论 | patterns/ecosystem |
| Product Hunt (AI 类别) | 产品发布 | business |
| TechCrunch (AI 频道) | 商业/融资 | business |
| Show HN (AI 项目) | 项目展示 | ecosystem/patterns |

## 数据 Schema (v4.0.0)

### graph.json 节点字段
```json
{
  "id": "unique_id",
  "label": "显示名称",
  "type": "github|paper|hn|techcrunch|products|showhn|news|discussion|concept|project",
  "pillar": "capabilities|patterns|ecosystem|business",
  "pm_score": 0.0-1.0,
  "tags": ["源类型", "pillar"],
  "summary": "中文摘要(200-500字)",
  "raw_content": "原始内容Markdown",
  "source_type": "github|papers|hn|techcrunch等",
  "date": "YYYY-MM-DD",
  "url": "原始链接",
  "stars": 0,
  "score": 0,
  "comments": 0
}
```

### daily_summary.json 字段（实际格式）
```json
{
  "daily_summary": {
    "date": "2026-05-14",
    "headline": "今日 AI 情报 · 2026-05-14",
    "overview": "一句话核心观点",
    "narratives": [
      {
        "title": "叙事标题",
        "body": "深度分析",
        "type": "validation|paradigm_shift|bottleneck"
      }
    ],
    "insights": [
      {
        "pillar": "💰 商业趋势",
        "pillar_key": "business",
        "narrative_title": "关联叙事",
        "insight": "洞察内容",
        "evidence": [
          {"id": "node-id", "title": "标题", "score": 0.6}
        ]
      }
    ],
    "stats": "技术能力: 11 | 产品模式: 1 | 工具生态: 2 | 商业趋势: 6",
    "total_items": 20,
    "high_value_count": 20,
    "all_today_ids": [{"id": "node-id", "label": "标题"}]
  }
}
```

### weekly_trends.json 字段
```json
{
  "narrative_chains": [
    {
      "id": "chain-id",
      "title": "趋势标题",
      "latest_date": "YYYY-MM-DD",
      "consecutive_days": 3,
      "trend_direction": "rising|stable|declining",
      "entries": [...]
    }
  ]
}
```

### 已移除字段
~~`group`~~、~~`summary_cn`~~、~~`pm_relevance`~~、~~`source_url`~~、~~`keywords`~~

### 边 (edges)
`{"source": "node_id", "target": "node_id", "relation": "...", "type": "KEYWORD|PILLAR|BELONGS_TO"}`

## PM Score 计算公式

```
score = engagement(0.3) + discussion(0.15) + timeliness(0.2) + LLM_relevance(0.35)
```
- **engagement**: stars/HN score，归一化到 0-0.3
- **discussion**: comments，归一化到 0-0.15
- **timeliness**: 距今天数衰减，最大 0.2
- **LLM_relevance**: (pm_relevance/10) * 0.35，最大 0.35

最终归一化到 0.0-1.0。

## LLM 分析集成

### ai_model_router 统一路由
- **双模型 fallback**: DashScope (Qwen) → DeepSeek
- **场景化配置**: `summary`（摘要生成）、`analysis`（深度分析）、`explorer`（探索分析）
- **缓存机制**: md5_hash(title + summary) 避免重复调用
- **降级策略**: LLM 失败 → 关键词分类

### 已知 LLM 配置
- Explorer: 批量分析 + JSON 缓存
- Daily Summary: LLM 深度洞察 + fallback 模式识别
- Daily Article: qwen-plus, scene=analysis, max_tokens=4000

## 前端架构

### 模板与数据分离
1. `graph_template.html` — 纯静态模板（含 `{{DATA}}` 占位符）
2. `graph.json` — 独立数据文件
3. `graph.html` = template + 注入的 JSON 数据（最终部署）

### 设计规范
- **视觉语言**: Airbnb 风格（圆角卡片、微妙阴影、响应式移动端布局）
- **品牌色**: `#ff385c` (Rausch 珊瑚红)
- **字体**: 系统默认无衬线字体
- **暗色主题**: 背景 `#08090a`，面板 `#0f1011`，边框 `rgba(255,255,255,0.08)`
- **节点**: 统一圆形 (`shape: 'dot'`)，大小映射 PM Score

### 布局
- **Header**: 收起按钮 + RSS 按钮 + 统计信息
- **左侧面板**: 默认展开，撑满窗口高度 (top:56px, bottom:12px, width:340px)
  - 内容: Headline → Watch List → Stats → 趋势洞察（全部展开）
  - 点击洞察文章 → 聚焦图谱节点
- **图例**: 画布上，跟随面板滑动 (展开: left 372px, 收起: left 12px)
- **右侧面板**: 460px，标题 + 标签 + 摘要(120字精炼) + 原文(完整) + 来源/日期/类型
- **相关情报**: 同 pillar 下 PM Score 最高的 5 个非 concept 节点

### 前端调试工作流
1. 修改 `graph_template.html`（HTML/CSS/JS 逻辑）
2. 运行数据注入（从 graph.json 读取数据替换 `{{DATA}}`）
3. 本地验证：`python3 -m http.server 8080` → 浏览器访问
4. 使用 `browser_console` 检查 JS 错误
5. 使用 `browser_vision` 确认视觉效果
6. 确认无误后 git push

### 已知前端陷阱
- ⚠️ `async` 函数声明遗漏 → **整个 JS 静默崩溃**
- ⚠️ `network.focus()` 不可靠 → 改用 `network.getPositions()` + `network.moveTo()`
- ⚠️ detail panel 原文预览必须用 `raw_content` 字段
- ⚠️ `searchArticle()` 匹配需多级策略（ID → 精确 → 包含 → 反向 → 摘要）
- ⚠️ **修改模板后必须重新生成 graph.html** — 线上加载的是 graph.html
- ⚠️ GitHub Pages CDN 缓存 → 需硬刷新（Ctrl+Shift+R）
- ⚠️ vis-network 节点抖动 → `physics.enabled: false` after stabilization

## 订阅系统

- **RSS Feed**: `feed.xml` (RSS 2.0)，每 4h 自动生成
- **生成脚本**: `~/.hermes/scripts/generate_rss.py`
- **Cron**: `ai-radar-rss-feed` (每 4h)

## 飞书集成

### Bitable 多维表格同步
- **脚本**: `~/.hermes/scripts/ai_radar_sync.py`
- **Cron**: `ai-radar-data-sync` (每日 06:00)
- **Bitable**: V1IZbGiLaa4V6ysQW3ycJamjngc
- **去重**: 基于文件名 + 内容哈希 (MD5)

### 飞书云文档
- **主文件夹**: `MPcgfuV3Zl6qsIdZlqRcDOCXnGd`
- **文件夹结构**:
  - `00-每日情报` → `AI 雷达早报`
  - `10-开源生态` → `GitHub 开源项目追踪`
  - `20-学术前沿` → `学术论文前沿`
  - `30-商业动态` → `AI 商业动态`
  - `40-研发效能` → `AI 研发效能工具库`
  - `90-综合报告` → `综合周报`

### API 能力边界
- ✅ 读取文件夹、创建文档、写入 Bitable、移动文件
- ❌ 创建文件夹（返回 404）、删除文档（无权限）

## 公众号文章系统

### 架构
- **脚本**: `~/.hermes/scripts/generate_daily_article.py`
- **技能**: `wechat-article-gen` (productivity 分类)
- **Cron**: `ai-radar-daily-deep-article` (每日 19:00)
- **数据源**: `daily_summary.json` (overview + narratives) + `graph.json` (当日节点)
- **输出**: HTML 文件（内联样式，微信公众号兼容）

### 生成流程
1. 读取 daily_summary.json 和 graph.json
2. 构建 LLM prompt（Stratechery 风格深度分析框架）
3. 调用 qwen-plus (scene=analysis, max_tokens=4000)
4. 保存到 `daily-articles/YYYY-MM-DD-标题.html`
5. Git add + commit + push
6. 通过飞书 API 发送 HTML 文件到聊天窗口

### 写作规范
- 深度归因，拒绝罗列（写出逻辑链，不是"A 发生了，B 发生了"）
- 每段一个论点，素材只是证据
- 专业、冷峻、客观（禁用情绪化词汇）
- 面向 PM（使用行业术语）

### 已知陷阱
- ⚠️ LLM 可能用 Markdown 代码块包裹 HTML（脚本已添加后处理清理）
- ⚠️ chat_id 硬编码在脚本中（第 190 行）
- ⚠️ 需要 FEISHU_APP_ID 和 FEISHU_APP_SECRET
- ⚠️ 生成后需手动复制到公众号编辑器发布

## Cron 任务清单 (当前 14 个活跃)

| 任务 | 调度 | 状态 | 职责 |
|------|------|------|------|
| ai-radar-explorer | 每 6h | ✅ 活跃 | 数据采集 + LLM 分析 + 图谱生成 |
| ai-radar-rss-feed | 每 4h | ✅ 活跃 | RSS Feed 生成 |
| ai-radar-health-check | 每 4h | ✅ 活跃 | 系统健康监控 |
| ai-radar-data-sync | 每日 06:00 | ✅ 活跃 | 飞书 Bitable + 云文档同步 |
| ai-daily-briefing | 每日 08:00 | ✅ 活跃 | 每日 AI 简报（飞书推送） |
| ai-product-launch-tracker | 周四 08:00 | ✅ 活跃 | 产品发布追踪 |
| ai-funding-intelligence | 周五 09:00 | ✅ 活跃 | 融资情报 |
| ai-community-buzz | 周二 09:00 | ✅ 活跃 | 社区热点 |
| dev-efficiency-tools-digest | 5/20日 09:00 | ✅ 活跃 | 研发效能 |
| arxiv-paper-digest | 周三 08:00 | ✅ 活跃 | 学术论文 |
| github-ai-trending-digest | 周一 09:00 | ✅ 活跃 | GitHub 趋势 |
| ai-radar-weekly-digest | 周一 10:00 | ✅ 活跃 | 综合周报 |
| ai-radar-daily-deep-article | 每日 19:00 | ✅ 活跃 | 公众号深度文章 |
| ai-chat-health-monitor | 每 30min | ✅ 活跃 | Chat Server 监控 |

**已暂停 6 个**: design-tools, monthly-trends, china-ai-news, company-strategy, agent-framework, open-model-benchmark

## 开发流程

1. **前端修改**: 改 `graph_template.html` → 本地测试 → 重新注入数据 → 验证 → push
2. **数据流水线**: 改 `ai_radar_explorer.py` → 验证语法 → 本地运行 → 验证 graph.json → push
3. **RSS 修改**: 改 `generate_rss.py` → 运行测试
4. **公众号文章**: 改 `generate_daily_article.py` → 本地运行 → 验证 HTML → push
5. **技能更新**: 修改后必须验证，废弃技能及时更新或删除

### 核心原则
- ❌ **不要把线上当测试场** — 用户明确要求先本地测试再推送
- ✅ **每次修改必须验证** — `python3 -m http.server` + `browser_console` + `browser_vision`
- ✅ **检查数据链路完整性** — 修改一处时检查整个链路（graph.json 是否丢失历史数据）
- ✅ **对数据准确性零容忍** — 概览数字与实际数量不一致必须修复

## 已知问题与修复状态

| 问题 | 状态 | 说明 |
|------|------|------|
| classify_pillar 返回 unknown | ✅ 已修复 (2026-05-14) | 默认改为 capabilities |
| graph.json 存在 unknown pillar 节点 | ✅ 已修复 (2026-05-14) | 2 个数学论文已修复 |
| ai-radar-daily-article 与 deep-article 冲突 | ✅ 已修复 (2026-05-14) | 移除旧任务 |
| daily_summary.json 格式文档不一致 | ✅ 已修复 (2026-05-14) | DESIGN.md 已更新为实际格式 |

## 环境依赖

- **Python 3.x** — 所有脚本
- **DASHSCOPE_API_KEY** — LLM 分析（Explorer + Summary + Article）
- **FEISHU_APP_ID / FEISHU_APP_SECRET** — 飞书集成
- **BITABLE_APP_TOKEN** — Bitable 同步（通过 cron 环境加载）
- **BITABLE_TABLE_ID** — Bitable 表格 ID
- **Git** — 版本控制 + GitHub Pages 部署

## 域名与部署

- **域名**: archwang.top
- **部署**: GitHub Pages (ttmens/ai-radar-wiki)
- **仓库**: github.com/ttmens/ai-radar-wiki
