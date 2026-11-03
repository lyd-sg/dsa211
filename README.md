# DSA211 — Predicting Online Purchases (PRD v3.4)

**Current scope:** [PRD v3.4](PRD_v3.4.md) · **New notebook:** [online_shoppers_prd_v3_4.ipynb](online_shoppers_prd_v3_4.ipynb) · **Execution and independent audit:** [build-prd-v3-4.yml](.github/workflows/build-prd-v3-4.yml) · [implementation and evaluation notes](docs/implementation_v3_4.md).

**Status:** The new v3.4 source is implemented on a separate branch; **v3.4 performance claims require a fully executed notebook, independent audit PASS and versioned saved evidence**.

## This is an extension, not a replacement

v3.4 inherits the entire executed v3.3 notebook and the existing EDA, source data, split, CV folds, preprocessing, model diagnostics, six-way comparison, independent tree pruning, threshold illustrations, and full refit. All older notebooks, PRDs and artifact folders remain unchanged.

### Model-family-grouped development, as requested

The new notebook renders one **full chronological historical table per classifier**, rather than a single mixed table:

| Section | Original and new trials | Retained v3.3 model |
|---|---|---|
| **7.1 Logistic Regression** | L0–L10, **L13** LASSO, **L14** Elastic Net | L1 |
| **7.2 LDA** | D0–D11, **D15** backward source selection | D0 |
| **7.3 GaussianNB** | G0–G9, no v3.4 modifications | G7 |
| **7.4 BernoulliNB** | B0–B4, no v3.4 modifications | B3 |
| **7B Classification trees** | Independently selected Gini and Entropy pruning paths, unchanged | Earlier two selected trees |

All **41** original-family attempts are tracked, including rejected proposals. New probes are labelled separately from the historical v3.1 sequential development and the independent anchored v3.2/v3.3 probes. Unused candidate IDs are intentionally skipped.

### Three exactly scoped new tests

**L13**: L1 logistic with six existing log1p activity transformations, fold-safe standardisation, L1 LASSO penalty, six-value `C` grid, nested three-fold penalty tuning.

**L14**: Elastic Net logistic with fixed `l1_ratio=0.5`, the same fold-safe transformation and penalty grid. Compare sequentially to the latest accepted Logistic Regression, L1 or L13, **replacing** rather than stacking the penalty.

**D15**: Backward LDA selection, deleting one of the 16 original source predictor groups at a time (categorical groups kept intact), using inner three-fold ROC-AUC to construct the source deletion path and the syllabus's within-one-SE simplicity rule to choose subset size. Test the full selection procedure only in the five outer validation folds.

Every v3.4 candidate is accepted **only if its mean outer CV AUC gain exceeds its own outer AUC SE**, the original project's conservative heuristic. No accepted new candidate is required for completion.

### Execution acceptance

The current workflow must verify the full executed notebook with no errors, **41 family-trial records, 51 scored model specifications, 255 fold results, 37 original-family decisions,** the selected regularisation grids and nonzero coefficients, five 16-to-1 backward-selection paths, both tree pruning paths, four threshold references and one historically reused holdout check. New evidence goes under **`artifacts/prd_v3_4/`** only.

Our training folds and the already-examined reserved set have been reused across multiple explorations. Comparisons remain exploratory and are not newly independent test evidence. The project is prediction-focused, not causal inference or validated upsell economics.

### Historical files, preserved

- [v3.3 PRD](PRD_v3.3.md), [executed v3.3 notebook](online_shoppers_prd_v3_3.ipynb), [verified v3.3 results](docs/results_v3_3.md)
- [v3.2 PRD](PRD_v3.2.md), [executed v3.2 notebook](online_shoppers_prd_v3_2.ipynb)
- [v3.1 PRD](PRD_v3.1.md), [v3.1 notebook](online_shoppers_prd_v3_1.ipynb)
- [v3.0 notebook](online_shoppers_prd_v3.ipynb)
