# jianying-skills（中文）

**剪映自动化剪辑 Agent Skills — 草稿生成、口播精剪、字幕/音频/动效设计**

[English](./README.md) | 简体中文

## 📖 简介

**jianying-skills** 收集剪映专业版自动化剪辑相关的 Agent Skills，属于
[Full AIGC Skills](https://github.com/full-aigc-skills) 生态的剪映包。

本包包含 **2 个技能**。原理：剪映草稿是 JSON 工程
（`draft_content.json` + `draft_meta_info.json`），可离线生成、在剪映中
继续编辑后导出。

## 📦 安装

```bash
npx skills add full-aigc-skills/jianying-skills
```

## 🧩 Skills

| Skill | 职责 |
|---|---|
| `jianying-edit` | 剪辑计划 JSON（jianying-plan/v1）→ 原生可编辑剪映草稿：多轨视频/文字/音频、转场、关键帧、口播精剪桥接 |
| `jianying-draft` | pyJianYingDraft 直接生成：API 速查、版本敏感、常见坑 |

配套引擎：[partme-ai/jy-headless](https://github.com/partme-ai/jy-headless)
（Apache-2.0，`jianying-plan/v1` → 原生草稿的确定性 CLI）。

## 🤝 使用边界

- 需要**剪映专业版已安装**且启动过一次；生成的是可在剪映中继续编辑的
  原生草稿，MP4 导出在剪映内由用户完成。
- 方法论参考 mcncarl/jianying-headless 与 mcncarl/yichen-skills
  （yichen-jianying-edit）；本包为独立 Apache-2.0 实现，无上游代码或文本复制。

## License

Apache-2.0。
