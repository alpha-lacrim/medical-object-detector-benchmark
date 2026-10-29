"""Offline post-hoc external diagnostics with immutable input gates and replay."""

from __future__ import annotations

import argparse
import csv
import json
import platform
from collections import defaultdict
from importlib.metadata import version
from pathlib import Path
from typing import Any

import numpy as np

from scripts.verify_frozen_external import baseline_paths, historical_editorial_view
from src.data.prepare_vindr import ensure_private, resolve_root
from src.evaluate_vindr_external import deserialize, read_gzip
from src.stats.external_generalization import (
    ap_events,
    error_decomposition,
    joint_bootstrap,
    local_annotations,
    prevalence_metrics,
    prevalence_weights,
)
from src.stats.paired import json_number
from src.stats.run_statistics import load_coco_targets
from src.stats.run_vindr_statistics import (
    artifact,
    close,
    prepare_dataset,
    read_json,
    read_yaml,
    require,
    summarize_values,
    verify_artifact,
    write_csv,
    write_json,
)
from src.stats.run_vindr_statistics import (
    preflight as baseline_preflight,
)
from src.stats.transportability import interval_rows


def preflight(config_path: Path) -> dict:
    """Verify original hashes, exact run identities and restricted source annotations."""
    config = read_yaml(config_path)
    require(config["status"] == "posthoc_exploratory", "Post-hoc status is mandatory")
    with historical_editorial_view(Path.cwd()):
        gate = baseline_preflight(Path(config["statistics_config"]))
    protocol = gate["protocol"]
    ensure_private(
        Path(config["outputs"]["private_root"]) / config["outputs"]["draws"],
        Path(protocol["outputs"]["private_root"]),
    )
    source = resolve_root(protocol) / protocol["dataset"]["paths"]["boxes"]
    require(
        artifact(source)["sha256"] == protocol["dataset"]["source_sha256"]["boxes"],
        "Source annotations differ from the frozen release",
    )
    targets, _ = load_coco_targets(Path(protocol["outputs"]["local_annotations"]))
    with source.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    annotations, audit = local_annotations(rows, targets, protocol, config["analysis"])
    require(
        not set(audit["local_box_counts"]) & set(config["analysis"]["global_labels_excluded"]),
        "Global labels cannot supply localization boxes",
    )
    require(
        set(config["analysis"]["non_target_classes"]).issubset(audit["local_box_counts"]),
        "Requested non-target local labels absent",
    )
    mapped = baseline_paths(Path.cwd())
    inputs = []
    for entry in gate["inputs"]:
        path = mapped.get(Path(entry["path"]).resolve(), Path(entry["path"]))
        item = artifact(path)
        require(item["sha256"] == entry["sha256"], "Baseline input binding changed")
        inputs.append(item)
    extra = [config_path, config["protocol_document"], source, *config["source_files"]]
    inputs.extend(artifact(p) for p in extra)
    return {
        "config": config,
        "baseline": gate,
        "inputs": inputs,
        "targets": targets,
        "annotations": annotations,
        "annotation_audit": audit,
    }


def aggregate(rows: list[dict], keys: list[str], fields: list[str]) -> list[dict]:
    """Average each per-run quantity equally, retaining undefined denominators."""
    groups: dict = defaultdict(list)
    for row in rows:
        groups[tuple(row[k] for k in keys)].append(row)
    return [
        {
            **dict(zip(keys, key, strict=True)),
            "quantity": field,
            **summarize_values([r[field] for r in values]),
        }
        for key, values in sorted(groups.items())
        for field in fields
    ]


def intervals(points: dict, arrays: dict, config: dict) -> tuple[list, list]:
    """Reconstruct marginal intervals from saved draws without any favorable retry."""
    analysis = config["analysis"]
    change = interval_rows(
        np.asarray(points["change"]),
        arrays["changes"],
        analysis["change_endpoints"],
        analysis["confidence_level"],
    )
    prev = []
    for mode, index in (("original", 0), ("standardized", 1), ("change", None)):
        samples = (
            arrays["prevalence"][:, index]
            if index is not None
            else (arrays["prevalence"][:, 1] - arrays["prevalence"][:, 0])
        )
        point = np.asarray(points["prevalence"])
        point = point[index] if index is not None else point[1] - point[0]
        prev.extend(
            {"mode": mode, **row}
            for row in interval_rows(
                point,
                samples,
                ["custom_weighted_ap50", "historical_precision"],
                analysis["confidence_level"],
            )
        )
    return change, prev


