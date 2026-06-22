# grady-agents

This is Grady's personal Claude Code agents and skills repository for McEasy — a B2B SaaS telematics and logistics platform based in Indonesia.

## Repository Structure

```
grady-agents/
├── .claude/
│   ├── agents/               # Claude agent definitions (.md files with frontmatter)
│   │   └── iot-research.md
│   └── skills/               # Reusable skill definitions
├── CLAUDE.md                 # This file
└── README.md
```

## Agents

Each agent lives in `.claude/agents/<agent-name>/` as a Markdown file with YAML frontmatter. The frontmatter defines the agent's name, description, model, and tools.

| Agent | Purpose |
|-------|---------|
| `iot-research` | IoT and telematics market research — vendor comparison, market sizing, competitor intel, regulation. Primary focus on Indonesia and SEA. |

## Skills

Skills live in `.claude/skills/` and are reusable prompt workflows invocable across agents or directly in Claude Code sessions.

## Conventions

- Agent files use YAML frontmatter (`name`, `description`, `model`, `tools`) followed by the system prompt in Markdown.
- Model choices: use `opus` for deep research agents, `sonnet` for general-purpose, `haiku` for fast/cheap tasks.
- Tools should be scoped to the minimum the agent needs — don't give every agent `Write` if it only reads.
- Primary market context for all agents: Indonesia / Southeast Asia / McEasy business domain.
