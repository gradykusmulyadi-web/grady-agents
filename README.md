# grady-agents

Personal Claude Code agents and skills for Grady @ McEasy.

McEasy is a B2B SaaS telematics and logistics platform based in Indonesia. Products include GPS tracking devices, TrackVision (AI dashcam with DMS/ADAS), and a fleet management platform serving vehicle owners, 3PL logistics operators, and transportation vendors across Indonesia and Southeast Asia.

---

## Structure

```
grady-agents/
├── .claude/
│   ├── agents/
│   │   └── iot-research.md
│   └── skills/
├── CLAUDE.md
└── README.md
```

### .claude/agents/

Each subdirectory is one agent. The `.md` file inside contains:
- **YAML frontmatter** — `name`, `description`, `model`, `tools`
- **System prompt** — the agent's full instructions in Markdown

### .claude/skills/

Reusable skill definitions that can be invoked across sessions or composed into agents.

---

## Agents

<!-- AGENTS-START -->
### `c-level-shield`

> Use after writer agent completes the PRD draft. Simulates hard questions from McEasy C-Level executives (CEO, COO, CFO, CTO, CBO, CDSO) and appends a Q&A section to the PRD. Protects the product owner from being caught off guard in real C-level reviews.

- **Model:** sonnet
- **Tools:** Read, Write

---

### `iot-research`

> Use when the user asks any question about the telematics or fleet management industry — market sizing, trends, vendor comparison, product specs, competitor intel, pricing, or regulation. Handles day-to-day research questions in a conversational way. Covers Indonesia and SEA as primary markets, with global context where relevant. Key vendors the user works with include Teltonika, BSJ, and Howen.

- **Model:** opus
- **Tools:** WebSearch, WebFetch, Read, Glob, Grep

---
<!-- AGENTS-END -->

## Adding a New Agent

1. Create `.claude/agents/<agent-name>.md` with this frontmatter:

```yaml
---
name: <agent-name>
description: <one-line trigger description for Claude Code>
model: opus | sonnet | haiku
tools: Tool1, Tool2, ...
---

<system prompt here>
```

3. Update this README with a row in the Agents table.