def analyze(gate: dict) -> tuple[dict, dict]:
    """Run reference/FP audits first, then existing-metric and new-contrast replays."""
    config, baseline = gate["config"], gate["baseline"]
    protocol = baseline["protocol"]
    evaluation = {
        **protocol["evaluation"],
        "class_ids": tuple(protocol["ontology"]["canonical_classes"]),
    }
    analysis = config["analysis"]
    tables: dict = defaultdict(list)
    for source in baseline["external"]["runs"]:
        detector, seed = source["metadata"]["detector"], source["metadata"]["seed"]
        ps = deserialize(read_gzip(Path(source["artifacts"][0]["path"]))["predictions"])
        result = error_decomposition(
            ps,
            gate["targets"],
            gate["annotations"],
            threshold=protocol["threshold_transport"]["primary"]["thresholds"][detector],
            evaluation=evaluation,
            analysis=analysis,
            strict_label=protocol["ontology"]["source_exact_class_name"],
        )
        historical = next(r for r in result["operating"] if r["support"] == "historical")
        expected = source["metrics"]["threshold_transport"]["primary"]
        require(
            all(historical[k] == expected[k] for k in ("tp", "fp", "detections")),
            "Error taxonomy disagrees with canonical operating counts",
        )
        for name, rows in result.items():
            tables[name].extend({"detector": detector, "seed": seed, **r} for r in rows)
        print(f"Reconciled external error categories: {detector} seed {seed}", flush=True)
    internal, irows, iscores, _, clusters = prepare_dataset(baseline, "internal")
    external, erows, escores, _, _ = prepare_dataset(baseline, "external")
    for row in [*irows, *erows]:
        score = next(
            s
            for s in [*iscores, *escores]
            if s["dataset"] == row["dataset"]
            and s["detector"] == row["detector"]
            and s["seed"] == row["seed"]
            and s["support"] == "all_retained_candidates"
        )
        for budget in evaluation["froc"]["fp_per_image_budgets"]:
            tables["candidate_support"].append(
                {
                    k: row[k]
                    for k in (
                        "dataset",
                        "detector",
                        "seed",
                        "images",
                        "images_at_collection_cap",
                        "floor_fp_per_image",
                        "floor_sensitivity",
                    )
                }
                | {
                    "cap_fraction": row["images_at_collection_cap"] / row["images"],
                    "candidate_floor": evaluation["candidate_score_floor"],
                    "minimum_score": score["min"],
                    "budget": budget,
                    "floor_limited": row[f"floor_limited_{budget:g}"],
                    "observed_sensitivity": row[f"froc_{budget:g}"],
                    "missing_support_upper": 1.0
                    if row[f"floor_limited_{budget:g}"]
                    else row[f"froc_{budget:g}"],
                }
            )
    q = np.mean(external[0][0].ap.target_counts > 0)
    for detector, runs in zip(protocol["models"]["detectors"], internal, strict=True):
        for run in runs:
            ones = np.ones(len(run.ap.image_ids), dtype=int)
            weights = prevalence_weights(run.ap.target_counts, ones, q)
            event = ap_events(run.ap)
            original = prevalence_metrics(run, event, ones, analysis["prevalence_recall_points"])
            standardized = prevalence_metrics(
                run, event, weights, analysis["prevalence_recall_points"]
            )
            canonical = run.ap.evaluate(ones)[0]
            close(
                original[0],
                canonical,
                "Unit-weight AP disagrees with COCO",
                evaluation["froc"]["numeric_tolerance"],
            )
            tp, _ = weights @ run.primary_counts
            tables["prevalence_per_run"].append(
                {
                    "detector": detector,
                    "seed": run.seed,
                    "original_ap50": canonical,
                    "standardized_custom_ap50": standardized[0],
                    "original_precision": original[1],
                    "standardized_precision": standardized[1],
                    "original_recall": run.primary_counts[:, 0].sum() / run.ap.target_counts.sum(),
                    "standardized_recall": tp / (weights @ run.ap.target_counts),
                    "internal_positive_frequency": float(np.mean(run.ap.target_counts > 0)),
                    "target_positive_frequency": float(q),
                    "image_weight_ess": float(weights.sum() ** 2 / (weights @ weights)),
                }
            )
    arrays, points = joint_bootstrap(
        internal,
        external,
        clusters,
        analysis,
        config["analysis_id"],
        evaluation["froc"]["numeric_tolerance"],
    )
    change, prevalence = intervals(points, arrays, config)
    tables["change_intervals"], tables["prevalence_intervals"] = change, prevalence
    for name, keys, fields in (
        ("reference_errors", ["detector", "category"], ["count", "fraction"]),
        ("false_positives", ["detector", "support", "category"], ["count", "fraction"]),
        ("non_target_overlaps", ["detector", "support", "class_name"], ["count", "fraction"]),
        ("availability", ["detector", "iou"], ["count", "fraction"]),
        (
            "candidate_support",
            ["dataset", "detector", "budget"],
            ["observed_sensitivity", "missing_support_upper"],
        ),
    ):
        tables[name + "_means"] = aggregate(tables[name], keys, fields)
    return {
        "status": "complete",
        "analysis_id": config["analysis_id"],
        "status_of_findings": "posthoc_exploratory",
        "baseline_commit": config["baseline_commit"],
        "annotation_audit": gate["annotation_audit"],
        "points": points,
        "tables": dict(tables),
        "inputs": gate["inputs"],
        "environment": {
            "python": platform.python_version(),
            **{p: version(p) for p in ("numpy", "pycocotools", "matplotlib", "PyYAML")},
        },
        "bootstrap_support": {
            "any_limited_draws": int(
                np.count_nonzero(np.any(arrays["floor_limited_selected_runs"] > 0, axis=(1, 2)))
            )
        },
    }, arrays


