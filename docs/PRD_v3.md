# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.0

**Date:** 31 October 2026  
**Status:** Owner-approved requirements, recorded for implementation; **not yet implemented or validated**.  
**Supersedes:** [PRD v2.0](PRD_v2.md), which remains preserved for history. [PRD v1.0](PRD.md) and earlier model comparisons are historical.  
**Current implementation boundary:** The existing [main notebook](../online_shoppers_revised.ipynb), [technical plan](technical_plan.md), [repository instructions](../AGENTS.md) and README describe v2 implementation until explicitly updated for v3. This document does not claim that notebook code or results have changed.

---

## 1. Research question, objective and deliverables

**Research question:** How effectively can online browsing-session characteristics predict whether a session ends in a purchase (**Revenue = 1**), and which defensible specification of the taught classifiers provides the strongest predictive discrimination?

- **Primary goal:** Prediction, not coefficient inference, causal inference or treatment-effect estimation.
- **Classifiers:** Four independently developed modelling pathways: Logistic Regression, Linear Discriminant Analysis (LDA), Gaussian Naive Bayes (GNB) and Bernoulli Naive Bayes (BNB). These are four pathways across three course families; GNB and BNB are distinct Naive Bayes variants, not four unrelated theoretical families.
- **Development:** Start each pathway with all operational predictors and build a short, EDA-motivated sequence of **3–5 attempted specifications including the baseline**, changing one element at a time. Keep or reject each change using training cross-validation (CV) and the agreed one-standard-error principle. Report **every** attempted specification, not just retained ones.
- **Model selection:** Compare the four retained pathway finalists on **mean five-fold training ROC-AUC**; supporting average precision (AP), ROC/PR plots and fold variability contextualise the result.
- **Secondary applied analysis:** Interpret purchase-probability thresholds using a **hypothetical live-agent upselling** decision. An economically motivated classification cutoff is a coursework decision illustration, **not** evidence of actual incremental sales or deployable policy effectiveness.
- **Outputs:** A concise, executable, submission-ready Jupyter notebook; separate training-only supplementary EDA; machine-readable evidence and audit log; and **slides for a 20-minute presentation**. Slides—not a live notebook walkthrough—are the principal presentation medium.

**Outside scope:** Vouchers and discount optimisation; separate revenue simulation; causal uplift modelling; inference-focused coefficient claims; exhaustive feature-selection or transformation searches; other untaught classification families (including QDA or KNN) unless separately approved.

### Authority and approval gates

Verified assignment/professor instructions take precedence. This PRD is the agreed project scope. A v3-aligned technical plan and subsequent notebook changes require their own review and verification; approval of requirements does not mean completed implementation or independent testing.

Professor's 29 October guidance governs the revision logic: **EDA proposes a change; training CV decides whether to retain it; three to five specifications per classifier; one modification at a time; regularisation selected within CV; all tried specifications reported; final test used once after selection.** The professor permits explicitly stated, reasonable business cost assumptions and identifies AP/PR analysis as useful at approximately 15.5% prevalence.

## 2. Data, feature availability and validation protocol

| Element | Requirement |
|---|---|
| Data | UCI Online Shoppers Purchasing Intention; **12,330 browsing sessions**, **17** source predictors and binary **Revenue** |
| Unit | Session, not an identifiable unique customer |
| Duplicates | Retain all rows including **125 excess exact duplicate full rows**; document potential validation dependence; duplicates do not prove duplicate people |
| Quality | Check types, missing/blank values, nonfinite numeric values, outcome distribution and duplicates **before** splitting |
| Imbalance | Approximately **15.5% buyers**; report exact observed training prevalence and explain why accuracy alone misleads |
| Partition | Existing stratified **80/20** split, **random_state = 42**; training **9,864**, reserved **2,466** |
| CV | **Five shuffled stratified** folds on the training partition, **random_state = 42**; reuse identical outer fold membership throughout |
| EDA and selection | Training rows only; no holdout-assisted feature decisions, hyperparameter tuning, model selection or threshold selection |
| Preprocessing | All learned encoders, scalers, rare-level group maps, fold-derived medians, transformations and model parameters fit **within the relevant fitting fold** |
| Operating features | Keep the same **16 original source predictors excluding PageValues**; retained derived features count as engineered representations, not new source fields |
| Categorical variables | Treat Month, OperatingSystems, Browser, Region, TrafficType and VisitorType as nominal, never as artificially ordinal integers |

