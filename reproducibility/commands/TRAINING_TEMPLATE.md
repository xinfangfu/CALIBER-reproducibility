# Training command templates (not part of the read-only audit)

The Stage 2B.12 audit did not execute training, inference, or checkpoint loading.  Existing
dataset entry points expose the frozen experiment configuration and should be inspected before
any future independent rerun:

```bash
python scripts/MIT/MIT-early30.py --help
python scripts/XJTU/XJTU-early30.py --help
python scripts/AGING_MATRIX/AGING_MATRIX-early30.py --help
python scripts/DYNAMIC/DYNAMIC-early30.py --help
```

A future retraining release must use authorized local datasets, a new output directory, and
the seeds declared in the manuscript.  It must never overwrite the frozen evidence package.
