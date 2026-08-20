"""Churn cohort v2 -- data loading, reconciliation, and computation.

Loads McEasy's two CSV extracts and produces the record sets the workbook
writer consumes. No openpyxl here; this module is pure data so it can be
exercised on its own.

Verified points about these files:

  1. ARR annualization is `subtotal * 12`, regardless of billing frequency.
     `subtotal` is a MONTHLY-NORMALISED amount, not the amount per invoice.
     Verified three ways:
       - `subtotal == unit_price` in 100% of rows at every one of the 10
         billing frequencies, and `unit_price` is the monthly rate.
       - For churned lines matched to Nonaktif (whose `ARR Lost per
         Salesperson` is a known annual figure), the implied multiplier is
         median 12.00 for `/ Month`, `/ Year`, `/ 3 Months`, `/ 4 Months` and
         `/ 6 Months` alike -- not 12/period_months.
       - `multipler` is months-per-invoice; it scales the INVOICE amount
         (subtotal * multipler), not the annual run-rate.
     An earlier version of this script divided by the period length, which
     understated ARR by roughly IDR 20B and silently down-weighted every
     annually-billed line by 12x. Do not reintroduce that.

  2. Churn date in Subscription is `date_end`, not `accounting_date`.
     `accounting_date` equals `date_start`. `date_end` is NULL on every
     active row and populated only on churned ones -> right-censored panel.

  3. Nonaktif stores every line as exactly 2 rows (one per salesperson slot),
     and it mixes two incompatible conventions for split-commission deals:
       - 816 grains DUPLICATE the value (both slots carry the full amount)
       - 479 grains SPLIT it (the two slots sum to the real amount)
     So neither sum() nor max() is right on its own. Rule applied per grain:
     equal nonzero values -> duplicate -> take one; unequal -> split -> sum.
     Externally validated: Tempirai Energy Resources reconciles to the
     Subscription register to the rupiah under this rule (295,320,000) where
     naive summing gives exactly 2x that.

  4. `Unit Lost per Salesperson` is a commission ALLOCATION, not a vehicle
     count -- it takes fractional values (0.5, 0.4, 0.6, 0.8). Vehicles are
     counted as distinct (Account, nopol) instead: 14,109 churned vehicles,
     a hard count that no allocation convention can distort.

Console here is cp1252; keep stdout ASCII-only.
"""

from __future__ import annotations

import collections
import csv
import datetime as dt
from pathlib import Path

csv.field_size_limit(10 ** 9)

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

# Billing-cycle length in months, keyed on the `yearly/monthly` column.
# NOT used for ARR -- see module docstring point 1. Retained because billing
# frequency is a useful cut in its own right (96.5% of the active book bills
# monthly, which matters when pricing a prepay offer) and because an unknown
# value here signals a new frequency worth looking at.
PERIOD_MONTHS = {
    "/ Month": 1, "/ 2 Months": 2, "/ 3 Months": 3, "/ 4 Months": 4,
    "/ 6 Months": 6, "/ 10 Months": 10, "/ 11 Months": 11, "/ Year": 12,
    "/ 2 Years": 24, "/ 3 Years": 36,
}

# `subtotal` is a monthly-normalised amount at every billing frequency.
MONTHS_PER_YEAR = 12

SIZE_ORDER = ["A<=5", "B<=10", "C<=20", "D<=50", "E<=100", "F<400", "G>=400",
              "(unassigned)"]

# Reasons that are not a customer leaving: re-papering, ERP cleanup, or a plan
# change. Excluded from every churn figure per the requester's decision.
# NOTE: Downgrade is excluded from CHURN but retained as revenue contraction in
# the net-retention view -- it is real ARR loss and the most AM-addressable
# kind, so dropping it entirely would blind the program to it.
ADMIN_REASONS = {
    "Administrasi",
    "Administration - Pindah Quotation",
    "Churn Erp",
    "Downgrade",
    "Trial Pindah Ke Order",
    "Upgrade",
}
CONTRACTION_REASONS = {"Downgrade"}

