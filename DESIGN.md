# AI Radar 系统设计文档 (System Design Document)

> **版本**: v3.10.1  
> **最后更新**: 2026-05-08  
> **维护者**: Hermes Agent  

> **在线地址**: https://ttmens.github.io/ai-radar-wiki/graph.html

---

## 1. 系统概述

AI 产品设计雷达是一个自动化 AI 技术情报系统，通过**采集 → 分析 → 可视化 → 推送**的完整链路，持续追踪 AI 领域的开源项目、学术论文、商业动态和研发效能工具，帮助 AI 产品经理和开发者快速获取高价值情报。

### 核心价值主张
- 🎯 **AI PM 视角**：按"技术/模式/生态/商业"四大维度评估项目
- ⏱️ **自动化**：每日自动采集、分析、生成报告，无需人工干预
- 🔗 **可交互**：知识图谱支持点击、搜索、筛选，一目了然
- 📈 **趋势分析**：周视图、叙事生命周期追踪、矛盾信号检测
- 🛡️ **保活机制**：自动监控、故障恢复、健康检查

---

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    数据采集层 (Scraper)                   │
│  GitHub API  │  ArXiv API  │  TechCrunch  │  HN/PShow   │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   智能分析层 (LLM Agent)                  │
│  中文摘要翻译  │  4-Pillar 分类  │  PM Score  │  缓存   │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    数据生成层 (Explorer)                  │
│  graph.json (节点/边)  │  wiki/  (Markdown 知识库)        │
│  daily-digest/ (日报)  │  ai-readable.jsonl (原始数据)     │
│  graph_template.html  │  feed.xml (RSS)                  │
│  daily_summary.json   │  weekly_trends.json (周趋势)     │
│  summary_archive/     │  health_log.json (健康日志)      │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    前端展示层 (Frontend)                  │
│  graph.html (交互式图谱)  │  Template-Data 分离架构        │
│  智瞰 NexSight 顶栏 │ 图谱 (vis-network) │ 左：情报面板 / 右：详情（桌面）     │
│  RSS·Star·Fork·统计 │ 概念=六边形        │ 窄屏：情报底栏 + 详情 Bottom Sheet │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    分发推送层 (Delivery)                  │
│  GitHub Pages (公开)  │  Feishu Bot (群聊/个人)           │
│  Cron 定时推送        │  RSS/Atom Feed                   │
└─────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    保活监控层 (Health)                    │
│  健康检查脚本  │  自动恢复  │  停滞检测  │  告警推送     │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 数据流水线 (Data Pipeline)

### 3.1 两阶段架构
| 阶段 | 职责 | 执行频率 | 工具 |
|------|------|----------|------|
| **Stage 1: 数据采集** | 从 GitHub/ArXiv/TechCrunch/HN 抓取 | 每 6 小时 | `ai_radar_explorer.py` |
| **Stage 2: 智能分析** | LLM 翻译、分类、评分、摘要生成 | 同 Stage 1 | DashScope qwen3.6-plus |

### 3.2 数据源与 Fetcher 配置

| 数据源 | Fetcher 函数 | 去重 Key | 状态 |
|--------|-------------|----------|------|
| GitHub | `fetch_github()` | `url` | ✅ 5 个独立查询（OR 不支持） |
| arXiv | `fetch_arxiv()` | `url` | ✅ 正常 |
| Hacker News | `fetch_hackernews()` | `hn_url` | ✅ 正常 |
| Product Hunt | `fetch_product_hunt()` | `url` | ✅ 正常 |
| TechCrunch AI | `fetch_techcrunch()` | `url` | ✅ 正常 |
| Show HN | `fetch_hn_show()` | `hn_url` | ✅ 正常 |

**GitHub API 重要限制**：GitHub Search API 不支持 `(topic:A OR topic:B)` 语法，必须拆分为多次独立查询：
```python
queries = [
    "stars:>50 pushed:>2026-04-01 topic:llm",
    "stars:>50 pushed:>2026-04-01 topic:artificial-intelligence",
    "stars:>50 pushed:>2026-04-01 topic:ai",
    "stars:>50 pushed:>2026-04-01 topic:machine-learning",
    "stars:>50 pushed:>2026-04-01 topic:deep-learning",
]
```
每个查询最多 2 页 (per_page=30)，使用 `seen_repos` 集合去重。

### 3.3 LLM 分析策略

