# 4. Gate Submission Templates — the 8 CEO Gates

These are **submission documents**: the Responsible party writes one up and submits it, and the Accountable approves by ticking the block at the top. They are not decision forms — the substance is the document.

The format follows the existing McEasy pattern (`HW DoE - Teltonika TFT100 Manual CAN`): approval block first, then the content the approver needs in order to decide. Section headings are English; write the body in whatever language suits the audience.

One template per gate where the **CEO is Accountable**: T02, T05, T11, T13, T24, T27, T36, T44. The other six gates (T19 PRD/CTO, T21 SW QC, T22 integration test, T33 BAST, T35 SDPPI blocker check) are approved inside the delivery workflow and do not need a submission document.

## House rules for all eight

| Rule | Detail |
|---|---|
| **Approval block goes first** | Before any content. The approver should see who is signing what without scrolling. |
| **Decision is three-way** | Approve / Rework / Kill. Approving because the form has no other box is the failure this prevents. T36 is Approve/Rework; T44 is Scale/Fix/Sunset. |
| **Kill criteria are written before the gate runs** | Not after seeing the results. A gate with no kill criteria is a rubber stamp. Fill that section when you *start* the work, not when you submit. |
| **SLA** | 3 working days from submission. On breach the request auto-escalates and the delay is logged against the project timeline. |
| **Named delegate** | If the CEO is unavailable more than 2 working days, the named standing delegate signs. This is a schedule control — 8 CEO gates sit on the critical path. |
| **R ≠ A** | Whoever prepares the document does not approve it. |
| **Rework names a target** | State which task it returns to and attach the defect list. "Revise and resubmit" is not a decision. |

**Title convention:** `<Gate> - <Product> (<Scope>)` — e.g. `GATE 3 Functional Test - Teltonika TFT100 (Manual CAN)`.

**Confluence:** each template is separated by `---` so it lifts cleanly into its own page. Save as a page template (Space Settings → Templates) for per-project reuse. Plain headings, tables and `- [ ]` checkboxes only — they convert on paste.

---

# GATE 1 · T02 — Business Case

> **Submitted by** IoT Product Owner · **Approved by** CEO · **Consulted** Finance, Commercial
> **Purpose of this gate:** release or withhold the budget envelope. Nothing is spent before this is approved. Cheapest exit in the whole process.

---

# `<Product Name>` - Business Case

**Approval**

- [ ] `<IoT Product Owner name>` (prepared) - [DATE]
- [ ] `<CEO name>` (approved) - [DATE]

**Decision** — tick one

- [ ] **Approve** — budget envelope released: `<amount>`
- [ ] **Rework** — return to business case drafting. Defect list below.
- [ ] **Kill** — reason and sunk cost below.

**Submitted:** [DATE] · **SLA due:** [DATE + 3 working days] · **Delegate if CEO unavailable:** `<name>`

# Background and Purpose

`<What problem or opportunity is this? Why now? 2-4 bullets.>`

# Current State

`<How is this handled today — by us, by customers, or not at all? What does it cost us to leave it alone?>`

# Benefits

`<What changes if we do this. Be specific and measurable where possible.>`

# Commercial Consideration

`<Market context and why demand is moving.>`

**Target customers and volume projection:**

| Customer / Segment | Projected units per year | Notes |
| --- | --- | --- |
| `<customer>` | `<qty>` | |
| `<customer>` | `<qty>` | |
| **Total** | | |

# Cost and Margin Envelope

These become **design constraints** in the L1 requirement at T04, and are tested against real quotes at the T15 cost checkpoint.

| Item | Target |
| --- | --- |
| Target BOM cost (per unit) | |
| Target selling price | |
| Target gross margin % | |
| Margin envelope (floor) | |
| Capex ask | |

# Success Criteria

`<What does success look like in numbers? These become the L1 KPIs.>`

| KPI | Target |
| --- | --- |
| Install success rate | |
| Uptime | |
| Data completeness | |
| RMA rate | |
| Attach rate | |

# Estimated Timeline

