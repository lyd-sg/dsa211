# Approved methodology

The unchanged [PRD](PRD.md), [plan](technical_plan.md), [independent plan review](technical_plan_review.md) and [recipe review](recipe_review.md) define requirements and staged evidence gates.

## Data and preprocessing

Use the committed UCI 468 CSV. Verify 12,330 rows, 17 predictors plus binary target, types/missing markers, duplicates/description and class balance before splitting. Retain repeated rows; identical fields do not identify sessions or unique people. New stratified 80/20 split, seed 42: training 9,864 / test 2,466. Supplementary EDA reconstructs identical row IDs and immediately drops nontraining rows. All predictor EDA and recipe choices remain training-only. This holdout overlaps previous historical exposure and is not pristine.

Materialise five shuffled stratified training folds (seed 42) once. Candidate clones fit categories, mappings and any learned preprocessing only within each fit fold. Retain row/fold assignments, warning and numerical evidence; unknown categories have deterministic documented handling.

## Models and comparison

Four all-17 diagnostic and four 16-source operational baselines use unpenalised Logit, GaussianNB, BernoulliNB and standard LDA. PageValues is operationally excluded for possible timing leakage. Baselines retain raw numeric magnitudes and numeric SpecialDay; Bernoulli alone uses the required magnitude > 0 indicators. Weekend remains 0/1. Nominal fields use k−1 OHE for Logit/LDA and full k for NB. No optional baseline scaling, logs, penalty, weights or deletion.

Inspect Logit convergence, separation, rank and objective/prediction stability. Finite returned coefficients do not establish a finite MLE. Inspect LDA feasibility. Gaussian dummy marginals, dependence, Bernoulli intensity loss and mixed-data Gaussian assumptions are explicit limitations; correlation alone is permitted under LDA.

Supplementary training evidence supports one revision per family. Exact recipes are frozen in the plan addendum and independently reviewed before scoring; no grid/search. Compare seven operational slots. Highest mean fold ROC-AUC selects one, ties by label; report AP, sample SD, SE and per-fold evidence. OOF ROC overlay is illustrative; pooled AUC differs from mean fold AUC. One-SE proximity is descriptive; training-informed candidate selection can be optimistic.

## Policy and final evaluation

Winner OOF histogram and sensitivity/specificity plot inform threshold interpretation. Exactly four OOF references are training prevalence, 0.5, exact 2/3 and deterministic crossover. Report precision, confusion counts, voucher count/share and revenue at q = 0.50. Keep 2/3 primary independent of revenue. At 2/3, scenarios q = 0.10, 0.25, 0.50, 1.00 vary only assumed incremental conversion; discount 0.20, assignments and common A units stay fixed.

Freeze the winner and policy, refit on training and obtain one saved test probability vector. Report ROC/AUC/AP and confusion/rates at 2/3; the voucher illustration reuses those predictions. Clone the exact specification and refit all 12,330 rows after the audit; do not score again. Earlier held-out performance remains the reported audit.

## Verification limits

Execute notebooks and inspect source, actual results, figures and claims; independently recompute saved metrics/counts/revenue. No new automated code-checking suite; preserve the existing notebook-execution workflow. Final verification distinguishes completed checks from unavailable checks. Original labs/lectures and the professor's workflow file are absent; direct source comparison cannot be claimed. No treatment outcomes, customer identifiers, order values or margins support causal effects, profit or deployment claims.