**API 配置**：
- **端点**: `https://coding.dashscope.aliyuncs.com/v1`
- **模型**: `qwen3.6-plus`
- **Key**: `DASHSCOPE_API_KEY` (环境变量)
- **协议**: 兼容 OpenAI API

**LLM 分析优化**（防止超时）：
1. **限制数量**：最多 LLM 分析 30 条（按 stars 排序取 Top 30）
2. **缓存优先**：基于 MD5 hash 的 `llm_cache.json`，避免重复分析
3. **关键词降级**：超出 30 条的新情报自动走关键词分类降级
4. **并发控制**：并发度 = 8，带重试机制
5. **降级策略**：LLM 失败时自动回退到关键词分类

**PM Score 计算公式**：
```python
pm_score = (
    novelty_weight * (0-10) +      # 新颖度：技术突破/模式创新
    impact_weight * (0-10) +       # 影响力：Star 数/引用数/讨论热度
    relevance_weight * (0-10) +    # 相关性：对 AI PM 的参考价值
    timeliness_weight * (0-10)     # 时效性：发布时间衰减
) / 4.0
```

### 3.4 数据 Schema

graph.json 节点实际字段（v3.10.0）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一节点标识（如 `mempalacemempalace`） |
| `label` | string | 节点显示名称 |
| `pillar` | string | 四支柱分类：`capabilities`/`patterns`/`ecosystem`/`business` |
| `summary` | string | 中文摘要（LLM 生成或关键词降级） |
| `date` | string | 采集日期 `YYYY-MM-DD` |
| `pm_score` | float | PM 评分 0.0-10.0 |
| `url` | string | 原始链接 |
| `raw_content` | string | 原始内容（Markdown 格式，含概览+数据+关系） |
| `type` | string | 节点类型：`github`/`paper`/`hn`/`techcrunch`/`products`/`showhn`/`news`/`concept` |
| `tags` | array | 标签数组（如 `["github", "ecosystem"]`） |
| `source_type` | string | 数据来源类型（如 `github`/`papers`/`hn`/`news`/`techcrunch`/`products`） |
| `stars` | int | GitHub Star 数（仅 github 类型） |
| `score` | int | HN 得分（仅 hn/showhn 类型） |
| `comments` | int | 评论数（GitHub discussions / HN） |

**已移除字段**（v3.6.0 起）：
- ~~`group`~~ — 已合并到 `pillar`
- ~~`summary_cn`~~ — 已合并到 `summary`
- ~~`pm_relevance`~~ — 不再使用
- ~~`source_url`~~ — 统一使用 `url`
- ~~`keywords`~~ — 不再使用

边 (edges) 字段：
```json
{ "id": "edge_id", "from": "node_id", "to": "node_id", "type": "PILLAR" }
```

### 3.5 日报 Digest 数据源

每日情报 Digest 由两个数据源组成：

**1. `daily-digest/YYYY-MM-DD.md`**：从 `graph.json` 读取**当天全部节点**，按 `pm_score` 排序后生成 Markdown 摘要。

**2. `daily_summary.json`**（v3.7.0 新增）：结构化深度分析摘要，由 `generate_daily_summary.py` 生成：

```json
{
  "daily_summary": {
    "date": "2026-05-08",
    "headline": "今日 AI 情报 · 2026-05-08",
    "overview": "一句话概括今天最重要的跨节点趋势",
    "narratives": [
      {
        "title": "叙事标题（如：AI从对话走向自主操作系统级控制）",
        "body": "2-3句深度分析：解释趋势含义 + PM启示 + 后续发展",
        "type": "paradigm_shift|bottleneck|maturation|validation"
      }
    ],
    "insights": [
      {
        "pillar": "📱 产品模式",
        "pillar_key": "patterns",
        "insight": "该pillar的深度洞察（基于信号识别）",
        "evidence": [
          {"id": "节点ID", "title": "标题", "score": 0.0, "url": "...", "reason": "里程碑式进展"}
        ],
        "trend": "new|rising|stable|declining"
      }
    ],
    "stats": "分类统计",
    "total_items": 总数,
    "high_value_count": "PM Score >= 0.3 的数量",
    "all_today_ids": [{"id": "节点ID", "label": "标题"}]
  }
}
```

