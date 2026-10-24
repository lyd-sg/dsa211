# PRD v1.0 revision summary

Implementation is in progress; current result figures will be recorded only after training numerical review and the single-winner audit. Older 75/25, 0.80-threshold and 20-design scores are historical and are not results of this revision.

Completed governance and EDA: fetched the specified approved-PRD branch, created a separate implementation branch, preserved the PRD and historical files, obtained independent plan PASS, executed the separate training EDA and obtained independent PASS for exactly three conditional recipes. Source, split and fold identities were independently reconstructed. The [supervision log](implementation_log.md) records code/output corrections and actual execution evidence.

The final scope is four raw operational baselines plus revised Logit, mixed-likelihood NB and LDA justified by actual training EDA. No recipe is chosen by voucher revenue. Seven operational slots share folds and the highest mean training ROC-AUC selects one. Primary threshold remains exact 2/3, with four OOF references and four fixed-recipient q scenarios. Final evaluation and all-data refit remain gated pending numerical and statistical review.
