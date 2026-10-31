# DSA211 repository implementation instructions — PRD v3.0

**Authority:** [Approved PRD 3.0](docs/PRD_v3.md) → [v3 technical plan](docs/technical_plan_v3.md) → [executed v3 notebook](online_shoppers_prd_v3.ipynb). The v2 notebook, PRD, technical plan and [v2 agent instructions](docs/AGENTS_v2_archive.md) are historical and must be preserved.

## Scope
- Prediction of session Revenue only, not inference, causal intervention effects or real sales gains. Four pathways across three taught families: Logit, LDA, Gaussian NB, Bernoulli NB; no Mixed NB in active v3.
- Preserve UCI source data (12,330 sessions and retained duplicate rows), established 80/20 seed-42 split, five shared training CV folds, training-only EDA and strict fold-contained preprocessing. Four all-17 diagnostics are noncompeting; operational models use 16 original sources excluding PageValues as a timing precaution.
- Run L0–L4, D0–D4, G0–G4, B0–B4 as predeclared sequential, individually EDA-justified modifications. Every challenger compares to its *current accepted incumbent*, with the one-SE simplicity decision. Show all 20 operational attempts and their recorded fold evidence, including rejections.
- Nested inner training CV tunes C for L4 and shrinkage for D4. Preserve encoders, fold-fitted medians and rare-level category pooling inside the fitting pipeline.
- Rank four family finalists by mean five-fold ROC-AUC, with AP and SD/SE supporting context. Winner OOF ROC/PR curves and reliability checks are descriptive, not proof of calibration.
- Illustrative upsell assumptions S$3 cost, 30% success among buyers, S$50 incremental gross margin: C_FP=3, C_FN=12, cutoff 0.20. Compare training prevalence, 0.50, crossover and 0.20; q sensitivity at 20/30/40%. Never claim actual sales uplift.
- After freezing the family recipe, evaluate the v3 reserved set without further tuning and refit the unchanged model on all data. Disclose historical previous use of this held-out partition.

## Verification and delivery
- The executed notebook is [online_shoppers_prd_v3.ipynb](online_shoppers_prd_v3.ipynb), built by [scripts/build_prd_v3.py](scripts/build_prd_v3.py) and executed by [.github/workflows/build-prd-v3.yml](.github/workflows/build-prd-v3.yml).
- Save generated outputs in artifacts/prd_v3. Audit all 24 CV candidate fold metrics and mean/SD/SE, four finalists, local one-SE decisions, threshold confusion counts and finite probabilities, plus warnings and provenance.
- Keep interpretation concise, numerical, and grounded in saved results. Preserve the v2 history and source files. Work in a separate branch and request review; do not automatically merge or claim lecturer approval.
