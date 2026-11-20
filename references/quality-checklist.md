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
