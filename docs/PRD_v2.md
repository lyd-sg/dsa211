# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v2.0

**Status:** APPROVED by the project owner on 27 October 2026, following sequential review of the final two open items.  
**Supersedes:** PRD v1.0 as of 27 October 2026. The earlier [PRD v1.0](PRD.md) is preserved unchanged for provenance.  
**Implementation state:** Requirements document only. The current [main notebook](../online_shoppers_revised.ipynb) still contains the old voucher policy; this PRD does not claim the notebook is updated.  
**Scope:** One prediction objective. No voucher economics.

---

## 1. Research question and deliverables

**Research question**

How well do variables describing an online browsing session predict whether that session ends in a purchase (`Revenue = 1`), and which of the DSA211 classification specifications provides the most defensible predictive performance?

**Objective**

- **Prediction only**, not coefficient inference, causal inference or a business-case optimisation exercise.
- Compare the three course-model families: Logistic Regression, Naive Bayes (NB), and Linear Discriminant Analysis (LDA).
- Use the agreed seven-candidate comparison: **four minimally processed baselines and three EDA-informed revisions**.
- Select one model by **highest mean five-fold training CV ROC-AUC**. Report average precision (AP), fold variability and ROC/PR evidence to make class imbalance explicit.
- Interpret the winner using training out-of-fold (OOF) purchase probabilities and threshold sensitivity analysis. Use the **sensitivity–specificity crossover** as the balanced operating reference, **not** an economically or universally optimal threshold.

**Deliverables**

- One self-contained, top-to-bottom executable, submission-ready **main Jupyter notebook** with concise lab-style code, results, charts and interpretation.
- A separate **supplementary training-only EDA notebook** retained in the repository but **not submitted**. It supports substantive hypotheses and must not duplicate entire analyses in the main notebook.
- Reproducibility and review evidence in repository documentation and artifacts; historical analyses preserved and clearly labelled.

**Removed from scope**

- Voucher targeting/allocation and the 20% discount.
- Fixed 2/3 or 0.667 purchase cutoff, voucher-derived costs, assumptions about incremental conversion, revenue/profit arithmetic, and all hypothetical voucher scenarios.
- Any claim about uplift, treatment effects or a deployable real-time pricing/discount policy.

These removals apply to **all notebook prose, visuals, tables, conclusions and supporting documentation that presents current decisions**. Historical archived records may remain, clearly labelled as obsolete.

## 2. Decision authority and implementation gates

1. Verified mandatory professor/assessment instructions take precedence.
2. **This approved PRD v2.0** supersedes conflicting provisions of v1.0 and older technical-plan/repository guidance.
3. A revised technical implementation plan must be reviewed and approved independently before notebook implementation; prior plan approvals applied to earlier scope and do not automatically approve new modifications.
4. The completed implementation must be independently checked against the final approved v2.0, including source code, numerical outputs, figures, statistical claims and provenance.
5. **PRD approval does not mean the implementation or its evaluation has passed acceptance.** The revised technical plan and notebook must still be reviewed and verified.

**Source of decisions:** PRD v1.0 (27 approved earlier project choices); the subsequent seven-model regularisation revision; and the detailed 26 October PRD v2.0 review. In that review, Changes 1–6 were agreed. On 27 October the owner approved the limitations, acceptance and implementation safeguards (Changes 7–9), subject to a concise submission narrative that reports training CV performance without describing the development history, and approved the unchanged full-data final refit. Sections 10–12 incorporate those approvals.

## 3. Non-negotiable notebook writing and presentation

Every **substantive** notebook analysis must answer:

- **Purpose:** What question are we addressing, and why does it matter for prediction?
- **Evidence/method:** What specific data, plot, code or result answers the question?
- **Interpretation:** What does the output establish, and what does it not establish?
- **Implication:** What change, modelling choice, limitation or conclusion follows?

**Execution/presentation rules**

