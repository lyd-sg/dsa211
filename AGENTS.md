# DSA211 repository instructions

## Source-of-truth and change-control rule (user-confirmed 24 October 2026)

- **Read `docs/PRD.md` first.** It is the consolidated project-specific requirements document. While marked **DRAFT**, it is a working register for grilling: only explicitly confirmed choices are settled, and its proposed/open items do **not** authorize implementation. Once the user explicitly approves PRD v1.0, the **approved PRD becomes the authoritative consolidated source of truth** for the project's objectives, modelling/reporting scope, requirements, boundaries, acceptance criteria and agreed decisions.
- **Priority:** official DSA211 assignment requirements and instructor instructions > approved `docs/PRD.md` > `AGENTS.md` and other technical/implementation documentation > legacy notebooks, historical notes or older chat prompts. Never interpret the PRD as permission to disregard the academic brief. Surface contradictions and request a decision; never silently override one source.
- **Approval gates:** drafting and grilling do not authorize changes to models/notebooks; approval of the PRD is separate from approval of a technical plan and implementation batch. Explicitly approved changes to `AGENTS.md` and PRD documentation during grilling are exceptions limited to documenting governance/decisions.
- **Maintenance:** when a project requirement is revised, update/version the PRD first following the user's approval; reconcile `AGENTS.md`, methodology, README, notebooks and relevant supporting docs with it. Do not treat prior implementation or a newly proposed prompt as superior to the PRD.
- **Confirmed Q1/Q2:** Predictive classification is the primary research objective. Voucher simulation is a **simple secondary extension**, never an objective used to select or tune the classifier or its threshold. Choose the classifier by training-CV predictive performance; select a classification threshold by an independently justified statistical rule (Q3 still open), allocate hypothetical vouchers to predicted non-buyers, and report simulated revenue whether positive or negative. Observed actual or causal voucher lift cannot be established from the dataset.

## Current project

The active entry point is `online_shoppers_revised.ipynb`. Read `README.md`, `docs/project_decisions.md`, `docs/methodology.md` and `docs/phase2_scope.md` before changing the analysis. The current authorized revision removes QDA and the Yeo–Johnson/quantile-transform experiments. The prior executed revised notebook and original full-project notebook are retained byte-for-byte under `archive/online-shoppers/`.

Predict session-level `Revenue` and compare exactly two simulated revenue scenarios: no vouchers and model-guided vouchers. Predict Buy means no voucher; Predict No Buy means voucher. Keep observed labels unchanged. Vouchers are hypothetical actions after classification, not predictors.

## Required framework

- A1 guaranteed conversion; A2 20% discount without minimum spend; A3 common order value `A`; A4 observed outcomes represent no-voucher behaviour.
- **Confirmed new modelling rule (24 Oct 2026):** Select the classifier by highest mean training five-fold CV ROC-AUC (with AP and fold variation reported). Do **not** choose or tune any model or threshold by simulated voucher revenue. A classification threshold must be selected independently of voucher revenue on training data only; its exact statistical criterion is **not yet approved (Q3)**. Then allocate hypothetical vouchers to predicted non-buyers and compare the same two assumed revenue scenarios, allowing a negative result. The legacy 1:4 voucher-cost framing and theoretical 0.80 revenue threshold are retained only as historical scenario context, **not a selection/optimisation requirement**. Avoid claiming measured causal revenue lift. All work remains subject to official brief requirements and approval gates.
- Preserve the 75/25 stratified split, seed 42, and five stratified training folds. Fit preprocessing inside folds.
- The first pass uses all 17 predictors with Logistic Regression, Gaussian Naive Bayes and LDA. Document genuine warnings/failures.
- Treat nominal numeric-coded categories as unranked. Investigate `PageValues`, then exclude it from operational models on availability grounds.
- Compare raw, `log1p` and fold-fitted `zeroind` treatments for all three classifiers. Preserve logistic L2 `C=0.1` and `C=10`, logistic numerical interactions, the predeclared five-predictor logistic model, GaussianNB variance smoothing and LDA shrinkage. Retain existing raw mixed Gaussian/Categorical NB and numeric-only LDA alternatives.
- Report ROC-AUC and PR-AUC (average precision), fold means and sample SDs, selected per-fold results, ROC/PR curves and historical test metrics. Keep threshold analysis and historical-test caveats.
- Freeze specification and threshold before historical test evaluation. Disclose candidate/threshold selection optimism and the previously viewed test partition.
- Do not claim actual voucher effects, profitability, unique customers or reliable sales-growth forecasts. Record predictor-timing limitations.

## File and review discipline

Preserve `data/uci_468.csv` and historical archives unchanged. Keep only the active revised notebook at the repository root; prior notebooks are archived as directed. Preserve valid project history and document splits, seeds, CV, preprocessing and actual execution. Use a branch for changes before delivery.

Ground interpretations in freshly computed results and keep notebook outputs, plots and documentation consistent. Use manual review plus full notebook execution; do not add automated code-checking tests for this task. Preserve the existing end-to-end GitHub notebook execution workflow.
