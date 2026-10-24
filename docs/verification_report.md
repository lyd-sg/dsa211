# DSA211 final verification report

Status: **IN PROGRESS — final acceptance not yet granted.** Date: 25 October 2026 (Asia/Singapore).

## Scope and approval evidence

The approved PRD v1.0 is unchanged. Work starts from `revise-three-model-scope` at `8cbeeb085be1c6b322f7a7dca8885dd7c5cbe536`, on `implement-approved-prd`. The owner's autonomous instruction authorises independent Sol review as the separate technical-plan gate. [Plan review](technical_plan_review.md) and [recipe review](recipe_review.md) record substantive PASS decisions and reviewed hashes before modelling. [Supervision log](implementation_log.md) records Luna implementation and Sol's actual inspection/correction loop.

## Acceptance criteria

| PRD §11 criterion | Current verification evidence | Final status |
|---|---|---|
| Purpose-first A1–A14 and supplementary reasoning | Supplementary five investigations inspected; main pending completion | Pending |
| Four baselines, conditional revisions, professor sequence | Plan and three recipes independently approved; actual models under inspection | Pending |
| Quality before split, training-only choices, common fold pipelines | Supplementary source and exact split/fold identities independently verified | Pending main |
| Actual EDA-to-model logic, supplementary separate | Executed supplementary evidence and recipe review independently verified; no AUC-driven recipe search | Passed for design/EDA |
| Required output coverage | Main CV, policy, audit and final-refit evidence pending | Pending |
| Cost/revenue mathematics and fixed policy | Plan equations independently checked; actual numerical tables pending | Pending |
| Lab-style readability and labels | Supplementary tables/three figures inspected; main pending | Pending |
| Reproducibility and numerical feasibility | Supplementary seven code cells executed officially, no errors; main numerical gate pending | Pending |
| Actual claims, historical exposure and limitations | Source limitations and policy assumptions documented; final results pending | Pending |
| History, unchanged PRD, separately approved plan, current guidance | Approval records, protected-file hashes and independent role separation inspected | Pending final hash check |

## Completed independent checks

- Source data SHA-256 is `b3055ee355f59134d851d32641183cb4a8b45def7124d2f50442a042f358e0d9`.
- PRD SHA-256 is `5b92dd103a386bf494e56e247cd8cee23f24bd57e1aa58121730843c3e0c420d`.
- Prior active notebook preserved byte-for-byte in `archive/online-shoppers/online_shoppers_pre_prd_v1.ipynb`, SHA-256 `fe15cdefe2449245ca5a4ccbbaa09307050090fb5ae0b2d46dde7f9fcb448292`.
- Full source has 12,330 rows / 18 fields; 125 excess exact duplicates, 12,205 unique full rows. Duplicates are retained and their low-activity, nonbuying description was reverified during quality checks.
- Independently reconstructed the split from the source: 9,864 training and 2,466 test row IDs, disjoint and exhaustive. Training has 1,526 buyers. No predictor-based choices used test rows.
- Independently reconstructed all five seed-42 validation-fold mappings on sorted training IDs. Sizes 1,973 / 1,973 / 1,973 / 1,973 / 1,972; each training row is validated once.
- Independently inspected supplementary source, actual outputs and all three images; verified numerical EDA evidence. Corrections to tie-splitting bins and an LDA/correlation interpretation were applied and officially re-executed before recipe approval.

## Execution and numerical review

Supplementary notebook: seven code cells executed in order with repository `.venv` and Jupyter nbconvert; no notebook error outputs. A preliminary custom in-process runner was not accepted as sufficient final execution evidence. Local kernel networking required explicit additional runtime networking; no user approval was required.

Main notebook: pending completed execution and estimator/convergence/stability review. No successful main execution or final statistical acceptance is claimed at this draft stage.

## Checks not performed and limitations

Original Labs 1, 5, 6, 7, Lectures 5–8 and `project_cv_workflow.html` were unavailable in the repository or attachments. Direct verification against those original files was **not performed**; reviews use the course constraints consolidated in the approved PRD. The archived working proposal is explicitly revisable context, not an authenticated contrary professor mandate.

Remote GitHub CI has not been claimed as run. The existing execution workflow is preserved; no new automated code-checking test suite is introduced. Local execution, source review and independent numerical reconstruction are separate evidence.

The new holdout overlaps historical data exposure and is not pristine independent confirmation. Training-informed recipes/model selection can be optimistic. Identical data patterns do not establish unique visitor identity. Distributional assumptions, rare-level separation and probability calibration need cautious interpretation. Remaining predictors are not certified available mid-session. Voucher response, counterfactuals, order values and margins are absent; q scenarios do not establish actual lift, profit or deployment feasibility.