| Phase | Timing | Notes / Target |
| --- | --- | --- |
| Pre-DoE (L1, vendor sourcing) | | |
| DoE (test, design freeze) | | |
| Integration | | |
| PoC | | |
| Commercialization | | |

# Strategic Fit

`<How this extends or defends the existing portfolio. What happens to our position if we don't do it.>`

# Risks and Kill Criteria

**Written before this gate is run.**

| # | Risk | Kill if… |
| --- | --- | --- |
| 1 | Market too small | Addressable market below `<threshold>` |
| 2 | Economics do not work | Target price cannot support the margin envelope at target BOM cost |
| 3 | No strategic fit | Does not extend or defend an existing line |
| 4 | Capex | Ask exceeds portfolio allocation for the period |
| 5 | | |

# Decision Notes

`<Approver's reasoning, conditions attached, or — if Rework/Kill — the defect list or the reason plus sunk cost to date.>`

---

# GATE 2 · T05 — L1 Product Requirement

> **Submitted by** IoT Product Owner · **Approved by** CEO
> **Purpose of this gate:** baseline the requirement. Everything downstream is measured against it, and any later change is a change-control event.

---

# `<Product Name>` - L1 Product Requirement

**Approval**

- [ ] `<IoT Product Owner name>` (prepared) - [DATE]
- [ ] `<CEO name>` (approved) - [DATE]

**Decision** — tick one

- [ ] **Approve** — L1 baselined as version `<id>`
- [ ] **Rework** — defect list below
- [ ] **Kill** — reason and sunk cost below

**Submitted:** [DATE] · **SLA due:** [DATE + 3] · **Delegate:** `<name>` · **Traceable to business case:** `<T02 doc link>`

# Background and Purpose

`<Short restatement of the approved business case and what this requirement has to deliver.>`

# Scope

**In scope:** `<what this product must do>`

**Out of scope:** `<explicitly excluded, so it does not creep back in>`

# Functional Requirements

| # | Requirement | Priority (Must/Should/Could) | Acceptance criterion |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |

# Performance Requirements

| # | Parameter | Target | Measurement method |
| --- | --- | --- | --- |
| 1 | | | |

# Design Constraints

Cost enters the requirement here on purpose — engineers need a cost budget the way they need a spec.

| Constraint | Value |
| --- | --- |
| Target BOM cost (per unit) | |
| Margin envelope (floor) | |
| Physical / environmental constraints | |
| Compatibility constraints (platform, existing fleet) | |

# Success KPIs

These are what T43 tracks and what GATE 8 judges. Vague KPIs here make the post-release review a storytelling session.

| KPI | Target | Measured how | Measured when |
| --- | --- | --- | --- |
| Install success rate | | | 30/60/90 day |
| Uptime | | | 30/60/90 day |
| Data completeness | | | 30/60/90 day |
| RMA rate | | | 30/60/90 day |
| Attach rate | | | 30/60/90 day |
| Realised margin | | | 90 day |

# Dependencies and Assumptions

`<Platform dependencies, vendor dependencies, regulatory assumptions, anything outside our control.>`

# Risks and Kill Criteria

| # | Risk | Kill if… |
| --- | --- | --- |
| 1 | Not buildable in budget | Requirement cannot be met within the T02 envelope |
| 2 | BOM target unreachable | Engineering assesses target BOM cost as not achievable |
| 3 | Unmeasurable value claim | No measurable KPI can be defined for the core value claim |
| 4 | Drift from business case | Requirement has materially diverged from what was approved at T02 |
| 5 | | |

# Change Control — active from approval

From this approval onward, **any change to this L1** must: raise a change request → receive an impact assessment covering cost, schedule and scope → be approved by the CEO, the same authority that baselined it.

**An unapproved change is a defect, not an adjustment.**

# Decision Notes

`<Approver's reasoning, conditions, or defect list.>`

---

# GATE 3 · T11 — Functional Test Result (DoE)

> **Submitted by** IoT Engineer · **Approved by** CEO
> **Purpose of this gate:** accept the functional result against thresholds committed *before* testing began, and — in the hardware lanes — approve the robustness test plan that follows.
> **New SW Feature lane:** this gate also releases the software build. No PRD is written and no development starts until it passes.

