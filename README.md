# DSA211 Topic 2 dataset bake-off

Decides on measured evidence, not assumption, whether the **ACRA Singapore
firm-survival** data or the **Taiwan credit-default** data is the better base for a
classification-evaluation report.

## Run

```bash
bash run.sh
```

Or manually:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python bakeoff.py --self-test     # synthetic, no network, proves the pipeline works
python bakeoff.py                 # the real thing
```

## Outputs, written to `results/`

| File | Contents |
|---|---|
| `scorecard.csv` | Nine pass/fail criteria per dataset |
| `verdict.txt` | The ranking and how to read the failures |
| `supporting_numbers.csv` | Leakage premium, AUC spread, diagnostics, thresholds |
| `leakage_screen_*.csv` | Univariate AUC and differential missingness per feature |
| `results.json` | Everything, machine readable |
| `roc_*.png` | Out-of-fold ROC overlay and threshold sweep |

## Useful flags

```bash
python bakeoff.py --cost-ratio 10          # C_FN / C_FP, moves the threshold
python bakeoff.py --cohort 2008 2014       # ACRA incorporation window
python bakeoff.py --letters A,G,S          # which ACRA letter files
python bakeoff.py --only taiwan            # one dataset
python bakeoff.py --acra-local a.csv s.csv # skip the download
python bakeoff.py --taiwan-local uci.xls   # skip the download
```

## If a download fails

The ACRA dataset IDs and the data.gov.sg download endpoint were taken from page
metadata, not from a confirmed fetch. Both loaders print the real error and the
real CSV header. Fall back to the manual path:

- ACRA, from <https://data.gov.sg/collections/2/view>, then `--acra-local`
- Taiwan, from <https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients>, then `--taiwan-local`
