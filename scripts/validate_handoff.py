#!/usr/bin/env python3
"""Validate an Agent Handoff V1 package. Standard library only.

Structural and heuristic privacy checks; NOT factual or complete security verification.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

HEADINGS = [
    '01. 交接摘要', '02. 背景与目标', '03. 当前状态', '04. 已有成果',
    '05. 关键决策', '06. 未解决事项', '07. 下一步计划', '08. 接手操作',
    '09. 来源与限制',
]
ALLOWED_MODES = {'quick', 'full', 'update'}
SECRET_PATTERNS = [
    ('private key block', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),
    ('GitHub token', re.compile(r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b')),
    ('OpenAI-like key', re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b')),
    ('AWS access key id', re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
    ('possible credential assignment', re.compile(r'(?im)^\s*(?:api[_ -]?key|secret|password|access[_ -]?token|client[_ -]?secret)\s*[:=]\s*["\']?(?!\[REDACTED\]|<REDACTED>|未知\b|unknown\b|none\b|null\b|\$\{|\$[A-Z_])[A-Za-z0-9_+./=-]{12,}')),
]


def validate(root: Path, expected_mode=None):
    errors, warnings = [], []
    if not root.is_dir():
        return [f'Not a directory: {root}'], warnings
    manifest_path = root / 'manifest.json'
    if not manifest_path.is_file():
        return ['Missing manifest.json'], warnings
    try:
        data = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        return [f'Invalid manifest.json: {exc}'], warnings
    if not isinstance(data, dict):
        return ['Manifest must be an object'], warnings
    if data.get('schema_version') != '1.0':
        errors.append('schema_version must equal "1.0"')
    if data.get('skill') != 'agent-handoff':
        errors.append('skill must equal "agent-handoff"')
    if not isinstance(data.get('skill_version'), str) or not data['skill_version']:
        errors.append('skill_version must be nonempty string')
    mode = data.get('mode')
    package_mode = data.get('package_mode')
    if mode not in ALLOWED_MODES:
        errors.append(f'Unknown mode: {mode!r}')
    if expected_mode and mode != expected_mode:
        errors.append(f'Expected mode {expected_mode!r}, got {mode!r}')
    if package_mode not in {'quick', 'full'}:
        errors.append('package_mode must be quick or full')
    if mode in {'quick', 'full'} and package_mode != mode:
        errors.append('package_mode must match mode unless mode is update')
    timestamp = data.get('generated_at')
    try:
        date = dt.datetime.fromisoformat(timestamp)
        if date.utcoffset() is None:
            errors.append('generated_at must include timezone')
    except (ValueError, TypeError):
        errors.append('generated_at must be ISO-8601 timestamp')
    if not isinstance(data.get('language'), str) or not data['language'].strip():
        errors.append('language must be nonempty')
    listed = data.get('files')
    if not isinstance(listed, list) or not all(isinstance(x, str) for x in listed):
        errors.append('files must be a string list')
        listed = []
    if len(listed) != len(set(listed)):
        errors.append('Duplicate manifest file names')
    mandatory = {'HANDOFF.md', 'NEXT_AGENT_PROMPT.md'}
    if package_mode == 'full':
        mandatory.add('PROJECT_STATE.md')
    for name in sorted(mandatory - set(listed)):
        errors.append(f'Missing mandatory file in manifest: {name}')
    actual = {p.name for p in root.iterdir() if p.is_file() and p.name != 'manifest.json'}
    for name in listed:
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not name or relative.name != name:
            errors.append(f'Unsafe or unsupported file name in manifest: {name!r}')
            continue
        if not (root / name).is_file():
            errors.append(f'Manifest lists nonexistent file: {name}')
    for name in sorted(mandatory - actual):
        errors.append(f'Missing mandatory file: {name}')
    for name in sorted(actual - set(listed)):
        warnings.append(f'Unlisted output file: {name}')
    validation = data.get('validation')
    if not isinstance(validation, dict) or validation.get('status') not in {'not_run', 'passed', 'passed_with_warnings', 'failed'}:
        errors.append('validation.status must be recognized')

    handoff = root / 'HANDOFF.md'
    if handoff.is_file():
        content = handoff.read_text(encoding='utf-8')
        matches = list(re.finditer(r'(?m)^## (.+?)\s*$', content))
        found = [(m.group(1), m.start(), m.end()) for m in matches]
        position = -1
        for heading in HEADINGS:
            candidates = [(idx, item) for idx, item in enumerate(found) if item[0] == heading]
            if len(candidates) != 1:
                errors.append(f'Required heading must occur exactly once: {heading}')
                continue
            idx, item = candidates[0]
            if idx <= position:
                errors.append(f'Heading out of order: {heading}')
            position = idx
            after = found[idx+1][1] if idx+1 < len(found) else len(content)
            body = content[item[2]:after].strip()
            body = re.sub(r'(?m)^\s*---\s*$', '', body).strip()
            if not body:
                errors.append(f'Empty heading: {heading}')
        if len(content) < 250:
            warnings.append('HANDOFF.md is unusually short; check usefulness')
    receiver = root / 'NEXT_AGENT_PROMPT.md'
    if receiver.is_file():
        content = receiver.read_text(encoding='utf-8')
        if len(content.strip()) < 130:
            warnings.append('Receiver prompt seems too short for actionable continuation')
        if not re.search(r'验收|acceptance|完成标准|success criteria', content, re.I):
            errors.append('Receiver prompt needs acceptance criteria')
        if not re.search(r'验证|核验|verify|check', content, re.I):
            errors.append('Receiver prompt needs verification instruction')
    for name in sorted(set(listed) & actual):
        if name.endswith(('.md', '.txt', '.json')):
            text = (root / name).read_text(encoding='utf-8')
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f'Secret-like content ({label}) in {name}; inspect and redact')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path, help='handoff output directory')
    parser.add_argument('--mode', choices=sorted(ALLOWED_MODES), help='expected mode')
    args = parser.parse_args()
    errors, warnings = validate(args.directory, args.mode)
    for item in errors:
        print('ERROR:', item)
    for item in warnings:
        print('WARNING:', item)
    print(f'Validation: {"FAILED" if errors else "PASSED"} ({len(errors)} errors, {len(warnings)} warnings)')
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