*This template follows the existing `HW DoE` document structure most closely — it is the one your team already uses.*

---

# HW DoE - `<Vendor Model>` (`<Scope>`)

**Approval**

- [ ] `<IoT Engineer name>` (prepared) - [DATE]
- [ ] `<CEO name>` (approved) - [DATE]

**Decision** — tick one

- [ ] **Approve** — functional result accepted; robustness test plan approved (HW lanes)
- [ ] **Rework** — return to `T10 Execute functional test`. Defect list below.
- [ ] **Kill** — reason and sunk cost below

**Submitted:** [DATE] · **SLA due:** [DATE + 3] · **Delegate:** `<name>`

# Background and Purpose

`<Why this DoE exists. What capability gap or customer need it addresses.>`

# Current State

`<How this is handled today, what it costs, what the alternatives are.>`

# Benefits

`<What improves if this device/capability is adopted.>`

# Commercial Consideration

`<Why demand is moving. Then the customer/volume list.>`

| Customer / Segment | Projected units per year |
| --- | --- |
| `<customer>` | `<qty>` |

# Success Criteria

The DoE is considered successful if:

1. `<criterion with a numeric threshold>`
2. `<criterion with a numeric threshold>`
3. `<criterion with a numeric threshold>`

> **These thresholds must be the ones set at T09, before testing started.** If any threshold changed during testing, attach the change-control record. Thresholds written after seeing results are not thresholds.

# Estimated Timeline

| Phase | Timing | Notes / Target |
| --- | --- | --- |
| DoE Execution | Week 1 | |
| Collect Data | Week 2 | |
| Data Analysis | Week 3 | |
| Integration | Week 4 | |
| Review | Week 5 | |

# DoE Summary

*There are 4 types of DoE test case:*

- **Functional test** — data accuracy, logic verification, alert functionality, communication protocol
- **Parameter test** — experiment to set the right parameter
- **Stress test** — temperature, vibration, etc.
- **Power Consumption / Profiling test** — if this is a concern

| # | Test Case | Objective | Type | Threshold | Result | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | Functional Test | | | |
| 2 | | | Functional Test | | | |
| 3 | | | Profiling Test | | | |

# DoE Conclusion

`<3-5 bullets: what passed, what did not, and the recommendation. State limitations plainly — e.g. "not recommended for vehicles with battery < 6Ah".>`

# Robustness Test Plan
*(Full NPD and HW Upgrade lanes only — this gate approves the plan, T12 executes it.)*

| Test | Threshold | Method | Sample size |
| --- | --- | --- | --- |
| Temperature | | | |
| Vibration | | | |
| Power consumption | | | |
| IP rating | | | |
| Backup on power loss | | | |

# Risks and Kill Criteria

| # | Kill if… |
| --- | --- |
| 1 | A must-pass threshold fails with no viable engineering fix |
| 2 | The fix requires a hardware change that breaks the target BOM cost |
| 3 | Vendor cannot or will not remediate a failed case |
| 4 | Pass rate below `<floor>` across the sample set |
| 5 | |

# Detail of DoE

## Test #1 - `<Test Name>`

| Topic | Details |
| --- | --- |
| Objective | |
| Hypothesis | |
| Independent Variable (and its level) | |
| Dependent Variable | |
| Control Variable | |
| Testing Equipment Required | |
| Experiment Setup (Diagram / Pic) | |
| Add'l Information | |

### Data Collection Result

`<Table of raw results, and/or link to the source data file.>`

Source: `<link>`

### Data Analysis

`<What the numbers mean. Include comparisons against the reference device where applicable.>`

### Summary

`<One paragraph: does this test pass against its threshold, and what is the caveat.>`

---

