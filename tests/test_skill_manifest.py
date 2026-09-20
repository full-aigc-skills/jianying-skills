import importlib.util
import json
import re
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("skill_manifest", ROOT / "scripts/skill_manifest.py")
MANIFEST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MANIFEST)
PREFLIGHT_SPEC = importlib.util.spec_from_file_location(
    "release_preflight", ROOT / "scripts" / "release_preflight.py"
)
PREFLIGHT = importlib.util.module_from_spec(PREFLIGHT_SPEC)
PREFLIGHT_SPEC.loader.exec_module(PREFLIGHT)


class SkillManifestTests(unittest.TestCase):
    def test_skill_digest_rejects_symlinked_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / "fixture-skill"
            skill.mkdir()
            outside = root / "outside.md"
            outside.write_text("external content", encoding="utf-8")
            (skill / "SKILL.md").write_text("fixture", encoding="utf-8")
            (skill / "linked.md").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "symbolic links are forbidden"):
                MANIFEST.hash_skill_dir(skill)

    def test_rendered_manifest_covers_all_skills_and_capabilities(self) -> None:
        manifest = MANIFEST.render_manifest()
        self.assertEqual(manifest["schema"], "jianying-skills-manifest/v1")
        self.assertEqual(manifest["repository"], MANIFEST.CANONICAL_REPOSITORY)
        self.assertEqual(manifest["version"], "2.0.3")
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
            if arguments == ("remote", "get-url", "origin"):
                return MANIFEST.CANONICAL_REPOSITORY
            if arguments == ("rev-parse", "HEAD"):
                return commit
            if arguments == ("rev-parse", "v2.0.3^{commit}"):
                return commit
            raise AssertionError(arguments)

        with mock.patch.object(MANIFEST, "git", side_effect=fake_git), \
                mock.patch.object(MANIFEST, "resolve_tag", return_value=commit):
            released = MANIFEST.render_release_manifest("v2.0.3", "origin")
        self.assertEqual(released["content_state"], "released")
        self.assertEqual(released["release_ref"], "v2.0.3")
        self.assertEqual(released["source_commit"], commit)

    def test_release_manifest_rejects_dirty_or_wrong_ref(self) -> None:
        with mock.patch.object(MANIFEST, "git", return_value=" M skills/example/SKILL.md"):
            with self.assertRaisesRegex(RuntimeError, "clean working tree"):
                MANIFEST.render_release_manifest("v2.0.3", "origin")

        with mock.patch.object(MANIFEST, "git", return_value=""):
            with self.assertRaisesRegex(RuntimeError, "release ref must be v2.0.3"):
                MANIFEST.render_release_manifest("v1.9.9", "origin")

    def test_release_manifest_rejects_noncanonical_remote_before_tag_resolution(self) -> None:
        def fake_git(*arguments: str) -> str:
            if arguments == ("status", "--porcelain"):
                return ""
            if arguments == ("remote", "get-url", "origin"):
                return "/tmp/jianying-release-simulation"
            raise AssertionError(arguments)

        with mock.patch.object(MANIFEST, "git", side_effect=fake_git), \
                mock.patch.object(MANIFEST, "resolve_tag") as resolve_tag:
            with self.assertRaisesRegex(RuntimeError, "canonical GitHub repository"):
                MANIFEST.render_release_manifest("v2.0.3", "origin")
        resolve_tag.assert_not_called()

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
        self.assertIn("concurrency:\n  group: ${{ github.workflow }}-${{ github.ref }}", release)
        self.assertIn("cancel-in-progress: false", release)
        self.assertIn("workflow_dispatch:", release)
        self.assertIn("permissions:\n  contents: read", release)
        self.assertIn(
            "\n  publish:\n    if: startsWith(github.ref, 'refs/tags/v')\n"
            "    needs: validate\n",
            release,
        )
        self.assertIn("permissions:\n      contents: write", release)
        self.assertIn("name: jianying-skills-release-manifest", release)
        self.assertIn("--draft", release)
        self.assertIn("immutable-releases", release)
        self.assertGreaterEqual(
            release.count('--repository "$GITHUB_REPOSITORY"'), 3,
        )
        self.assertIn("gh release verify-asset", release)
        self.assertIn("asset attestation not visible yet", release)
        self.assertIn("existing immutable release matches this manifest", release)
        self.assertIn("scripts/release_publication_plan.py", release)
        self.assertGreaterEqual(release.count("--remote origin"), 2)
        self.assertGreaterEqual(release.count('--expected-commit "$(git rev-parse HEAD)"'), 2)
        self.assertIn("resuming a byte-identical partial draft release", release)
        self.assertNotIn('gh release view "$GITHUB_REF_NAME"', release)
        self.assertIn(
            'test "$(jq -r .action "$release_plan")" = "verify_existing"',
            release,
        )
        self.assertIn('if [ "$publication_action" != "verify_existing" ]; then', release)
        self.assertIn("for attempt in $(seq 1 30)", release)
        self.assertIn('gh release download "$GITHUB_REF_NAME"', release)
        self.assertNotIn("release already exists; refusing to replace immutable assets", release)
        self.assertIn("jianying-edit-plugin/dispatches", release)
        self.assertIn("client_payload[manifest_sha256]", release)
        self.assertNotIn("gh release upload", notify)
        self.assertIn("isImmutable", notify)
        self.assertIn("gh release verify-asset", notify)
        self.assertIn("cmp \\", notify)
        self.assertIn("client_payload[manifest_sha256]", notify)
        self.assertIn("Validate release tag and immutable repository setting", release)
        self.assertIn("tag ${GITHUB_REF_NAME} does not match package version", release)
        self.assertIn("enable GitHub immutable releases before running release checks", release)
        self.assertIn("scripts/release_preflight.py", release)
        self.assertIn(
            "secrets.RELEASE_RULESET_READ_TOKEN || github.token", release
        )
        self.assertIn('--output "$RUNNER_TEMP/release-preflight.json"', release)
        self.assertIn("name: jianying-skills-remote-preflight", release)
        self.assertIn("path: ${{ runner.temp }}/release-preflight.json", release)
        self.assertNotIn("--output release-preflight.json", release)
        self.assertIn('if [[ "$GITHUB_REF" == refs/tags/v* ]]', release)
        self.assertIn('exit "$preflight_status"', release)
        for step in (
            "Validate release tag and immutable repository setting",
            "Generate the immutable release manifest before publication",
            "Publish manifest through a draft release",
            "Notify consumer repositories",
        ):
            self.assertIn(
                f"- name: {step}\n        if: startsWith(github.ref, 'refs/tags/v')",
                release,
                f"manual candidate validation must skip {step}",
            )
        self.assertLess(
            release.index("scripts/release_preflight.py"),
            release.index("python3 scripts/lint_skills.py"),
        )

    def test_remote_preflight_distinguishes_prerequisites_from_release_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".claude-plugin").mkdir()
            (root / ".claude-plugin/plugin.json").write_text(
                json.dumps({"version": "2.0.3"}),
                encoding="utf-8",
            )

            def query(arguments: list[str]) -> dict:
                if arguments[0] == "api" and "immutable-releases" in arguments[1]:
                    return {"enabled": True}
                if arguments[0] == "api" and "rulesets" in arguments[1]:
                    return PREFLIGHT.release_tag_ruleset_fixture()
                raise PREFLIGHT.RemoteQueryError("release not found")

            report = PREFLIGHT.build_report(root, query)
            self.assertTrue(report["prerequisitesReady"])
            self.assertFalse(report["releaseComplete"])
            self.assertEqual(report["blockedPrerequisites"], [])
            self.assertEqual(report["blocked"], ["release.expected"])
            self.assertEqual(report["expected"]["ref"], "v2.0.3")

    def test_remote_preflight_blocks_disabled_immutable_releases(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".claude-plugin").mkdir()
            (root / ".claude-plugin/plugin.json").write_text(
                json.dumps({"version": "2.0.3"}),
                encoding="utf-8",
            )

            def query(arguments: list[str]) -> dict:
                if arguments[0] == "api" and "immutable-releases" in arguments[1]:
                    return {"enabled": False}
                if arguments[0] == "api" and "rulesets" in arguments[1]:
                    return PREFLIGHT.release_tag_ruleset_fixture()
                return {
                    "tagName": "v2.0.3",
                    "isDraft": False,
                    "isPrerelease": False,
                    "isImmutable": True,
                    "publishedAt": "2026-09-20T00:00:00Z",
                }

            report = PREFLIGHT.build_report(root, query)
            self.assertFalse(report["prerequisitesReady"])
            self.assertFalse(report["releaseComplete"])
            self.assertEqual(
                report["blockedPrerequisites"],
                ["repository.immutable_releases"],
            )

    def test_remote_preflight_requires_active_non_bypassable_tag_protection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".claude-plugin").mkdir()
            (root / ".claude-plugin/plugin.json").write_text(
                json.dumps({"version": "2.0.3"}),
                encoding="utf-8",
            )

            def query(arguments: list[str]) -> dict:
                if "immutable-releases" in " ".join(arguments):
                    return {"enabled": True}
                if "rulesets" in " ".join(arguments):
                    return []
                raise PREFLIGHT.RemoteQueryError("release not found")

            report = PREFLIGHT.build_report(root, query)
            self.assertFalse(report["prerequisitesReady"])
            self.assertEqual(
                report["blockedPrerequisites"],
                ["repository.release_tag_protection"],
            )

    def test_remote_preflight_loads_inherited_ruleset_detail(self) -> None:
        self_link = (
            "https://api.github.com/orgs/full-aigc-skills/rulesets/42"
        )

        def query(arguments: list[str]) -> object:
            if arguments[1] == self_link:
                return PREFLIGHT.release_tag_ruleset_fixture()[0]
            return [{"id": 42, "_links": {"self": {"href": self_link}}}]

        details = PREFLIGHT.load_release_tag_rulesets(query, PREFLIGHT.REPOSITORY)
        self.assertTrue(PREFLIGHT.release_tags_are_protected(details))


if __name__ == "__main__":
    unittest.main()
