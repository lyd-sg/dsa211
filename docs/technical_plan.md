# DSA211 — Technical implementation plan v2.0
**Date:** 27 October 2026  
**Governing specification:** [Approved PRD v2.0](PRD_v2.md)  
**Status:** Implementation plan for PRD v2.0; execution and independent validation required.  
**Historical reference:** [Archived v1 plan](technical_plan_v1_archive.md), preserved as historical documentation; not current implementation authority.

## 1. Scope, inputs and non-goals

Implement the approved **prediction-only** PRD v2.0 in `online_shoppers_revised.ipynb`. Preserve the existing, already validated **seven operational candidates**, training-fold assignments, primary mean five-fold ROC-AUC ranking, supporting AP and numerical safeguards. Retain the separate, training-only supplementary EDA notebook.

**Remove completely from the active main notebook:** voucher issuance, prices, discount costs, fixed threshold `2/3`, conversion parameter `q`, voucher-count/share and revenue calculations, policy conclusions and corresponding obsolete plots/artifacts generated during execution. Archived evidence may remain with clear historical status.

New threshold analysis is **purchase classification only**: reference cutoffs (a) exact training prevalence, (b) `0.5`, and (c) training-OOF sensitivity–specificity crossover. **Crossover is the selected balanced operating reference**, not a universally best or cost-optimised threshold. Include one winner PR curve and report average precision explicitly due to imbalance.

### File contract
| Path | Treatment |
|---|---|
| `online_shoppers_revised.ipynb` | Update headings, purpose-first interpretations, winner PR plot, 3-threshold OOF table/curve, refit and summary |
| `docs/technical_plan.md` | Replace historical technical plan with this approved-PRD-aligned plan |
| `docs/technical_plan_v1_archive.md` | Preserve old plan byte-for-byte; history only |
| `docs/PRD_v2.md` | Preserve approved requirements unchanged |
| `docs/PRD.md`, `data/uci_468.csv`, `archive/`, `supplementary/training_eda.ipynb` | Preserve original files; no source or training-EDA rewrites |
| `README.md` and current guidance | Update active scope; link approved PRD v2.0; label legacy voucher documents historical |
| `artifacts/` | Emit new version-specific training CV, OOF predictions, threshold, PR and refit evidence; old economic artifacts remain historical, not current |
| `.github/workflows/validate-notebook.yml` | Preserve existing CI executor; run notebook using actual 12,330 source records on PR |

No new model families, hyperparameter sweeps, automated feature elimination, causal claims, calibration experiment, voucher scenario or unapproved decision rule.

## 2. Data, split and leakage contract

1. Read `data/uci_468.csv`; validate exactly **12,330 sessions, 17 source predictors and binary Revenue**; check missing/blank/nonfinite values, types and duplicate excess **before** split. Retain all records, including **125 excess exact duplicates**, with their statistical limitations.
2. Reproduce `train_test_split(test_size=.2, stratify=Revenue, random_state=42)` to **9,864 training / 2,466 reserved historical rows** and save source row IDs; train-only EDA and model selection never fit on excluded rows.
3. Reuse **five identical shuffled stratified training folds** with seed `42` for all baseline, revised and all-17 diagnostic candidates. Each of the 9,864 training rows must be predicted **exactly once OOF per candidate**.
4. Every fitted transformation/encoder/scaler, category map, presence-column eligibility and covariance estimate must be learned on the specific fold's fitting rows only. A model's validation fold is never used for its fit.
5. **Evidence boundary:** the current regularised revision reports cross-validation results, not a fresh independent held-out test AUC/AP. Do not score the historical holdout to present the changed winner as independently validated. Existing test artifacts are historical and do not evaluate the new recipe.
6. At the end, clone the winner's exact frozen specification, check a full **training-only fit** for numerical validity, then refit the same frozen specification on **all 12,330 records**, without new candidate choice or in-sample metric reported as predictive generalisation. The final full-data recipe is not a fresh validation.

## 3. Predictor and baseline contracts

