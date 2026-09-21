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
