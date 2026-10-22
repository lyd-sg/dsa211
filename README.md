# DSA211 — Online Shoppers Purchasing Intention

Predict whether a browsing **session** ends in a purchase, then evaluate a hypothetical model-guided voucher strategy against a no-voucher baseline. The positive class is `Revenue=1`. This is prediction and simulated sales-revenue analysis, not a causal intervention study or a profitability forecast.

## Start here

- [Executed revised notebook](online_shoppers_revised.ipynb): the current analysis, including EDA, all-predictor first passes, bounded CV improvements, threshold optimisation and historical test evaluation.
- [Project decisions](docs/project_decisions.md): assumptions, decision rule and revenue derivation.
- [Methodology](docs/methodology.md): split, CV, selection and interpretation.
- [Scope and verification](docs/phase2_scope.md): provenance, execution evidence and limitations.
- [Validation workflow](.github/workflows/validate-notebook.yml): reruns the revised notebook on the committed dataset and retains an executed artifact.
- [Original notebook](online_shoppers_full_project.ipynb) and [archives](archive/README.md): unchanged historical records, not the current business framework.

## Voucher framework

Predict Buy → **no voucher**. Predict No Buy → **voucher**. Observed labels never change.

Assume **A1** guaranteed conversion for every voucher recipient; **A2** a 20% discount with no minimum spend; **A3** identical representative order value `A`; and **A4** recorded purchases represent no-voucher behaviour. Voucher effectiveness is unobserved, so A1 is hypothetical.

In units of `A`, no-voucher revenue is `TP+FN`, and model-guided revenue is `TP+0.80(FN+TN)`. The difference is `0.80TN−0.20FN`; relative change divides this by `TP+FN`. The common order value cancels. FP and FN opportunity costs are `0.80A` and `0.20A`, respectively: `C_FN:C_FP=1:4`.

The calibrated theoretical cutoff is `0.80`. Select the model and empirical threshold jointly using **training out-of-fold simulated revenue**; report ROC-AUC separately as discrimination. Compare exactly the two stated scenarios, even if the selected threshold allocates vouchers to nearly every session under guaranteed conversion.

## Computed results

The actual-data execution selected **logistic regression with quantile-transformed numeric predictors**, cutoff **0.8359523283877723**. Model and cutoff were fixed from training OOF revenue before evaluating the historical test.

| Metric | Training CV/OOF | Historical test |
|---|---:|---:|
| Mean fold ROC-AUC | 0.761455 | — |
| Pooled ROC-AUC | 0.761013 | 0.740891 |
| Sensitivity at selected cutoff | 0.000699 | 0.000000 |
| Specificity at selected cutoff | 1.000000 | 1.000000 |
| TP / FP / FN / TN | 1 / 0 / 1,430 / 7,816 | 0 / 0 / 477 / 2,606 |
| Vouchers issued | 9,246 / 9,247 | 3,083 / 3,083 |
| No-voucher revenue | 1,431.0A | 477.0A |
| Model-guided simulated revenue | 7,397.8A | 2,466.4A |
| Simulated difference | +5,966.8A (+416.97%) | +1,989.4A (+417.06%) |

The selected rule sends vouchers to **every historical test session**. Its test sensitivity is therefore zero and specificity one; it provides no selective targeting on that partition. Higher simulated revenue is conditional on A1–A4 and chiefly reflects guaranteed conversion, not evidence of actual sales growth or profit.

Quantile and log-transformed logistic candidates tied on maximum training OOF revenue; the declared AUC tie-break selected the quantile candidate. Do not interpret this tiny, sample-dependent distinction as robust superiority. Of 29 attempted designs, 27 completed; default QDA failed on singular covariance in both initial predictor sets and its regularised alternatives were evaluated separately.

## Reproduce

Use Python 3.12, as validated for this revision. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyter lab
```

Open `online_shoppers_revised.ipynb`. The committed local dataset avoids a network download. Run all cells in order, or produce a separate executed notebook:

```bash
python -m jupyter nbconvert --to notebook --execute online_shoppers_revised.ipynb \
  --ExecutePreprocessor.timeout=1200 \
  --output online_shoppers_revised_executed.ipynb \
  --output-dir=/tmp
```

Execution performs real statistical analysis. In the cloud, the prepared virtual environment is `/workspace/dsa211/.venv`. If the home directory is read-only, set Jupyter/IPython/Matplotlib configuration and runtime paths to writable workspace directories as described in the saved cloud startup instructions.

## Statistical scope and limitations

Retain the historical **75/25 stratified split, seed 42**, and **five-fold stratified training CV**. Attempt logistic regression, Gaussian Naive Bayes, LDA and QDA with all 17 predictors first; record real warnings and failures. Exclude `PageValues` operationally after its timing review, and fit all preprocessing inside folds. Retain the two extensions: threshold analysis and CV versus historical test comparison.

The same OOF results guide candidate and threshold selection, so selected CV results have selection optimism. The historical test partition was already viewed in the original notebook and is **not fresh independent confirmation**. Session-end predictor timing requires review before real-time deployment; customer IDs are unavailable. Voucher outcomes are absent, guaranteed conversion is unverified, and expenses and margins are excluded. Numerical simulated gains must not be presented as a reliable forecast of actual growth.
