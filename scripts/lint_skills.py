"""Lint gate for skill packages: every skills/<name>/SKILL.md must be well-formed.

Rules (exit 1 on any violation):
- every directory under skills/ contains SKILL.md
- frontmatter has a `name` equal to its directory name
- `description` is present, single-line (block scalars break some hosts), 20-1024 chars
- skill names are lowercase kebab-case without a `codex-` prefix
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RISK_LEVELS = {"read_only", "reversible_write", "high_risk_write", "external_native_execution"}
EVIDENCE_LEVELS = {"plan", "structural", "cold_reopen", "playback", "native_export"}
FORBIDDEN_RUNTIME_PATTERNS = {
    "jydraft_run.py": "legacy Python runner",
    "JIANYING_HEADLESS_ROOT": "external headless checkout",
    "from pyJianYingDraft": "pyJianYingDraft API",
    "import pyJianYingDraft": "pyJianYingDraft API",
}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fields = {}
    for line in text[4:end].splitlines():
        if line and not line.startswith(" ") and ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
        elif line.startswith(" ") or line.startswith("-"):
            # continuation of a block scalar or list: mark parent as multiline
            if fields:
                last = next(reversed(fields))
                fields[last] = fields[last] + "\n" + line
    return fields


def load_contract_matrix(path: Path) -> dict:
    """加载技能到 Rust CLI capability 的正典迁移矩阵。"""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {"_load_error": str(error)}


def validate_contract_matrix(matrix: dict, skill_names: list[str], capability_manifest: dict | None) -> list[str]:
    """验证技能清单完整性，并阻止未获 CLI 证据的 ready 声明。"""
    errors: list[str] = []
    if matrix.get("_load_error"):
        return [f"contract matrix cannot be loaded: {matrix['_load_error']}"]
    if matrix.get("schema") != "jianying-skill-contract-matrix/v1":
        errors.append("contract matrix schema must be jianying-skill-contract-matrix/v1")
    rows = matrix.get("skills", [])
    names = [row.get("name") for row in rows]
    if sorted(names) != sorted(skill_names):
        errors.append(f"contract matrix skill list mismatch: matrix={sorted(names)}, actual={sorted(skill_names)}")
    if len(names) != len(set(names)):
        errors.append("contract matrix contains duplicate skill names")

    supported = set()
    if capability_manifest is not None:
        supported = {
            entry.get("id")
            for entry in capability_manifest.get("capabilities", [])
            if entry.get("status") == "supported"
        }
    for row in rows:
        name = row.get("name", "<unknown>")
        required = row.get("required_capabilities")
        for key in ("minimum_cli_version", "risk_level", "success_evidence", "migration_state"):
            if not row.get(key):
                errors.append(f"{name}: contract matrix missing {key}")
        if not isinstance(required, list) or not required:
            errors.append(f"{name}: required_capabilities must be a non-empty list")
            required = []
        if row.get("risk_level") not in RISK_LEVELS:
            errors.append(f"{name}: invalid risk_level {row.get('risk_level')}")
        if row.get("success_evidence") not in EVIDENCE_LEVELS:
            errors.append(f"{name}: invalid success_evidence {row.get('success_evidence')}")
        if row.get("migration_state") == "ready":
            if capability_manifest is None:
                errors.append(f"{name}: ready requires a verified CLI capability manifest")
            else:
                missing = sorted(set(required) - supported)
                if missing:
                    errors.append(f"{name}: CLI capability manifest lacks supported capabilities {missing}")
    return errors


def validate_skill_contract(skill_dir: Path, row: dict) -> list[str]:
    """验证技能正文与矩阵契约一致，并确保粒度安装资源自包含。"""
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    required_fragments = [
        "## 运行契约",
        "- 触发条件：",
        "- 所需 capability：",
        "- 最低 CLI 版本：",
        "- 默认风险：",
        "- 输入事实：",
        "- 确认点：",
        "- 成功证据：",
        "- 禁止行为：",
        row.get("minimum_cli_version", ""),
        row.get("risk_level", ""),
        row.get("success_evidence", ""),
    ]
    required_fragments.extend(row.get("required_capabilities", []))
    for fragment in required_fragments:
        if fragment and fragment not in text:
            errors.append(f"{skill_dir.name}: SKILL.md missing contract fragment {fragment!r}")
    if len(text.splitlines()) >= 500:
        errors.append(f"{skill_dir.name}: SKILL.md must stay below 500 lines")

    for relative in ("references/workflow.md", "examples/minimal-job.json"):
        if not (skill_dir / relative).is_file():
            errors.append(f"{skill_dir.name}: missing self-contained {relative}")

    markdown_files = sorted(skill_dir.rglob("*.md"))
    json_files = sorted(skill_dir.rglob("*.json"))
    for path in [*markdown_files, *json_files]:
        content = path.read_text(encoding="utf-8")
        for pattern, label in FORBIDDEN_RUNTIME_PATTERNS.items():
            if pattern in content:
                errors.append(f"{skill_dir.name}: {path.relative_to(skill_dir)} references {label}")
        if re.search(r"\]\(\.\./(?:\.\./)?jianying-[^)]+\)", content):
            errors.append(f"{skill_dir.name}: {path.relative_to(skill_dir)} links to a sibling skill")
        if path.suffix == ".md":
            for raw_target in MARKDOWN_LINK_RE.findall(content):
                target = raw_target.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (path.parent / target).resolve()
                try:
                    resolved.relative_to(skill_dir.resolve())
                except ValueError:
                    errors.append(
                        f"{skill_dir.name}: {path.relative_to(skill_dir)} local link escapes skill {raw_target}"
                    )
                    continue
                if not resolved.exists():
                    errors.append(
                        f"{skill_dir.name}: {path.relative_to(skill_dir)} has missing local link {raw_target}"
                    )
    return errors


def validate_package_manifest(path: Path, skill_names: list[str]) -> list[str]:
    """验证包版本和 13 个技能入口均可发现。"""
    errors: list[str] = []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"package manifest cannot be loaded: {error}"]
    if manifest.get("name") != "jianying-skills":
        errors.append("package manifest name must be jianying-skills")
    if manifest.get("version") != "2.0.0":
        errors.append("package manifest version must be 2.0.0")
    declared = []
    for value in manifest.get("skills", []):
        prefix = "./skills/"
        if not isinstance(value, str) or not value.startswith(prefix):
            errors.append(f"package manifest has invalid skill path {value!r}")
            continue
        declared.append(value[len(prefix):])
    if len(declared) != len(set(declared)):
        errors.append("package manifest contains duplicate skill paths")
    if sorted(declared) != sorted(skill_names):
        errors.append(f"package manifest skill list mismatch: {declared}")
    return errors


def main() -> int:
    errors = []
    skills_dir = ROOT / "skills"
    dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if not dirs:
        errors.append("skills/ has no skill directories")
    for skill_dir in dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue
        fm = frontmatter(skill_md.read_text())
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append(f"{skill_dir.name}: frontmatter missing name")
        elif name != skill_dir.name:
            errors.append(f"{skill_dir.name}: name '{name}' != directory name")
        if not NAME_RE.match(skill_dir.name):
            errors.append(f"{skill_dir.name}: not lowercase kebab-case")
        if skill_dir.name.startswith("codex-"):
            errors.append(f"{skill_dir.name}: host-prefixed names are not allowed in source packages")
        if not desc:
            errors.append(f"{skill_dir.name}: frontmatter missing description")
        else:
            if "\n" in desc or desc in ("|", ">", "|-", ">-", "|+", ">+"):
                errors.append(f"{skill_dir.name}: description must be single-line (no block scalars)")
            elif not (20 <= len(desc) <= 1024):
                errors.append(f"{skill_dir.name}: description length {len(desc)} outside 20..1024")
    matrix = load_contract_matrix(ROOT / "docs/RUST_CLI_SKILL_MATRIX.json")
    manifest = None
    manifest_path = os.environ.get("JIANYING_CLI_CAPABILITY_MANIFEST")
    if manifest_path:
        try:
            manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"CLI capability manifest cannot be loaded: {error}")
    errors.extend(validate_contract_matrix(matrix, [path.name for path in dirs], manifest))
    rows = {row.get("name"): row for row in matrix.get("skills", [])}
    for skill_dir in dirs:
        row = rows.get(skill_dir.name)
        if row:
            errors.extend(validate_skill_contract(skill_dir, row))
    errors.extend(
        validate_package_manifest(
            ROOT / ".claude-plugin" / "plugin.json",
            [path.name for path in dirs],
        )
    )
    for error in errors:
        print(f"ERROR: {error}")
    print(f"lint_skills: {len(dirs)} skills, contract matrix checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
