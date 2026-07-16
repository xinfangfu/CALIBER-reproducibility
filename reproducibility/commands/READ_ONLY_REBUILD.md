# Read-only reconstruction commands

Run from the repository root, or from a directory containing this `reproducibility/` folder:

```bash
python reproducibility/scripts/verify_all_checksums.py
python reproducibility/scripts/rebuild_frozen_tables.py --output-dir /tmp/caliber_tables
```

The reconstructed outputs cover the lean system table, official Ag reference, five-arm table,
paired-effect aggregates, gate-threshold table, grouped conformal table, and BatteryLife
summary.  Outputs go only to the caller-provided directory.
