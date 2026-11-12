"""Source-gated CPU analysis of constrained repairability on saved study outputs."""

from __future__ import annotations

import argparse
import csv
import io
import platform
from pathlib import Path
from time import perf_counter

import networkx as nx
import numpy as np
import scipy

from scripts.verify_frozen_external import historical_editorial_view
from src.data.prepare_vindr import ensure_private
from src.evaluate_vindr_external import deserialize, read_gzip
from src.meddet_benchmark.evaluation import ImagePrediction
from src.stats.constrained_diagnostics import (
    METRICS,
    CountRun,
    extended_interval,
    oc_cost,
    problem_from_outputs,
)
from src.stats.constrained_repairability import count_constraint, solve, uniform_cost
from src.stats.paired import (
    build_patient_clusters,
    draw_independent_run_bootstrap_multiplicities,
    json_number,
    stable_rng_seed,
)
from src.stats.run_statistics import load_coco_targets, load_patient_group_map
from src.stats.run_threshold_repairability import read_csv, verify
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
from src.stats.threshold_repairability import METRICS as V2_METRICS
from src.stats.threshold_repairability import build_run, compatible_masks, transform, verify_control
from src.stats.transportability import aligned_records, draw_observations


def grid_rows(
    problem,
    counts: np.ndarray,
    base,
    settings: dict,
    budgets: list,
    identity: dict,
    tolerance: float,
) -> list[dict]:
    """Compare exact flow with the closed form at every original budget/target."""
    h, r, full, n, candidates = map(int, counts.sum(axis=0))
    images = len(counts)
    values = base.evaluate(np.ones(images, dtype=int), budgets, tolerance)
    rows = []
    for b, budget in enumerate(budgets):
        bound = count_constraint(budget, images, ceiling=False)
        for target in settings["target_recalls"]:
            k = count_constraint(target, n, ceiling=True)
            exact = solve(problem, k, bound)
            expected = uniform_cost(
                h, r, full, k, bound, settings["promotion_cost"], settings["suppression_cost"]
            )
            require(
                (None if exact is None else exact.cost) == expected,
                "Exact flow disagrees with uniform-cost theorem",
            )
            rows.append(
                dict(
                    **identity,
                    budget=budget,
                    target_recall=target,
                    target_count=k,
                    fp_budget_count=bound,
                    images=images,
                    references=n,
                    retained_candidates=candidates,
                    historical_selected=h,
                    historical_rank=r,
                    full_rank=full,
                    historical_greedy_tp=int(base.primary[:, 0].sum()),
                    froc_recall=values[b, 0],
                    geometry_recall=full / n,
                    feasible=exact is not None,
                    cost="infinite" if exact is None else exact.cost,
                    cost_per_reference="infinite" if exact is None else exact.cost / n,
                    cost_per_image="infinite" if exact is None else exact.cost / images,
                    promotions=None if exact is None else exact.promotions,
                    suppressions=None if exact is None else exact.suppressions,
                    geometry_deficit=max(0, k - full),
                    formula_verified=True,
                )
            )
    return rows


def controls(
    predictions,
    targets,
    base,
    baseline: np.ndarray,
    settings: dict,
    config: dict,
    evaluation: dict,
    threshold: float,
    budgets: list,
    identity: dict,
) -> list:
    """Impose output changes only; preserve original annotations and saved bundles."""
    jobs = [("power", power, 0) for power in config["powers"]] + [
        (family, level, rep)
        for family in config["families"]
        for level in config["fractions"]
        for rep in range(config["replicates"])
    ]
    mask = compatible_masks(predictions, targets, evaluation["matching_iou_threshold"])
    output = []
    ones = np.ones(len(targets), dtype=int)
    tolerance = evaluation["froc"]["numeric_tolerance"]
    before_values = CountRun(identity["seed"], baseline).evaluate(
        ones,
        budgets,
        settings["target_recalls"],
        settings["promotion_cost"],
        settings["suppression_cost"],
    )
    b = budgets.index(settings["primary_budget"])
    t = settings["target_recalls"].index(settings["primary_target"])
    for family, level, rep in jobs:
        rng = np.random.default_rng(
            stable_rng_seed(
                config["seed"],
                f"{identity['dataset']}:{identity['detector']}:{identity['seed']}:{family}:{rep}",
            )
        )
        changed, selected = transform(predictions, mask, family=family, level=level, rng=rng)
        cutoff = threshold**level if family == "power" else threshold
        _, counts = problem_from_outputs(
            changed,
            targets,
            threshold=cutoff,
            iou=evaluation["matching_iou_threshold"],
            promotion=settings["promotion_cost"],
            suppression=settings["suppression_cost"],
        )
        evidence = build_run(
            changed,
            targets,
            seed=identity["seed"],
            threshold=cutoff,
            evaluation=evaluation,
            floor=0,
        )
        verify_control(base, evidence, family, level, tolerance)
        values = CountRun(identity["seed"], counts).evaluate(
            ones,
            budgets,
            settings["target_recalls"],
            settings["promotion_cost"],
            settings["suppression_cost"],
        )
        if family == "power":
            require(np.array_equal(counts, baseline), "Power changed historical membership")
            require(np.array_equal(values, before_values, equal_nan=True), "Power changed cost")
        if family == "remove_incompatible":
            require(np.array_equal(counts[:, 1:3], baseline[:, 1:3]), "Incompatible rank changed")
            require(
                np.all(values[..., 1] <= before_values[..., 1]), "Incompatible removal cost rose"
            )
        h, r, full, n, _ = map(int, counts.sum(axis=0))
        output.append(
            dict(
                **identity,
                family=family,
                level=level,
                replicate=rep,
                selected_candidates=selected,
                historical_selected=h,
                historical_rank=r,
                full_rank=full,
                geometry_recall=full / n,
                budget=budgets[b],
                target_recall=settings["target_recalls"][t],
                cost="infinite" if np.isinf(values[b, t, 1]) else values[b, t, 1],
                froc_recall=evidence.evaluate(ones, budgets, tolerance)[b, 0],
                invariants_passed=True,
            )
        )
    return output


