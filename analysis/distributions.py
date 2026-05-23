#!/usr/bin/env python3
"""
Generate per-axis distribution bar charts from a merged coded CSV.

Usage:
    python distributions.py CODED_CSV [--output DIR]
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


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


def _axis_title(col):
    return col.replace("_primary", "").replace("_", " ").title()


def plot_primary(df, axis, out_dir):
    counts = df[axis].value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 4))
    counts.plot(kind="bar", ax=ax, color="steelblue", edgecolor="white", width=0.7)
    ax.set_title(_axis_title(axis), fontsize=13, pad=10)
    ax.set_xlabel("Category", labelpad=6)
    ax.set_ylabel("Papers (n)", labelpad=6)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(rotation=35, ha="right", fontsize=9)
    plt.tight_layout()
    out_path = out_dir / f"{axis}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path.name}")


def plot_multilabel(df, axis, out_dir):
    all_labels = []
    for val in df[axis].dropna():
        all_labels.extend(v.strip() for v in str(val).split("|") if v.strip())
    if not all_labels:
        print(f"  Skipped {axis}: no data.")
        return
    counts = pd.Series(all_labels).value_counts().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 4))
    counts.plot(kind="bar", ax=ax, color="darkorange", edgecolor="white", width=0.7)
    ax.set_title(f"{_axis_title(axis)} (multi-label)", fontsize=13, pad=10)
    ax.set_xlabel("Label", labelpad=6)
    ax.set_ylabel("Papers (n, multi-label)", labelpad=6)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(rotation=35, ha="right", fontsize=9)
    plt.tight_layout()
    out_path = out_dir / f"{axis}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path.name}")


def main():
    parser = argparse.ArgumentParser(
        prog="distributions.py",
        description="Generate per-axis distribution bar charts from a merged (post-adjudication) coded CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python distributions.py coding/merged_final.csv
  python distributions.py coding/merged_final.csv --output manuscript/figures/
        """,
    )
    parser.add_argument("coded_csv", metavar="CODED_CSV", help="Merged coded CSV (post adjudication)")
    parser.add_argument(
        "--output", "-o",
        metavar="DIR",
        default=None,
        help="Output directory for figures (default: analysis/output/figures/)",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.coded_csv)
    out_dir = Path(args.output) if args.output else Path(__file__).parent / "output" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Writing figures to: {out_dir}\n")

    print("Primary axes:")
    for axis in PRIMARY_AXES:
        if axis not in df.columns:
            print(f"  WARNING: '{axis}' not in CSV — skipping.")
            continue
        plot_primary(df, axis, out_dir)

    print("\nMulti-label axes:")
    for axis in MULTILABEL_AXES:
        if axis not in df.columns:
            print(f"  WARNING: '{axis}' not in CSV — skipping.")
            continue
        plot_multilabel(df, axis, out_dir)

    print(f"\nDone. {len(list(out_dir.glob('*.png')))} figures in {out_dir}")


if __name__ == "__main__":
    main()
