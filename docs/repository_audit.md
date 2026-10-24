# Repository and requirements audit — 25 October 2026

## Authority and provenance

Sol read the complete approved PRD v1.0 on `revise-three-model-scope`, commit `8cbeeb085be1c6b322f7a7dca8885dd7c5cbe536`. The initially mounted `work` branch was older (`921cf3a`); the implementation branch `implement-approved-prd` starts at the specified current source branch, preserving that history. Working tree was clean before branching. The PRD is unchanged. Its SHA-256 is `5b92dd103a386bf494e56e247cd8cee23f24bd57e1aa58121730843c3e0c420d`.

The owner's attached autonomous-implementation instruction explicitly delegates technical-plan approval to an independent Sol review. This supplies the PRD's separate plan gate without another manual approval. It does not change the approved analytical requirements. Mandatory independently confirmed instructor instructions remain superior.

## Available evidence

- Read `AGENTS.md`, README, all six existing supporting documents, requirements and the GitHub notebook execution workflow.
- Inspected all 45 source cells of the executed active notebook and the archive inventory. Existing notebook has 21 code cells, 20 designs, three classifier baselines, a 75/25 split and revenue-optimised 0.80 threshold: these are historical results, not acceptable implementations of the new PRD.
- Read extracted text of the archived two-page working proposal. Its live-sales-support objective, QDA, repeated CV, 5:1 costs and extension sweeps conflict with the expressly revisable proposal's successor PRD; they are not separately authenticated professor mandates.
- Dataset `data/uci_468.csv` and historical archives are available. Record hashes before changes and verify unchanged at delivery. Do not use archived output to choose new models.
- Labs 1, 5, 6, 7, Lectures 5–8 and `project_cv_workflow.html` are referenced in the PRD but their original files are absent from the available repository/attachments. Therefore direct comparison against the original teaching materials cannot be claimed. Follow the course requirements explicitly consolidated in the approved PRD, disclose this verification limit, and inspect any originals that become available.
- Existing `.venv` supplies Python 3.12.14, scikit-learn 1.9.1, pandas 3.0.6, NumPy 2.5.4, nbformat 5.11.1, nbclient 0.11.0, nbconvert 7.17.2 and statsmodels 0.15.0. System Python differs; use `.venv/bin/python`. Preserve the existing CI workflow.

## Retain, correct, replace

Retain the committed data, archives, history, seed 42, pipeline/CV pattern, warning capture, confusion-matrix conventions and honest limitations. Preserve the pre-revision active notebook separately before replacing it. Reuse only code whose new behaviour is inspected, rather than assuming existing outputs remain applicable.

Replace the active analysis sequence and specifications: quality before a new stratified 80/20 split; training-only supplementary EDA; four all-17 diagnostic fits; four minimally processed operational baselines; up to three evidence-supported family revisions; one seven-slot CV comparison; fixed 2/3 policy and four threshold references; four conversion sensitivities; single-winner test audit; exact all-data refit. Reconcile stale repository instructions and supporting prose. No new automated code-checking test suite is required by repository instructions; use visible numerical assertions, execution and independent manual inspection.

## Material risks and controls

1. Historical data exposure cannot be undone by resplitting. State this wherever calling the new holdout an audit; never claim pristine independence.
2. Unscaled unpenalised Logit may converge poorly or encounter rare-level separation. Use a documented unpenalised solver and numerical checks, recording warnings/failures. Do not silently regularise, scale or delete baseline inputs.
3. Gaussian NB on dummy columns and LDA on mixed data violate distributional idealisations; Bernoulli loses intensity and dependent dummies violate NB independence. Keep all four baselines eligible; do not privilege legacy alternatives.
4. Supplementary EDA can inform a small fixed revision set, not a model search. Inspect training only, freeze evidence and recipes before fitting the three revisions, and disclose adaptation optimism.
5. Numeric-coded nominal variables require encoding; `SpecialDay` remains numerical and `Weekend` remains 0/1. Learn categories inside folds; unknown categories must not crash validation.
6. Keep test outcomes inaccessible until winner and policy are frozen. Code review and training-stage corrections precede the one test audit; subsequent validation should inspect/reuse its saved predictions rather than evaluate other specifications.
7. Thresholds and q scenarios illustrate assumptions, not optimisation. Use exact 2/3 internally and 0.667 for display. All q scenarios hold recipients fixed; revenue is in common-A units, not profit or measured treatment effects.
