# Agent Handoff Skill V1.0

全场景 Agent 交接 Skill：将当前任务状态转换为可继续执行的交接包，而非普通聊天摘要。

## 安装

将 `agent-handoff/` 整个文件夹放进支持 Agent Skills 的客户端 Skill 目录，然后重新加载 Skill（具体路径随客户端不同而变化）。安装的根目录必须包含 `SKILL.md`；不能只放 ZIP 而不解压（除非客户端支持 ZIP 导入）。

## 使用示例

- `用 agent-handoff 快速交接当前任务给新 Agent。`
- `用 agent-handoff 的 full 模式生成完整项目交接。`
- `更新之前的 agent-handoff 交接文件。`
- `准备交接给同事，帮我脱敏并整理接手说明。`

也可以使用明确调用 `/agent-handoff`，但斜杠命令是否可用取决于宿主客户端。

## 输出

Quick 输出 `HANDOFF.md`、`NEXT_AGENT_PROMPT.md`、`manifest.json`；Full 额外有 `PROJECT_STATE.md`，其他附录按需输出。无文件写权限时生成可复制的 Markdown 文本。

## 验证

```bash
python3 scripts/validate_handoff.py /path/to/handoff --mode quick
python3 -m unittest discover -s tests -v
```

本工具的脚本仅做结构检查、有限敏感信息检查，不能证明内容事实准确，也不能替代人工审查。

## 设计原则

- 不假装访问不存在的上下文，不暗示能后台常驻。
- 任务进度和证据可信度严格区分。
- 默认只读、最小权限、脱敏交接。
- 不依赖仓库、外部 API 或专用服务。

格式参照 [Agent Skills Specification](https://agentskills.io/specification)。不同宿主的自动发现、工具权限、调用方式不保证完全一致。
