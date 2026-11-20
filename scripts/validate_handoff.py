#!/usr/bin/env python3
"""Validate portable Agent Handoff packages (v1.0 and v1.1; stdlib only).

Checks structure, optional task DAG and file integrity, plus heuristic credential
patterns. Passing does NOT prove the factual accuracy or safety of a handoff.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

HEADINGS = [
    "01. 交接摘要", "02. 背景与目标", "03. 当前状态", "04. 已有成果",
    "05. 关键决策", "06. 未解决事项", "07. 下一步计划", "08. 接手操作",
    "09. 来源与限制",
]
ALLOWED_MODES = {"quick", "full", "update"}
TASK_STATUSES = {"done", "in_progress", "todo", "blocked"}
EVIDENCE_STATUSES = {"verified", "reported", "inferred", "unknown", "conflicted"}
SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("OpenAI-like key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("credential assignment", re.compile(
        r"(?im)^\s*(?:api[_ -]?key|secret|password|access[_ -]?token|client[_ -]?secret)"
        r"\s*[:=]\s*[\"']?(?!\[REDACTED\]|<REDACTED>|unknown\b|none\b|null\b|\$\{|\$[A-Z_])"
        r"[A-Za-z0-9_+./=-]{12,}"
    )),
]


def _safe_file(root, name):
    """Only regular top-level files; reject traversal, separators and symlinks."""
    if not isinstance(name, str) or not name or name in {".", ".."}:
        return False
    if "/" in name or "\\" in name or Path(name).is_absolute():
        return False
    path = root / name
    return not path.is_symlink() and path.is_file()


def _check_tasks(path, errors):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError, OSError) as exc:
        errors.append(f"Invalid TASKS.json: {exc}")
        return
    if not isinstance(obj, dict) or not isinstance(obj.get("tasks"), list):
        errors.append("TASKS.json must be an object with tasks array")
        return
    by_id = {}
    for index, task in enumerate(obj["tasks"]):
        label = f"TASKS.json tasks[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{label} must be an object")
            continue
        tid = task.get("id")
        if not isinstance(tid, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{1,63}", tid):
            errors.append(f"{label} invalid id")
            continue
        if tid in by_id:
            errors.append(f"Duplicate task id: {tid}")
        by_id[tid] = task
        if not isinstance(task.get("name"), str) or not task["name"].strip():
            errors.append(f"{tid}: missing name")
        if task.get("status") not in TASK_STATUSES:
            errors.append(f"{tid}: invalid status")
        if task.get("evidence_status") not in EVIDENCE_STATUSES:
            errors.append(f"{tid}: invalid evidence_status")
        criteria = task.get("acceptance_criteria")
        if not isinstance(criteria, list) or not criteria or not all(
            isinstance(item, str) and item.strip() for item in criteria
        ):
            errors.append(f"{tid}: acceptance_criteria must have nonempty strings")
        deps = task.get("dependencies", [])
        if not isinstance(deps, list) or not all(isinstance(d, str) for d in deps):
            errors.append(f"{tid}: dependencies must be a string list")
        if task.get("evidence_status") == "verified":
            check = task.get("verification")
            if not isinstance(check, dict) or not all(
                isinstance(check.get(k), str) and check[k].strip()
                for k in ("source", "method", "observed_at")
            ):
                errors.append(f"{tid}: verified requires verification source/method/observed_at")
    graph = {}
    for tid, task in by_id.items():
        deps = task.get("dependencies", [])
        deps = deps if isinstance(deps, list) else []
        graph[tid] = [d for d in deps if isinstance(d, str)]
        for dep in graph[tid]:
            if dep not in by_id:
                errors.append(f"{tid}: unknown dependency {dep}")
    visiting, visited = set(), set()

    def walk(tid):
        if tid in visiting:
            errors.append(f"Cyclic task dependency involving {tid}")
            return
        if tid in visited:
            return
        visiting.add(tid)
        for dep in graph.get(tid, []):
            if dep in graph:
                walk(dep)
        visiting.remove(tid)
        visited.add(tid)

    for tid in graph:
        walk(tid)


def validate(root: Path, expected_mode=None):
    errors, warnings = [], []
    if not root.is_dir():
        return [f"Not a directory: {root}"], warnings
    manifest_path = root / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        return ["Missing or unsafe manifest.json"], warnings
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError, OSError) as exc:
        return [f"Invalid manifest.json: {exc}"], warnings
    if not isinstance(data, dict):
        return ["Manifest must be an object"], warnings
    if data.get("schema_version") not in {"1.0", "1.1"}:
        errors.append("schema_version must be '1.0' or '1.1'")
    if data.get("skill") != "agent-handoff":
        errors.append('skill must equal "agent-handoff"')
    if not isinstance(data.get("skill_version"), str) or not data["skill_version"].strip():
        errors.append("skill_version must be nonempty string")
    mode, package_mode = data.get("mode"), data.get("package_mode")
    if mode not in ALLOWED_MODES:
        errors.append(f"Unknown mode: {mode!r}")
    if expected_mode and mode != expected_mode:
        errors.append(f"Expected mode {expected_mode!r}, got {mode!r}")
    if package_mode not in {"quick", "full"}:
        errors.append("package_mode must be quick or full")
    if mode in {"quick", "full"} and package_mode != mode:
        errors.append("package_mode must match mode unless mode is update")
    try:
        date = dt.datetime.fromisoformat(data.get("generated_at"))
        if date.utcoffset() is None:
            errors.append("generated_at must include timezone")
    except (ValueError, TypeError):
        errors.append("generated_at must be ISO-8601 timestamp")
    if not isinstance(data.get("language"), str) or not data["language"].strip():
        errors.append("language must be nonempty")
    listed = data.get("files")
    if not isinstance(listed, list) or not all(isinstance(x, str) for x in listed):
        errors.append("files must be a string list")
        listed = []
    if len(listed) != len(set(listed)):
        errors.append("Duplicate manifest file names")
    mandatory = {"HANDOFF.md", "NEXT_AGENT_PROMPT.md"}
    if package_mode == "full":
        mandatory.add("PROJECT_STATE.md")
    for name in sorted(mandatory - set(listed)):
        errors.append(f"Missing mandatory file in manifest: {name}")
    actual = {p.name for p in root.iterdir() if p.is_file() and p.name != "manifest.json"}
    for name in listed:
        if not _safe_file(root, name):
            errors.append(f"Unsafe or missing file in manifest: {name!r}")
    for name in sorted(mandatory - actual):
        errors.append(f"Missing mandatory file: {name}")
    for name in sorted(actual - set(listed)):
        warnings.append(f"Unlisted output file: {name}")
    validation = data.get("validation")
    if not isinstance(validation, dict) or validation.get("status") not in {
        "not_run", "passed", "passed_with_warnings", "failed"
    }:
        errors.append("validation.status must be recognized")

    handoff = root / "HANDOFF.md"
    if _safe_file(root, "HANDOFF.md"):
        content = handoff.read_text(encoding="utf-8")
        matches = list(re.finditer(r"(?m)^## ([^\r\n]+?)\s*$", content))
        found = [(m.group(1).strip(), m.start(), m.end()) for m in matches]
        last = -1
        for heading in HEADINGS:
            candidates = [(i, item) for i, item in enumerate(found) if item[0] == heading]
            if len(candidates) != 1:
                errors.append(f"Required heading must occur exactly once: {heading}")
                continue
            index, item = candidates[0]
            if index <= last:
                errors.append(f"Heading out of order: {heading}")
            last = index
            end = found[index + 1][1] if index + 1 < len(found) else len(content)
            body = re.sub(r"(?m)^\s*---\s*$", "", content[item[2]:end]).strip()
            if not body:
                errors.append(f"Empty heading: {heading}")
        if len(content) < 250:
            warnings.append("HANDOFF.md is unusually short")
    if _safe_file(root, "NEXT_AGENT_PROMPT.md"):
        content = (root / "NEXT_AGENT_PROMPT.md").read_text(encoding="utf-8")
        if len(content.strip()) < 130:
            warnings.append("Receiver prompt seems too short")
        if not re.search(r"验收|acceptance|完成标准|success criteria", content, re.I):
            errors.append("Receiver prompt needs acceptance criteria")
        if not re.search(r"验证|核验|verify|check", content, re.I):
            errors.append("Receiver prompt needs verification instruction")
    if "TASKS.json" in listed and _safe_file(root, "TASKS.json"):
        _check_tasks(root / "TASKS.json", errors)
    integrity = data.get("integrity")
    if integrity is None:
        warnings.append("No integrity hashes: run handoff_tools.py seal to detect later changes")
    elif not isinstance(integrity, dict) or integrity.get("algorithm") != "sha256" or not isinstance(integrity.get("digests"), dict):
        errors.append("integrity must have algorithm='sha256' and a digests object")
    else:
        digests = integrity["digests"]
        if set(digests) != set(listed):
            errors.append("integrity.digests keys must match manifest.files")
        for name in listed:
            if not _safe_file(root, name):
                continue
            digest = digests.get(name)
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"Missing/invalid sha256 digest for {name}")
            elif hashlib.sha256((root / name).read_bytes()).hexdigest() != digest:
                errors.append(f"Integrity mismatch: {name}")

    for name in listed:
        if _safe_file(root, name) and name.endswith((".md", ".txt", ".json")):
            try:
                content = (root / name).read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"Unreadable text file {name}: {exc}")
                continue
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(content):
                    errors.append(f"Secret-like content ({label}) in {name}; inspect and redact")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--mode", choices=sorted(ALLOWED_MODES))
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="Machine-readable report")
    args = parser.parse_args()
    errors, warnings = validate(args.directory, args.mode)
    passed = not errors and (not args.strict or not warnings)
    if args.json:
        print(json.dumps({"ok": passed, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        for item in errors:
            print("ERROR:", item)
        for item in warnings:
            print("WARNING:", item)
        print(f"Validation: {'PASSED' if passed else 'FAILED'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
