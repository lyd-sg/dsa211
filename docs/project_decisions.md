# Current project decisions

Approved [PRD v1.0](PRD.md) is authoritative and unchanged. The owner's autonomous instruction delegates separate technical-plan approval to independent Sol; the [plan review](technical_plan_review.md) and [recipe review](recipe_review.md) record the staged approvals. Previous 75/25, three-baseline, scaled/penalised and revenue-optimised 0.80 rules are superseded historical work.

Predict session-level Revenue; prediction is primary and hypothetical voucher arithmetic secondary. Quality checks precede a new stratified 80/20 split, seed 42 (9,864/2,466); retain all 12,330 rows. Five common shuffled stratified training folds use seed 42. Predictor EDA, recipes and threshold references use training only; previous overlapping-data exposure is disclosed.

Four all-17 diagnostic fits and four operational baselines use unpenalised raw Logit, GaussianNB, BernoulliNB and standard LDA. All operational baselines use 16 sources without PageValues, excluded for timing uncertainty rather than predictive association alone. Six nominal inputs are unranked indicators; SpecialDay remains numeric and Weekend remains 0/1. Model-required encodings follow PRD §6.2; no optional baseline scaling, transforms, weights or penalty.

At most one EDA-supported revision per family is frozen after independent evidence review before scoring. All seven operational slots share folds and eligibility. Highest mean CV ROC-AUC wins, exact ties by label; AP and fold SD/SE support interpretation. One-SE proximity is descriptive, not a test of equivalence.

Buyer if `p >= 2/3` → no voucher; otherwise voucher. Labels remain unchanged. Discount 0.20 and assumed q_ref = 0.50 give C_FN = 0.20A, C_FP = 0.40A and threshold 2/3, conditional on meaningful probabilities. Four training references are exact prevalence, 0.5, 2/3 and rate crossover. Never substitute the most revenue-favourable threshold.

`R0/A = TP + FN`; `Rq/A = TP + 0.8 FN + 0.8 q TN`; `delta/A = 0.8 q TN - 0.2 FN`. At fixed 2/3 recipients, vary only q = 0.10, 0.25, 0.50, 1.00. A is a common normalisation; q is unobserved, not measured voucher response. This is neither profit nor actual lift.

Freeze the winner, specification and policy before one test prediction vector. Report ROC/AUC/AP and confusion/rates at 2/3 without alternative test models or thresholds. Refit the exact winner on all data after the audit, with no further score. Saved audit predictions support numerical and presentation verification. Historical exposure, timing uncertainty, duplicates, selection optimism and distributional/probability limitations remain disclosed.