**分析模式**：
- **LLM 模式**：跨节点综合研判（需 DashScope API key），参考 Stratechery 风格
- **Fallback 模式**：基于 8 种信号主题的自动模式识别，检测 4 种叙事类型
  - 🔄 范式转移、⚠️ 核心瓶颈、📈 行业成熟、💡 模式验证
- **Insight 去重**：每个叙事主线一对一分配到最佳匹配的 pillar，避免多 pillar 重复相同文本

### 3.6 周趋势分析（Phase 2 - v3.9.0 新增）

**文件**: `weekly_trends.json` + `summary_archive/`

**功能**：
- **支柱趋势**：计算 4 大支柱的日环比变化（`delta`），标记趋势状态（`🔥 升温`/`➡️ 平稳`/`❄️ 降温`）
- **叙事链追踪**：跨天匹配相同叙事标题，合并为"出现在 [日期列表]"的紧凑形式
- **矛盾信号检测**：识别同一天内相互矛盾的叙事（如"A 公司成功" vs "A 公司失败"）
- **叙事生命周期**：标记叙事阶段（`rising`/`stable`/`declining`）

**数据结构**：
```json
{
  "generated_at": "2026-05-08T15:59:30",
  "days_analyzed": 2,
  "pillar_trends": {
    "capabilities": {"trend": "stable", "delta": 0, "current": 1, "previous": 1},
    "patterns": {"trend": "stable", "delta": 0, "current": 1, "previous": 1},
    "ecosystem": {"trend": "stable", "delta": 0, "current": 1, "previous": 1},
    "business": {"trend": "stable", "delta": 0, "current": 1, "previous": 1}
  },
  "narrative_chains": [
    {
      "title": "AI从对话式向自主操作系统级控制演进",
      "type": "paradigm_shift",
      "days": ["2026-05-08"],
      "instances": [{"date": "2026-05-08", "title": "..."}],
      "latest_type": "paradigm_shift",
      "lifecycle": "rising"
    }
  ],
  "contradictions": [
    {"narrative_a": "...", "narrative_b": "...", "reason": "矛盾描述"}
  ]
}
```

**前端集成**：
- 日/周视图切换按钮（透明 tab 风格，固定在面板顶部）
- 周视图显示：支柱趋势状态、叙事链（去重后）、矛盾信号
- 点击"✕"关闭周视图，返回日视图

### 3.7 四象限分类体系 (4-Pillar Framework)
| Pillar | 中文 | 颜色 | 覆盖范围 |
|--------|------|------|----------|
| `capabilities` | 🤖 技术能力 | `#58a6ff` (蓝) | 新模型、算法、工具、技术突破 |
| `patterns` | 📱 模式/范式 | `#3fb950` (绿) | 新交互方式、工作流、AI 应用模式 |
| `ecosystem` | 🔧 开发生态 | `#a371f7` (紫) | 框架、SDK、库、平台、开源社区 |
| `business` | 💰 商业动态 | `#f0883e` (橙) | 融资、产品发布、公司战略、市场 |

### 3.8 去重与缓存机制
- **去重 Hash**: 持久化在 `state.json` 的 `seen` 数组
- **重建机制**: `rebuild_seen_from_raw()` 从 `raw/` 目录重建去重 hash
- **LLM 缓存**: `llm_cache.json` 存储 LLM 分析结果，避免重复调用
- **raw/ TTL**: `clean_old_raw(ttl_days=30)` 自动清理 30 天前的原始文件

### 3.9 graph.json 数据持久化（v3.7.0 修复）

**问题**（v3.6.0 及之前）：`build_graph_json(all_items)` 每次运行都用**本次新增的 items** 重新构建整个 graph.json。当某次采集到 0 条新数据时，graph.json 被覆盖为只剩概念节点，**历史数据全部丢失**。

**修复**：`build_graph_json()` 改为合并模式：
1. 先加载现有 `graph.json` 的所有节点和边
2. 将本次新增节点合并进去（按 `id` 去重）
3. 保留所有历史边
4. 按 `pm_score` 排序后输出

```python
# 伪代码
existing = load("graph.json")
all_nodes = list(new_nodes) + [n for n in existing.nodes if n.id not in new_ids]
all_edges = list(new_edges) + existing.edges
```

---

## 4. 前端设计规范 (Frontend Design)

### 4.1 核心架构原则
> **模板与数据分离 (Template-Data Separation)**

