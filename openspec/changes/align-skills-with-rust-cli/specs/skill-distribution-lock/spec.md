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

#### Scenario: 技能内容包含符号链接或特殊文件
- **WHEN** 任一技能目录或其内容是 symlink、FIFO、socket、设备等非普通文件/目录，即使链接目标可读且目录摘要能够计算
- **THEN** 正典 manifest 生成和插件导入都必须在复制前 fail closed；不得跟随链接把仓库外内容纳入摘要或 vendored 分发

#### Scenario: 已发布版本包含后来发现的活动旧契约
- **WHEN** 不可变技能版本已经发布，但随后发现 supporting reference 仍把退休运行时描述为当前契约
- **THEN** 不覆盖旧 tag；修复进入更高的新版本，插件在锁定消费该版本前保持发布和最终 cutover 阻塞

### Requirement: 跨技能引用可安装
技能之间的交接 SHALL 使用技能名和安装命令，不得依赖粒度安装后不存在的兄弟相对路径。

#### Scenario: 单技能安装
- **WHEN** 用户只安装 `jianying-audio`
- **THEN** 其中所有本地链接均指向本技能资源，跨技能交接包含可执行安装指引

### Requirement: 不可变 manifest 发布可恢复
技能发布 SHALL 在 Release 公开后验证自动 attestation；若证明存在延迟，流水线必须可在不修改 immutable Release 的前提下恢复。公开前上传中断形成的 Draft 只有在已有资产是本次 manifest 集合的逐字节相同子集时才可续传。

#### Scenario: Draft manifest 上传中断
- **WHEN** tag workflow 已创建 Draft，但 manifest 尚未上传或上传后工作流中断
- **THEN** 重跑必须按名称、uploaded 状态、字节长度和 GitHub SHA-256 校验已有资产，只上传缺失 manifest；完整集合再次验证后才可公开，且不得 clobber

#### Scenario: Draft manifest 漂移或含额外资产
- **WHEN** 同 tag Draft 的同名 manifest 内容漂移，或出现本次发布不期望的资产
- **THEN** workflow 必须在公开前 fail closed，不得覆盖、删除或把污染 Draft 锁为不可变 Release

#### Scenario: 同 tag 技能发布并发重跑
- **WHEN** 同一 tag 的两个 workflow 运行同时等待发布，或完整 Draft 在初次检查后发生变化
- **THEN** workflow 必须按 workflow/ref 保证同一时刻只有一个运行进入发布区且不取消已运行中的发布；GitHub 可以替换尚未开始的旧 pending 重跑。任何实际获准运行的发布都必须在公开 Draft 前重新读取远端 manifest 元数据执行完整状态机校验

#### Scenario: Draft 阶段技能 tag 被移动
- **WHEN** Release 仍为 Draft，远端 lightweight tag 或 annotated tag 的 peeled commit 不再等于本次技能 checkout
- **THEN** 初次和公开前最终 publication plan 均必须 fail closed，不得生成或公开来源提交漂移的 immutable manifest Release

#### Scenario: 技能发布缺少 tag 防篡改规则
- **WHEN** 正典仓库缺少覆盖 `refs/tags/v*` 的 active、无 bypass、禁止删除和非快进更新的 tag ruleset
- **THEN** tag workflow 必须在创建或公开 Draft 前 fail closed，并在结构化预检证据中报告该阻塞

#### Scenario: tag workflow 在公开后失败
- **WHEN** manifest 已上传且 Release 已变为 immutable，但 attestation 暂未可见
- **THEN** 流水线轮询完整 Release attestation 和逐资产证明；完整证明必须绑定远端 tag 对象、正典仓库/tag 以及 manifest SHA-256，publication plan 另行绑定 annotated tag 的 peeled commit；重跑时验证稳定状态、下载远端 manifest 并与当前 tag 生成物逐字节相等后继续，禁止覆盖或替换资产

#### Scenario: tag 或仓库发布设置无效
- **WHEN** tag 不等于 manifest 包版本的 `v<version>`，仓库尚未启用 GitHub Immutable Releases，或缺少所需 tag ruleset
- **THEN** 流水线在 lint、测试、TRACE 和 manifest 生成前 fail-closed，不创建或修改 Release

#### Scenario: 发布前置检查需要独立证据
- **WHEN** tag workflow 检查正典仓库 Immutable Releases 设置和预期稳定 Release 状态
- **THEN** 流水线必须在 lint、测试与 TRACE 前生成并始终上传结构化预检 JSON；证据必须写到 checkout 外部，不能使 release manifest 的 clean-worktree 门禁被流水线自身污染；构建前置状态不得循环要求尚待本次工作流创建的 Release 已存在

#### Scenario: 手工预演发布候选
- **WHEN** 维护者通过 `workflow_dispatch` 验证尚未创建 tag 的技能发布候选
- **THEN** 流水线必须执行远端预检、lint、测试、canonical manifest check 和 TRACE 门禁，但不得签发 `content_state=released` manifest、创建或修改 Release、发送消费者同步事件；远端前置条件尚未满足时只保留结构化报告，不得阻断候选内容验证

#### Scenario: 非正典 remote 提供同名 tag
- **WHEN** `skill_manifest.py release` 指向本地路径、镜像仓库或其他非 `full-aigc-skills/jianying-skills` GitHub remote，即使该 remote 存在相同 tag 和 commit
- **THEN** 生成器在解析远端 tag 前拒绝签发 `content_state=released` 清单；隔离演练只能作为候选内容验证，不能成为正式发布身份
