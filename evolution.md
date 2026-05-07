# AI Radar Wiki — Self-Evolution Log

> 系统自进化记录。每次 Cron 运行自动更新。

## 机制说明

### 1. 动态权重 (pm_score)
- **信号强度**: GitHub stars / HN score / 评论数
- **时效性**: 新鲜内容获得更高权重
- **用户反馈**: 点击、点赞、忽略行为影响权重
- **公式**: `pm_score = 0.4*signal + 0.25*recency + 0.15*engagement + 0.2*relevance`

### 2. 内容淘汰
- 超过 90 天无更新 且 pm_score < 0.15 的节点标记为 `deprecated`
- 重复实体自动合并

### 3. 趋势检测
- 新标签在单次运行中出现 ≥3 次，自动上报到 trending_tags
- Agent 分析 trending 趋势，建议更新 SCHEMA.md

## 运行日志

## [2026-05-07 13:48] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 13:31] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 13:27] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'business': 11, 'patterns': 8, 'ecosystem': 1, 'unknown': 6, 'capabilities': 7}
- Top tags: {'research': 24, 'news': 15, 'techcrunch': 15, 'business': 11, 'patterns': 8}
- No actions needed


## [2026-05-07 13:25] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 1, 'unknown': 6, 'patterns': 5, 'capabilities': 6}
- Top tags: {'research': 24, 'unknown': 6, 'capabilities': 6, 'discussion': 5, 'hacker-news': 5}
- No actions needed


## [2026-05-07 13:23] Evolution Run
- Deprecated: 0 nodes
- Pillar distribution: {'ecosystem': 1, 'unknown': 6, 'patterns': 5, 'capabilities': 6}
- Top tags: {'research': 24, 'unknown': 6, 'capabilities': 6, 'discussion': 5, 'hacker-news': 5}
- No actions needed

