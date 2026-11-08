#!/usr/bin/env python3
"""Execute and independently inspect the PRD v3.7 notebook.

This script does not reimplement the statistical model. It runs the inherited
v3.6 computational notebook with the v3.7 amendments and independently
verifies the saved decision lineage, aliases and result invariants.
"""
from __future__ import annotations
import argparse
import ast
import json
import math
import os
from pathlib import Path
import pandas as pd
import nbformat

ROOT=Path(__file__).resolve().parents[1]
NOTEBOOK=ROOT/"online_shoppers_prd_v3_7.ipynb"
ART=ROOT/"artifacts"/"prd_v3_7"
ALIASES={
    "Logit": ["L0","L1","L3","L4","L10","L13","L14"],
    "LDA": ["D0","D1","D3","D4","D9","D11","D15"],
    "GaussianNB":["G0","G2","G3","G4","G7","G8","G9"],
    "BernoulliNB":["B0","B1","B2","B3","B4","B5","B6"],
}

def verify_static():
    nb=nbformat.read(NOTEBOOK,as_version=4)
    nbformat.validate(nb)
    sources=[c.source for c in nb.cells]
    merged="\n".join(sources)
    assert len(nb.cells)>=60, f"Expected v3.5 restored EDA and inherited v3.6: {len(nb.cells)} cells"
    for i,c in enumerate(nb.cells):
        if c.cell_type=="code":
            ast.parse(c.source,filename=f"{NOTEBOOK.name}:cell:{i}")
    for phrase in ("### 2.1 Zero-versus-positive", "### 3.1 VisitorType",
                   "### 3.2 Rare", "### 3.3 SpecialDay",
                   "### 4.1 Predictor availability", "### 4.2 Distribution tails",
                   "### EDA-to-experiment bridge",
                   "product_composite", "('B5'", "('B6'",
                   "Retained after iteration"):
        assert phrase in merged, f"Missing v3.7 requirement: {phrase}"
    idx_tree=next(i for i,s in enumerate(sources) if "## 7B. Classification trees" in s)
    idx_entropy=next(i for i,s in enumerate(sources) if "### 7B.1 Pruned Entropy" in s)
    idx_six=next(i for i,s in enumerate(sources) if "## 8. Six finalists" in s)
    assert idx_tree < idx_entropy < idx_six
    print(f"PASS static notebook: {len(nb.cells)} cells, "
          f"{sum(c.cell_type=='code' for c in nb.cells)} parseable code cells; Entropy tree correctly placed")
    return nb

def verify_results(nb):
    for i,c in enumerate(nb.cells):
        if c.cell_type=="code":
            assert c.execution_count is not None, f"Unexecuted code cell {i}"
            assert not [o for o in c.get("outputs",[]) if o.output_type=="error"],f"Error output in cell {i}"
    required=["all_attempts_ledger.csv","all_attempt_fold_scores.csv",
              "presentation_id_map.csv","six_finalists.csv",
              "tree_full_vs_selected.csv","run_metadata.json"]
    for name in required:
        assert (ART/name).is_file(),f"Missing {name}"
    ledger=pd.read_csv(ART/"all_attempts_ledger.csv")
    mapping=pd.read_csv(ART/"presentation_id_map.csv")
    finalists=pd.read_csv(ART/"six_finalists.csv")
    tree=pd.read_csv(ART/"tree_full_vs_selected.csv")
    run=json.loads((ART/"run_metadata.json").read_text())
    audit=run["training_evidence_audit"]
    assert audit["status"]=="PASS",audit
    assert len(ledger)==43
    assert len(ledger[ledger.status=="SCORED"])==38
    assert len(ledger[ledger.status=="SKIPPED_INAPPLICABLE"])==5
    assert set(ledger.loc[ledger.status=="SKIPPED_INAPPLICABLE","step"])=={"D5","D6","D8","G5","G6"}
    assert len(mapping)==28
    assert len(finalists)==6 and finalists.pathway.nunique()==6
    assert len(tree)==2 # two families, with full+pruned metrics per record
    for fam, original in ALIASES.items():
        rows=mapping.loc[mapping.family==fam].sort_values("display_ordinal")
        prefix=rows.display_id.iloc[0][0]
        assert rows.display_id.tolist()==[f"{prefix}{j}" for j in range(7)],fam
        assert rows.original_trial_id.tolist()==original
        assert set(rows.original_trial_id).issubset(set(ledger[ledger.status=="SCORED"].step)),fam
        stage=ledger[ledger.pathway==fam].retained_after_step
        accepted_ids={x.split(" | ")[0] for x in stage if not x.startswith("Operational16")}
        assert accepted_ids.issubset(set(original)),(fam,accepted_ids-set(original))
        for row in rows.itertuples(index=False):
            observed=ledger[(ledger.pathway==fam)&(ledger.step==row.original_trial_id)].iloc[0]
            true_id=prefix+"0" if observed.retained_after_step.startswith("Operational16") else observed.retained_after_step.split(" | ")[0]
            mapping_by_id=dict(zip(rows.original_trial_id,rows.display_id))
            assert row.retained_original_id==true_id
            assert row.retained_display_id==mapping_by_id[true_id]
    assert set(ledger[ledger.pathway=="BernoulliNB"].step)=={f"B{i}" for i in range(7)}
    assert ledger.set_index("step").loc["B5","status"]=="SCORED"
    assert ledger.set_index("step").loc["B6","status"]=="SCORED"
    assert not run["historically_pristine_holdout"]
    print("PASS numerical lineage: 43 planned / 38 scored / 5 skipped; 28 aliases; six finalists")
    return {"status":"PASS","notebook":NOTEBOOK.name,"planned":43,"scored":38,
            "skipped":5,"displayed":28,"finalists":finalists[["pathway","candidate","mean_auc","mean_ap"]].to_dict("records"),
            "training_evidence_audit":audit}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--run",action="store_true",help="Execute notebook from beginning, then audit")
    parser.add_argument("--verify",action="store_true",help="Audit existing executed notebook")
    args=parser.parse_args()
    nb=verify_static()
    if args.run:
        from nbclient import NotebookClient
        import time
        start=time.monotonic()
        os.environ["MPLBACKEND"]="Agg"
        nb=NotebookClient(nb,timeout=3600,kernel_name="python3",allow_errors=False,
             resources={"metadata":{"path":str(ROOT)}}).execute()
        nbformat.write(nb,NOTEBOOK)
        print(f"Executed v3.7 in {time.monotonic()-start:.1f}s")
    if args.verify or args.run:
        result=verify_results(nb)
        ART.mkdir(parents=True,exist_ok=True)
        (ART/"v3_7_verification.json").write_text(json.dumps(result,indent=2,default=str)+"\n")
        print("VERIFIED v3.7 PASS")

if __name__=="__main__":
    main()
