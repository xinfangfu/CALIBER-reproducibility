#!/usr/bin/env python3
"""Render paired-effect panels from archived cell effects and intervals."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


PACKAGE = Path(__file__).resolve().parents[1]
EFFECTS = PACKAGE / "summaries/figures/paired_per_cell_effects.csv"
INTERVALS = PACKAGE / "summaries/figures/paired_hierarchical_bootstrap.csv"
DATASETS = (("mit", "MIT"), ("aging_matrix", "Aging"), ("dynamic_cycling", "Dynamic"), ("xjtu_lpo", "XJTU-LPO"), ("isu_ilcc_lpo", "ISU-LPO"))
COMPARISONS = ("Ag-A0", "Abc-A0", "Ac-A0")
COLORS = ("#2F6B9A", "#D07A2D", "#4C956C")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    points = defaultdict(list)
    with EFFECTS.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["comparison"] in COMPARISONS:
                points[(row["dataset"], row["comparison"])].append(float(row["delta_rmse"]))
    intervals = {}
    with INTERVALS.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["comparison"] in COMPARISONS:
                intervals[(row["dataset"], row["comparison"])] = tuple(float(row[key]) for key in ("observed_mean_of_seed_means", "ci_low", "ci_high"))
    mpl.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "pdf.fonttype": 42, "svg.fonttype": "none", "svg.hashsalt": "caliber-paired-summary-v1"})
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 5.2), constrained_layout=True)
    for panel, ((dataset, label), ax) in enumerate(zip(DATASETS, axes.ravel())):
        all_values = []
        for x, comparison in enumerate(COMPARISONS):
            values = points[(dataset, comparison)]
            all_values.extend(values)
            ax.scatter([x] * len(values), values, s=6, alpha=0.16, color=COLORS[x], linewidths=0)
            mean, low, high = intervals[(dataset, comparison)]
            ax.errorbar(x, mean, yerr=[[mean-low], [high-mean]], fmt="s", color="#111111", capsize=2)
        bound = max(abs(value) for value in all_values) * 1.1 or 0.001
        ax.set_ylim(-bound, bound)
        ax.axhline(0, color="#666666", linestyle="--", linewidth=0.8)
        ax.set_xticks(range(3), ["Ag-A0", "Abc-A0", "Ac-A0"])
        ax.set_title(label)
        ax.text(-0.13, 1.05, chr(97 + panel), transform=ax.transAxes, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    axes.ravel()[-1].axis("off")
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    fixed_time = dt.datetime(2026, 7, 16, tzinfo=dt.timezone.utc)
    for suffix in ("pdf", "svg", "png"):
        metadata = {"CreationDate": fixed_time, "ModDate": fixed_time} if suffix == "pdf" else ({"Date": "2026-07-16"} if suffix == "svg" else {"Software": "Matplotlib 3.10.1"})
        fig.savefig(out / f"fig_paired_cell_effects.{suffix}", dpi=300, bbox_inches="tight", metadata=metadata)
    plt.close(fig)
    print(f"PASS: rendered summary-only paired-effect figure to {out}")


if __name__ == "__main__":
    main()
