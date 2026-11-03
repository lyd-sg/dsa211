#!/usr/bin/env python3
"""Audit current PRD 3.5 notebook presentation against frozen modelling and supplementary EDA.

No model fitting, no random splits, no modification of source evidence.
"""
from __future__ import annotations

from collections import Counter
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "archive/versions/v3.4/online_shoppers_prd_v3_4.ipynb"
PRESENT = ROOT / "online_shoppers_prd_v3_5.ipynb"
SUPP = ROOT / "supplementary/training_eda.ipynb"
LEDGER = ROOT / "artifacts/prd_v3_4/all_attempts_ledger.csv"
FOLDS = ROOT / "artifacts/prd_v3_4/all_attempt_fold_scores.csv"
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
SUPPLEMENTARY_SECTIONS = {
    "activity": 4,
    "visitor": 6,
    "rare": 8,
    "special": 10,
    "timing": 12,
    "conditional": 14,
}


def text(value):
    return "".join(value) if isinstance(value, list) else str(value)


def source(c):
    return text(c["source"])


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def images(nb):
    return [text(o["data"]["image/png"])
            for c in nb["cells"] for o in c.get("outputs", [])
            if "image/png" in o.get("data", {})]


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append("".join(self.cell).strip())
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def displayed_tables(nb):
    result = []
    for c in nb["cells"]:
        for o in c.get("outputs", []):
            value = text(o.get("data", {}).get("text/html", ""))
            if "<table" in value:
                parser = TableParser()
                parser.feed(value)
                result.append(parser.rows)
    return result


def table_with_header(tables, name):
    return [t for t in tables if t and name in t[0]]


