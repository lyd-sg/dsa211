# Revised classification and voucher-revenue methodology

## Data and validation protocol

Run `online_shoppers_revised.ipynb` from the repository root using committed `data/uci_468.csv`. The unit is a browsing session and `Revenue=1` is an observed purchase without the proposed intervention. Vouchers are downstream hypothetical actions, never predictors or replacement labels.

Check schema, types, missingness, duplicates and class balance. Do not remove identical rows on the assumption they identify duplicate customers. Preserve the historical 75/25 stratified split, seed 42: 9,247 training and 3,083 historical test sessions. Outcome-related numerical and categorical EDA uses training data only.

## Classifiers and candidate scope

The first pass fits Logistic Regression, Gaussian Naive Bayes and LDA with all 17 predictors. Preserve actual warnings and failures. Compare `PageValues` during the diagnostic stage, then exclude it from operational models because its availability at voucher-allocation time is uncertain. This is an availability decision, not a conclusion from AUC alone.

The 20 attempted designs comprise three all-17 first-pass models, three operational raw baselines, two existing raw mixed/numeric-only alternatives, six log1p/zeroind comparisons (two transforms across all three classifiers), two retained logistic interaction/subset variants, and four retained model-specific variants. The original numeric scope excludes the prohibited Yeo–Johnson and quantile experiments. `zeroind` applies `log1p` plus indicators for numerical predictors whose training-fold zero share is at least 50%; it does not binarize predictors. All preprocessing is fitted inside each CV fold.

Retain logistic L2 regularization at `C=0.1` and `C=10`, logistic numerical interactions, the five-original-predictor logistic model, GaussianNB variance smoothing and LDA covariance shrinkage. Retain the existing raw mixed Gaussian/Categorical NB and raw numeric-only LDA alternatives. The one-hot GaussianNB and LDA variants are reported as approximate diagnostics; only Logistic variants and the existing raw mixed NB/numeric-only LDA alternatives enter final eligibility. The Naive Bayes and LDA coverage trade-offs remain explicit.

## Selection and reporting

Select the eligible classifier by highest mean training-fold ROC-AUC, with deterministic candidate-label tie-breaking. Then select only its threshold from training OOF simulated revenue under the retained 1:4 opportunity-cost framework. Report average precision as a complementary metric, fold means and sample SDs, selected fold scores, OOF/test metrics, sensitivity/specificity, confusion matrices and ROC/PR plots. Freeze the model and threshold before historical test evaluation.

The theoretical voucher-revenue cutoff is 0.80 only when a score equals the true no-voucher purchase probability. It is a reference rather than a forced empirical threshold. Do not use test labels to select candidates, transforms or thresholds.

## Interpretation and limitations

In the current execution, Logistic `zeroind` had the highest mean fold AUC (0.761161 ± 0.022013); pooled OOF AUC was 0.760887 and historical test AUC was 0.742293. Mean fold AP was 0.340692 ± 0.034901; pooled OOF AP was 0.335089 and test AP was 0.328956. `log1p` and `zeroind` increased CV AUC relative to raw for each family; these small differences are descriptive and are not significance tests. Logistic interactions and GaussianNB smoothing increased AUC relative to their raw references; five-predictor reduction, Logistic L2 changes and LDA shrinkage did not. See `revision_summary.md` for exact values and the baseline tables. Distinguish predictive discrimination from the voucher simulation. A1–A4 are assumptions; voucher response is unobserved, revenue is not profit, and simulated gains are not actual sales-growth forecasts. Predictor timing, repeated sessions without customer IDs, selection optimism, one-retailer data and prior historical-test viewing remain limitations.
