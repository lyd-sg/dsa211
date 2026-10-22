# DSA211 repository instructions

## Current project

The active entry point is `online_shoppers_revised.ipynb`. Read `README.md`, `docs/project_decisions.md`, `docs/methodology.md` and `docs/phase2_scope.md` before changing the analysis. The current authorised phase includes statistical revision and execution; the old Phase 1 housekeeping-only restriction is superseded.

Predict session-level `Revenue` and compare exactly two simulated revenue scenarios: no vouchers and model-guided vouchers. Predict Buy means no voucher; Predict No Buy means voucher. Keep observed labels unchanged. Vouchers are hypothetical actions after classification, not predictors.

## Required framework

- A1 guaranteed conversion; A2 20% discount without minimum spend; A3 common order value `A`; A4 observed outcomes represent no-voucher behaviour.
- Revenue opportunity costs are `C_FN=0.20A`, `C_FP=0.80A`, ratio `1:4`. Do not restore superseded business assumptions or invent monetary inputs.
- The calibrated theoretical threshold is `0.80`. Select the empirical threshold and model using training OOF simulated revenue; AUC measures discrimination separately.
- Preserve 75/25 stratified split, seed 42; five stratified training folds. Fit preprocessing inside folds.
- First attempt all 17 predictors with logistic regression, Gaussian Naive Bayes, LDA and QDA. Document genuine warnings/failures before changes.
- Treat nominal numeric-coded categories as unranked. Investigate `PageValues`, then exclude it from operational models on availability grounds.
- Keep improvements bounded and relevant; preserve threshold analysis and CV-versus-historical-test comparison. Do not add unrelated classifiers or extensive bootstrap experiments.
- Freeze specification and threshold before historical test evaluation. Disclose candidate/threshold selection optimism and the previously viewed test partition.
- Do not claim actual voucher effects, profitability, unique customers or reliable sales-growth forecasts. Record predictor-timing limitations.

## File and review discipline

Preserve `online_shoppers_full_project.ipynb`, `data/uci_468.csv` and historical archives unchanged. Keep the original notebook at root so its relative path continues to resolve. Preserve valid Phase 2 history and document splits, seeds, CV, preprocessing and actual execution. Use a branch for changes before authorised delivery.

Ground interpretations in freshly computed results and keep notebook outputs, plots and documentation consistent. The current revision uses manual code/deliverable review plus full notebook execution; do not add automated code-checking tests for this task. Preserve the existing end-to-end GitHub notebook execution workflow.