- `graph_template.html`: 纯静态前端模板（HTML/CSS/JS），不含业务数据，包含 `{{DATA}}` 占位符
- `graph.json`: 独立数据文件（节点/边）
- `graph.html`: 部署文件（模板 + JSON 注入）；开发与样式修改以 **`graph_template.html` 为准**，再同步/注入到 `graph.html`
- Python 注入：`json.dumps(graph_data, ensure_ascii=False)`，禁止带未转义控制字符的裸 JSON

### 4.2 视觉语言与设计基线（当前实现）

整体遵循 **Airbnb 系浅色情报产品** 语言（注释见 `graph_template.html` 样式头部）：

| 维度 | 约定 |
|------|------|
| **主色 / CTA** | Rausch 珊瑚色 `--rausch: #ff385c`（`theme-color` 同步）；悬停 `--rausch-active` |
| **画布** | 页面背景 `--bg` / `--surface-soft`，图谱区域 `--graph-canvas: #ebebeb` |
| **面板** | `--panel-bg: #ffffff`，细边 `--hairline` / `--hairline-soft` |
| **正文** | `--ink` / `--body-ink`，次要文字 `--muted` 体系 |
| **圆角** | `--radius-sm` 8px → `--radius-lg` 20px |
| **阴影层级** | `--shadow-sm` / `--shadow-md` / `--shadow-lg`；桌面左栏与右侧详情以 **`shadow-md`** 为主，避免多层重阴影堆叠 |
| **移动端再上提一层** | 节点详情底栏（modal 层）阴影略重于情报底栏；顶栏 RSS 为次要入口（`.header-rss` 灰阶弱强调，非主色满铺） |

### 4.3 页面布局（桌面 vs 移动）

**桌面（宽屏）** — 顶栏绝对定位，下方为图谱画布；**左侧情报**与**右侧节点详情**均为贴边侧栏（`position: absolute`），高度由 `--header-h`（JS 实测顶栏高度）与 `--side-sheet-from-top` / `--side-sheet-gap-bottom` 约束。

**移动（`max-width: 900px`）** — 布局切换为「地图 + 底栏」模式：

- **情报 ` #dashboard `**：贴屏幕**底**，高度约 **`60vh` / `60dvh`**，顶缘圆角；顶区 **拖条**可下滑收起（并可键盘 Enter/空格触发收起辅助）。
- **`#dashboard-expand-btn`（情报摘要）**：右下 **FAB** 展开已收起的情报栏。
- **节点详情 ` #detail-panel `**：自屏幕**底缘**上滑的 **Bottom Sheet**；关闭态使用 **`translate3d(0, 100dvh, 0)`**（辅 `100vh`）保证整页划入划出，避免 `translateY(100%)` 随内容高度变化导致抖动；**`#panel-scrim`** 在窄屏用 **opacity + visibility** 过渡，减少 `display` 切换导致的整页跳动。
- **顶栏**：单行横向滚动；**节点/边统计**迁入 **`#graph-stats-hud`** 浮层；顶栏右侧加 **极弱右侧内阴影** 提示「右滑还有更多操作」。窄屏隐藏顶栏「摘要」按钮，以底栏/FAB 为主入口。
- **图例 ` #legend `**：窄屏为顶栏下方的**横向滚动条**，不遮挡主图区。

### 4.4 核心 UI 组件（与实现对应）

#### 左侧情报（Dashboard / `.dash-content`）
- **Brief headline（`.brief-headline`）**：`position: sticky; top: 0; z-index: 100`，实心背景 + 底部分割，滚动时压住下方叙事卡片。
- **滚动容器**：`.dash-content` **顶部 padding 为 0**，避免 WebKit 下 sticky 与 padding 叠加出现正文「漏缝」；左右仍保留内边距。
- **首屏加载**：`.dash-skeleton` 骨架占位；若 `daily_summary.json` 失败而走 fallback，顶部 **`dash-data-banner`** 标明离线/基于图谱的摘要。
- **日/周切换**：`view-toggle` 分段控件（详见周趋势章节）。

#### 右侧详情（Detail Panel）
- **桌面**：从右侧 **`translateX(100%)` → `0`** 滑入，`z-index: 80`。
- **移动**：自底部滑入；章节标题为纯文字：**摘要总结 / 原文 / 相关情报**（主面板区去除装饰性 emoji，与高密度阅读场景一致）；主操作仍为「查看原文」「完整原文」。
- **遮罩**：移动开启详情时 **`#panel-scrim`** 可点按关闭，与 **`Escape`** 键一致；打开时 **`role="dialog"`**、窄屏 **`aria-modal="true"`**，焦点进入关闭按钮且 **`focus({ preventScroll: true })`**，避免移动端视口被焦点滚动带偏。

