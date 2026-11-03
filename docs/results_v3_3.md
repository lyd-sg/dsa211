# DSA211 PRD v3.3 — verified execution and interpretation

**Execution:** [GitHub Actions 41622824180](https://github.com/lyd-sg/dsa211/actions/runs/41622824180) — **SUCCESS**.  
**Verified source:** [executed v3.3 notebook](../archive/versions/v3.3/online_shoppers_prd_v3_3.ipynb).  
**Evidence:** [v3.3 trial ledger](../artifacts/prd_v3_3/all_attempts_ledger.csv), [fold scores](../artifacts/prd_v3_3/all_attempt_fold_scores.csv), [independent audit](../artifacts/prd_v3_3/independent_training_audit.json), [six finalists](../artifacts/prd_v3_3/six_finalists.csv), [run metadata](../artifacts/prd_v3_3/run_metadata.json).

## 1. Validation status

**PASS:** All 37 cells retained, all 20 Python cells executed with zero error outputs. Evidence audit independently recomputed **48 CV model specifications**, **240 model-fold AUC/AP results**, **34** nonbaseline strict one-SE decisions (16 v3.1, 11 v3.2, 7 v3.3), all **722** tree-alpha candidates/**3,610** pruning folds, six finalists and four winner-only threshold references. All original dataset/provenance and historical project versions were preserved.

The v3.3 dataset remains 12,330 sessions, training 9,864 and historically reused reserved 2,466, shared stratified seed-42 folds. No new out-of-sample claim is warranted from repeated historical reserved-set use.

## 2. Every v3.3 candidate, against the frozen v3.2 family anchor

| ID | Single EDA-motivated revision | Mean 5-fold CV AUC | CV AUC SE | Gain over anchor | Pass gain > challenger SE? |
|---|---|---:|---:|---:|---|
| L8 | BounceRates fixed 0.01-knot piecewise linear basis | 0.7586176 | 0.0054391 | +0.0011502 | No |
| L9 | SpecialDay categorical one-hot | 0.7584630 | 0.0061719 | +0.0009956 | No |
| L10 | Add duration per product page, safe zero denominator | 0.7585475 | 0.0061452 | +0.0010801 | No |
| D8 | log1p ProductRelated only | 0.7412646 | 0.0054471 | +0.0003860 | No |
| D9 | Fold-trained p99 winsorise ProductRelated_Duration | 0.7430076 | 0.0062573 | +0.0021289 | No |
| D10 | Add Informational >0 indicator | 0.7417008 | 0.0055717 | +0.0008222 | No |
| D11 | BounceRates nominal zero / low-positive / high-positive bands | 0.7363376 | 0.0051678 | −0.0045410 | No |

Comparison anchors: L1 Logit **0.7574674** and D0 LDA **0.7408787**. Each of the seven was evaluated **even though none qualified**. Six raised point-estimated mean AUC slightly; one (D11) reduced it. Rejection means the strict pre-existing model-selection rule was not satisfied, **not** that a formal hypothesis test disproved the EDA.

## 3. Interpretation by family

**Logit:** All three v3.3 variations generated small positive mean CV AUC gains (~0.001). Their effect is limited relative to the ~0.0054–0.0062 challenger SE. The feature relationships described by marginal EDA may be largely captured by retained L1 log1p activity terms and existing predictors, or may require differently structured nonlinear hypotheses; these results do not distinguish those explanations. L8's piecewise representation was not clearly more successful than the earlier rejected L5 quadratic term.

**LDA:** After **11 attempted modifications** (D1–D4, D5–D7, D8–D11), no single change has qualified. D9's p99 winsorisation was the most promising v3.3 trial (+0.00213), but still well below its own SE (0.00626). The earlier blanket log1p D1 improved AUC more (+0.00285) than D9, but also failed the original one-SE rule. LDA's original linear discriminant may be robust to moderate changes in representation; its normality assumptions are not established by the data. These results demonstrate that improving a marginal distribution's shape does not necessarily improve multivariable prediction by enough to justify adopting the change.

**D11:** The rough three-level BounceRates categorisation produced a lower AUC than continuous BounceRates. A plausible explanation is lost continuous discrimination after coarse binning, but no diagnostic here proves that mechanism.

## 4. Final six-way competition (v3.3)

| Finalist | Mean five-fold CV ROC-AUC | Mean AP |
|---|---:|---:|
| **L1 Logistic Regression** | **0.7574674** | 0.3362262 |
| Selected Entropy tree | 0.7441426 | 0.3130022 |
| B3 Bernoulli NB | 0.7422679 | 0.3015810 |
| D0 LDA | 0.7408787 | 0.3164879 |
| Selected Gini tree | 0.7330554 | 0.3038944 |
| G7 Gaussian NB | 0.7128375 | 0.2679294 |

**Chosen winner:** L1 Logistic Regression; unchanged from v3.2. Its historically reused reserved check: **ROC-AUC 0.7405425**, **AP 0.3271986**. Do not describe this as a pristine lifetime-independent test, a significance demonstration or calibrated causal business impact.

## 5. Recommendation

**Stop broad specification searching after v3.3.** The trained family comparison already presents substantive EDA-driven transformations, transparent negative/positive findings and an interpretable course-scope winning model. Numerous additional post-hoc candidates using the same five folds would exacerbate selection optimism and risk confusing an academic EDA-guided workflow with an indefinite optimisation exercise.

If further work is required by the course team, prioritise explaining why the Logit L1 activity transformation was accepted, why G7 GNB benefited from only ProductRelated_Duration log1p, and why 11 LDA transformations did not meet the retention criterion. Do not change the statistical threshold merely to force an accepted LDA revision.
