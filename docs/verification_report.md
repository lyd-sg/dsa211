# DSA211 final verification report

**Lead verification: PASS.** Independent final review is recorded separately in [final_independent_review.md](final_independent_review.md). Date: **25 October 2026, Asia/Singapore**.

The submitted artifact is the fully executed `online_shoppers_revised.ipynb`. The executed `supplementary/training_eda.ipynb` is retained separately and **is not submitted**. Prediction and the voucher illustration are distinct: the selected model ranks sessions moderately, while its precommitted 2/3 rule detects no held-out buyers and distributes vouchers almost universally.

## Actual results

| Evidence | Result |
|---|---:|
| Selected operational specification | Revised Logit: six activity log1p magnitudes plus fold-fitted zero-heavy presence indicators |
| Mean five-fold training ROC-AUC | 0.757646761 |
| Fold AUC sample SD / SE | 0.013016452 / 0.005821134 |
| Mean fold average precision | 0.335012100 |
| Single-winner test ROC-AUC / average precision | 0.741209515 / 0.326790493 |
| Fixed primary policy | Exact 2/3; predicted buyer → no voucher |
| Test TN / FP / FN / TP | 2,082 / 2 / 382 / 0 |
| Test sensitivity / specificity / precision | 0 / 0.999040307 / 0 |
| Test vouchers | 2,464 / 2,466 (99.9189%) |
| Final exact-specification refit | 12,330 rows; no subsequent prediction or score |

Precision is defined here: both of the two buyer predictions are false positives. None of the 382 observed buyers is detected at 2/3. This is reported directly in the notebook; no model, threshold or feature treatment was changed after seeing the test result. ROC-AUC evaluates ranking and does not establish calibration or useful policy targeting.

At the same frozen test assignments, discount 0.20 and common order-value unit A:

| Assumed incremental conversion q | No-voucher R0/A | Hypothetical Rq/A | Difference/A |
|---:|---:|---:|---:|
| 0.10 | 382 | 472.16 | 90.16 |
| 0.25 | 382 | 722.00 | 340.00 |
| 0.50 | 382 | 1,138.40 | 756.40 |
| 1.00 | 382 | 1,971.20 | 1,589.20 |

These are arithmetic scenarios conditional on unobserved q, not measured targeting effectiveness, actual growth or profit. All four rows use exactly the same 2,464 recipients. At q=.50, the assumed .40TN contribution of 832.8A is offset by .20FN discount loss of 76.4A.

## Individual PRD acceptance checks

| PRD §11 criterion | Completed evidence and assessment |
|---|---|
| **Purpose-first A1–A14** | **PASS.** Each substantive main analysis has an explicit preceding purpose/question, actual code/output and a concrete interpretation/implication. The five supplementary investigations follow the same structure. The zero-buyer test finding and limited policy selectivity are explicit. |
| **Course alignment and workflow** | **PASS against the approved PRD.** Four taught baselines, three independently approved EDA-supported revisions and exactly seven operational comparison slots. All-17 models remain diagnostics. One CV-selected winner is refitted on training, audited on test and then cloned/refitted on all data. Direct comparison with unavailable original teaching files is not claimed. |
| **Data discipline** | **PASS.** Quality precedes the stratified 80/20 seed-42 split; 9,864/2,466 original row IDs are disjoint and exhaustive. All 12,330 observations, including 125 excess exact duplicates, remain. Predictor EDA and choices use training only. Five common shuffled stratified folds use seed 42; learned encoding, maps and presence eligibility fit within each fit fold. Test rows are reloaded only after freeze/refit/numerical guards. |
| **Transparent EDA-to-model logic** | **PASS.** Actual tails, zero/positive differences, sparse categories, nonmonotone SpecialDay evidence and timing uncertainty motivate the limited recipes. Counterevidence is retained; no interaction/pooling or AUC-driven recipe search was added. Supplementary EDA is separate and extends the main summaries. |
| **Required output coverage** | **PASS.** Four all-17 versus operational baseline comparisons; seven-row AUC/SD/SE/AP table; selected fold scores; OOF ROC overlay and histogram; four threshold references and sensitivity/specificity figure; one test ROC/confusion audit; four fixed-policy q cases; final all-data fit and actual conclusions. |
| **Mathematical consistency** | **PASS.** C_FN=.20A and C_FP=.80×.50A=.40A imply 2/3 for meaningful probabilities. TP/FP/FN/TN conventions, voucher direction, R0=TP+FN, Rq=TP+.80FN+.80qTN and delta=.80qTN−.20FN reconcile in code, tables and prose. Recipient-level arithmetic independently verifies every threshold/q total. |
| **Readability and labels** | **PASS.** Main figures/tables were inspected; eight substantive main figures and three supplementary figures have labelled variables, classes, units and purposes. The Q–Q panel caption identifies both variables. The notebook contains no exercises, placeholders, broad coefficient-inference summaries or redundant test q chart. |
| **Reproducibility and numerical feasibility** | **PASS.** Official full nbconvert exit 0; all 18 main code cells executed in sequence 1–18 with no error outputs. Supplementary seven code cells also execute. Seed/folds/row IDs, actual warnings, pinned versions and solver settings are recorded. All 15 CV Logit reference checks and the full-training winner check pass; final full-data fit has finite parameters and no convergence warning. |
| **Claims and provenance** | **PASS.** Results are freshly computed; historical overlapping-data exposure, duplicate patterns, selection optimism, probability/distributional assumptions, unknown q and unresolved predictor timing are disclosed. No causal lift, profit, unique-customer or deployment claim is made. |
| **Governance and preservation** | **PASS.** Approved PRD unchanged; independent plan/recipe/baseline/pre-test/static gates precede their authorised stages. Sol reviewed actual Luna source, outputs and corrections. Git history, source data, old archives and execution workflow are preserved on a separate implementation branch. |

