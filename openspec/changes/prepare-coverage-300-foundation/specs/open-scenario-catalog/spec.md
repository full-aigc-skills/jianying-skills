# open-scenario-catalog 增量规格

## Purpose

补回 v2 目录在替代 v1 时丢失的执行绑定与内容一致性门禁，使场景扩容到 300 时
既不会退化为纯知识文档，也不会让例文与目录失去互相校验。

## ADDED Requirements

### Requirement: CAT-06 场景执行绑定

每个 v2 场景 SHALL 声明 `skills`、`required_capabilities`、`beats` 与
`editorial_intent`，用于把场景路由到具体技能与 CLI capability。
`skills` 与 `required_capabilities` SHALL 非空；`beats` 与 `editorial_intent`
SHALL 非空且为非空字符串。缺失或为空 MUST 返回 `catalog_schema_invalid`。

绑定来源 SHALL 可追溯：对既有场景，四个字段的值必须与其 v1 冻结基线一致；
回填 MUST NOT 修改 v1 文件，且对已声明字段的场景保持幂等。

#### Scenario: 场景缺少执行绑定

- **WHEN** v2 场景声明了名称、领域与来源，但没有 `required_capabilities`
- **THEN** 返回 `catalog_schema_invalid` 并指出场景 ID，不接受"暂缺执行绑定"

#### Scenario: 回填保持幂等

- **WHEN** 回填脚本对已带四个字段的场景重复执行
- **THEN** 目录内容逐字节不变，v1 冻结目录亦不变

#### Scenario: 回填值与 v1 不一致

- **WHEN** 某场景的 v1 `edit` 与 v2 `editorial_intent` 同时存在且文本不同
- **THEN** 返回 `scene_backfill_conflict` 并指出场景 ID，不以任一侧覆盖另一侧

### Requirement: CAT-07 例文与目录内容一致

对 `status` 为 `published_knowledge` 的场景，校验 SHALL 读取本地例文正文，
并要求正文逐字包含 `editorial_intent` 与 `acceptance` 中的每一条；
场景引用的每个来源，其 `url` MUST 出现在正文中。
缺失分别返回 `scene_example_disagrees` 与 `scene_source_not_cited`。

读取 SHALL 复用既有路径与体积边界；`test_fixture` 场景在 `--allow-test` 下
MUST 跳过正文检查，门禁 MUST NOT 放宽为可选。

#### Scenario: 例文丢失剪辑取舍原则

- **WHEN** 场景目录声明了 `editorial_intent`，但例文正文只字未提
- **THEN** 返回 `scene_example_disagrees` 并指出场景 ID

#### Scenario: 来源只存在于目录

- **WHEN** 场景 `source_ids` 引用了一个来源，但例文正文没有引用其 URL
- **THEN** 返回 `scene_source_not_cited`；目录中的来源条目不因此被丢弃

#### Scenario: 测试夹具不被文档门禁阻断

- **WHEN** `--allow-test` 下目录含 `status` 为 `test_fixture` 的场景且例文未逐字对齐
- **THEN** 正文检查跳过，Schema 与引用完整性检查仍然执行

### Requirement: CAT-08 规模陈述不得成为上限

技能正文、场景索引、种子映射与 README SHALL 描述目录规模时以目录实际值为准，
MUST NOT 把某个具体数字表述为扩容上限。
同一数字在多处出现时 SHALL 由单一来源生成或明确标注其来源。

#### Scenario: 场景数增长到 300

- **WHEN** v2 目录扩容到 300 条
- **THEN** 校验与文档均无需为"108"做例外处理，正文表述不与目录冲突
