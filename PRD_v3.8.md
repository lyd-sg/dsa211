# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.8 — Concise, evidence-led EDA presentation

**Status:** IMPLEMENTED — EDA AND PRESENTATION VERIFIED; MODEL RESULTS INHERITED UNCHANGED FROM VERIFIED v3.7  
**Date:** 8 November 2026  
**Scope:** EDA presentation and narrative restructuring only; no new modelling experiments.  
**Active presentation:** [v3.8 notebook](online_shoppers_prd_v3_8.ipynb). **Frozen numerical provenance:** [archived executed v3.7 notebook](archive/versions/v3.7/online_shoppers_prd_v3_7.ipynb), [archived v3.7 PRD](archive/versions/v3.7/PRD_v3.7.md), [v3.7 PASS audit](artifacts/prd_v3_7/v3_7_verification.json). v3.8 is the active presentation; its model results are inherited unchanged from v3.7.

### 1. Objective and non-negotiable boundaries

Produce an easier-to-follow notebook by eliminating redundant EDA outputs while preserving every distinct, relevant finding. The presentation must progress from **full-data overview → split → general training EDA → in-depth training EDA → model development**.

1. **EDA shows only the analysis performed and what the data reveal.** Do not introduce model specifications, transformations, CV results, predictions, or an EDA-to-experiment bridge in Sections 1–3. Explanations of how findings motivate particular experiments belong inside **Model Development**.
2. **Keep each result once.** Combine duplicate summaries, repeated histograms, replicated correlations, long intermediate tables and repeated commentary. Retain short interpretations, sample support where it affects reliability, and approved figures.
3. **No statistical redesign.** Preserve the fixed source data, duplicate-row retention, split, fold membership, preprocessing, all historical candidate configurations/IDs, sequential 1-SE decisions, inner tuning, trees, thresholds, finalist selection, saved performance and final refit. Do not silently modify or rerun model selection as part of presentation cleanup.
4. **Preserve v3.7.** Keep the original executed notebook, PRD and verification source in `archive/versions/v3.7/` and the retired workflow in `archive/workflows/`. Leave the original numerical evidence under `artifacts/prd_v3_7/` unchanged.
5. **Course-aligned and prediction-only.** No causal claims, unsupported significance claims, claims of verified predictor availability, or additional techniques unrelated to the already executed project.

### 2. Final notebook narrative and exact EDA requirements

#### Section 1 — Initial Data Overview (full dataset only)

**1.1 Dataset overview:** One compact table: 12,330 sessions; 17 predictors (10 numerical, 6 nominal categorical, 1 binary `Weekend`); binary outcome `Revenue`; 18 original source columns. No redundant explanatory paragraph or chart.

**1.2 Data quality:** One compact table: zero missing values, zero blank nominal entries, 125 excess identical full rows, 12,205 distinct full-record patterns. The 125 excess identical observations are all non-purchases. Include this agreed interpretation, or faithful shorter wording:

> The dataset contains 125 identical observations, already present in the original UCI data. As UCI specifies that sessions represent distinct users, these are treated as matching feature profiles rather than confirmed duplicate records. All observations are retained.

Precisely, “125 identical observations” refers to **125 excess repeated full rows**, not 125 distinct duplicate pairs. The UCI sampling description does not independently prove row identity; do not claim that record-level uniqueness was established.

**1.3 Target distribution:** One table: non-purchases 10,422 (84.53%), purchases 1,908 (15.47%), total 12,330; one concise finding that the outcome is imbalanced. No redundant class bar chart.

**1.4 Train–holdout split:** At the **end** of Section 1, show one short table: stratified 80/20 on `Revenue`, seed 42, 9,864 training and 2,466 reserved observations. State that detailed EDA from Section 2 onward uses training observations only. The reserved sample was historically inspected and is **not pristine**. **Do not explain five-fold CV here**; introduce CV with model development.

#### Section 2 — General EDA (training data only; n=9,864)

