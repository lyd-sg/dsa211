# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.7 — Seven-per-family, EDA-grounded, sequential 1-SE

**Status:** **IMPLEMENTED AND VERIFIED — PASS**. The executed [v3.7 notebook](online_shoppers_prd_v3_7.ipynb), [full audit](artifacts/prd_v3_7/v3_7_verification.json), and [versioned results](artifacts/prd_v3_7/) satisfy the frozen acceptance criteria.  
**Date:** 5 November 2026.  
**Development provenance:** `planning/prd-v3-7-seven-per-family` → [PR #17](https://github.com/lyd-sg/dsa211/pull/17) → `main`.  
**Computational predecessor:** [executed v3.6 notebook](online_shoppers_prd_v3_6.ipynb), with its [v3.6 requirements](PRD_v3.6.md) and [v3.6 evidence](artifacts/prd_v3_6/).  
**Presentation predecessor:** [v3.5 notebook on main](https://github.com/lyd-sg/dsa211/blob/main/online_shoppers_prd_v3_5.ipynb) and [PRD v3.5](PRD_v3.5.md).  
**Delivered:** [executed `online_shoppers_prd_v3_7.ipynb`](online_shoppers_prd_v3_7.ipynb), with [PASS audit](artifacts/prd_v3_7/v3_7_verification.json) and separately versioned evidence under `artifacts/prd_v3_7/`. `README.md` and `AGENTS.md` have been updated with verified results.

### 1. Objective and development strategy — inherit, do not start from scratch

The project is **prediction-only**, comparing course-appropriate classifiers for session `Revenue=1`. v3.7 is an **incremental successor to earlier iterations, not a new implementation**.

1. **Copy the complete, executed `online_shoppers_prd_v3_6.ipynb` as the computational starting point.** Preserve its data, split, fixed common CV folds, feature engineering, fitted evaluator, sequential one-SE decision engine, inner tuning, diagnostics, trees, results infrastructure, audit, thresholds, and refit workflow. Do not regenerate the project from an empty notebook, rewrite proven core routines, or silently substitute a different statistical design.
2. **Port the substantive EDA and polished reporting improvements from v3.5** into the appropriate existing v3.6 sections; integrate rather than add duplicate sections or figures. In particular recover the saved supplementary investigations and the EDA-to-experiment bridge. Keep the v3.6 computed model results and sequential decisions authoritative; the v3.5 family scores, lineage, and old finalists are historical, **not** v3.7 results.
3. Add exactly two pre-specified BernoulliNB experiments (Section 3), score them with the inherited evaluator, and recompute downstream objects that actually depend on their results. Reuse cached/frozen v3.6 evidence when unchanged; independently check that unchanged sections agree. Do not refit older experiments merely to change display labels or formatting.
4. Apply the curated **seven-per-classifier display** and consecutive presentation-only IDs described in Section 2. Retain the complete computational lineage with original immutable IDs. No reranking, result-driven additions, new model family, broad feature search, or replacement of previously agreed experiments.
5. Preserve v3.0–v3.6 documents, notebooks, scripts, and artefacts; avoid overwriting prior versions. Branch-based delivery with a separate verification record.

The source dataset remains `data/uci_468.csv`: 12,330 observations; the original seed-42 80/20 split is 9,864 training and 2,466 historically consulted reserved rows. Keep all-17 first-pass diagnostics and the operational 16-source restriction, with `PageValues` excluded due to **uncertain prediction-time availability**, not a proven leakage event. Five shared stratified outer training folds remain unchanged.

### 2. Four balanced tables; consecutive presentation IDs

The **visible notebook tables must have consecutive labels** `L0`–`L6`, `D0`–`D6`, `G0`–`G6`, and `B0`–`B6`; no gaps within a displayed table. These are **presentation labels only**. The original experiment IDs and machine-readable trial lineage are not renumbered or conflated. A deterministic ID mapping must exist in the v3.7 evidence and be testable; explanatory notes identify the transformation without forcing readers through legacy gaps.

| Classifier | New visible ID → original experiment ID | Visible transformations / method |
|---|---|---|
| Logistic Regression | L0→L0; L1→L1; L2→L3; L3→L4; L4→L10; L5→L13; L6→L14 | Baseline; activity `log1p`; rare-level pooling; scaled L2; duration-per-page ratio; LASSO; Elastic Net |
| LDA | D0→D0; D1→D1; D2→D3; D3→D4; D4→D9; D5→D11; D6→D15 | Baseline; activity `log1p`; rare-level pooling; covariance shrinkage; fold-p99 winsorisation; binned BounceRates; grouped backward selection |
| Gaussian NB | G0→G0; G1→G2; G2→G3; G3→G4; G4→G7; G5→G8; G6→G9 | Baseline; drop BounceRates; drop ProductRelated; drop SpecialDay; targeted duration `log1p`; targeted administrative-duration `log1p`; remove nominal predictors |
| Bernoulli NB | B0→B0; B1→B1; B2→B2; B3→B3; B4→B4; B5→new B5; B6→new B6 | Baseline; training-median ProductRelated binning; training-median ProductRelated_Duration binning; training-median ExitRates binning; remove BounceRates; binary composite; rare-level pooling |

**Important presentation/lineage rules:**
- Show **exactly 7 scored rows per family** (28 in four tables), subject to the new B5/B6 experiments executing successfully. Keep exactly the approved, diverse seven; do not silently replace a model based on its score.
- Historic omitted trials **still occurred** in the actual sequential timeline, including where a rejected experiment sits between displayed rows. The visible `Retained after iteration` column must be derived from the **true full v3.7 sequential ledger** after that displayed trial, then mapped to the correct consecutive visible ID. Never recompute a shortened seven-step selection that ignores hidden trials.
- Every model **actually retained** at any development step must be among the visible seven for that family; assert this rather than assume it. If new B5/B6 outcomes change the Bernoulli path, derive the column from the executed results, without guessing.
- Preserve historical canonical IDs (including gaps such as L11–L12) **in the full audit**. The presentation labels are aliases and cannot be used as computational configuration keys or mistaken for new trials. For example, visible `L2` is original `L3`, **not** the historically attempted original L2.
- Clearly distinguish an experiment's effect from its inherited configuration: each challenger is evaluated relative to the latest incumbent, **not** necessarily the immediately preceding displayed row.

**Uniform visible table columns, in this order:** `Model`, `CV ROC-AUC`, `AUC SE`, `CV AP`, `ΔAUC`, `Complexity`, `Retained after iteration`. Define `ΔAUC` as challenger mean AUC minus that step's **actual** incumbent mean AUC (not vs a visually adjacent row) and label the baseline `—`. Complexity follows the v3.6 family convention. Use consistent rounding and annotate which specifications are baseline, rejected, or later retained in prose beneath the table without extra administrative columns. The `Retained after iteration` label is **not** an indication that the row was accepted; it reports the surviving candidate.

**Never display** `status`, `trial_version`, `parent`, `decision`, `skip_reason`, `retained_after_step` raw strings, `accepted`, or other internal audit fields as table columns. Do not show skipped specifications, NaNs for them, `SKIPPED_INAPPLICABLE` messages, or a standalone full history dump in the submitted notebook. Retain these in the versioned computational ledger and verification files.

### 3. Two new Bernoulli NB experiments — exact pre-specified hypotheses

Continue **after the historical B4 attempt and its resulting retained incumbent**. Both experiments must use the existing Bernoulli NB with binary inputs, all learning inside the proper fit folds, and the inherited v3.6 sequential 1-SE decision rule.

**B5 — binary composite of correlated product engagement.** Replace the two separate `ProductRelated` and `ProductRelated_Duration` binary inputs with **one** binary indicator:
`I(ProductRelated > median_train(ProductRelated) AND ProductRelated_Duration > median_train(ProductRelated_Duration))`.
Fit both medians on the relevant training fold only and retain all other incumbent features/encodings. Do not leave the original two binary inputs alongside the composite. The EDA motivation is strong within-class dependence of the count and duration (historically about 0.839 for nonbuyers and 0.896 for buyers). This is a **hypothesis** that less duplicated likelihood information could improve Bernoulli NB; the conjunction could also discard useful information. Make sure the new composite logic is compatible with inherited `median_cols`; no double counting.

**B6 — rare Browser and TrafficType level pooling.** On the retained incumbent after B5's selection decision, apply the existing training-fold-only rare-level pooling convention to these two nominal predictors: observed categories with fewer than 50 fit-fold sessions become `__OTHER__`, then one-hot encode as binary inputs. Maintain the fixed unknown-category handling. EDA notes historically four Browser and nine TrafficType categories below 50 on the training data. This tests sparse-category simplification, **not** removal of Bernoulli NB's conditional-independence assumption.

For either proposal, if the original representation has been removed by a retained prior transformation, handle inapplicability explicitly in the audit rather than inventing metrics; the expected seven-per-family reporting contract depends on both new proposals being applicable and scored. Avoid changing B0–B4 or reordering the historic attempts. No new hyperparameter optimisation or threshold tuning is authorised for these trials.

**Results unknown until implementation:** B5 and B6 may be rejected, accepted, or change the Bernoulli family finalist. The overall six-way winner may therefore change; do not pre-write the v3.7 winning model, AUC, AP, threshold, cost estimates, or reserved-set score.

### 4. Preserve v3.6's selection rule exactly

Within each family, compare only the incumbent and one challenger at a time, using the **same five outer CV folds**. Let `best` be the higher **mean CV ROC-AUC** of those two, with incumbent as the exact-AUC tie default:

`SE_best = sd(best's five outer-fold ROC-AUC values, ddof=1) / sqrt(5)`  
`cutoff = mean_auc_best - SE_best`.

Among these **two** candidates satisfying `mean_auc >= cutoff`, retain the **simpler model**. On complexity ties retain the higher-AUC model, then incumbent on an exact tie. Keep v3.6 simplicity definitions: mean nonzero non-intercept coefficients across folds for Logistic, and mean fitted encoded feature counts for LDA/GaussianNB/BernoulliNB (D15 uses nested selected features). Expose complexity and its definition; don't falsely equate binary dummy columns with original feature groups.

**Do not replace this with global best-over-all-experiments selection.** The five-fold one-SE rule is a parsimony heuristic adapted to maximising AUC, **not** a statistical significance test.

Preserve inner 1-SE tuning for Logistic L2/LASSO/Elastic Net (`C`: smallest eligible = strongest penalty), LDA covariance shrinkage (largest eligible), and leakage-safe nested grouped backward source selection for D15. The new displayed IDs must not break the historical mappings from `L4`, `L13`, `L14`, `D4`, and `D15` to their actual fitted recipes. No outer-validation or reserved-set labels may influence preprocessing or inner selection.

### 5. Restore v3.5 EDA and connect it to course materials

Retain v3.6's base EDA and **restore v3.5's additional training-only diagnostics** in the existing Sections 2–4, without duplicating identical code/output:

- Numerical skewness and long tails; appropriate examples: `ProductRelated_Duration`, `Informational_Duration`, `Administrative_Duration`.
- Zero-versus-positive activity rates and positive-value quantiles/intensity.
- Categorical counts and sample support, including `VisitorType × Month` and small cells; do not infer a stable interaction effect from sparse combinations.
- Rare `Browser`, `TrafficType`, and `Region` levels.
- `SpecialDay` exact scores versus positive presence.
- Original-source feature availability/timing checks, including the caveat around `PageValues`.
- Within-class correlations, Q–Q/tail checks, and binned marginal purchase rates/empirical logits.
- A concise EDA-to-experiment bridge connecting each supported observation to a visible modelling hypothesis or appropriately explained audited alternative.

Restore figures only when they communicate separate evidence, preserve the lecture/lab style **purpose → code → specific output → interpretation → next modelling implication**, and distinguish descriptive EDA from predictive CV evidence. Do not imply log transforms prove Gaussianity, category pooling automatically improves performance, or marginal patterns establish multivariable/causal effects.

**Course/lab coverage check (explicit pre-build and post-build audit):**
- Lecture 2/Lab 2: main effects, categorical coding, nonlinear/polynomial and interaction concepts. The duration-per-page combination (`L4` visible = historic L10) is a course-aligned derived feature. Do not force `VisitorType × Month` interaction despite sparse cells; note why if relevant.
- Lecture 4: collinearity, drop/combine remedies, functional form, transformation. The B5 composite is a direct adaptation to Bernoulli's binary feature space.
- Lecture/Lab 6: generative classifiers, independence and distribution assumptions, Bernoulli binarisation. Avoid unjustified `log1p` applied directly to Bernoulli's binary variables.
- Lecture 7/Lab 7: pipelines, leakage-safe CV and polynomial features; quadratic `BounceRates` historical L5 and piecewise L8 are tested **audit-only** examples under the seven-row cap. Discuss them only if material; never claim they were not evaluated.
- Lecture 8: subset and stepwise selection and one-SE; D15 is a nested **grouped backward LDA adaptation**, not an identical demonstration of forward stepwise regression.
- Lecture/Lab 9: Ridge, LASSO, Elastic Net and CV penalty selection; original historic L4/L13/L14 are **penalised logistic extensions** of the linear-regression penalty concepts, identified accurately.
- Lecture 10: Gini/Entropy classification-tree pruning and selection.

Do **not** force every syllabus topic into a model experiment. PCR/PLS are overview material, and interactions should not be added without adequate support. Coverage means grounded justification of the experiments performed, not a compulsory demonstration of every statistical transformation on all four classifiers.

For every **visible** family trial, give a concise, correct commentary below its table covering the single change, specific EDA motivation, classifier-specific rationale, actual inherited parent (in prose if needed), and **actual sequential 1-SE retention result**. Statements from v3.5 about old retained finalists and their scores must not be reused uncritically.

### 6. Tree placement and six-way comparison

Keep the **existing v3.6** Gini and Entropy pruning implementation and exact alpha-path methodology. In Section **7B**, show only the **four concise rows**: full Gini, pruned Gini, full Entropy and pruned Entropy, with their relevant AUC/AP/complexity metrics. Place the **pruned Entropy tree plot immediately after this table, in Section 7B**, **before** Section 8's six-way comparison. Do not duplicate the plot elsewhere or add a standalone full-alpha notebook table. Preserve all tree alpha-fold evidence under versioned artefacts.

After B5/B6, recompute the four family finalists plus two tree finalists ranking. Select the **highest mean five-fold training ROC-AUC across six**; AP supports interpretation but does not break from the frozen ranking convention. Do **not** apply a new global one-SE simplicity rule across classifier families. Update winner-dependent ROC/PR, score histogram, confusion matrices, threshold examples, hypothetical cost illustration, training fit and full-data refit only if the winner changes (otherwise verify preserved outputs).

### 7. Notebook readability / table hygiene

- Restore clear sectional hierarchy and short purpose/method/interpretation text matching v3.5.
- Standardise the seven-column model tables, per-model annotated transformations, controlled decimal precision and sensible figure labels.
- Remove unnecessary technical printing (`Fitting...`, `recomputing...`, skipped statuses), wide audit/status/lineage tables, verbose tree hyperparameter paths and raw metadata dictionaries from the notebook's presentation.
- Do not delete or weaken programmatic assertions, reproducible evidence, or full audit records merely to remove their visible prints.
- The tree figure stays in the tree section. All visual evidence appears where first discussed, not after the final selection.
- No obsolete v3.5/winner assertions, no stale counts, no misleading `7`-per-family label for unscored or hidden skipped trials.
- Retain original split and deployed-input caveats, no causal/economic-impact claim.

### 8. Counts and audit evidence

The existing v3.6 plan had **41** original-family trial IDs, of which **five** were inapplicable under its newly retained pathway (`D5,D6,D8,G5,G6`) and **36** were scored. v3.7 proposes **two** additional Bernoulli trials:

| Measure | Expected v3.7 |
|---|---:|
| Planned original-family trial ledger entries | **43** |
| Previously skipped original-family trials | **5** |
| Expected scored original-family trials if B5/B6 run | **38** |
| Scored originals shown in four visible family tables | **28 = 7 × 4** |
| Other scored originals retained only in audit | **10** |
| Separately shown tree full/pruned comparison rows | **4** |
| Finalist comparison | **6 = 4 original families + 2 pruned trees** |

These counts were **confirmed by the executed v3.7 notebook and independent PASS audit**. Preserve the remaining ten scored trials and five skipped trials in `artifacts/prd_v3_7/all_attempts_ledger.csv`, and retain the exact canonical IDs alongside aliases and complete fold-level metrics. In particular, skipped trials exist **only as audit entries**, never as visible table rows. Ensure the actual ledger/fold counts reconcile; fail verification if an unexpected additional skip prevents seven scored display rows.

Keep original `artifacts/prd_v3_4/`, `artifacts/prd_v3_5/`, and `artifacts/prd_v3_6/` untouched. New evidence includes a presentation-ID mapping file, complete attempts/decisions, all fold scores, family configurations, nested selection diagnostics, tree pruning evidence, final six-way comparison, winner-dependent metrics and run metadata.

### 9. Frozen verification and acceptance criteria

**A. Inherited baseline and compilation**
1. v3.7 is structurally derived from the **executed v3.6 notebook** and integrates the v3.5 EDA/presentation assets; do not create a fresh notebook from scratch or manually fabricate saved outputs. Proven model kernels stay unchanged except the minimal B5/B6 integration, label rendering, and their necessary downstream propagation.
2. Valid notebook `nbformat` v4; cells execute top-to-bottom without errors; no stale outputs, spurious `SKIPPED` prints, or unverified results labelled v3.7.
3. Dataset size, source hash, split IDs, common outer folds, 17-to-16 feature policy and fixed original experiments remain identical to v3.6. Verify unchanged numerical results and trees against the existing executed evidence.
**B. Method and lineage**
4. Audit 43 planned IDs and the actual scored/skipped counts; require B5 and B6 to execute to meet the 7×4 display contract. Assert no removed predictor is reintroduced, no binary composite is double counted, and no encoding/median leaks across folds.
5. Independently recompute each sequential best-AUC-minus-best-SE cutoff, eligible candidate set, simplicity tie break, true incumbent, retained pathway and complete fold-level counts. Validate inner one-SE tuning and the four family finalists.
6. Cross-check that **every accepted historical step** is represented by a displayed row. Independently verify that the `Retained after iteration` alias matches the actual full ledger after each displayed original trial, even across hidden intermediate steps.
**C. Presentation and syllabus**
7. Exactly seven visible scored rows with consecutive IDs `L0–L6`, `D0–D6`, `G0–G6`, `B0–B6`; the seven standard columns and correct true-incumbent ΔAUC. A consistent canonical-to-display mapping is preserved in artefacts.
8. v3.5's substantive EDA/interpretations restored, with specific EDA-to-change links; every showcased technique checked against the relevant lectures/labs, and extensions explicitly named. No forced interaction/PCR/PLS experiments.
9. Exactly four tree full/pruned comparison rows; pruned Entropy illustration **before** six-way ranking in Section 7B; no duplicated large trial/alpha ledger or status fields displayed.
**D. Outcome, preservation, documentation**
10. Six-way ranking, ROC/PR and threshold-related displays correspond to the **new actually scored final winner**, not a presupposed v3.6 winner. A historically reused reserved check is expressly **non-pristine** and is never consulted to choose the winner.
11. Versioned numerical and presentation audit returns an explicit `PASS` or `FAIL`; no claim of successful execution until it is demonstrated and evidence committed.
12. After notebook verification, update **`README.md`**, **`AGENTS.md`**, and the appropriate version references to make v3.7 the current project, give correct run instructions, counts, finalist values and evidence paths. Do not change the README to claim v3.7 is current before the notebook exists and passes audit. Preserve earlier source and archive links.

### 10. Guardrails and limitations

The repeated training CV folds and reserved observations have informed historical model development; additional B5/B6 experimentation can increase selection optimism. The sequential one-SE rule is not a hypothesis test or guarantee of true model equality. ROC-AUC/AP evaluate ranking, not calibrated probabilities. Threshold economics use hypothetical assumptions, and the reused reserved check is **not an untouched independent test**. Neither classifier coefficients nor EDA relations establish a causal effect of purchasing-related interventions.

**Implementation boundary:** The approved change is an incremental v3.6→v3.7 presentation and EDA restoration, with **only B5/B6** as genuinely new model hypotheses. If new numerical outcomes require updated conclusion/refit, make those changes; otherwise preserve and verify existing computations. **Do not build from scratch.**

### 11. Execution closeout (5 November 2026)

The source notebook executed **all 31 code cells with no error outputs** and passed independent verification: **43 planned**, **38 scored**, **five skipped**, **28 consecutive display aliases**, **34 independently verified sequential decisions**, **48 evaluated CV designs** and **240 fold scores**. Both original tree pruning workflows were checked (722 alpha candidates and 3,610 alpha-fold values). All seven-row classifier display tables and EDA restorations are present; the Entropy tree plot is in Section 7B before the overall comparison.

**New Bernoulli trials:** B5 (composite) AUC **0.74003** and B6 (rare-level pooling) AUC **0.73953**, both retained for greater simplicity under the sequential 1-SE rule. The final Bernoulli NB specification is original/displayed **B6** (mean AP **0.30574**).

**Final six-way winner:** original **L13 Logistic Regression**, displayed **L5**, with mean five-fold training CV ROC-AUC **0.75892** and mean AP **0.34236**. The next-ranked pruned Entropy tree AUC was **0.74414**. The historically consulted reserved sample scored AUC **0.74313** and AP **0.33358**; these **are not independent generalisation estimates**, because earlier versions examined that sample.

The authoritative machine-readable closeout is [`artifacts/prd_v3_7/v3_7_verification.json`](artifacts/prd_v3_7/v3_7_verification.json), with all full historical trial IDs, family configurations, fold scores, presentation-ID mapping, trees, and evaluation outputs preserved in the versioned artefact folder. No unapproved new model families or experiments were introduced.
