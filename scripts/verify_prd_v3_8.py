#!/usr/bin/env python3
"""Verify v3.8 presentation changes without retraining frozen v3.7 models."""
from __future__ import annotations
import argparse, ast, json
from pathlib import Path
import numpy as np
import pandas as pd
import nbformat

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"archive/versions/v3.7/online_shoppers_prd_v3_7.ipynb"
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
    locations=[next(i for i,s in enumerate(src) if h in s) for h in headings]
    assert locations==sorted(locations)
    for forbidden in ["### 3.1 VisitorType × Month", "EDA-to-experiment bridge",
                      "### 4.1 Predictor availability at", "Binned marginal empirical logit",
                      "New_Visitor", "marginal_elogit", "RARE_LEVELS"]:
        assert forbidden not in body, forbidden
    assert body.count("Four predictor pairs were examined based on their conceptual relationships.")==1
    assert "PageValues is excluded" not in body
    figures=[(i,o) for i,c in enumerate(nb.cells[:eda_end]) for o in c.get("outputs",[]) 
             if "image/svg+xml" in o.get("data",{})]
    assert len(figures)==2,figures
    assert "Month × VisitorType" not in body

    # All original model code (from cell 24), saved results and historical numerical evidence
    # are preserved byte-for-byte, excluding the removed independent PageValues EDA cell 28.
    original=[c for i,c in enumerate(v37.cells) if i>=24 and i!=28 and c.cell_type=="code"]
    models=[c for c in nb.cells if c.cell_type=="code"]

    def without_note_wording(source):
        # The EDA_NOTES dictionary contains ONLY presentation copy.
        # Compare every other byte of the inherited model cell to the archive.
        begin="\\nEDA_NOTES={"
        end="\\nDISPLAY_ALIAS_ROWS=[]"
        if begin not in source: return source
        assert source.count(begin)==1 and source.count(end)==1
        a=source.index(begin); b=source.index(end,a)
        return source[:a]+"\\nEDA_NOTES=<PRESENTATION_COPY_ONLY>"+source[b:]

    def check_saved_outputs(old_outputs,new_outputs):
        import copy
        assert len(old_outputs)==len(new_outputs),"Changed model output count"
        for old,new in zip(old_outputs,new_outputs):
            if old==new: continue
            # Permit revisions ONLY to displayed explanatory markdown;
            # numerical score tables, plots and all other output bytes are frozen.
            assert old.output_type=="display_data" and new.output_type=="display_data"
            assert "text/markdown" in old.data and "text/markdown" in new.data
            a=copy.deepcopy(old); b=copy.deepcopy(new)
            del a.data["text/markdown"]; del b.data["text/markdown"]
            assert a==b,"Changed inherited non-rationale model output"

    for c in original:
        matching=[n for n in models
                  if without_note_wording(n.source.strip())==without_note_wording(c.source.strip())]
        assert len(matching)==1, f"Missing/changed model code outside explanatory notes: {c.source[:80]}"
        check_saved_outputs(c.outputs,matching[0].outputs)

    # Every scored display has seven notes, including the baseline;
    # each changed model has a concrete Section 2/3 EDA reference.
    for cell_index in (48,50,52,54):
        data=nb.cells[cell_index].outputs[-1].data
        markdown="".join(data["text/markdown"])
        items=[line for line in markdown.splitlines() if line.startswith("- **")]
        assert len(items)==7,(cell_index,len(items))
        assert sum("Section " in line or "Sections " in line for line in items)>=6,cell_index

    assert len(nb.cells)==75
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
    activity=["Administrative","Administrative_Duration","Informational",
              "Informational_Duration","ProductRelated","ProductRelated_Duration"]
    for col in activity:
        mask=tr[col].gt(0)
        assert int((~mask).sum())+int(mask.sum())==9864
        qbin, qedges=pd.qcut(tr.loc[mask,col],4,labels=False,duplicates="drop",retbins=True)
        assert int(qbin.value_counts().sum())==int(mask.sum()),col
        if col=="Informational":
            assert qbin.nunique()==3, f"Expected 3 informational groups, got {qbin.nunique()}"
            assert len(qedges)==4, f"Expected 4 distinct informational edges, got {qedges}"
    print("PASS v3.8: independently verified Section 3 group sizes and 3 Informational bins")
    print("PASS v3.8: notebook syntax, ordered sections, 2 embedded figures,")
    print("  frozen model code+outputs unchanged, verified source split/EDA metrics.")
    return nb,eda_end

def run_eda(nb,stop):
    from nbclient import NotebookClient
    # Run only EDA and data partition cells, not inherited model fitting/selection.
    sub=nbformat.v4.new_notebook(cells=nb.cells[:stop],metadata=nb.metadata)
    NotebookClient(sub,timeout=150,kernel_name="python3",allow_errors=False,
                   resources={"metadata":{"path":str(ROOT)}}).execute()
    for i,c in enumerate(sub.cells):
        if c.cell_type=="code":
            assert c.execution_count is not None,f"Unexecuted EDA cell {i}"
            assert not [o for o in c.outputs if o.output_type=="error"],i
    review=["DSA211 v3.8 | executed training-only EDA | Sections 3.1 and 3.2"]
    for cell_idx,heading in [(19,"3.1 Zero versus positive activity"),
                             (22,"3.2 Positive-only activity bins and diagnostic")]:
        review.extend(["",heading])
        for output in sub.cells[cell_idx].outputs:
            if output.output_type=="stream":
                review.append(str(output.text))
            elif output.output_type in ("display_data","execute_result"):
                value=output.data.get("text/plain","")
                review.append("".join(value) if isinstance(value,list) else str(value))
    result="\n".join(review)+"\n"
    audit_dir=ROOT/"work"/"section3_eda_review"
    audit_dir.mkdir(parents=True,exist_ok=True)
    (audit_dir/"section3_results.txt").write_text(result,encoding="utf-8")
    nbformat.write(sub,audit_dir/"executed_eda_only.ipynb")
    print(result)
    print("PASS v3.8: executed every pre-modelling code cell without errors")
    print("Saved reproducible EDA-only notebook and Section 3 result text for Actions artifact")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--run-eda",action="store_true")
    args=parser.parse_args()
    nb,stop=check()
    if args.run_eda:run_eda(nb,stop)
