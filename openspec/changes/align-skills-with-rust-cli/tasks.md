## 1. 能力矩阵与统一契约

- [x] 1.1 清点现有 13 个技能、references、examples、脚本、跨技能交接和 Python/fork 依赖
- [x] 1.2 建立 13 个技能到 `jianying-cli` schema、capability、最低版本、风险等级和证据等级的矩阵
- [x] 1.3 定义统一契约头模板，包含触发条件、输入事实、所需能力、最低版本、默认风险、确认点、成功证据和禁止行为
- [x] 1.4 建立 CLI capability manifest 校验，阻止技能宣称 CLI 尚未通过门禁的能力
- [x] 1.5 保留现有 13 个技能名称及触发语义，为未来合并决策记录独立评估指标但不在本变更中改名

## 2. 四个基础技能迁移

- [x] 2.1 重写 `jianying-use` 为统一入口、最小询问、capability 路由和诊断交接
- [x] 2.2 重写 `jianying-setup` 为 Rust CLI、媒体工具、草稿根、Runtime Profile 和 doctor 指南
- [x] 2.3 重写 `jianying-draft` 为 Job/Plan Schema、领域概念、v1 兼容和证据边界指南
- [x] 2.4 重写 `jianying-harness` 为任务、审批、配置、MCP 和三宿主契约指南
- [x] 2.5 为四个基础技能分别补齐本技能内的 references、examples 和失败恢复案例
- [x] 2.6 将 `runtime discover` 收敛到 setup 技能与 capability 矩阵，区分应用安装、孤儿草稿根和精确 Runtime Profile，禁止因路径发现自动启用原生控制

## 3. 九个领域技能迁移

- [x] 3.1 重写 `jianying-edit` 的创建与已有草稿隔离编辑端到端工作流
- [x] 3.2 重写 narration 工作流，使用 Rust Job/Plan 和 ASR/TTS capability 门禁
- [x] 3.3 重写 subtitles 工作流，覆盖探测、导入、生成、样式、校验和恢复
- [x] 3.4 重写 audio 工作流，覆盖音量、淡入淡出、对齐、音效、静音和重链
- [x] 3.5 重写 motion 工作流，覆盖变换、关键帧、速度和量化报告
- [x] 3.6 重写 transitions 工作流，覆盖转场能力、边界检查和降级说明
- [x] 3.7 重写 inspect 工作流，区分结构验证、冷重开、播放和原生导出证据
- [x] 3.8 重写 export-prep 工作流，明确代理预览、原生导出授权、输出和 Runtime Profile
- [x] 3.9 重写 recover 工作流，覆盖任务 show/retry/audit、快照恢复和 ambiguous 外部操作
- [x] 3.10 为九个领域技能分别补齐自包含 references、examples 和最小任务路径
- [x] 3.11 将官方 whisper.cpp Rust CLI adapter 收敛到 narration/subtitles 技能路由，要求 capability、executable/model 哈希、`--plan` 零执行、账本复用和显式失败重试，且不得自动下载或捆绑权重

## 4. 安全与渐进式披露

- [x] 4.1 为所有工作流标注只读、可逆写入、高风险写入或外部/原生执行等级
- [x] 4.2 在已有草稿修改、发布、删除、付费 ASR、启动剪映和原生导出前写明目标级确认点
- [x] 4.3 将高级参数、资源目录、86 项能力映射和故障恢复移入按需 references，保持每个 SKILL.md 小于 500 行
- [x] 4.4 验证简单任务只暴露必要选择，不向用户倾倒完整命令百科
- [x] 4.5 为缺失 capability、版本过旧、不支持平台和证据不足提供明确停止与诊断路径

## 5. 清除旧执行叙事

- [x] 5.1 删除所有生成临时 Python 草稿脚本和调用 pyJianYingDraft API 的说明与示例
- [x] 5.2 删除 `jydraft_run.py`、`pymediainfo`、Python 主路径/Rust 快路径三层路由说明
- [x] 5.3 删除外部 headless checkout、`JIANYING_HEADLESS_ROOT` 和 fork 专业档指南
- [x] 5.4 全仓扫描 Python/fork 遗留词并逐项标注为删除、历史迁移说明或合法第三方声明
- [x] 5.5 验证每个技能只调用 `jianying-cli` 或插件的 Rust Runtime Adapter

## 6. 自包含安装与跨技能交接

- [x] 6.1 将跨技能交接统一改为技能名加 `npx skills add ... --skill ...` 安装指引
- [x] 6.2 扫描所有 Markdown，禁止指向兄弟技能目录的相对链接
- [x] 6.3 将粒度安装所需 schema 片段、示例和验收清单物化到各自技能目录
- [x] 6.4 对 13 个技能分别执行单技能安装模拟并验证所有本地链接、脚本和 references 可用

## 7. 文档、来源与市场元数据

- [x] 7.1 更新中文 README 为单一 Rust CLI 架构、13 技能职责、安装和迁移说明
- [x] 7.2 更新英文 README 并验证与中文能力声明一致
- [x] 7.3 更新第三方声明，保留 Apache-2.0/MIT 来源义务并声明非商业 headless 仓库不作为实现来源
- [x] 7.4 更新 marketplace 元数据、版本和技能清单，验证 13 个入口完整可发现
- [x] 7.5 生成完整 capcut-cli 能力审计文档的链接，不在每个技能重复维护 86 项表格

