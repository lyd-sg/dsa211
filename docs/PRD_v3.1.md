# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.1

**Date:** 3 November 2026  
**Status:** Owner-approved v3.1 modelling requirements; **tree extension not yet implemented or validated**.  
**Supersedes:** [PRD v3.0](PRD_v3.md) as the requirements specification; preserve v3.0 and earlier PRDs unchanged for provenance.  
**Current implementation boundary:** The existing [executed v3.0 notebook](../online_shoppers_prd_v3.ipynb), [v3.0 technical plan](technical_plan_v3.md), [repository instructions](../AGENTS.md) and README describe the **v3.0 implementation**, not v3.1 results. Creating this requirements document does **not** constitute implementation, execution or validation of classification trees.

---

## 1. Research question, objective and deliverables

**Research question:** How effectively can online browsing-session characteristics predict whether a session ends in a purchase (**Revenue = 1**), and which defensible specification of the taught classifiers provides the strongest predictive discrimination?

- **Primary goal:** Prediction, not coefficient inference, causal inference or treatment-effect estimation.
- **Classifiers:** Five modelling pathways: Logistic Regression, Linear Discriminant Analysis (LDA), Gaussian Naive Bayes (GNB), Bernoulli Naive Bayes (BNB), and **Classification Trees**. The first four are separate development pathways across three previously used classifier families; the fifth comprises **Gini** and **Entropy** tree specifications. Both selected tree specifications enter the final comparison independently.
- **Development:** Retain the **3–5 attempted specifications including the baseline** requirement for each of the **four existing EDA-driven pathways**, changing one element at a time and reporting every attempt. **Classification Trees are exempt**: fit full-grown Gini and Entropy baselines, then use **cost-complexity pruning** and a five-fold CV ROC-AUC **one-standard-error (1-SE)** rule as their complete tuning procedure. Report full versus selected pruned performance and pruning-path evidence.
- **Model selection:** Compare **six specifications directly**: the four retained existing-pathway finalists and **both** independently selected Gini and Entropy trees, using **mean five-fold training ROC-AUC**. Do **not** preselect a single tree finalist. Supporting average precision (AP), ROC/PR plots and fold variability contextualise the result.
- **Secondary applied analysis:** Interpret purchase-probability thresholds using a **hypothetical live-agent upselling** decision. An economically motivated classification cutoff is a coursework decision illustration, **not** evidence of actual incremental sales or deployable policy effectiveness.
- **Outputs:** A concise, executable, submission-ready Jupyter notebook; separate training-only supplementary EDA; machine-readable evidence and audit log; and **slides for a 20-minute presentation**. Slides—not a live notebook walkthrough—are the principal presentation medium.

**Outside scope:** Vouchers and discount optimisation; separate revenue simulation; causal uplift modelling; inference-focused coefficient claims; exhaustive feature-selection or transformation searches; other untaught classification families (including QDA or KNN) unless separately approved.

### Authority and approval gates

Verified assignment/professor instructions take precedence. This PRD is the agreed project scope. A v3.1-aligned technical plan and subsequent notebook changes require their own review and verification; approval of requirements does not mean completed implementation or independent testing.

Professor's 29 October guidance governs the **four established EDA-driven revision paths**: **EDA proposes a change; training CV decides whether to retain it; three to five specifications per existing pathway; one modification at a time; regularisation selected within CV; all tried specifications reported; final test used once after selection.** The **tree extension follows Lesson 10's grow-and-prune method instead of artificial sequential feature revisions**. The professor permits explicitly stated, reasonable business cost assumptions and identifies AP/PR analysis as useful at approximately 15.5% prevalence.

## 2. Data, feature availability and validation protocol

