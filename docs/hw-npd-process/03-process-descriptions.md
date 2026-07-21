# 3. Process Descriptions

Source: `IoT BP V3.6.xlsx`, Master Matrix. Deliverable / exit criteria are quoted verbatim from the workbook; purpose, inputs and steps are written for this document.

Day numbers in each entry refer to the **Full NPD** schedule computed in deliverable 2 and are indicative, not commitments.

---

## Roles

| Role | Scope |
|---|---|
| **CEO** | Accountable on 8 gates. A named standing delegate is mandatory. |
| **CTO** | Approves the platform PRD (T19) before development starts. New in V6. |
| **IoT Product Owner** | Owns the product end to end — business case, L1 requirement, PoC, pricing, launch, KPI tracking. Responsible on every CEO gate. |
| **IoT Engineer** | HW engineering, test execution and acceptance, SOP and QC parameters, install quality review. Accountable for the integration test (T22). |
| **Application Engineer** | Field application, installer training and certification, support escalation. |
| **Kernel Engineer** | Device-to-platform data integration and firmware. |
| **SW Product** | Platform product definition, PRD authoring, platform feature delivery. |
| **SW Engineering** | Platform engineering delivery and SW QC. |
| **QA / QC** | Consulted on SW QC approval (T21) only. |
| **Procurement** | Vendor sourcing, qualification, contracting, stock and logistics. Also owns SDPPI certification (T14, T35) and vendor contract sign-off (T28), since there is no legal function. |
| **Finance** | Business case validation, landed-cost checkpoint, margin envelope, stock PO. |
| **Head of Service** | Service readiness, training, support runbook, field quality. |
| **Commercial (CBO / Mktg)** | Pricing input, packaging, launch communication, sales enablement. |

## RACI rules — read before anything else

- **R — Responsible.** Does the work. One or more per task; T22 has two, since Kernel Engineer and SW Product both deliver it.
- **A — Accountable.** Owns the outcome and signs it off. Exactly one per task.
- **R/A — both.** Permitted on **non-gate tasks only**, where inventing a second approver would be fake governance.
- **C — Consulted.** Two-way. Their input is required before the task can complete.
- **I — Informed.** One-way. Told the outcome, no approval right.

> **The rule that carries the weight:** on any gate, R and A must be different people, and R/A is not permitted. This is what stops self-certification — the defect that let the IoT Engineer execute, present and approve their own robustness test in BP V3.

## Gate mechanics

Every gate is **three-way, never binary**:

- **Approve** — proceed to the next stage. Recorded with date and approver.
- **Rework** — return to a *named* prior task with a written defect list. Re-entry requires the same gate to be re-run.
- **Kill** — stop. Document reason and sunk cost. This is a success outcome, not a failure.

**Kill criteria must be written before the gate is run.** A gate with no kill criteria is a rubber stamp.

**SLA: 3 working days** from submission. On breach the request auto-escalates and the delay is logged against the project timeline. Every approver has one named standing delegate; if the approver is unavailable for more than 2 working days, the delegate decides.

## Change control

**Trigger:** any change to the L1 requirement after GATE 2 (T05), or to landed cost after T15.

**Process:** raise change request → impact assessment (cost, schedule, scope) → approved by the same authority that approved the original baseline.

Changes made outside this process are the single most common cause of a missed launch date. **Treat an unapproved change as a defect.**

## Lane routing

| Lane | When to use |
|---|---|
| **Full NPD** | New hardware platform, new product category, or first engagement with an unproven vendor. |
| **New Vendor / HW Upgrade** | Existing category, new supplier or revised hardware revision. Reuses the original L1, L2 and test cases. |
| **FW Upgrade** | Firmware change to devices already in the field. |
| **New SW Feature** | Platform-side feature on existing hardware. |

When a change spans two lanes — e.g. a firmware change that also alters the data contract — **take the heavier lane**.

---

# Stage 0 — Opportunity

## T01 · Draft business case

| | |
|---|---|
| Stage | 0. Opportunity · **Days** 5 · **Track** Main · **Critical path** Yes · Indicative day 0–5 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO · **C** Finance, Commercial |

**Purpose.** Establish that the opportunity is worth spending money on, before any money is spent. In BP V3 spending began at vendor sourcing with no approved business case at all; this task exists to close that.

**Inputs.** Market signal or customer demand, competitive context, current portfolio gaps.

**Steps.** Size the market and the addressable segment → set a target BOM cost and target price → derive the margin envelope → state the capex ask → argue strategic fit against the existing portfolio → review with Finance and Commercial before submission.

