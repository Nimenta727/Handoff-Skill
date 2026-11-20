#!/usr/bin/env python3
"""Reproducible, offline source distribution for Agent Handoff Skill.

Standard library only. Package source and documentation; never package local
handoff outputs, credentials, development caches, or generated dashboards.
"""
import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT_FILES = ("SKILL.md", "README.md", "CHANGELOG.md", "RELEASE_NOTES.md", "VERSION", ".gitignore")
ROOT_DIRS = ("references", "scripts", "examples", "docs", "tests")
ALLOWED_EXT = {".md", ".py", ".json", ".txt", ".yml", ".yaml"}
SKIP_DIRS = {"__pycache__", ".git", ".venv", ".pytest_cache", "dist", "node_modules"}
SKIP_FILES = {".DS_Store"}


def source_files(root):
    root = root.resolve()
    found = []
    for name in ROOT_FILES:
        p = root / name
        if p.is_file():
            found.append(p)
    for name in ROOT_DIRS:
        folder = root / name
        if not folder.is_dir():
            continue
        for p in folder.rglob("*"):
            rel = p.relative_to(root)
            if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts):
                continue
            if not p.is_file() or p.name in SKIP_FILES or p.suffix.lower() not in ALLOWED_EXT:
                continue
            found.append(p)
    if root / "SKILL.md" not in found or root / "VERSION" not in found:
        raise ValueError("SKILL.md and VERSION are required")
    files = sorted(set(found), key=lambda p: p.relative_to(root).as_posix())
    if any(p.is_symlink() or not p.resolve().is_relative_to(root) for p in files):
        raise ValueError("Source symlinks / paths outside repository are not allowed")
    return files


def build(root, dest, version=None):
    root = root.resolve()
    version = version or (root / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Expected semantic version MAJOR.MINOR.PATCH")
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / f"agent-handoff-v{version}.zip"
    digest_file = dest / (archive.name + ".sha256")
    if archive.is_symlink() or digest_file.is_symlink():
        raise ValueError("Refusing symbolic-link distribution paths")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in source_files(root):
            path = "agent-handoff/" + p.relative_to(root).as_posix()
            info = zipfile.ZipInfo(path, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    digest_file.write_text(digest + "  " + archive.name + "\n", encoding="utf-8")
    return archive, digest_file, digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=Path("dist"))
    args = parser.parse_args()
    try:
        archive, checksum, digest = build(args.root, args.out)
    except (OSError, ValueError, UnicodeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    print("Archive:", archive)
    print("SHA256:", digest)
    print("Checksum file:", checksum)
    return 0


if __name__ == "__main__":
    sys.exit(main())