**2.1 Numerical distributions**
- One ten-row table with `Predictor | Median | % Zeros | Skewness` for all ten source numerical variables, including `PageValues` as an original **descriptive** source variable; excluding `PageValues` from operational modelling is a separate issue.
- Keep the numerical table only; the two redundant duration histograms have been removed for readability.
- Findings: (i) substantial right-skewness, especially duration variables; (ii) strong zero concentrations, particularly `SpecialDay`, informational measures and `PageValues`.
- Consolidate duplicate distribution tables/histograms from original notebook cells; no modelling discussion.

**2.2 Categorical distributions**
- One six-row table with `Predictor | Number of categories | Categories with n < 50`.
- Counts from the executed training EDA: `Month` 10/0; `OperatingSystems` 8/3; `Browser` 13/4; `Region` 9/0; `TrafficType` 20/9; `VisitorType` 3/0.
- Findings: `Browser` and `TrafficType` have 13 rare levels combined; very small cells yield unreliable observed purchase rates. Rare `OperatingSystems` levels also exist (3); do not falsely imply Browser and TrafficType are the only sparse variables.
- **Do not include a purchase-rate-range column.** The previously proposed `Month × VisitorType` investigation is removed, so do not keep a descriptive range merely to motivate a deleted analysis.
- Fold the evidence from the old standalone 42-row `Browser/TrafficType/Region` rare-category table into these findings; remove the large table.

#### Section 3 — In-depth EDA (training data only)

**3.1 Zero versus positive activity**
- Six-row table, one row per `ACTIVITY` variable, with `Predictor | Purchase rate (X=0) | Sessions with X = 0 (n) | Purchase rate (X>0) | Sessions with X > 0 (n)`. Show both rates and both group sizes (approved post-v3.8 review). The denominators come from the **9,864 training sessions**, not all 12,330 rows.
- Findings: positive activity is associated with higher observed buying rates for all six measures; the `ProductRelated=0` comparison is particularly uncertain because it contains only **27 sessions**.
- No causal or adjusted-effect language. Remove repeats of the same zero-versus-positive contrasts elsewhere.

**3.2 Positive activity intensity**
- Among **X>0 observations only**, calculate up to four quantile-based activity bins and their purchase rates and group sizes; show a six-row table:
  `Predictor | Bin 1 (lowest) | Bin 2 | Bin 3 | Bin 4 (highest)`.
- Every populated cell is **purchase rate (%) and sessions (n)**, e.g. `20.2% (n=1,234)`. Use ordered bin labels rather than claiming four exact 25%-sized intervals when tied values collapse boundaries. A dash signifies an absent bin, **not missing observations**.
- Add a compact, executable diagnostic immediately below the table for `Informational`: requested positive-only quartile values, actual `qcut` boundaries, observed minimum/maximum activity in each bin, sessions and purchase rates. Verify its three bins against the training data. This addresses the approved Section 3.2 review without changing any model.
- Findings: purchase rates climb strongly across `ProductRelated` count and duration intensity groups; administrative/informational trends are less uniformly increasing.
- Do not also show raw percentile-cutoff and positive-quantile ledgers. Preserve the tabulated values from executed training evidence, not guessed recalculations.

**3.3 BounceRates and purchase behaviour**
- One five-row table with `BounceRates range | Sessions (n) | Purchase rate`, rows exactly labelled **`0`, `0–25th percentile`, `25th–50th percentile`, `50th–75th percentile`, `75th–100th percentile`**.
- Percentiles refer to **positive** `BounceRates` observations. Approved rounded display based on the original eight positive-value bins combined into quartiles: zero **4,423 / 19.2%**; positive quartiles **1,361 / 23.4%**, **1,365 / 16.7%**, **1,355 / 8.0%**, **1,360 / 1.8%**. Reconcile the grouped-bin method against the source data before final output; do not fabricate alternative cutoffs.
- Findings: non-monotonic near zero; increasingly high bounce rates correspond to sharply lower observed purchase rates. No extra eight-bin empirical-logit ledger in the main EDA.