# Excluded by explicit instruction: single largest churn event, distorts every
# segment average it touches (11.1% of gross churned ARR on its own).
EXCLUDE_CUSTOMERS = {"Corin Mulia Gemilang, PT"}

# Reason coding began mid-2024: blank rate is 96.6% in 2022, 93.3% in 2023,
# 32.2% in 2024, 0.0% in 2025-26. Reason-driven views are windowed from here.
REASON_WINDOW_START = "2025-01"

# Vehicle proxy on the active base. Subscription has no `nopol` and `qty` is
# always 1, so one GPS-mapped line stands in for one vehicle. Validated at
# +10.9% against Nonaktif's explicit unit count -- see reconcile().
GPS_MAPPINGS = {"GPS", "GPS Enterprise/PRO"}

# `Fleet Category` is a sales-CRM field describing the CUSTOMER'S TOTAL FLEET,
# not the vehicles they subscribe. Evidence: 87.3% of companies hold fewer
# subscribed vehicles than their band ceiling, and median penetration falls
# monotonically 67% (A<=5) -> 2% (G>=400). It is therefore the right field for
# "customer size" but the WRONG field for "how many vehicles we have".
# It is also partly stale: 12.7% of companies breach their own ceiling,
# including several of the largest accounts in the file (PERUM DAMRI carries
# 1,911 subscribed vehicles under a D<=50 label).
# So subscribed vehicles get their own derived band, used wherever the question
# is about McEasy's actual footprint rather than the customer's size.
VEH_BANDS = [(1, 5, "1-5 veh"), (6, 10, "6-10 veh"), (11, 20, "11-20 veh"),
             (21, 50, "21-50 veh"), (51, 100, "51-100 veh"),
             (101, 399, "101-399 veh"), (400, 10 ** 9, "400+ veh")]
VEH_ORDER = [lab for _lo, _hi, lab in VEH_BANDS] + ["0 veh (no GPS line)"]

# Band ceilings, for the penetration and breach diagnostics.
BAND_CEIL = {"A<=5": 5, "B<=10": 10, "C<=20": 20, "D<=50": 50, "E<=100": 100,
             "F<400": 399, "G>=400": 10 ** 9}
BAND_MID = {"A<=5": 3, "B<=10": 8, "C<=20": 15, "D<=50": 35, "E<=100": 75,
            "F<400": 250, "G>=400": 600}


def vehicle_band(n):
    if not n:
        return "0 veh (no GPS line)"
    for lo, hi, lab in VEH_BANDS:
        if lo <= n <= hi:
            return lab
    return "400+ veh"

# Reason -> intervention family. Groups 29 sales-entered labels into buckets an
# AM program can actually own. Substring match, first hit wins, case-folded.
REASON_BUCKETS = [
    ("kendala pembayaran", "Payment / Credit"),
    ("menunggak", "Payment / Credit"),
    ("tidak ingin melanjutkan renewal", "Renewal Decision"),
    ("tidak ingin harga naik", "Renewal Decision"),
    ("kontrak dengan vendor sudah habis", "Renewal Decision"),
    ("tidak ada kebutuhan lagi", "No Longer Needed"),
    ("unit dijual", "Fleet Event"),
    ("kondisi kendaraan", "Fleet Event"),
    ("pengembalian ke vendor", "Fleet Event"),
    ("ditarik leasing", "Fleet Event"),
    ("kendaraan tidak sedang dipakai", "Fleet Event"),
    ("device hilang", "Fleet Event"),
    ("kompetitor", "Competitor"),
    ("device bermasalah", "Product / Tech Failure"),
    ("device atau sensor tidak kompatible", "Product / Tech Failure"),
    ("kesalahan teknis", "Product / Tech Failure"),
    ("kesalahan pemasangan", "Product / Tech Failure"),
    ("aplikasi v2", "Product / Tech Failure"),
    ("produk tidak sesuai", "Value / Fit"),
    ("permintaan customer yang belum dapat dihandle", "Value / Fit"),
    ("layanan pelanggan yang buruk", "Service Failure"),
    ("hard contact", "Unreachable"),
    ("tidak lanjut trial", "Trial Lapse"),
]

