"""视频质量档案合同测试。"""
import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jianying-video-planning'


class QualityProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        validator = ROOT / 'scripts/validate_quality_profiles.py'
        if not validator.is_file():
            raise AssertionError('quality profile validator is not implemented')
        spec = importlib.util.spec_from_file_location('quality_profiles', validator)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def setUp(self):
        file = SKILL / 'references/quality-profiles-v1.json'
        self.assertTrue(file.is_file(), 'quality profile catalog is not implemented')
        self.catalog = self.module.parse_json(file.read_text())

    def validate(self):
        return self.module.validate(SKILL, self.catalog)

    def test_three_representative_profiles_are_valid_and_digest_is_stable(self):
        self.assertEqual(self.validate(), [])
        profiles = {item['profile_id']: item for item in self.catalog['profiles']}
        self.assertEqual(set(profiles), {
            'vlog.personal-story',
            'course.multi-delivery',
            'wedding.multi-purpose',
        })
        first = self.module.canonical_digest(self.catalog)
        second = self.module.canonical_digest(
            self.module.parse_json(json.dumps(self.catalog, ensure_ascii=False, sort_keys=True))
        )
        self.assertEqual(first, second)
        self.assertRegex(first, r'^[0-9a-f]{64}$')

    def test_duplicate_identity_and_unknown_references_are_rejected(self):
        self.catalog['profiles'].append(copy.deepcopy(self.catalog['profiles'][0]))
        self.assertTrue(any(item['code'] == 'profile_identity_conflict' for item in self.validate()))

        self.setUp()
        self.catalog['profiles'][0]['metadata']['partme.workflow_ids'] = ['UNKNOWN']
        self.assertTrue(any(item['code'] == 'profile_reference_invalid' for item in self.validate()))

        self.setUp()
        self.catalog['profiles'][0]['metadata']['partme.source_ids'] = ['UNKNOWN']
        self.assertTrue(any(item['code'] == 'profile_reference_invalid' for item in self.validate()))

    def test_unknown_field_unregistered_action_and_duplicate_dimension_are_rejected(self):
        self.catalog['profiles'][0]['command'] = 'rm -rf /tmp/example'
        self.assertTrue(any(item['code'] == 'profile_schema_invalid' for item in self.validate()))

        self.setUp()
        self.catalog['profiles'][0]['allowed_actions'].append('shell')
        self.assertTrue(any(item['code'] == 'profile_action_invalid' for item in self.validate()))

        self.setUp()
        duplicate = copy.deepcopy(self.catalog['profiles'][0]['dimensions'][0])
        self.catalog['profiles'][0]['dimensions'].append(duplicate)
        self.assertTrue(any(item['code'] == 'profile_identity_conflict' for item in self.validate()))

    def test_forbidden_execution_fields_are_rejected_at_any_depth(self):
        self.catalog['profiles'][0]['metadata']['partme.runtime'] = {'handler': 'execute'}
        self.assertTrue(any(item['code'] == 'profile_execution_field' for item in self.validate()))

    def test_profiles_keep_hard_gates_and_human_boundaries(self):
        profiles = {item['profile_id']: item for item in self.catalog['profiles']}
        for profile in profiles.values():
            self.assertTrue(profile['human_boundaries'])
            self.assertTrue(any(item['hard_gate'] for item in profile['dimensions']))
            self.assertTrue(all(item['evidence_types'] for item in profile['dimensions']))
        wedding = profiles['wedding.multi-purpose']
        license_gate = next(item for item in wedding['dimensions']
                            if item['dimension_id'] == 'commercial_usage_authorization')
        self.assertTrue(license_gate['hard_gate'])

    def test_profile_dimensions_cover_the_three_representative_workflows(self):
        profiles = {item['profile_id']: {dimension['dimension_id'] for dimension in item['dimensions']}
                    for item in self.catalog['profiles']}
        self.assertTrue({
            'narrative_establishment', 'narrative_change', 'ending_reflection',
            'pacing_and_repetition', 'audio_visual_coherence', 'personal_privacy',
        }.issubset(profiles['vlog.personal-story']))
        self.assertTrue({
            'instructional_completeness', 'teaser_context_fidelity',
            'subtitle_timing_and_layout', 'bilingual_accuracy', 'delivery_isolation',
        }.issubset(profiles['course.multi-delivery']))
        self.assertTrue({
            'ceremony_continuity', 'emotional_arc', 'commercial_usage_authorization',
            'purpose_isolation', 'multi_camera_integrity',
        }.issubset(profiles['wedding.multi-purpose']))

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'profile_duplicate_key'):
            self.module.parse_json('{"schema":1,"schema":2}')


if __name__ == '__main__':
    unittest.main()