**3.4 Within-class predictor correlations**
- Use **exactly** this introductory sentence: **“Four predictor pairs were examined based on their conceptual relationships.”**
- One four-row table: `Pair | Conceptual relationship | Pearson r (Y=0) | Pearson r (Y=1)`; pairs and training estimates:
  - `BounceRates × ExitRates`: exit behaviour; **0.915 / 0.723**.
  - `ProductRelated × ProductRelated_Duration`: product page count and duration; **0.839 / 0.896**.
  - `Informational × Informational_Duration`: informational page count and duration; **0.632 / 0.634**.
  - `Administrative × Administrative_Duration`: administrative page count and duration; **0.586 / 0.589**.
- Findings: strong positive dependence for several pairs; correlation strengths can differ by outcome class. Do **not** conclude that differing individual correlations prove unequal full covariance matrices.
- Merge the two original correlation calculations and outputs into one.

**3.5 Distributional assumptions (Q–Q plots)**
- Keep **two normal Q–Q plots** for `ProductRelated_Duration` and `Informational_Duration`, each showing purchasers and non-purchasers separately.
- Findings: substantial departures from marginal normality in these duration measures, including within classes. Do not claim two Q–Q plots prove or disprove multivariate normality of the entire predictor vector.
- No extra table; this is distinct from whole-training-sample skewness in 2.1.

**3.6 SpecialDay and purchase behaviour**
- Keep the existing **line chart** of `SpecialDay` score against observed purchase rate, plotting **all six distinct scores** `0, 0.2, 0.4, 0.6, 0.8, 1.0` and annotating **each point's sample size**. Each point is the group purchase rate, not an individual session, and lines between scores are visual guides only.
- Findings: `SpecialDay=0` has **16.6%** purchase rate versus **5.9%** across positive scores collectively; positive scores have **non-monotonic** rates.
- Do not repeat the six-row level table, separate zero/positive table or numeric interpretation of all six values in text.

### 3. Explicit removals, consolidations and relocations

**Remove entirely from the new EDA presentation:**
- The standalone **`Month × VisitorType`** purchase-rate matrix, support matrix, line plot and sparse-cell table. It did **not** motivate a tested specification or necessary further analysis. Do not retain an elaborate justification of why an untested interaction was omitted.
- The standalone **`PageValues` versus `Revenue`** purchase-rate table (3.7% at zero vs 56.5% positive) and its commentary. It is not part of the operational specification evidence.
- The 17-row predictor timing/availability table.
- The standalone 42-level rare-category output (merge its distinct insight into 2.2).
- Duplicate skewness/zero-share summaries, repeated numerical histograms, duplicate correlations, raw multi-variable empirical-logit ledgers that repeat the approved zero/intensity/BounceRates findings, and repetitive narration.
- The standalone **EDA-to-experiment bridge** from EDA.

**Move into Model Development, once and only where relevant:**
- Short predictor timing line before operational baseline discussion: **“PageValues is excluded because its availability at the intended prediction time is uncertain; the remaining 16 predictors are assumed available.”** Do not imply the other 16 predictors' timing has been independently established.
- The **EDA-to-experiment rationale**, embedded concisely when introducing each experiment or its classifier family's specification pathway. Do not create a second large EDA summary/bridge that simply restates Sections 2–3.
- **Approved model-by-model rationale:** for each displayed L0–L6, D0–D6, G0–G6 and B0–B6 model, retain its accepted/not-retained label and write **one or two sentences** connecting a specific Section 2 or Section 3 finding (preferably with a relevant number) to the exact feature/estimation change and what it tests. Baselines may cite the common 16-predictor timing constraint. Respect the display-alias → historical-trial mapping, inherited cumulative incumbent configurations and frozen model results; EDA provides motivation, not proof of performance. Add an analogous short rationale for full-versus-pruned trees without reinstating a standalone EDA-to-model bridge.
- Introduce **five-fold stratified CV, within-fold preprocessing, model-selection logic and one-SE** at the beginning of Model Development, not in Section 1.
- Retain the six **All17** diagnostic baselines (which deliberately include `PageValues`) followed by six **Operational16** models (which do not). The exclusion and same-fold AUC comparison belong in Model Development.

