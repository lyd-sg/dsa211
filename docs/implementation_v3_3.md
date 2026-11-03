# PRD v3.3 — implementation and verification plan

**Frozen design:** [PRD v3.3](../archive/versions/v3.3/PRD_v3.3.md). **Notebook:** [v3.3](../archive/versions/v3.3/online_shoppers_prd_v3_3.ipynb). **Branch:** `analysis/prd-v3-3-notebook`.

## Historical-source contract

The v3.3 notebook was copied from the **executed** v3.2 notebook, but its v3.3 code-cell outputs were cleared before the new execution. Existing PRDs, v3.0/v3.1/v3.2 executed notebooks and results, supplementary EDA, data and historical attempts are preserved.

The previous 20 original-model entries and 11 v3.2 anchored trials are **recomputed on the same source, split, preprocessing and folds** and logged before the additional seven v3.3 trials; old historical outcomes are not deleted. The v3.3 source uses the same one-SE challenger acceptance criterion and independently pruned trees, and writes new evidence solely under `artifacts/prd_v3_3/`.

## Exactly seven new model candidates

- **L8:** In place of numeric BounceRates, three fixed features: positive indicator, clipped lower linear segment `min(x,0.01)` and upper hinge `max(x-0.01,0)`.
- **L9:** Fold-fitted nominal SpecialDay one-hot representation, dropping one reference category.
- **L10:** Add `ProductRelated_Duration / ProductRelated` with zero count mapped to exact zero, and retain both original activity signals.
- **D8:** Only `ProductRelated` changes to `log1p`.
- **D9:** Only `ProductRelated_Duration` is capped above the **99th percentile of the fit-fold training values**. This cutoff is learned independently in each fold.
- **D10:** Add `1[Informational>0]`; retain original magnitude.
- **D11:** Replace numeric BounceRates with a fold-fitted nominal three-level category: exactly zero, positive ≤0.01 and >0.01. The numeric cutoff is fixed before execution.

For each: reuse the **frozen v3.2 family finalist** as its anchor, compute mean five-fold AUC and AP and fold SD/SE, accept only if gain exceeds challenger SE, and choose the highest qualified new contender within the family. Do not combine independent new probes. No additional new changes may be introduced based on results.

## Expected evidence

Full execution and acceptance checks must verify:

1. 37 notebook cells and 20 Python cells, compilable and fully executed with no error outputs.
2. 38 logged original-family entries (20 v3.1 + 11 v3.2 + **7 v3.3**); 48 audited specification scores and 240 specification-fold scores; 34 verified decisions.
3. Exact v3.3 anchors, seven candidate labels and parameters, unchanged one-SE selection and best-qualifying family finalists; the old 11 v3.2 anchors and decisions remain independently checked.
4. Both full Gini/Entropy pruning paths with 5-fold alpha scores, simplest eligible selected trees, direct six-way competition, all four threshold references, finite parameters and OOF validity.
5. One selected-winner reserved-set check **after training selection**, with the historical prior-use warning, and unchanged all-data refit.
6. `artifacts/prd_v3_3/independent_training_audit.json` reports `status=PASS`; `run_metadata.json` reports `prd=v3.3`; executed notebook and results are committed on the branch after successful CI.

The repeated folds and prior reserved-set exposures make v3.3 exploratory. Neither the strict one-SE heuristic nor a large marginal EDA effect establishes significance or real economic impact.
