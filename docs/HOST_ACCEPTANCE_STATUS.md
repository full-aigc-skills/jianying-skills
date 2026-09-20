# 三宿主技能验收状态

验收日期：2026-09-20。既有验收对象为不可变发布 `v2.0.2`；`2.0.0` 的远端安装发现了
4 个由 `openspec init` 生成的开发辅助技能，因此不能作为“仅 13 个产品技能”的通过证据。
源码现已进入 `v2.0.4` 发布候选：该候选修复了 `jianying-harness` supporting reference 中
仍存的退休外部 headless plan 活动叙事，并新增发布 lint。`v2.0.4` 未发布前，以下
`v2.0.2` 结果只作为历史安装证据，不能解除当前插件技能锁门禁。

## 已取得证据

- `npx skills add <local-source> --skill jianying-use --agent codex --copy --json`
  在隔离项目中只安装一个技能，安装摘要为 `installed`，内容摘要为
  `842edfe9b7e8352e6baaf6d4cd5747197088f52f9601c3a389908241180a3767`。
- Codex CLI `0.153.4` 通过 `debug prompt-input` 的只读投影发现项目级
  `jianying-use`，模型可见路径指向隔离项目的 `.agents/skills/jianying-use/SKILL.md`；
  该检查未发起模型请求。
- `npx skills add <local-source> --skill jianying-use --agent zcode --copy --json`
  在隔离项目中只安装一个技能；ZCode CLI `0.16.9` 的 `skills list --json`
  发现该项目级技能，来源为 `zcode`，该技能路径没有诊断。
- Kimi 的安装器目标名为 `kimi-code-cli`。使用该名称执行相同的单技能安装后，
  Kimi Code CLI `0.43.1` 所用 `.agents/skills/jianying-use` 目录包含 SKILL、三份
  references、三个 Markdown examples 和 `minimal-job.json`，摘要与另外两个宿主一致。
- Kimi 本地 Web Server 的 `/api/v1/meta` 报告 `skill` feature 为 `Active`；本次仅
  使用回环地址和 bearer token，并通过 `/api/v1/shutdown` 正常关闭，没有发起模型请求。

## 不可变 v2.0.2 fresh-install 复验

- 从远端标签 `v2.0.2` fresh clone，检出提交
  `e26e6b1c483a435479dadd87130da93ad2e5aaa1`；`skills/` 下只有 13 个产品技能，未包含
  OpenSpec 开发辅助技能。
- 在三个全新 Git 项目中分别以 `codex`、`zcode`、`kimi-code-cli` 为安装目标，只安装
  `jianying-use`。三次安装均返回 `installed`，安装器内容摘要均为
  `842edfe9b7e8352e6baaf6d4cd5747197088f52f9601c3a389908241180a3767`。
- 三个安装目录都只有 8 个技能文件，与标签源码逐文件一致；按相对路径和文件 SHA-256
  聚合得到相同摘要 `fdca7729f47ebf5fc83471a2d9b9e0369b14021ff59756d1915ae25e8d3135b6`。
- 当前 Codex CLI `/Users/wandl/.local/bin/codex` 报告 `0.147.0`，其 `debug prompt-input`
  只读投影包含项目级 `jianying-use` 和隔离安装路径，没有发起模型请求。
- ZCode CLI `0.16.9` 的 `skills list --json` 发现项目级发布版技能且目标路径无诊断；同时也
  发现用户插件缓存 `jianying-edit/0.11.1` 中的旧版同名技能。项目级技能列在前，但最终模型
  行为验收仍必须证明实际加载的是发布版 Rust-only 内容。
- Kimi Code CLI `0.43.1` 从发布版安装目录启动本地回环 Web Server，`/api/v1/meta` 再次报告
  `skill` feature 为 `Active`；服务器通过带 bearer token 的 `/api/v1/shutdown` 正常关闭，
  未发起模型请求。

## 尚未满足的门禁

OpenSpec 任务 `9.4` 继续保持未勾选。以下行为必须由三个真实宿主分别加载本次技能版本后
执行，不能由文件发现、安装摘要或插件 Harness 测试替代：

1. 简单草稿任务的技能触发和最小询问行为。
2. 可恢复失败后的 `job show`、精确重新批准和 `job retry` 引导。
3. 原生导出前对 command、arguments、target、task 和 expiry 的目标级授权。

不可变 `v2.0.2` 的 fresh install 和静态宿主发现已经完成；当前候选还需要先发布并重新执行
`v2.0.4` fresh install。真实行为验收会调用宿主模型并
消耗账号额度，因此在没有独立授权时不自动执行；ZCode 验收还必须记录同名旧技能的实际解析
结果，不能只依赖列表顺序推断。

