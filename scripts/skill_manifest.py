#!/usr/bin/env python3
"""渲染或校验 jianying-skills 正典内容清单。"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "jianying-skills.manifest.json"
CANONICAL_REPOSITORY = "https://github.com/full-aigc-skills/jianying-skills.git"
CANONICAL_REMOTE_URLS = {
    CANONICAL_REPOSITORY,
    CANONICAL_REPOSITORY.removesuffix(".git"),
    "git@github.com:full-aigc-skills/jianying-skills.git",
    "git@github.com:full-aigc-skills/jianying-skills",
    "ssh://git@github.com/full-aigc-skills/jianying-skills.git",
    "ssh://git@github.com/full-aigc-skills/jianying-skills",
}


def hash_skill_dir(skill_dir: Path) -> str:
    """按相对路径与逐文件哈希计算稳定目录摘要。"""
    if skill_dir.is_symlink() or not skill_dir.is_dir():
        raise ValueError(f"skill directory is invalid or symbolic: {skill_dir}")
    digest = hashlib.sha256()
    for path in sorted(skill_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symbolic links are forbidden in skill content: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f"special files are forbidden in skill content: {path}")
        relative = path.relative_to(skill_dir).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def git(*arguments: str) -> str:
    """运行只读 Git 查询。"""
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def render_manifest(
    *,
    content_state: str = "release_candidate",
    release_ref: str | None = None,
    source_commit: str | None = None,
) -> dict:
    """从当前技能树和契约矩阵构造正典清单。"""
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    matrix = json.loads((ROOT / "docs/RUST_CLI_SKILL_MATRIX.json").read_text(encoding="utf-8"))
    rows = {row["name"]: row for row in matrix["skills"]}
    names = [value.removeprefix("./skills/") for value in plugin["skills"]]
    skills = []
    aggregate = hashlib.sha256()
    for name in names:
        digest = hash_skill_dir(ROOT / "skills" / name)
        required = rows[name]["required_capabilities"]
        entry = {
            "name": name,
            "sha256": digest,
            "minimum_cli_version": rows[name]["minimum_cli_version"],
            "required_capabilities": required,
        }
        skills.append(entry)
        aggregate.update(name.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(digest.encode("ascii"))
        aggregate.update(b"\n")
    return {
        "schema": "jianying-skills-manifest/v1",
        "package": "jianying-skills",
        "repository": CANONICAL_REPOSITORY,
        "version": plugin["version"],
        "source_commit": source_commit,
        "content_state": content_state,
        "release_ref": release_ref,
        "minimum_cli_capabilities": sorted(
            {capability for row in rows.values() for capability in row["required_capabilities"]}
        ),
        "skills": skills,
        "content_sha256": aggregate.hexdigest(),
    }


def resolve_tag(remote: str, release_ref: str) -> str:
    """解析远端 tag；annotated tag 使用 peeled commit。"""
    output = subprocess.run(
        ["git", "-C", str(ROOT), "ls-remote", "--tags", remote,
         f"refs/tags/{release_ref}", f"refs/tags/{release_ref}^{{}}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    resolved = None
    for line in output.splitlines():
        commit, _, name = line.partition("\t")
        if name == f"refs/tags/{release_ref}^{{}}":
            resolved = commit
        elif name == f"refs/tags/{release_ref}" and resolved is None:
            resolved = commit
    if resolved is None:
        raise RuntimeError(f"remote tag not found: {remote} {release_ref}")
    return resolved


def render_release_manifest(release_ref: str, remote: str) -> dict:
    """仅为已提交、已打 tag 且远端可验证的版本生成发布清单。"""
    if git("status", "--porcelain"):
        raise RuntimeError("release manifest requires a clean working tree")
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    expected_ref = f"v{plugin['version']}"
    if release_ref != expected_ref:
        raise RuntimeError(f"release ref must be {expected_ref}")
    remote_url = git("remote", "get-url", remote).rstrip("/")
    if remote_url not in CANONICAL_REMOTE_URLS:
        raise RuntimeError(
            f"release remote must be the canonical GitHub repository: {CANONICAL_REPOSITORY}"
        )
    head = git("rev-parse", "HEAD")
    local = git("rev-parse", f"{release_ref}^{{commit}}")
    if local != head:
        raise RuntimeError(f"local tag {release_ref} does not point to HEAD")
    remote_commit = resolve_tag(remote, release_ref)
    if remote_commit != head:
        raise RuntimeError(f"remote tag {release_ref} does not point to HEAD")
    return render_manifest(content_state="released", release_ref=release_ref, source_commit=head)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("render", "check", "release"))
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--ref", dest="release_ref")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if arguments.command == "release":
        if not arguments.release_ref:
            print("ERROR: release requires --ref v<version>")
            return 1
        try:
            current = render_release_manifest(arguments.release_ref, arguments.remote)
        except (RuntimeError, subprocess.CalledProcessError) as error:
            print(f"ERROR: {error}")
            return 1
        rendered = json.dumps(current, ensure_ascii=False, indent=2) + "\n"
        if arguments.output:
            arguments.output.write_text(rendered, encoding="utf-8")
            print(f"release skill manifest written: {arguments.output}")
        else:
            print(rendered, end="")
        return 0
    current = render_manifest()
    if arguments.command == "render":
        rendered = json.dumps(current, ensure_ascii=False, indent=2) + "\n"
        if arguments.output:
            arguments.output.write_text(rendered, encoding="utf-8")
            print(f"skill manifest written: {arguments.output}")
        else:
            print(rendered, end="")
        return 0
    try:
        recorded = json.loads(arguments.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: cannot load manifest: {error}")
        return 1
    if recorded != current:
        print("ERROR: canonical skill manifest differs from the current skill tree")
        return 1
    print(f"skill manifest: {len(current['skills'])} skills, digest verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
