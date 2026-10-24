# DSA211 — Online Shoppers Classification Study
## Product Requirements Document · Draft v0.5 · 24 October 2026

> **Status: UNAPPROVED WORKING DRAFT — decision checkpoint after Q7.** The decisions marked **Confirmed** are agreed; remaining items are proposals or open questions. This checkpoint is **not approval to implement** notebook or modelling changes. This is a retrospective PRD: previously viewed test results and past decisions must not be represented as prospective.

### Governance — consolidated source of truth [Confirmed, 24 October 2026]

- **Once explicitly approved as v1.0, this PRD is the single consolidated project-specific source of truth** for the research objective, scope, constraints, agreed decisions, acceptance evidence, and delivery expectations. Other repository documents (`AGENTS.md`, methodology, decisions, README, notebooks, past instructions) must conform to the approved PRD rather than independently redefining requirements.
- **Authority order:** official DSA211 assignment and instructor instructions → **approved PRD** → technical design / implementation guidance (including `AGENTS.md`) → existing notebooks and historical notes. The PRD cannot waive or contradict course requirements. A conflict must be surfaced for a user decision, not silently reconciled.
- **Draft versus approval:** During grilling, this document is the working register of confirmed decisions, proposals and open questions, **not yet an approved implementation mandate**. No exploratory idea becomes a requirement unless agreed explicitly. Once approved, changes to project scope or requirements must be discussed and recorded as a versioned PRD amendment before implementation.
- **Documentation sync:** `AGENTS.md` should direct agents to the approved repository PRD (target path `docs/PRD.md`) before any work. Existing secondary docs must be reconciled against it when implementing; changes may not override it by accident.


### 1. Purpose and intended deliverable

**Problem.** Evaluate whether historical browsing-session variables predict a session-level purchase (`Revenue=1`) sufficiently well to justify a defensible classifier and any stated operational interpretation.

**Audience.** DSA211 instructor/markers and a statistically literate reader. **Artifact.** A concise, fully executable Python notebook presenting an academic predictive classification analysis, not a deployed e-commerce product.

**Main outcome [Confirmed during grilling, Q1].** A **prediction-focused** project: compare eligible models on defensible validation, explain what the data support, select a model reproducibly, and communicate limitations. The project is not a coefficient-inference or causal voucher-effect study.

**Secondary application [Confirmed Q2–Q5].** Select the classifier using predictive performance, then apply a **pre-specified cost-based classification threshold** from DSA211 Lecture 5. Predicted buyers receive no voucher; predicted non-buyers receive a hypothetical 20%-discount voucher. The reference assumption is that **50% of people who would not otherwise purchase convert if offered a voucher**, while people who would already purchase continue to do so. This implies a theoretical cutoff of **2/3 (≈0.667)** (derivation below). Hold the selected classifier, threshold and recipient assignments fixed, then compare no-voucher revenue with simulated voucher revenue for **10%, 25%, 50%, and 100%** assumed incremental conversion. Report outcomes whether favourable or not. **Do not search for the model or threshold that maximizes empirical simulated revenue.** The theoretical threshold is nevertheless derived from assumed voucher opportunity costs; it is **not independent of voucher economics**. There are no observed voucher treatment outcomes, so this cannot establish actual sales lift or causality.

**Academic-brief conflict [Open].** The original two-page project brief frames *live sales support directed toward likely buyers* with a **5:1** missed-buyer-to-wasted-support assumption; the revised illustrative action is a **voucher to predicted non-buyers**, with a threshold derived from 20% discounts and 50% incremental conversion. The original rationale and any mandatory assignment obligations must be reconciled before final approval, not silently overwritten.

### 2. Source hierarchy and non-negotiable academic constraints

- **[Source constraint]** Satisfy actual DSA211 assignment requirements and explicit instructor instructions; where a grading rubric is not present, do not claim to have independently verified it.
- **[Previously recorded instructor guidance]** Choose prediction *or* inference (project currently prediction); fit all predictors first for each taught model, then modify based on evidence; consider binarizing zero-heavy numerical data where justified.
- **[Source]** The supplied *Predicting Online Purchases — Project brief* describes the UCI Online Shoppers dataset (12,330 sessions, 17 candidate predictors), skew/zero-heavy data, class imbalance, possible `PageValues` leakage and model comparisons. It proposes methods and experiments that are not all compatible with the latest scoping decisions. Differences require explicit resolution rather than silent substitution.
- **[Source/current repo]** `lyd-sg/dsa211`, branch `revise-three-model-scope`, active `online_shoppers_revised.ipynb`; repo docs `project_decisions.md`, `methodology.md`, `requirements_audit.md`, `phase2_scope.md`. The newly pasted revision request proposes further edits; none have been executed as part of this draft.

