---
title: When to Write and When to Suppress: Route-Specialized Dual Adapters for Memory-A
created: 2026-06-15
updated: 2026-06-15
type: concept
pillar: capabilities
pm_score: 0.43
tags: ["research", "capabilities"]
sources: ["raw/papers/when-to-write-and-when-to-suppress-route-specialized-dual-adapters-for-memory-as.json"]
---

# When to Write and When to Suppress: Route-Specialized Dual Adapters for Memory-Assisted Knowledge Editing

## 中文摘要
本文研究在知识编辑系统中，如何基于记忆辅助机制实现选择性知识更新：通过检索编辑记忆并使用参数高效适配器修正模型的对象偏好，同时保持邻近无关行为不变。关键创新在于提出路由选择双适配器架构，能自动决定何时写入新知识、何时抑制干扰。该技术可提升AI模型的动态更新能力，降低重新训练成本，对需要频繁修正事实型知识的商业应用（如客服、问答系统）具有重要价值，同时避免模型在相关领域出现错误泛化。

## PM 关注指标
- 🎯 PM Score: 0.43
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, benchmark, embedding, parameter, accuracy

## 作者
Yining Huang

## 摘要
Knowledge editing systems must update selected facts while preserving nearby but irrelevant behavior. This paper studies this problem in a memory-assisted setting where an edit memory is retrieved at inference time and a parameter-efficient adapter corrects the model's object preference. We argue th...

## 中文摘要
本文研究在知识编辑系统中，如何基于记忆辅助机制实现选择性知识更新：通过检索编辑记忆并使用参数高效适配器修正模型的对象偏好，同时保持邻近无关行为不变。关键创新在于提出路由选择双适配器架构，能自动决定何时写入新知识、何时抑制干扰。该技术可提升AI模型的动态更新能力，降低重新训练成本，对需要频繁修正事实型知识的商业应用（如客服、问答系统）具有重要价值，同时避免模型在相关领域出现错误泛化。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.14668v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
