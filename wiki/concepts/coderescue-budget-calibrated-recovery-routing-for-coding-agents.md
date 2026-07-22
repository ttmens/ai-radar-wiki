---
title: CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents
created: 2026-07-22
updated: 2026-07-22
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/coderescue-budget-calibrated-recovery-routing-for-coding-agents.json"]
---

# CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents

## 中文摘要
CodeRescue 提出了一种预算校准的恢复路由策略，用于编码代理在执行环境中失败后获取反馈的场景。与传统的成本感知系统（先尝试廉价模型，失败后再升级到强模型）不同，该方法通过动态调整路由策略，在预算约束下更智能地分配不同模型资源，从而在保证修复成功率的同时控制整体成本。这对于构建高效、经济的 AI 编程助手具有重要商业价值，能显著降低 API 调用费用并提升用户体验的产品创新点。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: benchmark, training

## 作者
Qijia He, Jiayi Cheng, Chenqian Le, Rui Wang, Xunmei Liu

## 摘要
Coding agents increasingly operate in executable environments where a failed attempt produces actionable feedback rather than merely an incorrect answer. Existing cost-aware systems typically treat such failures as cascade decisions: try a cheap model first, then escalate hard cases to a stronger an...

## 中文摘要
CodeRescue 提出了一种预算校准的恢复路由策略，用于编码代理在执行环境中失败后获取反馈的场景。与传统的成本感知系统（先尝试廉价模型，失败后再升级到强模型）不同，该方法通过动态调整路由策略，在预算约束下更智能地分配不同模型资源，从而在保证修复成功率的同时控制整体成本。这对于构建高效、经济的 AI 编程助手具有重要商业价值，能显著降低 API 调用费用并提升用户体验的产品创新点。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.19338v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
