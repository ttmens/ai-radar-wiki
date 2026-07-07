---
title: LLM-as-a-Verifier: A General-Purpose Verification Framework
created: 2026-07-07
updated: 2026-07-07
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/llm-as-a-verifier-a-general-purpose-verification-framework.json"]
---

# LLM-as-a-Verifier: A General-Purpose Verification Framework

## 中文摘要
本文提出将“验证（verification）”作为大语言模型（LLM）能力提升的新缩放轴，即让LLM作为通用验证器来判断输出结果的正确性，与预训练、后训练和测试时计算并行。该方法通过独立扩展验证能力，显著提升模型在代码、数学等领域的可靠性，降低错误率。对产品经理而言，这一框架可直接用于构建高精度应用（如自动代码审查、金融合规检查），将验证从事后步骤升级为可并行优化的核心能力，实现“验证即服务”的产品创新。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: token, benchmark, reasoning, training, grpo

## 作者
Jacky Kwok, Shulu Li, Pranav Atreya, Yuejiang Liu, Yixing Jiang

## 摘要
Scaling pre-training, post-training, and test-time compute have become the central paradigms for improving the capabilities of LLMs. In this work, we identify verification, the ability to determine the correctness of a solution, as a new scaling axis. To unlock this and demonstrate its effectiveness...

## 中文摘要
本文提出将“验证（verification）”作为大语言模型（LLM）能力提升的新缩放轴，即让LLM作为通用验证器来判断输出结果的正确性，与预训练、后训练和测试时计算并行。该方法通过独立扩展验证能力，显著提升模型在代码、数学等领域的可靠性，降低错误率。对产品经理而言，这一框架可直接用于构建高精度应用（如自动代码审查、金融合规检查），将验证从事后步骤升级为可并行优化的核心能力，实现“验证即服务”的产品创新。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.05391v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
