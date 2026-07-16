# Verified software environment

The release candidate was audited on Python 3.10.16 with PyTorch 2.6.0+cu124 and CUDA runtime
12.4.  Key packages were NumPy 2.1.3, pandas 2.2.3, SciPy 1.15.2, scikit-learn 1.6.1, and
Matplotlib 3.10.1.  Exact pip-visible versions are listed in `requirements-lock.txt`.

Create a compatible environment with:

```bash
conda env create -f reproducibility/environment.yml
conda activate caliber-repro
```

The two tabular audit commands use only the standard library.  pandas is required only to
re-export split manifests from local records; Matplotlib is required only for figure
rendering.  CUDA and PyTorch are not used by the read-only reconstruction commands.

Random seeds in the manuscript are 2026--2029 for the official four-seed system and
2026--2028 for the lean comparison harness.  Internal split seeds are recorded per row in
`splits/`; a textual `predefined_source_split` marker is used when the frozen cache does not
record a recoverable split seed rather than guessing one.
