# 1. Swimlane Flowcharts — HW IoT Product Development

Source: `IoT BP V3.6.xlsx`, Master Matrix. Regenerate from `extract/matrix.json` when the workbook version changes.

## How to read these

- **Each swimlane column is a role** — specifically the **Responsible (R)** role, the one that does the work. Flow runs top to bottom.
- The **Accountable (A)** role — the one that signs and owns the outcome — is printed inside the node as `A: <role>`.
- **Gates** are hexagonal `{{ }}` nodes. Every gate has three outcomes, and all three are drawn:
  - solid edge forward = **Approve**
  - dashed edge backward = **Rework**, which returns to a named prior task with a written defect list
  - dashed edge to the red terminal = **Kill**
- Kill is drawn as a real path on purpose. The governance rules state that killing early is the point of gates and is a success outcome, not a failure. A diagram that only shows the happy path teaches the opposite.
- Duration in working days is shown as `(5d)`.
- Deferred tasks (T31 warranty/RMA, T32 OTA lifecycle) are not drawn — they are `Status = Deferred` in the workbook. See deliverable 3.

**Diagram sizing.** Each diagram is split so it renders legibly in a standard Confluence content column (roughly 1,300–2,000 px wide). Long lanes are split by stage rather than compressed into one unreadable chart. Every task in a lane appears exactly once across that lane's diagrams.

**Confluence:** paste each fenced block into a Mermaid macro. See `README.md`.

---

## 1.1 Full NPD — Stage 0 to Stage 2 (Opportunity → Design Freeze → Cost Checkpoint)

New hardware platform, new product category, or first engagement with an unproven vendor. This section runs T01–T15 and ends at the landed-cost kill trigger — the last cheap exit before integration spend starts.

```mermaid
flowchart TB
  classDef gate fill:#fff4e5,stroke:#d97706,stroke-width:2px
  classDef kill fill:#fee2e2,stroke:#dc2626,stroke-width:2px

  subgraph PO["IoT Product Owner"]
    T01["T01 Draft business case (5d)<br/>A: CEO"]
    T02{{"T02 GATE 1<br/>Business Case Approval (3d)<br/>A: CEO"}}
    T04["T04 Create L1 Requirement (7d)<br/>incl. BOM cost + margin envelope<br/>A: CEO"]
    T05{{"T05 GATE 2<br/>L1 Requirement Approval (3d)<br/>A: CEO"}}
    T06["T06 Source vendors (7d)<br/>min 3 quoted<br/>A: Procurement"]
    T14["T14 SDPPI certification (45d)<br/>PARALLEL<br/>A: Procurement"]
  end

  subgraph PR["Procurement"]
    T07["T07 Vendor qualification (3d)<br/>A: IoT Product Owner"]
    T08["T08 Procure samples (10d)<br/>A: IoT Product Owner"]
    T15{{"T15 GATE<br/>Cost checkpoint (2d)<br/>landed BOM vs margin<br/>A: Finance"}}
  end

  subgraph ENG["IoT Engineer"]
    T09["T09 L2 + functional test cases (7d)<br/>A: IoT Product Owner"]
    T10["T10 Execute functional test (3d)<br/>A: IoT Engineer (R/A)"]
    T11{{"T11 GATE 3<br/>Functional test approval (3d)<br/>A: CEO"}}
    T12["T12 Execute robustness test (7d)<br/>A: IoT Engineer (R/A)"]
    T13{{"T13 GATE 4<br/>Robustness approval (3d)<br/>DESIGN FREEZE<br/>A: CEO"}}
  end

  KILL(["Kill / documented stop<br/>reason + sunk cost recorded"])
  NEXT(["→ Stage 3 Integration<br/>see 1.2"])

  T01 --> T02
  T02 -->|Approve| T04
  T02 -.->|Rework| T01
  T02 -.->|Kill| KILL

  T04 --> T05
  T05 -->|Approve| T06
  T05 -.->|Rework| T04
  T05 -.->|Kill| KILL

  T06 --> T07 --> T08 --> T09 --> T10 --> T11
  T11 -->|Approve| T12
  T11 -.->|Rework| T10
  T11 -.->|Kill| KILL

  T12 --> T13
  T13 -->|Approve| T15
  T13 -->|Design freeze triggers| T14
  T13 -.->|Rework| T12
  T13 -.->|Kill| KILL

  T15 -->|Proceed| NEXT
  T15 -.->|Renegotiate| T06
  T15 -.->|Kill| KILL
  T14 -.->|feeds T35 blocker check| NEXT

  class T02,T05,T11,T13,T15 gate
  class KILL kill
```