**Deliverable / exit criteria.** *Business case doc: market size, target BOM cost, target price, margin envelope, capex ask, strategic fit.*

**Watch-outs.** The target BOM cost set here becomes a binding design constraint at T04 and is tested against reality at T15. A soft or optimistic number here produces a kill at T15 that could have been avoided.

## T02 · GATE 1 — Business Case Approval

| | |
|---|---|
| Stage | 0. Opportunity · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 5–8 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO · **C** Finance |
| Decision | **Approve / Rework / Kill** |

**Purpose.** Release — or withhold — the budget envelope. This is the first of the eight CEO gates and the cheapest place in the entire process to stop.

**Deliverable / exit criteria.** *Signed approval + budget envelope released. Kill criteria recorded in writing.*

**Watch-outs.** Nothing downstream may be spent against an unapproved envelope; T08 sample procurement draws directly against it. Template: `04-approval-templates.md` §T02.

---

# Stage 1 — Pre-DoE

## T04 · Create L1 Product Requirement

| | |
|---|---|
| Stage | 1. Pre-DoE · **Days** 7 · **Track** Main · **Critical path** Yes · Indicative day 8–15 |
| Lanes | Full NPD, FW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO · **C** IoT Engineer, SW Product, Finance |

**Purpose.** Define what the product must do and what it must cost, in one document. Cost is deliberately placed inside the requirement rather than discovered later — engineers need a cost budget the way they need a spec.

**Inputs.** Approved business case and budget envelope from T02.

**Steps.** Write functional and performance requirements → define success KPIs → carry the target BOM cost and margin envelope in as explicit design constraints → consult IoT Engineer on feasibility and SW Product on platform implications → consult Finance on the margin envelope.

**Deliverable / exit criteria.** *L1 doc incl. success KPIs (install success rate, uptime, data completeness, RMA rate, attach rate). Where hardware is in scope, also target BOM cost and margin envelope.*

**Lane differences.** **HW Upgrade** does not run this task — it reuses the original product's L1. **New SW Feature** does not run it either; that lane starts at L2, which is why it carries no KPI baseline (see Known Limitations).

**Watch-outs.** The KPIs written here are what T43 tracks and what T44 judges. Vague KPIs here make GATE 8 a storytelling session.

## T05 · GATE 2 — L1 Requirement Approval

| | |
|---|---|
| Stage | 1. Pre-DoE · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 15–18 |
| Lanes | Full NPD, FW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO |
| Decision | **Approve / Rework / Kill** |

**Purpose.** Baseline the requirement. Everything after this point is measured against it, and any change to it is a change-control event.

**Deliverable / exit criteria.** *Approved L1 baselined. Any later change goes through Change Control.*

**Watch-outs.** This gate is the change-control trigger point. Silent scope creep after this gate is the most common cause of a missed launch date. Template: §T05.

## T06 · Source vendors (min 3 quoted, min 2 technically viable)

| | |
|---|---|
| Stage | 1. Pre-DoE · **Days** 7 · **Track** Main · **Critical path** Yes · Indicative day 18–25 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** Procurement · **C** IoT Engineer |

**Purpose.** Create genuine competitive tension and a fallback. Two technically viable options is the minimum that gives you negotiating position and protects against a single vendor failing qualification.

**Deliverable / exit criteria.** *Vendor longlist + comparison matrix. Single-source requires a signed risk waiver.*

**Watch-outs.** Single-sourcing is permitted but must be a written, signed decision — not a default that emerges because only one vendor replied.

## T07 · Vendor qualification & risk assessment

| | |
|---|---|
| Stage | 1. Pre-DoE · **Days** 3 · **Track** Main · **Critical path** Yes · Indicative day 25–28 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** Procurement · **A** IoT Product Owner · **C** IoT Engineer |

**Purpose.** Assess whether the vendor can actually supply at volume and support the product over its life — separately from whether the hardware works.

**Deliverable / exit criteria.** *Vendor scorecard: company size / annual sales volume — presence in SE Asia & Indonesia — MOQ — warranty model.*

**Watch-outs.** Simplified to four criteria in V5. Commercial terms are deliberately *not* settled here — they are handled at T28, after the technology is proven, which preserves negotiating position.

## T08 · Procure evaluation samples

| | |
|---|---|
| Stage | 1. Pre-DoE · **Days** 10 · **Track** Main · **Critical path** Yes · Indicative day 28–38 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** Procurement · **A** IoT Product Owner |

