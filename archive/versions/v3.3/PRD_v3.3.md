# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.3

**Frozen design date:** 3 November 2026  
**Branch:** `analysis/prd-v3-3-notebook`, based on the executed v3.2 branch.  
**Scope status:** Seven additional exploratory EDA-driven specifications; execution evidence is a separate acceptance gate.  
**Historical materials:** Keep all v3.0, v3.1 and v3.2 PRDs, executed notebooks, supporting EDA and evidence unchanged.

## 1. Objective

Predict online-shopping session `Revenue=1` from session predictors and choose the taught classifier with the highest **mean five-fold training ROC-AUC**. Prediction, **not** coefficient inference, causal upsell impact or a decision-time deployment claim. Competing families remain Logistic Regression, LDA, Gaussian NB, Bernoulli NB, and independently cost-complexity-pruned Gini and Entropy classification trees.

The user explicitly selected **ALL seven** new hypotheses from the previous discussion. Run **L8, L9, L10, D8, D9, D10 and D11**; do not prefilter to four priority ideas. The seven are exploratory **post-v3.2** proposals, not a fresh independent preregistration. Preserve every unsuccessful v3.1/v3.2 attempt and the strict selection rule.

## 2. Data, splits and preprocessing safeguards

- Original 12,330-session, 17-source-predictor dataset `data/uci_468.csv`. Keep the existing 125 excess exact duplicates for continuity and disclose possible dependence.
- Deterministic original stratified split, seed 42: training 9,864 and historically reused reserved set 2,466. Identical five shuffled stratified training CV folds, seed 42, for every competitor.
- Operational models start with the same **16** source predictors, excluding `PageValues` due to uncertain decision-time availability, **not** proven leakage. Retain six all-17 feature-timing diagnostics and the six operational baselines.
- Fit encoder, any percentile clipping, rare category pooling, scale, median and hyperparameter tuning inside the **appropriate training fold only**. Keep six nominal predictors nominal. Do not create feature representations from validation or holdout targets.
- The historical reserved set was examined in previous versions: v3.3 reserved AUC cannot be represented as a pristine independent model-selection-free evaluation. Run its version-specific winner check only after freezing the training winner, then refit the unchanged recipe to all rows.

## 3. Existing modelling history and starting points

All 31 original-family v3.2 ledger entries remain (L0–L7, D0–D7, G0–G9, B0–B4), including baseline and rejected entries, and the original 16 historical sequential decisions and eleven v3.2 anchored probes.

- Original v3.1 family finalists: L1 Logistic Regression, D0 LDA, G0 Gaussian NB, B3 Bernoulli NB.
- Verified v3.2 family finalists: **L1 Logistic Regression**, **D0 LDA**, **G7 Gaussian NB**, **B3 Bernoulli NB**.
- Original Gini/Entropy tree alpha searches and one-SE simplest-tree selection remain unchanged.
- After adding seven new probes, expected **38 original-family entries**: 20 v3.1 + 11 v3.2 + 7 v3.3. Together with non-ledger diagnostic/tree designs, expect **48 model specification CV results / 240 specification-fold scores** and **34** nonbaseline decisions (16+11+7). Tree-alpha candidate/fold evidence remains audited separately.

Every new probe is a **single, independently anchored transformation of its own v3.2 family finalist**, not a cumulative chain. The frozen anchors are L1 for L8–L10 and D0 for D8–D11. v3.2 and older trials never change their parent or original accepted/rejected evaluation.

## 4. Seven exact new specifications (predeclared before running)

| ID | Family | One new feature change relative to frozen v3.2 anchor | EDA motivation and limitation |
|---|---|---|---|
| **L8** | Logistic | **Replace** raw `BounceRates` with a three-column **piecewise linear** basis: `1[BounceRates>0]`, `min(BounceRates,0.01)` and `max(BounceRates−0.01,0)`; retain all other L1 features unchanged. The fixed positive knot is **0.01** (no tuning). | Training-only bins show a zero mass (44.8%) and a sharp nonuniform decrease in marginal buyer rate as BounceRates increases. Binned marginal purchase rates do not establish conditional curvature; earlier quadratic L5 did not qualify. |
| **L9** | Logistic | Treat `SpecialDay` as **nominal categorical** with fold-fitted one-hot encoding (drop one category, unknown levels ignored), instead of one numeric column. Preserve all other L1 features. | Observed buying rates across SpecialDay 0, 0.2,…,1.0 are nonmonotone and zero-heavy. A discrete representation changes functional flexibility but may overfit sparse levels. |
| **L10** | Logistic | **Add** numeric average duration per product page `ProductRelated_Duration / ProductRelated` where count>0, otherwise 0. Preserve raw count and original L1 `log1p(ProductRelated_Duration)`, etc. No additional transform, tuning or thresholding of this ratio. | EDA records high within-class correlation between count and duration; a ratio tests time spent per visited product page, distinct from total exposure. The ratio's own conditional contribution is **not yet demonstrated** by EDA. |
| **D8** | LDA | Replace raw `ProductRelated` with `log1p(ProductRelated)`; do not log-transform other activity columns. | Strong skewness 4.37 and exceptionally few exact zeros (0.3%) make a targeted transform plausible; whole-six-feature log D1 did not qualify. |
| **D9** | LDA | **Winsorise** `ProductRelated_Duration` at the **99th percentile of that fold's training rows**, replacing larger values with the learned cap; other features unchanged. | Training duration has a long tail (skew 8.01) and large extremes that can dominate covariance estimation; winsorisation differs from log1p by primarily modifying the upper tail. |
| **D10** | LDA | **Add** `1[Informational>0]` while retaining raw `Informational` and all other D0 features. | 78.5% zeros; observed buyer rates at zero and positive were 13.3% versus 23.4%. The contrast can be redundant with other activity features and a binary indicator does not improve Gaussianity. |
| **D11** | LDA | **Replace** raw `BounceRates` with a **three-level nominal category**: exactly zero; low-positive `0<BounceRates<=0.01`; high-positive `BounceRates>0.01`. Fold-fit one-hot encoding with a reference category; thresholds fixed before fitting. | High point mass at zero and marked nonlinear-looking marginal buyer rate; tests a simpler functional representation than a linear numeric LDA coefficient. |