- All-17 models: four training-only diagnostic comparisons with `PageValues`; include the fact that its availability at prediction time is uncertain, so it is excluded from operational models. Correlation with the outcome alone is not proof of leakage.
- Operational models: all start from the same 16 remaining original sources. Six nominal predictors are `Month`, `OperatingSystems`, `Browser`, `Region`, `TrafficType`, `VisitorType`. `Weekend` is binary. `SpecialDay` remains numeric unless a specified revised model changes representation.
- Raw Logit: unpenalised `LogisticRegression(C=np.inf, solver='newton-cg', tol=1e-8, max_iter=2000)`; original numeric magnitudes, `SpecialDay`, `Weekend`; k−1 categorical dummies.
- Gaussian NB: raw numeric plus full-k categorical one-hot indicators, default GaussianNB.
- Bernoulli NB: numeric `>0` indicators, full-k categorical one-hot, `Weekend` 0/1, `BernoulliNB(binarize=None)`.
- Standard LDA: original numeric plus k−1 nominal dummies; standard `solver='svd'`.
- Preserve robust unseen-category treatment, representation checks and common-fold comparison. Logit numerical warnings and pure category levels must be recorded, not hidden; valid finite solver iterates alone do not certify a finite MLE.

## 4. Fixed three EDA-informed revisions

| Candidate | Frozen specification | Motivation and restrictions |
|---|---|---|
| **Revised Logit** | Six activity fields `log1p`; fold-eligible `>0` indicators only where **>=50% fitting-fold zeros**; original other 16-source inputs, k−1 nominal encoding; **fold-fitted StandardScaler**; `LogisticRegression(C=1.0, solver='lbfgs', tol=1e-8, max_iter=3000)` | Long tails, zero mass, correlated predictors and sparse/pure categories; no `C` search. Penalty and feature engineering effects cannot be isolated from baseline difference |
| **Revised LDA** | Six `log1p` activity fields, otherwise same 16 sources and k−1 nominal encoding; `LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')` | Fold-estimated shrinkage may stabilise covariance; correlation itself is permitted and shrinkage may worsen AUC |
| **Revised Mixed NB** | Gaussian block: six log-activity + `BounceRates`/`ExitRates`; categorical block: six nominals, `Weekend`, `SpecialDay>0`; empirical prior **once**; reserve unknown category, Laplace `alpha=1` | Mixed marginal types; conditional independence remains an approximation; smoothing is not L2 |

All learned category maps and covariance estimates are fold-specific. Do not add interactions, more candidates, extra penalties or QDA/KNN. Preserve preexisting fitting/numerical diagnostics.

## 5. Required notebook sequence and exact outputs

| Stage | Required output | Explicit answer/implication |
|---|---|---|
| 0 — Protocol | Research question, prediction-only objective and deterministic training-CV boundaries | What is being predicted and how evaluated |
| 1 — Data quality | Data completeness, duplicate count, class prevalence and split IDs | Why accuracy alone misleads |
| 2 — Numerical EDA | Median, zero share, skewness; selected training-only activity histograms | Whether zero/presence and log compression are plausible |
| 3 — Categorical EDA | Category support and selected observed buyer-rate contrasts | Why rare levels need caution |
| 4 — Assumptions | Selected within-class correlations, Q–Q examples and distribution commentary | Gaussianity, dependence, coefficient stability — without mischaracterising LDA |
| 5 — All17 | Four full-predictor diagnostics | Why `PageValues` is excluded from the operational comparison |
| 6 — Operational16 | Four raw baseline results | Unchanged model-family references |
| 7 — Three revisions | EDA motivation, precise differences and full-recipe limitation | Why these hypotheses were tested |
| 8 — Selection | **One** seven-row mean CV AUC/SD/SE/AP table; **one** seven-curve OOF ROC comparison | Highest mean five-fold AUC winner, small deltas and limits |
| 9 — Winner scores | **One** OOF histogram split by true class | Overlap/ranking vs calibration |
| 10 — Precision–recall | **One** OOF winner PR plot, label axes and AP plus training-prevalence baseline | Minority-class performance; do not confuse AP with precision at any single t |
| 11 — Thresholds | **One** sensitivity–specificity vs threshold plot, crossover marked; **one** 3-row prevalence/0.5/crossover table of **threshold, sensitivity, specificity, precision** | Crossover balances rates and is not necessarily optimal |
| 12 — Numerical/refit | Fitted winner on training with checks; final refit on 12,330 records; small provenance summary | Final fitted recipe is not validation evidence |
| 13 — Conclusion | Actual CV winner, AUC/AP and concise implications, assumptions and boundaries | Direct answer to prediction objective |

**No repeated plots or unnecessary warning/failure tables.** Internal saved audit evidence can be more extensive. Every substantive stage has purpose before result and concise actual interpretation after it. Use British English, label tables/curves and keep graphs legible.

