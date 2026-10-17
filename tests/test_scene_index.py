"""场景索引生成器测试：黄金样本逐字节一致、输出确定性、
--check 能发现目录与索引漂移、新增场景按首个 domain 归类且显示 ID 取 id 尾段大写。"""
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jianying-video-planning'
INDEX = SKILL / 'references/scene-index.md'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized_disk():
    """Windows 检出按 core.autocrlf 转成 CRLF；按统一换行后比对，不放宽内容一致性。"""
    return INDEX.read_bytes().decode('utf-8').replace('\r\n', '\n')


class SceneIndexGoldenTests(unittest.TestCase):
    """生成结果必须与当前手写 scene-index.md 逐字节一致——最强正确性证据。"""

    def setUp(self):
        self.module = load(ROOT / 'scripts/gen_scene_index.py', 'gen_scene_index')

    def test_render_matches_current_scene_index_byte_for_byte(self):
        self.assertEqual(self.module.build(SKILL), normalized_disk())

    def test_output_is_deterministic_lf_only(self):
        first = self.module.build(SKILL)
        self.assertEqual(self.module.build(SKILL), first)
        self.assertNotIn('\r', first)


class SceneIndexCommandTests(unittest.TestCase):
    def setUp(self):
        self.module = load(ROOT / 'scripts/gen_scene_index.py', 'gen_scene_index')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / 'skill'
        shutil.copytree(SKILL / 'references', self.skill / 'references')
        self.catalog_path = self.skill / 'references/planning-catalog-v2.json'
        self.catalog = json.loads(self.catalog_path.read_text(encoding='utf-8'))
        self.index = self.skill / 'references/scene-index.md'

    def add_scene(self, scene, source=None):
        self.catalog['scenes'].append(scene)
        if source is not None:
            self.catalog['sources'].append(source)
        self.catalog_path.write_text(
            json.dumps(self.catalog, ensure_ascii=False, indent=1), encoding='utf-8')

    def new_scene(self, scene_id='scene.d26.xx01', domain='D26', name='扩容占位场景'):
        scene = copy.deepcopy(self.catalog['scenes'][0])
        scene.update(id=scene_id, legacy_ids=[], name=name, aliases=[],
                     domain_ids=[domain], source_ids=[],
                     example_path=f'examples/scenarios/new-family/{scene_id.rsplit(".", 1)[-1]}.md',
                     primary_recipe_id='R06', applies_when=['占位适用条件'])
        return scene

    def test_check_passes_on_current_tree(self):
        self.assertEqual(self.module.main(['--skill', str(self.skill), '--check']), 0)

    def test_check_fails_after_scene_added_then_regenerate_fixes(self):
        self.add_scene(self.new_scene())
        self.assertEqual(self.module.main(['--skill', str(self.skill), '--check']), 1)
        self.assertEqual(self.module.main(['--skill', str(self.skill)]), 0)
        self.assertEqual(self.module.main(['--skill', str(self.skill), '--check']), 0)
        self.assertIn('- [XX01 扩容占位场景](../examples/scenarios/new-family/xx01.md)'
                      ' — R06；占位适用条件', self.index.read_text(encoding='utf-8'))

    def test_new_scene_grouped_by_first_domain_with_tail_display_id(self):
        self.add_scene(self.new_scene())
        self.assertEqual(self.module.main(['--skill', str(self.skill)]), 0)
        lines = [line for line in self.index.read_text(encoding='utf-8').split('\n') if line]
        headers = [line for line in lines if line.startswith('## ')]
        self.assertEqual(headers[-1], '## 教育技能')
        entry = '- [XX01 扩容占位场景](../examples/scenarios/new-family/xx01.md) — R06；占位适用条件'
        self.assertEqual(lines[lines.index('## 教育技能') + 1], entry)
        # 既有 108 条的家族分组与顺序保持不变。
        self.assertTrue(lines[4].startswith('- [VG01 日常一天](../examples/scenarios/vg01.md)'), lines[4])

    def test_regeneration_is_byte_idempotent(self):
        self.assertEqual(self.module.main(['--skill', str(self.skill)]), 0)
        first = self.index.read_bytes()
        self.assertEqual(self.module.main(['--skill', str(self.skill)]), 0)
        self.assertEqual(self.index.read_bytes(), first)


if __name__ == '__main__':
    unittest.main()
