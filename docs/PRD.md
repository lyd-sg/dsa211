# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) · v1.0 approval candidate · 25 October 2026

> **Status: Final PRD prepared for user approval; implementation NOT authorised.** This document consolidates agreed planning decisions through Q27 and adds an explicit purpose requirement for every substantive analysis. It replaces earlier PRD drafts on this branch. No notebook, dataset or modelling implementation has been changed by preparation of this PRD.

### 1. Project purpose

**Research question:** How well can variables describing a browsing session predict whether that session ends in a purchase (`Revenue = 1`), and which of the DSA211 classification approaches provides the most defensible predictions?

**Primary objective: prediction.** Evaluate and compare the three coursework model families — Logistic Regression, Naive Bayes, and Linear Discriminant Analysis (LDA) — using reproducible cross-validation. Select **one** specification based on predictive discrimination, then conduct **one** held-out test audit. This project is **not** a coefficient-inference or causal-effects study.

**Secondary objective: interpretation of a hypothetical voucher policy.** Use the selected model's predicted purchase probabilities to illustrate how alternative classification thresholds affect targeting, and how assumed voucher conversion rates affect hypothetical revenue. The simulation **does not measure actual voucher effectiveness**.

**Deliverable:** One self-contained, executable, lab-style Python notebook with focused plots/tables and concise statistical interpretation. A separate **supplementary training-only EDA notebook must be maintained in the repository but is not submitted**, as agreed in Q9 and Q15.

**Target reader:** DSA211 instructor/markers and a statistically literate reader. All methods must be traceable to the course, with extensions clearly labelled.

### 2. Governing requirements and approval

**Authority:** Mandatory instructor/assignment instructions → this PRD once explicitly approved → technical plan/`AGENTS.md` → previous notes and notebooks. The earlier two-page `Predicting Online Purchases` working proposal is revisable; its live sales-support, 5:1 cost, QDA and other proposed extensions do not override the current agreed scope. If an independently confirmed mandatory requirement conflicts with this PRD, raise it before implementation.

**Instructor's project-specific workflow (`project_cv_workflow.html`, 1 October 2026):** check data quality and split once → training-only EDA → fold-contained preprocessing → common CV folds/metric → compare candidates → choose and refit one winner on training → score the winner on test **once** → refit that exact specification on all data without a new test score. This supersedes the simpler in-sample evaluation used for teaching in parts of Lab 6.

**Approval gates:**
1. **PRD approval:** user explicitly approves this v1.0 candidate.
2. **Technical plan approval:** code-level methods, source files, candidate revisions, checks and implementation sequence are agreed separately.
3. **Implementation and review:** only then modify analysis notebooks; execute and verify against this PRD.

Preparing or approving the PRD by itself does **not** approve any code change. Subsequent scope changes must be recorded before implementation.

### 3. Non-negotiable communication rule: state the purpose of every analysis

**Every substantive analysis block in the submitted notebook must make its purpose immediately clear — before its code or output.** No plot, table, diagnostic or model comparison should appear merely because it is standard in statistical analysis.

Use the following short format where appropriate:

> **Purpose / question:** What precisely are we trying to establish, and why does it matter for this prediction task?
>
> **Method and evidence:** Show the relevant Python code and its actual table/figure/result.
>
> **Interpretation:** What does this output say, and what does it **not** establish?
>
> **Implication / decision:** What does it change (or not change) about features, assumptions, model specification, evaluation or application?

A one-sentence purpose and one-to-three concise sentences of interpretation are normally sufficient. Do not create empty ritual headings for trivial setup cells; the rule targets **substantive** analyses.

**EDA is useful only when it informs reasoning.** For example, do not stop at “`Informational` is zero-heavy.” State why its many zeros might make a Gaussian likelihood implausible or why a positive-versus-zero representation might be considered, then state whether the result warrants investigation. Equally, do not treat an observed association as proof of causality or leakage.

**Presentation benchmark:** DSA211 Labs 1, 5, 6 and 7. Use clear section labels, short Markdown context, executable code, selected tables and labelled plots, then interpretation. Unlike teaching labs, omit exercise questions, `YOUR CODE HERE` placeholders, tutorials of elementary syntax, repeated printouts and unnecessary verbose model summaries. **There is no arbitrary word count, plot quota or 50% prose-cutting target.**

### 4. Dataset and held-out-data discipline