| Element | Requirement |
|---|---|
| Data | UCI Online Shoppers Purchasing Intention; **12,330 browsing sessions**, **17** source predictors and binary **Revenue** |
| Unit | Session, not an identifiable unique customer |
| Duplicates | Retain all rows including **125 excess exact duplicate full rows**; document potential validation dependence; duplicates do not prove duplicate people |
| Quality | Check types, missing/blank values, nonfinite numeric values, outcome distribution and duplicates **before** splitting |
| Imbalance | Approximately **15.5% buyers**; report exact observed training prevalence and explain why accuracy alone misleads |
| Partition | Existing stratified **80/20** split, **random_state = 42**; training **9,864**, reserved **2,466** |
| CV | **Five shuffled stratified** folds on the training partition, **random_state = 42**; reuse identical fold membership throughout model comparison, including Gini and Entropy tree CV |
| EDA and selection | Training rows only; no holdout-assisted feature decisions, hyperparameter tuning, model selection or threshold selection |
| Preprocessing | All learned encoders, scalers, rare-level group maps, fold-derived medians, transformations and model parameters fit **within the relevant fitting fold** |
| Operating features | Keep the same **16 original source predictors excluding PageValues** across all five pathways; tree splitting selects features automatically; retained derived features in existing paths count as engineered representations, not new source fields |
| Categorical variables | Treat Month, OperatingSystems, Browser, Region, TrafficType and VisitorType as nominal, never as artificially ordinal integers; encode nominal features consistently for scikit-learn trees within fitting folds |

**Predictor timing:** PageValues has a very strong observed association with Revenue but is excluded because whether it would be available at an actionable decision time is unclear. Association alone is **not** proof of leakage. Other session-aggregate variables also lack documented real-time availability; no live-deployment feasibility claim is warranted.

**All-17 diagnostic comparison:** Preserve the v2 idea of fitting the **four existing classifiers** on all **17** original source predictors as an **EDA/feature-timing diagnostic**, then start operational development with the four corresponding **16-source baselines**. The new Gini and Entropy operational tree baselines use **16 sources directly**; **no new all-17 tree diagnostic** is required. The all-17 diagnostics do not compete in the operational model-selection stage.

**Holdout integrity qualification:** Earlier repository versions have already used the reserved 20% observations. For v3.1, keep them completely outside **this version's** modelling and threshold decisions and perform at most one final post-selection holdout evaluation. Describe it accurately as a version-specific held-out check, **not a newly pristine independent test across the entire project's development history**. Do not reuse historical holdout results to choose v3.1 changes. Disclose the limitation briefly without turning the notebook into a development-history narrative.

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

**Tree-specific EDA implication:** Long-tailed activity measures, zero-heavy variables, potential threshold effects and conditional relationships motivate testing tree-based splits. Trees do **not** require Gaussian predictors or input standardisation and can discover nonlinear decision rules and interactions; these features do **not** establish that trees will outperform other classifiers. Do not add tree-specific manual transformations, binarisations or selected interaction terms.

The 30% upsell assumption in Section 7 is **not an EDA finding**. It is a separate illustrative business premise.

## 4. Six operational baseline specifications

All **six operational baseline specifications** use the same 16 original sources. The four existing baselines retain their exact v3.0 contracts below; the two new tree baselines use their own shared contract. Each has only the representation required for that estimator.

| Input group | Logistic (L0) | LDA (D0) | Gaussian NB (G0) | Bernoulli NB (B0) |
|---|---|---|---|---|
| Activity counts, durations, rates | Raw continuous | Raw continuous | Raw Gaussian marginals | x>0 indicators |
| SpecialDay | Numeric | Numeric | Numeric Gaussian marginal | 1[SpecialDay>0] |
| Six nominal sources | k−1 one-hot dummies | k−1 one-hot dummies | full categorical one-hot indicators | full categorical one-hot indicators |
| Weekend | 0/1 | 0/1 | 0/1 | 0/1 |
| Estimator | Unpenalised Logit | Standard shared-covariance LDA | Standard GNB | Standard BNB |

Nominal one-hot representation is a modelling compromise for GNB; nominal category indicators and many zero values challenge its Gaussian marginal assumption. With BNB, full one-hot indicators for each category are mutually constrained and therefore not conditionally independent; document that limitation. Encode unknown levels deterministically inside the fitting pipeline.

