# Final revision scope and verification

## Provenance and preserved work

The prior executed analysis is retained as a read-only historical record. Its exact source files remain in `archive/online-shoppers/`. The current active entry point is `online_shoppers_revised.ipynb`; the source dataset remains unchanged. The current revision follows the latest user brief and clarification, including the removal of QDA, Yeo–Johnson and quantile-transform work and retention of the 1:4 voucher-revenue threshold framework.

## Included analysis

- Session-level UCI 468 purchase prediction with Logistic Regression, Gaussian Naive Bayes and LDA.
- Historical 75/25 stratified split, seed 42; five stratified training folds.
- Data quality and training-only numerical/categorical EDA.
- All-17-predictor first passes, actual warnings/failures, `PageValues` timing review and operational exclusion.
- Raw, `log1p` and fold-fitted `zeroind` comparisons for each classifier.
- Retained logistic L2 settings, numerical interactions, predeclared five-predictor logistic model, GaussianNB smoothing and LDA shrinkage.
- Existing raw mixed Gaussian/Categorical NB and numeric-only LDA eligible alternatives.
- ROC-AUC and PR-AUC (average precision), fold means/sample SDs, per-fold selected-model scores, ROC/PR curves, pooled OOF and historical test results.
- Classifier selection by mean training-CV ROC-AUC, followed by training OOF threshold optimization under the latest-confirmed 1:4 revenue framework.
- Threshold and CV-versus-historical-test comparisons; exactly two revenue scenarios, with unchanged observed labels.

## Verification status

All active notebook outputs now come from the full current execution; earlier cached results were cleared before the run. Full execution completed successfully: all 21 code cells ran in order, all 20 candidate designs completed and 9 candidates were eligible; no cell or candidate failed. Expected rare unseen-category one-hot warnings were recorded. Tables and eight figures were inspected manually, and an HTML review copy was rendered. No automated code-checking tests were added; the existing GitHub notebook-execution workflow remains unchanged.

Dataset SHA-256: `b3055ee355f59134d851d32641183cb4a8b45def7124d2f50442a042f358e0d9`.
Historical active notebook SHA-256: `e860944111af5684ceeccd88e54a45b72fa2354f4719aecc5cebc2445a452f92`.
Historical original notebook SHA-256: `debec6b36b796a2bc41d92d6abe57a645281d1d027a5d56f99cde32880636e17`.

The current winner is Logistic Regression `zeroind`, threshold 0.800000: mean fold AUC 0.761161 (SD 0.022013), pooled OOF AUC 0.760887, historical test AUC 0.742293. Mean fold AP is 0.340692 (SD 0.034901), pooled OOF AP 0.335089 and historical test AP 0.328956. Training confusion counts are TP=0, FP=0, FN=1,431, TN=7,816; historical test counts are TP=0, FP=0, FN=477, TN=2,606. At this cutoff all sessions receive vouchers. The run summary, baselines and simulated-revenue calculations are in `revision_summary.md`.

## Remaining methodological limitations

Voucher effectiveness cannot be verified without intervention outcomes. Revenue simulation is conditional on A1–A4, excludes profitability, and is not a sales-growth forecast. Predictor availability at decision time remains unresolved. Session identities do not identify unique customers. Selecting candidates and threshold on the same OOF predictions induces selection optimism. The previously inspected historical holdout is not independent confirmation.
