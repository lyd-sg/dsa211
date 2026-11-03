# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.5: concise, EDA-grounded final presentation

**Frozen presentation specification:** 3 November 2026.  
**Source of truth:** [PRD v3.4](archive/versions/v3.4/PRD_v3.4.md), [fully executed v3.4 notebook](archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb) and the [v3.4 all-trials ledger](artifacts/prd_v3_4/all_attempts_ledger.csv).  
**Isolated development branch:** `analysis/prd-v3-5-presentation`, based on successful executed v3.4 branch `analysis/prd-v3-4-notebook`.  
**Work authorised now:** **PRD only.** Do **not** edit, recreate, execute, commit or regenerate any notebook, numeric result, plot, audit, modelling recipe or data artefact during this phase.

## 1. Purpose and decisions frozen

Version 3.5 is a **presentation-only curation** of the completed prediction project. The final notebook will be designed to read as a defensible EDA → hypothesis → experiment → CV outcome → retain/revert narrative rather than presenting every historical trial. All 41 original-family trial records remain discoverable and auditable; the reader sees **no more than seven per family** in the main report.

**Final visible original-family shortlist (26 total):**

- **Logistic Regression (7):** L0, L1, L4, L7, L8, L13, L14.
- **LDA (7):** D0, D1, D4, D9, D10, D11, D15.
- **Gaussian NB (7):** G0, G1, G2, G3, G6, G7, G8.
- **Bernoulli NB (5):** B0, B1, B2, B3, B4.
- **Trees:** exactly four main comparison rows, *full* and *selected pruned* for each of Gini and Entropy; both complete alpha paths remain in supplementary evidence.

A baseline is included because it is the **baseline**, not because an EDA observation recommended it. In particular, **D0's rationale column must say exactly "Baseline".** D0 is the final retained LDA specification only because no LDA challenger satisfied the existing acceptance rule. Do not invent an EDA-based explanation for choosing D0, or claim it was accepted through an improvement test.

**Historical modelling results are frozen:** winner L1 Logistic Regression, five-fold training mean ROC-AUC 0.75746739, historically reused reserved ROC-AUC 0.74054250. No more model searches or threshold optimisation are authorised in v3.5.

## 2. Non-negotiable preservation rules

1. **Source data/protocol unchanged:** UCI 12,330 rows, the established 9,864/2,466 stratified split (seed 42), same five outer training folds and 16 operational predictors, with PageValues excluded as a decision-time availability precaution, not established leakage.
2. **No statistical recomputation:** Preserve original definitions, results, fit warnings, penalties, inner CV, selected source subsets, fold IDs, all OOF probabilities, tree-alpha searches, thresholds, full-data refit and reserved check. The reserved set has already been consulted across versions and is **not pristine**.
3. **All original experiments remain:** exactly 41 original-family attempts (20 v3.1 + 11 v3.2 + 7 v3.3 + 3 v3.4), 51 scored designs (including diagnostics/baselines/selected trees), 255 five-fold score rows, 37 nonbaseline acceptance decisions and 80 D15 backward-path rows. The 26 displayed rows are a *view*, not a new 26-model rerun.
4. **Historical accept/reject decisions are immutable:** use gain > challenger five-fold AUC SE (strict), respecting each trial's **actual historical comparison parent**. v3.2/v3.3 trials were independently anchored; L13/L14 followed the v3.4 sequential rule. The internal D15 one-SE subset-size selection is a distinct procedure.
5. **No post-hoc explanations presented as proof:** label reasons as *EDA-motivated hypotheses*, never as validated causality or a demonstration that the observed effect is driven by a specific mechanism. A trial may show a higher mean AUC and still fail the fixed acceptance hurdle.
6. **Version isolation:** the future presentation notebook, if authorised, will be a new `online_shoppers_prd_v3_5.ipynb`, with any future presentation-only assets under `artifacts/prd_v3_5/`; none are to be created in the current PRD-only phase. Never overwrite v3.0–v3.4 notebooks, PRDs or evidence.
7. **Show all course-method coverage as a truthful status matrix:** distinguish "applied", "considered but not fitted", "not applicable to binary classification" and "marked not examinable". Do not mislabel unimplemented methods as experiments.

## 3. Exact curated experiment tables and on-screen rationales