**Additional classification-tree baseline contracts (both use the same 16 source features):**

| Baseline | Tree criterion | Starting complexity | Input treatment | Rationale |
|---|---|---|---|---|
| **T-G0: Full Gini tree** | `criterion='gini'` | `ccp_alpha=0`, `max_depth=None`, `min_samples_leaf=1`, `min_samples_split=2`, `class_weight=None`, `random_state=42` | Fold-fitted one-hot encoding for nominal sources, numeric values unchanged, no scaling | Establish the unpruned Gini benchmark and let splitting choose predictors/thresholds |
| **T-E0: Full Entropy tree** | `criterion='entropy'` | Same defaults as T-G0 | Same 16-source preprocessing | Establish an independently grown Entropy benchmark; the two impurity criteria can produce different partitions |

Both full-grown trees are **baselines, not assumed final models**. Evaluate their five-fold training ROC-AUC and AP alongside the existing four operational baselines. Tree probabilities use positive-class proportions in terminal leaves; for ROC-AUC/AP use `predict_proba(X)[:, 1]`, not `predict(X)`. A full-grown tree can overfit severely and may produce extreme or coarse leaf probabilities.

Baseline results are reference points, not a claim that any estimator has validated normality, independence or equal covariance.

## 5. Pre-specified sequential paths and classification-tree pruning

**Rule for the four existing paths only (Logit, LDA, GNB, BNB):** Each path attempts its baseline and up to **four** sequential, singly motivated modifications, in the specified order. Compare each challenger to the **currently retained specification**; if rejected, revert to the incumbent before evaluating the next listed change. Thus a nominal step does **not** imply that earlier rejected modifications were retained. Record the actual composed recipe, results and rejection reason for every attempt. Do not test combinations or adjust the order based on observed winner hunting.

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

### 5.5 Guardrails for the four EDA-driven sequential paths

- Every attempted specification retains the full trial trail: parent/retained model, one changed element, EDA rationale, fold scores, mean ROC-AUC, AUC SD/SE, mean AP, acceptance outcome and any warnings.
- Up to **20 sequential-path operational CV attempts total** across the four original paths (including their four baselines); fewer are acceptable when a path ends early or a step is inapplicable. **Tree baseline and pruning-path evaluations are recorded separately, not counted against the 20 attempts.** No 4×4 cross-product of modifications.
- A family may finish at its original baseline. A change accepted in one family is **not** automatically copied to another.
- Learned rare-level pooling, binarisation medians and preprocessing are implemented as reusable, fold-safe pipeline steps; never fit them on the complete training set before CV.
- Neither input-variable transformations nor model hyperparameters are chosen using the final test set.
- Keep model-family specific limitations explicit; do not manufacture a four-family consensus for neatness.

### 5.6 Classification Trees — baseline plus cost-complexity pruning (no 3–5-step requirement)

**Scope and rationale:** Trees automatically discover splits, nonlinear thresholds and interactions using the same 16 source predictors. Rather than invent EDA-led transformations to fill a 3–5-step quota, the **only tree complexity tuning** is pruning via `ccp_alpha`. Fit both Gini and Entropy independently, retaining baseline and pruning results for each.

**For each criterion:**

1. Start from its **full-grown operational baseline** in Section 4: `ccp_alpha=0`, no artificial depth cap, `min_samples_leaf=1`, `min_samples_split=2`, `class_weight=None`. Reuse `random_state=42`.
2. Generate the candidate penalty path from that full-grown tree on the **training partition only**, using `cost_complexity_pruning_path(X_train, y_train).ccp_alphas`. Include `alpha=0` and deduplicate candidates; follow the lecture in omitting the final root-only candidate if the returned path contains it. **Never use the reserved test set.**
3. For each candidate `ccp_alpha`, compute five-fold **stratified** CV ROC-AUC on the same shared training folds; fit any nominal encoding within the fold. Calculate mean AUC, sample SD and SE. Compute AP as a supporting metric, never as a substitute for ROC-AUC when choosing alpha.
4. Apply the **1-SE pruning rule in Section 6.5** independently for Gini and Entropy. Record the selected alpha, resulting leaf count and depth, and fold-level/mean CV ROC-AUC and AP. **If alpha=0 qualifies and is chosen, the selected tree remains unpruned.**
5. Show **full baseline versus selected tree** for each criterion, including any AUC trade-off and reduction in leaf count. Neither AUC improvement nor strict pruning is guaranteed.
6. Send **both selected tree specifications directly** to the six-candidate final comparison. Do **not** compare Gini versus Entropy to pick one before that stage. Their alpha values are in **different impurity units**, so compare models by CV AUC, not raw `ccp_alpha`.

