# AI Radar 4层聚合架构升级实施计划

> **版本**: v1.0  
> **制定日期**: 2026-05-08  
> **目标**: 从 Data→Insight 两层架构升级为 Data→Information→Knowledge→Insight 四层架构  
> **总周期**: 预计 4-6 周（分 5 批次执行）

---

## 📐 总体架构对齐

### 当前架构（2层）
```
L1: 原始节点 (graph.json nodes)
  ↓ 直接聚合
L4: 日报/周报 (daily_summary, weekly_trends)
```

### 目标架构（4层）
```
L1: Data (数据层) - raw/, graph.json 原始节点
  ↓ 聚类、关联、标签化
L2: Information (信息层) - 概念节点、实体 Hub、模式库、关系图谱
  ↓ 趋势计算、基线对比、成熟度评估
L3: Knowledge (知识层) - concept_trends.json, hype_cycle, pattern_evolution
  ↓ 叙事绑定、机会/风险评估、决策矩阵
L4: Insight (洞察层) - daily_summary, strategic_radar, decision_matrix
```

---

## 📅 批次执行计划

### 🟢 Batch 1: L2 概念提取与关联 (第 1-2 周)
**目标**: 建立概念节点体系，实现项目→概念的自动映射

| 维度 | 详情 |
|------|------|
| **范围** | Explorer 脚本修改、graph.json Schema 扩展、前端概念节点渲染 |
| **技术方案** | LLM prompt 增加 concept 提取、新增 `type: "concept"` 节点、`BELONGS_TO` 边 |
| **交付物** | `concept_extractor.py`, 更新的 `graph.json`, 前端概念聚类视图 |
| **验收标准** | 100% 新节点自动关联 2-3 个概念；概念节点可在图谱中可视化；点击概念可下钻关联项目 |
| **风险评估** | LLM 概念提取一致性差 → 增加概念词典约束 + 关键词降级兜底 |

#### 详细任务清单
1. **Schema 设计** (2h)
   - 定义概念节点字段：`id`, `label`, `type: "concept"`, `pillar`, `related_nodes[]`, `first_seen`, `last_seen`, `node_count`, `avg_pm_score`
   - 定义新边类型：`BELONGS_TO` (项目→概念), `RELATED_TO` (概念→概念)

2. **LLM Prompt 改造** (4h)
   ```python
   # 原有返回
   {"pillar": "capabilities", "summary": "...", "pm_score": 0.65}
   
   # 新增返回
   {
     "pillar": "capabilities",
     "summary": "...",
     "pm_score": 0.65,
     "concepts": ["AI Memory", "Long-term Context"],
     "entities": ["MemPalace"],
     "patterns": ["Benchmark-driven Development"]
   }
   ```

3. **Explorer 脚本修改** (6h)
   - `analyze_item_llm()` 解析新增字段
   - `build_graph_json()` 增加概念节点合并逻辑
   - `build_wiki_pages()` 增加概念页面生成

4. **前端概念视图** (8h)
   - 概念节点样式：六边形 (`shape: 'hexagon'`)，颜色与 pillar 一致
   - 点击概念节点：右侧面板显示关联项目列表（按 PM Score 排序）
   - 图例增加概念节点说明

5. **测试与验证** (4h)
   - 本地运行验证概念提取准确率
   - 前端验证概念节点渲染和交互
   - Git 推送

**预计工时**: 24h | **里程碑**: M1 - 概念体系上线

---

### 🔵 Batch 2: L3 趋势指标计算 (第 3 周)
**目标**: 为概念建立时间序列指标，实现热度追踪和成熟度评估

| 维度 | 详情 |
|------|------|
| **范围** | 趋势计算脚本、concept_trends.json、成熟度规则引擎 |
| **技术方案** | 基于 summary_archive 滑动窗口计算、Gartner 曲线映射规则 |
| **交付物** | `calculate_concept_trends.py`, `concept_trends.json`, 成熟度标签系统 |
| **验收标准** | 每个概念有 7/30 天热度曲线；自动打标成熟度阶段；前端可展示趋势 |
| **风险评估** | 数据不足导致趋势不准 → 增加"数据不足"标签，避免误导 |

#### 详细任务清单
1. **趋势数据结构设计** (2h)
   ```json
   {
     "concept_id": "ai-memory",
     "label": "AI Memory",
     "metrics": {
       "7d": {"node_count": 5, "avg_pm": 0.62, "delta": 2, "trend": "rising"},
       "30d": {"node_count": 12, "avg_pm": 0.58, "delta": 7, "trend": "rising"},
       "90d": {"node_count": 12, "avg_pm": 0.58, "delta": 12, "trend": "stable"}
     },
     "maturity": "growth",  // early/growth/mature/declining
     "hype_phase": "peak_inflated",  // innovation_trigger/peak_inflated/trough_disillusionment/slope_enlightenment/plateau_productivity
     "updated_at": "2026-05-08"
   }
   ```