**Predictor timing:** PageValues has a very strong observed association with Revenue but is excluded because whether it would be available at an actionable decision time is unclear. Association alone is **not** proof of leakage. Other session-aggregate variables also lack documented real-time availability; no live-deployment feasibility claim is warranted.

**All-17 diagnostic comparison:** Preserve the v2 idea of fitting the four minimally treated classifiers on all **17** original source predictors as an **EDA/feature-timing diagnostic**, then start operational development with the four corresponding **16-source baselines**. The all-17 diagnostics do not compete in the operational model-selection stage.

**Holdout integrity qualification:** Earlier repository versions have already used the reserved 20% observations. For v3, keep them completely outside **this version's** modelling and threshold decisions and perform at most one final post-selection holdout evaluation. Describe it accurately as a version-specific held-out check, **not a newly pristine independent test across the entire project's development history**. Do not reuse historical holdout results to choose v3 changes. Disclose the limitation briefly without turning the notebook into a development-history narrative.

## 3. Training-only EDA: findings and testable hypotheses

Retain the separate [supplementary EDA notebook](../supplementary/training_eda.ipynb). Bring only decision-relevant evidence into the submitted notebook. The established training-only observations are **descriptive**, not proof of predictive improvement:

| Finding | Observed training evidence | Modelling hypothesis |
|---|---|---|
| Long-tailed activity magnitudes | Skew of ProductRelated_Duration **8.01**; Informational_Duration **7.70**; ProductRelated **4.37** | Test log(1+x) to reduce tail influence, particularly for LDA and GNB |
| Zero-heavy informational activity | Informational **78.5%** zero; Informational_Duration **80.5%** zero | Test separating presence (x>0) from positive intensity for Logit |
| Conditional predictor dependence | BounceRates/ExitRates correlation among nonbuyers **0.915**, buyers **0.723** | Test reducing duplicated NB evidence; consider shrinkage for LDA covariance estimation |
| Product count/duration dependence | Within-class correlations **0.839** and **0.896** | Test GNB feature removal; do not call either predictor irrelevant a priori |
| Sparse nominal levels | **9** TrafficType levels and **4** Browser levels have fewer than 50 training rows | Test fold-fitted rare-level grouping in Logit/LDA; do not assume pooling is necessarily better |
| SpecialDay | **89.7%** zero; buyer rates **16.6%** at zero versus **5.9%** for positive values; positive-level rates non-monotone | Test a presence representation for LDA or dropping the misspecified Gaussian marginal in GNB |
| Intensity lost in BNB | Only **0.27%** of ProductRelated values and **0.62%** of ExitRates values are zero | Test binarisation at a fold-fitted median instead of default x>0 |
| VisitorType x Month | Some striking descriptive rates but sparse cross-cells | **No automatic interaction**: existing EDA is insufficient to justify a candidate interaction |

The 30% upsell assumption in Section 7 is **not an EDA finding**. It is a separate illustrative business premise.

## 4. Four baseline contracts

All operational baselines use the same 16 original sources. Each has only the representation required for that estimator.

| Input group | Logistic (L0) | LDA (D0) | Gaussian NB (G0) | Bernoulli NB (B0) |
|---|---|---|---|---|
| Activity counts, durations, rates | Raw continuous | Raw continuous | Raw Gaussian marginals | x>0 indicators |
| SpecialDay | Numeric | Numeric | Numeric Gaussian marginal | 1[SpecialDay>0] |
| Six nominal sources | k−1 one-hot dummies | k−1 one-hot dummies | full categorical one-hot indicators | full categorical one-hot indicators |
| Weekend | 0/1 | 0/1 | 0/1 | 0/1 |
| Estimator | Unpenalised Logit | Standard shared-covariance LDA | Standard GNB | Standard BNB |

