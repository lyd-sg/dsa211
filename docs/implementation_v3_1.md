# PRD v3.1 — implemented notebook protocol

**Requirements:** [PRD v3.1](../archive/versions/v3.1/PRD_v3.1.md) and its [requirements alignment audit](PRD_v3.1_alignment_audit.md). **Notebook:** [v3.1](../archive/versions/v3.1/online_shoppers_prd_v3_1.ipynb). **Historical reference:** [executed v3.0](../archive/versions/v3.0/online_shoppers_prd_v3.ipynb).

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

The selected winner determines the saved OOF score display, ROC/PR analyses, cost-based confusion counts, frozen training refit and one v3.1 reserved-set check. The same unchanged model recipe is then fitted on all 12,330 rows. The holdout is explicitly *not pristine across previous project versions*. The single workflow [build-prd-v3-1.yml](../archive/workflows/build-prd-v3-1.yml) executes the notebook and checks source integrity, fold and alpha ledgers, all six finalists, one-SE decisions, threshold counts, saved figures, fit evidence and version separation.

**Evidence directory:** `artifacts/prd_v3_1/`. [The complete GitHub Actions execution](https://github.com/lyd-sg/dsa211/actions/runs/41595364066) passed notebook execution, independent numerical audit, provenance, version preservation and evidence checks. Actual results come from the saved v3.1 evidence, not from historical v3.0 metrics.

**Excluded:** nested CV as a new outer estimation regime, additional model families, alternate tree hyperparameter grids, manual tree feature engineering, threshold optimisation, probability calibration and causal upsell estimates.

## Executed v3.1 outcome (3 November 2026)

- **All-17 diagnostics:** 6; **operational all-16 baselines:** 6; all-17 diagnostics excluded from tuning and finalist selection.
- **Cost-complexity candidates:** Gini 364 alphas (1,820 fold evaluations), Entropy 358 (1,790 fold evaluations), total 722 alphas / 3,610 fold evaluations. One-SE cutoff then fewest leaves then higher AUC was independently reconstructed from saved folds.
- **Gini:** baseline depth 35, leaves 1,388, CV AUC 0.576629; selected alpha 0.0010076415, depth 4, leaves 8, CV AUC 0.733055, mean AP 0.303894.
- **Entropy:** baseline depth 36, leaves 1,288, CV AUC 0.579729; selected alpha 0.0012870610, depth 6, leaves 14, CV AUC 0.744143, mean AP 0.313002.
- **Six-way winner:** L1 Logistic Regression, CV AUC 0.757467, AP 0.336226. Selected Entropy ranks second and Gini fifth; neither tree was preselected or excluded before six-way ranking.
- **Held-out check:** 2,466 rows, AUC 0.740543, AP 0.327199; final all-data refit passed. No extrapolation to previously untouched lifetime-independent test data.
- **Independent numeric audit:** PASS; 30 specification-level CV results / 150 folds, 722 candidate alphas / 3,610 folds, 16 legacy sequential decisions, four threshold references. Expected unknown-category fold-encoding warnings were saved; training and final full-data fits reported no warnings.
