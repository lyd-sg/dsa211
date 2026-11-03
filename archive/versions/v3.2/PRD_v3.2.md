# DSA211 — Predicting Online Purchases
## Product Requirements Document (PRD) v3.2

**Date:** 3 November 2026  
**Status:** Approved development scope; **implementation and numerical results require separate executed verification**.  
**Branch:** `analysis/prd-v3-2-notebook`  
**Supersedes as active specification:** [PRD v3.1](PRD_v3.1.md). Preserve all historical notebooks, results, archives, and the v3.1 PRD unchanged.

## 1. Objective and change control

**Research question:** How effectively do browsing-session characteristics predict whether a session ends with `Revenue=1`, and which taught-classifier specification achieves the highest mean five-fold **training** ROC-AUC?

Prediction only, not coefficient inference, causal treatment effect, business uplift or deployment. Use the original six competing specifications: Logistic Regression, LDA, Gaussian NB, Bernoulli NB, independently pruned Gini tree and independently pruned Entropy tree. Deliver an executable new `online_shoppers_prd_v3_2.ipynb`, versioned evidence under `artifacts/prd_v3_2/`, a reproducible audit and 20-minute presentation slides separately.

**Requested extension:** Retain all 20 L0–L4, D0–D4, G0–G4 and B0–B4 existing historical attempts **including rejected candidates** and evaluate **all 11 additional proposed EDA-motivated specifications** L5–L7, D5–D7 and G5–G9. Do not delete historical failures, overwrite v3.1 evidence, silently choose only promising new candidates or lower the acceptance criterion after results.

These 11 proposals are **exploratory v3.2 extensions** prompted by review of v3.1 training/validation results. They are not the professor's original 3–5-step requirement, which is satisfied by the historical four pathways and is preserved as the original sequence. Disclose the expanded search and selection optimism; do not describe the 31-candidate inventory as professor-prescribed.

## 2. Data, splitting, processing and honest validation

- Use original UCI online shopper source `data/uci_468.csv`: 12,330 session rows, 17 predictors, binary `Revenue`; retain 125 excess exact duplicate full rows and acknowledge possible fold dependence. Prediction unit is a session, not an identifiable customer.
- Stratified 80/20 train/reserved split with seed 42 (9,864 training / 2,466 reserved); all modelling EDA and CV selection use training only. Five *shared*, shuffled, stratified training CV folds, seed 42. All per-fold levels, medians, scalers, groupings and model parameters fitted within each training fold.
- All operational candidates use the **same original 16 available-source candidates excluding PageValues**, unless a named trial explicitly deletes a feature or source group. `PageValues` remains in separate **six all-17 timing diagnostics only**; its association is not proof of leakage or availability at decision time. Every other session-aggregate predictor has an unresolved live-availability caveat.
- Treat six nominal sources (Month, OperatingSystems, Browser, Region, TrafficType, VisitorType) as categories rather than ordered integer measurements. Bernoulli NB uses binary inputs; GNB remains the taught Gaussian likelihood on encoded features and bears the usual independence/shape caveats.
- Prior versions have already inspected these same reserved rows; therefore even a single v3.2 held-out check is **not a pristine independent validation across project history**. Do not use v3.1 holdout outcomes to select v3.2 candidates. No further changes after v3.2's frozen training selection that rely on its holdout.

## 3. Evidence and motivating hypotheses (training-only, not guarantees)

Retain the main and [supplementary](supplementary/training_eda.ipynb) EDA as the supporting observational record. These are hypotheses to **try**, not assertions of forecast gains.

| Hypothesis | Training EDA evidence | Interpretation limit |
|---|---|---|
| H1: Logit may need curvature in BounceRates | Marginal binned buyer rate falls to <1% at high bounce values, with nonmonotonic behaviour near zero | Marginal curves do not establish conditional curvature |
| H2: Activity onset may convey incremental information | Administrative buyer rate 8.7% at zero vs 21.4% positive; ProductRelated_Duration 1.3% vs 16.4% | Contrast can be redundant with continuous magnitudes/other activity |
| H3: LDA blanket transformation may be too broad | Duration skew 5.68 for Administrative_Duration and 8.01 for ProductRelated_Duration | Transforming one variable does not prove joint class-normality |
| H4: NB feature deletion might retain wrong member of highly correlated pair | Within-class BounceRates/ExitRates correlations 0.915 and 0.723; ProductRelated/count-duration 0.839 and 0.896 | Correlation is not proof of predictive redundancy |
| H5: Targeting only skewed duration variables might work better for GNB | Zero fractions and skew vary markedly across activity columns; G1 blanket log1p worsened some folds | Log1p does not eliminate zero mass or make nominal indicators Gaussian |
| H6: BNB intensity rather than presence matters | ProductRelated and ExitRates virtually always positive; B1/B3 accepted | Existing BNB results support keeping this family unchanged |

