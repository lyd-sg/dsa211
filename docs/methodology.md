# Working methodology — for statistical revision (not executed here)

This is the intended flow from the uploaded `project_cv_workflow.html`, the Week 7/8 course materials, and the latest professor/group instructions. It is **not** a replacement for the results already shown in the preserved notebook.

## Dataset and existing split

- Prediction target: `Revenue`; observational unit: **browsing session**, not an identified individual customer.
- Existing notebook: 12,330 sessions with a **75/25 stratified split** (`random_state=42`). Phase 1 does **not** change this.
- Course guide: perform only data-quality checks before splitting; do outcome-related EDA and model selection on **training data only**. The final test set is used once for the chosen model.
- **Historical holdout caveat:** The existing notebook has already produced test results. Its test set cannot be presented as newly untouched merely by reorganising files or re-running the notebook.

## Intended analysis order

1. Check dataset structure, response type, missing values, duplicate rows and class balance; preserve an audit trail.
2. Split training/test once (or retain the already executed 75/25 split when continuing the historical analysis).
3. Conduct EDA using **training data only**: class balance, skewness, zero frequencies, numerical/categorical relationships, and likely encoding issues.
4. Attempt **all required first-pass classifier families** with all original predictors in unoptimised forms. Apply only technically essential encoding so a numeric-input estimator can be fitted; record any default-model failure instead of hiding it.
5. Evaluate initial models by a shared **StratifiedKFold** scheme. Record AUC, sensitivity, specificity, confusion matrices and other predeclared metrics. Clearly separate first-pass diagnostics from subsequent improvements.
6. Compare proposed preprocessing, binary representations, transformations, model-specific tuning and predictor subsets **inside leakage-free CV pipelines**. Any fitted encoder, scaler, imputer or selector must learn only from that fold's training partition.
7. Choose the final family, specification and classification threshold using training/CV data. The **CAC and discount×AOV cost framework remains pending** and replaces no prior output until clarified and recomputed.
8. Reserve final independent test scoring for one predeclared winner. If examining the historical test results, identify them as **previously viewed**, not an unused fresh audit. Refit the final, fixed specification on all data only after assessment if appropriate.

## Known Phase 2 review items

- Historical notebook omits `PageValues` after an early leakage argument, whereas the new professor instruction calls for a first-pass all-predictor attempt. Make the stages explicit when revising.
- Baseline QDA has a documented singular-covariance fitting failure; preserve that observation and distinguish any stabilised QDA variant.
- Historic threshold calculations assume `C_FN/C_FP=5`; these must be revisited rather than reported as the current group's business-cost conclusion.
- The old source notebook and all outputs are preserved **byte-for-byte** in this housekeeping change.

## Executing the current notebook

Run from the **repository root**; it opens `data/uci_468.csv` through a relative path. Consult `README.md` for environment setup. Changes to notebook code, tests and metrics belong in Phase 2.
