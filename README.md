# DSA211 — Predicting Online Purchases

Predict whether a browsing **session** ends in a purchase, compare the approved coursework classifiers, and illustrate a hypothetical voucher policy. Prediction is the primary objective. Voucher arithmetic is neither measured treatment response nor a profit forecast.

## Review and reproduce

- [Main notebook](online_shoppers_revised.ipynb): academic submission; self-contained code and visible results.
- [Supplementary training EDA](supplementary/training_eda.ipynb): five targeted investigations; retained separately and **not submitted**.
- [Approved PRD v1.0](docs/PRD.md): unchanged requirements.
- [Repository audit](docs/repository_audit.md), [technical plan](docs/technical_plan.md), [independent plan review](docs/technical_plan_review.md) and [recipe review](docs/recipe_review.md): provenance and approval gates.
- [Final verification](docs/verification_report.md) and [independent final review](docs/final_independent_review.md): acceptance criteria, actual execution, numerical checks and limitations.
- [Supervision record](docs/implementation_log.md): Sol instructions, Luna implementation, inspections and corrections.
- [Methodology](docs/methodology.md), [project decisions](docs/project_decisions.md) and [requirements audit](docs/requirements_audit.md).
- [Historical archives](archive/): prior work. The immediately preceding active notebook is preserved byte-for-byte as `archive/online-shoppers/online_shoppers_pre_prd_v1.ipynb`; its old scores are not current results.

Use Python 3.12 from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyter lab
```

Run the main notebook in order. To generate an executed review copy:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python -m jupyter nbconvert --to notebook --execute online_shoppers_revised.ipynb \
  --ExecutePreprocessor.timeout=1200 --output main_review.ipynb --output-dir=/tmp
```

The supplementary notebook runs from the repository root or its own directory; artifact paths resolve to the repository. The committed CSV avoids a download. The existing [GitHub workflow](.github/workflows/validate-notebook.yml) executes the main notebook and retains its executed artifact. Routine reproduction repeats the frozen analysis; it must never use test results to change models or policy.

## Fixed design

Quality checks precede a new stratified **80/20** split, seed 42: 9,864 training and 2,466 test sessions. Five common shuffled stratified training folds (seed 42) fit preprocessing within folds. All predictor EDA and choices use training only. Four all-17 diagnostic counterparts explain possible `PageValues` timing leakage; the operational comparison excludes it.

Four minimally processed baselines are unpenalised Logit, GaussianNB, BernoulliNB and standard LDA. One independently reviewed, EDA-supported revision per family gives seven operational specifications. Highest mean CV ROC-AUC selects one; AP and fold SD/SE support interpretation. After its one held-out audit, refit that exact specification on all 12,330 observations without another score.

## Executed results

The main notebook completed all 18 code cells in 4m52s. Revised Logit wins mean training-CV ROC-AUC at **0.757647**; its single-winner test ROC-AUC/AP are **0.741210 / 0.326790**. At the fixed 2/3 threshold, **TN=2,082, FP=2, FN=382, TP=0**: no buyers are detected, and **2,464/2,466 sessions receive vouchers**. The model and threshold were not changed after this finding. The exact final pipeline was then fitted on all 12,330 rows without another score.

The ranking result does not establish useful targeting under this almost-universal voucher policy. Revenue differences are conditional on assumed q, not measured voucher effects. See the verification report for the full criterion-by-criterion audit.

## Hypothetical policy

Predict buyer when `p >= 2/3` → no voucher; otherwise offer a hypothetical 20% voucher. Observed labels never change. The primary threshold stays fixed regardless of simulated revenue. Four training references compare prevalence, 0.5, 2/3 and sensitivity–specificity crossover.

At fixed 2/3 recipients, vary only assumed incremental conversion `q = 0.10, 0.25, 0.50, 1.00`. In common order-value units `A`:

- No-voucher reference: `R0/A = TP + FN`.
- Hypothetical expected voucher revenue: `Rq/A = TP + 0.8 FN + 0.8 q TN`.
- Difference: `delta/A = 0.8 q TN - 0.2 FN`.

The reference q = 0.50 gives assumed opportunity costs 0.20A (FN) and 0.40A (FP), hence buyer cutoff 2/3 if probabilities are meaningful. The dataset does not identify q or actual voucher effectiveness.

## Limits

Prior work viewed an overlapping historical 75/25 partition; the revised holdout is not historically untouched. Training-informed recipe/model choice creates optimism. Retained duplicate patterns, sparse categories, separation, NB/LDA assumptions and probability calibration affect interpretation. Session-end predictors are not certified available at a voucher decision time. Original labs, lectures and instructor workflow files were unavailable for direct comparison; verification uses their requirements recorded in the approved PRD. No causal lift, unique-customer count, profit or real-time deployment claim is supported.
