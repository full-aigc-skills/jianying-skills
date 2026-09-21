import importlib.util
import re
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lint_skills", ROOT / "scripts/lint_skills.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)


class ContractMatrixTests(unittest.TestCase):
    PANEL_SKILLS = {
        "jianying-media": "media.",
        "jianying-audio": "audio.",
        "jianying-text": "text.",
        "jianying-stickers": "sticker.",
        "jianying-effects": "effect.",
        "jianying-transitions": "transition.",
        "jianying-subtitles": "caption.",
        "jianying-smart-package": "smart_package.",
        "jianying-filters": "filter.",
        "jianying-adjustments": "adjustment.",
        "jianying-templates": "template.",
        "jianying-digital-human": "digital_human.",
        "jianying-editing-console": "console.",
    }

    def test_package_exposes_twenty_four_product_skills(self) -> None:
        published = sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))
        auxiliary = sorted(
            path
            for root in (".agents", ".kimi-code", ".zcode")
            for path in (ROOT / root / "skills").glob("*/SKILL.md")
        )
        self.assertEqual(len(published), 24)
        self.assertTrue(set(self.PANEL_SKILLS) <= set(published))
        self.assertEqual(auxiliary, [], "development integrations must not leak into npx skills add")

    def test_each_panel_skill_describes_semantic_operation_routes(self) -> None:
        forbidden = ("screen_coordinate", "coordinates", "固定坐标", "坐标点击")
        for name, prefix in self.PANEL_SKILLS.items():
            workflow = ROOT / "skills" / name / "references" / "workflow.md"
            self.assertTrue(workflow.is_file(), name)
            text = workflow.read_text(encoding="utf-8")
            for marker in ("## 功能动线", "语义动作", "执行路由", "验证", "恢复"):
                self.assertIn(marker, text, f"{name}: missing {marker}")
            self.assertIn(prefix, text, f"{name}: missing semantic action prefix")
            self.assertFalse(any(value in text for value in forbidden), name)

    def test_panel_operation_routes_are_unique_and_broadly_enumerated(self) -> None:
        operation_id = re.compile(r"`([a-z][a-z0-9_]*(?:\.[a-z0-9_]+){2,})`")
        observed = []
        for name, prefix in self.PANEL_SKILLS.items():
            text = (ROOT / "skills" / name / "references" / "workflow.md").read_text(
                encoding="utf-8"
            )
            routes = [value for value in operation_id.findall(text) if value.startswith(prefix)]
            self.assertGreaterEqual(len(routes), 6, name)
            observed.extend(routes)
        self.assertGreaterEqual(len(observed), 100)
        self.assertEqual(len(observed), len(set(observed)), "semantic operation IDs must be unique")

    def test_current_matrix_is_complete_and_preserves_unfinished_runtime_gates(self) -> None:
        matrix = LINT.load_contract_matrix(ROOT / "docs/RUST_CLI_SKILL_MATRIX.json")
        skills = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
        self.assertEqual(LINT.validate_contract_matrix(matrix, skills, None), [])
        planning = next(row for row in matrix["skills"] if row["name"] == "jianying-video-planning")
        self.assertEqual(planning["migration_state"], "candidate_validated")
        self.assertEqual(planning["success_evidence"], "plan")
        self.assertFalse(any(row["migration_state"] == "ready" for row in matrix["skills"]))
        panel = {row["name"]: row for row in matrix["skills"]
                 if row["name"] in self.PANEL_SKILLS}
        self.assertEqual(set(panel), set(self.PANEL_SKILLS))
        self.assertEqual(panel["jianying-adjustments"]["migration_state"], "blocked_on_gui_adapter")
        self.assertEqual(panel["jianying-digital-human"]["migration_state"], "blocked_on_provider_and_gui")

    def test_ready_skill_requires_supported_cli_capabilities(self) -> None:
        matrix = {
            "schema": "jianying-skill-contract-matrix/v1",
            "skills": [{
                "name": "jianying-use",
                "minimum_cli_version": "1.6.0",
                "required_capabilities": ["doctor", "capabilities"],
                "risk_level": "read_only",
                "success_evidence": "structural",
                "migration_state": "ready"
            }]
        }
        errors = LINT.validate_contract_matrix(matrix, ["jianying-use"], None)
        self.assertTrue(any("capability manifest" in error for error in errors))

        manifest = {"capabilities": [{"id": "doctor", "status": "supported"}]}
        errors = LINT.validate_contract_matrix(matrix, ["jianying-use"], manifest)
        self.assertTrue(any("capabilities" in error for error in errors))

    def test_non_ready_skill_still_rejects_unknown_capability_ids(self) -> None:
        matrix = {
            "schema": "jianying-skill-contract-matrix/v1",
            "skills": [{
                "name": "jianying-media",
                "minimum_cli_version": "1.6.19",
                "required_capabilities": ["media.probe", "project.concat"],
                "risk_level": "reversible_write",
                "success_evidence": "cold_reopen",
                "migration_state": "blocked_on_gui_adapter"
            }]
        }
        manifest = {"capabilities": [{"id": "media.probe", "status": "supported"}]}
        errors = LINT.validate_contract_matrix(matrix, ["jianying-media"], manifest)
        self.assertTrue(any("unknown capability" in error for error in errors))

    def test_every_skill_has_a_self_contained_rust_cli_contract(self) -> None:
        matrix = LINT.load_contract_matrix(ROOT / "docs/RUST_CLI_SKILL_MATRIX.json")
        rows = {row["name"]: row for row in matrix["skills"]}
        errors = []
        for skill_dir in sorted((ROOT / "skills").iterdir()):
            if skill_dir.is_dir():
                errors.extend(LINT.validate_skill_contract(skill_dir, rows[skill_dir.name]))
        self.assertEqual(errors, [])

    def test_each_skill_survives_granular_install(self) -> None:
        matrix = LINT.load_contract_matrix(ROOT / "docs/RUST_CLI_SKILL_MATRIX.json")
        rows = {row["name"]: row for row in matrix["skills"]}
        with tempfile.TemporaryDirectory() as directory:
            install_root = Path(directory)
            for source in sorted((ROOT / "skills").iterdir()):
                if not source.is_dir():
                    continue
                installed = install_root / source.name
                shutil.copytree(source, installed)
                self.assertEqual(
                    LINT.validate_skill_contract(installed, rows[source.name]),
                    [],
                    source.name,
                )
                shutil.rmtree(installed)

    def test_retired_headless_plan_schema_is_rejected_in_supporting_files(self) -> None:
        matrix = LINT.load_contract_matrix(ROOT / "docs/RUST_CLI_SKILL_MATRIX.json")
        row = next(item for item in matrix["skills"] if item["name"] == "jianying-harness")
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "jianying-harness"
            shutil.copytree(ROOT / "skills" / "jianying-harness", installed)
            stale = installed / "references" / "stale-plan.md"
            stale.write_text("schema: jy14-headless-plan/v1\n", encoding="utf-8")
            errors = LINT.validate_skill_contract(installed, row)
        self.assertTrue(any("retired external headless plan schema" in error for error in errors))

    def test_package_manifest_discovers_all_skills_in_order(self) -> None:
        names = [path.name for path in sorted((ROOT / "skills").iterdir()) if path.is_dir()]
        self.assertEqual(
            LINT.validate_package_manifest(ROOT / ".claude-plugin/plugin.json", names),
            [],
        )


if __name__ == "__main__":
    unittest.main()