**Main notebook display contract:** Render **one independent family table**, in the order below, with columns **ID**, **actual comparison parent**, **change tested**, **EDA rationale / baseline purpose**, **mean five-fold CV ROC-AUC** and **historical decision**. The following are the *locked trial IDs, EDA rationales and verified v3.4 values*. Rationale must be immediately visible in the family table (not only in a distant methodology section). When displaying, also show the recorded AP and challenger AUC SE where space allows, but never substitute other values or alter the decision.

### 3.1 Logistic Regression — exactly 7

| ID | Parent | Change tested | EDA rationale / purpose | Mean 5-fold CV ROC-AUC | Historical decision |
|---|---|---|---|---:|---|
| L0 | — | Operational 16-predictor baseline | Baseline; no EDA hypothesis | 0.75002 | Baseline |
| L1 | Operational16 | log1p on six activity predictors | All six activity variables are right-skewed, notably ProductRelated_Duration (skew 8.01) and Informational_Duration (7.70); log1p preserves zero readings | 0.75747 | Accepted; **retained** |
| L4 | L1 | Standardised L2-penalised Logit, inner-CV C | Strong within-class correlations, including BounceRates–ExitRates (0.915 nonbuyers; 0.723 buyers), motivate regularisation (Lecture 9) | 0.75787 | Not accepted |
| L7 | L1 | ProductRelated_Duration positive-presence indicator | ProductRelated_Duration is extremely skewed (8.01), with 6.2% zeros; test whether zero versus any activity adds information beyond amount | 0.76014 | Not accepted |
| L8 | L1 | Fixed-knot piecewise-linear BounceRates | BounceRates is zero in 44.8% of sessions and skewed (2.92); examine a possible nonlinear predictive effect without claiming EDA chose the knot | 0.75862 | Not accepted |
| L13 | L1 | LASSO (L1) Logistic, inner-CV C | Redundant and correlated features motivate sparse shrinkage, a classification adaptation of Lecture 9 | 0.75848 | Not accepted |
| L14 | L1 | Elastic Net Logistic (fixed L1 ratio 0.5), inner-CV C | Correlated predictor blocks motivate combined L1/L2 shrinkage (Lecture 9), replacing rather than stacking the LASSO penalty | 0.75828 | Not accepted |

**Required interpretation:** L1 is the sole accepted and retained Logistic revision. Although L7 had the highest displayed point-estimate AUC (0.76014), its gain over L1 (0.00267) did not exceed its own SE (0.00563); it cannot replace the retained model under the frozen heuristic. L4, L13 and L14 demonstrate Lecture 9 L2 / LASSO / Elastic Net coverage, with all coefficients and tuning fitted inside appropriate folds. L14 compares against L1 because L13 did not pass; its penalty replaces rather than stacks L13.

### 3.2 Linear Discriminant Analysis — exactly 7

| ID | Parent | Change tested | EDA rationale / purpose | Mean 5-fold CV ROC-AUC | Historical decision |
|---|---|---|---|---:|---|
| D0 | — | Operational 16-predictor LDA baseline | Baseline | 0.74088 | Baseline; **retained** |
| D1 | Operational16 | log1p on six activity predictors | Strong right-skew and non-normal duration Q–Q plots motivate checking more Gaussian-like marginal inputs | 0.74373 | Not accepted |
| D4 | Operational16 | Inner-CV covariance shrinkage | Within-class predictor correlations motivate testing stability of the shared pooled covariance estimate | 0.74088 | Not accepted |
| D9 | Operational16 | Training-fold p99 winsorisation of ProductRelated_Duration | Extreme ProductRelated_Duration right tail (skew 8.01) motivates assessing outlier sensitivity | 0.74301 | Not accepted |
| D10 | Operational16 | Informational > 0 indicator | Informational is zero for 78.5% of training sessions; presence may capture a distinct engagement signal | 0.74170 | Not accepted |
| D11 | Operational16 | BounceRates zero / low-positive / high-positive bands | BounceRates is zero in 44.8% of sessions; test whether coarse categories help or discard useful continuous information | 0.73634 | Not accepted |
| D15 | Operational16 | Nested grouped backward-stepwise LDA | Strong correlations among source predictors motivate deleting redundant source groups; demonstrates Lecture 8 subset selection without dummy-level cherry-picking | 0.73411 | Not accepted |

