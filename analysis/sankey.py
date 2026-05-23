#!/usr/bin/env python3
"""
Generate cross-axis Sankey / flow diagrams from a merged coded CSV.

For each (source, target) axis pair, produces:
  - A contingency table printed to stdout
  - A placeholder figure saved to the output directory

For publication-quality Sankey diagrams, replace _draw_placeholder() with
a Plotly go.Sankey trace and call fig.write_image() or fig.write_html().

Usage:
    python sankey.py CODED_CSV [--output DIR] [--pair SRC TGT ...]
"""

import argparse
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd


# Default cross-axis pairs to visualise
DEFAULT_PAIRS = [
    ("axis_1a_encoder_config_primary", "axis_1b_fusion_mechanism_primary"),
    ("axis_2_adaptation_primary",      "axis_4a_precision_primary"),
    ("axis_5_topology_primary",        "axis_4b_sparsity_primary"),
]


def _contingency(df, src, tgt):
    counts = df.groupby([src, tgt]).size().reset_index(name="count")
    pivot = counts.pivot_table(index=src, columns=tgt, values="count", fill_value=0)
    return counts, pivot


def _draw_placeholder(src, tgt, pivot, out_dir):
    """Minimal stub figure — replace with Plotly Sankey for publication."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis("off")
    summary = f"Pairs: {len(pivot.index)} sources × {len(pivot.columns)} targets"
    ax.text(
        0.5, 0.5,
        f"Sankey: {src}\n→ {tgt}\n\n{summary}\n\n"
        "(Replace with Plotly go.Sankey for publication figures)",
        ha="center", va="center", transform=ax.transAxes, fontsize=10,
        bbox=dict(boxstyle="round,pad=0.6", facecolor="lightyellow", edgecolor="gray"),
    )
    title = f"{src.replace('_primary','').replace('_',' ')}  →  {tgt.replace('_primary','').replace('_',' ')}"
    ax.set_title(title, fontsize=11, pad=12)
    plt.tight_layout()
    safe = f"{src}__to__{tgt}.png"
    out_path = out_dir / safe
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def process_pair(df, src, tgt, out_dir):
    if src not in df.columns or tgt not in df.columns:
        print(f"  WARNING: '{src}' or '{tgt}' not in CSV — skipping.")
        return

    counts, pivot = _contingency(df, src, tgt)

    print(f"\n{'─'*70}")
    print(f"  {src}  →  {tgt}")
    print(f"{'─'*70}")
    print(pivot.to_string())

    out_path = _draw_placeholder(src, tgt, pivot, out_dir)
    print(f"  Figure → {out_path.name}")


def main():
    parser = argparse.ArgumentParser(
        prog="sankey.py",
        description="Generate cross-axis Sankey / flow diagrams from a merged coded CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python sankey.py coding/merged_final.csv
  python sankey.py coding/merged_final.csv --output manuscript/figures/
  python sankey.py coding/merged_final.csv --pair axis_3a_optimizer_primary axis_5_topology_primary
        """,
    )
    parser.add_argument("coded_csv", metavar="CODED_CSV", help="Merged coded CSV (post adjudication)")
    parser.add_argument(
        "--output", "-o",
        metavar="DIR",
        default=None,
        help="Output directory for figures (default: analysis/output/figures/)",
    )
    parser.add_argument(
        "--pair",
        nargs=2,
        metavar=("SRC_COL", "TGT_COL"),
        action="append",
        help="Extra column pair to plot (repeatable; additive with defaults)",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.coded_csv)
    out_dir = Path(args.output) if args.output else Path(__file__).parent / "output" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Writing figures to: {out_dir}")

    pairs = list(DEFAULT_PAIRS)
    if args.pair:
        pairs.extend(tuple(p) for p in args.pair)

    for src, tgt in pairs:
        process_pair(df, src, tgt, out_dir)

    print(f"\nDone.")


if __name__ == "__main__":
    main()