Nominal one-hot representation is a modelling compromise for GNB; nominal category indicators and many zero values challenge its Gaussian marginal assumption. With BNB, full one-hot indicators for each category are mutually constrained and therefore not conditionally independent; document that limitation. Encode unknown levels deterministically inside the fitting pipeline.

Baseline results are reference points, not a claim that any estimator has validated normality, independence or equal covariance.

## 5. Pre-specified EDA-informed sequential paths

**Rule:** Each path attempts its baseline and up to **four** sequential, singly motivated modifications, in the specified order. Compare each challenger to the **currently retained specification**; if rejected, revert to the incumbent before evaluating the next listed change. Thus a nominal step does **not** imply that earlier rejected modifications were retained. Record the actual composed recipe, results and rejection reason for every attempt. Do not test combinations or adjust the order based on observed winner hunting.

### 5.1 Logistic Regression — up to five specifications

| Step | Candidate change relative to current retained specification | EDA reason |
|---|---|---|
| **L0** | All-16 minimally treated unpenalised baseline | Reference |
| **L1** | Replace the six activity count/duration magnitudes with log(1+x) | Long tails and non-linear-looking marginal empirical logits |
| **L2** | Add separate positive-presence indicators for Informational and Informational_Duration; keep their current magnitude representation | Both ~79–80% zeros; distinct zero/positive buyer rates |
| **L3** | Pool rare levels of Browser and TrafficType using a predeclared frequency rule, fitted on the fitting fold | Small categorical groups and potential coefficient instability |
| **L4** | Introduce **L2** coefficient penalty; standardise the fitted design within the pipeline and select inverse penalty strength **C** using **inner CV** | Correlated predictors and sparse indicators may cause instability/overfitting |

Neither Logit nor its features need to be normally distributed. Log transforms here test functional form rather than a Logit normality requirement. Standardisation paired with L2 is an estimator/tuning configuration, not an extra feature search. Define a compact C grid before scoring; no post-hoc expansion.

### 5.2 Linear Discriminant Analysis — up to five specifications

| Step | Candidate change relative to current retained specification | EDA reason |
|---|---|---|
| **D0** | All-16 standard LDA baseline | Reference |
| **D1** | Apply log(1+x) to the six activity count/duration variables | Extremely skewed marginals challenge class-Gaussian approximation |
| **D2** | Replace numeric SpecialDay with 1[SpecialDay>0] | Mostly zero and no clear monotone pattern among positive levels |
| **D3** | Pool rare Browser and TrafficType levels inside folds | Sparse dummies may worsen covariance estimation |
| **D4** | Introduce covariance shrinkage with strength selected by **inner CV** within the outer-fit pipeline | Potential covariance estimation instability from many encoded, related variables |

LDA **allows** correlation between predictors; high correlation alone is not evidence that LDA assumptions fail. Shrinkage does not establish multivariate Gaussianity or equality of class covariance matrices. Automatic shrinkage can be considered within a predeclared tuning strategy, not retroactively switched based on test outcomes.

### 5.3 Gaussian Naive Bayes — up to five specifications

| Step | Candidate change relative to current retained specification | EDA reason |
|---|---|---|
| **G0** | All-16 standard GNB baseline | Reference |
| **G1** | Apply log(1+x) to the six activity variables | Heavily right-skewed positive magnitudes |
| **G2** | Remove BounceRates, retain ExitRates | Extremely strong conditional correlation may double-count similar evidence |
| **G3** | Remove ProductRelated, retain ProductRelated_Duration | Another strongly dependent source pair |
| **G4** | Remove SpecialDay's Gaussian input | Heavily zero-concentrated, discrete input poorly matched to a Gaussian marginal |

