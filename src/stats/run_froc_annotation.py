"""CPU-only shared-annotation sensitivity analysis of frozen saved detections."""

from __future__ import annotations

import argparse
import csv
import io
import platform
from pathlib import Path
from time import perf_counter

import numpy as np

from scripts.verify_frozen_external import historical_editorial_view
from src.data.prepare_vindr import ensure_private
from src.evaluate_vindr_external import deserialize, read_gzip
from src.stats.constrained_repairability import count_constraint
from src.stats.froc_annotation import (
    count_curve,
    deletion_endpoints,
    deletion_losses,
    deletion_sets,
    paired_bounds,
)
from src.stats.paired import (
    build_patient_clusters,
    draw_independent_run_bootstrap_multiplicities,
    json_number,
    stable_rng_seed,
)
from src.stats.run_statistics import load_coco_targets, load_patient_group_map
from src.stats.run_threshold_repairability import interval, read_csv, verify
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
from src.stats.transportability import aligned_records, build_froc_cache, draw_observations


def evaluate(
    domains: list,
    observations: list[np.ndarray],
    run_weights: tuple,
    budgets: list[float],
    edit_counts: list[int],
) -> np.ndarray:
    """Recompute bounds after the common observation draw and independent run draws."""
    output = []
    for domain, obs in zip(domains, observations, strict=True):
        curves = [[count_curve(cache, obs) for cache in family] for family in domain]
        counts = np.array([count_constraint(b, int(obs.sum()), ceiling=False) for b in budgets])
        output.append(paired_bounds(curves, run_weights, counts, edit_counts))
    return np.asarray(output)


def bootstrap(
    domains: list, clusters: object, budgets: list[float], settings: dict, label: str
) -> tuple[np.ndarray, np.ndarray]:
    """Use patient/image units and couple checkpoint multiplicities across domains."""
    sizes = [len(domain[0][0].image_ids) for domain in domains]
    for d, domain in enumerate(domains):
        reference = domain[0][0]
        for family in domain:
            for cache in family:
                require(cache.image_ids == reference.image_ids, "Image order differs")
                require(
                    np.array_equal(cache.target_counts, reference.target_counts),
                    "References differ",
                )
        if d == 0:
            require(clusters.image_ids == reference.image_ids, "Patient order differs")
    weights = tuple(np.ones(len(family), dtype=int) for family in domains[0])
    point = evaluate(
        domains,
        [np.ones(n, dtype=int) for n in sizes],
        weights,
        budgets,
        settings["bootstrap_edits"],
    )
    draws = np.empty((settings["bootstrap_resamples"], *point.shape))
    rng = np.random.default_rng(stable_rng_seed(settings["bootstrap_seed"], label))
    started = perf_counter()
    for i in range(len(draws)):
        observations = [
            draw_observations(rng, sizes[0], clusters),
            draw_observations(rng, sizes[1], None),
        ]
        weights = draw_independent_run_bootstrap_multiplicities(
            rng, detector_a_run_count=len(weights[0]), detector_b_run_count=len(weights[1])
        )
        draws[i] = evaluate(domains, observations, weights, budgets, settings["bootstrap_edits"])
        if settings["progress_every"] and (i + 1) % settings["progress_every"] == 0:
            print(f"Annotation joint bootstrap {i + 1}/{len(draws)}", flush=True)
            require(
                (perf_counter() - started) * len(draws) / (i + 1)
                < settings["runtime_limit_seconds"],
                "Projected bootstrap exceeds runtime limit",
            )
    return point, draws


