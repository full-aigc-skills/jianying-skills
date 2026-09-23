# open-scenario-catalog Specification

## Purpose
为新消费者提供可扩容、可验证和可追溯的视频场景目录，同时保留旧消费者的固定种子基线。
使数量增长不破坏版本、来源、例文、安全引用和不可变发布的既有信任边界。
## Requirements
### Requirement: CAT-01 v2 数量解耦

v2 目录 SHALL 按声明的 Schema、唯一身份、引用完整性和资源限额判断有效性，
MUST NOT 要求固定 108 场景、18 家族、每类 6 项、12 Recipe 或一场景一来源。
合法目录 SHALL 非空；每个引用的集合必须存在对应对象，未引用的分类允许为空。

#### Scenario: 超过种子数量

- **WHEN** v2 fixture 含 109 或 1000 个合法场景，领域分布不均且 Recipe 数量变化
- **THEN** 校验通过且全部场景可检索，不截断成 108，也不强行均分家族

#### Scenario: 合法的小目录

- **WHEN** v2 fixture 只有 1 个合法场景及其完整依赖
- **THEN** 校验通过；空场景目录则返回 `catalog_empty`

### Requirement: CAT-02 双版本与冻结兼容

系统 SHALL 保留 v1 资源路径及原 108 个 ID、例文内容和语义基线，v2 SHALL 使用独立资源入口。
新消费者 SHALL 显式选择目录版本；未知版本 MUST 返回 `unsupported_catalog_schema`，不得猜测解析。
新合同与原固定计数要求的适用范围分别为 v2 与 v1，不能用新规则重新解释旧发布资产。

#### Scenario: 新技能包仍提供旧视图

- **WHEN** 旧消费者取得兼容发布包并按原路径读取 v1
- **THEN** 得到冻结的 108 项；新增 v2 场景不污染 v1 文件或旧结果

#### Scenario: 错把新目录送给旧解析器

- **WHEN** 目录解析器收到自己不支持的 Schema
- **THEN** 拒绝解析且不写草稿；已发布旧程序可保留原未知目录错误，新程序提供上述结构化代码

### Requirement: CAT-03 身份别名与多对多引用

每个 v2 场景 SHALL 有稳定 ID、非空名称、唯一的旧 ID 别名集合、example 路径、主 Recipe、
标签和至少一个直接方法来源。场景可有多个领域和来源；来源可被多个场景复用。
全局 ID/别名冲突、未知 Recipe、来源或标签 MUST 拒绝，不以最后写入值覆盖。

#### Scenario: 两个场景抢占 VG01

- **WHEN** 两个场景声明同一个旧 ID 别名 VG01
- **THEN** 返回 `catalog_identity_conflict` 并指出冲突对象

#### Scenario: 来源共享不导致丢失

- **WHEN** 两个场景引用同一来源且一个场景另有第二来源
- **THEN** 保留所有引用；不要求来源数量等于场景数量

### Requirement: CAT-04 数据和文件的安全边界

所有本地资源 SHALL 为技能根内的普通文件，并通过目录摘要与规范化路径检查。
绝对路径、父目录逃逸、符号链接和引用不存在资源 MUST 拒绝；URL 只能作来源，不自动下载或执行。
读取 SHALL 受字节、条目和单例正文上限约束，超限返回 `catalog_resource_limit`，不能部分静默接受。

#### Scenario: 恶意例文路径

- **WHEN** example 指向 `../outside.md`、绝对路径或根内指向外部的符号链接
- **THEN** 在读取正文前返回 `catalog_path_invalid`

#### Scenario: 超过配置的读取上限

- **WHEN** 索引超过本机已声明上限
- **THEN** 明确给出超限类别，不继续完整加载或截断后声称成功

### Requirement: CAT-05 发布与 provenance

正式消费 SHALL 验证正典来源、不可变发布身份和逐目录摘要；开发候选必须显式标识。
目录版本、技能 ref/commit/digest SHALL 随规划结果保留；内容修改不得继承旧正式 provenance。
旧 Release 不可改写；任何修正 SHALL 通过新版本和兼容审查交付。

#### Scenario: 本地内容被篡改

- **WHEN** 锁定技能内容与其摘要不一致
- **THEN** 拒绝正式消费，不自动回退到开发仓或网络同名内容

#### Scenario: 候选与正式隔离

- **WHEN** 测试使用显式开发目录
- **THEN** 输出标明开发候选，不满足正式分发或宿主验收门禁

