# Final revision scope and verification

## Provenance and preserved work

The revision incorporates the complete existing `analysis/phase-2-core-notebook` history through `ab31c233850d0b6692eac275cc120a8194b2abeb`, rather than replacing or discarding that branch. The original notebook, source CSV and historical archives remain unchanged.

The group's final revision brief replaces the prior business assumptions. It preserves the professor's core classification work and two extensions, while excluding unrelated experiments. The archived PDF is a historical project source; its earlier intervention narrative, costs, optional experiments and unviewed-test claims are superseded by the explicit current brief.

## Included analysis

- Session-level UCI 468 purchase prediction; four families: logistic regression, Gaussian Naive Bayes, LDA and QDA.
- Historical 75/25 stratified split, seed 42; five stratified training folds.
- Data quality and training-only numerical/categorical EDA with modelling implications.
- All-17-predictor first passes, recorded warnings/failures, `PageValues` review and operational exclusion.
- Bounded Phase 2 transformations, zero indicators, interactions, subset and model-specific tuning; fold-fitted preprocessing.
- Joint model/threshold selection maximising training OOF simulated revenue; AUC reported separately.
- **Extension 1:** empirical training threshold, theoretical 0.80 reference, sensitivity/specificity, revenue/opportunity-cost plots and calibration context.
- **Extension 2:** fixed-strategy CV versus historical test comparison.
- Exactly two revenue scenarios: no voucher and selected model-guided vouchers; unchanged observed labels; all four confusion outcomes explained.
- Executed outputs and computed interpretations in the revised notebook.

## Current business specification

A1 guaranteed voucher conversion; A2 20% discount without minimum spend; A3 common order value `A`; A4 observed labels represent no-intervention behaviour. Predict Buy means no voucher; Predict No Buy means voucher. `C_FN:C_FP=1:4` follows from `0.20A` versus `0.80A` opportunity costs.

Report `R0/A=TP+FN`, `Rmodel/A=TP+0.80(FN+TN)`, and relative change `(0.80TN−0.20FN)/(TP+FN)`. No invented monetary parameters, profit claims, universal-voucher policy comparison or causal effect estimates are introduced.

## Verification protocol

Execute the entire revised notebook using actual committed data, inspect its output, render an HTML copy for review, and inspect formulas, confusion interpretation, threshold selection and all narrative claims manually. No automated code-checking test suite is added. The existing GitHub workflow remains an end-to-end notebook execution workflow with output artifacts.

Dataset SHA-256: `b3055ee355f59134d851d32641183cb4a8b45def7124d2f50442a042f358e0d9`.
Original notebook SHA-256: `debec6b36b796a2bc41d92d6abe57a645281d1d027a5d56f99cde32880636e17`.

The actual-data execution completed all 20 code cells without a cell error. Of 29 candidate designs, 27 completed; the two default-QDA covariance failures are intentional recorded analysis outcomes, not unhandled notebook errors. Separately labelled regularised QDA designs completed. Tables, all eight generated figures and the HTML export were inspected manually; no automated code-checking tests were added.

The selected candidate is quantile-transformed logistic regression, threshold `0.8359523283877723`: mean fold AUC `0.7614554422`, pooled OOF AUC `0.7610129055`, historical test AUC `0.7408914439`. Training confusion counts are TP=1, FP=0, FN=1,430, TN=7,816. Test counts are TP=0, FP=0, FN=477, TN=2,606. The training-optimal rule sends vouchers to every historical test session, so its simulated test revenue `2,466.4A` exceeds the no-voucher `477A` by `1,989.4A` (`417.06%`) under guaranteed conversion. This is an assumption-driven simulation, not a growth forecast or evidence of meaningful test-set targeting.

Python 3.12.14, NumPy 2.5.4, pandas 3.0.6 and scikit-learn 1.9.1 were used locally; runtime metadata is also printed in the notebook. Thread counts were capped at one for BLAS/OpenMP. The existing requirements file remains unchanged and specifies minimum versions rather than a frozen environment.

[GitHub Actions](https://github.com/lyd-sg/dsa211/actions/workflows/validate-notebook.yml) reruns the real-data notebook on `main` pushes and retains the executed artifact. The workflow definition by itself is not evidence of a successful remote run; inspect the run for the delivered commit.

## Remaining methodological limitations

Voucher effectiveness cannot be verified without intervention outcomes. Revenue simulation is conditional on A1–A4, excludes profitability, and is not a sales-growth forecast. Predictor availability at decision time remains unresolved. Session identities do not identify unique customers. Selecting among candidates and thresholds on the same OOF predictions induces selection optimism. The previously inspected historical holdout cannot become a new independent evaluation by rerunning the notebook.
