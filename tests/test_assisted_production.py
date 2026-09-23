import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_assisted_workflows.py"
SPEC = importlib.util.spec_from_file_location("assisted_workflows", SCRIPT)
ASSISTED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ASSISTED)

PLANNING = ROOT / "skills/jianying-video-planning"
MOTION = ROOT / "skills/jianying-motion"
MEDIA = ROOT / "skills/jianying-media"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AssistedProductionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load(PLANNING / "references/assisted-production-workflows-v1.json")
        self.events = load(MOTION / "examples/interaction-events-v1.json")
        self.zoom = load(MOTION / "examples/smart-zoom-plan-v1.json")
        self.preflight = load(MEDIA / "examples/media-preflight-v1.json")

    def test_repository_contract_is_valid(self):
        self.assertEqual(ASSISTED.validate_repository(ROOT), [])

    def test_catalog_rejects_duplicate_recipe_and_execution_fields(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["recipes"][1]["id"] = catalog["recipes"][0]["id"]
        catalog["recipes"][0]["command"] = "python smart_zoomer.py"
        errors = ASSISTED.validate_catalog(catalog)
        self.assertTrue(any("duplicate recipe" in error for error in errors))
        self.assertTrue(any("execution field" in error for error in errors))

    def test_catalog_rejects_unknown_step_and_missing_source_pin(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["source_baseline"]["commit"] = "main"
        catalog["recipes"][0]["steps"].append("unknown.execute")
        errors = ASSISTED.validate_catalog(catalog)
        self.assertTrue(any("source commit" in error for error in errors))
        self.assertTrue(any("unknown step" in error for error in errors))

    def test_interaction_events_reject_keyboard_and_invalid_coordinates(self):
        events = copy.deepcopy(self.events)
        events["capture"]["keyboard_content_captured"] = True
        events["events"][0]["x"] = 1.2
        events["events"][1]["time_us"] = events["events"][0]["time_us"] - 1
        errors = ASSISTED.validate_interaction_events(events)
        self.assertTrue(any("keyboard" in error for error in errors))
        self.assertTrue(any("normalized coordinate" in error for error in errors))
        self.assertTrue(any("time order" in error for error in errors))

    def test_smart_zoom_rejects_unbound_media_and_unsafe_scale(self):
        zoom = copy.deepcopy(self.zoom)
        zoom["source_media_sha256"] = "0" * 64
        zoom["constraints"]["max_scale"] = 3.0
        zoom["sessions"][0]["keyframes"][1]["time_us"] = -1
        errors = ASSISTED.validate_smart_zoom_plan(zoom, self.events)
        self.assertTrue(any("media digest" in error for error in errors))
        self.assertTrue(any("max_scale" in error for error in errors))
        self.assertTrue(any("keyframe time" in error for error in errors))

    def test_media_preflight_rejects_path_digest_and_unaccounted_derivative(self):
        preflight = copy.deepcopy(self.preflight)
        preflight["source"]["sha256"] = "md5-of-path"
        preflight["derivative"].pop("sha256")
        errors = ASSISTED.validate_media_preflight(preflight)
        self.assertTrue(any("source sha256" in error for error in errors))
        self.assertTrue(any("derivative sha256" in error for error in errors))

    def test_granular_contract_files_are_self_contained(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for skill in (PLANNING, MOTION, MEDIA):
                shutil.copytree(skill, root / skill.name)
            self.assertEqual(ASSISTED.validate_granular_install(root), [])


if __name__ == "__main__":
    unittest.main()