def verify(config_path: Path, replay: bool = False) -> dict:
    """Verify immutable inputs/output hashes and saved-draw reconstruction; optionally recompute."""
    config = read_yaml(config_path)
    out = config["outputs"]
    saved = read_json(Path(out["public_root"]) / out["summary"])
    for item in saved["inputs"] + saved["artifacts"]:
        verify_artifact(item)
    with np.load(Path(out["private_root"]) / out["draws"], allow_pickle=False) as arrays:
        change, prev = intervals(saved["points"], arrays, config)
        require(
            json_number(change) == saved["tables"]["change_intervals"], "Change intervals differ"
        )
        require(
            json_number(prev) == saved["tables"]["prevalence_intervals"],
            "Prevalence intervals differ",
        )
        if replay:
            fresh, new_arrays = analyze(preflight(config_path))
            for key in ("tables", "points", "annotation_audit", "bootstrap_support"):
                require(json_number(fresh[key]) == saved[key], f"Replay mismatch: {key}")
            for key, values in new_arrays.items():
                require(np.array_equal(values, arrays[key], equal_nan=True), f"Draws differ: {key}")
    return {
        "status": "verified",
        "full_replay": replay,
        "inputs": len(saved["inputs"]),
        "tables": len(saved["tables"]),
        "summary": artifact(Path(out["public_root"]) / out["summary"]),
    }


def run(config_path: Path) -> dict:
    """Write once; keep every private array inside the established ignored data tree."""
    gate = preflight(config_path)
    config, out = gate["config"], gate["config"]["outputs"]
    public, private = Path(out["public_root"]), Path(out["private_root"])
    require(
        not public.exists() and not private.exists() and not Path(out["report"]).exists(),
        "Output already exists; use verify/replay or a separately reviewed version",
    )
    saved, arrays = analyze(gate)
    public.mkdir(parents=True)
    private.mkdir(parents=True)
    draw_path = private / out["draws"]
    np.savez_compressed(draw_path, **arrays)
    for name, rows in saved["tables"].items():
        write_csv(public / f"{name}.csv", rows)
    from src.stats.report_external_generalization import render

    figures = render(json_number(saved), config)
    saved["artifacts"] = [
        artifact(p)
        for p in [draw_path, Path(out["report"]), *sorted(public.glob("*.csv")), *figures]
    ]
    write_json(public / out["summary"], saved)
    return verify(config_path)


def main() -> None:
    """Expose reproducible offline modes without model loading or GPU actions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--mode", choices=("preflight", "run", "verify", "replay"), required=True)
    args = parser.parse_args()
    if args.mode == "preflight":
        gate = preflight(args.config)
        result: dict[str, Any] = {
            "status": "passed",
            "inputs": len(gate["inputs"]),
            "annotation_audit": gate["annotation_audit"],
        }
    elif args.mode == "run":
        result = run(args.config)
    else:
        result = verify(args.config, args.mode == "replay")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