- Use short, direct British English, concise bullets and meaningful headings. Put each prominent/bold heading on its own line.
- A purpose sentence followed by **one to three relevant interpretation sentences** is often enough. Avoid generic textbook paragraphs in the submitted notebook.
- Retain the **lab style**: runnable code → actual output → specific statistical interpretation. Tables should contain only results needed to answer the analysis question or displayed in the taught workflow.
- **Each essential curve/table appears exactly once** in the main notebook. Edit/reuse the original rather than duplicating ROC, PR, sensitivity–specificity, threshold or summary displays in multiple sections.
- No orphan plots, gratuitous diagnostics, repeated model-summary dumps, duplicated tables, empty boilerplate headings, exercises, placeholders or artificial word/plot quotas.
- Internal convergence/failure assertions and provenance may be extensive, but **do not display long warning/failure/check tables** in the academic narrative. Explain material failures or remedies succinctly and keep audit evidence accessible separately.
- For substantive comparisons, state the **actual before/after numbers**, direction and magnitude (for example, AUC improved from X to Y, by Z), and distinguish meaningful changes from very small ones.
- Supplementary EDA should complement—not repeat—the main notebook. Bring only decision-relevant supporting evidence into the submitted notebook.

## 4. Dataset, validation design and leakage prevention

| Design item | Requirement |
|---|---|
| Source | UCI Online Shoppers Purchasing Intention dataset |
| Unit | **Browsing session**, not identifiable unique customer |
| Records | **12,330**; 17 original predictors and binary `Revenue` |
| Missingness and types | Check actual missing/blank markers, numeric finiteness, categorical types and binary outcome before modelling |
| Duplicates | **Retain all 12,330 rows**, including **125 excess exact duplicate full rows**; do not infer repeated rows identify the same real-world session/person |
| Positive-class prevalence | Approximately **15.5%** buyers; report actual observed shares and explain why accuracy alone misleads |
| Split | One stratified **80/20**, seed **42**: **9,864 training**, **2,466 historical holdout** |
| CV | **Five-fold shuffled stratified** CV on the training partition, seed **42**, identical fold memberships for every candidate |
| EDA and selection | **Training only**: outcome associations, feature decisions, candidates, transformations and threshold comparisons |
| Preprocessing | Fit learned encoders, scalers, mappings, presence eligibility and covariance estimates separately within each CV fitting fold |
| Independent test reporting | **No new independent test performance estimate is reported for the selected revised model**; mean training CV performance is the model-comparison evidence |

**Order:** confirm data quality → partition once → train-only EDA → specify and freeze candidate recipes → compare on common CV folds → freeze the winner/operating reference → perform supported final-fit/reproducibility audit, with evaluation limitations disclosed.

**Reporting boundary:** the professor's ideal workflow is *choose by training CV → refit on training → evaluate on a truly independent test set once → refit the unchanged specification on all data*. This revision **reports training five-fold CV evidence, not a new independent test estimate**. No test AUC/AP is attributed to the newly selected L2 model. A future independent test would require genuinely new, previously unused evaluation data. In the submitted notebook, state this scope concisely without a development-history narrative or any claim that a holdout was untouched.

## 5. Analytical workflow and required purposes

| Block | Required question and evidence | Required decision/interpretation |
|---|---|---|
| **A1 — Quality and imbalance** | Shape, types, missingness, excess duplicates, buyer prevalence | Establish analysis readiness; retain duplicates; reject accuracy-only evaluation |
| **A2 — Numerical EDA** | Focused medians, zeros, skewness, count/duration plots | Explain long tails and absence-versus-intensity hypotheses |
| **A3 — Categorical EDA** | Category counts, buyer rates and sparse levels; informative `Month`/`VisitorType` examples | Identify predictive group patterns without over-interpreting rare cells |
| **A4 — Relationships/assumptions** | Within-class dependence, selected correlations, Q–Q or empirical-logit checks where relevant | State what challenges NB/LDA/Logit and what correlations do **not** prove |
| **A5 — All-17 diagnostics** | Four original model families using all 17 source predictors; compare identical-fold results with the operational equivalents | Describe `PageValues` association and its **potential decision-time leakage**, without declaring association itself proof of leakage |
| **A6 — Four operational baselines** | Logit, Gaussian NB, Bernoulli NB, standard LDA with the 16 retained source predictors | Provide a transparent unenhanced reference with model-required representations only |
| **A7 — Three justified revisions** | One feature/estimator recipe per family, supported by EDA | Explain hypotheses, trade-offs and remaining assumptions; no arbitrary winner-seeking feature sweep |
| **A8 — Seven-candidate CV comparison** | Single seven-row CV table, fold AUC SD/SE, mean AP; one seven-model training-OOF ROC overlay | Choose by highest mean CV ROC-AUC; acknowledge small gaps and training-informed selection optimism |
| **A9 — Winner predictions and PR evaluation** | One winner OOF probability distribution; one PR curve with AP; explain prevalence baseline | Interpret score overlap, minority-class detection, ranking versus calibration |
| **A10 — Threshold sensitivity** | One sensitivity–specificity-versus-threshold curve with crossover; one **three-threshold** table based on training OOF | Compare prevalence, 0.500 and crossover for sensitivity, specificity and precision; adopt crossover as the balanced reference |
| **A11 — Selected-model fit/stability** | Refit the exact selected recipe on all 9,864 training sessions; finite-parameter/probability and convergence checks | Verify the trained specification is computationally usable; training fit is not independent predictive validation |
| **A12 — Evaluation boundary and all-data refit** | State that current predictive assessment uses five-fold training CV; retain version-specific results in the repository; refit the exact winner on all 12,330 observations for the final recipe | No new independent test claim, no newly tuned specification on full data and no in-sample score presented as validation |
| **A13 — Conclusion** | Answer research question using actual CV AUC/AP and threshold evidence | Distinguish prediction ranking, cutoff performance, numerical stability, calibration and limitations |

