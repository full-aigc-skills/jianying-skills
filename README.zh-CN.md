# jianying-skills

**剪映（JianYing Pro）自动化剪辑技能集 — pyJianYingDraft 直驱草稿生成、口播精剪、字幕/音频/动效/转场设计、可选 fork 专业档**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-purple.svg)](https://agentskills.io)

简体中文 | [English](./README.md)

## 📖 简介

**jianying-skills** 是 [Full AIGC Skills](https://github.com/full-aigc-skills)
生态的剪映技能包：**13 个技能**覆盖从需求到剪映专业版原生草稿的完整链路。
本仓是技能的**唯一正典**——下游插件只通过 vendoring 消费，不自行维护副本。

引擎分层：主力 = vendored [pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft)
（Apache-2.0）；快路径 = 内置 Rust CLI `jycut`；专业档（可选）= 用户自己的
[partme-ai/jianying-headless](https://github.com/partme-ai/jianying-headless)
fork 检出（上游个人学习与非商业许可，零改动驱动）。

## 📦 安装

```bash
npx skills add full-aigc-skills/jianying-skills
```

## 🎯 技能（13 个）

与英文版同表：use（路由）/edit（核心工作流）/draft（API 手册）/setup/narration/
subtitles/audio/motion/transitions/inspect/export-prep/recover/harness（专业档）。

## 🤝 下游

由 [`partme-ai/partme-jianying-plugin`](https://github.com/partme-ai/partme-jianying-plugin)
打包发行（Codex/ZCode/Kimi 三平台）；技能体经 `skill_vendor.py` vendor，
`skills.lock.json` 锁定。承载插件需提供 `scripts/jydraft_run.py`、
`scripts/jydraft_check.py` 与可选 `cli/`（jycut）。

## 📄 许可

Apache-2.0；第三方边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