#### 无障碍与动效
- **`prefers-reduced-motion: reduce`**：`#dashboard`、`#detail-panel`、`#legend`、FAB、主要按钮等 **transition 近似关闭**；骨架 pulse 关闭。
- **RSS**：`title` + `aria-label` 标明订阅含义。

### 4.5 节点与边（vis-network）

| 属性 | 规则 |
|------|------|
| **普通节点** | `shape: 'dot'`，大小与 `pm_score`、类型相关 |
| **概念节点** | `shape: 'hexagon'`，尺寸与 `node_count` 相关，颜色按 pillar 略加深 |
| **颜色** | 与四支柱色一致（capabilities / patterns / ecosystem / business） |
| **字色** | 节点标签浅色描边以保证深背景上的可读性（见模板内 `font` 配置） |
| **边** | `BELONGS_TO`、PILLAR 等类型区分颜色与线宽 |

窄屏下图谱相机脚本会将簇心对齐到**顶栏与情报底栏之间的可视带**，避免节点被挡。

### 4.6 顶栏（Header）控件

| 区域 | 内容 |
|------|------|
| 品牌 | Logo（`nexsight-mark.svg`）+ **智瞰 NexSight** + 副标题 **面向产品经理的AI全景情报**（单行省略） |
| RSS | 文案「RSS」，样式 **`.header-rss`**（次要灰阶按钮，非主色 CTA） |
| 统计 | 桌面：`N 节点` / `M 边`（中文）；窄屏：`#stats` 隐藏，由 HUD 展示 |
| GitHub | Star / Fork（窄屏可缩为图标优先级） |

### 4.7 技术约束（前端）

- **零外部依赖**：`vis-network.min.js` 等必须为本地化脚本
- **单页静态**：适合 GitHub Pages；**浅色主题**为当前默认（不再使用文档旧版所述 GitHub Dark 整块配色作为图谱页主界面）
- **安全区**：`env(safe-area-inset-*)` 参与顶栏、底栏、FAB、`--side-sheet-gap-bottom` 等
- **JSON 注入**：同 4.1，必须 `ensure_ascii=False` 且无非法控制字符

---

## 5. 定时任务系统 (Cron Jobs)

### 5.1 任务矩阵
| 任务名称 | 频率 | 职责 | 交付目标 | 状态 |
|----------|------|------|----------|------|
| `ai-radar-explorer` | 每 6h | 数据采集 + 分析 + 生成 graph.json/wiki | 本地文件 + Git Push | ✅ 运行中 |
| `ai-radar-data-sync` | 每日 06:00 | 同步数据到飞书 Bitable | Feishu Bitable | ✅ 运行中 |
| `ai-daily-briefing` | 每日 08:00 | 生成并推送早报 | Feishu 群聊 | ✅ 运行中 |
| `ai-radar-weekly-digest` | 每周一 10:00 | 生成周报 | Feishu + 本地文件 | ✅ 运行中 |
| `ai-radar-rss-feed` | 每 4h | 生成 RSS Feed | feed.xml + Git Push | ✅ 运行中 |
| `ai-radar-health-check` | 每 4h | 健康检查 + 自动恢复 | 本地日志 | ✅ 运行中 |
| `github-ai-trending-digest` | 每周一 09:00 | GitHub 趋势分析 | Feishu | ✅ 运行中 |
| `dev-efficiency-tools-digest` | 每月 5/20 | 研发效能分析 | Feishu | ✅ 运行中 |
| `arxiv-paper-digest` | 每周三 08:00 | 论文分析 | Feishu | ✅ 运行中 |
| `ai-funding-intelligence` | 每周五 09:00 | 融资情报 | Feishu | ✅ 已恢复 |
| `ai-product-launch-tracker` | 每周四 08:00 | 产品发布追踪 | Feishu | ✅ 已恢复 |
| `ai-community-buzz` | 每周二 09:00 | 社区讨论挖掘 | Feishu | ✅ 已恢复 |
| ~~ai-design-tools-digest~~ | ~~半月~~ | ~~设计工具分析~~ | ~~Feishu~~ | ⏸️ 已暂停 |
| ~~china-ai-news-digest~~ | ~~周~~ | ~~中国 AI 新闻~~ | ~~Feishu~~ | ⏸️ 已暂停 |
| ~~ai-company-strategy-watch~~ | ~~周~~ | ~~大厂战略追踪~~ | ~~Feishu~~ | ⏸️ 已暂停 |
| ~~ai-agent-framework-watch~~ | ~~周~~ | ~~Agent 框架追踪~~ | ~~Feishu~~ | ⏸️ 已暂停 |
| ~~open-model-benchmark~~ | ~~半月~~ | ~~开源模型基准~~ | ~~Feishu~~ | ⏸️ 已暂停 |
| ~~monthly-tech-trends~~ | ~~月~~ | ~~月度趋势报告~~ | ~~Feishu~~ | ⏸️ 已暂停 |

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

