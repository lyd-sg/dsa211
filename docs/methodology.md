# Revised classification and voucher-revenue methodology

## Data and validation protocol

Run `online_shoppers_revised.ipynb` from the repository root using committed `data/uci_468.csv`. The unit is a browsing session and `Revenue=1` is an observed purchase without the proposed intervention. Vouchers are downstream hypothetical actions, never predictors or replacement labels.

Check schema, types, missingness, duplicates and class balance. Do not remove identical rows on the assumption they identify duplicate customers. Preserve the historical 75/25 stratified split, seed 42: 9,247 training and 3,083 historical test sessions. Outcome-related numerical and categorical EDA uses training data only; explain how skewness, zeros, sparse categories and dependence motivate candidate improvements.

## First pass and bounded improvements

Attempt logistic regression, Gaussian Naive Bayes, LDA and QDA with all 17 original predictors. Technical encoding and fold-fitted imputation/scaling permit numeric-input fitting; do not drop predictors, binarise zeros or silently repair QDA before this pass. Retain warnings and failures in the ledger.

Compare inclusion/exclusion of `PageValues` on identical training folds. The AUC difference is diagnostic, not proof of leakage. Its possible transaction-derived definition and uncertain availability at allocation justify exclusion from operational 16-predictor candidates. Whole-session totals and rates also need prospective availability checks.

Reuse the bounded Phase 2 candidates: raw inputs; log, Yeo–Johnson and quantile transformations; fold-fitted zero indicators; numeric interactions; a predeclared five-predictor subset; and model-specific regularisation or smoothing. Assumption diagnostics inform plausibility rather than guarantee predictive gains. Fit all preprocessing inside pipelines. Do not introduce unrelated classifiers or extensive bootstrap searches.

## Training CV and joint selection

Use five stratified training folds, shuffled with seed 42. Every training session receives a probability from a model fitted without its fold. Report mean fold AUC, pooled out-of-fold AUC, sensitivity, specificity, confusion matrices, ROC curves and calibration information. Mean fold AUC and pooled AUC are different summaries.

For each eligible operational candidate, choose the threshold maximising training out-of-fold simulated revenue. Select model and threshold jointly by revenue, using a declared deterministic tie rule and AUC as a secondary discrimination measure. Do not first select on AUC and then claim to maximise revenue across models.

Evaluate attainable classifications at observed probability cutpoints, including endpoint assignments. Keep the no-voucher revenue baseline fixed for each sample. Threshold changes affect voucher allocation, not observed labels. Do not constrain an extreme optimum to create a preferred story or add a third business-policy comparison.

Although each fold's preprocessing and fitting exclude its validation rows, candidate and threshold selection reuse the out-of-fold results. Selected training estimates have selection optimism and are not a separate unbiased post-selection evaluation. The already-viewed test set does not provide a fresh confirmatory audit.

## Extension 1: threshold and revenue

Apply A1–A4 in [project decisions](project_decisions.md). With positive class `Revenue=1`:

| Outcome | Action and simulated outcome | Revenue |
|---|---|---|
| TP | No voucher; baseline buyer purchases | `A` |
| FP | No voucher; baseline non-buyer does not purchase | `0` |
| FN | Voucher; baseline buyer receives an unnecessary discount | `0.80A` |
| TN | Voucher; baseline non-buyer converts under A1 | `0.80A` |

Missing an assumed discounted conversion costs `0.80A` per FP; unnecessarily discounting a baseline purchase costs `0.20A` per FN. Hence `C_FN:C_FP=1:4`. Comparing full-price expected revenue `pA` with voucher revenue `0.80A` gives theoretical threshold `0.80` for calibrated probabilities.

Compare the training-selected threshold with `0.80` and `0.5`. Plot sensitivity/specificity and revenue/opportunity cost across thresholds. Discuss calibration and finite-sample variation without treating a calibration diagnostic as proof of the cause. These are operating points of the same model-guided scenario, not extra business-policy scenarios.

## Extension 2: historical test and two scenarios

Freeze the winning specification and threshold, fit on the entire training partition, then evaluate on the historical test once. Report CV-versus-test AUC, sensitivity, specificity and confusion matrices. Do not revise the strategy after viewing test results.

Compare exactly:

1. No vouchers: `R0/A=TP+FN`.
2. Selected model-guided vouchers: `Rmodel/A=TP+0.80(FN+TN)`.

Then `delta/A=0.80TN-0.20FN` and relative change is `(0.80TN-0.20FN)/(TP+FN)`. The common order value cancels. Positive, zero and negative changes mean higher, equal and lower simulated sales revenue. Show counts and arithmetic; the conclusion concerns direction under the assumptions, not an actual sales-growth forecast.

## Interpretation and limitations

Every major section states its objective, methodology and implementation, followed by computed results, interpretation and implication. Retain executed tables and plots. Numerical interpretations must derive from the current run.

Disclose unverified conversion, absent intervention outcomes, no causal revenue effects, revenue rather than profit, predictor timing, unavailable customer identity, candidate/threshold selection optimism and historical test reuse. New independent sessions and intervention evidence are needed for stronger claims.
