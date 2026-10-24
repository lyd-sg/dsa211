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

**Decision:** training evidence supports the three bounded recipes documented in the technical-plan addendum; negative evidence supports no category interaction/pooling. Independent recipe review remains the separate modelling gate. Existing data/archives/PRD unchanged.
