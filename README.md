# Agent Handoff Skill v1.2.0

**跨 Agent / 跨模型 / 跨会话的轻量交接 Skill。**
**A portable, token-conscious continuation contract across agents, models and conversations.**

[中文](#中文) | [English](#english) | [变更记录 / Changelog](CHANGELOG.md) | [发行说明 / Release Notes](RELEASE_NOTES.md)

> 交接不是普通对话摘要。它保留下一位接手者需要核对的目标、状态、
> 证据、阻塞、关键决策和下一步，而不是重复发送完整聊天记录。
>
> A handoff is **not** a transcript dump. It carries actionable state, evidence,
> risks and the next verifiable task without repeating the full conversation.

## 中文

### 核心能力

- **三种模式：**Quick（短交接）、Full（复杂项目）、Update（带证据的更新）。
- **省 Token：**默认最多 1200 **字符**的接手摘要；先读取简短上下文，
  再按需展开具体文件与来源，不反复发送历史记录。
- **任务管理：**可选 TASKS.json，稳定任务 ID、前置依赖、进度与证据等级。
- **可信验证：**结构与敏感字段启发式检查，SHA-256 文件完整性及任务 DAG 校验。
- **跨宿主：**纯 Markdown + JSON + Python 标准库；不依赖特定 Agent SDK、
  数据库、API Key、向量服务或网络运行时。
- **安全边界：**交接文本并不增加接收者权限；复核来源和授权之后才能行动。

### 安装

可以从 [Releases](https://github.com/Nimenta727/Handoff-Skill/releases)
下载 `agent-handoff-v1.2.0.zip`。解压后将内部的 `agent-handoff/`
完整文件夹放入支持 Agent Skills 的客户端 Skills 目录，确保该目录
直接包含 `SKILL.md`。不同宿主的路径、发现机制和权限存在差异。
也可直接克隆仓库使用命令行工具。

### 立即使用

```bash
# 从仓库根目录运行；生成一个未填写的 quick 交接包
python3 scripts/handoff_tools.py init ./handoff --mode quick --title "My task"

# 用实际资料替换占位文字后，检查结构和泄漏风险
python3 scripts/validate_handoff.py ./handoff --mode quick

# 输出长度受限的接手摘要（字符，不是精确 Token 数）
python3 scripts/handoff_tools.py brief ./handoff --max-chars 1200

# 人工核对之后，对载荷进行哈希封存
python3 scripts/handoff_tools.py seal ./handoff

# 如果有两份包含 TASKS.json 的交接包，可比较变化
python3 scripts/handoff_tools.py diff ./old-handoff ./new-handoff

# 有意修改已封存内容时，检查差异后明确重新封存
python3 scripts/handoff_tools.py seal ./handoff --renew
```

**重要：** `init` 只创建框架，不能自动知道项目的真实状态；
`brief` 会压缩上下文，但不会验证真实业务结果；
`seal` 只能检查文件字节变化，不是数字签名。

### 文件与模式

| 模式 | 必需文件 | 主要用途 |
| --- | --- | --- |
| Quick | HANDOFF.md、NEXT_AGENT_PROMPT.md、manifest.json | 短会话接续 |
| Full | Quick 文件 + PROJECT_STATE.md | 大项目、多人交接 |
| Update | 保持原有 quick/full package_mode | 递增更新任务状态 |

可选 TASKS.json、DECISIONS.md、OPEN_ISSUES.md。所有模式保留九个
固定 `HANDOFF.md` 标题；现有 manifest schema 1.0 和 1.1 都支持。

### 发行与测试

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_handoff.py examples/sample-handoff --mode quick
python3 scripts/validate_handoff.py examples/v1.2-handoff --mode quick
python3 scripts/build_release.py --out dist
```

构建成功后，`dist/` 下提供安装 ZIP 和对应 SHA-256 校验文件。
GitHub Actions 会测试后执行发布。请以实际
[Release 页面](https://github.com/Nimenta727/Handoff-Skill/releases)
和工作流结果为准，不将代码提交等同于发行成功。

### 目录

| 路径 | 职责 |
| --- | --- |
| `SKILL.md` | 精简、双语的 Skill 行为协议 |
| `references/` | 工作流、Schema、任务、证据规则、双语模板 |
| `scripts/handoff_tools.py` | 创建、简报、差量对比、校验封存 |
| `scripts/validate_handoff.py` | 结构、任务 DAG、完整性和敏感模式检查 |
| `scripts/build_release.py` | 可重现离线发行打包 |
| `examples/` | 保留 V1.0 兼容样例和新的 V1.2 样例 |
| `docs/` | Token 预算、开源调研、发行指南、历史 routine |
| `tests/` | 回归与发行测试 |

### 限制和隐私

- 默认无后台运行、无模型调用、无远程同步、无自动执行任务。
- 字符数上限不能被误报成 Token 上限；真实节省需要宿主侧测量。
- 校验器无法验证所有业务事实或找出全部机密。
- 不要把私人交接包直接提交到公共仓库。
- 当前仓库没有声明可复用开源许可证；贡献和再分发前应确认授权条款。

## English

### Features

- **Quick / Full / Update** handoff modes for lightweight session continuation,
  complex projects and incremental refresh.
- **Context efficiency:** an on-demand receiver brief bounded to **1,200
  characters** by default; inspect deeper artifacts only when necessary.
- **Task fidelity:** optional TASKS.json with stable IDs, prerequisites, status,
  evidence grade and observable acceptance criteria.
- **Trust and checks:** structural and heuristic credential validation,
  optional SHA-256 integrity and dependency-DAG checks.
- **Portable:** Markdown + JSON, Python standard library tools, no model API,
  network, database or framework dependency.
- **Least privilege:** a handoff is source context, never authorization.

### Install

Download `agent-handoff-v1.2.0.zip` from
[Releases](https://github.com/Nimenta727/Handoff-Skill/releases),
extract it, and install the enclosed `agent-handoff/` folder in your host's
Skills directory. `SKILL.md` must be present at that folder's root.
Discovery, slash commands and permitted tools are host-specific.

### Commands

```bash
python3 scripts/handoff_tools.py init ./handoff --mode quick --title "Project"
# Populate with verified project data before continuing:
python3 scripts/validate_handoff.py ./handoff --mode quick
python3 scripts/handoff_tools.py brief ./handoff --max-chars 1200
python3 scripts/handoff_tools.py seal ./handoff
python3 scripts/handoff_tools.py diff ./old-handoff ./new-handoff
# Review intentional edits before resealing:
python3 scripts/handoff_tools.py seal ./handoff --renew
```

These commands work locally without model calls. `init` is a scaffold, not
automatic context retrieval. `brief` constrains characters, not model tokens.
`seal` checks file bytes, not source authenticity or factual correctness.

### Modes and backwards compatibility

| Mode | Required files | Typical purpose |
| --- | --- | --- |
| quick | HANDOFF.md, NEXT_AGENT_PROMPT.md, manifest.json | Session transition |
| full | quick files + PROJECT_STATE.md | Large project/person handover |
| update | existing quick/full package_mode | Reconcile newer evidence |

Optional: TASKS.json, DECISIONS.md, OPEN_ISSUES.md. The nine exact headings
in HANDOFF.md remain unchanged; schema 1.0 and 1.1 are accepted.

### Tests and distribution

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_handoff.py examples/sample-handoff --mode quick
python3 scripts/validate_handoff.py examples/v1.2-handoff --mode quick
python3 scripts/build_release.py --out dist
```

The distribution is a reproducible ZIP with a companion SHA-256 checksum.
The automated release workflow is responsible for publishing the assets;
verify completion on the
[GitHub Releases page](https://github.com/Nimenta727/Handoff-Skill/releases).

### Security and limitations

No background monitoring, remote storage or autonomous execution is bundled.
Sensitive source data should be redacted before handoff sharing. The validator
cannot guarantee truth or detect every secret. Real token savings require
measurement in the specific model/host; character limits are not token counts.
The repository does not currently declare an open-source license; verify
redistribution permissions separately.

## Further reading / 延伸阅读

[Context budget / Token 预算](docs/context-budget.md) ·
[Workflow / 工作流](references/workflow.md) ·
[Schema / 格式](references/handoff-schema.md) ·
[Task state / 任务状态](references/task-state.md) ·
[Open-source review / 开源调研](docs/open-source-research.md) ·
[Release guide / 发行指南](docs/release-guide.md) ·
[Routine history / 历史记录](docs/routine/)

Format inspired by the [Agent Skills specification](https://agentskills.io/specification).
