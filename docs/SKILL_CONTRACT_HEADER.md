# 剪映技能统一契约头模板

每个 `SKILL.md` 在 frontmatter 后、具体工作流前必须逐项回答以下内容。字段可写成自然语言，但语义不能缺失。

```markdown
## 运行契约

- 触发条件：什么用户目标应使用本技能。
- 所需 capability：来自 `jianying-cli capabilities --json` 的稳定 ID。
- 最低 CLI 版本：只用于升级提示，实际路由以 capability 为准。
- 默认风险：read_only / reversible_write / high_risk_write / external_native_execution。
- 输入事实：开始规划前必须实际探测的素材、草稿和运行时事实。
- 确认点：需要用户批准时，绑定具体 command、arguments、cwd/target 和任务。
- 成功证据：plan / structural / cold_reopen / playback / native_export。
- 禁止行为：不得生成 Python 草稿脚本，不得调用外部 headless checkout，不得把低等级证据描述为最终完成。
```

## 迁移期规则

- 当前 13 个技能均为 `blocked_on_cli_contract`，在 CLI 发布目标 capability manifest 前不得改成 `ready`。
- `scripts/lint_skills.py` 会读取 `docs/RUST_CLI_SKILL_MATRIX.json`；若任何技能声明 `ready`，必须通过 `JIANYING_CLI_CAPABILITY_MANIFEST` 提供已验证清单。
- 高级参数和恢复细节进入本技能自己的 `references/`，不得依赖粒度安装后不存在的兄弟目录。
