#!/usr/bin/env python3
"""Rebuild manuscript-facing CSVs from archived summaries without model execution."""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import statistics
from collections import defaultdict
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
SUMMARIES = PACKAGE / "summaries"


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = fields or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=columns, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def assert_close(observed: float, expected: float, label: str, tolerance: float = 1e-12) -> None:
    if not math.isclose(observed, expected, rel_tol=0.0, abs_tol=tolerance):
        raise RuntimeError(f"{label}: observed={observed} expected={expected}")


def rebuild_lean(output: Path) -> dict:
    source = read_csv(SUMMARIES / "main_tables/lean_harness_table.csv")
    runs = read_csv(SUMMARIES / "external_baselines/per_seed_run_index.csv")
    aliases = {
        "dlinear_std": "DLinear",
        "itransformer": "iTransformer",
        "lstm": "LSTM",
        "transformer": "vanilla Transformer",
        "patchtst": "PatchTST",
        "cptransformer": "CPTransformer",
        "ours_paramknee": "CALIBER-base",
    }
    grouped = defaultdict(list)
    for row in runs:
        method = aliases.get(row["method"], row["method"])
        grouped[(method, row["dataset"])].append(float(row["test_cb_rmse"]))
    rebuilt = []
    verified = 0
    for row in source:
        key = (row["method"], row["dataset"])
        out = dict(row)
        if key in grouped:
            values = grouped[key]
            mean = statistics.fmean(values)
            std = statistics.pstdev(values)
            assert_close(mean, float(row["cb_rmse_mean"]), f"lean mean {key}")
            assert_close(std, float(row["cb_rmse_std"]), f"lean std {key}")
            out["cb_rmse_mean"] = format(mean, ".17g")
            out["cb_rmse_std"] = format(std, ".17g")
            out["n_seeds"] = len(values)
            verified += 1
        rebuilt.append(out)
    write_csv(output / "lean_harness_table.csv", rebuilt)
    return {"rows": len(rebuilt), "per_seed_groups_recomputed": verified}


def rebuild_paired(output: Path) -> dict:
    effects = read_csv(SUMMARIES / "figures/paired_per_cell_effects.csv")
    frozen = {(row["dataset"], row["comparison"]): row for row in read_csv(SUMMARIES / "main_tables/paired_effects_table.csv")}
    grouped = defaultdict(list)
    for row in effects:
        grouped[(row["dataset"], row["comparison"])].append(float(row["delta_rmse"]))
    audit = []
    for key, values in sorted(grouped.items()):
        expected = frozen[key]
        mean = statistics.fmean(values)
        improve = sum(value < 0 for value in values) / len(values)
        worse = sum(value > 0 for value in values) / len(values)
        equal = sum(value == 0 for value in values) / len(values)
        assert_close(mean, float(expected["mean_delta"]), f"paired mean {key}")
        assert_close(improve, float(expected["improve_rate"]), f"paired improve rate {key}")
        assert_close(worse, float(expected["worse_rate"]), f"paired worse rate {key}")
        assert_close(equal, float(expected["equal_rate"]), f"paired equal rate {key}")
        audit.append({"dataset": key[0], "comparison": key[1], "n_pairs": len(values),
                      "mean_delta": format(mean, ".17g"), "improve_rate": format(improve, ".17g"),
                      "worse_rate": format(worse, ".17g"), "equal_rate": format(equal, ".17g")})
    write_csv(output / "paired_effects_recomputed.csv", audit)
    shutil.copyfile(SUMMARIES / "main_tables/paired_effects_table.csv", output / "paired_effects_full_frozen.csv")
    return {"comparison_groups": len(audit), "paired_rows": len(effects)}


def validate_and_copy(output: Path, source_name: str, output_name: str, required: set[str]) -> dict:
    source = SUMMARIES / "main_tables" / source_name
    rows = read_csv(source)
    missing = required - set(rows[0])
    if missing:
        raise RuntimeError(f"{source_name} missing columns {sorted(missing)}")
    shutil.copyfile(source, output / output_name)
    return {"rows": len(rows), "columns": len(rows[0])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "mode": "frozen-summary-only; no training, inference, checkpoint, download, or test selection",
        "lean_harness": rebuild_lean(output),
        "paired_effects": rebuild_paired(output),
        "five_arm": validate_and_copy(output, "five_arm_table.csv", "five_arm_table.csv", {"dataset", "arm", "cb_rmse_mean"}),
        "official_ag": validate_and_copy(output, "official_ag_reference.csv", "official_ag_reference.csv", {"dataset", "arm", "cb_rmse_mean"}),
        "gate_threshold": validate_and_copy(output, "gate_threshold_table.csv", "gate_threshold_table.csv", {"dataset", "decision", "frozen_decision"}),
        "grouped_conformal": validate_and_copy(output, "grouped_conformal_table.csv", "grouped_conformal_table.csv", {"dataset", "grp_cell_coverage"}),
        "batterylife": validate_and_copy(output, "batterylife_summary.csv", "batterylife_summary.csv", {"domain", "caliber_mean_mape_pct"}),
    }
    (output / "rebuild_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
