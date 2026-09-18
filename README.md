# jianying-skills

**剪映（JianYing Pro）自动化剪辑技能集 — pyJianYingDraft 直驱草稿生成、口播精剪、字幕/音频/动效/转场设计、可选 fork 专业档**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-purple.svg)](https://agentskills.io)

English | [简体中文](./README.zh-CN.md)

## 📖 Introduction

**jianying-skills** 是 [Full AIGC Skills](https://github.com/full-aigc-skills)
生态的剪映技能包：**13 个技能**覆盖从需求到剪映专业版原生草稿的完整链路。
本仓是技能的**唯一正典（source of truth）**——下游插件只通过 vendoring 消费
（见 Consumers），不自行维护副本。

引擎分层：

| 层 | 引擎 | 许可 |
|---|---|---|
| 主力 | [pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft)（由承载插件 vendor，逐文件 SHA-256 钉扎） | Apache-2.0 |
| 快路径 | 内置 Rust CLI `jycut`（由承载插件携带） | Apache-2.0 |
| 专业档（可选） | 用户自己的 [partme-ai/jianying-headless](https://github.com/partme-ai/jianying-headless) fork 检出 | 上游为个人学习与非商业许可，零改动驱动 |

## 📦 Install

```bash
npx skills add full-aigc-skills/jianying-skills
```

或安装单个技能：`npx skills add full-aigc-skills/jianying-skills --skill jianying-edit`

## 🎯 Skills (13)

| Skill | 职责 |
|---|---|
| `jianying-use` | 路由 + Step 0 环境预检（三层引擎分流） |
| `jianying-edit` | 核心工作流：需求 → pyJianYingDraft 脚本 → 原生草稿 |
| `jianying-draft` | pyJianYingDraft API 手册（核实签名/坑清单） |
| `jianying-setup` | 环境诊断（MediaInfo/ffprobe/草稿根/fork 专业档） |
| `jianying-narration` | 口播精剪（keep/drop → 截取段） |
| `jianying-subtitles` | 字幕/标题/描边/背景 + SRT 导入 |
| `jianying-audio` | 解说/BGM/原声分层与音量纪律 |
| `jianying-motion` | 关键帧与入场出场动画（alpha 帧陷阱） |
| `jianying-transitions` | 453 转场目录纪律（VIP 边界） |
| `jianying-inspect` | 素材/草稿探测（实测时长铁律） |
| `jianying-export-prep` | 导出前检查清单 + 导出边界 |
| `jianying-recover` | 同名冲突/恢复（allow_replace 门禁） |
| `jianying-harness` | （可选专业档）fork CLI 全参考 |

## 🤝 Consumers

- **Packaged by [`partme-ai/partme-jianying-plugin`](https://github.com/partme-ai/partme-jianying-plugin)** —
  剪映编辑插件（Codex/ZCode/Kimi 三平台）。技能体由插件经
  `scripts/vendor/skill_vendor.py` 从本仓 vendor（`skills.lock.json` 锁定
  ref+sha+逐技能摘要）；上游 push 时经 `notify-consumers` workflow 触发
  下游同步 PR。

承载插件需提供的运行时配套（技能内以 `${CLAUDE_PLUGIN_ROOT}` 引用）：
`scripts/jydraft_run.py`（vendor 引擎引导运行器）、`scripts/jydraft_check.py`
（环境自检）、`cli/`（jycut，快路径可选）。

## 📄 License

Apache-2.0。第三方边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