**Two things this diagram is meant to make obvious:**

1. **T14 certification branches at design freeze, not later.** SDPPI/Postel is 45 days of fixed external queue time that cannot be compressed by adding people. It cannot start before T13, because certification covers a specific frozen hardware configuration — any change means re-certifying. T13 is therefore the earliest safe start, and starting it there keeps it off the critical path.
2. **T15 sits before Stage 3, not inside it.** Integration is the most expensive phase (Kernel Engineer + SW Engineering + SW Product all engaged). Testing the economics at ~day 63 instead of ~day 150 is the entire reason this task exists.

---

## 1.2 Full NPD — Stage 3 & 4 (Integration → PoC)

```mermaid
flowchart TB
  classDef gate fill:#fff4e5,stroke:#d97706,stroke-width:2px
  classDef kill fill:#fee2e2,stroke:#dc2626,stroke-width:2px

  START(["from T15 Cost checkpoint"])

  subgraph ENG["IoT Engineer"]
    T16["T16 Create integration contract (3d)<br/>A: SW Product"]
    T17["T17 Present contract to SW team (3d)<br/>A: SW Product"]
  end

  subgraph KE["Kernel Engineer"]
    T18["T18 Integrate data to MEP Server (14d)<br/>A: SW Engineering"]
  end

  subgraph SWP["SW Product"]
    T19{{"T19 GATE<br/>PRD Approval (3d)<br/>A: CTO"}}
    T20["T20 Develop platform functions (7d)<br/>Live View, Report, Dashboard<br/>A: SW Engineering"]
    T21{{"T21 GATE<br/>SW QC approval, JIRA (3d)<br/>A: SW Engineering"}}
    T22{{"T22 GATE<br/>Integration test approval (3d)<br/>R: Kernel Eng + SW Product<br/>A: IoT Engineer"}}
  end

  subgraph PO["IoT Product Owner"]
    T23["T23 Run product final UAT (3d)<br/>A: IoT Product Owner (R/A)"]
    T24{{"T24 GATE 5<br/>Final UAT vs L1 (3d)<br/>A: CEO"}}
    T25["T25 Define PoC plan (3d)<br/>min 3 sites, signed agreement<br/>A: CEO"]
    T26["T26 Run PoC on customer sites (21d)<br/>A: CEO"]
    T27{{"T27 GATE 6<br/>PoC Go / No-Go (3d)<br/>last cheap exit<br/>A: CEO"}}
  end

  KILL(["Kill / documented stop"])
  NEXT(["→ Stage 5 Pre-Comm<br/>see 1.3"])

  START --> T16 --> T17 --> T18 --> T19
  T19 -->|Approve| T20
  T19 -.->|Rework - revise PRD| T19

  T20 --> T21
  T21 -->|Approve| T22
  T21 -.->|Rework| T20

  T22 -->|Approve| T23
  T22 -.->|Rework| T18

  T23 --> T24
  T24 -->|Approve| T25
  T24 -.->|Rework| T22
  T24 -.->|Kill| KILL

  T25 --> T26 --> T27
  T27 -->|Approve| NEXT
  T27 -.->|Rework| T26
  T27 -.->|Kill| KILL
  T25 -.->|parallel tracks branch here| NEXT

  class T19,T21,T22,T24,T27 gate
  class KILL kill
```

