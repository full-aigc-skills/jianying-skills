## Context

`jianying-cli v1.6.19` 已提供机器可读命令目录、capability manifest、原生控件目录和部分 GUI Adapter 合同。`jianying-skills v2.2.2` 目前有 14 个按工程阶段划分的技能，其中音频、字幕和转场可直接承担面板分类职责，其余面板分类缺少独立入口。

## Goals / Non-Goals

- 目标：一个面板分类一个独立技能；一个功能动作一条稳定语义动线；执行路由、能力状态、权益门禁和完成证据可审计。
- 非目标：本变更不凭文字补齐 CLI 未实现能力，不把视觉坐标固化为生产接口，不绕过素材授权、费用、上传或真实剪映验收。

## Decisions

### 1. 保持 13 个用户分类，避免重复技能

音频使用 `jianying-audio`，转场使用 `jianying-transitions`，字幕使用 `jianying-subtitles`；新增 `jianying-media`、`jianying-text`、`jianying-stickers`、`jianying-effects`、`jianying-smart-package`、`jianying-filters`、`jianying-adjustments`、`jianying-templates`、`jianying-digital-human`、`jianying-editing-console`。

### 2. 操作动线使用稳定语义 ID

每个动线采用 `<domain>.<group>.<action>`，例如 `media.import.asset`、`media.import.subdraft`。技能先说明用户界面路径，再给事实读取、结构化 argv 或 Harness 合同、验证和恢复。禁止把屏幕坐标作为动作身份。

### 3. 四级执行路由

优先级为：Rust 草稿协议命令 → Rust Runtime 原生控制 → 版本绑定 Accessibility Adapter → 带 Canary 的视觉兜底。capability 为 partial、external_dependency 或缺失时，技能只能停在计划、预览或批准门禁，不得声称已执行。

### 4. 自包含但不复制整本手册

每个技能的 `SKILL.md` 只保留触发、边界和主流程；完整功能树写入本技能 `references/workflow.md`，最小执行合同放入 `examples/minimal-job.json`，保证粒度安装可用。

### 5. 发布消费链不旁路

先在技能仓验证并发布不可变版本，再由插件导入发布 manifest 和逐技能摘要。插件仓的 vendored Skill 不接受手工修改。

## Risks / Trade-offs

- [剪映版本改变入口] → 动线身份绑定语义 ID 和版本，GUI 路由必须通过 Canary。
- [技能数量增加] → `jianying-use` 只做分流，按需加载目标技能，避免同时载入全部说明。
- [CLI 与界面能力不对齐] → 表中分别标记 supported、partial、GUI-only 和 blocked，不以相似命令替代。
- [官方素材授权变化] → 下载和应用分开审批，保存资源收据、权益快照和用途。

## Migration Plan

1. 先增加失败测试，冻结 13 分类、24 个总技能、自包含资源和动线字段。
2. 新增/增强技能并以 `v1.6.19` 发布命令目录校验能力引用。
3. 更新包清单、契约矩阵、README 和候选 manifest，完成严格 OpenSpec 验证。
4. 发布新的不可变技能版本；插件只通过发布 manifest 导入。
5. 插件发布后在 Codex、ZCode、Kimi 验证分类技能可发现、可路由和可停止在正确门禁。
