# DSA211 — Online Shoppers Classification Study
## Product Requirements Document · Draft v0.4 · 24 October 2026

> **Status: UNAPPROVED WORKING DRAFT for grilling.** This is not authorization to implement notebook or modelling changes. Requirements below are categorized as **Source constraint**, **Previously recorded decision**, **Proposal**, or **Open**. A retrospective PRD cannot pretend that past modelling and test inspections were prospective.

### Governance — consolidated source of truth [Confirmed, 24 October 2026]

- **Once explicitly approved as v1.0, this PRD is the single consolidated project-specific source of truth** for the research objective, scope, constraints, agreed decisions, acceptance evidence, and delivery expectations. Other repository documents (`AGENTS.md`, methodology, decisions, README, notebooks, past instructions) must conform to the approved PRD rather than independently redefining requirements.
- **Authority order:** official DSA211 assignment and instructor instructions → **approved PRD** → technical design / implementation guidance (including `AGENTS.md`) → existing notebooks and historical notes. The PRD cannot waive or contradict course requirements. A conflict must be surfaced for a user decision, not silently reconciled.
- **Draft versus approval:** During grilling, this document is the working register of confirmed decisions, proposals and open questions, **not yet an approved implementation mandate**. No exploratory idea becomes a requirement unless agreed explicitly. Once approved, changes to project scope or requirements must be discussed and recorded as a versioned PRD amendment before implementation.
- **Documentation sync:** `AGENTS.md` should direct agents to the approved repository PRD (target path `docs/PRD.md`) before any work. Existing secondary docs must be reconciled against it when implementing; changes may not override it by accident.


### 1. Purpose and intended deliverable

**Problem.** Evaluate whether historical browsing-session variables predict a session-level purchase (`Revenue=1`) sufficiently well to justify a defensible classifier and any stated operational interpretation.

**Audience.** DSA211 instructor/markers and a statistically literate reader. **Artifact.** A concise, fully executable Python notebook presenting an academic predictive classification analysis, not a deployed e-commerce product.

**Main outcome [Confirmed during grilling, Q1].** A **prediction-focused** project: compare eligible models on defensible validation, explain what the data support, select a model reproducibly, and communicate limitations. The project is not a coefficient-inference or causal voucher-effect study.

**Secondary application [Confirmed during grilling, Q2].** After choosing a classifier using statistical predictive-performance criteria, apply its predictions and an independently chosen classification threshold to assign hypothetical vouchers to predicted non-buyers. Compare simulated revenue under the original no-voucher observations and the voucher scenario. **Do not select models or thresholds to maximize voucher revenue**, and do not change the model to make voucher results look favourable. Positive, negative or null simulated differences are acceptable. There is no intervention/response dataset: simulated revenue is **not observed revenue uplift or a causal effect**. The original two-page brief instead describes allocating *live sales support to likely buyers* with 5:1 missed-buyer-to-wasted-support costs; the current repository uses a voucher rule with an illustrative 1:4 opportunity-cost ratio. Retain this documented brief/repository conflict for reconciliation against academic requirements; Q2 does not authorize overlooking the original brief.

### 2. Source hierarchy and non-negotiable academic constraints

- **[Source constraint]** Satisfy actual DSA211 assignment requirements and explicit instructor instructions; where a grading rubric is not present, do not claim to have independently verified it.
- **[Previously recorded instructor guidance]** Choose prediction *or* inference (project currently prediction); fit all predictors first for each taught model, then modify based on evidence; consider binarizing zero-heavy numerical data where justified.
- **[Source]** The supplied *Predicting Online Purchases — Project brief* describes the UCI Online Shoppers dataset (12,330 sessions, 17 candidate predictors), skew/zero-heavy data, class imbalance, possible `PageValues` leakage and model comparisons. It proposes methods and experiments that are not all compatible with the latest scoping decisions. Differences require explicit resolution rather than silent substitution.
- **[Source/current repo]** `lyd-sg/dsa211`, branch `revise-three-model-scope`, active `online_shoppers_revised.ipynb`; repo docs `project_decisions.md`, `methodology.md`, `requirements_audit.md`, `phase2_scope.md`. The newly pasted revision request proposes further edits; none have been executed as part of this draft.

### 3. Desired outcomes

**O1 — Methodological validity.** Features, preprocessing, model selection and any classification-threshold selection avoid preventable data leakage and unjustified claims. Voucher revenue must not determine classifier or threshold selection.

