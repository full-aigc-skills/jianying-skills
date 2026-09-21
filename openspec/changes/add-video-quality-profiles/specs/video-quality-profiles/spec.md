## Purpose

为剪映场景化质量循环提供来源可追溯、可锁定、不可携带执行权的评审档案，使不同视频用途拥有独立硬门禁和证据要求。

## ADDED Requirements

### Requirement: PROFILE-01 版本化档案与完整性

质量档案集合 SHALL 有版本化 Schema；每个 profile SHALL 有唯一身份、SemVer、维度、动作、人工边界、代表工作流和来源引用。未知字段、重复身份、未知来源或未知工作流 MUST 拒绝。

#### Scenario: 正式目录通过

- **WHEN** 三个首批 profile 的身份、引用、Schema 和内容均有效
- **THEN** 校验器输出稳定内容摘要并允许进入技能发布清单

### Requirement: PROFILE-02 硬门禁与证据

每个维度 SHALL 声明权重、阈值、是否硬门禁及所需证据。硬门禁 MUST NOT 因其他维度高分而自动通过；缺专业、语言、版权或用途判断时 SHALL 保留人工边界。

#### Scenario: 婚礼商业许可缺失

- **WHEN** 商业广告分支没有用途和人物/音乐许可证据
- **THEN** profile 要求保持阻塞，不能用情绪或画面评分抵消

### Requirement: PROFILE-03 知识不得获得执行权

Profile SHALL 只列受信建议动作类别，MUST NOT 包含命令、脚本、handler、任意模型供应商配置、用户批准、素材时间码或运行成功声明。

#### Scenario: 档案夹带命令

- **WHEN** profile 出现 shell、handler、已批准或执行参数
- **THEN** 校验失败，插件不得消费或自动修复该档案

