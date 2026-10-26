# Final independent statistical and technical review

**Decision: PASS against approved PRD v1.0 — 25 October 2026.** No material unresolved implementation, statistical, numerical or reporting defect was found after the recorded corrections. The verification limits below remain explicit; this decision does not certify unavailable teaching sources, remote CI, real voucher effectiveness or deployment suitability.

## Reviewed deliverables and execution

| Artifact | Independently verified identity/evidence |
|---|---|
| Final main notebook | `online_shoppers_revised.ipynb`; SHA-256 `9e1eaa78c4b0c67867bc367e485023ccc58479234e85cabcd6a4c32aebb00794` |
| Approved executable code | SHA-256 `0e4f0f0dab80d2ac61a6a6e62ee0c0f6397c99e6f049b642632bcd6d19ca302e`; unchanged from the pre-execution static review |
| Raw official executed notebook | SHA-256 `12baf88b76d42bf3ea0e3fa925348cbd16fb0d5e95ec5cbcbc7e1b8bc8b66558`; 37 cells, 18 code cells executed sequentially 1–18, zero error outputs |
| Official execution record | nbconvert exit 0; 10:54:09–10:59:01 SGT on 25 October, elapsed 4m52s; eight embedded main figures |
| Separate supplementary notebook | SHA-256 `82988b7f6c3a4a02d5cfc65a7f181a3e1f8b31cbc67b478b0b3e984c110bfee9`; seven sequential code cells, zero errors, three figures; retained outside submission |

The reviewer inspected actual source and outputs, all eight main figures, the supplementary analysis, saved CV/test predictions, numerical/warning records, freeze/authorisation evidence, final-refit metadata and reconciled supporting documentation. The reviewer independently reconstructed metrics and arithmetic from saved vectors without fitting another model or producing another test prediction.

Every code-cell record, including source, outputs, execution count and execution metadata, is identical between the final main notebook and the raw official executed copy. Only two Markdown clarifications followed the audit: an explicit zero-buyer-detection interpretation and a caption identifying the Q–Q panels. No code, model, probability, threshold or numerical output changed. No further notebook execution was used for those clarifications.

## Individual PRD §11 acceptance decisions

| Acceptance criterion | Decision and inspected evidence |
|---|---|
| **Purpose-first A1–A14** | **PASS.** Every substantive block has a preceding purpose/question, actual evidence and defensible implication. A1 establishes data/imbalance; A2–A4 generate bounded hypotheses; A5–A8 distinguish diagnostics, baselines, revisions and selection; A9–A11 interpret probabilities/policy assumptions; A12–A14 report the one audit, final fit and limitations. Supplementary findings follow the same reasoning structure. |
| **Course alignment and workflow** | **PASS against requirements recorded in the approved PRD.** Four prescribed raw baselines and exactly three justified family revisions are implemented. Four all-17 fits remain diagnostic. The sequence is training CV → one winner → identical training refit → one saved test vector → exact all-data refit without another score. Original course-file comparison remains unperformed, as disclosed. |
| **Data discipline** | **PASS.** Quality checks precede splitting; all 12,330 rows and 125 excess duplicates remain. The seed-42 stratified split has 9,864/2,466 disjoint exhaustive original IDs. Predictor EDA/decisions use training only. Five common seed-42 shuffled stratified folds fit encoders/maps/presence eligibility within fit folds. Freeze and training-only numerical guards precede test reload. |
| **Transparent EDA-to-model logic** | **PASS.** Actual tail/zero-mass, category-support, SpecialDay and timing findings motivate the approved limited recipes before scoring. Sparse/nonmonotone counterevidence is retained; no arbitrary pooling, interaction sweep or AUC-driven replacement is introduced. Supplementary EDA extends the main summaries and remains separate. |
| **Required output coverage** | **PASS.** Four comparable all-17/operational results; seven-row AUC/SD/SE/AP comparison and fold evidence; OOF ROC overlay and winner histogram; four OOF threshold references and sensitivity/specificity plot; one test ROC/confusion audit; four constant-recipient q scenarios; visible final fitted pipeline and actual conclusions are present. |
| **Mathematical consistency** | **PASS.** Positive class, voucher direction, exact 2/3 cost derivation, confusion definitions and all revenue equations agree. Independent row-level reconstruction checks threshold/q totals. Neither model nor primary threshold is selected by simulated revenue; varying q does not change recipients. |
| **Readability** | **PASS.** All eight actual main figures and three supplementary figures were inspected. Labels identify variables, classes, rates and hypothetical units. The close Q–Q titles are disambiguated by an explicit panel caption. The notebook has no exercises/placeholders or broad coefficient-inference output. Zero sensitivity and nearly universal vouchers are interpreted plainly, not hidden behind ranking metrics. |
| **Reproducibility/numerical feasibility** | **PASS.** Official clean execution, deterministic IDs/folds, pinned local versions and actual warnings are recorded. All 15 CV Logit numerical checks and the full-training winner check pass unchanged tolerances. Final refit has finite parameters and no convergence warning. Saved metrics/counts reconcile independently. No new automated code-checking test suite was introduced. |
| **Claims and provenance** | **PASS.** Current numerical results match saved evidence; historical overlapping exposure, duplicates, selection optimism, probability/distributional assumptions, rare-level separation and timing uncertainty are disclosed. The work does not claim causal voucher effects, measured growth, profit, unique customers or operational readiness. |
| **Governance and preservation** | **PASS.** Separate plan, evidence-recipe, baseline, pre-test and static-code reviews preceded authorised work. The supervision record documents actual corrections. All 46 protected-file hashes independently match, including the unchanged PRD/data/old archives/workflow and byte-preserved prior active copy. Git history remains ancestral to the specified starting commit on the implementation branch. |

