# Changelog / 更新日志

All significant changes are recorded without rewriting their historical claims.
全部重要改动按版本保留，旧版协议不会被悄悄改写。

## 1.2.0 — 2026-11-20 / Bilingual release / 双语发行

### 中文
- 全面补充 README、SKILL、参考文件、模板、示例和历史文档的中英文内容。
- 新增标准库发行打包脚本：可重现 ZIP 和 SHA-256 文件。
- 增加自动化发行工作流、发行说明、版本管理和回归测试。
- 保持 1.0/1.1 manifest 兼容，并延续省 Token、按需加载设计。
- 未加入可视化、前端服务、模型调用或外部运行时。

### English
- Added bilingual README, SKILL, references, templates, examples and history.
- Added reproducible ZIP archive with SHA-256, built using only Python stdlib.
- Added release workflow, versioning, release notes and regression tests.
- Preserved 1.0/1.1 manifest support and token-aware progressive loading.
- No visualization UI, frontend, model calls or extra runtime dependencies.

## 1.1.0 — 2026-11-20 / Token-conscious continuation / 省 Token 续接

### 中文
- 默认不超过 1200 字符的接手摘要；按需展开附件。
- 引入稳定任务 ID 增量对比、TASKS.json 依赖检查、文件哈希验证。
- 新增 init、brief、diff、seal 工具及自动化测试。
- 字符数不是精确 Token 计量；SHA-256 不等于数字签名。

### English
- Introduced a bounded 1,200-character receiver brief and selective reads.
- Added stable task-ID diffs, optional task DAG and file-integrity hashes.
- Added init/brief/diff/seal commands plus automated tests.
- Character budget is not a token count; SHA-256 is not a signature.

## 1.0.0 — 2026-11-18 / Initial skill / 首版

### 中文
- 发布 Quick / Full / Update 模式，九个标准交接章节，接手提示、
  manifest.json、初代验证器和测试。
- 以证据等级、最小权限和脱敏作为主要原则。

### English
- Initial Quick/Full/Update skill, nine-heading format, receiver prompt,
  manifest, validator and tests.
- Established evidence grading, least privilege and redaction.

## Compatibility / 兼容性

Version 1.2.0 is the Skill/tool release, not a new manifest schema.
The validator still accepts schema_version 1.0 and 1.1; the legacy example
is retained as a regression fixture.
1.2.0 为 Skill/工具版本，并非 manifest schema 版本升级。
