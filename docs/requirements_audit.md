# PRD v2.0 implementation traceability

**Controlling document:** [Approved PRD v2.0](PRD_v2.md). Precise implementation contract: [Technical plan v2.0](technical_plan.md). [Earlier requirements audit](requirements_audit_v1_archive.md) applies to v1.0 only.

| Acceptance area | Implementation location | Verification requirement |
|---|---|---|
| Prediction only, correct scope | Main notebook title, objective, conclusion | No discount, business-cost or conversion analysis |
| Data readiness, class balance, preserved duplicates | Notebook sections 1–2 | 12,330 source records; types/missing/duplicates verified |
| Fixed split and common CV folds | Setup/data block and saved row-ID artifacts | 9,864 train, 2,466 reserved; seed 42; identical folds |
| Training-only EDA | Notebook numerical/categorical/assumption blocks; supplementary EDA | No held-out target information used to choose features |
| Four all-17 diagnostics and PageValues | Initial comparison | Timing uncertainty distinguished from proven leakage |
| Four baseline classifiers | Operational16 comparison | Exact raw model-specific feature handling |
| Three current revisions | Revised model section and recipe audit | L2 Logit, shrinkage LDA and Mixed NB match frozen recipes |
| Seven-model selection | Seven CV rows, fold/OOF evidence, OOF ROC overlay | Highest mean CV ROC-AUC; AP and SD/SE supported |
| Positive-class performance | Winner OOF PR plot | Correct AP baseline and distinction between pooled and mean AP |
| Probability-score interpretation | Winner OOF histogram | Ranking is not probability calibration |
| Three threshold references | Sensitivity–specificity plot and one 3-row table | Prevalence, 0.5 and crossover; sensitivity, specificity, precision |
| Final refits | Train-fit numerical audit and full-data fit | Stable, finite and unchanged specification; no in-sample validation claim |
| Presentation and claims | Every substantive markdown/code pair | Purpose-first, accurate actual results, no duplicate graphs |
| Reproducibility | GitHub Actions executed notebook; saved artifacts | Clean full execution and independent numeric review |
| Version control | Active implementation branch and PR | Historical files intact; no accidental merge |

**Status:** Traceability criteria only. Do not mark the implementation PASS until the actual execution output and independent numerical/visual review have been verified.
