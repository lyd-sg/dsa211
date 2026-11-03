# DSA211 — Predicting Online Purchases

## Current version: PRD v3.5

**Open the current project:** [PRD v3.5](PRD_v3.5.md) · [executed presentation notebook](online_shoppers_prd_v3_5.ipynb) · [presentation audit — PASS](artifacts/prd_v3_5/presentation_audit.json).

**Status (3 November 2026):** v3.5 is an editorial, EDA-grounded presentation of the successfully executed and independently verified v3.4 modelling results. **No new model was trained for v3.5.** **Merged into `main` via [PR #15](https://github.com/lyd-sg/dsa211/pull/15)**; the original review branch remains for provenance.

### What the notebook shows

- **Logistic Regression:** 7 selected experiments (L0, L1, L4, L7, L8, L13, L14). Retained L1.
- **LDA:** 7 (D0, D1, D4, D9, D10, D11, D15). Retained D0; its reason is simply **Baseline**.
- **Gaussian NB:** 7 (G0, G1, G2, G3, G6, G7, G8). Retained G7; G6 also qualified independently.
- **Bernoulli NB:** all 5 (B0–B4). Retained B3.
- **Classification trees:** full versus pruned Gini and Entropy comparisons.
- **Lecture 8/9 techniques:** explained alongside the relevant iterations (D15; L4/L13/L14), not in a separate methods matrix.

**All used supplementary EDA is now integrated into the main EDA sections:** zero/positive activity and intensity, VisitorType×Month support, rare categories, SpecialDay, predictor availability, correlations, marginal empirical logits and long-tail plots. The six EDA investigations' original saved outputs are retained, alongside the original figures. Each family table reports only numerical results; individual modification rationales and outcomes appear underneath. The selected pruned Entropy tree plot now sits in the tree section, before final winner selection.

These are **26 displayed original-family trials**, not a fresh 26-model search. All 41 original-family trials, 51 scored designs, 255 fold scores, 37 decisions, nested stepwise paths and complete tree pruning evidence remain in the frozen [v3.4 artifacts](artifacts/prd_v3_4/).

### Verified model and statistical limitations

The retained winner is **L1 Logistic Regression**, mean five-fold training ROC-AUC **0.75747** and mean AP **0.33623**. The historically reused reserved-set ROC-AUC is **0.74054**, AP **0.32720**. The reserved observations were inspected in earlier versions; this is **not** a pristine holdout. The original improvement > challenger-SE rule is a conservative heuristic, not a significance test. The hypothetical contact-cost threshold does not establish upsell causality or deployment-ready profitability.

### Reproducibility

The current notebook includes **all seven original figures and three original supplementary EDA figures**, with v3.4-computed model results and previously executed training-only supplementary EDA outputs. A presentation-only audit checks every visible curated trial against the frozen full trial ledger, the four tree rows, all original embedded figures and unchanged modelling code **without rerunning models**:

```bash
python -m pip install nbformat==5.10.4
python scripts/verify_prd_v3_5_presentation.py
```

The automated audit runs in [the active v3.5 workflow](.github/workflows/verify-prd-v3-5.yml). The frozen computation is archived byte-for-byte at [v3.4 notebook](archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb), with [independent training PASS](artifacts/prd_v3_4/independent_training_audit.json).

### Repository organisation

| Location | Purpose |
|---|---|
| [PRD_v3.5.md](PRD_v3.5.md) | Current requirements |
| [online_shoppers_prd_v3_5.ipynb](online_shoppers_prd_v3_5.ipynb) | Current readable notebook, with saved outputs |
| [artifacts/prd_v3_5/](artifacts/prd_v3_5/) | Non-training presentation verification |
| [artifacts/prd_v3_4/](artifacts/prd_v3_4/) | **Frozen authoritative** modelling evidence |
| [archive/versions/](archive/versions/) | Retired v3.0–v3.4 notebooks and PRDs, indexed by version |
| [archive/workflows/](archive/workflows/) | Disabled historical CI definitions; not active GitHub Actions workflows |
| [archive/legacy/](archive/legacy/) | Early superseded working notebook |
| [docs/](docs/) | Prior technical notes and reviews (historical; see its index) |
| [data/uci_468.csv](data/uci_468.csv) | Original source dataset |

**Preservation policy:** Older notebooks, PRDs, scripts and workflows are relocated, not deleted from repository history or rewritten to change their conclusions. Versioned evidence folders remain under `artifacts/` because the frozen audit and current notebook reference those exact paths. For historical material, use the [archive index](archive/README.md), not legacy root paths.

