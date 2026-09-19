## Purpose

确保全部剪映技能以统一 Rust CLI 为唯一执行入口，并用稳定 capability 和版本声明替代 Python API 与外部 fork 路由。

## ADDED Requirements

### Requirement: 单一运行时叙事
所有技能 SHALL 只指导智能体调用 `jianying-cli` 或承载插件的 Rust CLI adapter，不得生成 Python 草稿脚本或调用外部 headless checkout。

#### Scenario: 用户请求制作字幕草稿
- **WHEN** `jianying-subtitles` 被触发
- **THEN** 技能生成 Rust Job/Plan 或对应 CLI 调用，不引用 pyJianYingDraft API

### Requirement: Capability 与版本声明
每个技能 SHALL 声明所需 CLI capability、最低兼容版本、输入事实和输出证据等级。

#### Scenario: 缺少所需能力
- **WHEN** 技能需要原生导出但 CLI 未声明该 capability
- **THEN** 技能停止并路由到升级或环境诊断，不提供虚假成功路径

### Requirement: 13 个场景入口保持可发现
技能包 SHALL 保留现有 13 个用户场景入口或提供明确迁移别名，避免升级后触发名称失效。

#### Scenario: 旧技能名安装
- **WHEN** 用户仍按现有名称安装 `jianying-draft`
- **THEN** 安装结果提供统一 Rust 草稿能力说明或明确的迁移交接
