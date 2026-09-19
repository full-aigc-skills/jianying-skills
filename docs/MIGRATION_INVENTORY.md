# Rust CLI 技能迁移清点与处置记录

基线提交：`99fb872c00ff14dbaf5b854327fc873877dfe309`。下表的“原遗留叙事”仅用于保存迁移审计事实，
不是当前运行指南。当前 13 个技能正文已切换为单一 Rust CLI 契约。

| 技能 | 基线行数 | 原遗留执行叙事 | 当前处置 |
|---|---:|---|---|
| jianying-use | 60 | Python 预检、pyJianYingDraft 主路径、外部 headless 专业档 | 已删除；改为 capability 路由 |
| jianying-edit | 59 | `jydraft_run.py`、生成 Python 脚本 | 已删除；改为 `jianying-job/v2` |
| jianying-draft | 89 | pyJianYingDraft API 手册 | 已删除 API cookbook；改为 Rust 领域模型 |
| jianying-setup | 40 | Python 检查器、`JIANYING_HEADLESS_ROOT` | 已删除；改为 Rust doctor/runtime status |
| jianying-narration | 48 | pyJianYingDraft 片段生成 | 已删除；改为 ASR ledger + timeline edit |
| jianying-subtitles | 51 | pyJianYingDraft 文本 API | 已删除；改为 captions 命令组 |
| jianying-audio | 44 | pyJianYingDraft 音频 API | 已删除；改为 media/timeline capability |
| jianying-motion | 56 | pyJianYingDraft 关键帧 API | 已删除；改为 timeline capability 门禁 |
| jianying-transitions | 34 | pyJianYingDraft 转场 API | 已删除；改为 catalogue + transition gate |
| jianying-inspect | 39 | 混合引擎探测语义 | 已删除；改为只读 Rust 检查 |
| jianying-export-prep | 45 | Python/UIA 与外部导出边界 | 已删除旧路径；改为 proxy/native 分级门禁 |
| jianying-recover | 38 | pyJianYingDraft `allow_replace` 恢复语义 | 已删除；改为 task audit/snapshot restore |
| jianying-harness | 88 | 外部 headless Python 命令全集 | 已删除；改为 Rust jobs/approvals/config/MCP |

## 仓库级处置

- `README.md`、`README.zh-CN.md` 已改为 Rust CLI 单一架构。
- `THIRD_PARTY_NOTICES.md` 保留 Apache/MIT 声明义务，并明确非商业 headless 实现材料不作为迁移输入。
- 13 个技能均已物化本技能内的 `references/workflow.md` 和 `examples/minimal-job.json`。
- lint 和粒度安装测试持续阻止兄弟技能相对链接、资源缺失及旧运行依赖回归。

## 兼容决定

13 个现有名称和触发语义在本次迁移中全部保留。是否合并重叠入口必须等待触发准确率、安装数据和交接失败率评估，并另开主版本规格。
