import importlib.util
import json
import re
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("skill_manifest", ROOT / "scripts/skill_manifest.py")
MANIFEST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MANIFEST)


class SkillManifestTests(unittest.TestCase):
    def test_rendered_manifest_covers_all_skills_and_capabilities(self) -> None:
        manifest = MANIFEST.render_manifest()
        self.assertEqual(manifest["schema"], "jianying-skills-manifest/v1")
        self.assertEqual(manifest["repository"], MANIFEST.CANONICAL_REPOSITORY)
        self.assertEqual(manifest["version"], "2.0.1")
        self.assertEqual(len(manifest["skills"]), 13)
        self.assertEqual(len({entry["name"] for entry in manifest["skills"]}), 13)
        self.assertIn("schema.job_v2", manifest["minimum_cli_capabilities"])
        self.assertRegex(manifest["content_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(manifest["content_state"], "release_candidate")
        self.assertIsNone(manifest["source_commit"])

    def test_recorded_manifest_matches_current_tree(self) -> None:
        recorded = json.loads((ROOT / "jianying-skills.manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(recorded, MANIFEST.render_manifest())

    def test_release_manifest_requires_clean_tagged_remote_commit(self) -> None:
        commit = "a" * 40

        def fake_git(*arguments: str) -> str:
            if arguments == ("status", "--porcelain"):
                return ""
            if arguments == ("rev-parse", "HEAD"):
                return commit
            if arguments == ("rev-parse", "v2.0.1^{commit}"):
                return commit
            raise AssertionError(arguments)

        with mock.patch.object(MANIFEST, "git", side_effect=fake_git), \
                mock.patch.object(MANIFEST, "resolve_tag", return_value=commit):
            released = MANIFEST.render_release_manifest("v2.0.1", "origin")
        self.assertEqual(released["content_state"], "released")
        self.assertEqual(released["release_ref"], "v2.0.1")
        self.assertEqual(released["source_commit"], commit)

    def test_release_manifest_rejects_dirty_or_wrong_ref(self) -> None:
        with mock.patch.object(MANIFEST, "git", return_value=" M skills/example/SKILL.md"):
            with self.assertRaisesRegex(RuntimeError, "clean working tree"):
                MANIFEST.render_release_manifest("v2.0.1", "origin")

        with mock.patch.object(MANIFEST, "git", return_value=""):
            with self.assertRaisesRegex(RuntimeError, "release ref must be v2.0.1"):
                MANIFEST.render_release_manifest("v1.9.9", "origin")

    def test_workflow_uses_immutable_actions_and_never_clobbers_manifest(self) -> None:
        action_reference = re.compile(r"^\s*-\s+uses:\s+([^\s#]+)", re.MULTILINE)
        immutable_action = re.compile(r"^[^/\s]+/[^@\s]+@[0-9a-f]{40}$")
        workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
        for workflow in workflows:
            text = workflow.read_text(encoding="utf-8")
            for reference in action_reference.findall(text):
                self.assertRegex(reference, immutable_action)
            self.assertNotIn("--clobber", text)

        release = (ROOT / ".github/workflows/release-skills.yml").read_text(encoding="utf-8")
        notify = (ROOT / ".github/workflows/notify-consumers.yml").read_text(encoding="utf-8")
        self.assertIn("--draft", release)
        self.assertIn("--json isImmutable", release)
        self.assertIn("gh release verify-asset", release)
        self.assertNotIn("gh release upload", notify)
        self.assertIn("isImmutable", notify)
        self.assertIn("gh release verify-asset", notify)
        self.assertIn("cmp \\", notify)


if __name__ == "__main__":
    unittest.main()