**T27 is the last cheap exit.** Everything after it involves stock commitment, executed contracts and public announcements.

---

## 1.3 Full NPD — Stage 5 to Stage 7 (Pre-Comm → Post-Comm)

The three parallel tracks (Commercial, Service, Supply) branch from T25 and run alongside the PoC, which is why they appear here with start points earlier than the main chain.

```mermaid
flowchart TB
  classDef gate fill:#fff4e5,stroke:#d97706,stroke-width:2px
  classDef kill fill:#fee2e2,stroke:#dc2626,stroke-width:2px

  START(["from T25 PoC plan (parallel tracks)<br/>and T27 PoC Go/No-Go (main)"])

  subgraph PR["Procurement"]
    T28["T28 Finalise vendor agreement (7d)<br/>PARALLEL - Commercial<br/>A: Procurement (R/A)"]
    T30["T30 Manufacturing + logistics readiness (10d)<br/>PARALLEL - Supply<br/>A: IoT Engineer"]
    T38["T38 Pre-order initial stock (3d)<br/>A: Finance"]
  end

  subgraph ENG["IoT Engineer"]
    T29["T29 Prepare SOP, WI, QC parameters (7d)<br/>PARALLEL - Service<br/>A: Head of Service"]
    T42["T42 Review installation quality (30d)<br/>first 20-50 installs<br/>A: Head of Service"]
  end

  subgraph AE["Application Engineer"]
    T33{{"T33 GATE<br/>Train Service Leader BAST (3d)<br/>+ certify installers<br/>A: Head of Service"}}
  end

  subgraph HOS["Head of Service"]
    T34["T34 Support readiness (5d)<br/>PARALLEL - Service<br/>A: Application Engineer"]
  end

  subgraph PO["IoT Product Owner"]
    T35{{"T35 Confirm SDPPI received (2d)<br/>HARD BLOCKER<br/>A: Procurement"}}
    T36{{"T36 GATE 7<br/>Pricing + Packaging (3d)<br/>A: CEO"}}
    T37["T37 Present commercialization deck (3d)<br/>A: IoT Product Owner (R/A)"]
    T39["T39 Monthly Product Demo (3d)<br/>PARALLEL - Commercial<br/>A: IoT Product Owner (R/A)"]
    T43["T43 Track KPIs 30/60/90 (90d)<br/>A: IoT Product Owner (R/A)"]
    T44{{"T44 GATE 8<br/>3-month post-release review (3d)<br/>A: CEO"}}
    T45["T45 Annual lifecycle + EOL review (5d)<br/>A: CEO"]
  end

  subgraph COM["Commercial (CBO / Mktg)"]
    T40["T40 Launch external communication (14d)<br/>PARALLEL - Commercial<br/>A: IoT Product Owner"]
    T41["T41 Sales enablement ready (7d)<br/>LAUNCH MILESTONE<br/>A: IoT Product Owner"]
  end

  HOLD(["Launch blocked<br/>no legal right to sell"])
  SUNSET(["Sunset<br/>EOL + migration plan"])

  START --> T28
  START --> T29
  START --> T30
  START --> T35

  T29 --> T33
  T33 -->|Approve| T34
  T33 -.->|Rework| T29

  T35 -->|Certificate in hand| T36
  T35 -.->|Not received - HOLD| HOLD

  T36 -->|Approve| T37
  T36 -.->|Rework - re-price| T36
  T36 -.->|parallel| T39

  T37 --> T38
  T30 --> T38
  T38 --> T41
  T38 -.->|parallel| T40

  T41 --> T42
  T41 --> T43
  T42 --> T44
  T43 --> T44
  T44 -->|Scale| T45
  T44 -.->|Fix| T42
  T44 -.->|Sunset| SUNSET

  class T33,T35,T36,T44 gate
  class HOLD,SUNSET kill
```

