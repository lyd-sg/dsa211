# DSA211 implementation handoff — PRD v3.7 candidate

**Branch:** `planning/prd-v3-7-seven-per-family`. **Draft review:** [PR #17](https://github.com/lyd-sg/dsa211/pull/17). **Notebook:** [online_shoppers_prd_v3_7.ipynb](online_shoppers_prd_v3_7.ipynb). **Requirements:** [PRD_v3.7.md](PRD_v3.7.md). This candidate is constructed but **not numerically verified** until `artifacts/prd_v3_7/v3_7_verification.json` reports PASS. Main's latest verified presentation remains v3.5.

## Core implementation principle

**Do not rebuild v3.7 from scratch.** Preserve the exact executed v3.6 notebook's computation, seed-42 split, common outer folds, fold-fitted feature transform, sequential 1-SE comparator, nested regularisation selection, D15 grouped backward subset search, trees, selection, thresholds, training/reserved check and refits. Restore the six substantive EDA investigations and readable presentation from the executed v3.5 notebook. Add **only** B5/B6 as new model hypotheses. Keep historical v3.4/v3.5/v3.6 evidence unchanged.

## v3.7 presentation aliases

- Logistic: displayed `L0–L6` maps to original `L0,L1,L3,L4,L10,L13,L14`.
- LDA: displayed `D0–D6` maps to original `D0,D1,D3,D4,D9,D11,D15`.
- Gaussian NB: displayed `G0–G6` maps to original `G0,G2,G3,G4,G7,G8,G9`.
- Bernoulli NB: displayed `B0–B6` maps to original `B0,B1,B2,B3,B4,B5,B6`.

Display tables contain only: **Model, CV ROC-AUC, AUC SE, CV AP, ΔAUC against real incumbent, Complexity, Retained after iteration**. Exactly seven scored rows per family. No status, trial-version, raw-parent, skip-reason or full-ledger table in the submitted notebook. All original experiment IDs, parents, skipped trials, fold results and acceptance decisions must remain in machine-readable audit files. `Retained after iteration` is derived from the **full actual sequential** pathway, including hidden scored tests; it is not recomputed by replaying only seven displayed rows.

**B5:** Replace `ProductRelated` and `ProductRelated_Duration` Bernoulli binary inputs with one conjunction of their separate training-fold median exceedance indicators. Learn both medians within each fitting fold; do not retain the original pair alongside the composite. **B6:** Pool rare Browser/TrafficType categories with fewer than 50 observations per fitting fold, preserving binary one-hot encoding. Apply B6 to the actually retained incumbent after the B5 selection decision. Do not assume either is accepted.

**Sequential selection:** The 1-SE cutoff uses the **best mean fold ROC-AUC of the incumbent/challenger pair minus the SE of that best model**. Select simplest candidate above cutoff; break complexity ties by higher AUC, then incumbent. Inner regularisation picks the strongest penalty within inner 1-SE. Across six finalists select highest mean training ROC-AUC, not a global 1-SE model. AP and hypothetical business thresholds do not drive selection.

## EDA / syllabus contract

Restore zero/positive activity, positive intensity, Month × VisitorType support, rare-category counts, SpecialDay, feature availability, within-class covariance, long tails, binned marginal logits and the EDA-to-hypothesis bridge. Cite course correspondences as appropriate: Lectures 2–4 for function forms, collinearity and interactions; Lecture/Lab 6 for Naive Bayes and binarisation; Lab 7 for cross-validation, leakage-safe pipelines and polynomial features; Lecture 8 for grouped subset/1-SE; Lecture/Lab 9 for Ridge, LASSO and Elastic Net; Lecture 10 for classification trees. Do not add unsupported VisitorType × Month interaction or unrelated models solely for syllabus breadth.

**Tree:** Four compact full/pruned comparison rows in Section 7B. The **Entropy pruned tree image must be directly after this comparison and before Section 8**.

## Verification and change discipline

Run `python scripts/run_verify_prd_v3_7.py --run` using the repository's `requirements.txt`. Its audit expects **43 planned**, **38 scored**, **five skipped** (`D5,D6,D8,G5,G6`), **28 displayed**, and six finalists; these counts are *provisional until execution*. `artifacts/prd_v3_7/` receives a full ledger, fold results, display-ID mapping, original and pruned trees, finalist OOF, outcome analyses and run metadata. Reconfirm independently that all accepted sequential stages are visible. Do not claim a result before the run is verified.

After successful execution and audit, update README/AGENTS/PRD status with **verified actual** scores, finalist choices and evidence, and only then consider merging PR #17. The reserved sample is historically reused and must never be described as pristine. Avoid overwriting `artifacts/prd_v3_4/`, `artifacts/prd_v3_5/`, `artifacts/prd_v3_6/`, or archived notebooks. Avoid moving goalposts: no new hypotheses or extra experiments without a concrete defect or user authorisation.
