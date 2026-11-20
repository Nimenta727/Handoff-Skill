# Handoff schema V1.0 / V1.1

## Required `HANDOFF.md` headings

Use these **exact** level-2 heading strings (in this order; internal content language may vary):

1. `## 01. 交接摘要`
2. `## 02. 背景与目标`
3. `## 03. 当前状态`
4. `## 04. 已有成果`
5. `## 05. 关键决策`
6. `## 06. 未解决事项`
7. `## 07. 下一步计划`
8. `## 08. 接手操作`
9. `## 09. 来源与限制`

Explicitly mark missing facts as `未知` / `Unknown`; nonapplicable sections as `无适用内容` / `Not applicable`. No empty mandatory headings.

## Task record

Use the following fields where helpful. Human-readable bullet/table formats are allowed; these field names specify semantics:

```yaml
id: TASK-001
name: "具体任务"
status: in_progress  # done | in_progress | todo | blocked
priority: high       # high | medium | low
evidence_status: reported  # verified | reported | inferred | unknown | conflicted
completed_work: []
remaining_work: []
blocked_by: []
acceptance_criteria:
  - "observable outcome"
references:
  - "file/path or source"
```

**Progress ≠ confidence:** `done` + `reported` only means someone reported completion. It is not proof of success. Use stable IDs for long projects. The next step needs an owner/actor when known, inputs or prerequisites, a specific action, and verifiable acceptance criteria.

## Evidence statements

For consequential claims, include at least the statement, confidence status, source and how to verify it. `verified` additionally requires check method and time/scope; if those are unavailable downgrade to `reported` or `unknown`.

## `manifest.json` schema

A portable manifest describes the package, not semantic truth. Required fields:

```json
{
  "schema_version": "1.0",
  "skill": "agent-handoff",
  "skill_version": "1.0.0",
  "mode": "quick",
  "package_mode": "quick",
  "generated_at": "2026-11-18T16:51:00+08:00",
  "language": "zh-CN",
  "files": ["HANDOFF.md", "NEXT_AGENT_PROMPT.md"],
  "validation": {"status": "not_run", "notes": "Not yet validated"}
}
```

`mode` is `quick`, `full`, or `update`. `package_mode` describes file requirements and is either `quick` or `full` (for `update`, carry forward existing package type). `generated_at` must be valid ISO-8601 with timezone offset. `files` lists relative paths within the output folder, without `manifest.json` itself. The validator uses this schema for structural checks; it does **not** certify claims are accurate or safe.

## Expected deliverables

| Mode | Mandatory | Optional |
| --- | --- | --- |
| quick | `HANDOFF.md`, `NEXT_AGENT_PROMPT.md`, `manifest.json` | none |
| full | quick files, `PROJECT_STATE.md` | `DECISIONS.md`, `OPEN_ISSUES.md` |
| update | mandatory based on `package_mode` | same optional files |

Suggested `PROJECT_STATE.md` sections: artifact map, task ledger, domain-specific environment or prerequisites, evidence summary. `DECISIONS.md`: decision, rationale, alternatives rejected, implications. `OPEN_ISSUES.md`: issue, impact, unblocker, next diagnostic step.

## V1.1 optional extensions (V1.0 packages remain valid)

- schema_version may be 1.0 or 1.1. Keep nine exact headings and existing mandatory files.
- manifest.integrity is OPTIONAL for backwards compatibility; when present it is
  {"algorithm":"sha256","digests":{"HANDOFF.md":"<64-lowercase-hex>", ...}}
  and MUST cover every file in manifest.files. manifest.json is intentionally
  excluded to prevent self-hashing recursion.
- SHA-256 checks changed bytes, not authenticity, identity, trust or semantic truth.
- TASKS.json is OPTIONAL and MUST appear in files when used; see task-state.md.
- Minimal receiver input may be generated with handoff_tools.py brief --max-chars 1200.
  This is a character budget, never a promise of precise model-token counting.
- Update mode retains package_mode; deliberate edits to sealed artifacts need
  inspection and an explicit handoff_tools.py seal --renew step.

The full handoff remains the source of truth; a brief is a disposable view,
not another independently maintained state file.
