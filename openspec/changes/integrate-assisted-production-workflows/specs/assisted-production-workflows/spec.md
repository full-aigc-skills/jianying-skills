## Purpose

为录屏、智能缩放、Web 动效、媒体标准化、影视解说、曝光匹配和模板批产提供来源可追溯、可机器校验、不能越权执行的剪映技能知识合同。

## ADDED Requirements

### Requirement: APW-01 来源与重写边界

技能包 SHALL 固定研究来源仓库、提交、许可证和采用方式，并 SHALL 明确禁止复制 Python 运行时、内嵌草稿引擎、UI 自动化脚本、云下载脚本、缓存资源数据库、专有媒体和效果资源。来源知识 MUST 经过独立重写，不能因上游整体许可证而推断第三方资源可再分发。

#### Scenario: 来源基线完整

- **WHEN** 校验辅助制作知识目录
- **THEN** 来源记录包含固定提交、许可证、允许吸收范围、禁止复制范围和 Rust-only 目标边界

#### Scenario: 目录夹带旧运行时

- **WHEN** 技能正文、示例或知识目录引用 Python 草稿运行时、外部 headless checkout 或研究仓资源数据库
- **THEN** 校验失败且内容不得进入发布清单

### Requirement: APW-02 五条辅助制作 Recipe

技能包 SHALL 提供软件教程录屏、README 安装教程、产品演示智能缩放、Web 数据可视化片头、影视解说与 B-roll 匹配五条版本化 Recipe。每条 Recipe MUST 声明输入事实、知识步骤、责任技能、所需 capability、人工门禁、目标证据和未实现边界；Recipe MUST NOT 携带命令字符串、用户批准或运行成功声明。

#### Scenario: Recipe 可独立路由

- **WHEN** 只安装 `jianying-video-planning` 并读取辅助制作目录
- **THEN** 五条 Recipe 均可从用户意图路由到自包含的责任技能、步骤与停止条件

#### Scenario: Provider 未安装

- **WHEN** Recipe 需要录屏、浏览器渲染或模型分析而插件没有对应 Provider
- **THEN** Recipe 保持 `provider_required` 或 `plan_only`，不得降级为伪造素材或自由 shell 命令

### Requirement: APW-03 交互事件与智能缩放合同

技能包 SHALL 定义 `interaction-events/v1` 与 `smart-zoom-plan/v1` 的知识 Schema。事件 MUST 绑定录屏素材摘要、捕获范围、显示器缩放、窗口偏移、时间基准和归一化坐标；缩放计划 MUST 绑定项目 FPS、片段范围、最大缩放、黑边安全约束、去抖/分组规则、量化报告和人工删除入口。按键内容 MUST 默认禁止捕获。

#### Scenario: 合法事件生成可审查计划

- **WHEN** 事件账本包含有效素材摘要、视口映射、递增时间和归一化点击坐标
- **THEN** 规划器可生成不含草稿写入命令的确定性缩放计划，并要求后续 capability 与播放验证

#### Scenario: 坐标或时间不可复核

- **WHEN** 事件越出捕获区域、时间倒序、缺失 HiDPI 映射或包含按键内容
- **THEN** 校验失败且不得编译为关键帧

### Requirement: APW-04 媒体预检与标准化合同

技能包 SHALL 定义 `media-preflight/v1`，记录原始内容摘要、探测事实、兼容性结论、拟议转换、派生媒体摘要、质量差异、暂存策略和回滚路径。转换 MUST 显式批准，原文件 MUST 保留；路径摘要或同尺寸文件不能代替内容摘要。

#### Scenario: WebM 需要转换

- **WHEN** 探测结果表明 WebM 或其他素材与当前剪映能力不兼容
- **THEN** 预检输出显式转换计划、目标格式、质量边界和批准要求，不静默转码

#### Scenario: 派生媒体无法对账

- **WHEN** 转换后缺失内容摘要、探测结果或与源媒体的关系
- **THEN** 预检状态为阻塞且不得导入生产草稿

### Requirement: APW-05 安全 Provider 与原生资源边界

录屏知识 SHALL 要求精确屏幕/窗口/区域、系统音频选择、点击记录选择、隐私预览和原始媒体与事件账本分别授权。Web VFX 知识 SHALL 要求来源类型、Origin allowlist、浏览器沙箱、网络策略、超时、字体/脚本来源、分辨率、FPS、Alpha 和确定性摘要。原生资源知识 SHALL 要求资源身份、剪映版本、基础版/专业版权益、账号可用性、下载收据、用途许可和禁止再分发标记。

#### Scenario: 任意远程 Web 动效

- **WHEN** Web VFX 请求使用未在 allowlist 的远程 Origin 或未知第三方脚本
- **THEN** 工作流在渲染前阻塞，不以研究示例中的任意 CDN 策略继续

#### Scenario: 专业版资源候选

- **WHEN** 候选资源需要专业版权益或账号下载
- **THEN** 知识合同要求先取得当前账号权益和用途收据，再允许 Harness 请求应用

### Requirement: APW-06 Skills、Harness 与 Rust CLI 权限分离

Skills SHALL 只提供路由、知识、能力需求和验收规则；Harness SHALL 负责 Provider、审批、恢复、成本、隐私和证据账本；只有不可变发布的 Rust `jianying-cli` SHALL 修改草稿。Compound Clip 在发布二进制黑盒 capability 未为 `supported` 前 MUST 保持 `plan_only`。

#### Scenario: 从智能缩放计划进入执行

- **WHEN** 用户批准已校验的缩放计划
- **THEN** 插件只能将其编译为 `WorkflowPlan` 与 `jianying-job/v2`，再由锁定发布的 Rust CLI 执行并按目标追加播放或原生导出证据

#### Scenario: 知识文件夹带执行权

- **WHEN** 知识目录包含 handler、任意 argv、Provider 凭据、批准状态或已执行标记
- **THEN** 校验失败且插件不得消费该版本

