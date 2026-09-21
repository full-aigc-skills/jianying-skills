import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jianying-video-planning'
SPEC = importlib.util.spec_from_file_location('video_catalog', ROOT / 'scripts/validate_video_catalog.py')
CATALOG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CATALOG)


class VideoPlanningTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((SKILL / 'references/video-taxonomy.json').read_text())

    def test_108_real_examples_and_source_capability_references(self):
        self.assertEqual(CATALOG.validate(SKILL, self.catalog), [])

    def test_duplicate_or_traversal_is_rejected(self):
        self.catalog['scenes'][1]['id'] = self.catalog['scenes'][0]['id']
        self.catalog['scenes'][0]['example'] = '../outside.md'
        errors = CATALOG.validate(SKILL, self.catalog)
        self.assertTrue(any('duplicate' in e for e in errors))
        self.assertTrue(any('path' in e for e in errors))

    def test_unknown_recipe_and_capability_are_rejected(self):
        self.catalog['scenes'][0]['recipe'] = 'unknown'
        self.catalog['scenes'][1]['required_capabilities'].append('video.magic')
        errors = CATALOG.validate(SKILL, self.catalog)
        self.assertTrue(any('recipe' in e for e in errors))
        self.assertTrue(any('capability' in e for e in errors))

    def test_granular_install_is_self_contained(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'jianying-video-planning'
            shutil.copytree(SKILL, target)
            self.assertEqual(CATALOG.validate(target, self.catalog), [])

    def test_popularity_requires_metric(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'skill'
            shutil.copytree(SKILL, target)
            path = target / 'references/source-index.json'
            sources = json.loads(path.read_text())
            sources['sources'][0]['popularity'] = {'status': 'measured', 'metrics': []}
            path.write_text(json.dumps(sources))
            self.assertTrue(any('popularity' in e for e in CATALOG.validate(target, self.catalog)))
