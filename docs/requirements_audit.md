# Manual requirements audit

This audit reconciles the final implementation brief with the subsequently supplied **Consolidated Requirements and Agreed Decisions (22 October 2026)**. It records manual review and actual-data notebook execution; no automated code-checking test suite was added.

## Why the voucher allocation becomes extreme

The current assumptions guarantee revenue `0.80A` after a voucher, whereas withholding a voucher has expected revenue `pA`. Therefore every calibrated session probability below `0.80` favours a voucher. In a dataset with approximately 15.5% purchases and few high-confidence buyers, this can favour issuing vouchers to nearly every session.

An extreme allocation is not, by itself, evidence of a reversed decision rule or a revenue-formula error. It does mean the simulation can be dominated by A1 rather than demonstrate useful selective targeting. Keep that distinction explicit. Do not modify assumptions, thresholds or results merely to obtain a preferred allocation.

## Gaps found and corrected

| Consolidated requirement | Gap in the first delivered revision | Correction |
|---|---|---|
| PR-AUC and fold-to-fold spread | ROC-AUC was present, but PR-AUC was absent | Add average precision, fold means/SDs, selected per-fold scores, OOF/test AP and PR curves |
| Defensible mixed-data NB/LDA specifications | Numerical transforms left Gaussian dummy-variable assumptions unresolved | Add mixed Gaussian/Categorical NB and numerical-only LDA/QDA; keep challenged dummy-coded fits as diagnostics outside final operational eligibility |
| Separate prediction from the voucher extension | Revenue could dominate the interpretation of a valid discrimination comparison | Report predictive winners separately from the selected business rule and explain any near-universal allocation |

The user resolved the selection question during this audit: **choose the classifier by mean training CV ROC-AUC, then optimise only its voucher threshold by training OOF simulated revenue**. This supersedes the earlier joint revenue-selection instruction. PR-AUC remains an additional reported metric; neither test scores nor simulated test revenue choose the classifier.

The six added model specifications follow the explicit mixed-predictor requirement, not the historical test scores. Candidate eligibility and selection rules are stated before final test evaluation. Earlier results and test inspection remain part of the historical-reuse limitation.

## Requirement-by-requirement review

| Requirement | Implementation evidence |
|---|---|
| Prediction, session unit, unchanged `Revenue` labels | Introduction, data/split cell, fixed classifier target and limitations |
| 12,330 sessions; 17 predictors; eight categorical variables | Data schema/quality output and explicit numeric/category lists |
| Nominal technical codes and ten observed months | Fold-fitted categorical encoding and training categorical EDA |
| Historical 75/25 split, seed 42, training-only EDA | Split before substantive EDA; 9,247/3,083 partition |
| No preselected classifier; all-predictor first pass | All four default families attempted on all 17 predictors; failures preserved |
| Gaussian/dummy issue and workaround | Dedicated mixed-predictor section; mixed NB and numerical-only discriminant candidates |
| Zero-heavy predictors and justified changes | Training diagnostics; fold-fitted zero indicators and bounded transformation comparisons |
| Five-fold CV; preprocessing inside folds | Cached OOF probabilities and fold metrics from fold-specific pipelines |
| `PageValues` timing review | All-predictor diagnostic comparison, then exclusion from operational candidates |
| ROC-AUC, PR-AUC, spread, confusion metrics | Fold mean/SD tables, selected per-fold metrics, ROC/PR curves and CV/test audit |
| Voucher decision rule | `p >= t` → predicted Buy → no voucher; `p < t` → voucher |
| Opportunity costs | `C_FP=0.80A`, `C_FN=0.20A`, hence FN:FP=1:4 |
| Theoretical and empirical thresholds | Calibrated reference 0.80 and exact training OOF cutpoint search |
| Fixed no-voucher baseline | `TP+FN` equals observed buyers at every cutoff |
| Exactly two revenue scenarios | No voucher versus selected model-guided vouchers; no extra policy comparator |
| Revenue arithmetic | `Rmodel/A=TP+0.80(FN+TN)`; `delta/A=0.80TN-0.20FN`; divide by fixed buyers for relative change |
| Historical test not used for tuning | Select configuration/cutoff on training CV, then fit full training and evaluate the fixed rule |
| Both required extensions | Threshold curves and CV-versus-historical-test comparison |
| No unsupported causal/profit claim | A1–A4, unobserved voucher effects, sales revenue rather than profit |
| Dataset/predictor limitations | One historical retailer, session-end feature availability, no customer IDs, selection optimism and prior test viewing |
| Preserve original work | Original notebook, dataset and archives unchanged; Phase 2 commit ancestry incorporated |
| Reviewable GitHub deliverable | Executed revised notebook, documentation and end-to-end GitHub execution workflow on `main` |

## What compliance cannot establish

Neither correct arithmetic nor successful notebook execution establishes voucher effectiveness. The data contain no treatment assignment or voucher response. A more credible targeting decision would require intervention evidence and assumptions grounded in it; this revision does not invent such parameters. Predictor timing, dependence among sessions and new independent evaluation also remain unresolved.
