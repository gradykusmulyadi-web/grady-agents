"""Churn cohort v2 -- turns the loaded records into the tables the workbook writes.

Everything here is derived. No file IO, no formatting, so the numbers can be
checked in isolation. Assertions are hard failures: a margin that does not tie
should stop the run, not print a warning nobody reads.
"""

from __future__ import annotations

import collections
import statistics

import core

HORIZON = 48
MIN_CELL_ARR = 100e6          # below this an active base is too small to rate

# Right-censoring guard. Observation ends at the snapshot, so accounts can only
# be seen churning at ages they have reached. By tenure month 40 barely 5% of
# the month-0 ARR is still under observation, and a single mid-size churn there
# swings the hazard by a percentage point. Any month whose at-risk pool has
# fallen below this share of the month-0 pool is reported but marked thin, and
# is excluded from peak-finding and phase indices. The first run of this script
# put "peak hazard at month 40" in its output; that was this artifact.
STABLE_MIN_SHARE = 0.15

PHASES = [("Months 0-5 (onboarding)", 0, 6),
          ("Months 6-11 (first renewal run-up)", 6, 12),
          ("Months 12-19 (early year 2)", 12, 20),
          ("Months 20-27 (year-2 exit window)", 20, 28),
          ("Months 28-47 (thin -- read with care)", 28, 48)]
COHORT_STEPS = [3, 6, 12, 18, 24, 30, 36, 42, 48]

# Product families: `Product Mapping` already collapses 87 product names into 24
# values, but the tail is long and thin. Keep the ones that carry real ARR and
# lump the accessories, otherwise every cross-tab is 24 columns of noise.
KEEP_FAMILIES = ["GPS", "GPS Enterprise/PRO", "TV", "MDVR", "Fuel", "Temp",
                 "Door", "Easy Lock", "TMS"]


def family(pmap):
    return pmap if pmap in KEEP_FAMILIES else "Other / accessory"


FAMILY_ORDER = KEEP_FAMILIES + ["Other / accessory"]


def pct(a, b):
    return (a / b) if b else 0.0


def median_or_zero(xs):
    return statistics.median(xs) if xs else 0.0


def surv_share(km, m):
    """At-risk pool at month m as a share of that subgroup's own month-0 pool.

    The whole-portfolio censoring guard is not enough: a SUBGROUP can be far
    younger than the portfolio and its long-horizon survival then measures
    nothing. 36-month contracts are the live example -- barely sold before 2024,
    so by tenure month 24 only 7.5% of their starting ARR had been observed that
    long, and their 98% 24-month survival is an artifact of youth, not evidence
    that long contracts retain. Anyone reading that number as a pricing signal
    would be badly wrong, so every per-subgroup survival figure is checked here.
    """
    a0 = km["at_risk"][0]
    return (km["at_risk"][m] / a0) if a0 else 0.0


def surv_thin(km, m):
    return surv_share(km, m) < STABLE_MIN_SHARE


def cond_hazard(km, t, span=12):
    """P(churn within `span` months | survived to month t). The conditional form
    is what a target list needs: an account already 20 months in is not exposed
    to months 0-19 any more."""
    t = max(0, min(int(t), HORIZON))
    e = min(t + span, HORIZON)
    s_t, s_e = km["survival"][t], km["survival"][e]
    return 1.0 - (s_e / s_t) if s_t > 0 else 0.0


