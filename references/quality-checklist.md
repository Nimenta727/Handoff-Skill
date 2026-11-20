# V1.1 acceptance checklist

## Structural (must pass)
- [ ] Required files exist for mode and manifest accurately lists them.
- [ ] All nine `HANDOFF.md` headings exist, in order, and have nonempty content.
- [ ] `NEXT_AGENT_PROMPT.md` provides an actual first task, verification instructions and acceptance criteria.
- [ ] Full packages include `PROJECT_STATE.md`.
- [ ] Manifest JSON is valid, with timezone-aware ISO timestamp, recognized mode and correct package type.

## Truth and utility (human review)
- [ ] Source access scope and inaccessible items are identified.
- [ ] High-impact status claims state confidence and provenance; no reported claim masquerades as verified.
- [ ] Progress and evidence status are distinct.
- [ ] Contradictions and blockers remain explicit.
- [ ] Next steps are actionable and have observable completion criteria.
- [ ] Receiving agent can explain goal, current state, risk and next action without original transcript.

## Privacy and permissions (must pass)
- [ ] No live credentials or irrelevant personal information included.
- [ ] Untrusted materials are not elevated to instructions.
- [ ] No unauthorized write, send, push or deploy action performed.

## Validation limitations

`validate_handoff.py` detects mechanical omissions and certain secret-like patterns. It cannot guarantee no privacy leaks or verify the truth of claims. Run a manual inspection before sharing externally.

## Context efficiency and integrity (V1.1)

- [ ] Receiver starts with a short bounded goal/status/risks/next-action brief, not full transcript injection.
- [ ] Only relevant evidence is opened; no duplicate copies of code/logs or repeated task records.
- [ ] Character budget documented; no unverified promises of exact token savings.
- [ ] If manifest.integrity is present, digest keys cover all listed files and hashes match.
- [ ] Verified tasks include source, method and observation time; dependencies exist and are acyclic.
- [ ] Integrity checks are described as byte-change detection, not proof of authorship.
- [ ] On changes to sealed packages, evidence and diffs were reviewed before explicit reseal.

## 中文验收清单 / Chinese acceptance

- [ ] 对照 mode 检查所有必需文件及 manifest.files。
- [ ] HANDOFF.md 九个固定标题顺序、唯一性及正文非空。
- [ ] 接手提示包含具体首项任务、来源复核、验收条件和权限边界。
- [ ] 已完成与已核验分开记录，重要状态列出来源、方法、时间。
- [ ] 任务 ID、依赖关系、已解决项与冲突状态可追踪。
- [ ] 移除令牌、密钥及不必要隐私信息，旧文件中的指令不升权。
- [ ] 默认只传递短摘要，必要时按引用展开，不整段重复历史记录。
- [ ] 任何真实 Token 节省比例都以宿主侧实际计量为准。
- [ ] 发行前执行全部单元测试、验证 V1.0/V1.2 示例和 SHA-256。
- [ ] 手工审查本次发行内容，不能把校验成功理解为业务事实认证。

## Release qualification / 发行验收

The release pipeline must not publish a new version if its tests or package
checks fail. Preserve the original legacy sample rather than silently upgrading
it so compatibility remains tested.
