# Release guide / 发行指南

## 中文

1. 更新 VERSION（SemVer），同步 README、CHANGELOG、RELEASE_NOTES。
2. 校对中英文文档、模板、旧示例与当前示例。
3. 执行全部单元测试，并验证 schema 1.0 和 1.1 两套示例。
4. 构建可重现 ZIP 和 SHA-256，检查安装根目录直接有 SKILL.md。
5. VERSION 变化推送到 main 后，GitHub Actions 会重新测试，
   然后创建对应版本的 Release，并上传 ZIP 与 SHA-256。
6. 查阅真实 Actions 和 Release 结果，不能把 Git commit 当作发行成功。

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_handoff.py examples/sample-handoff --mode quick
python3 scripts/validate_handoff.py examples/v1.2-handoff --mode quick
python3 scripts/build_release.py --out dist
cd dist && sha256sum -c agent-handoff-v1.2.0.zip.sha256
```

仅发行 Skill、参考、测试、文档和示例，不包含私人 handoff、环境变量及缓存。
SHA-256 用于文件一致性校验，不能证明发布者身份。仓库还没有明确的
开源许可证，不应由工具擅自替所有者选择。

## English

1. Update VERSION (SemVer), README, CHANGELOG and RELEASE_NOTES.
2. Proofread bilingual documentation, templates, legacy and current examples.
3. Run all tests and validate schema 1.0 and 1.1 fixtures.
4. Build a reproducible ZIP + SHA-256; confirm SKILL.md is at the install root.
5. Pushing a changed VERSION to main runs the release workflow: it tests again,
   then creates a GitHub Release with both archive and checksum assets.
6. Inspect the real Actions and Release pages. A commit is not proof of release.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py --out dist
cd dist && sha256sum -c agent-handoff-v1.2.0.zip.sha256
```

No private handoff, environment variables, cached files or generated context
is packaged. SHA-256 is not a publisher signature. A public license has not
yet been selected by the repository owner.

## Troubleshooting / 故障排查

- Permission denied: verify GITHUB_TOKEN contents write access in repository settings.
  / 无权限：检查 Actions Token 的 contents: write。
- Tag already exists: inspect existing tag/release, do not force-push.
  / 标签已存在时先核查，禁止强制覆盖。
- Fixture fails: correct the schema or content before publication.
  / 样例失败先修复。
- Missing assets: check ZIP and SHA-256 on the GitHub Release page.
  / 确认两个附件都存在。
