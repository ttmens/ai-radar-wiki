---
title: Hierarchical Advantage Weighting for Online RL Fine-Tuning of VLAs from Sparse E
created: 2026-06-16
updated: 2026-06-16
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/hierarchical-advantage-weighting-for-online-rl-fine-tuning-of-vlas-from-sparse-e.json"]
---

# Hierarchical Advantage Weighting for Online RL Fine-Tuning of VLAs from Sparse Episode Outcomes

## 中文摘要
本文提出层次优势加权方法（Hierarchical Advantage Weighting），用于在在线强化学习中微调预训练VLA（视觉-语言-动作）策略。针对每个回合仅产生稀疏二元结果（成功/失败）的挑战，传统方法将结果简化为单一标量奖励或优势信号，导致过渡级监督不足。新方法通过层次结构对不同时间尺度的优势进行加权，有效利用稀疏结果信号引导actor更新，提升微调效率和最终策略性能。该方法有望降低具身智能任务中数据标注成本，加速机器人从稀疏反馈中学习，对产品化部署具有实用价值。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: vision, fine-tuning, sft, gradient

## 作者
Tongyan Fang, Siyuan Huang, Naiyu Fang, Ganlong Zhao, Zhongjin Luo

## 摘要
When pretrained VLA policies are fine-tuned through online RL, each rollout episode produces only a single binary outcome (success or failure), yet the actor update requires per-transition supervision. Existing approaches commonly reduce this sparse outcome to a single scalar reward or advantage sig...

## 中文摘要
本文提出层次优势加权方法（Hierarchical Advantage Weighting），用于在在线强化学习中微调预训练VLA（视觉-语言-动作）策略。针对每个回合仅产生稀疏二元结果（成功/失败）的挑战，传统方法将结果简化为单一标量奖励或优势信号，导致过渡级监督不足。新方法通过层次结构对不同时间尺度的优势进行加权，有效利用稀疏结果信号引导actor更新，提升微调效率和最终策略性能。该方法有望降低具身智能任务中数据标注成本，加速机器人从稀疏反馈中学习，对产品化部署具有实用价值。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.17043v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
