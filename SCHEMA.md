# AI Radar Wiki — Schema

## Domain
AI 产品设计雷达知识库 — 追踪 GitHub 高星项目、arXiv 前沿论文、HackerNews 热点讨论、ProductHunt 新产品、AI 公司战略动态。

## Conventions
- 文件名：小写，连字符，无空格（如 `agent-framework.md`）
- 每个页面必须有 YAML frontmatter（见下）
- 使用 `[[wikilinks]]` 交叉引用（每页至少 2 个出站链接）
- 更新页面时必须 bump `updated` 日期
- 新页面必须添加到 `index.md` 对应分区
- 每个操作追加到 `log.md`
- 每条图谱边标注来源：`EXTRACTED`（直接提取）/ `INFERRED`（推断）/ `AMBIGUOUS`（模糊）

## Frontmatter
```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | timeline | query
tags: [来自下方分类体系]
sources: [raw/github/xxx.md]
---
```

## Tag Taxonomy
### 实体类
- `company` — AI 公司（OpenAI, Anthropic, 字节等）
- `project` — 开源项目/框架（LangChain, vLLM, Dify 等）
- `model` — AI 模型（GPT-4, Qwen, Llama 等）
- `person` — 关键人物

### 技术类
- `architecture` — 模型架构（Transformer, MoE, Diffusion 等）
- `agent` — Agent 框架/模式
- `rag` — RAG 相关
- `multimodal` — 多模态
- `inference` — 推理优化
- `training` — 训练/微调
- `data` — 数据集/数据处理

### 领域类
- `design-tool` — 设计工具
- `dev-tool` — 研发效能工具
- `funding` — 融资/投资
- `policy` — 政策/法规
- `research` — 学术研究

### 元标签
- `comparison` — 对比分析
- `timeline` — 时间线
- `trend` — 趋势分析
- `breakthrough` — 突破性进展

## Page Thresholds
- **创建页面**：实体/概念在 2+ 来源出现，或在 1 个来源中为核心内容
- **追加到现有页面**：来源提及已覆盖的内容
- **不创建页面**：仅一笔带过的次要内容
- **拆分页面**：超过 200 行时分拆为子主题+交叉引用

## Graph Format
知识图谱存储在 `graph.json` 中，格式：
```json
{
  "nodes": [{"id": "openai", "label": "OpenAI", "type": "company", "tags": ["company", "model"]}],
  "edges": [{"source": "openai", "target": "gpt-4", "relation": "developed", "type": "EXTRACTED", "evidence": "source file"}]
}
```
