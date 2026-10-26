# DSA211 — Predicting Online Purchases

Predict whether a browsing **session** ends in a purchase, compare the approved coursework classifiers, and illustrate a hypothetical voucher policy. Prediction is the primary objective. Voucher arithmetic is neither measured treatment response nor a profit forecast.

## Current revision — 26 October 2026

The active notebook now compares **exactly seven** training-CV candidates: four unchanged operational baselines and three EDA-informed revisions. Revised Logit adds fixed **L2 C=1.0** with fold-only standardisation to the existing activity log/presence engineering; revised LDA adds **automatic covariance shrinkage** to its log-activity engineering; revised MixedNB retains mixed likelihoods and categorical smoothing. Exact motivations and the one-table revision log are in [Regularisation revision log](docs/regularisation_revision_log.md).

**Evaluation boundary:** This reopened model search is **training-only**. The project's previously inspected test set is not a fresh independent holdout for the changed candidate selection. Scores in the 25 October verification report and archived test artifacts belong to the **older unpenalised** winner and must not be attributed to this revision. The current notebook prints the new seven-candidate CV results and writes a separate `regularisation_revision_summary.json` upon execution. It reports the best-performing **tested** CV specification, not a newly validated test winner.

## Review and reproduce

- [Main notebook](online_shoppers_revised.ipynb): academic submission; self-contained code and visible results.
- [Supplementary training EDA](supplementary/training_eda.ipynb): five targeted investigations; retained separately and **not submitted**.
- [Approved PRD v1.0](docs/PRD.md): unchanged requirements.
- [Repository audit](docs/repository_audit.md), [technical plan](docs/technical_plan.md), [independent plan review](docs/technical_plan_review.md) and [recipe review](docs/recipe_review.md): provenance and approval gates.
- [Historical 25 October verification](docs/verification_report.md) and [independent review](docs/final_independent_review.md): valid only for the former unpenalised specification; do not treat its test metrics as updated-model evidence.
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

Four minimally processed baselines are unpenalised Logit, GaussianNB, BernoulliNB and standard LDA. The three revisions are L2-penalised feature-engineered Logit, covariance-shrinkage feature-engineered LDA, and mixed-likelihood NB. Highest mean training CV ROC-AUC selects one; AP and fold SD/SE support interpretation. The selected model is refitted on training data for a finite-parameter check, **without** reusing the historical holdout for a new test comparison.

## Executed results

The **25 October historical, unpenalised** notebook completed 18 code cells, with revised Logit CV AUC **0.757647** and historical test AUC/AP **0.741210 / 0.326790**. The old 2/3 voucher policy selected almost everyone. **These are not results for the regularisation revision.** **Validated on GitHub Actions:** the reopened seven-model CV completed successfully with revised L2 Logit the winner (mean five-fold ROC-AUC **0.758074**, SD **0.012727**, average precision **0.335193**). Regularised LDA scored **0.741698** and revised MixedNB **0.731474**. Execution artifact: [GitHub Actions run](https://github.com/lyd-sg/dsa211/actions/runs/40255397327). The new notebook deliberately does not compute a fresh test metric from previously inspected data.

The ranking result does not establish useful targeting under this almost-universal voucher policy. Revenue differences are conditional on assumed q, not measured voucher effects. See the verification report for the full criterion-by-criterion audit.

## Hypothetical policy

Predict buyer when `p >= 2/3` → no voucher; otherwise offer a hypothetical 20% voucher. Observed labels never change. The primary threshold stays fixed regardless of simulated revenue. Four training references compare prevalence, 0.5, 2/3 and sensitivity–specificity crossover.

At fixed 2/3 recipients, vary only assumed incremental conversion `q = 0.10, 0.25, 0.50, 1.00`. In common order-value units `A`:

- No-voucher reference: `R0/A = TP + FN`.
- Hypothetical expected voucher revenue: `Rq/A = TP + 0.8 FN + 0.8 q TN`.
- Difference: `delta/A = 0.8 q TN - 0.2 FN`.

The reference q = 0.50 gives assumed opportunity costs 0.20A (FN) and 0.40A (FP), hence buyer cutoff 2/3 if probabilities are meaningful. The dataset does not identify q or actual voucher effectiveness.

## Limits

For the regularisation revision, the previous model-selection and test results are historical and not comparable as if evaluated on a new untouched holdout. This analysis can report the best model *within the seven tested training-CV candidates*, but cannot establish independently validated superiority of a newly regularised winner.

Prior work viewed an overlapping historical 75/25 partition; the revised holdout is not historically untouched. Training-informed recipe/model choice creates optimism. Retained duplicate patterns, sparse categories, separation, NB/LDA assumptions and probability calibration affect interpretation. Session-end predictors are not certified available at a voucher decision time. Original labs, lectures and instructor workflow files were unavailable for direct comparison; verification uses their requirements recorded in the approved PRD. No causal lift, unique-customer count, profit or real-time deployment claim is supported.