**Required interpretation:** The inclusion rationale for **D0 is "Baseline"**. It remains the family finalist because *none* of the tested revisions met the acceptance threshold. D1/D9 inspect skewness sensitivity, D4 the pooled covariance, D10 zero-heavy inputs, D11 information loss from coarse categorisation, and D15 nested, group-wise backward selection (Lecture 8). Do not claim that modifying univariate marginals establishes multivariate Gaussian assumptions.

### 3.3 Gaussian Naive Bayes — exactly 7

| ID | Parent | Change tested | EDA rationale / purpose | Mean 5-fold CV ROC-AUC | Historical decision |
|---|---|---|---|---:|---|
| G0 | — | Operational 16-predictor Gaussian NB baseline | Baseline; no EDA hypothesis | 0.69202 | Baseline |
| G1 | Operational16 | log1p on all six activity predictors | Strong skewness motivates a blanket Gaussian-marginal adjustment; included as a diagnostic negative comparison | 0.67163 | Not accepted |
| G2 | Operational16 | Drop BounceRates (keep ExitRates) | Within-class BounceRates–ExitRates correlations of 0.915 (nonbuyers) and 0.723 (buyers) challenge NB conditional independence | 0.68882 | Not accepted |
| G3 | Operational16 | Drop ProductRelated (keep its duration) | ProductRelated–ProductRelated_Duration correlations of 0.839 (nonbuyers) and 0.896 (buyers) imply redundant information under NB | 0.68927 | Not accepted |
| G6 | Operational16 | Drop ProductRelated_Duration (keep count) | Compare which member of the highly correlated ProductRelated pair is more useful under Gaussian NB | 0.70776 | Qualified vs G0; not selected |
| G7 | Operational16 | log1p ProductRelated_Duration only | This duration is extremely right-skewed (8.01); a targeted marginal transformation tests whether blanket transformations are unnecessary | 0.71284 | Qualified vs G0; **retained** |
| G8 | Operational16 | log1p Administrative_Duration only | Administrative_Duration is highly skewed (5.68) with 47.7% zeros; test a second targeted marginal repair | 0.69514 | Not accepted |

**Required interpretation:** Gaussian NB's conditional independence assumption is put under pressure by the observed strong within-class correlations. G6 and G7 were **both qualified against the independent G0 baseline anchor**, not sequentially against each other; G7 had the higher mean AUC and became the finalist. Show why selective right-skew correction G7 outperformed the all-six blanket change G1. Do not misstate G6 as rejected.

### 3.4 Bernoulli Naive Bayes — all 5

| ID | Parent | Change tested | EDA rationale / purpose | Mean 5-fold CV ROC-AUC | Historical decision |
|---|---|---|---|---:|---|
| B0 | — | Operational 16-predictor Bernoulli NB baseline | Baseline; no EDA hypothesis | 0.72313 | Baseline |
| B1 | Operational16 | ProductRelated threshold: positive presence -> training-fold median | ProductRelated count is right-skewed (4.37) but nearly always positive (0.3% zeros); presence alone may discard useful variation | 0.73160 | Accepted; later superseded |
| B2 | B1 | ProductRelated_Duration training-fold median threshold | Duration is extremely right-skewed (8.01); median threshold tests a more discriminating binary representation | 0.73882 | Not accepted |
| B3 | B1 | ExitRates training-fold median threshold | ExitRates is continuous and right-skewed (2.13); median split tests information beyond the default binary encoding | 0.74227 | Accepted; **retained** |
| B4 | B3 | Drop BounceRates | High BounceRates–ExitRates dependence motivates removing a potentially redundant Bernoulli NB input | 0.73974 | Not accepted |

**Required interpretation:** Retain the entire small family. B1 was accepted and became the anchor for B2 and B3. B2 was not accepted; **B3 was accepted against B1** and retained. B4 was then tested against B3 and rejected. These are *training-fold median* thresholds when the method specifies a median, not transformations computed on the full dataset before CV.

### 3.5 Tree methods — four display rows only

| Family | Display row | Mean 5-fold CV ROC-AUC | Explanation required |
|---|---|---:|---|
| Gini tree | Operational16 unpruned | 0.57663 | Baseline full tree; assess overfitting |
| Gini tree | Selected cost-complexity pruned | 0.73306 | Fold-CV pruning path, one-SE simpler-tree rule; final 8 leaves, depth 4 |
| Entropy tree | Operational16 unpruned | 0.57973 | Baseline full tree under entropy split criterion |
| Entropy tree | Selected cost-complexity pruned | 0.74414 | Independent fold-CV pruning path, one-SE simpler-tree rule; final 14 leaves, depth 6 |