The earlier v1.0 A10–A14 business-economics sequence is **replaced**, not retained under new headings. There is no voucher or revenue analysis block.

### 5.1 Supplementary training-only EDA — five focused investigations

| Investigation | Statistical purpose / action |
|---|---|
| Zero versus positive activity, then intensity among positives | Determine whether log1p and/or activity-presence features are defensible |
| `VisitorType × Month` group patterns | Investigate apparent interactions with adequate cell counts; **do not** add interactions solely because rates vary |
| Rare categories (`TrafficType`, `Browser`, `Region`) | Avoid unstable pure-class estimates; consider pooling only if supported, not automatically |
| `SpecialDay` interpretation | Check whether original proximity magnitude or a presence indicator is more defensible for a particular family |
| Availability when prediction must be made | Check whether source fields could exist at prediction time; do not claim operational mid-session feasibility |

A null/negative finding matters. No automated sweep of transformations, interactions or hyperparameters for the largest AUC.

## 6. Source variables and baseline treatments

The **four first-pass all-17 models** are a diagnostic step and **not part of the seven-model operational selection**. Exclude `PageValues` from operational models because whether the information exists **before a prospective classification decision** is unclear. Its strong observed purchase association does **not by itself** establish leakage. The remaining fields are likewise not automatically certified usable in real time.

All four operational baselines use the **same remaining 16 original predictor sources**.

| Predictor treatment | Unpenalised Logit | Gaussian NB | Bernoulli NB | Standard LDA |
|---|---|---|---|---|
| Numeric counts, durations, rates | Raw numeric | Raw numeric Gaussian marginals | Indicator `1[x > 0]` | Raw numeric |
| `SpecialDay` | Original numeric | Original numeric | `1[x > 0]` | Original numeric |
| Six nominal categoricals | `k-1` one-hot dummies | Full `k` indicators | Full `k` indicators | `k-1` dummies |
| `Weekend` | Original 0/1 | Original 0/1 | Original 0/1 | Original 0/1 |

- Baselines do **not** add optional log transforms, standardisation, weights, automatically selected features or regularisation.
- Bernoulli's `>0` input conversion is **model-required**, and deliberately discards magnitude.
- Nominal variables remain nominal; their integer labels are not treated as an artificial ordered numerical scale.
- For Logit and LDA, omit a dummy reference level. For NB, retain full-category representation required by the selected approach, while acknowledging dependencies between indicators of the same source.
- Fit category encoders inside each fitting fold; specify and audit deterministic handling of previously unseen validation levels.
- Correlated predictors are permitted under LDA; conditional independence is an NB modelling assumption. Logit does not require normally distributed inputs.

## 7. The three latest EDA-informed revisions

**Exactly seven operational specifications** are the accepted current comparison: four above, plus the following three. Preserve the regularisation revision already validated on GitHub; v2.0's policy edits do not silently undo model development.

