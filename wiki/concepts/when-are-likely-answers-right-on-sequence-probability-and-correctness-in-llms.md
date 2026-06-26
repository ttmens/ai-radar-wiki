---
title: When are likely answers right? On Sequence Probability and Correctness in LLMs
created: 2026-06-26
updated: 2026-06-26
type: concept
pillar: capabilities
pm_score: 0.515
tags: ["research", "capabilities"]
sources: ["raw/papers/when-are-likely-answers-right-on-sequence-probability-and-correctness-in-llms.json"]
---

# When are likely answers right? On Sequence Probability and Correctness in LLMs

## 中文摘要
该论文探讨了LLM解码方法中序列概率与答案正确性之间的关系。许多解码技术（如贪心搜索、束搜索）通过将概率质量转移到模型认为更可能的输出上来提高表现，但高概率并不总是对应正确答案。研究揭示了何时高序列概率意味着正确性，涉及模型校准、不确定性量化以及事实性对齐。对产品经理而言，这有助于设计更可靠的AI应用，例如通过概率阈值判断答案可信度，或开发混合策略（低概率时触发验证）。商业价值在于减少幻觉、提升用户信任，产品创新可包括概率驱动的质量控制机制或动态决策路由。

## PM 关注指标
- 🎯 PM Score: 0.515
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, parameter, accuracy, dataset

## 作者
Johannes Zenn, Jonas Geiping

## 摘要
Many decoding methods for large language models can be understood as shifting probability mass toward outputs that are more likely under the model, either locally at the token level or globally at the sequence level. Therefore, their success depends on a fundamental question: when does sequence prob...

## 中文摘要
该论文探讨了LLM解码方法中序列概率与答案正确性之间的关系。许多解码技术（如贪心搜索、束搜索）通过将概率质量转移到模型认为更可能的输出上来提高表现，但高概率并不总是对应正确答案。研究揭示了何时高序列概率意味着正确性，涉及模型校准、不确定性量化以及事实性对齐。对产品经理而言，这有助于设计更可靠的AI应用，例如通过概率阈值判断答案可信度，或开发混合策略（低概率时触发验证）。商业价值在于减少幻觉、提升用户信任，产品创新可包括概率驱动的质量控制机制或动态决策路由。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.27359v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
