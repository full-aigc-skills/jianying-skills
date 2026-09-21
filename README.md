# jianying-skills

新增：**jianying-video-planning**，18 类、108 个独立场景 example、12 套 Recipe。
从 [场景索引](skills/jianying-video-planning/references/scene-index.md) 按需阅读。108 个是方法场景，不是热榜或实机通过数；来源和热度边界逐项记录。

Planning only: [open scenario coverage](docs/video-scenarios/COVERAGE_PLAN.md)
treats the 108 examples as seeds, not an exhaustive taxonomy or a capability ceiling.
[Representative workflow knowledge vectors](skills/jianying-video-planning/references/representative-workflows-v1.json)
freeze the asset gaps and acceptance boundaries for Vlog, multi-version courses, and multi-delivery weddings; they are not execution evidence.
The released v1 catalogue is unchanged. The local 2.2.0 candidate adds a separate
v2 catalogue and validator; its 108 seeds are not yet fully annotated on all axes.

Agent Skills for creating, editing, inspecting, recovering, and exporting JianYing/CapCut drafts through one Rust runtime: `jianying-cli`.

[简体中文](README.zh-CN.md) | English

## Architecture

The skills never implement a second editing engine. They compile user intent into
`jianying-job/v2` or structured CLI commands, then call either `jianying-cli` directly or the
hosting plugin's Rust Runtime Adapter.

```mermaid
flowchart LR
    U[User goal] --> S[One of 24 skills]
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
| `jianying-video-planning` | 108 scenario seeds, channel strategy, recipes, and delivery-level planning |
| `jianying-media` | Local/official materials, subdraft import, replace, relink, and verification |
| `jianying-text` | Text, styles, bubbles, animations, and text templates |
| `jianying-stickers` | Sticker discovery, download, placement, transform, and recovery |
| `jianying-effects` | Scene, character, and audio effects with bounded ranges |
| `jianying-smart-package` | Smart package/B-Roll preview, approval, apply, and recovery |
| `jianying-filters` | Filter discovery, range, intensity, apply, and remove |
| `jianying-adjustments` | Version-bound exposure, color, detail, and reset controls |
| `jianying-templates` | Template libraries, presets, replacement, and track import |
| `jianying-digital-human` | Persona, voice, upload, cost, task, and artifact gates |
| `jianying-editing-console` | Timeline, track, segment, keyframe, session, record, and zoom controls |
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

This repository is the only source of truth for all 24 skill bodies. Consumer plugins must import an
immutable release ref and commit, verify every skill digest, and never patch vendored bodies.

## License

Apache-2.0. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for provenance and excluded-source boundaries.