**Note on T35.** This is not a normal gate — it is a blocker check with no rework path. Either the certificate is in hand or the product cannot legally be sold. If T14 slipped, this is where you find out, and by then stock is about to be ordered and installers are already trained. That is the failure mode the early-certification move was designed to prevent.

---

## 1.4 New Vendor / HW Upgrade — Stage 0 to Stage 2

Existing category, new supplier or revised hardware revision. **Reuses the original L1 and L2 and their test cases** — no new requirement authoring (T04, T05, T09 are absent). Keeps certification, vendor qualification and the full test execution, because a different supplier's hardware is genuinely unproven even in a known category.

31 tasks in total, 146 critical-path days.

```mermaid
flowchart TB
  classDef gate fill:#fff4e5,stroke:#d97706,stroke-width:2px
  classDef kill fill:#fee2e2,stroke:#dc2626,stroke-width:2px

  subgraph PO["IoT Product Owner"]
    T01["T01 Draft business case (5d)<br/>A: CEO"]
    T02{{"T02 GATE 1<br/>Business Case Approval (3d)<br/>A: CEO"}}
    T06["T06 Source vendors (7d)<br/>min 3 quoted<br/>A: Procurement"]
    T14["T14 SDPPI certification (45d)<br/>PARALLEL<br/>A: Procurement"]
  end

  subgraph PR["Procurement"]
    T07["T07 Vendor qualification (3d)<br/>A: IoT Product Owner"]
    T08["T08 Procure samples (10d)<br/>A: IoT Product Owner"]
    T15{{"T15 GATE<br/>Cost checkpoint (2d)<br/>vs ORIGINAL margin envelope<br/>A: Finance"}}
  end

  subgraph ENG["IoT Engineer"]
    T10["T10 Execute EXISTING test cases (3d)<br/>A: IoT Engineer (R/A)"]
    T11{{"T11 GATE 3<br/>Functional test approval (3d)<br/>A: CEO"}}
    T12["T12 Execute robustness test (7d)<br/>A: IoT Engineer (R/A)"]
    T13{{"T13 GATE 4<br/>Robustness approval (3d)<br/>DESIGN FREEZE<br/>A: CEO"}}
  end

  KILL(["Kill / documented stop"])
  NEXT(["→ Stage 3 onward<br/>see 1.5"])

  T01 --> T02
  T02 -->|Approve| T06
  T02 -.->|Rework| T01
  T02 -.->|Kill| KILL

  T06 --> T07 --> T08 --> T10 --> T11
  T11 -->|Approve| T12
  T11 -.->|Rework| T10
  T11 -.->|Kill| KILL

  T12 --> T13
  T13 -->|Approve| T15
  T13 -->|Design freeze| T14
  T13 -.->|Rework| T12
  T13 -.->|Kill| KILL

  T15 -->|Proceed| NEXT
  T15 -.->|Renegotiate| T06
  T15 -.->|Kill| KILL
  T14 --> NEXT

  class T02,T11,T13,T15 gate
  class KILL kill
```

---

## 1.5 New Vendor / HW Upgrade — Stage 3 & 4 (Integration → PoC)

