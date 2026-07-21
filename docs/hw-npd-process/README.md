# HW IoT Product Development — Process Documentation

Operating documentation derived from `IoT BP V3.6.xlsx` (Master Matrix). The workbook remains the single source of truth for **what** the tasks and RACI are; these documents cover **how the process runs** — sequence, parallelism, descriptions and approval artefacts.

## Deliverables

| Document | Contents |
|---|---|
| [01-swimlanes.md](01-swimlanes.md) | Swimlane flowcharts by role, one per lane (Full NPD split across two diagrams). All three gate outcomes drawn, including Kill. |
| [02-gantt-dependencies.md](02-gantt-dependencies.md) | Inferred dependency map, Gantt per lane sectioned by parallel track, and reconciliation against the workbook's own totals. |
| [03-process-descriptions.md](03-process-descriptions.md) | One entry per task: purpose, inputs, steps, exit criteria, RACI, lane differences, watch-outs. Plus roles, RACI rules, gate mechanics, change control and known limitations. |
| [04-approval-templates.md](04-approval-templates.md) | Gate submission documents for the 8 CEO gates — what the Responsible writes up and submits, with the approval block at the top for the Accountable. Follows the existing `HW DoE` house format. |
| [diagrams/](diagrams/) | Pre-rendered SVGs of all 12 diagrams, for decks and documents. |

## Regenerating after a workbook update

```bash
cd extract
python extract.py "/path/to/IoT BP V3.7.xlsx"   # → matrix.json
python schedule.py                               # → schedules, Gantt blocks, reconciliation
```

`extract.py` normalises the Master Matrix into `matrix.json`. `schedule.py` runs a forward pass over the dependency map it carries, prints the per-lane schedule and critical path, and can emit the Mermaid Gantt blocks used in deliverable 2.

**The dependency map lives in `schedule.py` (`DEPS`) and is documented in `02-gantt-dependencies.md` §2.1. Change both together.**

## Generating the diagram images

You usually do **not** need image files — Confluence renders the Mermaid blocks directly from the Markdown (see below), and so does GitHub. Generate images only when you need them for a slide deck, a Word document, a PDF or an email.

Pre-rendered SVGs are already in [`diagrams/`](diagrams/) — 8 swimlanes plus 4 Gantts. To regenerate them after editing a diagram:

```bash
cd docs/hw-npd-process/extract
npm install mermaid@11      # one-off, ~3 MB, local to this folder
python export_diagrams.py
```

It starts a local server, opens the page in your default browser, renders each diagram, and writes a standalone SVG per diagram into `diagrams/`. The browser tab closes itself out of the loop once it reports "Done". No headless-Chrome download is required.

**Need PNG instead of SVG?** Open the SVG in a browser and export, or use Inkscape (`inkscape in.svg -o out.png -w 2400`). SVG is preferred for decks and Confluence because it stays sharp at any zoom — several of these diagrams are 2,000–2,500 px tall and lose text detail when rasterised small.

**One-off edits** are fastest at [mermaid.live](https://mermaid.live): paste a single fenced block's contents, edit, then use Actions → PNG/SVG.

## Confluence

- Diagrams are Mermaid. Paste each fenced block into a **Mermaid macro** (Confluence Cloud: type `/mermaid`; Server/DC: install a Mermaid app such as Mermaid Diagrams for Confluence).
- Everything else is plain Markdown — headings, tables and `- [ ]` checkboxes convert on paste. No HTML and no nested tables anywhere, which is what keeps the paste clean.
- The eight approval templates are separated by `---` so each lifts cleanly into its own page. Save them as Confluence page templates for per-project reuse.

## Open items before this becomes a baseline

1. **Confirm the dependency map** (§2.1) line by line. It is inferred — the workbook has no predecessor column.
2. **Resolve note C**: can GATE 8 (T44) run before T43's 90 days of KPI data exist? This determines whether Full NPD is a 183-day or a 243-day programme.
3. **Re-baseline T14 SDPPI's 45-day estimate** with the regulatory contact. Float is 26 days on Full NPD, 16 on HW Upgrade.
4. **Decide note A**: should T19 PRD approval gate all of Stage 3, rather than sitting after 14 days of integration work?
5. **Decide note B**: should T30 depend on T28, so logistics readiness follows agreed Incoterms and MOQ?
