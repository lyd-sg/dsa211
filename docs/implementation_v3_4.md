# PRD v3.4 implementation and verification contract

**Source of truth:** [PRD v3.4](../archive/versions/v3.4/PRD_v3.4.md).  
**Notebook:** [online_shoppers_prd_v3_4.ipynb](../archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb).  
**Workflow:** [build-prd-v3-4.yml](../archive/workflows/build-prd-v3-4.yml).

## Incremental extension

Inherit the **executed v3.3 notebook**. Preserve its first-pass 17-variable diagnostics, 16-variable operational baselines, EDA, fixed seed-42 train/reserved split, five common outer CV folds, every v3.1/v3.2/v3.3 original-family experiment (20 + 11 + 7), all tree pruning, thresholds, final training CV winner and reserved/final-data refit. Only the new notebook and `artifacts/prd_v3_4/` may store new executed results.

### Grouped presentation

The original single mixed development cell has been split into a *definitions and reusable original-testing functions* cell followed by four sequential family sections: Logit, LDA, GaussianNB, BernoulliNB. Each section runs the exact original historical v3.1/v3.2/v3.3 candidate definitions and comparison rules **for that family**, then independently adds the permitted v3.4 candidate(s). Each renders a complete chronological history with parent, method, version, AUC, SE, AP, gain and accept/reject decision. A fifth subsection consolidates a machine-readable ledger only after all four sections.

The original v3.2 and v3.3 independent anchored comparisons remain intact. Only v3.4 L13→L14 is **sequential against latest accepted** within Logit. All earlier candidates remain visibly rejected/accepted as recorded rather than rewritten.

### v3.4 additions

- `L13 | Logit`: original L1 log activity representation, train-fold scaler, `LogisticRegression(penalty='l1',solver='saga',max_iter=10000,tol=1e-4)`, inner three-fold ROC-AUC tune `C=[0.01,0.05,0.2,1,5,20]`.
- `L14 | Logit`: replaces penalty with `penalty='elasticnet'`, fixed `l1_ratio=0.5`, same grid, inner CV and scaling. Evaluated against the latest accepted Logit, L13 if accepted else L1.
- `D15 | LDA`: original D0 source features, grouped backward elimination (whole categorical sources). For each outer-fit fold, each of its three *inner* fold encoders is learned on the inner-train rows only. Train/test arrays are cached; all 16→1 nested source-subset candidates are scored by inner-fold mean ROC-AUC. Highest-scoring one-source deletion at each size defines the path; simplest subset within one SE of best inner AUC is refitted on the outer training data. Only the outer fold evaluates the entire selected-source procedure.

Both logistic penalty tuning and LDA source selection are refitted with the outer-fit-fold data only. CV effects remain exploratory because the project has repeatedly inspected the same fold results in earlier versions.

### Expected evidence

- 41 history rows, exactly three new `trial_version=v3.4` IDs, 51 total scored specifications, 255 specification-fold rows, 37 acceptance comparisons.
- 5 outer fold × 16 source sizes = 80 rows in `backward_lda_selection_paths.csv` with complete 16→1 paths; `backward_lda_outer_folds.csv` records chosen source groups and each outer fold AUC.
- Inner 3-fold best `C` and nonzero coefficient counts for each of five L13 and five L14 outer fold fits.
- Gini/Entropy full pruning path audit and simplicity-selection, six-way comparison by mean five-fold AUC, all four threshold references, finite parameters, one (historically reused) reserved check, full-data refit.
- Only report new numerical results when the notebook is **fully executed** and the independent audit reports `status=PASS`.

### Course source basis

Lecture 8: subset and forward/backward stepwise, within-fold feature search, model-size selection by the one-SE rule. Lecture 9: standardisation, Ridge/LASSO/Elastic Net, cross-validated penalties. These lectures' core examples are linear regression; v3.4 adapts the principles to logistic/LDA classification, with CV ROC-AUC rather than regression RSS/RMSE.
