# Revised classification and voucher-revenue methodology

## Data and validation protocol

Run `online_shoppers_revised.ipynb` from the repository root using committed `data/uci_468.csv`. The unit is a browsing session and `Revenue=1` is an observed purchase without the proposed intervention. Vouchers are downstream hypothetical actions, never predictors or replacement labels.

Check schema, types, missingness, duplicates and class balance. Do not remove identical rows on the assumption they identify duplicate customers. Preserve the historical 75/25 stratified split, seed 42: 9,247 training and 3,083 historical test sessions. Outcome-related numerical and categorical EDA uses training data only; explain how skewness, zeros, sparse categories and dependence motivate candidate improvements.

## First pass and bounded improvements

Attempt logistic regression, Gaussian Naive Bayes, LDA and QDA with all 17 original predictors. Technical encoding and fold-fitted imputation/scaling permit numeric-input fitting; do not drop predictors, binarise zeros or silently repair QDA before this pass. Retain warnings and failures in the ledger.

Compare inclusion/exclusion of `PageValues` on identical training folds. The AUC difference is diagnostic, not proof of leakage. Its possible transaction-derived definition and uncertain availability at allocation justify exclusion from operational 16-predictor candidates. Whole-session totals and rates also need prospective availability checks.

Reuse the bounded Phase 2 candidates: raw inputs; log, Yeo–Johnson and quantile transformations; fold-fitted zero indicators; numeric interactions; a predeclared five-predictor subset; and model-specific regularisation or smoothing. Assumption diagnostics inform plausibility rather than guarantee predictive gains. Fit all preprocessing inside pipelines. Do not introduce unrelated classifiers or extensive bootstrap searches.

The expanded comparison means multiple specifications within the same model families, beyond the professor's minimum of fitting one version of each required classifier:

| Group | Number of configurations | Purpose |
|---|---:|---|
| All-predictor/operational baselines and initial QDA repair | 9 | Record the first pass and the effect of excluding `PageValues` |
| Transformations | 12 | Compare log, Yeo–Johnson, quantile and log-plus-zero-indicator inputs across logistic, Gaussian NB and LDA |
| Interaction/subset alternatives | 3 | Test numeric predictor interactions and one predeclared five-predictor logistic model |
| Parameter settings | 5 | Compare logistic regularisation, NB smoothing, LDA shrinkage and QDA covariance regularisation |
| Mixed/numerical-only specifications | 6 | Address the Gaussian/dummy mismatch for NB, LDA and QDA |

These sum to 35 configurations, including baselines and failed fits. The first 29 designs came from the existing Phase 2 workflow; the six mixed/numerical-only alternatives address the subsequent consolidated requirements. Transformation, interaction, subset and tuning searches are optional refinements beyond the professor's minimum list, not separate project objectives.

## Mixed-predictor resolution

One-hot encoding makes nominal features usable by numeric-input estimators, but it does not make their binary values Gaussian. Transforming numerical columns does not repair that distributional mismatch. Preserve the legacy Gaussian NB, LDA and QDA dummy-coded experiments as approximate diagnostic comparisons, including their failures. Exclude those challenged specifications from the final operational selection registry.

Add six bounded alternatives required by the consolidated checklist: mixed Gaussian/Categorical Naive Bayes with raw and Yeo–Johnson numerical inputs; numerical-only LDA with raw and Yeo–Johnson inputs; and numerical-only QDA with default and regularised covariance. Together with the original 29 designs, this gives 35 recorded attempts.

The mixed NB alternatives use Gaussian likelihoods for the eight operational numerical variables and smoothed categorical likelihoods for each of the eight nominal variables. Category encodings identify levels rather than order them; validation-only levels receive an explicit unknown code. Fit every encoder, imputer, transform and likelihood using that fold's training rows. Combine the conditional likelihoods with a single class prior. Conditional independence and approximate numerical normality remain assumptions, not established facts.

The numerical-only LDA/QDA alternatives deliberately omit all eight categorical predictors, after satisfying the mandated all-17 first pass. This avoids claiming that binary dummy columns follow a multivariate Gaussian distribution, at the price of discarding potentially useful category information. Their numerical class distributions can still depart from normality. Compare their actual CV results rather than assuming this workaround improves prediction. Logistic variants remain eligible with one-hot predictors because logistic regression does not require Gaussian predictor distributions.

## Training CV and sequential selection

Use five stratified training folds, shuffled with seed 42. Every training session receives a probability from a model fitted without its fold. Report ROC-AUC and PR-AUC (defined as average precision), mean and sample SD across folds, pooled OOF metrics, sensitivity, specificity, confusion matrices, ROC/PR curves. Average precision is the recall-step-weighted precision summary, not trapezoidal PR integration. Mean fold scores and pooled OOF scores are different summaries; SD is fold-to-fold spread, not a confidence interval. The PR no-skill reference is training purchase prevalence.

The user's audit clarification settles the previously unresolved selection criterion: select the classifier with the highest mean training CV ROC-AUC among defensible eligible specifications, then fix that classifier and optimise only its threshold for training OOF simulated revenue. Break exact AUC ties deterministically by candidate label. Report PR-AUC and the best-AP candidate as additional predictive evidence, not an unstated replacement selection rule. Do not claim this sequential procedure maximises revenue across classifiers.

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

Missing an assumed discounted conversion costs `0.80A` per FP; unnecessarily discounting a baseline purchase costs `0.20A` per FN. Hence `C_FN:C_FP=1:4`. Comparing full-price expected revenue `pA` with voucher revenue `0.80A` gives theoretical threshold `0.80` when `p` equals the true no-voucher purchase probability.

Compare the training-selected threshold with `0.80` and `0.5`. Plot sensitivity/specificity and revenue/opportunity cost across thresholds. Explain the distinction between the theoretical true-probability rule and the empirical training OOF optimum; finite-sample variation can affect the empirical cutoff. These are operating points of the same model-guided scenario, not extra business-policy scenarios.

## Extension 2: historical test and two scenarios

Freeze the winning specification and threshold, fit on the entire training partition, then evaluate on the historical test once. Report CV-versus-test AUC, sensitivity, specificity and confusion matrices. Do not revise the strategy after viewing test results.

Compare exactly:

1. No vouchers: `R0/A=TP+FN`.
2. Selected model-guided vouchers: `Rmodel/A=TP+0.80(FN+TN)`.

Then `delta/A=0.80TN-0.20FN` and relative change is `(0.80TN-0.20FN)/(TP+FN)`. The common order value cancels. Positive, zero and negative changes mean higher, equal and lower simulated sales revenue. Show counts and arithmetic; the conclusion concerns direction under the assumptions, not an actual sales-growth forecast.

## Interpretation and limitations

Every major section states its objective, methodology and implementation, followed by computed results, interpretation and implication. Retain executed tables and plots. Numerical interpretations must derive from the current run.

Disclose unverified conversion, absent intervention outcomes, no causal revenue effects, revenue rather than profit, predictor timing, unavailable customer identity, one-retailer historical data, candidate/threshold selection optimism and historical test reuse. Marginal binned-logit plots are descriptive and do not establish conditional log-odds linearity after adjusting for other predictors. New independent sessions and intervention evidence are needed for stronger claims.
