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

### `iot-research`

> Senior IoT and telematics market researcher embedded at McEasy.

- **Model:** Opus
- **Tools:** WebSearch, WebFetch, Read, Glob, Grep
- **Scope:** Market sizing, vendor comparison, competitor intel, hardware specs, regulation — Indonesia and SEA primary, global context where relevant.
- **Key vendors:** Teltonika, BSJ, Howen

---

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
