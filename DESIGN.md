# AI Radar 系统设计文档 (System Design Document)

> **版本**: v3.15.0  
> **最后更新**: 2026-05-13  
> **维护者**: Hermes Agent  

> **在线地址**: https://ttmens.github.io/ai-radar-wiki/ （简报） · [/graph.html](https://ttmens.github.io/ai-radar-wiki/graph.html) （探索）

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
│  brief_snapshot.json   │  （当日节点瘦数据，简报首页优先）  │
│  summary_archive/     │  health_log.json (健康日志)      │
└──────────────────────────┬──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    前端展示层 (Frontend)                  │
│  index.html (今日简报，Pages 默认 `/`)                    │
│  graph.html (探索) │ vis-network │ 左情报 / 右详情（桌面）  │
│  共用 site-chrome.css / site-chrome.js（顶栏·订阅·问答壳）   │
│  RSS·Star·Fork·统计 │ 概念=六边形 │ 窄屏：底 Tab + 情报 Sheet │
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

### 3.3 Explorer 执行顺序（v3.12.0 修复）

`ai_radar_explorer.py` 的 `main()` 函数按以下顺序执行：

```
1. batch_analyze_items(all_items)         — LLM 分析（翻译、分类、PM Score）
2. build_wiki_pages(all_items)            — 写入 wiki/entities/ 和 wiki/concepts/
3. build_graph_json(all_items)            — 合并新节点到 graph.json（保留历史数据）
4. generate_daily_summary.py              — 从 graph.json 读取今日节点生成日报
5. generate_graph_html(graph_data)        — 数据注入 graph_template.html → graph.html
6. update_index() / update_readme()       — 更新 Wiki 索引和 README
7. run_self_evolution()                   — 自我进化（更新旧 wiki 页面）
8. generate_daily_digest(all_items)       — 生成 daily-digest/ 目录的 Markdown 日报
9. save_state(state)                      — 保存采集状态（seen URLs、统计）
10. clean_old_raw(ttl_days=30)            — 清理 30 天前的原始数据文件
11. weekly_trends.py                      — 从 summary_archive 计算周趋势
```

**关键修复**（v3.12.0）：`generate_daily_summary.py` 必须在 `build_graph_json()` **之后**运行，因为它从 graph.json 中读取带有 `date` 字段的今日节点。之前顺序反了，导致日报读到的是旧 graph.json（无今日数据），输出 `total_items: 0`。

### 3.4 LLM 分析策略

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

### 3.5 数据 Schema

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

### 3.6 日报 Digest 数据源

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
- **LLM 模式**：跨节点综合研判（需 DashScope API key），参考 Stratechery 风格，生成动态叙事（基于当天真实数据，非硬编码模板）
- **Fallback 模式**：基于 8 种信号主题的自动模式识别，检测 4 种叙事类型
  - 🔄 范式转移、⚠️ 核心瓶颈、📈 行业成熟、💡 模式验证
- **LLM 输出去重**（v3.12.0）：`generate_daily_summary.py` 增加后处理去重层，按 `title|id` 键去重 LLM 返回的 evidence
- **Insight 去重**（v3.11.0）：每个叙事主线一对一分配到最佳匹配的 pillar（`assigned_narratives` 集合），避免多 pillar 重复相同文本
- **证据去重**（v3.11.0）：按 article title 去重（而非 ID），同一文章从不同来源产生时只保留一次
- **叙事生成**（v3.11.0 重大更新）：叙事正文不再使用硬编码模板，而是基于当天真实数据动态生成，引用实际证据项目名称和信号指标
- **f-string 转义修复**（v3.12.0）：`build_llm_prompt()` 中 `{narrative_title}` 转义为 `{{narrative_title}}`，防止 Python 当作变量解析导致 NameError

### 3.6 周趋势分析（Phase 2 - v3.9.0 新增）

**文件**: `weekly_trends.json` + `summary_archive/`

**功能**：
- **支柱趋势**：计算 4 大支柱的日环比变化（`delta`），标记趋势状态（`🔥 升温`/`➡️ 平稳`/`❄️ 降温`/`⚠️ 数据不足`）
- **叙事链追踪**：跨天匹配相同叙事标题，合并为"出现在 [日期列表]"的紧凑形式
- **矛盾信号检测**：识别同一天内相互矛盾的叙事（如"A 公司成功" vs "A 公司失败"）
- **叙事生命周期**：标记叙事阶段（`emerging`/`rising`/`hot`/`declining`）
- **叙事→证据匹配**（v3.11.0 重构）：每个叙事只关联到与其相关的证据，不再共享同一份证据

**叙事→证据匹配策略**（v3.11.0）：

1. **精确匹配**：如果 insight 文本以叙事标题开头（`insight.startswith(narrative_title)`），直接提取该 insight 的证据
2. **关键词重叠匹配**：计算叙事正文与 insight 文本的字符级重叠（中文分词不准确，使用字符集交集），取最佳匹配
3. **信号关键词 fallback**：维护叙事标题→信号关键词的映射表，匹配证据标题中的关键词
4. **去重**：按 article title 去重（同一文章从不同来源可能有不同 ID）

```python
# 匹配优先级
1. insight.startswith(narrative_title) → 直接提取
2. char_overlap(narrative_body, insight_text) > threshold → 最佳匹配
3. SIGNAL_THEMES_FALLBACK 关键词匹配 → fallback
4. 无匹配 → 证据列表为空（不强行关联不相关内容）
```

