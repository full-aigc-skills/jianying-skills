# TRACE 迁移评估

评估器：`skill-trace-evaluation/scripts/trace_evaluate.py`，确定性离线评分。

- 迁移前基线：`99fb872c00ff14dbaf5b854327fc873877dfe309`。
- 迁移后对象：`v2.0.0` 发布候选工作树；对应 canonical manifest 状态为 `release_candidate`。
- 评估日期：2026-09-20。

## 汇总

| 维度 | 迁移前 | 初版迁移 | 发布候选 | 相对迁移前 |
|---|---:|---:|---:|---:|
| Trust | 4.369 | 4.356 | 4.806 | +0.437 |
| Reliability | 3.535 | 3.546 | 4.580 | +1.045 |
| Adaptability | 4.330 | 4.330 | 4.450 | +0.120 |
| Convention | 3.758 | 3.988 | 4.670 | +0.912 |
| Effectiveness | 3.812 | 3.888 | 4.400 | +0.588 |
| Overall | 3.962 | 4.022 | 4.585 | +0.623 |

发布候选在初版迁移基础上补齐了使用时机、能力边界、六步工作流、规则、Gotchas、验证清单、
成功/恢复/拒绝边界示例，并把细节放入按需 references。运行时真实性仍由 capability、来源和证据门禁承担，
不通过夸大 CLI 能力换取分数。

## 逐技能 Overall

| 技能 | 迁移前 | 初版迁移 | 发布候选 |
|---|---:|---:|---:|
| jianying-audio | 3.93 | 4.02 | 4.58 |
| jianying-draft | 3.97 | 4.01 | 4.58 |
| jianying-edit | 3.93 | 4.02 | 4.58 |
| jianying-export-prep | 3.99 | 4.02 | 4.58 |
| jianying-harness | 4.01 | 4.02 | 4.58 |
| jianying-inspect | 3.96 | 4.02 | 4.58 |
| jianying-motion | 3.93 | 4.06 | 4.61 |
| jianying-narration | 3.97 | 4.02 | 4.58 |
| jianying-recover | 3.97 | 4.02 | 4.58 |
| jianying-setup | 3.93 | 3.97 | 4.58 |
| jianying-subtitles | 3.97 | 4.06 | 4.61 |
| jianying-transitions | 3.93 | 4.02 | 4.58 |
| jianying-use | 4.01 | 4.02 | 4.58 |

## 门禁与剩余证据

13 个技能全部达到 4.5 门槛，最低 4.58、最高 4.61。CI 固定 TRACE 评估器 commit，任何技能正文变更都会重新评分。
以下运行时证据仍未完成，不以离线评分代替：

- Codex、ZCode、Kimi 的隔离单技能安装已完成，Codex/ZCode 已取得宿主发现证据，
  Kimi 已取得安装与 skill feature 激活证据；需要模型参与的简单任务、恢复和原生导出授权
  行为验收仍未执行。详见 `HOST_ACCEPTANCE_STATUS.md`。
- 原生剪映冷重开、播放、导出和 Windows Runtime Profile 仍受外部环境门禁限制。
- `partial` capability 的领域技能只能提供停止/诊断路径，不能通过夸大支持状态换取更高评分。
- 发布后的真实安装数据、触发准确率和恢复成功率尚未形成线上证据。

因此本报告证明技能文档质量门禁已通过，但不把 TRACE 分数当作三宿主或剪映原生运行时完成证明。