| Item | Agreed specification |
|---|---|
| Dataset | UCI *Online Shoppers Purchasing Intention*: **12,330 sessions**, 17 source predictors and binary `Revenue` outcome |
| Unit of analysis | **Session**, not an identified unique customer |
| Data completeness | Dataset reported with no missing values; verify types/missing markers when loading |
| Duplicate policy | **Retain all 12,330 observations**, including **125 excess exact duplicate rows** (12,205 unique full rows). Earlier inspection found that these repeated rows describe **low-activity, non-purchasing sessions (`Revenue=0`)**; reverify this descriptive finding during data-quality checks. Matching records are **not** proof of the same visitor/session, and repeated patterns may affect fitted models and cross-validation. |
| Outcome imbalance | Approximately **15.5%** purchase rate; do not rely on accuracy alone |
| Split | New **stratified 80% train / 20% held-out test**, **9,864 / 2,466** records |
| Reproducibility | Use **`random_state=42`** for the agreed new stratified 80/20 split and shuffled five-fold stratified CV, preserving Q14's earlier decision. The professor's project workflow illustrates `2026` as a seed, **not a mandate to override our fixed seed**. Record the seed and folds for reproducibility. |
| CV | **Five-fold StratifiedKFold**, shuffled with fixed seed, **identical folds for all seven operational specifications** |
| Test access | The 20% test set is reserved for **one single-winner audit only**; no exploratory plots, target-dependent EDA, feature/model selection or threshold tuning on it |
| Historic caveat | A previously explored 75/25 partition of the **same dataset** was seen before this revised protocol. Do **not** describe the new holdout as historically untouched or fully independent of that earlier exposure. |

**Data ordering is mandatory:** perform basic quality checks (shape, variable types, missingness, duplicates, class balance), **then split**. Predictor distributions, predictor–`Revenue` associations, diagnostics, transformation hypotheses and all model comparisons belong on the **80% training partition only**. Any data-learned preprocessing belongs within the training fold of a pipeline.

### 5. Analytical plan — purpose, evidence and decision

The notebook must preserve this causal **reasoning chain** (not claim causal effects):

| Analysis / section | **Purpose — question it answers** | Required evidence | Implication / decision supported |
|---|---|---|---|
| **A1. Data quality and class balance** | Can the source be analysed reliably, and why is accuracy misleading for this target? | Data shape/types, missingness, duplicate count and class balance | Retain session-level observations; choose AUC as principal metric; explain data limitations |
| **A2. Training numerical EDA** | Which activity variables are skewed or mostly zero, and why might this matter for model assumptions or representation? | Focused summary/zero-share distribution plots for relevant numeric predictors | Generate **hypotheses**, not automatic transformations |
| **A3. Training categorical EDA** | Do purchase rates vary across meaningful categorical groups, and are rates based on enough sessions to interpret? | Selected category counts, buyer-rate comparisons or compact plots | Identify potentially useful predictors/group effects; avoid overclaiming sparse groups |
| **A4. Training predictor relationships / assumptions** | Are predictors strongly related to each other or to purchase, and which assumptions of NB/LDA/Logit may be strained? | Selected correlations, within-class relationships, empirical-logit/other course-aligned checks where relevant | Explain model assumptions, possible instability or EDA-informed revisions; no blanket battery of irrelevant tests |
| **A5. Initial all-17-predictor models** | What happens if we follow the professor's “start with all predictors” guidance, and how much does `PageValues` affect results? | **Four** training-only initial models; transparent all-17 versus without-`PageValues` comparison on comparable training validation evidence | Exclude `PageValues` from all operational models due to **possible timing/availability leakage**, not because predictive association alone proves leakage |
| **A6. Four operational baselines** | How do course-taught classification methods compare **before optional EDA-based improvements**? | Logit, Gaussian NB, Bernoulli NB and LDA fitted from the same 16 source variables with prescribed encodings | Establish fair interpretable reference models; expose assumptions and model-specific input differences |
| **A7. Three EDA-informed revisions** | Can a **documented issue** in the predictors or model assumptions motivate a more appropriate specification? | One revised Logit, one revised NB, one revised LDA **if justified**; concise before/after explanation | Decide which changes are defensible. Do not create changes merely to boost AUC or pretend unhelpful changes worked |
| **A8. Five-fold CV comparison** | Which operational specification is most likely to discriminate buyers from non-buyers on unseen sessions? | One **seven-row** same-fold CV table: mean ROC-AUC, SD/SE across folds and average precision; overlaid **training OOF ROC curves** | Select **one winner by primary ROC-AUC**, consider course parsimony/one-SE reasoning when practically tied; never select by voucher revenue |
| **A9. Winner probability histogram** | Are the winning model's predicted probabilities spread out or extreme, and could a fixed threshold behave oddly? | Histogram of **training out-of-fold predicted purchase probabilities** | Discuss limitations of probability accuracy, especially NB; **AUC does not establish calibration** |
| **A10. Threshold sensitivity** | How do plausible, coursework-supported thresholds change false-positive/false-negative rates and voucher coverage? | Training-OOF sensitivity/specificity plot and **four-threshold** comparison table including precision, voucher share and simulated revenue at fixed reference assumptions | Explain trade-offs; retain **0.667 as the primary policy**, not whichever threshold reports the most revenue |
| **A11. Voucher-conversion sensitivity** | How dependent is simulated business performance on an unknown **incremental conversion probability**? | Four-scenario revenue comparison (`q = 0.10, 0.25, 0.50, 1.00`) at **fixed 0.667** with constant recipients | Communicate assumption sensitivity; **no claim of measured treatment effects or real revenue lift** |
| **A12. Single test audit** | Does the **one CV-selected winner**, already fixed on training, generalise to held-out sessions? | One final **20% test** ROC-AUC/ROC figure, confusion matrix and relevant sensitivity, specificity and precision at **0.667** | Report its independent-under-the-revised-protocol audit, noting historical exposure; do not score another model or use test results to improve it |
| **A13. Final all-data refit** | Having completed evaluation, what model uses all available observations for the final specification? | Refit the **exact selected specification** on train + test (12,330 sessions) **after** audit | Present the final fitted model; retain the **earlier held-out performance** as the reported audit, with no further test |
| **A14. Conclusion and limitations** | What did we learn about predictive ranking, model assumptions, threshold trade-offs and applicability? | Direct answers to research question and major findings, with practical caveats | Clearly distinguish defensible prediction from hypothetical policy economics and deployment feasibility |

