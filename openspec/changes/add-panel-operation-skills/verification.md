# 验证记录

## 2026-09-22：本地候选

- 分类：13 个面板分类均有独立技能入口；音频、转场、字幕增强既有技能，其余新增 10 个技能。
- 动线：13 个 `references/workflow.md` 共登记 106 个唯一语义动作 ID；每类至少 6 条，均含入口、前置事实、执行路由、验证和恢复。
- CLI 事实源：下载并校验不可变 `jianying-cli v1.6.19` darwin-arm64 制品，
  二进制 SHA-256
  `3582b57e471b206c068bb1fb304c41dd79ef65a62317946bba69bef8852deee2`；
  使用其发布 `provenance/CAPABILITIES.json` 校验全部矩阵 capability ID。
- TDD 红灯：新增测试最初报告 14 != 24、`jianying-media` 工作流缺失和 manifest 仅 14 项；实现后聚焦测试转绿。
- 技能 lint：24 skills，契约矩阵 0 error；带发布 capability manifest 再校验仍为 0 error。
- 单元测试：`python3 -m unittest discover -s tests -v`，51/51 通过。
- TRACE：24 个技能平均 4.588、最低 4.51，阈值 4.50，通过。
- OpenSpec：`openspec validate add-panel-operation-skills --strict` 通过；
  `git diff --check` 通过。

## 发布与插件消费

- `v2.3.0` 已在 commit
  `23e6ce195f5e3ef3c003d58bf262620f8603735a` 发布为 GitHub Immutable Release；
  发布清单 SHA-256 为
  `889504f710c5b31c8ecfcee0f06bf947fcb070556aaa8c2f2b3a9a851b1341ce`，
  `gh release verify-asset` 验证通过。
- 插件已从上述 Release 原子导入 24 个技能，锁定 `v2.3.0` 和 commit
  `23e6ce195f5e3ef3c003d58bf262620f8603735a`。`skill_vendor.py check`
  在线与离线摘要检查均通过，没有手改 vendored 副本。
- 使用远端 `v0.25.0` tag 对应 commit
  `d3ab18487e0126bc53ad9085e58097fd11c712e0` 构造隔离插件归档；归档包含
  502 个文件和 24 个技能，Rust-only 审计通过，SHA-256 为
  `58e93c7eb874b7ca6354106e9a8c57c48cfac0b317b26f02c677e46a481b9ef5`。
- 在 `/tmp/jianying-panel-fresh-install.J1Oect` 解压归档后执行 fresh-install。
  发布 CLI `v1.6.19` 在 `PATH=/usr/bin:/bin`、无 Cargo 条件下完成 version、
  capability 与 Skills 最低合同握手；运行来源为 `installed_fallback`，
  `cargoAvailableInHandshakePath=false`。
- 以上证据完成任务 4.2，但不等于插件 GitHub Release 或三宿主验收。
  插件 `v0.25.0` GitHub Release 仍不存在；正式发布仍受插件仓 ruleset API
  的 GitHub 计划级 403 阻塞。
- 技能发布工作流的构建、TRACE、Release 和 asset attestation 均成功；最后的
  consumer dispatch 因同步 token 无法看到插件仓而返回 404。本轮使用同一不可变
  manifest 手动导入，不影响已发布 Release 完整性。
- 任务 4.3 仍未完成：Codex/ZCode/Kimi 正式 `v0.25.0` 安装包的 13 分类
  发现、路由、停止、恢复和证据展示尚未验收。
- 调节、智能包装、数字人和部分官方资源应用仍受发布 capability 中的
  partial/external/GUI 门禁约束；技能明确停在对应门禁，不声称已底层执行。
