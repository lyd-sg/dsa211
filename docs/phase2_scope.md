# Completed PRD scope and verification

The approved [PRD v1.0](PRD.md) supersedes the older three-baseline, 75/25, revenue-optimised analysis and remains unchanged. The owner's autonomous instruction authorises independent technical-plan approval; the plan, recipe, baseline, pre-test and static audit-code review records document those gates.

The branch descends from `revise-three-model-scope` at `8cbeeb085be1c6b322f7a7dca8885dd7c5cbe536`. The committed source data and historical archives are unchanged. The pre-revision active notebook is preserved byte-for-byte as `archive/online-shoppers/online_shoppers_pre_prd_v1.ipynb` (SHA-256 `fe15cdefe2449245ca5a4ccbbaa09307050090fb5ae0b2d46dde7f9fcb448292`). Old outputs are historical, not current evidence.

Completed analysis: quality before a stratified 80/20 split; separate training-only supplementary EDA; four all-17 diagnostics; four prescribed raw baselines; three fixed EDA-supported revisions; seven same-fold operational comparisons; one CV-selected winner; four OOF threshold references; four fixed-recipient q scenarios; one frozen test audit at 2/3; exact all-data refit without another score.

The official self-contained main notebook completed all 18 code cells in 4m52s with zero error outputs. Revised Logit wins training mean AUC at 0.757647; test AUC/AP are 0.741210/0.326790. At the frozen 2/3 policy it detects zero of 382 buyers and offers 2,464/2,466 vouchers. These poor threshold findings are retained. Assumed q=.10/.25/.50/1.00 changes only scenario arithmetic, never selection or assignments.

The final exact pipeline fit uses 12,330 rows and is not scored. Saved probabilities, folds, numerical checks, metrics, warnings and frozen decisions are in `artifacts/`. The [verification report](verification_report.md) checks every acceptance criterion and separates completed local/source/numerical checks from unavailable original-course-file comparison and unrun remote CI. No new automated code-checking suite was added; the original notebook execution workflow remains unchanged.

The supplementary notebook is not submitted. Historical exposure, duplicate patterns, training selection optimism, NB/LDA assumptions, Logit boundary uncertainty, probability calibration and predictor timing remain limitations. Voucher outcomes, customer identity, actual order values and margins are absent; scenarios do not establish actual effects, profit or deployment feasibility.
