# Technical implementation plan — v1 — 25 October 2026

Status: **APPROVED for staged implementation by independent Sol review** in `technical_plan_review.md`. Initial PASS authorises supplementary training EDA; exact recipe addendum needs its own independent PASS before model implementation. Owner's current attachment authorises that independent gate and automatic implementation after PASS. PRD v1.0 remains unchanged.

## Files and task boundaries

| File | Change and requirement |
|---|---|
| `online_shoppers_revised.ipynb` | Replace active analysis with self-contained executed A1–A14 notebook; PRD §§3–11 |
| `supplementary/training_eda.ipynb` | Separate executed five-investigation training-only EDA; §§1, 5.1; not submitted |
| `archive/online-shoppers/online_shoppers_pre_prd_v1.ipynb` | Byte-for-byte preserve pre-revision active notebook; governance/history |
| `docs/repository_audit.md` | Source conflicts, retained work, original course-material availability and risks |
| `docs/technical_plan.md`, `docs/technical_plan_review.md` | Approval, recipe evidence addendum and independent review history |
| `docs/verification_report.md` | Criterion-by-criterion acceptance, actual execution, arithmetic and limitations |
| `docs/implementation_log.md` | Sol task instructions, Luna implementation/execution and Sol inspection/corrections |
| `AGENTS.md`, README, `docs/{project_decisions,methodology,phase2_scope,requirements_audit,revision_summary}.md` | Reconcile current entry points, protocol and actual results with approved PRD; remove stale current-result claims |
| `requirements.txt` | Record reproducible working package versions; retain necessary notebook dependencies |
| `artifacts/` | Compact audit evidence: split/fold row IDs, CV/fold tables, warnings, frozen decision, single test predictions/metrics, numerical summary and run provenance; no new experiments |

No edits to `docs/PRD.md`, `data/uci_468.csv`, existing archive files or original workflow. Scratch builders, execution logs and plot previews go in ignored `work/`. Export review copies for delivery outside the repository. A final model object may be written locally during full refit; self-contained notebook code recreates it, so an unsafe/version-sensitive pickle is not required for academic delivery.

## Protocol and data contract (PRD §§4, 6, 7)

Verify shape 12,330 × 18 and expected names, target boolean/0–1 values, types, missing markers including blank strings, finite numerics, duplicate excess/unique count and class balance **before splitting**. Retain all rows. Reverify duplicate nonbuyer/low-activity description with an explicitly basic quality summary, not a feature-selection analysis. Describe what the activity values actually show rather than defining “low” after viewing test data. Store original CSV row IDs.

Split row IDs once with `train_test_split(test_size=.20, stratify=y, random_state=42)` to 9,864/2,466. The supplementary notebook independently reconstructs that same deterministic split and immediately drops all nontraining rows. Main keeps test inaccessible to all EDA and candidate routines. Five shared `(fit, validation)` positional index arrays from `StratifiedKFold(5, shuffle=True, random_state=42)` are materialised once on training. Persist original row IDs/fold membership for review; each row gets exactly one OOF prediction per specification. No grouped split is possible without visitor identifiers.

Define six nominal columns: `Month`, `OperatingSystems`, `Browser`, `Region`, `TrafficType`, `VisitorType`; cast them consistently to strings without imposing numeric ranks. `Weekend` is numeric 0/1. All other predictors are numeric, including `SpecialDay`. Nine numeric predictors remain after removing `PageValues`, plus Weekend and six nominal variables = 16 sources. No fitted categories or scaling constants come from full data. `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` learns fold categories and deterministic sorted order; unseen levels become all-zero blocks. Explain that unknown levels are effectively mapped to a reference under k−1 encoding and lack a dedicated observed effect. Record actual warnings, unseen-level occurrences and encoded dimensions. No imputation silently repairs a failed completeness contract.

## Notebook sequence and evidence map

Each row below becomes an explicit purpose before code, followed by concise actual-result interpretation and implication. Setup cells need no ritual analysis headings.

