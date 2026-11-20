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

## 中文：任务记录使用建议 / Chinese task guidance

TASKS.json 是可选的**结构化任务状态文件**，适合有多个子任务和依赖关系的项目；
简单交接不需要生成它。每项至少记录 id、name、status、
evidence_status、acceptance_criteria；dependencies 可为空数组。

状态取值：done（完成）、in_progress（进行中）、todo（未开始）、
blocked（阻塞）。证据取值：verified（已独立验证）、reported（被报告）、
inferred（推断）、unknown（未知）、conflicted（冲突）。

只有 verified 才需要填写 verification 中的来源、方法和观察时间；
这仍不代表代码已成功部署。更新时应保留稳定 ID，若任务被删除，
也不能自动推断它已完成。依赖必须存在且不能形成环。

示例中含虚构任务，不能作为真实项目完成情况。接手时优先读取
简短摘要，再按需打开该文件，避免将完整任务表反复传给模型。