## Independent statistical and numerical evidence

The seven operational candidates supply **69,048 OOF records**, 9,864 unique training IDs each, and **35 same-fold comparisons**. The reviewer recomputed AUC from Mann–Whitney ranks and AP from grouped descending-score precision, including ties. All fold scores, means, sample SDs and SEs match fresh official-run artifacts within **1.11e−16** using round-trip CSV parsing.

**Revised Logit** is the highest mean-CV-AUC specification: **0.7576467609891068**, SD **0.01301645157689007**, SE **0.0058211341103521054**, mean AP **0.335012099515201**. The approximately .007627 AUC gain over raw Logit is descriptive after training-informed candidate formation; no significance or equivalence claim is justified. The declared highest-mean rule, exact-tie handling and descriptive one-SE comparison are correctly applied.

The four baseline encodings and all three revisions match the approved recipes. Revised Logit learns the two informational presence columns within each fit fold; no validation rows determine their eligibility. Mixed NB has eight Gaussian and eight categorical components. Independent checks cover all **40 categorical supports/count denominators** and **eight actual component examples**, including three unknown codes. Manual Gaussian log density plus one empirical prior and smoothed categorical likelihood reproduces OOF posteriors within **1.50e−15**. Unknown support is included in Laplace denominators and does not impose an artificial nominal ordering.

All **15 fresh CV Logit** comparisons pass the frozen same-likelihood IRLS/pseudoinverse criteria. Maximum absolute mean fit-NLL difference is approximately **2.18e−8**; maximum validation-probability difference is **3.21e−4**, below the unchanged 1e−6/1e−3 bounds. The winner's full-training refit also passes: **9.61e−10** and **1.51e−6**. These support finite-iterate numerical scoring at the stated precision. They do **not** certify finite or unique MLE coefficients: pure levels, separation and rank deficiency remain visible, and rejected numerical attempts are labelled separately. Baseline inputs were not silently scaled, penalised or deleted.

The reviewer independently reconstructs the training crossover **0.17961341093938224** and exact prevalence **0.15470397404703973**, plus all four threshold tables and fixed-recipient training scenarios. The exact 2/3 remains primary despite its poor operating characteristics.

## Sole held-out audit and final refit

The saved 2,466-row test vector has exactly the frozen held-out IDs and unchanged source outcomes. Independent rank/grouped-precision calculations give:

- **ROC-AUC 0.7412095145260323; AP 0.32679049302477653**, agreeing with notebook/library values to floating precision.
- **TN=2,082, FP=2, FN=382, TP=0** at exact 2/3.
- **Sensitivity 0, specificity 0.9990403071017274, precision 0**. Precision is defined because there are two predicted buyers, both false positives.
- **2,464/2,466 vouchers (99.9189%)**. No observed buyer is detected; the primary policy supplies almost no selectivity. This adverse finding remains unchanged and is explicitly interpreted in the final notebook.

At those same assignments, q=.10/.25/.50/1.00 gives hypothetical **Rq/A=472.16 / 722.00 / 1,138.40 / 1,971.20**, against **R0/A=382**. Direct recipient-level reconstruction agrees within **4.55e−13**. At q=.50 the assumed 832.8A nonbuyer contribution less 76.4A buyer discount loss gives 756.4A difference. These amounts follow assumed conversion; they do not demonstrate targeting effectiveness, actual revenue or profit.

The reviewed code contains one held-out pipeline probability call; all test metrics and q scenarios reuse that vector. Execution/freeze/authorisation evidence supports the documented once-only audit. The final object then clones the exact winner and fits **12,330 rows**, with encoded rank **68/69**, **27 iterations**, finite parameters and no convergence warning. No prediction or score follows that fit; earlier audit performance remains the reported evidence. The reviewer did not rerun the audit or refit to verify it.

## Documentation, preservation and limits

The final README, methodology/decisions/scope, result summary, artifact guide, supervision record and lead verification report were reconciled against the actual run. No material current-result contradiction remains. The approved PRD hash is `5b92dd103a386bf494e56e247cd8cee23f24bd57e1aa58121730843c3e0c420d`; dataset hash is `b3055ee355f59134d851d32641183cb4a8b45def7124d2f50442a042f358e0d9`. The prior active notebook copy matches its original hash `fe15cdefe2449245ca5a4ccbbaa09307050090fb5ae0b2d46dde7f9fcb448292`. All 46 final protected-manifest entries match actual file bytes. The original notebook-execution workflow is unchanged.

Checks **not performed**:

1. Direct comparison against original Labs 1/5/6/7, Lectures 5–8 and `project_cv_workflow.html`: the files were unavailable. Course verification uses the approved PRD's consolidated requirements.
2. Remote GitHub CI and a new clean-environment dependency installation: neither was run by this review or claimed as completed. Official execution used the supplied pinned Python 3.12 environment.
3. A second model fit/test execution: intentionally not performed for independent checking; saved vectors, actual source/output, logs and arithmetic were used instead.
4. Historically pristine validation, real voucher response, calibration certification or deployment feasibility: these cannot be established by the available retrospective data/protocol. Their limitations remain part of the accepted findings.

This PASS accepts the completed work and its honestly reported unfavourable threshold result. It does not turn the hypothetical policy into a recommendation for a real intervention.
