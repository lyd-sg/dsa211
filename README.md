# DSA211 — Online Shoppers Purchasing Intention

Predict whether a browsing **session** ends in a purchase, then assess a hypothetical model-guided voucher policy against a no-voucher baseline. The positive class is `Revenue=1`. This is prediction and simulated sales-revenue analysis, not a causal intervention study or profitability forecast.

## Start here

- [Revised notebook](online_shoppers_revised.ipynb): the fully executed current analysis. To reproduce it, run all cells in order from the repository root.
- [Project decisions](docs/project_decisions.md): current assumptions and decision rules.
- [Methodology](docs/methodology.md): split, CV, candidate scope and interpretation.
- [Scope and verification](docs/phase2_scope.md): provenance, execution status and limitations.
- [Requirements audit](docs/requirements_audit.md): current scope reconciliation.
- [Validation workflow](.github/workflows/validate-notebook.yml): executes the active notebook against the committed dataset.
- [Historical archives](archive/README.md): prior executed/revised and original project notebooks.

## Voucher framework

Predict Buy → **no voucher**. Predict No Buy → **voucher**. Observed labels never change. The existing assumptions are A1 guaranteed conversion for every voucher recipient, A2 a 20% discount without minimum spend, A3 common order value `A`, and A4 recorded outcomes represent no-voucher behaviour. Voucher effectiveness is unobserved, so A1 is hypothetical.

In units of `A`, no-voucher revenue is `TP+FN`, and model-guided revenue is `TP+0.80(FN+TN)`. The difference is `0.80TN−0.20FN`; relative change divides this by `TP+FN`. The common order value cancels. The associated opportunity costs are `C_FN=0.20A` and `C_FP=0.80A`, ratio `1:4`, with a theoretical revenue cutoff of `0.80` when probabilities are calibrated. The threshold and revenue objective follow the latest user clarification to retain this framework.

## Current analysis scope

The active notebook compares Logistic Regression, Gaussian Naive Bayes and LDA. It retains all-17 first-pass diagnostics with `PageValues`, then excludes that field from operational models. Operational models compare raw, `log1p`, and fold-fitted `zeroind` treatments, with the zero-indicator threshold learned within each training fold. Logistic L2 settings (`C=0.1` and `C=10`), numerical interactions, the predeclared five-predictor logistic model, GaussianNB variance smoothing and LDA shrinkage remain. Existing raw mixed Gaussian/Categorical NB and numeric-only LDA references remain eligible; no transformed variants of those references are added.

The notebook retains the stratified 75/25 split, seed 42, five stratified training folds, fold-fitted preprocessing, mean-CV ROC-AUC model selection, OOF revenue-threshold selection, AP/fold variation reporting, and fixed historical test comparison. The current full execution completed all 21 code cells and 20 candidate designs; 9 were selection-eligible and none failed. It selected Logistic Regression `zeroind`, with threshold 0.800000, mean CV ROC-AUC 0.761161 ± 0.022013, pooled OOF AUC 0.760887 and historical test AUC 0.742293. Mean CV average precision was 0.340692 ± 0.034901; pooled OOF and test AP were 0.335089 and 0.328956.

At that cutoff, all sessions receive vouchers in both OOF and historical-test samples. Sensitivity is zero and specificity is one. Simulated revenue is 7,397.6A vs 1,431.0A in training OOF and 2,466.4A vs 477A in the historical test under guaranteed conversion. This is assumption-driven simulation, not evidence of actual voucher lift or selective targeting. See [executed results and change log](docs/revision_summary.md) for first-pass and operational baselines, confusion counts and fold variation.

## Limitations

The historical test partition was previously examined, so it is not fresh independent confirmation. Candidate and threshold selection on the same training OOF predictions creates optimism. Session-end predictors require availability review before real-time decisions. Customer IDs and voucher outcomes are absent. Simulated gains under guaranteed conversion are not evidence of actual sales growth or profit.

## Reproduce

Use Python 3.12 from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyter lab
```

Run all cells in `online_shoppers_revised.ipynb` in order. To create an executed copy without replacing the source:

```bash
python -m jupyter nbconvert --to notebook --execute online_shoppers_revised.ipynb \
  --ExecutePreprocessor.timeout=1200 \
  --output online_shoppers_revised_executed.ipynb \
  --output-dir=/tmp
```

The committed dataset avoids a network download. The GitHub workflow also runs the notebook against the committed data and retains an executed artifact.
