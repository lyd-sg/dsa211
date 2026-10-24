# Current requirements audit

This audit maps the latest revision request to the active notebook. It replaces the prior consolidated-checklist audit where that document described QDA, Yeo–Johnson, quantile transforms, a 35-design search or stale model results. The pasted brief's cost ratio conflict was resolved by the user: preserve the latest notebook's voucher-revenue objective at `C_FN:C_FP=1:4`.

| Requirement | Active implementation |
|---|---|
| Session prediction; unchanged `Revenue` labels | Introduction, fixed target and voucher limitations |
| Historical 75/25 stratified split, seed 42 | Data/split cell |
| Five stratified CV folds; fold-fitted preprocessing | Shared fold evaluator and pipelines |
| Three classifier families only | Logistic Regression, Gaussian Naive Bayes and LDA |
| All-17 first pass | One baseline candidate for each family, with `PageValues` |
| Operational models exclude `PageValues` | 16-predictor operational set and availability discussion |
| Raw/log1p/zeroind across all three classifiers | Common five-fold transformation loop; zero threshold learned within each training fold |
| Preserve Logistic L2 `C=.1,10`, interactions and five-predictor model | Retained candidate registrations |
| Preserve GaussianNB smoothing and LDA shrinkage | Retained model-specific candidate registrations |
| Retain existing raw mixed NB and numeric-only LDA | Raw alternatives; no transformed variants |
| ROC-AUC primary, AP and spread reported | Candidate ranking, fold metrics and selected-fold results |
| OOF threshold selection and holdout warning | Training OOF threshold scan; fixed historical test evaluation and disclosure |
| Keep current voucher revenue framework | A1–A4, `C_FN:C_FP=1:4`, theoretical reference 0.80 |
| Current computed outputs | Active notebook was fully re-executed; reported tables/plots and summary reflect the current 20-design scope |
| Preserve archive files and notebook workflow | Prior notebooks archived byte-for-byte; workflow retained |

## Execution result

The notebook completed all 21 code cells. All 20 attempted designs completed, 9 were eligible, and 0 failed. Logistic `zeroind` won mean-fold AUC at 0.761161 ± 0.022013; threshold 0.800000; historical test AUC 0.742293 and AP 0.328956. At the selected threshold the rule vouchers every session in the training and historical-test samples. Full metrics and first-pass baselines are recorded in `revision_summary.md`.

## Interpretation limits

Successful execution and correct arithmetic do not establish voucher effectiveness. The data contain no voucher assignment or response. Predictor timing, unavailable customer identity, selection optimism and historical test reuse remain unresolved limitations. Do not claim causal lift, profitability or reliable actual sales growth.