```mermaid
flowchart TB
  classDef gate fill:#fff4e5,stroke:#d97706,stroke-width:2px
  classDef kill fill:#fee2e2,stroke:#dc2626,stroke-width:2px

  START(["from T15 Cost checkpoint"])

  subgraph ENG["IoT Engineer"]
    T16["T16 Create integration contract (3d)<br/>A: SW Product"]
    T17["T17 Present contract to SW team (3d)<br/>A: SW Product"]
  end

  subgraph KE["Kernel Engineer"]
    T18["T18 Integrate data to MEP Server (14d)<br/>A: SW Engineering"]
  end

  subgraph SWP["SW Product"]
    T21{{"T21 GATE<br/>SW QC approval, JIRA (3d)<br/>A: SW Engineering"}}
    T22{{"T22 GATE<br/>Integration test approval (3d)<br/>A: IoT Engineer"}}
  end

  subgraph PO["IoT Product Owner"]
    T23["T23 Run product final UAT (3d)<br/>A: IoT Product Owner (R/A)"]
    T24{{"T24 GATE 5<br/>Final UAT vs ORIGINAL L1 (3d)<br/>A: CEO"}}
    T25["T25 Define PoC plan (3d)<br/>A: CEO"]
    T26["T26 Run PoC, min 3 sites (21d)<br/>A: CEO"]
    T27{{"T27 GATE 6<br/>PoC Go / No-Go (3d)<br/>A: CEO"}}
  end

  KILL(["Kill / documented stop"])
  NEXT(["→ Stage 5 onward<br/>see 1.6"])

  START --> T16 --> T17 --> T18 --> T21
  T21 -->|Approve| T22
  T21 -.->|Rework| T18
  T22 -->|Approve| T23
  T22 -.->|Rework| T18

  T23 --> T24
  T24 -->|Approve| T25
  T24 -.->|Rework| T22
  T24 -.->|Kill| KILL

  T25 --> T26 --> T27
  T27 -->|Approve| NEXT
  T27 -.->|Rework| T26
  T27 -.->|Kill| KILL
  T25 -.->|parallel tracks branch here| NEXT

  class T21,T22,T24,T27 gate
  class KILL kill
```

---

## 1.6 New Vendor / HW Upgrade — Stage 5 to Stage 7

```mermaid
flowchart TB
  classDef gate fill:#fff4e5,stroke:#d97706,stroke-width:2px
  classDef kill fill:#fee2e2,stroke:#dc2626,stroke-width:2px

  START(["from T25 PoC plan (parallel tracks)<br/>and T27 PoC Go/No-Go (main)"])

  subgraph PR["Procurement"]
    T28["T28 Finalise vendor agreement (7d)<br/>PARALLEL - Commercial<br/>A: Procurement (R/A)"]
    T30["T30 Manufacturing + logistics readiness (10d)<br/>PARALLEL - Supply<br/>A: IoT Engineer"]
    T38["T38 Pre-order initial stock (3d)<br/>LAUNCH MILESTONE<br/>A: Finance"]
  end

  subgraph ENG["IoT Engineer"]
    T29["T29 Prepare SOP, WI, QC parameters (7d)<br/>PARALLEL - Service<br/>A: Head of Service"]
    T42["T42 Review installation quality (30d)<br/>A: Head of Service"]
  end

  subgraph AE["Application Engineer"]
    T33{{"T33 GATE<br/>Train Service Leader BAST (3d)<br/>+ certify installers<br/>A: Head of Service"}}
  end

  subgraph PO["IoT Product Owner"]
    T35{{"T35 Confirm SDPPI received (2d)<br/>HARD BLOCKER<br/>A: Procurement"}}
    T36{{"T36 GATE 7<br/>Pricing + Packaging (3d)<br/>A: CEO"}}
    T43["T43 Track KPIs vs original L1 (90d)<br/>A: IoT Product Owner (R/A)"]
    T44{{"T44 GATE 8<br/>3-month post-release review (3d)<br/>A: CEO"}}
  end

  HOLD(["Launch blocked<br/>no legal right to sell"])

  START --> T28
  START --> T29
  START --> T30
  START --> T35

  T29 --> T33

  T35 -->|Certificate in hand| T36
  T35 -.->|Not received - HOLD| HOLD

  T36 --> T38
  T30 --> T38
  T38 --> T42
  T38 --> T43
  T42 --> T44
  T43 --> T44
  T44 -.->|Fix| T42

  class T33,T35,T36,T44 gate
  class HOLD kill
```

**Note.** There is no T19 PRD gate and no T20 platform development in this lane — a vendor swap should not require new platform features. If a proposed HW upgrade *does* require them, the change spans two lanes and the routing rule says take the heavier lane: run Full NPD. Also absent: T34 support readiness, T37, T39, T40, T41, T45.

