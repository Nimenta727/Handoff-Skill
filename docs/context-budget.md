# Context efficiency / Token 预算工程

## What is guaranteed

The receiver-brief CLI bounds **characters**, not model tokens.
Default max: 1200 characters. Minimum accepted: 600.

```bash
python3 scripts/handoff_tools.py brief ./handoff --max-chars 1200
```

True token usage depends on the model tokenizer, host prompts, tool wrappers,
and language. The project does NOT claim an exact token savings percentage.

## Progressive context tiers

| Tier | Read | Policy |
| --- | --- | --- |
| 0 | manifest + bounded brief | Start here |
| 1 | relevant HANDOFF.md section | Only when necessary |
| 2 | TASKS.json, PROJECT_STATE.md or linked artifacts | Only for target task |
| 3 | old chats, broad repo scan, verbose logs | Last resort, evidence gap only |

Preserve five non-negotiable elements in every brief: goal and hard constraints,
current progress with confidence, blockers, concrete next step, and a pointer to
details. Truncated fields must explicitly cite the source section.

Avoid copying source code or logs into a handoff. Prefer paths, commit hashes,
test commands and issue URLs. Do not send unchanged historical tasks repeatedly.
Use incremental comparison by stable task ID. The deterministic CLI does no LLM,
network, database, vector search or multi-agent routing calls.

## Validation and real-world measurement

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_handoff.py ./handoff --json
```

Compare the real prompt tokens the host reports for the same task with and
without the short handoff. Also measure accurate first-task completion,
repeated discovery calls and lost constraints. Fewer characters with worse
outcomes is not an optimization.

中文：1200 是字符上限，不等于 1200 tokens。默认只加载极简上下文，
细节按需读取。不能为了压缩而丢弃关键约束、风险或验证条件。

## 中文完整说明 / Chinese reference

`brief --max-chars 1200` 承诺的是**字符上限**，不是模型 Token 数。
同一段中文/英文在不同宿主及 tokenizer 下有不同消耗，不能把摘要
字符数直接转换为 Token 节省比例。

四层渐进加载：第一层只读清单与短摘要；第二层根据疑问读取
HANDOFF.md 中的具体章节；第三层只读与当前任务相关的 TASKS.json、
PROJECT_STATE.md 与证据；第四层在必要时才回溯长日志或历史会话。

压缩时优先保留用户目标、硬约束、已完成与未完成任务、可信状态、
阻塞项、最先执行的动作及验收标准；长日志使用路径、提交号和复现命令
代替。增量更新必须保证原有事实不被无证据地修改。若需要验证实际
成本，应在相同模型、相同任务、相同宿主分别记录 prompt tokens、
工具调用次数、任务成功率、误判与遗漏约束。