def build_context(sub, non, non_meta, coverage, coverage_arr, base, excluded,
                  customers, snapshot, gap_detail):
    ctx = {}
    # `active` is the RATE DENOMINATOR, so the excluded customer leaves it too.
    active_all = [r for r in sub if r["status"] == "active"]
    active = [r for r in active_all if r["company"] not in core.EXCLUDE_CUSTOMERS]
    churn_all = [r for r in sub if r["status"] == "churn"]
    excluded_active_arr = sum(r["arr"] for r in active_all
                              if r["company"] in core.EXCLUDE_CUSTOMERS)

    for r in sub:
        r["family"] = family(r["pmap"])

    # Rate views run on customers excluding the excluded ones; the target list
    # keeps them, because operationally they still matter.
    rate_customers = {k: v for k, v in customers.items()
                      if k not in core.EXCLUDE_CUSTOMERS}
    ctx["excluded_active_arr"] = excluded_active_arr
    ctx["rate_customers"] = rate_customers

    gross_churn = sum(r["arr"] for r in churn_all)
    base_churn = sum(r["arr"] for r in base)
    active_arr = sum(r["arr"] for r in active)   # excludes EXCLUDE_CUSTOMERS
    exc_admin = sum(r["arr"] for r in excluded if r["excluded"] == "admin reason")
    exc_customer = sum(r["arr"] for r in excluded if r["excluded"] == "excluded customer")
    downgrade = [r for r in excluded if r["reason"] in core.CONTRACTION_REASONS
                 and r["excluded"] == "admin reason"]
    exc_downgrade = sum(r["arr"] for r in downgrade)

    ctx.update(snapshot=snapshot, non_meta=non_meta, coverage=coverage,
               coverage_arr=coverage_arr, customers=customers,
               gross_churn=gross_churn, base_churn=base_churn, active_arr=active_arr,
               exc_admin=exc_admin, exc_customer=exc_customer,
               exc_downgrade=exc_downgrade,
               n_sub_rows=len(sub), n_active_lines=len(active),
               n_nonmonthly=sum(1 for r in sub if r["period_months"] != 1),
               n_yearly=sum(1 for r in sub if r["freq"] == "/ Year"))

    # ---------------- vehicle proxy bias ----------------
    churn_gps = sum(1 for r in churn_all if r["is_veh"])
    ctx["veh_bias"] = 100.0 * (churn_gps - non_meta["n_vehicles"]) / non_meta["n_vehicles"]
    ctx["churn_gps_lines"] = churn_gps

    # ---------------- controls + bridge ----------------
    starts = [r["start"] for r in sub if r["start"]]
    ends = [r["end"] for r in churn_all if r["end"]]
    ctx["controls"] = [
        ("Subscription rows (subscription lines)", len(sub), "rows", "One row = one subscription line; qty is always 1."),
        ("  of which active", len(active), "rows", "date_end is NULL on every one -- these are the censored observations."),
        ("  of which churned", len(churn_all), "rows", "date_end populated = the churn date."),
        ("  of which not activated", sum(1 for r in sub if r["status"] == "not activated"), "rows", "Never billed; excluded from all views."),
        ("Distinct companies (Subscription)", len({r["company"] for r in sub}), "companies", "Never count customers by counting rows."),
        ("Active ARR (annualised), analysis denominator", active_arr, "IDR", "The denominator v1 did not have. Excludes the excluded customer."),
        ("Active ARR held by the excluded customer", excluded_active_arr, "IDR", "Removed from BOTH sides of every rate. It is %.1f%% of the total active base, so leaving it in the denominator while dropping its churn from the numerator would have understated churn badly -- it materially changes the segment picture." % (100 * pct(excluded_active_arr, excluded_active_arr + active_arr))),
        ("Gross churned ARR (annualised)", gross_churn, "IDR", "Before any exclusion."),
        ("Analysis-base churned ARR", base_churn, "IDR", "After admin-reason and excluded-customer removal."),
        ("Nonaktif raw rows", non_meta["n_raw"], "rows", "Two rows per line (salesperson slots)."),
        ("Nonaktif deduped lines", non_meta["n_grains"], "lines", "Grain: Account + WO + nopol + Item + Deal No."),
        ("Nonaktif deduped ARR", non_meta["dedup_arr"], "IDR", "Per-grain convention detection; see gap bridge."),
        ("Nonaktif churned vehicles", non_meta["n_vehicles"], "vehicles", "Distinct (Account, nopol) -- a hard count, allocation-proof."),
        ("Observation window (starts)", "%s .. %s" % (min(starts), max(starts)), "", "Subscription line start dates."),
        ("Observation window (churn)", "%s .. %s" % (min(ends), max(ends)), "", "date_end range."),
        ("Snapshot / censoring date", str(snapshot), "", "Active lines are censored here."),
    ]

    residual = gross_churn - (non_meta["dedup_arr"] - gap_detail["absent_arr"]
                              - gap_detail["active_arr"] + gap_detail["sub_only_arr"])
    # kind: 'start' and 'delta' rows sum to the 'end' row. 'subtotal' rows are
    # running totals shown for readability and are NOT part of the sum.
    ctx["bridge"] = [
        ("Nonaktif, naive sum of all rows", non_meta["sum_all_arr"], "start",
         "What summing the file gives. Wrong: double-counts split-commission deals."),
        ("less salesperson-slot duplication", -non_meta["dup_excess_arr"], "delta",
         "%d duplicate grains. Validated to the rupiah against Subscription on Tempirai and Indosarana." % non_meta["n_duplicate_grains"]),
        ("= Nonaktif, deduped", non_meta["dedup_arr"], "subtotal",
         "The defensible Nonaktif figure. Running total, not an adjustment."),
        ("less accounts absent from Subscription entirely", -gap_detail["absent_arr"], "delta",
         "%d accounts. In Nonaktif but with no Subscription record at all." % gap_detail["absent_n"]),
        ("less accounts Subscription still shows as active", -gap_detail["active_arr"], "delta",
         "%d accounts churned per Nonaktif but carrying only active Subscription lines. A genuine register disagreement -- raise with the data owner." % gap_detail["active_n"]),
        ("plus accounts churned in Subscription but absent from Nonaktif", gap_detail["sub_only_arr"], "delta",
         "%d accounts." % gap_detail["sub_only_n"]),
        ("residual per-account valuation differences", residual, "delta",
         "Bidirectional, %.1f%% of the authoritative figure. Pricing/period basis. Disclosed, not reconciled to zero." % (100 * pct(abs(residual), gross_churn))),
        ("= Subscription churned ARR (authoritative)", gross_churn, "end",
         "Numerator and denominator both come from this register."),
    ]
    chain = sum(v for _l, v, k, _n in ctx["bridge"] if k in ("start", "delta"))
    assert abs(chain - gross_churn) < 1.0, \
        "gap bridge does not tie: chain %.2f vs authoritative %.2f" % (chain, gross_churn)

    # ---------------- blank reason by year ----------------
    by_year = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for r in churn_all:
        if not r["end"]:
            continue
        y = str(r["end"].year)
        by_year[y][0] += r["arr"]
        if not r["reason"]:
            by_year[y][1] += r["arr"]
        if r["reason"] in core.ADMIN_REASONS:
            by_year[y][2] += r["arr"]
    ctx["blank_by_year"] = [(y, v[0], pct(v[1], v[0]), pct(v[2], v[0]))
                            for y, v in sorted(by_year.items())]

    # ---------------- Kaplan-Meier ----------------
    ev_arr, ev_cnt, ev_veh = core.line_events(sub, snapshot, base_only=True)
    ctx["km_arr"] = core.kaplan_meier(ev_arr, HORIZON)
    ctx["km_cnt"] = core.kaplan_meier(ev_cnt, HORIZON)
    ctx["km_veh"] = core.kaplan_meier(ev_veh, HORIZON)
    ctx["km_logo"] = core.kaplan_meier(core.customer_events(customers), HORIZON)
    km = ctx["km_arr"]
    ctx["overall_24"] = 1.0 - km["survival"][24]

    # Censoring guard: which tenure months still carry enough at-risk ARR to
    # read a hazard off. Everything downstream that ranks or indexes hazards
    # uses only these months.
    a0 = km["at_risk"][0]
    ctx["at_risk_share"] = [pct(km["at_risk"][m], a0) for m in range(HORIZON + 1)]
    stable = [m for m in range(1, HORIZON + 1)
              if ctx["at_risk_share"][m] >= STABLE_MIN_SHARE]
    ctx["stable_months"] = set(stable)
    ctx["last_stable_month"] = max(stable) if stable else 0
    ctx["stable_min_share"] = STABLE_MIN_SHARE
    ctx["peak_month"] = max(stable, key=lambda m: km["hazard"][m]) if stable else 0
    ctx["peak_hazard"] = km["hazard"][ctx["peak_month"]]

    overall_mean_h = statistics.mean([km["hazard"][m] for m in stable]) if stable else 0.0
    ctx["overall_mean_hazard"] = overall_mean_h
    base_tenures = {}
    for r in base:
        t = core.line_tenure(r, snapshot)
        base_tenures[id(r)] = t
    phases = []
    for label, lo, hi in PHASES:
        months = [m for m in range(lo, min(hi, HORIZON + 1))]
        thin = [m for m in months if m not in ctx["stable_months"] and m > 0]
        hs = [km["hazard"][m] for m in months]
        mean_h = statistics.mean(hs) if hs else 0.0
        amt = sum(r["arr"] for r in base
                  if base_tenures[id(r)] is not None and lo <= base_tenures[id(r)] < hi)
        phases.append({"label": label, "mean_h": mean_h,
                       "index": pct(mean_h, overall_mean_h), "arr": amt,
                       "share": pct(amt, base_churn),
                       "thin": len(thin) > len(months) / 2})
    ctx["phases"] = phases

    def km_subset(pred):
        e, _, _ = core.line_events([r for r in sub if pred(r)], snapshot, base_only=True)
        return core.kaplan_meier(e, HORIZON)

    rated = [r for r in sub if r["status"] in ("active", "churn")
             and r["company"] not in core.EXCLUDE_CUSTOMERS]
    band_keys = [b for b in core.SIZE_ORDER if any(r["band"] == b for r in rated)]
    ctx["band_keys"] = band_keys
    ctx["km_by_band"] = [(b, km_subset(lambda r, b=b: r["band"] == b)) for b in band_keys]

    fam_keys = [f for f in FAMILY_ORDER if any(r["family"] == f for r in rated)]
    ctx["product_keys"] = fam_keys
    ctx["km_by_product"] = [(f, km_subset(lambda r, f=f: r["family"] == f)) for f in fam_keys]
    ctx["thin_families"] = {f for f, k in ctx["km_by_product"] if k["at_risk"][0] < MIN_CELL_ARR}
    ctx["thin_bands"] = {b for b, k in ctx["km_by_band"] if k["at_risk"][0] < MIN_CELL_ARR}
    km_band = dict(ctx["km_by_band"])
    km_fam = dict(ctx["km_by_product"])

    # ---------------- rates by segment ----------------
    ctx["gross_overall"] = pct(base_churn, base_churn + active_arr)

    def rate_rows(keyfn, keys, km_map):
        out = []
        for k in keys:
            a = sum(r["arr"] for r in active if keyfn(r) == k)
            c = sum(r["arr"] for r in base if keyfn(r) == k)
            la = sum(1 for r in active if keyfn(r) == k)
            lc = sum(1 for r in base if keyfn(r) == k)
            cust_a = len({cu["company"] for cu in rate_customers.values()
                          if cu["status"] != "full churn" and cu.get("band") == k}) \
                if keyfn is _band else 0
            cust_f = len({cu["company"] for cu in rate_customers.values()
                          if cu["status"] == "full churn" and cu.get("band") == k}) \
                if keyfn is _band else 0
            kmk = km_map[k]
            out.append({"key": k, "active": a, "churn": c, "gross": pct(c, a + c),
                        "km24": 1.0 - kmk["survival"][24],
                        "km24_share": surv_share(kmk, 24),
                        "km24_thin": surv_thin(kmk, 24),
                        "lines_active": la, "lines_churn": lc,
                        "logos_active": cust_a, "logos_full": cust_f,
                        "logo_rate": pct(cust_f, cust_a + cust_f)})
        return out

    ctx["rate_by_band"] = rate_rows(_band, band_keys, km_band)
    ctx["rate_by_product"] = rate_rows(_family, fam_keys, km_fam)

    # Derived footprint band -- the honest answer to "does a small account churn
    # harder", since Fleet Category measures the customer's total fleet rather
    # than what they subscribe.
    vb_keys = [v for v in core.VEH_ORDER if any(r.get("veh_band") == v for r in rated)]
    ctx["veh_band_keys"] = vb_keys
    ctx["km_by_veh_band"] = [(v, km_subset(lambda r, v=v: r.get("veh_band") == v))
                             for v in vb_keys]
    km_vb = dict(ctx["km_by_veh_band"])
    vb_rows = []
    for v in vb_keys:
        a = sum(r["arr"] for r in active if r.get("veh_band") == v)
        c = sum(r["arr"] for r in base if r.get("veh_band") == v)
        cs = [cu for cu in rate_customers.values() if cu["veh_band"] == v]
        n_full = sum(1 for cu in cs if cu["status"] == "full churn")
        vb_rows.append({"key": v, "active": a, "churn": c, "gross": pct(c, a + c),
                        "km24": 1.0 - km_vb[v]["survival"][24],
                        "km24_share": surv_share(km_vb[v], 24),
                        "km24_thin": surv_thin(km_vb[v], 24),
                        "lines_active": sum(1 for r in active if r.get("veh_band") == v),
                        "lines_churn": sum(1 for r in base if r.get("veh_band") == v),
                        "logos_active": len(cs) - n_full, "logos_full": n_full,
                        "logo_rate": pct(n_full, len(cs))})
    ctx["rate_by_veh_band"] = vb_rows

    # ---------------- penetration / share of wallet ----------------
    pen = []
    for b in band_keys:
        cs = [c for c in rate_customers.values() if c["band"] == b]
        if not cs or b not in core.BAND_MID:
            continue
        vt = sorted(c["veh_total"] for c in cs)
        breach = sum(1 for c in cs if c["band_breach"])
        km_b = km_band.get(b, km)
        pen.append({
            "band": b, "n": len(cs), "median_veh": median_or_zero(vt),
            "band_mid": core.BAND_MID[b],
            "median_pen": pct(median_or_zero(vt), core.BAND_MID[b]),
            "breach_n": breach, "breach_pct": pct(breach, len(cs)),
            "active_arr": sum(c["arr_active"] for c in cs),
            "km24": 1.0 - km_b["survival"][24], "km24_thin": surv_thin(km_b, 24),
            "headroom_veh": max(0.0, core.BAND_MID[b] * len(cs) - sum(vt))})
    ctx["penetration"] = pen
    ctx["breach_total"] = sum(1 for c in rate_customers.values() if c["band_breach"])
    ctx["breach_worst"] = sorted(
        ((c["veh_total"], c["band"], c["company"], c["arr_active"])
         for c in rate_customers.values() if c["band_breach"]), reverse=True)[:12]

    bp = collections.defaultdict(lambda: {"active": 0.0, "churn": 0.0})
    for r in active:
        bp[(r["band"], r["family"])]["active"] += r["arr"]
    for r in base:
        bp[(r["band"], r["family"])]["churn"] += r["arr"]
    ctx["band_product"] = dict(bp)
    bt = collections.defaultdict(lambda: {"active": 0.0, "churn": 0.0})
    for r in active:
        bt[r["band"]]["active"] += r["arr"]
    for r in base:
        bt[r["band"]]["churn"] += r["arr"]
    ctx["band_totals"] = dict(bt)

    # ---------------- tenure distribution ----------------
    for r in base:
        r["_tenure"] = base_tenures[id(r)]
    buckets = []
    dom_bucket = core.dominance(base, lambda r: core.tenure_label(r["_tenure"]))
    seen_labels = {core.tenure_label(r["_tenure"]) for r in base}
    for label in core.TENURE_ORDER:
        if label not in seen_labels:
            continue
        rows = [r for r in base if core.tenure_label(r["_tenure"]) == label]
        d = dom_bucket[label]
        buckets.append({"label": label, "arr": sum(r["arr"] for r in rows),
                        "share": pct(sum(r["arr"] for r in rows), base_churn),
                        "veh": sum(1 for r in rows if r["is_veh"]),
                        "cust": len({r["company"] for r in rows}),
                        "top": d["top"], "top_share": d["top_share"]})
    ctx["tenure_buckets"] = buckets
    assert abs(sum(b["arr"] for b in buckets) - base_churn) < 1.0, "tenure buckets do not tie"

    dom_month = core.dominance(base, lambda r: r["_tenure"])
    ctx["tenure_month"] = {}
    for m in range(0, HORIZON + 1):
        rows = [r for r in base if r["_tenure"] == m]
        d = dom_month.get(m)
        ctx["tenure_month"][m] = {
            "arr": sum(r["arr"] for r in rows),
            "cust": len({r["company"] for r in rows}),
            "top_share": d["top_share"] if d else 0.0}

    # ---------------- contract term ----------------
    term_counts = collections.Counter(r["term"] for r in sub if r["term"])
    main_terms = [t for t, _ in term_counts.most_common(4)]
    main_terms.sort()
    ctx["main_terms"] = main_terms
    contract = []
    for t, _n in sorted(term_counts.items(), key=lambda kv: -kv[1])[:8]:
        rows = [r for r in base if r["term"] == t and r["_tenure"] is not None]
        if not rows:
            continue
        tens = [r["_tenure"] for r in rows]
        at_b = sum(r["arr"] for r in rows
                   if t and min(r["_tenure"] % t, t - (r["_tenure"] % t)) <= 2
                   and r["_tenure"] >= t - 2)
        med = median_or_zero(tens)
        n_active = sum(1 for r in active if r["term"] == t)
        km_t = km_subset(lambda r, t=t: r["term"] == t)
        if t <= 3:
            read = "month-to-month, not a real commitment"
        elif abs(med - t) <= 3:
            read = "runs to term then leaves"
        elif med < t - 3:
            read = "leaves well before term"
        else:
            read = "runs past term"
        thin = len(rows) < 500 or n_active < 500
        if thin:
            read += " -- SMALL n, indicative only"
        contract.append({
            "term": t, "lines": len(rows), "arr": sum(r["arr"] for r in rows),
            "median": med, "active": n_active, "thin": thin,
            "km24": 1.0 - km_t["survival"][24],
            "km24_share": surv_share(km_t, 24),
            "km24_thin": surv_thin(km_t, 24),
            "s12": km_t["survival"][12], "s12_thin": surv_thin(km_t, 12),
            "at_boundary": pct(at_b, sum(r["arr"] for r in rows)),
            "read": read})
    ctx["contract"] = sorted(contract, key=lambda d: -d["arr"])

    tt = collections.defaultdict(float)
    tt_tot = collections.defaultdict(float)
    for r in base:
        if r["term"] in main_terms:
            tt[(r["term"], core.tenure_label(r["_tenure"]))] += r["arr"]
            tt_tot[r["term"]] += r["arr"]
    ctx["term_tenure"] = dict(tt)
    ctx["term_tenure_totals"] = dict(tt_tot)
    ctx["term_tenure_labels"] = {lab for (_t, lab) in tt}

    m24 = ctx["tenure_month"][24]["arr"]
    t24 = [d for d in ctx["contract"] if d["term"] == 24]
    t12 = [d for d in ctx["contract"] if d["term"] == 12]
    findings = [
        "Tenure month 24 alone carries IDR %s, %.1f%% of analysis-base churned ARR. It is not "
        "the cliff v1 described." % (format(int(m24), ","), 100 * pct(m24, base_churn)),
    ]
    if t12 and t24:
        findings.append(
            "A LONGER TERM DOES NOT RETAIN BETTER, on the evidence here. 24-month contracts "
            "show a HIGHER 24-month churn probability than 12-month ones (%.1f%% vs %.1f%%) "
            "and lower survival at every horizon (S12 %.1f%% vs %.1f%%). Median tenure at "
            "churn looks better for the 24-month term (%.0f vs %.0f months) but that statistic "
            "is computed over churned lines only and cannot see the accounts still alive -- it "
            "is the wrong measure and it points the wrong way."
            % (100 * t24[0]["km24"], 100 * t12[0]["km24"], 100 * t24[0]["s12"],
               100 * t12[0]["s12"], t24[0]["median"], t12[0]["median"]))
        findings.append(
            "Where the 12-month term DOES differ is timing: %.0f%% of its churned ARR lands "
            "within two months of a term boundary, against %.0f%% for the 24-month term. Annual "
            "contracts concentrate churn into predictable renewal moments. That is an "
            "opportunity for a renewal calendar, not evidence of a retention problem."
            % (100 * t12[0]["at_boundary"], 100 * t24[0]["at_boundary"]))
    t36 = [d for d in ctx["contract"] if d["term"] == 36]
    if t36:
        findings.append(
            "DO NOT quote the 36-month term's %.1f%% 24-month survival. 36-month contracts were "
            "barely sold before 2024, so by tenure month 24 only %.1f%% of their starting ARR "
            "had been observed that long -- the number measures their youth, not their "
            "stickiness. Their 12-month survival (%.1f%%, on %.0f%% of the pool still observed) "
            "is on firmer ground and genuinely better than the 12- and 24-month terms, but even "
            "that is confounded: longer terms are sold to larger, more committed customers, so "
            "selection and not the contract may be doing the work. Settling this needs a "
            "like-for-like comparison of similar accounts offered different terms."
            % (100 * (1 - t36[0]["km24"]), 100 * t36[0]["km24_share"],
               100 * t36[0]["s12"], 100 * surv_share(km_subset(lambda r: r["term"] == 36), 12)))
    findings.append(
        "Peak monthly hazard within the statistically stable window (at-risk pool still above "
        "%.0f%% of month 0, i.e. months 1-%d) sits at tenure month %d, at %.2f%% of at-risk "
        "ARR. Months beyond %d are reported but too thinly observed to rank -- an earlier cut "
        "of this analysis read a spurious peak at month 40 off a pool that had shrunk to 5%% "
        "of its starting size."
        % (100 * STABLE_MIN_SHARE, ctx["last_stable_month"], ctx["peak_month"],
           100 * ctx["peak_hazard"], ctx["last_stable_month"]))
    findings.append(
        "Monthly hazard runs at %.2f%% across months 1-11 and %.2f%% across months 20-%d -- "
        "a %.1fx step-up. The year-2 risk window is real, but it opens around month 20, not "
        "month 12."
        % (100 * statistics.mean([km["hazard"][m] for m in range(1, 12)]),
           100 * statistics.mean([km["hazard"][m] for m in range(20, min(28, ctx["last_stable_month"] + 1))]),
           ctx["last_stable_month"],
           pct(statistics.mean([km["hazard"][m] for m in range(20, min(28, ctx["last_stable_month"] + 1))]),
               statistics.mean([km["hazard"][m] for m in range(1, 12)]))))
    ctx["contract_findings"] = findings

    # ---------------- full vs partial ----------------
    status_rows = []
    for st in ("full churn", "partial churn", "never churned"):
        cs = [c for c in rate_customers.values() if c["status"] == st]
        ch = sum(c["arr_churn_base"] for c in cs)
        ac = sum(c["arr_active"] for c in cs)
        status_rows.append({
            "status": st, "n": len(cs), "churn": ch, "active": ac,
            "veh_churn": sum(c["veh_churn"] for c in cs),
            "veh_active": sum(c["veh_active"] for c in cs),
            "nrr": pct(ac, ac + ch)})
    ctx["status_rows"] = status_rows

    pb = []
    for b in band_keys:
        cs = [c for c in rate_customers.values()
              if c["status"] == "partial churn" and c["band"] == b]
        if not cs:
            continue
        ch = sum(c["arr_churn_base"] for c in cs)
        ac = sum(c["arr_active"] for c in cs)
        vc = sum(c["veh_churn"] for c in cs)
        va = sum(c["veh_active"] for c in cs)
        pb.append({"band": b, "n": len(cs), "churn": ch, "active": ac,
                   "nrr": pct(ac, ac + ch), "nvr": pct(va, va + vc)})
    ctx["partial_by_band"] = pb

    # ---------------- reason (2025+) ----------------
    win = [r for r in base if r["end"]
           and r["end"].strftime("%Y-%m") >= core.REASON_WINDOW_START]
    reason_total = sum(r["arr"] for r in win)
    ctx["reason_total"] = reason_total
    veh_total = sum(1 for r in win if r["is_veh"])
    cust_total = len({r["company"] for r in win})
    dom_reason = core.dominance(win, lambda r: r["reason_bucket"])
    rows = []
    for b in core.BUCKET_ORDER:
        rs = [r for r in win if r["reason_bucket"] == b]
        if not rs:
            continue
        a = sum(r["arr"] for r in rs)
        v = sum(1 for r in rs if r["is_veh"])
        n = len({r["company"] for r in rs})
        ap, vp, cp = pct(a, reason_total), pct(v, veh_total), pct(n, cust_total)
        spread = max(ap, vp, cp) - min(ap, vp, cp)
        rows.append({
            "bucket": b, "arr": a, "arr_pct": ap, "veh": v, "veh_pct": vp,
            "cust": n, "cust_pct": cp,
            "median_tenure": median_or_zero([r["_tenure"] for r in rs
                                             if r["_tenure"] is not None]),
            "top_share": dom_reason[b]["top_share"],
            "concordance": "concordant" if spread < 0.10
                           else "diverges -- check for one big account"})
    ctx["reason_rows"] = sorted(rows, key=lambda d: -d["arr"])

    raw = collections.defaultdict(lambda: [0.0, set()])
    for r in win:
        raw[r["reason"]][0] += r["arr"]
        raw[r["reason"]][1].add(r["company"])
    ctx["reason_raw"] = sorted(
        ((k, core.reason_bucket(k), v[0], len(v[1])) for k, v in raw.items()),
        key=lambda t: -t[2])

    fp_full = collections.defaultdict(float)
    fp_part = collections.defaultdict(float)
    for r in win:
        st = customers[r["company"]]["status"]
        (fp_full if st == "full churn" else fp_part)[r["reason_bucket"]] += r["arr"]
    tf, tp = sum(fp_full.values()), sum(fp_part.values())
    fp = []
    for b in core.BUCKET_ORDER:
        if not (fp_full.get(b) or fp_part.get(b)):
            continue
        fpc, ppc = pct(fp_full.get(b, 0), tf), pct(fp_part.get(b, 0), tp)
        fp.append({"bucket": b, "full": fp_full.get(b, 0.0), "full_pct": fpc,
                   "partial": fp_part.get(b, 0.0), "partial_pct": ppc,
                   "note": "diverges sharply" if abs(fpc - ppc) > 0.15
                           else "similar"})
    ctx["reason_full_partial"] = sorted(fp, key=lambda d: -d["full"])

    cb = collections.defaultdict(lambda: {"arr": 0.0, "lines": 0, "cust": set()})
    for r in downgrade:
        d = cb[r["band"]]
        d["arr"] += r["arr"]
        d["lines"] += 1
        d["cust"].add(r["company"])
    ctx["contraction_by_band"] = sorted(cb.items(), key=lambda kv: -kv[1]["arr"])

    # ---------------- reason cross-tabs ----------------
    buckets_present = bucket_present(win)
    xb = collections.defaultdict(float)
    for r in win:
        xb[(r["reason_bucket"], r["band"])] += r["arr"]
    xp = collections.defaultdict(float)
    for r in win:
        xp[(r["reason_bucket"], r["family"])] += r["arr"]
    ctx["reason_crosstabs"] = [
        ("Reason bucket x size band", buckets_present, band_keys, dict(xb), reason_total),
        ("Reason bucket x product family", buckets_present, fam_keys, dict(xp), reason_total),
    ]

    # ---------------- concentration ----------------
    conc = core.concentration(base)
    ctx["conc"] = conc
    flags = []
    for m, d in sorted(core.dominance(base, lambda r: r["_tenure"]).items(),
                       key=lambda kv: -(kv[1]["total"])):
        if m is None or d["top_share"] <= 0.5 or d["total"] < 50e6:
            continue
        flags.append(("tenure month", m, d))
    for b, d in core.dominance(base, lambda r: r["band"]).items():
        if d["top_share"] > 0.5:
            flags.append(("size band", b, d))
    for b, d in core.dominance(win, lambda r: r["reason_bucket"]).items():
        if d["top_share"] > 0.5:
            flags.append(("reason bucket", b, d))
    ctx["dominance_flags"] = flags[:15]

    verify = []
    for name, why in [
        ("PERUM DAMRI", "IDR 2.09B / 950 vehicles in Nonaktif -- roughly 4x the figure in the "
                        "extract v1 saw. Either the earlier extract was truncated or this one "
                        "double-counts a re-papering. Second largest single contributor."),
        ("Koperasi Wahana Kalpika", "Reason 'Tidak Ingin Melanjutkan Renewal' at a tenure of "
                                    "under 7 months on 426 vehicles. A renewal decline before "
                                    "the first renewal is not a thing that happens."),
    ]:
        c = customers.get(name)
        if not c:
            continue
        verify.append({"name": name, "arr": c["arr_churn_base"],
                       "veh": c["veh_churn"],
                       "tenure": c["tenure"] if c["tenure"] is not None else 0,
                       "reason": c["reason_bucket"], "why": why})
    ctx["verify_rows"] = verify

    # ---------------- cohort retention ----------------
    ctx["cohort_steps"] = COHORT_STEPS
    coh = collections.defaultdict(lambda: {"arr0": 0.0, "lines": 0, "rows": []})
    for r in sub:
        if r["status"] == "not activated" or not r["start"]:
            continue
        if r.get("excluded"):
            continue
        q = "%dQ%d" % (r["start"].year, (r["start"].month - 1) // 3 + 1)
        d = coh[q]
        d["arr0"] += r["arr"]
        d["lines"] += 1
        d["rows"].append(r)
    cohorts = []
    for q in sorted(coh):
        d = coh[q]
        if d["arr0"] < 50e6:
            continue
        age = max(core.months_between(r["start"], snapshot) for r in d["rows"])
        ret = {}
        for s in COHORT_STEPS:
            if s > age:
                ret[s] = None
                continue
            alive = sum(r["arr"] for r in d["rows"]
                        if r["status"] == "active"
                        or (r["end"] and core.months_between(r["start"], r["end"]) > s))
            ret[s] = pct(alive, d["arr0"])
        cohorts.append((q, {"arr0": d["arr0"], "lines": d["lines"], "ret": ret}))
    ctx["cohorts"] = cohorts

    # ---------------- target list ----------------
    targets = []
    for c in customers.values():
        if c["arr_active"] <= 0 or c["status"] == "full churn":
            continue
        t = c["tenure"] if c["tenure"] is not None else 0
        kmb = km_band.get(c["band"], km)
        haz = cond_hazard(kmb, t, 12)
        flags_s, plays = [], []
        if 12 <= t < 24:
            flags_s.append("year-2 window")
        if c["status"] == "partial churn":
            flags_s.append("already shedding")
        if c["term"] and t >= c["term"] - 3:
            flags_s.append("at/past contract term")
        if c["arr_active"] >= 500e6:
            flags_s.append("top-decile ARR")
        if c["company"] in core.EXCLUDE_CUSTOMERS:
            flags_s.append("EXCLUDED from churn analysis -- retained here because it is the "
                           "single largest active account")
        phase = next((lab for lab, lo, hi in PHASES if lo <= t < hi), "Months 48+")
        if c["status"] == "partial churn":
            plays.append("net-retention save: recover shed vehicles")
        elif 12 <= t < 24:
            plays.append("month 15-18 value/renewal gate")
        elif t < 6:
            plays.append("onboarding to first-value checkpoint")
        else:
            plays.append("scheduled business review")
        targets.append({
            "company": c["company"], "band": c["band"], "pmap": family(c["pmap"]),
            "industry": c["industry"], "arr": c["arr_active"], "veh": c["veh_active"],
            "tenure": t, "term": c["term"] or "", "phase": phase,
            "peer_hazard": haz, "expected": c["arr_active"] * haz,
            "flags": ", ".join(flags_s) or "-", "play": plays[0]})
    targets.sort(key=lambda d: -d["expected"])
    ctx["targets"] = targets
    exp = sorted(d["expected"] for d in targets)
    ctx["target_p90"] = exp[int(0.9 * len(exp))] if exp else 0.0

    # ---------------- quality + narrative ----------------
    ctx["quality"] = [
        ("Churned lines with no start date", sum(1 for r in churn_all if not r["start"]),
         "Dropped from tenure and hazard views only."),
        ("Churned lines with negative tenure", sum(
            1 for r in churn_all if r["start"] and r["end"]
            and core.months_between(r["start"], r["end"]) < 0),
         "date_end precedes date_start. Dropped from hazard; the records are wrong."),
        ("Lines with blank Fleet Category", sum(1 for r in sub if r["band"] == "(unassigned)"),
         "Kept as an explicit (unassigned) band, never folded into A<=5."),
        ("Churned ARR on loose reason match (L3 company-level)",
         coverage_arr.get("L3 co", 0.0),
         "Reason inferred from the company's dominant reason, not its own line. %.1f%% of "
         "churned ARR." % (100 * pct(coverage_arr.get("L3 co", 0.0), gross_churn))),
        ("Churned ARR with no reason match at all", coverage_arr.get("unmatched", 0.0),
         "Appears in ARR views, absent from reason views."),
        ("Vehicle-count proxy error", ctx["veh_bias"],
         "GPS-mapped lines vs Nonaktif's distinct-nopol count, in percent. Subscription has "
         "no nopol and qty is always 1, so a vehicle count there is necessarily a proxy."),
        ("Nonaktif accounts Subscription still shows as active", gap_detail["active_n"],
         "These churned per Nonaktif but carry only active Subscription lines. A real "
         "register disagreement -- raise with the data owner."),
        ("Customers holding more than one size band",
         sum(1 for c in rate_customers.values() if len(c["bands"]) > 1),
         "Resolved to the band of their largest-ARR line."),
        ("Customers whose subscribed vehicles exceed their own Fleet Category ceiling",
         ctx["breach_total"],
         "%.1f%% of all customers. Fleet Category reads as the customer's TOTAL fleet (87%% "
         "sit at or below their ceiling, and median penetration falls monotonically from 67%% "
         "in A<=5 to 2%% in G>=400) -- but these breaches are outright wrong under either "
         "reading. PERUM DAMRI carries 1,911 subscribed vehicles under a D<=50 label. Use the "
         "derived vehicle band for footprint questions."
         % (100 * pct(ctx["breach_total"], len(rate_customers)))),
        ("Tenure months too thinly observed to rate",
         HORIZON - ctx["last_stable_month"],
         "Months %d-%d hold under %.0f%% of the month-0 at-risk pool. Shown but marked thin, "
         "and excluded from peak-finding. This is the right-censoring trap: an earlier cut of "
         "this analysis reported a spurious hazard peak at month 40."
         % (ctx["last_stable_month"] + 1, HORIZON, 100 * STABLE_MIN_SHARE)),
    ]
    ctx["data_requests"] = [
        "Usage / telemetry per account (active devices, login frequency, feature adoption). "
        "The AM program has no leading indicator without it -- everything here is a lagging "
        "structural signal.",
        "AR ageing per customer over time, including days-past-due at termination. This is "
        "what would settle whether arrears is a cause of churn or the way a renewal decision "
        "gets executed. It is the single highest-value missing dataset.",
        "Support-ticket volume and severity per account, to corroborate or contradict the "
        "sales-entered reason labels.",
        "Bookings/origination records including accounts that never became billable ARR, so "
        "pre-revenue failures stop being invisible.",
        "A written definition of the six administrative reason codes from the data owner. "
        "IDR %s currently sits in a bucket we are excluding on inference about what the "
        "labels mean." % format(int(exc_admin), ","),
        "Confirmation on PERUM DAMRI and Koperasi Wahana Kalpika before any of this is "
        "presented upward.",
    ]
    ctx["tab_index"] = [
        ("02_Reconciliation", "CONTROL", "Tie-outs and the Nonaktif/Subscription gap bridge."),
        ("03_Hazard_Survival", "RATE", "Kaplan-Meier. Age-adjusted risk. Prioritise on this."),
        ("04_Churn_Rate_Segment", "RATE", "Churn rate by customer size, subscribed-vehicle "
                                         "band and product. Two rate definitions."),
        ("04b_Penetration", "RATE", "Share of wallet by band, and the Fleet Category breaches."),
        ("05_Tenure_Distribution", "MIX", "Where churn lands across tenure. NOT risk."),
        ("06_Contract_Term", "RATE + MIX", "Whether the month-24 spike is contractual."),
        ("07_Full_vs_Partial", "MIX + RATE", "Net retention; partial churn; contraction."),
        ("08_Reason_2025plus", "MIX", "Sales-entered reason mix. Testimony, not fact."),
        ("09_Reason_x_Band_x_Prod", "MIX", "Core cohort cross-tabs."),
        ("10_Concentration", "MIX", "Named accounts and single-account dominance screen."),
        ("11_Cohort_Retention", "RATE", "Start-cohort retention triangle."),
        ("12_Data_Quality", "CONTROL", "Defects and what this cannot conclude."),
    ]
    ctx["limits"] = [
        "The excluded customer is removed from BOTH numerator and denominator of every rate. "
        "It holds IDR %s of active ARR (%.1f%% of the base), so this materially changes the "
        "segment picture: band B<=10 reads 28.4%% 24-month churn with it removed and 6.8%% "
        "with its active ARR left in the denominator. It is retained on the target list only."
        % (format(int(excluded_active_arr), ","),
           100 * pct(excluded_active_arr, excluded_active_arr + active_arr)),
        "Fleet Category measures the CUSTOMER'S TOTAL FLEET, not the vehicles they subscribe. "
        "It is the right field for 'customer size' and the wrong one for 'our footprint'. "
        "%d customers (%.1f%%) breach their own band ceiling, so it is also partly stale. "
        "Footprint questions use the derived vehicle band instead."
        % (ctx["breach_total"], 100 * pct(ctx["breach_total"], len(rate_customers))),
        "Fleet Category is an as-of-snapshot attribute, not as-of-churn. An account's band "
        "today may differ from its band when it churned.",
        "Hazard beyond tenure month %d rests on under %.0f%% of the starting at-risk pool and "
        "is marked thin. Do not rank or plan against those months."
        % (ctx["last_stable_month"], 100 * STABLE_MIN_SHARE),
        "Vehicle counts on the active base are a proxy (GPS-mapped lines); measured at %+.1f%% "
        "against Nonaktif's hard distinct-nopol count." % ctx["veh_bias"],
        "Full vs partial is evaluated as of the snapshot. A company that fully churned in 2023 "
        "and returned in 2025 reads as partial.",
        "Reason is sales-entered testimony with an obvious incentive to log a payment problem "
        "rather than a lost renewal. No behavioural data exists in these files to corroborate "
        "it, so the reason-driven routing in the AM program rests on unverified labels.",
        "Whether arrears is a cause of churn or the mechanism by which a renewal decision gets "
        "executed CANNOT be settled from this extract. It needs AR ageing joined to usage "
        "decline. This is the most important open question and it remains open.",
        "Subscription lines within one customer are not independent, so line-level hazard "
        "understates uncertainty. Logo-level KM is reported alongside for that reason.",
        "Register survivorship is unverified: lines deleted from the source system rather than "
        "marked churned would be invisible here.",
        "The target list ranks by structural exposure, not predicted churn. It answers 'who to "
        "call first', not 'who will leave'.",
    ]
    return ctx


def _band(r):
    return r["band"]


def _family(r):
    return r["family"]


def bucket_present(rows):
    present = {r["reason_bucket"] for r in rows}
    return [b for b in core.BUCKET_ORDER if b in present]
