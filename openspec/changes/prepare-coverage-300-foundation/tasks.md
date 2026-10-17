# 前置收口任务

## 1. v2 执行绑定

- [x] 1.1 为"场景缺少执行绑定"与"回填值冲突"编写失败优先测试
- [x] 1.2 在 `planning-catalog-v2.schema.json` 增加 `skills`、`required_capabilities`、
      `beats`、`editorial_intent` 并设为必填非空
- [x] 1.3 实现 `scripts/backfill_scene_binding.py`：按 `legacy_ids` 连接 v1 冻结目录回填，
      幂等、不修改 v1、冲突时返回 `scene_backfill_conflict`
- [x] 1.4 对现有 108 条执行回填并验证目录差异仅新增四个字段
      （回填后复跑 `filled: 0`，v1 冻结文件 SHA-256 未变，目录 diff 为 2600 行纯新增）

## 2. 内容一致性门禁

- [x] 2.1 为"例文缺少剪辑取舍原则""来源未出现在正文""测试夹具跳过正文检查"编写失败优先测试
- [x] 2.2 在 `validate_open_catalog.py` 实现 `scene_example_disagrees` 与
      `scene_source_not_cited`，复用既有 `safe_file` 边界
- [x] 2.3 确认 `test_fixture` 在 `--allow-test` 下跳过正文检查，其余检查不受影响
- [x] 2.4 门禁在真实 108 条上直接通过（`{"ok": true, "errors": []}`），证明 v1 时期
      的正文一致性保证在存量内容上成立

## 3. 场景骨架生成器

- [x] 3.1 为完整输入产出合规例文、缺来源拒绝、缺语义字段拒绝、重复生成幂等、
      已存在文件不覆盖编写失败优先测试
- [x] 3.2 实现 `scripts/gen_scene_scaffold.py`，输出七段式骨架与不可变段
- [x] 3.3 验证生成结果可直接通过 v2 目录校验（`test_generated_example_survives_catalog_validation`）
- [x] 3.4 以 VG01/TR01 等存量场景反向验证房屋风格：除热度行采用来源记录内逐源 `scope`
      （比原固定模板句信息量更大）外无结构性差异

## 4. 规模陈述

- [x] 4.1 更新 `SKILL.md`、`references/scene-index.md`、`docs/video-scenarios/SEED_MAPPING.md`、
      `README.md`、`README.zh-CN.md`、`docs/VIDEO_PLANNING_VALIDATION.md`，
      移除"108 是上限"的表述并标注以目录为准
- [x] 4.2 确认 v1 冻结目录未被本变更修改（`validate_video_catalog.py` 仍为 108 且 0 错误；
      定点的历史验证文档保留原始数字并加注指向当前事实源）

## 5. 门禁回归

- [x] 5.1 运行 `lint_skills.py`、`unittest discover -s tests`、`validate_open_catalog.py`、
      `skill_manifest.py check`（74 项测试通过，2 项因本机无符号链接权限跳过）
- [x] 5.2 运行 `validate_video_catalog.py` 确认 v1 冻结基线仍为 108 且零错误
- [ ] 5.3 运行 `trace_gate.py` 确认门槛未被放宽
- [ ] 5.4 运行 OpenSpec 严格校验

## 6. 跨平台缺陷修复（非本变更目标，但阻塞门禁）

- [x] 6.1 `validate_video_catalog.py` 用 `as_posix()` 生成相对路径，修正 Windows 反斜杠误判
- [x] 6.2 `test_frozen_v1_bytes` 按统一换行后比对摘要，区分检出策略与内容改动
- [x] 6.3 两处符号链接用例在本机无权限时显式 `skipTest`，不删除安全检查
