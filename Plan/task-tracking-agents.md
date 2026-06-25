# Task Tracking Agent System — Plan

## Context

Grady needs a lightweight personal task tracking system inside Claude Code. Tasks come from various stakeholders at McEasy and have structured metadata. Three agents handle the full lifecycle: intake → flag resolution/editing → daily/weekly prioritization.

---

## Storage

**File:** `.claude/tasks/tasks.md`

A markdown table with one row per task. Git-tracked, readable by all three agents.

### Schema (columns)

| Field | Notes |
|---|---|
| ID | Auto-incremented (T001, T002...) |
| Name | Task title |
| Requested By | Stakeholder who asked for it |
| Collaborators | Who Grady works with on this |
| Due Date | YYYY-MM-DD or "TBD" |
| Detail | 1-3 sentence description |
| Priority | P0 / P1 / P2 |
| Type | Strategy / IoT / Others |
| Status | `Active` / `Done` / `Flagged` |
| Flag Notes | What field(s) are unclear — blank if clean |
| Created | YYYY-MM-DD |

### Priority definitions

| Priority | Meaning |
|---|---|
| P0 | Urgent / time-critical / blocking |
| P1 | Important, has a specific due date |
| P2 | Backlog — no time commitment yet |

---

## Agents

### 1. `task-intake` — Receive and parse new tasks

**Model:** `haiku` (structured extraction — fast and cheap)
**Tools:** `Read`, `Write`

**Trigger:** User describes a task in natural language (or pastes notes/meeting output).

**Behavior:**
- Parse the input and map to each schema field.
- If a field is confidently inferred, populate it.
- If a field is missing or ambiguous, set Status = `Flagged` and write the issue in Flag Notes.
- Append the row to `.claude/tasks/tasks.md`.
- Confirm back to user: show the parsed task as a table row, highlight flagged fields in bold.

**Priority inference rules:**
- P0: user says "urgent", "ASAP", "blocking", or due date ≤ 3 days
- P1: has a specific due date more than 3 days out
- P2: no due date, or user says "backlog" / "someday"

---

### 2. `task-editor` — Edit tasks, resolve flags, mark complete

**Model:** `haiku`
**Tools:** `Read`, `Write`

**Trigger:** User wants to update a field, resolve flagged tasks, mark a task done, or view the interactive UI.

**Behavior — Conversational mode (default):**
- **Flag resolution:** Filter Status = `Flagged`, surface Flag Notes, ask targeted follow-ups, update row and clear flag.
- **Field update:** User says "update T003 due date to July 10" — agent finds the row, shows current value, confirms the change, writes it.
- **Mark complete:** User says "mark T003 done" — agent shows full task detail and asks "Confirm marking [task name] as Done?" before writing Status = `Done`.
- All write operations include a confirmation step before saving.

**Behavior — UI mode (triggered by "show task editor"):**
- Agent reads tasks.md and returns all Active + Flagged tasks as a structured `TASK_EDITOR_UI_DATA` JSON block.
- Main Claude Code session renders an interactive HTML widget using `show_widget`:
  - Inline-editable fields (click to edit)
  - Priority and status badges that cycle on click
  - Save button per row — calls `sendPrompt()` with a structured update command
  - The update command is then handled by `task-editor` in conversational mode

---

### 3. `task-daily-review` — Daily and weekly work prioritization

**Model:** `sonnet` (needs date math and nuanced prioritization reasoning)
**Tools:** `Read`

**Trigger:** User asks what to work on today or this week.

**Behavior:**
- Read `.claude/tasks/tasks.md`, filter Status = `Active` and `Flagged`.
- Rank by: P0 first → overdue → due within 3 days → due within 7 days → P1 beyond 7 days → P2 backlog.
- Output a prioritized table with a "Why Now" reasoning column per row.
- Weekly mode: show all tasks due within 7 days + any P0s regardless of date.
- Surface overdue tasks explicitly.

---

## Files Created

| File | Purpose |
|---|---|
| `.claude/agents/task-intake.md` | Agent definition + system prompt |
| `.claude/agents/task-editor.md` | Agent definition + system prompt |
| `.claude/agents/task-daily-review.md` | Agent definition + system prompt |
| `.claude/tasks/tasks.md` | Task storage (markdown table, git-tracked) |

---

## How to Invoke

| Action | How |
|---|---|
| Add a task | Describe it in natural language → routes to `task-intake` |
| Edit a task | "update T003 ..." → routes to `task-editor` |
| Mark done | "mark T001 done" → routes to `task-editor` |
| Fix flagged tasks | "fix flagged tasks" → routes to `task-editor` |
| View interactive UI | "show task editor" → `task-editor` returns JSON → main session renders widget |
| Daily focus | "what should I work on today?" → routes to `task-daily-review` |
| Weekly recap | "weekly recap" → routes to `task-daily-review` |

You can also explicitly call agents with `@agent-name`.

---

## Verification

1. Run `task-intake` with a realistic task description — confirm it parses and saves correctly.
2. Give a vague task (no due date, no collaborator) — confirm it saves as `Flagged` with correct Flag Notes.
3. Run `task-editor` — confirm it surfaces flagged rows and saves updates correctly.
4. Run `task-daily-review` — confirm P0 before P1, earlier due dates first, reasoning column is accurate.
