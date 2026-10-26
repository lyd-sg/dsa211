# Independent training-evidence and recipe review

**Decision: PASS — 25 October 2026.** The exact three revised recipes in the technical-plan addendum are approved for implementation and training-only scoring. This does not approve uninspected model code, numerical results or test access.

Reviewed snapshots:

- Technical plan including recipe addendum: SHA-256 `eabb952438b3b87bac64cb4addc23fbacf8ef0e4f4e3e85eed3b7ead535a8bfa`.
- Executed supplementary notebook: SHA-256 `82988b7f6c3a4a02d5cfc65a7f181a3e1f8b31cbc67b478b0b3e984c110bfee9`.

The independent reviewer inspected all supplementary source cells and substantive outputs, the three rendered charts, the addendum and its consistency with approved PRD §§5.1–7. The seven code cells have execution counts 1–7 and no error outputs. The reviewer separately reconstructed split membership and CV mappings and recomputed the principal training-only descriptive statistics from the committed CSV. No models were fitted or scored by this review and no holdout outcomes were explored.

## Evidence verification

Training and held-out row-ID sets match the prescribed stratified seed-42 split exactly: 9,864 and 2,466 disjoint records. The training set contains 1,526 buyers. All five persisted fold mappings match shuffled StratifiedKFold with seed 42 on the documented sorted training-row order; every training record occurs in validation exactly once. Predictor investigations operate on the training rows after the full-data quality block, which retains and describes duplicates without deriving a model rule from holdout predictors.

Independently recomputed activity skewness, zero shares and zero/positive buyer rates agree with notebook/addendum evidence. Five activity variables have skewness above 2; Administrative count is 1.966817, which the addendum candidly distinguishes from the others. Informational and Informational_Duration zero shares are .785381 and .804745, with zero/positive buyer rates .132955/.234294 and .134921/.236241. The positive sample sizes are substantial. Applying one activity-block compression is a defensible limited representation hypothesis; these marginal contrasts do not establish conditional logit shape or predictive improvement.

The revised empirical-logit code preserves every zero in one stratum and bins positive actual values with tie-preserving qcut. It no longer splits identical zero values according to row rank. Positive-bin counts need not be equal; corrected prose accurately describes quantile bins that preserve ties. Product-duration patterns make compression plausible, while uneven administrative/informational bins remain visible counterevidence.

The supported subgroup tables and rare-category tables support restraint: sparse cells do not warrant a new interaction or arbitrary pooling. SpecialDay presence counts independently reconcile to 8,850/1,466 buyers at zero and 1,014/60 at positive scores, with buyer rates .165650/.059172. Nonmonotone positive-score rates support a coarse discrete representation as a hypothesis without proving that score intensity is useless.

Within-class correlations independently match the stated values. The earlier wording implying that strong correlation itself violates LDA was corrected and reexecuted: dependence challenges NB conditional independence, whereas LDA permits correlated predictors. Selected class-correlation differences do not by themselves establish unequal full covariance matrices. Long tails and mixed feature types provide a cautious motivation for the LDA representation revision; the analysis does not certify Gaussianity or equal covariance after transformation.

The three figures have meaningful titles/axes; Month is chronological, SpecialDay points identify support, and histogram count axes explicitly use log scale. Each of the five required supplementary investigations states purpose, evidence and implication. The complete feature-availability table appropriately distinguishes assumptions from verified decision-time availability.

## Exact recipe assessment

| Conditional slot | Decision and rationale | Required implementation boundaries |
|---|---|---|
| Revised Logit | PASS. Six activity log1p magnitudes plus fit-fold-selected presence indicators address documented tails and informational zero mass without a feature search. | Keep all 16 sources, raw BounceRates/ExitRates/SpecialDay/Weekend, k−1 nominal encoding, no scaling or penalty. Learn zero-share ≥.50 eligibility within each fit fold. Retain the fixed recipe if CV deteriorates. Apply the mandatory separation/numerical gate from the plan review. |
| Revised NB | PASS. Gaussian log-activity/rate likelihoods plus categorical nominal/Weekend/SpecialDay-presence likelihoods address the baseline likelihood mismatch as one clearly labelled extension. | Exactly eight Gaussian inputs and eight discrete inputs as specified. Fit maps/unknown support on fit folds; alpha=1 includes reserved unknown support. Count the empirical class prior once when combining log likelihoods and normalise stably. No added correlated presence block, tuning, deletion or alternate NB search. Retain the remaining zero-mass/dependence caveats. |
| Revised LDA | PASS. The same limited six-activity log1p block is a plausible tail-compression hypothesis, whose value remains unknown. | Keep all 16 sources, raw rates/SpecialDay/Weekend, k−1 nominal encoding and standard SVD. No shrinkage or feature deletion. Do not claim that correlation is prohibited by LDA or that log1p repairs its assumptions. |

Together with the four unchanged prescribed baselines, these are **exactly seven operational specifications**, with common folds and equal selection eligibility subject to honest numerical validity. The four all-17 diagnostic counterparts remain outside operational winner selection. Neither EDA evidence nor this PASS predicts which model will win or whether any revision will improve ROC-AUC.

## Next review boundary

The training-only modelling stage may proceed. Before test access, independently inspect actual encodings, likelihood/prior code, fold fits, all seven OOF vectors, warning records and Logit convergence/separation/stability evidence. Rare pure levels require transparent investigation; a finite numerical iterate must not be represented as a certified finite MLE. Freeze the selected specification and exact 2/3 policy only after that inspection passes. Existing held-out and final-refit restrictions remain unchanged.

Original teaching materials remain unavailable, so direct comparison against their files was not performed. This review uses the course requirements recorded in the approved PRD. No new scope or statistical extension beyond the reviewed addendum is authorised.
