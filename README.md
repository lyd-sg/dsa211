# DSA211 — Predicting Online Purchases

## Current presentation: PRD v3.8 (EDA verified) · Numerical baseline: v3.7 (fully verified)

**v3.8:** [New notebook](online_shoppers_prd_v3_8.ipynb) · [v3.8 PRD](PRD_v3.8.md) · [EDA/preservation verifier](scripts/verify_prd_v3_8.py) · [PASS CI run](https://github.com/lyd-sg/dsa211/actions/runs/42484250765). The new notebook reorganises EDA into concise full-data overview, general EDA and in-depth EDA; all model code and saved results are inherited unchanged. **Only EDA was re-executed for v3.8 verification, not full model retraining.**

**v3.7 computational evidence:**

**Current project entry points:** [Requirements](PRD_v3.7.md) · [v3.7 notebook](online_shoppers_prd_v3_7.ipynb) · [verification script](scripts/run_verify_prd_v3_7.py) · [merged PR #17](https://github.com/lyd-sg/dsa211/pull/17).

**Verification (5 November 2026): PASS.** All 31 code cells executed without errors. [Independent numerical verification](artifacts/prd_v3_7/v3_7_verification.json) confirms all 43 planned trials, 38 scored, 5 inapplicable, 28 displayed aliases, 34 sequential decisions and 240 fold records. This executed v3.7 notebook is the current analysis on `main`.

### What v3.7 changes

- **Built from earlier versions, not from scratch:** Computational structure, split, fold indices, 1-SE selection implementation, tree pruning, downstream metrics and audit inherited from [archived executed v3.6](archive/versions/v3.6/online_shoppers_prd_v3_6.ipynb).
- **Restore v3.5's EDA/presentation:** Zero versus positive activity and positive intensity, VisitorType × Month support, rare nominal levels, SpecialDay, prediction-time feature availability, class correlations, long tails, empirical logits, and EDA-to-experiment bridge.
- **Exactly two new experiments:** Bernoulli **B5** (fold-median composite product-engagement indicator) and **B6** (fold-fitted rare Browser/TrafficType level pooling), both scored and audited.
- **Four readable tables, seven rows each:** Consecutive **presentation labels** `L0–L6`, `D0–D6`, `G0–G6`, `B0–B6`, while original experiment IDs and all intermediate incumbent/selection decisions remain available in audit evidence.
- **Clean table columns:** Model, CV ROC-AUC, AUC SE, CV AP, ΔAUC against the actual incumbent, complexity, and retained after iteration. Hidden/scored and skipped attempts are excluded from main tables, not deleted from the audit.
- **Tree section:** Four full-versus-pruned Gini/Entropy rows, with the selected Entropy tree diagram directly after this comparison and before the six-way ranking.
- **Course references:** Fold-safe feature engineering and CV; binary NB likelihoods; combined/dropped/trimmed predictors; nonlinear transformations and the penalised Logistic / grouped backward LDA course adaptations.

**Verified trial accounting:** 43 planned original-family attempts; **38 scored**, **five inapplicable** historical attempts, **28 displayed** (7 per classifier), and ten additional scored attempts retained in audit evidence. Tree pruning was independently verified over 722 alpha candidates and 3,610 tree fold scores.

### Methodology and reporting boundaries

Selection is **sequential within each family**. At every iteration, take the higher of the incumbent/challenger mean five-fold ROC-AUC values, subtract **that best model's fold AUC SE**, and choose the simplest model still above the cutoff. A tie in complexity favours higher AUC, then the incumbent. Inner regularisation strength also uses the one-SE principle. The overall six-way comparison uses highest mean five-fold training ROC-AUC, with AP as supporting minority-class ranking information.

Use the original **12,330 sessions**, seed-42 stratified **9,864/2,466** training/reserved split, the same five outer training folds, and 16 operational inputs (excluding `PageValues` because its decision-time availability has not been verified). The reserved observations were historically inspected; they are **not a pristine independent test**. The project is prediction-only and makes no causal claim.

### Execution and verification

From the repository root, in a Python environment with `requirements.txt` installed:

```bash
python scripts/run_verify_prd_v3_7.py --run
```

This parses every source cell, executes the entire notebook from top to bottom, checks the full sequential ledger, all 28 canonical-to-presentation aliases, five skipped entries, two new Bernoulli trials, the six finalists, and the output files, then writes `artifacts/prd_v3_7/v3_7_verification.json` **only on PASS**. The initial [v3.7 verification workflow](.github/workflows/verify-prd-v3-7.yml) produced the executed notebook and versioned evidence; its maintained main-branch configuration checks the saved results without refitting models.

**Verified six-way winner:** Original trial **L13 Logistic Regression** (displayed as **L5** in the curated table), training CV mean ROC-AUC **0.75892** and mean AP **0.34236**. Runner-up: pruned Entropy tree, ROC-AUC **0.74414**. New Bernoulli NB B5 and B6 were **both retained for simplicity**; Bernoulli finalist B6 has mean AUC **0.73953** and AP **0.30574**. The historically consulted reserved sample scored AUC **0.74313** and AP **0.33358**, and **is not a pristine independent test**. These are descriptive, not causal or calibrated-probability claims.

### Evidence and preservation

| Location | Purpose |
|---|---|
| [PRD_v3.7.md](PRD_v3.7.md) | New specification and frozen acceptance criteria |
| [online_shoppers_prd_v3_7.ipynb](online_shoppers_prd_v3_7.ipynb) | **Executed and verified** notebook, with saved outputs |
| [scripts/run_verify_prd_v3_7.py](scripts/run_verify_prd_v3_7.py) | Full run plus independent lineage/alias verification |
| [artifacts/prd_v3_7/](artifacts/prd_v3_7/) | Version-isolated results, fold-level evidence, lineage and **PASS** audit |
| [v3.6 PRD](archive/versions/v3.6/PRD_v3.6.md), [v3.6 notebook](archive/versions/v3.6/online_shoppers_prd_v3_6.ipynb) | Archived corrected sequential model-selection predecessor |
| [v3.5 PRD](archive/versions/v3.5/PRD_v3.5.md), [v3.5 notebook](archive/versions/v3.5/online_shoppers_prd_v3_5.ipynb) | Archived EDA-oriented presentation predecessor |
| [artifacts/prd_v3_4/](artifacts/prd_v3_4/) | Historical v3.4 model outputs; never silently treated as updated v3.7 predictions |
| [archive/versions/](archive/versions/) | Read-only index of v3.0–v3.6 notebooks, PRDs, version scripts and historical references |
| [data/uci_468.csv](data/uci_468.csv) | Original fixed input data |

Previous notebooks, historical results and original artefacts remain preserved. The executed v3.7 evidence is verified in [v3_7_verification.json](artifacts/prd_v3_7/v3_7_verification.json); use this notebook as the current analysis rather than the superseded v3.5 results.
