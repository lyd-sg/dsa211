# Phase 2 scope and verification

## Agreed scope

This branch adds `online_shoppers_revised.ipynb`, using the uploaded two-page *Predicting Online Purchases* brief as the starting point, with the professor's later instruction to **attempt all predictors with all model families first**.

- **Prediction, not coefficient inference.**
- Dataset: UCI 468, target `Revenue`, 12,330 browsing **sessions**.
- Outer split: retain the previously used **75/25 stratified split, random seed 42**.
- CV: **5-fold stratified** training-only validation; each fold fits its own preprocessing.
- Models: logistic regression, Gaussian Naive Bayes, LDA and QDA (with transparent default-QDA failure or repair notes).
- Explicit all-17-predictor first pass, then operational 16-predictor models excluding `PageValues`, following the brief's timing/leakage argument.
- EDA, assumptions, bounded CV-guided transformations and tuning, before/after comparisons, confusion matrices, sensitivity, specificity, ROC/AUC.
- **Extension 1:** training-OOF threshold optimisation and sensitivity/specificity/cost curves.
- **Extension 2:** CV-versus-historical-holdout comparison on the preselected winner and threshold.

The previously discussed optional additional analyses—KNN, gradient boosting, splines, a bootstrap of the threshold, learning curves and exhaustive experimentation—are **deliberately excluded from this Phase 2 notebook**.

## Cost and historical evaluation

The two-page brief uses a **hypothetical** cost ratio `C_FN/C_FP=5`; this Phase 2 notebook implements that assumption and stress-tests alternatives, rather than treating the group's later CAC/discount × AOV proposal as settled. It does not make causal claims about live support creating purchases.

The original project notebook already displayed test-set results for the **same** 25% holdout. Consequently, re-executing the revised notebook's test section is **retrospective**, not an entirely new independent validation. New data would be required for that claim.

## Notebook quality controls

- `online_shoppers_full_project.ipynb` is **unchanged**.
- The revised notebook uses `data/uci_468.csv` and does not download or silently replace it.
- Every statistical conclusion follows executable code. There are no pre-filled numerical claims that were not recomputed.
- A smoke run with structurally compatible **synthetic** data confirmed all 28 notebook cells can execute. Synthetic scores were **not** retained as findings.
- `.github/workflows/validate-notebook.yml` runs the notebook on the actual committed dataset; when it completes, the executed notebook is available as a workflow artifact.
- No previously viewed test data are used to fit the CV folds, transformation or selected threshold.

## Reproduce

```bash
python -m pip install -r requirements.txt
python -m pip install nbconvert nbclient
jupyter nbconvert --to notebook --execute online_shoppers_revised.ipynb \
  --output online_shoppers_revised_executed.ipynb
```

Run from the repository root. The generated executed notebook is an **output**, not a replacement for the archived full notebook.

## Changes deferred to a later approval

- Optional extra benchmarks, calibration/bootstrapping/learning curves.
- New business-cost assumption based on a defined intervention and actual CAC/AOV.
- Genuine fresh confirmatory testing on new, independent sessions.