**O2 — Empirical discipline.** EDA and model diagnostics motivate a small number of hypothesis-driven experiments; failures and negligible gains are reported honestly.

**O3 — Coherent decision.** The study selects an eligible classifier using a predeclared primary statistic; if an operational policy is included, that policy has a logically consistent objective, metrics and limitations.

**O4 — Communication.** A significantly shorter, easily audited report; every main section conveys *why, how, result, implication* without excessive printouts or repeated explanations.

**O5 — Reproducibility.** Re-execution produces the stated numerical tables, plots and conclusions; previous revisions are preserved.

### 4. Draft requirements and acceptance evidence

| ID | Draft requirement and status | Acceptance evidence |
|---|---|---|
| R1 | **[Source / recorded]** Define `Revenue` and distinguish sessions from customers; establish dataset provenance, basic quality, class imbalance and appropriate EDA. | Dataset checks, focused numerical/categorical summaries, and interpretation linked to modelling decisions. |
| R2 | **[Recorded]** Historical stratified 75/25 train–test split, `random_state=42`; five stratified folds on training; identical fold membership for fair model comparisons. | Explicit split/fold configuration, counts and reproducible CV results. Historical test reuse disclosed. |
| R3 | **[Recorded]** Start with all 17 original predictors for Logistic Regression, Gaussian Naive Bayes and LDA; inspect `PageValues`; exclude it from 16-feature operational candidates if not available at decision time. | Three first-pass results and reasoned feature-availability/leakage comparison. No unsupported claim that leakage is proven solely by association. |
| R4 | **[Recorded / proposal]** Compare operational raw, `log1p`, zero-indicator treatments; retain suitable NB/LDA alternatives and appropriate regularization/smoothing checks. Explicitly mark eligibility rules. | Side-by-side five-fold CV metrics, equivalent preprocessing standards, documented candidate selection. |
| R5 | **[New proposal]** Replace arbitrary five-variable and blanket 28-interaction experiments with five separate targeted experiments relative to Logistic `log1p`: (i) remove `BounceRates`; (ii) replace product duration with safe mean time per product page; (iii) replace two informational variables with `Informational>0`; (iv) `ProductRelated × ExitRates`; (v) `VisitorType × log1p(ProductRelated_Duration)`. Keep main effects for interactions. | Training-only correlation/VIF diagnostic; CV AUC and ΔAUC comparison for each isolated experiment; do not label hypotheses as successful before results. |
| R6 | **[Recorded]** Fit data-derived preprocessing in training folds; avoid using historical test outcomes for feature selection, hyperparameter tuning or thresholds. | Inspected preprocessing pipelines and complete runnable notebook. |
| R7 | **[Recorded]** Primary classifier selection by mean five-fold training ROC-AUC; AP reported as complementary; report variability, confusion matrix, sensitivity and specificity where decision thresholds matter. | Model comparison with numerically reproducible values and modest interpretation of small differences. |
| R8 | **[Confirmed Q2 / threshold rule still open]** After choosing the classifier by training-CV predictive performance, classify `Buy` → no voucher; `No Buy` → voucher. Use a classification threshold selected independently of voucher revenue (precise statistical rule: Q3 pending). Retain existing illustrative voucher assumptions provisionally: A1 guaranteed conversion, A2 20% discount, A3 uniform order value `A`, A4 historical purchases reflect no intervention. Compare the two simulated scenarios without optimizing model or threshold on revenue; the old theoretical 0.80 revenue cutoff is **not** the selection rule. | Explicit predefined classification rule, share receiving vouchers, revenue arithmetic and assumption-based scenario comparison; never claim observed/causal lift, actual sales or profit. Positive, zero or negative simulated impact is acceptable. |
| R9 | **[New proposal]** Reduce explanatory prose by at least ~50% where possible, excluding equations/code/tables; use concise tables/plots and minimal warning clutter while preserving genuine error detection and essential methodological detail. | Before/after prose comparison, reader-facing notebook review and warnings/error audit. |
| R10 | **[New proposal]** Preserve report order: introduction, EDA, initial baselines, diagnostics, targeted improvements, model selection, threshold/revenue (if retained), historical test/conclusion. | Executed notebook follows flow, avoids repetition and uses consistent numerical rounding. |
| R11 | **[Recorded / proposal]** Preserve prior revisions, execute the entire notebook, recompute all dependent metrics, and leave a brief change log. | Complete run, checks for divide-by-zero/category issues, final result consistency audit, archived source history. |