## 6. 安全与配置管理

### 6.1 敏感信息管理
- **API Key 存储**: `~/.hermes/.env` 文件
- **.gitignore 规则** (~/ai-radar-wiki/.gitignore):
  ```
  # Secrets - NEVER commit
  .env
  .env.*
  *.key
  *.pem
  ```
- **验证**: `git ls-files .env` 确认未提交

### 6.2 LLM API 配置
```bash
# ~/.hermes/.env
DASHSCOPE_API_KEY=***
DASHSCOPE_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
```

### 6.3 Explorer 脚本配置
- **路径**: `~/.hermes/scripts/ai_radar_explorer.py`
- **模板路径**: `~/ai-radar-wiki/graph_template.html`
- **降级逻辑**: 模板不存在时，自动从 `graph.html` 提取并生成 `graph_template.html`
- **自动创建目录**: `build_wiki_pages()` 启动时自动创建 `wiki/entities/`、`wiki/concepts/`、`daily-digest/`、`summary_archive/`

---

## 7. 保活监控机制 (Health Check)

### 7.1 监控脚本
**文件**: `~/.hermes/scripts/ai_radar_health_check.py`

**功能**:
- **图谱停滞检测**: 检查 `graph.json` 更新时间，超过 12 小时未更新视为停滞
- **节点增长监控**: 跟踪节点增长趋势，连续 3 次无显著新增触发告警
- **Cron 任务状态**: 检查关键 cron 任务是否正常运行
- **数据源健康度**: 验证各数据源是否有数据
- **自动恢复**: 自动创建缺失目录、尝试重新运行 explorer

### 7.2 告警阈值
| 检查项 | 阈值 | 告警级别 |
|--------|------|----------|
| graph.json 更新时间 | > 12 小时 | WARNING |
| 连续零新增次数 | ≥ 3 次 | WARNING |
| 关键 cron 任务状态 | 暂停/失败 | WARNING |
| 数据源无数据 | 主要源为空 | CRITICAL |

### 7.3 自动恢复动作
1. 检查并创建 `wiki/concepts/`、`wiki/entities/`、`daily-digest/`、`summary_archive/`
2. 检查 `vis-network.min.js` 是否存在
3. 如果数据停滞超过阈值，自动触发 explorer 运行

---

## 8. 需求清单 (Requirements Checklist)

