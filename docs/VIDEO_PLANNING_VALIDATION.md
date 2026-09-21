# 108 场景规划验证

日期：2026-09-21；候选版本：2.1.0；规格：add-video-planning-skill。

- 18 个家族、108 个独立 Markdown 场景文件、12 个 Recipe；每场景有独立检索词与来源记录。
- 18 个来源有播放/点赞/使用量快照，其余 90 个标 popularity_unverified；不是108个已证实热门案例。
- 具体网页访问失败时退回已返回的搜索摘录并标 search_excerpt；没有观看完整视频，没有下载或复制源媒体。
- 108 项方案为本项目独立改编，不是已执行的成片；人工判断、外部工具与 Rust 原子能力分开。
- 公开二进制 v1.6.13 capability 快照校验全部能力 ID；未访问 Rust 源码来充当用户侧能力。
- 内容校验、粒度安装复制验证、5 项新测试与24项原测试通过，共29项。
- lint_skills：14个技能、0错误；manifest 内容摘要检查通过；OpenSpec严格校验通过。
- TRACE：新规划技能4.50，包平均4.579，现有4.5门槛未降低。
- skill-creator quick_validate 因现有 Python 缺少 PyYAML 无法运行；未擅自安装。现有包 lint 已验证 frontmatter、名称、入口和本地资源链接。

尚未证明：108场景各自的剪映冷重开、播放、原生导出及三宿主真实行为，不能由上述静态测试推导。

## 正式发布—消费证据

- 不可变 Release：v2.1.0；源码 commit：686e5e0b68e7b8cc31b853bc43b759d2c6e29ddc。
- GitHub skill-lint 35558232249 和 release-skills 35558282294 均成功。
- Release manifest SHA-256：d1122fa4e829283cea17ed1130bf5c9da51526facb738775a30d4d7a7a5f4eea。
- 内容聚合 SHA-256：34149aa1d7d1932c06d1753bd3714547364d7b383d48ae3f022cd70f38cf787b。
- gh release verify-asset 通过；全新 GitHub tag 克隆重新生成 released manifest，与下载资产逐字节一致。
- 全新克隆中108文件校验通过；插件通过正式导入器锁定此版本，默认规划入口返回 locked_release，不依赖源仓路径。
- 插件本体0.18.0仍是发布候选，技能Release成功不等于插件市场发布或三宿主验收通过。
