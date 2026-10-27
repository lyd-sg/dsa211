# DSA211 — Predicting Online Purchases

**Current project authority:** [approved PRD v2.0](docs/PRD_v2.md) and [technical implementation plan v2.0](docs/technical_plan.md).

**Research question:** How well can variables describing a browsing session predict whether it results in a purchase (`Revenue=1`), and which DSA211 classification model ranks buyers and non-buyers most effectively? The project is **prediction-only**, not coefficient inference, causal inference or a commercial-discount study.

## Active notebook and evidence

- **[Main notebook](online_shoppers_revised.ipynb):** one submission-oriented notebook covering source quality, train-only EDA, seven-model five-fold CV comparison, OOF ROC and PR curves, selected model's probability distribution, sensitivity–specificity crossover and final full-data refit.
- **[Supplementary training EDA](supplementary/training_eda.ipynb):** five targeted investigations, not part of the submission.
- **[Revision decisions](docs/regularisation_revision_log.md):** exact EDA motivations and 26 October validated model comparison.
- **[PRD v1.0](docs/PRD.md), [prior technical plan](docs/technical_plan_v1_archive.md), [prior AGENTS rules](docs/AGENTS_v1_archive.md)** and historical reports/artifacts are retained for provenance; **they are not current requirements**.

## Dataset and evaluation

- UCI Online Shoppers dataset: **12,330 session rows**; original binary target `Revenue`, 17 source predictors, 125 excess exact duplicates retained.
- Stratified 80/20 split, random seed **42**: **9,864 training** / **2,466 reserved** rows. Five shuffled stratified folds with common membership for every model.
- Four operational baselines: unpenalised Logit, Gaussian NB, Bernoulli NB and standard LDA, with `PageValues` omitted as a precaution over prediction-time availability.
- Three revised candidates: log/presence-engineered **L2 Logit C=1** with fold scaling, log-activity **covariance-shrinkage LDA**, and Gaussian/discrete **Mixed NB** with smoothing.
- Select by **highest mean five-fold training ROC-AUC**. Report fold SD/SE, average precision and ROC/PR evidence for class imbalance.

**Previously validated seven-model comparison (26 October):**

| Model | Mean fold ROC-AUC |
|---|---:|
| Operational Logit | 0.750020 |
| Operational Gaussian NB | 0.692021 |
| Operational Bernoulli NB | 0.723133 |
| Operational LDA | 0.740879 |
| **Revised L2 Logit** | **0.758074** |
| Revised shrinkage LDA | 0.741698 |
| Revised Mixed NB | 0.731474 |

The selected model's mean-fold AP was approximately **0.335193**. These are **training-CV results, not independent test scores**. The revised model has no newly reported independent test estimate.

## Three-threshold interpretation

On winner **training OOF** probabilities compare:

1. Exact training purchase prevalence.
2. Conventional **0.500**.
3. The **sensitivity–specificity crossover**, found by minimising the gap between the two rates across empirical cutoffs.

Report sensitivity, specificity and precision. The crossover is a **balanced reference**, not proven optimal for all use cases. No voucher, discount, business-cost, revenue or conversion simulation forms part of the current notebook.

## Reproduce and verify

Run from the repository root using Python 3.12 and the pinned dependency file:

```bash
python -m pip install -r requirements.txt
python -m pip install "nbconvert>=7" "nbclient>=0.10" "nbformat>=5"
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  jupyter nbconvert --to notebook --execute online_shoppers_revised.ipynb \
  --ExecutePreprocessor.timeout=1200 --output online_shoppers_revised_executed.ipynb
```

The GitHub Actions workflow runs the same notebook on pull requests and relevant branch pushes. Use its result and generated executed-notebook artifact for verification; **a commit alone does not prove successful execution**.

After selection, the exact winner is refitted on 9,864 training rows for numerical checks and on all 12,330 rows as the final model. Full-data fitted predictions are never presented as an independent validation metric. Avoid claims of causal drivers, reliable calibration, unique customers or real-time availability of all source predictors.

## Scope and provenance

The old `docs/phase2_scope.md`, `docs/verification_report.md` and related dated reports describe previous analyses. Interpret them only as historical records for their exact earlier specifications. Current model choices are governed by the approved PRD v2.0 and active technical plan.
