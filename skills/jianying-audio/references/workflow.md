# 音频工作流参考

## 分层

- 对白/解说为语义主层。
- 原声随视频片段管理，避免重复导入造成相位或重声。
- BGM 和音效独立轨道，按场景和对白动态调整。
- 所有时长来自探测，不能以计划时长填补素材边界。

## TTS 边界

- `media.tts_local=supported` 只证明本地/系统执行路径；云厂商还必须检查
  `media.tts_provider`。其为 `partial` 时不得自动路由或宣称全厂商可用；具名云厂商只有在用户明确
  选择、当前 CLI 执行子路径握手通过并取得精确审批后才能提交。
- 具名 Provider 要逐项检查 voice、emotion、SSML、timestamps、streaming 和字符上限。
- 真实云请求使用内容哈希幂等账本；ambiguous 不自动重提。
- 输出需验证格式、时长和 SHA-256 后才能加入草稿。

### Provider 路由

| 类型 | CLI provider | 关键门禁 |
|---|---|---|
| 系统语音 | `system-macos`、`system-windows` | 当前平台、实际可执行文件和输出音频探测 |
| 通用本地运行时 | `local-command`、`local-http`、`local-process` | HTTP 仅回环；进程使用绝对路径和结构化 argv；不能冒充具名模型证据 |
| 联网客户端 | `edge-tts` | 明确报告联网属性，不得按离线模型处理 |
| 云厂商 | `xiaomi-mimo`、`volcengine`、`aliyun-bailian`、`baidu`、`tencent-cloud`、`minimax`、`zhipu-glm` | 凭据只写环境变量名；先 `--plan`，精确审批后才提交；火山使用 V3 SSE，必须传 `--resource-id` 与 `--uid`，禁止旧 V1 `--app-id/--cluster` |

云厂商安全计划示例：

```bash
jianying media tts /abs/draft \
  --provider minimax \
  --text-file /abs/narration.txt \
  --format mp3 \
  --model speech-2.8-hd \
  --voice male-qn-qingse \
  --credential-env MINIMAX_API_KEY \
  --task-id episode-01-narration \
  --max-cost-microunits 50000 \
  --plan --json
```

输出必须只有哈希化审批绑定、endpoint、预算与凭据引用名，不得出现原始文本或秘密值。

火山引擎计划使用同一审批流程，但参数必须对应 V3 协议：

```bash
jianying media tts /abs/draft \
  --provider volcengine \
  --text-file /abs/narration.txt \
  --format mp3 \
  --voice <speaker-id> \
  --resource-id <v3-resource-id> \
  --uid <stable-user-id> \
  --credential-env VOLCENGINE_TTS_API_KEY \
  --task-id episode-01-volcengine \
  --max-cost-microunits 50000 \
  --plan --json
```

`--resource-id` 决定已开通的 V3 能力，不能由技能猜测；旧 `--app-id`/`--cluster` 会被当前
Rust CLI 明确拒绝。V3 响应只有在终止帧到达且所有 Base64 音频分片可解码时才可进入制品账本。

把返回的 `approval_binding` 交给宿主审批流；审批记录落入指定目录后，保持其余参数完全一致，去掉
`--plan` 并追加：

```bash
  --approval-id <exact-approval-id> \
  --approval-root /abs/approval-state \
  --tts-state-root /abs/tts-state
```

执行前仍需再次确认用户确实授权该厂商、文本、模型、音色、目标和最大预算。凭据值只放在
`--credential-env` 指向的环境变量中，不得进入参数、日志或任务正文。4xx 明确拒绝进入 failed；
超时、连接中断、5xx、响应无法确定或制品落盘失败进入 ambiguous，均不得普通重提。succeeded
制品必须由账本核对 SHA-256 后复用，避免重复计费。

`--live-canary` 必须生成 `tts.cloud.live-canary` 独立绑定，不能复用普通生产审批。 capability 仍为
`partial` 时不得自动发起真实云请求或宣称全厂商支持；用户未明确选择、审批不匹配、执行子路径
未握手或需要真实 canary 证据时，报告 `BLOCKED` 并保留计划。不得在真实工作流使用隐藏的
`--cloud-endpoint-override` 测试开关。

## 恢复

重链失败时保持源路径不变；只在候选唯一且探测类型匹配时提交。试听发现混音问题时从隔离副本继续，不覆盖已验收版本。
