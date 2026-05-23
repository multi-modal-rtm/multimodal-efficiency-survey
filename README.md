# Multimodal Efficiency Survey

A systematic survey of efficiency techniques for multimodal large language models, targeting the *Journal of Artificial Intelligence Research* (JAIR).

## Repository Structure

```
multimodal-efficiency-survey/
├── rubric/
│   ├── rubric_v1.md          # Coding rubric (canonical, versioned)
│   ├── examples.md           # Worked examples for ambiguous cases
│   └── CHANGELOG.md          # Rubric version history
├── coding/
│   ├── schema.json           # JSON Schema (draft-07) for coded entries
│   ├── coding_template.csv   # Blank template — one row per paper
│   └── pilot/
│       └── coder_A_pilot.csv # Pilot results (coder A)
├── analysis/
│   ├── reliability.py        # Computes Cohen's κ and Krippendorff's α
│   ├── distributions.py      # Per-axis distribution bar charts
│   ├── sankey.py             # Cross-axis Sankey / flow diagrams
│   └── requirements.txt
├── papers/
│   └── bibtex/               # Zotero .bib exports go here
└── manuscript/
    ├── main.tex              # JAIR LaTeX template
    ├── sections/             # One .tex file per section
    └── figures/              # Publication-ready figures
```

## Overview

This repository contains the infrastructure for a systematic survey of efficiency techniques in multimodal AI systems. The survey applies a five-axis taxonomy across ~80–150 papers.

**All qualitative coding is performed exclusively by human coders. No automated paper classification is performed anywhere in this workflow.**

## Pre-Registration

The coding rubric will be tagged as **release v1.0** before any paper coding begins. This tag constitutes the pre-registration of the coding scheme. No rubric changes may be made after v1.0 is tagged without creating a new versioned release and documenting the change in `rubric/CHANGELOG.md`.

```bash
# Tag the pre-registration release (run only when rubric is finalized):
git tag -a v1.0 -m "Pre-registration: coding rubric v1.0"
git push origin v1.0
```

## Coder Workflow

### 1 — Setup

```bash
git clone <repo-url>
cd multimodal-efficiency-survey
pip install -r analysis/requirements.txt
```

### 2 — Before Coding

- Read `rubric/rubric_v1.md` in full.
- Work through all examples in `rubric/examples.md`.
- Complete the pilot phase: code your assigned pilot papers into `coding/pilot/coder_<ID>_pilot.csv`.
- Attend the calibration meeting to resolve pilot disagreements before proceeding to full coding.

### 3 — Coding Papers

Copy the blank template to a new batch file:

```bash
cp coding/coding_template.csv coding/coder_A_batch_1.csv
```

Then open the CSV in your preferred spreadsheet application or text editor and code papers one row at a time.

**Field conventions:**

| Value | Meaning |
|-------|---------|
| `NA`  | Axis does not apply to this paper |
| `NR`  | Axis applies but information is not reported |
| `other-specify` | Use when no listed category fits; elaborate in `coder_notes` |

- Multi-label fields use `|` as separator: `vision-image|audio|text`
- Fill `coder_id` and `coding_date` (ISO 8601) for every row
- List uncertain axes in `uncertainty_flags` (pipe-separated axis names)

Commit after each session:

```bash
git add coding/coder_A_batch_1.csv
git commit -m "coder_A: batch 1 complete (papers 001-025)"
```

### 4 — Reliability Analysis

After both coders complete a batch, compute inter-coder reliability:

```bash
python analysis/reliability.py coding/coder_A_batch_1.csv coding/coder_B_batch_1.csv
```

Review the report at `analysis/output/reliability_report.md`.

**Thresholds:**

| Metric | Axis type | Strong | Acceptable | Below threshold |
|--------|-----------|--------|------------|-----------------|
| Cohen's κ | Primary-label axes | ≥ 0.70 | ≥ 0.60 | < 0.60 |
| Krippendorff's α | Multi-label axes | ≥ 0.70 | ≥ 0.60 | < 0.60 |

Axes below threshold require adjudication discussion before proceeding.

## Analysis Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `analysis/reliability.py` | Inter-coder reliability (κ, α) | `python reliability.py A.csv B.csv` |
| `analysis/distributions.py` | Per-axis distribution bar charts | `python distributions.py merged.csv` |
| `analysis/sankey.py` | Cross-axis Sankey flow diagrams | `python sankey.py merged.csv` |

All scripts accept `--help` for full usage information.

## Schema Validation

```bash
# Validate schema.json is well-formed JSON:
python -c "import json; json.load(open('coding/schema.json')); print('Schema OK')"

# Verify CSV template loads cleanly:
python -c "import pandas as pd; df = pd.read_csv('coding/coding_template.csv'); print(f'Columns: {len(df.columns)}, Rows: {len(df)}')"
```

## Taxonomy Axes

| # | Field | Type | Categories |
|---|-------|------|------------|
| 1a | `axis_1a_encoder_config` | primary + secondary | 5 + NA + NR |
| 1b | `axis_1b_fusion_mechanism` | primary + secondary | 10 + other-specify + NA + NR |
| 1c | `axis_1c_modality_set` | multi-label array | controlled vocab |
| 2  | `axis_2_adaptation` | primary + secondary | 8 + NA + NR |
| 3a | `axis_3a_optimizer` | primary + secondary | 7 + other-specify + NA + NR |
| 3b | `axis_3b_memory_techniques` | multi-label array | controlled vocab |
| 4a | `axis_4a_precision` | primary + secondary | 8 + NA + NR |
| 4b | `axis_4b_sparsity` | primary + secondary | 7 + NA + NR |
| 5  | `axis_5_topology` | primary + secondary | 7 + NA + NR |

See `rubric/rubric_v1.md` for full category definitions and decision rules.

## Notes for Coders

- **Coding is manual.** Do not use automated tools to assign codes.
- **Use `NA`** when an axis genuinely does not apply.
- **Use `NR`** when an axis applies but the paper does not report sufficient information.
- **When uncertain**, still record your best-fit code and add the axis name to `uncertainty_flags`.
- **Paper IDs** should be short and memorable (e.g., `liu2023llava`, `zhu2023minigpt4`).
- Consult `rubric/examples.md` for worked cases before raising ambiguities with your co-coder.

## Contributing / Rubric Changes

All rubric changes require a new version entry in `rubric/CHANGELOG.md` and consensus from both coders. Retroactive re-coding of completed batches requires explicit documentation of which papers were affected and why.