**Purpose.** Get physical units in hand for the DoE stage.

**Deliverable / exit criteria.** *Samples received + goods receipt. Spend against T02 budget envelope.*

**Watch-outs.** Ten days is the workbook's estimate and assumes no customs delay. Imported samples into Indonesia can exceed this; it sits on the critical path, so a slip here moves the launch date.

---

# Stage 2 — DoE

## T09 · Prepare L2 requirement + functional test cases

| | |
|---|---|
| Stage | 2. DoE · **Days** 7 · **Track** Main · **Critical path** Yes · Indicative day 38–45 |
| Lanes | Full NPD, New SW Feature |
| RACI | **R** IoT Engineer · **A** IoT Product Owner |

**Purpose.** Translate L1 into a testable technical specification, and — critically — write the PASS/FAIL thresholds *before* any testing happens, so gates are judged on data rather than narrative.

**Deliverable / exit criteria.** *L2 spec + test cases with PASS/FAIL thresholds defined BEFORE testing. In the New SW Feature lane, update the existing L2 where applicable rather than creating a new one.*

**Lane differences.** **New SW Feature** updates the existing L2 rather than authoring a new one — this is where that lane begins. **HW Upgrade** skips this task entirely and reuses the original L2 and its test cases.

**Watch-outs.** Thresholds written after seeing results are not thresholds. If a threshold has to be revised mid-test, that is a change-control event, not a note in the margin.

## T10 · Execute functional test case

| | |
|---|---|
| Stage | 2. DoE · **Days** 3 · **Track** Main · **Critical path** Yes · Indicative day 45–48 |
| Lanes | Full NPD, HW Upgrade, New SW Feature |
| RACI | **R/A** IoT Engineer |

**Purpose.** Test the sample hardware against the pre-committed functional thresholds.

**Deliverable / exit criteria.** *Test report vs thresholds.*

**Lane differences.** In **New SW Feature**, this runs *before any software build starts* — see T11. In **HW Upgrade**, this executes the original product's existing test cases against the new vendor's hardware.

**Watch-outs.** `R/A` on the same person. This is the self-certification pattern flagged in the BP V3 review, retained deliberately given current headcount. The only mitigation is that the CEO signs T11.

## T11 · GATE 3 — Functional test result approval

| | |
|---|---|
| Stage | 2. DoE · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 48–51 |
| Lanes | Full NPD, HW Upgrade, New SW Feature |
| RACI | **R** IoT Engineer · **A** CEO |
| Decision | **Approve / Rework / Kill** |

**Purpose.** Accept the functional result and — for the hardware lanes — approve the robustness test plan that follows.

**Deliverable / exit criteria.** *Approved functional test result. For the Full NPD and HW Upgrade lanes, also the robustness test plan: temperature — vibration — power consumption — IP rating — backup on power loss.*

**Lane differences.** In **New SW Feature** this gate carries unusual weight: it gates the software build. No PRD is written and no development starts until the hardware functional result passes. Template: §T11.

## T12 · Execute robustness test (min 1 week)

| | |
|---|---|
| Stage | 2. DoE · **Days** 7 · **Track** Main · **Critical path** Yes · Indicative day 51–58 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R/A** IoT Engineer |

**Purpose.** Prove the hardware survives the physical environment it will be deployed into — temperature, vibration, power consumption, IP rating, and backup behaviour on power loss.

**Deliverable / exit criteria.** *Robustness report vs thresholds.*

**Watch-outs.** Minimum one week is a floor, not a target. Same `R/A` self-certification note as T10.

## T13 · GATE 4 — Robustness result approval · **DESIGN FREEZE**

| | |
|---|---|
| Stage | 2. DoE · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 58–61 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Engineer · **A** CEO · **C** IoT Product Owner |
| Decision | **Approve / Rework / Kill** |

**Purpose.** Accept the robustness result and declare design freeze. This is the hinge of the whole schedule: certification (T14) cannot start before it, and any hardware change after it means re-certifying.

**Deliverable / exit criteria.** *Signed QA acceptance. Design freeze declared here.*

**Watch-outs.** Approving this gate while a hardware change is still under discussion silently destroys the certification timeline. If the design is not genuinely frozen, the honest decision is Rework. Template: §T13.

## T14 · Initiate SDPPI / Postel certification

| | |
|---|---|
| Stage | 2. DoE · **Days** 45 · **Track** **Certification (parallel)** · **Critical path** No · Indicative day 61–106 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** Procurement · **C** IoT Engineer |

