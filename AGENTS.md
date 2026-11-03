# DSA211 active implementation guidance — PRD v3.3

**Current branch:** `analysis/prd-v3-3-notebook`.  
**Active source of truth:** [PRD v3.3](PRD_v3.3.md) and [v3.3 implementation notes](docs/implementation_v3_3.md).  
**Notebook:** [online_shoppers_prd_v3_3.ipynb](online_shoppers_prd_v3_3.ipynb).  
**Acceptance CI:** [.github/workflows/build-prd-v3-3.yml](.github/workflows/build-prd-v3-3.yml).

## Model research and experiment rules

- Prediction-only `Revenue=1`; use taught Logit, LDA, Gaussian NB, Bernoulli NB, and full-grown/pruned Gini and Entropy trees. Do not broaden to untaught classifiers or claim causal effects.
- Original dataset, 12,330 rows (125 excess exact duplicates retained), seed-42 80/20 split (training 9,864/reserved 2,466), five common stratified CV folds. Fold-safe training-only numeric percentile, one-hot encoding and hyperparameter selection.
- Baselines and 16 operational source variables unchanged. Exclude PageValues from operational candidates due to timing uncertainty rather than a proved leakage diagnosis; six all-17 timing diagnostics separately retained.
- Record and retain all **20 v3.1 entries, 11 v3.2 probes and SEVEN v3.3 probes**. Do not delete rejected trials; v3.3 inventory is **38 rows**, with **48 scored specifications** and **240 fold scores** before tree-alpha CV expansion.
- Seven mandatory one-change new probes are **L8, L9, L10, D8, D9, D10, D11**, as frozen in [PRD v3.3](PRD_v3.3.md). Every one is independently compared against the **v3.2** retained finalist of its own family, not combined cumulatively.
- Same `mean CV AUC gain > challenger five-fold AUC SE` qualification. Select highest mean AUC among qualified new probes within a family, else retain frozen v3.2 incumbent. No modifications post-execution to manufacture an LDA winner; failure to improve is an informative result.
- Both pruned trees enter a six-way comparison with updated four-family finalists; highest **mean** five-fold ROC-AUC wins; AP/OOF/thresholds are secondary.
- All outputs for v3.3 go under `artifacts/prd_v3_3/`, while older PRDs/notebooks/artifacts and source are immutable. The new notebook must be actually executed; only after the full independent audit reports PASS are new results considered complete.
- Prior historical holdout examination and repeated training CV folds limit claims of independent validation. The hypothetical fixed S$3/S$12 cost ratio, threshold 0.2 and 20/30/40% q scenarios do not measure real upsell effects.
- Do not automatically merge v3.3 into v3.2 or main without review. The user's request was to test **all seven**, not select four.
