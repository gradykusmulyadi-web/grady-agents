# grady-agents

This is Grady's personal Claude Code agents and skills repository for McEasy — a B2B SaaS telematics and logistics platform based in Indonesia.

## Repository Structure

```
grady-agents/
├── .claude/
│   ├── agents/               # Claude agent definitions (.md files with frontmatter)
│   │   └── iot-research.md
│   ├── skills/               # Reusable skill definitions
│   │   └── screen-cv/        # CV screening orchestrator (SKILL.md + deterministic scorers)
│   └── tasks/
│       └── tasks.md          # Personal task tracker (git-tracked)
├── jobs/                     # One folder per open position (screen-cv skill); _TEMPLATE scaffolds new ones
├── outputs/                  # Generated screening spreadsheets (git-ignored)
├── CLAUDE.md                 # This file
└── README.md
```

## Agents

Each agent lives in `.claude/agents/<agent-name>/` as a Markdown file with YAML frontmatter. The frontmatter defines the agent's name, description, model, and tools.

<!-- AGENTS-TABLE-START -->
| Agent | Model | Purpose |
|-------|-------|---------|
| `c-level-shield` | sonnet | Use after writer agent completes the PRD draft. Simulates hard questions from McEasy C-Level executives (CEO, COO, CFO, CTO, CBO, CDSO) and appends a Q&A section to the PRD. Protects the product owner from being caught off guard in real C-level reviews. |
| `cv-screener` | sonnet | Core CV screening engine. Reads a single CV file against the job rubric and examples, and emits a structured scoring record. Called in a loop by the /screen-cv skill for every file in inbox/. Recommended model: Sonnet. |
| `feedback-learner` | opus | Reads a recruiter-corrected screening spreadsheet, diffs agent tiers vs recruiter overrides, and updates rubric.md and examples.md to close the gap. Recommended model: Opus. |
| `fireflies-summarizer` | sonnet | Fetches a Fireflies.ai transcript by ID and produces a structured meeting summary — themes, decisions, action items, and a critical read. Invoke with a transcript ID. |
| `iot-research` | opus | Use when the user asks any question about the telematics or fleet management industry — market sizing, trends, vendor comparison, product specs, competitor intel, pricing, or regulation. Handles day-to-day research questions in a conversational way. Covers Indonesia and SEA as primary markets, with global context where relevant. Key vendors the user works with include Teltonika, BSJ, and Howen. |
| `rubric-builder` | opus | Converts a raw Job Description into a structured, editable rubric.md that the cv-screener agent uses for scoring. Run once per new position. Recommended model: Opus. |
| `task-daily-review` | sonnet | Use when the user wants to know what to work on today or this week. Reads all active tasks, prioritizes by urgency, and outputs a ranked table with reasoning. Triggers include "what should I work on today", "daily review", "weekly recap", "what's due this week", "task priority", "morning briefing", "what's on my plate". |
| `task-editor` | haiku | Use when the user wants to edit a task, update task fields, resolve flagged tasks, or mark a task as complete. Also use when the user says "show task editor" to render the full task list as an interactive UI. Triggers include "update task", "mark done", "fix flagged", "edit T003", "resolve flags", "show task editor", "task editor UI". |
| `task-intake` | haiku | Use when the user wants to add a new task. Parses natural language task descriptions, fills structured fields, flags missing or unclear data, and appends to the task tracker. Triggers include phrases like "add a task", "new task", "I need to track", "log a task", or when the user describes work they need to do. |
<!-- AGENTS-TABLE-END -->

## Skills

Skills live in `.claude/skills/` and are reusable prompt workflows invocable across agents or directly in Claude Code sessions.

| Skill | Purpose |
|-------|---------|
| `screen-cv` | Orchestrates the CV screening pipeline. Sub-commands: `setup` (scaffold a job folder + build its rubric via `rubric-builder`), `<job-id>` (screen every CV in `jobs/<job-id>/inbox/` via `cv-screener`, score deterministically, emit a ranked spreadsheet to `outputs/`), and `feedback <job-id>` (apply recruiter corrections via `feedback-learner`). Tier/score are computed by `score.py`/`score.ps1`, never by hand. |
| `fireflies` | The `/fireflies` slash command. Summarizes a Fireflies.ai meeting transcript: pass a transcript ID to summarize directly, a partial meeting name to search the last 2 weeks and pick, or nothing to list recent transcripts. Delegates all fetching/analysis to the `fireflies-summarizer` agent. |

## Conventions

- Agent files use YAML frontmatter (`name`, `description`, `model`, `tools`) followed by the system prompt in Markdown.
- Model choices: use `opus` for deep research agents, `sonnet` for general-purpose, `haiku` for fast/cheap tasks.
- Tools should be scoped to the minimum the agent needs — don't give every agent `Write` if it only reads.
- Primary market context for all agents: Indonesia / Southeast Asia / McEasy business domain.