**Purpose.** Obtain the Indonesian regulatory permit without which the product cannot legally be sold.

**Deliverable / exit criteria.** *Application filed + test lab slot booked.*

**Watch-outs — the most important scheduling risk in the process.**
- Fixed external queue time. **It cannot be compressed by adding people.**
- Cannot start before T13, because certification covers a specific frozen hardware configuration.
- Moved earlier in V4. In BP V3 it sat after PoC, where a slip would leave you with finished product, trained staff, ordered stock and no legal right to sell.
- **The 45-day figure is a placeholder.** Float is 26 days on Full NPD and only 16 on HW Upgrade. Above 71 days (61 for HW Upgrade) it becomes the critical path for the entire programme. **Re-baseline with the regulatory contact before committing any plan.**

## T15 · GATE — Cost checkpoint: landed BOM vs margin envelope

| | |
|---|---|
| Stage | 2. DoE · **Days** 2 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 61–63 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** Procurement · **A** Finance · **C** IoT Product Owner |
| Decision | **Proceed / Renegotiate / Kill** |

**Purpose.** Test the economics before the most expensive phase begins. Integration engages Kernel Engineer, SW Engineering and SW Product simultaneously; if the BOM cannot support the margin, stopping at ~day 63 rather than ~day 150 is the difference this task exists to make.

**Deliverable / exit criteria.** *Landed cost model (unit + duty + freight + provisioning) vs the governing L1 margin envelope — the new L1, or the original product's in the HW Upgrade lane.*

**Watch-outs.** **This is a kill trigger, not a status report.** Breaking the margin envelope means stopping or renegotiating, not proceeding with a note. Note that `A` is Finance, not the CEO — deliberately, so the economics are judged by the function that owns them. Landed cost after this point is a change-control trigger.

---

# Stage 3 — Integration

## T16 · Create integration contract (data logic, SW spec)

| | |
|---|---|
| Stage | 3. Integration · **Days** 3 · **Track** Main · **Critical path** Yes · Indicative day 63–66 |
| Lanes | Full NPD, HW Upgrade, FW Upgrade |
| RACI | **R** IoT Engineer · **A** SW Product · **C** IoT Product Owner, Kernel Engineer |

**Purpose.** Fix the data contract between device and platform in writing, so both sides build against the same definition.

**Deliverable / exit criteria.** *Signed integration contract.*

## T17 · Present integration contract to SW team

| | |
|---|---|
| Stage | 3. Integration · **Days** 3 · **Track** Main · **Critical path** Yes · Indicative day 66–69 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Engineer · **A** SW Product · **C** Kernel Engineer, SW Engineering |

**Purpose.** Walk the SW team through the contract and obtain committed estimates, rather than handing over a document and assuming it was read.

**Deliverable / exit criteria.** *Walkthrough done, SW estimates committed.*

## T18 · Integrate data from HW to MEP Server

| | |
|---|---|
| Stage | 3. Integration · **Days** 14 · **Track** Main · **Critical path** Yes · Indicative day 69–83 |
| Lanes | Full NPD, HW Upgrade, FW Upgrade |
| RACI | **R** Kernel Engineer · **A** SW Engineering · **C** IoT Engineer |

**Purpose.** Make device data actually flow into the platform.

**Deliverable / exit criteria.** *Data flowing, parser deployed to staging.*

**Watch-outs.** At 14 days this is the largest single block in the integration stage and one of the few realistic compression targets on the critical path.

## T19 · GATE — PRD Approval

| | |
|---|---|
| Stage | 3. Integration · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 83–86 |
| Lanes | Full NPD, New SW Feature |
| RACI | **R** SW Product · **A** **CTO** · **C** IoT Product Owner, SW Engineering |
| Decision | **Approve / Rework** |

**Purpose.** Ensure platform scope and acceptance criteria are agreed before any platform build starts. New in V6, and the only gate the CTO owns.

**Deliverable / exit criteria.** *Approved PRD covering platform scope, acceptance criteria, and dependencies on the integration contract.*

**Watch-outs.** No Kill option — by this point the decision to build has been taken at T24's predecessors. **Open question raised in deliverable 2, note A:** this gate currently sits *after* T18, so 14 days of integration work happen before the PRD is approved. Confirm whether that is intended.

## T20 · Develop platform functions (Live View, Report, Dashboard)

| | |
|---|---|
| Stage | 3. Integration · **Days** 7 · **Track** Main · **Critical path** Yes · Indicative day 86–93 |
| Lanes | Full NPD, New SW Feature |
| RACI | **R** SW Product · **A** SW Engineering · **C** IoT Product Owner |

