# PRD v3.1 — requirements alignment and housekeeping audit

**Date:** 3 November 2026  
**Active requirements:** [PRD v3.1](../PRD_v3.1.md)  
**Archived v3.0 requirements:** [PRD v3.0](../archive/PRD_v3.md)  
**Scope:** Requirements and repository housekeeping only. **No v3.1 classification-tree code has been implemented, run or validated by this update.** The executed notebook and supporting v3.0 output are not labelled as v3.1 findings.

## Decisions explicitly agreed in conversation

| Requirement | PRD v3.1 location |
|---|---|
| Extend rather than rebuild PRD v3.0; preserve original four modelling pathways | Intro; §§1, 5.1–5.5 |
| Add classification trees as fifth pathway | §§1, 4, 5.6 |
| Use 16 operational predictor sources, excluding PageValues | §§2, 4, 5.6 |
| Grow full Gini and Entropy trees as the two tree baselines | §§4, 5.6 |
| Classification Error is not a candidate splitting criterion | §4 (Gini/Entropy only), §5.6 |
| Use cost-complexity pruning with candidate ccp_alpha values | §§5.6, 6.5 |
| Select alpha by the 1-SE simplicity rule on five-fold CV **ROC-AUC**, separately for Gini and Entropy | §§5.6, 6.1, 6.5 |
| Do not impose the original 3–5 EDA-driven specification steps on trees | §§1, 5.5–5.6 |
| Report full-grown baseline versus selected tree for each criterion | §§4, 5.6, 9 |
| Compare both independently selected tree specifications **directly** with the four existing pathway finalists | §§1, 6.4, 9, 12–13 |
| Keep mean five-fold training CV ROC-AUC as primary selection metric and AP secondary | §§1, 6, 9 |
| Follow the professor's ordinary CV + held-out test workflow rather than introducing a new nested-CV evaluation regime | §§2, 6.3–6.5, 11 |
| Keep existing winner-only classification-threshold analysis | §§7–8 |

## Requirements inherited unchanged from PRD v3.0

- Prediction-only objective, session-level unit, data size/duplicates and PageValues timing qualification.
- Stratified 80/20 training/held-out partition, seed 42 and five shared stratified training folds.
- Four original EDA-informed specification paths and their local one-SE acceptance rules; existing Logit/LDA inner hyperparameter CV remains unchanged.
- Existing four full-17 source-feature timing diagnostics (trees begin directly at the 16-source operational baseline).
- Business scenario assumptions and four threshold references, including the hypothetical cost-based 0.20.
- Existing final frozen winner, held-out check and unchanged all-data refit requirements.
- Original caveat concerning prior historical test use remains **because it was already in v3.0**. This was **not** used as a rationale for introducing nested CV.

## Implementation conventions distinguished from confirmed requirements

The following were specified as supporting implementation choices or lecture conventions rather than independently approved new methodological objectives:

1. **Encoding and defaults:** fold-fitted one-hot encoding for nominal tree inputs; default `max_depth=None`, `min_samples_leaf=1`, `min_samples_split=2`, `class_weight=None`, `ccp_alpha=0`, and seed 42. These were reviewed as the proposed tree defaults; they are *not* separately tuned.
2. **Root-only tree:** the course's pruning example drops the final `ccp_alphas[-1]` candidate, which collapses to a one-leaf root-only tree. This is documented in v3.1 as following Lesson 10, not as a new comparative modelling family.
3. **Tie resolution:** v3.1 requires the simplest tree satisfying the 1-SE cutoff. No specific alpha tie-break (such as largest alpha) is imposed as an owner-agreed rule. If exactly equal-size eligible candidates arise, record and predeclare a deterministic implementation tie-break.
4. **Tree all-17 diagnostic:** no extra tree-based all-17 timing diagnostic was added; the v3.0 diagnostic panel remains four models, and trees use the agreed 16 operational sources.

These conventions should be surfaced for owner review during the v3.1 technical-plan stage, rather than asserted as additional separately approved research requirements.

## Structural integrity checks

- Canonical PRD moved to root `PRD_v3.1.md`; original `docs/PRD_v3.1.md` is a navigation stub.
- Archived requirements stored at `archive/PRD_v3.md`; old `docs/PRD_v3.md` is a navigation stub.
- Archived v3.0 substantive requirements remain unchanged; relative Markdown links were adjusted to continue resolving.
- README, AGENTS, archive index, v3.0 technical plan and v3.0 requirements audit distinguish active v3.1 requirements from executed v3.0 implementation.
- No existing notebooks, source data, build scripts, workflows or previous output artifacts were altered as part of this documentation-only housekeeping.
- Active documentation links and all thirteen major PRD sections were checked; any actual future v3.1 performance claims require a separate executed model implementation and audit.