def prepare(config: dict, gate: dict, smoke: bool) -> tuple:
    """Read all five seeds on both cohorts and compare original FROC/v2 quantities."""
    protocol, settings = gate["protocol"], config["analysis"]
    evaluation = dict(
        protocol["evaluation"], class_ids=list(protocol["ontology"]["canonical_classes"])
    )
    budgets = evaluation["froc"]["fp_per_image_budgets"]
    tolerance = evaluation["froc"]["numeric_tolerance"]
    reference = {
        (r["dataset"], r["detector"], int(r["seed"]), float(r["budget"])): r
        for r in read_csv(config["v2_per_run"])
    }
    tables = dict(per_run=[], perturbations=[], correction_comparison=[])
    domains, clusters = [], None
    for dataset in settings["datasets"]:
        if dataset == "internal":
            internal = gate["internal_statistics"]
            targets_path = internal["inputs"]["test_annotations"]
            sources = {
                (r["detector"], r["seed"]): r["comparison_row"]["prediction_bundle"]
                for r in read_json(gate["internal_froc"]["inputs"]["phase5_summary"])["runs"]
            }
        else:
            targets_path = protocol["outputs"]["local_annotations"]
            sources = {
                (r["metadata"]["detector"], r["metadata"]["seed"]): r["artifacts"][0]["path"]
                for r in gate["external"]["runs"]
            }
        targets, categories = load_coco_targets(Path(targets_path))
        targets.sort(key=lambda r: r.image_id)
        require(categories == protocol["ontology"]["canonical_classes"], "Ontology changed")
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
                identity = dict(dataset=dataset, detector=detector, seed=seed)
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
                ones = np.ones(len(targets), dtype=int)
                values = base.evaluate(ones, budgets, tolerance)
                for b, budget in enumerate(budgets):
                    expected = reference[dataset, detector, seed, budget]
                    close(
                        values[b],
                        [float(expected[k]) for k in V2_METRICS],
                        "V2 baseline replay changed",
                        tolerance,
                    )
                problem, counts = problem_from_outputs(
                    predictions,
                    targets,
                    threshold=threshold,
                    iou=evaluation["matching_iou_threshold"],
                    promotion=settings["promotion_cost"],
                    suppression=settings["suppression_cost"],
                )
                require(np.array_equal(counts[:, 2], base.geometry), "Independent ranks disagree")
                tables["per_run"].extend(
                    grid_rows(problem, counts, base, settings, budgets, identity, tolerance)
                )
                for policy, cutoff in (("historical", threshold), ("all_retained", 0)):
                    costs = []
                    for p, target in zip(predictions, targets, strict=True):
                        keep = p.scores >= cutoff
                        selected = ImagePrediction(
                            p.image_id,
                            p.image_size,
                            p.boxes_xyxy[keep],
                            p.labels[keep],
                            p.scores[keep],
                        )
                        costs.append(oc_cost(selected, target, **config["oc_cost"]))
                    tables["correction_comparison"].append(
                        dict(
                            **identity,
                            policy=policy,
                            oc_cost_mean=float(np.mean(costs)),
                            images=len(costs),
                            localization_weight=config["oc_cost"]["localization_weight"],
                            dummy_cost=config["oc_cost"]["dummy_cost"],
                        )
                    )
                if not smoke or not tables["perturbations"]:
                    tables["perturbations"].extend(
                        controls(
                            predictions,
                            targets,
                            base,
                            counts,
                            settings,
                            config["perturbations"],
                            evaluation,
                            threshold,
                            budgets,
                            identity,
                        )
                    )
                runs.append(CountRun(seed, counts))
                print(f"Flow/formula/v2 gates: {dataset}/{detector}/{seed}", flush=True)
            domain.append(runs)
        domains.append(domain)
    return domains, clusters, tables