**Purpose.** Build the customer-facing platform features against the approved PRD.

**Deliverable / exit criteria.** *Features deployed to staging.*

**Watch-outs.** Renumbered from T19 in V6. No build starts without T19 approved.

## T21 · GATE — SW QC approval (JIRA)

| | |
|---|---|
| Stage | 3. Integration · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 93–96 |
| Lanes | **All four** |
| RACI | **R** SW Product · **A** SW Engineering · **C** QA / QC |
| Decision | **Approve / Rework** |

**Purpose.** Confirm the software is defect-clear before end-to-end testing.

**Deliverable / exit criteria.** *JIRA tickets closed, regression suite green.*

**Watch-outs.** This is the **only** task in the entire process where QA/QC appears, and only as Consulted.

## T22 · GATE — Integration test approval (SW + HW data flow)

| | |
|---|---|
| Stage | 3. Integration · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 96–99 |
| Lanes | Full NPD, HW Upgrade, FW Upgrade |
| RACI | **R** Kernel Engineer **+** SW Product · **A** IoT Engineer · **C** SW Engineering |
| Decision | **Approve / Rework** |

**Purpose.** Prove the hardware and software work together end to end, not just independently.

**Deliverable / exit criteria.** *End-to-end test report signed.*

**Watch-outs.** The only task with two Responsible parties. The RACI rule was relaxed in V6 to allow this, because both sides genuinely deliver it. R and A remain different people, so the gate rule holds.

## T23 · Run product final UAT

| | |
|---|---|
| Stage | 3. Integration · **Days** 3 · **Track** Main · **Critical path** Yes · Indicative day 99–102 |
| Lanes | **All four** |
| RACI | **R/A** IoT Product Owner · **C** Head of Service |

**Purpose.** Accept the product against the requirement from the product owner's perspective, not the engineering one.

**Deliverable / exit criteria.** *UAT executed against L1 acceptance criteria.*

**Watch-outs.** Applies to every lane — nothing ships unaccepted.

## T24 · GATE 5 — Final UAT approval vs L1

| | |
|---|---|
| Stage | 3. Integration · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 102–105 |
| Lanes | **All four** |
| RACI | **R** IoT Product Owner · **A** CEO |
| Decision | **Approve / Rework / Kill** |

**Purpose.** CEO acceptance that the built product meets the requirement it was approved against.

**Deliverable / exit criteria.** *Signed UAT acceptance against the governing requirement — L1, the original L1 in the HW Upgrade lane, or L2 in the New SW Feature lane.*

**Lane differences.** The governing requirement differs by lane — check which document you are approving against. Template: §T24.

---

# Stage 4 — PoC

## T25 · Define PoC plan

| | |
|---|---|
| Stage | 4. PoC · **Days** 3 · **Track** Main · **Critical path** Yes · Indicative day 105–108 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO · **C** Commercial |

**Purpose.** Define what the PoC has to prove and who pays for it, before it starts.

**Deliverable / exit criteria.** *PoC plan: min 3 sites, customer selection criteria, success thresholds, cost owner, signed customer PoC agreement.*

**Watch-outs.** BP V3 had an undefined 1-site PoC with no success criteria, which meant it could not fail. The signed customer agreement matters — there is no legal function reviewing it.

**Schedule note.** The three parallel tracks (T28 Commercial, T29 Service, T30 Supply) branch from here.

## T26 · Run PoC on customer sites (min 3)

| | |
|---|---|
| Stage | 4. PoC · **Days** 21 · **Track** Main · **Critical path** Yes · Indicative day 108–129 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO · **C** IoT Engineer, Head of Service |

**Purpose.** Prove the product works in real customer conditions across enough sites to distinguish signal from a single friendly deployment.

**Deliverable / exit criteria.** *PoC results vs pre-agreed thresholds.*

**Watch-outs.** The largest single block on the critical path apart from T42. Compressing it is a quality decision, not a scheduling one.

## T27 · GATE 6 — PoC Go / No-Go

| | |
|---|---|
| Stage | 4. PoC · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 129–132 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO · **C** Finance, Commercial |
| Decision | **Approve / Rework / Kill** |

**Purpose.** Commit to commercial launch, or stop. **This is the last cheap exit** — everything after it involves stock, contracts and public commitments.

**Deliverable / exit criteria.** *Commercial launch commitment or documented kill.*

**Watch-outs.** Template: §T27.

