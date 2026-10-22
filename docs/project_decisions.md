# Project decisions

The current authorities are the group's **Final Project Revision and GitHub Implementation** brief and the subsequent **Consolidated Requirements and Agreed Decisions** supplied for the follow-up audit. They replace earlier business assumptions while retaining the professor's core classification workflow. The archived two-page brief remains historical evidence; its previous intervention narrative and additional experiments are superseded.

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

If `p` represents the true no-voucher purchase probability, full-price expected revenue is `pA`, versus `0.80A` with a voucher under A1. The theoretical threshold is therefore `0.80`. The user's subsequent audit clarification selects the classifier by highest mean training CV ROC-AUC, then optimises only that classifier's threshold using training OOF simulated revenue. This explicitly supersedes the earlier joint revenue-based model-selection instruction. Report PR-AUC and fold variation alongside ROC-AUC; keep predictive model choice separate from the business extension.

## Statistical decisions retained

- UCI 468; historical 75/25 stratified split, seed 42; five stratified training folds.
- Attempt all 17 predictors with logistic regression, Gaussian Naive Bayes, LDA and QDA first. Record actual numerical warnings and failures before repairs.
- Treat numeric-coded nominal predictors as unranked. Fit imputation, encoding, scaling and transformations inside CV pipelines.
- Investigate `PageValues` in first-pass fits, then exclude it operationally because its availability before voucher allocation is uncertain. AUC differences alone do not prove leakage.
- Retain the bounded Phase 2 transformation, interaction, subset and tuning comparisons. Exclude unrelated classifiers and extensive resampling experiments.
- Resolve the Gaussian/dummy mismatch with mixed Gaussian/Categorical NB and numerical-only LDA/QDA alternatives. Preserve the old dummy-coded experiments as diagnostics; exclude them from final operational selection. Compare all four families without preselecting a winner.
- Report ROC-AUC and PR-AUC (average precision), including fold-to-fold SD and selected per-fold scores, as well as pooled OOF and historical test results.
- Select specification and threshold before historical test evaluation; never use that partition for tuning.
- Retain both extensions: threshold analysis and CV-versus-historical-test comparison.

## Unresolved practical limitations

Voucher response is absent, so A1 cannot be verified. Large simulated gains cannot be forecast as actual sales growth. Costs, margins and expenses are omitted. Session totals, durations, exit/bounce information and `PageValues` require prediction-time availability checks. Customer IDs are absent, so repeated people cannot be reliably identified or group-split. The historical test has already been inspected; candidate and threshold selection on the same training CV predictions introduces selection optimism.

The original notebook, dataset and archives remain unchanged historical records; their retained results and assumptions are not current findings.
