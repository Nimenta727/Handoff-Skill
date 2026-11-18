import datetime
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_handoff import HEADINGS, validate


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.ctx = tempfile.TemporaryDirectory()
        self.root = Path(self.ctx.name)
        body = '# Example\n\n' + '\n\n'.join(f'## {h}\n\n已知信息，证据：对话记录；未知部分待核验。' for h in HEADINGS)
        (self.root / 'HANDOFF.md').write_text(body, encoding='utf-8')
        (self.root / 'NEXT_AGENT_PROMPT.md').write_text(
            '# Receiver\n\n先验证文件，核验当前状态，之后完成第一项工作。\n\n'
            '目标：整理已有任务。输入：已有笔记。行动：阅读并核对。'
            '验收标准：列出下一步和风险，并得到用户确认。' * 2,
            encoding='utf-8')
        self.data = {
            'schema_version': '1.0', 'skill': 'agent-handoff', 'skill_version': '1.0.0',
            'mode': 'quick', 'package_mode': 'quick',
            'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'language': 'zh-CN', 'files': ['HANDOFF.md', 'NEXT_AGENT_PROMPT.md'],
            'validation': {'status': 'not_run', 'notes': 'test'},
        }
        self.save()

    def tearDown(self):
        self.ctx.cleanup()

    def save(self):
        (self.root / 'manifest.json').write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')

    def test_valid_quick(self):
        self.assertEqual(validate(self.root)[0], [])

    def test_missing_mandatory_file(self):
        (self.root / 'HANDOFF.md').unlink()
        self.assertTrue(validate(self.root)[0])

    def test_missing_heading(self):
        p = self.root / 'HANDOFF.md'
        p.write_text(p.read_text().replace('## 07. 下一步计划', '## 07. 临时章节'))
        self.assertTrue(any('07. 下一步计划' in s for s in validate(self.root)[0]))

    def test_empty_heading(self):
        p = self.root / 'HANDOFF.md'
        p.write_text(p.read_text().replace('## 03. 当前状态\n\n已知信息，证据：对话记录；未知部分待核验。', '## 03. 当前状态\n'))
        self.assertTrue(any('Empty heading' in s for s in validate(self.root)[0]))

    def test_invalid_timezone(self):
        self.data['generated_at'] = '2026-11-18T10:00:00'
        self.save()
        self.assertTrue(any('timezone' in s for s in validate(self.root)[0]))

    def test_full_requires_project_state(self):
        self.data['mode'] = self.data['package_mode'] = 'full'
        self.save()
        self.assertTrue(any('PROJECT_STATE.md' in s for s in validate(self.root)[0]))

    def test_full_valid(self):
        self.data['mode'] = self.data['package_mode'] = 'full'
        self.data['files'].append('PROJECT_STATE.md')
        (self.root / 'PROJECT_STATE.md').write_text('# Progress\n\nNo extra state.')
        self.save()
        self.assertEqual(validate(self.root)[0], [])

    def test_update_preserves_package_mode(self):
        self.data['mode'] = 'update'
        self.save()
        self.assertEqual(validate(self.root)[0], [])

    def test_unsafe_path(self):
        self.data['files'].append('../secrets.txt')
        self.save()
        self.assertTrue(any('Unsafe' in s for s in validate(self.root)[0]))

    def test_secret_detected(self):
        with (self.root / 'HANDOFF.md').open('a') as f:
            f.write('\npassword = "superlongpassword123456"\n')
        self.assertTrue(any('Secret-like' in s for s in validate(self.root)[0]))

    def test_no_verification_instruction(self):
        (self.root / 'NEXT_AGENT_PROMPT.md').write_text('第一步：整理数据。验收标准：完成目录。' * 10)
        self.assertTrue(any('verification' in s for s in validate(self.root)[0]))

    def test_manifest_missing(self):
        (self.root / 'manifest.json').unlink()
        self.assertTrue(validate(self.root)[0])


if __name__ == '__main__':
    unittest.main()