**数据结构**（v3.12.0 更新）：
```json
{
  "generated_at": "2026-05-10T04:59:56",
  "days_analyzed": 3,
  "pillar_trends": {
    "capabilities": {"trend": "stable", "delta": 0, "current": 0, "previous": 0, "has_data": false},
    "patterns": {"trend": "down", "delta": -1, "current": 2, "previous": 3, "has_data": true},
    "ecosystem": {"trend": "data_missing", "delta": -2, "current": 0, "previous": 2, "has_data": false},
    "business": {"trend": "down", "delta": -1, "current": 2, "previous": 3, "has_data": true}
  },
  "narrative_chains": [
    {
      "title": "AI从对话式向自主操作系统级控制演进",
      "type": "paradigm_shift",
      "latest_type": "paradigm_shift",
      "days": ["2026-05-08"],
      "instances": [{"date": "2026-05-08", "title": "...", "evidence": [...]}],
      "lifecycle": "emerging"
    }
  ],
  "contradictions": [
    {"date": "2026-05-08", "type": "growth_vs_risk", "description": "..."}
  ],
  "weekly_summary": "数据覆盖 **2026-05-08 至 2026-05-10**（3天），累计 **59** 条情报。..."
}
```

**叙事链字段说明**（v3.12.0 修复）：
- `latest_type`：叙事最新一次的类型（`paradigm_shift`/`bottleneck`/`maturation`/`validation`），v3.12.0 修复了创建时未初始化的 bug
- `lifecycle`：根据出现天数计算：1 天=`emerging`、≤3天=`rising`、≤7天=`hot`、>7天=`declining`
- `instances`：每天出现的具体实例，包含 date、title、body、type、evidence
- `days`：该叙事出现过的日期列表

**前端集成**：
- 日/周视图切换按钮（透明 tab 风格，固定在面板顶部）
- 周视图显示：支柱趋势状态、叙事链（去重后）、矛盾信号
- 点击"✕"关闭周视图，返回日视图

### 3.7 四象限分类体系 (4-Pillar Framework)
| Pillar | 中文 | 颜色 | 覆盖范围 |
|--------|------|------|----------|
| `capabilities` | 🤖 技术能力 | `#58a6ff` (蓝) | 新模型、算法、工具、技术突破、benchmark、安全研究、模型架构、神经网络、训练/推理 |
| `patterns` | 📱 模式/范式 | `#3fb950` (绿) | 新交互方式、工作流、AI 应用模式、Agent、Copilot、RAG、语音交互、多智能体 |
| `ecosystem` | 🔧 开发生态 | `#a371f7` (紫) | 框架、SDK、库、平台、开源社区、DevTool、CI/CD、版本控制、基础设施 |
| `business` | 💰 商业动态 | `#f0883e` (橙) | 融资、产品发布、公司战略、市场、裁员、数据泄露、反垄断、专利纠纷 |

**分类逻辑**（v3.11.0 优化）：
1. 关键词匹配：`classify_pillar()` 扫描文本匹配各 pillar 关键词
2. **capabilities 加权**：技术类关键词权重 ×1.2（避免被 business 的通用词覆盖）
3. 返回匹配数量最多的 pillar（加权后）

### 3.8 去重与缓存机制
- **URL 去重 Hash**: 持久化在 `state.json` 的 `seen` 数组，基于 URL MD5
- **标题去重**（v3.11.0 新增）：`build_graph_json()` 中增加 `seen_titles` 字典，同一文章因不同来源产生多个 entry 时，保留 score/star 最高的一个
- **重建机制**: `rebuild_seen_from_raw()` 从 `raw/` 目录重建去重 hash
- **LLM 缓存**: `llm_cache.json` 存储 LLM 分析结果，避免重复调用
- **raw/ TTL**: `clean_old_raw(ttl_days=30)` 自动清理 30 天前的原始文件

### 3.8.1 噪音过滤（v3.11.0 新增）

**问题**：TechCrunch 促销广告（"50% off"）、会议注册（"Register now"）、招聘等非情报内容混入数据。

**方案**：`is_noise()` 函数在采集后、去重前过滤：
```python
NOISE_PATTERNS = [
    "get 50% off", "discount", "early bird", "last day", "register now",
    "join us at", "coming to", "conference 2026", "summit 2026",
    "we're hiring", "job opening", "career opportunity",
    "ad:", "sponsored", "promoted",
    "newsletter:", "subscribe to", "sign up for",
]
```
过滤后统计输出：`{name}: {len(items)} found, {len(clean_items)} clean, {new_count} new`

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
| **移动端再上提一层** | 节点详情底栏（modal 层）阴影略重于情报底栏；顶栏 **「订阅」** 使用与其它 `header-btn` 一致的主按钮样式；RSS 仅在订阅面板的「进阶」项中链接 `feed.xml` |

### 4.3 页面布局（桌面 vs 移动）

**桌面（宽屏）** — 顶栏绝对定位，下方为图谱画布；**左侧情报**与**右侧节点详情**均为贴边侧栏（`position: absolute`），高度由 `--header-h`（JS 实测顶栏高度）与 `--side-sheet-from-top` / `--side-sheet-gap-bottom` 约束。

**移动（`max-width: 900px`）** — 布局切换为「地图 + 底栏」模式：

