# Project decisions

The latest user clarification retains the existing voucher-revenue framework at `C_FN:C_FP=1:4`. It supersedes the pasted brief's conflicting 5:1 threshold instruction. The active notebook is `online_shoppers_revised.ipynb`; prior executed/revised and original notebooks are preserved in `archive/online-shoppers/`.

## Research and voucher framework

Predict whether a browsing **session** purchases (`Revenue=1`). This is a prediction project, not coefficient inference or a causal study. Predict Buy (`p >= t`) means no voucher; Predict No Buy (`p < t`) means voucher. Recorded labels remain unchanged. Vouchers are a hypothetical downstream intervention, never predictors.

- **A1:** every voucher recipient redeems and purchases with 100% certainty. This is hypothetical and unverified.
- **A2:** each voucher discounts the order by 20%, with no minimum spend.
- **A3:** all orders share representative value `A`; report revenue in units of `A`, without assigning money.
- **A4:** recorded outcomes represent purchasing behaviour without the proposed intervention.

Compare exactly two scenarios: no vouchers and the selected model-guided voucher strategy. Evaluate sales revenue, not profitability. Do not invent AOV, margins, acquisition costs or voucher-effect estimates.

No-voucher revenue is `R0/A=TP+FN`; model-guided revenue is `Rmodel/A=TP+0.80(FN+TN)`. The difference is `delta/A=0.80TN-0.20FN`, and relative change is `(0.80TN-0.20FN)/(TP+FN)`. The theoretical cutoff is 0.80 when predicted probability equals true no-voucher purchase probability. The associated conditional opportunity costs are `C_FN=0.20A`, `C_FP=0.80A`, ratio `1:4`.

Select the classifier by highest mean training-fold ROC-AUC with deterministic label tie-breaking, then optimize only that classifier's threshold using training OOF simulated revenue. Report PR-AUC and fold variation alongside ROC-AUC. Keep predictive model choice separate from the voucher-policy objective.

## Statistical decisions retained

- UCI 468 session-level target; historical 75/25 stratified split, seed 42; five stratified training folds.
- First pass: Logistic Regression, Gaussian Naive Bayes and LDA with all 17 original predictors. Preserve actual warnings and failures.
- Treat numeric-coded nominal predictors as unranked. Fit imputation, encoding, scaling and transforms within each fold.
- Compare `PageValues` in first pass, then exclude it from operational 16-predictor candidates because availability at decision time is uncertain.
- Compare raw, `log1p` and `zeroind` treatments for all three classifiers. `zeroind` adds fold-fitted indicators for predictors with at least 50% training-fold zeros after log1p; it does not binarize predictors.
- Retain logistic numerical interactions, five-original-predictor logistic model, L2 `C=0.1` and `C=10`, GaussianNB variance smoothing and LDA shrinkage.
- Retain existing raw mixed Gaussian/Categorical Naive Bayes and raw numeric-only LDA alternatives. One-hot GaussianNB/LDA comparisons are approximate diagnostics; eligible candidates are Logistic variants plus those two existing raw alternatives.
- Preserve the threshold analysis and historical CV-versus-test comparison. Do not add unrelated classifiers or experiments.

## Limitations

Voucher response is absent, so A1 cannot be verified. Simulated gains are not actual sales growth. Costs beyond the stated discount, margins and expenses are excluded. Session totals, durations, exit/bounce information and `PageValues` require prediction-time availability checks. Customer IDs are absent, so repeated people cannot be reliably identified or group-split. The historical test has already been inspected; candidate/threshold selection also introduces optimism.