---

# Stage 5 — Pre-Commercialization

## T28 · Finalise vendor agreement

| | |
|---|---|
| Stage | 5. Pre-Comm · **Days** 7 · **Track** **Commercial (parallel)** · **Critical path** No · Indicative day 108–115 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R/A** Procurement · **C** IoT Product Owner, Finance |

**Purpose.** Execute the supply contract now that the technology is proven and negotiating position is strongest.

**Deliverable / exit criteria.** *Executed contract: quality agreement, EOL/lifecycle clause, Incoterms, warranty terms, MOQ & lead time.*

**Watch-outs.** `R/A` on Procurement, with **no legal review anywhere in the process**. Procurement both negotiates and signs off the contract. Warranty terms are captured here, but there is no internal RMA workflow behind them (T31 deferred).

## T29 · Prepare SOP, WI, Techapp, QC parameters

| | |
|---|---|
| Stage | 5. Pre-Comm · **Days** 7 · **Track** **Service (parallel)** · **Critical path** No · Indicative day 108–115 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Engineer · **A** Head of Service · **C** Application Engineer |

**Purpose.** Produce the operating documentation the field organisation needs before installers are trained against it.

**Deliverable / exit criteria.** *Published SOP/WI set.*

## T30 · Manufacturing & logistics readiness

| | |
|---|---|
| Stage | 5. Pre-Comm · **Days** 10 · **Track** **Supply (parallel)** · **Critical path** No · Indicative day 108–118 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** Procurement · **A** IoT Engineer · **C** Head of Service · **I** Finance |

**Purpose.** Make sure the physical supply chain can actually receive, provision and ship units. BP V3 jumped straight from PoC to stock pre-order.

**Deliverable / exit criteria.** *Incoming QC procedure, IMEI/serial management, provisioning & flashing process, packaging spec, import/customs path.*

**Watch-outs.** See deliverable 2 note B — this arguably cannot complete before T28 fixes Incoterms and MOQ.

## T31 · Define warranty, RMA & spare parts policy — **DEFERRED**

| | |
|---|---|
| Status | **Deferred** in V5 — retained for future revision. Not in any lane. |
| Would be | 5 d · Supply track · **R** Head of Service · **A** Finance · **C** Procurement |

**Consequence of the deferral.** Warranty *terms* are still captured in the vendor agreement at T28, but there is **no internal RMA workflow and no spare-parts stocking plan** anywhere in the process. Note that `RMA rate` is one of the L1 success KPIs tracked at T43 — the process measures a rate it has no defined workflow to handle.

## T32 · Define OTA / firmware lifecycle policy — **DEFERRED**

| | |
|---|---|
| Status | **Deferred** in V5 — retained for future revision. Not in any lane. |
| Would be | 5 d · Supply track · **R** Kernel Engineer · **A** IoT Product Owner · **C** IoT Engineer, Head of Service |

**Consequence of the deferral — highest-severity known gap.** The FW Upgrade lane currently has **no staged-rollout and no rollback step**. A firmware release goes from CEO UAT approval (T24) directly to the entire installed fleet at once. There is no versioning scheme, no 5%/25%/100% staged rollout, no rollback procedure and no fleet firmware compliance tracking. **Worth closing before the first at-scale OTA.**

## T33 · GATE — Train Service Leader (BAST) + certify installers

| | |
|---|---|
| Stage | 5. Pre-Comm · **Days** 3 · **Track** **Service (parallel)** · **Critical path** No · **GATE** · Indicative day 115–118 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** Application Engineer · **A** Head of Service · **C** IoT Engineer |
| Decision | **Approve / Rework** |

**Purpose.** Confirm the field organisation is trained and installers are formally certified before units reach customers.

**Deliverable / exit criteria.** *BAST signed + installer certification register.*

**Watch-outs.** Install success rate is an L1 KPI measured at T42 and T43. Weak certification here shows up as a KPI failure three months later.

## T34 · Support readiness

| | |
|---|---|
| Stage | 5. Pre-Comm · **Days** 5 · **Track** **Service (parallel)** · **Critical path** No · Indicative day 118–123 |
| Lanes | Full NPD, FW Upgrade, New SW Feature |
| RACI | **R** Head of Service · **A** Application Engineer · **C** IoT Product Owner |

**Purpose.** Make sure support can handle the product on day one rather than learning from tickets.

**Deliverable / exit criteria.** *Support runbook, escalation matrix, L1/L2 troubleshooting scripts, known-issues list.*

