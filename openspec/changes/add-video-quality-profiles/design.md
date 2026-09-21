## Context

现有 108 场景目录和三条代表工作流描述“剪什么、缺什么、如何验收”，但尚无适合机器绑定的分项质量档案。插件已经定义单个 `jianying-quality-profile/v1` 消费合同，本仓提供档案集合与来源边界。

## Goals / Non-Goals

**Goals:** 首批三个 profile 可独立校验、摘要和锁定消费；硬门禁不被总分覆盖；知识与执行权限分离。

**Non-Goals:** 不评价真实视频、不调用模型、不生成时间码、不证明真实剪映播放或导出、不穷举全部场景。

## Decisions

### 1. 单目录集合，单档案运行消费

集合使用 `jianying-quality-profile-catalog/v1`，每项保持插件可直接验证的 `jianying-quality-profile/v1` 结构。目录只增加 `workflow_ids` 和 `source_ids` 的索引映射，不复制第三方正文。

### 2. 硬门禁与评分分离

隐私、用途许可、教学语境和仪式连续性等不可由加权总分抵消。权重用于排序返工优先级，`hard_gate=true` 仍需独立证据。

### 3. 动作只是建议类别

档案只能引用插件已注册的 `trim/reorder/replace_clip/adjust_volume/caption_edit/crop/scale/color_adjust/music_edit`。它不携带参数、命令、文件路径或 capability 状态；插件运行时再检查能力与批准。

```mermaid
flowchart LR
    SRC[来源索引与代表工作流] --> PROFILE[QualityProfile 知识档案]
    PROFILE --> RELEASE[不可变 Skills Release]
    RELEASE --> LOCK[插件 Skills lock]
    LOCK --> EVAL[插件评估合同]
    EVAL -->|建议动作| PLAN[新 WorkflowPlan revision]
    PLAN -->|批准后| CLI[发布 Rust CLI]
```

## Risks / Trade-offs

- [评分规则过于通用] → 首批仅覆盖三条代表链，并保留人工边界。
- [知识被误作执行能力] → Schema 禁止执行字段，文档明确只提供建议。
- [档案漂移] → 进入技能内容摘要并由插件锁定校验。

## Migration Plan

先加入 Schema、三个档案和负例测试；再更新 SKILL 路由。通过完整性检查后发布新 Skills 版本，插件只在正式锁更新后启用消费。回滚恢复旧锁，不修改已有 Release。
