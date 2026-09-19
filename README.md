# jianying-skills

Agent Skills for creating, editing, inspecting, recovering, and exporting JianYing/CapCut drafts through one Rust runtime: `jianying-cli`.

[简体中文](README.zh-CN.md) | English

## Architecture

The skills never implement a second editing engine. They compile user intent into
`jianying-job/v2` or structured CLI commands, then call either `jianying-cli` directly or the
hosting plugin's Rust Runtime Adapter.

```mermaid
flowchart LR
    U[User goal] --> S[One of 13 skills]
    S --> G[Version, schema, capability gate]
    G --> J[jianying-job/v2 or structured command]
    J --> R[jianying-cli Rust runtime]
    R --> D[Editable draft / proxy / native task]
    D --> E[Evidence: structural to native export]
```

No skill generates temporary draft scripts, loads a legacy embedded engine, or routes execution
through an external headless checkout. Capabilities marked `partial`, `external_dependency`, or
missing stop the affected workflow.

## Install

Install the package:

```bash
npx skills add full-aigc-skills/jianying-skills
```

Install one self-contained skill:

```bash
npx skills add full-aigc-skills/jianying-skills --skill jianying-edit
```

Every skill contains its own workflow reference and minimal Job example; granular installation
does not rely on sibling skill directories.

## Skills

| Skill | Responsibility |
|---|---|
| `jianying-use` | Entry routing, minimal questions, and capability diagnosis |
| `jianying-setup` | CLI, media tools, draft roots, configuration, and runtime readiness |
| `jianying-draft` | `jianying-job/v2`, domain concepts, and v1 compatibility |
| `jianying-harness` | Persistent jobs, approvals, configuration, MCP, and host contracts |
| `jianying-edit` | New drafts and isolated editing of existing drafts |
| `jianying-narration` | Governed ASR reuse and narration condensing |
| `jianying-subtitles` | Caption import, editing, styling, translation, and export |
| `jianying-audio` | Audio layers, volume, fades, effects, relinking, and TTS gates |
| `jianying-motion` | Transform, keyframe, animation, speed, and quantization planning |
| `jianying-transitions` | Catalogue-backed transitions and boundary checks |
| `jianying-inspect` | Read-only media and draft facts with evidence levels |
| `jianying-export-prep` | Proxy/native export readiness and artifact validation |
| `jianying-recover` | Task audit, explicit retry, snapshots, and ambiguous operations |

## Compatibility and evidence

The target contract requires `jianying-cli >= 1.6.0`, but capability state remains authoritative.
Each skill declares its required IDs, risk level, confirmation points, and maximum completion
evidence. A structural pass is not a cold reopen, playback check, or native export.

The complete capcut-cli command parity evidence is maintained by
[`jianying-cli`](https://github.com/full-aigc-plugins/jianying-cli/blob/main/docs/capcut-command-evidence.md),
not duplicated across the skills.

## Distribution

This repository is the only source of truth for skill bodies. Consumer plugins must import an
immutable release ref and commit, verify every skill digest, and never patch vendored bodies.

## License

Apache-2.0. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for provenance and excluded-source boundaries.
