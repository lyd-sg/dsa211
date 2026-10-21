#!/usr/bin/env python3
"""Run every candidate dataset through the Topic 2 requirements and rank them.

bakeoff.py scored datasets against nine PROXY criteria. That proxy gave ACRA
9 of 9 while the actual deliverable turned out degenerate, so the criteria below
are reverse-engineered from the graded requirements themselves: each one asks
whether a required section of the report can actually be written.

Nothing here is hand-computed. Every number in the output, including the final
recommendation text, is derived from the measurements in report_eval.run_dataset.
"""

import os, json, argparse, traceback
import numpy as np
import pandas as pd

import bakeoff as B
import report_eval as RE
import candidates as C


# ---------------------------------------------------------------------------
# Each criterion states WHY it exists. "breaks" names the section of the report
# that cannot be written if the criterion fails.
REPORT_CRITERIA = [
    ("Train positives >= 500", "n_train_pos", lambda v: v >= 500, ">= 500",
     "per-fold estimates become unstable below this", "k-fold CV section"),
    ("Held-out positives >= 100", "n_test_pos", lambda v: v >= 100, ">= 100",
     "test sensitivity needs a usable confidence interval", "CV vs held-out section"),
    ("Numeric features >= 3", "n_numeric", lambda v: v >= 3, ">= 3",
     "scaling must be exercised, and LDA/NB assume continuous inputs", "preprocessing + LDA/NB sections"),
    ("Categorical features >= 3", "n_categorical", lambda v: v >= 3, ">= 3",
     "one-hot encoding must be refitted per fold to be demonstrated", "leakage-free pipeline section"),
    ("3 distinct confusion matrices", "distinct test confusions", lambda v: v == 3, "== 3",
     "if two models score identically the comparison table is empty", "three-model comparison table"),
    ("Models separate beyond noise", "separated beyond noise", lambda v: bool(v), "True",
     "otherwise model ranking is not a finding", "three-model comparison"),
    ("Operating point informative", "min(sens,spec) @t", lambda v: v >= 0.35, ">= 0.35",
     "a point pinned at sens=1 or spec=0 is the trivial rule in disguise", "threshold extension"),
    ("Sensitivity not saturated", "test sens @t", lambda v: v <= 0.98, "<= 0.98",
     "a pinned sensitivity makes its confidence interval meaningless", "threshold + CI discussion"),
    ("Cost can pick a model", "cost gap best vs 2nd", lambda v: v >= 0.01, ">= 1%",
     "the brief requires justifying the final model on cost, not just AUC", "model-choice justification"),
    ("Cost cut vs 0.5 >= 5%", "cost cut vs 0.5", lambda v: v >= 0.05, ">= 5%",
     "justifies operating anywhere other than 0.5", "threshold extension"),
    ("Cost cut vs trivial >= 5%", "cost cut vs trivial", lambda v: v >= 0.05, ">= 5%",
     "the model must beat the best constant rule", "threshold extension"),
    ("|CV - test AUC| <= 0.03", "|CV - test AUC|", lambda v: v <= 0.03, "<= 0.03",
     "the CV estimate has to hold up out of sample", "CV vs held-out section"),
    ("Sens 95% CI width <= 0.20", "sens CI width", lambda v: v <= 0.20, "<= 0.20",
     "a wide interval makes the held-out comparison uninformative", "CV vs held-out section"),
    ("Best CV AUC in [0.62, 0.95]", "best CV AUC", lambda v: 0.62 <= v <= 0.95, "0.62-0.95",
     "below is noise; above is near-separable and flattens the sens/spec trade", "whole report"),
    ("Brier spread >= 0.01", "Brier spread across 3", lambda v: v >= 0.01, ">= 0.01",
     "gives the calibration discussion something to say", "calibration / depth"),
]


def build_jobs(args):
    """(name, callable -> (X, y, suspects, notes, origin))"""
    jobs = []

    def taiwan():
        raw, src = (B.load_taiwan_from_file(args.taiwan_local)
                    if args.taiwan_local else B.load_taiwan())
        X, y, s, n = B.adapt_taiwan(raw)
        return X, y, s, n + [f"source {src}"], "Taiwan (Asia)"

    def acra():
        raw, src = B.load_acra(local_paths=args.acra_local)
        X, y, s, n = B.adapt_acra(raw, cohort=tuple(args.cohort))
        return X, y, s, n + [f"source {src}"], "Singapore (Asia)"

    jobs.append(("Taiwan credit default", taiwan))
    jobs.append(("ACRA firm survival", acra))
    for nm, fn in C.CANDIDATES.items():
        jobs.append((nm, (lambda f=fn: f(args.cache_dir))))
    if args.only:
        keep = {k.strip().lower() for k in args.only.split(",")}
        jobs = [j for j in jobs if any(k in j[0].lower() for k in keep)]
    return jobs


def score(summaries):
    """Apply REPORT_CRITERIA. Returns (scorecard df, tally dict, fails dict)."""
    rows, tally, fails = [], {}, {}
    for label, key, test, target, why, breaks in REPORT_CRITERIA:
        row = {"criterion": label, "target": target}
        for s in summaries:
            d = s["dataset"]
            v = s.get(key, np.nan)
            try:
                ok = bool(test(v)) and not (isinstance(v, float) and not np.isfinite(v))
            except Exception:
                ok = False
            tally[d] = tally.get(d, 0) + int(ok)
            if not ok:
                fails.setdefault(d, []).append((label, v, breaks))
            shown = f"{v:.4f}" if isinstance(v, (float, np.floating)) and np.isfinite(v) else str(v)
            row[d] = f"{shown}  {'PASS' if ok else 'fail'}"
        rows.append(row)
    return pd.DataFrame(rows).set_index("criterion"), tally, fails


