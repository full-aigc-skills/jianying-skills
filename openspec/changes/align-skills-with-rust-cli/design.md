## Context

当前 13 个技能已经是插件 vendoring 的声明事实源，但正文仍描述 Python 主路径、Rust 快路径和外部 fork 专业档。目标是保持用户场景入口稳定，同时把所有可执行步骤切换为统一 Rust capability 和 Job/Plan 契约。

## Goals / Non-Goals

**Goals:**

- 13 个技能均能独立安装并正确路由到 Rust CLI。
- 用户只看到任务相关的少量选择，复杂 CLI 参数通过 references 渐进披露。
- 每个技能明确版本、capability、风险、确认和验收等级。
- 插件副本能够被确定性锁定与验证。

**Non-Goals:**

- 技能不复制 Rust 实现或承担运行时功能。
- 技能不依赖兄弟技能目录在粒度安装时存在。
- 技能不承诺 CLI 尚未通过对应证据门禁的能力。

## Decisions

### 1. 保留 13 个名称，重新定义职责

- `jianying-use`：唯一入口、capability 路由和最小询问。
- `jianying-edit`：端到端创建/编辑工作流。
- `jianying-draft`：Job/Plan Schema 与领域概念，不再是 Python API 手册。
- `jianying-setup`：CLI、媒体工具、草稿根和运行时诊断。
- narration/subtitles/audio/motion/transitions：领域工作流。
- inspect/export-prep/recover：验证、导出和恢复。
- `jianying-harness`：任务、审批、配置、MCP 与宿主契约，不再代表外部 fork。

### 2. 每个 SKILL.md 使用统一契约头

正文开头包含：触发条件、所需 capability、最低 CLI 版本、默认风险级别、输入事实、成功证据和禁止行为。CLI 细节放在本技能 `references/`，保持 SKILL.md 小于 500 行。

### 3. 使用任务语言而非命令百科

技能首先说明“要达到什么结果”和最小流程，再提供推荐命令。86 项能力的完整映射生成到本仓审计文档和 CLI spec，不把整表复制进每个技能。

### 4. 可安装交接

跨技能引用使用技能名和 `npx skills add ... --skill ...`。每个技能需要的 schema 片段、示例或验收清单放在自身目录。共享源数据可以在仓库内用于生成，但发布前必须将需要内容物化到目标技能。

### 5. 同步锁为发布门禁

发布生成 canonical manifest：版本、commit、技能列表、每个目录摘要、最低 CLI capability 集。插件同步后运行反向摘要检查；任何人工修改都失败。

### 6. 文档与证据同步

README 只描述单一 Rust 架构。第三方声明分别说明 Apache/MIT 来源和“非商业仓库不作为实现来源”。技能对能力状态引用 CLI capability manifest，不维护独立的“已实现”表。

## Risks / Trade-offs

- [CLI 仍在分阶段实现] → 技能使用 capability gate，允许发布文档但禁止调用缺失能力。
- [保留旧技能名造成语义误解] → README 和每个技能首段明确新职责，并提供迁移说明。
- [共享资料重复] → 通过生成器保持一致，但发布物仍自包含以支持粒度安装。
- [插件同步滞后] → 通知 workflow 加上 CLI/技能兼容矩阵校验，未匹配版本不能发布插件。
- [本地 ahead 提交被覆盖] → 所有修改直接建立在当前 `99fb872` 之后，不重置或重建历史。

## Migration Plan

1. 建立 13 技能到 CLI capability 的矩阵和统一契约头模板。
2. 先更新 setup、use、draft、harness 四个基础技能。
3. 更新九个领域技能和各自 references/examples。
4. 清除 Python runner、pyJianYingDraft API、fork checkout 和旧环境变量说明。
5. 执行跨技能相对链接、frontmatter、500 行和 TRACE 评估。
6. 更新中英文 README、第三方声明和 marketplace 元数据。
7. 发布新技能版本并生成锁清单。
8. 由插件同步 PR 消费，三宿主新鲜安装验证后再把旧技能版本标为过时。

回滚通过技能版本 ref 完成；不在插件内手工逆向修改 vendored 副本。

## Open Questions

- 13 个技能是否在后续主版本合并少量重叠入口，可根据触发准确率与用户安装数据决定，本变更先保持兼容名称。
