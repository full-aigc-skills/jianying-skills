#!/usr/bin/env python3
"""验证108场景的来源、引用、路径和能力契约，不把静态校验当成片验收。"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "skills/jianying-video-planning"

def validate(skill, catalog=None):
    skill = Path(skill).resolve()
    load = lambda name: json.loads((skill / "references" / name).read_text(encoding="utf-8"))
    catalog = catalog or load("video-taxonomy.json")
    recipes_doc = load("edit-recipes.json")
    recipes = {r["id"]: r for r in recipes_doc["recipes"]}
    sources_list = load("source-index.json")["sources"]
    sources = {s["id"]: s for s in sources_list}
    known = {c["id"] for c in load("cli-capability-snapshot.json")["capabilities"]}
    scenes = catalog["scenes"]
    errors = []
    if catalog.get("schema") != "jianying-video-taxonomy/v1":
        errors.append("unknown catalog schema")
    if len(scenes) != 108 or len({s["id"] for s in scenes}) != 108:
        errors.append("108 unique scenes required; duplicate or missing ID")
    if len(recipes) != 12 or len(catalog["families"]) != 18:
        errors.append("18 families and 12 recipes required")
    if len(sources_list) != 108 or len(sources) != 108:
        errors.append("108 independent source records required")
    for family in catalog["families"]:
        if sum(s["family"] == family for s in scenes) != 6:
            errors.append(f"family count: {family}")
    paths = []
    for scene in scenes:
        sid = scene["id"]
        if not re.fullmatch(r"[A-Z]{2}[0-9]{2}", sid):
            errors.append(f"{sid}: invalid ID")
        if scene["recipe"] not in recipes:
            errors.append(f"{sid}: unknown recipe")
        for key in ("brief", "assets", "beats", "edit", "acceptance", "guardrail", "skills"):
            if not scene.get(key):
                errors.append(f"{sid}: missing {key}")
        missing = set(scene["required_capabilities"]) - known
        if missing:
            errors.append(f"{sid}: unknown capability {sorted(missing)}")
        relative = scene["example"]
        expected = f"examples/scenarios/{sid.lower()}.md"
        target = (skill / relative).resolve()
        if relative != expected or not target.is_relative_to(skill):
            errors.append(f"{sid}: invalid example path")
            continue
        paths.append(relative)
        if not target.is_file():
            errors.append(f"{sid}: missing example")
            continue
        text = target.read_text(encoding="utf-8")
        if scene["edit"] not in text or scene["acceptance"] not in text:
            errors.append(f"{sid}: example disagrees with editorial catalog")
        source = sources.get(scene["source_id"])
        if not source:
            errors.append(f"{sid}: missing source")
            continue
        for key in ("url", "title", "query", "accessed_on", "access_scope"):
            if not source.get(key):
                errors.append(f"{sid}: source missing {key}")
        if not source["url"].startswith("https://") or source["url"] not in text:
            errors.append(f"{sid}: invalid source link")
        popularity = source["popularity"]
        if popularity["status"] not in ("measured", "popularity_unverified"):
            errors.append(f"{sid}: invalid popularity status")
        if popularity["status"] == "measured" and not popularity.get("metrics"):
            errors.append(f"{sid}: popularity claim lacks metric")
        if source.get("video_watched") is not False:
            errors.append(f"{sid}: no video-watching evidence in this research")
    actual = {str(p.relative_to(skill)) for p in (skill / "examples/scenarios").glob("*.md")}
    if set(paths) != actual or len(actual) != 108:
        errors.append("example path set differs from exactly 108 files")
    for recipe in recipes.values():
        ids = recipe["required_capabilities"] + [c for values in recipe["optional_capabilities"].values() for c in values]
        if set(ids) - known:
            errors.append(f"{recipe['id']}: unknown recipe capability")
    for ids in recipes_doc["delivery_capabilities"].values():
        if set(ids) - known:
            errors.append("unknown delivery capability")
    return errors

if __name__ == "__main__":
    errors = validate(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT)
    for error in errors:
        print("ERROR:", error)
    print(f"video catalog: 108 scenes; {len(errors)} errors")
    raise SystemExit(bool(errors))