**Every A1–A14 block must contain an explicit purpose in the submitted notebook.** The exact sections can be grouped for readability; the analytical questions, evidence and conclusions must not disappear.

#### 5.1 Supplementary EDA: five focused investigations, not a model search

The separate, non-submitted EDA notebook must **extend rather than repeat** the existing main-notebook EDA. These five checks also require an explicit **purpose → evidence → implication**.

| Supplementary question | Why investigate it? | How the result may affect the main notebook |
|---|---|---|
| **Zero versus positive activity, and intensity when positive** | Does “no activity” convey different information from “how much activity”, especially for informational/administrative variables? | May justify a `>0` indicator, transformed magnitude or retaining the original feature; no change forced |
| **Targeted categorical subgroup patterns** (e.g., `VisitorType × Month`) | Could apparent group effects differ across a second contextual factor? | Support a small, justified interaction or show why one is unnecessary |
| **Rare categories** (`TrafficType`, `Browser`, `Region`) | Are striking conversion rates artifacts of tiny cell sizes? | Warn against overinterpretation; consider pooling only if defensible |
| **Meaning of `SpecialDay`** | Does this numeric holiday-proximity score behave like an ordered/intensity variable or a simpler binary indicator? | Baseline stays numeric; alternative representation needs evidence |
| **Feature availability at proposed voucher decision time** | Would a model actually know each predictor before the session ends? | Qualify any intervention interpretation; do not claim real-time feasibility |

**Carry forward only decision-relevant findings** into the submitted EDA, including counterevidence or null findings where necessary. This supplementary notebook must not become an automated grid of model/feature combinations scored repeatedly for the highest AUC. **The exact three revised model recipes are deliberately conditional on the training EDA** and are to be documented in the technical plan once supported.

### 6. Model specifications

#### 6.1 Fixed scope

**Three model families, four coursework-based baselines, three potentially revised family-level specifications.** This creates **seven planned operational comparison slots**:

| Family | Baseline(s) | Revised specification | Purpose of comparison |
|---|---|---|---|
| **Logistic Regression** | Unregularised, maximum-likelihood Logit | EDA-motivated Logit | Check whether justified representation changes help a standard discriminative classifier |
| **Naive Bayes** | **GaussianNB** and **BernoulliNB** | EDA-motivated NB; **mixed-likelihood NB only if justified** | Contrast Gaussian marginals with binary-present/absent marginals; explore a mixed treatment only with a clear reason |
| **LDA** | Standard LDA | EDA-motivated LDA | Check whether data-informed representation changes improve the shared-covariance generative model |