def evaluate(
    domains: list, observations: list, run_weights: tuple, settings: dict, budgets: list
) -> np.ndarray:
    """Average only selected runs, so zero multiplicity never multiplies infinity."""
    output = np.empty(
        (
            len(domains),
            len(run_weights),
            len(budgets),
            len(settings["target_recalls"]),
            len(METRICS),
        )
    )
    for d, domain in enumerate(domains):
        for m, runs in enumerate(domain):
            selected = np.flatnonzero(run_weights[m])
            values = [
                runs[i].evaluate(
                    observations[d],
                    budgets,
                    settings["target_recalls"],
                    settings["promotion_cost"],
                    settings["suppression_cost"],
                )
                for i in selected
            ]
            output[d, m] = np.average(values, axis=0, weights=run_weights[m][selected])
    return output


def bootstrap(domains: list, clusters, settings: dict, budgets: list, label: str) -> tuple:
    """Joint observation/run draws, including extended costs and infeasible runs."""
    sizes = [len(d[0][0].counts) for d in domains]
    run_ones = tuple(np.ones(len(r), dtype=int) for r in domains[0])
    point = evaluate(domains, [np.ones(n, dtype=int) for n in sizes], run_ones, settings, budgets)
    draws = np.empty((settings["bootstrap_resamples"], *point.shape))
    rng = np.random.default_rng(stable_rng_seed(settings["bootstrap_seed"], label))
    started = perf_counter()
    for i in range(len(draws)):
        observations = [
            draw_observations(rng, sizes[0], clusters),
            draw_observations(rng, sizes[1], None),
        ]
        weights = draw_independent_run_bootstrap_multiplicities(
            rng, detector_a_run_count=len(run_ones[0]), detector_b_run_count=len(run_ones[1])
        )
        draws[i] = evaluate(domains, observations, weights, settings, budgets)
        if settings["progress_every"] and (i + 1) % settings["progress_every"] == 0:
            print(f"Joint constrained bootstrap {i + 1}/{len(draws)}", flush=True)
            require(
                (perf_counter() - started) * len(draws) / (i + 1)
                <= settings["runtime_limit_seconds"],
                "Bootstrap runtime limit",
            )
    return point, draws


def summaries(
    point: np.ndarray,
    draws: np.ndarray,
    domains: list,
    settings: dict,
    detectors: list,
    budgets: list,
) -> tuple[list, list]:
    """Report extended intervals and separate deterministic annotation-edit bounds."""
    intervals, edits = [], []
    for d, dataset in enumerate(settings["datasets"]):
        mean_ranks = [
            float(np.mean([r.counts[:, 2].sum() for r in family])) for family in domains[d]
        ]
        difference = mean_ranks[0] - mean_ranks[1]
        n = int(domains[d][0][0].counts[:, 3].sum())
        for k in range(settings["annotation_max_edits"] + 1):
            edits.append(
                dict(
                    dataset=dataset,
                    edits=k,
                    edits_per_original_reference=k / n,
                    mean_rank_a=mean_ranks[0],
                    mean_rank_b=mean_ranks[1],
                    difference=difference,
                    lower=difference - k,
                    upper=difference + k,
                    strict_a_above_b=difference > k,
                    strict_b_above_a=difference < -k,
                    interpretation="conditional_bound_not_attainability_or_label_error_estimate",
                )
            )
        for m, detector in enumerate(detectors):
            for b, budget in enumerate(budgets):
                for t, target in enumerate(settings["target_recalls"]):
                    for j, metric in enumerate(METRICS):
                        intervals.append(
                            dict(
                                dataset=dataset,
                                detector=detector,
                                budget=budget,
                                target_recall=target,
                                metric=metric,
                                **extended_interval(
                                    point[d, m, b, t, j],
                                    draws[:, d, m, b, t, j],
                                    settings["confidence_level"],
                                ),
                            )
                        )
    return intervals, edits


