---
title: TiRex-2: Generalizing TiRex to Multivariate Data and Streaming
created: 2026-07-02
updated: 2026-07-02
type: concept
pillar: capabilities
pm_score: 0.48
tags: ["research", "capabilities"]
sources: ["raw/papers/tirex-2-generalizing-tirex-to-multivariate-data-and-streaming.json"]
---

# TiRex-2: Generalizing TiRex to Multivariate Data and Streaming

## 中文摘要
TiRex-2是基于xLSTM架构的时间序列基础模型，将原单变量模型扩展为支持多变量预测，并能同时利用历史协变量和未来已知协变量。该模型采用循环设计，适合流式数据场景，可处理连续到达的观测值并捕捉变量间的联合演化。商业上可用于金融、供应链、IoT等领域的实时预测，降低定制模型开发成本。产品创新在于将基础模型范式引入时序预测，提升泛化能力和部署效率。

## PM 关注指标
- 🎯 PM Score: 0.48
- 🏷️ Pillar: capabilities
- 🔑 Keywords: inference, training, transformer, attention, parameter

## 作者
Patrick Podest, Marco Pichler, Elias Bürger, Levente Zólyomi, Bernhard Voggenberger

## 摘要
We introduce TiRex-2, a recurrent xLSTM-based time series foundation model that generalizes the univariate TiRex to multivariate forecasting with both past and future covariates. Real-world forecasting is inherently sequential: observations arrive continuously, variables evolve jointly, and a subset...

## 中文摘要
TiRex-2是基于xLSTM架构的时间序列基础模型，将原单变量模型扩展为支持多变量预测，并能同时利用历史协变量和未来已知协变量。该模型采用循环设计，适合流式数据场景，可处理连续到达的观测值并捕捉变量间的联合演化。商业上可用于金融、供应链、IoT等领域的实时预测，降低定制模型开发成本。产品创新在于将基础模型范式引入时序预测，提升泛化能力和部署效率。

## 链接
- 📄 arXiv: http://arxiv.org/abs/2607.01204v1

## PM 视角解读
> 由 Stage 2 LLM 分析后补充

## 相关
- 相关概念: TBD
