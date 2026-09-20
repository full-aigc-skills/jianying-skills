# 字幕工作流参考

## 最小命令面

```text
jianying captions list|get
jianying captions import-srt|import-ass
jianying captions add|set|style|translate
jianying captions export-srt|export-ass
```

具体参数从 `jianying captions <command> --help` 获取。

字幕源尚不存在且允许使用本地 whisper.cpp 时，先交给 **`jianying-narration`** skill 运行
`media transcribe` 并取得经账本验证的 SRT/VTT/JSON 制品，再回到本技能导入。Install:
`npx skills add full-aigc-skills/jianying-skills --skill jianying-narration`。不得把 ASR segment
时间戳直接当作剪映播放验收，也不得在 `media.asr_whisper_cpp` 未 supported 时自动选用它。

## 样式规则

- 同一字幕轨保持字体、描边和基准位置一致。
- 中文可读时长和行长按内容调整，不硬编码为所有项目的统一阈值。
- 平台 UI 安全区属于项目约束；冷重开后目视检查。
- 翻译保持 segment ID 和时间不变，缺失映射要报告而非删除原文。

## 恢复

导入失败时源草稿不变；查看 mutation audit，修正字幕文件后重新创建隔离副本。导出文件已存在时不覆盖，除非批准明确包含该路径。