| PRD block | Purpose | Python method / expected evidence | Interpretation / decision |
|---|---|---|---|
| A1 | Is the dataset usable, and why avoid accuracy alone? | Quality/type/duplicate/missing and balance tables, source hash; split/fold counts | Retain rows, disclose repeated patterns; AUC primary/AP secondary |
| A2 | Which numeric distributions challenge likelihoods/representations? | Training median, skew, zero shares and selected raw/log-view histograms | Generate limited representation hypotheses; no automatic improvements |
| A3 | Which categorical groups differ with adequate support? | Month/VisitorType counts and buyer rates, annotate n | Retain nominal encoding; sparse groups are uncertain, not causal |
| A4 | Which model assumptions are strained? | Selected within-class numeric correlations; representative class QQ plots and binned empirical-logit shape | Dependence/long tails motivate conditional recipes; marginal plots do not prove conditional linearity or certify Gaussian assumptions |
| A5 | What changes when starting with all predictors? | Four all-17 same-fold baseline results, compared to their four operational equivalents | PageValues association is not proof of leakage; exclude for possible timing/availability |
| A6 | How do the four taught baselines compare? | Raw operational Logit, GaussianNB, BernoulliNB and LDA means/SD/SE/AP | Common 16 source inputs; input likelihoods differ as explicitly required |
| A7 | Does an observed issue justify each family revision? | Supplementary evidence table, three frozen recipes and before/after mean CV changes | Record adverse or null changes; no search for a better recipe after scoring |
| A8 | Which specification ranks sessions most defensibly? | Seven-slot same-fold table, per-fold AUC/AP, overlaid OOF ROC curves | Choose highest mean AUC with deterministic label exact-tie break; report one-SE proximity descriptively without automatic substitution |
| A9 | Are winner scores extreme/concentrated? | Training OOF histogram stratified by observed outcome | AUC is ranking, not calibration; fixed thresholds may behave oddly |
| A10 | What trade-offs do four supported thresholds create? | OOF sensitivity/specificity curve and four-row threshold/rates/precision/voucher/revenue table | Keep 2/3 primary regardless of simulated revenue |
| A11 | How assumption-dependent is voucher revenue? | Exactly q=.10,.25,.50,1, fixed assignments and 2/3, OOF table and same frozen test prediction illustration | q is unidentified; simulation in A units, not measured uplift/profit |
| A12 | Does the frozen winner generalise under this protocol? | Fit on all training; one test `predict_proba` call, ROC/AUC/AP, labelled confusion matrix and rates at 2/3 | Honest single-winner audit with historical exposure caveat; no post-test revisions |
| A13 | What final fit uses all observations? | Clone exact chosen pipeline, fit 12,330 rows after audit; report class/feature/dataset size and parameters | No further scoring; earlier audit metrics remain reported |
| A14 | What does evidence support? | Computed concise summary of winner, baseline/revision deltas, threshold/q findings | Prediction versus policy assumptions; timing, dependence, duplicates, imbalance, selection and history limits |

## Minimal baselines, solvers and shared CV

For all-17 diagnostic versions and 16-source operational baselines use exactly the PRD treatment: original numeric magnitudes and SpecialDay for Logit/GaussianNB/LDA, numeric `>0` indicators for BernoulliNB, Weekend 0/1 throughout; full k one-hot for both NB types and k−1 for Logit/LDA. No scaling, penalties, class weights, optional logs, feature removal or engineering in baselines. BernoulliNB uses `binarize=None` after explicit binary conversion, default alpha=1 and empirical class priors; GaussianNB uses default variance smoothing; LDA uses standard SVD solver.

Use `LogisticRegression(C=np.inf, solver='newton-cg', tol=1e-7, max_iter=2000)` for unpenalised ML Logit on installed sklearn 1.9.1, intercept fitted. (`penalty=None` is the equivalent older API, not an added penalty.) Newton-CG handles disparate raw feature scales without altering representations. Capture convergence warnings, iteration counts, finite coefficients/probabilities, encoded design rank and conditioning where relevant. Examine each training fold's category-by-outcome support for pure rare levels and report separation risks explicitly: finite returned coefficients/no warning do not prove a finite MLE exists. Where boundary estimates or numerical concerns arise, check training objective and validation-prediction stability under stricter tolerance/more iterations for the identical statistical specification, without using test data or selecting settings by validation AUC. Record stable finite-iterate predictions as such, never a certified finite MLE; escalate if reliable predictions cannot be obtained. A numerical retry may increase iterations or switch to another unpenalised solver without changing the statistical specification, with attempt provenance. Do not declare failed/nonconverged estimates valid. If baseline cannot be estimated reliably after numerical remedies, preserve actual failed row and escalate genuine PRD feasibility issues rather than regularise silently. LDA SVD can accommodate deficient rank but record warnings/encoded rank; do not substitute numeric-only LDA as baseline.

CV fits clones inside each training fold and uses positive-class probability matching `classes_==1`. Retain all OOF vectors and fold AUC/AP, means, sample SD (`ddof=1`), SE (`SD/sqrt(5)`). First-pass models are diagnostics only and excluded from winner selection. All seven operational slots have equal eligibility, same folds and primary metric. Preserve warning/failure logs rather than suppressing them. The winner is highest mean AUC; exact ties resolve by label. Discuss any simpler models within one SE, but choosing the highest is precommitted here. No candidate is selected by voucher performance.

## Supplementary EDA and conditional revision gate

After initial plan PASS, Luna implements and executes **only** training EDA first. This is required because PRD §5.1 intentionally defers exact recipes. Sol inspects the actual evidence; write a recipe addendum and obtain independent PASS on it **before model implementation/scoring**. No new technical approval from the owner is needed. This is a staged implementation gate, not permission for an adaptive search.

Five investigations: (1) zero versus positive counts/buyer rates and positive-only quantiles/intensity bins for Administrative/Informational measures; (2) VisitorType×Month support and buyer rates; (3) counts/rare-level buyer rates for TrafficType, Browser, Region; (4) SpecialDay value-level support and buyer rates; (5) complete source-predictor availability table, distinguishing observed session summaries from speculative decision-time availability.

A narrow decision rule determines one revision per family from actual training evidence, without comparing alternatives by AUC:

