# 场景目录扩容前置与执行绑定

## Why

108 个场景之所以长期停在"知识文档"，不是因为数量不够，而是因为 v2 目录在替代 v1 时
丢掉了决定场景**怎么真正执行**的四个字段。v1 的 `skills`、`required_capabilities`、
`beats` 和 `edit`（剪辑取舍原则）在 v2 中没有对应物，场景因此无法绑定到具体技能与
CLI capability，智能体拿到场景后仍不知道该调用什么。

同时内容门禁出现了净损失：v1 校验器强制"例文正文必须逐字包含目录里的 `edit` 与
`acceptance`"以及"来源 URL 必须出现在正文"，v2 校验器没有这两条。一旦 v2 成为扩容
的唯一事实源，文档与目录就会失去一致性约束。

现有规格 CAT-02 要求 v1 作为冻结基线保留给旧消费者，因此 v1 不退役、不修改；本次
变更只把门禁与执行绑定落到 v2，让扩容从 108 走向 300 时不退化。

## What Changes

- v2 场景 Schema 新增四个执行绑定字段 `skills`、`required_capabilities`、`beats`、
  `editorial_intent`，并从 v1 冻结目录回填现有 108 条。
- v2 校验器补回两条内容门禁：例文正文必须逐字包含 `editorial_intent` 与每条
  `acceptance`；引用来源的 URL 必须出现在例文正文中。
- 新增场景骨架生成器，以 Recipe、领域、素材清单和来源记录为输入产出合规例文，
  把单篇人工成本从整篇写作压缩到语义字段与来源核实。
- 同步技能正文、场景索引、种子映射与中英文 README 中写死的"108"表述。
- v1 目录、例文与其校验器保持冻结不变，作为旧消费者的兼容基线。

## Capabilities

### New Capabilities

- `scenario-scaffold-generation`: 定义场景例文的骨架生成、模板不可变段与人工字段边界。

### Modified Capabilities

- `open-scenario-catalog`: v2 场景新增执行绑定字段，恢复内容一致性门禁。

## Non-goals

- 本变更不新增第 109 个及以后的场景，扩容属于 `scale-scenarios-to-300`。
- 不修改、删除或重新编号 v1 冻结目录的任何条目。
- 不放宽现有安全边界、来源约束或 TRACE 门槛。
- 不宣称任何场景已完成真实剪映端到端验收。

## Impact

- 规格：`open-scenario-catalog`、`scenario-scaffold-generation`。
- 数据：`planning-catalog-v2.json`、`planning-catalog-v2.schema.json`。
- 脚本：`scripts/validate_open_catalog.py`、新增 `scripts/gen_scene_scaffold.py`。
- 测试：`tests/test_open_catalog.py`、新增骨架生成器用例。
- 正文：`SKILL.md`、`references/scene-index.md`、`docs/video-scenarios/SEED_MAPPING.md`、
  `README.md`、`README.zh-CN.md`、`docs/VIDEO_PLANNING_VALIDATION.md`。
- 消费方：`jianying-edit-plugin` 锁定导入新技能版本后按新字段编译工作流。
