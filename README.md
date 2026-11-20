# Agent Handoff Skill V1.1

[中文](#中文说明) · [English](#english)

Portable, evidence-aware and token-conscious task handoffs across AI agents,
models, chat sessions and human collaborators. **Not a transcript summarizer.**

## 中文说明

V1.1 在 V1.0 Quick / Full / Update 的基础上增加：

- **省 Token：**接手先读至多 1200 字符的短摘要，其余文件按需打开；
  不复制整个聊天、代码或长日志。字符不等于 Tokens。
- **安全验证：**可选 SHA-256 字节完整性；敏感信息启发式检测；
  TASKS.json 的依赖环、重复任务、无来源的已验证状态检查。
- **增量更新：**按稳定 TASK ID 比较新旧任务，无需每次重复全部上下文。
- **轻量兼容：**仅用 Python 标准库；不用数据库、LLM API 或第三方依赖；
  保留 V1.0 manifest 兼容性。

### 安装

将包含 `SKILL.md` 的仓库目录放入支持 Agent Skills 的客户端 Skill 目录。
具体安装路径和自动发现行为取决于宿主客户端。没有 Python 的环境可按
SKILL.md 手工生成相同的交接内容。

### 快速使用

```bash
# 创建框架；之后必须以真实事实替换示例/占位内容
python3 scripts/handoff_tools.py init ./handoff --mode quick --title "My task"

# 结构、隐私启发式、任务依赖检查
python3 scripts/validate_handoff.py ./handoff --mode quick

# 只输出短版接手上下文，最多 1200 字符
python3 scripts/handoff_tools.py brief ./handoff --max-chars 1200

# 审阅完全部内容后添加 SHA-256 完整性记录
python3 scripts/handoff_tools.py seal ./handoff

# 比较两份交接中任务状态的变化
python3 scripts/handoff_tools.py diff ./old-handoff ./new-handoff

# 有意修改已封存内容后，先复核再显式更新校验值
python3 scripts/handoff_tools.py seal ./new-handoff --renew

python3 -m unittest discover -s tests -v
```

### 输出格式

| 模式 | 必需文件 |
| --- | --- |
| quick | HANDOFF.md, NEXT_AGENT_PROMPT.md, manifest.json |
| full | quick 全部文件，以及 PROJECT_STATE.md |
| update | 保留已有 quick/full 的 package_mode |

可选 TASKS.json：包含任务 ID、进度、证据等级、验收标准和依赖关系，
需列入 manifest 的 files。可选完整性信息在 manifest.integrity。

### 安全边界

交接不是授权。接手者必须重新核验来源、权限、测试和运行环境。
脚本不自动读取历史对话、不执行项目任务、不监听模型上下文、不部署。
SHA-256 只能发现字节变化，不能证明来源可信或内容真实。
校验器无法排除全部敏感信息与业务事实错误。

### 结构

- `SKILL.md` — 主协议，优先读取，精简上下文
- `references/` — 工作流、规范、任务状态、模板和校验规则
- `scripts/` — 完整性与任务校验，以及 init/brief/diff/seal
- `tests/` — 新旧版本及异常场景回归
- `docs/context-budget.md` — 渐进式加载与 Token 衡量方法
- `docs/open-source-research.md` — 开源方案的借鉴与拒绝项
- `docs/routine/` — 每次 GitHub 改动的时间记录和后续计划

## English

Agent Handoff is a portable continuation contract. It captures task goal,
current status, evidence confidence, key decisions, blockers, artifacts and
the next verifiable action. Load a bounded brief before reading deeper sources.

Quick setup:

```bash
python3 scripts/handoff_tools.py init ./handoff --mode quick --title "Project"
python3 scripts/validate_handoff.py ./handoff
python3 scripts/handoff_tools.py brief ./handoff --max-chars 1200
python3 scripts/handoff_tools.py seal ./handoff
```

The 1200-character limit is **not** a measured token count. True savings must
be measured using the receiving host and tokenizer. V1.0 packages remain valid;
manifest.integrity and TASKS.json are optional V1.1 additions.

See [context budget](docs/context-budget.md),
[task schema](references/task-state.md),
[open-source design research](docs/open-source-research.md),
and [routine logs](docs/routine/).
Based on the [Agent Skills specification](https://agentskills.io/specification).
