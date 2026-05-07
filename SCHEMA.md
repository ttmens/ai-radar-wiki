# AI Radar Wiki — Schema (AI PM Focused)

## Domain
面向 AI 产品经理的知识库。
核心关注：**模型能力边界**、**产品形态演变**、**技术栈成熟度**、**商业化落地**。

## AI PM Knowledge System (4 Pillars)

### 1. 模型与技术能力 (Model & Tech Capabilities)
- 关注点：Context Window, Latency, Cost, Multimodal, Reasoning.
- 标签: `model`, `benchmark`, `inference`, `multimodal`, `agent`, `rag`, `fine-tuning`
- *PM 视角*: 能做什么？不能做什么？成本多少？

### 2. 产品与交互模式 (Products & Patterns)
- 关注点：Chat, Copilot, Agent Workflow, Background Automation.
- 标签: `pattern`, `ux`, `use-case`, `design-tool`
- *PM 视角*: 怎么把能力包装给用户？

### 3. 工具与生态 (Tools & Ecosystem)
- 关注点：Orchestration, VectorDB, Evaluation, Open Source vs Proprietary.
- 标签: `dev-tool`, `project`, `framework`, `evaluation`, `data`
- *PM 视角*: 用什么构建？有哪些坑？

### 4. 商业与趋势 (Business & Trends)
- 关注点：Funding, Moat, User Growth, Ethics, Regulation.
- 标签: `company`, `funding`, `policy`, `trend`, `comparison`
- *PM 视角*: 市场风向？护城河在哪里？

## Tag Taxonomy
### 核心分类
- `entity`: 具体对象 (Model, Project, Company)
- `pattern`: 产品模式 (e.g. "Text-to-Image", "Agent-in-loop")
- `metric`: 指标 (e.g. "Latency", "Cost per 1K tokens")

## Graph Format
知识图谱存储在 `graph.json` 中，包含 `pm_score` (PM 关注权重)。
```json
{
  "nodes": [
    {"id": "openai", "label": "OpenAI", "type": "company", "pm_score": 0.9, "tags": ["company", "model"]}
  ],
  "edges": [
    {"source": "openai", "target": "gpt-4", "relation": "developed", "type": "EXTRACTED", "pm_relevance": 0.8}
  ]
}
```
