## Context

见 [proposal.md](proposal.md)。现有技能采用粒度安装，每个技能必须自包含；发布清单会摘要全部技能内容。研究基线没有 CodeGraph 索引，因此本变更只基于固定提交中的可读源码与规则提取概念，不能声称迁移其动态调用图。

## Goals / Non-Goals

**Goals:** 建立可锁定的辅助制作知识目录；让录屏事件、智能缩放和媒体预检拥有明确数据边界；把五条工作流路由到现有技能；用校验器阻止旧 Python 引擎和不安全资源重新进入发布包。

**Non-Goals:** 不实现录屏、浏览器渲染、转码、CV、TTS 或原生资源 Provider；不修改插件；不复制研究仓代码/资产；不宣称真实剪映、播放或导出已通过。

## Decisions

### 1. 一个机器目录，多个技能自包含合同

五条 Recipe 由 `jianying-video-planning` 的版本化 JSON 统一索引，事件/缩放和媒体预检 Schema 分别存放在 `jianying-motion` 与 `jianying-media`。这样路由有单一入口，同时粒度安装后的执行技能仍能独立解释自己的输入。

未采用新建单体 `jianying-editor` 技能，因为它会重复现有技能责任并模糊 Skills 与 Harness 权限。

### 2. 只保存知识步骤，不保存可执行命令

Recipe 使用受限步骤 ID 和 capability ID，不携带 shell、argv、handler、凭据、批准或成功状态。插件后续根据不可变 Skills lock 把步骤编译成 `WorkflowPlan`；CLI 再以发布 capability 决定是否可执行。

```mermaid
flowchart LR
    BRIEF[创作简报] --> RECIPE[辅助制作 Recipe]
    RECIPE --> CONTRACT[事件/媒体知识合同]
    CONTRACT --> HARNESS[插件 Harness]
    HARNESS --> PROVIDER[受控 Provider]
    PROVIDER --> LEDGER[素材与事件账本]
    LEDGER --> PLAN[WorkflowPlan]
    PLAN --> JOB[jianying-job/v2]
    JOB --> CLI[不可变 Rust CLI]
    CLI --> DRAFT[隔离草稿]
    DRAFT --> VERIFY[冷重开/播放/导出]
```

### 3. 智能缩放采用两阶段合同

`interaction-events/v1` 只描述捕获事实；`smart-zoom-plan/v1` 只描述确定性规划结果。两者以录屏内容摘要和时间基准绑定，防止把其他录屏的点击账本误用于当前素材。位置统一为捕获区域内归一化坐标，显示器像素、HiDPI 与窗口偏移作为显式映射证据。

研究仓的 5 秒分组、1.5 倍缩放和跟随阈值只视为启发，不成为默认真理；本合同要求这些值显式记录并受可访问性、黑边与人工删减门禁约束。

### 4. 媒体标准化必须是显式派生关系

`media-preflight/v1` 同时保存源与派生媒体内容 SHA-256、探测事实、转换参数和质量比较。预检可建议 WebM→兼容格式，但不静默执行；原文件保留。未采用研究仓的路径 MD5 命名和“同尺寸即复用”，因为它们不能证明内容身份。

### 5. 来源说明进入包级门禁

包级来源记录声明 MIT 研究仓与内嵌 Apache-2.0 组件，并列出没有复制的资源类别。校验器扫描正式技能内容，拒绝 Python 草稿入口、外部 headless、研究仓数据文件和执行字段。该门禁验证的是本包边界，不替代上游逐文件法律审查。

## Risks / Trade-offs

- [知识 Schema 先于插件实现] → 明确 `provider_required`/`plan_only`，不把目录存在当能力证据。
- [跨技能内容重复] → 机器目录只在规划技能保存，执行技能仅保存本领域 Schema 与最小例子。
- [研究算法参数被误当最佳实践] → 参数必须在计划中显式给出并经过素材、可访问性和播放门禁。
- [新参考文件漏出发布摘要] → 运行 `skill_manifest` 完整性测试和粒度复制校验。
- [已有工作区改动冲突] → 只添加新 change 和新参考文件；对现有 SKILL 的修改限制为局部链接与路由段落。

## Migration Plan

1. 先加入负例测试与空缺断言，确认当前失败。
2. 加入来源记录、知识目录、Schema、示例与领域参考。
3. 更新九个现有技能的局部路由，不改变原子 capability 所有权。
4. 运行严格 OpenSpec、技能 lint、目录校验、单测、粒度安装与内容摘要回归。
5. 本地验证后保持未发布；待不可变 Skills Release 创建并由插件 fresh install 锁定消费后，完成最终任务并归档。

回滚只需让插件继续锁定旧 Skills Release；已发布版本不可覆写。
