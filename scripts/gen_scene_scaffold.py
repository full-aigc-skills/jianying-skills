#!/usr/bin/env python3
"""按目录条目生成场景例文骨架。只生成结构与可推导段落，语义与来源必须人工提供。

生成器不是内容生产者：来源链接、剪辑取舍原则、叙事节拍、验收与护栏都必须在输入中
逐字给出，缺失即拒绝生成。这样"扩容到 300"的人工成本落在判断上，而不是排版上。
"""
import argparse
import json
from pathlib import Path

SKILL_DEFAULT = Path(__file__).resolve().parents[1] / 'skills/jianying-video-planning'
CATALOG = 'references/planning-catalog-v2.json'

# 固定段落：与扩容无关，改动会影响全部场景，须与 spec 的不可变段要求一致。
FOLLOW_UP = '只追问会改变剪法的信息：交付渠道/比例、目标时长、上述关键素材是否齐全、期望交付等级。缺素材时给补拍清单，不编造镜头。'
BEAT_BODY = '从真实素材清单选择相应片段，记录源文件和经探测的入出点。'
CAPABILITY_NOTE = ('只规划无需调用这些写入能力。执行前从已安装 Rust 二进制获取 '
                   '`jianying capabilities --json`，逐项检查所选步骤是否 supported，不能以源代码存在作为能力证据。')
def optional_note(example_path):
    """能力映射链接的相对深度随落盘目录变化：顶层 ../../、子目录逐级加深，
    否则 lint_skills 的本地链接检查会因链接指向不存在的路径变红。"""
    depth = len(Path(example_path).parts) - 1
    prefix = '../' * depth
    return ('可选 ASR、TTS、转场不默认启用；选择后才增加相应能力和许可检查。'
            f'详见 [能力映射]({prefix}references/capability-mapping.md)。')
PLANNING_NOTE = ('此为规划输入，不是可执行 job。实际执行需补齐已探测媒体事实、时间码与授权；'
                 '由 jianying-draft 形成 `jianying-job/v2`，交给 jianying-edit 执行。')
FAILURE_BRANCHES = [
    '缺素材：返回 waiting_input，列出缺项，不生成虚构素材路径。',
    '缺必要能力：返回 blocked_capability；可删减可选效果，但必须说明降级并保留用户目标。',
    '结构通过不等于播放正常。代理预览须标注 proxy_preview；要求原生输出时需 render.native、运行环境及真实产物证据，不能静默降级。',
    '不明执行结果先核查已有任务与产物，不重复原生导出或付费调用。',
]
BULLET = '- '
DISCLAIMER = '所有来源仅供方法研究，不授予其中媒体的复制或商业使用权。'
STATUS_NOTE = '状态：方法示例，未做此场景真实剪映端到端验收。'
INSTALL = '安装：`npx skills add full-aigc-skills/jianying-skills --skill {skill}`。'


def sentence(text):
    """补句末标点。目录里的语义字段不带句号，正文按中文习惯补齐。"""
    text = str(text).strip()
    return text if text.endswith(('。', '！', '？', '：')) else text + '。'

# 必须由人工逐字提供、生成器不得编造或兜底填充的字段。
REQUIRED_TEXT = ('editorial_intent', 'beats', 'acceptance', 'guardrails', 'asset_requirements')


class SpecError(Exception):
    """输入不足以生成合规例文。"""


def check(spec):
    """缺来源或缺人工语义字段时拒绝生成。"""
    source = spec.get('source') or {}
    if not str(source.get('url', '')).strip():
        raise SpecError('spec_source_url_missing')
    if not str(source.get('title', '')).strip():
        raise SpecError('spec_source_title_missing')
    if not str(source.get('accessed_on', '')).strip():
        raise SpecError('spec_source_accessed_on_missing')
    for field in REQUIRED_TEXT:
        value = spec.get('scene', {}).get(field)
        if isinstance(value, list):
            if not value or not all(str(item).strip() for item in value):
                raise SpecError(f'spec_scene_field_missing:{field}')
        elif not str(value or '').strip():
            raise SpecError(f'spec_scene_field_missing:{field}')


