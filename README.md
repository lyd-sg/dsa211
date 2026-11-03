# DSA211 — Predicting Online Purchases (PRD v3.2 experimental extension)

**Active v3.2 specification:** [PRD v3.2](PRD_v3.2.md) · **New v3.2 notebook:** [online_shoppers_prd_v3_2.ipynb](online_shoppers_prd_v3_2.ipynb) · **Execution + acceptance workflow:** [build-prd-v3-2.yml](.github/workflows/build-prd-v3-2.yml) · **Implementation notes:** [implementation_v3_2.md](docs/implementation_v3_2.md).

**Status:** v3.2 source implemented; **new quantitative results are not accepted until the complete v3.2 execution and its independent audit pass**. The new notebook initially contains no execution outputs. Prior v3.1 results are historical only. This branch is separate from `main`; do not merge without reviewing the new evidence.

## What v3.2 adds

v3.2 retains the 20 original baseline/step attempts across four original pathways, **including every rejected trial**, and adds exactly **eleven** new EDA-driven candidates:

| Path | Added trials |
|---|---|
| Logistic Regression | L5 squared BounceRates; L6 Administrative positive indicator; L7 ProductRelated_Duration positive indicator |
| LDA | D5 `log1p(ProductRelated_Duration)`; D6 `log1p(Administrative_Duration)`; D7 categorical SpecialDay |
| Gaussian NB | G5 drop ExitRates; G6 drop ProductRelated_Duration; G7 `log1p(ProductRelated_Duration)`; G8 `log1p(Administrative_Duration)`; G9 remove six nominal sources |
| Bernoulli NB | No new trial; preserve B0–B4 and B3 as the pre-v3.2 finalist |
| Classification Trees | No new specifications; independently grow/prune both Gini and Entropy under unchanged v3.1 protocol |

New probes are **independent one-change alternatives applied to each frozen v3.1 family finalist**, not cumulative steps. This makes all eleven tests meaningful even where a proposed deletion conflicts with a proposed transformation. Each new challenger qualifies only if `mean CV AUC improvement > its own 5-fold AUC SE`. If several qualify within a family, the highest-scoring qualified one-change alternative becomes that family's v3.2 finalist. If none qualifies, the unchanged v3.1 incumbent remains.

Inventory: **31 original-family attempts** (20 historical + 11 new), plus six diagnostics / six operational baselines and two independently selected pruned trees. Expected audited model specifications: **41**, with **205** candidate/fold AUC/AP records; tree alpha paths are audited separately.

## Statistical question and validation protocol

Predict `Revenue=1` from browsing-session characteristics, choose the best of six taught finalist specifications by **mean five-fold training CV ROC-AUC** (AP as minority-class context), then evaluate the frozen winner's score distributions, ROC/PR, four threshold references and the hypothetical S$3/S$12 cost scenario. Preserve the same 12,330-row source dataset, original 80/20 seed-42 split, five shared stratified training folds, fold-contained preprocessing, PageValues exclusion from all operational contenders, Gini/Entropy pruning and 1-SE simplicity rule.

**Exploratory caveat:** v3.2 changes were proposed after examining v3.1's training CV results. The historical 20% reserved partition has already been accessed by earlier project versions, so no v3.2 held-out result can be described as newly pristine. Repeated CV selection also risks optimistic training estimates. Neither AUC nor the cost-cutoff illustration establishes causal upsell effects or deployability.

## Execute and verify

Use Python 3.12 and `requirements.txt`. The GitHub Actions [v3.2 workflow](.github/workflows/build-prd-v3-2.yml) is the standard consolidated validation:

```bash
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  jupyter nbconvert --to notebook --execute online_shoppers_prd_v3_2.ipynb \
  --ExecutePreprocessor.timeout=7200 --output online_shoppers_prd_v3_2_executed.ipynb
```

When the workflow passes, it commits the executed v3.2 notebook and isolated `artifacts/prd_v3_2/` evidence. A clean run must verify all 11 predeclared proposals, 31-entry ledger, 41 CV specifications, 205 fold-level scores, 27 one-SE decisions (16 original + 11 added), both independent pruning paths, six direct finalists, threshold confusion counts, finite model results, one version-specific held-out check, and historical-file preservation.

## Preserved v3.1 and earlier results

The original [v3.1 notebook](online_shoppers_prd_v3_1.ipynb), [v3.1 requirements](PRD_v3.1.md), [v3.1 implementation notes](docs/implementation_v3_1.md) and [v3.1 evidence](artifacts/prd_v3_1/) remain untouched. Their verified run [41595364066](https://github.com/lyd-sg/dsa211/actions/runs/41595364066) selected **L1 Logistic Regression** (mean five-fold ROC-AUC 0.757467; AP 0.336226); the version-specific previously used reserved-set check reported ROC-AUC 0.740543 and AP 0.327199. Gini and Entropy selected tree AUCs were 0.733055 and 0.744143, respectively. **These are v3.1 values, not v3.2 findings.**

Original [v3.0 notebook](online_shoppers_prd_v3.ipynb), [v3.0 artefacts](artifacts/prd_v3/), [v3.0 technical plan](docs/technical_plan_v3.md), historical notebooks and `data/uci_468.csv` remain available for reproducibility.

Slides for the 20-minute class presentation remain a separate deliverable.
