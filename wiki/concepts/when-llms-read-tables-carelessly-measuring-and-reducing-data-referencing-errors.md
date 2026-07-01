---
title: When LLMs Read Tables Carelessly: Measuring and Reducing Data Referencing Errors
created: 2026-07-01
updated: 2026-07-01
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/when-llms-read-tables-carelessly-measuring-and-reducing-data-referencing-errors.json"]
---

# When LLMs Read Tables Carelessly: Measuring and Reducing Data Referencing Errors

## 中文摘要
大型语言模型（LLM）在执行表格任务时虽然能理解表格结构，但仍会犯数据引用错误（DREs），即错误引用或遗漏表格中的数值。这类错误不仅影响最终答案的准确率，更直接损害模型在数据密集型场景（如金融分析、报告生成）中的正确性和可靠性。该研究系统测量了DREs的类型与频率，并提出了减少错误的改进方法。对产品经理而言，这意味着在构建基于LLM的数据查询、表格问答等产品时，需关注模型对具体数值的忠实度，通过优化提示词或引入验证机制来提升产品可信度和用户信任。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, reasoning, parameter, accuracy

## 作者
Yuqing Yang, Qi Zhu, Zhen Han, Boran Han, Zhengyuan Shen

## 摘要
While large language models (LLMs) perform well on table tasks, they still make data referencing errors (DREs), i.e., incorrectly citing or omitting table values, despite understanding the table structure. Beyond final-answer accuracy, DREs directly compromise the correctness and reliability of inte...

## 中文摘要
大型语言模型（LLM）在执行表格任务时虽然能理解表格结构，但仍会犯数据引用错误（DREs），即错误引用或遗漏表格中的数值。这类错误不仅影响最终答案的准确率，更直接损害模型在数据密集型场景（如金融分析、报告生成）中的正确性和可靠性。该研究系统测量了DREs的类型与频率，并提出了减少错误的改进方法。对产品经理而言，这意味着在构建基于LLM的数据查询、表格问答等产品时，需关注模型对具体数值的忠实度，通过优化提示词或引入验证机制来提升产品可信度和用户信任。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.32029v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
