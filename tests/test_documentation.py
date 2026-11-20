"""Bilingual and release-readiness tests (no external network calls)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    "README.md", "SKILL.md", "CHANGELOG.md", "RELEASE_NOTES.md",
    "docs/context-budget.md", "docs/open-source-research.md",
    "docs/release-guide.md",
    "references/workflow.md", "references/handoff-schema.md",
    "references/verification-rules.md", "references/quality-checklist.md",
    "references/task-state.md",
    "references/templates/quick.md", "references/templates/full.md",
    "references/templates/next-agent.md", "examples/README.md",
    "examples/sample-handoff/HANDOFF.md",
    "examples/sample-handoff/NEXT_AGENT_PROMPT.md",
    "examples/v1.2-handoff/HANDOFF.md",
    "examples/v1.2-handoff/NEXT_AGENT_PROMPT.md",
]


class DocumentationTests(unittest.TestCase):
    def test_bilingual_files(self):
        for name in DOCS:
            with self.subTest(file=name):
                s = (ROOT / name).read_text(encoding="utf-8")
                self.assertRegex(s, r"[\u4e00-\u9fff]")
                self.assertRegex(s, r"[A-Za-z]{4,}")

    def test_release_version_sync(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        for file in ("README.md", "CHANGELOG.md", "RELEASE_NOTES.md"):
            with self.subTest(file=file):
                self.assertIn(version, (ROOT / file).read_text(encoding="utf-8"))

    def test_cancelled_visualization_not_shipped(self):
        self.assertFalse((ROOT / "scripts/visualize_handoff.py").exists())
        self.assertFalse((ROOT / "docs/visualization.md").exists())

    def test_legacy_schema_remains_legacy(self):
        old = json.loads((ROOT / "examples/sample-handoff/manifest.json").read_text())
        new = json.loads((ROOT / "examples/v1.2-handoff/manifest.json").read_text())
        self.assertEqual(old["schema_version"], "1.0")
        self.assertEqual(new["schema_version"], "1.1")
        self.assertEqual(new["skill_version"], (ROOT / "VERSION").read_text().strip())


if __name__ == "__main__":
    unittest.main()