No QDA, KNN, boosting, exhaustive regularisation searches or unrelated classifiers. Mixed-likelihood NB is **not** one of the mandatory taught baselines; if used, explain it as an extension of Lecture 6's conditional-independence framework. If EDA does **not** justify a distinct revision in a family, state that candidly rather than manufacturing a seventh unique model.

#### 6.2 Source predictors and baseline treatment

Four first-pass all-17 fits are for **training-only diagnostic comparison**, not operational candidates. Remove `PageValues` for the seven planned operational specifications because its availability at a real decision point is questionable. **All operational baselines start from the same remaining 16 source predictors.** Revisions may modify/remove features **only with stated EDA evidence**, not silently or solely to inflate CV scores.

| Input type | Logit baseline | Gaussian NB baseline | Bernoulli NB baseline | LDA baseline |
|---|---|---|---|---|
| Numerical counts, durations, rates | Original numeric values | Original numeric values | `1[x > 0]`, else 0 | Original numeric values |
| `SpecialDay` (proximity score) | Original numeric values | Original numeric values | `1[SpecialDay > 0]` | Original numeric values |
| Nominal categorical columns | **k−1** reference-level indicators | Full **k** one-hot indicators | Full **k** one-hot indicators | **k−1** reference-level indicators |
| `Weekend` | Original 0/1 | Original 0/1 | Original 0/1 | Original 0/1 |

- **Minimal preprocessing:** no optional scaling/standardisation, automatic log transforms, automatic predictor deletion, class weighting, penalisation or extra feature engineering in the initial operational baselines.
- **Bernoulli exception:** binarising magnitudes is necessary to use the taught Bernoulli likelihood; it loses intensity information and is **not** itself evidence of predictive improvement.
- **Distributional caveats:** Gaussian NB imposes Gaussian marginals on dummy columns; one-hot columns from the same categorical variable are dependent; Bernoulli NB ignores original magnitudes; LDA assumes multivariate Gaussian features and pooled class covariance despite mixed inputs. A model may still rank well under imperfect assumptions; interpret probabilities cautiously.
- **Pipeline discipline:** encoders and any steps estimating quantities from data are fit **inside each training CV fold**; maintain fixed training-derived column order/handling of unforeseen categories. Check unregularised Logit convergence and LDA numerical feasibility rather than silently switching estimator/regularisation.
- The categorical-encoding detail and all EDA-dependent revisions must be traceable in code and the technical plan.

### 7. Evaluation, selection and final-model workflow

1. **Define before results:** primary model-selection metric is **mean five-fold training CV ROC-AUC** (threshold-free ranking); report **average precision** for class imbalance, plus fold **SD and SE = SD/√5** as supporting evidence. Accuracy alone is unsuitable.
2. **Compare fairly:** same stratified folds for each of seven operational specifications. Every candidate pipeline is fitted anew inside its training folds. **Overlaid out-of-fold ROC curves** are illustrative; the pooled OOF AUC need not exactly equal the mean of the five per-fold AUCs used for selection.
3. **Choose one:** prefer the highest mean CV ROC-AUC. For a practical near tie, consider a **simpler specification within approximately one SE of the best** in the professor's taught parsimony spirit; document the exact reason. This is **not** a formal hypothesis test or automatic claim that models are statistically equivalent.
4. **Refit the winner on all 80% training observations**, freezing its predictor treatment and estimator before test access.
5. **Evaluate that one winner on the 20% test once.** Report its ROC-AUC, confusion matrix and pertinent rates at the **precommitted primary threshold 2/3**. **Do not** compare or select additional models/thresholds based on test outcomes.
6. **After the audit, refit the exact winner on all 12,330 observations** for the final model; **do not** rerun a test or substitute this refitted model's in-sample score for the held-out audit.

**Historical exposure limitation:** prior work examined the same overall dataset with a different 75/25 partition, so the new holdout is not historically pristine. Explicitly mention that fact; subsequent work must nonetheless honour the now-frozen holdout.

### 8. Threshold policy and hypothetical voucher calculation

**Positive class:** `Revenue=1`, i.e. the session would result in a purchase without the hypothetical voucher.

**Policy:** predict buyer when `p ≥ t` and **do not** issue a voucher; when `p < t`, classify as non-buyer and offer a hypothetical **20% voucher**. The policy is deliberately an illustration applied retrospectively to complete historical sessions, **not** a proven deployable intervention.

#### 8.1 Primary threshold (cost reasoning from Lecture 5)

