# DSA211 PRD v3 — Implemented technical plan

**Authority:** [PRD v3](PRD_v3.md). **Current executed deliverable:** [online_shoppers_prd_v3.ipynb](../online_shoppers_prd_v3.ipynb). **Rebuild:** [builder](../scripts/build_prd_v3.py). The [v2 plan](technical_plan.md) is historical.

## Preserved work
Reuse the original notebook's imports, data quality checks, training/holdout split, numerical and categorical EDA, assumption checks, four all-17 diagnostic models, and four operational baselines. Retain the original v2 notebook.

## Sequential experimental design
- Dataset: UCI 12,330 sessions, 17 predictors; 125 excess exact duplicate rows retained. Exclude PageValues for 16-feature operational models due to uncertain decision-time availability.
- Validation: fixed stratified train/test 80/20 with seed 42; shared five training stratified folds, seed 42. Fold-contained fitting of any encoder, log transform, median cutoff and category pooling. All four classifier pathways start with an all-16 baseline.
- Logit L1–L4: log1p activity, informational presence indicators, rare Browser/TrafficType pooling, then scaled L2 logistic with inner three-fold CV C in {0.05, 0.2, 1, 5, 20}.
- LDA D1–D4: log1p activity, SpecialDay binary, rare-level pooling, covariance shrinkage selected by inner three-fold CV in {0, .1, .3, .6, .9}.
- Gaussian NB G1–G4: log1p activity; remove BounceRates, ProductRelated, then SpecialDay as separate single changes.
- Bernoulli NB B1–B4: fold-fitted median cutoffs for ProductRelated, ProductRelated_Duration and ExitRates, then remove BounceRates.
- Each challenger is compared with the **last retained** family recipe on common outer folds. Retain only when mean fold AUC improvement exceeds one challenger fold AUC SE; otherwise revert. Preserve all rejected attempts and scores.
- Select one finalist per family and the overall winner by highest mean **five-fold** ROC-AUC; AP, SD and SE contextualise, without overriding this ranking.

## Economics and finalisation
- Illustrative upsell agent assistance: S$3 per contact, assumed 30% conditional upsell success, S$50 incremental gross margin. FP cost S$3, FN net opportunity cost S$12, theoretical cutoff **0.20**. No observed intervention uplift.
- Training OOF threshold references: buyer prevalence, 0.50, closest sensitivity-specificity crossover and fixed 0.20. Scenario q sensitivity: 20%, 30%, 40% with corresponding 0.30, 0.20, 0.15 cutoffs.
- Freeze model and cutoff before the reserved-set check, and perform unchanged all-data refit. Prior historical use of the reserved rows prevents a pristine independent test claim.
- Verification includes a clean execution, independent fold-level AUC/AP recomputation for every trial, recomputed SD/SE, checked sequential decisions and threshold confusion counts, finite parameter and output checks, and saved warning and package-version evidence.

## Evidence and limits
Evidence is versioned in [artifacts/prd_v3/](../artifacts/prd_v3/). The notebook is predictive only. AUC/AP do not prove calibrated probabilities, and UCI lacks observed upsell interventions. The project also needs separate presentation slides for the 20-minute talk; those are not contained in the notebook.