**Code safety:** Original notebook EDA cells define aliases including `X`, `y` and `NUMERIC`; remove or rewrite cells only after checking that these bindings and all downstream model dependencies remain valid. Formatting cleanup must never silently change the fitting or evaluation pipeline.

### 4. Internal EDA-to-experiment traceability (implementation audit ONLY)

This mapping is **not** to be printed in EDA. IDs below are **original/canonical trial IDs**, **not** the v3.7 seven-per-family display aliases.

| EDA evidence | Relevant original experiment IDs |
|---|---|
| 2.1 skewness, 3.2 activity magnitude, 3.5 class-specific shape | L1, D1, G1, G7, G8; D9 for extreme duration |
| 2.1 zeros, 3.1 presence contrasts | L2, L6, L7, D10 |
| 2.2 rare nominal levels | L3, D3, B6 |
| 3.2 positive intensity | B1, B2; contextual support for L10 (duration per product page) |
| 3.3 nonlinear BounceRates pattern | L5, L8, D11 |
| 3.4 BounceRates/ExitRates and product-pair dependence | G2, G3, B4, B5; broader support for L4, L13, L14 and D4 |
| 3.6 SpecialDay levels/presence | D2, D7, L9, G4 |

An EDA finding **motivates testing** a specification; it does not demonstrate improved out-of-sample performance. Report trial scores and actual sequential acceptance in Model Development, and preserve all full-ledger trial IDs. Do not retrofit or invent an experiment solely to justify an EDA result.

### 5. Inherited model-development contract — unchanged

All requirements and PASS evidence from **PRD v3.7 Sections 2–4 and 6–11** remain binding **except where this PRD explicitly changes EDA layout/presentation**.

- Preserve the seed-42 **9,864/2,466** train/reserved split, the same five stratified outer folds and nested fit-only operations.
- Preserve **43 planned / 38 scored / 5 inapplicable** original-family ledger entries, **28 visible aliases** (seven scored models per family), **six finalists** (four classifier families plus two pruned trees), and the exact v3.7 sequential 1-SE rule.
- Preserve all historical trial configurations, genuine incumbent/challenger lineage, complexity definitions, one-SE decisions, tree alpha/pruning logic, AP/AUC results and hypothetically illustrated thresholds. Do not change which historical attempts are displayed.
- Preserve original v3.7 winner: canonical **L13 Logistic Regression** (displayed **L5**) with training mean CV ROC-AUC **0.75892**, AP **0.34236**, **unless a legitimate verification uncovers an existing inconsistency**. A presentation revision must not produce new model scores.
- Preserve the reserved-set caveat: historically consulted, **not** a fresh independent generalisation test. Preserve final refit's 16-source predictor set.
- Do not modify data, source hashes, deduplication policy, tree outputs, final training/refit recipe, threshold formulas, financial assumptions or model-selection criteria.
- Any v3.7 verification **heading-count** assertions and old requirements expecting restored `Month × VisitorType`, the long timing table or the bridge in EDA are superseded. Adapt version-specific checks rather than breaking correctness checks or leaving stale expectations.

### 6. Implementation and acceptance criteria

The implementation has been completed, with v3.8 EDA execution verified and inherited v3.7 model code/outputs checked unchanged; the following acceptance criteria remain applicable.