BUCKET_ORDER = [
    "Payment / Credit", "Renewal Decision", "No Longer Needed", "Fleet Event",
    "Value / Fit", "Product / Tech Failure", "Competitor", "Service Failure",
    "Unreachable", "Trial Lapse", "(no reason recorded)",
]


def reason_bucket(reason: str) -> str:
    low = (reason or "").strip().lower()
    if not low:
        return "(no reason recorded)"
    for key, bucket in REASON_BUCKETS:
        if key in low:
            return bucket
    return "(no reason recorded)"


# --------------------------------------------------------------------------
# Parsing primitives
# --------------------------------------------------------------------------


def parse_date(value):
    """dd/mm/yyyy [hh:mm:ss] -> date, else None."""
    s = (value or "").strip()
    if not s:
        return None
    try:
        return dt.datetime.strptime(s[:10], "%d/%m/%Y").date()
    except ValueError:
        return None


def parse_num(value):
    """Handles thousands separators and the blank/#N/A sentinels."""
    s = (value or "").replace(",", "").strip()
    if s in ("", "-", "#N/A", "#REF!"):
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def month_key(d):
    return d.strftime("%Y-%m") if d else None


def months_between(a, b):
    """Whole months from a to b. Negative if b precedes a."""
    return (b.year - a.year) * 12 + (b.month - a.month)


# --------------------------------------------------------------------------
# Subscription extract -- the authoritative register
# --------------------------------------------------------------------------


def load_subscription(path: Path):
    """One record per subscription line. Carries both active and churned."""
    rows = []
    unknown_periods = collections.Counter()

    with open(path, encoding="utf-8-sig", newline="") as fh:
        for raw in csv.DictReader(fh):
            freq = (raw["yearly/monthly"] or "").strip()
            period = PERIOD_MONTHS.get(freq)
            if period is None:
                unknown_periods[freq] += 1
                period = 1
            arr = parse_num(raw["subtotal"]) * MONTHS_PER_YEAR

            start = parse_date(raw["date_start"])
            end = parse_date(raw["date_end"])
            status = (raw["Churn?"] or "").strip()
            band = (raw["Fleet Category"] or "").strip() or "(unassigned)"
            pmap = (raw["Product Mapping"] or "").strip() or "(unmapped)"

            rows.append({
                "company": (raw["company"] or "").strip(),
                "account_id": (raw["Account ID"] or "").strip(),
                "status": status,
                "arr": arr,
                "start": start,
                "end": end,
                "band": band,
                "pmap": pmap,
                "pcat": (raw["product category"] or "").strip(),
                "product": (raw["product"] or "").strip(),
                "industry": (raw["Industry"] or "").strip(),
                "province": (raw["provinsi"] or "").strip(),
                "term": int(parse_num(raw["contract_period"]) or 0),
                "point": parse_num(raw["Total Point"]),
                "is_veh": pmap in GPS_MAPPINGS,
                "freq": freq,
                "period_months": period,
                # filled by propagate_reasons()
                "reason": "", "reason_bucket": "", "match_level": "",
            })

    return rows, unknown_periods


# --------------------------------------------------------------------------
# Nonaktif extract -- source of Reason and true unit counts only
# --------------------------------------------------------------------------


def _clean(value):
    """Nonaktif `nopol` values carry a leading tab from the source export."""
    return (value or "").strip().strip("\t").strip()