Each deletion is a **test**, not proof of no contribution. GNB's conditional independence assumption still requires discussion even after deletions, especially across categorical indicator columns. No Mixed NB is included in v3.

### 5.4 Bernoulli Naive Bayes — up to five specifications

| Step | Candidate change relative to current retained specification | EDA reason |
|---|---|---|
| **B0** | All-16 BNB baseline with default positive-presence conversion for numeric magnitudes | Reference |
| **B1** | For ProductRelated, change binary representation from x>0 to x above the fitting-fold median | Nearly all values exceed zero; presence alone loses intensity |
| **B2** | For ProductRelated_Duration, use the fitting-fold median as binary cutoff | Substantial positive duration variation is discarded by x>0 |
| **B3** | For ExitRates, use the fitting-fold median as binary cutoff | Almost all sessions have a positive ExitRates value |
| **B4** | Remove BounceRates | Strong conditional dependence with ExitRates challenges NB independence |

Median thresholds are selected **from the fitting fold without outcome-guided scanning**; validation/test medians must never be used. These are input-binarisation hypotheses, **not classification probability thresholds**. BNB is useful for checking whether binary activity levels outperform mere activity presence; it necessarily loses within-group magnitude information.

### 5.5 Guardrails for all paths

- Every attempted specification retains the full trial trail: parent/retained model, one changed element, EDA rationale, fold scores, mean ROC-AUC, AUC SD/SE, mean AP, acceptance outcome and any warnings.
- Up to **20 operational CV attempts total** across four paths (including four baselines); fewer are acceptable when a path ends early or a step is inapplicable. No 4×4 cross-product of modifications.
- A family may finish at its original baseline. A change accepted in one family is **not** automatically copied to another.
- Learned rare-level pooling, binarisation medians and preprocessing are implemented as reusable, fold-safe pipeline steps; never fit them on the complete training set before CV.
- Neither input-variable transformations nor model hyperparameters are chosen using the final test set.
- Keep model-family specific limitations explicit; do not manufacture a four-family consensus for neatness.

## 6. CV acceptance, selection and model-comparison accounting

### 6.1 Common CV score

- **Primary:** Mean **five-fold training ROC-AUC** (higher is better).
- **Supporting:** Mean fold AP, positive-class prevalence, ROC/PR curves, sample SD across five AUC values, and standard error **SE = SD/sqrt(5)**, where SD uses **ddof=1**.
- Mean fold AUC is the selection statistic; pooled out-of-fold (OOF) AUC may differ and is for visual illustration, **not** substituted into ranking.
- AUC measures ranking, not calibration, accurate probabilities or operating-point value. AP provides minority-class ranking context at ~15.5% prevalence.

### 6.2 One-SE adaptation for sequential revision decisions

The course presents the **one-standard-error rule** as choosing the simpler specification when its CV performance is within one SE of the best. Apply that principle **locally to each incumbent-versus-challenger comparison**:

1. Run both on the same five outer folds; calculate fold AUC means and sample SD/SE.
2. If the challenger has a higher mean AUC, treat it as the higher-scoring candidate; **retain the simpler incumbent if its mean is within one SE of the challenger's mean**.
3. Retain the challenger only when it improves mean AUC by **more than that one-SE tolerance**; otherwise reject/revert.
4. If the challenger has no AUC gain, reject it. Report fold-level variability and avoid interpreting this heuristic as a formal significance test.

This is an **operational adaptation** of the lecture's 1-SE model-simplicity principle to the professor's sequential revision process, not a new hypothesis test. The professor's phrase “fold-to-fold spread” did not specify whether to use SD or SE; this PRD fixes **one SE** per the project's course-based decision.

### 6.3 Hyperparameters and outer validation

For Logit L4 and LDA D4, predeclare a small, sensible hyperparameter grid and use **inner stratified CV (e.g. three folds)** inside each outer training fold. Scaling/encoding and hyperparameter selection belong within that inner fit pipeline; the outer validation fold must not select C or shrinkage. On final refit, retune the hyperparameter using training data only with the same predeclared inner-CV method.