def write_report(summaries, sc, tally, fails, outdir, ratio):
    n = len(REPORT_CRITERIA)
    by = sorted(tally.items(), key=lambda kv: -kv[1])
    smap = {s["dataset"]: s for s in summaries}
    L = []
    L.append("# Topic 2 dataset bake-off, final report\n")
    L.append(f"Criteria reverse-engineered from the graded requirements. "
             f"Cost ratio C_FN/C_FP = {ratio}. {n} criteria.\n")

    L.append("\n## Ranking\n")
    L.append("| rank | dataset | origin | passed | best CV AUC | test sens/spec @t | verdict |")
    L.append("|---|---|---|---|---|---|---|")
    for i, (d, t) in enumerate(by, 1):
        s = smap[d]
        verdict = ("usable" if t == n else
                   "usable with caveats" if t >= n - 2 else "not usable")
        L.append(f"| {i} | {d} | {s['origin']} | {t}/{n} | {s['best CV AUC']:.4f} | "
                 f"{s['test sens @t']:.3f} / {s['test spec @t']:.3f} | {verdict} |")

    L.append("\n## Failed criteria, and what each one breaks\n")
    for d, _ in by:
        f = fails.get(d, [])
        if not f:
            L.append(f"**{d}** — no failures.\n")
            continue
        L.append(f"**{d}** — {len(f)} failed:\n")
        for label, v, breaks in f:
            shown = f"{v:.4f}" if isinstance(v, (float, np.floating)) and np.isfinite(v) else str(v)
            L.append(f"- `{label}` = {shown} → breaks the **{breaks}**")
        L.append("")

    L.append("\n## Supporting numbers\n")
    comp = pd.DataFrame(summaries).set_index("dataset").T
    L.append(comp.to_markdown())

    L.append("\n## Recommendation\n")
    top, ttop = by[0]
    asian = [d for d, _ in by if "CONTROL" not in smap[d]["origin"]]
    best_asian = asian[0] if asian else None
    L.append(f"- Highest scoring overall: **{top}** ({ttop}/{n}), origin {smap[top]['origin']}.")
    if best_asian and best_asian != top:
        L.append(f"- Highest scoring that meets the Asian preference: **{best_asian}** "
                 f"({tally[best_asian]}/{n}).")
        L.append(f"- The gap to the control is {ttop - tally[best_asian]} criteria; "
                 f"if that gap is 0 the Asian option costs nothing.")
    else:
        L.append(f"- **{top}** also satisfies the Asian preference, so no trade is needed.")
    txt = "\n".join(L) + "\n"
    with open(os.path.join(outdir, "FINAL_REPORT.md"), "w") as fh:
        fh.write(txt)
    return txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cost-ratio", type=float, default=5.0)
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--test-size", type=float, default=0.25)
    ap.add_argument("--cohort", type=int, nargs=2, default=[2010, 2015])
    ap.add_argument("--outdir", default="results_all")
    ap.add_argument("--cache-dir", default=".uci_cache")
    ap.add_argument("--acra-local", nargs="*", default=None)
    ap.add_argument("--taiwan-local", default=None)
    ap.add_argument("--only", default=None, help="comma separated substrings of dataset names")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    print(f"cost ratio {a.cost_ratio} | theoretical t* {1/(1+a.cost_ratio):.4f} | "
          f"folds {a.folds} | test size {a.test_size}\n")

    summaries = []
    for name, fn in build_jobs(a):
        try:
            X, y, susp, notes, origin = fn()
            smry, req, alt = RE.run_dataset(name, X, y, susp, notes, a.outdir,
                                            a.cost_ratio, a.folds, a.test_size,
                                            origin=origin)
            summaries.append(smry)
        except Exception as e:
            print(f"\n!! {name} FAILED: {repr(e)[:300]}")
            traceback.print_exc(limit=2)

    if not summaries:
        print("nothing evaluated"); return

    sc, tally, fails = score(summaries)
    print("\n" + "=" * 100)
    print("REPORT-SUITABILITY SCORECARD")
    print("=" * 100)
    print(sc.to_string())

    print("\n" + "=" * 100)
    print("TALLY")
    for d, t in sorted(tally.items(), key=lambda kv: -kv[1]):
        print(f"  {d:<28} {t} of {len(REPORT_CRITERIA)}")

    sc.to_csv(os.path.join(a.outdir, "report_scorecard.csv"))
    pd.DataFrame(summaries).set_index("dataset").T.to_csv(
        os.path.join(a.outdir, "all_dataset_comparison.csv"))
    with open(os.path.join(a.outdir, "all_summaries.json"), "w") as fh:
        json.dump(summaries, fh, indent=2, default=str)
    txt = write_report(summaries, sc, tally, fails, a.outdir, a.cost_ratio)
    print("\n" + "=" * 100)
    print(txt)
    print(f"wrote {a.outdir}/FINAL_REPORT.md, report_scorecard.csv, "
          f"all_dataset_comparison.csv, model_table_*.csv, report_*.png")


if __name__ == "__main__":
    main()
