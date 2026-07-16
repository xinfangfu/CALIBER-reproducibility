# Data Availability — release-candidate text and evidence map

## Candidate statement

This study reuses the MIT fast-charging, XJTU, ISU-ILCC, Aging Matrix, Dynamic Cycling, and
BatteryLife benchmark datasets described and cited in the manuscript.  Raw third-party data
are not redistributed in this package and remain subject to the access and reuse terms of
their original providers.  The package supplies cell/protocol split manifests, source-file
SHA256 hashes, preprocessing-script versions, and derived numerical summaries sufficient to
audit the reported partitions and reconstruct the frozen manuscript tables without model
execution.  A persistent public archive identifier will be added only after author deposit.

## Dataset-to-artifact map

| Dataset | Raw data in package | Split evidence | Derived results in package | Remaining action |
|---|---|---|---|---|
| MIT fast charging | No | `splits/mit_split_manifest.csv` | main/five-arm/paired/UQ summaries | Verify original provider terms before release |
| Aging Matrix | No | `splits/aging_split_manifest.csv` | main/five-arm/paired/UQ summaries | Verify original provider terms before release |
| Dynamic Cycling | No | `splits/dynamic_split_manifest.csv` | main/five-arm/paired/UQ summaries | Verify original provider terms before release |
| XJTU-LPO | No | `splits/xjtu_lpo_split_manifest.csv`; recovered builder hash | main/five-arm/paired/UQ summaries | Verify original provider terms before release |
| ISU-ILCC-LPO | No | `splits/isu_lpo_split_manifest.csv` | main/five-arm/paired/UQ summaries | Verify original provider terms before release |
| BatteryLife four-domain benchmark | No | `splits/batterylife_split_manifest.csv` from 22 split JSONs | four-domain summary | Verify upstream dataset-by-dataset terms |

The manifests contain identifiers and partition metadata, not electrochemical time-series
measurements.  No statement that “all data are public” is made because redistribution rights
have not been verified for every upstream dataset.
