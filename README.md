# jianying-skills

**剪映（JianYing Pro）自动化剪辑技能集 — 草稿生成、口播精剪、字幕/音频/动效设计**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-purple.svg)](https://agentskills.io)

English | [简体中文](./README.zh-CN.md)

## 📖 Introduction

**jianying-skills** 收集与剪映专业版自动化剪辑相关的 Agent Skills，是
[Full AIGC Skills](https://github.com/full-aigc-skills) 生态的剪映包。

本包包含 **2 个技能**，均以
[pyJianYingDraft](https://github.com/GuvaI/pyJianYingDraft)（Apache-2.0）为底座：
剪映草稿是 JSON 工程（`draft_content.json`），可离线生成、在剪映中继续编辑。

## 📦 Install

```bash
npx skills add full-aigc-skills/jianying-skills
```

## 🧩 Skills

| Skill | 职责 |
|---|---|
| `jianying-edit` | 剪辑计划 JSON（jianying-plan/v1）→ 原生可编辑剪映草稿：多轨视频/文字/音频、转场、关键帧、口播精剪桥接 |
| `jianying-draft` | pyJianYingDraft 直接生成：API 速查、版本敏感、常见坑（静态机位/样式/关键帧） |

配套引擎：[partme-ai/jy-headless](https://github.com/partme-ai/jy-headless)
（Apache-2.0，`jianying-plan/v1` → 原生草稿的确定性 CLI）。

## 🤝 使用边界

- 需要**剪映专业版已安装**且启动过一次（草稿根存在）；生成的是可在剪映中
  继续编辑的原生草稿，MP4 导出在剪映内由用户完成。
- 方法论参考 mcncarl/jianying-headless 与 mcncarl/yichen-skills
  （yichen-jianying-edit）；本包为独立 Apache-2.0 实现，无上游代码或文本复制。

## License

Apache-2.0。
