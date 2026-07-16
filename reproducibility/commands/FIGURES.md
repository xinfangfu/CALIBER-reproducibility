# Figure reconstruction commands

```bash
python reproducibility/scripts/plot_five_arm_trajectory_from_summary.py --output-dir /tmp/caliber_figures
python reproducibility/scripts/plot_paired_effects_from_summary.py --output-dir /tmp/caliber_figures
```

These scripts use compact aggregate/cell-effect CSVs already in the package.  They do not
load model checkpoints or regenerate predictions.  They create PDF, SVG, and 300-dpi PNG
outputs in the requested directory.
