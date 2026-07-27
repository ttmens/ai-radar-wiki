---
title: The Regression Tax: Decomposing Why Skills Help and Hurt LLM Agents
created: 2026-07-27
updated: 2026-07-27
type: concept
pillar: patterns
pm_score: 0.43
tags: ["research", "patterns"]
sources: ["raw/papers/the-regression-tax-decomposing-why-skills-help-and-hurt-llm-agents.json"]
---

# The Regression Tax: Decomposing Why Skills Help and Hurt LLM Agents

## 中文摘要
该论文提出“技能回归税”概念，揭示给LLM agent添加程序化技能时，平均成功率提升背后隐藏着部分任务性能下降的风险。通过在近6000次运行中对比有无技能的agent，发现技能可能“帮倒忙”，导致特定场景表现恶化。对产品经理而言，这提醒在构建AI agent功能时需谨慎评估技能引入的副作用，避免一味堆砌技能；而应通过细分场景、动态调整或混合策略来平衡技能收益与损失。该研究为agent技能设计提供了重要的权衡视角，尤其适用于办公自动化等复杂任务场景。

## PM 关注指标
- 🎯 PM Score: 0.43
- 🏷️ Pillar: patterns
- 🔑 Keywords: agent, rag

## 作者
Darshan Tank, Baran Nama

## 摘要
Adding procedural skills to an LLM agent is typically evaluated by average improvement in task success. However, this metric hides an important cost: skills can also make agents worse. We measure both sides by comparing agents with and without skills across nearly 6,000 runs spanning two office auto...

## 中文摘要
该论文提出“技能回归税”概念，揭示给LLM agent添加程序化技能时，平均成功率提升背后隐藏着部分任务性能下降的风险。通过在近6000次运行中对比有无技能的agent，发现技能可能“帮倒忙”，导致特定场景表现恶化。对产品经理而言，这提醒在构建AI agent功能时需谨慎评估技能引入的副作用，避免一味堆砌技能；而应通过细分场景、动态调整或混合策略来平衡技能收益与损失。该研究为agent技能设计提供了重要的权衡视角，尤其适用于办公自动化等复杂任务场景。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.22520v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