Do not reuse an outer-fold validation observation inside its inner model-selection process. Distinguish the effects of feature changes from those of adding/tuning regularisation; only one numbered revision is assessed at each step.

### 6.4 Finalist selection and optimism

After sequential development, select **one retained finalist per pathway** (four total). Choose the overall model by **highest mean outer-CV ROC-AUC**. Show AP and SE to contextualise close scores, but do not silently replace the primary rule with AP, accuracy, the financial threshold or a post-hoc preference. Small AUC differences do not imply statistical superiority.

Selecting from multiple attempted specifications makes the winning CV estimate potentially optimistic. A one-time reserved-set evaluation is intended as a check, subject to Section 2's historical-use caveat. No revision after inspecting test results without a fresh, properly separated evaluation design.

## 7. Cost-sensitive classification: hypothetical upselling scenario

**Decision story:** The retailer may send a live sales agent to a session predicted **likely to purchase**, to offer an additional product or order upgrade. Customers predicted not to purchase are **not** contacted under this illustration.

**Assumptions, not UCI measurements:**

| Parameter | Hypothetical value | Definition |
|---|---:|---|
| Agent cost per assisted session, s | **S$3** | 10 minutes of labour at S$18/hour, incurred **whenever contacted** |
| Probability of a successful upsell conditional on a buyer, q | **30%** | Assumed success rate among customers who would make the original purchase |
| Additional gross margin per successful upsell, g | **S$50** | Incremental margin from the **upsell**, not from the original order |
| Predicted probability p | Model estimate of **P(Revenue=1 | browsing inputs)** | The model does **not** predict q or upsell response |

**Payoff logic relative to not providing support:**

| True outcome | Send agent (model predicts Buy) | Do not send agent (model predicts No Buy) |
|---|---|---|
| Actual buyer (Revenue=1) | Expected incremental value **qg − s = S$12** | **S$0** |
| Actual nonbuyer (Revenue=0) | **−S$3** agent cost; assume no upsell | **S$0** |

The corresponding **relative misclassification-loss** convention is **C_FP = S$3** (unnecessary assistance) and **C_FN = S$12** (foregone **net** expected upsell benefit), with zero loss assigned to correct classifications. The TP case incurs S$3 labour cost too; it is already netted against the S$15 expected gross upsell contribution. **Do not label C_FN = S$15**, because that would omit the cost of assisting true buyers.

**Decision threshold, using the course formula:**

\[
t^*=\frac{C_{FP}}{C_{FP}+C_{FN}}
=\frac{3}{3+12}
=\boxed{0.20}.
\]

Equivalently, contact when the expected incremental contribution of assisting a session is positive:

\[
E[\text{incremental contribution}\mid p]
=p(qg)-s=15p-3>0
\quad\Longleftrightarrow\quad p>0.20.
\]

The operational interpretation uses **purchase probability**, not a probability of receiving benefit from support. At equality the retailer is economically indifferent under the illustration; for reproducible binary classification use **predicted Buy if estimated p ≥ 0.20**.

**Sensitivity, without a revenue simulation:** Keep s=S$3 and g=S$50, vary **hypothetical q = 20%, 30%, 40%**, yielding respective theoretical thresholds **0.30, 0.20, 0.15**. Alternatively show the corresponding loss ratio alongside each threshold. These sensitivity values are **scenario inputs**, not observed or tuned using model outcomes. Do **not** choose q to force a threshold near prevalence or crossover.

**Limits:** The dataset has neither agent-assignment records nor observed upsell outcomes. Thus q, margin and behavioural response are not identified; observed Revenue does not demonstrate that contacting a customer causes an upsell. Theoretical 0.20 is decision-optimal only **under the assumed payoffs and sufficiently calibrated conditional purchase probabilities**. In particular, Naive Bayes posterior probabilities may be miscalibrated despite reasonable AUC. Do not call the threshold a validated revenue-maximising or deployable policy.