### 3. Desired outcomes

**O1 — Methodological validity.** Features, preprocessing, model selection and classification-threshold selection avoid preventable data leakage and unjustified claims. Select the model on predictive metrics, not voucher revenue; derive the cost-based threshold from declared reference assumptions **without** searching the data for maximum simulated revenue.

**O2 — Empirical discipline.** EDA and model diagnostics justify **at most one deliberately chosen modification per classifier** (potentially none). Transformation is a minor supporting component, not the main study. Failures or negligible gains are reported honestly.

**O3 — Coherent decision.** The study selects an eligible classifier using a predeclared primary statistic; if an operational policy is included, that policy has a logically consistent objective, metrics and limitations.

**O4 — Communication.** A significantly shorter, easily audited report; every main section conveys *why, how, result, implication* without excessive printouts or repeated explanations.

**O5 — Reproducibility.** Re-execution produces the stated numerical tables, plots and conclusions; previous revisions are preserved.

### 4. Draft requirements and acceptance evidence

| ID | Draft requirement and status | Acceptance evidence |
|---|---|---|
| R1 | **[Source / recorded]** Define `Revenue` and distinguish sessions from customers; establish dataset provenance, basic quality, class imbalance and appropriate EDA. | Dataset checks, focused numerical/categorical summaries, and interpretation linked to modelling decisions. |
| R2 | **[Recorded]** Historical stratified 75/25 train–test split, `random_state=42`; five stratified folds on training; identical fold membership for fair model comparisons. | Explicit split/fold configuration, counts and reproducible CV results. Historical test reuse disclosed. |
| R3 | **[Confirmed Q6 / previously recorded]** Compare **exactly three classifier families**: Logistic Regression, Naive Bayes and LDA (**exclude QDA**). Start each with all 17 original predictors as the professor instructed; examine `PageValues`, then exclude it from 16-feature operational candidates based on decision-time availability. | Three initial all-predictor baselines, availability/leakage reasoning, three operational baselines and valid comparison. No unsupported claim that association alone proves leakage. |
| R4 | **[Confirmed Q7 scope limit; details Open]** Keep operational raw baselines, then allow **at most one EDA-justified modification for each of the three classifier families**. A classifier need not be modified if there is no compelling rationale; a tested modification need not be retained. Prior raw/`log1p`/zero-indicator grids, additional NB/LDA variants and broad tuning are **historical/proposed**, not automatically required in the final scope. | One concise EDA-to-hypothesis-to-CV comparison per modified classifier, reporting performance change and decision; explicit comparable baseline and eligibility criteria. |
| R5 | **[Confirmed Q7: bounded, EDA-led changes; exact three experiments Open]** Transformation and feature engineering must **not** dominate the project. Select up to one candidate change for each of Logistic Regression, Naive Bayes and LDA **after reviewing actual EDA and model assumptions**; do not pre-approve the five experiments from the pasted revision request or exhaustive pairwise interactions. Separate hypothesis from verified improvement. | A brief justification tied to a specific EDA finding or taught assumption, isolated CV ROC-AUC comparison, and defensible retain/reject decision; no exploratory sprawl. |
| R6 | **[Recorded]** Fit data-derived preprocessing in training folds; avoid using historical test outcomes for feature selection, hyperparameter tuning or thresholds. | Inspected preprocessing pipelines and complete runnable notebook. |
| R7 | **[Recorded]** Primary classifier selection by mean five-fold training ROC-AUC; AP reported as complementary; report variability, confusion matrix, sensitivity and specificity where decision thresholds matter. | Model comparison with numerically reproducible values and modest interpretation of small differences. |
| R8 | **[Confirmed Q2–Q5]** Select a classifier by mean training-fold CV ROC-AUC, **not** revenue. Use the **Lecture 5 cost-based theoretical threshold** with 50% reference incremental conversion and 20% discount, giving **t*=2/3**. Classify predicted `Buy` (p ≥ t*) → no voucher; predicted `No Buy` (p < t*) → voucher. Freeze model, threshold and assignments; compute illustrative revenue for incremental conversion rates **10%, 25%, 50%, 100%** against no vouchers. Do not re-optimize for any scenario. | Threshold derived clearly from costs, training-only application, confusion matrix and recipient share, plus transparent four-scenario simulation. Revenue may rise or fall; no claim of causal lift, actual profit or real-world response. |
| R9 | **[New proposal]** Reduce explanatory prose by at least ~50% where possible, excluding equations/code/tables; use concise tables/plots and minimal warning clutter while preserving genuine error detection and essential methodological detail. | Before/after prose comparison, reader-facing notebook review and warnings/error audit. |
| R10 | **[New proposal]** Preserve report order: introduction, EDA, initial baselines, diagnostics, targeted improvements, model selection, threshold/revenue (if retained), historical test/conclusion. | Executed notebook follows flow, avoids repetition and uses consistent numerical rounding. |
| R11 | **[Recorded / proposal]** Preserve prior revisions, execute the entire notebook, recompute all dependent metrics, and leave a brief change log. | Complete run, checks for divide-by-zero/category issues, final result consistency audit, archived source history. |

