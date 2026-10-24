# PRD implementation scope and provenance

The approved [PRD v1.0](PRD.md) supersedes the older three-baseline, 75/25, revenue-optimised analysis. Its contents are preserved unchanged. The owner explicitly authorised independent technical-plan review and autonomous implementation after PASS; see [plan review](technical_plan_review.md) and [recipe review](recipe_review.md).

The implementation branch descends from `revise-three-model-scope` at `8cbeeb085be1c6b322f7a7dca8885dd7c5cbe536`. The dataset and existing archives remain protected. The pre-revision active notebook was preserved byte-for-byte at `archive/online-shoppers/online_shoppers_pre_prd_v1.ipynb` (SHA-256 `fe15cdefe2449245ca5a4ccbbaa09307050090fb5ae0b2d46dde7f9fcb448292`). Old outputs are historical, not evidence for current model choices.

The current scope is training-only EDA, four all-17 diagnostics, four raw 16-source baselines and three independently approved EDA-informed revisions; seven common-fold operational comparison slots, one CV-selected winner, fixed 2/3 policy, four OOF threshold references, four fixed-recipient conversion scenarios, one winner test audit, then exact all-data refit. No automatic feature search, regularisation competition, QDA or unrelated classifiers.

The separate supplementary notebook contains the five PRD investigations and is not submitted. All split/fold original row IDs are retained in `artifacts/`; they document membership, not identified visitors. The supervision record distinguishes implementation evidence from Sol's independent inspection and corrections.

The final verification report will record completed execution and criterion-by-criterion evidence. Original course source files are absent, so direct lab/lecture/workflow-file comparison cannot be claimed. Historical overlapping test exposure, duplicate patterns, selection optimism, probability/distributional assumptions and unresolved feature timing remain limitations regardless of successful execution. Voucher response, order values and margins are unobserved; scenarios do not establish actual effectiveness or profit.
