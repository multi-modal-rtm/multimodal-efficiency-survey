"""
Validate consistency across rubric, schema, and CSV files.
Run after any structural change to the repository.
Exit code 0 if all checks pass, 1 if any errors found.
"""

import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).parent.parent
ERRORS = []

# Check 1: All CSVs in coding/ have identical column structure
csvs = sorted((REPO / "coding").rglob("*.csv"))
if csvs:
    reference_cols = pd.read_csv(csvs[0]).columns.tolist()
    reference_path = csvs[0]
    for csv_path in csvs[1:]:
        cols = pd.read_csv(csv_path).columns.tolist()
        if cols != reference_cols:
            ERRORS.append(
                f"Column mismatch: {csv_path} differs from {reference_path}\n"
                f"  Reference: {reference_cols}\n"
                f"  This file: {cols}"
            )

# Check 2: Schema enum values appear in rubric text
schema = json.load(open(REPO / "coding" / "schema.json"))
rubric_text = (REPO / "rubric" / "rubric_v1.md").read_text()

def collect_enums(node, path=""):
    if isinstance(node, dict):
        if "enum" in node:
            yield path, node["enum"]
        for k, v in node.items():
            yield from collect_enums(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from collect_enums(v, f"{path}[{i}]")

UNIVERSAL_CODES = {"NA", "NR", "other-specify", "none-reported", "none"}

for enum_path, enum_values in collect_enums(schema):
    for value in enum_values:
        if value in UNIVERSAL_CODES:
            continue
        if value not in rubric_text:
            ERRORS.append(
                f"Enum value '{value}' (at {enum_path}) not found in rubric_v1.md"
            )

# Report
if ERRORS:
    print(f"FOUND {len(ERRORS)} CONSISTENCY ERRORS:\n")
    for err in ERRORS:
        print(f"  - {err}\n")
    exit(1)
else:
    print(f"All consistency checks passed.")
    print(f"  - {len(csvs)} CSV file(s) checked for column alignment")
    print(f"  - Schema enum values cross-referenced against rubric")
