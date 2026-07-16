# Hardware and runtime record

## Verified audit host

- GPU: NVIDIA GeForce RTX 4090, 24,564 MiB; driver 535.183.01.
- CPU: 13th Gen Intel Core i9-13900K; 32 online logical CPUs reported by the host.
- Memory: 131,670,428 kB total system memory reported by `/proc/meminfo`.
- OS/kernel: Linux 5.15.0-139-generic, x86_64.
- Python/PyTorch: Python 3.10.16; PyTorch 2.6.0+cu124; CUDA runtime 12.4.

The manuscript's official training runs used a single RTX 4090.  The current host query is
consistent with that record.  The read-only table reconstruction itself requires no GPU.

## Runtime boundary

- Single-training-run wall-clock time: **not recoverable from frozen logs**.
- Total end-to-end HPO wall-clock time: **not recoverable from frozen logs**.
- No time was estimated from file modification times.
- Per-method/dataset HPO trial counts are recorded from the existing JSON inventory in
  `summaries/external_baselines/hpo_trial_index.csv`.

The package therefore supports evidence and split reconstruction, not a claim about exact
training duration or compute cost.
