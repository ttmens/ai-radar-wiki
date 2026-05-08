# 智瞰 NexSight · AI 产品设计雷达

**面向产品经理与构建者的 AI 全景情报站**——把散落的开源动态、论文、媒体与社区讨论，收成一张**可点击的知识图谱**，配上**中文摘要**与**PM 视角评分**，让你少刷十条信息流，多做一个靠谱决策。

[![在线图谱](https://img.shields.io/badge/打开-智瞰_NexSight_图谱-ff385c?style=for-the-badge)](https://ttmens.github.io/ai-radar-wiki/graph.html)
[![RSS](https://img.shields.io/badge/RSS-订阅情报-orange?style=flat-square)](https://ttmens.github.io/ai-radar-wiki/feed.xml)
[![设计文档](https://img.shields.io/badge/DESIGN-系统与前端规范-blue?style=flat-square)](DESIGN.md)

---

## 为什么是这个项目？

AI 领域的信息不是太少，而是**太碎、太快、太难对齐到「我该不该跟」**。NexSight 做的是三件事：

1. **收敛噪声** —— 多源采集（GitHub、论文、科技媒体、Hacker News 等），去重后进入同一条流水线。  
2. **翻译成人话** —— LLM 生成**中文摘要**、**四支柱分类**，并给出 **PM Score**（新颖度、影响力、相关性、时效性的综合信号，便于横向对比）。  
3. **连成地图** —— 不是列表页，而是 **vis-network 力导向图谱**：普通项目是圆点，概念聚合是六边形，颜色对应技术 / 模式 / 生态 / 商业四条主线。点一个节点，右侧（或手机上的底栏）直接看摘要、原文出处与相关情报。

你可以把它理解成：**给自己用的、自动更新的「AI PM 情报剪贴板 + 关系白板」**——数据在仓库里跑，页面在 GitHub Pages 上打开即用。

---

## 立刻体验

| 做什么 | 链接 |
|--------|------|
| **玩转图谱**（推荐从这里开始） | [graph.html — 智瞰 NexSight](https://ttmens.github.io/ai-radar-wiki/graph.html) |
| **订阅更新** | [feed.xml](https://ttmens.github.io/ai-radar-wiki/feed.xml) |
| **结构化今日情报** | [daily_summary.json](https://ttmens.github.io/ai-radar-wiki/daily_summary.json) |
| **原始图谱数据** | [graph.json](https://ttmens.github.io/ai-radar-wiki/graph.json) |
| **Wiki 条目索引** | [index.md](https://ttmens.github.io/ai-radar-wiki/index.md) |

> 节点数、边数与摘要覆盖率会随采集任务持续增长，**以线上图谱页顶栏 / HUD 显示为准**；本 README 不固定张贴易过期的数字。

---

## 你会得到什么能力？

- **今日情报面板**：叙事主线、分领域证据、日/周视图切换（趋势与矛盾信号等能力见 [DESIGN.md](DESIGN.md)）。  
- **节点详情**：摘要、来源域名、日期、类型、原文预览、一键跳转；同支柱下**相关情报**按分数排序。  
- **四支柱思维模型**：技术能力 · 产品模式 · 工具生态 · 商业动态 —— 和学校教科书里的分区无关，这是**产品研判用的坐标系**。  
- **离线也能逛**：核心前端零外部 CDN 依赖，适合归档与内网镜像（详见设计文档中的前端约束）。

---

## 适合谁读、谁用？

- **AI / 互联网产品经理**：追新工具、判模式、写调研、回老板「最近有什么值得看的」。  
- **技术负责人 & 架构师**：快速扫开源与论文动向，结合 PM Score 决定要不要深入读代码。  
- **独立开发者与创作者**：需要**持续选题**与**可信来源**，RSS + 图谱比纯订阅列表更立体。  
- **学习者**：想进 AI 产品/工程领域，需要一张**能缩放、能点、带中文解释**的全景图。

若你只做一件事：**打开 [图谱页](https://ttmens.github.io/ai-radar-wiki/graph.html)，点几个节点，再展开左下角情报摘要**——就能感受产品与数据的组合方式。

---

## 工作原理（一页纸）

```
信源采集  →  LLM 分析与结构化（中文摘要 / 分类 / PM Score）
         →  graph.json + wiki + 日报 JSON + RSS
         →  静态页面（graph.html）渲染图谱与面板
         →  （可选）飞书等渠道推送
```

流水线细节、数据源表、Schema、定时任务与健康检查等，全部收录在 **[DESIGN.md](DESIGN.md)**，适合二次开发与运维阅读。

---

## 仓库里有什么？

| 路径 | 说明 |
|------|------|
| `graph_template.html` | 前端模板（样式与脚本真源，含 `{{DATA}}` 占位符） |
| `graph.html` | 发布用页面（数据已注入，由生成脚本产出） |
| `graph.json` | 图谱节点与边 |
| `daily_summary.json` / `weekly_trends.json` | 日/周结构化摘要与趋势 |
| `wiki/` | 按实体与概念展开的 Markdown 知识页 |
| `feed.xml` | RSS 输出 |
| `DESIGN.md` | 系统设计、数据规范与**前端设计规范** |

---

## 开发与本地预览

1. 克隆本仓库。  
2. 静态预览：`python -m http.server 8080`，浏览器打开 `http://localhost:8080/graph.html`（若仅修改模板，可先测 `graph_template.html` 需自行注入数据或使用占位）。  
3. 数据生成与注入流程以 **DESIGN.md §9** 为准（Explorer / 注入规则等）。

---

## Star · Fork · 反馈

若 NexSight 帮你省下哪怕一小时的信息检索时间，欢迎 **Star** 本仓库；issue 与 PR 也开放给愿意改进数据源、提示词或前端体验的贡献者。

---

<p align="center">
  <b>智瞰 NexSight</b> — 全景趋势 · 决策情报<br/>
  <a href="https://ttmens.github.io/ai-radar-wiki/graph.html">打开图谱</a> · <a href="https://ttmens.github.io/ai-radar-wiki/feed.xml">RSS</a> · <a href="./DESIGN.md">设计文档</a>
</p>
