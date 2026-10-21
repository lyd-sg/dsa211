# DSA211 — Online Shoppers Purchasing Intention

Prediction-focused classification project using the [UCI Online Shoppers Purchasing Intention dataset](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention). The response is `Revenue` (whether a browsing **session** ends in a purchase).

> **Status:** Existing exploratory work has been preserved; the notebook is **not an approved final analysis**. The professor's latest baseline instruction and the group's revised business-cost assumptions still need statistical review. This housekeeping change does **not** rerun models, alter results, or validate earlier conclusions.

## Phase 2 — revised core analysis

- [**`online_shoppers_revised.ipynb`**](online_shoppers_revised.ipynb) — new step-by-step, prediction-focused notebook for the professor-specified core analysis and two agreed extensions. The notebook has been **executed against the actual committed dataset in GitHub Actions**; the source notebook remains free of generated outputs, and a successful run's executed notebook can be downloaded from the workflow artifacts.
- [**`docs/phase2_scope.md`**](docs/phase2_scope.md) — scope, analysis stages, old-versus-new differences and verification caveats.
- [**Notebook validation workflow**](.github/workflows/validate-notebook.yml) — executes the revised notebook against `data/uci_468.csv` and uploads an executed notebook artifact when GitHub Actions is enabled.

The original main notebook is still kept at the root unchanged as a historical reference. Both notebooks expect the repository root as their working directory.

## Start here

- [`online_shoppers_full_project.ipynb`](online_shoppers_full_project.ipynb) — full, **unchanged** analysis notebook. It contains EDA, model comparisons, CV, tuning, historical test-set results, and provisional conclusions.
- [`docs/project_decisions.md`](docs/project_decisions.md) — recorded professor instructions, group consensus, and outstanding questions.
- [`docs/methodology.md`](docs/methodology.md) — proposed workflow for the subsequent statistical revision; **not a claim that every step has been completed**.
- [`data/uci_468.csv`](data/uci_468.csv) — version of the dataset currently used by the notebook.
- [`archive/README.md`](archive/README.md) — previous dataset-selection work and superseded Online Shoppers drafts.

## Run the existing notebook

From the **repository root**, with Python installed:

```bash
python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python -m jupyter lab
```

Open `online_shoppers_full_project.ipynb`. Keep its kernel working directory at the repository root: the existing code refers to `data/uci_468.csv` relative to that directory. The notebook also has an upstream UCI download fallback if the local CSV is absent.

**Important:** Running the notebook executes experiments and reuses its existing train/test split; it is not an untouched new holdout evaluation. Preserved notebook outputs and results reflect the earlier modelling and cost assumptions (including `C_FN/C_FP = 5`), not the group's latest CAC/discount proposal.

## Scope and modelling plan

The group has chosen **prediction**, not inference, and will compare the three taught classifier families (logistic regression, Naive Bayes, discriminant analysis). The professor requested an initial attempt with all predictors and each model in its as-is form before testing modifications. Numeric-coded nominal categories must not be treated as ranked quantities. Cross-validation should guide subsequent modifications, and the test partition should remain outside model selection.

The existing notebook's historical 75/25 stratified split is retained. No split, results, model specification, target or cost calculation was changed during this repository cleanup.

## Repository layout

```text
online_shoppers_full_project.ipynb   # preserved main analysis (root for existing paths)
data/uci_468.csv                      # dataset used by the notebook
docs/project_decisions.md             # latest instructions, decisions, open questions
docs/methodology.md                   # planned workflow; no new analyses
archive/online-shoppers/             # previous drafts and brief
archive/dataset-selection/           # old multi-dataset bake-off code and outputs
AGENTS.md / CLAUDE.md                 # current contributor / agent guidance
requirements.txt                      # main notebook dependencies
.gitignore                            # ignore local/generated files
```

No new predictive or cost-based findings are claimed by this reorganisation.
