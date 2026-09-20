## Purpose

确保全部剪映技能以统一 Rust CLI 为唯一执行入口，并用稳定 capability 和版本声明替代 Python API 与外部 fork 路由。

## ADDED Requirements

### Requirement: 单一运行时叙事
所有技能 SHALL 只指导智能体调用 `jianying-cli` 或承载插件的 Rust CLI adapter，不得生成 Python 草稿脚本或调用外部 headless checkout。

#### Scenario: 用户请求制作字幕草稿
- **WHEN** `jianying-subtitles` 被触发
- **THEN** 技能生成 Rust Job/Plan 或对应 CLI 调用，不引用 pyJianYingDraft API

#### Scenario: Supporting reference 保留退休活动契约
- **WHEN** 任一技能正文、reference 或 example 把外部 headless plan、Python API 或 fork 私有字段描述为当前输入契约
- **THEN** 技能 lint 和发布门禁失败，并要求改用 `jianying-job/v2` 与实际 capability manifest

#### Scenario: 用户请求本地 Whisper 转写
- **WHEN** CLI capability manifest 报告 `media.asr_whisper_cpp=supported`，且用户提供已审查的绝对 executable、model 和源媒体
- **THEN** narration 技能先执行 `media transcribe --plan` 固定身份和幂等键，再执行同一请求；失败仅在显式 `--retry` 下重试，不下载或捆绑运行时/模型

#### Scenario: 用户排查本机剪映安装
- **WHEN** setup 技能执行 `runtime discover` 后只发现草稿根或发现未验证应用
- **THEN** 技能分别报告 `drafts_without_editor` 或 unverified 安装，并保持 `automatic_routing=false`，不得把路径发现升级为 Runtime Profile 或真实宿主证据

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
