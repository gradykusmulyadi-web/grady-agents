---
name: screen-cv
description: Orchestrates the CV screening pipeline. Sub-commands: setup (create job + build rubric), <job-id> (screen inbox CVs), feedback <job-id> (apply recruiter corrections).
---

You are the **screen-cv** skill orchestrator for McEasy's CV screening system.

Parse the user's input to determine the sub-command, then execute the steps below.

---

## Sub-command routing

| Input | Sub-command |
|-------|-------------|
| `/screen-cv setup` | → **SETUP** |
| `/screen-cv <job-id>` | → **SCREEN** |
| `/screen-cv feedback <job-id>` | → **FEEDBACK** |
| Anything else | → print usage and stop |

**Usage (print if no match):**
```
Usage:
  /screen-cv setup              — Create a new job folder and build its rubric
  /screen-cv <job-id>           — Screen all CVs in jobs/<job-id>/inbox/
  /screen-cv feedback <job-id>  — Apply recruiter corrections from the spreadsheet
```

---

## SETUP sub-command

**Goal:** scaffold a new job folder and produce an initial `rubric.md`.

### Steps

1. **Ask for the Job Description.**
   Say: "Please paste the full Job Description text now."
   Wait for the user to provide it.

2. **Suggest a job ID slug.**
   Extract the job title from the JD (first line or most prominent heading).
   Normalize: lowercase, replace spaces/punctuation with hyphens, strip special chars.
   Example: "Senior Backend Engineer – Logistics" → `senior-backend-engineer-logistics`
   Say: "Suggested job ID: `<slug>` — press Enter to accept, or type a different one."
   Wait for confirmation or override. Normalize whatever the user types.

3. **Guard: check for existing job folder.**
   If `jobs/<job_id>/` already exists, say:
   > "A folder for `<job_id>` already exists. To avoid overwriting it, I've stopped.
   > If you want to replace it, delete `jobs/<job_id>/` manually and re-run setup."
   Then stop.

4. **Scaffold the job folder.**
   - Copy structure from `jobs/_TEMPLATE/` to `jobs/<job_id>/`:
     - Create `jobs/<job_id>/inbox/`, `jobs/<job_id>/processed/`
     - Create empty `jobs/<job_id>/examples.md` with a header comment
     - Create empty `jobs/<job_id>/rubric.md` (placeholder — will be filled next)
   - Write the JD text to `jobs/<job_id>/job-description.md`.

5. **Run the rubric-builder agent.**
   Invoke the `rubric-builder` agent with `job_id` = `<job_id>`.
   The agent reads `job-description.md` and writes `rubric.md`.

6. **Human checkpoint.**
   After the agent finishes, say:
   > "Rubric written to `jobs/<job_id>/rubric.md`. **Please review and edit it before
   > running the first screening.** Pay special attention to:
   > - Must-haves (any `[RECRUITER: please clarify]` items)
   > - Nice-to-have weights (do the relative weights match your priorities?)
   > - Tier thresholds (are the cut-offs right for this role?)
   >
   > When you're ready to screen CVs, drop them in `jobs/<job_id>/inbox/` and run:
   > `/screen-cv <job_id>`"

---

## SCREEN sub-command

**Goal:** score every CV in `jobs/<job_id>/inbox/` and produce a ranked spreadsheet.

### Steps

1. **Guard: verify job folder exists.**
   If `jobs/<job_id>/` does not exist, say:
   > "No job folder found for `<job_id>`. Run `/screen-cv setup` first."
   Then stop.

2. **Guard: verify rubric exists and is not a placeholder.**
   Read `jobs/<job_id>/rubric.md`. If it is empty or still contains only a placeholder,
   warn the recruiter and ask them to complete the rubric before continuing.

3. **Discover CV files.**
   List all files in `jobs/<job_id>/inbox/`. Supported: `.pdf`, `.docx`, `.txt`.
   If the folder is empty, say so and stop.

4. **Extract text from each CV.**

   **PDF:** Use the Read tool directly — Claude can read PDF content.

   **DOCX:** Run:
   ```bash
   pandoc "<file>" -t plain --wrap=none 2>/dev/null || python3 -c "
   import sys
   from docx import Document
   doc = Document(sys.argv[1])
   print('\n'.join(p.text for p in doc.paragraphs))
   " "<file>"
   ```
   If both fail, note the file as "parse error" and continue with remaining CVs.

   **TXT:** Read directly.

   Extract candidate name from the top of each CV (first non-empty line, or line
   following "Name:"). Fall back to the filename stem if no name is detectable.

