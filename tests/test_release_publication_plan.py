"""技能不可变 Release 的 Draft 恢复契约。"""

import importlib.util
import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "release_publication_plan", ROOT / "scripts" / "release_publication_plan.py"
)
PLAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLAN)
ATTESTATION_SPEC = importlib.util.spec_from_file_location(
    "verify_release_attestation", ROOT / "scripts" / "verify_release_attestation.py"
)
ATTESTATION = importlib.util.module_from_spec(ATTESTATION_SPEC)
ATTESTATION_SPEC.loader.exec_module(ATTESTATION)


class ReleasePublicationPlanTests(unittest.TestCase):
    def test_release_attestation_binds_commit_and_exact_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            asset = Path(temporary) / "jianying-skills.manifest.json"
            asset.write_bytes(b"manifest")
            commit = "a" * 40
            evidence = {"verificationResult": {"statement": {
                "predicate": {"repository": "full-aigc-skills/jianying-skills", "tag": "v2.0.3"},
                "subject": [
                    {"uri": "pkg:github/full-aigc-skills/jianying-skills@v2.0.3", "digest": {"sha1": commit}},
                    {"name": asset.name, "digest": {"sha256": hashlib.sha256(b"manifest").hexdigest()}},
                ],
            }}}
            ATTESTATION.verify(evidence, "full-aigc-skills/jianying-skills", "v2.0.3", commit, [asset])
            evidence["verificationResult"]["statement"]["predicate"]["tag"] = "v2.0.2"
            with self.assertRaisesRegex(ValueError, "repository or tag differs"):
                ATTESTATION.verify(evidence, "full-aigc-skills/jianying-skills", "v2.0.3", commit, [asset])

    def test_release_query_treats_only_explicit_http_404_as_absent(self) -> None:
        def missing(*_args, **_kwargs):
            return subprocess.CompletedProcess(
                [], 1, '{"message":"Not Found","status":"404"}\n',
                "gh: Not Found (HTTP 404)\n",
            )

        self.assertIsNone(PLAN.query_release_metadata(
            "full-aigc-skills/jianying-skills", "v2.0.3", missing,
        ))

        def server_error(*_args, **_kwargs):
            return subprocess.CompletedProcess(
                [], 1, '{"message":"server error","status":"500"}\n',
                "gh: server error (HTTP 500)\n",
            )

        with self.assertRaisesRegex(ValueError, "cannot query GitHub release"):
            PLAN.query_release_metadata(
                "full-aigc-skills/jianying-skills", "v2.0.3", server_error,
            )

    def test_annotated_remote_tag_must_peel_to_expected_commit(self) -> None:
        release_ref = "v2.0.3"
        commit = "a" * 40
        output = (
            f"{'b' * 40}\trefs/tags/{release_ref}\n"
            f"{commit}\trefs/tags/{release_ref}^{{}}\n"
        )
        self.assertEqual(
            PLAN.verify_remote_tag_output(output, release_ref, commit), commit
        )
        with self.assertRaisesRegex(ValueError, "remote tag commit differs"):
            PLAN.verify_remote_tag_output(output, release_ref, "c" * 40)

    def test_partial_draft_resumes_but_complete_draft_publishes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = root / "jianying-skills.manifest.json"
            manifest.write_bytes(b"manifest")
            empty = {
                "tagName": "v2.0.3",
                "isDraft": True,
                "isPrerelease": False,
                "isImmutable": False,
                "assets": [],
            }
            resumed = PLAN.plan_publication(empty, [manifest], "v2.0.3")
            self.assertEqual(resumed["action"], "resume_draft")
            self.assertEqual(resumed["missing"], [str(manifest)])

            empty["assets"] = [PLAN.describe_expected(manifest)]
            complete = PLAN.plan_publication(empty, [manifest], "v2.0.3")
            self.assertEqual(complete["action"], "publish_draft")
            self.assertEqual(complete["missing"], [])

    def test_draft_content_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / "jianying-skills.manifest.json"
            manifest.write_bytes(b"manifest")
            asset = PLAN.describe_expected(manifest)
            asset["digest"] = "sha256:" + "0" * 64
            with self.assertRaisesRegex(ValueError, "digest differs"):
                PLAN.plan_publication(
                    {
                        "tagName": "v2.0.3",
                        "isDraft": True,
                        "isPrerelease": False,
                        "isImmutable": False,
                        "assets": [asset],
                    },
                    [manifest],
                    "v2.0.3",
                )


if __name__ == "__main__":
    unittest.main()