def load_nonaktif(path: Path):
    """Dedup the salesperson-slot duplication, return one record per line.

    Grain is (Account, WO, nopol, Item, Deal No); 15,882 of 15,896 grains hold
    exactly 2 rows, one per salesperson slot. The file mixes two conventions
    for split deals, so the rule is decided per grain:

        all nonzero values equal -> DUPLICATE  -> take the single value
        values differ            -> TRUE SPLIT -> sum them

    Vehicles are NOT taken from `Unit Lost per Salesperson` (a fractional
    commission allocation). They are counted as distinct (Account, nopol).
    """
    n_raw = 0
    group_sizes = collections.Counter()
    seen = collections.defaultdict(list)
    attrs = {}

    with open(path, encoding="utf-8-sig", newline="") as fh:
        for raw in csv.DictReader(fh):
            n_raw += 1
            key = (
                _clean(raw["Account Name"]), _clean(raw["WO"]),
                _clean(raw["nopol"]), _clean(raw["Item"]),
                _clean(raw["Deal No"]),
            )
            seen[key].append((parse_num(raw["ARR Lost per Salesperson"]),
                              parse_num(raw["Unit Lost per Salesperson"])))
            # Attributes are identical across a grain's rows except that the
            # unpopulated salesperson slot blanks Group/Sales. Reason, dates and
            # bands repeat, so first-non-blank wins.
            a = attrs.setdefault(key, {})
            for field, col in (("reason", "Reason"), ("band", "Fleet Category"),
                               ("pcat", "Kategori"), ("pay_type", "Type Pembayaran")):
                if not a.get(field):
                    a[field] = _clean(raw[col])
            if "date" not in a:
                a["date"] = parse_date(raw["Accounting Date"])
                a["first_installed"] = parse_date(raw["First Installed"])
                a["month_diff"] = parse_num(raw["Month Diff"])

    recs = []
    n_dup = n_split = 0
    sum_all_arr = 0.0
    for key, vals in seen.items():
        group_sizes[len(vals)] += 1
        arrs = [a for a, _ in vals if a > 0]
        sum_all_arr += sum(a for a, _ in vals)
        if not arrs:
            arr = 0.0
        elif len(set(arrs)) == 1:
            arr = arrs[0]
            n_dup += 1 if len(arrs) > 1 else 0
        else:
            arr = sum(arrs)
            n_split += 1
        a = attrs[key]
        recs.append({
            "company": key[0], "wo": key[1], "nopol": key[2], "item": key[3],
            "arr": arr,
            "reason": a.get("reason", ""),
            "reason_bucket": reason_bucket(a.get("reason", "")),
            "date": a.get("date"),
            "first_installed": a.get("first_installed"),
            "band": a.get("band") or "(unassigned)",
            "pcat": a.get("pcat", ""),
            "pay_type": a.get("pay_type", ""),
            "month_diff": a.get("month_diff", 0.0),
        })

    vehicles = {(r["company"], r["nopol"]) for r in recs if r["nopol"]}
    dedup_arr = sum(r["arr"] for r in recs)

    meta = {
        "n_raw": n_raw,
        "n_grains": len(seen),
        "group_sizes": group_sizes,
        "n_duplicate_grains": n_dup,
        "n_split_grains": n_split,
        "sum_all_arr": sum_all_arr,
        "dedup_arr": dedup_arr,
        "dup_excess_arr": sum_all_arr - dedup_arr,
        "sum_all_units": sum(u for v in seen.values() for _, u in v),
        "n_vehicles": len(vehicles),
        "n_customers": len({r["company"] for r in recs}),
    }
    return recs, meta


# --------------------------------------------------------------------------
# Reason propagation, Nonaktif -> Subscription
# --------------------------------------------------------------------------


def propagate_reasons(sub_rows, non_recs):
    """Attach a Reason to each churned Subscription line.

    Cascade, tightest grain first, because company-level fallback will smear a
    dominant reason across lines that churned for different stated causes:
        L1  company + churn-month + product name
        L2  company + churn-month
        L3  company
    Within a key the ARR-dominant reason wins. Match level is retained per line
    so the workbook can report how much of the analysis rests on the loose
    fallbacks (5.6% at L3, 1.4% unmatched).
    """
    l1 = collections.defaultdict(collections.Counter)
    l2 = collections.defaultdict(collections.Counter)
    l3 = collections.defaultdict(collections.Counter)

    for r in non_recs:
        ym = month_key(r["date"])
        w = r["arr"] if r["arr"] > 0 else 1.0
        if ym:
            l1[(r["company"], ym, r["item"])][r["reason"]] += w
            l2[(r["company"], ym)][r["reason"]] += w
        l3[r["company"]][r["reason"]] += w

    coverage = collections.Counter()
    coverage_arr = collections.Counter()

    for row in sub_rows:
        if row["status"] != "churn":
            continue
        ym = month_key(row["end"])
        company = row["company"]
        hit = None
        for level, table, key in (
            ("L1 co+month+product", l1, (company, ym, row["product"])),
            ("L2 co+month", l2, (company, ym)),
            ("L3 co", l3, company),
        ):
            bucket = table.get(key)
            if bucket:
                hit = (level, bucket.most_common(1)[0][0])
                break

        level, reason = hit if hit else ("unmatched", "")
        row["match_level"] = level
        row["reason"] = reason
        row["reason_bucket"] = reason_bucket(reason)
        coverage[level] += 1
        coverage_arr[level] += row["arr"]

    return coverage, coverage_arr


