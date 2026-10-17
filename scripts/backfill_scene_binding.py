#!/usr/bin/env python3
"""把 v1 冻结目录的执行绑定回填到 v2 扩容目录。只做一次性迁移，不修改 v1。

v1 是旧消费者的冻结基线，不得被本次迁移改写；v2 是扩容的唯一事实源，需要补回
v1 具备而 v2 丢失的执行绑定字段。回填按 legacy_ids 连接，幂等，冲突即失败。
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jianying-video-planning'
V1 = SKILL / 'references/video-taxonomy.json'
V2 = SKILL / 'references/planning-catalog-v2.json'

# v1 字段 → v2 字段。brief/assets/acceptance/guardrail 已由 v2 的
# applies_when/asset_requirements/acceptance/guardrails 承载，不在此重复回填。
BINDING = {
    'skills': 'skills',
    'required_capabilities': 'required_capabilities',
    'beats': 'beats',
    'edit': 'editorial_intent',
}


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def merge_scene(scene, origin):
    """按规范字段顺序合并：执行绑定排在 status 之前，保持文件可人工维护。"""
    binding, conflict = {}, None
    for source_field, target_field in BINDING.items():
        expected = origin[source_field]
        if target_field in scene:
            if scene[target_field] != expected:
                conflict = f"{scene['id']}.{target_field}"
            binding[target_field] = scene[target_field]
        else:
            binding[target_field] = expected
    merged = {}
    for key, value in scene.items():
        if key == 'status':
            merged.update(binding)
        if key not in binding:
            merged[key] = value
    if 'status' not in scene:
        merged.update(binding)
    return merged, conflict


def plan(catalog, legacy):
    """返回 (更新后的场景列表, 冲突列表)。不改动入参对象。"""
    frozen = {scene['id']: scene for scene in legacy['scenes']}
    conflicts, updated = [], []
    for scene in catalog['scenes']:
        origin = next((frozen[i] for i in scene.get('legacy_ids', []) if i in frozen), None)
        if origin is None:
            updated.append(scene)
            continue
        merged, conflict = merge_scene(scene, origin)
        if conflict:
            conflicts.append({'code': 'scene_backfill_conflict', 'message': conflict})
        updated.append(merged)
    return updated, conflicts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true', help='写回目录；缺省只做只读预演')
    args = parser.parse_args()
    catalog, legacy = load(V2), load(V1)
    updated, conflicts = plan(catalog, legacy)
    filled = sum(1 for before, after in zip(catalog['scenes'], updated)
                 if before != after)
    if conflicts:
        print(json.dumps({'ok': False, 'conflicts': conflicts}, ensure_ascii=False, indent=2))
        return 1
    if args.write and filled:
        merged_catalog = dict(catalog)
        merged_catalog['scenes'] = updated
        V2.write_text(json.dumps(merged_catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'ok': True, 'filled': filled, 'total': len(catalog['scenes'])}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
