"""场景骨架生成器行为测试。生成结果必须能直接通过 v2 目录校验。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/open_catalog_v2.json'
SECTIONS = ['## 网上实操参考', '## 最小输入与追问', '## 场景独有的剪辑流程',
            '## 映射到技能与能力', '## Harness 交接输入', '## 验收与失败分支', '## 场景护栏']


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SceneScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.module = load(ROOT / 'scripts/gen_scene_scaffold.py', 'gen_scene_scaffold')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name)
        (self.skill / 'references').mkdir()
        (self.skill / 'examples/scenarios').mkdir(parents=True)
        catalog = json.loads(FIXTURE.read_text())
        catalog['scenes'][0]['status'] = 'published_knowledge'
        catalog['scenes'][0]['example_path'] = 'examples/scenarios/new01.md'
        catalog['sources'][0].update(
            access_scope='search_excerpt',
            adaptation='参考公开方法，方案为本项目独立编写。')
        (self.skill / 'references/planning-catalog-v2.json').write_text(
            json.dumps(catalog, ensure_ascii=False), encoding='utf-8')
        self.catalog = catalog
        self.spec = {
            'scene_id': 'NEW01',
            'family': '个人生活 Vlog',
            'scene': catalog['scenes'][0],
            'source': self.catalog['sources'][0],
            'human_requirements': '人工选择叙事主线和镜头。',
            'delivery_channel': 'custom',
            'not_for': ['商业广告'],
        }

    def generate(self, **overrides):
        spec = {**self.spec, **overrides}
        path = self.skill / 'spec.json'
        path.write_text(json.dumps(spec, ensure_ascii=False), encoding='utf-8')
        code = self.module.main(['--skill', str(self.skill), '--spec', str(path)])
        target = self.skill / 'examples/scenarios/new01.md'
        return code, (target.read_text(encoding='utf-8') if target.is_file() else None)

    def test_generated_example_is_complete_and_citable(self):
        code, text = self.generate()
        self.assertEqual(code, 0)
        self.assertIsNotNone(text)
        for section in SECTIONS:
            self.assertIn(section, text, section)
        scene = self.catalog['scenes'][0]
        self.assertIn(scene['editorial_intent'], text)
        for line in scene['acceptance']:
            self.assertIn(line, text)
        self.assertIn(self.catalog['sources'][0]['url'], text)
        self.assertIn(scene['primary_recipe_id'], text)

    def test_generated_example_survives_catalog_validation(self):
        self.generate()
        validator = load(ROOT / 'scripts/validate_open_catalog.py', 'open_catalog')
        errors = validator.validate(self.skill, json.loads(
            (self.skill / 'references/planning-catalog-v2.json').read_text(encoding='utf-8')))
        self.assertEqual(errors, [])

    def test_missing_source_refuses_to_generate(self):
        for source in ({}, {'url': ''}, None):
            with self.subTest(source=source):
                code, text = self.generate(source=source)
                self.assertNotEqual(code, 0)
                self.assertIsNone(text)

    def test_missing_human_semantics_refuses_to_generate(self):
        for field in ('editorial_intent', 'beats', 'acceptance', 'guardrails'):
            scene = {k: v for k, v in self.catalog['scenes'][0].items() if k != field}
            with self.subTest(field=field):
                code, text = self.generate(scene=scene)
                self.assertNotEqual(code, 0)
                self.assertIsNone(text)

    def test_repeated_generation_is_byte_identical(self):
        self.assertEqual(self.generate()[0], 0)
        first = (self.skill / 'examples/scenarios/new01.md').read_bytes()
        self.assertEqual(self.generate()[0], 0)
        self.assertEqual((self.skill / 'examples/scenarios/new01.md').read_bytes(), first)

    def test_existing_different_example_is_not_overwritten(self):
        target = self.skill / 'examples/scenarios/new01.md'
        target.write_text('人工修改过的正文', encoding='utf-8')
        code, text = self.generate()
        self.assertNotEqual(code, 0)
        self.assertEqual(text, '人工修改过的正文')

    def test_nested_example_capability_link_resolves(self):
        """子目录落点时能力映射链接深度必须随之加深，否则 lint 本地链接检查变红。"""
        nested = 'examples/scenarios/new-family/xx01.md'
        self.catalog['scenes'][0]['example_path'] = nested
        (self.skill / 'references/planning-catalog-v2.json').write_text(
            json.dumps(self.catalog, ensure_ascii=False), encoding='utf-8')
        self.spec['scene'] = self.catalog['scenes'][0]
        code = self.generate()[0]
        self.assertEqual(code, 0)
        target = self.skill / nested
        text = target.read_text(encoding='utf-8')
        self.assertIn('(../../../references/capability-mapping.md)', text)
        # 生成文件自身可解析到真实的 capability-mapping.md。
        resolved = (target.parent / '../../../references/capability-mapping.md').resolve()
        self.assertEqual(resolved, (self.skill / 'references/capability-mapping.md').resolve())

    def test_generator_never_invents_source_link(self):
        code, text = self.generate(source={'title': '只有标题没有链接'})
        self.assertNotEqual(code, 0)
        self.assertIsNone(text)
        self.assertNotIn('只有标题没有链接', '\n'.join(
            p.name for p in (self.skill / 'examples/scenarios').iterdir()))