### 7.1 Revised Logistic Regression

- Keep all **16** original operational source predictors.
- Apply `log1p` to the **six activity count/duration** fields (Administrative, Administrative_Duration, Informational, Informational_Duration, ProductRelated, ProductRelated_Duration).
- For those activity fields only, add `1[x>0]` where **at least 50%** of the fold's **fitting** values are zero. Recalculate eligibility inside every CV fitting fold.
- Retain numeric BounceRates, ExitRates, SpecialDay and Weekend; encode six nominal fields with `k-1` indicators.
- **Within-fold `StandardScaler` on the encoded design**, then fixed **L2-penalised Logit (`C=1.0`)**. No after-the-fact `C` grid search. The intercept is not penalised.
- **Why:** long activity tails and substantial zero masses; strong related predictors; rare or pure-category outcomes may destabilise unpenalised coefficients. L2 shrinks coefficient estimates to trade some bias for potentially better stability.
- **What cannot be claimed:** a revised-versus-baseline AUC gap isolates L2's contribution. The revision also changes feature representation and scaling. L2 does not automatically improve ranking.

### 7.2 Revised LDA

- Keep all 16 original sources, with `log1p` on the same six activity columns; `k-1` nominal encoding.
- Use LDA with **`solver='lsqr', shrinkage='auto'`**; estimate covariance and any learned transformation **within each training CV fold**.
- **Why:** strong within-class dependence and mixed engineered features may destabilise the shared covariance estimate; shrinkage may reduce estimation variance.
- **Limitations:** correlation alone does **not** violate LDA. Shrinkage does not establish class normality or identical population covariances and might lower AUC. This is a documented course-adjacent computational extension, not a claim that all shrinkage theory was covered in class.

### 7.3 Revised Mixed Naive Bayes

- Keep all 16 source variables, represented using an **eight-input Gaussian block** (six `log1p` activity variables plus BounceRates and ExitRates) and an **eight-input discrete/categorical block** (six nominal variables, Weekend and `1[SpecialDay>0]`).
- Use the empirical class prior **once**; fit discrete category maps inside each fold with deterministic unseen-category support; apply **Laplace smoothing `alpha=1`** to discrete likelihoods.
- **Why:** a single all-Gaussian model is unnatural for nominal fields; an all-Bernoulli model discards intensity. A mixed likelihood represents these types more naturally.
- **Limitations:** within-class independence still may fail; smoothing is not an L1/L2 penalty; probabilities need not be calibrated.

### 7.4 Revision accountability

- The exact latest revision recipes and motivations are recorded in [regularisation_revision_log.md](regularisation_revision_log.md).
- Revisions are **pre-specified hypotheses**, not guaranteed improvements or automated AUC-driven searches.
- Preserve and explain unchanged, negative or very small gains. Do not attribute a whole-recipe gain to one transformation/penalty.
- This project includes the standard three taught model families; Mixed NB and covariance shrinkage must be clearly labelled as motivated extensions, not misrepresented as separate taught classifier families.

## 8. Evaluation metrics and model selection

**Primary:** highest **mean five-fold stratified training CV ROC-AUC** among the seven fixed candidates.

**Secondary:** mean **average precision (AP)**, **precision–recall curve**, sample fold AUC standard deviation, fold SE `SD/sqrt(5)` and relevant OOF ROC curves. These should be **reported and interpreted**, not used post-hoc to change the winner unless the selection rule is formally changed before looking at results.

- ROC-AUC measures ability to rank a random buyer above a random non-buyer. **AUC does not measure accuracy, precision, threshold performance or calibration.**
- AP is important because only ~15.5% of sessions are buyers. Its approximate no-skill baseline is the positive-class prevalence; **AP is not precision at a chosen threshold**.
- Common folds isolate model differences from differing validation observations.
- Average per-fold ROC-AUC, not pooled OOF ROC-AUC, is the fixed winner-selection statistic. Pooled OOF ROC curves remain useful illustrations but need not give numerically identical AUCs.
- Display **one** seven-model comparison table and **one** ROC overlay. Display the winner's **one** PR curve with AP and appropriate prevalence benchmark.
- Select by highest mean AUC; document very small differences, the one-SE proximity as *descriptive context*, and avoid informal significance or superiority claims.
- Do not compare models using classification threshold, price, voucher coverage, simulated revenue or profit.