- **Logit:** if activity magnitudes have marked positive-tail skew (absolute skew >2) and empirical-logit evidence makes a simple monotonic compression plausible, a single log1p treatment of the six count/duration activity variables is eligible. Include fixed `>0` indicators only for activity columns with training zero share ≥50% and supported zero/positive evidence; if used, learn the zero-share eligibility inside each CV fold. No interaction sweeps, optional scaling or penalisation. If evidence does not justify this form, record no distinct revision rather than invent one.
- **NB:** mixed Gaussian-numeric/categorical-nominal likelihood is eligible if continuous skew/zero structure and nominal support show why using Gaussian dummy marginals or discarding all intensity is questionable. Permit log1p on the same activity magnitudes only when distributional evidence supports compression; treat Weekend as Bernoulli or two-level categorical, SpecialDay as numeric unless its evidence warrants a binary presence treatment. Use one prior exactly once. Learn categorical maps on fit fold with reserved unknown support and Laplace smoothing. Explain as conditional-independence extension, not an additional baseline. No alpha or variance-smoothing search.
- **LDA:** same single activity-log1p treatment is eligible if within-class tails/covariance patterns support a less extreme representation. Keep k−1 nominal dummies and all 16 sources unless evidence explicitly supports a change. No automatic feature deletion, covariance-shrinkage competition or interaction expansion. If no defensible distinct form, explicitly mark the revision slot uninstantiated and explain.

Global training EDA informing a finite candidate set is allowed, but creates adaptation optimism in training CV; the holdout audits the frozen winner. Transformations with learned thresholds/parameters fit inside folds; log1p and `>0` are fixed formulas. Main notebook reproduces compact decision-relevant evidence directly from training rather than relying on a live supplementary kernel or importing external helpers.

## Thresholds and voucher arithmetic (PRD §8)

Policy uses `p >= t` → buyer/no voucher, otherwise voucher. Always use exact `PRIMARY_THRESHOLD=2/3`, discount `.20`, reference q `.50`. Costs are `.20A` for FN and `.40A` for FP, hence cutoff `.40/(.40+.20)`; meaningful probabilities and those assumed opportunity costs are required for that theoretical rationale.

Four OOF references only: exact `y_train.mean()`, `.5`, `2/3`, and sensitivity–specificity crossover. Define crossover reproducibly by all empirical OOF ROC cutoffs (no dropped intermediate points), restricted finite probabilities in [0,1] plus endpoint cutoffs; minimise absolute sensitivity–specificity difference, tie by lower cutoff. The curve can use the same cutoffs. Show sensitivity, specificity, precision (undefined if no predicted buyers, labelled), TP/FP/FN/TN, voucher count/share, R0/A, Rq/A and delta/relative delta at q=.50. Reference rows stay labelled even if numeric thresholds coincide. No revenue-maximising threshold scan or threshold substitution.

For fixed confusion counts, `R0/A=TP+FN`, `Rq/A=TP+.8*FN+.8*q*TN`, `delta/A=.8*q*TN-.2*FN`. Four q scenarios hold every other quantity fixed, at 2/3 only. OOF q results may precede test; test illustration reuses its sole saved predictions. Validate algebra against recipient-level expected revenue without additional model fitting/prediction. q=1 recovers guaranteed conversion as a scenario, not baseline truth.

## Supervision, execution and acceptance sequence

1. Sol completes audit and plan; independent fresh-context Sol reads PRD and records substantive PASS/FAIL. Fix all material findings before implementation.
2. Luna (requested medium thinking) implements supplementary training EDA; executes it with `.venv`. Sol inspects source/output, checks training IDs, and reviews evidence; reviewer approves recipe addendum.
3. Luna implements main data/EDA/pipelines and training-only comparisons/thresholds, stopping before test. Sol inspects actual encodings, estimator parameters, numerical diagnostics, common folds, seven slots, formulas and warning records. Correct until PASS.
4. Freeze model, preprocessing, fold definition, selection rule and 2/3 policy in an audit manifest before test. Luna executes complete notebook through one-winner test audit and final all-data refit once. Preserve executed notebook, test prediction vector, freeze record and machine-readable metrics. Re-execution for reproducibility must not introduce another candidate or alter decisions; prefer independent checks of saved evidence after the audit.
5. Sol and independent reviewer inspect actual code and outputs, recompute AUC/AP/rates from saved prediction vectors, reconcile confusion totals and verify algebra against a separate direct calculation. Inspect each chart/label and purpose/evidence/implication. No automated code-checking test suite; visible runtime assertions and manual numerical verification are appropriate.
6. Reconcile supporting docs, verify unchanged PRD/data/archives and prior active copy, and write acceptance table with every §11 criterion, evidence and outstanding limits. Export executed notebooks and HTML review copy. Commit and push completed branch (no force push, no merge); report actual branch/SHA. If access/CI cannot be verified, state exactly what was not performed rather than claiming success.

Only test-independent presentation or reporting fixes are permitted after audit, using preserved predictions. Any genuine post-audit modelling defect must be disclosed explicitly; never silently rerun and relabel an audit as untouched. Successful execution alone does not establish statistical correctness.
