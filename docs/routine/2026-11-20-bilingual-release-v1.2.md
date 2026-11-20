# 2026-11-20 — Bilingual release v1.2 / 双语发行整理

## 中文：已实施改动

用户已纠正此前的“可视化”要求，因此本次发行**不包含可视化前端**。

- README、SKILL、references、templates、historical docs、examples 双语统一。
- 保留 schema 1.0 样例供历史兼容测试，增加 V1.2 当前示例。
- 添加 VERSION、CHANGELOG、RELEASE_NOTES、发行指南。
- 增加可重现 ZIP、SHA-256、单元测试和 CI/发行自动化。
- 保留 Quick/Full/Update、九个固定标题与 Token 按需加载。
- 不添加模型调用、后台监控、数据库或远程运行时。

## English: changes

The user canceled the earlier visualization request; no UI or frontend is
included. This release harmonizes bilingual documentation and historical
files, preserves the legacy fixture, adds a current sample, versioning and
release notes, reproducible source distribution, checksum tests and CI-gated
publishing. No extra model, backend or remote dependency is introduced.

## 验证 / Verification

Release is complete only after successful GitHub Actions and a visible GitHub
Release with ZIP and SHA-256 assets. / 必须以实际自动测试和发行附件为准。

## 下一步 / Next steps

1. 检查发行 CI、Release 标签及附件，修复失败；Review CI, tag and assets.
2. 在 ChatGPT、Claude、Codex 实测 Token 与恢复成功率；Measure host-side
   prompt tokens and first-action success.
3. 改进冲突合并、证据过期回归；Test conflicts and stale evidence.
4. 由所有者决定开源许可证；Owner to choose an explicit license.