**Validated, historical training-CV comparison from 26 October 2026** (these results guide accurate reporting, not a new model-selection exercise):

| Candidate | Mean 5-fold ROC-AUC |
|---|---:|
| Baseline unpenalised Logit | 0.750020 |
| Baseline Gaussian NB | 0.692021 |
| Baseline Bernoulli NB | 0.723133 |
| Baseline LDA | 0.740879 |
| **Revised L2 Logit** | **0.758074** |
| Revised covariance-shrinkage LDA | 0.741698 |
| Revised Mixed NB | 0.731474 |

The revised L2 Logit is the **observed training-CV winner** (fold AUC SD ~0.012727; SE ~0.005692; mean AP ~0.335193). Its AUC is about **0.008054** above operational Logit. That is a **whole-recipe difference**, not proof of an independent effect of regularisation or of an unseen-test improvement. These figures must be verified when the final notebook is executed; do not substitute historical unregularised test scores for this revised model.

## 9. Threshold sensitivity and prediction interpretation

**Positive class:** `Revenue=1`, an observed purchase.

**Prediction rule:** `predicted purchase = 1` when `p_hat >= t`; otherwise `0`. **There is no associated voucher or business action in v2.0.**

The threshold analysis must use **OOF probabilities from the selected model on training rows**. Show:

1. **One OOF probability histogram** by observed class, explaining score overlap or concentration and why rank-based AUC does not imply well-calibrated probabilities.
2. **One sensitivity–specificity-versus-threshold curve** on training OOF predictions, marking the crossover at which `|sensitivity-specificity|` is minimised on the empirical candidate cutoffs. Handle finite endpoints, exact ties and undefined rates deterministically.
3. **One table with exactly three reference thresholds:**

| Reference | Definition | Role |
|---|---|---|
| Training purchase prevalence | Exact `mean(y_train)` (~0.155) | Class-imbalance reference |
| Conventional cutoff | `0.500` | Standard comparator |
| **Sensitivity–specificity crossover** | OOF cutoff where the rates are nearest | **Selected balanced operating reference** |

For each row, show only **threshold, sensitivity, specificity and precision** in the main comparison table. A compact confusion matrix for the crossover may be provided **once** where necessary to interpret the selected classifier's errors, without duplicating the entire table.

**Interpretation requirements**

- Sensitivity = `TP/(TP+FN)`; specificity = `TN/(TN+FP)`; precision = `TP/(TP+FP)`.
- Raising the purchase cutoff generally decreases sensitivity and increases specificity; precision does not necessarily increase monotonically at every empirical cutoff.
- Crossover is **balanced**, not universally optimal, cost optimal, maximally precise or validated as best for an unspecified use case.
- The winner was chosen by threshold-free ROC-AUC; the operating threshold is a **separate training-stage descriptive choice**.
- Do **not** select thresholds based on any held-out test scores or post-hoc business arithmetic.
- Remove the `2/3` threshold line, voucher counts/shares, discount policy, FN/FP monetary loss labels, the conversion-`q` scenarios and revenue figures/plots.

## 10. Reliability and statistical limitations

Every claim must distinguish what the observed data support from what they do not.

- **Prediction versus inference:** report predictive discrimination, not causal determinants or claims that every included coefficient is statistically significant.
- **Imbalance:** accuracy is misleading when non-buyers predominate; interpret AP and PR evidence alongside ROC-AUC and confusion rates.
- **Calibration:** ROC-AUC/AP concern ranking, **not** accurate numeric probability calibration; discuss limitations and available elementary score diagnostics, **without introducing a formal calibration programme** unless separately authorised.
- **Data assumptions:** skewed/zero-heavy fields, dependence, non-Gaussian dummies, NB conditional independence and LDA Gaussian/shared-covariance assumptions remain relevant even if performance is acceptable.
- **Numerical stability:** do not hide warnings. Audit convergence, separation/pure categories, rank/conditioning, coefficient stability where relevant, finite parameters and probabilities. Record warnings and attempted remedies in audit evidence; do not silently delete predictors or change estimators to make a fit appear successful.
- **Duplicates:** repeated identical fields are not proof of the same person, but they can affect fitting, prevalence, folds and measured validation performance. Keep the agreed full dataset.
- **PageValues/prediction time:** association with Revenue does not prove leakage. Exclusion is precautionary due to timing uncertainty, and **other session-end variables are not certified available early in a live session**.
- **Model-selection optimism:** EDA-informed recipe development and winner selection on training CV may make the selected CV score optimistic.
- **Independent performance boundary:** the latest seven-model regularised winner has **no reported independent test estimate**. Assess it using training cross-validation, disclose that independent testing has not been reported, and never attribute metrics from a different fitted recipe to the new L2 model.
- **External validity:** no identifier proves unique users, and neither changing session behaviour nor deployment generalisation has been established.
- **No intervention claims:** no voucher response, causal effect, real conversion lift, prices, profit or optimal discount/decision claim remains in this prediction-only project.

