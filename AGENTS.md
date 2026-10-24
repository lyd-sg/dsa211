# DSA211 repository instructions

## Current project

The active entry point is `online_shoppers_revised.ipynb`. Read `README.md`, `docs/project_decisions.md`, `docs/methodology.md` and `docs/phase2_scope.md` before changing the analysis. The current authorized revision removes QDA and the Yeo–Johnson/quantile-transform experiments. The prior executed revised notebook and original full-project notebook are retained byte-for-byte under `archive/online-shoppers/`.

Predict session-level `Revenue` and compare exactly two simulated revenue scenarios: no vouchers and model-guided vouchers. Predict Buy means no voucher; Predict No Buy means voucher. Keep observed labels unchanged. Vouchers are hypothetical actions after classification, not predictors.

## Required framework

- A1 guaranteed conversion; A2 20% discount without minimum spend; A3 common order value `A`; A4 observed outcomes represent no-voucher behaviour.
- The latest user clarification retains revenue opportunity costs `C_FN=0.20A`, `C_FP=0.80A`, ratio `1:4`; the theoretical voucher threshold is `0.80` for calibrated true no-voucher probabilities. Select the classifier by highest mean training CV ROC-AUC, then optimize only its threshold using training OOF simulated revenue. Report PR-AUC and fold variation alongside ROC-AUC.
- Preserve the 75/25 stratified split, seed 42, and five stratified training folds. Fit preprocessing inside folds.
- The first pass uses all 17 predictors with Logistic Regression, Gaussian Naive Bayes and LDA. Document genuine warnings/failures.
- Treat nominal numeric-coded categories as unranked. Investigate `PageValues`, then exclude it from operational models on availability grounds.
- Compare raw, `log1p` and fold-fitted `zeroind` treatments for all three classifiers. Preserve logistic L2 `C=0.1` and `C=10`, logistic numerical interactions, the predeclared five-predictor logistic model, GaussianNB variance smoothing and LDA shrinkage. Retain existing raw mixed Gaussian/Categorical NB and numeric-only LDA alternatives.
- Report ROC-AUC and PR-AUC (average precision), fold means and sample SDs, selected per-fold results, ROC/PR curves and historical test metrics. Keep threshold analysis and historical-test caveats.
- Freeze specification and threshold before historical test evaluation. Disclose candidate/threshold selection optimism and the previously viewed test partition.
- Do not claim actual voucher effects, profitability, unique customers or reliable sales-growth forecasts. Record predictor-timing limitations.

## File and review discipline

Preserve `data/uci_468.csv` and historical archives unchanged. Keep only the active revised notebook at the repository root; prior notebooks are archived as directed. Preserve valid project history and document splits, seeds, CV, preprocessing and actual execution. Use a branch for changes before delivery.

Ground interpretations in freshly computed results and keep notebook outputs, plots and documentation consistent. Use manual review plus full notebook execution; do not add automated code-checking tests for this task. Preserve the existing end-to-end GitHub notebook execution workflow.