def prepare(config: dict, gate: dict) -> tuple:
    """Read complete cohorts; enumerate common deletions without publishing identifiers."""
    protocol = gate["protocol"]
    evaluation = protocol["evaluation"]
    budgets = evaluation["froc"]["fp_per_image_budgets"]
    tolerance = evaluation["froc"]["numeric_tolerance"]
    reference = {
        (r["dataset"], r["detector"], int(r["seed"]), float(r["budget"])): r
        for r in read_csv(config["v2_per_run"])
    }
    domains, tables, private_arrays = [], dict(per_run=[], envelopes=[], exact_deletions=[]), {}
    clusters = None
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
        targets.sort(key=lambda t: t.image_id)
        require(categories == protocol["ontology"]["canonical_classes"], "Ontology differs")
        n, images = sum(len(t.labels) for t in targets), len(targets)
        counts = np.array([count_constraint(b, images, ceiling=False) for b in budgets])
        if dataset == "internal":
            groups = load_patient_group_map(
                Path(internal["inputs"]["test_split_manifest"]),
                image_column=internal["analysis"]["manifest_image_column"],
                patient_group_column=internal["analysis"]["patient_group_column"],
            )
            clusters = build_patient_clusters(tuple(t.image_id for t in targets), groups)
        subsets = {d: deletion_sets(n, d) for d in config["analysis"]["exact_deletion_counts"]}
        exact = {d: [] for d in subsets}
        domain = []
        for detector in protocol["models"]["detectors"]:
            family, family_exact = [], {d: [] for d in subsets}
            for seed in protocol["models"]["seeds"]:
                predictions = deserialize(read_gzip(Path(sources[detector, seed]))["predictions"])
                predictions, targets = aligned_records(predictions, targets)
                cache = build_froc_cache(
                    predictions,
                    targets,
                    class_ids=tuple(categories),
                    floor=evaluation["candidate_score_floor"],
                    iou=evaluation["matching_iou_threshold"],
                    cap=evaluation["max_detections_per_image"],
                )
                curve = count_curve(cache, np.ones(images, dtype=int))
                tp, fp = curve.endpoint(counts)
                for b, budget in enumerate(budgets):
                    close(
                        tp[b] / n,
                        float(reference[dataset, detector, seed, budget]["threshold_ceiling"]),
                        "FROC baseline replay differs",
                        tolerance,
                    )
                    tables["per_run"].append(
                        dict(
                            dataset=dataset,
                            detector=detector,
                            seed=seed,
                            images=images,
                            references=n,
                            budget=budget,
                            fp_budget=int(counts[b]),
                            tp=int(tp[b]),
                            fp=int(fp[b]),
                            recall=tp[b] / n,
                        )
                    )
                for d, cases in subsets.items():
                    losses = deletion_losses(
                        predictions,
                        targets,
                        cache,
                        floor=evaluation["candidate_score_floor"],
                        iou=evaluation["matching_iou_threshold"],
                        cap=evaluation["max_detections_per_image"],
                        subsets=cases,
                    )
                    family_exact[d].append(deletion_endpoints(curve, losses, counts) / (n - d))
                family.append(cache)
                print(f"Annotation gates: {dataset}/{detector}/{seed}", flush=True)
            domain.append(family)
            for d in subsets:
                exact[d].append(family_exact[d])
        domains.append(domain)
        curves = [[count_curve(c, np.ones(images, dtype=int)) for c in family] for family in domain]
        weights = tuple(np.ones(len(f), dtype=int) for f in domain)
        edits = list(range(config["analysis"]["maximum_edits"] + 1))
        detectors = protocol["models"]["detectors"]
        entities = [*detectors, f"{detectors[0]}-{detectors[1]}"]
        for mode in config["analysis"]["modes"]:
            values = paired_bounds(curves, weights, counts, edits, mode)
            require(
                np.all(values[..., 0] <= values[..., 1] + tolerance)
                and np.all(np.diff(values[..., 0], axis=2) <= tolerance)
                and np.all(np.diff(values[..., 1], axis=2) >= -tolerance),
                "Envelope ordering/nesting failed",
            )
            for m, entity in enumerate(entities):
                for b, budget in enumerate(budgets):
                    for j, k in enumerate(edits):
                        tables["envelopes"].append(
                            dict(
                                dataset=dataset,
                                entity=entity,
                                mode=mode,
                                budget=budget,
                                edits=k,
                                edits_per_reference=k / n,
                                lower=values[m, b, j, 0],
                                upper=values[m, b, j, 1],
                                original_references=n,
                                images=images,
                            )
                        )
        for d, arrays in exact.items():
            values = np.asarray(arrays)  # detector, run, shared deletion subset, FP budget
            private_arrays[f"{dataset}_delete_{d}"] = values
            means = values.mean(axis=1)
            for m, entity in enumerate(entities):
                if m < 2:
                    shared = means[m]
                    independent_lower = values[m].min(axis=1).mean(axis=0)
                    independent_upper = values[m].max(axis=1).mean(axis=0)
                else:
                    shared = means[0] - means[1]
                    independent_lower = values[0].min(axis=1).mean(axis=0) - values[1].max(
                        axis=1
                    ).mean(axis=0)
                    independent_upper = values[0].max(axis=1).mean(axis=0) - values[1].min(
                        axis=1
                    ).mean(axis=0)
                for b, budget in enumerate(budgets):
                    tables["exact_deletions"].append(
                        dict(
                            dataset=dataset,
                            entity=entity,
                            deletions=d,
                            cases=len(subsets[d]),
                            budget=budget,
                            lower=shared[:, b].min(),
                            upper=shared[:, b].max(),
                            independent_lower=independent_lower[b],
                            independent_upper=independent_upper[b],
                            original_references=n,
                            remaining_references=n - d,
                            sampling_uncertainty="not_estimated_for_exact_subset_census",
                        )
                    )
    return domains, clusters, tables, private_arrays


