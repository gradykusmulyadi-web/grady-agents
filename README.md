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

### `cv-screener`

> Core CV screening engine. Reads a single CV file against the job rubric and examples, and emits a structured scoring record. Called in a loop by the /screen-cv skill for every file in inbox/. Recommended model: Sonnet.

- **Model:** sonnet
- **Tools:** Read, Write, Bash

---

### `feedback-learner`

> Reads a recruiter-corrected screening spreadsheet, diffs agent tiers vs recruiter overrides, and updates rubric.md and examples.md to close the gap. Recommended model: Opus.

- **Model:** opus
- **Tools:** Read, Write, Bash

---

### `iot-research`

> Use when the user asks any question about the telematics or fleet management industry — market sizing, trends, vendor comparison, product specs, competitor intel, pricing, or regulation. Handles day-to-day research questions in a conversational way. Covers Indonesia and SEA as primary markets, with global context where relevant. Key vendors the user works with include Teltonika, BSJ, and Howen.

- **Model:** opus
- **Tools:** WebSearch, WebFetch, Read, Glob, Grep

---

### `rubric-builder`

> Converts a raw Job Description into a structured, editable rubric.md that the cv-screener agent uses for scoring. Run once per new position. Recommended model: Opus.

- **Model:** opus
- **Tools:** Read, Write, Bash

---

### `task-daily-review`

> Use when the user wants to know what to work on today or this week. Reads all active tasks, prioritizes by urgency, and outputs a ranked table with reasoning. Triggers include "what should I work on today", "daily review", "weekly recap", "what's due this week", "task priority", "morning briefing", "what's on my plate".

- **Model:** sonnet
- **Tools:** Read

---

### `task-editor`

> Use when the user wants to edit a task, update task fields, resolve flagged tasks, or mark a task as complete. Also use when the user says "show task editor" to render the full task list as an interactive UI. Triggers include "update task", "mark done", "fix flagged", "edit T003", "resolve flags", "show task editor", "task editor UI".

- **Model:** haiku
- **Tools:** Read, Write

---

### `task-intake`

> Use when the user wants to add a new task. Parses natural language task descriptions, fills structured fields, flags missing or unclear data, and appends to the task tracker. Triggers include phrases like "add a task", "new task", "I need to track", "log a task", or when the user describes work they need to do.

- **Model:** haiku
- **Tools:** Read, Write

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