**Worth questioning:** T34 (support readiness) is absent from this lane, yet a new supplier's hardware may fail in ways the existing support runbook does not cover.

---

## 1.7 FW Upgrade lane

Firmware change to devices already in the field. Needs an L1 requirement and CEO sign-off, then integration and acceptance. No L2 authoring, no procurement, no certification.

11 tasks, 39 critical-path days.

```mermaid
flowchart TB
  classDef gate fill:#fff4e5,stroke:#d97706,stroke-width:2px
  classDef kill fill:#fee2e2,stroke:#dc2626,stroke-width:2px
  classDef risk fill:#fee2e2,stroke:#dc2626,stroke-dasharray:5 5

  subgraph PO["IoT Product Owner"]
    T04["T04 Create L1 Requirement (7d)<br/>A: CEO"]
    T05{{"T05 GATE 2<br/>L1 Requirement Approval (3d)<br/>A: CEO"}}
    T23["T23 Run product final UAT (3d)<br/>A: IoT Product Owner (R/A)"]
    T24{{"T24 GATE 5<br/>Final UAT approval (3d)<br/>A: CEO"}}
    T39["T39 Monthly Product Demo (3d)<br/>PARALLEL - Commercial<br/>A: IoT Product Owner (R/A)"]
    T43["T43 Track KPIs (90d)<br/>A: IoT Product Owner (R/A)"]
  end

  subgraph ENG["IoT Engineer"]
    T16["T16 Create integration contract (3d)<br/>A: SW Product"]
  end

  subgraph KE["Kernel Engineer"]
    T18["T18 Integrate data to MEP Server (14d)<br/>A: SW Engineering"]
  end

  subgraph SWP["SW Product"]
    T21{{"T21 GATE<br/>SW QC approval, JIRA (3d)<br/>A: SW Engineering"}}
    T22{{"T22 GATE<br/>Integration test approval (3d)<br/>A: IoT Engineer"}}
  end

  subgraph HOS["Head of Service"]
    T34["T34 Support readiness (5d)<br/>PARALLEL - Service<br/>A: Application Engineer"]
  end

  GAP["NO STAGED ROLLOUT STEP<br/>OTA lifecycle policy is Deferred -<br/>a bad release reaches the whole fleet at once"]
  KILL(["Kill / documented stop"])

  T04 --> T05
  T05 -->|Approve| T16
  T05 -.->|Rework| T04
  T05 -.->|Kill| KILL

  T16 --> T18 --> T21
  T21 -->|Approve| T22
  T21 -.->|Rework| T18
  T22 -->|Approve| T23
  T22 -.->|Rework| T18

  T23 --> T24
  T24 -->|Approve| GAP
  T24 -.->|Rework| T22
  T24 -.->|Kill| KILL
  GAP --> T34 --> T39 --> T43

  class T05,T21,T22,T24 gate
  class KILL kill
  class GAP risk
```

**The gap is drawn deliberately.** T32 (OTA / firmware lifecycle policy — versioning, 5%/25%/100% staged rollout, rollback procedure, fleet FW compliance tracking) is marked `Deferred` in the workbook, and this is the one lane where that deferral has teeth. A firmware release currently goes from CEO UAT approval straight to the whole installed base with no rollback procedure. This is the highest-severity known gap in the process and worth closing before the first at-scale OTA.

---

## 1.8 New SW Feature lane

Platform-side feature on existing hardware. Starts at L2, and — unusually — **the HW team runs functional testing first**. Only once the CEO approves that result does SW Product write the PRD and start the build.

13 tasks, 39 critical-path days.

