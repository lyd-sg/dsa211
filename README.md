# DSA211 — Predicting Online Purchases (PRD v3.3 exploratory extension)

**Active requirements:** [PRD v3.3](PRD_v3.3.md) · **Notebook:** [online_shoppers_prd_v3_3.ipynb](online_shoppers_prd_v3_3.ipynb) · **Execution verification:** [.github/workflows/build-prd-v3-3.yml](.github/workflows/build-prd-v3-3.yml).

## Experiment scope

**All seven newly proposed EDA-motivated specifications are included**, not only the four initially prioritised:

| Family | New tests |
|---|---|
| Logistic Regression | **L8** fixed 0.01-knot piecewise BounceRates; **L9** categorical SpecialDay; **L10** product-page average duration ratio |
| LDA | **D8** log1p ProductRelated; **D9** fold-training-p99 winsorised ProductRelated_Duration; **D10** Informational positive indicator; **D11** 3-category BounceRates |
| Gaussian NB, Bernoulli NB | Existing v3.2 retained finalists, no new tests |
| Gini and Entropy trees | Existing independent full pruning paths, no new changes |

All seven are **independent one-change probes** against the frozen **v3.2** family finalist (L1 Logit or D0 LDA). Their motivation comes from training-only main/supplementary EDA; they are empirical hypotheses, not promises of improved AUC or assumption satisfaction. The fixed one-SE qualification rule and six-way overall mean five-fold training ROC-AUC selection remain unchanged.

Historical evidence is preserved: 20 v3.1 original pathway records, 11 v3.2 anchored experiments, and seven v3.3 trials, for **38 original-family attempt rows**. The independent audit expects **48 evaluated specification results and 240 fold scores**, **34 decisions**, two independently pruned trees and six finalists. New outputs are saved under `artifacts/prd_v3_3/` only.

## Execution and acceptance

The CI workflow must execute and verify the notebook **before** any new v3.3 metrics or final selection are claimed. Results should be reported only after an actual passing run, an executed notebook with cell outputs and a `status=PASS` independent training audit.

Reproduce on Python 3.12 using pinned dependencies:

```bash
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  jupyter nbconvert --to notebook --execute online_shoppers_prd_v3_3.ipynb \
  --ExecutePreprocessor.timeout=7200 --output online_shoppers_prd_v3_3_executed.ipynb
```

The workflow commits the executed notebook and isolated v3.3 evidence after passing all audits; do not confuse historical saved results with new outputs.

## Scope, interpretation and historical preservation

Predict `Revenue=1` only; do not interpret probabilities as causal upsell effects or validated profit. The dataset has 12,330 sessions, including 125 excess duplicate rows. Six operational classifiers use 16 sources, excluding PageValues as a timing precaution (not proven leakage), on the original seed-42 80/20 split and shared five stratified training CV folds. All transformation statistics are fitted inside each training fold. The original 20% reserved set has been examined in previous project versions; v3.3 is exploratory and cannot provide newly pristine independent testing.

The six-way competition includes four selected original families plus both independently cost-complexity-pruned trees, ranked by mean CV ROC-AUC. AP, OOF/ROC/PR, threshold curves, the fixed hypothetical S$3/S$12 decision-cost cutoff and cost sensitivity remain supporting analyses.

**Historical sources, unchanged:** [v3.2 PRD](PRD_v3.2.md), [executed v3.2 notebook](online_shoppers_prd_v3_2.ipynb), [v3.2 evidence](artifacts/prd_v3_2/), [supplementary training EDA](supplementary/training_eda.ipynb), [v3.1 PRD](PRD_v3.1.md), [v3.1 notebook](online_shoppers_prd_v3_1.ipynb) and [v3.0 notebook](online_shoppers_prd_v3.ipynb). Current verified v3.2 winner: L1 Logit mean training CV AUC approximately 0.75747. This is **historical v3.2 evidence**, not v3.3 outcome evidence.
