# Supervision and implementation record

Dates use the owner's Asia/Singapore context (25 October 2026).

## Roles and authorization

The owner explicitly requested Sol supervision, a fresh independent Sol plan review and Luna coding at medium thinking. A separate Luna subagent uses the available `gpt-6-luna` model with `medium` reasoning. A second Sol reviewer has fresh context (`fork_turns=none`), independently reads the PRD, and does not rely on the lead's assurances. Lead Sol owns instructions, plan, integration, source/output inspection and final verification. No claim of review or execution is made before its evidence exists.

The owner's current instruction authorises independent PASS as the separate technical-plan approval gate and automatic continuation. Approved PRD v1.0 is preserved.

## Task 0 — repository preflight (complete)

**Sol instruction:** inspect code, environment and available teaching resources; do not change notebooks or run data/model experiments before plan approval. Identify reusable code and numerical risks. Acceptance: actual source inspection, explicit unavailable resources and package import evidence.

**Luna evidence:** `work/luna_preflight.md`; all 45 existing notebook cells inspected; `.venv` imports and versions recorded. No code/notebook changes or data/model experiments. Highlighted old split/threshold/regularisation scope and raw Logit/LDA/NB numerical risks.

**Sol verification:** independently inspected active notebook source in `work/existing_notebook.txt`, approved PRD, archive proposal, repository docs and workflow; ran independent package-signature/version checks. Confirmed initial mounted checkout was stale and fetched current specified branch before branching. No findings from old output used to choose new model. Existing dataset/archive/PRD/active hashes recorded in ignored `work/before_hashes.json`. PASS for preflight; analytical implementation remains gated by plan review.

## Task 1 — supplementary training EDA (Sol inspection complete)

**Sol instruction:** after independent plan PASS, implement and execute only the separate five-investigation EDA notebook; no model fitting/scoring. Verify quality before split, discard nontraining data, preserve IDs, purpose/evidence/implication for each investigation and actual findings for the exact-recipe gate.

**Luna evidence:** `supplementary/training_eda.ipynb`, seven code cells executed officially with repository `.venv` and Jupyter nbconvert; row/fold ID CSVs in `artifacts/`; descriptive handoff in `work/eda_findings.md`. Default sandbox blocked local kernel networking; explicit additional networking enabled normal nbconvert execution. A preliminary in-process execution was not treated as sufficient final notebook validation.

**Sol corrections and verification:** inspected actual source/outputs, all three chart images, and independently reconstructed train/test IDs and all five validation folds. Exact matches; 9,864/2,466 disjoint rows and one validation assignment per training row. Identified misleading rank-based quantile bins that split equal zeros by row order; Luna replaced with actual-value bins preserving ties and a single zero stratum, then re-executed. Required actual evidence-based implications, chronological month ordering and root-relative artifact paths. Independent reviewer identified a correlation/LDA overclaim; Luna corrected source and output to distinguish NB dependence, possible covariance heterogeneity and LDA Gaussian-tail concerns, then re-executed officially. Final seven execution counts are 1–7, no errors. No model fit, CV score or holdout predictor EDA occurred.

**Decision:** training evidence supports the three bounded recipes documented in the technical-plan addendum; negative evidence supports no category interaction/pooling. Independent recipe review subsequently granted PASS in `recipe_review.md` before modelling. Existing data/archives/PRD remained unchanged.

## Task 2A — four diagnostics and four operational baselines

**Sol instruction:** implement main A1–A6 and fold-contained sklearn pipelines only; execute four all-17 diagnostics and four operational baselines, with no revised candidate, winner, threshold or test code. Inspect raw unpenalised Logit, GaussianNB/full k OHE, BernoulliNB/required binary inputs/full k OHE and standard LDA/k−1 OHE. All 16 operational sources remain present.

**Inspection/corrections:** Sol inspected actual source before handoff and requested corrected warning-to-fold association, validation-transform warning capture, explicit unseen-level support, preprocessing failure capture, finite parameters including intercepts/priors, exact fit-fold logistic objective, pipeline cloneability and compact EDA/output. Main subgroup EDA was shortened so the supplementary notebook extends it rather than repeating it. The independent reviewer checked additional numerical-status and historical-exposure wording. Stale concurrent draft in-place runs were stopped; subsequent execution used an isolated output target.

**Numerical evidence and remedies:** a real `.venv`/nbconvert baseline execution completed, but its initial tolerance and strict numerical retry were not accepted as final evidence. Unscaled unpenalised Logit has pure nominal levels and rank-deficient designs; finite coefficients are not evidence of a finite MLE. Newton-Cholesky strict retries failed with singular-Hessian fallback, iteration limits and large objective/probability discrepancies. These failed numerical attempts are retained separately, never substituted into accepted scoring.

Before inspecting final comparison deltas, lead and independent Sol agreed absolute mean **fit-fold** logistic NLL difference ≤1e-6 per observation and maximum label-free validation-probability difference ≤1e-3, with finite quantities and explicit warning provenance. Sol caught a preliminary check using validation NLL and missing explicit pseudoinverse configuration; Luna replaced it with fit-fold NLL and `GLM(..., Binomial).fit(method='IRLS', wls_method='pinv', maxiter=200, tol=1e-10)`. The preliminary check is not final admission evidence.

The initial Newton-CG tolerance 1e-7 passed nine comparisons but failed one all-17 fold's probability criterion. Training-only diagnosis traced this to a pure TrafficType level's separating coefficient, not a fitted-design nullspace. A genuine cold-start tolerance 1e-8 passed that fold, then was applied uniformly across all ten baseline Logit fits without AUC-based choice. Both Sol agents independently inspected the actual scripts and gate table: mean fit-NLL differences 9.85e-9–2.18e-8 and maximum probability differences 3.25e-6–3.21e-4; every gate passes. IRLS references converge in 16–19 iterations and preserve their rank-deficiency warnings. Finite-iterate boundary predictions are accepted computationally; finite or unique MLE coefficients are not claimed.

**Independent arithmetic:** both Sol agents reconstructed fold AUC/AP from all eight saved OOF vectors. Using `float_precision='round_trip'` reproduces every fold metric exactly; default CSV parsing can perturb near-one GaussianNB ties and AP, so audit reads must preserve round-trip precision. Final integrated source and updated tolerance-1e-8 OOF artifacts remain subject to stage review before revised-model implementation. Final delivery still requires a fresh official full-notebook run; intermediate cached outputs are not described as final execution.
