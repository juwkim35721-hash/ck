---
name: cofa-eda
description: Data and log auditing skill. Runs /tmp/cofa-kit/snippets/data_audit.py against CSV/JSON/JSONL/SQLite/log files to uncover missing values, negative outliers, duplicates, and schema traps.
---
# Cofa-EDA: Rapid Data & Anomaly Audit Workflow

1. Run `python3 /tmp/cofa-kit/snippets/data_audit.py` on all dataset files in `~/workspace` (and inspect sample lines).
2. Summarize findings in Korean:
   - Exact row/column counts, data types, and timestamp ranges.
   - Missing value (`Null`/`NaN`/empty) counts per field.
   - Corrupted or extreme outliers (e.g., `-999`, negative numbers, spikes, malformed dates, duplicate IDs).
   - Concrete preprocessing and filtering rules to apply in code (and any edge case to confirm with `업무 담당자`).