# --------------------------------------------------------------------------
# Exclusions
# --------------------------------------------------------------------------


def classify_exclusion(row):
    """Why a churned line is out of the analysis base, or '' if it is in."""
    if row["company"] in EXCLUDE_CUSTOMERS:
        return "excluded customer"
    if row["reason"] in ADMIN_REASONS:
        return "admin reason"
    return ""


def apply_exclusions(sub_rows):
    """Split churned lines into the analysis base and the excluded pools.

    An excluded CUSTOMER is removed from both sides of every rate -- its active
    lines are flagged too. Dropping a customer's churn from the numerator while
    leaving its active ARR in the denominator is indefensible, and it is not a
    hypothetical: Corin Mulia Gemilang holds IDR 19.25B of active ARR, 91% of
    everything in the B<=10 band. Excluding only its churn made B<=10 look like
    the best-retaining band in the portfolio. It is not.
    """
    base, excluded = [], []
    for row in sub_rows:
        if row["company"] in EXCLUDE_CUSTOMERS:
            row["excluded"] = "excluded customer"
            if row["status"] == "churn":
                excluded.append(row)
            continue
        if row["status"] != "churn":
            row["excluded"] = ""
            continue
        why = classify_exclusion(row)
        row["excluded"] = why
        (excluded if why else base).append(row)
    return base, excluded


# --------------------------------------------------------------------------
# Customer-level rollup
# --------------------------------------------------------------------------


