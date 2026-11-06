"""CPU-only, source-gated joint repairability audit of existing saved predictions."""

from __future__ import annotations

import argparse
import csv
import io
import platform
from pathlib import Path
from time import perf_counter

import numpy as np

from scripts.verify_frozen_external import baseline_paths, historical_editorial_view
from src.data.prepare_vindr import ensure_private
from src.evaluate_vindr_external import deserialize, read_gzip
from src.stats.paired import build_patient_clusters, json_number, stable_rng_seed
from src.stats.run_statistics import load_coco_targets, load_patient_group_map
from src.stats.run_vindr_statistics import (
    artifact,
    close,
    preflight,
    read_json,
    read_yaml,
    require,
    verify_artifact,
    write_csv,
    write_json,
)
from src.stats.threshold_repairability import (
    METRICS,
    bootstrap,
    build_run,
    compatible_masks,
    transform,
    verify_control,
)
from src.stats.transportability import aligned_records


def read_csv(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def interval(point: float, draws: np.ndarray, confidence: float) -> dict:
    finite = draws[np.isfinite(draws)]
    tails = [(1 - confidence) / 2, (1 + confidence) / 2]
    low, high = np.quantile(finite, tails) if len(finite) else (np.nan, np.nan)
    return dict(
        point=point, lower=low, upper=high, valid=len(finite), undefined=len(draws) - len(finite)
    )


def summarize(
    point: np.ndarray,
    draws: np.ndarray,
    datasets: list,
    detectors: list,
    budgets: list,
    confidence: float,
) -> tuple[list, list]:
    """Use coupled draws for every contrast, including difference of domain changes."""
    intervals, contrasts = [], []
    for d, dataset in enumerate(datasets):
        for m, detector in enumerate(detectors):
            for b, budget in enumerate(budgets):
                for k, metric in enumerate(METRICS):
                    intervals.append(
                        dict(
                            dataset=dataset,
                            detector=detector,
                            budget=budget,
                            metric=metric,
                            **interval(point[d, m, b, k], draws[:, d, m, b, k], confidence),
                        )
                    )
    comparisons = (
        [
            (
                f"{datasets[d]}:{detectors[0]}-{detectors[1]}",
                point[d, 0] - point[d, 1],
                draws[:, d, 0] - draws[:, d, 1],
            )
            for d in range(2)
        ]
        + [
            (
                f"external-internal:{detectors[m]}",
                point[1, m] - point[0, m],
                draws[:, 1, m] - draws[:, 0, m],
            )
            for m in range(2)
        ]
        + [
            (
                "difference_of_domain_changes",
                (point[1, 0] - point[0, 0]) - (point[1, 1] - point[0, 1]),
                (draws[:, 1, 0] - draws[:, 0, 0]) - (draws[:, 1, 1] - draws[:, 0, 1]),
            )
        ]
    )
    for name, estimate, samples in comparisons:
        for b, budget in enumerate(budgets):
            for k, metric in enumerate(METRICS):
                contrasts.append(
                    dict(
                        contrast=name,
                        budget=budget,
                        metric=metric,
                        **interval(estimate[b, k], samples[:, b, k], confidence),
                    )
                )
    return intervals, contrasts


def controls(
    predictions,
    targets,
    base,
    *,
    dataset,
    detector,
    seed,
    config,
    evaluation,
    threshold,
    budgets,
    tolerance,
) -> list:
    settings = config["perturbations"]
    mask = compatible_masks(predictions, targets, evaluation["matching_iou_threshold"])
    source_scores = np.sort(np.concatenate([p.scores for p in predictions]))
    ones = np.ones(len(targets), dtype=np.int64)
    baseline = base.evaluate(ones, budgets, tolerance)
    jobs = [("power", power, 0) for power in settings["powers"]] + [
        (family, level, rep)
        for family in settings["families"]
        for level in settings["fractions"]
        for rep in range(settings["replicates"])
    ]
    rows = []
    for family, level, rep in jobs:
        rng = np.random.default_rng(
            stable_rng_seed(settings["seed"], f"{dataset}:{detector}:{seed}:{family}:{rep}")
        )
        changed, selected = transform(predictions, mask, family=family, level=level, rng=rng)
        if family == "permute_scores":
            require(
                np.array_equal(source_scores, np.sort(np.concatenate([p.scores for p in changed]))),
                "Score permutation changed the marginal score multiset",
            )
        evidence = build_run(
            changed,
            targets,
            seed=seed,
            threshold=threshold,
            evaluation=evaluation,
            floor=settings["recompute_after_transform_floor"],
        )
        verify_control(base, evidence, family, level, tolerance)
        values = evidence.evaluate(ones, budgets, tolerance)
        for b, budget in enumerate(budgets):
            row = dict(
                dataset=dataset,
                detector=detector,
                seed=seed,
                family=family,
                level=level,
                replicate=rep,
                budget=budget,
                selected_candidates=selected,
            )
            row.update(zip(METRICS, values[b], strict=True))
            row.update(
                (f"delta_{metric}", values[b, k] - baseline[b, k])
                for k, metric in enumerate(METRICS)
            )
            rows.append(row)
    return rows


def summarize_controls(rows: list) -> list:
    """Average imposed replicates within a checkpoint, then average checkpoints."""
    fields = [*METRICS, *[f"delta_{m}" for m in METRICS]]
    grouped = {}
    for row in rows:
        key = tuple(row[k] for k in ("dataset", "detector", "family", "level", "budget"))
        grouped.setdefault(key, {}).setdefault(row["seed"], []).append([row[k] for k in fields])
    output = []
    for key, runs in grouped.items():
        per_run = np.asarray([np.mean(values, axis=0) for values in runs.values()])
        row = dict(zip(("dataset", "detector", "family", "level", "budget"), key, strict=True))
        row.update(runs=len(runs), interventions=sum(len(v) for v in runs.values()))
        row.update(zip(fields, per_run.mean(axis=0), strict=True))
        output.append(row)
    return output


def prepare(config: dict, gate: dict, smoke: bool) -> tuple:
    protocol = gate["protocol"]
    evaluation = dict(
        protocol["evaluation"], class_ids=list(protocol["ontology"]["canonical_classes"])
    )
    budgets, tolerance = (
        evaluation["froc"]["fp_per_image_budgets"],
        evaluation["froc"]["numeric_tolerance"],
    )
    references = {
        (r["dataset"], r["detector"], int(r["seed"])): r
        for r in read_csv(config["reference_per_run"])
    }
    geometry = {
        (r["detector"], int(r["seed"])): r
        for r in read_csv(config["reference_geometry"])
        if r["arm"] == "baseline"
    }
    rows, interventions, domains, clusters = [], [], [], None
    started, completed = perf_counter(), 0
    total = (
        len(config["analysis"]["datasets"])
        * len(protocol["models"]["detectors"])
        * len(protocol["models"]["seeds"])
    )
    for dataset in config["analysis"]["datasets"]:
        if dataset == "internal":
            internal = gate["internal_statistics"]
            target_path = internal["inputs"]["test_annotations"]
            sources = {
                (r["detector"], r["seed"]): r["comparison_row"]["prediction_bundle"]
                for r in read_json(gate["internal_froc"]["inputs"]["phase5_summary"])["runs"]
            }
        else:
            target_path = protocol["outputs"]["local_annotations"]
            sources = {
                (r["metadata"]["detector"], r["metadata"]["seed"]): r["artifacts"][0]["path"]
                for r in gate["external"]["runs"]
            }
        targets, categories = load_coco_targets(Path(target_path))
        require(
            categories == protocol["ontology"]["canonical_classes"], "Category contract mismatch"
        )
        targets.sort(key=lambda t: t.image_id)
        if dataset == "internal":
            groups = load_patient_group_map(
                Path(internal["inputs"]["test_split_manifest"]),
                image_column=internal["analysis"]["manifest_image_column"],
                patient_group_column=internal["analysis"]["patient_group_column"],
            )
            clusters = build_patient_clusters(tuple(t.image_id for t in targets), groups)
        domain = []
        for detector in protocol["models"]["detectors"]:
            runs = []
            threshold = protocol["threshold_transport"]["primary"]["thresholds"][detector]
            for seed in protocol["models"]["seeds"]:
                predictions = deserialize(read_gzip(Path(sources[detector, seed]))["predictions"])
                predictions, targets = aligned_records(predictions, targets)
                base = build_run(
                    predictions,
                    targets,
                    seed=seed,
                    threshold=threshold,
                    evaluation=evaluation,
                    floor=evaluation["candidate_score_floor"],
                )
                ones = np.ones(len(targets), dtype=np.int64)
                values = base.evaluate(ones, budgets, tolerance)
                reference = references[dataset, detector, seed]
                fp, recall = base.froc.curve(ones)
                actual = [
                    len(targets),
                    sum(base.froc.target_counts),
                    sum(base.froc.target_counts > 0),
                    *base.primary.sum(axis=0),
                    fp[-1],
                    recall[-1],
                    sum(base.at_cap),
                ]
                expected = [
                    float(reference[k])
                    for k in (
                        "images",
                        "target_boxes",
                        "positive_images",
                        "primary_tp",
                        "primary_fp",
                        "floor_fp_per_image",
                        "floor_sensitivity",
                        "images_at_collection_cap",
                    )
                ]
                close(
                    actual,
                    expected,
                    f"Baseline count replay failed: {dataset}/{detector}/{seed}",
                    tolerance,
                )
                close(
                    values[:, 0],
                    [float(reference[f"froc_{b:g}"]) for b in budgets],
                    "Baseline FROC mismatch",
                    tolerance,
                )
                close(
                    values[:, 10],
                    [float(reference[f"floor_limited_{b:g}"].lower() == "true") for b in budgets],
                    "Floor flags mismatch",
                    tolerance,
                )
                if dataset == "external":
                    close(
                        values[0, 5],
                        float(geometry[detector, seed]["geometric_coverage_iou_0.5"]),
                        "Geometry census replay failed",
                        tolerance,
                    )
                for b, budget in enumerate(budgets):
                    rows.append(
                        dict(
                            dataset=dataset,
                            detector=detector,
                            seed=seed,
                            budget=budget,
                            **dict(zip(METRICS, values[b], strict=True)),
                        )
                    )
                if not smoke or completed == 0:
                    interventions.extend(
                        controls(
                            predictions,
                            targets,
                            base,
                            dataset=dataset,
                            detector=detector,
                            seed=seed,
                            config=config,
                            evaluation=evaluation,
                            threshold=threshold,
                            budgets=budgets,
                            tolerance=tolerance,
                        )
                    )
                runs.append(base)
                completed += 1
                print(
                    f"Baseline and control gates {completed}/{total}: {dataset}/{detector}/{seed}",
                    flush=True,
                )
                if not smoke:
                    projected = (perf_counter() - started) * total / completed
                    require(
                        projected <= config["analysis"]["runtime_limit_seconds"],
                        "Projected preparation runtime exceeds configured limit",
                    )
            domain.append(runs)
        domains.append(domain)
    return domains, clusters, rows, interventions


def verify(summary_path: Path) -> dict:
    summary = read_json(summary_path)
    for item in [*summary["inputs"], *summary["artifacts"]]:
        verify_artifact(item)
    return summary


def run(config_path: Path, *, smoke: bool = False, replay: bool = False) -> dict:
    config = read_yaml(config_path)
    root, private = Path(config["outputs"]["public_root"]), Path(config["outputs"]["private_root"])
    if replay:
        verify(root / config["outputs"]["summary"])
    elif not smoke:
        require(
            not root.exists() and not private.exists(),
            "Output namespace exists; use replay, never overwrite",
        )
    with historical_editorial_view(Path.cwd()):
        gate = preflight(Path(config["statistics_config"]))
    mapped = baseline_paths(Path.cwd())
    inputs = []
    for item in gate["inputs"]:
        path = mapped.get(Path(item["path"]).resolve(), Path(item["path"]))
        current = artifact(path)
        require(current["sha256"] == item["sha256"], "Archived prerequisite mismatch")
        inputs.append(current)
    for path in [
        config_path,
        config["protocol_document"],
        config["reference_per_run"],
        config["reference_geometry"],
        config["pilot_config"],
        *config["source_files"],
    ]:
        inputs.append(artifact(path))
    inputs = list({item["path"]: item for item in inputs}.values())
    protocol = gate["protocol"]
    ensure_private(private / config["outputs"]["draws"], Path(protocol["outputs"]["private_root"]))
    started = perf_counter()
    domains, clusters, rows, interventions = prepare(config, gate, smoke)
    settings = dict(config["analysis"])
    if smoke:
        settings["bootstrap_resamples"] = settings["smoke_resamples"]
    remaining = settings["runtime_limit_seconds"] - (perf_counter() - started)
    require(remaining > 0, "Preparation exceeded configured runtime")
    settings["runtime_limit_seconds"] = remaining
    budgets = protocol["evaluation"]["froc"]["fp_per_image_budgets"]
    point, draws = bootstrap(
        domains,
        clusters,
        budgets,
        settings,
        protocol["evaluation"]["froc"]["numeric_tolerance"],
        config["analysis_id"],
    )
    intervals, contrasts = summarize(
        point,
        draws,
        settings["datasets"],
        protocol["models"]["detectors"],
        budgets,
        settings["confidence_level"],
    )
    tables = dict(
        per_run=rows,
        intervals=intervals,
        contrasts=contrasts,
        perturbations=interventions,
        perturbation_summary=summarize_controls(interventions),
    )
    for item in inputs:
        verify_artifact(item)
    elapsed = perf_counter() - started
    require(
        elapsed <= config["analysis"]["runtime_limit_seconds"],
        "Analysis exceeded configured runtime",
    )
    if smoke:
        return dict(
            status="smoke_passed_no_outputs_written",
            seconds=elapsed,
            runs=sum(len(r) for d in domains for r in d),
            control_rows=len(interventions),
        )
    if replay:
        for key, table in tables.items():
            buffer = io.StringIO(newline="")
            writer = csv.DictWriter(buffer, fieldnames=list(table[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(json_number(table))
            require(
                buffer.getvalue() == (root / config["outputs"][key]).read_text(encoding="utf-8"),
                f"Replay differs: {key}",
            )
        with np.load(private / config["outputs"]["draws"]) as saved:
            require(
                np.array_equal(point, saved["point"], equal_nan=True)
                and np.array_equal(draws, saved["draws"], equal_nan=True),
                "Joint draw replay differs",
            )
        return dict(
            status="exact_replay_passed", seconds=elapsed, tables=len(tables), draws=len(draws)
        )
    root.mkdir(parents=True)
    private.mkdir(parents=True)
    for key, table in tables.items():
        write_csv(root / config["outputs"][key], table)
    np.savez_compressed(private / config["outputs"]["draws"], point=point, draws=draws)
    outputs = [artifact(root / config["outputs"][key]) for key in tables]
    outputs.append(artifact(private / config["outputs"]["draws"]))
    summary = dict(
        schema_version=1,
        analysis_id=config["analysis_id"],
        status="completed_exploratory",
        inputs=inputs,
        artifacts=outputs,
        config=config_path.as_posix(),
        datasets=settings["datasets"],
        detectors=protocol["models"]["detectors"],
        seeds=protocol["models"]["seeds"],
        budgets=budgets,
        metrics=list(METRICS),
        bootstrap_resamples=len(draws),
        confidence_level=settings["confidence_level"],
        internal_patient_groups=len(clusters.patient_group_ids),
        images=[len(d[0][0].froc.image_ids) for d in domains],
        target_boxes=[int(d[0][0].froc.target_counts.sum()) for d in domains],
        invariant_checks_passed=True,
        historical_lower_floor_replay_passed=True,
        control_interventions=len(interventions) // len(budgets),
        elapsed_seconds=elapsed,
        environment=dict(
            python=platform.python_version(), numpy=np.__version__, platform=platform.platform()
        ),
        limitations=[
            "Post-hoc exploratory analysis; marginal, not simultaneous intervals",
            "Fixed retained candidates and reference ontology; not causal shares of domain loss",
            "External patient linkage unknown; independent external images assumed",
            "Five checkpoint runs; conditional on training sample and recipes",
            "Annotation-informed controls are not deployable repairs; no new inference or tuning",
        ],
    )
    write_json(root / config["outputs"]["summary"], summary)
    return dict(
        status=summary["status"],
        seconds=elapsed,
        control_interventions=summary["control_interventions"],
        summary=artifact(root / config["outputs"]["summary"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--smoke", action="store_true")
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        config = read_yaml(args.config)
        summary = verify(Path(config["outputs"]["public_root"]) / config["outputs"]["summary"])
        print(f"Verified {len(summary['inputs'])} inputs and {len(summary['artifacts'])} outputs")
    else:
        print(run(args.config, smoke=args.smoke, replay=args.replay))


if __name__ == "__main__":
    main()
