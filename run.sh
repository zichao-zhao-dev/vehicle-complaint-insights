#!/usr/bin/env bash
set -euo pipefail

python fetch.py
python load.py
python split_components.py
sqlite3 data/complaints.db < analysis.sql > reports/summary.txt

echo "Done. Report written to reports/summary.txt"