def summarize(
    point: np.ndarray, draws: np.ndarray, config: dict, budgets: list, detectors: list
) -> tuple[list, list]:
    """Keep epistemic envelope endpoints separate from their sampling intervals."""
    rows, contrasts = [], []
    settings = config["analysis"]
    entities = [*detectors, f"{detectors[0]}-{detectors[1]}"]
    for d, dataset in enumerate(settings["datasets"]):
        for m, entity in enumerate(entities):
            for b, budget in enumerate(budgets):
                for j, edits in enumerate(settings["bootstrap_edits"]):
                    for side, endpoint in enumerate(("lower", "upper")):
                        rows.append(
                            dict(
                                dataset=dataset,
                                entity=entity,
                                budget=budget,
                                edits=edits,
                                endpoint=endpoint,
                                **interval(
                                    point[d, m, b, j, side],
                                    draws[:, d, m, b, j, side],
                                    settings["confidence_level"],
                                ),
                            )
                        )
    zero = settings["bootstrap_edits"].index(0)
    for m, detector in enumerate(detectors):
        for b, budget in enumerate(budgets):
            for j, edits in enumerate(settings["bootstrap_edits"]):
                for side, endpoint in enumerate(("lower", "upper")):
                    estimate = point[0, m, b, zero, 0] - point[1, m, b, j, 1 - side]
                    samples = draws[:, 0, m, b, zero, 0] - draws[:, 1, m, b, j, 1 - side]
                    contrasts.append(
                        dict(
                            contrast="internal_minus_external_external_edits_only",
                            detector=detector,
                            budget=budget,
                            external_edits=edits,
                            endpoint=endpoint,
                            **interval(estimate, samples, settings["confidence_level"]),
                        )
                    )
    return rows, contrasts


