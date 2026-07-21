"""Forward-pass scheduler over the inferred dependency map.

The workbook has no predecessor column, so the links below are inferred. They are
published for correction in 02-gantt-dependencies.md - edit there and here together.

Computes earliest start / finish per task per lane, finds the longest path, and
compares it against the workbook's own stated totals so any disagreement between
the inferred dependencies and the sheet's arithmetic is visible rather than silent.

Usage:
    python schedule.py
"""

import json
from pathlib import Path

MATRIX = Path(__file__).with_name("matrix.json")

# Inferred predecessors, keyed by task. Applied per lane: any predecessor not
# present in a lane is skipped, and the task falls back to its nearest present
# ancestor. See 02-gantt-dependencies.md for the basis and confidence of each.
DEPS = {
    "T01": [],
    "T02": ["T01"],
    "T04": ["T02"],
    "T05": ["T04"],
    "T06": ["T05"],
    "T07": ["T06"],
    "T08": ["T07"],
    "T09": ["T08"],
    "T10": ["T09"],
    "T11": ["T10"],
    "T12": ["T11"],
    "T13": ["T12"],
    "T14": ["T13"],          # design freeze - governance-stated
    "T15": ["T13"],
    "T16": ["T15"],          # cost checkpoint precedes integration spend
    "T17": ["T16"],
    "T18": ["T17"],
    "T19": ["T18"],
    "T20": ["T19"],          # governance-stated: no build without approved PRD
    "T21": ["T20"],
    "T22": ["T21"],
    "T23": ["T22"],
    "T24": ["T23"],
    "T25": ["T24"],
    "T26": ["T25"],
    "T27": ["T26"],
    "T28": ["T25"],          # governance-stated: parallel to PoC
    "T29": ["T25"],          # governance-stated: parallel to PoC
    "T30": ["T25"],
    "T33": ["T29"],
    "T34": ["T33"],
    "T35": ["T27", "T14"],   # governance-stated: certificate must be in hand
    "T36": ["T35"],
    "T37": ["T36"],
    "T38": ["T37", "T30"],
    "T39": ["T36"],
    "T40": ["T38"],
    "T41": ["T38"],
    "T42": ["T41"],          # install review starts once units are in the field
    "T43": ["T41"],          # KPI tracking starts at launch, parallel to T42
    "T44": ["T43", "T42"],   # 3-month review needs the 90d KPI data
    "T45": ["T44"],
}

LANES = {
    "full_npd": "Full NPD",
    "hw_upgrade": "New Vendor / HW Upgrade",
    "fw_upgrade": "FW Upgrade",
    "new_sw_feature": "New SW Feature",
}


def resolve(task_id, present, cache=None):
    """Nearest predecessors that exist in this lane, walking up when one is absent."""
    cache = cache if cache is not None else {}
    if task_id in cache:
        return cache[task_id]
    out = []
    for pred in DEPS.get(task_id, []):
        if pred in present:
            out.append(pred)
        else:
            out.extend(resolve(pred, present, cache))
    out = sorted(set(out))
    cache[task_id] = out
    return out


def schedule(tasks):
    """Forward pass. Returns {id: (start_day, finish_day)} with day 0 = kickoff."""
    present = {t["id"] for t in tasks}
    by_id = {t["id"]: t for t in tasks}
    cache = {}
    times = {}

    def finish(task_id):
        if task_id in times:
            return times[task_id][1]
        preds = resolve(task_id, present, cache)
        start = max((finish(p) for p in preds), default=0)
        end = start + by_id[task_id]["days"]
        times[task_id] = (start, end)
        return end

    for task_id in present:
        finish(task_id)
    return times, cache


def longest_path(tasks, times, cache):
    present = {t["id"] for t in tasks}
    end_task = max(present, key=lambda t: times[t][1])
    chain = [end_task]
    while True:
        preds = resolve(chain[-1], present, cache)
        if not preds:
            break
        driver = max(preds, key=lambda p: times[p][1])
        if times[driver][1] != times[chain[-1]][0]:
            break
        chain.append(driver)
    return list(reversed(chain))


TRACK_ORDER = ["Main", "Certification", "Commercial", "Service", "Supply"]


def emit_gantt(label, tasks, times):
    """Mermaid gantt, day-offset axis, one section per Track."""
    lines = [
        "```mermaid",
        "gantt",
        f"  title {label} - working days from kickoff (Day 0)",
        "  dateFormat X",
        "  axisFormat %s",
        "  todayMarker off",
    ]
    for track in TRACK_ORDER:
        in_track = [t for t in tasks if t["track"] == track]
        if not in_track:
            continue
        lines.append(f"  section {track}")
        for t in sorted(in_track, key=lambda x: (times[x["id"]][0], x["id"])):
            start, finish = times[t["id"]]
            pic = t["responsible"][0] if t["responsible"] else "?"
            if len(t["responsible"]) > 1:
                pic += " + " + t["responsible"][1]
            name = t["task"].replace(":", " -").replace("(", "").replace(")", "")
            prefix = "GATE " if t["is_gate"] else ""
            tag = "crit, " if t["critical_path"] else ""
            lines.append(
                f"    {prefix}{t['id']} {name} [{pic}] :{tag}{start}, {finish}"
            )
    lines.append("```")
    return "\n".join(lines)


def main():
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    all_tasks = [t for t in data["tasks"] if t["status"] != "Deferred"]

    for key, label in LANES.items():
        tasks = [t for t in all_tasks if key in t["lanes"]]
        times, cache = schedule(tasks)
        chain = longest_path(tasks, times, cache)
        span = max(f for _, f in times.values())
        sheet_crit = sum(t["days"] for t in tasks if t["critical_path"])
        sheet_total = sum(t["days"] for t in tasks)

        print(f"\n=== {label}  ({len(tasks)} tasks)")
        print(f"  computed elapsed span      : {span} working days")
        print(f"  workbook 'critical path'   : {sheet_crit} d")
        print(f"  workbook 'total incl. par' : {sheet_total} d  (naive sum of all durations)")
        print(f"  longest path: {' -> '.join(chain)}")

        # Float on the certification track - how much T14 can slip before it bites.
        if "T14" in times:
            t14_start, t14_end = times["T14"]
            t35_start = times["T35"][0]
            print(f"  T14 cert: day {t14_start}-{t14_end}, needed by day {t35_start}"
                  f"  -> float {t35_start - t14_end} d"
                  f"  (becomes critical above {t35_start - t14_start} d duration)")

    print("\n--- task-level schedule, Full NPD ---")
    tasks = [t for t in all_tasks if "full_npd" in t["lanes"]]
    times, _ = schedule(tasks)
    for t in sorted(tasks, key=lambda x: (times[x["id"]][0], x["id"])):
        s, f = times[t["id"]]
        print(f"  {t['id']}  d{s:>4}-{f:<4} {t['days']:>3}d  {t['track']:<14} "
              f"{'GATE ' if t['is_gate'] else '     '}{t['task'][:44]}")


if __name__ == "__main__":
    main()
