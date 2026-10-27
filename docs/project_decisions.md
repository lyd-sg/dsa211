# Current project decisions — approved PRD v2.0 (27 October 2026)

See [PRD v2.0](PRD_v2.md) for the governing requirements and complete 24-decision ledger, and [technical plan v2.0](technical_plan.md) for precise implementation. [Historical decisions](project_decisions_v1_archive.md) describe the superseded economics scope.

- **Research:** prediction of session-level `Revenue=1`, not inference or treatment effects.
- **Source:** UCI 12,330 rows including 125 excess duplicate full rows, 17 source predictors; retain all original observations.
- **Protocol:** stratified 80/20 seed 42, five common stratified training CV folds seed 42; train-only EDA, fold-contained fitted preprocessing.
- **Four all-17 diagnostic models:** Logit, Gaussian NB, Bernoulli NB, LDA. Operational model inputs use the same remaining 16 sources without PageValues due to prediction-time availability uncertainty.
- **Four baselines:** raw, unpenalised Logit; Gaussian NB; Bernoulli NB; standard LDA.
- **Three revisions:** activity log/presence L2 Logit `C=1` with fold scaling; activity log and automatic covariance-shrinkage LDA; mixed Gaussian/discrete NB with Laplace smoothing.
- **Winner:** highest mean five-fold training ROC-AUC, with mean AP, fold SD and SE reported. Seven candidates use identical folds. Revised L2 Logit is the observed 26 October CV winner (0.758074 mean AUC; 0.335193 mean AP).
- **Thresholds:** exactly training prevalence, 0.5 and sensitivity–specificity crossover; report sensitivity, specificity and precision using winner OOF scores. Crossover is a balanced reference, not an optimal decision claim.
- **Display:** one CV table, one 7-model ROC overlay, one winner PR curve, one winner OOF score histogram, one sensitivity–specificity plot and a single three-threshold table. No redundant warnings/diagnostics in the main output.
- **Final fit:** numerical refit on all 9,864 training observations, then unchanged recipe fit on all 12,330 rows. Training-CV selection evidence only; no new independent test performance claim.
- **Submission:** concise lab-style notebook with a statistical purpose, evidence, interpretation and implication for each substantive analysis. Separate supplementary EDA is not submitted.
- **Removed:** economic discount, voucher policy, fixed 2/3, conversion scenarios, monetary cost/profit interpretation and causal uplift.

Historical technical verification results may be preserved without applying them to the currently revised estimator.