**Not included:** Voucher economics, estimates of actual intervention uplift, detailed financial forecasts, quota/capacity optimisation, or selecting the statistical model by simulated upsell profit.

## 8. Threshold reporting on training OOF predictions

Once the classifier is selected on CV, calculate thresholds using the selected model's **training OOF purchase probabilities**. Report **exactly four primary references**:

| Reference | Definition | Purpose |
|---|---|---|
| Training prevalence | Exact proportion Revenue=1 in training (~0.155) | Imbalance reference, **not inherently optimal** |
| Conventional | **0.500** | Standard classifier comparison |
| Sensitivity–specificity crossover | OOF cutoff where sensitivity and specificity are nearest | Balanced reference, **not cost-optimal** |
| **Cost-based (primary business illustration)** | **0.200**, fixed by Section 7 assumptions | Hypothetical upsell decision cutoff |

For each row display **threshold, TP, FP, TN, FN, sensitivity, specificity and precision**, or one compact confusion matrix for the primary cutoff plus a nonredundant comparison table. Optionally include expected loss under the stated relative loss matrix, explicitly labelled **hypothetical**; do not infer actual incremental revenue. Show one threshold-versus-sensitivity/specificity figure with clear markers for crossover and 0.20; include prevalence/0.5 markers only where readable.

The cost-based threshold is determined **by assumptions before consulting OOF classification results**, not chosen to optimise the same OOF confusion table. Compare the numerical proximity to prevalence or crossover **after** calculating all references, not as justification for the costs. OOF threshold metrics are descriptive training-stage estimates and do not validate calibrated probabilities.

## 9. Required notebook narrative and visuals

Every substantive notebook section follows **purpose → method/evidence → actual interpretation → implication**. Use short British English explanations and specific reported numbers rather than generic statistical definitions.

| Section | Evidence/output | Required interpretation |
|---|---|---|
| A1 — Data and split | Source shape, duplicates, missingness, prevalence; fixed split | Session-level unit, imbalance and data integrity |
| A2 — Numerical EDA | Focused skew/zero summaries; essential histograms | Long-tail/absence-versus-intensity hypotheses |
| A3 — Categorical EDA | Month, VisitorType rates; sparse levels | Predictive variation versus small-sample uncertainty |
| A4 — Assumptions | Selected conditional correlations and suitable distribution diagnostics | NB independence, LDA Gaussian/shared-covariance caveats, Logit functional-form motivation |
| A5 — All-17 diagnostics | Four baseline-family diagnostics and operational comparison | PageValues association/timing caution |
| A6 — Four operational baselines | One baseline CV table | Establish reference performance |
| A7 — Four sequential development paths | Compact **all-attempts** ledger with each changed element, AUC/AP/SE and keep/revert | Explain **why** EDA proposed each change and **what** CV showed; no unreported discarded trials |
| A8 — Finalists and selection | One four-finalist CV comparison with AUC/AP/SD/SE and one appropriate ROC comparison | Select one winner by mean CV AUC and disclose winner-selection optimism |
| A9 — Winner's scores | One winner OOF score distribution and **one** PR curve with AP and prevalence benchmark | Ranking, probability concentration and calibration limits |
| A10 — Thresholds | One sensitivity–specificity curve and one four-reference threshold table | Compare 0.20 against crossover/prevalence/0.5 and their FP/FN trade-offs |
| A11 — Cost sensitivity | Small q-sensitivity table/annotation (20%, 30%, 40%) | Consequences of hypothetical business premises; no causal sales claim |
| A12 — Finalisation | One held-out check per Section 2, fit audit and unchanged all-data refit | What was validated, what was not; no training score claimed as test performance |
| A13 — Conclusions | Explicit research answer, empirical results and scoped business interpretation | Limitations and implications without overclaiming |

**Visual discipline:** Each major plot or table should appear **once**. Prefer a concise attempts table over separate repetitive path charts. Keep extensive warnings, fold-by-fold detail and feature/pipeline diagnostics in machine-readable artifacts; show only material anomalies in the academic narrative. No orphan plots, redundant notebook sections or purely decorative figures.

