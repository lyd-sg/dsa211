# DSA211 — model revision decisions and regularisation evidence log
**26 October 2026 · supersedes prior exact revised-model recipes for this exploratory comparison**

## Research objective and fixed comparison

The single aim is **predictive classification** of `Revenue`. Compare **exactly seven** operational candidates on identical five-fold stratified training CV (mean ROC-AUC primary, average precision and between-fold variability secondary). Retain the four minimally processed baselines. Modify only the three existing *revised* slots, preserving their earlier EDA-supported feature treatments. Choose the model with highest CV ROC-AUC regardless of family.

The strengths `C=1.0` for L2 Logit and `shrinkage='auto'` for LDA are specified before the revised candidate comparison: there is **no nested or post-hoc hyperparameter search**. For L2, encoded predictors are standardised with `StandardScaler` fitted only on the fold training rows; the intercept is not penalised. The chosen L2 penalty is a reasonable first hypothesis, **not** a claim to have found an optimal penalty. The baseline Logit stays unpenalised (`C=np.inf`), and baseline LDA stays standard SVD.

## Three revisions: changes, statistical reasons and what they do not prove

| Model | Exact change versus its operational baseline | EDA / model motivation | Prediction hypothesis | What the result cannot establish |
|---|---|---|---|---|
| **Revised Logit** | Log-transform six activity magnitudes; fit-fold positive indicators only for activity fields ≥50% zero; scale all encoded predictors within each fold; logistic L2 penalty **C=1.0**. All 16 original operational predictor sources retained. | Activity counts/durations are heavily right-skewed and several have substantial zero masses. Within-class BounceRates–ExitRates and product count–duration correlations are high. Pure/rare outcome category levels appeared in previous numerical checks. | Shrinkage may reduce variance and stabilise coefficients and predictions; log/presence terms may better represent extreme and absent activity. | Cannot separately attribute gains to L2, scaling or the log/presence transformations; regularisation might lower AUC. The categorical rarity issue is not fully eliminated by regularisation. |
| **Revised LDA** | Log-transform the same six activity variables; use `LinearDiscriminantAnalysis(solver='lsqr',shrinkage='auto')` for fit-fold covariance shrinkage; all 16 sources retained, k−1 encoding. | Long numeric tails challenge Gaussian approximations; strong within-class correlations and many indicators create a potentially unstable covariance estimate. | Shrinking estimated covariance may reduce estimation variance and improve held-out ranking. | LDA permits correlated predictors. Correlation does **not** by itself violate LDA, and shrinkage does not guarantee Gaussianity, shared class covariance or improved AUC. |
| **Revised MixedNB** | As before: Gaussian likelihood on six log-activity magnitudes and two rates; categorical likelihoods for six nominal sources, Weekend and presence of SpecialDay; discrete Laplace smoothing `alpha=1`. | Numeric magnitudes and nominal levels cannot all be modelled naturally by one Gaussian or one Bernoulli likelihood; zero-heavy activity is also a concern. | Better matching of marginal data types than either all-Gaussian or all-Bernoulli NB. | The conditional-independence assumption remains questionable for correlated predictors. `alpha=1` is smoothing, not a new L1/L2 penalty. |

**Evidence is a justification for testing, not proof of improvement.** Because the original revised models already contained feature engineering, the new revised-versus-baseline AUC differences represent the effects of the *whole* recipe.

## Evaluation governance

The project has already examined test observations in prior versions, including the former 80/20 historical test. The reopened seven-candidate comparison thus uses the **original 9,864 training rows only**, and the source notebook explicitly **does not rescore its prior test holdout**. A fresh unbiased new-version test score cannot be produced from these previously viewed observations. The 25 October `artifacts/test_metrics.json`, prior frozen decision, historical verification report and full-data model refer to **the earlier unpenalised recipe**, not to the new candidate ranking.

The new notebook writes *separate*, training-only revision artifacts and prints all seven mean CV ROC-AUC scores. Any observed winner is a **training-CV winner**, not proof of external deployment superiority.

## Implementation status

- Notebook edit: new revised pipelines, in-fold standardisation for L2 Logit, automatic LDA covariance shrinkage, appropriate model-specific numerical gates.
- Run: GitHub Actions `Validate DSA211 revised notebook` on the review branch; record the exact execution status before merging to `main`.
- Numeric results and selected candidate are determined by execution, not inserted by hand.