**Watch-outs.** Notably absent from the HW Upgrade lane — a new supplier's hardware may fail in new ways that the existing runbook does not cover. Worth questioning.

## T35 · Confirm SDPPI certification received — **HARD BLOCKER**

| | |
|---|---|
| Stage | 5. Pre-Comm · **Days** 2 · **Track** Main · **Critical path** Yes · **BLOCKER CHECK** · Indicative day 132–134 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** Procurement · **I** CEO |
| Decision | **Blocker check** — not a three-way gate |

**Purpose.** Verify the certificate is physically in hand before anything is sold.

**Deliverable / exit criteria.** *Certificate in hand. HARD BLOCKER — no legal sale without it.*

**Watch-outs.** This is not a normal gate — there is no rework path and no discretion. Either the certificate exists or the product cannot legally be sold. If T14 slipped, this is where you discover it, at day 132, with stock about to be ordered and installers already trained. That is precisely the failure mode the early-certification move was designed to prevent, and it is why T14's real lead time must be verified.

## T36 · GATE 7 — Pricing & Packaging approval

| | |
|---|---|
| Stage | 5. Pre-Comm · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 134–137 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO · **C** Finance, Commercial |
| Decision | **Approve / Rework** |

**Purpose.** Set the price. Price stays late deliberately — it needs real landed-cost data (T15) and PoC evidence of value (T26).

**Deliverable / exit criteria.** *Approved price book + packaging, validated against T15 landed cost.*

**Watch-outs.** This is now a **confirmation** against the T04 cost target, not a discovery. In BP V3 pricing was step 29 of 31, with everything already sunk. If the price here cannot deliver the T04 margin envelope, that is a change-control event against the L1 baseline — not a quiet adjustment. Template: §T36.

## T37 · Present commercialization deck to commercial leaders

| | |
|---|---|
| Stage | 5. Pre-Comm · **Days** 3 · **Track** Main · **Critical path** Yes · Indicative day 137–140 |
| Lanes | **Full NPD only** |
| RACI | **R/A** IoT Product Owner · **C** Commercial |

**Purpose.** Bring the commercial organisation onto the product and surface sales objections before launch rather than after.

**Deliverable / exit criteria.** *Deck delivered, sales objections logged.*

**Watch-outs.** Full NPD only — a vendor swap is not re-sold to the commercial team.

---

# Stage 6 — Commercialization

## T38 · Pre-order initial stock

| | |
|---|---|
| Stage | 6. Comm · **Days** 3 · **Track** Main · **Critical path** Yes · Indicative day 140–143 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** Procurement · **A** Finance · **C** IoT Product Owner |

**Purpose.** Commit working capital to stock against an approved forecast.

**Deliverable / exit criteria.** *PO raised against approved forecast.*

**Watch-outs.** The first genuinely irreversible spend. It sits after T35, so stock is never ordered against an uncertified product.

## T39 · Present in Monthly Product Demo

| | |
|---|---|
| Stage | 6. Comm · **Days** 3 · **Track** **Commercial (parallel)** · **Critical path** No · Indicative day 137–140 |
| Lanes | Full NPD, FW Upgrade, New SW Feature |
| RACI | **R/A** IoT Product Owner |

**Deliverable / exit criteria.** *Demo delivered.* Absent from HW Upgrade — nothing new to demo on a vendor swap.

## T40 · Launch external communication w/ Marketing

| | |
|---|---|
| Stage | 6. Comm · **Days** 14 · **Track** **Commercial (parallel)** · **Critical path** No · Indicative day 143–157 |
| Lanes | Full NPD, New SW Feature |
| RACI | **R** Commercial (CBO/Mktg) · **A** IoT Product Owner |

**Deliverable / exit criteria.** *Launch collateral live.* Marketing executes; IoT Product Owner owns the outcome.

## T41 · Sales enablement ready

| | |
|---|---|
| Stage | 6. Comm · **Days** 7 · **Track** Main · **Critical path** Yes · Indicative day 143–150 |
| Lanes | Full NPD, New SW Feature |
| RACI | **R** Commercial (CBO/Mktg) · **A** IoT Product Owner · **C** Head of Service |

**Purpose.** Put the sales organisation in a position to actually sell the product.

**Deliverable / exit criteria.** *Battlecard, demo kit, pricing calculator, objection handling, trained AEs.*

**Watch-outs.** Full NPD and New SW Feature only — existing enablement already covers the category on an upgrade. **This is the effective launch milestone** (day 150 in Full NPD).

---

