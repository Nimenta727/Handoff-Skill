# V1 acceptance checklist

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
