# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.4

**Design frozen:** 3 November 2026.  
**Base:** The fully executed [PRD v3.3](PRD_v3.3.md), branch `analysis/prd-v3-3-notebook`.  
**New branch:** `analysis/prd-v3-4-notebook`.  
**Scope:** Exactly **three** syllabus-informed experiments: **L13, L14 and D15**. Retain every prior experiment and add new analyses without recreating or overwriting earlier versions.

## 1. Objective and scope

The prediction-only objective remains to classify a session's `Revenue=1`, choosing the highest **mean five-fold training ROC-AUC** across four original teaching families (Logistic Regression, LDA, Gaussian NB, Bernoulli NB) and two independently pruned classification trees (Gini and Entropy).

This version addresses multicollinearity and redundant predictors identified in training-only EDA using systematic **regularisation and feature selection**, rather than additional simple one-variable distributional transformations. Lecture 8 covers forward/backward stepwise and nested model-selection CV in the linear-regression setting; Lecture 9 covers Ridge, LASSO, Elastic Net and nested penalty selection. The new logistic L1/Elastic Net and backward-selected LDA are **classification adaptations of syllabus methods**, not claims that the lecture's OLS code directly applies unchanged.

**No new model families**, interaction feature candidates, trees, QDA, KNN, random forests or boosting. Keep all raw 16 operational source variables (excluding PageValues, whose decision-time availability is uncertain rather than established leakage).

## 2. Locked data and validation protocol

- Original UCI data `data/uci_468.csv`: 12,330 sessions, 17 source predictors, binary `Revenue`; retain known 125 excess exact duplicates for version comparability, but disclose possible fold dependence.
- Original seed-42 stratified 80/20 train/reserved split: 9,864 training and 2,466 reserved sessions.
- The same five shared shuffled stratified **outer** training CV folds (seed 42) for all candidates. Within each outer fit fold, a new three-fold stratified **inner** CV (seed 42) selects regularisation strength or LDA subset size. No outcome from outer validation folds is accessible to tuning or feature selection.
- Reuse the existing source, EDA, fold-fitted one-hot categorical encoding, all-17 diagnostic models, four operational baselines, four family pathways, tree pruning, thresholds, business-cost assumptions and overall winner selection. New outputs only under `artifacts/prd_v3_4/`.
- The historical reserved set was examined in v3.1/v3.2/v3.3. A v3.4 winner check cannot restore its status as a pristine independent test; run the version-specific reserved check only after freezing the training-selected winner.

## 3. Exactly three new experiments, sequential against latest retained family model

### L13 — LASSO-penalised Logistic Regression

**Latest accepted starting point:** L1 Logistic Regression from v3.3, with `log1p` of all six activity variables. Preserve the same 16 operational source predictors and fold-safe encoding.

**Single new modelling change:** Replace the unpenalised logistic estimator with **L1-penalised Logistic Regression**; train-fold standardisation is required because coefficient penalties depend on predictor scale. The entire estimator and scaler are learned in the appropriate fit fold.

**Frozen inner-CV tuning:** `LogisticRegression(penalty='l1', solver='saga', max_iter=10000, tol=1e-4)`; grid `C=[0.01,0.05,0.2,1.0,5.0,20.0]`, `GridSearchCV(scoring='roc_auc',cv=StratifiedKFold(3,shuffle=True,random_state=42),refit=True)`. Smaller `C` means a stronger penalty. Refit at each outer fit fold's selected `C` before scoring its outer validation fold.

**EDA hypothesis:** Collinear and low-information predictors may add unnecessary variance; penalised sparse coefficients could improve out-of-fold prediction. Report fold-selected `C`, sparsity/nonzero-coefficient counts and a full-data final selected feature list **only if this candidate becomes the overall finalist**. Selection is predictive; zero coefficients do not imply a causal absence of effect.

### L14 — Elastic-Net-penalised Logistic Regression

**Anchor:** The **latest accepted Logistic Regression**, i.e. L13 if L13 qualifies, else L1. The **penalty is replaced**, never stacked or cumulated.

**Single new modelling change:** Use `LogisticRegression(penalty='elasticnet', l1_ratio=0.5, solver='saga', max_iter=10000, tol=1e-4)` with the same fold-safe feature representation and standardisation as L13 and identical fixed inner-CV `C` grid. The 50/50 split between L1 and L2 is fixed in advance, following the course's regularisation comparison.

**EDA hypothesis:** Strongly correlated groups, e.g. BounceRates/ExitRates, may be handled more stably by combined shrinkage than pure LASSO. Report inner-selected `C` and coefficient sparsity.

### D15 — Backward stepwise LDA source-feature selection

**Anchor:** The latest accepted LDA, currently D0, using the 16 original operational source predictors.

**Method:** Inside each outer **training** fold, start with all 16 **source predictor groups**. Repeatedly delete one source group at a time (for nominal predictors, drop the entire group of dummy columns, never select individual dummy levels). For each possible deletion, estimate a **three-fold inner-CV ROC-AUC** with the unchanged standard LDA `solver='svd'`. Choose the highest inner-CV-AUC deletion, ties by original source order; continue until one source remains. Record the full resulting 16-to-1 nested subset path.

