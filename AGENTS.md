# Brief for the agent

## What this repository is

`bakeoff.py` is a decision instrument. It measures whether the ACRA Singapore
firm-survival data or the Taiwan credit-default data is the better base for a
university classification-evaluation report. It is not a model I am trying to
improve. Its job is to produce an honest verdict, including an unflattering one.

The report it feeds requires logistic regression, Naive Bayes and LDA, each
evaluated by confusion matrix, ROC, AUC, sensitivity and specificity, under
k-fold cross-validation in a leakage-free pipeline, plus a justified operating
threshold other than 0.5 and a comparison of CV estimates against a held-out set.

## Run it in this order

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python bakeoff.py --self-test --outdir results_selftest
python bakeoff.py --outdir results
```

The self-test uses synthetic data with a deliberately planted leak and needs no
network. If it does not pass, the environment is broken, not the datasets.
Expected self-test behaviour: ACRA leakage premium around 0.35, Taiwan leakage
premium exactly 0.0000 with `PAY_0` flagged but kept.

## Hard rules

Do not do any of the following, even if it would make the output look better.

1. **Do not loosen a threshold in `CRITERIA`.** The nine thresholds are the
   instrument. A fail is a measurement, not a bug.
2. **Do not set `--auto-drop-flagged` or flip `AUTO_DROP_FLAGGED`** without
   saying so explicitly in your summary. A flagged feature is not proven
   leakage; a genuinely strong predictor also scores high on a univariate screen.
3. **Do not move the train/test split.** It happens first, in `evaluate`, and
   the test set is touched exactly once at the end. Do not fit, select or tune
   anything on it.
4. **Do not lift preprocessing out of the pipeline.** Imputation, scaling and
   one-hot encoding must stay inside `make_pre` so they are refitted per fold.
   Fitting them on the full training set before CV is the exact error the report
   is being marked on.
5. **Do not invent numbers.** If a loader fails, say it failed. Do not
   substitute figures from the internet or from memory.

## Expected failure modes, and what to do

- **ACRA download returns a non-200 or an unexpected payload.** The dataset IDs
  in `ACRA_LETTERS` and the `poll-download` endpoint were read off page
  metadata, not confirmed. Ask me to download the letter CSVs by hand from
  <https://data.gov.sg/collections/2/view>, then use `--acra-local`.
- **ACRA header does not contain a role the adapter wants.** `_read_acra_one`
  prints the actual header. Add the real column name to `ACRA_WANTED` and rerun.
  Do not rewrite `adapt_acra` around the missing column.
- **`ucimlrepo` fails.** The second fallback reads the UCI `.xls`, which needs
  `xlrd`. If both fail, ask me for the file and use `--taiwan-local`.
- **A dataset yields fewer than 500 training positives.** Try a wider
  `--cohort` or more `--letters` before concluding anything.

## What to report back to me

Keep it short. Bullets, one sentence each.

1. The verdict line and the pass tally per dataset.
2. **Every failed criterion, and what section of the report it breaks.** A fail
   on "Models separate beyond noise" empties the three-way model comparison. A
   fail on "Cost cut vs best trivial rule" empties the threshold extension.
   These matter more than a wide confidence interval on held-out sensitivity.
3. The leakage premium for each dataset, and which columns were dropped. A large
   ACRA premium confirms that `no_of_officers` and the filing dates encode the
   outcome, since a struck-off company has no officers and stale returns.
4. Any feature flagged but not dropped, and your view on whether it is real
   signal or leakage. Say which, and why.
5. The diagnostics and what they imply for the write-up: mean absolute
   correlation predicts whether Naive Bayes will suffer under its independence
   assumption, the QDA minus LDA gap prices the equal-covariance assumption, and
   a wide Brier spread across models with similar AUCs is the calibration point.
6. Whether `--cost-ratio` should be rerun at a different value, given that the
   chosen threshold and one criterion move with it.

Do not recommend a dataset on tally alone. Name the trade.