Categorical SpecialDay is an exploratory response to nonmonotone marginal buyer rates (e.g. zero 16.6% versus positive 5.9%), not a verified conditional relationship. Rare Browser/TrafficType pooling and LDA shrinkage failures remain in historical evidence.

## 4. Baselines and historical sequential development (immutable in interpretation)

Maintain the original all-17 noncompeting family diagnostics and the six all-16 operational baselines. Original four historical development pathways:

| Path | Baseline | Steps retained as attempted, including failures |
|---|---|---|
| Logit | L0 unpenalised, six nominal sources encoded | L1 log1p six activity variables; L2 add Informational/Informational_Duration presence; L3 rare-level pooling; L4 scaled L2 Logit with inner-CV C |
| LDA | D0 shared-covariance LDA | D1 log1p six activity variables; D2 SpecialDay positive indicator; D3 rare pooling; D4 shrinkage with inner-CV tuning |
| Gaussian NB | G0 raw Gaussian marginals with encoded nominal indicators | G1 log1p six activity variables; G2 drop BounceRates; G3 drop ProductRelated; G4 drop SpecialDay |
| Bernoulli NB | B0 presence-style numerical binarisation | B1 ProductRelated training-fold median; B2 ProductRelated_Duration median; B3 ExitRates median; B4 drop BounceRates |

In the historical phase, each challenger is applied to the **last retained** family specification and accepted only if its mean five-fold AUC improvement is **strictly greater than its own fold AUC SE** (sample SD divided by sqrt(5)); otherwise revert. L4/C grid is {0.05,0.2,1,5,20} and D4 shrinkage grid {0,.1,.3,.6,.9}, each with 3-fold inner training CV; preserve these exact details.

## 5. Eleven newly requested, separately interpretable single-change probes

Freeze each family’s **v3.1 retained finalist** as its anchor for the new v3.2 probe set (L1 Logit, D0 LDA, G0 GNB; B3 BNB unchanged). **Every new candidate starts from that frozen anchor, not the prior new candidate.** This is intentional: G6 deletes ProductRelated_Duration whereas G7 transforms it; a cumulative path would make G7 a no-op if G6 were accepted. The new experiments are independent, one-change alternatives, and must not be described as a cumulative sequential path.

| ID | Anchor | One new change | Rationale |
|---|---|---|---|
| **L5** | L1 Logit | Add `BounceRates²`, retaining the original linear term | Test conditional curvature |
| **L6** | L1 Logit | Add `1[Administrative>0]` while retaining magnitude | Distinguish activity onset from intensity |
| **L7** | L1 Logit | Add `1[ProductRelated_Duration>0]`, retaining magnitude | Test product-engagement onset |
| **D5** | D0 LDA | Apply `log1p` **only** to ProductRelated_Duration | Target long duration tail |
| **D6** | D0 LDA | Apply `log1p` **only** to Administrative_Duration | Target long duration tail |
| **D7** | D0 LDA | Encode SpecialDay as categorical one-hot (k−1 dummies), not numeric | Avoid imposing numeric linear progression across nonmonotone categories |
| **G5** | G0 Gaussian NB | Drop ExitRates, retain BounceRates | Alternative correlated-feature retention |
| **G6** | G0 Gaussian NB | Drop ProductRelated_Duration, retain ProductRelated | Alternative count/duration retention |
| **G7** | G0 Gaussian NB | Apply `log1p` only to ProductRelated_Duration | Target duration asymmetry without blanket changes |
| **G8** | G0 Gaussian NB | Apply `log1p` only to Administrative_Duration | Target duration asymmetry |
| **G9** | G0 Gaussian NB | Drop **all six nominal source predictors**; retain numerical inputs including Weekend | Test the information/assumption tradeoff of removing Gaussian likelihoods for binary category indicators |

`log1p` is a deterministic, fold-safe transformation; presence indicators use strict >0. All categorical encoding in D7 is fold-fitted with unknown-level handling. No other new transformations or hidden grids are permitted. G9 counts as one predeclared group-deletion experiment, although it changes six source columns. Do not call dropping variables “fulfilling normality”; all hypotheses remain empirical.

### v3.2 probe qualification and family selection