- **情报 ` #dashboard `**：贴屏幕**底**，高度约 **`60vh` / `60dvh`**，顶缘圆角；顶区 **拖条**可下滑收起（并可键盘 Enter/空格触发收起辅助）。**当前约定**：初次进入探索页时情报区 **默认收起**，图谱区 **全幅铺满**，避免 Bottom Sheet 抢占首屏。
- **`#dashboard-expand-btn`（情报摘要）**：右下 **FAB** 展开已收起的情报栏。定位：`bottom` 使用 `calc(var(--mobile-tab-bar-stack) + <间距>)`；**`z-index`** 高于底部 Tab Bar、低于订阅浮层（订阅约 **220** 量级，具体以 `site-chrome.css` 为准）。
- **节点详情 ` #detail-panel `**：自屏幕**底缘**上滑的 **Bottom Sheet**；关闭态使用 **`translate3d(0, 100dvh, 0)`**（辅 `100vh`）保证整页划入划出，避免 `translateY(100%)` 随内容高度变化导致抖动；**`#panel-scrim`** 在窄屏用 **opacity + visibility** 过渡，减少 `display` 切换导致的整页跳动。
- **顶栏**：单行横向滚动；**节点/边统计**迁入 **`#graph-stats-hud`** 浮层；顶栏右侧加 **极弱右侧内阴影** 提示「右滑还有更多操作」。**当前约定**：探索页顶栏 **已移除「摘要」按钮**（桌面与移动皆然）；打开情报统一走 **FAB**（及 Dashboard 拖条交互），与主导航 **底栏 Tab** 分工清晰。
- **底栏主导航（≤900px）**：顶栏 **pill** 在断点下由 **`site-chrome.js` / `site-chrome.css` 实现的 3 Tab 底栏**承接（简报 / 探索 / 问 AI），见 **4.9**。
- **图例 ` #legend `**：窄屏为顶栏下方的**横向滚动条**，不遮挡主图区。

### 4.4 核心 UI 组件（与实现对应）

#### 左侧情报（Dashboard / `.dash-content`）
- **Brief headline（`.brief-headline`）**：`position: sticky; top: 0; z-index: 100`，实心背景 + 底部分割，滚动时压住下方叙事卡片。
- **滚动容器**：`.dash-content` **顶部 padding 为 0**，避免 WebKit 下 sticky 与 padding 叠加出现正文「漏缝」；左右仍保留内边距。
- **首屏加载**：`.dash-skeleton` 骨架占位；若 `daily_summary.json` 失败而走 fallback，顶部 **`dash-data-banner`** 标明离线/基于图谱的摘要。
- **日/周切换**：`view-toggle` 分段控件（详见周趋势章节）。

#### 右侧详情（Detail Panel）
- **桌面**：从右侧 **`translateX(100%)` → `0`** 滑入，`z-index: 80`。**当前约定**：关闭态在 transform 之外保留 **额外水平外推（offset）**，避免 **面板阴影压在画布** 上；关闭控件与左侧情报 Sheet **统一为图标样式**（**`.dash-close-btn--icon`**），并注意选择器层叠：**`.dash-close-btn:not(.dash-close-btn--icon)`** 不得盖写图标按钮尺寸（详见 **4.9.6**）。
- **移动**：自底部滑入；章节标题为纯文字：**摘要总结 / 原文 / 相关情报**（主面板区去除装饰性 emoji，与高密度阅读场景一致）；主操作仍为「查看原文」「完整原文」。
- **遮罩**：移动开启详情时 **`#panel-scrim`** 可点按关闭，与 **`Escape`** 键一致；打开时 **`role="dialog"`**、窄屏 **`aria-modal="true"`**，焦点进入关闭按钮且 **`focus({ preventScroll: true })`**，避免移动端视口被焦点滚动带偏。

#### 无障碍与动效
- **`prefers-reduced-motion: reduce`**：`#dashboard`、`#detail-panel`、`#legend`、FAB、主要按钮等 **transition 近似关闭**；骨架 pulse 关闭。
- **订阅面板**：`#header-subscribe-btn` 打开 `#subscribe-panel`；**Escape** 与点击外部关闭。窄屏下面板为 **`position: fixed`**（`top: calc(var(--header-h) + 8px)`），避免顶栏 `overflow-x: auto` 裁切下拉层。

### 4.5 节点与边（vis-network）

| 属性 | 规则 |
|------|------|
| **普通节点** | `shape: 'dot'`，大小与 `pm_score`、类型相关 |
| **概念节点** | `shape: 'hexagon'`，尺寸与 `node_count` 相关，颜色按 pillar 略加深 |
| **颜色** | 与四支柱色一致（capabilities / patterns / ecosystem / business） |
| **字色** | 节点标签浅色描边以保证深背景上的可读性（见模板内 `font` 配置） |
| **边** | `BELONGS_TO`、PILLAR 等类型区分颜色与线宽 |

窄屏下图谱相机脚本会将簇心对齐到**顶栏与情报底栏之间的可视带**，避免节点被挡；**当前约定**：在 `network.fit` 之后再 **二次取景（reframe）**，使内容落在该段 **顶栏下缘 →（若展开）情报 Sheet 顶缘 / 或底部 Tab Bar 上缘** 之间的可视带；配合 **`applyMobileGraphCamera`**、对簇心 **略向上偏置**；**`toggleDashboard`**（展开/收起情报）后 **重新 fit / reframe**。vis-network 初始化宜设 **`improvedLayout: false`** 以减少移动端大幅位移。细节见 **4.9.5**。

### 4.6 顶栏（Header）控件

| 区域 | 内容 |
|------|------|
| 主导航 | **简报** `index.html` · **探索** `graph.html`（当前页 aria-current）。**桌面**：分段式 **pill** 放在 **品牌行左侧**，与简报首页同一 flex 行（品牌在右）。**移动（≤900px）**：顶栏 pill **替换为底部 3 Tab**（简报 / 探索 /「问 AI」占位），见 **4.9**；样式与脚本见 `assets/site-chrome.css`、`assets/site-chrome.js` |
| 品牌 | Logo（`nexsight-mark.svg`）+ **智瞰 NexSight** + 副标题 **面向产品经理的AI全景情报**（单行省略） |
| 订阅 | **「订阅」** 按钮（`.header-btn`），展开含收藏链接、GitHub Watch、**RSS（feed.xml）**、邮件/微信说明 |
| 统计 | 桌面：`N 节点` / `M 边`（中文）；窄屏：`#stats` 隐藏，由 HUD 展示 |
| GitHub | Star / Fork（窄屏可缩为图标优先级） |

### 4.7 技术约束（前端）

