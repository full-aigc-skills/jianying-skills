# 环境诊断参考

## 就绪层级

1. CLI 存在且版本可解析。
2. capability manifest schema 可识别，所需 ID 为 `supported`。
3. ffprobe/ffmpeg 和目标草稿根可用。
4. 配置 profile 通过 schema 校验。
5. Runtime Profile 精确识别产品、版本、平台和文件身份。
6. 真实剪映 canary 通过后，才能报告 app-open/playback/native-export 证据。

## 常见恢复建议

- CLI 缺失或哈希错误：停止，要求从已验证制品重新安装。
- 版本过旧：报告最低版本；不要在诊断中自动升级。
- 剪映正在运行：涉及草稿写入时停止；只读命令仍可继续。
- Runtime Profile 未支持：保持 fail-closed，允许代理预览，不伪装成原生导出。
- 配置损坏：先展示 `config file` 和 `config validate` 诊断；修改需要单独批准。