Select subset size from the resulting inner-CV mean AUC profile using the **course's within-one-SE parsimony rule**: among path sizes whose inner mean ROC-AUC is at least `(best inner mean AUC − SE of best-size CV AUC)`, select the **smallest number of source predictors**. Fit LDA on all outer-fit-fold rows using the selected subset and predict only the held-out outer fold. Different outer folds may legitimately select different sources. The **outer** five-fold AUC is therefore the evaluation of the *whole backward-selection procedure*, not of one fixed post-hoc subset.

**EDA hypothesis:** Correlated inputs and over-inclusive feature sets may destabilise the shared LDA covariance and add variance. Removing source groups systematically may improve class separation.

**Implementation constraints:** Fit per-inner-fold dummy encoding only on its inner-training rows and never before inner CV. Efficiently cache full 16-source encoded matrices for each inner fold and select source index groups without refitting the encoding globally, verifying one-hot group mapping and finite scores. All class means and covariance estimates remain fitted inside the applicable fit fold. Report selected source count and the actual subset per outer fold; record the complete inner-CV deletion paths and the refit-selected subset.

## 4. Preserved sequential acceptance

Keep the **existing** conservative between-specification rule unchanged, for direct v3.1–v3.4 comparability:

`gain = mean outer CV ROC-AUC(challenger) − mean outer CV ROC-AUC(latest accepted family model)`.  
`SE_challenger = SD(five challenger outer fold ROC-AUCs) / sqrt(5)`.  
**Accept iff** `gain > SE_challenger` (strict).

- For **L13**, compare to latest accepted L1. If accepted, L14 compares against **L13** and inherits its logistic feature representation while **replacing** its L1 penalty; otherwise L14 compares to L1.
- For **D15**, compare against latest accepted LDA D0.
- An unaccepted new candidate is reported as such, not dropped. The course's **internal** one-SE choice of LDA subset size is distinct from this **external** candidate-acceptance hurdle. The latter is **not** a formal paired difference test.
- No additional tests, grid revisions, external threshold tuning or post-result criterion changes may be introduced to force acceptance.

## 5. Notebook organisation requested by the user

The user explicitly requires **all trials grouped by model family**, not one mixed development table. Extend and reorganise the existing v3.3 notebook's experiment presentation without rebuilding its data/EDA/diagnostic/plotting sections:

1. **Logistic Regression (L0–L10, L13, L14)**: source-to-v3.4 progression in step order, with version, exact parent, transformation/penalty, mean CV AUC/AP, fold SE, gain, accepted and retained family model; render an independent family-specific table and summary.
2. **LDA (D0–D11, D15)**: identical family-specific chronological ledger, plus source selection stability and paths.
3. **GaussianNB (G0–G9)**: full history and retained G7.
4. **BernoulliNB (B0–B4)**: full history and retained B3.
5. **Gini and Entropy classification trees**: continue to render independent pruning selection and tree comparisons in their pre-existing section.
6. **Six-way final model comparison**, winner, ROC/PR, calibration, thresholds, frozen reserved check and full-data refit, all retaining the previous order and methods.

Preserve all historical candidate definitions and accepted/rejected results *as recorded*; older v3.2/v3.3 alternatives retain their original independent anchored comparisons and must not be retroactively relabelled as sequential candidates. Only L13, L14 and D15 use the current sequential latest-accepted rule. Gaps in experiment IDs are intentional (L11–L12 and D12–D14 were never executed).

## 6. Expected evidence and acceptance gates

The original 20 v3.1 development records, eleven v3.2 anchored candidates and seven v3.3 anchored candidates remain; add **exactly three v3.4 trials**, for **41** logged family attempts. Six all-17 diagnostics, six operational baselines and two selected trees bring the scored specification count to **51** with **255** five-fold result rows and **37** original-family postbaseline acceptance decisions (16+11+7+3). Tree-alpha candidates/folds are audited separately under the existing full-path rules.

A result can only be accepted once the full notebook has executed and the independent audit confirms:

1. All code cells compile and execute without error outputs, and the executed v3.4 notebook is saved.
2. Exact **41** trial rows and IDs `L13,L14,D15`, exact **51** scored specifications, **255** score rows, **37** decisions, no changed prior acceptance history.
3. Each new regularised Logit candidate's train-only standardisation, solver/penalty, `l1_ratio`, fixed `C` grid and three-fold inner tuning, plus independently checked inner-fold chosen `C` and nonzero counts.
4. D15 full 16→1 group deletion paths and per-outer-fold subset, one-SE within-path choice, and no data leakage from outer validation labels.
5. Four separately rendered, chronological family history tables covering all **41** trials, source and decision metadata, plus independent full Gini/Entropy pruning audits and six finalists.
6. Winner-only threshold references, finite model parameters and probability bounds, frozen reserved check and all-data refit; source hash, row IDs, fold IDs and historical evidence unchanged.
7. New evidence committed only after **PASS**; `artifacts/prd_v3_4/independent_training_audit.json` and `run_metadata.json` are mandatory and correspond to the saved executed notebook.

## 7. Interpretation limitations

All three are exploratory adaptations proposed after inspecting v3.1–v3.3 CV, so later candidate selection is subject to multiple-search optimism. An accepted change is not established to improve future deployment economics. Our original one-SE hurdle is a heuristic, not a significance test. LDA covariance structure is not rendered Gaussian by variable selection, and regularised coefficients are not suitable for naïve unadjusted inference.

Do not merge into v3.3 or main without review. No new v3.4 AUC claims until execution and independent verification have passed.