### 8.1 已实现 ✅
- [x] 四象限分类体系 (Capabilities/Patterns/Ecosystem/Business)
- [x] PM Score 评分系统
- [x] 交互式知识图谱 (vis-network + 力导向布局)
- [x] 模板与数据分离架构
- [x] 中文摘要生成 (LLM qwen3.6-plus)
- [x] 左侧仪表盘 (叙事主线 + 分领域证据)
- [x] 右侧详情面板 (完整摘要 + 原文预览 + 原文链接 + 相关情报)
- [x] 图例 (左下角固定，面板收起时跟随滑动)
- [x] 节点圆形（普通）/ 六边形（概念）+ 大小映射 PM Score
- [x] 浅色主题（Airbnb/Rausch 情报视觉，图谱页默认）
- [x] 零外部依赖 (本地 vis-network)
- [x] GitHub Pages 部署
- [x] 定时数据采集 (每 6h)
- [x] 飞书早报推送 (每日 08:00)
- [x] 飞书 Bitable 同步 (每日 06:00)
- [x] 周报生成 (每周一)
- [x] RSS Feed 生成
- [x] LLM 分析缓存 (避免重复调用)
- [x] LLM 分析限制 (Top 30 + 关键词降级)
- [x] GitHub fetcher OR 查询拆分
- [x] JSON 注入控制字符修复
- [x] 模板自动提取降级逻辑
- [x] .gitignore 防泄露
- [x] raw/ 目录 TTL 清理
- [x] 去重 Hash 重建机制
- [x] graph.json 数据持久化 (合并模式，不再丢失历史数据)
- [x] 每日深度分析摘要 (Narratives + Insights + Evidence)
- [x] Sticky Headline + 竖向展开按钮
- [x] 两侧面板高度对齐
- [x] GitHub Star/Fork 按钮
- [x] 基于 ID 的节点精确定位 (非模糊文本匹配)
- [x] 日/周视图切换 (v3.9.1)
- [x] 周趋势分析框架 (v3.9.0)
- [x] 叙事链去重追踪
- [x] 矛盾信号检测
- [x] 保活监控脚本 (v3.10.0)
- [x] 自动恢复机制
- [x] 健康日志追踪
- [x] 移动端：情报底栏（≈60vh）+ 节点详情 Bottom Sheet + 顶栏/FAB 布局
- [x] 图谱页无障碍基础：详情 Escape、焦点 preventScroll、dialog 语义、RSS 可访问名称
- [x] prefers-reduced-motion 下降动效强度

### 8.2 待实现/优化 🚧
- [ ] 移动端体验持续优化（如首次使用引导、图例说明入口等增量）
- [ ] 节点时间轴过滤 (按日期范围筛选)
- [ ] 多语言切换 (中/英)
- [ ] 导出功能 (PNG/SVG 图谱截图)
- [ ] 节点关系强度可视化 (边的粗细/颜色)
- [ ] 历史版本对比 (本周 vs 上周)
- [ ] 用户收藏/书签功能
- [ ] 邮件订阅后端集成 (Formspree/Resend)
- [ ] 中文字体本地化 (解决截图中文本方块问题)
- [ ] 飞书告警推送 (健康检查告警)
- [ ] 数据源扩展 (更多商业/生态数据源)

### 8.3 已知问题/限制 ⚠️
- 飞书 API 无法创建文件夹和删除文档
- GitHub Pages 屏蔽外部 CDN，必须本地化所有依赖
- LLM 分析有 Token 成本，已控制频率（Top 30 + 缓存）
- DashScope coding 端点仅支持 `qwen3.6-plus`，标准端点 Key 无效
- 浏览器截图环境中文字体缺失（显示为方块），但实际访问正常
- `weekly_trends.json` 需要 7+ 天数据才能生成有意义的趋势分析（当前仅 2 天）

---

## 9. 开发规范 (Development Guidelines)

### 9.1 前端修改流程
1. 修改 `graph_template.html` (纯 HTML/CSS/JS)
2. 本地测试: `cd ~/ai-radar-wiki && python3 -m http.server 8080`
3. 运行数据注入: `python3 explorer.py --inject-only`
4. 验证 `graph.html` 输出（JSON 合法性检查）
5. Git Commit + Push

### 9.2 数据 Pipeline 修改流程
1. 修改 `ai_radar_explorer.py` 采集/分析逻辑
2. 本地运行: `python3 ai_radar_explorer.py`
3. 验证 `graph.json`、`wiki/`、`graph.html` 输出
4. Git Commit + Push
5. 观察 Cron 下次执行结果

### 9.3 JSON 注入规则
```python
# ✅ 正确：使用 json.dumps 序列化
data_json = json.dumps(graph_data, ensure_ascii=False)
html = html_template.replace("{{DATA}}", data_json)

# ❌ 错误：直接嵌入格式化 JSON（包含控制字符）
data_json = json.dumps(graph_data, indent=2, ensure_ascii=False)
```

### 9.4 需求变更管理
- 所有需求变更需更新本文档 (版本递增)
- 前端需求 → 更新 Section 4
- 数据需求 → 更新 Section 3
- 定时任务 → 更新 Section 5
- 安全配置 → 更新 Section 6
- 需求清单 → 更新 Section 8

---

## 10. 技术栈

| 层级 | 技术 |
|------|------|
| **数据采集** | Python 3.10+, Requests, BeautifulSoup, ArXiv API |
| **智能分析** | DashScope qwen3.6-plus (coding endpoint) |
| **数据格式** | JSON, Markdown, JSONL |
| **前端渲染** | vis-network.js (本地化), Vanilla JS, CSS3 |
| **部署** | GitHub Pages (Static Hosting) |
| **定时任务** | Cron (Linux), Hermes Agent Cron Jobs |
| **消息推送** | Feishu/Lark Bot API |
| **版本控制** | Git, GitHub |

