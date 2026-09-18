# 剪辑计划格式 `jianying-plan/v1`

引擎 `jy-headless`（partme-ai/jy-headless）的输入契约。所有时间为**微秒整数**；
坐标为归一化值（0-1，相对画面）。

## 顶层

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| schema | string | ✅ | 恒为 `"jianying-plan/v1"` |
| draft | object | ✅ | `name`（草稿名，草稿根内唯一）、`width`、`height`、`fps` |
| tracks | array | ✅ | 轨道数组，按堆叠顺序：video 最底，text/audio 依层级 |

## 轨道类型与 clip 字段

### video

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| material | string | ✅ | 本地媒体文件路径 |
| start_us | int | ✅ | 源内入点（微秒） |
| duration_us | int | ✅ | 段长 |
| volume | float | — | 0-1+，默认 1.0 |
| speed | float | — | 默认 1.0；配 duration 换算注意源长 |
| transition_out | object | — | `{type, duration_us}`；type 见转场目录 |
| keyframes | array | — | `{property, time_offset_us, value}`；property ∈ uniform_scale / position_x / position_y / rotation / scale_x / scale_y |

### text

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| text | string | ✅ | 字幕/标题文案 |
| start_us / duration_us | int | ✅ | 时间 |
| size | float | — | 字号（默认 8.0） |
| color | array | — | [r,g,b] 0-1 |
| bold / italic / underline | bool | — | 默认 false |
| align | int | — | 0 左 / 1 中 / 2 右 |
| letter_spacing | int | — | 字距 |

### audio

同 video（无 keyframes/transition），`material` 为音频文件。

## 校验规则

- 各段 `duration_us` 之和 = 期望成片时长（帧级换算：`us = frames / fps × 1e6`）。
- 草稿名唯一；覆盖需显式 `allow_replace`。
- 素材文件必须真实存在（引擎生成前不自动下载）。
- 转场时长 ≤ 1s；关键帧 time_offset 在段内。

## 与白模预演的衔接

白模镜头表的切点（帧）按 `us = frame / fps × 1e6` 换算为段边界；
逐镜首尾帧投喂生成模型后，实测切点（detect_shots）回填本计划——
**计划值是设计意图，实测值才是草稿边界**。
