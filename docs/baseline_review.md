# Independent baseline implementation review — Task 2A

**Decision: PASS for the training-only baseline stage, 25 October 2026.** Implementation of the three already-approved revised recipes may proceed. This decision does **not** authorise test access or certify the unfinished full notebook as executed.

Reviewed snapshots:

- Main notebook source: SHA-256 `e41bcd31e3b8962a0fcd6c8b608e64f43a25a2258168827b574442fb3cc30508`.
- Current ten-fold numerical gate CSV: SHA-256 `86d8621acbbdd0f3709b8fdf3d03eaeeab1b3ecba11ad30359cd8f9e1ce1afdb`.
- Canonical eight-model baseline summary: SHA-256 `c6c1011260c4be50a86e0d80960aa9bc1526a99b4a912f8598cc9ae8ea48ddbb`.
- Canonical 40-fold metrics/diagnostics: SHA-256 `bbf5285cef73137bd38fb354879d380b6114e8e7f71c34f832bceae6304943e8`.

## Scope and independently inspected evidence

The reviewer inspected actual main-notebook source for data checks, training EDA, sklearn pipelines, likelihood inputs, fold fitting, numerical diagnostics, warning handling, tables and persistence. The reviewer also inspected the actual executed training-only checking/refinement scripts, accepted fold artifacts, all eight OOF prediction vectors and rejected-attempt provenance. No new model fit or holdout-outcome inspection was performed by this review.

The intermediate active notebook has **uncached/unexecuted outputs** after integration edits. Earlier complete execution supplies the six unchanged non-Logit candidate vectors; the updated current `run_spec` supplies both five-fold Logit vectors and their current IRLS checks. The artifact README discloses this provenance. A final official top-to-bottom execution of the complete self-contained notebook remains mandatory; this PASS must not be described as that final execution.

## Requirement findings

| Check | Independent finding |
|---|---|
| A1 data discipline | PASS. Basic quality checks precede splitting; 12,330 rows including the 125 excess duplicate records remain. The main notebook discards nontraining records after reconstructing the prescribed stratified 80/20 membership. Sorted original training-row order and shared five-fold mappings agree with the reviewed supplementary protocol. Historical overlapping 75/25 exposure is explicitly disclosed. |
| A2–A4 reasoning | PASS for source and inspected training evidence. Purpose precedes substantive analyses; numerical tails/zero mass, supported category summaries and selected within-class relationships lead to bounded implications. Main summaries are now shorter than supplementary cross-cell investigations. LDA dependence and PageValues timing overclaims were corrected. Final chart/output consistency remains part of final execution review. |
| Four all-17 fits | PASS. Logit, GaussianNB, BernoulliNB and LDA use the same training folds and are diagnostic only. Operational counterparts permit paired same-fold PageValues comparisons. Association is described as descriptive; timing is possible/unverified rather than asserted as proven leakage. |
| Four operational baselines | PASS. All use the same 16 source predictors. Original numerical magnitudes, numeric SpecialDay and 0/1 Weekend are retained except Bernoulli's required >0 conversion. Six nominal variables use k−1 OHE for Logit/LDA and full k OHE for both NB models. No optional scaling, penalty, weighting, deletion or engineering was introduced. |
| Pipeline/fold containment | PASS. New sklearn Pipeline/ColumnTransformer/estimator instances are fitted per fit fold; validation data use only that fitted encoding. Positive-class probabilities are selected using the fitted class label, not a silent class-order assumption. |
| Unknown levels | PASS. OHE ignores unseen levels as documented all-zero blocks; actual validation-level values/counts are persisted. Reference ambiguity for k−1 encoding remains a limitation. Validation-transform warnings are captured with the correct candidate/fold. |
| Non-Logit numerical evidence | PASS for this stage. Saved predictions and fitted-parameter checks are finite. Standard SVD LDA retains its full prescribed inputs and known rank limitations; it was not replaced by a numeric-only or shrinkage alternative. NB likelihood shortcomings are disclosed, not used to remove their eligibility. |
| Logit estimation transparency | PASS under the explicitly recorded finite-iterate numerical admission rule below. Pure levels and rank deficiency are visible; no finite or unique MLE is claimed. Same-model solver accuracy changes do not alter the baseline likelihood or input representation. |
| Metrics and provenance | PASS. Each of the eight vectors has 9,864 unique training row IDs. Independently reconstructed fold AUC/AP, mean, sample SD, SE and pooled metrics match canonical artifacts within 1.11e−16. ROC-AUC mean and pooled OOF AUC remain distinct. Warnings are now recorded once, with separate primary and IRLS-reference labels. |
| Stage boundary | PASS. No revision, winner, threshold or held-out evaluation is implemented/scored in this stage. A later training-stage review must inspect all seven operational specifications and frozen decisions before test access. |

## Logit numerical admission

The original cold Newton-CG tolerance 1e−7 did not meet the precommitted probability-stability criterion for one all-17 fold. The strict Newton-Cholesky attempt was also rejected after singular-Hessian fallback and large objective/probability discrepancies. Their evidence is retained as failed/earlier numerical attempts; neither is silently presented as the accepted estimate.

Both Sol agents agreed the following predictive numerical criteria before seeing final comparison deltas: finite parameters/probabilities, a converged same-likelihood reference, absolute **mean fit-fold** logistic NLL difference ≤1e−6 per observation and maximum label-free validation-probability difference ≤1e−3. These tolerances were not relaxed based on AUC. A training-only diagnosis of the discrepant pure TrafficType level distinguished boundary approximation error from fitted-design nullspace ambiguity.

The accepted baseline uses cold-start `LogisticRegression(C=np.inf, solver='newton-cg', tol=1e-8, max_iter=2000)` uniformly. The actual source compares it to `GLM(Binomial).fit(method='IRLS', wls_method='pinv', maxiter=200, tol=1e-10)` on the identical fit-fold encoded design with an explicit intercept and no penalty, scaling or deletion. It computes direct stable logistic NLL on fit rows and compares validation probabilities without using validation labels in the admission rule. Finite intercepts/priors and reference fit/validation linear predictors are checked.

All ten current-source Logit fit-fold comparisons pass unchanged criteria. Primary fits take 248–556 iterations. Absolute mean training-NLL differences are approximately 9.85e−9–2.18e−8; maximum validation-probability differences are approximately 3.25e−6–3.21e−4. The current references converge in 13–18 iterations and preserve their rank-deficiency warnings. The gate and combined warnings file now distinguish primary pipeline warnings from IRLS-reference warnings.

This supports reproducible finite-iterate predictive scoring at the stated precision. Pure nominal levels mean a finite MLE may not exist; rank deficiency means coefficients may not be uniquely identified. A passed objective/probability comparison does not establish either finite or unique coefficients, calibration, inferential validity or absence of every separating direction. The notebook correctly preserves that distinction. The same numerical criteria must be applied to revised Logit and any later training refit, without outcome-driven relaxation.

## Reproducibility and remaining gates

Read saved probability CSVs with `float_precision='round_trip'` for metric verification. Default parsing can alter last-bit distinctions near probability one and change GaussianNB AP through score ties; this is a serialization precision issue, not an additional model result. Current artifacts reconcile with round-trip parsing.

No material unresolved baseline-stage defect remains. Before any holdout access, inspect the actual three revised implementations, exactly seven operational rows, their common-fold OOF evidence, numerical validity, winner-selection rule and frozen exact 2/3 policy. The final complete notebook must then execute officially, with current outputs, a single-winner test audit and exact all-data refit. Original teaching files remain unavailable; direct source-file course verification is still unperformed and disclosed.
