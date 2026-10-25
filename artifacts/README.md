# Audit artifacts

These files support the training-only baseline and revision stages; they are not additional model searches. Row IDs are zero-based positions in the unchanged committed CSV, not customer identifiers.

- train_row_ids.csv, test_row_ids.csv: seed-42 stratified 80/20 membership in original-row order. Test IDs are recorded for reproducibility only.
- cv_fold_row_ids.csv: five shuffled stratified folds (seed 42) on sorted training IDs, with fit/validation roles.
- baseline_summary.csv and baseline_fold_metrics_diagnostics.csv preserve the eight reviewed baseline candidates (four all-17 diagnostics and four raw operational baselines). model_summary.csv/json, model_fold_metrics_diagnostics.csv, and model_warnings.csv extend that evidence with the three revisions for eleven model rows total. The two raw Logit candidates use cold-start newton-cg tolerance 1e-8; the other six original baseline vectors are unchanged from the reviewed run.
- Eight baseline OOF files and three revised_*_oof.csv files: canonical candidate probability vectors. Read CSV probabilities with float_precision=round_trip for exact metric reconstruction.
- logit_tol1e8_numerical_gate.csv/json: accepted raw baseline comparisons against same-likelihood Binomial IRLS.
- revised_logit_numerical_gate.csv: five-fold revised Logit objective/probability gate and fit-fold zero-share presence eligibility.
- revision_baseline_comparisons.csv: paired changes against Logit, LDA, GaussianNB and BernoulliNB baselines.
- seven_candidate_cv.csv, seven_candidate_fold_scores.csv, seven_candidate_oof_predictions.csv: complete seven-slot training comparison.
- training_oof_roc_seven.png, training_winner_oof_probability_histogram.png: training-only ranking and score-distribution figures.
- winner_four_thresholds.csv, winner_threshold_sensitivity_curve.csv, winner_threshold_sensitivity.png: exactly four supported threshold references and training-OOF sensitivity/specificity curve.
- winner_q_scenarios_at_two_thirds.csv, winner_q_scenario_sensitivity.png: four fixed-recipient conversion scenarios at threshold 2/3.
- mixed_nb_component_audit.json: per-fold likelihood component evidence for independent prior, category-support and prediction-arithmetic review.
- training_freeze.json: strict-JSON training decision and exact split/fold IDs, pending root/reviewer pre-test review; it does not authorize test access.
- numerical_attempt_cholesky_* and numerical_attempt_tol1e7_to_tol1e8_provenance.csv: rejected/earlier solver attempts retained as provenance, not accepted model outputs.

No held-out predictions or metrics are present. A full official top-to-bottom notebook execution remains for the later integrated stage.
