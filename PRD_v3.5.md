# DSA211 — Predicting Online Purchases
## PRD v3.5 — Approved EDA-complete, streamlined notebook presentation

**Current revision:** 3 November 2026. **Active branch:** `main` (merged from `analysis/prd-v3-5-presentation` via PR #15).  
**Current notebook:** [online_shoppers_prd_v3_5.ipynb](online_shoppers_prd_v3_5.ipynb).  
**Frozen modelling origin:** [archived executed v3.4](archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb) · [verified v3.4 evidence](artifacts/prd_v3_4/) · [source supplementary EDA](supplementary/training_eda.ipynb).  
**Nature of revision:** Reformatting and inclusion of previously executed EDA only; **no new modelling, new AUC claims or threshold optimisation**.

## 1. Frozen scientific objective and protocol

Predict `Revenue=1` for an online browsing session, using the 16 operational predictors. The 17th source predictor `PageValues` is excluded as a cautious decision-time availability judgment, **not** demonstrated label leakage.

The source has 12,330 observations and the frozen seed-42 stratified partition includes 9,864 training and 2,466 historically consulted reserved observations. Every original model uses the same five shuffled stratified training folds and leakage-safe fold-specific preprocessing. Original v3.1 sequential, v3.2/v3.3 anchored and v3.4 sequential experiments remain unaltered.

Historical acceptance is **mean challenger five-fold ROC-AUC minus mean parent five-fold ROC-AUC strictly greater than challenger's own five-fold AUC SE**. It is an exploratory heuristic, **not** a formal significance test. Retained overall champion **L1 Logistic Regression**: training mean ROC-AUC **0.75746739** and AP **0.33622615**; historically reused reserved-set AUC **0.74054250**, AP **0.32719856**. The reserved set is **not pristine**; no causal upsell-effect claim is justified.

## 2. EDA completeness — integrate all used supporting investigations

The main notebook must retain its original data-quality, numerical, categorical and predictor-assumption EDA **and directly incorporate** all substantive supplementary training-only analyses, with their **original saved outputs** (not newly computed models):

1. **Zero versus positive activity and intensity**: all six activity variables' zero/positive session support, buyer rates, positive quantiles, positive-intensity bins. This supports log1p and positive-presence hypotheses (especially L7, D10).
2. **VisitorType × Month**: observed cross-cell sample counts and purchase rates, chart, sparse cell check. This informed the decision not to force an interaction from a few thin cells.
3. **Rare nominal levels**: full training-level support/rates for Browser, TrafficType and Region, including 13 of 42 levels with fewer than 50 observations. This motivates cautious one-hot modelling and warns against overinterpreting rare levels.
4. **SpecialDay raw score versus presence**: per-score support/rate, zero-versus-positive contrast and plot, previously used to consider representation trials (even though excluded from the final 26 displayed shortlist).
5. **Timing/availability assessment**: all 17 source predictors with what they measure and plausible time-of-availability issues. This is critical support for omitting `PageValues` but does not certify other predictors as real-time-safe.
6. **Detailed shapes and conditional evidence**: numerical skew/zero shares/p95, within-class correlation summaries, six binned marginal empirical-logit tables, and four original distribution plots. These motivate skew, nonlinear and dependence-aware trials without establishing multivariate Gaussianity or causality.

The supplementary data-quality/split check is already represented by the original main data-quality section; avoid needless duplicate code. All included EDA must be **training-only** and clearly labelled **descriptive**. Reuse the original executed supplementary outputs and code adapted to the frozen main training partition. Preserve the supplementary source notebook as supplementary evidence.

## 3. Exact curated experiment tables and on-screen rationales

**Reference only:** The detailed matrices below preserve the locked trial IDs, EDA motivations, exact parents and historical decisions. **They are NOT the display format of the current notebook**. The notebook's own tables show **numbers only**—ID, CV ROC-AUC, AUC SE, AP and AUC gain. Immediately *under* each table, one explanation per iteration reports the change, parent, EDA rationale and acceptance. No unshortlisted model appears in the main model-family tables.

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


## 4. Final notebook presentation and ordering

1. Keep Sections **0–4** (protocol, source quality, numerical EDA, categorical EDA and predictor assumptions), now with the complete detailed training EDA of Section 2 visibly embedded **under the corresponding EDA sections**. Explain why the evidence motivated the experiments.
2. Keep **six all-17 first-pass diagnostics** and **six operational baselines** as separate numerical comparisons. Do not convert baseline specifications into post-baseline accepted changes.
3. **Remove the former 6A course-methods matrix entirely.** Lecture 8's grouped backward selection appears under D15; Lecture 9's Ridge/LASSO/Elastic Net adaptations appear under L4/L13/L14. Do not claim that unrelated OLS-only syllabus methods were fitted.
4. Present **four separate model-family subsections** with exactly **7 / 7 / 7 / 5 numeric-only result rows**, in the locked order from Section 3. Each table has only **ID, CV ROC-AUC, AUC SE, CV AP and AUC gain**.
5. **Directly below each numeric table**, explain **every displayed iteration**, including the actual historical parent, exactly what was changed, the supporting EDA/theoretical motivation, and whether accepted. Correctly identify D0 as **Baseline**. Preserve L7's higher-but-unaccepted AUC and G6/G7's independent qualification vs G0.
6. **Bernoulli NB conclusion:** five original trials suffice. The three **retained pathway stages** are B0 baseline, B1 accepted, B3 accepted; **only B1 and B3 are accepted improvements**. Stop trying more variations after B4 fails. Do not falsely say there were three accepted improvements.
7. **Remove the previous 7.5 historical-evidence heading** from the visible notebook; the complete 41-attempt ledger remains accessible in the frozen artefacts, with its original code-generated evidence preserved.
8. Present two independently pruned trees as four full-versus-pruned rows. **Move the illustration of the selected Entropy tree into the tree section, BEFORE the six-way overall model comparison**; explain it is the stronger *tree finalist*, **not** the overall winner.
9. Keep the subsequent **six-way final comparison**, original winner OOF score distributions, ROC/PR, reliability, four thresholds, cost sensitivity, historically reused reserved check, final refit and limitations **unchanged in their substantive numerical findings**.

The result should read **EDA → modelling hypothesis → numerical comparison → decision narrative → overall selection**, not a wall of wide justification tables.

## 5. Invariants and source of truth

- **Four original-family shortlists:** 7 Logistic, 7 LDA, 7 Gaussian NB and 5 Bernoulli NB; 26 displayed, 41 historical trials preserved.
- **Unchanged metrics/evaluation:** 51 scored model designs, 255 fold scores, 37 original-family nonbaseline decisions, 80 D15 subset-path entries, 722 tree alpha candidates and 3,610 tree-alpha fold results.
- **Unchanged source/statistics:** data SHA, partition, folds, model specifications, coefficients, winner, OOF scores, six finalists, fit diagnostics, thresholds and reserved check.
- **Preserved archive:** no rewriting archived v3.0–v3.4 notebooks/PRDs or the original `artifacts/prd_v3_4/` evidence.
- **Presentation integrity:** the newly embedded supplementary EDA outputs and three supplementary PNGs match the original `supplementary/training_eda.ipynb`; the seven original notebook figures remain.
- **Notebook correctness:** all original computational model and statistical audit code remains; no error outputs; every code cell passes syntax compilation. A **presentation-only audit** verifies these properties without refitting any model.
- **Branch:** `main`; merge approved by user and completed in PR #15.

## 6. Hand-off and verification

The notebook is the active v3.5 submission candidate on `main`. The Python verification script `scripts/verify_prd_v3_5_presentation.py` and [GitHub Actions workflow](.github/workflows/verify-prd-v3-5.yml) must report **PASS** against the archived original, the complete v3.4 ledger and original supplementary EDA. The suite performs **no model training**.

The inclusion of earlier executed EDA does not make its descriptive relationships causal, nor does the reuse of historical CV folds or reserved observations create new independent validation.
