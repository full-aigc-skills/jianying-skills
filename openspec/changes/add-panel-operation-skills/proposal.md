## Why

现有技能主要按工程阶段划分，不能让智能体直接从剪映面板分类进入具体功能。用户需要素材、音频、文本、贴纸、特效、转场、字幕、智能包装、滤镜、调节、模板、数字人和剪辑控制台各自拥有独立技能，并把“素材 → 导入 → 素材”“素材 → 导入 → 子草稿”这类逐级操作动线写清楚。

## What Changes

- 建立 13 个剪映面板分类的技能入口；复用并增强已有音频、转场和字幕技能，新增其余 10 个技能。
- 每个技能定义语义动作 ID、入口、发现/筛选、下载或预览、参数、执行路由、验证与撤销/恢复动线。
- 所有命令以已发布 `jianying-cli` 命令目录和 capability manifest 为事实源；未支持能力显式路由到版本绑定 GUI Adapter 或保持阻断。
- 保持技能仓为正文唯一来源，插件只消费不可变发布和逐目录摘要。

## Capabilities

### New Capabilities

- `jianying-panel-operation-skills`: 面向剪映面板分类、可由智能体检索和编排的逐功能操作技能族。

### Modified Capabilities

- `canonical-rust-cli-skills`: 扩展可发现技能集合和 Rust CLI/GUI Adapter 路由说明。
- `skill-distribution-lock`: 新技能必须随不可变技能发布进入插件锁定快照。

## Impact

影响技能目录、契约矩阵、包清单、README、发布 manifest、插件技能锁与三宿主安装验收。不会在技能中实现第二套剪辑引擎，也不会把只有坐标的 GUI 操作写成稳定能力。
