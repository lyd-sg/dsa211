#!/usr/bin/env python3
"""DSA211 Topic 2 dataset bake-off.

Decides, on measured evidence rather than assumption, whether the ACRA
Singapore firm-survival data or the Taiwan credit-default data is the better
base for a classification-evaluation report.

Run `python bakeoff.py --self-test` first. It needs no network.
Then `python bakeoff.py`.
"""

# ----------------------------------------------------------------------
#  cell 2 - imports and configuration
import io, os, re, sys, json, zipfile, argparse, warnings
import numpy as np
import pandas as pd
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis as LDA,
    QuadraticDiscriminantAnalysis as QDA,
)
from sklearn.model_selection import (
    StratifiedKFold, cross_val_predict, train_test_split,
)
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, brier_score_loss

warnings.filterwarnings("ignore")
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 80)

# ---------------- configuration ----------------
RANDOM_STATE   = 42
TEST_SIZE      = 0.25      # held out, split first, used once
N_SPLITS       = 5         # k in k-fold
COST_FN_OVER_FP = 5.0      # a false negative costs this many times a false positive
LEAK_AUC_FLAG  = 0.80      # univariate AUC above this is FLAGGED for your judgement
AUTO_DROP_FLAGGED = False  # flagged != leaked. A genuinely strong predictor also scores high.
                           # Set True only after you have read the screen and agreed.
MAX_CAT        = 30        # cap one-hot cardinality, fitted in fold
CAT_CARD_MAX   = 12        # integer column with this many or fewer levels is treated as categorical

ACRA_COHORT    = (2010, 2015)   # incorporation window, equalises exposure time

# Dataset ids read off data.gov.sg page URLs. NOT verified by a successful download.
ACRA_LETTERS = {
    "A": "d_8575e84912df3c28995b8e6e0e05205a",
    "G": "d_b58303c68e9cf0d2ae93b73ffdbfbfa1",
    "S": "d_df7d2d661c0c11a7c367c9ee4bf896c1",
    "X": "d_1cd970d8351b42be4a308d628a6dd9d3",
    "Z": "d_4e3db8955fdcda6f9944097bef3d2724",
}

MODELS = {
    "Logistic": lambda: LogisticRegression(max_iter=3000),
    "GaussianNB": lambda: GaussianNB(),
    "LDA": lambda: LDA(solver="svd"),
}

OUTDIR = "results"


# ----------------------------------------------------------------------
#  cell 3 - small helpers, all name-agnostic

def _norm(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).strip().lower()).strip("_")

def resolve(cols, candidates):
    # exact normalised match first, then substring
    m = {_norm(c): c for c in cols}
    for cand in candidates:
        k = _norm(cand)
        if k in m:
            return m[k]
    for cand in candidates:
        k = _norm(cand)
        for nk, orig in m.items():
            if k and k in nk:
                return orig
    return None

def schema_report(df, name, head=80):
    print(f"\n--- {name}: {df.shape[0]:,} rows x {df.shape[1]} cols ---")
    info = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "n_unique": df.nunique(dropna=True),
        "pct_missing": df.isna().mean().round(4),
    })
    print(info.head(head).to_string())
    return info

def split_types(df, max_card=CAT_CARD_MAX):
    # categorical if non-numeric, or numeric with few distinct levels
    num, cat = [], []
    for c in df.columns:
        s = df[c]
        if pd.api.types.is_numeric_dtype(s):
            (cat if s.nunique(dropna=True) <= max_card else num).append(c)
        else:
            cat.append(c)
    return num, cat

def make_pre(num, cat):
    num_p = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("sc", StandardScaler()),
    ])
    cat_p = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("oh", OneHotEncoder(drop="if_binary",
                             handle_unknown="infrequent_if_exist",
                             min_frequency=0.005, max_categories=MAX_CAT,
                             sparse_output=False)),
    ])
    parts = []
    if num: parts.append(("num", num_p, num))
    if cat: parts.append(("cat", cat_p, cat))
    return ColumnTransformer(parts, remainder="drop")

def wilson(count, nobs, alpha=0.05):
    try:
        from statsmodels.stats.proportion import proportion_confint
        return proportion_confint(count, nobs, alpha=alpha, method="wilson")
    except Exception:
        from math import sqrt
        if nobs == 0: return (np.nan, np.nan)
        z = 1.959963985
        p = count / nobs
        d = 1 + z**2/nobs
        c = (p + z**2/(2*nobs)) / d
        h = z*sqrt(p*(1-p)/nobs + z**2/(4*nobs**2)) / d
        return (max(0, c-h), min(1, c+h))



# ----------------------------------------------------------------------
#  cell 4 - Taiwan loader, three fallbacks

