## Why

插件的目标驱动质量循环需要场景专属、可锁定和可摘要验证的评审规则；通用分数或自然语言提示不能可靠区分 Vlog、课程和婚礼的不同完成条件。Skills 应保存知识档案，插件保存评估与执行合同，避免知识文档直接获得执行权。

## What Changes

- 新增 `jianying-quality-profile-catalog/v1`，首批包含 Vlog、课程多交付和婚礼多用途三个 QualityProfile。
- 每个档案声明评估维度、硬门禁、阈值、所需证据、允许建议动作和人工审校边界。
- 档案关联现有代表工作流与来源索引，但不包含命令、handler、供应商凭据、批准或运行成功声明。
- 新增确定性校验及测试，保证身份唯一、来源有效、动作受限和正式资源可进入技能摘要。

## Capabilities

### New Capabilities

- `video-quality-profiles`: 为场景化视频评审提供版本化知识档案、来源、人工边界和发布完整性合同。

### Modified Capabilities

无。

## Impact

- 修改 `jianying-video-planning` 的 references 和路由说明。
- 插件通过不可变 Skills lock 消费档案；本仓不实现 evaluator、WorkflowPlan、Job 或 CLI。
- 配套插件变更为 `add-iterative-video-quality-loop`。
