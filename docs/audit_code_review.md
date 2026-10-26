# Independent static audit/refit code review — Task 3A

**Decision: PASS for the reviewed source, 25 October 2026.** Lead Sol may authorise the single official complete notebook execution. This is a static source decision; no test result, successful execution or final-project acceptance is claimed here.

Reviewed notebook file SHA-256: `e45b4cc2be310452130097cd5a62d7533603587cefaf3890b099e08c7c2f4872`.

Reviewed code-only SHA-256: `0e4f0f0dab80d2ac61a6a6e62ee0c0f6397c99e6f049b642632bcd6d19ca302e`. Reproduction convention: concatenate the source of every code cell, in notebook order, with exactly two newline characters between cells; encode UTF-8 and compute SHA-256. This hash permits checking that execution changes outputs rather than model/audit code.

The reviewer inspected the actual A12–A14 source and its integration with the reviewed training protocol, freeze, factories and persistence. The reviewed notebook has 37 cells, including 18 code cells, and zero cached outputs. The reviewer did not execute notebook cells, fit a model, reload test outcomes for analysis or inspect any test result.

## Findings

| Static check | Independent finding |
|---|---|
| Training decisions precede test access | PASS. A12 verifies the reviewed winner label, exact 2/3, source hash/16-source list, independent pre-test review record, seven operational labels and four diagnostics. Complete finite fold evidence and every required Logit numerical gate are required before test reload. Training IDs, partition size and disjointness are checked. |
| Exact training refit | PASS. A clone from the same revised-Logit factory fits all 9,864 training rows. C=Infinity, Newton-CG, tolerance 1e−8 and maximum iterations 2,000 are checked. The fit-population presence rule and k−1 encoding are refitted by the existing preprocessor; no feature or statistical specification changes. |
| Training-only numerical validation | PASS. Finite parameters/probabilities and absence of a primary convergence warning are checked before test reload. The same unpenalised Binomial IRLS/pseudoinverse reference compares direct mean training NLL and training probabilities under the unchanged 1e−6/1e−3 criteria. This comparison does not evaluate another model on test. Pure levels, rank and reference warnings are recorded without finite-MLE certification. |
| Test data and category contract | PASS. Source identity is checked again before reload; frozen and in-memory held-out IDs must agree. Exactly the reserved 2,466 rows and the 16 approved predictors are selected. Nominal columns retain string treatment; Weekend is explicitly numeric 0/1. Target and row-count checks precede scoring. |
| Single test prediction vector | PASS. There is exactly one held-out `WINNER_PIPELINE.predict_proba(...)` call. Its positive class is identified from fitted classes, prediction warnings are captured, probabilities are checked and the vector is saved immediately with IDs, observed labels and exact-2/3 assignments. No other test model or policy threshold is implemented. |
| Test calculations | PASS. ROC-AUC, AP, ROC, confusion matrix and sensitivity/specificity/precision all reuse the saved vector. All four q scenarios reuse the same 2/3 recipient assignments and verify expected revenue against direct per-row arithmetic. They do not trigger another prediction call or threshold choice. Undefined precision is safely displayed and stored as null. |
| Final refit after audit | PASS. Only after the test audit, train/test rows and labels are concatenated and checked against the full unique original-ID range 0–12,329. The final object clones the exact audited pipeline and verifies estimator parameters. Finite parameters, rank and warnings are recorded; a convergence warning stops completion. No prediction, performance metric or test score follows this refit. The fitted pipeline is displayed. |
| Persistence, plots and summary | PASS. Training artifacts are persisted before A12. Test prediction/unknown/warning/metric artifacts and final-fit metadata have distinct purposes. JSON uses sanitised finite/null values with `allow_nan=False`. ROC/confusion labels identify the positive class and fixed threshold; confusion annotation contrast is handled. Conclusion values come from actual runtime variables and retain historical, timing, probability, boundary-estimation and hypothetical-policy limitations. |

## Corrections verified before this PASS

The reviewer previously identified an A13 promise of an unimplemented post-refit numerical reference gate, missing final-convergence stop and a training-only persistence message positioned after the audit. These were corrected: A13 now describes its actual finite/convergence checks without promising a new score; convergence warnings halt completion; training persistence occurs before test access and reports its true scope. Protocol prose now permits the prescribed held-out q illustration only by reusing the one frozen vector. Final title/introduction cover the complete project, and the displayed final pipeline does not compute a score. Lead Sol also required test-prediction warning capture and removal of a claim that resplitting establishes independence; both are present in the inspected source.

## Execution and final acceptance boundary

No material unresolved static defect was found. Runtime numerical failures must stop at their existing guards; this PASS does not waive them. If failure occurs before test access, resolve it using training-only evidence and record any same-specification numerical remedy. Once test access occurs, preserve the vector and disclose any subsequent modelling defect rather than silently generating a replacement audit.

After the authorised full run, the independent final audit must inspect actual outputs and warnings, confirm the code-only hash, independently recompute held-out metrics/revenue from the saved vector, verify the exact final refit and assess every PRD acceptance criterion. Successful static inspection alone does not establish successful or statistically correct execution. Original teaching materials remain unavailable for direct source comparison, as recorded in the earlier reviews.