### 5. Confirmed analytical boundaries and proposed technical constraints

- **[Confirmed Q6]** Use only Logistic Regression, Naive Bayes and LDA; **no QDA**. Do not expand to KNN, gradient boosting, splines or unrelated classifiers without a further decision. The original brief listed QDA and broader extensions; verify whether they are mandatory before treating exclusions as assignment-compliant.
- **[Confirmed Q7]** Limit feature/model alterations to **at most one EDA-motivated change per classifier**. Do not automatically run the earlier five-feature-experiment request, all-28 interactions, broad regularisation/smoothing searches, or every named transformation. Exact three candidate changes are **unresolved** until EDA review. Preserve the original raw comparisons as a reference.
- **[Previously recorded]** Use the same training folds across comparisons; fit encoders, transformations and other data-derived preprocessing inside training folds. Explain any model-specific feature representation, rather than treating all comparisons as identical.
- **[Confirmed Q3–Q5]** Derive the theoretical classification threshold using lecture-taught error costs, rather than selecting a threshold from maximum *observed simulated* voucher revenue. It is still a **voucher-economics-based** threshold.
- **[Recorded]** Consider `PageValues` timing and session-end features before claiming real-time voucher feasibility. Preserve committed data and historical archives; avoid carrying forward stale execution results.
- **[Unapproved example only]** If an eventual selected feature requires division by `ProductRelated`, handle zeros safely. This is not a requirement to engineer `AvgProductTime`.

### 6. Explicit non-goals

- Production website, deployable voucher engine or live sales-support system.
- Customer-level predictions (dataset contains sessions, not verified unique persons).
- Inference or causal evaluation of vouchers, actual treatment effects, actual revenue lift, profit, margin or cost-effectiveness without source data.
- A claim of a never-seen test set, since the historical partition was previously inspected.
- Automatically chasing higher AUC through indiscriminate specification search.

### 7. Known current state — historical, not a project target

**[Executed state on `revise-three-model-scope` before checkpoint]** The notebook completed 21 code cells, 20 candidate designs (9 eligible) and selected Logistic Regression `zeroind` with mean five-fold ROC-AUC **0.761161** and historical test ROC-AUC **0.742293**. Its legacy revenue-optimised threshold **0.80** gave vouchers to every evaluated session **under the old 100%-conversion assumption**. That historic result illustrates how assumptions can dominate a policy; it is **not** evidence of model-guided targeting, and **must not be copied** into results for the agreed 50%-reference / sensitivity-analysis framework. After the approved implementation batch, rerun and recompute all relevant predictions, classifications and scenarios.

### 7A. Agreed threshold mathematics — for implementation and verification

Let `A` be the common no-discount order value; `d=0.20` the voucher discount; `q=0.50` the **reference incremental conversion probability among otherwise non-buyers**; and `p` the model-predicted probability of buying **without** a voucher. Assume existing buyers still buy if offered a voucher; all voucher buyers pay `0.80A`; observed `Revenue` records no-voucher outcomes.

