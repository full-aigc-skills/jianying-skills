---
name: jianying-edit
description: Turn an edit-plan JSON (jianying-plan/v1: video/text/audio tracks with per-clip material, start, duration, volume, speed, transitions, keyframes) into a native, fully editable JianYing Pro draft via the jy-headless engine. Deterministic, offline, non-destructive to existing drafts. Use for AI-edited shorts, narration condensing deliverables, and batch draft generation.
---

# JianYing Edit（剪辑计划 → 原生草稿）

把结构化剪辑计划生成为**剪映专业版原生草稿**：多轨视频/文字/音频、微秒级时间、
生成结果可在剪映中继续编辑。确定性引擎 `jy-headless`（Apache-2.0），
基于 pyJianYingDraft 0.3.0。

## 前置条件

1. 剪映专业版已安装且启动过至少一次（macOS `com.lemon.lvpro` / Windows 官方安装包）。
2. `jy-headless` 引擎可用（`pip install jy-headless` 或插件内置 vendored 版）。
3. 计划引用的全部素材文件真实存在。

任一不满足：先跑环境诊断（`jy-headless detect`），按输出修复后再继续。

## 工作流

### 1. 生成剪辑计划

按 `jianying-plan/v1` 契约产出计划（完整字段见
[references/plan-format.md](references/plan-format.md)）：

```json
{
  "schema": "jianying-plan/v1",
  "draft": {"name": "episode-01", "width": 1280, "height": 720, "fps": 24},
  "tracks": [
    {"type": "video", "clips": [
      {"material": "generated/shot-01.mp4", "start_us": 0,
       "duration_us": 6000000, "volume": 1.0, "speed": 1.0,
       "transition_out": {"type": "叠化", "duration_us": 500000}}
    ]},
    {"type": "text", "clips": [
      {"text": "解说字幕", "start_us": 500000, "duration_us": 3000000,
       "size": 8.0, "color": [1.0, 1.0, 1.0], "bold": true}
    ]},
    {"type": "audio", "clips": [
      {"material": "narration.mp3", "start_us": 0,
       "duration_us": 6000000, "volume": 1.0}
    ]}
  ]
}
```

规则：时间用微秒整数；每个 `material` 必须是真实存在的本地媒体文件；
草稿名在草稿根内唯一（除非显式允许替换）；转场作用于段尾（`transition_out`），
关键帧（`uniform_scale`/`position_x`/`position_y`/`rotation`）随段内时间线性插值。

### 2. 生成

```bash
jy-headless generate --plan plan.json [--root <草稿根>] [--no-replace]
```

草稿根探测顺序：`--root` → `JY_DRAFT_ROOT` → 平台默认路径。同名草稿默认
报错（`--no-replace` 显式化）；允许替换需用户明确同意。

### 3. 校验

```bash
jy-headless verify --draft-dir <草稿目录>
```

校验 `draft_content.json` 可解析并报告轨道/段数。逐段核对：段起点对齐预期切点、
字幕不重叠、音频无同刻叠加。

### 4. 交付

用户在剪映专业版开始页打开该草稿——它是原生多轨工程，可继续编辑（精修、调色、
加效果）后导出 MP4。**导出动作在剪映内由用户完成，引擎不声称自动化导出。**

## 口播精剪桥接

长口播素材的 keep/drop 决策（ASR 逐字稿 → 语义单元取舍）产出的保留区间，
直接映射为本技能的计划：每段保留区间 = video 轨一个 clip（原声随段），
字幕轨对齐语音，解说轨按语义分层。流程细节见
`jianying-narration`（如已安装）。

## 迭代与恢复

- 被否决的剪辑 = 改计划重生成，换新草稿名（旧稿留作对比）。
- 用户在剪映里编辑过的草稿**永不覆盖**（`--no-replace` 门禁）。
- 素材被移动：新路径回填计划重新生成，或在剪映里手动重链。

## Never do

- Never 引用不存在的素材路径，或用占位媒体冒充真实素材。
- Never 覆盖用户可能编辑过的同名草稿。
- Never 声称已自动化 MP4 导出（导出在剪映内由用户完成）。
- Never 生成侵犯第三方权利的内容（素材需用户自有或已授权）。
