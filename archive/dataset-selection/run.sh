#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "=== self test, no network needed ==="
python bakeoff.py --self-test --outdir results_selftest
echo
echo "=== real run ==="
python bakeoff.py --outdir results
