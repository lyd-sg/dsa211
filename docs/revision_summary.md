# Completed PRD v1.0 revision

The active main notebook is fully executed. The separate executed supplementary EDA is retained but is not submitted. The approved PRD, dataset, historical archives and existing execution workflow are unchanged. The preceding active notebook was preserved byte-for-byte before replacement.

The revision replaces the historical 75/25, three-baseline and revenue-optimised 0.80 analysis with the approved stratified 80/20 split, four minimal baselines, three EDA-supported family revisions, five common stratified training folds, fixed 2/3 policy, four threshold references, four conversion assumptions, one winner audit and exact all-data refit. No feature/hyperparameter search or unrelated classifier was added.

## Training comparison

| Operational specification | Mean CV ROC-AUC | Mean fold AP |
|---|---:|---:|
| Raw Logit | 0.750020 | 0.324955 |
| GaussianNB | 0.692021 | 0.257450 |
| BernoulliNB | 0.723133 | 0.276353 |
| Raw LDA | 0.740879 | 0.316488 |
| Revised Logit | **0.757647** | **0.335012** |
| Revised LDA | 0.743728 | 0.321003 |
| Revised mixed NB | 0.731474 | 0.289378 |

Revised Logit is selected solely by mean fold ROC-AUC. Its fold AUC SD is 0.013016 and SE is 0.005821. Its descriptive gain over raw Logit is 0.007627 AUC; neither this gain nor one-SE proximity is a significance test. All three recipes were frozen from actual training EDA before scoring and retained without replacement.

The four all-17 diagnostic AUCs are 0.889716 (Logit), 0.787947 (GaussianNB), 0.876559 (BernoulliNB) and 0.899652 (LDA). Their better ranking with PageValues does not prove leakage. Operational exclusion is based on possible timing/availability concerns, which also remain relevant to the other session-summary predictors.

## Frozen policy and held-out audit

The official full run completed in 4m52s: all 18 code cells executed sequentially without errors. The one selected-model audit gives **ROC-AUC 0.741210 and AP 0.326790**. At exact **2/3**, TN=2,082, FP=2, FN=382, TP=0. Sensitivity and precision are zero; specificity is 0.999040. The policy assigns **2,464/2,466 vouchers (99.92%)**, so this threshold supplies no buyer detection and little selective targeting in the audit. No threshold or model was revised after these results.

At those same assignments, q=.10/.25/.50/1.00 produces hypothetical Rq/A of 472.16/722.00/1,138.40/1,971.20 against R0/A=382. q is unobserved; these totals are assumptions, not measured lift, actual revenue or profit.

The final clone of that exact specification was fitted to all 12,330 observations after the audit. It used 27 iterations, emitted no convergence warning, and was not scored again. The notebook displays the final fitted pipeline; its code recreates the object without requiring a serialized pickle.

## Numerical verification and limits

Raw unpenalised Logit required documented accuracy checks because rare pure levels and rank deficiency prevent finite/unique-MLE certification. Uniform cold Newton-CG tolerance 1e-8 passes all 15 CV same-likelihood IRLS comparisons; the full-training refit also passes. Failed earlier numerical attempts are explicitly labelled. Four teaching baselines, all source treatments and fold containment remain intact.

Independent checks reconstruct saved fold/test metrics, confusion counts, mixed-NB likelihoods, threshold crossover and voucher equations. Only factual Markdown clarifications followed the audit; code and outputs match the official execution. See [verification report](verification_report.md) and review records for individual PRD criteria, actual evidence and unperformed checks. Original teaching files were unavailable; remote CI was not run; historical overlapping-data exposure, calibration/assumption limitations and unknown voucher response remain explicit.
