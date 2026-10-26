# Approved PRD traceability

The unchanged approved [PRD](PRD.md) governs the revision. The autonomous owner instruction delegates the separate technical-plan gate to independent Sol; see [plan review](technical_plan_review.md) and [recipe review](recipe_review.md). This replaces older current-scope summaries; historical notebook outputs remain archived.

| Requirement | Implementation / evidence location |
|---|---|
| A1 quality before split, imbalance, retained duplicates | Main data-quality block; supplementary provenance; source hash and split ID artifacts |
| New stratified 80/20, seed 42; five common stratified folds | Both notebook provenance blocks; `artifacts/*row_ids.csv` |
| A2–A4 numerical/categorical/assumption evidence, training only | Focused main EDA and separate supplementary five investigations |
| Supplementary extends main and is not submitted | `supplementary/training_eda.ipynb`; compact decision-relevant findings in main |
| A5 four all-17 diagnostics and PageValues comparison | Same-fold all-17 versus operational baseline evidence; availability rationale |
| A6 four prescribed minimal baselines | Logit, GaussianNB, BernoulliNB, LDA; all 16 remaining sources and required encodings |
| A7 one justified revision per family | Technical-plan evidence addendum and independent recipe review; no search |
| A8 seven-slot same-fold CV, AUC/SD/SE/AP and OOF ROC | Main training selection block; fold/OOF artifacts |
| A9 winner OOF probability histogram | Main probability/threshold section; calibration caveat |
| A10 four OOF thresholds, fixed 2/3 primary | Prevalence, 0.5, 2/3, rate crossover; rates/precision/voucher/revenue evidence |
| A11 four q scenarios at constant recipients | q = 0.10, 0.25, 0.50, 1.00; discount 0.20 and threshold 2/3 fixed |
| A12 one winner, one frozen holdout audit | Training decision manifest, one saved test probability vector; ROC/confusion at 2/3 |
| A13 exact all-data refit after audit | Final fit on 12,330 rows, no further score |
| A14 actual conclusion and limits | Main conclusion plus final verification report |
| Purpose → evidence → implication throughout | Manual source/output review; substantive blocks labelled A1–A14 |
| Numerical validity and reproducibility | Warning, convergence/separation/stability evidence; official notebook execution and independent reconstruction |
| Preserve data, archives, history, original workflow and approved PRD | Protected-file hashes; separate branch and preserved pre-revision active copy |

The [verification report](verification_report.md) records completed acceptance checks and unperformed checks. This mapping alone does not claim that unexecuted or unreviewed sections have passed.