def build_customers(sub_rows, snapshot):
    """One record per company, with the full/partial/never-churned label.

    Status is evaluated AS OF THE SNAPSHOT, not as of any churn event. A company
    that fully churned in 2023 and came back in 2025 reads as 'partial'.
    """
    cust = collections.defaultdict(lambda: {
        "company": "", "arr_active": 0.0, "arr_churn": 0.0,
        "veh_active": 0, "veh_churn": 0,
        "lines_active": 0, "lines_churn": 0,
        "bands": collections.Counter(), "pmaps": collections.Counter(),
        "reasons": collections.Counter(), "terms": collections.Counter(),
        "starts": [], "ends": [], "industry": "", "province": "",
        "arr_churn_base": 0.0,
    })

    for row in sub_rows:
        if row["status"] == "not activated":
            continue
        c = cust[row["company"]]
        c["company"] = row["company"]
        c["industry"] = c["industry"] or row["industry"]
        c["province"] = c["province"] or row["province"]
        if row["start"]:
            c["starts"].append(row["start"])
        if row["status"] == "active":
            c["arr_active"] += row["arr"]
            c["veh_active"] += 1 if row["is_veh"] else 0
            c["lines_active"] += 1
            c["bands"][row["band"]] += row["arr"]
            c["pmaps"][row["pmap"]] += row["arr"]
            if row["term"]:
                c["terms"][row["term"]] += 1
        else:
            c["arr_churn"] += row["arr"]
            c["veh_churn"] += 1 if row["is_veh"] else 0
            c["lines_churn"] += 1
            c["bands"][row["band"]] += row["arr"]
            if not row.get("excluded"):
                c["arr_churn_base"] += row["arr"]
                c["reasons"][row["reason_bucket"]] += row["arr"]
            if row["end"]:
                c["ends"].append(row["end"])

    for c in cust.values():
        if c["arr_churn"] > 0 and c["arr_active"] <= 0:
            c["status"] = "full churn"
        elif c["arr_churn"] > 0:
            c["status"] = "partial churn"
        else:
            c["status"] = "never churned"
        # Resolve multi-band customers to their largest-ARR band, matching the
        # prior run's convention.
        c["band"] = c["bands"].most_common(1)[0][0] if c["bands"] else "(unassigned)"
        c["pmap"] = c["pmaps"].most_common(1)[0][0] if c["pmaps"] else "(unmapped)"
        c["reason_bucket"] = (c["reasons"].most_common(1)[0][0]
                              if c["reasons"] else "(no reason recorded)")
        c["term"] = c["terms"].most_common(1)[0][0] if c["terms"] else 0
        c["first_start"] = min(c["starts"]) if c["starts"] else None
        c["last_end"] = max(c["ends"]) if c["ends"] else None
        ref = c["last_end"] if c["status"] == "full churn" and c["last_end"] else snapshot
        c["tenure"] = (months_between(c["first_start"], ref)
                       if c["first_start"] else None)
        c["arr_total"] = c["arr_active"] + c["arr_churn"]

        # Subscribed footprint, all-time, and the CRM band's implied fleet size.
        c["veh_total"] = c["veh_active"] + c["veh_churn"]
        c["veh_band"] = vehicle_band(c["veh_total"])
        ceil_ = BAND_CEIL.get(c["band"])
        c["band_breach"] = bool(ceil_ and c["veh_total"] > ceil_)
        mid = BAND_MID.get(c["band"])
        c["penetration"] = (c["veh_total"] / mid) if mid else None

    # Propagate the customer's derived vehicle band down to its lines, so
    # line-grain views can cut on actual footprint too.
    for row in sub_rows:
        c = cust.get(row["company"])
        row["veh_band"] = c["veh_band"] if c else "0 veh (no GPS line)"

    return dict(cust)


# --------------------------------------------------------------------------
# Kaplan-Meier
# --------------------------------------------------------------------------


def kaplan_meier(events, horizon):
    """events: [(observed_tenure_months, churned_bool, weight)].

    Returns per-month at-risk, event, hazard, and survival series.

    A unit contributes to the at-risk set at every month it was observed to
    reach. Censored units (still active at the snapshot) leave the denominator
    without ever appearing in the numerator -- that is the whole point, and it
    is what the prior churn-only run could not do.
    """
    at_risk = [0.0] * (horizon + 1)
    ev = [0.0] * (horizon + 1)

    for tenure, churned, weight in events:
        if tenure is None or tenure < 0:
            continue
        t = min(int(tenure), horizon)
        for m in range(0, t + 1):
            at_risk[m] += weight
        if churned and int(tenure) <= horizon:
            ev[t] += weight

    hazard, survival = [0.0] * (horizon + 1), [1.0] * (horizon + 1)
    s = 1.0
    for m in range(horizon + 1):
        h = ev[m] / at_risk[m] if at_risk[m] > 0 else 0.0
        hazard[m] = h
        s *= (1.0 - h)
        survival[m] = s
    return {"at_risk": at_risk, "events": ev, "hazard": hazard,
            "survival": survival, "horizon": horizon}


def line_events(sub_rows, snapshot, base_only=True):
    """Build KM input at subscription-line grain, ARR-weighted and unweighted.

    Lines within one customer are not independent, so line-level survival
    understates real uncertainty. It is still the right grain for ARR-weighted
    risk because that is what the money follows. Customer-level KM is computed
    separately for logo survival.
    """
    out_arr, out_cnt, out_veh = [], [], []
    for row in sub_rows:
        if row["status"] == "not activated" or not row["start"]:
            continue
        if base_only and row["company"] in EXCLUDE_CUSTOMERS:
            continue          # out of both numerator and denominator
        if row["status"] == "churn":
            if base_only and row.get("excluded"):
                continue
            if not row["end"]:
                continue
            tenure, churned = months_between(row["start"], row["end"]), True
        else:
            tenure, churned = months_between(row["start"], snapshot), False
        if tenure < 0:
            continue
        out_arr.append((tenure, churned, row["arr"]))
        out_cnt.append((tenure, churned, 1.0))
        if row["is_veh"]:
            out_veh.append((tenure, churned, 1.0))
    return out_arr, out_cnt, out_veh


