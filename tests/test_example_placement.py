"""扩容例文落盘位置测试：新增例文放 examples/scenarios/ 顶层子目录时，
v1 冻结门禁保持 0 错误、v2 校验通过、safe_file 接受嵌套相对路径；
同时证明顶层新增仍然变红——门禁没有被放宽。"""
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jianying-video-planning'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V1 = load(ROOT / 'scripts/validate_video_catalog.py', 'video_catalog_v1')
V2 = load(ROOT / 'scripts/validate_open_catalog.py', 'open_catalog_for_placement')


class SubdirectoryPlacementTests(unittest.TestCase):
    """新增例文放入 examples/scenarios/<family>/<xx>.md 的可行性证明。"""

    def copy_skill(self, tmp):
        target = Path(tmp) / 'jianying-video-planning'
        shutil.copytree(SKILL, target)
        return target

    def test_v1_gate_stays_green_when_subdirectory_example_added(self):
        """顶层之外的子目录例文对 v1 门禁不可见：glob('*.md') 只数冻结顶层。"""
        catalog = json.loads((SKILL / 'references/video-taxonomy.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as tmp:
            target = self.copy_skill(tmp)
            extra = target / 'examples/scenarios/new-family/xx01.md'
            extra.parent.mkdir(parents=True)
            extra.write_text('扩容场景例文占位', encoding='utf-8')
            self.assertEqual(V1.validate(target, catalog), [])

    def test_v1_gate_still_red_for_extra_top_level_example(self):
        """顶层新增例文依旧触发既有错误：落点结论不来自放宽门禁。"""
        catalog = json.loads((SKILL / 'references/video-taxonomy.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as tmp:
            target = self.copy_skill(tmp)
            (target / 'examples/scenarios/zz99.md').write_text('顶层新增', encoding='utf-8')
            errors = V1.validate(target, catalog)
            self.assertTrue(any('example path set' in e for e in errors), errors)

    def test_safe_file_accepts_nested_relative_path(self):
        """safe_file 只拒绝 \\ : . .. 绝对路径与符号链接；嵌套相对路径合法。"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / 'examples/scenarios/new-family/xx01.md'
            nested.parent.mkdir(parents=True)
            nested.write_text('body', encoding='utf-8')
            resolved = V2.safe_file(root, 'examples/scenarios/new-family/xx01.md', 1024)
            self.assertEqual(resolved, nested)
            for bad in ('examples/scenarios/../xx01.md', 'examples\\scenarios\\xx01.md'):
                with self.subTest(bad=bad):
                    with self.assertRaises(ValueError):
                        V2.safe_file(root, bad, 1024)

    def test_v2_validator_accepts_published_scene_with_nested_example(self):
        """真实目录树 + 追加无 legacy_ids 的新场景（子目录例文），v2 校验 0 错误。"""
        catalog = json.loads((SKILL / 'references/planning-catalog-v2.json').read_text(encoding='utf-8'))
        seed = copy.deepcopy(catalog['scenes'][0])
        source = copy.deepcopy(catalog['sources'][0])
        source.update(id='XX01', url='https://example.org/xx01-source',
                      title='扩容场景来源', popularity={
                          'status': 'popularity_unverified', 'metrics': [],
                          'observed_on': '2026-10-17', 'scope': '新增场景占位来源'})
        seed.update(id='scene.d01.xx01', legacy_ids=[], name='扩容占位场景', aliases=[],
                    example_path='examples/scenarios/new-family/xx01.md',
                    source_ids=['XX01'],
                    editorial_intent='占位剪辑意图：以子目录例文验证落点可行',
                    acceptance=['占位验收：读者能复述场景目标'])
        catalog['scenes'].append(seed)
        catalog['sources'].append(source)
        with tempfile.TemporaryDirectory() as tmp:
            target = self.copy_skill(tmp)
            example = target / seed['example_path']
            example.parent.mkdir(parents=True)
            example.write_text('\n'.join(
                [seed['editorial_intent'], *seed['acceptance'], source['url']]),
                encoding='utf-8')
            self.assertEqual(V2.validate(target, catalog), [])


if __name__ == '__main__':
    unittest.main()
