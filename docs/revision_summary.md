# Revision change log and executed results

## Changes

- Reduced the active notebook to Logistic Regression, Gaussian Naive Bayes and LDA. Removed QDA, Yeo–Johnson and quantile-transform experiments, imports and prose.
- Archived the prior executed notebook and original full-project notebook byte-for-byte. The only current project notebook at the repository root is `online_shoppers_revised.ipynb`.
- Compared raw, `log1p` and fold-fitted `zeroind` for all three classifiers. Preserved logistic L2 `C=0.1` and `C=10`, numerical interactions, the predeclared five-predictor logistic model, GaussianNB smoothing and LDA shrinkage. Retained the existing raw mixed NB and numeric-only LDA alternatives.
- Added a dynamic CV-AUC comparison of retained transformations and variants, generated from the current fold results, and reported 1:4 weighted opportunity cost in training/test summaries.
- Kept the 75/25 stratified split (seed 42), five stratified training folds, ROC-AUC selection, training OOF revenue threshold selection, historical test comparison and existing workflow.

The latest user clarification resolved the pasted brief's conflicting 5:1 instruction: retain the latest notebook's 1:4 voucher-revenue objective.

## Execution and baselines

All 21 code cells executed from first to last. All 20 candidate designs completed; 9 candidates were eligible and 0 failed. Rare unseen validation categories produced expected one-hot encoder warnings; the fits still completed. The historical test partition had previously been inspected and does not provide fresh independent confirmation.

| First-pass model | Mean five-fold ROC-AUC |
|---|---:|
| Logistic Regression, all 17 | 0.894718 |
| Gaussian Naive Bayes, all 17 | 0.698642 |
| LDA, all 17 | 0.900502 |

| Operational raw baseline | Mean five-fold ROC-AUC | Fold SD |
|---|---:|---:|
| Logistic Regression, 16 predictors | 0.754075 | 0.021676 |
| Gaussian Naive Bayes, 16 predictors | 0.660601 | 0.051285 |
| LDA, 16 predictors | 0.742414 | 0.020139 |

The eligible winner was Logistic Regression with `zeroind`, selected by highest mean training-CV ROC-AUC. Its threshold was 0.800000, optimized from training OOF simulated revenue under the retained assumptions.

| Metric | Training CV/OOF | Historical test |
|---|---:|---:|
| Mean fold ROC-AUC ± sample SD | 0.761161 ± 0.022013 | — |
| Pooled ROC-AUC | 0.760887 | 0.742293 |
| Mean fold average precision ± sample SD | 0.340692 ± 0.034901 | — |
| Pooled average precision | 0.335089 | 0.328956 |
| Sensitivity / specificity at 0.80 | 0.000 / 1.000 | 0.000 / 1.000 |
| TP / FP / FN / TN | 0 / 0 / 1,431 / 7,816 | 0 / 0 / 477 / 2,606 |
| Weighted opportunity cost (`0.80 FP + 0.20 FN`) | 286.2A | 95.4A |
| No-voucher / model-guided revenue | 1,431.0A / 7,397.6A | 477.0A / 2,466.4A |
| Simulated difference | +5,966.6A (+416.95%) | +1,989.4A (+417.06%) |

The selected rule issues vouchers to every session in both samples. The simulated gains follow from guaranteed conversion under A1; they do not show selective targeting, actual voucher effectiveness, profit or reliable sales growth.

## Retained-variant comparisons

Mean-fold AUC differences below are descriptive, not significance tests. `log1p` and `zeroind` increased mean-fold AUC over their corresponding operational raw baselines for all three classifiers. Logistic raw interactions increased from 0.754075 to 0.757376; five-predictor logistic, L2 `C=0.1` and `C=10` did not improve over raw. GaussianNB smoothing increased from 0.660601 to 0.706078. LDA shrinkage decreased from 0.742414 to 0.737362. The highest mean-fold average precision belonged to Logistic `log1p` (0.341664), while Logistic `zeroind` remained the AUC-selected candidate.

No automated test suite was added. The notebook was executed fully; its output tables and plots were inspected manually, and the existing end-to-end GitHub execution workflow was preserved.
