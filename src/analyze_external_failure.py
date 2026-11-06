"""Paired, post-hoc diagnostic interventions on frozen external detections."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment

from src.evaluate_vindr_external import deserialize, read_gzip
from src.meddet_benchmark.evaluation import ImagePrediction, _pairwise_iou, match_image
from src.stats.run_external_generalization import preflight as baseline_preflight
from src.stats.run_vindr_statistics import (
    artifact,
    read_json,
    read_yaml,
    require,
    verify_artifact,
    write_csv,
    write_json,
)
from src.stats.transportability import build_ap_cache


def select_indices(targets: list, settings: dict) -> list[int]:
    """Include every positive and sample negatives without consulting predictions."""
    require(settings["positive_images"] == "all_strict_target_positive", "Selection differs")
    order = sorted(range(len(targets)), key=lambda i: targets[i].image_id)
    positives = [i for i in order if len(targets[i].labels)]
    negatives = [i for i in order if not len(targets[i].labels)]
    require(0 < settings["negative_images"] <= len(negatives), "Invalid negative sample size")
    chosen = np.random.default_rng(settings["seed"]).choice(
        negatives, settings["negative_images"], replace=False
    )
    return sorted([*positives, *chosen.tolist()])


def retained(prediction: ImagePrediction, floor: float, cap: int) -> ImagePrediction:
    """Reproduce native strict-floor filtering and stable score-ordered truncation."""
    require(0 <= floor < 1 and cap > 0, "Invalid retention settings")
    eligible = np.flatnonzero(prediction.scores > floor)
    keep = eligible[np.argsort(-prediction.scores[eligible], kind="stable")][:cap]
    return ImagePrediction(
        prediction.image_id,
        prediction.image_size,
        prediction.boxes_xyxy[keep],
        prediction.labels[keep],
        prediction.scores[keep],
    )


def same_predictions(left: ImagePrediction, right: ImagePrediction) -> bool:
    """Require exact values, ordering, identities and image dimensions."""
    return (
        left.image_id == right.image_id
        and left.image_size == right.image_size
        and all(
            np.array_equal(getattr(left, field), getattr(right, field))
            for field in ("boxes_xyxy", "labels", "scores")
        )
    )


def maximum_coverage(prediction: ImagePrediction, target: object, iou: float) -> int:
    """Maximum one-to-one geometric coverage, independent of confidence ranking."""
    if not len(prediction.labels) or not len(target.labels):
        return 0
    edges = (_pairwise_iou(prediction.boxes_xyxy, target.boxes_xyxy) >= iou) & (
        prediction.labels[:, None] == target.labels[None, :]
    )
    rows, columns = linear_sum_assignment(edges.astype(np.int8), maximize=True)
    return int(edges[rows, columns].sum())


def image_counts(
    prediction: ImagePrediction,
    target: object,
    threshold: float,
    cap: int,
    ious: list[float],
    matching_iou: float,
) -> np.ndarray:
    """Counts for historical recall, negative-control FP and geometric coverage."""
    matches = match_image(
        prediction,
        target,
        score_threshold=threshold,
        iou_threshold=matching_iou,
        max_detections=cap,
    )
    return np.asarray(
        [
            len(matches.matches),
            len(matches.unmatched_prediction_indices) if not len(target.labels) else 0,
            *[maximum_coverage(prediction, target, iou) for iou in ious],
        ],
        dtype=np.int64,
    )


def paired_summary(
    counts: np.ndarray,
    target_counts: np.ndarray,
    settings: dict,
    arms: list[str],
    detector: str,
    seeds: list[int],
) -> tuple[list, list, np.ndarray]:
    """Resample the same images/runs across arms, separately by case stratum."""
    positive = np.flatnonzero(target_counts)
    negative = np.flatnonzero(target_counts == 0)
    require(len(positive) > 0 and len(negative) > 0, "Both case strata required")
    require(counts.shape[:3] == (len(arms), len(seeds), len(target_counts)), "Count axes differ")
    endpoints = [
        "historical_recall",
        "negative_control_fp_per_image",
        *[f"geometric_coverage_iou_{iou:g}" for iou in settings["support_ious"]],
    ]
    require(counts.shape[-1] == len(endpoints), "Metric count differs")
    denominators = np.full(len(endpoints), target_counts.sum(), dtype=float)
    denominators[1] = len(negative)
    per_run = counts.sum(axis=2) / denominators
    points = per_run.mean(axis=1)
    rng = np.random.default_rng(settings["bootstrap_seed"])
    draws = np.empty((settings["bootstrap_resamples"], len(arms), len(endpoints)))
    for b in range(len(draws)):
        weights = np.zeros(len(target_counts), dtype=np.int64)
        weights[positive] = rng.multinomial(
            len(positive), np.full(len(positive), 1 / len(positive))
        )
        weights[negative] = rng.multinomial(
            len(negative), np.full(len(negative), 1 / len(negative))
        )
        run_weights = rng.multinomial(len(seeds), np.full(len(seeds), 1 / len(seeds)))
        denom = np.full(len(endpoints), target_counts @ weights, dtype=float)
        denom[1] = len(negative)
        draws[b] = np.einsum("arim,r,i->am", counts, run_weights, weights) / len(seeds) / denom
    alpha = (1 - settings["confidence_level"]) / 2
    rows = []
    baseline = arms.index("baseline")
    for index, arm in enumerate(arms):
        delta = draws[:, index] - draws[:, baseline]
        lower, upper = np.quantile(delta, [alpha, 1 - alpha], axis=0)
        for j, endpoint in enumerate(endpoints):
            rows.append(
                dict(
                    detector=detector,
                    arm=arm,
                    endpoint=endpoint,
                    mean=points[index, j],
                    baseline=points[baseline, j],
                    delta=points[index, j] - points[baseline, j],
                    ci_lower=lower[j],
                    ci_upper=upper[j],
                    runs=len(seeds),
                    positive_images=len(positive),
                    negative_images=len(negative),
                    target_boxes=int(target_counts.sum()),
                )
            )
    indices = [arms.index(name) for name in ("expanded", "higher_cap", "lower_floor", "baseline")]
    signs = np.array([1, -1, -1, 1])
    interaction = np.einsum("bam,a->bm", draws[:, indices], signs)
    point = np.einsum("am,a->m", points[indices], signs)
    lower, upper = np.quantile(interaction, [alpha, 1 - alpha], axis=0)
    for j, endpoint in enumerate(endpoints):
        rows.append(
            dict(
                detector=detector,
                arm="floor_cap_interaction",
                endpoint=endpoint,
                mean=None,
                baseline=None,
                delta=point[j],
                ci_lower=lower[j],
                ci_upper=upper[j],
                runs=len(seeds),
                positive_images=len(positive),
                negative_images=len(negative),
                target_boxes=int(target_counts.sum()),
            )
        )
    runs = [
        dict(
            detector=detector,
            seed=seed,
            arm=arm,
            **dict(zip(endpoints, per_run[a, r].tolist(), strict=True)),
        )
        for a, arm in enumerate(arms)
        for r, seed in enumerate(seeds)
    ]
    return rows, runs, draws


def analyze(config_path: Path, *, replay: bool = False) -> dict:
    """Verify and recompute aggregates from private, complete paired collections."""
    config = read_yaml(config_path)
    private, public = (Path(config["outputs"][k]) for k in ("private_root", "public_root"))
    receipt = read_json(private / "collection.json")
    require(receipt["status"] == "complete", "Diagnostic collection is incomplete")
    for entry in receipt["inputs"]:
        verify_artifact(entry)
    for run in receipt["runs"]:
        verify_artifact(run["artifact"])
    gate = baseline_preflight(Path(config["baseline_analysis_config"]))
    protocol = gate["baseline"]["protocol"]
    all_targets = gate["targets"]
    indices = select_indices(all_targets, config["selection"])
    targets = [all_targets[i] for i in indices]
    prepared = read_json(private / "prepared.json")
    require(prepared["image_ids"] == [t.image_id for t in targets], "Diagnostic membership differs")
    arms, seeds = list(config["arms"]), protocol["models"]["seeds"]
    values = {
        d: np.zeros(
            (len(arms), len(seeds), len(targets), 2 + len(config["analysis"]["support_ious"])),
            dtype=np.int64,
        )
        for d in protocol["models"]["detectors"]
    }
    keys = [(r["detector"], r["seed"]) for r in receipt["runs"]]
    require(len(keys) == len(set(keys)) == len(seeds) * len(values), "Run count differs")
    for run in receipt["runs"]:
        bundle = read_gzip(Path(run["artifact"]["path"]))
        detector, seed = run["detector"], run["seed"]
        threshold = protocol["threshold_transport"]["primary"]["thresholds"][detector]
        for a, arm in enumerate(arms):
            predictions = deserialize(bundle["arms"][arm])
            require(len(predictions) == len(targets), "Incomplete arm")
            for i, (p, t) in enumerate(zip(predictions, targets, strict=True)):
                values[detector][a, seeds.index(seed), i] = image_counts(
                    p,
                    t,
                    threshold,
                    config["arms"][arm]["cap"],
                    config["analysis"]["support_ious"],
                    protocol["evaluation"]["matching_iou_threshold"],
                )
    rows, run_rows, arrays = [], [], {}
    for detector, counts in values.items():
        summary, runs, draws = paired_summary(
            counts,
            np.array([len(t.labels) for t in targets]),
            config["analysis"],
            arms,
            detector,
            seeds,
        )
        rows.extend(summary)
        run_rows.extend(runs)
        arrays[detector] = draws
        arrays[detector + "_counts"] = counts
    floors = config["analysis"]["full_cohort_ap_floors"]
    floor_rows = []
    for source in gate["baseline"]["external"]["runs"]:
        predictions = deserialize(read_gzip(Path(source["artifacts"][0]["path"]))["predictions"])
        scores = []
        for floor in floors:
            cache = build_ap_cache(
                predictions,
                all_targets,
                class_ids=tuple(protocol["ontology"]["canonical_classes"]),
                minimum_score=floor,
                max_dets=protocol["evaluation"]["ap"]["max_dets"],
                iou_thresholds=[protocol["evaluation"]["matching_iou_threshold"]],
                recall_points=protocol["evaluation"]["ap"]["recall_grid_points"],
            )
            scores.append(float(cache.evaluate(np.ones(len(all_targets), dtype=np.int64))[0]))
        require(
            np.isclose(scores[0], source["metrics"]["ap"]["ap50"], atol=1e-12, rtol=0),
            "Original full-cohort AP mismatch",
        )
        floor_rows.append(
            dict(
                detector=source["metadata"]["detector"],
                seed=source["metadata"]["seed"],
                original_ap50=scores[0],
                lower_evaluation_floor_ap50=scores[1],
                delta=scores[1] - scores[0],
                images=len(all_targets),
            )
        )
    tables = {
        "paired_changes.csv": rows,
        "per_run.csv": run_rows,
        "ap_floor_control.csv": floor_rows,
    }
    if replay:
        import csv

        from src.stats.paired import json_number

        for name, table in tables.items():
            with (public / name).open(encoding="utf-8", newline="") as stream:
                existing = list(csv.DictReader(stream))
            expected = [
                {k: "" if v is None else str(v) for k, v in row.items()}
                for row in json_number(table)
            ]
            require(existing == expected, f"Replay differs: {name}")
        with np.load(private / "draws.npz") as saved:
            require(
                all(np.array_equal(saved[k], v) for k, v in arrays.items()), "Draw replay differs"
            )
        summary = read_json(public / "summary.json")
        for entry in [*summary["inputs"], *summary["artifacts"]]:
            verify_artifact(entry)
        return {"status": "replay_passed", "tables": len(tables), "draws": len(draws)}
    require(not public.exists(), "Public outputs already exist; replay instead")
    public.mkdir(parents=True)
    for name, table in tables.items():
        write_csv(public / name, table)
    np.savez_compressed(private / "draws.npz", **arrays)
    summary = {
        "status": "complete_exploratory_diagnostic",
        "analysis_id": config["analysis_id"],
        "inputs": [
            *receipt["inputs"],
            artifact(private / "collection.json"),
            *[r["artifact"] for r in receipt["runs"]],
        ],
        "artifacts": [
            *[artifact(public / name) for name in tables],
            artifact(private / "draws.npz"),
        ],
        "cohort": prepared["cohort"],
        "pixel_audit": prepared["aggregate_pixel_audit"],
        "baseline_exact_replay": True,
        "retention_nested_exact_replay": True,
        "paired_changes": rows,
        "ap_floor_control": floor_rows,
    }
    write_json(public / "summary.json", summary)
    return {"status": summary["status"], "summary": (public / "summary.json").as_posix()}


def main() -> None:
    """Expose deterministic analysis/replay without inference."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    print(analyze(args.config, replay=args.replay))


if __name__ == "__main__":
    main()