def run(config_path: Path, *, smoke: bool = False, replay: bool = False) -> dict:
    """Bind sources and evidence; refuse overwrite and require exact numerical replay."""
    config = read_yaml(config_path)
    root, private = (Path(config["outputs"][k]) for k in ("public_root", "private_root"))
    if replay:
        verify(root / "summary.json")
    elif not smoke:
        require(not root.exists() and not private.exists(), "Output exists; use replay")
    v2 = verify(Path(config["v2_summary"]))
    with historical_editorial_view(Path.cwd()):
        gate = preflight(Path(config["statistics_config"]))
    inputs = list(v2["inputs"])
    for path in [
        config_path,
        config["v2_summary"],
        config["v2_per_run"],
        config["protocol_document"],
        *config["source_files"],
    ]:
        inputs.append(artifact(path))
    inputs = list({r["path"]: r for r in inputs}.values())
    for item in inputs:
        verify_artifact(item)
    ensure_private(private / "joint_draws.npz", Path(gate["protocol"]["outputs"]["private_root"]))
    started = perf_counter()
    domains, clusters, tables = prepare(config, gate, smoke)
    settings = dict(config["analysis"])
    if smoke:
        settings["bootstrap_resamples"] = settings["smoke_resamples"]
    protocol = gate["protocol"]
    budgets = protocol["evaluation"]["froc"]["fp_per_image_budgets"]
    point, draws = bootstrap(domains, clusters, settings, budgets, config["analysis_id"])
    tables["intervals"], tables["annotation_sensitivity"] = summaries(
        point, draws, domains, settings, protocol["models"]["detectors"], budgets
    )
    for item in inputs:
        verify_artifact(item)
    elapsed = perf_counter() - started
    require(elapsed <= settings["runtime_limit_seconds"], "Analysis runtime limit")
    if smoke:
        return dict(
            status="smoke_passed_no_outputs_written",
            seconds=elapsed,
            rows={k: len(v) for k, v in tables.items()},
        )
    if replay:
        for name, rows in tables.items():
            buffer = io.StringIO(newline="")
            writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(json_number(rows))
            require(
                buffer.getvalue() == (root / f"{name}.csv").read_text(encoding="utf-8"),
                f"Replay mismatch: {name}",
            )
        with np.load(private / "joint_draws.npz") as saved:
            require(
                np.array_equal(point, saved["point"], equal_nan=True)
                and np.array_equal(draws, saved["draws"], equal_nan=True),
                "Draw replay mismatch",
            )
        return dict(
            status="exact_replay_passed", seconds=elapsed, tables=len(tables), draws=len(draws)
        )
    root.mkdir(parents=True)
    private.mkdir(parents=True)
    for name, rows in tables.items():
        write_csv(root / f"{name}.csv", rows)
    np.savez_compressed(private / "joint_draws.npz", point=point, draws=draws)
    outputs = [artifact(root / f"{name}.csv") for name in tables]
    outputs.append(artifact(private / "joint_draws.npz"))
    write_json(
        root / "summary.json",
        dict(
            schema_version=1,
            analysis_id=config["analysis_id"],
            status="completed_exploratory",
            config=config_path.as_posix(),
            inputs=inputs,
            artifacts=outputs,
            elapsed_seconds=elapsed,
            rows={k: len(v) for k, v in tables.items()},
            datasets=settings["datasets"],
            detectors=protocol["models"]["detectors"],
            seeds=protocol["models"]["seeds"],
            budgets=budgets,
            target_recalls=settings["target_recalls"],
            bootstrap_resamples=len(draws),
            confidence_level=settings["confidence_level"],
            metrics=METRICS,
            formula_verified_all_cells=True,
            v2_replay_passed=True,
            controls_passed=True,
            internal_patient_groups=len(clusters.patient_group_ids),
            environment=dict(
                python=platform.python_version(),
                numpy=np.__version__,
                scipy=scipy.__version__,
                networkx=nx.__version__,
            ),
            limitations=[
                "Retrospective oracle; fixed candidates and reference ontology",
                "Uniform costs are determined by H,r,M; no new independent estimand",
                "Unknown external patient dependence; five runs and fixed training sample",
                "Infinite costs retained; intervals are marginal and exploratory",
                "Annotation edit bounds concern geometric counts, not FROC or clinical truth",
            ],
        ),
    )
    return dict(
        status="completed_exploratory", seconds=elapsed, summary=artifact(root / "summary.json")
    )


def main() -> None:
    """Command-line entry point for a separately versioned research namespace."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--smoke", action="store_true")
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        config = read_yaml(args.config)
        summary = verify(Path(config["outputs"]["public_root"]) / "summary.json")
        print(f"Verified {len(summary['inputs'])} inputs and {len(summary['artifacts'])} outputs")
    else:
        print(run(args.config, smoke=args.smoke, replay=args.replay))


if __name__ == "__main__":
    main()