No new grids for `max_depth`, `min_samples_leaf`, `class_weight`, manual feature filtering, log transformations, tree-specific classification thresholds or separate nested-CV performance-estimation process. **Rationale:** Pruning is the taught structural complexity control; adding further searches would depart from the agreed course-aligned scope.

## 6. CV acceptance, selection and model-comparison accounting

### 6.1 Common CV score

- **Primary:** Mean **five-fold training ROC-AUC** (higher is better).
- **Supporting:** Mean fold AP, positive-class prevalence, ROC/PR curves, sample SD across five AUC values, and standard error **SE = SD/sqrt(5)**, where SD uses **ddof=1**.
- Mean fold AUC is the selection statistic; pooled out-of-fold (OOF) AUC may differ and is for visual illustration, **not** substituted into ranking.
- AUC measures ranking, not calibration, accurate probabilities or operating-point value. AP provides minority-class ranking context at ~15.5% prevalence.

### 6.2 One-SE adaptation for the four existing sequential revision paths

The course presents the **one-standard-error rule** as choosing the simpler specification when its CV performance is within one SE of the best. For **L0–L4, D0–D4, G0–G4 and B0–B4 only**, apply that principle **locally to each incumbent-versus-challenger comparison**:

1. Run both on the same five outer folds; calculate fold AUC means and sample SD/SE.
2. If the challenger has a higher mean AUC, treat it as the higher-scoring candidate; **retain the simpler incumbent if its mean is within one SE of the challenger's mean**.
3. Retain the challenger only when it improves mean AUC by **more than that one-SE tolerance**; otherwise reject/revert.
4. If the challenger has no AUC gain, reject it. Report fold-level variability and avoid interpreting this heuristic as a formal significance test.

This is an **operational adaptation** of the lecture's 1-SE model-simplicity principle to the professor's sequential revision process, not a new hypothesis test. The professor's phrase “fold-to-fold spread” did not specify whether to use SD or SE; this PRD fixes **one SE** per the project's course-based decision.

### 6.3 Existing hyperparameter tuning and fold discipline

For Logit L4 and LDA D4, predeclare a small, sensible hyperparameter grid and use **inner stratified CV (e.g. three folds)** inside each outer training fold. Scaling/encoding and hyperparameter selection belong within that inner fit pipeline; the outer validation fold must not select C or shrinkage. On final refit, retune the hyperparameter using training data only with the same predeclared inner-CV method.

Do not reuse an outer-fold validation observation inside its inner model-selection process. Distinguish the effects of feature changes from those of adding/tuning regularisation; only one numbered revision is assessed at each step.

**Terminology and boundary:** The existing Logit/LDA inner CV for a penalised estimator is **preserved from v3.0** and does not mean that v3.1 adopts a new, additional nested-CV **outer performance-estimation framework**. Tree pruning uses the professor's ordinary **five-fold CV selection plus reserved held-out evaluation** workflow. Use the same five shared validation folds in all headline model comparisons. Pruning candidate selection and all other model decisions are training-only.

### 6.4 Finalist selection and optimism

