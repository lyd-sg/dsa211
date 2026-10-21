# DSA211 repository instructions

## Current project

The active task is a **prediction-focused** comparison of classification methods for UCI Online Shoppers Purchasing Intention (`Revenue`, **session-level** observations).

**Entry point:** `online_shoppers_full_project.ipynb` at the repository root. It is a preserved historical notebook. `data/uci_468.csv` matches its existing relative file path. Read [`docs/project_decisions.md`](docs/project_decisions.md), [`docs/methodology.md`](docs/methodology.md), and [`README.md`](README.md) before modifying analysis.

## Project-specific requirements

- Respect the professor's instruction to attempt **all required models with all candidate predictors on the first pass**, recording genuine numerical failures before CV-guided alterations.
- Compare the three taught families: logistic regression, Naive Bayes and discriminant analysis. Do not preselect the winner.
- Treat nominal numeric-coded categories as **unranked**; do not automatically binarise zero-heavy numeric predictors prior to the first pass.
- Keep outcome-related EDA, preprocessing fitted from data, selection and hyperparameter tuning within the training/CV workflow; the held-out test is not a tuning set.
- Distinguish existing historical results from any new execution. Do not present the already-viewed notebook test set as a fresh unused holdout.
- The group's proposed **CAC/discount×AOV** error costs are **not yet implemented or validated**. The preserved notebook uses `C_FN/C_FP=5`; do not silently present its threshold or final conclusion as updated.
- Do not assume repeated customers are identifiable. The dataset represents **sessions**; the group has unresolved questions about customer uniqueness.

## File and change discipline

- Phase 1 housekeeping: **no notebook cell/source/output changes, statistical recomputation or modified CSV/PDF findings**.
- Preserve `online_shoppers_full_project.ipynb` at root until a separately reviewed code-path change permits moving it without breaking `data/uci_468.csv` loading.
- Historical dataset-selection work is under `archive/`; do not use its old `bakeoff.py` or `FINAL_REPORT.md` as the current project specification.
- For future analysis changes: work on a branch, preserve an audit trail, document split/seed/CV/fitted preprocessing, and review the existing test-set caveat before claiming out-of-sample validation.
- Do not manufacture experiments, metrics, business costs or professor requirements.

See `archive/README.md` for the historical files.
