## Why

技能仓库虽然已经声明为唯一正典，但当前内容仍围绕“pyJianYingDraft 主路径 + Rust 快路径 + 外部 fork 专业档”。统一 Rust 引擎完成后，这套三层叙事会误导智能体并继续制造插件副本漂移，因此所有技能必须改为面向 `jianying-cli` 的单一执行契约。

## What Changes

- 保留 13 个面向用户场景的技能入口，但把执行方法统一为 `jianying-cli` Job/Plan 与结构化命令调用。
- 删除 Python API 手册、临时 Python 脚本生成和外部 fork 操作指南。
- 将 capcut-cli 86 项能力映射为按任务渐进披露的 Rust CLI 工作流，不要求用户记忆全部命令。
- 增加已有草稿编辑、ASR、批处理、任务恢复、原生导出和审批边界指导。
- 对每个技能声明所需 CLI capability、最低版本、读写风险级别、确认点和验收证据。
- 继续使用 ref + commit + 逐技能摘要锁同步到插件，禁止插件独立编辑正文。
- 更新中英文 README、第三方声明、安装说明和跨技能交接。
- **BREAKING**：移除 `jydraft_run.py`、`JIANYING_HEADLESS_ROOT` 和 Python/fork 三层路由的用户契约。

## Capabilities

### New Capabilities

- `canonical-rust-cli-skills`: 13 个技能以统一 Rust CLI 为唯一执行入口，并具备版本与 capability 声明。
- `workflow-guidance-and-safety`: 面向创建、编辑、字幕、音频、动效、批处理、导出与恢复的渐进式工作流和审批边界。
- `skill-distribution-lock`: 技能事实源、插件 vendoring、哈希锁、同步检查和漂移阻断机制。

### Modified Capabilities

无。仓库此前没有 OpenSpec 主规格。

## Impact

- 影响 `skills/*/SKILL.md`、references、examples、README、THIRD_PARTY_NOTICES、marketplace 元数据和同步工作流。
- 依赖 `jianying-cli` 的最终命令与 Schema 规格；插件只能消费本仓已发布、已锁定的技能版本。
- 本仓本地 `main` 当前领先 `origin/master` 两个提交，实施必须保留并建立在这些提交之上。
