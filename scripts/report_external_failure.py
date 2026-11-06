"""Render verified external-failure diagnostic tables and paired-change figure."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from src.stats.run_vindr_statistics import (
    artifact,
    read_json,
    read_yaml,
    require,
    verify_artifact,
    write_json,
)


def render(config_path: Path) -> None:
    """Present saved estimates without changing scientific outputs or selecting arms."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    config = read_yaml(config_path)
    root = Path(config["outputs"]["public_root"])
    summary_path = root / "summary.json"
    summary = read_json(summary_path)
    require(summary["status"] == "complete_exploratory_diagnostic", "Incomplete analysis")
    for item in [*summary["inputs"], *summary["artifacts"]]:
        verify_artifact(item)
    rows = summary["paired_changes"]
    detectors = list(dict.fromkeys(r["detector"] for r in rows))
    endpoints = list(dict.fromkeys(r["endpoint"] for r in rows))
    arms = [name for name in config["arms"] if name != "baseline"]
    labels = {
        "lower_floor": "Lower collection floor",
        "higher_cap": "Higher detection cap",
        "expanded": "Lower floor + higher cap",
        "dicom_window": "DICOM header window",
    }
    titles = {
        "historical_recall": "Historical-threshold recall",
        "negative_control_fp_per_image": "False positives per negative-control image",
        "geometric_coverage_iou_0.25": "One-to-one geometric coverage (IoU 0.25)",
        "geometric_coverage_iou_0.5": "One-to-one geometric coverage (IoU 0.50)",
    }
    fig, axes = plt.subplots(len(endpoints), 1, figsize=(10, 12), layout="constrained")
    for axis, endpoint in zip(axes, endpoints, strict=True):
        for d, detector in enumerate(detectors):
            values = [
                next(
                    r
                    for r in rows
                    if r["detector"] == detector and r["arm"] == arm and r["endpoint"] == endpoint
                )
                for arm in arms
            ]
            # Plot endpoints directly: a percentile CI need not contain the point estimate.
            y = np.arange(len(arms)) + (d - 0.5) * 0.18
            axis.hlines(
                y,
                [r["ci_lower"] for r in values],
                [r["ci_upper"] for r in values],
                color=f"C{d}",
                linewidth=2,
            )
            axis.scatter([r["delta"] for r in values], y, label=detector, color=f"C{d}")
        axis.axvline(0, color="gray", linewidth=0.8, linestyle="--")
        axis.set_yticks(np.arange(len(arms)), [labels[a] for a in arms])
        axis.set_title(titles[endpoint])
        axis.set_xlabel("Paired change from baseline (marginal 95% bootstrap interval)")
        axis.invert_yaxis()
        axis.grid(axis="x", alpha=0.2)
    axes[0].legend(loc="best")
    figure = root / "paired_changes.png"
    fig.savefig(figure, dpi=180)
    plt.close(fig)
    cohort = summary["cohort"]
    lines = [
        "# External failure isolation v1: executed diagnostic results",
        "",
        "Exploratory controlled diagnostic, designed after the original outcomes were known.",
        "See [protocol](EXTERNAL_FAILURE_ISOLATION_V1.md) for the frozen interventions and limits.",
        "",
        f"Cohort: {cohort['positive_images']} strict-positive images, "
        f"{cohort['target_boxes']} boxes, "
        f"{cohort['negative_images']} randomly selected strict negatives; "
        "five retained checkpoints per detector. Original predictions and nested baseline "
        "retention were replayed exactly for every image/run.",
        "",
        "These paired effects concern the tested implementation controls. They do not "
        "identify the causes of the total cross-dataset gap or validate new operating rules.",
        "",
        f"Summary SHA-256: `{artifact(summary_path)['sha256']}`.",
        "",
        "## Full-cohort evaluation-floor control",
        "",
        "All 3,000 external images, unchanged saved predictions and COCO maxDets 100. "
        "AP50 uses either the original evaluation floor 0.001 or 0.00001. Equal-run means:",
        "",
        "| Detector | Original AP50 | Lower evaluation floor AP50 | Change |",
        "|---|---:|---:|---:|",
    ]
    for detector in detectors:
        vals = [r for r in summary["ap_floor_control"] if r["detector"] == detector]
        means = [
            np.mean([r[k] for r in vals])
            for k in ("original_ap50", "lower_evaluation_floor_ap50", "delta")
        ]
        lines.append(f"| {detector} | " + " | ".join(f"{v:.9f}" for v in means) + " |")
    for endpoint in endpoints:
        lines.extend(
            [
                "",
                f"## {titles[endpoint]}",
                "",
                "| Detector | Arm | Mean | Change from baseline | 95% interval for change |",
                "|---|---|---:|---:|---|",
            ]
        )
        for r in rows:
            if r["endpoint"] == endpoint:
                mean = "n/a" if r["mean"] is None else f"{r['mean']:.6f}"
                lines.append(
                    f"| {r['detector']} | {r['arm']} | {mean} | {r['delta']:.6f} | "
                    f"[{r['ci_lower']:.6f}, {r['ci_upper']:.6f}] |"
                )
    lines.extend(
        [
            "",
            "## Limits",
            "",
            "Intervals are marginal and conditional on this diagnostic cohort and the five "
            "trained checkpoints. Zero-containing intervals do not establish equivalence. "
            "Geometric coverage is an annotation-informed one-to-one upper bound; it is "
            "not achieved recall or clinical correctness. Negative-control FP/image is "
            "conditional on the fixed negative sample. Clinical label equivalence, upstream "
            "proposals and population/acquisition causes remain unresolved.",
            "",
            "![Paired diagnostic effects](../" + figure.as_posix() + ")",
            "",
        ]
    )
    report = Path(config["outputs"]["report"])
    report.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    write_json(
        root / "report_build.json",
        {
            "inputs": [artifact(config_path), artifact(summary_path), artifact(Path(__file__))],
            "outputs": [artifact(report), artifact(figure)],
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    render(parser.parse_args().config)