---

## 11. 文件索引

```
~/ai-radar-wiki/
├── graph.html              # 最终部署文件 (数据已注入)
├── graph_template.html     # 前端模板 (开发用, 含 {{DATA}} 占位符)
├── graph.json              # 图谱数据 (节点/边)
├── vis-network.min.js      # 本地化图谱渲染库
├── wiki/                   # Markdown 知识库
│   ├── entities/           # 实体页面 (GitHub/HN/TC 等)
│   └── concepts/           # 概念页面 (arXiv 论文)
├── daily-digest/           # 每日情报 Markdown
├── summary_archive/        # 每日摘要存档 (趋势分析用)
├── daily_summary.json      # 结构化每日深度分析
├── weekly_trends.json      # 周趋势分析结果
├── health_log.json         # 健康检查日志
├── feed.xml                # RSS 订阅 Feed
├── index.md                # Wiki 索引
├── README.md               # 仓库 README
├── .gitignore              # Git 忽略规则 (含 .env 防泄露)
└── DESIGN.md               # 本文档

~/.hermes/scripts/
├── ai_radar_explorer.py    # 数据采集 + 分析 + 注入脚本
├── ai_radar_sync.py        # 飞书同步脚本
├── generate_daily_summary.py  # 每日摘要生成器
├── weekly_trends.py        # 周趋势分析脚本
└── ai_radar_health_check.py   # 保活监控脚本

~/.hermes/.env              # 环境变量 (API Keys)
```

---

## 12. 变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v3.10.1 | 2026-05-08 | 前端设计文档对齐：`graph_template.html` 浅色主题、窄屏底栏与节点详情 Bottom Sheet、设计 Token、无障碍与 `prefers-reduced-motion`、RSS 弱强调与中文 HUD 等 |
| v3.10.0 | 2026-05-08 | 保活监控机制：健康检查脚本 + 自动恢复 + 停滞检测 + 告警阈值 |
| v3.9.1 | 2026-05-08 | 日/周视图切换修复：转义修复 + 事件绑定优化 + 零边距布局 |
| v3.9.0 | 2026-05-08 | Phase 2 趋势分析框架：周视图、叙事生命周期追踪、矛盾信号检测、摘要历史存档 |
| v3.7.0 | 2026-05-08 | UI/UX 重构 + 数据持久化修复：左侧面板去掉独立标题栏 + Sticky Headline + 竖向展开按钮 + 两侧面板高度对齐 + Header 移除收起按钮 + Star/Fork 按钮 + `build_graph_json()` 合并模式 + `daily_summary.json` 叙事主线深度分析 |
| v3.6.0 | 2026-05-08 | Schema 标准化 + 日报 Digest 数据源说明 |
| v3.5.0 | 2026-05-07 | 系统修复完成：中文摘要链路修复 + 每日摘要恢复 + 仓库清理 + pipeline 优化 |
| v3.4.0 | 2026-05-07 | 设计文档整合：汇总所有需求、修复、配置到 DESIGN.md + LLM API 配置 + 完整安全规范 |
| v3.3.0 | 2026-05-07 | Pipeline 修复：LLM 分析限制 30 条 + GitHub OR 查询拆分 + JSON 控制字符修复 + .gitignore + 模板自动提取 |
| v3.2.0 | 2026-05-07 | Linear 风格重构：面板撑满高度 + 内容重排 + 右侧详情增加来源/日期 + 摘要精炼版 vs 完整原文 |
| v3.1.0 | 2026-05-07 | 结构化摘要 + 图例跟随滑动 + 左侧面板改为 LLM 结构化摘要 |
| v3.0.0 | 2026-05-07 | UI 重构 + 订阅功能：仓库根目录整理 + 原文预览 + RSS Feed + 邮件订阅页面 |
| v2.0.0 | 2026-05-07 | 架构重构：模板分离 + 四象限分类 + 左侧仪表盘 + 右侧详情面板 + 图例恢复 + 节点圆形化 |
| v1.0.0 | 2026-05-06 | 初始版本：基础图谱 + 飞书集成 + Cron 任务 |
