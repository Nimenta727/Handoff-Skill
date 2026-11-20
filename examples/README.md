# Examples / 示例

- `sample-handoff/` is the **original V1.0 manifest fixture**. Its manifest
  remains schema 1.0 on purpose to prove backward compatibility; text is bilingual.
  `sample-handoff/` 保留历史 1.0 清单，不升级协议版本，以便回归测试。
- `v1.2-handoff/` is a **schema 1.1 fixture for Skill v1.2.0** with
  a bilingual Quick handoff and optional TASKS.json dependency ledger.
  `v1.2-handoff/` 采用 1.1 清单及 1.2.0 Skill，包含双语任务与依赖示例。

Both projects are fictitious. Neither verifies a real user's progress,
deployment or project state. / 两个示例均为虚构演示，不代表实际任务已完成。

```bash
python3 scripts/validate_handoff.py examples/sample-handoff --mode quick
python3 scripts/validate_handoff.py examples/v1.2-handoff --mode quick
python3 scripts/handoff_tools.py brief examples/v1.2-handoff --max-chars 900
```
