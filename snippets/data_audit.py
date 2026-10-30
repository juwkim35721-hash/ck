#!/usr/bin/env python3
"""
Universal Data Auditor for Cofa-Probe (CSV / JSON / JSONL)
Usage: python3 /tmp/cofa-kit/snippets/data_audit.py <path_to_data_file>
"""
import csv
import json
import math
import os
import sys
from collections import Counter

def audit_rows(rows, label):
    print(f"=== 📊 DATA AUDIT REPORT: {label} ===")
    print(f"Total Rows: {len(rows)}")
    if not rows:
        return
    cols = list(rows[0].keys())
    print(f"Columns ({len(cols)}): {cols}\n")
    for c in cols:
        vals = [r.get(c) for r in rows]
        nulls = sum(1 for v in vals if v is None or str(v).strip() in ("", "null", "None", "NaN", "nan", "N/A"))
        num_vals = []
        for v in vals:
            if v is not None and str(v).strip() not in ("", "null", "None", "NaN", "nan", "N/A"):
                try:
                    fv = float(v)
                    if not math.isnan(fv) and not math.isinf(fv):
                        num_vals.append(fv)
                except ValueError:
                    pass
        if len(num_vals) > len(rows) * 0.5 and num_vals:
            num_vals.sort()
            p50 = num_vals[len(num_vals) // 2]
            negs = sum(1 for x in num_vals if x < 0)
            zeros = sum(1 for x in num_vals if x == 0)
            print(f"  - [{c}] (Numeric): nulls={nulls}, min={num_vals[0]}, median={p50}, max={num_vals[-1]}, negatives={negs}, zeros={zeros}")
        else:
            non_null = [str(v).strip() for v in vals if v is not None and str(v).strip() != ""]
            top = Counter(non_null).most_common(5)
            dups = len(non_null) - len(set(non_null))
            print(f"  - [{c}] (Categorical/Text): nulls={nulls}, unique={len(set(non_null))}, duplicates={dups}, top5={top}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 data_audit.py <file.csv|file.json|file.jsonl>")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)
    if path.endswith(".csv"):
        with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            audit_rows(list(reader), path)
    elif path.endswith(".jsonl"):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            rows = [json.loads(line) for line in f if line.strip()]
            audit_rows(rows, path)
    elif path.endswith(".json"):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
            if isinstance(data, list):
                audit_rows(data, path)
            elif isinstance(data, dict):
                print(f"JSON Dict Keys: {list(data.keys())}")
                for k, v in data.items():
                    if isinstance(v, list) and v and isinstance(v[0], dict):
                        audit_rows(v, f"{path}[{k}]")

if __name__ == "__main__":
    main()
