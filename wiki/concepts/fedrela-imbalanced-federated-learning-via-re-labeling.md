---
title: FedReLa: Imbalanced Federated Learning via Re-Labeling
created: 2026-06-25
updated: 2026-06-25
type: concept
pillar: capabilities
pm_score: 0.445
tags: ["research", "capabilities"]
sources: ["raw/papers/fedrela-imbalanced-federated-learning-via-re-labeling.json"]
---

# FedReLa: Imbalanced Federated Learning via Re-Labeling

## 中文摘要
FedReLa 提出了一种针对联邦学习中全局类别不平衡与跨客户端数据异构性共存的解决方案，通过重新标记（Re-Labeling）机制缓解本地与全局不平衡不匹配导致的性能下降。该技术无需共享原始数据，保护隐私的同时提升了模型在少数类上的泛化能力。商业价值在于，企业可在不集中敏感数据的情况下，利用各客户端异构数据训练更均衡的模型，适用于医疗、金融等数据分布极不均匀的场景，降低冷启动和偏见风险。产品创新体现在自适应调整客户端标签，实现全局优化。

## PM 关注指标
- 🎯 PM Score: 0.445
- 🏷️ Pillar: capabilities
- 🔑 Keywords: training, accuracy, dataset, model training

## 作者
Guangzheng Hu, Patricia Menéndez, Feng Liu, Mingming Gong, Guanghui Wang

## 摘要
Federated learning has emerged as the foremost approach for decentralized model training with privacy preservation. The global class imbalance and cross-client data heterogeneity naturally coexist, and the mismatch between local and global imbalances exacerbates the performance degradation of the ag...

## 中文摘要
FedReLa 提出了一种针对联邦学习中全局类别不平衡与跨客户端数据异构性共存的解决方案，通过重新标记（Re-Labeling）机制缓解本地与全局不平衡不匹配导致的性能下降。该技术无需共享原始数据，保护隐私的同时提升了模型在少数类上的泛化能力。商业价值在于，企业可在不集中敏感数据的情况下，利用各客户端异构数据训练更均衡的模型，适用于医疗、金融等数据分布极不均匀的场景，降低冷启动和偏见风险。产品创新体现在自适应调整客户端标签，实现全局优化。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2606.26037v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
