#!/usr/bin/env python3
"""Topic 2 full-requirement evaluation, run on both candidate datasets.

This does NOT modify bakeoff.py. It imports that module's loaders, adapters and
preprocessing so the leakage discipline is identical by construction:

  * the held-out split happens first, and the test set is scored once, at the end
  * imputation, scaling and one-hot encoding stay inside the pipeline (make_pre),
    so they are refitted on every training fold
  * every operating threshold is chosen from TRAINING out-of-fold predictions only

Where bakeoff.py answers "which dataset scores better on nine proxy criteria",
this answers "which dataset actually produces the better report", by running the
graded requirements themselves on both and comparing the outputs.
"""

import os, re, json, argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, brier_score_loss

import bakeoff as B

# The three models the brief requires, taken from bakeoff so they cannot drift.
REQUIRED = dict(B.MODELS)

# Alternatives, reported separately. These exist to satisfy "every decision needs
# a comparison against an alternative"; they are never eligible as the final model.
ALTERNATIVES = {
    "Logistic (balanced)": lambda: LogisticRegression(max_iter=3000, class_weight="balanced"),
    "LDA (shrinkage)":     lambda: LDA(solver="lsqr", shrinkage="auto"),
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def cm_stats(y, p, t):
    """Confusion matrix and the rates the brief asks for, at threshold t."""
    pred = (np.asarray(p) >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    sens = tp / (tp + fn) if (tp + fn) else np.nan
    spec = tn / (tn + fp) if (tn + fp) else np.nan
    prec = tp / (tp + fp) if (tp + fp) else np.nan
    return {
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
        "sens": sens, "spec": spec, "precision": prec,
        "balanced_acc": (sens + spec) / 2,
        "youden_J": sens + spec - 1,
    }


def expected_cost(y, p, t, ratio):
    """Cost per case at threshold t, same convention as bakeoff.cost_curve."""
    y = np.asarray(y)
    pred = (np.asarray(p) >= t).astype(int)
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    return (fn * ratio + fp) / len(y)


def run_dataset(name, X, y, suspects, notes, outdir, ratio, folds, test_size, origin="?"):
    print("=" * 78); print(name); print("=" * 78)
    for n in notes:
        print(" *", n)

    X = X.reset_index(drop=True)
    y = pd.Series(np.asarray(y)).reset_index(drop=True).astype(int)

    # ---- 1. held-out split FIRST -------------------------------------------
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=B.RANDOM_STATE)
    Xtr, Xte = Xtr.reset_index(drop=True), Xte.reset_index(drop=True)
    ytr, yte = ytr.reset_index(drop=True), yte.reset_index(drop=True)

    # ---- 2. drop declared leakage suspects, exactly as bakeoff does ---------
    cols = [c for c in Xtr.columns if c not in set(suspects)]
    Xtr_a, Xte_a = Xtr[cols], Xte[cols]
    num, cat = B.split_types(Xtr_a)
    print(f"\nrows {len(X):,} | prevalence {y.mean():.4f} | "
          f"train {len(Xtr):,} | test {len(Xte):,}")
    print(f"dropped suspects: {sorted(suspects) if suspects else 'none'}")
    print(f"numeric features {len(num)} | categorical features {len(cat)}")

    skf = StratifiedKFold(folds, shuffle=True, random_state=B.RANDOM_STATE)

    # ---- 2b. leakage screen on TRAINING data only, then price the suspects --
    # Screening on the full data would leak the test set into the screen itself.
    scr = B.leak_screen(Xtr_a, ytr)
    max_univ = float(scr["univariate_auc"].max())
    flagged = scr.loc[scr["flag"] == "LEAK?", "feature"].tolist()
    print(f"\nleakage screen (train only): max univariate AUC {max_univ:.4f}"
          f" | flagged and KEPT: {flagged or 'none'}")

    def cv_auc_of(frame):
        n2, c2 = B.split_types(frame)
        pipe = Pipeline([("pre", B.make_pre(n2, c2)),
                         ("clf", LogisticRegression(max_iter=3000))])
        pp = cross_val_predict(pipe, frame, ytr, cv=skf, method="predict_proba")[:, 1]
        return roc_auc_score(ytr, pp)

    auc_naive = cv_auc_of(Xtr) if suspects else np.nan
    auc_audited = cv_auc_of(Xtr_a)
    premium = float(auc_naive - auc_audited) if np.isfinite(auc_naive) else 0.0
    print(f"logistic CV AUC: all features "
          f"{auc_naive if np.isfinite(auc_naive) else auc_audited:.4f} | "
          f"after audit {auc_audited:.4f} | leakage premium {premium:.4f}")

    # ---- 3. CV out-of-fold predictions, preprocessing refitted per fold -----
    def oof_for(mk):
        pipe = Pipeline([("pre", B.make_pre(num, cat)), ("clf", mk())])
        return cross_val_predict(pipe, Xtr_a, ytr, cv=skf, method="predict_proba")[:, 1]

    oof = {m: oof_for(mk) for m, mk in REQUIRED.items()}
    oof_alt = {m: oof_for(mk) for m, mk in ALTERNATIVES.items()}

    # ---- 4. per-model metrics, threshold from TRAIN OOF only ----------------
    def model_row(m, p, is_alt=False):
        cv_auc = roc_auc_score(ytr, p)
        brier = brier_score_loss(ytr, p)
        fold = np.array([roc_auc_score(ytr.iloc[vi], p[vi]) for _, vi in skf.split(Xtr_a, ytr)])
        ts, cost, _, _ = B.cost_curve(ytr, p, ratio=ratio)
        t_star = float(ts[int(np.argmin(cost))])          # this model's own operating point
        cv_half = cm_stats(ytr, p, 0.5)
        cv_op = cm_stats(ytr, p, t_star)
        row = {
            "model": m, "kind": "alternative" if is_alt else "required",
            "CV AUC": cv_auc, "CV Brier": brier, "fold sd": fold.std(ddof=1),
            "t (from train OOF)": t_star,
            "CV sens @0.5": cv_half["sens"], "CV spec @0.5": cv_half["spec"],
            "CV sens @t": cv_op["sens"], "CV spec @t": cv_op["spec"],
            "CV youden @t": cv_op["youden_J"],
            "cost @0.5": expected_cost(ytr, p, 0.5, ratio),
            "cost @t": float(cost.min()),
        }
        row.update({f"CV {k} @t": v for k, v in cv_op.items() if k in ("TN", "FP", "FN", "TP")})
        return row, t_star, fold

    rows, thresholds, folds_auc = [], {}, {}
    for m, p in {**oof, **oof_alt}.items():
        r, t, fa = model_row(m, p, is_alt=(m in ALTERNATIVES))
        rows.append(r); thresholds[m] = t; folds_auc[m] = fa

    # ---- 5. held-out, scored once, at each model's train-chosen threshold ---
    # Selecting the final model uses TRAIN CV only; the test numbers below are
    # reported for the comparison the brief asks for, not used to choose.
    test_bits = {}
    for m, mk in {**REQUIRED, **ALTERNATIVES}.items():
        fitted = Pipeline([("pre", B.make_pre(num, cat)), ("clf", mk())]).fit(Xtr_a, ytr)
        pte = fitted.predict_proba(Xte_a)[:, 1]
        t = thresholds[m]
        st = cm_stats(yte, pte, t)
        lo, hi = B.wilson(st["TP"], st["TP"] + st["FN"])
        test_bits[m] = (pte, st)
        for r in rows:
            if r["model"] == m:
                r.update({
                    "test AUC": roc_auc_score(yte, pte),
                    "test sens @t": st["sens"], "test spec @t": st["spec"],
                    "test youden @t": st["youden_J"],
                    "test TN": st["TN"], "test FP": st["FP"],
                    "test FN": st["FN"], "test TP": st["TP"],
                    "sens 95% CI lo": lo, "sens 95% CI hi": hi,
                    "CV - test AUC": r["CV AUC"] - roc_auc_score(yte, pte),
                })

    tab = pd.DataFrame(rows).set_index("model")
    req = tab[tab["kind"] == "required"].drop(columns="kind")
    alt = tab[tab["kind"] == "alternative"].drop(columns="kind")

    show = ["CV AUC", "CV Brier", "t (from train OOF)", "CV sens @t", "CV spec @t",
            "cost @0.5", "cost @t", "test AUC", "test sens @t", "test spec @t",
            "CV - test AUC"]
    print("\n--- required three models -------------------------------------------")
    print(req[show].round(4).to_string())
    print("\n--- confusion matrices, held out, each at its own train-chosen t -----")
    print(req[["t (from train OOF)", "test TN", "test FP", "test FN", "test TP"]].to_string())
    print("\n--- alternatives (depth comparison, not eligible as final) -----------")
    print(alt[show].round(4).to_string())

    # ---- 6. final model on the two grounds the brief names ------------------
    by_auc = req["CV AUC"].idxmax()
    by_cost = req["cost @t"].idxmin()
    print(f"\nbest by predictive performance (CV AUC) : {by_auc}")
    print(f"best by expected cost at C_FN/C_FP={ratio}  : {by_cost}")
    print(f"the two grounds {'AGREE' if by_auc == by_cost else 'DISAGREE'}")

    # separation beyond fold noise, between best and worst of the required three
    worst = req["CV AUC"].idxmin()
    d = folds_auc[by_auc] - folds_auc[worst]
    se = d.std(ddof=1) / np.sqrt(len(d))
    separated = bool(abs(d.mean()) > 2 * se) if se > 0 else False
    print(f"{by_auc} vs {worst}: mean paired fold gap {d.mean():.4f}, SE {se:.4f}, "
          f"separated {separated}")

    # ---- 7. plots -----------------------------------------------------------
    os.makedirs(outdir, exist_ok=True)
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.4))
    for m in REQUIRED:
        fpr, tpr, _ = roc_curve(ytr, oof[m])
        ax[0].plot(fpr, tpr, lw=1.7, label=f"{m}  AUC {req.loc[m,'CV AUC']:.3f}")
    ax[0].plot([0, 1], [0, 1], "k--", lw=0.8)
    ax[0].set_xlabel("1 - specificity (false positive rate)")
    ax[0].set_ylabel("sensitivity (true positive rate)")
    ax[0].set_title(f"{name}\nROC, 5-fold out-of-fold, training data")
    ax[0].legend(fontsize=8, loc="lower right")

    for m in REQUIRED:
        ts, cost, sens, spec = B.cost_curve(ytr, oof[m], ratio=ratio)
        ax[1].plot(ts, sens, lw=1.5, label=f"{m} sensitivity")
        ax[1].plot(ts, spec, lw=1.5, ls="--", label=f"{m} specificity")
    ax[1].axvline(0.5, color="grey", ls=":", lw=1, label="0.5")
    ax[1].axvline(thresholds[by_auc], color="k", ls=":", lw=1.4,
                  label=f"chosen t {thresholds[by_auc]:.3f}")
    ax[1].set_xlabel("threshold"); ax[1].set_ylabel("rate")
    ax[1].set_title("Sensitivity and specificity vs threshold")
    ax[1].legend(fontsize=7, loc="center right")

    for m in REQUIRED:
        ts, cost, _, _ = B.cost_curve(ytr, oof[m], ratio=ratio)
        ax[2].plot(ts, cost, lw=1.6, label=f"{m} (min {cost.min():.3f} @ {ts[np.argmin(cost)]:.3f})")
        ax[2].plot(ts[np.argmin(cost)], cost.min(), "o", ms=5)
    prev = float(ytr.mean())
    ax[2].axhline(min(prev * ratio, 1 - prev), color="r", ls="--", lw=1,
                  label=f"best trivial rule {min(prev*ratio, 1-prev):.3f}")
    ax[2].set_xlabel("threshold"); ax[2].set_ylabel("expected cost per case")
    ax[2].set_title(f"Expected cost, C_FN/C_FP = {ratio}")
    ax[2].legend(fontsize=7)
    plt.tight_layout()
    pth = os.path.join(outdir, f"report_{slug(name)}.png")
    plt.savefig(pth, dpi=140); plt.close()
    print("saved plot ->", pth)

    tab.drop(columns="kind").to_csv(os.path.join(outdir, f"model_table_{slug(name)}.csv"))

    # ---- 8. the numbers that decide which dataset makes a better report -----
    op = req.loc[by_auc]

    # If two of the three required models give the SAME confusion matrix, the
    # comparison table the brief asks for has nothing in it.
    confs = {tuple(int(req.loc[m, c]) for c in ("test TN", "test FP", "test FN", "test TP"))
             for m in REQUIRED}
    # If the best and second-best model cost the same to four decimals, then
    # "justify the final model on cost" cannot actually pick a winner.
    cs = sorted(float(v) for v in req["cost @t"].values)
    cost_gap = float((cs[1] - cs[0]) / cs[0]) if len(cs) > 1 and cs[0] > 0 else np.nan

    summary = {
        "dataset": name, "origin": origin,
        "rows": len(X), "prevalence": float(y.mean()),
        "n_train_pos": int(ytr.sum()), "n_test_pos": int(yte.sum()),
        "max univ AUC (train)": max_univ,
        "n flagged kept": len(flagged),
        "leakage premium": premium,
        "distinct test confusions": len(confs),
        "cost gap best vs 2nd": cost_gap,
        "n_numeric": len(num), "n_categorical": len(cat),
        "final model (AUC)": by_auc, "final model (cost)": by_cost,
        "grounds agree": by_auc == by_cost,
        "best CV AUC": float(req["CV AUC"].max()),
        "AUC spread across 3": float(req["CV AUC"].max() - req["CV AUC"].min()),
        "separated beyond noise": separated,
        "Brier spread across 3": float(req["CV Brier"].max() - req["CV Brier"].min()),
        "chosen t": float(op["t (from train OOF)"]),
        "t moved from 0.5": abs(float(op["t (from train OOF)"]) - 0.5),
        "test sens @t": float(op["test sens @t"]),
        "test spec @t": float(op["test spec @t"]),
        "test youden @t": float(op["test youden @t"]),
        "min(sens,spec) @t": float(min(op["test sens @t"], op["test spec @t"])),
        "cost cut vs 0.5": float((op["cost @0.5"] - op["cost @t"]) / op["cost @0.5"]),
        "cost cut vs trivial": float((min(prev * ratio, 1 - prev) - op["cost @t"]) / min(prev * ratio, 1 - prev)),
        "|CV - test AUC|": abs(float(op["CV - test AUC"])),
        "sens CI width": float(op["sens 95% CI hi"] - op["sens 95% CI lo"]),
    }
    return summary, req, alt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cost-ratio", type=float, default=5.0)
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--test-size", type=float, default=0.25)
    ap.add_argument("--cohort", type=int, nargs=2, default=[2010, 2015])
    ap.add_argument("--outdir", default="results_report")
    ap.add_argument("--acra-local", nargs="*", default=None)
    ap.add_argument("--taiwan-local", default=None)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    print(f"cost ratio C_FN/C_FP = {a.cost_ratio} | theoretical t* = "
          f"{1/(1+a.cost_ratio):.4f} | folds {a.folds} | test size {a.test_size}\n")

    summaries, tables = [], {}

    try:
        raw, src = (B.load_taiwan_from_file(a.taiwan_local) if a.taiwan_local else B.load_taiwan())
        print("Taiwan source:", src)
        X, y, s, n = B.adapt_taiwan(raw)
        smry, req, alt = run_dataset("Taiwan credit default", X, y, s, n,
                                     a.outdir, a.cost_ratio, a.folds, a.test_size,
                                     origin="Taiwan (Asia)")
        summaries.append(smry); tables["Taiwan credit default"] = (req, alt)
    except Exception as e:
        print("TAIWAN FAILED:", repr(e)[:300])

    try:
        raw, src = B.load_acra(local_paths=a.acra_local)
        print("\nACRA source:", src)
        X, y, s, n = B.adapt_acra(raw, cohort=tuple(a.cohort))
        smry, req, alt = run_dataset("ACRA firm survival", X, y, s, n,
                                     a.outdir, a.cost_ratio, a.folds, a.test_size,
                                     origin="Singapore (Asia)")
        summaries.append(smry); tables["ACRA firm survival"] = (req, alt)
    except Exception as e:
        print("ACRA FAILED:", repr(e)[:300])

    if not summaries:
        print("\nNothing evaluated."); return

    comp = pd.DataFrame(summaries).set_index("dataset").T
    print("\n" + "=" * 78)
    print("WHICH DATASET PRODUCES THE BETTER REPORT")
    print("=" * 78)
    print(comp.to_string())
    comp.to_csv(os.path.join(a.outdir, "dataset_comparison.csv"))
    with open(os.path.join(a.outdir, "summaries.json"), "w") as fh:
        json.dump(summaries, fh, indent=2, default=str)
    print(f"\nwrote {a.outdir}/dataset_comparison.csv, model_table_*.csv, report_*.png")


if __name__ == "__main__":
    main()