2. **趋势计算脚本** (6h)
   - 从 `summary_archive/` 读取历史数据
   - 计算滑动窗口指标（7/30/90 天）
   - 实现趋势判断逻辑（rising/stable/declining）
   - 输出 `concept_trends.json`

3. **成熟度规则引擎** (4h)
   - 节点数阈值：`<5` = early, `5-20` = growth, `20-50` = mature, `>50` = declining (需结合 delta)
   - PM Score 趋势：连续上升 → growth, 连续下降 → declining
   - Gartner 曲线映射：基于成熟度 + 热度组合判断

4. **Cron 集成** (2h)
   - 新增 `ai-radar-concept-trends` cron 任务（每日 07:00 运行）
   - 与 explorer 和 daily_summary 执行顺序协调

5. **前端趋势展示** (6h)
   - 概念节点详情页增加趋势卡片
   - 热度曲线可视化（简易 CSS 条形图）
   - 成熟度标签显示

**预计工时**: 20h | **里程碑**: M2 - 趋势体系上线

---

### 🟣 Batch 3: L4 洞察升级 (第 4 周)
**目标**: 基于 L2/L3 数据升级日报/周报生成逻辑，增加机会/风险雷达

| 维度 | 详情 |
|------|------|
| **范围** | daily_summary.py 改造、strategic_radar.json、机会/风险评估模型 |
| **技术方案** | 从"扫描节点"改为"扫描概念变化"，基于规则的机会/风险识别 |
| **交付物** | 升级的 `daily_summary.json`, `strategic_radar.json`, 飞书推送模板 |
| **验收标准** | 日报包含概念趋势洞察；机会/风险雷达可量化；飞书推送结构化 |
| **风险评估** | 洞察过于抽象 → 增加"证据链"下钻，确保每个观点可追溯 |

#### 详细任务清单
1. **日报生成逻辑改造** (6h)
   - 原逻辑：扫描当日所有节点 → LLM 生成摘要
   - 新逻辑：扫描 concept_trends.json 变化 → 识别显著变化 → 生成洞察
   - 示例输出：
     ```
     🔥 升温概念：AI Memory (7d 新增 3 项目，PM Score 0.65↑)
        - MemPalace: 开源记忆系统 (PM 0.63)
        - Mem0 v2: 多模态记忆 (PM 0.71)
        - Letta: 分层记忆架构 (PM 0.58)
     ```

2. **机会/风险雷达模型** (4h)
   ```python
   # 机会识别规则
   opportunity = (
       heat_index > 7.0 and  # 高热度
       node_count < 10 and   # 低竞争
       trend == "rising" and # 上升中
       contradiction_count == 0  # 无矛盾
   )
   
   # 风险识别规则
   risk = (
       heat_index > 8.0 and  # 极高热度
       contradiction_count > 2 and  # 多矛盾信号
       maturity == "peak_inflated"  # 期望膨胀期
   )
   ```

3. **strategic_radar.json 生成** (4h)
   ```json
   {
     "date": "2026-05-08",
     "opportunities": [
       {"concept": "Edge AI", "score": 8.5, "reason": "高热度低竞争，上升中"}
     ],
     "risks": [
       {"concept": "AI Agent Framework", "score": 7.2, "reason": "期望膨胀期，路线分歧大"}
     ],
     "watch_list": [...]
   }
   ```

4. **飞书推送模板升级** (2h)
   - 增加概念趋势卡片
   - 增加机会/风险雷达摘要
   - 保持 Stratechery 风格叙事

**预计工时**: 16h | **里程碑**: M3 - 洞察体系升级

---

### 🟠 Batch 4: 前端战略视图 (第 5 周)
**目标**: 新增"战略视角"Tab，整合 L2/L3/L4 数据为决策支持界面

| 维度 | 详情 |
|------|------|
| **范围** | graph.html 新增 Tab、机会/风险看板、概念对比视图 |
| **技术方案** | 前端 Tab 切换、数据可视化、交互优化 |
| **交付物** | 更新的 `graph_template.html`, 战略视图 UI |
| **验收标准** | 新增"🎯 战略"Tab；可筛选机会/风险；概念对比视图可用 |
| **风险评估** | 前端复杂度增加 → 保持与现有 UI 一致的暗色/Linear 风格 |

#### 详细任务清单
1. **Tab 架构改造** (4h)
   - 新增 `🎯 战略` Tab（与 `📅 情报` 并列）
   - 实现 Tab 切换逻辑和数据加载

2. **机会/风险看板** (6h)
   - 左侧：机会列表（按 score 排序，点击展开证据）
   - 右侧：风险列表（按 score 排序，点击展开矛盾信号）
   - 底部：watch_list（需持续关注的概念）

3. **概念对比视图** (6h)
   - 选择 2-3 个概念进行对比
   - 对比维度：热度趋势、节点数、平均 PM Score、成熟度、代表项目
   - 可视化：简易雷达图或条形对比图