### 5. Technical constraints already proposed, not additional goals

- Focus on taught methods: Logistic Regression, Gaussian NB and LDA. **[Latest proposed scope]** Do not reintroduce QDA, gradient boosting, KNN, Yeo–Johnson, quantile transforms, splines, broad subset searches or arbitrary feature expansion. **[Conflict to verify]** The earlier two-page brief did propose QDA and some extensions; exclusions require academic-requirement check.
- `AvgProductTime=ProductRelated_Duration/ProductRelated` must define the zero-denominator case without creating artificial signal.
- All comparisons should use the same training folds and be transparent about model-specific feature representations.
- `PageValues` timing and other session-end predictor availability are prerequisites to any claim about real-time intervention feasibility.
- Preserve the existing committed data and archived notebooks; do not quietly overwrite previous results.

### 6. Explicit non-goals

- Production website, deployable voucher engine or live sales-support system.
- Customer-level predictions (dataset contains sessions, not verified unique persons).
- Inference or causal evaluation of vouchers, actual treatment effects, actual revenue lift, profit, margin or cost-effectiveness without source data.
- A claim of a never-seen test set, since the historical partition was previously inspected.
- Automatically chasing higher AUC through indiscriminate specification search.

### 7. Known current state — not prospective targets

**[From current repo at `revise-three-model-scope`, before latest proposed changes]** The active report completed 21 code cells, 20 candidate designs (9 eligible). Selected Logistic Regression `zeroind` with mean five-fold ROC-AUC **0.761161**, test ROC-AUC **0.742293**, and training-selected threshold **0.80**. Under that threshold **every tested session received a voucher**. The all-voucher outcome is the dominant conceptual issue: it produces simulated increases under the unverified assumption of guaranteed voucher conversion, but is not evidence of model-guided targeting. Revisions must recompute rather than copy these results.

### 8. Key risks / unresolved decisions (grilling queue)

1. **[RESOLVED Q1]** Primary objective: predictive classification. Voucher simulation: secondary illustrative analysis. Still resolve the original live-sales-support framing and 5:1 cost requirement.
2. **[RESOLVED Q2]** Voucher revenue is only a secondary illustrative calculation, not a modelling/threshold optimisation objective. Use the selected classifier's predictions to allocate vouchers and report simulated results without forcing a gain. The former revenue-maximising 0.80 threshold/all-voucher outcome is historical, not a desired behaviour or rule.
3. **[HIGH]** Are all proposed exclusions (notably QDA and the original brief's broader methods) compatible with actual submission requirements?
4. **[MEDIUM]** Are the five specified experiments the complete intended search space, and which legacy variants are truly essential?
5. **[MEDIUM]** What counts as a meaningful performance improvement versus a simpler equivalent model? Preserve fixed AUC-based selection or add parsimony rule?
6. **[MEDIUM]** What evidence is adequate to call a predictor available before purchase completion? Where must deployment feasibility be qualified?
7. **[MEDIUM]** What constitutes sufficient final acceptance: fully executed notebook, reporting artifacts, reviewer inspection, CI, and/or independent reproducibility?

### 9. Grilling decisions

- **Q1 — CONFIRMED (24 October 2026):** Predictive classification is the primary research objective. Voucher simulation is a secondary analysis; do not assert actual causal or commercial benefit. This choice does not itself settle which business framing/cost structure the report must retain.
- **Q2 — CONFIRMED (24 October 2026):** Determine the best eligible classifier statistically (currently mean training-CV ROC-AUC primary); next use a classification threshold chosen independently of voucher revenue to route hypothetical vouchers to predicted non-buyers; then calculate and honestly report the simulated revenue difference against no vouchers. Do not maximise model or threshold on revenue. A successful project need not produce positive simulated revenue. Historical 0.80 revenue-optimal cutoff is not an approved selection rule. The actual threshold-selection statistic remains open.

### 10. Approval and delivery gates

- **Gate A — Grilling:** resolve open questions and note explicit choices; no modelling changes. Documentation-only updates to track this PRD and its governance are permitted by explicit user instruction.
- **Gate B — PRD v1.0 approval:** user approves bounded requirements, acceptance evidence and non-goals.
- **Gate C — Technical plan approval:** map requirements to notebook changes, experiments and reproducibility checks.
- **Gate D — Implementation:** changes on an appropriate branch, full execution, review against approved PRD.

**This document is deliberately a decision artifact, not a substitute for the DSA211 assignment specification or a record of every previous alternative.**