# Archived modelling versions (read-only)

**Active version:** [v3.8 PRD](../../PRD_v3.8.md) · [v3.8 notebook](../../online_shoppers_prd_v3_8.ipynb) · [active verification](../../scripts/verify_prd_v3_8.py). Full numerical provenance is the archived v3.7 run and its [PASS audit](../../artifacts/prd_v3_7/v3_7_verification.json).

| Version | Frozen specification | Historical notebook | Numerical evidence | Notes |
|---|---|---|---|---|
| v3.0 | [PRD 3.0](v3.0/PRD_v3.md) | [Executed notebook](v3.0/online_shoppers_prd_v3.ipynb) | [v3.0](../../artifacts/prd_v3/) | Original four-classifier pathway |
| v3.1 | [PRD 3.1](v3.1/PRD_v3.1.md) | [Executed notebook](v3.1/online_shoppers_prd_v3_1.ipynb) | [v3.1](../../artifacts/prd_v3_1/) | Six-family comparison and pruning |
| v3.2 | [PRD 3.2](v3.2/PRD_v3.2.md) | [Executed notebook](v3.2/online_shoppers_prd_v3_2.ipynb) | [v3.2](../../artifacts/prd_v3_2/) | Eleven anchored probes |
| v3.3 | [PRD 3.3](v3.3/PRD_v3.3.md) | [Executed notebook](v3.3/online_shoppers_prd_v3_3.ipynb) | [v3.3](../../artifacts/prd_v3_3/) | Seven further probes |
| v3.4 | [PRD 3.4](v3.4/PRD_v3.4.md) | [Executed notebook](v3.4/online_shoppers_prd_v3_4.ipynb) | [v3.4](../../artifacts/prd_v3_4/) | Original frozen training result source for v3.5 |
| v3.5 | [PRD 3.5](v3.5/PRD_v3.5.md) | [Executed notebook](v3.5/online_shoppers_prd_v3_5.ipynb) | [v3.5](../../artifacts/prd_v3_5/) | Curated EDA/presentation of v3.4 results; [presentation auditor](v3.5/verify_prd_v3_5_presentation.py) archived |
| v3.6 | [PRD 3.6](v3.6/PRD_v3.6.md) | [Executed notebook](v3.6/online_shoppers_prd_v3_6.ipynb) | [v3.6](../../artifacts/prd_v3_6/) | Corrected sequential one-SE selection; [execution verifier](v3.6/execute_prd_v3_6.py) and [selection implementation](v3.6/prd_v3_6_sequential.py) archived |

| v3.7 | [PRD 3.7](v3.7/PRD_v3.7.md) | [Executed notebook](v3.7/online_shoppers_prd_v3_7.ipynb) | [v3.7 PASS](../../artifacts/prd_v3_7/v3_7_verification.json) | Fully executed computational reference for v3.8; [historical verifier](v3.7/run_verify_prd_v3_7.py) and [retirement manifest](v3.7/RETIREMENT_MANIFEST.json) |

The earlier [v3.0 notebook builder](v3.0/build_prd_v3.py) is retained as a historical source, not an active entry point. Archived notebooks are preserved as originally executed; they are not automatically rerun. The older internal file paths have not been cosmetically rewritten, to preserve the original contents and allow byte-for-byte history comparison. Use these index links to navigate between versions.

**Inherited numerical result for v3.8:** [v3.7 audit PASS](../../artifacts/prd_v3_7/v3_7_verification.json). The archived versions retain their historical results and assumptions; the v3.4 audit, v3.5 presentation audit and v3.6 audit remain available under their original `artifacts/` paths.
