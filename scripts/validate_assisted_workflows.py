"""确定性校验辅助制作知识目录与三个跨边界数据合同。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE_COMMIT = "32c56928ded4f9e2c2b80e099dc7abb793d2c30b"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_RECIPE_IDS = {"APW01", "APW02", "APW03", "APW04", "APW05"}
REQUIRED_PATTERN_IDS = {"APW-P01", "APW-P02", "APW-P03"}
ALLOWED_RECIPE_STATUS = {"provider_required", "capability_gated", "plan_only"}
ALLOWED_STEP_STATUS = {
    "provider_required",
    "knowledge_ready",
    "capability_gated",
    "approval_required",
    "plan_only",
}
FORBIDDEN_EXECUTION_FIELDS = {
    "command",
    "commands",
    "argv",
    "handler",
    "approval_id",
    "execution_result",
    "executed",
    "shell",
}
FORBIDDEN_RECIPE_TEXT = (
    "pyjianyingdraft",
    "jyproject",
    "smart_zoomer.py",
    "cloud_music_library.csv",
    "artistEffect",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def nested_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(key)
            keys.update(nested_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(nested_keys(child))
    return keys


def validate_catalog(catalog: dict[str, Any], known_capabilities: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    if catalog.get("schema") != "jianying-assisted-production-catalog/v1":
        errors.append("catalog schema must be jianying-assisted-production-catalog/v1")
    if catalog.get("version") != "1.0.0":
        errors.append("catalog version must be 1.0.0")

    source = catalog.get("source_baseline", {})
    if source.get("commit") != EXPECTED_SOURCE_COMMIT or not re.fullmatch(
        r"[0-9a-f]{40}", str(source.get("commit", ""))
    ):
        errors.append("source commit must be the fixed 40-hex research baseline")
    if source.get("license") != "MIT":
        errors.append("source license must be MIT")
    if source.get("adoption_mode") != "knowledge_rewrite_only":
        errors.append("source adoption mode must be knowledge_rewrite_only")
    if len(source.get("forbidden_runtime_imports", [])) < 6:
        errors.append("source boundary must enumerate forbidden runtime and resource imports")

    runtime = catalog.get("runtime_policy", {})
    expected_runtime = {
        "draft_mutator": "immutable_released_jianying_cli",
        "job_schema": "jianying-job/v2",
        "provider_owner": "jianying-edit-plugin",
        "knowledge_owner": "jianying-skills",
        "compound_clip": "plan_only",
    }
    for key, expected in expected_runtime.items():
        if runtime.get(key) != expected:
            errors.append(f"runtime policy {key} must be {expected}")

    step_contracts = catalog.get("step_contracts", {})
    if not isinstance(step_contracts, dict) or not step_contracts:
        errors.append("step_contracts must be a non-empty object")
        step_contracts = {}
    for step_id, contract in step_contracts.items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+", step_id):
            errors.append(f"invalid step id {step_id!r}")
        if not isinstance(contract, dict) or not contract.get("owner"):
            errors.append(f"step {step_id}: owner is required")
        if not isinstance(contract, dict) or contract.get("status") not in ALLOWED_STEP_STATUS:
            errors.append(f"step {step_id}: invalid status")
    if step_contracts.get("compound_clip.compile", {}).get("status") != "plan_only":
        errors.append("compound_clip.compile must remain plan_only")

    recipes = catalog.get("recipes", [])
    if not isinstance(recipes, list):
        errors.append("recipes must be an array")
        recipes = []
    recipe_ids = [recipe.get("id") for recipe in recipes if isinstance(recipe, dict)]
    if len(recipe_ids) != len(set(recipe_ids)):
        errors.append("duplicate recipe id")
    missing_recipes = sorted(REQUIRED_RECIPE_IDS - set(recipe_ids))
    if missing_recipes:
        errors.append(f"missing required recipes {missing_recipes}")

    for recipe in recipes:
        if not isinstance(recipe, dict):
            errors.append("recipe must be an object")
            continue
        recipe_id = recipe.get("id", "<unknown>")
        missing_fields = [
            field
            for field in (
                "name",
                "status",
                "intents",
                "owner_skills",
                "required_inputs",
                "steps",
                "required_capabilities",
                "human_gates",
                "target_evidence",
                "limits",
            )
            if not recipe.get(field)
        ]
        if missing_fields:
            errors.append(f"recipe {recipe_id}: missing fields {missing_fields}")
        if recipe.get("status") not in ALLOWED_RECIPE_STATUS:
            errors.append(f"recipe {recipe_id}: invalid status")
        unknown_steps = sorted(set(recipe.get("steps", [])) - set(step_contracts))
        if unknown_steps:
            errors.append(f"recipe {recipe_id}: unknown step {unknown_steps}")
        if known_capabilities is not None:
            unknown_capabilities = sorted(
                set(recipe.get("required_capabilities", [])) - known_capabilities
            )
            if unknown_capabilities:
                errors.append(
                    f"recipe {recipe_id}: unknown capabilities {unknown_capabilities}"
                )
        forbidden_keys = nested_keys(recipe) & FORBIDDEN_EXECUTION_FIELDS
        if forbidden_keys:
            errors.append(f"recipe {recipe_id}: execution field {sorted(forbidden_keys)} is forbidden")
        lowered = json.dumps(recipe, ensure_ascii=False).lower()
        for pattern in FORBIDDEN_RECIPE_TEXT:
            if pattern.lower() in lowered:
                errors.append(f"recipe {recipe_id}: forbidden runtime reference {pattern}")

    patterns = catalog.get("supporting_patterns", [])
    pattern_ids = {item.get("id") for item in patterns if isinstance(item, dict)}
    if not REQUIRED_PATTERN_IDS.issubset(pattern_ids):
        errors.append("supporting patterns must include exposure, clone-first and compound clip")
    for item in patterns:
        if not isinstance(item, dict):
            errors.append("supporting pattern must be an object")
            continue
        if item.get("step") not in step_contracts:
            errors.append(f"supporting pattern {item.get('id')}: unknown step")
    return errors


def validate_interaction_events(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "interaction-events/v1":
        errors.append("interaction schema must be interaction-events/v1")
    if not data.get("ledger_id"):
        errors.append("interaction ledger_id is required")
    if not is_sha256(data.get("source_media_sha256")):
        errors.append("interaction source media sha256 is invalid")
    if data.get("timebase") != "microseconds":
        errors.append("interaction timebase must be microseconds")

    capture = data.get("capture", {})
    if capture.get("target_type") not in {"screen", "window", "region"}:
        errors.append("capture target_type is invalid")
    if not is_sha256(capture.get("target_id_hash")):
        errors.append("capture target_id_hash is invalid")
    bounds = capture.get("bounds_px", {})
    if not all(isinstance(bounds.get(key), int) for key in ("x", "y", "width", "height")):
        errors.append("capture bounds must contain integer x/y/width/height")
    elif bounds["width"] <= 0 or bounds["height"] <= 0:
        errors.append("capture bounds width and height must be positive")
    if not isinstance(capture.get("display_scale"), (int, float)) or capture.get("display_scale", 0) <= 0:
        errors.append("capture display_scale must be positive")
    offset = capture.get("window_offset_px", {})
    if not isinstance(offset.get("x"), int) or not isinstance(offset.get("y"), int):
        errors.append("capture window_offset_px is required for coordinate mapping")
    if capture.get("keyboard_content_captured") is not False:
        errors.append("keyboard content capture must remain disabled")
    if capture.get("privacy_preview_approved") is not True:
        errors.append("privacy preview must be approved")

    events = data.get("events", [])
    if not isinstance(events, list) or not events:
        errors.append("events must be a non-empty array")
        return errors
    ids: list[str] = []
    previous_time = -1
    for index, event in enumerate(events):
        event_id = event.get("id") if isinstance(event, dict) else None
        ids.append(event_id)
        if not isinstance(event, dict) or event.get("type") not in {"click", "move"}:
            errors.append(f"event {index}: type must be click or move")
            continue
        time_us = event.get("time_us")
        if not isinstance(time_us, int) or time_us < 0:
            errors.append(f"event {index}: time_us must be non-negative integer")
        elif time_us < previous_time:
            errors.append(f"event {index}: time order must be non-decreasing")
        else:
            previous_time = time_us
        for axis in ("x", "y"):
            value = event.get(axis)
            if not isinstance(value, (int, float)) or not 0 <= value <= 1:
                errors.append(f"event {index}: normalized coordinate {axis} outside 0..1")
    if len(ids) != len(set(ids)) or any(not value for value in ids):
        errors.append("event ids must be non-empty and unique")
    return errors


def validate_smart_zoom_plan(
    data: dict[str, Any], events: dict[str, Any] | None = None
) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "smart-zoom-plan/v1":
        errors.append("smart zoom schema must be smart-zoom-plan/v1")
    if not is_sha256(data.get("source_media_sha256")):
        errors.append("smart zoom media digest is invalid")
    if events is not None:
        if data.get("source_ledger_id") != events.get("ledger_id"):
            errors.append("smart zoom source ledger does not match interaction ledger")
        if data.get("source_media_sha256") != events.get("source_media_sha256"):
            errors.append("smart zoom media digest does not match interaction media digest")
    fps = data.get("project_fps", {})
    if not isinstance(fps.get("num"), int) or fps.get("num", 0) <= 0:
        errors.append("project fps numerator must be positive")
    if not isinstance(fps.get("den"), int) or fps.get("den", 0) <= 0:
        errors.append("project fps denominator must be positive")
    constraints = data.get("constraints", {})
    max_scale = constraints.get("max_scale")
    if not isinstance(max_scale, (int, float)) or not 1 <= max_scale <= 2:
        errors.append("smart zoom max_scale must be within 1..2")
        max_scale = 1
    if constraints.get("accessibility_mode") not in {"standard", "reduced_motion"}:
        errors.append("smart zoom accessibility_mode is invalid")

    event_ids = {event.get("id") for event in (events or {}).get("events", [])}
    sessions = data.get("sessions", [])
    if not isinstance(sessions, list) or not sessions:
        errors.append("smart zoom sessions must be non-empty")
    for session_index, session in enumerate(sessions or []):
        start = session.get("start_us")
        end = session.get("end_us")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
            errors.append(f"session {session_index}: invalid time range")
            continue
        previous_time = -1
        keyframes = session.get("keyframes", [])
        if not isinstance(keyframes, list) or len(keyframes) < 2:
            errors.append(f"session {session_index}: at least two keyframes are required")
            continue
        for keyframe_index, keyframe in enumerate(keyframes):
            time_us = keyframe.get("time_us")
            if not isinstance(time_us, int) or time_us < 0 or not start <= time_us <= end:
                errors.append(f"session {session_index} keyframe {keyframe_index}: keyframe time is invalid")
            elif time_us <= previous_time:
                errors.append(f"session {session_index}: keyframe time order must be strict")
            else:
                previous_time = time_us
            scale = keyframe.get("scale")
            if not isinstance(scale, (int, float)) or not 1 <= scale <= max_scale:
                errors.append(f"session {session_index} keyframe {keyframe_index}: scale is unsafe")
            for axis in ("position_x", "position_y"):
                value = keyframe.get(axis)
                if not isinstance(value, (int, float)) or not -1 <= value <= 1:
                    errors.append(f"session {session_index} keyframe {keyframe_index}: {axis} is invalid")
            if events is not None and not set(keyframe.get("source_event_ids", [])).issubset(event_ids):
                errors.append(f"session {session_index} keyframe {keyframe_index}: unknown source event")
        if session.get("human_review") is not True:
            errors.append(f"session {session_index}: human_review must be true")
    report = data.get("quantization_report", {})
    if not isinstance(report.get("max_error_us"), int) or report.get("max_error_us", -1) < 0:
        errors.append("quantization max_error_us is invalid")
    if report.get("unsafe_offsets") != []:
        errors.append("quantization unsafe_offsets must be empty before execution")
    if data.get("target_evidence") != "playback" or data.get("plan_only") is not True:
        errors.append("smart zoom plan must remain plan_only with playback target evidence")
    return errors


def validate_media_preflight(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != "media-preflight/v1":
        errors.append("media preflight schema must be media-preflight/v1")
    for label in ("source", "derivative"):
        media = data.get(label, {})
        if not isinstance(media.get("path"), str) or not media.get("path", "").startswith("/"):
            errors.append(f"{label} path must be absolute")
        if not is_sha256(media.get("sha256")):
            errors.append(f"{label} sha256 must be a content digest")
        if not isinstance(media.get("size_bytes"), int) or media.get("size_bytes", 0) <= 0:
            errors.append(f"{label} size_bytes must be positive")
        probe = media.get("probe", {})
        required_probe = {"container", "video_codec", "width", "height", "fps", "alpha", "audio_codec"}
        if not required_probe.issubset(probe):
            errors.append(f"{label} probe is incomplete")
    compatibility = data.get("compatibility", {})
    if compatibility.get("target") != "jianying" or compatibility.get("status") not in {
        "compatible",
        "conversion_required",
        "blocked",
    }:
        errors.append("compatibility target or status is invalid")
    conversion = data.get("proposed_conversion", {})
    if not is_sha256(conversion.get("parameters_digest")):
        errors.append("conversion parameters_digest is invalid")
    approval = data.get("approval", {})
    if approval.get("required") is not True or approval.get("status") != "approved":
        errors.append("conversion must have explicit approved status")
    if not is_sha256(approval.get("binding_hash")):
        errors.append("conversion approval binding_hash is invalid")
    staging = data.get("staging", {})
    if staging.get("mode") not in {"copy", "hardlink"} or staging.get("self_contained") is not True:
        errors.append("staging must be self-contained copy or hardlink")
    if not is_sha256(staging.get("target_root_hash")):
        errors.append("staging target_root_hash is invalid")
    quality = data.get("quality_comparison", {})
    if quality.get("status") not in {"within_bounds", "manual_review", "failed"}:
        errors.append("quality comparison status is invalid")
    rollback = data.get("rollback", {})
    if rollback.get("retain_source") is not True:
        errors.append("rollback must retain source media")
    return errors


def validate_granular_install(root: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "jianying-video-planning": [
            "SKILL.md",
            "references/assisted-production-workflows-v1.json",
        ],
        "jianying-motion": [
            "SKILL.md",
            "references/interaction-events-v1.schema.json",
            "references/smart-zoom-plan-v1.schema.json",
            "references/smart-zoom-workflow.md",
            "examples/interaction-events-v1.json",
            "examples/smart-zoom-plan-v1.json",
        ],
        "jianying-media": [
            "SKILL.md",
            "references/media-preflight-v1.schema.json",
            "references/media-preflight-workflow.md",
            "examples/media-preflight-v1.json",
        ],
    }
    for skill, paths in required.items():
        for relative in paths:
            if not (root / skill / relative).is_file():
                errors.append(f"granular install {skill}: missing {relative}")
    return errors


def validate_repository(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    planning = root / "skills/jianying-video-planning"
    motion = root / "skills/jianying-motion"
    media = root / "skills/jianying-media"
    try:
        catalog = read_json(planning / "references/assisted-production-workflows-v1.json")
        events = read_json(motion / "examples/interaction-events-v1.json")
        zoom = read_json(motion / "examples/smart-zoom-plan-v1.json")
        preflight = read_json(media / "examples/media-preflight-v1.json")
        capability_snapshot = read_json(planning / "references/cli-capability-snapshot.json")
    except (OSError, json.JSONDecodeError) as error:
        return [f"cannot load assisted production contract: {error}"]
    capabilities = {
        item.get("id")
        for item in capability_snapshot.get("capabilities", [])
        if item.get("id")
    }
    errors.extend(validate_catalog(catalog, capabilities))
    errors.extend(validate_interaction_events(events))
    errors.extend(validate_smart_zoom_plan(zoom, events))
    errors.extend(validate_media_preflight(preflight))
    errors.extend(validate_granular_install(root / "skills"))

    provenance = root / "docs/ASSISTED_PRODUCTION_PROVENANCE.md"
    if not provenance.is_file() or EXPECTED_SOURCE_COMMIT not in provenance.read_text(encoding="utf-8"):
        errors.append("assisted production provenance must contain the fixed source commit")
    for schema_path, expected_title in (
        (motion / "references/interaction-events-v1.schema.json", "interaction-events/v1"),
        (motion / "references/smart-zoom-plan-v1.schema.json", "smart-zoom-plan/v1"),
        (media / "references/media-preflight-v1.schema.json", "media-preflight/v1"),
    ):
        try:
            schema = read_json(schema_path)
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"cannot load schema {schema_path.name}: {error}")
            continue
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{schema_path.name}: must use JSON Schema 2020-12")
        if schema.get("title") != expected_title:
            errors.append(f"{schema_path.name}: unexpected title")
    return errors


def main() -> int:
    errors = validate_repository(ROOT)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"validate_assisted_workflows: {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
