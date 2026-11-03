# DSA211 repository guidance — v3.2 exploratory modelling branch

**Authoritative active requirements on this branch:** [PRD v3.2](PRD_v3.2.md).  
**Source notebook:** [online_shoppers_prd_v3_2.ipynb](online_shoppers_prd_v3_2.ipynb).  
**Execution and independent audit:** [.github/workflows/build-prd-v3-2.yml](.github/workflows/build-prd-v3-2.yml).  
**Interpretation/implementation notes:** [docs/implementation_v3_2.md](docs/implementation_v3_2.md).  
**Preserved historical authority:** [PRD v3.1](PRD_v3.1.md), [v3.1 notebook](online_shoppers_prd_v3_1.ipynb) and [executed v3.1 evidence](artifacts/prd_v3_1/); [v3.0 notebook](online_shoppers_prd_v3.ipynb) and [v3.0 evidence](artifacts/prd_v3/) also remain unchanged.

## Modelling boundary

Prediction of session Revenue=1 using existing taught Logistic Regression, LDA, Gaussian NB, Bernoulli NB, and independently cost-complexity-pruned Gini/Entropy trees. No causal upsell, inference, counterfactual revenue, real-time eligibility claim or untaught new classifier. Dataset 12,330 sessions, 125 excess duplicate rows retained. Original seed-42 stratified 80/20 split and five shared stratified training folds. All learned processing fitted inside the training fold. Six all-17 models including PageValues are noncompeting timing diagnostics; operational models use the 16-source baseline excluding PageValues, except the explicit named GNB deletions.

Preserve all **20 historical** v3.1 attempt records and exact original L/D/G/B paths, including rejected outcomes, plus **11 new** L5–L7, D5–D7, G5–G9 candidates (31 total). All 11 must be evaluated, not preselected by expected gain. Bernoulli NB has no new modification.

The 11 proposals are **independent single-change challenges** against each family's frozen v3.1 retained finalist, not cumulative sequential modifications. This is necessary for G6 (remove ProductRelated_Duration) and G7 (transform ProductRelated_Duration) to both be valid tests. Each qualifies only when `meanCV_AUC(challenger)-meanCV_AUC(anchor) > challenger five-fold AUC SE`; if several qualify, choose the one with highest mean CV AUC, then step ID for exact ties; otherwise retain the original finalist. Do not adjust rule after observing output. Keep accepted qualification and selected family finalist distinct.

All six finalist specifications (four original pathways' updated selected contenders and independently pruned Gini and Entropy trees) compete on mean five-fold training ROC-AUC. AP and fold spread are supporting evidence, not alternative selection metrics. Use existing winner-only OOF ROC/PR/reliability/threshold charts. The business illustration is fixed S$3 assistance, hypothetical q=30%, S$50 margin, threshold 0.20; vary q=20/30/40% for sensitivity only.

## Version and validation guardrails

- **Do not edit v3.0/v3.1 artifacts, notebooks, PRDs, histories or original data.** All generated v3.2 output goes in `artifacts/prd_v3_2/`.
- v3.2 is exploratory because the team read v3.1 validation results before choosing new candidate types. The historical reserved set has been viewed across prior versions. Do not claim pristine out-of-sample evaluation, guaranteed calibration, a formal significance test from 1-SE, or real causal uplift.
- Do not use v3.1 reserved performance to choose new trials, thresholds, alpha, or hyperparameter grids. No additional specification beyond PRD v3.2 without explicit versioned approval.
- The v3.2 execution workflow must pass compilation, notebook execution, 31 attempt rows (20 old + 11 new), 41 CV specifications / 205 specification-fold scores, 27 acceptance comparisons, all Gini/Entropy pruning candidates, six finalists, four thresholds, numerical validity, and final evidence provenance. **An unexecuted notebook is not validated findings.**
- Work on this branch and create a reviewable pull request; never auto-merge into v3.1 or `main`.