Let `A` be a **common no-discount order value used only as a normalisation**, `d = 0.20` the discount and `q_ref = 0.50` an **assumed**, not observed, incremental conversion chance for an otherwise non-buying voucher recipient.

- **False negative** (actual buyer predicted non-buyer; unnecessarily receives voucher): `C_FN = dA = 0.20A` in foregone price.
- **False positive** (actual non-buyer predicted buyer; misses voucher): `C_FP = (1-d)q_ref A = 0.80 × 0.50 A = 0.40A` in assumed expected forgone voucher revenue.
- **Primary cost-based buyer threshold:** `t* = C_FP / (C_FP + C_FN) = 0.40 / 0.60 = 2/3 ≈ 0.667`.

This threshold is theoretically motivated **only under the stated costs and meaningful probabilities**. It is not empirically guaranteed optimal; poor NB probability calibration can make its use problematic even if AUC is respectable.

#### 8.2 Four coursework-supported threshold references — **training OOF only**

Compare the selected model at these **exactly four** operating points:

| Threshold | Why include it? |
|---|---|
| **Training purchase base rate** (about `0.155`; compute exact `mean(y_train)`) | Course prevalence-based starting reference for imbalanced data |
| **0.500** | Conventional equal-probability default |
| **0.667** (`2/3`) | **Primary, precommitted cost-based policy** |
| **Sensitivity–specificity crossover** | Training-OOF threshold where the two rates are closest; balanced classification reference, **not** cost optimal |

At fixed **20% discount and 50% reference conversion**, report for each **training-OOF** threshold: sensitivity, specificity, precision, number/share of vouchers, and hypothetical revenue (preferably as a change relative to no vouchers in units of `A`). Plot sensitivity and specificity against threshold, with clearly identified reference lines/crossover. **Do not change the primary threshold to whichever looks best.**

#### 8.3 Separate conversion-rate sensitivity — threshold fixed

At **`t = 2/3` only**, compare **`q ∈ {0.10, 0.25, 0.50, 1.00}`**, holding the model, predicted probabilities, recipient assignments, discount and common `A` fixed across scenarios. Vary **only** assumed incremental conversion. The chosen 0.667 threshold is **not re-optimised for each q**.

For a set of frozen classifications, use the confusion matrix with actual buyers as positive:

- **No-voucher reference:** `R_0/A = TP + FN`.
- **Illustrative expected voucher revenue:** `R_q/A = TP + 0.80 FN + 0.80q TN`.
- **Illustrative difference:** `ΔR_q/A = 0.80q TN − 0.20 FN`.

This is a **hypothetical arithmetic scenario**, not causal uplift, profit, measured discount response or actual revenue. If the simulation is presented alongside the held-out model audit, reuse the **same single-winner frozen held-out predictions at 0.667**; do not evaluate alternative test thresholds. Do not claim `q` is identified by the UCI data.

### 9. Required main-notebook outline and key visuals

Use the **purpose-first** rule in Section 3 for each section:

| Order | Section | Minimum substantive result |
|---|---|---|
| 1 | Research question, dataset, quality and split | Basic data checks; imbalance; protocol stated clearly |
| 2 | Training-only EDA and modelling implications | Selected numerical/categorical/assumption evidence; relevant supplementary EDA findings |
| 3 | Initial full-predictor diagnostic fits | Four all-17 results and explicit `PageValues` reasoning/comparison |
| 4 | Operational baselines | Four 16-source-feature baselines; model-required representations made visible |
| 5 | Motivated revisions | Up to three coherent family-level revisions and why each was or was not warranted |
| 6 | Training-CV model selection | **Seven-specification CV table** (where distinct revisions exist), **overlaid OOF ROC curves**, single-winner rationale |
| 7 | Threshold analysis | Winner OOF probability histogram; sensitivity–specificity plot; four-threshold comparison table |
| 8 | One held-out evaluation and voucher illustration | **One winner** test ROC and confusion matrix at **0.667**, plus the four conversion-rate hypothetical revenue scenarios |
| 9 | Full-data refit and conclusions | Refit exact winner; what predictive evidence shows; calibration/timing/historical test limitations |

An additional precision–recall curve may be included if it illuminates the imbalanced outcome, but is not compulsory; **average precision remains a reported metric**. Combine redundant plots where clarity improves.

**Evidence must remain visible:** all code runnable end to end; tables and charts have labelled axes/definitions; numerical results and written interpretations agree; no stale 75/25, 0.80 policy, 5:1 live-support or prior historical scores are presented as results of the revised analysis.

