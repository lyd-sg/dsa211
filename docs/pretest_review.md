# Independent pre-test training review — Task 2B

**Decision: PASS — 25 October 2026.** The reviewed training analysis and frozen winner/policy satisfy the pre-test gate. Lead Sol may authorise implementation of the single-winner test audit and exact final refit after inspecting that new code. This is not a final-project execution PASS, and it does not approve an alternative model, threshold or post-test revision.

Reviewed snapshots:

- Main training-stage notebook source: SHA-256 `5b57625708220e20999d68da667453f5baad3630f8392a46f96fd0825ed95f95`.
- Training freeze: SHA-256 `92c385c098fdba0dbb7575c1d4d13a3a1c0b1620c27073492f12d8e1ffa0ab30`.
- Seven-candidate CV table: SHA-256 `e05e39c3928982032645f3e40a6c5fc884fc4919bc4b34d889a105979dbcb96d`.
- Revised-Logit numerical evidence: SHA-256 `127a68471f1103fb58a842860f18acf4b31d145a33d7b2c92a7d6644ffdd9c18`.
- Mixed-NB component evidence: SHA-256 `b233d723455a3baeb2bea27cbb5b7a488aa3be607a8c7f742499b7a3611831b8`.

## Independent inspection and execution limits

The reviewer inspected the actual revised classes, generic CV implementation, admission checks, comparison/selection, OOF histogram, threshold arithmetic, q scenarios, persistence and freeze source. All seven saved operational OOF vectors, their five-fold evidence, mixed-likelihood components and four actual training figures were inspected independently. Numerical verification used saved predictions and direct arithmetic; the reviewer did not fit a model or explore holdout outcomes.

Task 2B executed the actual three revised implementations and training-analysis cells while reusing the already-reviewed baseline artifacts. The integrated active notebook still awaits its **official complete top-to-bottom execution**. Cached training-analysis recalculation does not stand in for that final execution. No test audit or final-refit source was present in this reviewed training snapshot.

## Model and leakage review

| Requirement | Independent finding |
|---|---|
| Exactly four baselines plus three conditional revisions | PASS. The operational list has seven distinct labels; all-17 diagnostics remain excluded from selection. Recipes match the approved evidence addendum and retain all 16 operational source predictors. |
| Revised Logit | PASS. The six activity magnitudes use fixed log1p; the >0 indicators are selected by zero share ≥.50 computed inside each fit fold. Every actual fold selects Informational and Informational_Duration. Rates, SpecialDay and Weekend remain untransformed; nominal indicators are k−1. No scaling, penalty or feature search appears. |
| Revised LDA | PASS. Only the six activity magnitudes receive log1p; standard SVD and all 16 sources remain. No shrinkage, deletion or added presence block appears. Correlated inputs are not incorrectly described as prohibited by LDA. |
| Revised mixed NB | PASS. Exactly eight Gaussian inputs and eight categorical fields match the recipe. Weekend is normalised to integer 0/1 before string encoding; SpecialDay becomes presence only in this revision. Fold-fitted maps reserve unknown code 0 and include it in Laplace support. |
| Mixed prior and likelihood calculation | PASS. Gaussian `predict_log_proba` already includes the empirical class prior once. Adding categorical log likelihoods and renormalising removes only a class-common constant, yielding the intended single-prior posterior. No second prior is added. |
| Fold containment and unknown levels | PASS. Preprocessors/maps/zero-share eligibility fit only on fit rows. Revised OHE unknowns use documented all-zero handling; mixed NB unknowns use smoothed code 0. Actual unseen values and support evidence are persisted. |
| Numerical admission | PASS. Revised Logit uses the uniformly fixed cold Newton-CG tolerance 1e−8. All five same-likelihood IRLS checks pass unchanged criteria: mean fit-NLL differences approximately 6.36e−10–1.02e−9 and maximum validation-probability differences 3.15e−7–1.38e−6. Pure levels/rank deficiency remain disclosed without finite/unique-MLE certification. Source now stops selection if a required all-17, baseline or revised Logit gate fails. |
| Fair selection | PASS. Complete finite OOF vectors, one validation assignment per training row, fold counts and stored metrics are checked before comparing seven operational specifications. Highest mean five-fold ROC-AUC wins; exact ties use label order. AP and hypothetical revenue do not select the model. One-SE proximity is descriptive. |

