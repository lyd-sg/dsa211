# DSA211 — Online Shoppers Purchasing Intention

Predict whether a browsing **session** ends in a purchase, then evaluate a hypothetical model-guided voucher strategy against a no-voucher baseline. The positive class is `Revenue=1`. This is prediction and simulated sales-revenue analysis, not a causal intervention study or a profitability forecast.

## Start here

- [Executed revised notebook](online_shoppers_revised.ipynb): the current analysis, including EDA, all-predictor first passes, bounded CV improvements, threshold optimisation and historical test evaluation.
- [Project decisions](docs/project_decisions.md): assumptions, decision rule and revenue derivation.
- [Methodology](docs/methodology.md): split, CV, selection and interpretation.
- [Scope and verification](docs/phase2_scope.md): provenance, execution evidence and limitations.
- [Requirements audit](docs/requirements_audit.md): consolidated checklist, corrected gaps and why guaranteed conversion can produce an extreme allocation.
- [Validation workflow](.github/workflows/validate-notebook.yml): reruns the revised notebook on the committed dataset and retains an executed artifact.
- [Original notebook](online_shoppers_full_project.ipynb) and [archives](archive/README.md): unchanged historical records, not the current business framework.

## Voucher framework

Predict Buy → **no voucher**. Predict No Buy → **voucher**. Observed labels never change.

Assume **A1** guaranteed conversion for every voucher recipient; **A2** a 20% discount with no minimum spend; **A3** identical representative order value `A`; and **A4** recorded purchases represent no-voucher behaviour. Voucher effectiveness is unobserved, so A1 is hypothetical.

In units of `A`, no-voucher revenue is `TP+FN`, and model-guided revenue is `TP+0.80(FN+TN)`. The difference is `0.80TN−0.20FN`; relative change divides this by `TP+FN`. The common order value cancels. FP and FN opportunity costs are `0.80A` and `0.20A`, respectively: `C_FN:C_FP=1:4`.

The calibrated theoretical cutoff is `0.80`. Select the classifier by **highest mean training CV ROC-AUC**, then optimise **only its threshold** using training out-of-fold simulated revenue, as clarified during the requirements audit. Report PR-AUC and fold variation as additional predictive evidence. Compare exactly the two stated revenue scenarios, even if the selected threshold allocates vouchers to nearly every session under guaranteed conversion.

## Computed results

The actual-data execution selected **logistic regression with Yeo–Johnson-transformed numerical predictors**, by highest mean training CV ROC-AUC. Its voucher discount is fixed at **20%**. Only after freezing that classifier was its threshold selected from training OOF revenue: **0.8018563753337375**.

| Metric | Training CV/OOF | Historical test |
|---|---:|---:|
| Mean fold ROC-AUC ± sample SD | 0.762099 ± 0.023055 | — |
| Pooled ROC-AUC | 0.761911 | 0.741041 |
| Mean fold PR-AUC/AP ± sample SD | 0.341894 ± 0.036092 | — |
| Pooled PR-AUC/AP | 0.337700 | 0.328847 |
| Sensitivity at selected cutoff | 0.000000 | 0.000000 |
| Specificity at selected cutoff | 1.000000 | 1.000000 |
| TP / FP / FN / TN | 0 / 0 / 1,431 / 7,816 | 0 / 0 / 477 / 2,606 |
| Vouchers issued | 9,247 / 9,247 | 3,083 / 3,083 |
| No-voucher revenue | 1,431.0A | 477.0A |
| Model-guided simulated revenue | 7,397.6A | 2,466.4A |
| Simulated difference | +5,966.6A (+416.95%) | +1,989.4A (+417.06%) |

PR-AUC is reported as average precision, not trapezoidal PR integration. Fold SD describes variation, not a confidence interval. The revised notebook reports all five selected-model fold scores.

The selected rule sends vouchers to **every training and historical test session**. Its sensitivity at that operating cutoff is zero and specificity one; it provides no selective targeting on these samples. Higher simulated revenue chiefly reflects guaranteed conversion under A1, not actual sales growth or profit. The probability rankings still have the AUC/AP performance shown above; those ranking metrics answer a different question from the thresholded voucher rule.

The leading ROC-AUC candidates differ by only about 0.0006; this does not establish robust superiority. Quantile logistic has the highest AP among eligible models, but the agreed selection criterion is mean CV ROC-AUC. Of **35** attempted designs, **33** completed. Default QDA failed on singular covariance in both initial predictor sets. Mixed Gaussian/Categorical NB and numerical-only LDA/QDA were added to resolve the consolidated checklist's mixed-predictor concern; legacy Gaussian fits on dummies remain visible diagnostics outside final eligibility.

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
