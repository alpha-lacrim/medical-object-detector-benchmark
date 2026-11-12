"""Generate the separate exploratory research report and figures from bound results."""

from __future__ import annotations

import argparse
import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.stats.run_threshold_repairability import read_csv, verify
from src.stats.run_vindr_statistics import (
    artifact,
    read_json,
    read_yaml,
    require,
    verify_artifact,
    write_json,
)


def number(value: str | float, digits: int = 1) -> str:
    """Render the extended cost without hiding infeasible values."""
    if str(value) == "infinite":
        return "infinity"
    return f"{float(value):.{digits}f}"


def report(
    config: dict, summary: dict, intervals: list, per_run: list, correction: list, annotation: list
) -> str:
    """Produce every numerical table from the accepted aggregate results."""
    budget = config["primary_budget"]
    selected = [r for r in intervals if float(r["budget"]) == budget]
    lookup = {
        (r["dataset"], r["detector"], float(r["target_recall"]), r["metric"]): r for r in selected
    }
    text = [
        "# Constrained repairability v1: exploratory results",
        "",
        "Generated from the separately hash-bound saved-output analysis. All costs are",
        "retrospective annotation-informed membership oracles, with free optimal",
        "assignment. They are not achieved performance or clinical correction effort.",
        "",
        f"All {len(summary['seeds'])} seeds per detector, both full cohorts, all "
        f"{len(summary['budgets'])} original budgets and all {len(summary['target_recalls'])} "
        f"target levels are included: {len(per_run)} exact flow/formula comparisons.",
        f"Infeasible run/grid cells: {sum(r['feasible'] == 'False' for r in per_run)}.",
        f"All {summary['rows']['perturbations']} imposed output controls passed.",
        "",
        "## Target costs at the original presentation budget",
        "",
        f"Budget {budget:g} FP/image. Unit cost counts promotions plus suppressions.",
        "The mean is infinite if any retained run is infeasible. Fractions are over",
        "the five observed runs. Brackets are marginal 95% joint observation/run",
        f"bootstrap percentile intervals ({summary['bootstrap_resamples']:,} draws; "
        "inverse empirical CDF).",
        "Infinity remains in the resampling distribution. It is not replaced by a finite average.",
        "",
        "| Cohort | Detector | Target recall | Feasible runs | Mean edits [95% interval] | "
        "Edits/reference | Edits/image | Infinite cost draws |",
        "|---|---|---:|---:|---|---:|---:|---:|",
    ]
    for dataset in summary["datasets"]:
        for detector in summary["detectors"]:
            for target in summary["target_recalls"]:
                key = dataset, detector, target
                cost = lookup[*key, "cost"]
                feasible = lookup[*key, "feasible_fraction"]
                n = round(float(feasible["point"]) * len(summary["seeds"]))
                normalized = lookup[*key, "cost_per_reference"]["point"]
                per_image = lookup[*key, "cost_per_image"]["point"]
                text.append(
                    f"| {dataset} | {detector} | {target:.0%} | {n}/{len(summary['seeds'])} | "
                    f"{number(cost['point'])} [{number(cost['lower'])}, {number(cost['upper'])}] | "
                    f"{number(normalized, 3)} | {number(per_image, 4)} | {cost['infinite']} |"
                )
    text += [
        "",
        "No undefined draws occurred in this real-data run; zero-reference synthetic",
        "draws remain explicitly undefined. Every budget and normalized interval is in",
        "[intervals.csv](../results/constrained_repairability_v1/intervals.csv).",
        "",
        "![All budgets and targets](../results/constrained_repairability_v1/cost_surface.png)",
        "",
        "## Counts and existing diagnostics",
        "",
        "Equal-run means. H is the historical selected count; r is its maximum",
        "matching count; M is full retained maximum matching. The new analysis",
        "checked that r equals historical greedy TP in every baseline run.",
        "",
        "| Cohort | Detector | H | r | M | Reference boxes | "
        f"FROC ceiling at {budget:g} | Geometric coverage |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for dataset in summary["datasets"]:
        for detector in summary["detectors"]:
            rows = [
                r
                for r in per_run
                if r["dataset"] == dataset
                and r["detector"] == detector
                and float(r["budget"]) == budget
                and float(r["target_recall"]) == summary["target_recalls"][0]
            ]
            values = [
                np.mean([float(r[k]) for r in rows])
                for k in (
                    "historical_selected",
                    "historical_rank",
                    "full_rank",
                    "references",
                    "froc_recall",
                    "geometry_recall",
                )
            ]
            text.append(
                f"| {dataset} | {detector} | {values[0]:.1f} | {values[1]:.1f} | "
                f"{values[2]:.1f} | {values[3]:.0f} | {values[4]:.6f} | {values[5]:.6f} |"
            )
    text += [
        "",
        "All external historical FP counts already fit the smallest original budget.",
        "Consequently, all feasible external unit-cost optima require zero suppression",
        "and depend only on K-r; increasing the FP budget leaves these costs unchanged.",
        "This demonstrates the gap between ideal reference-informed promotions and a",
        "real score-prefix policy; it does not demonstrate successful repair.",
        "",
        "## Conditional annotation-edit sensitivity",
        "",
        "| Cohort | Mean geometric count gap A-B | Largest integer k certifying strict A>B | "
        "k/original references |",
        "|---|---:|---:|---:|",
    ]
    for dataset in summary["datasets"]:
        rows = [r for r in annotation if r["dataset"] == dataset]
        certified = [r for r in rows if r["strict_a_above_b"] == "True"]
        last = certified[-1]
        text.append(
            f"| {dataset} | {float(rows[0]['difference']):.1f} | {last['edits']} | "
            f"{float(last['edits_per_original_reference']):.3f} |"
        )
    text += [
        "",
        "A=Faster R-CNN; B=YOLO11s. The theorem concerns shared reference insertions/",
        "deletions with fixed candidates; relocation counts as two. It does not bound",
        "FROC, estimate label error, establish clinical equivalence, or show the bound",
        "can actually be attained. Curves are deterministic, not confidence bands.",
        "",
        "![Annotation sensitivity]"
        "(../results/constrained_repairability_v1/annotation_sensitivity.png)",
        "",
        "## OC-cost diagnostic comparison",
        "",
        "Independent equation-based implementation, lambda=0.5 and beta=0.6, with",
        "the authors' dummy transport convention and zero cost for empty/empty images.",
        "Equal image weighting then equal run weighting; descriptive means, no CIs.",
        "No postprocessing parameter was optimized for this comparison.",
        "",
        "| Cohort | Detector | Historical selections | All retained candidates |",
        "|---|---|---:|---:|",
    ]
    for dataset in summary["datasets"]:
        for detector in summary["detectors"]:
            values = [
                np.mean(
                    [
                        float(r["oc_cost_mean"])
                        for r in correction
                        if r["dataset"] == dataset
                        and r["detector"] == detector
                        and r["policy"] == policy
                    ]
                )
                for policy in ("historical", "all_retained")
            ]
            text.append(f"| {dataset} | {detector} | {values[0]:.6f} | {values[1]:.6f} |")
    text += [
        "",
        "Lower OC-cost is better under its own objective. The low external historical",
        "values coexist with severe missed-object failure because empty/empty images",
        "contribute zero and images are weighted equally. The large full-retained",
        "values reflect dense extra predictions. These different estimands should not",
        "be ranked as competing clinical performance measures.",
        "",
        "## Interpretation",
        "",
        "The exact formula is C*=p*(K-r)+ + q*(H-r-B)+ whenever K<=M, infinity otherwise.",
        "Here x+ means max(0,x). Every grid cell agrees with integral minimum-cost flow.",
        "Thus unit costs re-express H,r,M rather than supply an independent diagnostic.",
        "See the [research assessment](CONSTRAINED_REPAIRABILITY_RESEARCH_ASSESSMENT.md)",
        "for full proofs, assumptions, counterexamples, prior work and the NO-GO verdict.",
        "",
    ]
    return "\n".join(text)


def figures(config: dict, summary: dict, intervals: list, annotation: list) -> dict[str, bytes]:
    """Draw cost surfaces and deterministic annotation envelopes without patient data."""
    labels = dict(
        internal="RSNA internal",
        external="VinDr external",
        faster_rcnn="Faster R-CNN",
        yolo11s="YOLO11s",
    )
    targets, budgets = summary["target_recalls"], summary["budgets"]
    fig, axes = plt.subplots(2, 2, figsize=config["style"]["costs_size"], layout="constrained")
    cmap = plt.colormaps["YlGnBu"].copy()
    cmap.set_bad("#eeeeee")
    lookup = {
        (r["dataset"], r["detector"], float(r["budget"]), float(r["target_recall"]), r["metric"]): r
        for r in intervals
    }
    max_cost = max(
        float(r["point"])
        for r in intervals
        if r["metric"] == "cost_per_reference" and r["point"] != "infinite"
    )
    for d, dataset in enumerate(summary["datasets"]):
        for m, detector in enumerate(summary["detectors"]):
            ax = axes[d, m]
            values = np.full((len(budgets), len(targets)), np.nan)
            for b, budget in enumerate(budgets):
                for t, target in enumerate(targets):
                    key = dataset, detector, budget, target
                    raw = lookup[*key, "cost"]["point"]
                    if raw != "infinite":
                        values[b, t] = float(lookup[*key, "cost_per_reference"]["point"])
                    run_count = len(summary["seeds"])
                    feasible = round(float(lookup[*key, "feasible_fraction"]["point"]) * run_count)
                    label = (
                        f"{float(raw):.1f}"
                        if raw != "infinite"
                        else f"inf\n{feasible}/{run_count} feasible"
                    )
                    color = "white" if values[b, t] > max_cost * 0.55 else "black"
                    ax.text(t, b, label, ha="center", va="center", color=color, fontsize=9)
            im = ax.imshow(values, cmap=cmap, vmin=0, vmax=max_cost, aspect="auto")
            ax.set(
                xticks=range(len(targets)),
                xticklabels=[f"{q:.0%}" for q in targets],
                yticks=range(len(budgets)),
                yticklabels=[f"{b:g}" for b in budgets],
                xlabel="Target recall",
                ylabel="FP/image budget",
                title=f"{labels[dataset]} / {labels[detector]}",
            )
    fig.colorbar(im, ax=axes, label="Mean oracle edits per reference (finite cells)", shrink=0.75)
    fig.suptitle(
        "Uniform-cost oracle: cells show mean edit counts; inf retains infeasible runs\n"
        "Retrospective diagnostic with free optimal assignment",
        fontsize=13,
    )
    output = {}
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=config["style"]["dpi"])
    output["costs_figure"] = buffer.getvalue()
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=config["style"]["annotation_size"], layout="constrained")
    for ax, dataset in zip(axes, summary["datasets"], strict=True):
        rows = [r for r in annotation if r["dataset"] == dataset]
        k = np.array([int(r["edits"]) for r in rows])
        gap = float(rows[0]["difference"])
        ax.fill_between(k, gap - k, gap + k, color="#cbdde9")
        ax.plot(k, gap - k, color="#21647b", label="Conditional lower bound D-k")
        ax.plot(k, gap + k, color="#21647b", linestyle="--", label="Conditional upper bound D+k")
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(gap, color="#ae5538", linestyle=":", label="Strict-order certificate ends")
        ax.set(
            xlabel="Shared reference insertions/deletions k",
            ylabel="Mean matching count gap A-B",
            title=f"{labels[dataset]}: original gap {gap:.1f}",
            xlim=(0, k[-1]),
        )
        ax.legend(fontsize=8)
    fig.suptitle(
        "Annotation sensitivity of geometric ranking: deterministic bounds, not FROC intervals"
    )
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=config["style"]["dpi"])
    output["annotation_figure"] = buffer.getvalue()
    plt.close(fig)
    return output