The displayed tree rows are **not** part of the seven-row limit per original classifier family. Preserve all 722 alpha-path candidates and their 3,610 fold scores; put the full pruning audit in the retained supplementary files, not as hundreds of visible notebook rows.

## 4. Final notebook narrative, ordering and visual requirements

When notebook work is separately authorised, keep the existing EDA, plots, model and reserved-check evidence; replace the *main displayed experiment-history views* with the sections below. Avoid new data exploration or model training solely to improve storytelling.

1. **Prediction objective and original data protocol.** Define Revenue=1 and the six-family comparison. Explain why PageValues is removed, avoiding an unsupported leakage assertion.
2. **Compact numerical/categorical EDA → explicit hypotheses.** Retain source-backed quantities: Informational 78.5% zero, Informational_Duration 80.5% zero, ProductRelated_Duration skew 8.01, Administrative_Duration skew 5.68, BounceRates 44.8% zero; within-class BounceRates–ExitRates correlations 0.915/0.723, ProductRelated–duration 0.839/0.896; categorical rare Browser/TrafficType levels. Connect each observation to the corresponding trial IDs. No invented diagnostic findings.
3. **Six all-17 versus operational-16 diagnostics.** One compact comparison, not additional hidden versions of family development tables.
4. **Course-method coverage table (Section 5 below).** Demonstrate conscious choice of methods across the taught module without falsely suggesting all possible algorithms were fitted.
5. **Four independent family development sections**, in this order: Logistic 7, LDA 7, GaussianNB 7, BernoulliNB 5. Each table must contain its own visible rationale column, parent and honest accepted/not accepted label, followed by **one short family-specific interpretation paragraph** explaining what the EDA predicted, what CV found, and why the retained model survived.
6. **Two independent tree paths summarised as four rows**, with their own brief explanation of why pruning matters. Do not display every alpha candidate in the main report.
7. **Unchanged six-way finalist table and existing ROC, PR and calibration plots**, threshold comparisons, hypothetical business assumptions, historically reused reserved-set check, final fit and limitations. The winner is unchanged by presentation choices.
8. **Supplementary full-history link / appendix** to the machine-readable all-41 attempt ledger, 51-design/five-fold evidence and independent PASS audit. If a reader wants omitted candidate results, they must remain accessible without being presented as extra main-table rows.

**Displaying findings:** Baselines and accepted retained trials must be distinguished from unsuccessful experiments. Put factual EDA reasons, including numerical evidence where available, in every displayed rationale. The AUC and acceptance decision must be shown **alongside** each trial. No statements of formal significance, causality, confirmed future economic value or fresh independent holdout generalisation.

## 5. Explicit course-method consideration matrix

Add the following compact matrix to the final notebook. It is a **methodological coverage statement**, not a claim that every taught technique was fitted. Preserve lecture naming and distinguish techniques taught for a continuous response from those adapted to the binary target.

| Lecture/topic | Relevant methods taught | Project coverage and honest status |
|---|---|---|
| Lecture 1: EDA | Numerical and categorical summaries, plots, skew, outliers, predictor relationships | **Applied:** EDA sections drive the annotated family experiments |
| Lectures 2–4: Linear Regression and diagnostics | Simple/multiple OLS, interactions, linear-model assumptions, residual/influence diagnostics, collinearity | **Considered/partly transferred:** continuous-response OLS and its specific inference/residual diagnostics are not fitted as the binary classifier; collinearity, transformations and model-complexity reasoning inform the workflow |
| Lecture 5: Logistic Regression | Logistic probabilities, classification threshold and interpretation | **Applied:** L0–L14 historical pathway, seven displayed |
| Lecture 6: Generative classification | LDA and Naive Bayes | **Applied:** D0–D15, G0–G9, B0–B4; KNN explicitly labelled *not examinable* in lecture, so not claimed as a missing experiment. QDA is not added under the frozen scope |
| Lecture 7: Validation and CV | Training/reserved split, five-fold CV, stratification, pipelines, ROC/PR and related metrics | **Applied:** fixed folds, leakage-safe tuning and final evaluation |
| Lecture 8: Model selection | Best subset, forward/backward stepwise, AIC/BIC, CV and one-SE parsimony | **Applied:** D15 group-wise nested backward selection with one-SE size choice. **Considered but not separately fitted:** exhaustive best subset, forward stepwise and AIC/BIC specifications (principally taught in linear-model setting) |
| Lecture 9: Regularisation and dimension reduction | Ridge, LASSO, Elastic Net, cross-validated penalty choice; PCR/PLS overview | **Applied classification adaptations:** L4 L2, L13 LASSO and L14 Elastic Net. **Considered but not fitted:** PCR/PLS, presented as course overview rather than claimed binary-classifier results |
| Lecture 10: Tree-Based Methods | Regression/classification trees, Gini/Entropy splits, cost-complexity pruning | **Applied:** independently chosen Gini/Entropy classification trees, full-versus-pruned comparison. Regression trees are inappropriate for the binary classification objective |

