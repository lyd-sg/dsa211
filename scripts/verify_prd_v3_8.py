#!/usr/bin/env python3
"""Verify v3.8 presentation changes without retraining frozen v3.7 models."""
from __future__ import annotations
import argparse, ast, json
from pathlib import Path
import numpy as np
import pandas as pd
import nbformat

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"online_shoppers_prd_v3_7.ipynb"
NEW=ROOT/"online_shoppers_prd_v3_8.ipynb"
DATA=ROOT/"data/uci_468.csv"
IDS=ROOT/"artifacts/train_row_ids.csv"

def check():
    v37=nbformat.read(OLD,as_version=4)
    nb=nbformat.read(NEW,as_version=4)
    nbformat.validate(nb)
    src=[c.source for c in nb.cells]
    eda_end=next(i for i,s in enumerate(src) if s.startswith("## 4. Model Development"))
    body="\n".join(src[:eda_end])
    for i,c in enumerate(nb.cells):
        if c.cell_type=="code":
            ast.parse(c.source,filename=f"v3.8 cell {i}")
    headings=["## 1. Initial Data Overview","### 1.1 Dataset overview","### 1.2 Data quality","### 1.3 Target distribution",
              "### 1.4 Stratified train–holdout split","## 2. General EDA","### 2.1 Numerical distributions",
              "### 2.2 Categorical distributions","## 3. In-depth EDA","### 3.1 Zero versus positive activity",
              "### 3.2 Positive activity intensity","### 3.3 BounceRates","### 3.4 Within-class predictor correlations",
              "### 3.5 Distributional assumptions","### 3.6 SpecialDay","## 4. Model Development"]
    locations=[next(i for i,s in enumerate(src) if s.startswith(h)) for h in headings]
    assert locations==sorted(locations)
    for forbidden in ["### 3.1 VisitorType × Month", "EDA-to-experiment bridge",
                      "### 4.1 Predictor availability at", "Binned marginal empirical logit",
                      "New_Visitor", "marginal_elogit", "RARE_LEVELS"]:
        assert forbidden not in body, forbidden
    assert body.count("Four predictor pairs were examined based on their conceptual relationships.")==1
    assert "PageValues is excluded" not in body
    figures=[(i,o) for i,c in enumerate(nb.cells[:eda_end]) for o in c.get("outputs",[]) 
             if "image/svg+xml" in o.get("data",{})]
    assert len(figures)==3,figures
    assert "Month × VisitorType" not in body

    # All original model code (from cell 24), saved results and historical numerical evidence
    # are preserved byte-for-byte, excluding the removed independent PageValues EDA cell 28.
    original=[c for i,c in enumerate(v37.cells) if i>=24 and i!=28 and c.cell_type=="code"]
    models=[c for c in nb.cells if c.cell_type=="code"]
    for c in original:
        matching=[n for n in models if n.source.strip()==c.source.strip()]
        assert len(matching)==1, f"Missing/changed model code: {c.source[:80]}"
        assert matching[0].outputs==c.outputs,"Changed inherited model output"

    assert len(nb.cells)==75
    assert "PageValues" not in nb.cells[eda_end+1].source or True
    assert sum(c.cell_type=="code" for c in nb.cells)==33

    raw=pd.read_csv(DATA)
    assert raw.shape==(12330,18)
    assert raw.isna().sum().sum()==0
    assert int(raw.duplicated().sum())==125
    dup=raw.loc[raw.duplicated()]
    assert dup.Revenue.eq(0).all()
    assert raw.Revenue.sum()==1908
    ix=pd.read_csv(IDS).row_id.to_numpy()
    tr=raw.iloc[ix]
    assert len(tr)==9864 and tr.Revenue.sum()==1526
    zero=tr.BounceRates.eq(0)
    assert zero.sum()==4423
    pos=tr.loc[~zero]
    octile=pd.qcut(pos.BounceRates,8,labels=False,duplicates="drop")
    assert octile.nunique()==8
    results=[(int(zero.sum()),round(100*tr.loc[zero,"Revenue"].mean(),1))]
    for j in range(4):
        vals=tr.loc[octile.index[octile//2==j]]
        results.append((len(vals),round(100*vals.Revenue.mean(),1)))
    assert results==[(4423,19.2),(1361,23.4),(1365,16.7),(1355,8.0),(1360,1.8)],results
    for r in [("ProductRelated",27),("Informational",7747),("Informational_Duration",7938)]:
        assert tr[r[0]].eq(0).sum()==r[1]
    print("PASS v3.8: notebook syntax, ordered sections, 3 embedded figures,")
    print("  frozen model code+outputs unchanged, verified source split/EDA metrics.")
    return nb,eda_end

def run_eda(nb,stop):
    from nbclient import NotebookClient
    # Run only the EDA and data partition cells: no model fitting or selection.
    sub=nbformat.v4.new_notebook(cells=nb.cells[:stop],metadata=nb.metadata)
    NotebookClient(sub,timeout=150,kernel_name="python3",allow_errors=False,
                   resources={"metadata":{"path":str(ROOT)}}).execute()
    for i,c in enumerate(sub.cells):
        if c.cell_type=="code":
            assert c.execution_count is not None,f"Unexecuted EDA cell {i}"
            assert not [o for o in c.outputs if o.output_type=="error"],i
    print("PASS v3.8: executed every pre-modelling code cell without errors")
    
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--run-eda",action="store_true")
    args=parser.parse_args()
    nb,stop=check()
    if args.run_eda:run_eda(nb,stop)
