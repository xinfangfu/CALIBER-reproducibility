# Data and split preparation boundary

Raw third-party data are not distributed.  For an authorized local copy, use the repository's
dataset-specific builders and preserve the resulting SHA256.  During manuscript freeze, do
not rerun builders over the canonical records files.

The safe release operation is a read-only manifest export:

```bash
python scripts/STAGE2B12/export_reproducibility_materials.py \
  --external-baseline-root <LOCAL_PREARCHIVE_EXTBASE_DIRECTORY>
```

That curator command reads existing records and small JSON summaries.  It performs no model
training or inference.  XJTU's canonical builder is retained for lineage inspection at
`scripts/DATASETS/build_xjtu_lpo.py`, but executing it would overwrite a frozen records file
and is not part of the release audit.
