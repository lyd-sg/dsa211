# DSA211 — Predicting Online Purchases

## v3.7 development candidate — numerical execution pending

**v3.7 entry points:** [Requirements](PRD_v3.7.md) · [v3.7 notebook](online_shoppers_prd_v3_7.ipynb) · [verification script](scripts/run_verify_prd_v3_7.py) · [draft review PR #17](https://github.com/lyd-sg/dsa211/pull/17).

**Important:** This feature branch contains the **constructed but not yet independently verified** v3.7 notebook. The notebook's saved execution outputs were cleared before re-execution; do **not** cite or reuse previous v3.6 model outputs as if they were v3.7 results. The current verified version on `main` remains [v3.5](https://github.com/lyd-sg/dsa211/blob/main/README.md); its findings follow the older v3.4 computation and selection policy.

### What v3.7 changes

- **Built from earlier versions, not from scratch:** Computational structure, split, fold indices, 1-SE selection implementation, tree pruning, downstream metrics and audit inherited from [executed v3.6](online_shoppers_prd_v3_6.ipynb).
- **Restore v3.5's EDA/presentation:** Zero versus positive activity and positive intensity, VisitorType × Month support, rare nominal levels, SpecialDay, prediction-time feature availability, class correlations, long tails, empirical logits, and EDA-to-experiment bridge.
- **Exactly two new experiments:** Bernoulli **B5** (fold-median composite product-engagement indicator) and **B6** (fold-fitted rare Browser/TrafficType level pooling). They must be scored before the new winner can be stated.
- **Four readable tables, seven rows each:** Consecutive **presentation labels** `L0–L6`, `D0–D6`, `G0–G6`, `B0–B6`, while original experiment IDs and all intermediate incumbent/selection decisions remain available in audit evidence.
- **Clean table columns:** Model, CV ROC-AUC, AUC SE, CV AP, ΔAUC against the actual incumbent, complexity, and retained after iteration. Hidden/scored and skipped attempts are excluded from main tables, not deleted from the audit.
- **Tree section:** Four full-versus-pruned Gini/Entropy rows, with the selected Entropy tree diagram directly after this comparison and before the six-way ranking.
- **Course references:** Fold-safe feature engineering and CV; binary NB likelihoods; combined/dropped/trimmed predictors; nonlinear transformations and the penalised Logistic / grouped backward LDA course adaptations.

**Expected trial accounting, conditional on successful execution:** 43 planned original-family attempts; 38 scored; five inapplicable historical attempts; **28 displayed** across four classifier tables, ten other scored attempts retained only in the audit. Plus two independent tree-pruning pathways and their separate four-row full/pruned comparison. **These counts are requirements, not execution results.**

### Methodology and reporting boundaries

Selection is **sequential within each family**. At every iteration, take the higher of the incumbent/challenger mean five-fold ROC-AUC values, subtract **that best model's fold AUC SE**, and choose the simplest model still above the cutoff. A tie in complexity favours higher AUC, then the incumbent. Inner regularisation strength also uses the one-SE principle. The overall six-way comparison uses highest mean five-fold training ROC-AUC, with AP as supporting minority-class ranking information.

Use the original **12,330 sessions**, seed-42 stratified **9,864/2,466** training/reserved split, the same five outer training folds, and 16 operational inputs (excluding `PageValues` because its decision-time availability has not been verified). The reserved observations were historically inspected; they are **not a pristine independent test**. The project is prediction-only and makes no causal claim.

### Execution and verification

From the repository root, in a Python environment with `requirements.txt` installed:

```bash
python scripts/run_verify_prd_v3_7.py --run
```

This parses every source cell, executes the entire notebook from top to bottom, checks the full sequential ledger, all 28 canonical-to-presentation aliases, five skipped entries, two new Bernoulli trials, the six finalists, and the output files, then writes `artifacts/prd_v3_7/v3_7_verification.json` **only on PASS**. The development-branch workflow [.github/workflows/verify-prd-v3-7.yml](.github/workflows/verify-prd-v3-7.yml) is intended to perform this check and commit the executed notebook and new v3.7 evidence.

**Do not label v3.7 verified, merge the draft PR, publish winning AUC/AP or claim a pristine test result until the audit file exists and reports PASS.**

### Evidence and preservation

| Location | Purpose |
|---|---|
| [PRD_v3.7.md](PRD_v3.7.md) | New specification and frozen acceptance criteria |
| [online_shoppers_prd_v3_7.ipynb](online_shoppers_prd_v3_7.ipynb) | New constructed notebook; awaiting executed outputs |
| [scripts/run_verify_prd_v3_7.py](scripts/run_verify_prd_v3_7.py) | Full run plus independent lineage/alias verification |
| `artifacts/prd_v3_7/` | Version-isolated evidence and audit **after execution** |
| [PRD_v3.6.md](PRD_v3.6.md), [online_shoppers_prd_v3_6.ipynb](online_shoppers_prd_v3_6.ipynb) | Corrected sequential model-selection predecessor |
| [PRD_v3.5.md](PRD_v3.5.md) | Prior presentation contract |
| [artifacts/prd_v3_4/](artifacts/prd_v3_4/) | Historical v3.4 model outputs; never silently treated as updated v3.7 predictions |
| [archive/versions/](archive/versions/) | Earlier archived source and evidence |
| [data/uci_468.csv](data/uci_468.csv) | Original fixed input data |

Previous notebooks, historical results and original artefacts are intentionally preserved. Once v3.7 passes execution and is selected as the repository's current version, replace this provisional status with **actual** verified winner, scores, audit hash and reproducible run instructions.
