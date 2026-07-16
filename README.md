# CALIBER frozen-evidence reproducibility package

This directory is the portable, release-candidate audit package for the manuscript.  It
contains split manifests, compact frozen summaries, selected baseline configuration
inventories, checksums, and read-only reconstruction scripts.  It does **not** contain raw
third-party battery data, checkpoints, private correspondence, credentials, or a public
repository/DOI claim.

## Fast read-only audit

From the repository root:

```bash
python reproducibility/scripts/verify_all_checksums.py
python reproducibility/scripts/rebuild_frozen_tables.py --output-dir /tmp/caliber_tables
python reproducibility/scripts/plot_five_arm_trajectory_from_summary.py --output-dir /tmp/caliber_figures
python reproducibility/scripts/plot_paired_effects_from_summary.py --output-dir /tmp/caliber_figures
```

The first two commands require only Python's standard library.  The plotting commands also
require the archived Matplotlib environment.  None of these commands imports model code,
loads a checkpoint, downloads data, trains, performs inference, or changes frozen inputs.

## Package map

- `splits/`: cell-level internal manifests and official BatteryLife fold manifests.
- `summaries/main_tables/`: manuscript-facing frozen table sources.
- `summaries/external_baselines/`: per-seed metric and HPO-trial inventories.
- `summaries/figures/`: compact aggregate inputs for the two manuscript figures.
- `configs/external_baselines/`: selected, path-sanitized configuration summaries.
- `manifests/`: split validation, release inventory, and dry-run evidence.
- `checksums/`: package and source-artifact SHA256 manifests.
- `commands/`: data, table, figure, and non-audit training command notes.
- `licenses/`: redistribution and unresolved-license boundaries.

## Evidence boundary

The package reconstructs reported tables from frozen summaries and recomputes paired-cell
descriptive aggregates from archived cell effects.  It is not a clean retraining capsule:
raw datasets and checkpoints are intentionally absent, and the original training wall-clock
time is not recoverable from the frozen logs.  Public repository URL, archival DOI, and the
final release license remain author actions documented in `CODE_AVAILABILITY_TEMPLATE.md`.

## Split lineage

Internal manifests were exported directly from the five frozen records files.  XJTU-LPO is
additionally tied to the recovered byte-identical builder
`scripts/DATASETS/build_xjtu_lpo.py`: protocol groups are shuffled with seed 2026 and assigned
whole to train/validation/test.  The frozen manifest contains 24/8/23 cells and holds out
`Batch-2_3C` and `Batch-5_RW`, with zero protocol overlap.  BatteryLife rows are exported
directly from its 22 official split JSON files (3 Li-ion, 4 CALB, 12 Na-ion, 3 Zn-ion folds).

## Publication status

This repository is publicly available at
`https://github.com/xinfangfu/CALIBER-reproducibility` under the MIT License
for first-party code and documentation. Release `v1.0.0` is archived on
Zenodo with version DOI
[`10.5281/zenodo.21387405`](https://doi.org/10.5281/zenodo.21387405).
The concept DOI for all versions is
[`10.5281/zenodo.21387404`](https://doi.org/10.5281/zenodo.21387404).

The frozen `reproducibility/` directory remains unchanged so that its
original Stage 2B.12 checksum manifest can still be verified. See
`PUBLICATION_STATUS.md` and `LICENSE_SCOPE.md` for the current publication
and licensing boundaries.