After sequential development, retain **one finalist from each of the four existing pathways**, plus the **Gini** and **Entropy** trees independently selected by the 1-SE pruning rule: **six total final specifications**. Compare all six **directly** on the same **mean five-fold training CV ROC-AUC** metric; do **not** preselect one tree. Choose the overall winner by highest mean CV ROC-AUC. Show AP and SE to contextualise close scores, but do not silently replace the primary rule with AP, accuracy, the financial threshold or a post-hoc preference. Small AUC differences do not imply statistical superiority. If a selected tree's alpha is zero, report it as the selected **unpruned** tree rather than falsely claiming pruning.

Selecting from multiple attempted specifications, including many pruning candidates, makes the winning CV estimate potentially optimistic. A one-time reserved-set evaluation is intended as a check, subject to Section 2's historical-use caveat. No revision after inspecting test results without a fresh, properly separated evaluation design.

### 6.5 Tree cost-complexity penalty selection — one-SE on CV ROC-AUC

For each splitting criterion independently, let `AUCbar(alpha)` be the mean of the five fold ROC-AUC values obtained using **predicted probabilities**. Let `alpha_best` maximise that mean (resolve equal means deterministically). Calculate

```text
SE_best = SD(AUC_fold1, ..., AUC_fold5 at alpha_best) / sqrt(5)
AUC_cutoff = mean_CV_AUC(alpha_best) - SE_best
Eligible = { alpha : mean_CV_AUC(alpha) >= AUC_cutoff }
```

Among eligible candidates, select the **smallest tree** (fewest terminal leaves when the corresponding alpha is refitted on the complete training partition). If several eligible alpha values yield the same leaf count, take the **largest alpha**; record the deterministic tie rule. This implements the agreed 1-SE preference for simplicity rather than blindly taking `alpha_best`.

