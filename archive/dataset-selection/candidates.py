#!/usr/bin/env python3
"""Additional candidate datasets for the Topic 2 bake-off.

Each adapter returns (X, y, suspects, notes, origin) in the same shape
bakeoff.adapt_taiwan / adapt_acra return, so report_eval.run_dataset can score
them under identical discipline.

`suspects` are columns declared as possible leakage BEFORE any modelling. They
are measured (they contribute to the leakage premium) and then dropped, exactly
as bakeoff.py treats the ACRA suspects. Declaring a suspect is a judgement call,
so each one carries its reason inline.

ucimlrepo's CSV endpoint is currently broken for every id tested (it raises
DatasetNotFoundError while metadata still resolves), so these read the UCI
static data_url directly via requests, which uses certifi.
"""

import io, os
import numpy as np
import pandas as pd
import requests

UCI = "https://archive.ics.uci.edu/static/public/{id}/data.csv"


def fetch_uci(ds_id, cache_dir=".uci_cache"):
    """Download and cache one UCI dataset as a DataFrame."""
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, f"uci_{ds_id}.csv")
    if not (os.path.exists(path) and os.path.getsize(path) > 500):
        r = requests.get(UCI.format(id=ds_id), timeout=600)
        r.raise_for_status()
        with open(path, "wb") as fh:
            fh.write(r.content)
    return pd.read_csv(path, low_memory=False), f"UCI id={ds_id} ({path})"


def _as_nominal(df, cols):
    """Force integer-coded nominal IDs to string.

    bakeoff.split_types calls a numeric column categorical only when it has
    <= CAT_CARD_MAX distinct levels. Codes like TrafficType have more levels
    than that and would otherwise be scaled as if they were quantities, which
    they are not. Casting to string states the intent explicitly.
    """
    for c in cols:
        if c in df:
            df[c] = df[c].astype(str)
    return df


# ---------------------------------------------------------------------------
def adapt_online_shoppers(cache_dir=".uci_cache"):
    """Online Shoppers Purchasing Intention (UCI 468). Turkish e-commerce."""
    df, src = fetch_uci(468, cache_dir)
    y = df["Revenue"].astype(bool).astype(int)
    X = df.drop(columns=["Revenue"])
    X = _as_nominal(X, ["OperatingSystems", "Browser", "Region", "TrafficType"])
    # PageValues is a Google Analytics metric averaged over sessions that
    # completed a transaction. It is partly derived from the outcome, so it is
    # declared a suspect and priced rather than silently used.
    suspects = ["PageValues"]
    notes = [f"source {src}", f"rows {len(X):,}",
             "suspect PageValues: GA metric computed from converting sessions",
             "OperatingSystems/Browser/Region/TrafficType cast to nominal"]
    return X, y, suspects, notes, "Turkey (Asia, transcontinental)"


def adapt_contraceptive(cache_dir=".uci_cache"):
    """Contraceptive Method Choice (UCI 30). 1987 Indonesian survey."""
    df, src = fetch_uci(30, cache_dir)
    # Original target is 3-class: 1 no-use, 2 long-term, 3 short-term.
    # Collapsed to the binary question the survey is actually about.
    y = (df["contraceptive_method"] != 1).astype(int)
    X = df.drop(columns=["contraceptive_method"])
    X = _as_nominal(X, ["husband_occupation"])
    notes = [f"source {src}", f"rows {len(X):,}",
             "3-class target collapsed to use (2,3) vs no-use (1)",
             "no leakage suspects: every field is demographic, measured at survey time"]
    return X, y, [], notes, "Indonesia (Asia)"


def adapt_bank_marketing(cache_dir=".uci_cache"):
    """Bank Marketing (UCI 222). Portuguese retail bank campaigns.

    Included deliberately as a NON-Asian structural control. It is the closest
    public match to this brief's requirements, so it answers "is Taiwan actually
    good, or merely the best of a weak field?".
    """
    df, src = fetch_uci(222, cache_dir)
    y = (df["y"].astype(str).str.strip().str.lower() == "yes").astype(int)
    X = df.drop(columns=["y"])
    # 'duration' is the length of the call being predicted. It is unknown until
    # the call ends, by which point the outcome is known. UCI's own page says to
    # discard it for any realistic model. Declared, measured, dropped.
    suspects = ["duration"]
    notes = [f"source {src}", f"rows {len(X):,}",
             "suspect duration: call length, unknown before the outcome exists",
             "NOT Asian - included as a structural control"]
    return X, y, suspects, notes, "Portugal (CONTROL, not Asian)"


def adapt_taiwan_bankruptcy(cache_dir=".uci_cache"):
    """Taiwanese Bankruptcy Prediction (UCI 572). TEJ database, 1999-2009."""
    df, src = fetch_uci(572, cache_dir)
    df.columns = [c.strip() for c in df.columns]
    y = df["Bankrupt?"].astype(int)
    X = df.drop(columns=["Bankrupt?"])
    notes = [f"source {src}", f"rows {len(X):,}",
             "95 accounting ratios, all continuous",
             "no suspects: ratios are drawn from filings predating the event"]
    return X, y, [], notes, "Taiwan (Asia)"


CANDIDATES = {
    "Online shoppers intent": adapt_online_shoppers,
    "Contraceptive choice":   adapt_contraceptive,
    "Bank marketing":         adapt_bank_marketing,
    "Taiwan bankruptcy":      adapt_taiwan_bankruptcy,
}
