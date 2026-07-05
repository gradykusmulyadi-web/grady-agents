---
name: fireflies
description: Fetch and summarize a Fireflies.ai meeting transcript by ID, or list recent transcripts to pick from when no ID is given. Use when the user runs /fireflies, asks for a meeting summary, or wants to review a Fireflies recording.
---

# Fireflies meeting summary

## If `$ARGUMENTS` contains a transcript ID

Delegate immediately to the `fireflies-summarizer` subagent, passing the
transcript ID from `$ARGUMENTS`. Do not fetch or analyze the transcript
yourself in this context — the subagent owns that work.

## If `$ARGUMENTS` matches a partial meeting name (not a transcript ID)

1. Search transcripts from today back to at most 2 weeks ago — do not search
   further back than that window.
2. Match `$ARGUMENTS` against meeting titles within that window and take up
   to the 3 most recent matches, newest first.
3. Present the matches as a markdown table:

   ```
   | # | Title | Date (GMT+7) | Time (GMT+7) | Duration | Transcript ID |
   |---|-------|--------------|--------------|----------|----------------|
   | 1 | ...   | ...          | ...          | ...      | ...            |
   ```

4. If no matches are found in the 2-week window, say so and stop.
5. Stop here and wait for the user's reply. Do not proceed further in this
   turn.
6. Once the user replies with a pick (by index or by name), take that
   transcript's ID and delegate to the `fireflies-summarizer` subagent with
   that ID.

## If `$ARGUMENTS` is empty

1. Find the available tool whose name ends with `fireflies_get_transcripts`
   (it will be prefixed with an MCP namespace UUID) and call it with `limit=5`,
   `format="json"`.
2. Convert each transcript's date/time to GMT+7 and present them as a
   markdown table:

   ```
   | # | Title | Date (GMT+7) | Time (GMT+7) | Duration | Transcript ID |
   |---|-------|--------------|--------------|----------|----------------|
   | 1 | ...   | ...          | ...          | ...      | ...            |
   ```

3. After the table, add a line offering to show more, e.g.
   `Type "more" to see 10 more meetings.`
4. Stop here and wait for the user's reply. Do not proceed further in this
   turn.
5. If the user replies with "more" (or an equivalent request for
   additional meetings): re-call the same `fireflies_get_transcripts` tool
   with `limit` increased by 10 over the previous call (5 → 15 → 25 → 35 → ...),
   re-present the full table from the newest meeting, and repeat
   the "type more" offer in step 3. The user can keep requesting "more"
   indefinitely, each time growing the limit by another 10.
6. Once the user replies with a pick (by index or by name) instead of
   "more", take that transcript's ID and delegate to the
   `fireflies-summarizer` subagent with that ID.

In both cases, the actual fetch + full analysis always happens in the
`fireflies-summarizer` subagent, never inline here.

## Delegation rules (critical)

When spawning the `fireflies-summarizer` subagent:

- Pass **only the transcript ID** in the prompt — do not write a custom
  prompt that describes the output format or sections. The agent's own
  definition in `.claude/agents/fireflies-summarizer.md` owns the
  output structure, including the **Claude Observations** section.
- A custom inline prompt will silently override the agent definition and
  drop sections (e.g. Claude Observations). Never do this.
- Minimal prompt example: `"Summarize transcript ID: <id>"`