### Slides: 20-minute presentation

Prepare a coherent slide deck organised around **question and business context → EDA evidence → four sequential modelling pathways → CV comparison and winner → four threshold references/upselling assumptions → limitations and conclusion**. Use slides for delivery; the notebook is reproducibility support. Allocate enough time to explain **why** changes were tried or rejected rather than displaying code or every intermediate diagnostic.

## 10. Statistical, operational and numerical limitations

- **Predictive, not causal:** Browsing variables and Revenue do not establish treatment effects, the natural no-agent purchase rate or who benefits from contact.
- **Potential probability miscalibration:** ROC-AUC and AP assess ordering, not expected-profit accuracy. The cost cutoff assumes approximate calibration; use simple OOF score/reliability inspection and qualify any failure. A separate elaborate calibration programme is **not** mandatory unless supported and approved.
- **Imbalance:** Accuracy can be high for a trivial no-purchase classifier. Interpret ROC-AUC, AP, recall, specificity and precision together.
- **Distribution/independence:** Right skew, zeros and nominal dummies challenge Gaussian marginals; within-class dependence especially challenges NB; LDA permits correlated predictors but assumes a shared class covariance and a Gaussian model; transformations do not prove these assumptions.
- **Rare categories:** Warn about unstable small-cell rates, quasi-separation and unseen validation levels. Never suppress fitting or convergence warnings without checking them.
- **Selection bias:** Many EDA-guided CV comparisons can make the selected mean AUC optimistic. One-SE is a **pragmatic complexity heuristic**, not formal proof of statistical superiority.
- **Duplicates and generalisation:** Retained duplicate rows may make CV/test membership partly dependent; source does not identify unique customers or support forecasts of future website conditions.
- **Session timing:** Existing measurements are not proven to be real-time available early enough to dispatch an agent; PageValues exclusion is precautionary rather than a guarantee.
- **Historical test use:** The v3 20% reserved observations were examined in earlier development; describe any reported v3 held-out score with the Section 2 qualification.
- **Business assumptions:** S$3 cost, 30% upsell success and S$50 margin are illustrative. No empirical profit uplift, deployment recommendation or “guaranteed purchase” claim is supported.

## 11. Reproducibility, audit and finalisation workflow

1. Preserve **data/uci_468.csv**, v1/v2 PRDs, archive, previous notebook evidence, Git history and existing historical artifacts.
2. Freeze v3 change order, fold definitions, acceptance rule, tuning grids and upselling parameters **before** new result inspection.
3. Execute reproducible training-only EDA, four all-17 diagnostics, four operational baselines and each pathway's bounded sequential trials; log kept and rejected results.
4. Independently recompute mean fold AUC/AP, SD/SE, selected-model identity, complete OOF coverage, threshold confusion counts and derived rates from saved fold/OOF outputs.
5. Confirm all transforms and hyperparameter searches fit **only** within the correct folds; guard against look-ahead or category-encoding leakage.
6. Freeze the selected finalist and training-stage cost threshold; refit on all **9,864 training rows** using the chosen pipeline. Inspect convergence, rank/variance issues, estimated probabilities, warnings, and reproducibility.
7. Evaluate the **frozen** model and threshold on the reserved **2,466 rows at most once in v3**. Report clearly that this check is not independent across earlier project versions. Do not revise the winner or threshold after test inspection.
8. Refit the **unchanged selected recipe** (including appropriate training-only hyperparameter procedure) on all **12,330 rows** for the final model; do **not** present full-data in-sample scores as external validation.
9. Save version-labelled CSV/JSON outputs: trial ledger and fold scores, finalists, OOF scores, thresholds, cost assumptions/sensitivity, test check, chosen pipeline parameters, warnings and provenance (source checksum, row IDs, package versions and random state).
10. Verify actual notebook outputs and figures top-to-bottom in a clean run. Only claim verification steps actually completed. Update active README, technical plan and AGENTS guidance **as part of the subsequent implementation**, so v2 code claims are not silently relabelled v3.