def load_taiwan():
    # 1) official UCI python client
    try:
        from ucimlrepo import fetch_ucirepo
        d = fetch_ucirepo(id=350)
        X = d.data.features.copy()
        y = d.data.targets.iloc[:, 0].copy()
        df = X.copy()
        df["__target__"] = pd.to_numeric(y, errors="coerce").values
        return df, "ucimlrepo id=350"
    except Exception as e:
        print("[taiwan] ucimlrepo failed:", repr(e)[:200])

    # 2) UCI static zip
    try:
        url = "https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip"
        blob = requests.get(url, timeout=180).content
        z = zipfile.ZipFile(io.BytesIO(blob))
        nm = [n for n in z.namelist() if n.lower().endswith((".xls", ".xlsx", ".csv"))][0]
        with z.open(nm) as fh:
            raw = fh.read()
        if nm.lower().endswith(".csv"):
            df = pd.read_csv(io.BytesIO(raw), header=1)
        else:
            df = pd.read_excel(io.BytesIO(raw), header=1)
        return _taiwan_tidy(df), f"UCI static zip ({nm})"
    except Exception as e:
        print("[taiwan] static zip failed:", repr(e)[:200])

    raise RuntimeError(
        "Taiwan load failed. Download 'default of credit card clients.xls' from "
        "https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients , "
        "upload it to Colab, then run: TW_RAW, TW_SRC = load_taiwan_from_file('/content/yourfile.xls')"
    )

def _taiwan_tidy(df):
    drop = [c for c in df.columns if _norm(c) == "id"]
    df = df.drop(columns=drop, errors="ignore")
    tgt = resolve(df.columns, ["default payment next month", "default_payment_next_month",
                               "default.payment.next.month", "Y", "default"])
    if tgt is None:
        tgt = df.columns[-1]
    df = df.rename(columns={tgt: "__target__"})
    df["__target__"] = pd.to_numeric(df["__target__"], errors="coerce")
    return df

def load_taiwan_from_file(path):
    df = pd.read_excel(path, header=1) if path.lower().endswith((".xls", ".xlsx")) else pd.read_csv(path, header=1)
    return _taiwan_tidy(df), f"manual upload ({path})"



# ----------------------------------------------------------------------
#  cell 5 - ACRA loader

ACRA_WANTED = {
    "status":   ["entity_status_description", "entity status description"],
    "inc_date": ["registration_incorporation_date", "registration incorporation date", "incorporation_date"],
    "etype":    ["entity_type_description"],
    "ctype":    ["company_type_description"],
    "constit":  ["business_constitution_description"],
    "ssic":     ["primary_ssic_code"],
    "postal":   ["postal_code"],
    # suspects - loaded on purpose so the leakage screen can measure them
    "officers": ["no_of_officers", "number_of_officers"],
    "acct_due": ["account_due_date"],
    "ar_date":  ["annual_return_date"],
}

def _datagovsg_url(ds_id):
    r = requests.get(
        f"https://api-open.data.gov.sg/v1/public/api/datasets/{ds_id}/poll-download",
        timeout=120,
    )
    r.raise_for_status()
    j = r.json()
    stack = [j]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            for k, v in cur.items():
                if k.lower() == "url" and isinstance(v, str) and v.startswith("http"):
                    return v
                stack.append(v)
        elif isinstance(cur, list):
            stack.extend(cur)
    raise RuntimeError("no url in poll-download payload: " + str(j)[:300])

def _read_acra_one(src, label):
    head = pd.read_csv(src, nrows=0)
    found, missing = {}, []
    for role, cands in ACRA_WANTED.items():
        col = resolve(head.columns, cands)
        if col is None:
            missing.append(role)
        else:
            found[role] = col
    if missing:
        print(f"  [{label}] roles not found: {missing}")
        print(f"  [{label}] actual header: {list(head.columns)}")
    usecols = list(dict.fromkeys(found.values()))
    df = pd.read_csv(src, usecols=usecols, low_memory=False, dtype=str)
    df = df.rename(columns={v: k for k, v in found.items()})
    df["__letter__"] = label
    return df

def load_acra(letters=ACRA_LETTERS, local_paths=None):
    frames = []
    if local_paths:
        for p in local_paths:
            print("reading", p)
            frames.append(_read_acra_one(p, p.split("/")[-1][:12]))
    else:
        for letter, ds_id in letters.items():
            try:
                print(f"resolving letter {letter} ...", end=" ")
                url = _datagovsg_url(ds_id)
                print("ok, downloading")
                frames.append(_read_acra_one(url, letter))
            except Exception as e:
                print(f"FAILED letter {letter}: {repr(e)[:180]}")
    if not frames:
        raise RuntimeError(
            "ACRA load failed. Open https://data.gov.sg/collections/2/view , download a few "
            "letter CSVs by hand, upload to Colab, then run: "
            "AC_RAW, AC_SRC = load_acra(local_paths=['/content/a.csv','/content/s.csv'])"
        )
    return pd.concat(frames, ignore_index=True), f"data.gov.sg letters {sorted(set(f['__letter__'].iloc[0] for f in frames))}"



# ----------------------------------------------------------------------
#  cell 6 - adapters. Each returns X, y, suspects, notes.

def adapt_taiwan(raw):
    df = raw.dropna(subset=["__target__"]).copy()
    y = df["__target__"].astype(int)
    X = df.drop(columns=["__target__"])
    X = X.apply(pd.to_numeric, errors="coerce")
    notes = [f"rows {len(X):,}", "no leakage suspects declared - all features are pre-outcome by construction"]
    return X, y, [], notes

