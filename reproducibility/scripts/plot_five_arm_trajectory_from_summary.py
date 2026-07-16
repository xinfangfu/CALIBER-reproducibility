#!/usr/bin/env python3
"""Render the five-arm trajectory panels from the archived aggregate CSV."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE / "summaries/figures/fig_traj_five_arm_aggregated.csv"
PANELS = (("mit", "MIT"), ("aging_matrix", "Aging"), ("xjtu_lpo", "XJTU-LPO"), ("isu_ilcc_lpo", "ISU-LPO"))
COLORS = {"Truth": "#111111", "A0": "#777777", "Ab": "#7A5195", "Ac": "#2F6B9A", "Abc": "#D07A2D", "Ag": "#2E8B57"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    grouped = defaultdict(list)
    with SOURCE.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["dataset"] in dict(PANELS) and row["included_in_main_figure"] == "True":
                grouped[(row["dataset"], row["series"])].append(row)
    mpl.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5, "pdf.fonttype": 42, "svg.fonttype": "none", "svg.hashsalt": "caliber-five-arm-summary-v1"})
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.2), constrained_layout=True)
    for index, ((dataset, label), ax) in enumerate(zip(PANELS, axes.ravel())):
        for (key_dataset, series), rows in sorted(grouped.items()):
            if key_dataset != dataset:
                continue
            rows.sort(key=lambda row: float(row["tau"]))
            x = [float(row["tau"]) for row in rows]
            med = [float(row["median_soh"]) for row in rows]
            q25 = [float(row["q25_soh"]) for row in rows]
            q75 = [float(row["q75_soh"]) for row in rows]
            color = COLORS.get(series, "#555555")
            ax.plot(x, med, color=color, linewidth=1.4, label=series)
            ax.fill_between(x, q25, q75, color=color, alpha=0.10, linewidth=0)
        ax.set_title(label)
        ax.set_xlabel("Normalized future fraction")
        ax.set_ylabel("SOH")
        ax.text(-0.12, 1.05, chr(97 + index), transform=ax.transAxes, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    handles, labels = axes.ravel()[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=max(1, len(labels)), frameon=False)
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    fixed_time = dt.datetime(2026, 7, 16, tzinfo=dt.timezone.utc)
    for suffix in ("pdf", "svg", "png"):
        metadata = {"CreationDate": fixed_time, "ModDate": fixed_time} if suffix == "pdf" else ({"Date": "2026-07-16"} if suffix == "svg" else {"Software": "Matplotlib 3.10.1"})
        fig.savefig(out / f"fig_traj_five_arm.{suffix}", dpi=300, bbox_inches="tight", metadata=metadata)
    plt.close(fig)
    print(f"PASS: rendered aggregate-only five-arm trajectory figure to {out}")


if __name__ == "__main__":
    main()