4. **移动端适配优化** (4h)
   - 确保战略视图在窄屏下可用
   - 触摸手势支持

**预计工时**: 20h | **里程碑**: M4 - 战略视图上线

---

### ⚪ Batch 5: 自进化与优化 (第 6 周)
**目标**: 概念自动发现、关系自学习、系统健康度提升

| 维度 | 详情 |
|------|------|
| **范围** | 新概念自动创建、概念合并/分裂、系统性能优化 |
| **技术方案** | 概念聚类算法、同义词合并、缓存优化 |
| **交付物** | 自进化逻辑、性能优化报告、文档更新 |
| **验收标准** | 新概念自动创建准确率>80%；系统响应时间<2s；DESIGN.md 全面更新 |
| **风险评估** | 概念爆炸 → 设置概念数量上限 + 人工审核机制 |

#### 详细任务清单
1. **概念自动发现** (6h)
   - 基于关键词共现和 LLM 判断，自动创建新概念
   - 新概念需满足：≥2 个项目关联、PM Score>0.3

2. **概念合并/分裂** (4h)
   - 合并：相似度>0.8 的概念自动合并（如 "AI Memory" 和 "Machine Memory"）
   - 分裂：节点数>50 的概念按子主题分裂

3. **性能优化** (4h)
   - graph.json 大小控制（>1000 节点时自动归档旧节点）
   - LLM 缓存优化（概念分析结果缓存）
   - 前端渲染优化（虚拟滚动）

4. **文档与设计更新** (4h)
   - 更新 DESIGN.md 至 v4.0.0
   - 更新 README.md
   - 编写概念体系使用指南

**预计工时**: 18h | **里程碑**: M5 - 自进化体系上线

---

## 📊 时间表与里程碑

```
Week 1-2: [Batch 1] L2 概念提取与关联
  ├── M1: 概念体系上线
  └── 交付：concept_extractor, graph.json schema, 前端概念视图

Week 3:   [Batch 2] L3 趋势指标计算
  ├── M2: 趋势体系上线
  └── 交付：concept_trends.json, 成熟度标签, 趋势可视化

Week 4:   [Batch 3] L4 洞察升级
  ├── M3: 洞察体系升级
  └── 交付：daily_summary v2, strategic_radar.json, 飞书推送模板

Week 5:   [Batch 4] 前端战略视图
  ├── M4: 战略视图上线
  └── 交付：🎯 战略 Tab, 机会/风险看板, 概念对比视图

Week 6:   [Batch 5] 自进化与优化
  ├── M5: 自进化体系上线
  └── 交付：自动概念发现、合并/分裂、性能优化、文档更新
```

---

## 🔧 技术依赖与前置条件

| 依赖项 | 状态 | 说明 |
|--------|------|------|
| DASHSCOPE_API_KEY | ✅ 有效 | LLM 分析必需 |
| graph.json 合并模式 | ✅ 已实现 | v3.7.0 修复 |
| summary_archive | ✅ 已运行 | 2 天数据，需积累 |
| weekly_trends.py | ✅ 已实现 | Phase 2 基础 |
| 前端 v3.10.0 | ✅ 已部署 | 日/周视图、健康检查 |

---

## ⚠️ 风险控制与回滚策略

| 风险 | 影响 | 缓解措施 | 回滚方案 |
|------|------|----------|----------|
| LLM 概念提取不一致 | 概念节点混乱 | 增加概念词典约束 + 关键词降级 | 关闭概念提取，退回原有模式 |
| graph.json 过大 | 前端加载慢 | 节点数>1000 时自动归档 | 启用 compact 模式，隐藏旧节点 |
| 趋势计算不准确 | 洞察误导 | 增加"数据不足"标签 | 显示原始节点列表，隐藏趋势 |
| 前端复杂度增加 | 维护成本高 | 保持模块化设计，组件隔离 | 隐藏战略 Tab，退回原视图 |

---

## 📈 预期收益与衡量指标

| 指标 | 当前值 | 目标值 | 衡量方式 |
|------|--------|--------|----------|
| 信息密度 | 298 节点 / 566 边 | 50+ 概念节点 / 200+ 概念关系 | graph.json 统计 |
| 洞察可解释性 | 文本描述，难追溯 | 100% 洞察可下钻到证据链 | 用户测试 |
| 趋势准确率 | 无 | >85% (与人工标注对比) | 抽样验证 |
| 系统响应时间 | <3s (graph.html) | <2s (增加概念层后) | Lighthouse |
| 知识积累速度 | 一次性日报 | 概念节点持续增长 | 每周概念新增数 |

---

## 🚀 启动条件

- [x] DASHSCOPE_API_KEY 有效
- [x] graph.json 合并模式已实现
- [x] 前端 v3.10.0 已部署
- [ ] 确认 Batch 1 优先级（建议先执行）
- [ ] 分配执行时间窗口（建议非高峰时段）

---

**下一步**: 确认批次优先级和执行时间，开始 Batch 1 实施。