### 10. Scope exclusions and statistical limitations

**Out of scope:** QDA; KNN; gradient boosting; splines; arbitrary polynomial/interaction sweeps; automated feature-search or regularisation competitions; broad inferential coefficient testing; formal calibration/reliability-curve procedures; new modelling algorithms unrelated to DSA211; intervention-effect estimation; production website or real-time voucher engine.

**Limitations to disclose when relevant:**
- **Association vs timing:** strong `PageValues`–`Revenue` association alone does not prove leakage; its potential unavailability at voucher time justifies a cautious exclusion. The remaining 16 features are **not certified available mid-session**.
- **Class imbalance and calibration:** high accuracy can coexist with poor buyer detection; ROC-AUC evaluates ranking, not probability calibration or monetary utility.
- **Naive Bayes/LDA assumptions:** predictors are skewed, zero-heavy, categorical and dependent, so fitted probability values may be unreliable even when discrimination is reasonable.
- **Duplicates:** retain the 125 excess full-row duplicates; earlier analysis found them to be **low-activity, `Revenue=0` observations** (to be reverified). Identical fields do not establish identical real-world sessions, but repeated patterns may influence model fit and CV.
- **Historical holdout exposure:** previous evaluation on an overlapping sample means the new test cannot honestly be called entirely untouched.
- **Voucher claims:** no observed counterfactuals, order values, margins or treatment labels exist to establish real conversion uplift, profit or deployability. All voucher amounts are in assumed common-`A` units.

### 11. Acceptance criteria — required before completion

- [ ] **Purpose-first audit:** every substantive analysis (A1–A14, including supplementary EDA findings imported into main analysis) begins with a clear purpose/question and ends with a defensible implication; no orphan plot or “so what?” gap.
- [ ] **Course alignment:** four taught baseline classifiers, three EDA-conditional family revisions, permitted feature handling, and correct single-winner professor CV/test/refit sequence.
- [ ] **Data discipline:** quality check before split; all target-related EDA and choices on training; fixed stratified 80/20 split; pipelines fitted within CV folds; holdout used only for final frozen winner.
- [ ] **Transparent EDA-to-model logic:** decisions are justified by actual observed evidence; supplementary EDA notebook retained in repo and not included with submission; no fabricated improvement if an EDA-informed revision is unsupported.
- [ ] **Output coverage:** baseline/`PageValues` comparison, seven-slot CV table, OOF ROC overlay and probability histogram, four threshold references, selected-model single test results, four fixed-policy conversion scenarios, final all-data refit.
- [ ] **Mathematical consistency:** cost threshold `2/3`, TP/FP/FN/TN definitions, revenue equations and all scenario assumptions agree across code, figures and prose.
- [ ] **Readability:** notebook follows DSA211 lab-style code → output → concise statistical interpretation; clear titles, labels, tables and no redundant large outputs or placeholders.
- [ ] **Reproducibility:** run top-to-bottom cleanly; convergence/numerical errors are investigated; classification totals and train/test counts reconcile; deterministic seed and fold definitions documented.
- [ ] **Claims and provenance:** report actual current results only, disclose historical test exposure and model/feature limitations, and avoid causal or deployment claims.
- [ ] **Governance:** preserve Git history; technical plan separately approved; reconcile `AGENTS.md` and other repository guidance to the approved PRD rather than allowing old material to redefine the scope.

### 12. Remaining conditional decisions and implementation boundary

**The research design is complete.** The following are **execution decisions**, not permission to broaden the project:
- Determine the specific three revised-model feature treatments **from supplementary training EDA**, including whether Mixed NB is worthwhile; record negative findings and any absence of a justified revision.
- Specify exact pipeline steps, categorical ordering/unknown-level behaviour, Bernoulli binary conversion, solver/convergence checks and file-level implementation details in the **technical plan**.
- Choose only the most informative final plots, preserving each required analytical purpose and evidence.

**No further user-facing scope decision is required solely to prepare this PRD.** The user must still explicitly approve this final PRD and then approve the separate technical implementation plan before code changes.

---

**Primary sources used for project constraints:** DSA211 Labs 1, 5, 6, 7; DSA211 Lectures 5–8 where relevant; instructor project-specific `project_cv_workflow.html` (1 October 2026); the group's prior working project brief and agreed decisions Q1–Q27. The professor's requirements take precedence over this document wherever there is a genuine conflict.