## 6. Exact CV and threshold computation

### Candidate evaluation
- Use identical `FOLD_INDICES` and `run_spec` on four raw 16-source baselines plus three predeclared revisions.
- Fit cloned pipelines within each fold; `predict_proba(...)` yields positive-class OOF probabilities.
- Record per-fold `roc_auc_score` and `average_precision_score`; select **highest mean of five fold ROC-AUCs**, exact ties deterministically alphabetic. Report `SD(ddof=1)`, `SE=SD/sqrt(5)` and mean AP.
- AUC/AP numerical checks recompute from stored OOF predictions; distinguish mean fold AUC from pooled OOF AUC. The 7-model OOF ROC overlay is descriptive and need not exactly equal mean-fold ranking.
- Correctly disclose that higher CV AUC does not establish calibrated `p`, formal significance or external-test performance.

### Precision–recall curve
- For selected winner use `precision_recall_curve(y_train, WINNER_OOF)`, `average_precision_score(y_train, WINNER_OOF)`.
- Mark horizontal no-skill precision = **exact training prevalence** `y_train.mean()`. Label x = recall/sensitivity, y = precision. Mean fold AP used in model table and pooled OOF AP on plot are **different quantities**; label them distinctly.
- Avoid interpreting AP as precision at the crossover or 0.5.

### Three threshold references
- Use **training OOF** scores only. Crossover candidates are all empirical finite thresholds returned by `roc_curve(y_train, WINNER_OOF, drop_intermediate=False)`, limited to valid [0,1] plus fixed endpoints 0 and 1. For each threshold compute `sensitivity=TP/(TP+FN)` and `specificity=TN/(TN+FP)`. Pick the threshold minimising `abs(sensitivity-specificity)`; resolve equal-gap ties by **lower threshold**. The crossover is an empirical nearest-point rule, not a mathematically guaranteed equality.
- References exactly: `y_train.mean()`, `0.5`, `CROSSOVER_THRESHOLD`. A repeated numeric cutoff is allowed if references coincide.
- Compute confusion counts deterministically using `pred = (WINNER_OOF >= t).astype(int)`; precision `TP/(TP+FP)` **may be undefined if no predicted positives**, and must be represented honestly, not silently as zero.
- Show the compact threshold table columns: **reference, threshold, sensitivity, specificity, precision**. For independent verification, save confusion counts to a detailed artifact but avoid redundant main-table columns.
- One plot of sensitivity/specificity across the same computed threshold candidates with three reference markers and a crossover marker; do not plot a 2/3 line.
- Do not vary thresholds using test results, revenue, cost or conversion assumptions. No voucher targeting.

## 7. Numerical audit and acceptance

**For unpenalised Logit**, retain the original same-likelihood IRLS reference gate on fitting folds: mean training negative log likelihood absolute difference <=1e-6 per case and max validation-probability difference <=1e-3, identical design, finite predictions/coefficients, and no suppressed convergence warnings. For L2, do not incorrectly compare to the unpenalised objective; require solver convergence and finite coefficient/prediction checks. Check LDA and NB valid class priors, covariances/variances and predictions.

**Acceptance gates**
- Notebook executes cleanly top to bottom in existing pinned Python environment and GitHub Actions.
- No current active markdown or code references **vouchers, discount, simulated revenue, q, cost-based 2/3, or threshold optimisation by profit**.
- Original 12,330-row source and train/test membership remain unchanged.
- All seven candidate representations and exact common CV folds unchanged; seven fold/OOF vectors complete and valid.
- Winner remains determined by mean fold AUC; actual scores/changes printed, no hardcoded fabricated results.
- Winner OOF **one** ROC overlay, **one** PR curve, **one** OOF histogram, **one** sensitivity/specificity plot and **one** three-reference table.
- Final training refit and exact full-data refit both finish with finite quantities. Neither train nor full-data score is reported as independent generalisation.
- No current independent-test result is invented; any historic test evidence stays labelled for old recipes.
- All purpose/evidence/implication statements are accurate; narrative and generated artifacts align with approved v2.0.
- Independently inspect source, output, table totals and metric computations after CI; record PASS/FAIL honestly.

**Version control and completion:** Changes on a separate `analysis/*` branch with a reviewable pull request; never force-push or merge automatically. Update README/current repo guidance, preserving historic plans/reports for traceability. No claim of submission readiness until clean notebook execution and independent review pass.