- **零外部依赖**：`vis-network.min.js` 等必须为本地化脚本
- **单页静态**：适合 GitHub Pages；**浅色主题**为当前默认（不再使用文档旧版所述 GitHub Dark 整块配色作为图谱页主界面）
- **安全区**：`env(safe-area-inset-*)` 参与顶栏、底栏、FAB、`--side-sheet-gap-bottom` 等
- **JSON 注入**：同 4.1，必须 `ensure_ascii=False` 且无非法控制字符

### 4.8 双页静态：简报首页与 Agent 占位

- **默认入口（GitHub Pages `/`）**：[`index.html`](index.html) — 中文「今日简报」：拉取 `daily_summary.json`、`weekly_trends.json`，以及优先 **`brief_snapshot.json`**（失败则回退完整 `graph.json` 并按 `daily_summary.date` 过滤当日非概念节点）。顶栏、订阅浮层与「问 AI」壳与探索页共用 [`assets/site-chrome.css`](assets/site-chrome.css)、[`assets/site-chrome.js`](assets/site-chrome.js)。
- **探索页**：[`graph.html`](graph.html) 仍由 [`graph_template.html`](graph_template.html) + `{{DATA}}` 生成；Cron/Explorer 中 `generate_graph_html()` 写回整页时**以模板为准**。
- **`brief_snapshot.json`**：由 [`scripts/generate_brief_snapshot.py`](scripts/generate_brief_snapshot.py) 从 `graph.json` 生成（北京时间**当日**、瘦字段、排除 `concept`），在 `ai_radar_explorer` 跑完 `weekly_trends` 后调用，减轻约 2MB 级 `graph.json` 在简报首屏的下载与解析压力。
- **问答（DeepWiki-open 范式）**：不在本仓库托管 RAG 后端。页面读取 `window.__NEXSIGHT_CONFIG__.agentIframeUrl`（可选）嵌入 iframe；**API 密钥不得入库**。未配置时展示中文说明占位。

### 4.9 产品信息架构与前端实现备忘（当前约定 · 2026-05-13）

本节从「产品决策 + 实现要点」收口 2026-05-13 会话中的约定，与上文 **4.3–4.8** 互补；技术流水线仍以 **第 3 节、第 6.4 节** 为准。

#### 4.9.1 信息架构与主路径

- **简报（`index.html`）** 与 **探索（`graph.html`）** 是两条 **主用例（primary modes）**：读当日结构化摘要 / 读图谱与情报仪表盘。
- **桌面**：主导航为 **分段 pill（简报 / 探索）**，置于 **品牌行左侧**，与首页 index **同一 flex 行**，避免与订阅、GitHub 星标争抢同一视觉优先级。
- **移动（≤900px）**：顶栏 **分段 pill 不再作为主导航**；改为 **底部 Tab Bar（3 Tab）**：简报、探索、以及「问 AI」入口位。

#### 4.9.2 响应式 Site Chrome（壳层）

- **顶栏容器**：`#header.site-chrome-header`，样式与交互共享 **`assets/site-chrome.css`**、**`assets/site-chrome.js`**（简报页与探索页一致）。
- **层叠**：顶栏 **`z-index`** **高于** 底部 Tab Bar，避免滚动或浮层时层次错乱；Bottom Sheet / 订阅等仍按各自规则压在内容之上。
- **堆叠高度变量**：`--mobile-tab-bar-stack` 汇总 **安全区 + Tab Bar 高度**，供 FAB `bottom`、`padding-bottom` 等统一计算。
- **安全区**：`env(safe-area-inset-*)` 参与顶栏、底栏与浮动控件（与 **4.7** 一致），避免刘海与 Home 条遮挡可点区域。

#### 4.9.3 「问 AI」与 Agent 面板（产品状态）

- **桌面**：顶栏「问 AI」入口 **全局隐藏**（不提供无效入口）。
- **移动**：底栏第三 Tab **禁用 + 灰色样式**，文案 **「即将开放」**；对 **`openPanel`** 及 Tab 切换须加 **guard**，避免打开未就绪的 Agent 壳。
- **FAB**：按产品策略，**桌面与窄屏均不展示**「问 AI」类 FAB（若未来再开放，需单独评审层级与 Tab Bar 关系）。
- **Agent 面板壳**：仍为 **DeepWiki 式 iframe 占位**；契约见 **4.8**（`agentIframeUrl`、无密钥入库）。后端接通前仅保留布局与关闭逻辑。

#### 4.9.4 探索页情报摘要（Dashboard）与 FAB（摘要入口）

- **当前约定**：探索页 **顶栏「摘要」按钮已移除**（不再在 graph 品牌行重复入口）；打开情报 **仅通过 `#dashboard-expand-btn` FAB**（及 Dashboard 自身拖条/手势）。
- **移动默认态**：情报 Bottom Sheet **默认收起**，保证 **全幅图谱**；FAB **固定定位**，`bottom` 为 **`calc(var(--mobile-tab-bar-stack) + gap)`**；**`z-index`** 高于 Tab Bar、**低于** 订阅相关浮层（约 **220**，以代码为准）。
- **`toggleDashboard`**：展开或收起后应对图谱 **重新 fit + mobile reframe**（见 **4.3** 与下条），避免「看不见选中节点」或簇心落在被挡区域。

#### 4.9.5 移动端图谱视口与相机

- 流程建议：**`network.fit`（或等价）→ 再执行 reframe**，使可见区域限制在 **顶栏以下、情报 Sheet 上缘或 Tab Bar 上缘以上** 的条带内。
- 使用 **`applyMobileGraphCamera`**（及簇心 **向上偏移**）将主簇置于 **可视带几何中心略偏上**，符合「地图优先」扫视。
- vis-network 配置：**`improvedLayout: false`**，减少移动端初始布局对自定义相机逻辑的干扰。

