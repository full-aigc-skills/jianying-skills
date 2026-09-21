# Verification

## 2026-09-21 本地 apply 证据

- 红测：`python3 -m unittest tests.test_quality_profiles` 因质量档案校验器缺失失败。
- 质量档案测试：7/7 通过，覆盖稳定摘要、重复身份、未知引用、未注册动作、执行字段、硬门禁和三条代表工作流维度。
- 全量 Python 回归：47/47 通过。
- `validate_quality_profiles.py`：通过；目录 SHA-256 为 `91172d3ee45c02efe06edeb522e01115dc27297b458b8cd4fc89f84aec6ee1bb`。
- `validate_open_catalog.py`：通过。
- `lint_skills.py`：14 个技能、0 错误。
- `skill_manifest.py check`：14 个技能及内容摘要一致。
- `openspec validate add-video-quality-profiles --strict --no-interactive`：通过。

## 2026-09-21 不可变发布与消费证据

- commit `18645222c0d60c7577b0cefc86e08298c0f3d0c9` 发布为不可变 `v2.2.1`；GitHub Actions
  run `35588471656` 的 validate/publish 全部通过，Release 资产
  `jianying-skills.manifest.json` SHA-256 为
  `8e28dea343ccc6658d4bc6773af171602e4a2ea099e637cae8775a5f0aa09d4c`。
- 插件从 Release manifest 原子导入 14 个技能并锁定精确 commit；`jianying-video-planning`
  内容摘要为 `c3a6b91880514e28f625ba6b6de224f3ddccd0acdb4d8efda227b13781139935`。
- 在 `/tmp/jianying-plugin-skills-fresh.DbXoGb` 的无 Git、无上游源码安装副本中，发布门禁
  14/14、目录/路由 134/134 通过；Vlog、课程、婚礼三份 profile 与 Schema 均可从锁定技能读取。

## 2026-09-21 安装基线修复

- 首次用发布 CLI 做 fresh-install 握手时，`v2.2.1` 的包级聚合能力错误包含
  `captions.verify`、`render.native`、`runtime.profile`、`runtime.status` 等场景专属门禁，真实 CLI
  按设计分别报告 `partial` 或 `external_dependency`，因此安装应失败而不是伪造支持。
- `v2.2.2` 将 `install_cli_capabilities` 固定为 `capabilities`、`job.run`、`schema.job_v2`；
  各技能 `required_capabilities` 和完整 `minimum_cli_capabilities` 聚合仍保留，继续在具体工作流执行前门禁。
- commit `0f0ea4e2f2f9472fba5a03ec394721468ed7073a` 已发布为不可变 `v2.2.2`；Release manifest
  SHA-256 为 `ae62ff9b3a0a5596ade75789c0eb00431969d456e3f7be496a4a341d138e2d41`。
- 插件原子导入后，发布 CLI `v1.6.17` 从空安装目录下载并通过无 Cargo 握手；二进制 SHA-256
  `38dc87b4a3e82a833aec93d4c7175d7589d304762a786c72bcaee248a9412acb`，能力清单与运行时逐字一致。
