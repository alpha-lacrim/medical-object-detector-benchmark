"""Nonidentifying aggregate figures and a generated post-hoc results appendix."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.stats.external_generalization import TARGET_CATEGORIES


def table(rows: list[dict], fields: list[str]) -> str:
    """Render deterministic aggregate tables, preserving undefined values."""

    def cell(value: object) -> str:
        if value is None:
            return "NA"
        return f"{value:.6f}" if isinstance(value, float) else str(value)

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(cell(r[f]) for f in fields) + " |" for r in rows],
        ]
    )


def render(saved: dict, config: dict) -> list[Path]:
    """Plot only per-run/equal-run aggregate quantities, never images or linked predictions."""
    root = Path(config["outputs"]["public_root"])
    tables, style = saved["tables"], config["plot"]
    detectors = list(style["colors"])
    labels = {"faster_rcnn": "Faster R-CNN", "yolo11s": "YOLO11s"}
    figures = []
    fig, axes = plt.subplots(1, 2, figsize=style["size"], layout="constrained")
    bottom = np.zeros(len(detectors))
    for category in TARGET_CATEGORIES:
        values = [
            next(
                r["mean"]
                for r in tables["reference_errors_means"]
                if r["detector"] == d and r["category"] == category and r["quantity"] == "fraction"
            )
            for d in detectors
        ]
        axes[0].bar(
            [labels[d] for d in detectors], values, bottom=bottom, label=category.replace("_", " ")
        )
        bottom += values
    axes[0].set(
        ylabel="Fraction of strict reference boxes",
        ylim=(0, 1),
        title="External error categories (equal-run mean)",
    )
    axes[0].legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    classes = config["analysis"]["non_target_classes"]
    for i, detector in enumerate(detectors):
        rows = tables["non_target_overlaps_means"]
        values = [
            next(
                r["mean"]
                for r in rows
                if r["detector"] == detector
                and r["support"] == "historical"
                and r["class_name"] == c
                and r["quantity"] == "fraction"
            )
            for c in classes
        ]
        axes[1].bar(
            np.arange(len(classes)) + (i - 0.5) * 0.35,
            values,
            0.35,
            color=style["colors"][detector],
            label=labels[detector],
        )
    axes[1].set(
        xticks=np.arange(len(classes)),
        xticklabels=classes,
        ylabel="Fraction of strict false positives",
        title=(
            "Other-finding overlap at historical thresholds\n"
            "Means conditional on nonempty false-positive populations"
        ),
    )
    axes[1].tick_params(axis="x", labelrotation=25)
    axes[1].legend(fontsize=8)
    path = root / "error_and_annotation_sensitivity.png"
    fig.savefig(path, dpi=style["dpi"])
    plt.close(fig)
    figures.append(path)
    fig, axes = plt.subplots(1, 2, figsize=style["size"], layout="constrained")
    for detector in detectors:
        rows = [r for r in tables["prevalence_per_run"] if r["detector"] == detector]
        for r in rows:
            axes[0].plot(
                [0, 1],
                [r["original_ap50"], r["standardized_custom_ap50"]],
                color=style["colors"][detector],
                alpha=0.5,
                marker="o",
                markersize=3,
            )
        axes[0].plot(
            [0, 1],
            [
                np.mean([r["original_ap50"] for r in rows]),
                np.mean([r["standardized_custom_ap50"] for r in rows]),
            ],
            color=style["colors"][detector],
            linewidth=3,
            label=labels[detector],
        )
    axes[0].set(
        xticks=[0, 1],
        xticklabels=["Original internal", "Reweighted internal"],
        ylabel="AP50 / custom weighted AP50",
        title="Population-weight sensitivity (all five runs)",
        ylim=(0, None),
    )
    axes[0].legend(fontsize=8)
    rows = tables["change_intervals"]
    for i, letter in enumerate(("a", "b", "difference")):
        y = np.arange(len(rows)) + (i - 1) * 0.18
        estimate = np.array([r[f"{letter}_estimate"] for r in rows])
        low = np.array([r[f"{letter}_ci_low"] for r in rows])
        high = np.array([r[f"{letter}_ci_high"] for r in rows])
        # Draw endpoints directly: a percentile interval need not contain its point estimate.
        axes[1].hlines(y, low, high, colors=f"C{i}")
        axes[1].plot(
            estimate,
            y,
            "o",
            color=f"C{i}",
            markersize=4,
            label=("Faster R-CNN change", "YOLO11s change", "Difference in changes")[i],
        )
    axes[1].axvline(0, color="gray", linestyle=":")
    axes[1].set(
        yticks=np.arange(len(rows)),
        yticklabels=[r["metric"] for r in rows],
        xlabel="VinDr minus RSNA; absolute change",
        title="Post-hoc marginal 95% intervals",
    )
    axes[1].legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.14))
    path = root / "prevalence_and_domain_changes.png"
    fig.savefig(path, dpi=style["dpi"])
    plt.close(fig)
    figures.append(path)
    sections = [
        "# Post-hoc external generalization results v1",
        "Generated from executed frozen-prediction analysis. Findings are EXPLORATORY; "
        "read-only verification and full replay are separate checks. "
        "Protocol: [version 1](POSTHOC_EXTERNAL_GENERALIZATION_PROTOCOL.md). "
        "No original result, target, threshold or prediction was changed.",
        "## Reference-box error decomposition",
        "Each category is exclusive with protocol-defined precedence. Means/SDs "
        "weight runs equally; "
        "availability does not imply successful one-to-one assignment. Missing retained output is "
        "not proof of absent pre-NMS/proposal output.",
        table(
            tables["reference_errors_means"],
            ["detector", "category", "quantity", "mean", "sd", "defined_runs", "attempted_runs"],
        ),
        "## Candidate availability (assignment ignored)",
        table(tables["availability_means"], ["detector", "iou", "quantity", "mean", "sd"]),
        "## Strict false positives and non-target findings",
        "FP overlap never reclassifies detections as true positives. Fractions use "
        "each run's strict FPs; "
        "undefined zero-FP runs are counted explicitly. Overlapping class flags need "
        "not sum to one. "
        "A broader Lung Opacity/Consolidation/Infiltration target remains UNRESOLVED "
        "pending expert "
        "instance/ontology review; no alternative-task AP is reported.",
        table(
            tables["false_positives_means"],
            [
                "detector",
                "support",
                "category",
                "quantity",
                "mean",
                "sd",
                "defined_runs",
                "attempted_runs",
            ],
        ),
        table(
            [
                r
                for r in tables["non_target_overlaps_means"]
                if r["class_name"] in config["analysis"]["non_target_classes"]
                and r["quantity"] == "fraction"
            ],
            ["detector", "support", "class_name", "mean", "sd", "defined_runs", "attempted_runs"],
        ),
        "![Reference categories and local annotation "
        "overlap.](../results/external_generalization_v1/error_and_annotation_sensitivity.png)",
        "## Prevalence standardization",
        "Weighted AP is a custom interpolated detection metric, not official COCO "
        "AP. Positive/negative "
        "image weights change the evaluation population while fixing internal "
        "conditional case mix. "
        "This is not a causal prevalence effect or a recreation of VinDr. Recall "
        "stays unchanged by "
        "construction. ESS describes image-weight concentration, not independent "
        "patients. Intervals "
        "condition on observed external positive frequency; patient/run resampling "
        "re-estimates internal "
        "frequency. Integer bootstrap multiplicities weight detection events in the custom metric; "
        "they do not use the distinct-copy COCO tie convention. Unit-weight observed "
        "AP is reconciled "
        "against canonical COCO for every run.",
        table(
            tables["prevalence_per_run"],
            [
                "detector",
                "seed",
                "original_ap50",
                "standardized_custom_ap50",
                "original_precision",
                "standardized_precision",
                "original_recall",
                "standardized_recall",
                "image_weight_ess",
            ],
        ),
        table(
            tables["prevalence_intervals"],
            [
                "mode",
                "metric",
                "a_estimate",
                "a_ci_low",
                "a_ci_high",
                "b_estimate",
                "b_ci_low",
                "b_ci_high",
                "a_valid",
                "a_undefined",
                "b_valid",
                "b_undefined",
            ],
        ),
        "## Cross-domain changes with shared checkpoint resampling",
        "A = Faster R-CNN; B = YOLO11s. Each change is external minus internal; the difference "
        "is change(A) minus change(B). Observations are paired within domain, independently drawn "
        "between domains; trained runs are independent between detector families and identical "
        "across domains within a family. All intervals are marginal and conditional on the fixed "
        "training data/recipe and retained support. Unknown repeated VinDr patients "
        "remain unresolved.",
        table(
            tables["change_intervals"],
            [
                "metric",
                "a_estimate",
                "a_ci_low",
                "a_ci_high",
                "b_estimate",
                "b_ci_low",
                "b_ci_high",
                "difference_estimate",
                "difference_ci_low",
                "difference_ci_high",
                "a_valid",
                "a_undefined",
                "b_valid",
                "b_undefined",
                "difference_valid",
                "difference_undefined",
            ],
        ),
        "![Population weighting and cross-domain "
        "changes.](../results/external_generalization_v1/prevalence_and_domain_changes.png)",
        "## Candidate support",
        "Per-run floor, minimum score, cap fraction and budget flags are in candidate_support.csv. "
        "These conservative upper values replace only floor-limited runs with one; they are not "
        "confidence bounds and cannot repair cap saturation. No extrapolation or new "
        "inference occurred.",
        table(
            tables["candidate_support_means"],
            ["dataset", "detector", "budget", "quantity", "mean", "sd"],
        ),
        "## Interpretation boundary",
        "These measurements separate emission/score/geometry/annotation disagreement "
        "in the retained "
        "outputs. They do not identify biological, acquisition or annotation causes. "
        "A spatial match "
        "to another class is not validated clinical correctness. Stronger evidence "
        "about degradation "
        "does not establish clinical utility, and an observed AP ordering does not "
        "establish superiority "
        "on an unsupported full FROC frontier. Further candidate collection and "
        "expert target review "
        "are separate proposed work. See the accompanying scientific interpretation document.",
    ]
    Path(config["outputs"]["report"]).write_text(
        "\n\n".join(sections) + "\n", encoding="utf-8", newline="\n"
    )
    return figures
