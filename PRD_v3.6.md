# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.6 — Sequential course-aligned 1-SE correction

**Status:** Implementation specification; numerical results remain **unverified until the v3.6 notebook has executed and passed its independent audit**.  
**Date:** 4 November 2026. **Development branch:** `analysis/prd-v3-6-sequential-one-se`.  
**Primary computational base:** [executed v3.4 notebook](archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb). **Presentation predecessor:** [PRD v3.5](PRD_v3.5.md).  
**New deliverable:** `online_shoppers_prd_v3_6.ipynb`, with new evidence in `artifacts/prd_v3_6/`.  
**Type of change:** Correct selection methodology and recompute only what this correction changes. Do **not** rewrite or overwrite the historical v3.0–v3.5 records.

### 1. Objective, data, scope

Prediction only: predict binary `Revenue=1` for a shopping session, not causal intervention response. Retain the original source file `data/uci_468.csv` (12,330 sessions), first-pass all-17 diagnostics, and 16 operational inputs excluding `PageValues` for **potential** decision-time unavailability rather than proven label leakage. Preserve the 80/20 seed-42 stratified division (9,864 training; 2,466 historically inspected reserved), the same five stratified outer training folds (seed 42), and fold-fitted preprocessing. Preserve the course-relevant four original classifier families (Logit, LDA, GaussianNB, BernoulliNB) and the Gini/Entropy tree paths unchanged. Preserve the EDA, diagnostics, original plots, hypothetical business-cost assumptions and their limitations.

The 41 **historical trial IDs** are the fixed experiment order (13 Logit, 13 LDA, 10 GaussianNB, 5 BernoulliNB, counting baselines), **not 41 automatically executable independent models** after changing the accepted pathway. No additional predictor hypotheses, grids, families, interaction searches, resampling strategies or post-hoc replacements may be added to improve the result. Missing IDs (L11–L12, D12–D14) were never executed. Historical v3.4 candidate outputs and decisions remain historical; newly built v3.6 candidates can differ because their parents differ.

### 2. Conventional one-standard-error rule

At **every sequential step within a family**, fit the single proposed challenger on the **latest retained** model, then compare the incumbent and challenger using their five *common* outer training folds. Let `best` be the higher mean five-fold CV ROC-AUC, ties broken deterministically by incumbent. Calculate

`SE_best = sample_sd(five AUCs of best, ddof=1) / sqrt(5)`  
`cutoff = mean_auc_best - SE_best`.

Of the two candidates with `mean_auc >= cutoff` (numerical tolerance `1e-12`), **retain the simpler candidate**. If the lower-AUC candidate lies below the cutoff, retain the best-AUC candidate. If complexity ties, prefer higher mean CV ROC-AUC, then the incumbent on an exact tie. This is an *AUC-maximisation adaptation* of Lecture 8's lowest-CV-error-plus-one-SE rule; it is not a significance or equivalence test.

**Freeze a reproducible simplicity measure:** Count fitted, non-intercept, **nonzero** regression coefficients (absolute value `>1e-10`) for Logistic Regression; use outer-fold mean counts, and report all five fold counts. Unpenalised Logistic and Ridge generally retain all encoded coefficients; LASSO/Elastic Net count only their active coefficients. For LDA and the two Naive Bayes families use the number of *retained encoded model inputs* (outer-fold mean); for D15 use each outer fold's actually selected encoded input count. Always report original retained source-group counts and encoded columns separately, so category pooling is not mislabelled an original source deletion. When equal complexity and AUC choose higher AUC. This complexity hierarchy is an **explicit project convention** informed by Lectures 8–9; the lectures do not prescribe a universal complexity metric across all classification estimators.

The source predictor `PageValues` remains excluded from all operational pathways. Do not make `PageValues` removal an ordinary model-selection step.

### 3. Fixed sequential experiment order and inheritance

Each family starts from its original `Operational16` baseline. For every historical trial ID in numeric chronological order **within that family**:

1. Snapshot the currently retained configuration and label.
2. Construct the one predeclared change on top of that retained configuration; **do not** use a frozen v3.1/v3.2/v3.3 family anchor.
3. If its prerequisites are absent, the operation is redundant, or the change is incompatible with its current retained representation, record `SKIPPED_INAPPLICABLE` and the exact reason; **no model fit, no invented score, no acceptance decision**. Example: if G6 drops `ProductRelated_Duration` and retains the deletion, G7's `log1p(ProductRelated_Duration)` is skipped. If G6 is not retained and that source remains, G7 may run.
4. Otherwise fit the challenger with all transformations, pooling, medians, scalers, tuning and model coefficients learnt **inside the applicable training folds**. Evaluate on the same held-out outer folds as the incumbent.
5. Apply Section 2's 1-SE simplest-model selection immediately. Carry forward the selected config to the next trial and write its exact parent, change, AUC, SE, complexity, cutoff, eligible status and decision into the v3.6 ledger.
6. Never carry a rejected change into a subsequent trial. A proposal replacing an existing alternative representation (e.g. SpecialDay binary vs categorical; Logistic penalty choice) must **replace**, not silently stack, the incompatible setting. Log such replacements explicitly.

**Fixed per-family order, matching the historical trial IDs:**  
Logit L0–L10, L13, L14; LDA D0–D11, D15; GaussianNB G0–G9; BernoulliNB B0–B4. The new v3.6 scores cannot be copied from historical v3.4 for any candidate whose parent or internal tuning changes.

**Practical incompatibility rules:** Removing a source is cumulative when the deletion is retained. Do not transform a removed source, construct a ratio when either numerator/denominator is gone, or reintroduce removed sources. Repeated application of an already-active identical transformation/indicator is a no-op to be skipped. L13 and L14 replace the preceding Logistic penalty instead of combining penalties. D15 keeps compatible current LDA feature engineering while performing inner-fold-safe grouped source selection; its unshrunk LDA search can replace a previously retained covariance-shrinkage configuration if necessary, with that replacement explicitly logged. The historical trial is retained in the ledger even if skipped. The set of scored candidates may therefore be **less than 41**.

### 4. Inner tuning: course's 1-SE regularisation rule

For L4 (L2 Logistic), L13 (LASSO) and L14 (Elastic Net, `l1_ratio=0.5`), retain the original **fixed historical C grids**, three stratified inner folds (seed 42), scaler fitted inside each inner training fold, solver and penalty. Change only the selection of `C`: calculate the **inner** mean ROC-AUC and one-SE cutoff of the best inner-CV AUC; among inner-grid eligible `C` values select the **smallest C** (strongest regularisation). Refit on the corresponding outer-fit data, then score the outer validation fold. This is the classification adaptation of Lecture 9's strongest-`lambda`-within-1-SE rule; smaller sklearn Logistic `C` means stronger regularisation. Record selected `C`, inner cutoff and outer nonzero coefficients per fold.

For D4's covariance-shrinkage grid, choose **strongest eligible shrinkage** (largest shrinkage value) using the same within-inner-grid one-SE principle, while identifying this explicitly as a project extension, not an example directly demonstrated by Lecture 9. The existing D15 grouped backward-selection procedure already selects the smallest source subset within one SE of its highest inner-CV AUC; preserve this nested logic, adapt its preprocessing to inherit retained compatible upstream representations, and retain its per-outer-fold path evidence.

**No leakage:** No outer-fold validation labels in inner tuning, training-only category pooling or stepwise paths. Compute outer AUC/SE exclusively on the fixed common outer validation folds.

### 5. Trees and overall winner

Do not modify the two classification tree candidate/pruning algorithms. Each tree's original entire cost-complexity path, five-fold AUCs, one-SE cutoff and fewest-leaves selection stay intact; preserve its independent v3.4 verified evidence. Following all four revised family pathways, compare the resulting four family finalists and the two unchanged tree finalists using highest **mean five-fold training ROC-AUC**. Use AP as supporting minority-class ranking evidence, not as a secondary optimisation target. Do not apply a universal simplicity penalty across distinct classifier families; the cross-family top-AUC choice is the original frozen project convention.

### 6. Notebook requirements — edit v3.4, do not rebuild

Start with a **copy** of `archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb`. Modify the smallest necessary modelling cells:

