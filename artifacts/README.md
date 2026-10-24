# Audit artifacts

These files support the approved training-only baseline stage; they are not additional model searches. Row IDs are zero-based positions in the unchanged committed CSV, not customer identifiers.

- `train_row_ids.csv`, `test_row_ids.csv`: seed-42 stratified 80/20 membership in original-row order. Test IDs are recorded only; no test features/outcomes are analyzed.
- `cv_fold_row_ids.csv`: five shuffled stratified folds (seed 42) on sorted training IDs, with fit/validation roles.
- `baseline_summary.csv`, `baseline_fold_metrics_diagnostics.csv`, `baseline_warnings.csv`, and the eight `*_oof.csv` files: canonical current baseline evidence. The two Logit candidates use the updated cold-start `newton-cg` tolerance `1e-8`; the other six candidate vectors come from the earlier completed notebook run and their recipes are unchanged.
- `logit_tol1e8_numerical_gate.csv`/`.json`: exact current-source comparison of all ten Logit folds with same-likelihood Binomial IRLS. Accepted only when fits/probabilities are finite, IRLS converges, absolute mean training-NLL delta is at most `1e-6`, and maximum validation probability difference is at most `1e-3`.
- `*_Logit_folds_tol1e8.csv`: fold-level current-source Logit diagnostics, including unseen category levels, pure nominal levels, and reference checks. `baseline_warnings.csv` and `logit_tol1e8_fit_and_reference_warnings.csv` preserve primary-pipeline warnings separately from IRLS-reference warnings.
- `numerical_attempt_cholesky_*` and `numerical_attempt_tol1e7_to_tol1e8_provenance.csv`: rejected/earlier numerical attempts retained for audit; they are not accepted model outputs.

The active notebook source is being updated in stages. Its final official complete execution will regenerate these outputs after all approved stages are integrated. Historical outputs in `archive/` belong to earlier protocols.
