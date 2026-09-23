# 开放目录首批实现验证

核对日期：2026-09-22。范围为本地工作树和已发布不可变技能制品，
不是插件三宿主或真实成片证明。当前记账 20/20；只更新本变更，不改变历史迁移计数。

## 环境与输入

- Node v24.18.0；Python 3.14.3；OpenSpec 1.8.0。
- 技能包候选 2.2.0；目录 revision 为 `2.2.0-candidate`。
- 旧基线为本地 Git tag `v2.1.0`；113 个资源逐个通过 `git show` 读取并核对 SHA-256。
- 108 个旧 ID、名称、Recipe、例文路径及字节未变；没有新增热门案例。
- v2 索引 SHA-256：`85951a0d0123a658fca4aa83b6672e87d1fa56e660111b512969a142144177d3`。
- 候选清单文件 SHA-256：`83aaf19147948a07a0fb443bf9d2706b5cadba12a7f11f0df92bc4a82c8ce872`。

## 开发合同向量所有权

目录 Schema 与测试数据的唯一维护源在本 Skills 仓。
插件 `tests/fixtures` 中对应文件只是本次开发向量的逐字节快照，不是第二套规范或发布资产。
更改应先在 Skills 完成合同验证，再同步快照与固定摘要；禁止单独放宽插件快照 Schema。
插件显式开发读取返回 `provenance.kind=development_candidate`、`production_ready=false`。

- `tests/fixtures/open_catalog_v2.json` → 插件同名快照；SHA-256：
  `084ed9a37893f04a0314a11f63c38414c05d319671b23a51e45ea8b50c26f374`。
- `tests/fixtures/legacy_planning_v1.json` → 插件同名快照；SHA-256：
  `538f406e88b15202b449b9616c857cd91a160d602b1d3708f3c9880e77185337`。
- `references/planning-catalog-v2.schema.json` → `open_catalog_v2.schema.json`；
  SHA-256：`b06c91befdf38b37b527ed1fadaa977aa65678b83e7351627f24ea85a8a31377`。

Schema 路径相对于 `skills/jianying-video-planning`；其他路径相对于仓库根。
核对时三对文件均字节一致。扩容测试为合成 fixture，不能作为正式收录或热度证据。

## 已完成项与证据

| 任务 | 实现与测试证据 |
| --- | --- |
| 1.1、2.4 | 冻结字节与迁移映射测试；Git tag 113 文件复核；插件 108 路由回归 |
| 1.3、2.1、2.2、2.3 | 身份、引用、版本、路径、重复键、限额及扩容正反例 |
| 3.1 | 上述三个跨仓向量字节核对，插件开发来源与正式来源分离测试 |
| 3.3 | `test_manifest_refuses_invalid_open_catalog`、完整清单检查；插件锁定内容篡改拒绝测试 |
| 3.4 | 插件缺 v2 明确失败、锁不变、开发结果不能通过生产 readiness；不自动回退 |
| 1.2、2.5 | 1/109/1000 非均分及独立 Recipe/来源数量；正式来源缺方法、热度依据或误用 fixture 均拒绝 |
| 3.2 | 插件 v1 冻结回归、v2 开放数量、旧包缺 v2、未知版本与篡改矩阵通过 |
| 4.1 至 4.3 | `representative-workflows-v1.json` 三条知识向量及场景、Recipe、输出和等待条件断言通过 |
| 4.4 | SKILL/中英文 README/覆盖计划已区分正式知识、fixture 与运行证据；全仓 Markdown 相对链接审计零断链 |
| 5.2 | GitHub Immutable Release `v2.2.0`；manifest attestation 通过 |
| 5.3 | 插件由正式 Release 原子导入 14 技能并校验摘要；锁定 v2.2.0 后 v1 108 回归与 v2 开放矩阵 20/20 |
| 5.4 | 真实 Release 回滚/重升级；v1、锁和 Release 身份均通过复核 |
| 5.1 | 本节命令及下列检查通过；只证明当前本地增量，不代表余下任务通过 |

## 真实 Release 回滚与重升级演练

演练目录：`/tmp/jianying-catalog-rollback.fSb8FD`。该目录是隔离副本，未修改工作仓库、
Git tag、GitHub Release 或远端设置。执行顺序和结果如下：

1. 从 GitHub 下载 `v2.1.0`、`v2.2.0` 的正式 `jianying-skills.manifest.json`，
   并从本地不可变 tag 建立 detached checkout。
2. 先把临时插件锁定导入 `v2.2.0`，再回退到 `v2.1.0`，最后重新导入 `v2.2.0`。
3. 每个阶段逐个核对 `tests/fixtures/legacy_planning_v1.json` 记录的 113 个文件；
   v1 均保持 108 场景和原摘要。
4. 回退后旧消费者正常读取 v1，v2 入口明确返回 `catalog_v2_unavailable`；
   重新升级后 v1 仍为 108 场景，v2 由 `locked_release` provenance 正常读取。
5. 初次导入与重新升级的 `skills.lock.json` SHA-256 均为
   `48183f813eb66c6f29cda27d69df3f9019bf0bc8a02d01e25e0f785648c717d1`，
   且无残留 `.skills-backup-*` 或 `jianying-skill-import-*` 目录。

远端前后两次查询结果一致：

- `v2.1.0`：immutable；manifest SHA-256
  `d1122fa4e829283cea17ed1130bf5c9da51526facb738775a30d4d7a7a5f4eea`。
- `v2.2.0`：immutable；manifest SHA-256
  `883489de386fdbaf5088b43f39d560fa9038dbe3d7f0c9c52ebb9e5902b73dc3`。

这证明回滚只切换插件的锁与 vendored 技能，不改写旧 Release；旧包不会读取 v2，
兼容发布也不会把 v2 内容灌入冻结 v1。

本轮重新执行以下检查：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/lint_skills.py
python3 scripts/validate_video_catalog.py
python3 scripts/validate_open_catalog.py
python3 scripts/skill_manifest.py check
npm exec --offline --yes markdownlint-cli2 -- \
  'openspec/changes/evolve-open-scenario-catalog/**/*.md'
openspec validate evolve-open-scenario-catalog --strict
git diff --check
```

单元测试 51/51；24 个技能 lint 通过；旧目录 108 场景、开放目录均零错误；
24 个技能内容摘要验证通过。配套插件 Python 70/70；Node 回归 302 项：
295 通过、7 个真实环境用例跳过、0 失败。
负例断言的失败代码包括 `catalog_identity_conflict`、`catalog_reference_invalid`、
`unsupported_catalog_schema`、`catalog_empty`、`catalog_path_invalid`、
`catalog_resource_limit`、`catalog_duplicate_key`；测试拒绝本身是预期结果。

## 变更边界和后续

本变更的目录兼容、正式发布、锁定消费和回滚要求已经形成独立证据；严格校验通过后可同步并归档。
插件 WorkflowPlan、三宿主和真实成片仍属于插件侧变更，不因本 Skills 变更归档而自动完成。