## Independent numerical reconstruction

Each operational candidate has 9,864 unique training row IDs, matching the committed source labels and the common fold map. The reviewer recomputed all 35 ROC-AUCs from Mann–Whitney ranks and all 35 average-precision values from grouped descending-score precision, including ties. Fold means, sample SDs and SEs agree with the comparison table within **1.18e−16**. Saved probabilities were read with round-trip CSV precision.

The selected model is **Revised | Logit**, mean CV ROC-AUC **0.7576467609891068**, with AP approximately **0.3350121**. Its improvement over raw operational Logit is approximately **0.007627 AUC**, a descriptive comparison after training-informed candidate formation. No other candidate falls within the selected winner's one-SE range under the declared rule; this is not a hypothesis test.

The reviewer checked all **40 categorical field supports** across five mixed-NB fit folds against actual fit-row category/outcome counts. Class counts, empirical priors, unknown counts of zero, support size K+1 and denominators N_class+alpha(K+1) reconcile. In **eight stored validation examples**, including three unknown codes, direct Gaussian log densities plus **one prior** and categorical log frequencies reproduce saved OOF posterior probabilities within **1.50e−15**. This checks actual likelihood components without fitting another classifier.

## Threshold and policy review

PASS. Source now derives C_FN=.20A and C_FP=.80×.50A=.40A, giving .40/(.40+.20)=2/3, with the meaningful-probabilities caveat. Exact 2/3 remains primary. The crossover uses rates from the full empirical OOF ROC cutoffs plus probability endpoints, with lower-threshold tie breaking; it no longer computes policy revenue across the entire cutoff curve.

The reviewer independently reconstructed the crossover as **0.17961341093938224** using sorted OOF scores and cumulative outcome counts. The exact training-prevalence reference is **0.15470397404703973**. The table contains exactly these references, .500 and 2/3. All four confusion counts, rates, voucher assignments and revenues reconcile with direct row-level arithmetic.

At 2/3, training OOF counts are **TP=4, FP=2, FN=1,522, TN=8,336**. The policy assigns **9,858/9,864 vouchers**, so very low sensitivity and minimal targeting selectivity are substantial findings, not evidence that AUC establishes useful threshold behaviour. The main notebook now interprets score concentration and near-universal voucher coverage explicitly rather than leaving only generic calibration caveats.

At frozen assignments, q=.10/.25/.50/1.00 yields Rq/A=**1,888.48 / 2,888.80 / 4,556.00 / 7,890.40**, with R0/A=1,526. Direct per-row reconstruction agrees within **9.1e−13**. At q=.50 the assumed .40TN contribution is 3,334.4A, offset by the .20FN discount loss of 304.4A, for a hypothetical difference of 3,030A. Only q varies; no recipient or threshold is reoptimised. These large totals reflect unobserved conversion assumptions, not measured growth, profit or demonstrated targeting value.

## Presentation, freeze and next boundary

The seven-curve ROC overlay, outcome-separated OOF histogram, sensitivity/specificity references and q-sensitivity figure have meaningful labels and appropriate training/hypothetical context. The threshold figure now distinguishes all four references visually and identifies the crossover. A7–A11 state their purposes, show actual evidence and provide concrete implications. Remaining probability, timing, historical-exposure and selection-adaptation limitations remain applicable.

The freeze records the verified winner recipe, selection rule, source hash, full split/fold IDs, exact primary threshold, discount, reference q and training policy counts. Its pending-review status accurately describes the snapshot reviewed here; this PASS supplies the independent review of that frozen analytical decision. Lead Sol should retain a separate dated approval record before proceeding to test code/execution.

**Remaining required work:** inspect new single-winner audit/refit code before execution; execute the full self-contained notebook officially; score only the frozen winner once; reuse that saved test vector for all audit calculations; then refit the exact specification on all 12,330 rows without another score. Any modelling defect discovered after test access must be disclosed. The final independent audit must inspect the actual executed notebook and final evidence against every PRD criterion. Original teaching files remain unavailable, so direct comparison against their originals is still unperformed and must remain disclosed.
