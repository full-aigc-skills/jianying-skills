# 辅助制作知识来源与禁止复制范围

## 固定研究基线

| 字段 | 值 |
|---|---|
| 上游 | `https://github.com/luoluoluo22/jianying-editor-skill` |
| 提交 | `32c56928ded4f9e2c2b80e099dc7abb793d2c30b` |
| 仓库许可证 | MIT，Copyright (c) 2026 luoluoluo22 |
| 内嵌第三方 | `pyJianYingDraft`，Apache-2.0，Copyright (c) 2024 GuanYixuan |
| 采用方式 | 阅读公开源码和规则后独立重写知识合同；不复制执行引擎 |

## 允许吸收的概念

- 录屏事件驱动的智能缩放工作流。
- Web 动效完成信号、透明通道和确定时长的需求。
- 导入前媒体兼容性检查、自包含暂存和转换回滚思想。
- 原生资源发现、影视解说、旁白字幕同步、曝光匹配和 Clone-first 模板策略。

这些概念在本包中被重写为路由、Schema、能力需求和验收规则。上游默认参数、Python API、资源 ID、路径和运行成功声明不成为本包事实。

## 禁止复制或分发

- Python `JyProject`、内嵌 `pyJianYingDraft` 和任何第二草稿引擎。
- Windows/macOS UI 自动化脚本、自动导出脚本和版本坐标。
- 云资源下载脚本、固定设备/API 参数、抓包日志、凭据和资源 URL。
- 音乐、音效、云视频、剪映缓存索引、CSV 数据库、`artistEffect` 或其他专有资源包。
- 上游录屏素材、点击标记图片、模型权重、浏览器产物和缓存。

上游 MIT 许可证不自动覆盖内嵌 Apache-2.0 组件或第三方素材。任何逐文件复制都必须重新经过版权与用途审查；本变更没有执行这类复制。

## 目标架构

Skills 只保存知识。插件 Harness 负责录屏、浏览器、模型、审批、成本、恢复和证据账本。所有草稿修改只通过插件锁定的不可变 Rust `jianying-cli` Release，经 `jianying-job/v2` 完成。

