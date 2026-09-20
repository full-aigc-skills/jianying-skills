# 三宿主技能验收状态

验收日期：2026-09-20。对象为 `2.0.2` 发布候选工作树；`2.0.0` 的远端安装发现了
4 个由 `openspec init` 生成的开发辅助技能，因此不能作为“仅 13 个产品技能”的通过证据。

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

## 尚未满足的门禁

OpenSpec 任务 `9.4` 继续保持未勾选。以下行为必须由三个真实宿主分别加载本次技能版本后
执行，不能由文件发现、安装摘要或插件 Harness 测试替代：

1. 简单草稿任务的技能触发和最小询问行为。
2. 可恢复失败后的 `job show`、精确重新批准和 `job retry` 引导。
3. 原生导出前对 command、arguments、target、task 和 expiry 的目标级授权。

真实行为验收可能调用宿主模型并消耗账号额度，因此在没有独立授权时不自动执行。发布后还需
从不可变 `v2.0.2` ref 重新做一次 fresh install，证明只发现 13 个产品技能，且本地工作树
没有掩盖分发问题。
