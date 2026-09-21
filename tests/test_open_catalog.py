"""开放目录行为测试；fixture 不计入正式场景数。"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jianying-video-planning'
FIXTURE = ROOT / 'tests/fixtures/open_catalog_v2.json'


class OpenCatalogTests(unittest.TestCase):
    def setUp(self):
        file = ROOT / 'scripts/validate_open_catalog.py'
        self.assertTrue(file.is_file(), 'v2 validator is not implemented')
        spec = importlib.util.spec_from_file_location('open_catalog', file)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.catalog = json.loads(FIXTURE.read_text())
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'examples/scenarios').mkdir(parents=True)
        (self.root / 'examples/scenarios/vg01.md').write_text('fixture')

    def check(self, **kwargs):
        return self.module.validate(self.root, self.catalog, allow_test=True, **kwargs)

    def test_cardinality_not_business_limit(self):
        for count in (1, 109, 1000):
            with self.subTest(count=count):
                seed = copy.deepcopy(self.catalog['scenes'][0])
                self.catalog['scenes'] = []
                for index in range(count):
                    scene = copy.deepcopy(seed)
                    scene.update(id=f'scene.life.case_{index}', legacy_ids=['VG01'] if index == 0 else [], aliases=[])
                    self.catalog['scenes'].append(scene)
                self.assertEqual(self.check(), [])

    def test_recipe_and_source_counts_are_independent_from_scene_count(self):
        second_recipe = copy.deepcopy(self.catalog['recipes'][0])
        second_recipe['id'] = 'R02'
        second_source = copy.deepcopy(self.catalog['sources'][0])
        second_source['id'] = 'source2'
        second_source['url'] = 'https://example.org/second-fixture'
        second = copy.deepcopy(self.catalog['scenes'][0])
        second.update(id='scene.life.second', legacy_ids=[], aliases=[], primary_recipe_id='R02',
                      source_ids=['source1', 'source2'])
        self.catalog['recipes'].append(second_recipe)
        self.catalog['sources'].append(second_source)
        self.catalog['scenes'].append(second)
        self.assertEqual(self.check(), [])
        self.assertEqual((len(self.catalog['scenes']), len(self.catalog['recipes']), len(self.catalog['sources'])),
                         (2, 2, 2))
        self.catalog['scenes'].append({**copy.deepcopy(second), 'id': 'scene.life.third',
                                       'source_ids': ['source1']})
        self.assertEqual(self.check(), [])

    def test_formal_source_requires_method_and_popularity_provenance(self):
        self.catalog['scenes'][0]['status'] = 'published_knowledge'
        self.catalog['sources'][0]['access_scope'] = 'test_fixture'
        self.assertTrue(any(e['code'] == 'catalog_source_invalid' for e in self.check()))
        self.catalog = json.loads(FIXTURE.read_text())
        self.catalog['scenes'][0]['status'] = 'published_knowledge'
        self.catalog['sources'][0]['popularity']['status'] = 'measured'
        self.catalog['sources'][0]['popularity']['metrics'] = []
        self.assertTrue(any(e['code'] == 'catalog_source_invalid' for e in self.check()))

    def test_duplicate_reference_schema_empty_and_unknown_field(self):
        for change, code in [
            (lambda c: c['scenes'].append(copy.deepcopy(c['scenes'][0])), 'catalog_identity_conflict'),
            (lambda c: c['scenes'][0].update(primary_recipe_id='missing'), 'catalog_reference_invalid'),
            (lambda c: c.update(schema='v999'), 'unsupported_catalog_schema'),
            (lambda c: c.update(scenes=[]), 'catalog_empty'),
            (lambda c: c['scenes'][0].update(handler='evil'), 'catalog_schema_invalid'),
        ]:
            self.catalog = json.loads(FIXTURE.read_text())
            change(self.catalog)
            self.assertTrue(any(e['code'] == code for e in self.check()), code)

    def test_file_boundaries_and_limits(self):
        for bad in ('../escape.md', '/tmp/escape.md', 'examples/../vg01.md', 'C:\\escape.md'):
            self.catalog['scenes'][0]['example_path'] = bad
            self.assertTrue(any(e['code'] == 'catalog_path_invalid' for e in self.check()))
        self.catalog = json.loads(FIXTURE.read_text())
        self.assertTrue(any(e['code'] == 'catalog_resource_limit' for e in self.check(max_example_bytes=1)))
        target = self.root / 'examples/scenarios/vg01.md'
        target.unlink()
        target.symlink_to(FIXTURE)
        self.assertTrue(any(e['code'] == 'catalog_path_invalid' for e in self.check()))

    def test_test_fixture_cannot_release(self):
        self.assertTrue(any(e['code'] == 'catalog_test_fixture' for e in self.module.validate(self.root, self.catalog)))

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(ValueError, 'catalog_duplicate_key'):
            self.module.parse_json('{"schema":1,"schema":2}')

    def test_seed_migration_preserves_old_ids_and_examples(self):
        file = SKILL / 'references/planning-catalog-v2.json'
        self.assertTrue(file.is_file(), 'v2 seed migration is not implemented')
        catalog = json.loads(file.read_text())
        self.assertEqual(self.module.validate(SKILL, catalog), [])
        old = json.loads((SKILL / 'references/video-taxonomy.json').read_text())
        mapping = {alias: scene for scene in catalog['scenes'] for alias in scene['legacy_ids']}
        self.assertEqual(set(mapping), {s['id'] for s in old['scenes']})
        for scene in old['scenes']:
            self.assertEqual(mapping[scene['id']]['example_path'], scene['example'])
            self.assertEqual(mapping[scene['id']]['primary_recipe_id'], scene['recipe'])
            self.assertEqual(mapping[scene['id']]['name'], scene['name'])

    def test_frozen_v1_bytes(self):
        baseline = json.loads((ROOT / 'tests/fixtures/legacy_planning_v1.json').read_text())
        for file, digest in baseline['files'].items():
            self.assertEqual(hashlib.sha256((SKILL / file).read_bytes()).hexdigest(), digest, file)

    def test_malformed_identity_and_duplicate_dimension_values(self):
        self.catalog['scenes'][0]['id'] = []
        self.assertTrue(any(e['code'] == 'catalog_schema_invalid' for e in self.check()))
        self.catalog = json.loads(FIXTURE.read_text())
        self.catalog['dimensions'][0]['values'].append({'id': 'personal', 'name': 'another name'})
        self.assertTrue(any(e['code'] == 'catalog_identity_conflict' for e in self.check()))

    def test_manifest_refuses_invalid_open_catalog(self):
        spec = importlib.util.spec_from_file_location('skill_manifest_open', ROOT / 'scripts/skill_manifest.py')
        manifest = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(manifest)
        planning = self.root / 'skills/jianying-video-planning/references'
        planning.mkdir(parents=True)
        (planning / 'planning-catalog-v2.json').write_text(json.dumps(self.catalog))
        with mock.patch.object(manifest, 'ROOT', self.root):
            with self.assertRaisesRegex(ValueError, 'open catalog'):
                manifest.render_manifest()

    def test_representative_workflow_knowledge_vectors(self):
        file = SKILL / 'references/representative-workflows-v1.json'
        self.assertTrue(file.is_file(), 'representative workflow knowledge is not implemented')
        vectors = self.module.parse_json(file.read_text())
        self.assertEqual(vectors['schema'], 'jianying-representative-workflows/v1')
        by_id = {item['id']: item for item in vectors['workflows']}
        self.assertEqual(set(by_id), {'VLOG-01', 'COURSE-01', 'WEDDING-01'})
        self.assertEqual(by_id['VLOG-01']['scene_ids'], ['VG01'])
        self.assertEqual(by_id['VLOG-01']['recipe_ids'], ['R01'])
        self.assertIn('生活主线', by_id['VLOG-01']['acceptance'])
        self.assertEqual(len(by_id['COURSE-01']['outputs']), 4)
        self.assertEqual(by_id['COURSE-01']['recipe_ids'], ['R06', 'R11'])
        self.assertEqual(by_id['COURSE-01']['subtitle_languages'], ['zh-CN', 'en'])
        self.assertEqual(len(by_id['WEDDING-01']['outputs']), 3)
        self.assertEqual(by_id['WEDDING-01']['recipe_ids'], ['R03', 'R02', 'R04'])
        self.assertEqual(by_id['WEDDING-01']['multi_camera'], 'awaiting_capability')
        for item in by_id.values():
            self.assertTrue(item['asset_requirements'])
            self.assertTrue(item['acceptance'])
            self.assertTrue(item['guardrails'])