*(Repeat the Test # block for each test case.)*

# Decision Notes

`<Approver's reasoning, conditions, or defect list.>`

---

# GATE 4 · T13 — Robustness Result & Design Freeze

> **Submitted by** IoT Engineer · **Approved by** CEO · **Consulted** IoT Product Owner
> **Purpose of this gate:** accept the robustness result **and declare design freeze**. SDPPI certification (T14) cannot start before this, and any hardware change after it means re-certifying.

---

# HW Robustness & Design Freeze - `<Vendor Model>`

**Approval**

- [ ] `<IoT Engineer name>` (prepared) - [DATE]
- [ ] `<CEO name>` (approved) - [DATE]

**Decision** — tick one

- [ ] **Approve** — robustness accepted and **DESIGN FREEZE DECLARED**. T14 certification authorised to start.
- [ ] **Rework** — return to `T12 Execute robustness test`. Defect list below.
- [ ] **Kill** — reason and sunk cost below

**Submitted:** [DATE] · **SLA due:** [DATE + 3] · **Delegate:** `<name>`

# Background and Purpose

`<Short restatement: which device, which lane, what was tested and why this gate matters to the schedule.>`

# Robustness Test Summary

Minimum 1 week of testing. Results against thresholds pre-committed at T09/T11.

| # | Test | Threshold | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| 1 | Temperature | | | |
| 2 | Vibration | | | |
| 3 | Power consumption | | | |
| 4 | IP rating | | | |
| 5 | Backup on power loss | | | |

**Sample set:** `<size, serial numbers>` · **Test duration:** `<dates>`

# Failed Cases and Disposition

| # | Failed test | Root cause | Disposition | Accepted by |
| --- | --- | --- | --- | --- |
| | | | | |

# Conclusion

`<What the device is and is not suitable for, stated plainly.>`

# Configuration to be Frozen

**This is the exact configuration certification will cover. Any change after approval means re-certifying.**

| Item | Value |
| --- | --- |
| BOM revision | |
| PCB revision | |
| Enclosure | |
| Firmware version | |
| Antenna / module variants | |

- [ ] Confirmed: no hardware change is pending, proposed or under discussion
- [ ] Confirmed: vendor can supply this exact configuration at volume
- [ ] Confirmed: vendor has agreed to notify us of any component change (EOL, substitution)

# Impact of Freeze

Approving this starts T14 SDPPI certification — currently modelled at **45 working days of fixed external queue time that cannot be compressed by adding people**. Float is 26 days on Full NPD and only 16 on HW Upgrade.

> **Do not approve a freeze that is not real.** If a hardware change lands after this signature, T14 restarts and the launch date moves by the full certification lead time. If the design is not genuinely frozen, the correct decision is Rework.

# Risks and Kill Criteria

| # | Kill if… |
| --- | --- |
| 1 | An environmental threshold fails with no viable fix inside the cost envelope |
| 2 | A fix requires re-opening the design and re-running T12 beyond schedule tolerance |
| 3 | IP rating or power-loss backup fails — these are typically contractual with customers |
| 4 | Vendor cannot guarantee configuration stability for the product's expected life |
| 5 | |

# Detail of Robustness Tests

## Test #1 - `<Test Name>`

| Topic | Details |
| --- | --- |
| Objective | |
| Hypothesis | |
| Independent Variable (and its level) | |
| Dependent Variable | |
| Control Variable | |
| Testing Equipment Required | |
| Experiment Setup (Diagram / Pic) | |
| Add'l Information | |

### Data Collection Result

Source: `<link>`

### Data Analysis

### Summary

---

*(Repeat per test.)*

# Decision Notes

---

# GATE 5 · T24 — Final UAT

> **Submitted by** IoT Product Owner · **Approved by** CEO
> **Purpose of this gate:** CEO acceptance that the built product meets the requirement it was approved against. Applies to **all four lanes** — nothing ships unaccepted.

---

# `<Product Name>` - Final UAT Acceptance

**Approval**

- [ ] `<IoT Product Owner name>` (prepared) - [DATE]
- [ ] `<CEO name>` (approved) - [DATE]

**Decision** — tick one

- [ ] **Approve** — UAT accepted against the governing requirement
- [ ] **Rework** — return to `<T22 / named task>`. Defect list below.
- [ ] **Kill** — reason and sunk cost below

**Submitted:** [DATE] · **SLA due:** [DATE + 3] · **Delegate:** `<name>`

**Governing requirement for this lane** — state the document and version:

| Lane | Governing requirement | Document ID / version |
| --- | --- | --- |
| Full NPD | L1 | |
| HW Upgrade | Original product's L1 | |
| FW Upgrade | L1 | |
| New SW Feature | L2 | |

# Background and Purpose

`<What was built, which lane, and what this UAT covers.>`

# UAT Scope

`<What was tested, on what environment, with what data, by whom.>`

# Acceptance Criteria vs Result

Every acceptance criterion in the governing requirement maps to a result. No blanks.

| # | Acceptance criterion (from L1/L2) | Priority | Test result | Pass/Fail |
| --- | --- | --- | --- | --- |
| 1 | | Must | | |
| 2 | | Must | | |

# Open Defects

| # | Defect | Severity | Fix plan | Target date | Blocks launch? |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

# Upstream Approvals

- [ ] **T21 SW QC approval** obtained — JIRA tickets closed, regression suite green · `<link>`
- [ ] **T22 Integration test approval** obtained — end-to-end report signed · `<link>`
- [ ] Any deviation from the baselined requirement has a change-control record · `<link>`

# Conclusion

`<Is the product acceptable, and with what caveats.>`

# Risks and Kill Criteria

| # | Kill if… |
| --- | --- |
| 1 | A must-have acceptance criterion is unmet with no viable path to meeting it |
| 2 | Remediation cost or schedule breaks the business case approved at T02 |
| 3 | Open severity-1 defect with no fix plan |
| 4 | Product as built no longer matches the value proposition in the business case |

> **FW Upgrade lane warning.** Approving this releases firmware to the **entire installed fleet at once**. T32 (OTA lifecycle policy — staged rollout, rollback) is deferred, so there is currently no 5%/25%/100% ramp and no rollback procedure. Attach a manual staged-rollout plan until T32 is implemented.

# Decision Notes

---

# GATE 6 · T27 — PoC Go / No-Go

> **Submitted by** IoT Product Owner · **Approved by** CEO · **Consulted** Finance, Commercial
> **Purpose of this gate:** commit to commercial launch, or stop. **This is the last cheap exit** — everything after involves stock, contracts and public commitments.

---

# `<Product Name>` - PoC Result & Go/No-Go

**Approval**

- [ ] `<IoT Product Owner name>` (prepared) - [DATE]
- [ ] `<CEO name>` (approved) - [DATE]

**Decision** — tick one

- [ ] **Approve** — commercial launch committed
- [ ] **Rework** — return to `T26 Run PoC`, extend or re-run. Defect list below.
- [ ] **Kill** — reason and sunk cost below

**Submitted:** [DATE] · **SLA due:** [DATE + 3] · **Delegate:** `<name>`

# Background and Purpose

`<What the PoC was meant to prove, and against what pre-agreed thresholds set at T25.>`

# PoC Scope

**Minimum 3 customer sites.** Site selection must meet the criteria agreed at T25.

| # | Customer | Site / fleet | Units | Duration | Signed PoC agreement |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | `<link>` |
| 2 | | | | | `<link>` |
| 3 | | | | | `<link>` |

# Results vs Pre-Agreed Thresholds

| # | Success threshold (from T25) | Site 1 | Site 2 | Site 3 | Met? |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |

# Incidents During PoC

| # | Incident | Site | Root cause | Resolution | Recurrence risk |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

# Customer Feedback

| Customer | What worked | Objections raised | Willing to buy at target price? |
| --- | --- | --- | --- |
| | | | |

# Commercial Evidence

`<Demand evidence against the T01 market sizing. Does the PoC support the volume assumptions?>`

| Customer / Segment | Projected units per year | Confidence |
| --- | --- | --- |
| | | |

# Economics Check

| Item | Value | Source |
| --- | --- | --- |
| Landed cost per unit | | T15 |
| Target price | | T04 |
| Observed install / support burden per unit | | PoC |
| Revised unit economics | | |

# Conclusion

`<Recommendation and the reasoning.>`

# Risks and Kill Criteria

| # | Kill if… |
| --- | --- |
| 1 | Fewer than `<n>` sites met the pre-agreed success thresholds |
| 2 | A field failure mode appeared that was not caught in DoE and has no fix |
| 3 | Customers will not pay the price the margin envelope requires |
| 4 | Install or support burden observed makes the unit economics unviable |
| 5 | Demand evidence does not support the T01 market sizing |

> **Approval here does not clear the product for sale.** T35 (SDPPI certificate in hand) is a hard blocker that follows. Do not order stock or announce before T35 clears.

# Decision Notes

---

# GATE 7 · T36 — Pricing & Packaging

> **Submitted by** IoT Product Owner · **Approved by** CEO · **Consulted** Finance, Commercial
> **Purpose of this gate:** approve the price book and packaging. This is a **confirmation** against the T04 cost target and the T15 landed cost — not a discovery.
> **Decision options: Approve / Rework only.** The launch commitment was made at T27.

---

# `<Product Name>` - Pricing & Packaging

**Approval**

- [ ] `<IoT Product Owner name>` (prepared) - [DATE]
- [ ] `<CEO name>` (approved) - [DATE]

**Decision** — tick one

- [ ] **Approve** — price book and packaging approved
- [ ] **Rework** — re-price. Defect list below.

**Submitted:** [DATE] · **SLA due:** [DATE + 3] · **Delegate:** `<name>`

# Background and Purpose

`<What is being priced and why now.>`

# Landed Cost Summary

From T15. This is the number the price must clear.

| Component | Cost per unit |
| --- | --- |
| Unit cost (ex works) | |
| Duty | |
| Freight | |
| Provisioning | |
| **Total landed cost** | |

# Proposed Price and Packaging

| SKU | Description | List price | Notes |
| --- | --- | --- | --- |
| | | | |

`<Packaging and bundling structure. Confirm it is operable by the supply process defined at T30.>`

# Margin Validation

The core check of this gate.

| Item | Value |
| --- | --- |
| Total landed cost (T15) | |
| Proposed list price | |
| **Realised gross margin %** | |
| **Margin envelope from L1 (T04)** | |
| **Clears the envelope?** | Yes / No |

# Willingness-to-Pay Evidence

From the PoC at T26 — not from assumption.

| Customer | Price tested | Response |
| --- | --- | --- |
| | | |

# Competitive Positioning

| Competitor | Comparable product | Their price | Our position |
| --- | --- | --- | --- |
| | | | |

# Volume Forecast

Feeds the T38 stock PO.

| Period | Forecast units | Basis |
| --- | --- | --- |
| | | |

# Conclusion

# Rework Criteria

This gate has no Kill. These force a Rework rather than an approval.

| # | Rework if… |
| --- | --- |
| 1 | Proposed price does not deliver the T04 margin envelope at the T15 landed cost |
| 2 | Price is not supported by PoC willingness-to-pay evidence |
| 3 | Price is uncompetitive against the T01 positioning |
| 4 | Packaging or SKU structure is not operable by the T30 supply process |

# Change Control

If the approved price **cannot** deliver the margin envelope baselined in the L1 at T05, that is a change to the L1 baseline. It requires a change request, an impact assessment, and CEO approval as the original baselining authority.

**Do not absorb the gap silently at this gate** — that turns a governance decision into an accounting surprise.

# Decision Notes

---

# GATE 8 · T44 — 3-Month Post-Release Review

> **Submitted by** IoT Product Owner · **Approved by** CEO · **Consulted** Finance
> **Purpose of this gate:** decide the product's future against **measured** KPI performance. The T43 dashboard exists so this is a data review, not a storytelling session.
> **Decision options: Scale / Fix / Sunset** — different wording from every other gate.

---

# `<Product Name>` - 3-Month Post-Release Review

**Approval**

- [ ] `<IoT Product Owner name>` (prepared) - [DATE]
- [ ] `<CEO name>` (approved) - [DATE]

**Decision** — tick one

- [ ] **Scale** — proceed to full commercial scale
- [ ] **Fix** — return to `<T42 / named task>`. Corrective plan below. Re-review due: `<date>`
- [ ] **Sunset** — reason, installed base and migration plan below

**Release date:** [DATE] · **Submitted:** [DATE] · **SLA due:** [DATE + 3] · **Delegate:** `<name>`

# Background and Purpose

`<What shipped, when, to how many customers and units.>`

# KPI Performance vs Target

Targets come from the governing requirement's L1. Fill all three windows.

| KPI | L1 target | 30 day | 60 day | 90 day | Met? |
| --- | --- | --- | --- | --- | --- |
| Install success rate | | | | | |
| Uptime | | | | | |
| Data completeness | | | | | |
| RMA rate | | | | | |
| Attach rate | | | | | |
| Realised margin | | | | | |

> `RMA rate` is a tracked KPI, but T31 (RMA workflow and spare-parts plan) is **deferred** — expect this row to be hard to populate until that is closed.

# Install Quality Summary

From T42, first 20–50 installs.

| Metric | Result | Target |
| --- | --- | --- |
| Installs reviewed | | |
| First-time-right rate | | |
| Rework required | | |

**Corrective actions:**

| # | Issue | Action | Owner | Status |
| --- | --- | --- | --- | --- |
| | | | | |

# Financial Performance

| Item | Plan (T02/T36) | Actual | Variance |
| --- | --- | --- | --- |
| Units sold | | | |
| Revenue | | | |
| Landed cost per unit | | | |
| Realised gross margin | | | |

# Issues and Field Learnings

`<What we did not anticipate. Failure modes, support burden, customer complaints.>`

# Conclusion

`<Recommendation with the reasoning, tied to the KPI table above.>`

# Decision Criteria — agreed before this gate runs

| Outcome | Trigger |
| --- | --- |
| **Scale** | All must-hit KPIs met; realised margin within envelope; no unresolved systemic install or quality issue |
| **Fix** | KPIs missed but root cause identified and addressable, and the business case still holds after the fix cost |
| **Sunset** | KPIs missed with no viable fix, or realised margin cannot reach the envelope, or demand did not materialise |

# If Sunset

| Item | Value |
| --- | --- |
| Installed base at sunset | |
| Migration plan for installed base | `<link>` |
| Total sunk cost | |
| Customer communication plan | `<link>` |

# Decision Notes

---

# Appendix — gate summary

| Gate | Task | Stage | Decision options | Prepared by (R) | Approved by (A) | Lanes |
|---|---|---|---|---|---|---|
| GATE 1 | T02 | 0. Opportunity | Approve / Rework / Kill | IoT Product Owner | CEO | NPD, HW Upg |
| GATE 2 | T05 | 1. Pre-DoE | Approve / Rework / Kill | IoT Product Owner | CEO | NPD, FW Upg |
| GATE 3 | T11 | 2. DoE | Approve / Rework / Kill | IoT Engineer | CEO | NPD, HW Upg, SW Feat |
| GATE 4 | T13 | 2. DoE | Approve / Rework / Kill | IoT Engineer | CEO | NPD, HW Upg |
| GATE 5 | T24 | 3. Integration | Approve / Rework / Kill | IoT Product Owner | CEO | all four |
| GATE 6 | T27 | 4. PoC | Approve / Rework / Kill | IoT Product Owner | CEO | NPD, HW Upg |
| GATE 7 | T36 | 5. Pre-Comm | Approve / Rework | IoT Product Owner | CEO | NPD, HW Upg |
| GATE 8 | T44 | 7. Post-Comm | **Scale / Fix / Sunset** | IoT Product Owner | CEO | NPD, HW Upg |

**Non-CEO gates, no submission document:** T19 PRD Approval (A: CTO), T21 SW QC approval (A: SW Engineering), T22 Integration test approval (A: IoT Engineer), T33 Train Service Leader + certify installers (A: Head of Service), T35 Confirm SDPPI received (A: Procurement — a blocker check, not a discretionary gate).
