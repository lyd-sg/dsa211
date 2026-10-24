# Current project decisions

Approved [PRD v1.0](PRD.md) is authoritative and unchanged. The owner's autonomous instruction delegates separate technical-plan approval to independent Sol; [review](technical_plan_review.md) records staged PASS. Previous75/25, three-baseline, scaled/penalised and revenue-optimised.80 rules are superseded historical work.

Predict session-level Revenue; prediction is primary and hypothetical voucher arithmetic secondary. Quality checks precede a new stratified80/20 split, seed42 (9,864/2,466); retain all12,330 rows. Five common shuffled stratified training folds, seed42. Predictor EDA, recipes and threshold references use training only; previous overlapping-data exposure is disclosed.

Four all17 diagnostic fits and four operational baselines: unpenalised raw Logit, GaussianNB, BernoulliNB, standard LDA. All operational baselines use16 sources without PageValues, excluded for timing uncertainty rather than predictive association alone. Six nominal inputs are unranked indicators; SpecialDay remains numeric, Weekend0/1. Baseline model-required encodings follow PRD§6.2; no optional scaling, transforms, weights or penalty.

At most one EDA-supported revision per family, frozen after independent evidence review before scoring. All seven planned operational slots share folds and eligibility. Highest mean CV ROC-AUC wins, exact ties by label; AP and fold SD/SE support interpretation. One-SE proximity is descriptive, not equivalence or a model-selection test.

Buyer if p>=2/3→no voucher; otherwise voucher. Labels remain unchanged. Discount.20 and assumed q_ref=.50 give C_FN=.20A, C_FP=.40A and threshold2/3, conditional on meaningful probabilities. Four training references: exact prevalence,.5,2/3,rate crossover. Never substitute the most revenue-favourable threshold.

R0/A=TP+FN; Rq/A=TP+.8FN+.8qTN; delta/A=.8qTN−.2FN. At fixed2/3 recipients vary only q=.10,.25,.50,1.00. A is common normalisation; q is unobserved, not measured voucher response. This is neither profit nor actual lift.

Freeze the winner/specification/policy before one test prediction vector. Report ROC/AUC/AP and confusion/rates at2/3 without alternative test models or thresholds. Refit exact winner on all data after audit, with no further score. Saved audit predictions support numerical/presentation verification. Historical exposure, timing uncertainty, duplicates, selection optimism and distributional/probability limitations remain disclosed.