def source_block(source, page_access='unavailable'):
    """来源段全部取自来源记录。热度未观测到数值时写明未观测，不填占位数字。"""
    popularity = source.get('popularity') or {}
    metrics = popularity.get('metrics') or []
    heat = '；'.join(metrics) if popularity.get('status') == 'measured' else '未取得可靠播放或使用量'
    scope = popularity.get('scope') or '只属于该来源的索引/页面快照，不是场景排行榜'
    return '\n'.join([
        f"- [{source['title']}]({source['url']})",
        f"- 查阅：{source['accessed_on']}；检索词：{source.get('query', '')}。",
        f"- 阅读范围：`{source.get('access_scope', 'search_excerpt')}`；原页面访问：{page_access}；未观看完整视频，不推断未读细节。",
        f"- 热度：{popularity.get('status', 'popularity_unverified')}。{heat}；{scope}。",
        f"- {source.get('adaptation', '参考公开方法，方案为本项目独立编写。')}",
    ])


def skill_block(scene):
    lines = [f"- **`{skill}`**；{INSTALL.format(skill=skill)}" for skill in scene['skills']]
    tail = '\n'.join(['结构草稿所需能力：' + '、'.join(f'`{c}`' for c in scene['required_capabilities']) + '。',
                      CAPABILITY_NOTE, optional_note(scene['example_path'])])
    return '\n\n'.join(['\n'.join(lines), tail])


def intent_block(scene, human_requirements):
    return '\n\n'.join(['\n'.join(f'{index}. {beat}：{BEAT_BODY}'
                                  for index, beat in enumerate(scene['beats'], 1)),
                        '关键取舍：' + sentence(scene['editorial_intent']),
                        '人工或外部环节：' + sentence(human_requirements)])


def harness_block(scene_id, channel):
    payload = {'schema': 'jianying-video-intent/v1', 'scene_id': scene_id,
               'delivery': 'plan', 'channel': channel, 'media': [], 'requested_features': []}
    return '```json\n' + json.dumps(payload, ensure_ascii=False, indent=2) + '\n```\n\n' + PLANNING_NOTE


def render(spec, recipe):
    """产出完整例文正文。结构与既有七段式约定一致。"""
    scene = spec['scene']
    title = f"# {spec['scene_id']} {scene['name']}"
    intro = f"{sentence(scene['applies_when'][0])}\n\n类型：{spec.get('family', '')}；Recipe：{recipe['id']} {recipe['name']}；{STATUS_NOTE}"
    minimum = (f"素材：{'、'.join(scene['asset_requirements'])}。\n{FOLLOW_UP}")
    acceptance = '\n'.join([BULLET + '场景验收：' + sentence(line) for line in scene['acceptance']]
                          + [BULLET + branch for branch in FAILURE_BRANCHES])
    guardrails = '。'.join(sentence(item) for item in scene['guardrails']).rstrip('。')
    return '\n\n'.join([title, intro, '## 网上实操参考\n\n' + source_block(spec['source'], spec.get('page_access', 'unavailable')),
                        '## 最小输入与追问\n\n' + minimum,
                        '## 场景独有的剪辑流程\n\n' + intent_block(scene, spec.get('human_requirements', '')),
                        '## 映射到技能与能力\n\n' + skill_block(scene),
                        '## Harness 交接输入\n\n' + harness_block(spec['scene_id'], spec.get('delivery_channel', 'custom')),
                        '## 验收与失败分支\n\n' + acceptance,
                        '## 场景护栏\n\n' + f'{guardrails}。{DISCLAIMER}']) + '\n'


def find_recipe(catalog, recipe_id):
    for recipe in catalog['recipes']:
        if recipe['id'] == recipe_id:
            return recipe
    raise SpecError(f'spec_recipe_unknown:{recipe_id}')


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--skill', type=Path, default=SKILL_DEFAULT)
    parser.add_argument('--spec', type=Path, required=True)
    parser.add_argument('--force', action='store_true', help='覆盖已存在且内容不同的例文')
    args = parser.parse_args(argv)
    try:
        spec = json.loads(args.spec.read_text(encoding='utf-8'))
        scene = spec.get('scene') or {}
        if not str(scene.get('name', '')).strip():
            raise SpecError('spec_scene_field_missing:name')
        catalog = json.loads((args.skill / CATALOG).read_text(encoding='utf-8'))
        recipe = find_recipe(catalog, scene.get('primary_recipe_id'))
        check(spec)
        body = render(spec, recipe)
        target = args.skill / scene['example_path']
        if target.is_file():
            if target.read_text(encoding='utf-8') == body:
                print(json.dumps({'ok': True, 'written': False, 'reason': 'identical'}, ensure_ascii=False))
                return 0
            if not args.force:
                raise SpecError('example_exists_with_different_content')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding='utf-8')
        print(json.dumps({'ok': True, 'written': True, 'path': scene['example_path']}, ensure_ascii=False))
        return 0
    except (SpecError, OSError, json.JSONDecodeError, KeyError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
