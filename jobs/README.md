# Recruiter Workflow

## Quick start (new position)

1. Run `/screen-cv setup`
2. Paste the Job Description when prompted
3. Confirm or override the suggested job ID slug
4. **Review and edit** `jobs/<job-id>/rubric.md` — especially any `[RECRUITER: please clarify]` items
5. Drop CVs (PDF or DOCX) into `jobs/<job-id>/inbox/`
6. Run `/screen-cv <job-id>`
7. Open `outputs/screening-<job-id>-<date>.xlsx`

## Giving feedback (learning loop)

1. In the spreadsheet, fill in `Recruiter override tier` where the agent got it wrong
2. Optionally add a note in `Recruiter feedback` explaining why
3. Run `/screen-cv feedback <job-id>`
4. Review the rubric changes the agent proposes, then re-run screening if needed

## Folder structure

```
jobs/
  _TEMPLATE/          # Master template — do not edit directly
  <job-id>/
    job-description.md   ← raw JD (written by setup)
    rubric.md            ← scoring rubric (agent-generated, recruiter-edited)
    examples.md          ← calibration examples (appended by feedback loop)
    inbox/               ← drop CVs here before running /screen-cv <job-id>
    processed/           ← CVs move here after screening (keep for audit trail)
```

## Important notes

- **The agent ranks and explains — you decide.** Never treat a "Not a fit" tier as an auto-rejection.
- **CVs are personal data.** Keep them local. Do not share the `inbox/` or `processed/` folders outside the hiring team.
- **Audit trail:** keep `processed/` files and output spreadsheets until the position is closed + 30 days (or per your HR retention policy).
- If you need to re-screen the same CVs (e.g. after a rubric update), move them back from `processed/` to `inbox/` manually.