## Execution and independent numerical verification

The official main run completed **10:54:09–10:59:01 SGT on 25 October 2026**, elapsed **4m52s**, using `.venv` and Jupyter nbconvert. All 37 cells have persistent unique IDs; all 18 code cells executed sequentially with zero error outputs. A non-fatal environment cache warning did not prevent execution or figure generation. The final exact model fit used 12,330 rows, 27 iterations and encoded design rank 68/69; it was not scored.

Two post-audit **Markdown-only** clarifications state the observed zero-buyer policy result and identify the Q–Q panels. Every code cell, numerical/figure output, execution count and code-cell execution metadata is identical to the official run. The approved code SHA-256 remains `0e4f0f0dab80d2ac61a6a6e62ee0c0f6397c99e6f049b642632bcd6d19ca302e`. No model was refit or test prediction recomputed for these clarifications.

Both Sol agents independently inspected actual source and saved evidence. They reconstructed all 35 operational fold AUC/AP values, means, sample SDs and SEs; differences are at floating precision (at most about 1.2e-16). Rank-based AUC and grouped-score AP provide checks separate from the notebook calculations. Saved test probabilities independently reproduce AUC/AP, all confusion counts/rates, voucher assignments and four q revenues. Use `float_precision='round_trip'` to read probability CSVs: near-one GaussianNB score ties otherwise can change AP in the last reported digits.

All 15 CV Logit comparisons with the same-likelihood fit-fold Binomial IRLS/pseudoinverse reference pass the frozen tolerances: absolute mean fit-NLL difference ≤1e-6 and maximum validation-probability difference ≤1e-3. Observed maxima are approximately 2.18e-8 and 3.21e-4. The full-training winner reference also passes (9.61e-10 and 1.51e-6). These are numerical checks, not calibration tests or certificates of finite/unique MLE coefficients. Pure categories and rank deficiency are explicitly retained. Rejected numerical attempts remain labelled separately.

Mixed-NB verification checked all 40 fitted categorical supports/count denominators and eight actual validation examples, including three unknown codes. Gaussian log densities plus one class prior and smoothed categorical frequencies reproduce saved posterior probabilities within about 1.5e-15, without another classifier fit.

Evidence is in `artifacts/execution_verification.json`, `model_*`, `seven_candidate_*`, `mixed_nb_component_audit.json`, `winner_*`, `test_*`, `final_refit_metadata.json`, the frozen decisions and the review records. No new automated unit/code-checking test suite was added; the original end-to-end notebook workflow is preserved.

## Preservation and approval trail

- Dataset SHA-256: `b3055ee355f59134d851d32641183cb4a8b45def7124d2f50442a042f358e0d9`.
- Approved PRD SHA-256: `5b92dd103a386bf494e56e247cd8cee23f24bd57e1aa58121730843c3e0c420d`.
- Prior active notebook preserved byte-for-byte in `archive/online-shoppers/online_shoppers_pre_prd_v1.ipynb`: `fe15cdefe2449245ca5a4ccbbaa09307050090fb5ae0b2d46dde7f9fcb448292`.
- All protected files match the recorded hashes, including existing archives and the unchanged GitHub workflow; see `artifacts/protected_files_sha256.json`.
- Final main notebook SHA-256 after the two Markdown clarifications: `9e1eaa78c4b0c67867bc367e485023ccc58479234e85cabcd6a4c32aebb00794`.
- Starting branch/commit: `revise-three-model-scope` / `8cbeeb085be1c6b322f7a7dca8885dd7c5cbe536`. Delivery branch: `implement-approved-prd`; final delivery SHA is included with the handoff.

The owner explicitly delegated the separate plan gate to independent Sol. See [plan review](technical_plan_review.md), [recipe review](recipe_review.md), [baseline review](baseline_review.md), [pre-test review](pretest_review.md), [audit-code review](audit_code_review.md) and [supervision log](implementation_log.md). Execution authorisation was recorded before any test prediction file existed.

## Checks not performed and remaining limitations

1. **Original teaching sources unavailable.** Labs 1, 5, 6, 7, Lectures 5–8 and `project_cv_workflow.html` were absent from the available repository/attachments. Direct file-by-file comparison was not performed. Course checks use their requirements consolidated in the approved PRD; the archived working proposal does not override it.
2. **Remote CI and a fresh environment install were not run.** The official local run used the provided Python 3.12 environment with pinned package versions; dependency consistency was checked. The original GitHub execution workflow is unchanged. No remote-CI success is claimed.
3. **Historically pristine validation is unavailable.** Earlier work viewed an overlapping sample. The frozen audit follows the revised protocol, but cannot erase that exposure. Training-informed recipe/candidate selection and repeated patterns may add optimism.
4. **Scientific limitations remain.** Formal calibration procedures were intentionally out of scope. NB/LDA assumptions and Logit boundary/nonidentifiability issues limit interpretation. Session-end predictors are not certified available before an intervention. Customer identifiers, voucher outcomes, counterfactuals, actual order values and margins are absent. The project cannot establish real voucher effectiveness, profit or production feasibility.