#### 4.9.6 节点详情面板（off-canvas / Sheet）

- **桌面**：详情 **off-canvas**；关闭态除 `translateX(100%)` 外增加 **额外外推 offset**，避免 **面板阴影压在画布** 上。
- **关闭按钮**：与左侧情报 Sheet **视觉统一**（**`.dash-close-btn--icon`**）；CSS 注意 **选择器顺序**：**`.dash-close-btn:not(.dash-close-btn--icon)`** 等规则不得覆盖图标按钮的圆形与尺寸。

#### 4.9.7 简报页（`index`）移动端滚动

- **滚动根节点**：**`main#brief-root`** 外包 **`.brief-shell`** 作为 **独立滚动容器**（与顶栏 / 底栏解耦）。
- **可选增强**：右下角 **小型圆形磨砂** 「上一段 / 下一段」按钮，**灰色 chevron**，在接近 **scrollTop / scrollBottom** 时 **渐隐**，减少长文跳转成本。

#### 4.9.8 主导航视觉与布局禁忌

- **分段 pill**：除静态高亮外，可采用 **滑动拇指（sliding thumb）** 增强「同一条控件」感知。
- **可选**：在支持的浏览器为 **跨页导航** 启用 **View Transitions API（meta / 脚本门控）**，使 thumb **在页面切换时连续**（降级无则忽略）。
- **禁忌**：**勿**在探索页品牌行对 **`h1` 使用 `flex: 1 1 auto`** —— 会把 **左侧分段导航** 挤到极右，破坏 **「导航在左、品牌在右」** 的定稿。

#### 4.9.9 UTF-8 与 Windows 工具链（产品风险）

- **根因**：Windows 默认代码页常为 **cp936**；PowerShell / CMD **重定向、`type`、`>`** 等易产生 **非 UTF-8 字节**，若不经 `encoding=utf-8` 写回，**`graph_template.html` / `graph.html`** 会出现 **声明与字节不一致**，线上表现为 **mojibake / 正则失灵**。
- **约定**：凡脚本读写 HTML、注入 JSON、patch 文案，**显式 `encoding="utf-8"`**（Python）或等价；避免依赖控制台默认编码。
- **仓库辅助工具**（按需使用）：
  - **`tools/restore_html_utf8_from_head.py`**：从 `<meta charset>` 声明方向修复落盘编码假设。
  - **`tools/check_graph_utf8.py`**：检查图谱相关 HTML 的 UTF-8 合法性。
  - **`tools/ensure_graph_js_regexes.py`**：内联 JS 正则与 **Unicode 字面量** 一致性（与周摘要解析器联动时尤须回归）。
  - **数据同步**：日常仍用 **`tools/inject_graph_data.py`**；模板大版本对齐时用 **`--from-template`**（遵守 **第 6.4 节**：自动化任务勿滥用）。
- **`parseWeeklySummaryText`（前端）**：正则中 **仅使用 `\\uXXXX` 类转义** 匹配中文标点等，**须与 `weekly_trends.py` 输出的 `weekly_summary` 字符串格式同步**；后端改文案格式 = **前端的解析契约变更**。

#### 4.9.10 数据层与 UI 变更边界

- **一般规则**：**纯 UI / CSS / 壳层脚本** 变更 **不要求** `graph.json`、Explorer、或 **第 6.4 节** 注入契约变更。
- **例外**：**周报摘要纯文本形态**（`weekly_trends.json` 中 `weekly_summary` 等）若发生句式、标点或结构化标记调整，**必须与** `parseWeeklySummaryText` **及正则约定一起评审**；**图数据 JSON 注入契约**（`#graph-data`、字段集合）**不变**，除非走完整 Pipeline 评审与版本记录。

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
| `ai-radar-daily-article` | 每日 19:00 | 公众号日报生成（WeChat HTML + 飞书文档） | 飞书文档（用户手动发布到公众号） | ✅ 运行中 |
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

### 5.3 公开访客订阅方式（RSS 与其它渠道）

- **背景**: RSS 对非技术用户不友好；静态站无账号系统，「订阅」需拆成多种低门槛入口。
- **站内实现**（`graph.html` / `graph_template.html`）:
  - 顶栏 **「订阅」** 浮层：**复制本页链接**、书签/「添加到主屏幕」说明、**GitHub Watch** 说明与入口、`feed.xml` 链接（RSS，进阶）、邮件/微信说明指向本文档。
  - **RSS** 入口并入「订阅」面板，不再单独占用顶栏（减少按钮数量）。
- **可选扩展**（需运营或第三方，不改动核心数据管线也可逐步上线）:
  | 方式 | 说明 |
  |------|------|
  | **邮件简报** | 通过 Formspree、Resend、Buttondown、MailerLite 等托管表单或 API 收集邮箱；Cron 或手工转発摘要链接。**密钥与 endpoint 不得写入仓库**。 |
  | **微信公众号** | 菜单/自动回复/推文放 `graph.html` 或定制域名；内容由运营维护，本站仍为静态页。 |
  | **Telegram Channel** | 每日转发 `feed.xml` 或早报链接，适合跨境读者。 |
  | **飞书** | 与第 5.1 节已存在之群内推送同源，面向团队而非匿名访客。 |

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
- **图谱页数据写入（强制）**: 更新 `graph.html` 内图数据时，须使用仓库 **`tools/inject_graph_data.py`** 所实现的「**仅替换 `#graph-data` 内联 JSON**」方式，或与该脚本**逐行等价**的逻辑；详见 §6.4

### 6.4 graph.html 注入规范（防「同步任务覆盖」线上 UI）

#### 根因说明