def run(config_path: Path, replay: bool) -> dict:
    """Build or byte-replay the public explanatory artifacts with a separate receipt."""
    config = read_yaml(config_path)
    summary = verify(Path(config["summary"]))
    root = Path(config["summary"]).parent
    intervals, per_run, correction, annotation = [
        read_csv(root / f"{k}.csv")
        for k in ("intervals", "per_run", "correction_comparison", "annotation_sensitivity")
    ]
    outputs = figures(config, summary, intervals, annotation)
    outputs["report"] = report(config, summary, intervals, per_run, correction, annotation).encode(
        "utf-8"
    )
    inputs = [artifact(p) for p in (config_path, config["source"], config["summary"])]
    if replay:
        receipt = read_json(config["outputs"]["receipt"])
        require(receipt["inputs"] == inputs, "Report input hashes changed")
        for item in receipt["artifacts"]:
            verify_artifact(item)
        for key, content in outputs.items():
            require(
                Path(config["outputs"][key]).read_bytes() == content,
                f"Report replay differs: {key}",
            )
        return dict(status="report_byte_replay_passed", outputs=len(outputs))
    require(
        all(not Path(config["outputs"][key]).exists() for key in (*outputs, "receipt")),
        "Report output exists; use replay",
    )
    for key, content in outputs.items():
        Path(config["outputs"][key]).write_bytes(content)
    write_json(
        Path(config["outputs"]["receipt"]),
        dict(inputs=inputs, artifacts=[artifact(config["outputs"][key]) for key in outputs]),
    )
    return dict(status="report_built", outputs=len(outputs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    print(run(args.config, args.replay))