def run(config_path: Path, *, smoke: bool = False, replay: bool = False) -> dict:
    """Freeze independent artifacts; permit only exact, read-only subsequent replays."""
    config = read_yaml(config_path)
    root, private = (Path(config["outputs"][key]) for key in ("public_root", "private_root"))
    if replay:
        verify(root / "summary.json")
    elif not smoke:
        require(not root.exists() and not private.exists(), "Output namespace exists; use replay")
    baseline = verify(Path(config["v2_summary"]))
    with historical_editorial_view(Path.cwd()):
        gate = preflight(Path(config["statistics_config"]))
    inputs = list(baseline["inputs"])
    for path in [
        config_path,
        config["v2_summary"],
        config["v2_per_run"],
        config["protocol_document"],
        *config["source_files"],
    ]:
        inputs.append(artifact(path))
    inputs = list({item["path"]: item for item in inputs}.values())
    for item in inputs:
        verify_artifact(item)
    ensure_private(private / "joint_draws.npz", Path(gate["protocol"]["outputs"]["private_root"]))
    started = perf_counter()
    domains, clusters, tables, private_arrays = prepare(config, gate)
    settings = dict(config["analysis"])
    if smoke:
        settings["bootstrap_resamples"] = settings["smoke_resamples"]
    settings["runtime_limit_seconds"] -= perf_counter() - started
    require(settings["runtime_limit_seconds"] > 0, "Preparation exceeded runtime limit")
    protocol = gate["protocol"]
    budgets = protocol["evaluation"]["froc"]["fp_per_image_budgets"]
    tolerance = protocol["evaluation"]["froc"]["numeric_tolerance"]
    point, draws = bootstrap(domains, clusters, budgets, settings, config["analysis_id"])
    tables["intervals"], tables["contrasts"] = summarize(
        point, draws, config, budgets, protocol["models"]["detectors"]
    )
    private_arrays.update(point=point, draws=draws)
    # Exact shared-subset ranges must fit the universal deletion-only relaxation.
    envelope = {
        (r["dataset"], r["entity"], r["budget"], r["edits"]): r
        for r in tables["envelopes"]
        if r["mode"] == "deletions"
    }
    for row in tables["exact_deletions"]:
        bound = envelope[row["dataset"], row["entity"], row["budget"], row["deletions"]]
        require(
            bound["lower"] <= row["lower"] + tolerance
            and row["upper"] <= bound["upper"] + tolerance,
            "Exact deletion census violates envelope",
        )
        require(
            row["independent_lower"] <= row["lower"] + tolerance
            and row["upper"] <= row["independent_upper"] + tolerance,
            "Shared extrema exceed independent relaxation",
        )
    for item in inputs:
        verify_artifact(item)
    elapsed = perf_counter() - started
    require(elapsed <= config["analysis"]["runtime_limit_seconds"], "Analysis runtime limit")
    if smoke:
        return dict(
            status="smoke_passed_no_outputs_written",
            seconds=elapsed,
            rows={key: len(rows) for key, rows in tables.items()},
        )
    if replay:
        for name, rows in tables.items():
            buffer = io.StringIO(newline="")
            writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(json_number(rows))
            require(
                buffer.getvalue() == (root / f"{name}.csv").read_text(encoding="utf-8"),
                f"Table replay differs: {name}",
            )
        with np.load(private / "joint_draws.npz") as saved:
            require(set(saved.files) == set(private_arrays), "Array keys differ")
            for key, values in private_arrays.items():
                require(
                    np.array_equal(values, saved[key], equal_nan=True),
                    f"Array replay differs: {key}",
                )
        return dict(
            status="exact_replay_passed", seconds=elapsed, tables=len(tables), draws=len(draws)
        )
    root.mkdir(parents=True)
    private.mkdir(parents=True)
    for name, rows in tables.items():
        write_csv(root / f"{name}.csv", rows)
    np.savez_compressed(private / "joint_draws.npz", **private_arrays)
    artifacts = [artifact(root / f"{name}.csv") for name in tables] + [
        artifact(private / "joint_draws.npz")
    ]
    write_json(
        root / "summary.json",
        dict(
            schema_version=1,
            analysis_id=config["analysis_id"],
            status="completed_exploratory",
            inputs=inputs,
            artifacts=artifacts,
            elapsed_seconds=elapsed,
            datasets=settings["datasets"],
            detectors=protocol["models"]["detectors"],
            seeds=protocol["models"]["seeds"],
            budgets=budgets,
            rows={k: len(v) for k, v in tables.items()},
            bootstrap_resamples=len(draws),
            bootstrap_edits=settings["bootstrap_edits"],
            confidence_level=settings["confidence_level"],
            internal_patient_groups=len(clusters.patient_group_ids),
            baseline_replay_passed=True,
            exact_deletion_envelope_gates_passed=True,
            environment=dict(python=platform.python_version(), numpy=np.__version__),
            limitations=[
                "Exploratory conditional sensitivity, not a clinical annotation-error estimate",
                "Universal mixed-edit bounds are conservative, not attainable extrema",
                "Exact shared-subset extrema only for one/two deletions of existing references",
                "Exact deletion census has no observation-sampling CI; "
                "universal endpoints have marginal joint-bootstrap intervals",
                "Bootstrap edit units are resampled copies; external patient linkage unknown",
                "Fixed predictions, score ties, image universe, IoU and serial matching; "
                "no crowd/ignore rules",
                "Does not identify clinical causes or validate ontology equivalence",
            ],
        ),
    )
    return dict(
        status="completed_exploratory", seconds=elapsed, summary=artifact(root / "summary.json")
    )


def main() -> None:
    """Run or verify an independently versioned exploratory research artifact."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--smoke", action="store_true")
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        config = read_yaml(args.config)
        result = verify(Path(config["outputs"]["public_root"]) / "summary.json")
        print(f"Verified {len(result['inputs'])} inputs and {len(result['artifacts'])} outputs")
    else:
        print(run(args.config, smoke=args.smoke, replay=args.replay))


if __name__ == "__main__":
    main()
