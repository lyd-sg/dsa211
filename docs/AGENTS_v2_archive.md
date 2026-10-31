# DSA211 repository implementation instructions — PRD v2.0

**Authoritative requirements:** [Approved PRD v2.0](docs/PRD_v2.md) → [current technical plan](docs/technical_plan.md) → implementation notes. The previous [AGENTS rules](docs/AGENTS_v1_archive.md), [PRD v1.0](docs/PRD.md) and older technical/review documents are historical.

## Non-negotiable current scope

- **Prediction only:** classify session `Revenue`; no voucher, business pricing, conversion probability, revenue/profit scenarios or cost-based threshold.
- Preserve the 12,330-row UCI dataset including duplicates. Data quality before split; stratified 80/20 seed 42 (9,864 / 2,466). Training-only EDA, five common shuffled stratified training folds seed 42 and fold-contained fitted preprocessing.
- Four original all-17 diagnostic fits. Operational models omit `PageValues` for uncertainty over availability at prediction time and use **16 original source predictors**.
- Four minimal baselines: unpenalised raw Logit, Gaussian NB, Bernoulli NB and standard LDA. Three exact EDA-informed revised candidates: L2 `C=1` log/presence-engineered Logit with fold standardisation; covariance-shrinkage `solver='lsqr', shrinkage='auto'` LDA; Gaussian/discrete Mixed NB with Laplace `alpha=1`.
- Seven operational candidates use identical folds. Winner = **highest mean five-fold ROC-AUC**; report mean AP, AUC fold SD and SE, one OOF ROC overlay, one selected-winner PR curve and one winner-score histogram. Small differences are descriptive, not superiority tests.
- Thresholds are **exactly three training OOF references:** prevalence, 0.5 and closest sensitivity–specificity crossover. One curve and one table showing threshold, sensitivity, specificity, precision. Crossover is balanced, not globally optimal.
- Refit the exact winner on training for numerical validity and all 12,330 rows for final recipe, without an independent held-out performance claim. Current notebook does not reuse historical test outcomes to claim new-version validation.
- Every substantive notebook section has **purpose → method/results → interpretation/implication**, with concrete figures and concise, nonduplicated presentation. Avoid large displayed warning or failure tables; keep detailed numerical records as artifacts.

## Verification and governance

Run the complete notebook with the actual UCI CSV; recompute fold AUC/AP and threshold confusion/rates from OOF evidence; check all source, saved artifacts, figures and printed claims. Preserve the source dataset, archived evidence, original PRD and existing Git history.

Record numerical warnings, category separation risks, convergence, parameter/probability validity and fold reproducibility without silently changing the modelling objective. No extra models or hyperparameter sweeps. All outputs for current scope must be free of legacy business-economics claims.

Work on a separate branch, open a reviewable pull request, never force-push or automatically merge. A successful run is necessary but not sufficient for declaring independent review or academic submission acceptance.