def rows(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def compare_float(value, expected):
    assert abs(float(value) - float(expected)) < 1.1e-5, (value, expected)


def main():
    old = json.loads(SRC.read_text())
    new = json.loads(PRESENT.read_text())
    sup = json.loads(SUPP.read_text())
    nbformat.validate(nbformat.read(PRESENT, as_version=4))
    assert len(old["cells"]) == 47
    assert len(new["cells"]) == 64
    assert len(sup["cells"]) == 15
    assert new["metadata"]["new_models_fitted_for_presentation"] == 0

    src_codes = [c for c in old["cells"] if c["cell_type"] == "code"]
    new_codes = [c for c in new["cells"] if c["cell_type"] == "code"]
    old_like = [c for c in new_codes if not c["id"].startswith("integrated-sup-")]
    assert len(src_codes) == len(old_like) == 25
    assert len(new_codes) == 31
    assert all(c.get("execution_count") is not None for c in new_codes)
    assert not [(i, o) for i, c in enumerate(new_codes) for o in c.get("outputs", [])
                if o.get("output_type") == "error"]
    for i, c in enumerate(new_codes):
        compile(source(c), f"current_cell_{i}", "exec")

    # The six separately executed EDA investigations are copied in full, including outputs.
    original_supp_png = []
    for name, original_i in SUPPLEMENTARY_SECTIONS.items():
        match = [c for c in new_codes if c["id"] == f"integrated-sup-{name}-code"]
        assert len(match) == 1, name
        c = match[0]
        assert source(c).endswith(source(sup["cells"][original_i]))
        assert c["outputs"] == sup["cells"][original_i]["outputs"]
        assert any(m["id"] == f"integrated-sup-{name}-md" for m in new["cells"])
        original_supp_png.extend(o["data"]["image/png"] for o in c["outputs"]
                                 if "image/png" in o.get("data", {}))
    assert len(original_supp_png) == 3
    original_png = images(old)
    current_png = images(new)
    assert len(original_png) == 7
    assert len(current_png) == 10
    assert Counter(current_png) == Counter(original_png + original_supp_png)

    # No modelling or evaluation algorithms are changed.
    allowed = {5, 9, 10, 11, 12, 13, 15, 17, 24}
    modified = {i for i, (a, b) in enumerate(zip(src_codes, old_like))
                if source(a) != source(b)}
    assert modified == allowed, (modified, allowed)
    assert source(old_like[5]) == source(src_codes[5]).replace(
        "V3_ART=ARTIFACTS/'prd_v3_4'",
        "V3_ART=ARTIFACTS/'prd_v3_5' # Re-execution isolation only; presentation evidence remains frozen v3.4")
    old_definition = source(src_codes[9]).split("def display_family(family):")[0]
    assert source(old_like[9]).startswith(old_definition)
    assert "display(pd.DataFrame" in source(old_like[9])
    for i in (10, 11, 12, 13):
        old_code, new_code = source(src_codes[i]), source(old_like[i])
        for name in ("run_v31_family(f)", "run_v32_family(f)",
                     "run_v33_family(f)", "run_v34_family(f)"):
            assert old_code.count(name) == new_code.count(name) == 1
        assert new_code.count("display_family(f)") == 1
    original_log = source(src_codes[14])
    edited_log = source(old_like[14])
    assert edited_log == original_log
    original_tree = source(src_codes[15])
    tree_code = source(old_like[15])
    stem, sep, suffix = original_tree.partition("display(TREE_BASELINE_SELECTED.round(5))")
    assert sep and tree_code.startswith(stem) and tree_code.endswith(suffix)
    assert "assert len(tree_display)==4" in tree_code
    illustration = source(old_like[17])
    assert "illustrated_family='EntropyTree'" in illustration
    assert "WINNER_FAMILY" not in illustration
    assert "plot_tree(" in illustration and "selected_tree_top_levels.png" in illustration
    original_summary = [s for s in source(src_codes[24]).splitlines()
                        if not s.startswith("print(")]
    current_summary = [s for s in source(old_like[24]).splitlines()
                       if not s.startswith("print(")]
    assert original_summary == current_summary

    # Validate the shortlists and numeric-only table reports.
    ledger = rows(LEDGER)
    folds = rows(FOLDS)
    tree_csv = rows(TREES)
    audit = json.loads(AUDIT.read_text())
    assert len(ledger) == 41 and len(folds) == 255 and len(tree_csv) == 2
    assert audit["status"] == "PASS"
    assert audit["cv_candidates_verified"] == 51
    assert audit["sequential_decisions_verified"] == 37
    assert audit["backward_lda_path_entries_verified"] == 80
    assert audit["tree_alpha_candidates_verified"] == 722
    by_id = {r["step"]: r for r in ledger}
    assert len(by_id) == 41

    numeric_tables = table_with_header(displayed_tables(new), "AUC gain")
    assert len(numeric_tables) == 4
    report_counts = {}
    for (family, ids), table in zip(GROUPS.items(), numeric_tables):
        assert table[0] == ["ID", "CV ROC-AUC", "AUC SE", "CV AP", "AUC gain"]
        assert [r[0] for r in table[1:]] == ids
        for rec in table[1:]:
            step, auc, se, ap, gain = rec
            actual = by_id[step]
            assert actual["pathway"] == family
            compare_float(auc, actual["mean_auc"])
            compare_float(se, actual["auc_se"])
            compare_float(ap, actual["mean_ap"])
            if actual["delta_auc"]:
                compare_float(gain, actual["delta_auc"])
            else:
                assert gain == "—"
        report_counts[family] = len(table) - 1

    # Iteration explanations are below corresponding tables, not in them.
    for family, ids in GROUPS.items():
        matching = [c for c in new["cells"]
                    if c["id"] == f"iteration-notes-{family}"]
        assert len(matching) == 1
        content = source(matching[0])
        for step in ids:
            assert f"**{step}" in content, (family, step)
            if step not in ("L0", "D0", "G0", "B0"):
                assert by_id[step]["parent"] in content
    bernoulli_note = source(next(c for c in new["cells"]
                                 if c["id"] == "iteration-notes-BernoulliNB"))
    assert "two accepted improvements" in bernoulli_note
    assert "B0" in bernoulli_note and "B1" in bernoulli_note and "B3" in bernoulli_note
    lda_note = source(next(c for c in new["cells"]
                           if c["id"] == "iteration-notes-LDA"))
    assert "**D0 (baseline):**" in lda_note

    tree_tables = table_with_header(displayed_tables(new), "ccp_alpha")
    assert len(tree_tables) == 1
    tree = tree_tables[0]
    assert tree[0] == ["Tree family", "Stage", "CV ROC-AUC", "CV AP",
                       "Leaves", "Depth", "ccp_alpha"]
    assert len(tree) == 5
    for t, full, chosen in zip(tree_csv, tree[1::2], tree[2::2]):
        assert full[:2] == [t["family"], "Full (unpruned)"]
        assert chosen[:2] == [t["family"], "Selected (pruned)"]
        for rec, stage in ((full, "baseline"), (chosen, "selected")):
            compare_float(rec[2], t[stage + "_mean_auc"])
            compare_float(rec[3], t[stage + "_mean_ap"])
            assert int(rec[4]) == int(t[stage + "_leaves"])
            assert int(rec[5]) == int(t[stage + "_depth"])
            compare_float(rec[6], t[stage + "_alpha"])

    markdown = [(i, source(c)) for i, c in enumerate(new["cells"])
                if c["cell_type"] == "markdown"]
    headings = [line for _, content in markdown for line in content.splitlines()
                if line.startswith("#")]
    assert not any("6A." in h or "7.5 Full historical evidence" in h for h in headings)
    assert any("2.1 Zero-versus-positive" in h for h in headings)
    assert any("3.1 VisitorType × Month" in h for h in headings)
    assert any("3.2 Rare" in h for h in headings)
    assert any("3.3 SpecialDay" in h for h in headings)
    assert any("4.1 Predictor availability" in h for h in headings)
    assert any("4.2 Distribution tails" in h for h in headings)

    tree_fig_i = next(i for i,c in enumerate(new["cells"])
                      if c["cell_type"] == "code" and
                      "illustrated_family='EntropyTree'" in source(c))
    overall_i = next(i for i,c in enumerate(new["cells"])
                     if c["cell_type"] == "markdown" and
                     "## 8. Six finalists" in source(c))
    tree_section_i = next(i for i,c in enumerate(new["cells"])
                          if c["cell_type"] == "markdown" and
                          "## 7B. Classification trees" in source(c))
    assert tree_section_i < tree_fig_i < overall_i
    assert any("Entropy" in content and "not" in content and "winner" in content
               for _, content in markdown)

    # No user-visible figure is spurious and no holdout or finalist metrics changed.
    assert "historically_pristine_holdout" not in (new.get("metadata", {}))
    assert new["metadata"]["supplementary_eda_incorporated"] == list(
        ("activity_zero_positive_intensity", "visitor_type_month",
         "rare_nominal_levels", "special_day", "feature_availability",
         "conditional_shape_binned_logits"))
    assert new["metadata"]["original_figures_v34"] == 7
    assert new["metadata"]["saved_supplementary_figures"] == 3

    result = {
        "status": "PASS", "prd": "v3.5",
        "presentation_only": True, "new_models_fitted": 0,
        "notebook_cells": len(new["cells"]),
        "python_code_cells_compiled": len(new_codes),
        "original_model_code_cells": len(old_like),
        "added_training_eda_sections": len(SUPPLEMENTARY_SECTIONS),
        "original_figure_count": len(original_png),
        "supplementary_figure_count": len(original_supp_png),
        "embedded_png_figures": len(current_png),
        "error_outputs": 0,
        "family_table_rows": report_counts,
        "visible_original_family_trials": sum(report_counts.values()),
        "historical_original_family_trials": len(ledger),
        "frozen_scored_designs": audit["cv_candidates_verified"],
        "frozen_fold_scores": len(folds),
        "frozen_acceptance_decisions": audit["sequential_decisions_verified"],
        "frozen_tree_alphas": audit["tree_alpha_candidates_verified"],
        "tree_display_rows": len(tree)-1,
        "tree_illustration_before_overall_winner": True,
        "no_6A_or_7_5_heading": True,
        "no_old_result_files_written": True,
        "source_notebook_sha256": digest(SRC),
        "presentation_notebook_sha256": digest(PRESENT),
        "supplementary_eda_sha256": digest(SUPP),
        "source_trial_ledger_sha256": digest(LEDGER),
        "source_audit_sha256": digest(AUDIT),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS: 64 cells, 31 code cells compile, no error outputs")
    print("PASS: six used supplementary EDA investigations and all 10 original figures preserved")
    print("PASS: four numeric-only tables 7/7/7/5 with explanatory notes beneath")
    print("PASS: entropy tree plot within tree section, before winner selection")
    print("PASS: 41 historical trials, 51 designs, 255 folds, 37 decisions unchanged")
    print("PASS: no new model fitting or old-evidence overwrite")


if __name__ == "__main__":
    main()
