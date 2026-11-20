# TASKS.json — optional portable task ledger

Use only for multi-task handoffs. HANDOFF.md stays the human-readable entry point.
Avoid duplicating full task records in narrative documents.

```json
{
  "tasks": [
    {
      "id": "TASK-001",
      "name": "Verify report references",
      "status": "in_progress",
      "evidence_status": "reported",
      "dependencies": [],
      "acceptance_criteria": ["All citations checked"],
      "references": ["reports/draft.md"]
    },
    {
      "id": "TASK-002",
      "name": "Publish reviewed draft",
      "status": "todo",
      "evidence_status": "unknown",
      "dependencies": ["TASK-001"],
      "acceptance_criteria": ["Approved draft exists"]
    }
  ]
}
```

Each task requires id, name, status, evidence_status and a nonempty array of
acceptance_criteria. Optional: dependencies, owner, priority, references and verification.

Status: done | in_progress | todo | blocked.
Evidence: verified | reported | inferred | unknown | conflicted.

For verified, include source, method, observed_at:

```json
"verification": {
  "source": "reports/checks.txt",
  "method": "Reviewed source citations",
  "observed_at": "2026-11-20T20:00:00+08:00"
}
```

The validator checks IDs, duplicate IDs, dangling/cyclic dependencies and required
verification metadata. It does not establish whether external claims are true.

Update rules: keep IDs stable, preserve conflicting evidence, only mark an item
done with the appropriate confidence, and never treat removal as completion.
Run `python3 scripts/handoff_tools.py diff OLD NEW` for changed task IDs.
A handoff is NOT a serialized executable checkpoint or permission grant.