- Giving a voucher to an actual existing buyer (predicted non-buyer: FN) forgoes `C_FN = dA = 0.20A`.
- Not giving a voucher to an actual non-buyer (predicted buyer: FP) forgoes *expected* incremental revenue `C_FP = (1-d)qA = 0.80 × 0.50 A = 0.40A`.
- **Fixed theoretical threshold** (Lecture 5): `t* = C_FP / (C_FP + C_FN) = 0.40/(0.40+0.20) = 2/3 ≈ 0.667`. Apply this same threshold to all scenarios; no search over thresholds for revenue lift.
- For any scenario `q_s ∈ {0.10, 0.25, 0.50, 1.00}`, let `TP, FP, FN, TN` use observed `Revenue=1` as the positive class **at the fixed classification rule**. No-voucher revenue: `R0/A = TP + FN`. Expected model-voucher revenue: `Rq/A = TP + 0.80 FN + 0.80 q_s TN`. Simulated difference: `ΔRq/A = 0.80 q_s TN − 0.20 FN`. Thus only the assumed incremental conversion rate changes across scenarios, not predicted probabilities or assignments.
- Cost-based `t*` is theory-based **under assumptions**, not a guarantee of empirical optimality, calibrated probabilities or actual causal uplift. The real `q` is unknown and there are no voucher intervention labels.

### 8. Key risks / unresolved decisions — after checkpoint

1. **[OPEN, NEXT]** Choose **up to one exact EDA-justified modification per classifier**, only after reviewing actual EDA. None is automatically mandatory. Decide what counts as sufficient improvement to retain a change.
2. **[OPEN: academic alignment]** Reconcile the original two-page *live-support* / 5:1 brief and its QDA/extension proposals with the agreed *voucher demonstration* / three-classifier approach. The PRD cannot independently waive any compulsory assessment requirement.
3. **[OPEN: reporting scope]** Which legacy modelling variants and supporting plots are necessary given the one-change-per-classifier cap? Avoid silently retaining the old 20-design search.
4. **[OPEN: assumptions and limits]** Confirm how to explain `PageValues` and session-end timing, score calibration for cost thresholds, generalisability, and previously examined test data.
5. **[OPEN: acceptance]** Final criteria for adequate model performance reporting, notebook concision, completed execution, numerical consistency, reproducibility and final review.

### 9. Confirmed grilling decisions — checkpoint 24 October 2026

| Decision | Confirmed agreement | Status |
|---|---|---|
| **Q1 — Objective** | **Prediction-focused** project; model performance is primary. No coefficient-inference or causal voucher-effect goal. | Confirmed |
| **Q2 — Voucher extension** | A **small secondary demonstration**: take the selected classifier's outputs, assign vouchers according to a prechosen cost-based cutoff, and report simulated revenue whether positive or negative. **No data-driven revenue optimisation** of the classifier or threshold. | Confirmed |
| **Q3 — Threshold method** | Use the **Lecture 5 cost-based threshold** `C_FP/(C_FP+C_FN)`, not default 0.5, base-rate selection, or Youden's J. | Confirmed |
| **Q4 — Conversion uncertainty** | Replace the guaranteed-conversion assumption with **sensitivity analysis at 10%, 25%, 50% and 100%** assumed incremental conversion among otherwise non-buyers; keep classification decisions fixed for all scenarios. | Confirmed |
| **Q5 — Reference economics** | Assume 20% voucher discount and 50% reference incremental conversion. Thus `C_FP=0.40A`, `C_FN=0.20A`, and the **fixed reference threshold is 2/3 ≈ 0.667**. The conversion assumption is illustrative, not observed; no claim it is objectively realistic. | Confirmed |
| **Q6 — Classifiers** | **Exactly three** model families: Logistic Regression, Naive Bayes and LDA. **QDA excluded**, subject to checking any compulsory assignment requirement. | Confirmed |
| **Q7 — Model changes** | **At most one** purposeful, EDA-/assumption-driven modification for each model family. Modifications may fail or be unnecessary. **No five-experiment slate is preapproved**; the exact modifications remain **OPEN** until EDA review. | Confirmed boundary; details Open |

**Checkpoint rule:** these seven agreements supersede conflicting draft proposals or obsolete notebook assumptions **within the working PRD**, but they do not constitute approval to modify the analysis. Further grilling resumes with choosing the specific EDA-led modifications.

### 10. Approval and delivery gates

- **Gate A — Grilling:** resolve open questions and note explicit choices; no modelling changes. Documentation-only updates to track this PRD and its governance are permitted by explicit user instruction.
- **Gate B — PRD v1.0 approval:** user approves bounded requirements, acceptance evidence and non-goals.
- **Gate C — Technical plan approval:** map requirements to notebook changes, experiments and reproducibility checks.
- **Gate D — Implementation:** changes on an appropriate branch, full execution, review against approved PRD.

**This document is deliberately a decision artifact, not a substitute for the DSA211 assignment specification or a record of every previous alternative.**