def customer_events(customers):
    """Logo survival: a customer is an event only on FULL churn."""
    out = []
    for c in customers.values():
        if c["tenure"] is None or c["tenure"] < 0:
            continue
        if c["company"] in EXCLUDE_CUSTOMERS:
            continue
        out.append((c["tenure"], c["status"] == "full churn", 1.0))
    return out


# --------------------------------------------------------------------------
# Aggregation helpers
# --------------------------------------------------------------------------


def blank_cell():
    return {"arr": 0.0, "veh": 0, "lines": 0, "cust": set()}


def crosstab(rows, rowkey, colkey):
    """Nested dict[row][col] -> measures. Customer counts are sets, so the
    margins on a customer-count view are deliberately NOT additive."""
    table = collections.defaultdict(lambda: collections.defaultdict(blank_cell))
    for r in rows:
        cell = table[rowkey(r)][colkey(r)]
        cell["arr"] += r["arr"]
        cell["veh"] += 1 if r.get("is_veh") else 0
        cell["lines"] += 1
        cell["cust"].add(r["company"])
    return table


def totals(rows):
    return {
        "arr": sum(r["arr"] for r in rows),
        "veh": sum(1 for r in rows if r.get("is_veh")),
        "lines": len(rows),
        "cust": len({r["company"] for r in rows}),
    }


def concentration(rows, key=lambda r: r["company"]):
    """Ranked contributors plus the n-for-50%/80% counts."""
    by = collections.defaultdict(float)
    veh = collections.defaultdict(int)
    for r in rows:
        by[key(r)] += r["arr"]
        veh[key(r)] += 1 if r.get("is_veh") else 0
    ranked = sorted(by.items(), key=lambda kv: -kv[1])
    total = sum(by.values())
    n50 = n80 = None
    cum = 0.0
    for i, (_, v) in enumerate(ranked, 1):
        cum += v
        if n50 is None and total and cum >= 0.5 * total:
            n50 = i
        if n80 is None and total and cum >= 0.8 * total:
            n80 = i
    return {"ranked": ranked, "veh": veh, "total": total,
            "n50": n50, "n80": n80, "n": len(ranked)}


def dominance(rows, binkey):
    """Largest single customer's share of each bin. Guards against calling a
    one-account event a lifecycle pattern (the prior run had three such bins)."""
    per_bin = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in rows:
        per_bin[binkey(r)][r["company"]] += r["arr"]
    out = {}
    for b, cust in per_bin.items():
        tot = sum(cust.values())
        top, top_v = max(cust.items(), key=lambda kv: kv[1])
        out[b] = {"total": tot, "top": top, "top_share": (top_v / tot) if tot else 0.0,
                  "n_cust": len(cust)}
    return out


TENURE_BINS = [(0, 3), (3, 6), (6, 12), (12, 18), (18, 24), (24, 30),
               (30, 36), (36, 48), (48, 10 ** 6)]


def tenure_label(m):
    if m is None or m < 0:
        return "(no/bad start date)"
    for lo, hi in TENURE_BINS:
        if lo <= m < hi:
            return "48+ mo" if hi == 10 ** 6 else "%d-%d mo" % (lo, hi)
    return "48+ mo"


TENURE_ORDER = ["0-3 mo", "3-6 mo", "6-12 mo", "12-18 mo", "18-24 mo",
                "24-30 mo", "30-36 mo", "36-48 mo", "48+ mo",
                "(no/bad start date)"]


def line_tenure(row, snapshot):
    if not row["start"]:
        return None
    ref = row["end"] if row["status"] == "churn" and row["end"] else snapshot
    return months_between(row["start"], ref)
