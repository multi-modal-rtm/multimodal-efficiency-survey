#!/usr/bin/env python3
"""
Compute inter-coder reliability from two coded CSVs.

Primary-label axes  → Cohen's κ  (sklearn)
Multi-label axes    → Krippendorff's α  (krippendorff package)

Usage:
    python reliability.py CODER_A_CSV CODER_B_CSV [--output REPORT.md]
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score
import krippendorff


# ── Axis definitions ──────────────────────────────────────────────────────────

PRIMARY_AXES = [
    "axis_1a_encoder_config_primary",
    "axis_1b_fusion_mechanism_primary",
    "axis_2_adaptation_primary",
    "axis_3a_optimizer_primary",
    "axis_4a_precision_primary",
    "axis_4b_sparsity_primary",
    "axis_5_topology_primary",
]

MULTILABEL_AXES = [
    "axis_1c_modality_set",
    "axis_3b_memory_techniques",
]

STRONG_THRESHOLD = 0.70
ACCEPTABLE_THRESHOLD = 0.60


# ── Helpers ───────────────────────────────────────────────────────────────────

def _interpret(score, strong=STRONG_THRESHOLD, acceptable=ACCEPTABLE_THRESHOLD):
    if score is None:
        return "N/A"
    if score >= strong:
        return "strong"
    if score >= acceptable:
        return "acceptable"
    return "BELOW THRESHOLD"


def _pipe_to_set(value):
    if not isinstance(value, str) or value.strip() == "":
        return set()
    return {v.strip() for v in value.split("|") if v.strip()}


# ── Per-axis computations ─────────────────────────────────────────────────────

def compute_primary_kappa(df_a, df_b, axis):
    """Return (kappa, n, disagreements_list) for a primary-label axis."""
    merged = (
        df_a[["paper_id", axis]]
        .merge(df_b[["paper_id", axis]], on="paper_id", suffixes=("_a", "_b"))
        .dropna(subset=[f"{axis}_a", f"{axis}_b"])
    )
    n = len(merged)
    if n < 2:
        return None, n, []

    labels_a = merged[f"{axis}_a"].tolist()
    labels_b = merged[f"{axis}_b"].tolist()
    all_labels = sorted(set(labels_a + labels_b))

    kappa = cohen_kappa_score(labels_a, labels_b, labels=all_labels)

    disagreements = [
        {"paper_id": row["paper_id"], "coder_A": row[f"{axis}_a"], "coder_B": row[f"{axis}_b"]}
        for _, row in merged.iterrows()
        if row[f"{axis}_a"] != row[f"{axis}_b"]
    ]
    return kappa, n, disagreements


def compute_multilabel_alpha(df_a, df_b, axis):
    """Return (alpha, n, disagreements_list) for a multi-label axis."""
    merged = (
        df_a[["paper_id", axis]]
        .merge(df_b[["paper_id", axis]], on="paper_id", suffixes=("_a", "_b"))
        .dropna(subset=[f"{axis}_a", f"{axis}_b"])
    )
    n = len(merged)
    if n < 2:
        return None, n, []

    all_labels = set()
    for val in merged[f"{axis}_a"].tolist() + merged[f"{axis}_b"].tolist():
        all_labels.update(_pipe_to_set(val))
    all_labels = sorted(all_labels)

    if not all_labels:
        return None, n, []

    def encode(series):
        rows = []
        for val in series:
            active = _pipe_to_set(val)
            rows.append([1 if lbl in active else 0 for lbl in all_labels])
        return rows

    data_a = encode(merged[f"{axis}_a"])
    data_b = encode(merged[f"{axis}_b"])

    # Flatten to (2 coders × n_papers*n_labels) for nominal Krippendorff's α
    flat_a = [v for row in data_a for v in row]
    flat_b = [v for row in data_b for v in row]
    reliability_data = np.array([flat_a, flat_b], dtype=float)

    alpha = krippendorff.alpha(
        reliability_data=reliability_data, level_of_measurement="nominal"
    )

    disagreements = [
        {"paper_id": row["paper_id"], "coder_A": row[f"{axis}_a"], "coder_B": row[f"{axis}_b"]}
        for _, row in merged.iterrows()
        if _pipe_to_set(row[f"{axis}_a"]) != _pipe_to_set(row[f"{axis}_b"])
    ]
    return alpha, n, disagreements


# ── Report generation ─────────────────────────────────────────────────────────

def build_markdown_report(results_primary, results_multilabel, path_a, path_b):
    lines = [
        "# Inter-Coder Reliability Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Coder A: `{path_a}`",
        f"Coder B: `{path_b}`",
        f"Thresholds: ≥ {STRONG_THRESHOLD} = strong, ≥ {ACCEPTABLE_THRESHOLD} = acceptable",
        "",
        "## Primary Axes — Cohen's κ",
        "",
        "| Axis | κ | n papers | Interpretation |",
        "|------|---|----------|----------------|",
    ]
    for r in results_primary:
        k = f"{r['score']:.3f}" if r["score"] is not None else "N/A"
        lines.append(f"| {r['axis']} | {k} | {r['n']} | {r['interpretation']} |")

    lines += [
        "",
        "## Multi-label Axes — Krippendorff's α",
        "",
        "| Axis | α | n papers | Interpretation |",
        "|------|---|----------|----------------|",
    ]
    for r in results_multilabel:
        a = f"{r['score']:.3f}" if r["score"] is not None else "N/A"
        lines.append(f"| {r['axis']} | {a} | {r['n']} | {r['interpretation']} |")

    all_disagree = [
        (r["axis"], d)
        for r in results_primary + results_multilabel
        for d in r.get("disagreements", [])
    ]
    lines += ["", "## Disagreements", ""]
    if all_disagree:
        lines += [
            "| paper_id | Axis | Coder A | Coder B |",
            "|----------|------|---------|---------|",
        ]
        for axis, d in all_disagree:
            lines.append(
                f"| {d['paper_id']} | {axis} | {d['coder_A']} | {d['coder_B']} |"
            )
    else:
        lines.append("*(none)*")

    return "\n".join(lines) + "\n"


def print_stdout_report(results_primary, results_multilabel):
    col = 46
    sep = "-" * 78

    print("\n=== PRIMARY AXES -- Cohen's kappa ===")
    print(f"{'Axis':<{col}} {'kappa':>7}  {'n':>5}  Interpretation")
    print(sep)
    for r in results_primary:
        k = f"{r['score']:.3f}" if r["score"] is not None else "    N/A"
        print(f"{r['axis']:<{col}} {k:>7}  {r['n']:>5}  {r['interpretation']}")

    print("\n=== MULTI-LABEL AXES -- Krippendorff's alpha ===")
    print(f"{'Axis':<{col}} {'alpha':>7}  {'n':>5}  Interpretation")
    print(sep)
    for r in results_multilabel:
        a = f"{r['score']:.3f}" if r["score"] is not None else "    N/A"
        print(f"{r['axis']:<{col}} {a:>7}  {r['n']:>5}  {r['interpretation']}")

    all_disagree = [
        (r["axis"], d)
        for r in results_primary + results_multilabel
        for d in r.get("disagreements", [])
    ]
    if all_disagree:
        print(f"\n=== DISAGREEMENTS ({len(all_disagree)} total) ===")
        print(f"{'paper_id':<20} {'Axis':<{col}} {'Coder A':<22} Coder B")
        print(sep)
        for axis, d in all_disagree:
            print(f"{d['paper_id']:<20} {axis:<{col}} {d['coder_A']:<22} {d['coder_B']}")
    else:
        print("\nNo disagreements found.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="reliability.py",
        description=(
            "Compute inter-coder reliability (Cohen's kappa for primary-label axes, "
            "Krippendorff's alpha for multi-label axes) from two coded CSV files."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python reliability.py coding/coder_A_batch_1.csv coding/coder_B_batch_1.csv
  python reliability.py --output reports/pilot.md coding/pilot/coder_A_pilot.csv coding/pilot/coder_B_pilot.csv

output:
  Prints a per-axis reliability table to stdout.
  Saves a Markdown report to analysis/output/reliability_report.md
  (or the path given by --output).

thresholds:
  strong      >= 0.70
  acceptable  >= 0.60
  below       <  0.60  (requires adjudication)
        """,
    )
    parser.add_argument("coder_a", metavar="CODER_A_CSV", help="Coded CSV for coder A")
    parser.add_argument("coder_b", metavar="CODER_B_CSV", help="Coded CSV for coder B")
    parser.add_argument(
        "--output", "-o",
        metavar="REPORT_MD",
        default=None,
        help="Output path for Markdown report (default: analysis/output/reliability_report.md)",
    )
    args = parser.parse_args()

    # Load
    try:
        df_a = pd.read_csv(args.coder_a)
        df_b = pd.read_csv(args.coder_b)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    for label, df in [("CODER_A_CSV", df_a), ("CODER_B_CSV", df_b)]:
        if "paper_id" not in df.columns:
            print(f"ERROR: {label} is missing the required 'paper_id' column.", file=sys.stderr)
            sys.exit(1)

    # Primary axes
    results_primary = []
    for axis in PRIMARY_AXES:
        if axis not in df_a.columns or axis not in df_b.columns:
            print(f"WARNING: '{axis}' not found in one or both CSVs — skipping.", file=sys.stderr)
            continue
        score, n, disagreements = compute_primary_kappa(df_a, df_b, axis)
        results_primary.append(
            {
                "axis": axis,
                "score": score,
                "n": n,
                "interpretation": _interpret(score),
                "disagreements": disagreements,
            }
        )

    # Multi-label axes
    results_multilabel = []
    for axis in MULTILABEL_AXES:
        if axis not in df_a.columns or axis not in df_b.columns:
            print(f"WARNING: '{axis}' not found in one or both CSVs — skipping.", file=sys.stderr)
            continue
        score, n, disagreements = compute_multilabel_alpha(df_a, df_b, axis)
        results_multilabel.append(
            {
                "axis": axis,
                "score": score,
                "n": n,
                "interpretation": _interpret(score),
                "disagreements": disagreements,
            }
        )

    # Output
    print_stdout_report(results_primary, results_multilabel)

    report_md = build_markdown_report(
        results_primary, results_multilabel, args.coder_a, args.coder_b
    )
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path(__file__).parent / "output" / "reliability_report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_md, encoding="utf-8")
    print(f"\nReport saved → {out_path}")


if __name__ == "__main__":
    main()
