"""Recombine verified public tables into a descriptive threshold-repair audit.

No inference, threshold selection, clinical relabeling or new confidence intervals.
All source endpoints remain conditional on the original retained candidate set.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml

COMPONENTS = (
    "historical_recall",
    "cutoff_headroom",
    "budget_barrier",
    "assignment_gap",
    "unavailable_geometry",
)


def binding(path: Path) -> dict:
    """Describe exact input bytes without modifying a prior manifest."""
    return {"path": path.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def require(condition: bool, message: str) -> None:
    """Fail rather than silently repair inconsistent scientific inputs."""
    if not condition:
        raise ValueError(message)


def components(
    historical: float,
    ceiling: float,
    all_retained: float,
    geometry: float,
    historical_fp: float,
    budget: float,
    tolerance: float,
) -> dict[str, float]:
    """Partition aggregate recall under an explicitly feasible historical policy."""
    values = np.asarray([historical, ceiling, all_retained, geometry])
    require(np.isfinite(values).all(), "Nonfinite recall")
    require(np.all((values >= 0) & (values <= 1)), "Recall outside [0, 1]")
    require(
        np.isfinite([historical_fp, budget, tolerance]).all()
        and min(historical_fp, budget, tolerance) >= 0,
        "Invalid false-positive budget or tolerance",
    )
    require(historical_fp <= budget + tolerance, "Historical policy exceeds budget")
    require(np.all(np.diff(values) >= -tolerance), "Recall ceilings are not nested")
    result = dict(zip(COMPONENTS, [historical, *np.diff(values), 1 - geometry], strict=True))
    require(abs(sum(result.values()) - 1) <= tolerance, "Recall identity failed")
    return result


def read_rows(path: str) -> list[dict]:
    """Load an aggregate CSV, never an image-linked prediction bundle."""
    with Path(path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def unique_runs(rows: list[dict]) -> dict[tuple[str, int], dict]:
    """Reject duplicates before joining by detector and checkpoint seed."""
    keyed = {(r["detector"], int(r["seed"])): r for r in rows}
    require(len(keyed) == len(rows), "Duplicate detector/seed rows")
    return keyed


def calculate(config: dict, protocol: dict) -> tuple[list[dict], list[dict]]:
    """Validate the census-positive join and preserve every frozen budget/run."""
    source = config["sources"]
    stats = unique_runs(
        [r for r in read_rows(source["statistics"]["path"]) if r["dataset"] == config["dataset"]]
    )
    geometry = unique_runs(
        [r for r in read_rows(source["geometry"]["path"]) if r["arm"] == config["baseline_arm"]]
    )
    detectors, seeds = (protocol["models"][k] for k in ("detectors", "seeds"))
    expected = {(d, seed) for d in detectors for seed in seeds}
    require(set(stats) == set(geometry) == expected, "Incomplete detector/run population")
    intervals = [
        r
        for r in read_rows(source["intervals"]["path"])
        if r["dataset"] == config["dataset"] and r["estimand"] == "training_procedure"
    ]
    froc = protocol["evaluation"]["froc"]
    tolerance = froc["numeric_tolerance"]
    budgets = froc["fp_per_image_budgets"]
    require(config["focus_budget"] in budgets, "Focus budget was not in frozen protocol")
    rows = []
    for detector in detectors:
        for seed in seeds:
            r, g = stats[detector, seed], geometry[detector, seed]
            require(
                abs(float(r["primary_recall"]) - float(g["historical_recall"])) <= tolerance,
                "Historical recall differs between joined sources",
            )
            for budget in budgets:
                result = components(
                    float(r["primary_recall"]),
                    float(r[f"froc_{budget:g}"]),
                    float(r["floor_sensitivity"]),
                    float(g[config["geometry_endpoint"]]),
                    float(r["primary_fp_per_image"]),
                    budget,
                    tolerance,
                )
                require(r[f"floor_limited_{budget:g}"] in ("True", "False"), "Invalid flag")
                rows.append(
                    dict(
                        detector=detector,
                        seed=seed,
                        budget=budget,
                        images=int(r["images"]),
                        positive_images=int(r["positive_images"]),
                        target_boxes=int(r["target_boxes"]),
                        **result,
                        threshold_ceiling=float(r[f"froc_{budget:g}"]),
                        geometry_ceiling=float(g[config["geometry_endpoint"]]),
                        historical_fp_per_image=float(r["primary_fp_per_image"]),
                        floor_limited=r[f"floor_limited_{budget:g}"] == "True",
                    )
                )
    aggregate = []
    for index, detector in enumerate(detectors):
        for budget in budgets:
            group = [r for r in rows if r["detector"] == detector and r["budget"] == budget]
            point = {
                key: float(np.mean([r[key] for r in group]))
                for key in (*COMPONENTS, "threshold_ceiling", "geometry_ceiling")
            }
            interval = [r for r in intervals if r["metric"] == f"froc_{budget:g}"]
            require(len(interval) == 1, "Missing or duplicate source interval")
            prefix = ("a", "b")[index]
            interval = interval[0]
            require(
                abs(point["threshold_ceiling"] - float(interval[f"{prefix}_estimate"]))
                <= tolerance,
                "Source interval point differs from run mean",
            )
            aggregate.append(
                dict(
                    detector=detector,
                    budget=budget,
                    runs=len(group),
                    **point,
                    threshold_ceiling_ci_low=float(interval[f"{prefix}_ci_low"]),
                    threshold_ceiling_ci_high=float(interval[f"{prefix}_ci_high"]),
                    source_interval_draws=int(interval["bootstrap_resamples"]),
                    floor_limited_runs=sum(r["floor_limited"] for r in group),
                )
            )
    return rows, aggregate


def csv_bytes(rows: list[dict]) -> bytes:
    """Use deterministic, portable CSV serialization."""
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def figure_bytes(rows: list[dict], config: dict) -> bytes:
    """Draw the exploratory point estimates without implying new intervals."""
    selected = [r for r in rows if r["budget"] == config["focus_budget"]]
    settings = config["figure"]
    fig, ax = plt.subplots(figsize=settings["size_inches"], layout="constrained")
    left = np.zeros(len(selected))
    labels = [
        "Detected at historical cutoff",
        "Additional recall possible by cutoff alone",
        "Retained matches beyond the FP budget",
        "Greedy-assignment gap",
        "No one-to-one retained geometry",
    ]
    for key, label, color in zip(COMPONENTS, labels, settings["colors"], strict=True):
        widths = np.asarray([r[key] for r in selected]) * 100
        ax.barh(np.arange(len(selected)), widths, left=left, color=color, label=label, height=0.46)
        for i, width in enumerate(widths):
            if width >= 10:
                ax.text(left[i] + width / 2, i, f"{width:.1f}%", ha="center", va="center")
        left += widths
    ax.set_yticks(
        np.arange(len(selected)),
        [
            f"{settings['names'][r['detector']]}\n"
            f"Cutoff ceiling: {100 * r['threshold_ceiling']:.1f}%"
            for r in selected
        ],
    )
    ax.invert_yaxis()
    ax.set(xlim=(0, 100), xlabel="Fraction of strict-reference boxes (%)")
    ax.set_title(
        f"Limits of threshold repair at {config['focus_budget']:g} FP/image\n"
        "Frozen retained candidates; equal-run point estimates"
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False)
    fig.suptitle(
        "Descriptive feasibility audit; intervals for new components are not estimated",
        fontsize=10,
    )
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=settings["dpi"])
    plt.close(fig)
    return buffer.getvalue()


def run(config_path: Path, *, verify: bool = False) -> dict:
    """Create once, or exactly replay, a separately identified feasibility package."""
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    for item in config["sources"].values():
        require(binding(Path(item["path"])) == item, f"Source hash mismatch: {item['path']}")
    protocol = yaml.safe_load(Path(config["sources"]["protocol"]["path"]).read_text())
    require(len(protocol["models"]["detectors"]) == 2, "Source interval has two detector columns")
    rows, aggregate = calculate(config, protocol)
    outputs = config["outputs"]
    root = Path(outputs["root"])
    files = {
        outputs["per_run"]: csv_bytes(rows),
        outputs["aggregate"]: csv_bytes(aggregate),
        outputs["figure"]: figure_bytes(aggregate, config),
    }
    summary = dict(
        analysis_id=config["analysis_id"],
        status=config["status"],
        scope="Descriptive aggregate recombination; not a new clinical or causal result",
        uncertainty="Ceiling intervals copied from verified source; no component intervals",
        inventory="Separate feasibility package; not integrated into the manuscript inventory",
        candidate_floor=protocol["evaluation"]["candidate_score_floor"],
        candidate_cap=protocol["evaluation"]["max_detections_per_image"],
        match_iou=protocol["evaluation"]["matching_iou_threshold"],
        inputs=[
            *config["sources"].values(),
            binding(config_path),
            *[binding(Path(p)) for p in config["source_files"]],
        ],
        artifacts=[
            {"path": (root / name).as_posix(), "sha256": hashlib.sha256(data).hexdigest()}
            for name, data in files.items()
        ],
        aggregate=aggregate,
    )
    files[outputs["summary"]] = (json.dumps(summary, indent=2, allow_nan=False) + "\n").encode()
    if verify:
        for name, data in files.items():
            require((root / name).read_bytes() == data, f"Replay mismatch: {name}")
    else:
        root.mkdir(parents=True, exist_ok=False)
        for name, data in files.items():
            (root / name).write_bytes(data)
    print(
        f"{'Verified' if verify else 'Created'} {len(rows)} run/budget rows "
        f"and {len(aggregate)} means"
    )
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    run(args.config, verify=args.verify)
