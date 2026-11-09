# DSA211 implementation handoff — active v3.8

**Active analysis:** [v3.8 notebook](online_shoppers_prd_v3_8.ipynb) and [PRD v3.8](PRD_v3.8.md). **Current verifier:** `python scripts/verify_prd_v3_8.py --run-eda` and [active workflow](.github/workflows/verify-prd-v3-8.yml). v3.8's pre-modelling cells were executed and all inherited modelling source/output checked; **a new full model retrain was not performed**.

**Frozen numerical provenance:** [archived executed v3.7 notebook](archive/versions/v3.7/online_shoppers_prd_v3_7.ipynb), [v3.7 requirements](archive/versions/v3.7/PRD_v3.7.md), [v3.7 PASS audit](artifacts/prd_v3_7/v3_7_verification.json). The [historical verifier](archive/versions/v3.7/run_verify_prd_v3_7.py) and [retired workflow](archive/workflows/verify-prd-v3-7.yml) are preserved **unchanged**; their original root-layout path assumptions do not make them current tools. Do not recreate root-level v3.7 duplicates.

## Scope and invariants

- Do **not** rebuild from scratch, add new classifiers, reselect models, or rerun the historically consulted reserved set. Preserve the 12,330-row original data, 125 excess identical full rows, seed-42 stratified **9,864/2,466** split, five shared outer folds, nested fold-safe fitting, 43 original trials, all selection decisions, trees, thresholds and final refit.
- `PageValues` remains included in the **All17 diagnostic baselines** but excluded from all **Operational16** specifications due to uncertain prediction-time availability. Other 16 input features are assumed available, not independently verified. The reserved set is not a pristine independent generalisation check.
- Never modify historical `artifacts/prd_v3_7/` (or prior versions), and do not change archived Git blobs. The active v3.8 verifier compares code and saved outputs to the archived v3.7 notebook.

## Approved v3.8 EDA narrative

1. **Initial Data Overview (full dataset):** Dataset structure, missingness/duplicates, outcome class balance; stratified split last.
2. **General EDA (training only):** Ten-row numerical table without histograms; six-row categorical summary and merged rare-level findings.
3. **In-depth EDA (training only):** Zero/positive activity **with n for both groups**; positive-only activity ordered quantile bins **with n per bin and an Informational collapsed-bin audit**; BounceRates (zero + four positive percentiles); four conceptually selected correlations; two class-conditional normal Q–Q plots; annotated six-point SpecialDay chart. Sample sizes in Sections 3.1–3.2 refer to **9,864 training observations**.
4. **Model Development:** Cross-validation and trial-specific motivations, results, acceptance decisions and final comparison.

Do not reinsert Month × VisitorType, standalone PageValues purchase-rate EDA, the lengthy timing table, redundant empirical-logit tables, or the EDA-to-experiment bridge. EDA text should only describe what the data show, not anticipate later trials.

## Classifier presentations and selection (unchanged)

Curated table labels are **display aliases**; original canonical IDs remain in the full historical ledger:

| Family | Display IDs | Original trial IDs |
|---|---|---|
| Logistic | L0–L6 | L0,L1,L3,L4,L10,L13,L14 |
| LDA | D0–D6 | D0,D1,D3,D4,D9,D11,D15 |
| Gaussian NB | G0–G6 | G0,G2,G3,G4,G7,G8,G9 |
| Bernoulli NB | B0–B6 | B0,B1,B2,B3,B4,B5,B6 |

Visible table columns: Model, CV ROC-AUC, AUC SE, CV AP, ΔAUC against **the true incumbent**, Complexity, Retained after iteration. A retained alias must reflect the **full sequential history**, not an abbreviated seven-step replay. All original trials, skips, fold scores and real parents are preserved in artifacts.

**Per-model EDA reasoning (approved review-branch refinement):** The existing iteration notes next to each displayed model must state, in one or two sentences, the **specific Section 2/3 EDA observation** and **why its feature, deletion or estimation change was tested**. Cite observed values where helpful; do not infer performance benefits before the model comparison. For display aliases such as G3, verify the underlying canonical trial before describing the change. This text stays within Model Development, not a restored EDA-to-model bridge. Inherited numerical model code and outputs remain frozen; verifier permits only the presentation-note dictionary and saved Markdown rationale changes. Tree pruning gets the same brief evidence-to-choice treatment.

The within-family sequential one-SE rule uses **the higher mean fold ROC-AUC of the incumbent/challenger pair minus the SE of that better model**; among the two eligible candidates choose the simpler (on complexity ties: higher AUC, then incumbent). Inner tuning is fold-safe. Overall finalist selection uses highest mean five-fold training ROC-AUC without a global one-SE rule. Retain historical grouped backward LDA, penalised logistic and Gini/Entropy tree pruning methods. A 1-SE cutoff is a parsimony heuristic, not a significance test.

**Frozen outcome:** 43 planned, 38 scored, 5 inapplicable; 28 visible trial aliases, six finalists. Canonical **L13 Logistic Regression** (display L5) wins with mean CV ROC-AUC **0.75892**, AP **0.34236**. Historically reused reserved check AUC **0.74313**, AP **0.33358**. No causal inference or pristine test-set claims.

## Verification and archival hygiene

Run only the active verifier for presentation checks:

```bash
python scripts/verify_prd_v3_8.py --run-eda
```

This **does not retrain models**. The archived v3.7 PASS audit supplies the fully executed numerical history. The old v3.7 verifier is immutable and retains historical root-path assumptions. Consult the [archive index](archive/versions/README.md), [workflow archive](archive/workflows/README.md) and [v3.7 retirement manifest](archive/versions/v3.7/RETIREMENT_MANIFEST.json) for source provenance. Don't reactivate archived workflows or overwrite evidence.