- **现象**: GitHub Pages 上 `graph.html` 的交互/UI 在 Cron 自动同步后**反复回退**，与本地或历史修复（如 **debd0e5**「仅更新内联 JSON、保留 graph.html 自定义 UI / 周视图逻辑」）不一致。
- **原因**: Hermes 侧 `generate_graph_html()` 若仍采用 **`graph_template.html` 读入 → `{{DATA}}` 替换 → 整文件覆盖写入 `graph.html`**，则：
  1. 任何**仅存在于** `graph.html`、尚未合并进 `graph_template.html` 的 JS/CSS 改动会被**抹掉**；
  2. 若模板版本**落后于** `graph.html`，每次 **auto-sync / explorer** 推送都会在远程复现「回退」。
- **结论**: **禁止**用模板整页覆盖已作为线上壳的 `graph.html`；**唯一安全的常规更新**是替换 **`<script id="graph-data" type="application/json">…</script>`** 内部的 JSON 正文。

#### 规范（Hermes / 本地必须遵守）

1. **默认路径**（`graph.html` 已存在且含 `id="graph-data"`）  
   - 从 `graph.json` 序列化 JSON（`json.dumps(..., ensure_ascii=False, separators=(',', ':'))`，见 §9.3），经 **非法控制字符清理**（避免内联脚本解析失败，参见 **95f10bb** 一类问题）后，**仅替换**上述 script 标签内文本，**其余字节不动**。  
   - 仓库提供可直接调用的参考实现：**`tools/inject_graph_data.py`**（支持 `--wiki-root`、`--dry-run`；推送前若刚改完模板、需要让 `graph.html` 与 **`graph_template.html` 完全对齐**，可本地执行一次 **`--from-template`**，仍由 `graph.json` 写入 `{{DATA}}`；**定时任务 / Hermes 日常同步不得使用该标志**，应继续用默认「仅替换 `#graph-data`」）。

2. **Hermes 集成方式（二选一）**  
   - **推荐**: `generate_graph_html()` 内 `subprocess.run` 调用  
     `python3 ~/ai-radar-wiki/tools/inject_graph_data.py --wiki-root ~/ai-radar-wiki`  
     便于与仓库行为锁定、可 diff。  
   - **或**: 将 `inject_graph_data.py` 中 `inject_into_html` / `load_graph` 逻辑**内联**到 `ai_radar_explorer.py`，并保持与仓库脚本**行为一致**（评审时对照 diff）。

3. **仅当 `graph.html` 不存在或缺少 `#graph-data` 时**  
   - 允许**一次性**由 `graph_template.html` + `{{DATA}}` 生成首版 `graph.html`；之后长期仍须走 §6.4 规范 1。

4. **防漂移**  
   - 所有面向用户的 UI/逻辑修改应**优先写入 `graph_template.html`**，推送前在仓库根执行 **`python3 tools/inject_graph_data.py --from-template`**，使 `graph.html` 与模板一致、数据来自 `graph.json`。  
   - **自动化任务不得**使用 `--from-template`，也不得用旧模板整页覆盖线上壳；日常仍只替换 JSON（规范 1）。

#### 验收（deploy / 改 explorer 后）

- 在仓库执行: `python3 tools/inject_graph_data.py --dry-run` 应返回 0。  
- grep `generate_graph_html`：确认无「仅用 `graph_template` 整页写 `graph.html`」且未 `git pull` 最新模板的分支路径。

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
- [x] graph.json 标题去重（v3.11.0）
- [x] 噪音过滤层：is_noise() 过滤促销/招聘/会议广告（v3.11.0）
- [x] 叙事生成动态化：从硬编码模板改为基于真实数据生成（v3.11.0）
- [x] 叙事→证据精确匹配：4 层匹配策略（v3.11.0）
- [x] evidence 按 title 去重（v3.11.0）
|- [x] Pillar 分类优化：capabilities 关键词扩展 + ×1.2 权重（v3.11.0）
|- [x] 日报执行顺序修复：`generate_daily_summary` 移到 `build_graph_json` 之后（v3.12.0）
|- [x] `build_llm_prompt` f-string 转义修复（v3.12.0）
|- [x] `generate_daily_summary` 后处理去重层（v3.12.0）
|- [x] `weekly_trends` 叙事链 `latest_type` 初始化修复（v3.12.0）
| - [x] 公众号日报系统（v3.13.0）：`wechat_article.py` 生成 WeChat HTML + 飞书文档

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
- [ ] **图谱页加载性能优化**（见 §8.2.1：分阶段、明确风险；**勿在未评审前改动数据注入契约**，以免 Explorer / GitHub Pages / 定时任务链路异常）

### 8.2.1 图谱页加载性能优化（待实现 · 方案与修改建议）

> **背景**：`graph.html` 内联约 1MB 级 `{{DATA}}` + 同步 `JSON.parse`，`init()` 串行等待 `daily_summary.json` 与 `weekly_trends.json`，且 fetch 使用 `?t=Date.now()` 导致缓存失效；`<head>` 对整页 `no-cache`。上述组合拉长首屏可交互时间（TTI）。**下列方案按风险分层**：可先落低风险纯前端项；涉及「数据接口 / 注入方式 / graph.json 形态」的须与 `ai_radar_explorer.py`、回滚策略一并评审后再做。

#### 现状摘要（便于对齐）

| 因素 | 说明 |
|------|------|
| 内联图数据 | 与 `graph.json` 同量级 JSON 嵌入 HTML，首包大；`JSON.parse` 占用主线程 |
| 初始化顺序 | `renderStructuredSummary()` → `loadWeeklyTrends()` → `renderNetwork()` 串行；图谱与摘要无硬依赖 |
| 缓存 | `daily_summary` / `weekly_trends` 请求带时间戳查询参数，难以命中浏览器缓存 |
| 整页缓存策略 | `no-cache` / `no-store` 使 HTML 难以复用；静态资源（如 `vis-network.min.js`）可独立长缓存 |
| 节点体积 | `raw_content` 与 `summary` 等并存，放大 JSON；详情面板可改为按需加载以瘦身 |

