---
title: DexCompose: Reusing Dexterous Policies for Multi-Task Manipulation with a Single
created: 2026-06-29
updated: 2026-06-29
type: concept
pillar: capabilities
pm_score: 0.36
tags: ["research", "capabilities"]
sources: ["raw/papers/dexcompose-reusing-dexterous-policies-for-multi-task-manipulation-with-a-single.json"]
---

# DexCompose: Reusing Dexterous Policies for Multi-Task Manipulation with a Single Hand

## 中文摘要
DexCompose 提出一种灵巧操作策略组合方法，利用单一灵巧手复用已有策略完成多任务操作。核心挑战在于不同任务对重叠手指和接触模式的冲突需求，该方法通过组合现有灵巧策略而非从头训练解决冲突，降低计算成本并提升泛化能力。技术要点在于策略组合时的冲突消解机制，使单手能柔性切换多种操作技能。商业价值体现在机器人灵巧手在多任务场景（如装配、医疗）中快速适配新任务，减少重新训练开销，推动灵巧操作产业化。产品创新在于将单任务策略模块化组合，实现灵活复用。

## PM 关注指标
- 🎯 PM Score: 0.36
- 🏷️ Pillar: capabilities
- 🔑 Keywords: framework, eval, serving

## 作者
Dihong Huang, Zhenyu Wei, Zhuxiu Xu, Yunchao Yao, Sikai Li

## 摘要
Dexterous manipulation policies can solve individual skills, but composing them to perform multiple tasks with a single hand remains challenging. Adding a new task on top of an existing manipulation skill often imposes conflicting demands on overlapping fingers and contact modes, causing destructive...

## 中文摘要
DexCompose 提出一种灵巧操作策略组合方法，利用单一灵巧手复用已有策略完成多任务操作。核心挑战在于不同任务对重叠手指和接触模式的冲突需求，该方法通过组合现有灵巧策略而非从头训练解决冲突，降低计算成本并提升泛化能力。技术要点在于策略组合时的冲突消解机制，使单手能柔性切换多种操作技能。商业价值体现在机器人灵巧手在多任务场景（如装配、医疗）中快速适配新任务，减少重新训练开销，推动灵巧操作产业化。产品创新在于将单任务策略模块化组合，实现灵活复用。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.28323v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
