## Why

用户需要根据真实素材选择剪辑类型，并明确要求 108 个场景各有一个网上实操来源支持的独立 example。现有技能只有通用操作指导，缺少场景差异与可查询的能力映射。

## What Changes

- 新增 jianying-video-planning 技能，维护 18 类、108 个场景、12 套 Recipe 及逐场景 example。
- 每个场景记录检索词、真实来源、查阅日期、可见热度或未核验状态、素材要求、步骤、验收及技能/CLI 映射。
- 数据与例文单一来源，保留现有技能及执行契约；计划结果不表示成片完成。

## Capabilities

### New Capabilities

- `video-planning-examples`: 可追溯的场景实操库与类型规划技能。

### Modified Capabilities

无；既有 Rust Runtime 迁移继续独立验收。

## Impact

技能包、manifest、契约矩阵、内容检查、来源索引和 README。

108 个例文是方法迁移，素材不下载、不再分发；搜索排名不作为热门证明。现有 CLI 未 supported 的能力保持门禁。

