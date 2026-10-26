# DSA211 repository instructions

Read complete approved `docs/PRD.md` first. Authority: mandatory authenticated instructor requirements → approved PRD → technical plan/current guidance → legacy work. Preserve the PRD unchanged. The owner's 25 October autonomous instruction authorises independent Sol PASS as separate technical-plan approval and automatic continuation; see `docs/technical_plan_review.md`. Exact recipes require the plan's staged evidence review. Prior scope does not override the PRD.

## Current analysis

Main: `online_shoppers_revised.ipynb`. Separate `supplementary/training_eda.ipynb` is retained but not submitted. Read README, project decisions, methodology, phase2_scope, plan and reviews before changing analysis.

- Predict session-level Revenue, not unique customers or causal effects. Retain all 12,330 observations including 125 excess exact duplicates; verify their description.
- Quality checks precede a new stratified 80/20 split (9,864/2,466), seed 42. Disclose historical overlapping 75/25 exposure. Predictor EDA and choices use training only. Five identical shuffled stratified folds use seed 42; learned preprocessing stays within folds.
- Four all-17 diagnostic fits; four operational baselines: unpenalised raw Logit, GaussianNB, BernoulliNB, standard LDA. Operational models omit PageValues for possible timing/availability leakage; association alone is not proof.
- Baselines use all 16 remaining sources without optional scaling, logs, penalties, weights, deletion or engineering. Numeric magnitudes and SpecialDay remain numeric except Bernoulli's required >0 conversion; Weekend remains 0/1. Six nominal columns use k−1 OHE for Logit/LDA, full k for NB.
- At most one EDA-justified revision per family; seven operational slots when all are supported. No automated model/feature/regularisation search. Mixed NB is a conditional extension with one prior. Record actual estimation warnings/failures; never silently alter a baseline model.
- Winner: highest mean training CV ROC-AUC, exact ties by label; report AP, sample SD/SE, fold evidence and OOF ROC overlay. State training adaptation and selection optimism.
- Primary threshold: exact 2/3. Exactly four training references: prevalence, 0.5, 2/3 and sensitivity–specificity crossover. No revenue-driven model or threshold optimisation.
- Buyer prediction → no voucher; nonbuyer → voucher; labels unchanged. Discount = 0.20, reference assumed q = 0.50. At fixed 2/3 recipients, vary only q = 0.10, 0.25, 0.50, 1.00. R0/A = TP+FN; Rq/A = TP+0.8FN+0.8qTN; delta/A = 0.8qTN−0.2FN.
- Freeze winner, specification and policy before one test probability vector; report one-winner audit at 2/3. Reuse saved predictions for checks, with no alternative test models/thresholds. Then refit the exact specification on 12,330 rows without another score.
- Every substantive A1–A14/supplementary analysis has purpose before evidence, concise actual interpretation and implication. Do not predetermine findings, improvement or winner.

## Preservation and review

Preserve `data/uci_468.csv`, existing archives and Git history. Archive the prior active notebook byte-for-byte. Work on a branch; no force push or merge. Scratch builders/logs belong in ignored `work/`.

Luna owns Python/notebook implementation at requested medium reasoning; Sol defines bounded tasks, inspects actual code/output, requests fixes and controls integration. A fresh reviewer verifies plan, exact recipes and final evidence. Record supervision in `docs/implementation_log.md`.

Use `.venv/bin/python` and the pinned working environment. Check Logit convergence, separation, objective/probability stability and rank; finite iterates do not certify finite MLE. Numerical solver remedies must preserve the unpenalised likelihood and source treatment, with attempts recorded; do not select numerical settings by AUC. Inspect NB likelihood/prior and LDA feasibility. No new automated code-checking suite: use notebook execution, visible numerical assertions and independent manual/numerical review. Preserve the existing GitHub execution workflow.

Disclose unavailable original teaching sources, historical exposure, repeated patterns, selection optimism, NB/LDA/probability assumptions and unresolved timing. No claims of actual voucher response, profit, actual lift or deployability.
