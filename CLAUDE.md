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

<!-- AGENTS-TABLE-START -->
| Agent | Model | Purpose |
|-------|-------|---------|
| `c-level-shield` | sonnet | Use after writer agent completes the PRD draft. Simulates hard questions from McEasy C-Level executives (CEO, COO, CFO, CTO, CBO, CDSO) and appends a Q&A section to the PRD. Protects the product owner from being caught off guard in real C-level reviews. |
| `iot-research` | opus | Use when the user asks any question about the telematics or fleet management industry — market sizing, trends, vendor comparison, product specs, competitor intel, pricing, or regulation. Handles day-to-day research questions in a conversational way. Covers Indonesia and SEA as primary markets, with global context where relevant. Key vendors the user works with include Teltonika, BSJ, and Howen. |
<!-- AGENTS-TABLE-END -->

## Skills

Skills live in `.claude/skills/` and are reusable prompt workflows invocable across agents or directly in Claude Code sessions.

## Conventions

- Agent files use YAML frontmatter (`name`, `description`, `model`, `tools`) followed by the system prompt in Markdown.
- Model choices: use `opus` for deep research agents, `sonnet` for general-purpose, `haiku` for fast/cheap tasks.
- Tools should be scoped to the minimum the agent needs — don't give every agent `Write` if it only reads.
- Primary market context for all agents: Indonesia / Southeast Asia / McEasy business domain.
