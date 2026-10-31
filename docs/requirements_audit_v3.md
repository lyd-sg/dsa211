# PRD 3.0 — notebook requirements verification

**Source of truth:** [PRD v3](PRD_v3.md). **Deliverable:** [executed notebook](../online_shoppers_prd_v3.ipynb). **Evidence:** [versioned artifacts](../artifacts/prd_v3/). The previous PRDs, v2 notebook, data and archives are preserved. This is a technical compliance audit, not academic examiner certification.

| PRD requirement | Implementation and evidence |
|---|---|
| Prediction research objective, taught families | Notebook introduction and four pathways: Logit, LDA, GNB, BNB; no mixed NB in v3 |
| Data checks | 12,330 session rows, 17 source predictors, Revenue, 125 excess duplicates, completeness and finite-value checks |
| Split and fold discipline | 80/20 stratified, seed 42; 9,864 training and 2,466 reserved; five shared stratified training folds seed 42 |
| Training EDA and feature timing | Numerical/categorical summaries, within-class correlations and Q-Q plots; separate training EDA retained; PageValues excluded for operational prediction timing |
| Baselines | Four all-17 diagnostics and four all-16 operational baselines; nominal variables encoded without arbitrary ordinality |
| Single-change sequential paths | Four baselines + sixteen ordered trials (L1–L4, D1–D4, G1–G4, B1–B4), with revert-to-incumbent behaviour |
| Fold-contained preprocessing | Fit per-fold one-hot levels, rare pooling (minimum count 50), activity logs, positive-presence features, BNB training medians |
| Inner tuning | L4 C and D4 shrinkage selected using three stratified inner folds and fitted pipelines |
| Local one-SE revision rule | Challenger retained only if mean fold ROC-AUC gain > challenger fold AUC SE (SD uses ddof=1); parent and outcome logged |
| All attempts report | Complete attempt ledger, mean AUC/AP/SD/SE, accepted/rejected reasons and per-fold outputs |
| Finalists and winner | Four retained finalists ranked by mean five-fold CV ROC-AUC; supporting AP, ROC plots and winner score histogram/PR curve |
| Calibration qualifications | Ten-bin training OOF reliability summary; AUC/AP not presented as calibrated probability evidence |
| Upsell costs | Assumed agent cost S$3, conditional upsell success 30%, gross margin S$50, relative costs FP=S$3 and FN=S$12; theoretical cutoff 0.20 |
| Thresholds | Training prevalence, 0.5, nearest sensitivity–specificity crossover, fixed 0.2; counts, recall, specificity, precision; curves and 20/30/40% assumed upsell-rate sensitivity |
| Frozen test check | Model and threshold selected using training only, then one reserved-set check for v3. Historical prior use of the same holdout is disclosed |
| Final fit | Selected frozen recipe refitted on 9,864 training rows for numerical checks and 12,330 rows for final deployment-independent fit; no all-data score claimed as out-of-sample |
| Numerical reproducibility | Clean notebook execution, all cell outputs saved, fold-level ROC-AUC/AP/SD/SE and sequential decisions checked, threshold confusion counts independently recomputed, warnings and package versions saved |
| Limitations | Data/class imbalance, potential calibration/feature-timing issues, duplicate dependence, NB/LDA assumptions, selection optimism and no causal upsell evidence |

### Separate PRD deliverables

PRD §1 and §9 also call for **20-minute presentation slides**. Slides are a separate deliverable and are not part of a request specifically to implement the notebook. The implemented notebook does not imply that the slides have been created.

### Key result for consistency checking

Prior verified execution selected **L1 Logistic Regression** (log1p activity), with mean training CV ROC-AUC **0.75746857**, mean fold AP **0.33622631**, reserved-set ROC-AUC **0.74054250**, and reserved-set AP **0.32719856**. Model selection remained based on training CV only. These values must be reconfirmed against the final executed notebook after any reporting-only rebuild.

**Validation qualification:** Technical assertions document the implemented design and recorded execution checks, not mathematical proof that no modelling judgment is debatable or an independent professor review.
