import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from handoff_tools import brief, delta, init, seal
from validate_handoff import validate


class Handoff11Tests(unittest.TestCase):
    def setUp(self):
        self.ctx = tempfile.TemporaryDirectory()
        self.root = Path(self.ctx.name) / "handoff"
        init(self.root, "quick", "Test task")

    def tearDown(self):
        self.ctx.cleanup()

    def _task(self, tid="TASK-001", deps=None, status="todo", evidence="reported"):
        return {"id": tid, "name": "Verify artifact", "status": status,
                "evidence_status": evidence,
                "dependencies": deps or [], "acceptance_criteria": ["Verified result"]}

    def _write_tasks(self, root, tasks):
        (root / "TASKS.json").write_text(json.dumps({"tasks": tasks}), encoding="utf-8")
        m = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        if "TASKS.json" not in m["files"]:
            m["files"].append("TASKS.json")
        (root / "manifest.json").write_text(json.dumps(m), encoding="utf-8")

    def test_init_quick_and_seal(self):
        self.assertEqual(validate(self.root)[0], [])
        self.assertEqual(seal(self.root), 2)
        self.assertEqual(validate(self.root), ([], []))

    def test_init_full(self):
        root = Path(self.ctx.name) / "full"
        init(root, "full", "Full task")
        self.assertEqual(validate(root)[0], [])
        seal(root)
        self.assertEqual(validate(root)[0], [])

    def test_init_no_clobber(self):
        with self.assertRaises(ValueError):
            init(self.root, "quick", "Other")

    def test_integrity_detects_tampering(self):
        seal(self.root)
        with (self.root / "HANDOFF.md").open("a") as out:
            out.write("\nTamper\n")
        self.assertTrue(any("Integrity mismatch" in item for item in validate(self.root)[0]))
        with self.assertRaises(ValueError):
            seal(self.root)
        seal(self.root, renew=True)
        self.assertEqual(validate(self.root)[0], [])

    def test_brief_bounded_and_mandatory_fields(self):
        seal(self.root)
        summary, warnings = brief(self.root, 600)
        self.assertLessEqual(len(summary), 600)
        for label in ("目标：", "状态：", "风险：", "下一步：", "接手验证："):
            self.assertIn(label, summary)
        self.assertEqual(warnings, [])
        self.assertIn("HANDOFF.md", summary)

    def test_brief_rejects_too_small_budget(self):
        with self.assertRaises(ValueError):
            brief(self.root, 300)

    def test_tasks_valid(self):
        self._write_tasks(self.root, [self._task()])
        self.assertEqual(validate(self.root)[0], [])
        seal(self.root)
        self.assertEqual(validate(self.root)[0], [])

    def test_tasks_missing_dependency(self):
        self._write_tasks(self.root, [self._task(deps=["MISSING"])])
        self.assertTrue(any("unknown dependency" in e for e in validate(self.root)[0]))

    def test_tasks_cycle(self):
        self._write_tasks(self.root, [self._task("TASK-001", ["TASK-002"]), self._task("TASK-002", ["TASK-001"])])
        self.assertTrue(any("Cyclic" in e for e in validate(self.root)[0]))

    def test_tasks_verified_requires_provenance(self):
        self._write_tasks(self.root, [self._task(evidence="verified")])
        self.assertTrue(any("verification source" in e for e in validate(self.root)[0]))

    def test_tasks_duplicate_id(self):
        self._write_tasks(self.root, [self._task(), self._task()])
        self.assertTrue(any("Duplicate task id" in e for e in validate(self.root)[0]))

    def test_delta_only_changed(self):
        self._write_tasks(self.root, [self._task()])
        root2 = Path(self.ctx.name) / "handoff2"
        init(root2, "quick", "Task update")
        self._write_tasks(root2, [self._task(status="in_progress"), self._task("TASK-002")])
        diff = delta(self.root, root2)
        self.assertEqual(diff["added"], ["TASK-002"])
        self.assertEqual([i["id"] for i in diff["changed"]], ["TASK-001"])
        self.assertEqual(diff["removed"], [])

    def test_symlink_rejected(self):
        ext = Path(self.ctx.name) / "unsafe.md"
        ext.write_text("unsafe")
        link = self.root / "LINK.md"
        try:
            link.symlink_to(ext)
        except (OSError, NotImplementedError):
            self.skipTest("symlink not supported")
        m = json.loads((self.root / "manifest.json").read_text())
        m["files"].append("LINK.md")
        (self.root / "manifest.json").write_text(json.dumps(m))
        self.assertTrue(any("Unsafe" in e for e in validate(self.root)[0]))


if __name__ == "__main__":
    unittest.main()