- Preserve data loading, train/reserved row IDs, original EDA, all-17 diagnostics, operational baselines, plot production and tree pruning sections.
- Update the feature/pipeline helper only to support inner 1-SE tuning, cumulative deletions/replacements, selected-feature counting and D15's inherited compatible feature engineering.
- Replace the historical decision-path orchestration with one fixed sequential decision engine; keep separate complete chronological tables for all four classifier families. Every historical ID must display `SCORED` or `SKIPPED_INAPPLICABLE`; show both numeric AUC/AP and complexity, the 1-SE cutoff, exact parent, and why a challenger was retained or rejected. Never display a stale v3.4 AUC as a v3.6 result.
- Retain 41 planned ledger entries including 4 baselines, but expect **variable scored count**. Dynamically audit the actual scored fold records; do not hardcode 51 scored designs, 255 fold rows, 37 scored decisions or 80 backward-path rows when trials may skip.
- Recompute from v3.6 predictions the final six-way table, winner OOF ROC/PR, reliability check, four diagnostic thresholds, cost table, training refit, historically reused reserved-set descriptive check and final all-data refit.
- Write **all new outputs only** to `artifacts/prd_v3_6/` and avoid changing `artifacts/prd_v3_4/` or archived notebook. Original common split/fold-ID files may be checked for equality; keep old immutable historical artefacts.
- In all prose, remove claims that L1/G7/B3/D0 must remain selected. Until execution, display no unverified updated finalist AUCs, reserved scores or threshold metrics. Original v3.4 results may be cited only when explicitly marked historical.
- Include a concise comparison of historical v3.4 finalists against newly recomputed v3.6 finalists, with no claim that the reserved set is fresh.

### 7. Verification and acceptance criteria (frozen)

1. New notebook is valid `nbformat` v4; code-cell sources compile; every cell executes in order from repository root with no error output, no missing model/fixture, and no stale modelling outputs masquerading as v3.6 results.
2. Original data SHA, 12,330 records, train/reserved membership, common outer CV folds and original 17-to-16 decision are unchanged. The source remains in the repository and all preprocessing remains fold-safe.
3. Exactly **41 trial-ID rows** are present, each scored or explicitly skipped, ordered by family and trial number. Four baseline rows are present. No more than 37 postbaseline scored decisions; each has parent equal to the previous retained specification and every skip has a deterministic reason.
4. Every scored trial has five finite ROC-AUC/AP values, complete OOF validation coverage and complexity counts; every accepted/rejected outcome is independently rederived from the two candidates' means, best SE, cutoff and complexity with the rule in Section 2.
5. In particular, G7 **must not execute if G6's deletion is retained**, and no deleted predictor may be silently reinstated. Regularisation uses inner 1-SE `C` selection and reports selected values and sparsity. D15 uses a separate nested one-SE group-size procedure if applicable.
6. Both trees reproduce the historically verified v3.4 selection metrics and leaf counts; final six-way comparison includes exactly four revised-family winners plus two selected trees.
7. Threshold confusion matrices and financial illustrations recompute from the **new winner OOF predictions**, and the selected winner alone receives a fresh v3.6 descriptive reserved-set check. Existing historical reserved scores are not mistaken for a pristine test or reused for tuning.
8. New artefacts, execution metadata, a compact v3.6 independent audit and versioned explanatory narrative all agree. Verification reports an explicit `PASS` or `FAIL`; never claim execution or statistical verification without a successful run.

### 8. Interpretation and provenance

The five repeated CV folds and historical reserved observations have already informed exploratory model development in v3.0–v3.5. Revising the selection protocol after reviewing their results can increase selection optimism. A course-aligned one-SE selection is a parsimony heuristic, **not** a significance or statistical-equivalence test. The reserved set is historically non-pristine and cannot become independent merely by re-running v3.6. ROC-AUC/AP do not show calibration, threshold economics are hypothetical (no observed treatment effects), and no feature selection proves causality.

**Immutable source of historical evidence:** [v3.4 executed notebook](archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb), [all 41 historical attempts](artifacts/prd_v3_4/all_attempts_ledger.csv), [all 255 historical fold scores](artifacts/prd_v3_4/all_attempt_fold_scores.csv) and [tree selection](artifacts/prd_v3_4/tree_selection.json). The v3.6 results must remain separately labelled.