def adapt_acra(raw, cohort=ACRA_COHORT):
    df = raw.copy()
    notes = [f"raw rows {len(df):,}"]

    inc = pd.to_datetime(df["inc_date"], errors="coerce", format="mixed")
    df["inc_year"] = inc.dt.year
    df["inc_month"] = inc.dt.month
    before = len(df)
    df = df[df["inc_year"].between(*cohort)]
    notes.append(f"cohort {cohort[0]}-{cohort[1]}: {len(df):,} rows kept of {before:,}")

    s = df["status"].map(_norm)
    is_pos = s.str.contains("struck", na=False)
    is_neg = s.str.startswith("live", na=False)
    keep = is_pos | is_neg
    notes.append(f"label Struck Off vs Live: {int(keep.sum()):,} rows kept, {int((~keep).sum()):,} other statuses dropped")
    notes.append("other statuses present: " + ", ".join(df.loc[~keep, "status"].value_counts().head(8).index.astype(str)))
    df = df[keep]
    y = is_pos[keep].astype(int)

    # transparent reductions
    df["ssic2"] = df["ssic"].astype(str).str.extract(r"^(\d{2})")[0]
    df["postal2"] = df["postal"].astype(str).str.extract(r"^(\d{2})")[0]

    base = ["etype", "ctype", "constit", "ssic2", "postal2", "inc_year", "inc_month"]
    base = [c for c in base if c in df.columns]

    # suspects, measured then dropped
    df["sus_officers"] = pd.to_numeric(df.get("officers"), errors="coerce")
    df["sus_acctdue_missing"] = df.get("acct_due").isna().astype(int) if "acct_due" in df else np.nan
    df["sus_ar_missing"] = df.get("ar_date").isna().astype(int) if "ar_date" in df else np.nan
    suspects = [c for c in ["sus_officers", "sus_acctdue_missing", "sus_ar_missing"] if c in df and df[c].notna().any()]

    X = df[base + suspects].copy()
    for c in ["inc_year", "inc_month"]:
        if c in X: X[c] = pd.to_numeric(X[c], errors="coerce")
    notes.append("NOTE letter-file sampling is by first letter of entity name, not random")
    return X, y.reset_index(drop=True), suspects, notes



# ----------------------------------------------------------------------
#  cell 7 - leakage screen. Run on TRAIN ONLY, otherwise the screen itself leaks the test set.

def leak_screen(X, y, cv=3):
    num, cat = split_types(X)
    skf = StratifiedKFold(cv, shuffle=True, random_state=RANDOM_STATE)
    rows = []
    for c in X.columns:
        auc = np.nan
        try:
            if c in num:
                v = pd.to_numeric(X[c], errors="coerce")
                v = v.fillna(v.median())
                if v.nunique() > 1:
                    auc = roc_auc_score(y, v)
                    auc = max(auc, 1 - auc)
            else:
                sub = X[[c]]
                if sub[c].nunique(dropna=True) > 1:
                    pipe = Pipeline([("pre", make_pre([], [c])),
                                     ("clf", LogisticRegression(max_iter=1000))])
                    p = cross_val_predict(pipe, sub, y, cv=skf, method="predict_proba")[:, 1]
                    auc = roc_auc_score(y, p)
        except Exception as e:
            pass
        miss = X[c].isna()
        dmiss = abs(miss[y == 1].mean() - miss[y == 0].mean()) if miss.any() else 0.0
        rows.append({"feature": c, "univariate_auc": auc,
                     "pct_missing": float(miss.mean()),
                     "diff_missing_by_class": float(dmiss)})
    out = pd.DataFrame(rows).sort_values("univariate_auc", ascending=False).reset_index(drop=True)
    out["flag"] = np.where(out["univariate_auc"] >= LEAK_AUC_FLAG, "LEAK?", "")
    return out

def cost_curve(y, p, ratio=None):
    # read the global at CALL time, otherwise --cost-ratio is silently ignored
    if ratio is None:
        ratio = COST_FN_OVER_FP
    ts = np.linspace(0.005, 0.995, 199)
    y = np.asarray(y)
    cost, sens, spec = [], [], []
    P, N = (y == 1).sum(), (y == 0).sum()
    for t in ts:
        pred = (p >= t).astype(int)
        tp = ((pred == 1) & (y == 1)).sum()
        fp = ((pred == 1) & (y == 0)).sum()
        fn = P - tp
        tn = N - fp
        cost.append((fn * ratio + fp) / len(y))
        sens.append(tp / P if P else np.nan)
        spec.append(tn / N if N else np.nan)
    return ts, np.array(cost), np.array(sens), np.array(spec)



# ----------------------------------------------------------------------
#  cell 8 - the evaluation engine

