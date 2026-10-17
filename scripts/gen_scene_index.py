#!/usr/bin/env python3
"""确定性生成 skills/jianying-video-planning/references/scene-index.md。

家族名只能经 legacy_ids join video-taxonomy.json(v1) 得到；
新场景 legacy_ids 为空，按 domain_ids 第一个领域归类，
显示 ID 取 scene.id 末段大写。无时间戳、LF 换行、幂等。
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL = ROOT / 'skills/jianying-video-planning'

PREAMBLE = (
    '# 视频场景索引\n'
    '\n'
    '规模以 [v2 目录](planning-catalog-v2.json) 的 `scenes` 实际条数为准，'
    '本文件不把任何数字写成上限。当前目录为 18 个家族、每类 6 个独立案例。'
    '先选渠道与目的，再读选中的 1–3 个例子；不一次加载全部正文。\n'
    '\n'
    '本库不是热榜：18 个参考来源取得可见指标，其余为实操/创作者案例参考、热度未核验。'
    '指标来自 2026-09-21 查阅时页面或搜索索引；没有完整观看来源视频。'
    '目录内各项尚未逐一进行真实剪映验收。\n'
)


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def display_id(scene):
    """显示 ID：有 legacy_ids 取第一个，否则取 scene.id 末段大写。"""
    if scene['legacy_ids']:
        return scene['legacy_ids'][0]
    return scene['id'].rsplit('.', 1)[-1].upper()


def build(skill):
    """按 v2 目录 + v1 家族映射渲染完整 scene-index.md 文本（LF、无时间戳）。"""
    skill = Path(skill)
    references = skill / 'references'
    v2 = load_json(references / 'planning-catalog-v2.json')
    v1 = load_json(references / 'video-taxonomy.json')
    family_order = list(v1['families'])
    family_by_legacy = {scene['id']: scene['family'] for scene in v1['scenes']}
    domain_by_id = {d['id']: d for d in v2['domains']}
    groups = {}
    order = []
    for scene in v2['scenes']:
        family = next((family_by_legacy[legacy] for legacy in scene['legacy_ids']
                       if legacy in family_by_legacy), None)
        if family is not None:
            key = (0, family_order.index(family), family)
        else:
            title = domain_by_id[scene['domain_ids'][0]]['name']
            key = (1, title, title)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(scene)
    order.sort()
    lines = [PREAMBLE, '\n']
    for position, key in enumerate(order):
        lines.append(f'## {key[2]}\n\n')
        for scene in groups[key]:
            lines.append(f"- [{display_id(scene)} {scene['name']}]"
                         f"(../{scene['example_path']}) — {scene['primary_recipe_id']}"
                         f"；{scene['applies_when'][0]}\n")
        if position + 1 < len(order):
            lines.append('\n')
    return ''.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description='生成或校验 scene-index.md')
    parser.add_argument('--skill', type=Path, default=DEFAULT_SKILL)
    parser.add_argument('--check', action='store_true',
                        help='内存重生成并与磁盘文件比对，不一致 exit 1')
    args = parser.parse_args(argv)
    rendered = build(args.skill)
    index = Path(args.skill) / 'references/scene-index.md'
    if args.check:
        disk = index.read_text(encoding='utf-8').replace('\r\n', '\n')
        if disk != rendered:
            print('scene-index.md is out of date; run scripts/gen_scene_index.py',
                  file=sys.stderr)
            return 1
        print('scene-index.md matches catalog')
        return 0
    index.write_text(rendered, encoding='utf-8', newline='\n')
    print(f'wrote {index}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