## 8. 发布锁与插件同步

- [x] 8.1 生成 canonical manifest，包含版本、commit、13 技能清单、逐目录摘要和最低 CLI capability 集
- [x] 8.2 实现 manifest 与工作树内容的反向摘要校验，人工修改必须失败
- [x] 8.3 发布新技能版本并记录不可变 ref、commit 和内容摘要
- [x] 8.4 在 `jianying-edit-plugin` 只通过锁定同步流程消费发布版本，不直接编辑 vendored 正文
- [x] 8.5 验证缺失技能、摘要漂移、CLI/技能版本不匹配时插件发布失败
- [x] 8.6 发布包含 `jianying-job/v2` supporting-reference 修复的不可变 `v2.0.4`，并由插件通过锁定同步消费；不得覆盖 `v2.0.2`
  - 本地门禁证据（2026-09-20）：release manifest 生成器已拒绝本地或镜像 remote，只有正典 GitHub remote 的同版本 tag/commit 才能签发 `released`；workflow 现会在 lint、测试和 TRACE 前生成并始终上传结构化远端预检，证据写入 checkout 外的 `$RUNNER_TEMP`，且提供 `contents: read` 的手工候选预演，只有 tag 才把生成的 released manifest 交给独立写权限 publish job。真实 `v2.0.4` Release 尚未发布，任务保持未完成。
  - 内容边界门禁（2026-09-21）：正典目录摘要器和插件导入器现同时拒绝技能目录或内容中的 symlink/特殊文件，禁止跟随链接读取仓库外内容后写入 manifest 或 vendored 副本；当前 13 技能 canonical manifest 摘要保持不变并通过反向检查。真实 `v2.0.4` Release 尚未发布，任务保持未完成。
  - Draft 恢复门禁（2026-09-21）：发布状态机现区分不存在、空/部分 Draft、完整 Draft 和已发布 immutable Release；只有名称、uploaded 状态、长度和 GitHub digest 与候选 manifest 一致的 Draft 才能补传缺失文件或公开，额外/漂移资产均 fail closed 且不使用 `--clobber`。真实 `v2.0.2` Release 的 4,878 字节 manifest 与 GitHub digest `a80df2c2a58b0989e94d51bce7aed7c5c32d98575acbd64b981a1d44687e8665` 已通过只读状态机 canary并返回 `verify_existing`/零缺失；真实 `v2.0.4` Release 尚未发布，任务保持未完成。
  - 发布竞态门禁（2026-09-21）：同一 workflow/ref 现串行且不取消在先运行；不存在、部分和完整 Draft 三条路径都在公开前重新读取远端 assets 并复用状态机验证完整 manifest 集合。真实 `v2.0.4` Release 尚未发布，任务保持未完成。
  - Tag 绑定门禁（2026-09-21）：初次与最终 publication plan 均重新解析远端 lightweight/annotated tag 并要求直接或 peeled commit 等于当前 checkout，覆盖 GitHub Draft 阶段 tag 尚可移动的边界；漂移、删除和异常输出均 fail closed。真实 `v2.0.4` Release 尚未发布，任务保持未完成。
  - 防篡改与证明门禁（2026-09-21）：预检现要求覆盖 `refs/tags/v*` 的 active、无 bypass、禁止删除和非快进更新的 tag ruleset；Release REST 查询只接受明确 404 为不存在。公开后状态机必须返回 `verify_existing`，完整 release attestation 同时绑定远端 tag 对象和 manifest SHA-256，publication plan 另行绑定 annotated tag 的 peeled commit。真实 `v2.0.2` attestation canary 已验证 tag 对象 `336dc9e57c6ede6b3b7efe923823f7b2209dbb2e` 与 manifest 摘要；当前远端尚无所需 ruleset，`v2.0.4` 仍未发布，任务保持未完成。
  - 正式发布与消费证据（2026-09-21）：正典仓库已启用 Immutable Releases，并建立 active、无 bypass、禁止删除和非快进更新的 `refs/tags/v*` ruleset。`v2.0.4` 已作为稳定 immutable Release 发布；资产 `jianying-skills-release-manifest.json` 为 5,048 字节，SHA-256 为 `21345983c877772303f5d21c9d16dfaebe17e8646db9f18a50a167d493864ea4`，GitHub release、完整 attestation 与 `gh release verify-asset` 均验证通过。插件随后锁定 tag `v2.0.4`、提交 `7917242f39349484e6785ae759c79381e934e15a`，原子导入 13 个技能并通过逐目录摘要与 readiness 复核；`v2.0.2` 未被覆盖。

## 9. 质量与三宿主验收

- [x] 9.1 验证 13 个 SKILL.md frontmatter、触发描述、命名、文件长度和本地资源路径
- [x] 9.2 执行全 Markdown 跨技能链接审计并确保无粒度安装死链
- [x] 9.3 对受影响技能运行 TRACE 评估，记录迁移前后 T/R/A/C/E 分数和未达标项
- [ ] 9.4 在 Codex、ZCode、Kimi 分别执行技能发现、单技能安装、简单任务、恢复和原生导出授权测试
- [x] 9.5 验证技能只报告实际获得的结构、冷重开、播放或原生导出证据等级
- [x] 9.6 确认所有测试建立在当前 `99fb872` 及既有本地提交之上，未重置用户历史后再标记变更可归档
