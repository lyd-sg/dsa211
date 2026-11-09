# DSA211 — Predicting Online Purchases

## Active version: PRD v3.8

**Current presentation:** [v3.8 notebook](online_shoppers_prd_v3_8.ipynb) · [v3.8 PRD](PRD_v3.8.md) · [verification script](scripts/verify_prd_v3_8.py) · [active GitHub Actions workflow](.github/workflows/verify-prd-v3-8.yml).

**Verified scope:** The v3.8 EDA was re-executed successfully, and all inherited model source code and saved model outputs were checked against v3.7. **The entire v3.8 model-development pipeline has not been retrained.** Its numerical results remain grounded in the fully executed, independently verified [archived v3.7 notebook](archive/versions/v3.7/online_shoppers_prd_v3_7.ipynb) and [v3.7 PASS audit](artifacts/prd_v3_7/v3_7_verification.json).

### Changes from v3.7 to v3.8

For the full section-by-section comparison, reasoning behind each retained/removed analysis, and verification boundaries, see the **[detailed v3.7 → v3.8 change report](docs/v3.7-to-v3.8-detailed-change-report.md)**.

- **Restructured EDA:** Separated the full-dataset overview and stratified split from training-only general and in-depth EDA.
- **Condensed general EDA:** Kept the numerical skewness and zero-share table; removed two redundant histograms; merged rare-category findings into the categorical summary.
- **Streamlined in-depth EDA:** Retained zero/positive activity rates, positive-intensity and BounceRates percentile tables, four within-class correlations, Q–Q plots and an annotated SpecialDay chart.
- **Removed redundant analyses:** Dropped Month × VisitorType, standalone PageValues purchase-rate EDA, the 17-row predictor-availability table and repeated tables/plots.
- **Improved narrative:** Moved the PageValues timing assumption into Model Development; removed the standalone EDA-to-experiment bridge while retaining broader model-specific discussion.
- **Preserved results and archived v3.7:** No model specifications, selection decisions or saved scores changed; retired v3.7 files are preserved under [archive/versions/v3.7](archive/versions/v3.7/).

### Notebook structure

1. **Initial Data Overview:** Dataset, missingness, 125 excess identical records retained, target distribution and finally the stratified 80/20 split.
2. **General EDA (training only):** Numerical distribution table (no separate histograms); concise categorical distribution and rare-level findings.
3. **In-depth EDA (training only):** Zero vs positive activity, positive-only intensity, BounceRates groups, within-class correlations, Q–Q plots and SpecialDay.
4. **Model Development:** Unchanged classifier and tree specification history, sequential one-SE model selection, finalist ranking and results. Modelling rationales are discussed here rather than in EDA.

### Fixed methodology and results

- **Dataset:** 12,330 source sessions; 17 predictors. Stratified seed-42 split: 9,864 training and 2,466 historically consulted reserved observations. Operational candidates use 16 predictors, excluding `PageValues` due to uncertain decision-time availability, not confirmed leakage.
- **Evaluation:** Five shared stratified training folds with fold-fitted preprocessing and nested tuning. Within classifier families, the sequential 1-SE parsimony rule compares the actual incumbent and challenger. Six finalists are ranked by highest mean training-fold ROC-AUC.
- **Original experiment lineage:** 43 planned, 38 scored, five inapplicable, and 28 displayed aliases (seven per classifier). Four classifier finalists and two pruned-tree finalists are retained.
- **Verified historical winner:** Original L13 Logistic Regression (displayed L6); mean training CV ROC-AUC **0.75892**, mean AP **0.34236**. Reserved ROC-AUC **0.74313**, AP **0.33358**. The historically reused reserved set is **not a pristine independent test**.

### Verification

From the repository root with project Python dependencies installed:

```bash
python scripts/verify_prd_v3_8.py --run-eda
```

This checks EDA calculations and figures against the original source rows, executes only pre-modelling code, and verifies that inherited modelling code and saved outputs match the **archived** v3.7 notebook. The historical v3.7 full-run evidence is available in [artifacts/prd_v3_7/](artifacts/prd_v3_7/); the retired v3.7 verifier is preserved byte-for-byte but assumes its original root-level layout.

### Archive and evidence

The [archive version index](archive/versions/README.md) includes v3.0–v3.7. The [v3.7 notebook](archive/versions/v3.7/online_shoppers_prd_v3_7.ipynb), [PRD](archive/versions/v3.7/PRD_v3.7.md), [historical verifier](archive/versions/v3.7/run_verify_prd_v3_7.py), and [retired workflow](archive/workflows/verify-prd-v3-7.yml) retain their original Git blobs. The [retirement manifest](archive/versions/v3.7/RETIREMENT_MANIFEST.json) records their exact identifiers. All prior-version `artifacts/` remain at their existing paths.

The project is prediction-only: EDA patterns and model scores are descriptive/predictive, not causal.
