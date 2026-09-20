import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lint_skills", ROOT / "scripts/lint_skills.py")
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)


class ContractMatrixTests(unittest.TestCase):
    def test_package_exposes_only_the_thirteen_product_skills(self) -> None:
        published = sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))
        auxiliary = sorted(
            path
            for root in (".agents", ".kimi-code", ".zcode")
            for path in (ROOT / root / "skills").glob("*/SKILL.md")
        )
        self.assertEqual(len(published), 13)
        self.assertEqual(auxiliary, [], "development integrations must not leak into npx skills add")

    def test_current_matrix_is_complete_but_not_ready(self) -> None:
        matrix = LINT.load_contract_matrix(ROOT / "docs/RUST_CLI_SKILL_MATRIX.json")
        skills = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
        self.assertEqual(LINT.validate_contract_matrix(matrix, skills, None), [])
        self.assertTrue(all(row["migration_state"] == "blocked_on_cli_contract" for row in matrix["skills"]))

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
