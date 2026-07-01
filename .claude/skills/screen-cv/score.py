#!/usr/bin/env python3
"""Deterministic scorer for the screen-cv skill.

WHY THIS EXISTS
---------------
The percentage and tier used to be computed by the LLM screener by hand. That
caused the same CV to land in different tiers across runs (e.g. one run divided
by the wrong "max possible" total and bumped a candidate from "Good fit" to
"Best fit"). Computers never miscount, so the arithmetic lives here instead.

The cv-screener agent now supplies ONLY raw judgments:
  - must_haves:  M-id -> "met" | "partial" | "missing"
  - nice_to_haves: N-id -> {"raw": 0..3, "weight": int}
  - red_flags: [{"detected": bool, "severity": "note"|"concern"|"disqualify"}]
This script fills in score_pct and tier with a fixed formula.

USAGE
-----
  python score.py records.json            # read from file
  cat records.json | python score.py      # or from stdin
Input may be a single record object or a JSON array of records.
Output is the enriched JSON array on stdout.
"""
import sys
import json


def score_record(rec):
    # Parse-error records are passed straight through, untouched by the math.
    if rec.get("parse_error") or rec.get("tier") == "Parse error":
        rec["tier"] = "Parse error"
        rec["score_pct"] = -1
        return rec

    # --- Nice-to-haves: weighted sum and max possible -----------------------
    # max possible is ALWAYS (sum of weights) x 3, because each criterion is
    # capped at a raw score of 3. This is the line the LLM used to get wrong.
    nth = rec.get("nice_to_haves", {}) or {}
    achieved = 0
    max_possible = 0
    for v in nth.values():
        raw = v.get("raw", 0) or 0
        weight = v.get("weight", 0) or 0
        raw = max(0, min(3, raw))          # clamp into 0..3
        weighted = raw * weight
        v["weighted"] = weighted           # normalise so the sheet matches
        achieved += weighted
        max_possible += 3 * weight

    pct = round(achieved / max_possible * 100, 1) if max_possible else 0.0

    # --- Must-haves: a "partial" counts as missing for tier capping ---------
    mh = rec.get("must_haves", {}) or {}
    missing = sum(1 for status in mh.values() if status != "met")

    # --- Red flags ----------------------------------------------------------
    flags = rec.get("red_flags", []) or []
    has_disqualify = any(f.get("detected") and f.get("severity") == "disqualify" for f in flags)
    has_concern = any(f.get("detected") and f.get("severity") == "concern" for f in flags)

    # --- Tier (rubric thresholds, applied in strict precedence) -------------
    if missing >= 2 or has_disqualify:
        tier = "Not a fit"
    elif missing == 1 or has_concern or pct < 50:
        tier = "Moderate fit"
    elif pct >= 80:
        tier = "Best fit"
    else:                                  # 50 <= pct < 80, all must-haves met
        tier = "Good fit"

    rec["score_pct"] = pct
    rec["tier"] = tier
    rec["_score_detail"] = {
        "achieved_weighted": achieved,
        "max_possible_weighted": max_possible,
        "must_haves_missing": missing,
        "disqualifying_flag": has_disqualify,
        "concern_flag": has_concern,
    }
    return rec


def main():
    raw = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding="utf-8").read()
    records = json.loads(raw)
    if isinstance(records, dict):
        records = [records]
    scored = [score_record(r) for r in records]
    json.dump(scored, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
