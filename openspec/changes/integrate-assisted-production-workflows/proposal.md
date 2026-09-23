## Why

现有技能已经覆盖剪映原子操作与开放场景规划，但录屏交互、智能缩放、Web 动效、媒体标准化、影视解说、曝光匹配和模板批产仍缺少可供 Harness 消费的知识合同。研究仓 `jianying-editor-skill` 提供了有价值的方法线索，同时携带与 Rust-only 架构冲突的 Python 运行时、UI 自动化和来源不明资源，因此必须以固定来源基线进行知识重写，而不能整体合并。

## What Changes

- 固定 `jianying-editor-skill@32c56928ded4f9e2c2b80e099dc7abb793d2c30b` 的来源、许可证、允许吸收范围和禁止复制范围。
- 新增五条辅助制作 Recipe：软件教程录屏、README 安装教程、产品演示智能缩放、Web 数据可视化片头、影视解说与 B-roll 匹配。
- 新增 `interaction-events/v1`、`smart-zoom-plan/v1` 与 `media-preflight/v1` 的知识 Schema、有效示例和确定性校验。
- 扩展媒体、动效、调节、音频/旁白/字幕和模板技能的操作动线，但不在 Skills 中实现 Provider 或草稿写入引擎。
- 保持所有草稿修改只能由不可变发布的 Rust `jianying-cli` 经 `jianying-job/v2` 完成；Compound Clip 在黑盒能力可用前保持 `plan_only`。
- 新增负例与发布完整性门禁，拒绝 Python 运行时、自由命令字符串、云资源数据库、私有资源包和未经能力证明的执行声明。

## Capabilities

### New Capabilities

- `assisted-production-workflows`: 定义辅助媒体工作流的来源边界、Recipe、事件/缩放/媒体预检知识合同、技能路由和证据门禁。

### Modified Capabilities

无。

## Impact

- 修改 `jianying-video-planning`、`jianying-media`、`jianying-motion`、`jianying-adjustments`、`jianying-audio`、`jianying-narration`、`jianying-subtitles`、`jianying-templates` 和 `jianying-harness` 的自包含参考资料与路由说明。
- 新增 stdlib 校验器和测试；不新增 Python 运行时依赖，不携带第三方媒体、效果包、缓存数据库、凭据或二进制。
- 配套插件变更应独立命名为 `add-assisted-media-provider-harness`，负责 Provider、审批、恢复、证据与 WorkflowPlan 编译；本变更不修改插件仓。