## 11. Refit, reproducibility and review workflow

1. Preserve the original CSV, historical notebooks, original PRD v1.0, project decisions and version history. Do not erase contrary historical results.
2. Re-run all source/type/duplicate checks, the fixed split and folds, and training-only EDA with recorded row IDs, source hash, random state, library versions and deterministic categorical handling.
3. Use exactly the approved seven candidate recipes and identical training folds. Learn all fitted preprocessing inside folds; obtain one OOF probability for every training observation and candidate.
4. Verify fold metrics against saved predictions. Audit any actual numerical warnings; do not silently suppress them. Keep internal traces concise in the submitted notebook.
5. Freeze the chosen CV winner and threshold rule from training OOF. Show the **one** seven-row table, ROC overlay, PR curve, winner score distribution, sensitivity–specificity curve and three-reference table in a coherent narrative.
6. Refit the exact selected specification on the **9,864 training records** for a numerical stability check. **Do not report a new independent test estimate** or imply that a training fit provides one.
7. Retain the professor's **final full-data refit** principle: once the analysis and its evaluation boundary are frozen, fit the **unchanged selected recipe** on all 12,330 sessions, without further feature/hyperparameter selection and **without reporting the all-data training score as validated performance**.
8. Preserve machine-readable outputs and a revision log linking each displayed result to the specific code/recipe. Reconcile README, technical plan and supporting docs so obsolete economics are not labelled as current.
9. Verify the notebook top-to-bottom in a clean environment. Independently recompute key AUC/AP, confusion and threshold rates from saved OOF predictions, inspect labels and visual readability, and record checks **actually completed**.
10. **Git protocol:** preserve Git history. The PRD is versioned rather than overwriting v1.0 prematurely; implementation requires its own review. Do not silently merge old and new evidence or relabel historical scores.

## 12. Acceptance criteria

- [ ] **Scope:** prediction is the only objective; no voucher, pricing, fixed 0.667, q scenarios or revenue/profit analysis in the active deliverable.
- [ ] **Research question:** single session-level `Revenue` classification question, three model families, clear interpretation of what prediction can and cannot show.
- [ ] **Data discipline:** 12,330 rows and duplicates retained, checked before stratified 80/20 split; seed 42; EDA/model selection restricted to 9,864 training rows; 5 common stratified training folds.
- [ ] **Feature integrity:** four all-17 diagnostics and clear `PageValues` timing caveat; four minimally treated 16-source baselines; fold-contained encoding and learned preprocessing.
- [ ] **Seven candidates:** current four baselines and three documented EDA-informed revisions, including fixed L2 `C=1`, automatic shrinkage LDA and properly implemented Mixed NB. No extra model or hyperparameter sweep.
- [ ] **Fair evaluation:** exact shared folds, mean fold ROC-AUC selection, AUC SD/SE, AP, one seven-model ROC overlay and one PR curve. Correct winner and no conflation of AUC with precision/calibration.
- [ ] **Threshold:** only prevalence, 0.50 and sensitivity–specificity crossover; use training OOF; table contains sensitivity, specificity and precision, with crossover reference and its limitation explained.
- [ ] **Visual discipline:** one useful instance of each required plot/table. No duplication and no large warning/failure/boilerplate tables.
- [ ] **Interpretation:** purpose → evidence → interpretation → implication for every substantive analysis; actual directions/magnitudes reported and no unsupported significance/causality claims.
- [ ] **Numerical checks:** actual convergence/warnings, fold prediction integrity, classification-rate identities and reproducibility inspected and documented.
- [ ] **Evidence boundary:** report training CV as the predictive assessment; no new-model independent test claim; do not attribute different-recipe evaluation metrics to the regularised winner.
- [ ] **Final fit:** selected exact model refitted on training for numerical audit and all 12,330 rows for final recipe, without new validation claims.
- [ ] **Preservation/traceability:** original v1.0, historical sources, data and Git history intact; all current repository documentation aligned after implementation.
- [x] **PRD approval:** v2.0 explicitly accepted by owner on 27 October 2026.
- [ ] **Remaining gates:** revised technical plan approved, notebook implementation completed and independently verified.