All numerical inputs are finite and the zero denominator in L10 must produce exactly zero (no division by zero). For D9, use `.quantile(0.99)` **inside the outer fold fit and all-data final fit**, not a percentile computed globally from train+holdout or ahead of CV. For D11 and L9, categories are explicitly nominal; one-hot encoding must be trained inside folds.

## 5. Acceptance and six-way selection

For each new probe `m`, compute the **mean of the five validation-fold ROC-AUCs**, their sample SD, `SE_m=SD_m/sqrt(5)`, mean average precision, OOF probabilities, warnings and its exact frozen parent.

`delta_m = mean_AUC(m) - mean_AUC(v3.2_family_anchor)`.

A new probe **qualifies only if `delta_m > SE_m`**, strictly; this is the unchanged heuristic, **not** a statistical test of the paired model difference. If several probes for the same family qualify, choose the highest mean CV AUC among qualifying individual modifications, breaking exact ties by ascending step ID. If none qualify, retain the v3.2 family finalist. Never combine multiple qualifying new feature changes post hoc.

Choose the final overall winner using **mean five-fold ROC-AUC** across the updated Logit, LDA, unchanged G7 GNB, unchanged B3 BNB, selected Gini and selected Entropy. Mean AP, OOF pooled ROC, PR curves and fold variability remain supporting information; no holdout/AP/cost-based retrospective re-ranking.

## 6. Preserved trees, thresholds and provenance

Retain full-grown Gini/Entropy trees, independent fold-based full alpha-path searches, exclude root-only terminal pruning point, and select the **fewest-leaf** tree within one SE of the best CV alpha, exactly as in v3.2. Both selected trees enter the six-way final comparison. No new trees, QDA, KNN or mixed likelihood models.

Retain winner-only training OOF displays, ROC and precision–recall plots, sensitivity/specificity and four pre-existing threshold references. The hypothetical illustration assumes S$3 contact cost, 30% conditional upsell success and S$50 margin, giving assumed false-positive/false-negative costs of S$3/S$12 and a 0.20 threshold; sensitivity scenarios remain assumptions, not measured uplift or validated profitability.

Preserve the data hash, row IDs, shared CV fold IDs, original model ledger and all v3.2 evidence. Write **only new output** under `artifacts/prd_v3_3/`; save a new executed `online_shoppers_prd_v3_3.ipynb` plus independent audit and metadata.

## 7. Execution acceptance contract

A v3.3 outcome can be reported as verified **only after** an execution run that:

1. Validates the new notebook format and compiles all 20 Python code cells; executes every cell with no error outputs.
2. Confirms **38 ledger entries** and the seven predeclared v3.3 IDs; 20 v3.1 + 11 v3.2 + 7 v3.3, **48** specification CV results and **240** fold result rows, and **34** one-SE comparisons.
3. Recomputes all specification-fold ROC-AUC and AP from the saved OOF vectors; verifies 7 v3.3 one-change parents, gain/SE decisions and correct winner among qualified anchored alternatives.
4. Independently audits full Gini and Entropy pruning alpha paths, eligible one-SE regions, selected leaf complexity and six finalists.
5. Validates four threshold references, finite fitted parameters and probabilities, complete provenance and one version-specific (historically reused) reserved check.
6. Saves the executed notebook and resulting artefacts on the v3.3 branch **after** validation, with no edits to earlier versioned notebook/PRD/evidence paths.

Any new v3.3 choices are post-v3.2 exploratory and expand the search beyond the professor's approximately 3–5 changes per original path. Document this limitation explicitly; do not seek a forced accepted LDA transformation.