5. **Score each CV.**
   For each CV, invoke the `cv-screener` agent with:
   - `job_id`
   - `cv_file` (path)
   - `cv_text` (extracted text)
   - `candidate_name`

   Collect the JSON record returned by each screener invocation. Each record
   carries only **raw** judgments (must-have status, nice-to-have `raw`+`weight`,
   red flags) — it does **not** contain `tier` or `score_pct`.

6. **Compute tier and score deterministically (code, never by hand).**

   The percentage and tier are calculated by a script, not by the model, so the
   same CV always yields the same result. The fixed formula is:
   - `max possible weighted` = (sum of all nice-to-have weights) × 3
   - `score_pct` = achieved weighted ÷ max possible × 100
   - `tier` from the rubric thresholds, applied in strict precedence:
     `Not a fit` (2+ must-haves missing OR any disqualifying flag) →
     `Moderate fit` (1 missing OR a concern flag OR pct < 50) →
     `Best fit` (pct ≥ 80) → else `Good fit`.

   Write all collected records as a JSON array to `outputs/_records-<job_id>.json`,
   then run the scorer (it prints the enriched records, with `tier` + `score_pct`
   filled in, to stdout — capture them for the spreadsheet):

   ```bash
   # macOS / Linux (Python):
   python3 .claude/skills/screen-cv/score.py outputs/_records-<job_id>.json
   ```
   ```powershell
   # Windows (no Python needed):
   powershell -NoProfile -File .claude/skills/screen-cv/score.ps1 outputs/_records-<job_id>.json
   ```

   Use whichever runtime exists on the machine. **Never compute `tier` or
   `score_pct` yourself** — always take them from the scorer's output.

7. **Compile the spreadsheet.**

   Use the `xlsx` skill to produce `outputs/screening-<job_id>-<YYYY-MM-DD>.xlsx`.

   **Sheet: Results**

   Columns (in order):

   | Column | Source |
   |--------|--------|
   | Candidate name | `candidate_name` |
   | Source file | `source_file` |
   | Agent tier | `tier` |
   | Score % | `score_pct` |
   | Must-haves (summary) | comma-list of missing M-ids, or "All met" |
   | Strengths | joined from `strengths` array |
   | Gaps / Flags | joined from `gaps` array + any detected red flags |
   | Recommendation | `recommendation` |
   | Screener note | `screener_note` |
   | **Recruiter override tier** | *(blank — recruiter fills in)* |
   | **Recruiter feedback** | *(blank — recruiter fills in)* |

   **Formatting:**
   - Sort by `score_pct` descending.
   - Color-code the `Agent tier` column by tier:
     - Best fit → green (#C6EFCE)
     - Good fit → light green (#E2EFDA)
     - Moderate fit → yellow (#FFEB9C)
     - Not a fit → light red (#FFC7CE)
     - Parse error → grey (#D9D9D9)
   - Freeze the header row.
   - Auto-fit column widths.

8. **Move processed CVs.**
   Move all successfully screened files from `jobs/<job_id>/inbox/` to
   `jobs/<job_id>/processed/`. Leave parse-error files in inbox with a note.

9. **Summary.**
   Report: total CVs screened, breakdown by tier, output file path, and any
   parse errors to follow up on.

---

## FEEDBACK sub-command

**Goal:** incorporate recruiter corrections from the spreadsheet into rubric + examples.

### Steps

1. **Guard: verify job folder exists.**
   Same check as SCREEN step 1.

2. **Find the latest spreadsheet.**
   List `outputs/screening-<job_id>-*.xlsx`. Use the most recent by filename date.
   If none found, say:
   > "No screening output found for `<job_id>`. Run `/screen-cv <job_id>` first."
   Then stop.

3. **Run the feedback-learner agent.**
   Invoke `feedback-learner` with `job_id` and `spreadsheet_path`.
   The agent reads the spreadsheet, diffs tiers, and updates `rubric.md` and `examples.md`.

4. **Report.**
   Display the summary from the feedback-learner agent.
   Ask the recruiter: "Would you like to re-run screening now with the updated rubric?
   (yes = run `/screen-cv <job_id>` again; no = done for now)"

---

## Utility: normalize_slug

When normalizing a job ID:
```python
import re
slug = text.lower().strip()
slug = re.sub(r'[^a-z0-9]+', '-', slug)
slug = slug.strip('-')
```
Apply this to both suggested and user-supplied slugs before using them as folder names.
