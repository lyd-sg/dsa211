# DSA211 repository instructions

Read complete approved `docs/PRD.md` first. Authority: mandatory authenticated instructor requirements → approved PRD → technical plan/current guidance → legacy work. Preserve PRD unchanged. The owner's 25 October autonomous instruction authorises independent Sol PASS as separate technical-plan approval and automatic continuation; see `docs/technical_plan_review.md`. Exact conditional recipes need the plan's staged evidence review. Prior scope does not override PRD.

## Current analysis

Main: `online_shoppers_revised.ipynb`. Separate `supplementary/training_eda.ipynb` is retained but not submitted. Read README, project decisions, methodology, phase2_scope, plan and review before changing analysis.

- Predict session-level Revenue, not unique customers or causal effects. Retain all12,330 observations including125 excess exact duplicates; verify duplicate description.
- Quality checks before a new stratified80/20 split (9,864/2,466), seed42. Disclose prior overlapping75/25 exposure. Predictor EDA and choices use training only. Five identical shuffled stratified folds, seed42; learned preprocessing within folds.
- Four all17 diagnostic fits; four operational baselines: unpenalised raw Logit, GaussianNB, BernoulliNB, standard LDA. Operational models omit PageValues for possible timing/availability leakage; association alone is not proof.
- Baselines use all16 remaining sources, without optional scaling, logs, penalties, weights, deletion or engineering. Numeric magnitudes and SpecialDay remain numeric except Bernoulli required >0 conversion; Weekend remains0/1. Six nominal columns: k−1 OHE for Logit/LDA, full k for NB.
- One EDA-justified revision per family at most; seven operational slots when all supported. No automated feature/model/regularisation search. Mixed NB is conditional extension with one prior. Record genuine estimation warnings/failures; never silently alter baseline model.
- Winner: highest mean training CV ROC-AUC, exact ties by label; AP, sample SD/SE, fold results and OOF ROC overlay reported. State training adaptation/selection optimism.
- Primary threshold exact2/3. Exactly four training references: prevalence, .5,2/3,sensitivity–specificity crossover. No revenue-driven model or threshold optimisation.
- Buyer prediction→no voucher; nonbuyer→voucher; observed labels unchanged. Discount=.20, reference assumed q=.50. At2/3 fixed recipients, vary only q=.10,.25,.50,1.00. R0/A=TP+FN; Rq/A=TP+.8FN+.8qTN; delta/A=.8qTN−.2FN.
- Freeze winner/specification/policy before one test probability vector; report one-winner audit at2/3. Reuse saved predictions for verification, no alternative test models/thresholds. Then refit exact specification on12,330 rows without another score.
- Every substantive A1–A14/supplementary analysis has purpose before evidence, concise actual interpretation and implication. Do not predetermine findings, improvement or winner.

## Preservation and review

Preserve data/uci_468.csv, existing archives and Git history. Archive prior active notebook byte-for-byte. Work on a branch; no force push/merge. Scratch builders/logs in ignored work/.

Luna owns Python/notebook implementation at requested medium reasoning; Sol defines bounded tasks, independently inspects actual code/output, requests fixes and controls integration. Fresh reviewer verifies plan, exact recipes and final evidence. Record supervision in docs/implementation_log.md.

Use .venv/bin/python. Check Logit convergence, separation, objective/prediction stability and rank; finite iterates do not certify finite MLE. Inspect NB likelihood/prior and LDA feasibility. No new automated code-checking suite: notebook execution, visible numerical assertions and independent manual/numerical review. Preserve existing GitHub notebook execution workflow.

Disclose unavailable original teaching sources, historical exposure, repeated patterns, selection optimism, NB/LDA/probability assumptions and unresolved timing. No claims of actual voucher response, profit, actual lift or deployability.