**Cost-complexity objective:** `R_alpha(T) = R(T) + alpha * |T|`, where `R(T)` is the leaf-weighted training impurity (scikit-learn's scaled impurity measure), `|T|` is the number of terminal leaves and `alpha` controls the complexity penalty. Higher penalties generally produce smaller trees. Gini and Entropy impurity scales differ; their selected alpha values are **not comparable numerically**.

**Rationale:** Full trees often overfit; CV AUC estimates ranking quality for the project's unbalanced binary outcome, and the one-SE cutoff avoids retaining unnecessary splits for minor CV gains. The 1-SE cutoff is a pragmatic model-complexity rule, **not** a hypothesis test or guarantee of improved test ROC-AUC. This same procedure applies independently to both Gini and Entropy; final six-way model comparison uses their selected CV AUCs.

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

Once the overall winner among **all six specifications** is selected on CV, calculate thresholds using that model's **training OOF purchase probabilities**. There is **no tree-specific threshold regime**; when the winner is a tree, use its leaf-based `predict_proba` probabilities and acknowledge that their coarse levels and possible miscalibration complicate the hypothetical 0.20 cost interpretation. Report **exactly four primary references**:

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
| A6 — Six operational baselines | One baseline CV table with Logit, LDA, GNB, BNB, full Gini and full Entropy | Establish reference performance without assuming pruning improves ROC-AUC |
| A7 — Four sequential paths and tree pruning | Preserve the four-path **all-attempts** ledger and add two full-versus-selected tree comparisons; save both candidate alpha paths with fold ROC-AUC/AP, SE, alpha and leaves | Explain EDA-led changes for existing models and why CV/1-SE selected each tree's complexity; no artificial 3–5 tree steps |
| A8 — Finalists and selection | One **six-specification** CV comparison (four existing finalists + both selected trees), with AUC/AP/SD/SE and one appropriate ROC comparison | Select one winner by mean CV AUC; do not preselect one tree; disclose winner-selection optimism |
| A9 — Winner's scores | One winner OOF score distribution and **one** PR curve with AP and prevalence benchmark | Ranking, probability concentration and calibration limits; recognise discrete leaf scores if a tree wins |
| A10 — Thresholds | One sensitivity–specificity curve and one four-reference threshold table | Compare 0.20 against crossover/prevalence/0.5 and their FP/FN trade-offs |
| A11 — Cost sensitivity | Small q-sensitivity table/annotation (20%, 30%, 40%) | Consequences of hypothetical business premises; no causal sales claim |
| A12 — Finalisation | One held-out check per Section 2, fit audit and unchanged all-data refit | What was validated, what was not; no training score claimed as test performance |
| A13 — Conclusions | Explicit research answer, empirical results and scoped business interpretation | Limitations and implications without overclaiming |

**Tree visualisation:** Include one readable illustration of a selected pruned tree (or interpretable top levels if too large) and explain main splits as predictive—not causal—associations. Report selected criterion, `ccp_alpha`, full/selected leaves and depth, five-fold CV AUC and AP. Do not invent splitting rules before fitting.

**Visual discipline:** Each major plot or table should appear **once**. Prefer a concise attempts table over separate repetitive path charts. Keep extensive warnings, fold-by-fold detail and feature/pipeline diagnostics in machine-readable artifacts; show only material anomalies in the academic narrative. No orphan plots, redundant notebook sections or purely decorative figures.

### Slides: 20-minute presentation

Prepare a coherent slide deck organised around **question and business context → EDA evidence → four EDA-led sequential pathways plus tree pruning → six-specification CV comparison and winner → four threshold references/upselling assumptions → limitations and conclusion**. Use slides for delivery; the notebook is reproducibility support. Allocate enough time to explain **why** changes were tried or rejected rather than displaying code or every intermediate diagnostic.

## 10. Statistical, operational and numerical limitations

- **Predictive, not causal:** Browsing variables and Revenue do not establish treatment effects, the natural no-agent purchase rate or who benefits from contact.
- **Potential probability miscalibration:** ROC-AUC and AP assess ordering, not expected-profit accuracy. The cost cutoff assumes approximate calibration; use simple OOF score/reliability inspection and qualify any failure. A separate elaborate calibration programme is **not** mandatory unless supported and approved.
- **Imbalance:** Accuracy can be high for a trivial no-purchase classifier. Interpret ROC-AUC, AP, recall, specificity and precision together.
- **Distribution/independence:** Right skew, zeros and nominal dummies challenge Gaussian marginals; within-class dependence especially challenges NB; LDA permits correlated predictors but assumes a shared class covariance and a Gaussian model; transformations do not prove these assumptions.
- **Rare categories:** Warn about unstable small-cell rates, quasi-separation and unseen validation levels. Never suppress fitting or convergence warnings without checking them.
- **Classification-tree limits:** Unpruned trees can severely overfit; pruned trees can be unstable under small training changes and may deliver a small set of repeated/extreme leaf-based purchase probabilities. Tree split importance and thresholds are predictive associations, not causal effects; ROC-AUC/AP do not establish probability calibration. One-hot nominal variables may yield multiple indicators of one source feature.
- **Selection bias:** Many EDA-guided and pruning-path CV comparisons can make the selected mean AUC optimistic. One-SE is a **pragmatic complexity heuristic**, not formal proof of statistical superiority.
- **Duplicates and generalisation:** Retained duplicate rows may make CV/test membership partly dependent; source does not identify unique customers or support forecasts of future website conditions.
- **Session timing:** Existing measurements are not proven to be real-time available early enough to dispatch an agent; PageValues exclusion is precautionary rather than a guarantee.
- **Historical test use:** The v3 20% reserved observations were examined in earlier development; describe any reported v3 held-out score with the Section 2 qualification.
- **Business assumptions:** S$3 cost, 30% upsell success and S$50 margin are illustrative. No empirical profit uplift, deployment recommendation or “guaranteed purchase” claim is supported.

## 11. Reproducibility, audit and finalisation workflow

1. Preserve **data/uci_468.csv**, **v1/v2/v3.0 PRDs**, archive, the executed v3.0 notebook and its evidence, Git history and existing historical artifacts. Create v3.1 artefacts separately; do not relabel v3.0 outputs as v3.1.
2. Preserve the v3.0 four-path sequential change order; freeze the tree baseline defaults, Gini/Entropy criteria, alpha candidate procedure, 1-SE rule, shared folds, comparison metric and existing upselling parameters **before** inspecting new tree results.
3. Reuse reproducible training-only EDA and four original all-17 diagnostics; preserve four existing operational baselines and sequential trial records. Add the two full-tree baselines, both pruning paths, full-versus-selected comparisons and six finalist scores. Log every tree alpha candidate separately from the 20-attempt legacy ledger.
4. Independently recompute mean fold AUC/AP, SD/SE, each tree's best alpha and 1-SE cutoff, smallest qualifying tree selection, six-way winner identity, complete OOF coverage, threshold confusion counts and derived rates from saved fold/OOF outputs.
5. Confirm all learned preprocessing and regularisation searches fit **only** within the correct folds, and that tree pruning candidates use training data only; guard against look-ahead, nominal encoding and reserved-test leakage.
6. Freeze the selected finalist and training-stage cost threshold; refit on all **9,864 training rows** using the chosen pipeline. Inspect convergence, rank/variance issues, estimated probabilities, warnings, and reproducibility.
7. Evaluate the **frozen** model and threshold on the reserved **2,466 rows at most once for the v3.1 procedure**. Report clearly that this check is not independent across earlier project versions. Do not revise the winner or threshold after test inspection.
8. Refit the **unchanged selected recipe** (including appropriate training-only hyperparameter procedure) on all **12,330 rows** for the final model; do **not** present full-data in-sample scores as external validation.
9. Save **v3.1-labelled** CSV/JSON outputs: four-path trial ledger and fold scores, tree Gini/Entropy alpha paths (candidate, fold scores, SE, leaves, depth, selected alpha), six finalists, OOF scores, thresholds, cost assumptions/sensitivity, test check, chosen pipeline parameters, warnings and provenance (source checksum, row IDs, package versions and random state).
10. Verify actual v3.1 notebook outputs and figures top-to-bottom in a clean run **during a subsequent implementation phase**. Only claim verification steps actually completed. Update the active README, technical plan and AGENTS guidance **with that implementation**, so the currently implemented v3.0 code/results are not silently relabelled v3.1.

## 12. Acceptance criteria for subsequent v3.1 implementation

- [ ] **Correct objective:** prediction-focused research question; four existing pathways plus one tree pathway (Gini and Entropy); no unsupported causal, inference or voucher claims.
- [ ] **Data discipline:** 12,330 sessions, original duplicates preserved, quality audit, stratified 80/20 split seed 42, five shared stratified training folds seed 42, no test-driven changes.
- [ ] **Features:** preserve four existing all-17 diagnostics; 16-source operational baselines for all four prior classifiers plus full Gini and Entropy trees, with PageValues excluded cautiously and nominal predictors appropriately encoded within folds.
- [ ] **Revision accountability:** up to five sequential attempts for **each of the four existing pathways**, one EDA-motivated change at a time, explicit keep/reject and all attempts recorded; **no 3–5-step rule for trees**; preserve exclusion of Mixed NB.
- [ ] **CV rule:** correct common-fold mean ROC-AUC, AP, fold SD/SE, local one-SE revision decisions for the four existing pathways, **six** final selected specifications (including Gini and Entropy), overall winner by highest mean ROC-AUC.
- [ ] **Existing inner tuning preserved:** logistic penalty C or LDA shrinkage strength tuned using only inner training CV inside the full preprocessing/estimator pipeline; **no new outer nested-CV evaluation regime**.
- [ ] **Tree growth and pruning:** both full-tree baselines use the stated defaults; independent Gini/Entropy alpha paths are generated on training data; candidate five-fold ROC-AUC/AP, SD/SE and 1-SE cutoffs independently verified; selected alpha gives the smallest eligible tree; full-versus-selected trees, leaves/depth and selection rationale reported.
- [ ] **Tree comparison:** both selected trees enter the final six-way model comparison **directly**, without a preliminary Gini-versus-Entropy winner; use `predict_proba` for ROC-AUC/AP; permit a chosen `alpha=0` without falsely claiming pruning.
- [ ] **Thresholds:** training OOF prevalence, 0.5, crossover and **fixed hypothetical 0.20**; interpretable FP/FN/sensitivity/specificity/precision; no threshold chosen using held-out data.
- [ ] **Economics:** exact S$3 / S$12 net misclassification costs derived from S$3 labour, 30% upsell success, S$50 incremental gross margin; show cost sensitivity, do not model or assert actual uplift.
- [ ] **Visuals/story:** one purposeful instance of each essential chart/table; concise purpose and numbers; no bloated warnings; 20-minute explanatory slide deck.
- [ ] **Test qualification:** single v3.1 reserved-set check **after freezing** the overall selected model and threshold; preserve the existing v3.0 historical-use disclosure, no claim of pristine lifetime independence or subsequent tuning.
- [ ] **Final refit:** model fitted on training for audit and unchanged specification finally fitted on all data; no in-sample performance inflation.
- [ ] **Verification:** complete run, result recomputation, fit/warning audit, source/figure/provenance checks and updated implementation documents.

## 13. Decision ledger and current boundary

| Decision | v3 resolution |
|---|---|
| Objective | **Prediction only**; cost threshold is a hypothetical interpretation, not a second causal objective |
| Classifiers | Four established **Logit, LDA, GNB, BNB** pathways plus a **Classification Trees** pathway with independently selected Gini/Entropy specifications; **Mixed NB removed** |
| Development | Preserve **3–5** ordered EDA-motivated specifications **only for four existing paths**; trees use full baselines and cost-complexity pruning rather than artificial sequential steps |
| Acceptance heuristic | **Course-based one-SE** simplicity principle applied locally to adjacent revisions for four existing pathways; trees use one SE below best CV ROC-AUC and select **smallest eligible tree** |
| Tree criteria/defaults | **Gini and Entropy**; initial `ccp_alpha=0`, unrestricted depth, min leaf=1, min split=2, no class weighting; categorical one-hot, no scaling |
| Tree pruning | Independent `cost_complexity_pruning_path` plus shared **five-fold stratified CV ROC-AUC** and 1-SE selection; record full versus selected tree |
| Tree final candidates | **Both** selected Gini and Entropy trees directly enter final comparison, no preliminary criterion winner |
| Tuning | Regularisation selected through **inner CV**, including fitted preprocessing |
| Winner | Highest **mean five-fold training ROC-AUC** among **six selected specifications** (four existing finalists + selected Gini + selected Entropy); AP secondary |
| Partition | Retain existing **80/20, seed 42**, five common outer training folds |
| Operational sources | Original **16 without PageValues**; separate all-17 diagnostics |
| Business scenario | Live agent upsells to **predicted buyers**, not rescue of proven abandoned purchases |
| Business inputs | **S$3 per contact**, **30% conditional upsell success**, **S$50 incremental gross margin** |
| Correct net cost matrix | **FP = S$3**, **FN = S$12**, baseline TP/TN error loss zero |
| Cost decision cutoff | **0.20**, compare against prevalence, **0.5** and sensitivity–specificity crossover |
| Sensitivity | Vary hypothetical q **20% / 30% / 40%**; no empirical profit or causal uplift conclusions |
| Holdout | One v3.1 post-selection reserved-set check, **existing historical prior-use caveat preserved** |
| Presentation | Slides for 20 minutes plus fully executable notebook |
| Remaining PRD-level questions | **None**; technical plan, notebook implementation, results and independent review remain future work |

**Version record:** PRD v3.1, dated 3 November 2026, is a **targeted amendment of v3.0**, adding two classification-tree baseline specifications, cost-complexity pruning with five-fold ROC-AUC/1-SE selection and a six-specification final comparison. All four v3.0 EDA-led paths, cost assumptions and threshold/reporting rules are retained unless explicitly modified above. PRD v3.0 and earlier history remain intact; **no v3.1 tree notebook, performance results or execution are claimed by this requirements document**.