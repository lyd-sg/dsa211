# PRD v3.1 — implemented notebook protocol

**Requirements:** [PRD v3.1](../PRD_v3.1.md) and its [requirements alignment audit](PRD_v3.1_alignment_audit.md). **Notebook:** [v3.1](../online_shoppers_prd_v3_1.ipynb). **Historical reference:** [executed v3.0](../online_shoppers_prd_v3.ipynb).

## Minimal-change boundary

The new notebook directly copies the executed v3.0 cells, preserving the established EDA, source-quality checks, 80/20 seed-42 split, five shuffled stratified training folds, original four feature-engineering configurations and 20 sequential attempts. Only sections requiring new tree models, six-way selection, dependent plots and finalisation checks were extended. `scripts/build_prd_v3.py`, the v3.0 notebook, v3.0 evidence, data and archived requirements are unchanged.

## Tree extension

- Six all-17 timing diagnostics: the four pre-existing classifier configurations and full-grown Gini/Entropy trees. All are noncompeting.
- Six all-16 operational baselines: original four plus Gini/Entropy full-grown trees, fixed `random_state=42`, `ccp_alpha=0`, `max_depth=None`, `min_samples_leaf=1`, `min_samples_split=2`, `class_weight=None`.
- Each tree uses the original fold-safe feature transformer with full one-hot nominal indicators, unchanged numeric source features and no scaling. The six nominal source variables are not treated as ordinal.
- Generate each distinct `ccp_alpha` from its own full-training 16-source cost-complexity path, including zero and excluding the terminal root-only penalty. No all-17 score participates in pruning.
- Evaluate every alpha using the five shared stratified folds and `predict_proba` to obtain mean ROC-AUC and AP, sample ROC-AUC SD and SE. To minimise repeated encoding, each fold's encoder is fitted once to its fold-training subset and its encoded data are reused across penalties.
- For each criterion independently, find the highest mean AUC and subtract its SE. Restrict to candidates above that cutoff, then minimise full-training leaf count, then maximise mean CV AUC among equal-leaf candidates. An exact tie on leaves and mean AUC is resolved by the lower alpha. Preserve unpruned alpha zero when selected.
- Rank all six final specifications directly using mean training CV ROC-AUC; AP is secondary. Reuse existing four training OOF threshold references, the S$3 / S$12 hypothetical costs and q sensitivity.

## Finalisation and verification

The selected winner determines the saved OOF score display, ROC/PR analyses, cost-based confusion counts, frozen training refit and one v3.1 reserved-set check. The same unchanged model recipe is then fitted on all 12,330 rows. The holdout is explicitly *not pristine across previous project versions*. The single workflow [build-prd-v3-1.yml](../.github/workflows/build-prd-v3-1.yml) executes the notebook and checks source integrity, fold and alpha ledgers, all six finalists, one-SE decisions, threshold counts, saved figures, fit evidence and version separation.

**Evidence directory:** `artifacts/prd_v3_1/`. Results and execution status must be taken from the actual workflow and its committed outputs; this protocol document does not assert that any unexecuted candidate has passed.

**Excluded:** nested CV as a new outer estimation regime, additional model families, alternate tree hyperparameter grids, manual tree feature engineering, threshold optimisation, probability calibration and causal upsell estimates.
