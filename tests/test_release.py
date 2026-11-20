"""Release and bilingual packaging regression tests (stdlib only)."""
import hashlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_release import build, source_files


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.ctx = tempfile.TemporaryDirectory()
        self.root = Path(self.ctx.name) / "project"
        self.root.mkdir()
        for name, body in (
            ("SKILL.md", "---\nname: agent-handoff\n---\n"),
            ("README.md", "# Readme\n"), ("VERSION", "1.2.0\n"),
        ):
            (self.root / name).write_text(body, encoding="utf-8")
        (self.root / ".env").write_text("DO_NOT_PACKAGE=secret\n", encoding="utf-8")
        docs = self.root / "docs"
        docs.mkdir()
        (docs / "guide.md").write_text("# Guide\n", encoding="utf-8")
        (docs / ".local-secret.md").write_text("secret\n", encoding="utf-8")
        (docs / "cache").mkdir()
        (docs / "cache" / "notes.bin").write_bytes(b"secret")

    def tearDown(self):
        self.ctx.cleanup()

    def test_reproducible_archive_checksum_and_paths(self):
        dist = Path(self.ctx.name) / "dist"
        archive, digest_file, digest = build(self.root, dist)
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), digest)
        self.assertEqual(digest_file.read_text(), digest + "  " + archive.name + "\n")
        with zipfile.ZipFile(archive) as z:
            paths = z.namelist()
        self.assertIn("agent-handoff/SKILL.md", paths)
        self.assertIn("agent-handoff/README.md", paths)
        self.assertIn("agent-handoff/docs/guide.md", paths)
        self.assertNotIn("agent-handoff/.env", paths)
        self.assertFalse(any("secret" in name or "cache" in name for name in paths))
        before = archive.read_bytes()
        build(self.root, dist)
        self.assertEqual(archive.read_bytes(), before)

    def test_invalid_version(self):
        with self.assertRaises(ValueError):
            build(self.root, Path(self.ctx.name) / "dist", "../1.2.0")

    def test_missing_required_file(self):
        (self.root / "SKILL.md").unlink()
        with self.assertRaises(ValueError):
            source_files(self.root)

    def test_no_symlink_escaping_source(self):
        dst = Path(self.ctx.name) / "outside.md"
        dst.write_text("private", encoding="utf-8")
        link = self.root / "docs" / "external.md"
        try:
            link.symlink_to(dst)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unsupported")
        with self.assertRaises(ValueError):
            source_files(self.root)


if __name__ == "__main__":
    unittest.main()
