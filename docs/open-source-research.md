# Open-source design review — 2026-11-20

Relevant designs were examined, but no external implementation code was copied.

| Reference | Insight | Local choice |
| --- | --- | --- |
| [Agent Skills spec](https://agentskills.io/specification) | Discoverable entry, references on demand | Small SKILL.md and lazy references |
| [OpenAI Agents SDK handoffs](https://openai.github.io/openai-agents-python/handoffs/) | Filters can limit forwarded history | Bounded local receiver brief, no SDK coupling |
| [LangGraph thinking](https://docs.langchain.com/oss/javascript/langgraph/thinking-in-langgraph) | Explicit state and checkpoints | Portable task ledger; NOT runtime checkpoints |
| [thieung handoff](https://github.com/thieung/agent-skills/blob/main/skills/handoff/SKILL.md) | Source pointers, cold-start context | Avoid pasted logs, use exact paths |
| [forest session handoff](https://github.com/forest/agent-skills/blob/main/plugins/session-handoff/skills/session-handoff/SKILL.md) | Fact-first concise summaries | Confidence grading and concise decisions |
| [wjgoarxiv handoff](https://github.com/wjgoarxiv/agent-handoff-skill/blob/main/SKILL.md) | Stale context reconciliation | Explicit update/diff mode |
| [Microsoft hve-core](https://github.com/microsoft/hve-core/blob/main/docs/rpi/context-engineering.md) | Durable artifacts prevent rediscovery | Read only evidence relevant to current phase |

Rejected as unnecessary for a portable Skill: DB-backed persistence,
multi-agent runtime, vector search, auto-compaction hooks, remote telemetry,
implicit code execution and claims of exact token savings without measurements.

Future: host-specific measured prompt-token benchmarks; opt-in low-permission
resume hooks; tests for conflicting and stale evidence; first-action success metrics.

## 中文摘要与架构取舍 / Chinese design notes

调研包括 Agent Skills 规范、OpenAI Agents SDK、LangGraph、社区 Handoff Skills
和微软上下文工程。主要借鉴渐进式加载、明确任务状态和来源引用，
而不是集成重量级框架。没有复制第三方实现代码；也不承诺未经实测的
Token 节省比例。下一步应在 ChatGPT、Claude、Codex 对比真实成本和质量。

## Research limitations / 调研限制

These sources inform architectural choices; the present Skill tests do not
verify other frameworks' performance claims. No external framework is bundled.
