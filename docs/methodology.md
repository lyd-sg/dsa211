# Current methodology — approved PRD v2.0

**Authority:** [PRD v2.0](PRD_v2.md) and [technical implementation plan v2.0](technical_plan.md). [Previous methodology](methodology_v1_archive.md) pertains to PRD v1.0 and is not current.

## Data and predictor preparation
Check UCI source quality, target, types, blank/missing and exact duplicate rows; retain all 12,330 sessions. Reconstruct stratified 80/20 split, `random_state=42`; perform EDA only within 9,864 training sessions. Common five stratified shuffled training folds, seed 42. Each fold's feature encoding, optional scaling, categorical likelihood maps, zero-share feature choice and covariance estimation use only fit rows. Unknown nominal categories are handled deterministically.

## Candidate models
Four initial all-17 diagnostic models establish effects of PageValues (excluded operationally due to uncertain availability before prediction). Seven operational candidates: four unchanged baselines using 16 sources and three EDA-motivated revised recipes: fixed-L2 log/presence/standardised Logit (`C=1.0`), log-transformed auto-shrinkage LDA, and smoothed mixed-likelihood NB. Exact recipes, data-type treatments and numerical checks are in the technical plan. No QDA, KNN, automated grids or post-hoc feature search.

## Evaluation
All seven candidates use identical training CV folds. Select highest **mean five-fold ROC-AUC**, report mean AP, AUC SD, AUC SE, per-fold details and a single OOF ROC overlay. The selected model is also shown with one OOF PR curve and a purchase-prevalence no-skill line. Mean fold AP differs from pooled OOF AP; label both accurately. ROC-AUC/AP evaluate ranking and do not certify probability calibration.

## Threshold analysis
On winner training OOF predictions, compare three references: training prevalence, 0.5 and closest sensitivity–specificity crossover. Define positive class Revenue=1 and predict positive for `p>=t`. Show sensitivity, specificity and precision, with undefined precision handled explicitly. The crossover minimises the absolute rate gap over valid empirical thresholds plus endpoints, tie by lower cutoff. No economic objective or price scenario.

## Refitting and reporting
Refit frozen CV winner on training to verify numerical validity; final fit of exact same recipe on all 12,330 rows for a finished specification. Do not report in-sample or new independent test scores as generalisation evidence. Include true uncertainty about prediction-time feature availability, class imbalance, CV selection optimism and NB/LDA assumptions.

**Output discipline:** purpose → evidence → interpretation → implication; concise, nonduplicated charts and tables. [Historical v1 reports](verification_report.md) are not evaluations of the current L2 recipe.