def evaluate(name, X, y, suspects, notes, make_plots=True):
    X = X.reset_index(drop=True)
    y = pd.Series(np.asarray(y)).reset_index(drop=True).astype(int)
    res = {"dataset": name, "notes": list(notes), "ok": False}

    print("=" * 78)
    print(name)
    print("=" * 78)
    for n in notes:
        print(" *", n)

    if len(X) < 500 or y.nunique() < 2:
        print("!! too small or single-class, stopping")
        res["fail_reason"] = "insufficient rows or single class"
        return res

    # ---- 1. split the held-out set FIRST, touch it once at the very end
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE)
    Xtr, Xte = Xtr.reset_index(drop=True), Xte.reset_index(drop=True)
    ytr, yte = ytr.reset_index(drop=True), yte.reset_index(drop=True)

    res["n_total"] = len(X)
    res["prevalence"] = float(y.mean())
    res["n_train_pos"] = int(ytr.sum())
    res["n_test_pos"] = int(yte.sum())
    print(f"\nrows {len(X):,} | prevalence {y.mean():.4f} | train pos {int(ytr.sum()):,} | test pos {int(yte.sum()):,}")

    # ---- 2. leakage screen on the training data only
    scr = leak_screen(Xtr, ytr)
    print("\nleakage screen (train only):")
    print(scr.to_string(index=False))
    res["leak_table"] = scr
    flagged = scr.loc[scr["flag"] == "LEAK?", "feature"].tolist()
    res["flagged"] = flagged

    # ---- 3. naive versus audited, using logistic only, to price the leakage
    def cv_auc(cols, Xa, ya):
        if not cols: return np.nan
        n, c = split_types(Xa[cols])
        pipe = Pipeline([("pre", make_pre(n, c)), ("clf", LogisticRegression(max_iter=3000))])
        skf = StratifiedKFold(N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
        p = cross_val_predict(pipe, Xa[cols], ya, cv=skf, method="predict_proba")[:, 1]
        return roc_auc_score(ya, p)

    all_cols = list(Xtr.columns)
    if flagged:
        print("\n!! FLAGGED for your judgement (high univariate AUC):", flagged)
        print("   A flagged feature is not automatically leakage. A genuinely strong")
        print("   predictor scores high too. Declared suspects are dropped; flagged")
        print("   features are kept unless AUTO_DROP_FLAGGED is True.")
    drop_set = set(suspects) | (set(flagged) if AUTO_DROP_FLAGGED else set())
    audited_cols = [c for c in all_cols if c not in drop_set]
    res["dropped_cols"] = sorted(drop_set)
    res["n_features_audited"] = len(audited_cols)

    naive_auc = cv_auc(all_cols, Xtr, ytr)
    audited_auc = cv_auc(audited_cols, Xtr, ytr) if audited_cols else np.nan
    res["auc_naive"] = naive_auc
    res["auc_audited_logit"] = audited_auc
    res["leakage_premium"] = (naive_auc - audited_auc) if np.isfinite(naive_auc) and np.isfinite(audited_auc) else np.nan
    print(f"\nlogistic CV AUC with everything      : {naive_auc:.4f}")
    print(f"logistic CV AUC after the audit      : {audited_auc:.4f}")
    print(f"leakage premium (how much was fake)  : {res['leakage_premium']:.4f}")
    print(f"dropped: {sorted(drop_set) if drop_set else 'nothing'}")

    if not audited_cols:
        res["fail_reason"] = "no features survive the audit"
        return res

    Xtr_a, Xte_a = Xtr[audited_cols], Xte[audited_cols]
    num, cat = split_types(Xtr_a)
    print(f"\nfeature typing -> numeric {num}\n                 categorical {cat}")
    res["numeric"], res["categorical"] = num, cat

    # ---- 4. three models, k-fold CV, all preprocessing inside the fold
    skf = StratifiedKFold(N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    oof, fold_auc, cv_auc_by_model, brier = {}, {}, {}, {}
    for mname, mk in MODELS.items():
        pipe = Pipeline([("pre", make_pre(num, cat)), ("clf", mk())])
        p = cross_val_predict(pipe, Xtr_a, ytr, cv=skf, method="predict_proba")[:, 1]
        oof[mname] = p
        cv_auc_by_model[mname] = roc_auc_score(ytr, p)
        brier[mname] = brier_score_loss(ytr, p)
        fa = []
        for tr_i, va_i in skf.split(Xtr_a, ytr):
            fa.append(roc_auc_score(ytr.iloc[va_i], p[va_i]))
        fold_auc[mname] = np.array(fa)
    res["cv_auc"] = cv_auc_by_model
    res["brier"] = brier
    res["fold_auc"] = fold_auc

    print("\nCV AUC (out of fold, train only):")
    for m in MODELS:
        print(f"  {m:<12} AUC {cv_auc_by_model[m]:.4f}   Brier {brier[m]:.4f}   "
              f"fold sd {fold_auc[m].std(ddof=1):.4f}")

    best = max(cv_auc_by_model, key=cv_auc_by_model.get)
    worst = min(cv_auc_by_model, key=cv_auc_by_model.get)
    spread = cv_auc_by_model[best] - cv_auc_by_model[worst]
    d = fold_auc[best] - fold_auc[worst]
    se = d.std(ddof=1) / np.sqrt(len(d))
    res["best_model"], res["auc_spread"] = best, spread
    res["separation_se"] = float(se)
    res["separated"] = bool(abs(d.mean()) > 2 * se) if se > 0 else False
    res["paired_fold_diff"] = float(d.mean())
    print(f"\nbest {best} vs worst {worst}")
    print(f"  pooled OOF AUC gap      {spread:.4f}")
    print(f"  mean paired fold gap    {d.mean():.4f}  (this is what the test uses)")
    print(f"  paired fold SE          {se:.4f}")
    print(f"  separated beyond noise  {res['separated']}  (|mean gap| > 2 SE)")

    # ---- 5. threshold chosen from train out-of-fold predictions only
    ts, cost, sens, spec = cost_curve(ytr, oof[best])
    t_emp = float(ts[int(np.argmin(cost))])
    t_theo = 1.0 / (1.0 + COST_FN_OVER_FP)
    c_half = float(cost[int(np.argmin(np.abs(ts - 0.5)))])
    c_theo = float(cost[int(np.argmin(np.abs(ts - t_theo)))])
    c_emp = float(cost.min())
    prev = float(ytr.mean())
    cost_all_neg = prev * COST_FN_OVER_FP        # predict nobody defaults
    cost_all_pos = 1.0 - prev                    # predict everybody defaults
    c_triv = min(cost_all_neg, cost_all_pos)
    res.update({"t_empirical": t_emp, "t_theoretical": t_theo,
                "cost_at_half": c_half, "cost_at_theo": c_theo, "cost_at_emp": c_emp,
                "cost_trivial": c_triv,
                "cost_reduction_vs_half": (c_half - c_emp) / c_half if c_half else np.nan,
                "cost_reduction_vs_trivial": (c_triv - c_emp) / c_triv if c_triv else np.nan})
    print(f"\nthreshold from train OOF: empirical {t_emp:.3f}, theoretical {t_theo:.3f}")
    print(f"expected cost per case  : 0.5 -> {c_half:.4f} | t* -> {c_theo:.4f} | empirical -> {c_emp:.4f}")
    print(f"best trivial rule cost  : {c_triv:.4f} "
          f"({'predict all negative' if cost_all_neg <= cost_all_pos else 'predict all positive'})")
    print(f"cost reduction versus 0.5           : {res['cost_reduction_vs_half']*100:.1f}%")
    print(f"cost reduction versus trivial rule  : {res['cost_reduction_vs_trivial']*100:.1f}%  <-- the one that matters")

    # ---- 6. diagnostics that explain WHY the models differ
    pre = make_pre(num, cat).fit(Xtr_a, ytr)
    M = np.asarray(pre.transform(Xtr_a), dtype=float)
    keep = M.std(axis=0) > 1e-9
    M = M[:, keep]
    if M.shape[1] > 1:
        C = np.corrcoef(M, rowvar=False)
        off = np.abs(C[~np.eye(C.shape[0], dtype=bool)])
        off = off[np.isfinite(off)]
        real = off[off < 0.999]        # drop structurally collinear dummy pairs
        res["mean_abs_corr"] = float(np.nanmean(real)) if real.size else np.nan
        res["p95_abs_corr"] = float(np.nanpercentile(real, 95)) if real.size else np.nan
    else:
        res["mean_abs_corr"] = res["p95_abs_corr"] = np.nan
    try:
        qp = Pipeline([("pre", make_pre(num, cat)), ("clf", QDA(reg_param=0.05))])
        pq = cross_val_predict(qp, Xtr_a, ytr, cv=skf, method="predict_proba")[:, 1]
        res["auc_qda"] = roc_auc_score(ytr, pq)
    except Exception:
        res["auc_qda"] = np.nan
    res["qda_minus_lda"] = res["auc_qda"] - cv_auc_by_model["LDA"] if np.isfinite(res["auc_qda"]) else np.nan
    print(f"\ndiagnostics: mean |corr| {res['mean_abs_corr']:.3f} (NB independence), "
          f"95th pct |corr| {res['p95_abs_corr']:.3f}")
    print(f"             QDA minus LDA AUC {res['qda_minus_lda']:.4f} (equal-covariance cost)")

    # ---- 7. the held-out set, used exactly once
    final = Pipeline([("pre", make_pre(num, cat)), ("clf", MODELS[best]())]).fit(Xtr_a, ytr)
    pte = final.predict_proba(Xte_a)[:, 1]
    res["test_auc"] = roc_auc_score(yte, pte)
    res["cv_minus_test_auc"] = cv_auc_by_model[best] - res["test_auc"]
    pred = (pte >= t_emp).astype(int)
    tn, fp, fn, tp = confusion_matrix(yte, pred, labels=[0, 1]).ravel()
    res["test_sens"] = tp / (tp + fn) if (tp + fn) else np.nan
    res["test_spec"] = tn / (tn + fp) if (tn + fp) else np.nan
    lo, hi = wilson(tp, tp + fn)
    res["test_sens_ci"] = (lo, hi)
    res["test_sens_ci_width"] = hi - lo
    print(f"\nheld out (used once): AUC {res['test_auc']:.4f} "
          f"(CV minus test {res['cv_minus_test_auc']:+.4f})")
    print(f"at t={t_emp:.3f}: sens {res['test_sens']:.3f} [{lo:.3f}, {hi:.3f}] "
          f"width {hi-lo:.3f} | spec {res['test_spec']:.3f}")
    print(f"confusion matrix (test): TN {tn} FP {fp} FN {fn} TP {tp}")

    if make_plots:
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
        for m in MODELS:
            fpr, tpr, _ = roc_curve(ytr, oof[m])
            ax[0].plot(fpr, tpr, lw=1.6, label=f"{m} {cv_auc_by_model[m]:.3f}")
        ax[0].plot([0, 1], [0, 1], "k--", lw=0.8)
        ax[0].set_xlabel("1 - specificity"); ax[0].set_ylabel("sensitivity")
        ax[0].set_title(f"{name}: out-of-fold ROC"); ax[0].legend(fontsize=8)
        ax[1].plot(ts, sens, label="sensitivity")
        ax[1].plot(ts, spec, label="specificity")
        ax[1].plot(ts, cost / cost.max(), label="expected cost (scaled)")
        ax[1].axvline(t_emp, color="k", ls=":", lw=1, label=f"t empirical {t_emp:.2f}")
        ax[1].axvline(t_theo, color="r", ls=":", lw=1, label=f"t theoretical {t_theo:.2f}")
        ax[1].set_xlabel("threshold"); ax[1].set_title(f"{name}: threshold sweep ({best})")
        ax[1].legend(fontsize=8)
        plt.tight_layout()
        _p = os.path.join(OUTDIR, "roc_" + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") + ".png")
        plt.savefig(_p, dpi=140); plt.close()
        print("saved plot ->", _p)

    res["ok"] = True
    return res



# =====================================================================
#  scorecard
# =====================================================================
CRITERIA = [
    ("n_train_pos", "Train positives", lambda r: r.get("n_train_pos"), lambda v: v >= 500, ">= 500"),
    ("n_test_pos", "Held-out positives", lambda r: r.get("n_test_pos"), lambda v: v >= 100, ">= 100"),
    ("n_features_audited", "Features after audit", lambda r: r.get("n_features_audited"), lambda v: v >= 5, ">= 5"),
    ("best_auc", "Best CV AUC", lambda r: max(r["cv_auc"].values()) if r.get("cv_auc") else np.nan, lambda v: v >= 0.62, ">= 0.62"),
    ("max_univ_audited", "Max univariate AUC left", None, lambda v: v <= 0.85, "<= 0.85"),
    ("separated", "Models separate beyond noise", lambda r: r.get("separated"), lambda v: bool(v), "True"),
    ("cost_reduction_vs_trivial", "Cost cut vs best trivial rule", lambda r: r.get("cost_reduction_vs_trivial"), lambda v: v >= 0.05, ">= 5%"),
    ("cv_minus_test_auc", "|CV AUC - test AUC|", lambda r: abs(r.get("cv_minus_test_auc", np.nan)), lambda v: v <= 0.03, "<= 0.03"),
    ("test_sens_ci_width", "95% CI width, test sens", lambda r: r.get("test_sens_ci_width"), lambda v: v <= 0.20, "<= 0.20"),
]

def max_univ_audited(r):
    t = r.get("leak_table")
    if t is None: return np.nan
    keep = t[~t["feature"].isin(r.get("dropped_cols", []))]
    return float(keep["univariate_auc"].max()) if len(keep) else np.nan

def scorecard(RESULTS, outdir=None):
    outdir = outdir or OUTDIR
    usable = {k: v for k, v in RESULTS.items() if v.get("ok")}
    if not usable:
        print("\nNo dataset evaluated successfully. Fix the loaders first.")
        return {}
    rows, passes = [], {}
    for key, label, getter, test, thresh in CRITERIA:
        row = {"criterion": label, "target": thresh}
        for dname, r in usable.items():
            v = max_univ_audited(r) if key == "max_univ_audited" else getter(r)
            try: ok = bool(test(v))
            except Exception: ok, v = False, np.nan
            passes.setdefault(dname, []).append(ok)
            row[dname] = (f"{v:.4f}" if isinstance(v, float) and np.isfinite(v) else str(v)) + ("  PASS" if ok else "  fail")
        rows.append(row)
    score = pd.DataFrame(rows).set_index("criterion")

    extra = []
    for dname, r in usable.items():
        extra.append({
            "dataset": dname,
            "rows": f"{r.get('n_total', 0):,}",
            "prevalence": f"{r.get('prevalence', np.nan):.4f}",
            "AUC naive": f"{r.get('auc_naive', np.nan):.4f}",
            "AUC audited": f"{r.get('auc_audited_logit', np.nan):.4f}",
            "leakage premium": f"{r.get('leakage_premium', np.nan):.4f}",
            "dropped": ", ".join(r.get("dropped_cols", [])) or "none",
            "flagged not dropped": ", ".join([c for c in r.get("flagged", []) if c not in r.get("dropped_cols", [])]) or "none",
            "best model": r.get("best_model"),
            "AUC spread (pooled)": f"{r.get('auc_spread', np.nan):.4f}",
            "paired fold gap": f"{r.get('paired_fold_diff', np.nan):.4f}",
            "mean |corr|": f"{r.get('mean_abs_corr', np.nan):.3f}",
            "p95 |corr|": f"{r.get('p95_abs_corr', np.nan):.3f}",
            "QDA - LDA": f"{r.get('qda_minus_lda', np.nan):+.4f}",
            "t empirical": f"{r.get('t_empirical', np.nan):.3f}",
            "t theoretical": f"{r.get('t_theoretical', np.nan):.3f}",
            "cost cut vs 0.5": f"{r.get('cost_reduction_vs_half', np.nan)*100:.1f}%",
            "cost cut vs trivial": f"{r.get('cost_reduction_vs_trivial', np.nan)*100:.1f}%",
            "Brier spread": f"{max(r['brier'].values()) - min(r['brier'].values()):.4f}" if r.get("brier") else "",
        })
    supp = pd.DataFrame(extra).set_index("dataset").T

    print("\n" + "=" * 78); print("SCORECARD"); print("=" * 78)
    print(score.to_string())
    print("\n" + "-" * 78); print("SUPPORTING NUMBERS (not pass/fail)"); print("-" * 78)
    print(supp.to_string())

    tally = {d: sum(v) for d, v in passes.items()}
    lines = ["VERDICT", "=" * 78]
    for d, n in sorted(tally.items(), key=lambda kv: -kv[1]):
        lines.append(f"  {d:<28} {n} of {len(CRITERIA)} criteria passed")
    if len(tally) < 2:
        lines.append("\nOnly one dataset loaded. Fix the other loader before deciding.")
    else:
        ranked = sorted(tally.items(), key=lambda kv: -kv[1])
        (d1, n1), (d2, n2) = ranked[0], ranked[1]
        if n1 > n2:
            lines.append(f"\n-> {d1} wins on measured criteria, {n1} versus {n2}.")
        else:
            lines.append(f"\n-> Tie at {n1} criteria each. Both are technically adequate, so the")
            lines.append("   decision falls back to novelty, which favours ACRA.")
        lines.append("")
        lines.append("Read the failures, not just the tally. A fail on 'Models separate beyond")
        lines.append("noise' or on 'Cost cut vs best trivial rule' guts a required section of the")
        lines.append("brief and outweighs a fail on CI width, which only makes one comparison")
        lines.append("noisier.")
    verdict = "\n".join(lines)
    print("\n" + "=" * 78); print(verdict)

    os.makedirs(outdir, exist_ok=True)
    score.to_csv(os.path.join(outdir, "scorecard.csv"))
    supp.to_csv(os.path.join(outdir, "supporting_numbers.csv"))
    open(os.path.join(outdir, "verdict.txt"), "w").write(verdict + "\n")
    for dname, r in usable.items():
        slug = re.sub(r"[^a-z0-9]+", "_", dname.lower()).strip("_")
        if r.get("leak_table") is not None:
            r["leak_table"].to_csv(os.path.join(outdir, f"leakage_screen_{slug}.csv"), index=False)
    dump = {d: {k: v for k, v in r.items() if k != "leak_table"} for d, r in usable.items()}
    def _j(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.ndarray,)): return o.tolist()
        return str(o)
    open(os.path.join(outdir, "results.json"), "w").write(json.dumps(dump, indent=2, default=_j))
    print(f"\nwrote {outdir}/scorecard.csv, supporting_numbers.csv, verdict.txt, "
          f"results.json, leakage_screen_*.csv and roc_*.png")
    return tally


# =====================================================================
#  synthetic self test - proves the pipeline works with no network
# =====================================================================
def self_test():
    rng = np.random.default_rng(0); n = 12000
    yr = rng.integers(2008, 2018, n)
    ssic = rng.choice(["46100", "62011", "70201", "56111", "41000", "82300"], n)
    lin = (ssic == "56111") * 0.8 + (ssic == "41000") * 0.5 - (ssic == "62011") * 0.4 + rng.normal(0, 1, n)
    struck = lin > 0.6
    status = np.where(struck, "Struck Off", "Live Company")
    status[rng.random(n) < 0.08] = "Dissolved"
    acra_raw = pd.DataFrame({
        "status": status,
        "inc_date": [f"{y}-0{rng.integers(1,9)}-15" for y in yr],
        "etype": rng.choice(["Local Company", "Business", "LLP"], n, p=[.7, .25, .05]),
        "ctype": rng.choice(["PRIVATE COMPANY LIMITED BY SHARES", "EXEMPT PRIVATE"], n),
        "constit": rng.choice(["Local Company", "Sole Proprietor"], n),
        "ssic": ssic,
        "postal": [f"{rng.integers(10,82):02d}{rng.integers(1000,9999)}" for _ in range(n)],
        "officers": np.where(struck, 0, rng.integers(1, 6, n)).astype(str),   # planted leak
        "acct_due": rng.choice(["2024-06-30", None], n),
        "ar_date": np.where(struck, None, "2024-01-01"),                      # planted leak
    })
    m = 9000
    tw = pd.DataFrame({
        "LIMIT_BAL": rng.lognormal(11, 0.6, m), "SEX": rng.integers(1, 3, m),
        "EDUCATION": rng.integers(0, 7, m), "PAY_0": rng.integers(-2, 9, m),
        "PAY_2": rng.integers(-2, 9, m), "AGE": rng.integers(21, 70, m),
        "BILL_AMT1": rng.normal(50000, 30000, m)})
    tw["BILL_AMT2"] = tw["BILL_AMT1"] * 0.95 + rng.normal(0, 3000, m)
    z = 0.35 * tw["PAY_0"] - 0.000004 * tw["LIMIT_BAL"] + rng.normal(0, 1, m)
    tw["__target__"] = (z > np.quantile(z, 0.78)).astype(int)

    R = {}
    Xt, yt, st, nt = adapt_taiwan(tw)
    R["Taiwan SYNTHETIC"] = evaluate("Taiwan SYNTHETIC", Xt, yt, st, nt)
    Xa, ya, sa, na = adapt_acra(acra_raw)
    R["ACRA SYNTHETIC"] = evaluate("ACRA SYNTHETIC", Xa, ya, sa, na)
    scorecard(R)
    print("\nSELF TEST COMPLETE. Expect the planted leaks to show as a large ACRA")
    print("leakage premium, and Taiwan's premium to be 0.0000 with PAY_0 flagged but kept.")


# =====================================================================
def main():
    global COST_FN_OVER_FP, ACRA_COHORT, AUTO_DROP_FLAGGED, OUTDIR, N_SPLITS, TEST_SIZE
    ap = argparse.ArgumentParser(description="DSA211 dataset bake-off: ACRA vs Taiwan credit default")
    ap.add_argument("--cost-ratio", type=float, default=COST_FN_OVER_FP,
                    help="C_FN / C_FP. Changes the chosen threshold and one criterion.")
    ap.add_argument("--cohort", type=int, nargs=2, default=list(ACRA_COHORT),
                    metavar=("FROM", "TO"), help="ACRA incorporation-year window")
    ap.add_argument("--letters", type=str, default=",".join(ACRA_LETTERS),
                    help="comma separated ACRA letter files, e.g. A,G,S")
    ap.add_argument("--acra-local", type=str, nargs="*", default=None,
                    help="local ACRA CSV paths, skips the download")
    ap.add_argument("--taiwan-local", type=str, default=None,
                    help="local UCI xls/csv path, skips the download")
    ap.add_argument("--auto-drop-flagged", action="store_true",
                    help="drop high-univariate-AUC features automatically. Off by default on purpose.")
    ap.add_argument("--folds", type=int, default=N_SPLITS)
    ap.add_argument("--test-size", type=float, default=TEST_SIZE)
    ap.add_argument("--outdir", type=str, default="results")
    ap.add_argument("--only", choices=["taiwan", "acra"], default=None)
    ap.add_argument("--self-test", action="store_true",
                    help="run on synthetic data with a planted leak, no network needed")
    a = ap.parse_args()

    COST_FN_OVER_FP = a.cost_ratio
    ACRA_COHORT = tuple(a.cohort)
    AUTO_DROP_FLAGGED = a.auto_drop_flagged
    N_SPLITS, TEST_SIZE, OUTDIR = a.folds, a.test_size, a.outdir
    os.makedirs(OUTDIR, exist_ok=True)

    print(f"cost ratio C_FN/C_FP = {COST_FN_OVER_FP}")
    print(f"theoretical Bayes threshold t* = {1/(1+COST_FN_OVER_FP):.4f}")
    print(f"folds {N_SPLITS} | test size {TEST_SIZE} | cohort {ACRA_COHORT} | "
          f"auto-drop flagged {AUTO_DROP_FLAGGED}")

    if a.self_test:
        self_test(); return

    RESULTS = {}

    if a.only != "acra":
        try:
            tw_raw, src = (load_taiwan_from_file(a.taiwan_local) if a.taiwan_local else load_taiwan())
            print("\nTaiwan source:", src)
            schema_report(tw_raw, "TAIWAN raw")
            X, y, s, nts = adapt_taiwan(tw_raw)
            RESULTS["Taiwan credit default"] = evaluate("Taiwan credit default", X, y, s, nts)
        except Exception as e:
            print("\nTAIWAN FAILED:", e)

    if a.only != "taiwan":
        try:
            letters = {k: v for k, v in ACRA_LETTERS.items() if k in a.letters.split(",")}
            ac_raw, src = load_acra(letters=letters, local_paths=a.acra_local)
            print("\nACRA source:", src)
            schema_report(ac_raw, "ACRA raw")
            print("\nfull status distribution:\n", ac_raw["status"].value_counts(dropna=False).head(25))
            X, y, s, nas = adapt_acra(ac_raw, cohort=ACRA_COHORT)
            RESULTS["ACRA firm survival"] = evaluate("ACRA firm survival", X, y, s, nas)
        except Exception as e:
            print("\nACRA FAILED:", e)

    scorecard(RESULTS)


if __name__ == "__main__":
    main()
