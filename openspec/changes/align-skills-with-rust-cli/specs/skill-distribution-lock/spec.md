## Purpose

建立技能仓到插件的单向、版本化和可验证分发关系，使唯一事实源不会因宿主副本或人工修补产生漂移。

## ADDED Requirements

### Requirement: 唯一事实源
技能正文 SHALL 只在 `jianying-skills` 维护；插件 vendored 副本不得作为独立编辑来源。

#### Scenario: 需要修正技能说明
- **WHEN** 插件发现技能内容错误
- **THEN** 修复先进入技能仓发布，再由锁定同步流程更新插件

### Requirement: 完整锁定
同步记录 SHALL 包含版本 ref、提交 SHA 和逐技能内容摘要，并验证技能清单完整性。

#### Scenario: 只同步部分技能
- **WHEN** 插件副本缺少发布版本中的任一声明技能
- **THEN** 同步或发布门禁失败并列出缺失技能

### Requirement: 跨技能引用可安装
技能之间的交接 SHALL 使用技能名和安装命令，不得依赖粒度安装后不存在的兄弟相对路径。

#### Scenario: 单技能安装
- **WHEN** 用户只安装 `jianying-audio`
- **THEN** 其中所有本地链接均指向本技能资源，跨技能交接包含可执行安装指引