#### P0 — 低风险（**不改数据文件形态、不改 Explorer 注入契约**）

仅改 `graph_template.html` / 同步到 `graph.html`，本地与 Pages 验证通过后上线。

1. **并行化 `init()`**  
   - **建议**：`Promise.all([renderStructuredSummary(), loadWeeklyTrends()])` 与 `renderNetwork()` **并行**，或 **先调用 `renderNetwork()`**，左栏摘要用骨架/占位后异步填充。  
   - **目的**：消除「等两轮 fetch 才画图」的瀑布。  
   - **注意**：若周视图首次渲染依赖 `weeklyTrends`，需确认 `renderStructuredSummary` 内对 `weeklyTrends` 的引用顺序；必要时「日视图先出、周视图切换时再拉/再渲染」。

2. **弱化 fetch 缓存穿透**  
   - **现状**：`'./daily_summary.json?t=' + Date.now()`（周趋势同理）每次唯一 URL。  
   - **建议**：改为 **`?v=<构建版本>`**（由 Explorer 注入或令与 `graph.json` 同次 commit 的短 hash）、或去掉查询参数依赖 **ETag/Last-Modified**（依赖托管对 JSON 的响应头）。  
   - **目的**：重复访问命中磁盘/HTTP 缓存，**不改变 JSON 路径与内容契约**。

3. **分层缓存 meta（可选）**  
   - **建议**：HTML 可维持较短 revalidate；对 **`vis-network.min.js`、`feed.xml`、版本化后的 `graph.json`**（若未来外置）使用 **长 `max-age` + 文件名/查询参数版本号**。  
   - **目的**：减少重复下载脚本与子资源。

#### P1 — 中风险（**可能触碰「页面如何拿到图数据」；须回归 Explorer 与注入脚本**）

实施前在分支上完整跑通：`inject-only`、全量 explorer、GitHub Pages 预览、Hermes Cron 推送。

1. **图数据外置 + 轻量壳页**  
   - **建议**：HTML 仅保留壳与脚本；运行时 **`fetch('./graph.json')`**（或与站点同源的压缩格式，若托管支持）。注入脚本改为 **不写内联 JSON** 或 **双模式**（内联/外置开关，便于灰度）。  
   - **收益**：首包缩小、下载可与脚本解析并行；可单独缓存 `graph.json`。  
   - **风险**：首屏白屏时间取决于二次请求；需错误处理与 CORS/路径一致性；**须更新 `generate_graph_html()` 与文档 §9.3**。

2. **主线程减负**  
   - **建议**：大块 `JSON.parse` 或 DataSet 构建放入 **Web Worker**（或分片 `parse`），主线程只做 `postMessage` 结果挂载。  
   - **风险**：与 vis-network 的数据结构对接、调试复杂度上升。

#### P2 — 高收益 / 高改动（**Pipeline + 前端契约**）

1. **「列表图」与「详情」分离**  
   - **建议**：生成 **`graph-lite.json`（或裁剪字段的 `graph.json`**）：布局与列表所需字段保留；**去掉或缩短 `raw_content`**。用户打开节点详情时再 **`fetch`** 单页 Markdown/JSON（如 `wiki/entities/xxx.md` 或专用 API）。  
   - **收益**：显著降低传输与 parse 成本。  
   - **风险**：`showPanel` / 离线打开逻辑须改；Explorer `build_graph_json` 需增加产物或裁剪步骤；**必须**端到端测试。

2. **vis-network 按需加载**  
   - **建议**：首屏后用动态 `import` 或 `defer` 脚本chunk再 `renderNetwork`。  
   - **风险**：首屏闪烁、加载失败重试；弱网体验需设计。

#### 验收建议（任一发版）

- Lighthouse / Performance：FCP、TTI、Main-thread 时间；弱网 3G 节流  
- 冷启动与**二次进入**（验证缓存策略）  
- 左侧摘要 / 周视图 / 节点详情 / RSS 链接无回归

### 8.3 已知问题/限制 ⚠️
- 飞书 API 无法创建文件夹和删除文档
- GitHub Pages 屏蔽外部 CDN，必须本地化所有依赖
- LLM 分析有 Token 成本，已控制频率（Top 30 + 缓存）
- DashScope coding 端点仅支持 `qwen3.6-plus`，标准端点 Key 无效
- 浏览器截图环境中文字体缺失（显示为方块），但实际访问正常
- **Pillar 趋势仅对比最后两天**：当某天缺少某 pillar 的 insight 时，会显示"平稳"或"数据不足"。这是"最后两天对比"的设计取舍，不是 bug
- **叙事链跨天连接率较低**：每天叙事标题用词差异大，模糊匹配要求 >50% 词重叠，目前 9 条叙事链均为 `emerging`（单天）。数据积累后叙事标题趋同会自然改善
- **Fallback 模式叙事**：LLM 失败时 fallback 生成的叙事正文较模板化，不如 LLM 模式深度

---

## 9. 开发规范 (Development Guidelines)

### 9.1 前端修改流程
1. 修改 `graph_template.html` (纯 HTML/CSS/JS)
2. 本地测试: `cd ~/ai-radar-wiki && python3 -m http.server 8080`
3. 运行数据注入: `python3 tools/inject_graph_data.py`（或 Hermes 等价逻辑）；勿用整页模板覆盖 `graph.html`（§6.4）
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
data_json = json.dumps(graph_data, ensure_ascii=False, separators=(',', ':'))
html = html_template.replace("{{DATA}}", data_json)

# ✅ graph.html 已存在时：禁止整页覆盖；应只替换 #graph-data 内联 JSON（见 §6.4、tools/inject_graph_data.py）
# html = inject_into_html(existing_graph_html, data_json)