`v2.0.2` 的 tag workflow 曾在 Release 已公开并变为 immutable 后，因为自动 attestation 尚未
可见而失败。`v2.0.4` 候选已将该路径改为 fail-closed 恢复：最多轮询 5 分钟；重跑只接受同
tag 的稳定 immutable Release，并要求下载的 manifest 与当前 tag 生成物逐字节一致，绝不覆盖
既有资产。发布工作流还会在 lint、测试、TRACE 和 manifest 生成前校验 tag 与包版本完全一致，
并确认仓库已启用 Immutable Releases；预检失败时不会创建或修改 Release。
该前置检查现由 `scripts/release_preflight.py` 同时输出
`jianying-skills-remote-release-preflight/v1`，并无论成功或失败都上传
`jianying-skills-remote-preflight` artifact。`prerequisitesReady` 只要求仓库发布设置可用，
`releaseComplete` 才要求 `v2.0.4` 稳定 immutable Release 已存在，因此不会让 tag workflow
在创建 Release 前循环依赖自身结果。
若首次 tag workflow 在 Draft 创建后中断，`scripts/release_publication_plan.py` 会校验已有
manifest 的名称、uploaded 状态、长度与 GitHub `sha256:` digest；空 Draft 只补传 manifest，
完整 Draft 直接公开。任何额外资产或内容漂移都在公开前失败，流程不使用 `--clobber`，因此
不会把污染的 Draft 转换为不可变 Release。
同一状态机已对真实 `v2.0.2` immutable Release 做只读 canary：GitHub 返回资产状态
`uploaded`、长度 4,878 和 digest
`a80df2c2a58b0989e94d51bce7aed7c5c32d98575acbd64b981a1d44687e8665`；下载字节匹配后计划
严格返回 `verify_existing` 且缺失资产为零，证明当前 GitHub CLI 元数据形状可被正式脚本消费。
同一 workflow/ref 的 tag 发布现在不取消已经运行中的发布；GitHub 可能替换尚未开始的旧 pending
重跑。所有实际获准运行且需要公开 Draft 的路径都会在
`gh release edit --draft=false` 前重新获取远端 assets 并再次执行状态机，完整 Draft 快路径也
不能绕过最终集合复核。
由于 GitHub 只在公开后锁定关联 tag，初次和最终状态机还会分别解析远端 tag：lightweight tag
直接取 commit，annotated tag 取 peeled commit，并要求与当前 checkout SHA 完全一致。Draft 期间
tag 被移动、删除或解析出异常多条记录时，发布在 immutable 锁定前失败。

正式 tag workflow 需要仓库 secret `RELEASE_RULESET_READ_TOKEN`，其 fine-grained 权限限定为
本仓库 Administration read，仅用于读取适用 repository/organization ruleset 的完整详情；
Release 写入仍由 `github.token` 完成。secret 缺失或权限不足时 tag 发布在 lint、TRACE 和 Draft
创建前 fail closed，手工预演只保留结构化 blocked 证据。
`release-skills.yml` 现在还提供只读 `workflow_dispatch` 候选预演：validate job 使用
`contents: read`，执行预检、lint、测试、canonical manifest check 和 TRACE；只有 tag 路径才生成
released manifest artifact，并进入独立、显式 `contents: write` 的 publish job。手工预演不会创建
Release，也不会发送消费者同步事件。预检 JSON 写入 `$RUNNER_TEMP` 而非 checkout，避免
`skill_manifest.py release` 的 clean-worktree 门禁被工作流自身生成的证据文件误触发。
隔离临时 Git 仓已按 validate job 顺序实际运行预检、lint、15 项测试和 manifest check；结束后
`git status --porcelain` 为空，且预检 artifact 只存在于 checkout 外部。

此前候选曾在隔离临时 Git 仓完成 `v2.0.4` tag、远端 ref 和 release manifest 演练；其候选内容
覆盖 13 个技能，聚合摘要为
`6198259b50845b1b4f28ac0668c112a303a19199966a14efe58499de8af905d4`，并通过插件导入器的离线
commit 注入路径完成原子消费和逐目录复核。现在 `skill_manifest.py release` 自身也只接受
`full-aigc-skills/jianying-skills` 的 GitHub HTTPS/SSH 正典 remote，本地或镜像 remote 会在解析
tag 前被拒绝，因此隔离演练只保留候选内容证据，不再能够生成新的正式 `released` 身份，亦不构成
`v2.0.4` 已发布证据。

2026-09-21 的发布内容边界加固使 `skill_manifest.py` 在哈希前拒绝技能目录和内容中的
symlink、FIFO、socket 或设备文件，避免跟随链接读取仓库外内容。插件侧不可变 manifest
导入器执行同一规则并在原子替换前失败；当前 13 个技能不含此类成员，canonical manifest
反向摘要校验继续通过。该门禁不替代 `v2.0.4` 正式 Release。
