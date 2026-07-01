---
title: TRIAGE: Role-Typed Credit Assignment for Agentic Reinforcement Learning
created: 2026-07-01
updated: 2026-07-01
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/triage-role-typed-credit-assignment-for-agentic-reinforcement-learning.json"]
---

# TRIAGE: Role-Typed Credit Assignment for Agentic Reinforcement Learning

## 中文摘要
TRIAGE论文提出一种角色化信用分配方法，用于智能体强化学习中的环境交互动作（如搜索、点击、编辑）的奖励归因。传统GRPO将所有动作令牌统一使用最终验证结果作为优势信号，而TRIAGE通过区分不同角色（如探索型、执行型）的动作并分配差异化信用，提升智能体在复杂任务中的训练效率与决策质量。该方法有望降低AI代理在真实场景（如自动化操作、工具使用）中的训练成本，加速产品落地。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, grpo, gradient, optimization

## 作者
Yuanda Xu, Zhengze Zhou, Hejian Sang, Xiaomin Li, Jiaxin Zhang

## 摘要
Agentic reinforcement learning requires assigning credit to environment-facing actions such as searches, clicks, edits, navigation commands, and object interactions. Standard GRPO uses the final verifier outcome as a uniform advantage over all action tokens. This outcome signal is useful but structu...

## 中文摘要
TRIAGE论文提出一种角色化信用分配方法，用于智能体强化学习中的环境交互动作（如搜索、点击、编辑）的奖励归因。传统GRPO将所有动作令牌统一使用最终验证结果作为优势信号，而TRIAGE通过区分不同角色（如探索型、执行型）的动作并分配差异化信用，提升智能体在复杂任务中的训练效率与决策质量。该方法有望降低AI代理在真实场景（如自动化操作、工具使用）中的训练成本，加速产品落地。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.32017v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