**Do not state that every regression-only method was implemented.** The objective is coverage of course reasoning and a justified choice of applied methods, not indiscriminate extra trials. An unimplemented item should have a brief defensible reason, not fabricated numbers.

## 6. Frozen statistical interpretation and result limitations

- The retained six-way ranking in the verified v3.4 training CV is: **L1 Logistic 0.75747**, Entropy tree **0.74414**, B3 Bernoulli NB **0.74227**, D0 LDA **0.74088**, Gini tree **0.73306**, G7 Gaussian NB **0.71284**.
- A higher point-estimated AUC for a rejected modification is **not** a rule violation. The original one-SE hurdle is a descriptive conservative selection heuristic, *not* a paired significance test or proof of equal predictive quality.
- More attempted candidates on the same shared CV folds create multiple-search optimism. The final shortlist is **post-hoc editorial curation of executed results**, not a new pre-registered model-selection procedure.
- Holdout v3.4 ROC-AUC **0.74054** / average precision **0.32720**, but the reserved set has been consulted in earlier versions and is **not a pristine new test set**.
- The dataset retains the original excess exact duplicates for comparability; note potential CV-fold dependence, source-metric limitations, model-assumption violations and hypothetical nature of business-cost examples.
- The project is **prediction-focused**. Avoid causal, inference and guaranteed commercial-uplift claims.

## 7. Acceptance criteria for the future presentation notebook

No execution is requested in this PRD-writing phase. If a separate notebook-build instruction is later given, the implementation is complete only when all of the following hold:

1. Four main tables contain **exactly 7 / 7 / 7 / 5** *uniquely identified* rows, in the locked order of Section 3, with no omitted baseline or newly invented ID. Each has **a visible rationales column**, including **D0: Baseline**.
2. Every displayed AUC, AP/SE if included, parent, historical accepted/rejected/superseded status and retained model matches the verified original `artifacts/prd_v3_4/all_attempts_ledger.csv`. Special checks: L7 higher AUC but rejected; G6 qualified but not chosen; G7 final; B1 → B3; L13/L14 rejected; D15 rejected.
3. The model-family tables each have concise EDA → trial → outcome → retain/revert interpretation. Every nonbaseline trial rationale is tied to an EDA observation, a course-taught technique, or both. Do not present those hypotheses as demonstrated causal explanations.
4. A separate methods matrix truthfully distinguishes applied versus considered/not fitted/out-of-scope course material, especially Lecture 8 and 9 techniques; no unsupported assertion that all methods were trained.
5. Four tree comparison rows, six all-17 diagnostic models, all six operational baselines and the six-way finalist ranking remain visible in their appropriate *separate* sections. The seven-per-family display cap is not used to delete these important comparisons.
6. All 41 historical attempts, 51 designs, 255 scored folds, 37 acceptance decisions, 80 D15 nested path records and 722 tree alpha candidates remain accessible and unchanged in the authoritative evidence. The original independent v3.4 training audit remains **PASS**.
7. No change in source hash, train/test row membership, seeds, preprocessing, model coefficients, fitted predictions, thresholds, selected winner, reserved check, test data usage, or audit meaning. If a derived presentation file is later generated, verify it traces to the frozen data rather than silently rerunning feature searches.
8. No pre-emptive update of `main` or past versioned files. Future work must occur on its own isolated branch, undergo user review and not be merged automatically.

## 8. Current handoff

**Authorised deliverable:** This `PRD_v3.5.md` file, committed on the separate v3.5 branch.  
**Not authorised yet:** v3.5 notebook implementation, edits to the executed v3.4 notebook, any reruns, new analyses, changes to project acceptance criteria, or a merge.

The next step requires an explicit instruction to rebuild the presentation notebook against this frozen specification.
