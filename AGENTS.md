# Active DSA211 guidance — PRD v3.5 presentation

**Current specification:** [PRD v3.5](PRD_v3.5.md).  
**Current review notebook:** [online_shoppers_prd_v3_5.ipynb](online_shoppers_prd_v3_5.ipynb).  
**Isolated branch:** `analysis/prd-v3-5-presentation`; do not merge without user review.

This phase is **presentation-only curation** of the successfully executed, independently verified v3.4 notebook; it is not a new modelling search. All earlier v3.0–v3.4 PRDs, notebooks, statistical results, original trial ledger and audits must remain unchanged.

## Visible original-family modelling shortlist

- **Logit (7):** L0, L1, L4, L7, L8, L13, L14. Retained model **L1**.
- **LDA (7):** D0, D1, D4, D9, D10, D11, D15. Retained model **D0**; its reason must be **"Baseline"**, not an EDA explanation.
- **GaussianNB (7):** G0, G1, G2, G3, G6, G7, G8. Retained model **G7**. G6 **also qualified** independently vs G0.
- **BernoulliNB (5):** B0–B4. Retained model **B3**, after B1 was accepted.
- **Trees:** four rows, full/pruned for Gini and Entropy; preserve their full paths in the original evidence.

Each visible family row must have the actual historical comparison parent, change tested, **EDA rationale (or baseline purpose)**, mean five-fold CV AUC, SE/AP and truthful historical acceptance outcome. The one-SE external selection rule and all previous anchor comparisons remain unchanged. No rejected trial becomes accepted simply because its AUC looks higher.

Keep a separate DSA211 methods-considered matrix including Lectures 8/9, distinguishing applied classification adaptations (backward selection, L2, LASSO, Elastic Net) from considered-but-not-fitted methods (e.g. best subset, forward stepwise, PCR/PLS overview). The classification target does not justify indiscriminate regression-only model fits.

## Frozen source/evidence

- **Original execution:** [v3.4 notebook](online_shoppers_prd_v3_4.ipynb).
- **Unmodified source ledger:** [41 trial rows](artifacts/prd_v3_4/all_attempts_ledger.csv); 51 scored designs; 255 five-fold results; 37 historical decisions.
- **Independent original audit:** [v3.4 PASS](artifacts/prd_v3_4/independent_training_audit.json).
- **Presentation audit:** [v3.5 PASS](artifacts/prd_v3_5/presentation_audit.json); validated 26 visible family rows, four tree rows, 25 compilable code cells, seven original figures and unchanged computational definitions, **without fitting any new model**.
- **Verification:** `python scripts/verify_prd_v3_5_presentation.py` (nbformat installed); GitHub workflow `.github/workflows/verify-prd-v3-5.yml`.

The v3.5 notebook embeds previously verified v3.4 numerical outputs for immediate inspection. Any *voluntary future* full notebook execution writes only to `artifacts/prd_v3_5/`, never to `artifacts/prd_v3_4/`. Do not automatically rerun models for presentation-only changes. Reserved observations have been repeatedly consulted in prior versions; do **not** describe them as pristine or make causal claims about the hypothetical upsell threshold.