## 12. Acceptance criteria for v3 implementation

- [ ] **Correct objective:** prediction-focused research question; three taught families represented by four distinct pathways; no unsupported causal, inference or voucher claims.
- [ ] **Data discipline:** 12,330 sessions, original duplicates preserved, quality audit, stratified 80/20 split seed 42, five shared stratified training folds seed 42, no test-driven changes.
- [ ] **Features:** four all-17 diagnostics; 16-source operational baseline with PageValues excluded cautiously and nominal predictors appropriately encoded.
- [ ] **Revision accountability:** up to five attempts per pathway, one EDA-motivated change at a time, explicit keep/reject and **all** attempts displayed or traceably recorded; Mixed NB removed.
- [ ] **CV rule:** correct common-fold mean ROC-AUC, AP, fold SD/SE, local one-SE revision comparison, four final retained candidates, overall winner by highest mean ROC-AUC.
- [ ] **Nested tuning:** any logistic penalty C or LDA shrinkage strength tuned using only inner training CV inside the complete preprocessing/estimator pipeline.
- [ ] **Thresholds:** training OOF prevalence, 0.5, crossover and **fixed hypothetical 0.20**; interpretable FP/FN/sensitivity/specificity/precision; no threshold chosen using held-out data.
- [ ] **Economics:** exact S$3 / S$12 net misclassification costs derived from S$3 labour, 30% upsell success, S$50 incremental gross margin; show cost sensitivity, do not model or assert actual uplift.
- [ ] **Visuals/story:** one purposeful instance of each essential chart/table; concise purpose and numbers; no bloated warnings; 20-minute explanatory slide deck.
- [ ] **Test qualification:** single v3 reserved-set check **after freezing** models, fully disclose prior historical use, no claim of pristine independence or subsequent tuning.
- [ ] **Final refit:** model fitted on training for audit and unchanged specification finally fitted on all data; no in-sample performance inflation.
- [ ] **Verification:** complete run, result recomputation, fit/warning audit, source/figure/provenance checks and updated implementation documents.

## 13. Decision ledger and current boundary

| Decision | v3 resolution |
|---|---|
| Objective | **Prediction only**; cost threshold is a hypothetical interpretation, not a second causal objective |
| Classifiers | Independent **Logit, LDA, GNB, BNB** pathways; **Mixed NB removed** |
| Development | EDA proposes; **3–5** ordered specifications per path; CV determines retention; report all |
| Acceptance heuristic | **Course-based one-SE** simplicity principle applied locally to adjacent revision comparisons |
| Tuning | Regularisation selected through **inner CV**, including fitted preprocessing |
| Winner | Highest **mean five-fold training ROC-AUC** among four retained finalists; AP secondary |
| Partition | Retain existing **80/20, seed 42**, five common outer training folds |
| Operational sources | Original **16 without PageValues**; separate all-17 diagnostics |
| Business scenario | Live agent upsells to **predicted buyers**, not rescue of proven abandoned purchases |
| Business inputs | **S$3 per contact**, **30% conditional upsell success**, **S$50 incremental gross margin** |
| Correct net cost matrix | **FP = S$3**, **FN = S$12**, baseline TP/TN error loss zero |
| Cost decision cutoff | **0.20**, compare against prevalence, **0.5** and sensitivity–specificity crossover |
| Sensitivity | Vary hypothetical q **20% / 30% / 40%**; no empirical profit or causal uplift conclusions |
| Holdout | One v3 post-selection reserved-set check, **historical prior-use caveat mandatory** |
| Presentation | Slides for 20 minutes plus fully executable notebook |
| Remaining PRD-level questions | **None**; technical plan, notebook implementation, results and independent review remain future work |

**Version record:** PRD v3.0 consolidates decisions through 31 October 2026. It replaces v2 requirements without rewriting or falsifying v1/v2 history. The old seven-model notebook and historical metrics must not be represented as v3 results.