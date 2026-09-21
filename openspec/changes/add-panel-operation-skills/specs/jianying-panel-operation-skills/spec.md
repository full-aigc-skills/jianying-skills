## Purpose

把剪映面板中的功能分类转化为可发现、可编排、可验证且不夸大能力的独立 Agent Skills。

## ADDED Requirements

### Requirement: 面板分类必须一类一技能

系统 SHALL 为素材、音频、文本、贴纸、特效、转场、字幕、智能包装、滤镜、调节、模板、数字人和剪辑控制台提供 13 个独立技能入口。音频、转场、字幕可以复用既有技能名，其余分类必须拥有独立技能。

#### Scenario: 用户要求导入子草稿
- **WHEN** 用户提出“素材 → 导入 → 子草稿”
- **THEN** 路由到素材技能，并根据整草稿或指定轨道选择 `project concat` 或 `template import-track`，不得退回笼统剪辑说明

### Requirement: 每项功能必须提供完整操作动线

每个分类技能 SHALL 使用稳定语义动作 ID 记录入口、前置事实、发现/筛选、预览或下载、执行路由、参数、确认点、成功证据、撤销和恢复。动线不得只列功能名称或屏幕坐标。

#### Scenario: 官方贴纸尚未下载
- **WHEN** 用户选择一个官方贴纸资源
- **THEN** 动线先检索和筛选候选，再预览、校验权益、触发下载、登记收据，最后才允许加入隔离草稿并验证资源身份

### Requirement: CLI 与 GUI 能力边界必须真实

系统 SHALL 以已发布 CLI 的命令目录和 capability manifest 为原子能力事实源。supported 能力可以生成固定 argv；partial、external_dependency、缺失能力或只有坐标的操作必须保持门禁，并说明版本绑定 GUI Adapter 或人工路径。

#### Scenario: 调节面板没有稳定 CLI 原子命令
- **WHEN** 用户要求修改曝光或色温而当前 capability 未 supported
- **THEN** 技能生成版本绑定的调节计划并停在 GUI Adapter/Canary 门禁，不得用滤镜命令冒充调节已完成

### Requirement: 技能必须支持粒度安装和不可变消费

每个分类技能 SHALL 在自身目录内包含入口、工作流参考和最小 Job 示例，不通过相对路径依赖兄弟技能。插件 SHALL 只从不可变技能 Release 导入并校验逐目录摘要。

#### Scenario: 单独安装数字人技能
- **WHEN** 只安装 `jianying-digital-human`
- **THEN** 其授权、费用、上传、任务恢复和证据说明仍完整可读，不要求相邻技能目录存在
