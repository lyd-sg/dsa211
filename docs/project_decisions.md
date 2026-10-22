# Project decisions

The current authority is the group's **Final Project Revision and GitHub Implementation** brief supplied for this revision. It replaces earlier business assumptions while retaining the professor's core classification workflow. The archived two-page brief remains historical evidence; its previous intervention narrative and additional experiments are superseded.

## Research and voucher framework

Predict whether a browsing **session** purchases (`Revenue=1`). This is a prediction project, not coefficient inference or a causal study. Predict Buy (`p >= t`) means no voucher; Predict No Buy (`p < t`) means voucher. Recorded labels remain unchanged. Vouchers are a hypothetical downstream intervention, never predictors.

- **A1:** every voucher recipient redeems and purchases with 100% certainty. This is hypothetical and unverified.
- **A2:** each voucher discounts the order by 20%, with no minimum spend.
- **A3:** all orders share representative value `A`; report revenue in units of `A`, without assigning money.
- **A4:** recorded outcomes represent purchasing behaviour without the proposed intervention.

Compare exactly two scenarios: no vouchers and the selected model-guided voucher strategy. Evaluate sales revenue, not profitability. Do not invent AOV, margins, acquisition costs or voucher-effect estimates.

## Opportunity costs and revenue

A false positive receives no voucher and misses an assumed discounted conversion: `C_FP=0.80A`. A false negative receives an unnecessary discount on an otherwise full-price order: `C_FN=0.20A`. Thus `C_FN:C_FP=1:4`. These are conditional opportunity costs, not measured financial losses.

The no-voucher baseline is `R0/A=TP+FN`. Model-guided revenue is `Rmodel/A=TP+0.80(FN+TN)`. The difference is `delta/A=0.80TN-0.20FN`, with relative change `(0.80TN-0.20FN)/(TP+FN)`. Revenue is higher exactly when `4TN>FN`.

For calibrated purchase probability `p`, full-price expected revenue is `pA`, versus `0.80A` with a voucher under A1. The theoretical threshold is therefore `0.80`. Choose the empirical threshold and model using training out-of-fold simulated revenue. ROC-AUC describes discrimination; it does not replace this selection objective.

## Statistical decisions retained

- UCI 468; historical 75/25 stratified split, seed 42; five stratified training folds.
- Attempt all 17 predictors with logistic regression, Gaussian Naive Bayes, LDA and QDA first. Record actual numerical warnings and failures before repairs.
- Treat numeric-coded nominal predictors as unranked. Fit imputation, encoding, scaling and transformations inside CV pipelines.
- Investigate `PageValues` in first-pass fits, then exclude it operationally because its availability before voucher allocation is uncertain. AUC differences alone do not prove leakage.
- Retain the bounded Phase 2 transformation, interaction, subset and tuning comparisons. Exclude unrelated classifiers and extensive resampling experiments.
- Select specification and threshold before historical test evaluation; never use that partition for tuning.
- Retain both extensions: threshold analysis and CV-versus-historical-test comparison.

## Unresolved practical limitations

Voucher response is absent, so A1 cannot be verified. Large simulated gains cannot be forecast as actual sales growth. Costs, margins and expenses are omitted. Session totals, durations, exit/bounce information and `PageValues` require prediction-time availability checks. Customer IDs are absent, so repeated people cannot be reliably identified or group-split. The historical test has already been inspected; candidate and threshold selection on the same training CV predictions introduces selection optimism.

The original notebook, dataset and archives remain unchanged historical records; their retained results and assumptions are not current findings.