```mermaid
flowchart TB
  classDef gate fill:#fff4e5,stroke:#d97706,stroke-width:2px
  classDef kill fill:#fee2e2,stroke:#dc2626,stroke-width:2px
  classDef risk fill:#fee2e2,stroke:#dc2626,stroke-dasharray:5 5

  subgraph ENG["IoT Engineer"]
    T09["T09 Update EXISTING L2 (7d)<br/>+ functional test cases<br/>A: IoT Product Owner"]
    T10["T10 Execute functional test (3d)<br/>runs BEFORE any software build<br/>A: IoT Engineer (R/A)"]
    T11{{"T11 GATE 3<br/>Functional test approval (3d)<br/>gates the software build<br/>A: CEO"}}
  end

  subgraph SWP["SW Product"]
    T19{{"T19 GATE<br/>PRD Approval (3d)<br/>A: CTO"}}
    T20["T20 Develop platform functions (7d)<br/>A: SW Engineering"]
    T21{{"T21 GATE<br/>SW QC approval, JIRA (3d)<br/>A: SW Engineering"}}
  end

  subgraph PO["IoT Product Owner"]
    T23["T23 Run product final UAT (3d)<br/>A: IoT Product Owner (R/A)"]
    T24{{"T24 GATE 5<br/>Final UAT vs L2 (3d)<br/>A: CEO"}}
    T39["T39 Monthly Product Demo (3d)<br/>PARALLEL - Commercial<br/>A: IoT Product Owner (R/A)"]
    T43["T43 Track KPIs (90d)<br/>qualitative in this lane<br/>A: IoT Product Owner (R/A)"]
  end

  subgraph HOS["Head of Service"]
    T34["T34 Support readiness (5d)<br/>PARALLEL - Service<br/>A: Application Engineer"]
  end

  subgraph COM["Commercial (CBO / Mktg)"]
    T40["T40 Launch external communication (14d)<br/>PARALLEL - Commercial<br/>A: IoT Product Owner"]
    T41["T41 Sales enablement ready (7d)<br/>A: IoT Product Owner"]
  end

  KILL(["Kill / documented stop"])
  NOGATE["NO post-release review gate in this lane<br/>and no L1, so no KPI baseline"]

  T09 --> T10 --> T11
  T11 -->|Approve| T19
  T11 -.->|Rework| T10
  T11 -.->|Kill| KILL

  T19 -->|Approve| T20
  T19 -.->|Rework - revise PRD| T19

  T20 --> T21
  T21 -->|Approve| T23
  T21 -.->|Rework| T20

  T23 --> T24
  T24 -->|Approve| T34
  T24 -.->|Rework| T20
  T24 -.->|Kill| KILL
  T24 -.->|parallel| T39
  T24 -.->|parallel| T40

  T34 --> T41 --> T43 --> NOGATE

  class T11,T19,T21,T24 gate
  class KILL kill
  class NOGATE risk
```

**The ordering here is the point of the lane.** T11 gates the software build: no PRD is written and no development starts until the hardware functional result passes. That inverts the usual instinct to start the build while testing proceeds, and it exists so platform effort is never spent against hardware behaviour that has not been proven.

**Two known limitations in this lane**, both flagged in the workbook's own Read Me: the lane carries no L1, so no success KPIs are set and T43 tracking is qualitative; and there is no post-release review gate, so a shipped SW feature is never formally reviewed against targets.

---

## Cross-lane observations

**The CEO is Accountable on 8 of the 14 gates** (T02, T05, T11, T13, T24, T27, T36, T44). Read across all eight diagrams and CEO calendar availability is effectively the critical path for the whole programme. The 3-working-day SLA and the named-standing-delegate rule are the only forcing functions preventing the BP V3 bottleneck — where 33 of 170 days were signature-waiting — from returning. They are load-bearing, not administrative.

**Self-certification remains on the HW test path.** T10 and T12 are both `R/A = IoT Engineer` — the same person executes the test and owns the result. QA/QC appears only as Consulted on T21 (software QC). The mitigation is that the CEO signs the two acceptance gates T11 and T13, but the CEO is not independently verifying test data. This is a known, accepted design choice; it is recorded here so it stays a decision rather than becoming an assumption.

**No security or privacy review appears in any lane.** Firmware signing, secure boot, OTA authentication and PII handling for location data are not covered anywhere in this process.
