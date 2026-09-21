# 开放目录首批实现验证

核对日期：2026-09-21。范围为本地工作树，不是发布、安装或真实成片证明。
当前记账 17/20；只更新本变更，不改变历史迁移计数。

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
| 5.1 | 本节命令及下列检查通过；只证明当前本地增量，不代表余下任务通过 |

本轮重新执行以下检查：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/lint_skills.py
python3 scripts/validate_video_catalog.py
python3 scripts/validate_open_catalog.py
python3 scripts/skill_manifest.py check
markdownlint-cli2 'openspec/changes/evolve-open-scenario-catalog/**/*.md'
openspec validate evolve-open-scenario-catalog --strict
git diff --check
```

单元测试 41/41；14 个技能 lint 通过；旧目录 108 场景、开放目录均零错误；
14 个技能内容摘要验证通过。配套插件 Node 回归 192 项：188 通过、4 跳过、0 失败。
负例断言的失败代码包括 `catalog_identity_conflict`、`catalog_reference_invalid`、
`unsupported_catalog_schema`、`catalog_empty`、`catalog_path_invalid`、
`catalog_resource_limit`、`catalog_duplicate_key`；测试拒绝本身是预期结果。

## 未勾选项和下一步

- 5.2 至 5.4：新版本不可变发布、插件正式干净安装以及旧锁回滚/规格同步尚未验收。

下一增量先补目录负例和 VLOG-01 知识向量，再由插件实现 WorkflowPlan 与编辑编译。
不能为消除数字缩减原验收标准；不归档未完成变更。
