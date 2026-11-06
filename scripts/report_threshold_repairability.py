"""Render public repairability tables/figures without loading private prediction arrays."""

from __future__ import annotations

import argparse
import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.stats.run_threshold_repairability import read_csv
from src.stats.run_vindr_statistics import (
    artifact,
    read_json,
    read_yaml,
    require,
    verify_artifact,
    write_json,
)
from src.stats.threshold_repairability import METRICS


def render(config_path: Path, *, replay: bool = False) -> dict:
    config = read_yaml(config_path)
    analysis = read_yaml(config["analysis_config"])
    root = Path(analysis["outputs"]["public_root"])
    summary_path = root / analysis["outputs"]["summary"]
    summary = read_json(summary_path)
    public = [e for e in summary["artifacts"] if Path(e["path"]).is_relative_to(root)]
    inputs = [
        artifact(summary_path),
        *public,
        artifact(config_path),
        artifact(config["analysis_config"]),
        artifact(Path(__file__)),
    ]
    for entry in inputs:
        verify_artifact(entry)
    receipt = Path(config["outputs"]["receipt"])
    if replay:
        old = read_json(receipt)
        for entry in [*old["inputs"], *old["outputs"]]:
            verify_artifact(entry)
    else:
        require(
            not any(Path(p).exists() for p in config["outputs"].values()),
            "Report outputs exist; use replay",
        )
    budget = analysis["analysis"]["primary_budget"]
    intervals = [
        r for r in read_csv(root / analysis["outputs"]["intervals"]) if float(r["budget"]) == budget
    ]
    controls = [
        r
        for r in read_csv(root / analysis["outputs"]["perturbation_summary"])
        if float(r["budget"]) == budget
    ]
    contrasts = [
        r for r in read_csv(root / analysis["outputs"]["contrasts"]) if float(r["budget"]) == budget
    ]
    index = {(r["dataset"], r["detector"], r["metric"]): r for r in intervals}
    groups = [(d, m) for d in summary["datasets"] for m in summary["detectors"]]
    plot = config["plot"]
    labels = [f"{plot['dataset_labels'][d]}\n{plot['detector_labels'][m]}" for d, m in groups]
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(
        1, 2, figsize=plot["figure_size"], sharey=True, gridspec_kw={"width_ratios": [1.25, 1]}
    )
    left = np.zeros(len(groups))
    names = ["Cutoff ceiling", "FP-budget barrier", "Assignment gap", "Unavailable geometry"]
    for metric, color, name in zip(METRICS[:4], plot["component_colors"], names, strict=True):
        values = np.array([float(index[d, m, metric]["point"]) for d, m in groups])
        axes[0].barh(np.arange(len(groups)), values, left=left, color=color, height=0.6, label=name)
        left += values
    axes[0].set_yticks(np.arange(len(groups)), labels)
    axes[0].invert_yaxis()
    axes[0].set_title("A  Recall accounting", loc="left", weight="bold")
    for metric, offset, marker, color, name in [
        ("threshold_ceiling", -0.1, "o", plot["component_colors"][0], "Cutoff ceiling"),
        ("geometry_ceiling", 0.1, "s", "#545D65", "Geometry ceiling"),
    ]:
        vals = np.array(
            [
                [float(index[d, m, metric][k]) for k in ["point", "lower", "upper"]]
                for d, m in groups
            ]
        )
        axes[1].errorbar(
            vals[:, 0],
            np.arange(len(groups)) + offset,
            xerr=[vals[:, 0] - vals[:, 1], vals[:, 2] - vals[:, 0]],
            fmt=marker,
            color=color,
            capsize=3,
            label=name,
        )
    axes[1].set_title("B  Marginal 95% intervals", loc="left", weight="bold")
    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_xlabel("Fraction of reference boxes")
        ax.grid(axis="x", alpha=0.17)
        ax.set_axisbelow(True)
    axes[1].legend(loc="lower right", fontsize=8)
    fig.legend(
        *axes[0].get_legend_handles_labels(), loc="lower center", ncol=4, fontsize=9, frameon=False
    )
    fig.suptitle(f"Limits of cutoff repair at {budget:g} FP/image", weight="bold")
    fig.tight_layout(rect=[0, 0.09, 1, 0.94])
    first = io.BytesIO()
    fig.savefig(first, format="png", dpi=plot["dpi"])
    plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=plot["controls_size"], sharex=True, sharey="row")
    families = analysis["perturbations"]["families"]
    titles = ["Permute scores", "Remove compatible boxes", "Remove incompatible boxes"]
    for col, (family, title) in enumerate(zip(families, titles, strict=True)):
        axes[0, col].set_title(title)
        for g, (dataset, detector) in enumerate(groups):
            selected = [
                r
                for r in controls
                if (r["dataset"], r["detector"], r["family"]) == (dataset, detector, family)
            ]
            selected.sort(key=lambda r: float(r["level"]))
            x = [0, *[float(r["level"]) for r in selected]]
            for row, metric in enumerate(["threshold_ceiling", "geometry_ceiling"]):
                axes[row, col].plot(
                    x,
                    [0, *[float(r[f"delta_{metric}"]) for r in selected]],
                    marker="o",
                    color=plot["series_colors"][g],
                    linestyle="-" if dataset == "internal" else "--",
                    label=labels[g].replace("\n", " / "),
                )
        for row in range(2):
            axes[row, col].axhline(0, color="#777777", lw=0.7)
            axes[row, col].grid(alpha=0.15)
            axes[row, col].set_xticks([0, *analysis["perturbations"]["fractions"]])
        axes[1, col].set_xlabel("Fraction of eligible candidates")
    axes[0, 0].set_ylabel("Change in cutoff ceiling")
    axes[1, 0].set_ylabel("Change in geometry ceiling")
    fig.legend(
        *axes[0, 0].get_legend_handles_labels(),
        loc="lower center",
        ncol=2,
        fontsize=8,
        frameon=False,
    )
    fig.suptitle("Controlled output changes: equal-run means, replicate-averaged", weight="bold")
    fig.tight_layout(rect=[0, 0.1, 1, 0.94])
    second = io.BytesIO()
    fig.savefig(second, format="png", dpi=plot["dpi"])
    plt.close(fig)

    def formatted(row):
        return f"{float(row['point']):.6f} [{float(row['lower']):.6f}, {float(row['upper']):.6f}]"

    lines = [
        "# Threshold repairability v2: complete computational results",
        "",
        "Exploratory analysis of original retained candidates. No new inference, training, "
        "threshold fitting or clinical relabeling.",
        "",
        f"All {len(summary['seeds'])} checkpoints per detector, both complete cohorts "
        f"({summary['images'][0]} internal / {summary['images'][1]} external images), "
        f"{summary['internal_patient_groups']} known internal patient groups and "
        f"{summary['bootstrap_resamples']:,} joint draws. "
        f"All {summary['control_interventions']} controlled interventions passed their "
        f"specified invariants.",
        "",
        "[Protocol](THRESHOLD_REPAIRABILITY_PROTOCOL_V2.md) | [Exact "
        "provenance](../results/threshold_repairability_v2/summary.json) | "
        "[Reproduction commands](../README.md#threshold-repairability-v2)",
        "",
        f"## Components at {budget:g} FP/image",
        "",
        "1 = cutoff ceiling + FP-budget barrier + assignment gap + unavailable geometry. "
        "Components describe fixed-output limits, not causal fractions of external loss. "
        "Intervals are marginal percentile intervals; their separate endpoints need not sum to "
        "one.",
        "",
        "| Cohort / detector | Component | Mean [95% CI] | Valid / undefined |",
        "|---|---|---:|---:|",
    ]
    for d, m in groups:
        for metric in METRICS:
            item = index[d, m, metric]
            lines.append(
                f"| {plot['dataset_labels'][d]} / {plot['detector_labels'][m]} | {metric} | "
                f"{formatted(item)} | {item['valid']} / {item['undefined']} |"
            )
    lines.extend(
        [
            "",
            "![Recall accounting and joint-bootstrap "
            "intervals](../results/threshold_repairability_v2/repairability.png)",
            "",
            "Historical feasibility is a fraction of selected runs; a negative signed cutoff "
            "difference is retained when the historical policy exceeds the budget. "
            "The cutoff ceiling averages per-run optimistic envelopes, not one common cutoff "
            "or an exported policy.",
            "",
            "## Coupled contrasts",
            "",
            "Internal patient clusters and external images are sampled independently. Each "
            "cohort's observations are shared across detectors and runs. "
            "Run multiplicities are independent between detectors and reused for the same "
            "checkpoints across cohorts. "
            "Every nonlinear endpoint is recomputed within each draw. Unknown external patient "
            "dependence remains a limitation.",
            "",
            "| Contrast | Component | Change [95% CI] | Valid / undefined |",
            "|---|---|---:|---:|",
        ]
    )
    for r in contrasts:
        if r["metric"] in METRICS[:6]:
            lines.append(
                f"| {r['contrast']} | {r['metric']} | {formatted(r)} | {r['valid']} / "
                f"{r['undefined']} |"
            )
    lines.extend(
        [
            "",
            "## Controlled output changes",
            "",
            "These interventions modify copies of saved outputs and use reference labels only "
            "for diagnostic controls. "
            "They do not estimate performance of an implementable repair. Three imposed "
            "replicates are averaged within each checkpoint before equal-run averaging; "
            "they are not extra training runs or patients. Score powers preserve the entire "
            "exact frontier; score permutations preserve geometry but can improve or worsen "
            "ranked recall. "
            "Removing all compatible candidates eliminates geometric coverage. Removing "
            "incompatible candidates cannot worsen the frontier. All effects, including null "
            "and adverse ones, are retained.",
            "",
            "| Cohort / detector | Family | Level | Cutoff-ceiling change | Geometry-ceiling "
            "change | Historical-recall change |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for r in controls:
        lines.append(
            f"| {r['dataset']} / {plot['detector_labels'][r['detector']]} | {r['family']} | "
            f"{float(r['level']):g} | "
            f"{float(r['delta_threshold_ceiling']):+.6f} | "
            f"{float(r['delta_geometry_ceiling']):+.6f} | "
            f"{float(r['delta_historical_recall']):+.6f} |"
        )
    lines.extend(
        [
            "",
            "![Controlled output changes](../results/threshold_repairability_v2/controls.png)",
            "",
            "## Scope and audit trail",
            "",
            "Exact FROC already supplies the cutoff ceiling and all-candidate recall. This "
            "analysis adds their interpretation alongside maximum geometric matching, "
            "coupled uncertainty and controlled verification; it does not propose a new "
            "ranking metric, prove a new theorem, or claim superiority over TIDE/LRP. "
            "Strictly increasing global score maps preserve prefixes when "
            "membership/ties/postprocessing remain fixed. Feature-dependent reranking, changed "
            "geometry, "
            "NMS, ontology, score floor or cap lie outside that bound. Original internal FP32 "
            "versus external AMP provenance remains unchanged.",
            "",
            "All baseline FROC, support and historical count checks passed; external maximum "
            "matching agrees with the prior census-positive diagnostic. "
            "Source/protocol hashes were checked before and after computation. The original "
            "scientific records and the separate v1 pilot remain unchanged.",
            "",
            "Complete machine-readable outputs retain all original budgets:",
            "",
            "- [Per-run components](../results/threshold_repairability_v2/per_run.csv)",
            "- [Marginal component intervals](../results/threshold_repairability_v2/intervals.csv)",
            "- [Joint contrasts](../results/threshold_repairability_v2/contrasts.csv)",
            "- [Every imposed "
            "intervention](../results/threshold_repairability_v2/perturbations.csv)",
            "- [Replicate-averaged "
            "controls](../results/threshold_repairability_v2/perturbation_summary.csv)",
            "",
            "Private joint arrays enable exact replay without publishing images, image "
            "identifiers, prediction arrays or restricted annotations. "
            "Confidence intervals condition on the available training sample, five checkpoints "
            "and references. Clinical equivalence and causal attribution remain unestablished.",
            "",
        ]
    )
    rendered = {
        "figure": first.getvalue(),
        "controls": second.getvalue(),
        "report": "\n".join(lines).encode("utf-8"),
    }
    for key, data in rendered.items():
        path = Path(config["outputs"][key])
        if replay:
            require(path.read_bytes() == data, f"Report replay differs: {key}")
        else:
            path.write_bytes(data)
    if not replay:
        write_json(
            receipt,
            dict(inputs=inputs, outputs=[artifact(config["outputs"][key]) for key in rendered]),
        )
    return {
        "status": "exact_report_replay_passed" if replay else "report_written",
        "outputs": list(rendered),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    print(render(args.config, replay=args.replay))