## 13. Decision ledger — major and minor recovered choices

| ID | Decision | Status |
|---|---|---|
| D01 | Prediction, not inference or causality | **Approved 26 Oct** |
| D02 | Drop entire voucher/revenue/discount business case | **Approved 26 Oct** |
| D03 | Remove fixed cost-derived 0.667 and all q/discount calculations | **Approved 26 Oct** |
| D04 | Retain threshold sensitivity as supporting predictive interpretation | **Approved 26 Oct** |
| D05 | Three references: prevalence, 0.500, sensitivity–specificity crossover | **Approved 26 Oct** |
| D06 | Three-reference table: sensitivity, specificity, precision | **Approved 26 Oct** |
| D07 | AUC-led seven-model CV; AP and PR evaluation for imbalance | **Approved/carry-forward** |
| D08 | Each main-notebook curve/table appears once only | **Approved 26 Oct** |
| D09 | EDA directly motivates revised-model feature choices | **Approved/carry-forward** |
| D10 | Preserve analysis purpose and concise interpretation in each section | **Approved/carry-forward** |
| D11 | Do not mask numerical warnings; diagnose and disclose | **Approved/carry-forward** |
| D12 | Retain probability-calibration caution without formal calibration modelling | **Approved/carry-forward** |
| D13 | Preserve 80/20 split, 5 common training folds, seed 42 | **Approved v1 carry-forward** |
| D14 | Retain all 12,330 observations including 125 excess duplicates | **Approved v1 carry-forward** |
| D15 | Four all-17 diagnostics then 16-source operational candidates, excluding PageValues cautiously | **Approved v1 carry-forward** |
| D16 | Four raw baselines and one motivated revision in each family | **Approved v1 carry-forward** |
| D17 | Latest tested L2 Logit, shrinkage LDA and Mixed NB recipes are the current seven-model revision | **Current implemented recipe; retain** |
| D18 | Common-fold primary ROC-AUC, report fold SD/SE and AP; no post-hoc winner swap | **Approved v1 carry-forward** |
| D19 | Keep supplementary EDA separate, training-only and not submitted | **Approved v1 carry-forward** |
| D20 | Use concise bullets/headings; omit redundant plots and warning/failure tables | **Approved/presentation preference** |
| D21 | Full-data refit remains in workflow; do not use in-sample training score as performance | **Reconfirmed and approved 27 Oct** |
| D22 | Report training CV without a new independent test claim or a development-history narrative | **Approved with reporting clarification 27 Oct** |
| D23 | No deployment, unique-customer, timing-leakage certainty or commercial-uplift claims | **Inherited statistical safeguard** |
| D24 | Update limitations, acceptance criteria, and implementation boundary to reflect the new scope | **Approved with reporting clarification 27 Oct** |

### Approval and remaining implementation boundary

**Approval:** the 26 October Changes 1–6, the 27 October approval of Changes 7–9 and the final-model refit, the carried-forward PRD v1.0 safeguards and the validated seven-model specifications together establish the approved PRD v2.0. No current model code has been modified by this documentation approval.

**Resolved on 27 October:** Sections 10–12 were approved with the reporting qualification that the submitted notebook should state the CV-only performance scope accurately but need not narrate development history. The final all-data refit was approved, with no independent test-performance claim or use of a full-data training score as validation.

**No PRD-level methodological decisions remain open.** Next steps are technical-plan approval, notebook implementation, full execution and independent validation. The technical plan may not reinstate business-economics outputs or change the candidate/evaluation protocol without a newly documented owner decision.
