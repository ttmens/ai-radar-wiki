---
title: LongTraceRL: Learning Long-Context Reasoning from Search Agent Trajectories with
created: 2026-06-01
updated: 2026-06-01
type: concept
pillar: capabilities
pm_score: 0.43
tags: ["research", "capabilities"]
sources: ["raw/papers/longtracerl-learning-long-context-reasoning-from-search-agent-trajectories-with.json"]
---

# LongTraceRL: Learning Long-Context Reasoning from Search Agent Trajectories with Rubric Rewards

## 中文摘要
该论文提出LongTraceRL方法，通过利用搜索代理的轨迹数据和基于rubric的奖励机制，训练大语言模型提升长上下文推理能力。传统强化学习可验证奖励（RLVR）受限于低置信度和任务复杂度，LongTraceRL从搜索代理成功检索并整合分散信息的路径中学习，结合细粒度rubric奖励信号，使模型在长文档中更精准地定位和推理关键信息。商业上，可增强知识密集型产品（如智能搜索、文档分析、客户支持）的准确性和可靠性，减少幻觉。产品创新在于将搜索过程作为训练信号，实现推理能力的可迁移学习。

## PM 关注指标
- 🎯 PM Score: 0.43
- 🏷️ Pillar: capabilities
- 🔑 Keywords: benchmark, vision, reasoning, training, dataset

## 作者
Nianyi Lin, Jiajie Zhang, Lei Hou, Juanzi Li

## 摘要
Long-context reasoning remains a central challenge for large language models, which often fail to locate and integrate key information in extensive distracting content. Reinforcement learning with verifiable rewards (RLVR) has shown promise for this task, yet existing methods are limited by low-conf...

## 中文摘要
该论文提出LongTraceRL方法，通过利用搜索代理的轨迹数据和基于rubric的奖励机制，训练大语言模型提升长上下文推理能力。传统强化学习可验证奖励（RLVR）受限于低置信度和任务复杂度，LongTraceRL从搜索代理成功检索并整合分散信息的路径中学习，结合细粒度rubric奖励信号，使模型在长文档中更精准地定位和推理关键信息。商业上，可增强知识密集型产品（如智能搜索、文档分析、客户支持）的准确性和可靠性，减少幻觉。产品创新在于将搜索过程作为训练信号，实现推理能力的可迁移学习。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2605.31584v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
