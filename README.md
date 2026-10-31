# DSA211 — Predicting Online Purchases (PRD v3.0)

**Current authority:** [Approved PRD v3.0](docs/PRD_v3.md) and [implemented technical plan](docs/technical_plan_v3.md).

**Research question:** How effectively can session characteristics predict `Revenue=1`, and which of the taught classification specifications produces the highest mean five-fold training ROC-AUC? This remains a **prediction** project, not coefficient inference, causal uplift analysis or a deployment claim.

## Current notebook and results

- **[Executed PRD v3 notebook](online_shoppers_prd_v3.ipynb)** — directly reusable v2 EDA and baselines; four sequential model pathways; complete attempted-specification ledger; four finalists and winner; ROC/PR and score displays; sensitivity/specificity and the hypothetical S$3/S$12 cost threshold.
- **[Supporting evidence](artifacts/prd_v3/)** — 20 attempted operational specifications, fold scores, finalist OOF probabilities, 0.20 cost-cutoff comparisons, sensitivity scenarios, one reserved-set check, warning logs and audit metadata.
- **[PRD v3 requirements audit](docs/requirements_audit_v3.md)** and [build source](scripts/build_prd_v3.py); [supplementary training EDA](supplementary/training_eda.ipynb).

The current selected specification is **L1 Logistic Regression** with `log1p` activity magnitudes, mean five-fold CV ROC-AUC **0.757469** and mean AP **0.336226**. The reserved-set check reports ROC-AUC **0.740543**, AP **0.327199**, with mandatory disclosure that the same reserved rows were examined in historical versions.

## Reproduce the full executed notebook

From the repository root with Python 3.12:

```bash
python -m pip install -r requirements.txt
python -m pip install 'nbformat>=5' 'nbconvert>=7' 'nbclient>=0.10'
python scripts/build_prd_v3.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  jupyter nbconvert --to notebook --execute online_shoppers_prd_v3.ipynb \
  --ExecutePreprocessor.timeout=3000 --output online_shoppers_prd_v3_executed.ipynb
```

The [GitHub Actions workflow](.github/workflows/build-prd-v3.yml) executes and validates the notebook, then commits the executed `.ipynb` and v3 evidence on the development branch. The builder **replaces cell outputs** with fresh results before execution; do not run it just to view the saved output.

## Boundaries and historical preservation

The dataset contains 12,330 browsing sessions and 125 excess exact duplicate rows. Operational models use 16 original predictors, excluding `PageValues` due to uncertain prediction-time availability; this does **not** prove leakage. The upsell illustration assumes S$3 agent assistance cost, 30% conditional success among actual buyers and S$50 incremental gross margin; the **0.20** threshold does **not** show true intervention uplift or necessarily calibrated probabilities. A separate **20-minute slide presentation** remains a different project deliverable.

The original [v2 notebook](online_shoppers_revised.ipynb), [v2 PRD](docs/PRD_v2.md), [v2 technical plan](docs/technical_plan.md), [v2 README snapshot](docs/README_v2_archive.md), [v2 agent instructions](docs/AGENTS_v2_archive.md) and historical artifacts remain available for provenance. The current notebook does not mix old v2 comparisons with v3 findings.
