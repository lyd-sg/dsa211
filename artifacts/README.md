# Final audit artifacts

These files come from the approved protocol and its official completed execution; they are not additional model searches. Row IDs are zero-based positions in the unchanged CSV, not customer identifiers. Read probability/metric CSVs with `float_precision='round_trip'` when reproducing numerical checks.

## Data, execution and preservation

- `train_row_ids.csv`, `test_row_ids.csv`, `cv_fold_row_ids.csv`: exact seed-42 stratified 80/20 membership and five common training folds, in original-row order.
- `execution_authorisation.json`: lead approval after independent training/static reviews, recorded before any test prediction file existed.
- `execution_verification.json`: actual official exit status, sequential cell counts, figure counts and unchanged approved code hash. Only Markdown clarifications followed execution.
- `protected_files_sha256.json`: protected data, approved PRD, archive, prior-active copy and original workflow hashes.

## Training evidence

- `baseline_summary.csv/.json`, `baseline_fold_metrics_diagnostics.csv`, `baseline_warnings.csv`: four all-17 diagnostics plus four operational raw baselines (8 models / 40 folds).
- `model_summary.csv/.json`, `model_fold_metrics_diagnostics.csv`, `model_warnings.csv`: all 11 designs / 55 folds. The seven operational rows alone are eligible for selection.
- `seven_candidate_cv.csv`, `seven_candidate_fold_scores.csv`, `seven_candidate_oof_predictions.csv`: exact seven-model mean AUC/SD/SE/AP comparison, 35 fold scores and 69,048 OOF records.
- Eleven canonical `*_oof.csv` files: 9,864 training predictions per design. `*_oof_tol1e8.csv` and `*_folds_tol1e8.csv` preserve the accepted numerical-precision checkpoint for the two raw Logits.
- `logit_tol1e8_numerical_gate.csv/.json`, `revised_logit_numerical_gate.csv`: accepted fold-level same-likelihood IRLS comparisons. Primary pipeline warnings and IRLS-reference warnings are distinct. Pure levels/rank deficiency remain limitations, not finite-MLE certification.
- `mixed_nb_component_audit.json`: five fitted mixed-NB likelihood records, 40 category supports/denominators and eight actual validation component examples, including unknown levels; class prior counted once.
- `revision_baseline_comparisons.csv`: actual revision changes, with mixed NB compared to both taught NB baselines.
- `winner_four_thresholds.csv`, `winner_threshold_sensitivity_curve.csv`, `winner_q_scenarios_at_two_thirds.csv` and labelled training figures: four OOF references and four fixed-recipient q scenarios. Primary 2/3 is never selected by revenue.
- `training_freeze_pretest_reviewed_snapshot.json`: the exact pending-review snapshot approved independently. `training_freeze.json` records the frozen winner/policy and the subsequent PASS pointer; Git history preserves both stages.
- `numerical_attempt_cholesky_*` and `numerical_attempt_tol1e7_to_tol1e8_provenance.csv`: explicitly rejected/earlier numerical attempts. They are not current accepted scoring results.

## Sole winner audit and final refit

- `winner_training_fullfit_audit.json`: exact training refit and training-only numerical reference before test access.
- `test_predictions.csv`: the sole frozen-winner held-out probability vector, source IDs, unchanged outcomes, 2/3 classifications and vouchers. Every subsequent test calculation reuses it.
- `test_metrics.json`, `test_q_scenarios.csv`, `test_unseen_categories.json`, `test_prediction_warnings.json`, `test_winner_roc.png`, `test_winner_confusion_matrix.png`: one audit at 2/3 and four hypothetical q scenarios with constant recipients. Zero buyer detection is retained and interpreted explicitly.
- `final_refit_metadata.json`: clone of the same specification fitted to all 12,330 rows after the audit; no subsequent prediction or score.
- `project_summary.json`: actual computed project results and limitations.

The fully executed main notebook is the academic submission; the supplementary EDA stays separate. Historical `archive/` outputs belong to earlier protocols. None of these artifacts establishes real voucher effects, profit, historically pristine validation or real-time feature availability.
