# Active DSA211 implementation guidance — PRD v3.4

Follow [PRD v3.4](PRD_v3.4.md) and [implementation notes](docs/implementation_v3_4.md). Work on `analysis/prd-v3-4-notebook` only; do **not** overwrite historical v3.0/v3.1/v3.2/v3.3 notebooks, PRDs, or their artefacts.

Prediction-only task with the unchanged UCI dataset, seed-42 9,864 training/2,466 historically reused reserved split, five shared stratified outer training CV folds, and 16 operational source predictors (PageValues excluded as a timing precaution, not established leakage).

**Keep all trials grouped by family in the notebook:**
1. Logit: L0–L10, plus L13 LASSO and L14 Elastic Net; standalone family history, chronological parent, effect, mean CV AUC/AP, fold SE, delta and retained verdict.
2. LDA: D0–D11, plus D15 nested grouped backward source elimination; its own complete history and selected-source stability table.
3. GaussianNB: G0–G9 including G7 retained; no new v3.4 tests.
4. BernoulliNB: B0–B4 including B3 retained; no new v3.4 tests.
5. Retain unchanged Gini/Entropy tree pruning and final six-way competition and business-threshold illustrations.

**New v3.4 experiments only:** L13 `LogisticRegression(penalty='l1', solver='saga')`; L14 `penalty='elasticnet', l1_ratio=.5`; both scaled inside the relevant fit fold with a frozen 6-point C grid and 3 inner folds; L14 sequentially compares to latest accepted Logit and replaces rather than stacks penalty. D15 backward LDA must select source-variable groups, group all nominal dummies, use 3-fold inner CV to build 16→1 source deletion path and choose fewest features within one SE of best; score entire procedure on five untouched outer validation folds.

**Preserve original acceptance rule:** challenger mean outer CV ROC-AUC gain against latest accepted family model must strictly exceed its own outer 5-fold SE. Earlier v3.2/v3.3 independent anchored trials retain their recorded comparison rules and labels. Do not tune thresholds or new candidate choices after seeing outcomes.

**Acceptance:** Require an executed notebook with no cell errors and independent numerical `PASS`: **41** original-family attempts (20+11+7+3), **51** scored designs, **255** fold results, **37** decisions, **80** nested D15 path records; four complete model-specific tables, both tree alpha audits and six-way model winner. Versioned evidence may only be created under `artifacts/prd_v3_4/`. The historical reserved set is **not pristine**.

Do not claim a new result before full execution, do not force an accepted LDA modification and do not merge without user review.
