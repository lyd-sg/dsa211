#!/usr/bin/env python3
"""Execute the edited PRD v3.6 notebook and verify corrected 1-SE evidence.

Run from repository root AFTER installing requirements.txt:
    python scripts/execute_prd_v3_6.py

The original v3.0–v3.5 sources and evidence are read-only. On failure, the
unexecuted v3.6 notebook is not replaced; the script exits with FAIL.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import nbformat
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "online_shoppers_prd_v3_6.ipynb"
TEMP = ROOT / "online_shoppers_prd_v3_6_executing.ipynb"
EVIDENCE = ROOT / "artifacts" / "prd_v3_6"
OLD = ROOT / "artifacts" / "prd_v3_4" / "all_attempts_ledger.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_source():
    assert OLD.exists(), "Cannot establish immutable original evidence"
    n = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(n)
    assert len(n.cells) == 47
    code = [c for c in n.cells if c.cell_type == "code"]
    assert len(code) == 25
    for i, c in enumerate(n.cells):
        if c.cell_type == "code":
            compile(c.source, f"v3.6 cell {i}", "exec")
    source = "\n".join(c.source for c in code)
    for symbol in ("run_v36_family", "SKIPPED_INAPPLICABLE",
                   "_inner_one_se_refit", "BackwardSelectedLDA"):
        assert symbol in source, symbol


def check_evidence():
    n = nbformat.read(TEMP, as_version=4)
    nbformat.validate(n)
    code = [c for c in n.cells if c.cell_type == "code"]
    assert len(code) == 25
    assert all(c.execution_count is not None for c in code)
    assert not [(i, o) for i, c in enumerate(code) for o in c.outputs
                if o.output_type == "error"]
    required = ["all_attempts_ledger.csv", "all_attempt_fold_scores.csv",
                "retained_pathways.csv", "independent_training_audit.json",
                "run_metadata.json", "six_finalists.csv",
                "finalist_oof_scores.csv", "four_threshold_references.csv",
                "tree_selection.json", "tree_alpha_paths.csv",
                "tree_alpha_fold_scores.csv", "frozen_holdout_scores.csv",
                "final_specification.json"]
    for name in required:
        assert (EVIDENCE / name).is_file() and (EVIDENCE / name).stat().st_size, name
    ledger = pd.read_csv(EVIDENCE / "all_attempts_ledger.csv")
    scores = pd.read_csv(EVIDENCE / "all_attempt_fold_scores.csv")
    finalists = pd.read_csv(EVIDENCE / "six_finalists.csv")
    audit = json.loads((EVIDENCE / "independent_training_audit.json").read_text())
    meta = json.loads((EVIDENCE / "run_metadata.json").read_text())
    assert len(ledger) == 41
    assert set(ledger.status).issubset({"SCORED", "SKIPPED_INAPPLICABLE"})
    assert ledger.step.nunique() == 41
    assert audit["status"] == "PASS"
    assert audit["scored_family_trials"] == int(ledger.status.eq("SCORED").sum())
    assert audit["skipped_inapplicable"] == int(
        ledger.status.eq("SKIPPED_INAPPLICABLE").sum())
    assert meta["prd"] == "v3.6"
    assert meta["historically_pristine_holdout"] is False
    assert len(scores) == 5 * len(scores.candidate.unique())
    assert scores.candidate.nunique() == audit["cv_designs_verified"]
    assert len(finalists) == 6 and finalists.pathway.nunique() == 6
    assert finalists.iloc[0].candidate == meta["selected_model"]
    assert len(pd.read_csv(EVIDENCE / "frozen_holdout_scores.csv")) == 2466
    assert len(pd.read_csv(EVIDENCE / "four_threshold_references.csv")) == 4
    trees = json.loads((EVIDENCE / "tree_selection.json").read_text())
    prior = json.loads((ROOT / "artifacts" / "prd_v3_4" /
                        "tree_selection.json").read_text())
    for family in ("GiniTree", "EntropyTree"):
        for attr in ("leaves", "depth", "ccp_alpha", "mean_auc",
                     "best_mean_auc", "best_auc_se", "one_se_cutoff"):
            assert np.isclose(trees[family][attr], prior[family][attr],
                              atol=1e-12, rtol=0), (family, attr)
    if bool(ledger.set_index("step").loc["G6", "accepted"]):
        assert ledger.set_index("step").loc["G7", "status"] == "SKIPPED_INAPPLICABLE"
    return n, audit, finalists


def main():
    os.chdir(ROOT)
    check_source()
    old_sha = sha256(OLD)
    env = os.environ.copy()
    for var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        env[var] = "1"
    cmd = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook", "--execute", NOTEBOOK.name,
        "--ExecutePreprocessor.timeout=7200",
        "--output", TEMP.name,
    ]
    print("Running original-data, fixed-fold v3.6 re-evaluation...", flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT, env=env)
    executed, audit, finalists = check_evidence()
    assert sha256(OLD) == old_sha, "Historical trial ledger was modified"
    executed.metadata["dsa211_execution_status"] = "EXECUTED_VERIFIED"
    nbformat.write(executed, TEMP)
    TEMP.replace(NOTEBOOK)
    print("PASS: PRD v3.6 notebook executed and independently checked")
    print("Trials:", audit["scored_family_trials"], "scored;",
          audit["skipped_inapplicable"], "skipped")
    print(finalists[["pathway", "candidate", "mean_auc", "mean_ap"]].to_string(index=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: PRD v3.6 execution or verification:", repr(exc), file=sys.stderr)
        raise SystemExit(1)
