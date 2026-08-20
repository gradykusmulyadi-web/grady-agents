---
name: record-pricing
description: Record one or more vendor pricing quotes (PDF or .xlsx) into the running vendor pricing master workbook. Use when the user runs /record-pricing, or asks to log/track/record a vendor quote or price proposal.
---

You are the **/record-pricing** skill. You are a thin entry point — all the real work
(extraction judgment + deterministic merge) lives in the `vendor-price-tracker` agent and
its `merge.py` script.

## Steps

1. **Resolve input file(s).** The user passes one or more file paths (PDF and/or `.xlsx`)
   as arguments. If no path was given, ask which vendor quote file(s) to process — don't
   guess at a path.
2. **Sanity-check the file(s) exist** and have a plausible extension (`.pdf`, `.xlsx`,
   `.xls`). If a path doesn't exist or isn't a document type this pipeline handles, say so
   and stop rather than passing it through.
3. **Invoke the `vendor-price-tracker` agent** with the resolved file path(s). Let it handle
   extraction, category/peripheral judgment, and running
   `.claude/skills/record-pricing/merge.py`.
4. **Relay the agent's summary back to the user** essentially as-is — new rows per tab,
   superseded prices, any currency codes that were added with a placeholder 1.0 rate and
   need a real rate set in the `Currency Master` tab of
   `outputs/vendor_pricing_master.xlsx`.

Don't try to parse the vendor document yourself in this skill — that's the agent's job.
Don't touch `outputs/vendor_pricing_master.xlsx` directly.
