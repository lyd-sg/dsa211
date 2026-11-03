# DSA211 — Predicting Online Purchases (PRD v3.1 implementation)

**Canonical requirements:** [PRD v3.1](PRD_v3.1.md). **New notebook:** [online_shoppers_prd_v3_1.ipynb](online_shoppers_prd_v3_1.ipynb). **Execution and acceptance verification:** [v3.1 GitHub Actions workflow](.github/workflows/build-prd-v3-1.yml). **Technical details:** [v3.1 implementation notes](docs/implementation_v3_1.md).

PRD v3.1 extends the executed v3.0 notebook with two full-grown all-17 tree diagnostics, two 16-source tree baselines, independent Gini/Entropy cost-complexity paths with five-fold 1-SE simplicity selection, and a direct six-way final model comparison. The selected winner controls the subsequent OOF plots, four pre-existing thresholds and single version-specific held-out evaluation. All new evidence is saved under `artifacts/prd_v3_1/` and must be verified by the workflow before use.

**Research question:** How effectively do session characteristics predict `Revenue=1`, and which taught model specification achieves the strongest mean five-fold training ROC-AUC? Prediction only; no causal upsell or deployment claim.

## Verified v3.1 findings

**Execution:** [GitHub Actions run 41595364066](https://github.com/lyd-sg/dsa211/actions/runs/41595364066) — PASS. Structural syntax, 37-cell notebook execution, numerical audit and versioned evidence checks passed. The notebook selects **L1 Logistic Regression**, mean five-fold CV ROC-AUC **0.757467**, mean AP **0.336226**. Its reserved-set check reports ROC-AUC **0.740543** and AP **0.327199**, with the pre-existing historical-use qualification.

**Tree finalists:** selected Gini `ccp_alpha=0.00100764`, 8 leaves, depth 4, CV AUC **0.733055** (full-grown **0.576629**); selected Entropy `ccp_alpha=0.00128706`, 14 leaves, depth 6, CV AUC **0.744143** (full-grown **0.579729**). Both enter the same direct six-way comparison; Entropy ranks second and Gini fifth. Every one of **722** tree alpha candidates was assessed on five common folds (**3,610** tree-alpha fold scores). Two tree baselines, two tree finalists, and the original four modelling paths are separately recorded.

**Reproducibility:** the independent training audit passed 30 CV specifications, 150 specification-fold evaluations, 16 sequential decisions, two one-SE alpha selections and four winner-dependent threshold references. Warnings from unseen nominal levels within folds are logged; the frozen training and final all-data fits reported no warnings. Results reside in [v3.1 evidence](artifacts/prd_v3_1/).
## Reproduce v3.1

From repository root, with Python 3.12 and the pinned requirements:

```bash
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  jupyter nbconvert --to notebook --execute online_shoppers_prd_v3_1.ipynb \
  --ExecutePreprocessor.timeout=7200 --output online_shoppers_prd_v3_1_executed.ipynb
```

The v3.1 notebook is a versioned direct extension of the executed v3.0 notebook, not a rebuild from `scripts/build_prd_v3.py`. The v3.0 notebook, builder and evidence remain unchanged.

## Preserved historical v3.0 notebook and results


- **[Executed PRD v3 notebook](online_shoppers_prd_v3.ipynb)** — directly reusable v2 EDA and baselines; four sequential model pathways; complete attempted-specification ledger; four finalists and winner; ROC/PR and score displays; sensitivity/specificity and the hypothetical S$3/S$12 cost threshold.
- **[Supporting evidence](artifacts/prd_v3/)** — 20 attempted operational specifications, fold scores, finalist OOF probabilities, 0.20 cost-cutoff comparisons, sensitivity scenarios, one reserved-set check, warning logs and audit metadata.
- **[PRD v3 requirements audit](docs/requirements_audit_v3.md)** and [build source](scripts/build_prd_v3.py); [supplementary training EDA](supplementary/training_eda.ipynb).

The current selected specification is **L1 Logistic Regression** with `log1p` activity magnitudes, mean five-fold CV ROC-AUC **0.757469** and mean AP **0.336226**. The reserved-set check reports ROC-AUC **0.740543**, AP **0.327199**, with mandatory disclosure that the same reserved rows were examined in historical versions.

## Reproduce the historical v3.0 notebook

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

The [archived v3.0 PRD](archive/PRD_v3.md) and original [v2 notebook](online_shoppers_revised.ipynb), [v2 PRD](docs/PRD_v2.md), [v2 technical plan](docs/technical_plan.md), [v2 README snapshot](docs/README_v2_archive.md), [v2 agent instructions](docs/AGENTS_v2_archive.md) and historical artifacts remain available for provenance. The current notebook does not mix old v2 comparisons with v3 findings.