# Stage 7 — Post-Commercialization

## T42 · Review installation quality (first 20–50 installs)

| | |
|---|---|
| Stage | 7. Post-Comm · **Days** 30 · **Track** Main · **Critical path** Yes · Indicative day 150–180 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Engineer · **A** Head of Service · **C** Application Engineer |

**Purpose.** Catch systematic installation problems in the first cohort, while the population is small enough to fix cheaply.

**Deliverable / exit criteria.** *Install quality report + corrective actions.*

## T43 · Track KPIs vs L1 targets (30/60/90 day)

| | |
|---|---|
| Stage | 7. Post-Comm · **Days** 90 · **Track** Main · **Critical path** No (see below) · Indicative day 150–240 |
| Lanes | **All four** |
| RACI | **R/A** IoT Product Owner · **C** Finance, Head of Service |

**Purpose.** Measure the product against the KPIs set in L1, so that GATE 8 is a data review rather than a storytelling session.

**Deliverable / exit criteria.** *KPI dashboard vs the governing requirement's KPI targets: install success, uptime, data completeness, RMA rate, attach rate, realised margin.*

**Lane differences.** In **New SW Feature** this lane carries no L1, so no KPI baseline exists and tracking here is **qualitative**.

**Watch-outs.** Flagged as non-critical-path in the workbook, but T44 is a *3-month* review that depends on this data. See deliverable 2 §2.4 — this is the single biggest open question in the schedule. Also note the process tracks `RMA rate` while T31 (RMA workflow) is deferred.

## T44 · GATE 8 — 3-month post-release review

| | |
|---|---|
| Stage | 7. Post-Comm · **Days** 3 · **Track** Main · **Critical path** Yes · **GATE** · Indicative day 240–243 |
| Lanes | Full NPD, HW Upgrade |
| RACI | **R** IoT Product Owner · **A** CEO · **C** Finance |
| Decision | **Scale / Fix / Sunset** |

**Purpose.** Decide the product's future against measured KPI performance.

**Deliverable / exit criteria.** *Scale / Fix / Sunset decision recorded against KPI targets.*

**Lane differences.** **Absent from FW Upgrade and New SW Feature** — those lanes have no post-release review gate at all. Template: §T44.

## T45 · Annual lifecycle & EOL review

| | |
|---|---|
| Stage | 7. Post-Comm · **Days** 5 · **Track** Main · **Critical path** No · Indicative day 243–248 |
| Lanes | **Full NPD only** |
| RACI | **R** IoT Product Owner · **A** CEO · **C** Procurement, Head of Service |

**Purpose.** Decide annually whether to continue, refresh or end-of-life the product, with a migration plan for the installed base.

**Deliverable / exit criteria.** *Continue / refresh / EOL decision + migration plan for installed base.*

**Watch-outs.** Product-level, not run per upgrade. BP V3 had no sunset path at all.

---

# Known limitations — decided, not forgotten

These are recorded so they remain visible decisions rather than becoming invisible assumptions.

| # | Limitation | Consequence |
|---|---|---|
| 1 | **No independent test acceptance.** T10 and T12 are `R/A = IoT Engineer`. QA/QC appears only as Consulted on T21. | The IoT Engineer executes, presents and owns the functional and robustness results. Mitigated only by CEO signature on T11 and T13 — and the CEO is not independently verifying test data. |
| 2 | **No security or privacy review anywhere.** | Firmware signing, secure boot, OTA authentication and PII handling for location data are not covered by any task in any lane. |
| 3 | **No legal / regulatory function.** | Procurement owns SDPPI certification (T14, T35) and vendor contract sign-off (T28). No legal review of contracts, PoC customer agreements or data privacy. |
| 4 | **T31 warranty / RMA deferred.** | Warranty terms exist in the T28 contract, but no internal RMA workflow or spare-parts plan — while `RMA rate` is a tracked KPI. |
| 5 | **T32 OTA lifecycle deferred.** | FW Upgrade lane has no staged rollout and no rollback. A bad firmware release reaches the whole fleet at once. **Highest severity of these five.** |
| 6 | **SW Feature lane has no KPI baseline.** | That lane starts at L2 and carries no L1, so no success KPIs are set. T43 tracking is qualitative and the lane has no T44 review gate. |
| 7 | **CEO throughput.** | Accountable on 8 of 14 gates. CEO calendar availability is effectively the critical path. The 3-day SLA and named-delegate rule are the only controls. If more than two products need to run concurrently, revisit — the CTO is the natural home for T11 and T24. |
