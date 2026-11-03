#!/usr/bin/env python3
"""PRD 3.5: verify curated executed notebook against frozen v3.4 evidence, with NO fitting."""
from __future__ import annotations

import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
SOURCE_NB = ROOT / "archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb"
PRESENT_NB = ROOT / "online_shoppers_prd_v3_5.ipynb"
LEDGER = ROOT / "artifacts/prd_v3_4/all_attempts_ledger.csv"
FOLD_SCORES = ROOT / "artifacts/prd_v3_4/all_attempt_fold_scores.csv"
TREES = ROOT / "artifacts/prd_v3_4/tree_full_vs_selected.csv"
AUDIT = ROOT / "artifacts/prd_v3_4/independent_training_audit.json"
PRD = ROOT / "PRD_v3.5.md"
OUTPUT = ROOT / "artifacts/prd_v3_5/presentation_audit.json"

GROUPS = {
    "Logit": ["L0", "L1", "L4", "L7", "L8", "L13", "L14"],
    "LDA": ["D0", "D1", "D4", "D9", "D10", "D11", "D15"],
    "GaussianNB": ["G0", "G1", "G2", "G3", "G6", "G7", "G8"],
    "BernoulliNB": ["B0", "B1", "B2", "B3", "B4"],
}
RETAINED = {
    "Logit": "L1 | Logit",
    "LDA": "Operational16 | LDA",
    "GaussianNB": "G7 | GaussianNB",
    "BernoulliNB": "B3 | BernoulliNB",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(cell) -> str:
    v = cell["source"]
    return "".join(v) if isinstance(v, list) else v


def as_text(v) -> str:
    return "".join(v) if isinstance(v, list) else str(v)


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self._row = None
        self._cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._row.append("".join(self._cell).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None


def parsed_table(html: str):
    p = TableParser()
    p.feed(html)
    return p.rows


def read_csv(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    n34_raw = json.loads(SOURCE_NB.read_text())
    n35_raw = json.loads(PRESENT_NB.read_text())
    n35_nb = nbformat.read(PRESENT_NB, as_version=4)
    nbformat.validate(n35_nb)
    assert len(n34_raw["cells"]) == 47
    assert len(n35_raw["cells"]) == 49
    old_code = [c for c in n34_raw["cells"] if c["cell_type"] == "code"]
    new_code = [c for c in n35_raw["cells"] if c["cell_type"] == "code"]
    assert len(old_code) == len(new_code) == 25
    assert all(c.get("execution_count") is not None for c in new_code)
    assert not [(i, o) for i, c in enumerate(new_code)
                for o in c.get("outputs", []) if o.get("output_type") == "error"]
    for i, c in enumerate(new_code):
        compile(source(c), f"v35_cell_{i}", "exec")
    imgs = [o for c in new_code for o in c.get("outputs", [])
            if "image/png" in o.get("data", {})]
    assert len(imgs) == 7

    # All numerical model definitions, evaluator internals, model-fit calls and tests
    # must remain unchanged. Only the output folder, renderer, visible stdout,
    # tree comparison renderer and final printed summary may differ.
    allowed_changes = {5, 9, 10, 11, 12, 13, 15, 24}
    modified = {i for i, (x, y) in enumerate(zip(old_code, new_code))
                if source(x) != source(y)}
    assert modified == allowed_changes, (modified, allowed_changes)
    o, v = source(old_code[5]), source(new_code[5])
    assert v == o.replace("V3_ART=ARTIFACTS/'prd_v3_4'",
                          "V3_ART=ARTIFACTS/'prd_v3_5' # Re-execution isolation only; presentation evidence remains frozen v3.4")
    o, v = source(old_code[9]), source(new_code[9])
    assert v.startswith(o.split("def display_family(family):")[0])
    assert "V35_CURATION" in v and "display(pd.DataFrame(annotated).round(5))" in v
    for i in (10, 11, 12, 13):
        old, new = source(old_code[i]), source(new_code[i])
        assert "contextlib.redirect_stdout(io.StringIO())" in new
        assert new.count("run_v31_family(f)") == old.count("run_v31_family(f)")
        assert new.count("run_v32_family(f)") == old.count("run_v32_family(f)")
        assert new.count("run_v33_family(f)") == old.count("run_v33_family(f)")
        assert new.count("run_v34_family(f)") == old.count("run_v34_family(f)")
        assert new.count("display_family(f)") == old.count("display_family(f)")
    old = source(old_code[15])
    new = source(new_code[15])
    before, _, after = old.partition("display(TREE_BASELINE_SELECTED.round(5))")
    assert before and after and new.startswith(before) and new.endswith(after)
    assert "assert len(tree_display)==4" in new
    old = [ln for ln in source(old_code[24]).splitlines() if not ln.startswith("print(")]
    new = [ln for ln in source(new_code[24]).splitlines() if not ln.startswith("print(")]
    assert old == new

    ledger = read_csv(LEDGER)
    scores = read_csv(FOLD_SCORES)
    trees = read_csv(TREES)
    old_audit = json.loads(AUDIT.read_text())
    assert len(ledger) == 41 and len(scores) == 255 and len(trees) == 2
    assert {k: sum(r["trial_version"] == k for r in ledger) for k in
            ("v3.1", "v3.2", "v3.3", "v3.4")} == {"v3.1": 20, "v3.2": 11, "v3.3": 7, "v3.4": 3}
    assert old_audit["status"] == "PASS"
    assert old_audit["cv_candidates_verified"] == 51
    assert old_audit["sequential_decisions_verified"] == 37
    assert old_audit["backward_lda_path_entries_verified"] == 80
    assert old_audit["tree_alpha_candidates_verified"] == 722

    prd_rows = {}
    for ln in PRD.read_text().splitlines():
        if not ln.startswith("| ") or not ln.split("|")[1].strip()[:1] in "LDBG":
            continue
        arr = [part.strip() for part in ln.split("|")[1:-1]]
        if len(arr) != 6 or not arr[0][1:].isdigit():
            continue
        step, parent, change, reason, auc, verdict = arr
        assert step not in prd_rows
        prd_rows[step] = (parent, change, reason, float(auc), verdict.replace("**", "").replace("; ", " · "))
    assert len(prd_rows) == 26
    by_id = {r["step"]: r for r in ledger}
    assert len(by_id) == 41

    # Every visible row is compared with BOTH the PRD and the frozen numerical ledger.
    rendered = {}
    family_tables = []
    for c in new_code:
        for out in c.get("outputs", []):
            html = as_text(out.get("data", {}).get("text/html", ""))
            if "Historical outcome" in html:
                family_tables.append(parsed_table(html))
    assert len(family_tables) == 4
    for (family, expected), table in zip(GROUPS.items(), family_tables):
        assert table[0] == ["ID", "Actual parent", "Change tested",
                            "EDA rationale / baseline purpose", "CV ROC-AUC",
                            "AUC SE", "CV AP", "Historical outcome"]
        assert [r[0] for r in table[1:]] == expected, (family, table)
        for row in table[1:]:
            step, parent, change, reason, auc, se, ap, verdict = row
            raw = by_id[step]
            pp, pc, pr, pa, pv = prd_rows[step]
            assert raw["pathway"] == family
            assert parent == raw["parent"]
            assert change == pc and reason == pr and verdict == pv
            assert ("—" if parent == "—" else parent.split(" | ")[0]) == pp
            assert abs(float(auc) - float(raw["mean_auc"])) < 0.000011
            assert abs(float(se) - float(raw["auc_se"])) < 0.000011
            assert abs(float(ap) - float(raw["mean_ap"])) < 0.000011
            assert abs(float(auc) - pa) < 0.000011
            if step in ("L0", "D0", "G0", "B0"):
                assert verdict.startswith("Baseline")
            elif raw["accepted"] == "True":
                assert verdict.startswith(("Accepted", "Qualified"))
            else:
                assert verdict == "Not accepted"
            rendered[step] = family

    assert len(rendered) == 26
    assert rendered["D0"] == "LDA"
    assert prd_rows["D0"][2] == "Baseline"
    assert by_id["G6"]["accepted"] == "True"
    assert by_id["G7"]["accepted"] == "True"
    assert by_id["L7"]["accepted"] == "False"
    assert by_id["D15"]["accepted"] == "False"

    # Exactly four tree rows, each numerically derived from the original v3.4 tree CSV.
    tree_tables = []
    for c in new_code:
        for out in c.get("outputs", []):
            html = as_text(out.get("data", {}).get("text/html", ""))
            if "Full (unpruned)" in html:
                tree_tables.append(parsed_table(html))
    assert len(tree_tables) == 1
    tab = tree_tables[0]
    assert tab[0] == ["Tree family", "Stage", "CV ROC-AUC", "CV AP",
                      "Leaves", "Depth", "ccp_alpha", "Rationale"]
    assert len(tab) == 5
    for t, a, b in zip(trees, tab[1::2], tab[2::2]):
        assert a[:2] == [t["family"], "Full (unpruned)"]
        assert b[:2] == [t["family"], "Selected (pruned)"]
        for row, prefix in ((a, "baseline"), (b, "selected")):
            assert abs(float(row[2]) - float(t[prefix + "_mean_auc"])) < 0.000011
            assert abs(float(row[3]) - float(t[prefix + "_mean_ap"])) < 0.000011
            assert int(row[4]) == int(t[prefix + "_leaves"])
            assert int(row[5]) == int(t[prefix + "_depth"])
            assert abs(float(row[6]) - float(t[prefix + "_alpha"])) < 0.000011

    md = "\n".join(source(c) for c in n35_raw["cells"] if c["cell_type"] == "markdown")
    assert "D0 rationale: Baseline" in md
    assert "DSA211 methods-considered matrix" in md
    assert "EDA-to-experiment bridge" in md
    assert "not a pristine holdout" in md
    assert "PCR/PLS" in md
    assert "post-hoc editorial curation" in md
    assert n35_raw["metadata"]["new_models_fitted_for_presentation"] == 0
    assert n35_raw["metadata"]["historical_trial_count"] == 41

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "status": "PASS",
        "prd": "v3.5",
        "presentation_only": True,
        "new_models_fitted": 0,
        "executed_source": "PRD v3.4",
        "notebook_cells": len(n35_raw["cells"]),
        "existing_code_cells": len(new_code),
        "python_code_cells_compiled": len(new_code),
        "code_cells_modified_for_display_only": sorted(modified),
        "embedded_original_figures": len(imgs),
        "error_outputs": 0,
        "family_table_rows": {family: len(ids) for family, ids in GROUPS.items()},
        "visible_original_family_trials": len(rendered),
        "frozen_original_family_trials": len(ledger),
        "frozen_scored_designs": old_audit["cv_candidates_verified"],
        "frozen_fold_scores": len(scores),
        "frozen_acceptance_decisions": old_audit["sequential_decisions_verified"],
        "tree_display_rows": len(tab) - 1,
        "frozen_alpha_candidates": old_audit["tree_alpha_candidates_verified"],
        "source_notebook_sha256": sha(SOURCE_NB),
        "presentation_notebook_sha256": sha(PRESENT_NB),
        "source_trial_ledger_sha256": sha(LEDGER),
        "frozen_audit_sha256": sha(AUDIT),
        "no_old_result_files_written": True,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: 49 notebook cells, 25 Python cells compile, no errors, 7 original figures")
    print("PASS: 7/7/7/5 curated family rows, all rationale and model status match PRD/ledger")
    print("PASS: 4 tree full/pruned rows match frozen numeric evidence")
    print("PASS: all 41 trials, 51 designs, 255 folds, 37 decisions preserved")
    print("PASS: no model fitting; display-only changes verified against v3.4")


if __name__ == "__main__":
    main()