**Required verification before declaring PASS:**
1. Versioned notebook parses/executes without errors; all rendered EDA tables/figures contain training-only values after 1.4.
2. Section order is **1 Initial Data Overview → 2 General EDA → 3 In-depth EDA → Model Development**; no CV explanation before Model Development and no model-motivation commentary in EDA.
3. Section 1 retains approved duplicate-row explanation and fixed 80/20 stratified split; no deduplication or data changes.
4. Section 2 contains only the approved 10-row numerical table, six-row categorical summary and their findings; no category purchase-rate ranges or standalone rare-level table.
5. Section 3 contains exactly the six approved distinct analyses: zero/positive activity, positive-only intensity, BounceRates quartiles, four conceptual correlation pairs, two class-specific Q–Q plots and the annotated six-point SpecialDay chart. Definitions, rounding, sample supports and stated findings reconcile with the data.
6. `Month × VisitorType` standalone output, 17-row timing table, dedicated `PageValues` purchase-rate output, duplicated empirical-logit output and EDA-to-experiment bridge are absent from EDA. The operational-input timing assumption appears once in Model Development.
7. Every original model specification, actual fold, selected incumbent, family finalist, tree, six-way winner, training metric, reserved check and full-data refit is numerically unchanged from verified v3.7, with independent machine-readable PASS/FAIL results. Check no EDA cleanup removes variables required downstream.
8. Update the new version-specific verifier, documentation and README **only after the new notebook passes**. The historical v3.7 verifier is archived unchanged; it was written for the former root-level layout and is retained for provenance, not as the active v3.8 command. Preserve all historical numerical evidence.
9. Delivery includes an explicit before/after EDA inventory and concise change log, and states clearly whether checks passed. Do not print a giant internal traceability table in the notebook's EDA.

### 7. Completion boundary

**Implemented:** The new [v3.8 notebook](online_shoppers_prd_v3_8.ipynb) implements the approved EDA redesign. Pre-modelling cells were independently re-executed successfully, and model code and saved outputs were checked against the frozen v3.7 notebook. **Full end-to-end model retraining was not repeated**; v3.7's numerical audit remains authoritative. Changes to model performance, selection, code outside presentation dependencies, or additions of experiments require a separate explicit scope decision.


### 8. v3.8 implementation closeout (8 November 2026)

- **Notebook:** [online_shoppers_prd_v3_8.ipynb](online_shoppers_prd_v3_8.ipynb), created separately from untouched v3.7; **75 cells / 33 code cells**. Its three EDA illustrations are embedded in notebook outputs and can be regenerated by the code under non-interactive backends.
- **Verification:** [v3.8 workflow](.github/workflows/verify-prd-v3-8.yml) and [version-specific verifier](scripts/verify_prd_v3_8.py) returned **PASS** on [GitHub Actions run 42484250765](https://github.com/lyd-sg/dsa211/actions/runs/42484250765). Every pre-modelling code cell executed without errors using the fixed source dataset and training-row IDs. All post-EDA model code and saved outputs were compared with the verified v3.7 notebook and confirmed unchanged.
- **Results:** Original v3.7 model results, winner, thresholds, holdout caveats and final refit are inherited without numerical changes. The verification is **not** a claim that the full computational model-development section was retrained from scratch in v3.8.
- **Presentation removals:** Month × VisitorType analysis; standalone PageValues purchase-rate output; detailed 17-row predictor timing table; duplicate category, correlation, histogram, quantile and empirical-logit tables; EDA-to-experiment bridge. Relevant rationales remain with model-development explanations.
- **No change** to source data, train/holdout partition, five CV folds, 43-trial ledger, 28 curated experiment labels, six finalists or original model-selection logic.


### 9. v3.7 retirement and active-version housekeeping (8 November 2026)

v3.8 is the sole root-level notebook/PRD pair. The superseded v3.7 executed notebook, PRD and historical verifier are preserved without byte changes in [`archive/versions/v3.7/`](archive/versions/v3.7/README.md); its historical GitHub Actions definition is preserved in [`archive/workflows/`](archive/workflows/verify-prd-v3-7.yml). [Historical numerical evidence](artifacts/prd_v3_7/) stays at its existing location because the v3.8 notebook inherits its results. The [active verifier](scripts/verify_prd_v3_8.py) checks v3.8 against the archived v3.7 notebook. The archival [manifest](archive/versions/v3.7/RETIREMENT_MANIFEST.json) records original Git blob identifiers. This change does not refit or reselect models.
