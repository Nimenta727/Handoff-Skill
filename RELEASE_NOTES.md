# Agent Handoff Skill v1.2.0 / 双语发行版

## 中文

本次发行聚焦于**全项目中英文双语、历史文档整理、可重现打包及自动验证**，
不引入可视化前端、在线服务或额外 Agent。

主要更新：
- README、SKILL、references、templates、examples、docs 及历史记录统一双语；
- 纯 Python 标准库构建 ZIP 安装包并提供 SHA-256 校验文件；
- GitHub Actions 在发布之前执行测试、校验新旧示例与打包；
- 保留 Quick/Full/Update 和九个固定标题，兼容 manifest 1.0/1.1；
- 继续默认短摘要、任务增量更新、按需读取，避免增加模型 Token 调用。

安装：解压 `agent-handoff-v1.2.0.zip`，将里面的 `agent-handoff/`
整个目录安装到宿主的 Skill 目录，确保根目录包含 `SKILL.md`。
具体宿主的安装方式和权限请参考 README。不要把 ZIP 作为未解压文件
放入不支持直接导入压缩包的客户端。

验证：ZIP 旁的 `.sha256` 是字节完整性校验，不是发布者签名。
自动化结构测试也不保证交接内容的事实真实性。

## English

This release standardizes **bilingual documentation, historical records,
reproducible packaging and automated verification**. It does not add
visualization, online services or multi-agent runtime dependencies.

Highlights:
- Bilingual README, SKILL, references, templates, examples and changelog;
- Reproducible source ZIP and SHA-256 checksum from Python standard library;
- CI-gated release pipeline, validating legacy and current examples;
- Quick/Full/Update retained with the nine required headings and manifest 1.0/1.1;
- Bounded resume brief and selective loading to reduce repeated context.

Install: Extract `agent-handoff-v1.2.0.zip` and install its
`agent-handoff/` folder in your host's Skill directory. Its root must include
`SKILL.md`; discovery differs between hosts.

Verify the adjacent `.sha256`. Hashes detect changes, not publisher identity.
Automated tests cannot establish factual accuracy of source claims.

## Release checks / 发行检验

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_handoff.py examples/sample-handoff --mode quick
python3 scripts/validate_handoff.py examples/v1.2-handoff --mode quick
python3 scripts/build_release.py --out dist
```

A release is complete only when GitHub Actions passes and the GitHub Release
contains both ZIP and SHA-256 assets. If permission or configuration prevents
publication, check the workflow logs before claiming success.
