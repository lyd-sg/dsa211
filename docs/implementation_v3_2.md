# PRD v3.2 implementation and evidence contract

**Source branch:** `analysis/prd-v3-2-notebook`. **Date:** 3 November 2026.  
**Authority:** [PRD v3.2](../PRD_v3.2.md) · [source notebook](../online_shoppers_prd_v3_2.ipynb) · [automated acceptance workflow](../.github/workflows/build-prd-v3-2.yml).

## Immutable history and new work

The 37-cell executed v3.1 notebook served as a source template. Its outputs were cleared in the new v3.2 source file, and its `artifacts/prd_v3_1/` directory, original PRD, existing v3.0 files and data were not changed. Original `PATHS` L1–L4, D1–D4, G1–G4, B1–B4 retain the precommitted evaluation order and strict challenger one-SE gate.

FoldSafeFeatures accepts five extra configuration parameters: `presence_cols`, `log_cols`, `quadratic_cols`, `special_categorical`, `drop_nominal`. They are inert for every original v3.1 configuration, so old model recipes remain comparable. D7 removes SpecialDay from the numeric block before fold-specific categorical dummy encoding, retaining the original numeric feature for D0. G9 removes all six nominal originals only for its named single group-deletion candidate.

## New model-selection phase

`V31_PATH_FINALISTS` and `V31_PATH_FINAL_CONFIGS` freeze each original family incumbent. For **each of the eleven** L5–L7, D5–D7, G5–G9:

1. Copy the appropriate v3.1 family incumbent configuration and make exactly the named change.
2. Fit on the same five existing training CV folds, in a fold-contained pipeline, saving validation OOF probabilities, AUC/AP, SD/SE, fitted warnings, parent and change.
3. Mark `accepted` as **qualification** when `mean_new_auc - mean_anchor_auc > new_auc_se`; do not change the threshold.
4. If any qualify in a pathway, select the qualifying proposal with the highest mean CV AUC, tie by step ID; otherwise keep the untouched incumbent.

These tests are independently anchored, **not** an added cumulative sequential path. The distinction is necessary because G6 drops ProductRelated_Duration whereas G7 log-transforms that same variable. Each is still evaluated, irrespective of the other outcome. No rejected v3.1 change is removed or altered.

The all-17 diagnostics, all-16 baselines, Gini/Entropy full-grown/pruning procedures, six direct finalists, ROC/PR descriptions, fixed threshold analysis and final refit are retained. Source and numerical outcomes are version-separated.

## Static and numerical verification

The new GitHub Actions workflow validates notebook structure and Python cell compilation, executes all 20 code cells, and checks:

- 31-trial ledger, split into original 20 and eleven new; original four baseline identifiers and 27 additional decision comparisons.
- 41 model specification summaries and 205 independently recomputed fold scores, with no missing OOF predictions.
- Each anchored parent, unchanged strict gain-vs-SE qualification, and best-qualified one-change finalist.
- Both complete tree alpha paths and fold evidence; one-SE eligible candidates and fewest-leaf selected candidate; six finalist candidate family set.
- Winner-only four threshold references and 0.20 cost threshold; frozen model finite-parameter checks; version-specific reserved-set evaluation and full-data refit.
- Original notebooks and historical evidence remain accessible; generated `artifacts/prd_v3_2/` is separate.

## Reporting limitations

No new v3.2 metric should be presented as completed until the workflow exits successfully and saves `artifacts/prd_v3_2/independent_training_audit.json` with `status=PASS`, the executed notebook, and matching metadata. Do not infer that the successful v3.1 audit proves a successful v3.2 run.

The extra candidates are **post-v3.1 exploratory refinements**, and the 20% reserved set has been viewed before. This is a genuine repeat-use limitation, not something resolved by retaining fold membership. The user's request to add all eleven exceeds the professor's original 3–5 tests per path; preserve original 3–5 histories and state the extension explicitly.