# ❌ 错误：直接嵌入格式化 JSON（包含控制字符）
data_json = json.dumps(graph_data, indent=2, ensure_ascii=False)
```

### 9.4 需求变更管理
- 所有需求变更需更新本文档 (版本递增)
- 前端需求 → 更新 Section 4（产品与壳层、当前约定汇总见 **4.9**）
- 数据需求 → 更新 Section 3
- 定时任务 → 更新 Section 5
- 安全配置 → 更新 Section 6
- 需求清单 → 更新 Section 8
- 图谱页性能与缓存策略 → 更新 Section 8.2.1（**动数据契约须与 Explorer/注入流程一并评审**）

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
├── tools/
│   └── inject_graph_data.py  # 仅替换 graph.html 内 #graph-data JSON（防 Cron 覆盖 UI）
├── vis-network.min.js      # 本地化图谱渲染库（或见 assets/）
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
├── ai_radar_explorer.py       # 数据采集 + 分析 + 注入（每6h）
├── ai_radar_sync.py           # 飞书 Bitable/云文档同步（每日06:00）
├── ai_radar_health_check.py   # 健康监控 + 自动恢复（每4h）
├── generate_daily_summary.py  # 每日深度分析摘要（explorer 子流程）
├── weekly_trends.py           # 周趋势分析（explorer 子流程）
├── generate_rss.py            # RSS Feed 生成（每4h）
├── wechat_article.py          # 公众号日报 HTML 生成（每日19:00）
├── bitable_sync.py            # Bitable 数据写入（sync 子模块）
├── feishu_bitable_writer.py   # 飞书 Bitable 写入器
├── feishu_push.py             # 飞书文档推送
├── extract_concepts.py        # 概念节点提取
├── reorganize_feishu.py       # 飞书文档结构重组
├── reorganize_radar.py        # Radar 数据重组
├── wiki_maintainer.py         # Wiki 维护工具
└── ai_radar_explorer.py.bak   # Explorer 备份（不追踪）

~/.hermes/.env              # 环境变量 (API Keys)
```

---

## 12. 变更日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v3.15.0 | 2026-05-13 | **产品与前端设计文档**：① 新增 **4.9**（信息架构、Site Chrome、问 AI 状态、Dashboard/FAB、移动相机、详情面板、简报滚动、导航视觉、UTF-8 工具链、数据/UI 边界）② **4.3 / 4.4 / 4.5 / 4.6** 与 **当前约定** 对齐（探索页顶栏摘要移除、相机 / z-index / 关闭按钮）③ 第 5.3 节表格去除「§」前缀写法 |
| v3.13.1 | 2026-05-12 | **Bug 修复**：① build_graph_json 日期归一化新增 RFC2822 格式支持（TechCrunch RSS pub_date 导致 8 个节点 date 格式异常） ② health_check vis-network 路径检查覆盖根目录+assets/ |
| v3.13.0 | 2026-05-12 | **定时任务与脚本归档**：① §5.1 补充 `ai-radar-daily-article`（公众号日报） ② §11 文件索引补全全部14个脚本及说明 ③ `~/.hermes/scripts/` 全量推送到 Git（13个新文件） |
| v3.12.4 | 2026-05-11 | **UI**：顶栏「跟进」改为「订阅」、移除独立 RSS 按钮（RSS 留在订阅面板）；订阅按钮与顶栏 `header-btn` 统一样式；窄屏订阅面板改为 `fixed` 避免被顶栏横向滚动裁切 |
| v3.12.3 | 2026-05-11 | **跟进/订阅**：顶栏「跟进」浮层（复制链接、GitHub Watch、RSS、邮件/微信说明）；DESIGN §5.3 列可选邮件/公众号/Telegram 等扩展路径 |
| v3.12.2 | 2026-05-11 | **防覆盖**: 新增 `tools/inject_graph_data.py`（仅替换 `graph.html` 内 `#graph-data` JSON）；新增 §6.4 说明 debd0e5 根因与 Hermes `generate_graph_html` 强制规范 |
| v3.12.1 | 2026-05-11 | **文档**：§8.2 新增「图谱页加载性能优化」待办；新增 §8.2.1（分 P0/P1/P2 的修改建议、风险与验收；**明确不得在未评审前擅自改数据注入契约**） |
| v3.12.0 | 2026-05-10 | **Pipeline 执行顺序 + Bug 修复**：① `generate_daily_summary` 移到 `build_graph_json` 之后（解决日视图数据为空） ② `build_llm_prompt` f-string `{narrative_title}` 转义修复 ③ `generate_daily_summary` 增加 LLM 输出后处理去重层 ④ `weekly_trends` 叙事链 `latest_type` 初始化修复 ⑤ 数据状态：329 节点，3053 边，3 天摘要存档 |
| v3.11.1 | 2026-05-09 | **graph.html 模板注入修复**：① generate_graph_html() 优先使用 graph.html 并仅替换内嵌 JSON，不再用 graph_template.html 覆盖自定义 UI ② 恢复周视图全部功能（view-toggle、叙事卡片、折叠功能） ③ 数据同步到最新 graph.json（318 节点，2738 边） |
| v3.11.0 | 2026-05-09 | **叙事→证据全链路修复**：① 叙事生成从硬编码模板改为动态生成（引用当天真实数据） ② 叙事→证据精确匹配（4 层策略：精确匹配→字符重叠→信号关键词→无匹配） ③ 证据按 title 去重（解决同文章多 ID 问题） ④ graph.json 标题去重（341→310 节点） ⑤ Pillar 分类优化（capabilities 关键词库扩展 + ×1.2 权重） ⑥ 噪音过滤层（is_noise 过滤促销/招聘/会议广告） ⑦ narrative→pillar 1:1 分配（assigned_narratives 集合） |
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