1. Evaluate all eleven candidates on the five existing training CV folds, with the same ROC-AUC/AP/SD/SE reporting. Save their exact anchor, one change, five fold scores, gain, qualification outcome and warnings.
2. For each probe `m`, `gain(m) = meanCV_AUC(m) − meanCV_AUC(v3.1 anchor)`. **Qualifies iff `gain(m) > SD(AUC_m)/sqrt(5)`**. The strict > is unchanged.
3. If none qualifies, retain that pathway’s unchanged v3.1 finalist. If more than one qualifies, choose the *highest mean training CV AUC* among the qualifying **independent one-change** probes, breaking exact ties lexically by ID. Do not compose accepted proposals together or conduct a post-hoc second-stage search.
4. Separate the historical sequential-phase ledger from the new anchored-probe register while retaining a single complete ledger of **31 entries**: 20 previous (including four baselines) + 11 new; **27 nonbaseline decisions**. Clarify that “qualifies” in the new register means passes one-SE against anchor, while “selected” means the best qualified family finalist.
5. The original model family finalist and model selection are not chosen by holdout, financial cutoff, AP alone, or by retrospective use of original failed alternatives.

**Caveat:** Using v3.1 CV results to propose these 11 changes makes v3.2 selection exploratory. The repeated folds and 1-SE heuristic do **not** constitute a formal significance test or eliminate winner’s optimism.

## 6. Classification-tree pathway — preserve v3.1

Grow full-grown, unpruned Gini and Entropy trees independently using their 16 original source predictors and fixed settings `random_state=42`, `min_samples_leaf=1`, `min_samples_split=2`, `max_depth=None`, `class_weight=None`, `ccp_alpha=0`. No standardisation or manual binarisation. Encode nominal features within each training fold. Also retain separate all-17 full-grown tree diagnostics with PageValues for timing assessment only.

For each tree criterion use its own `cost_complexity_pruning_path` candidate alphas (0 included, terminal root-only alpha excluded); five shared folds, scoring `predict_proba(... )[:,1]` ROC-AUC. Determine the highest mean AUC, calculate `cutoff=best_mean−best_SE`, choose among eligible alphas the **fewest full-training terminal leaves**, break equal-leaf ties by higher CV AUC, then lower alpha. Gini and Entropy both enter six-way selection; do not preselect only one tree. Historical v3.1 alpha scores and selected values are descriptive provenance, not a replacement for version-specific execution.

## 7. Six-way final comparison, threshold analysis and refit

After family qualification, compare the **four updated family finalists plus both selected pruned trees** on mean five-fold training ROC-AUC, choose highest. AP, fold SD/SE, ROC and PR curves contextualise ranking but do not alter it.

Preserve the existing winner-only OOF probability displays, sensitivity/specificity crossover, prevalence and 0.50 references, and business-motivated 0.20 threshold. Upselling illustration assumptions: S$3 agent cost per contacted session, assumed 30% success conditional on a buyer, S$50 incremental gross margin; `C_FP=3, C_FN=12`, threshold `3/(3+12)=0.20`. Change q to 20%, 30%, 40% only as labelled assumptions, thresholds 0.30, 0.20, 0.15. These are not measured causal uplift or validated profit.

Freeze the selected pathway, fitted training recipe and threshold before any v3.2 reserved-set assessment; one version-specific holdout check only, labelled **historically reused and exploratory**. Fit the unchanged final recipe on all 12,330 rows only after the check; never claim all-data refit scores are out of sample.

## 8. Reproducibility and acceptance requirements

All of the following must pass before presenting v3.2 numbers as executed findings:

- Notebook format and cell syntax; complete execution with no error outputs; all fold-safe preprocessing and inner CV; no validation/holdout leakage.
- Exactly six all-17 diagnostics and six operational baselines; 31 historical+new logged attempts (20 historical, 11 newly evaluated). Verify every new ID, anchor and predeclared change; all **41** stored specification-level CV outputs and **205** fold-level results, including two selected trees, fully recomputed using their OOF scores.
- Verify the 27 nonbaseline accept/qualify decisions against the unchanged >1 challenger-SE rule; verify each new family selection against qualified one-change alternatives.
- Independently recompute both full tree pruning paths, the 1-SE eligible sets, selected leaf counts and six model finalists.
- Verify four threshold references and confusion counts, finite predictions and fitted parameters, all code/environment warnings, versioned `run_metadata.json`, and one version-specific reserved assessment.
- Keep original v3.0 and v3.1 notebooks, PRDs, source data, and saved evidence **unchanged**. All v3.2 generated evidence lives in `artifacts/prd_v3_2/`. Do not relabel prior outputs as v3.2.
- Log any failed run or limitations rather than manufacturing a successful acceptance report.

## 9. Scope exclusions and reporting caveats

No additional model families, arbitrary interaction search, QDA/KNN, threshold optimisation to maximise reported payoff, mixed Naive Bayes, feature importance presented as causal, cost or calibration claims unsupported by data, or automatic change in the precommitted acceptance rule.

Describe v3.2 as a **post-v3.1 exploratory extension**, not a clean preregistered study. Reusing training folds and previously inspected holdout limits independent performance claims. A professor-imposed 3–5-path specification guideline should be discussed explicitly in the report rather than falsely representing all 31 attempts as mandatory or comparable to a pre-specified four-step search.
