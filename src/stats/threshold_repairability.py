"""Fixed-output recall accounting, paired uncertainty and controlled perturbations."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any

import numpy as np

from src.analyze_external_failure import maximum_coverage
from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget, box_iou
from src.stats.paired import draw_independent_run_bootstrap_multiplicities, stable_rng_seed
from src.stats.transportability import (
    FrocCache,
    aligned_records,
    build_froc_cache,
    draw_observations,
    operating_counts,
    validate_weights,
)

METRICS = (
    "threshold_ceiling",
    "budget_barrier",
    "assignment_gap",
    "unavailable_geometry",
    "all_candidate_recall",
    "geometry_ceiling",
    "historical_recall",
    "signed_cutoff_difference",
    "historical_fp_per_image",
    "historical_feasible_fraction",
    "floor_limited_fraction",
    "cap_saturation_fraction",
)


@dataclass
class RepairRun:
    """Per-image integer counts and the exact retained-score curve for one run."""

    seed: int
    froc: FrocCache
    geometry: np.ndarray
    primary: np.ndarray
    at_cap: np.ndarray

    def evaluate(self, weights: np.ndarray, budgets: list[float], tolerance: float) -> np.ndarray:
        """Recompute nonlinear budget endpoints before averaging selected runs."""
        validate_weights(weights, len(self.froc.image_ids))
        fp, recall = self.froc.curve(weights)
        b = np.asarray(budgets)
        rb = recall[np.searchsorted(fp, b + tolerance, side="right") - 1]
        denominator = int(weights @ self.froc.target_counts)
        g = float(weights @ self.geometry / denominator) if denominator else np.nan
        tp, false = weights @ self.primary
        r0 = float(tp / denominator) if denominator else np.nan
        fp0 = float(false / weights.sum())
        values = np.column_stack(
            [
                rb,
                recall[-1] - rb,
                np.full(len(b), g - recall[-1]),
                np.full(len(b), 1 - g),
                np.full(len(b), recall[-1]),
                np.full(len(b), g),
                np.full(len(b), r0),
                rb - r0,
                np.full(len(b), fp0),
                (fp0 <= b + tolerance).astype(float),
                (fp[-1] < b - tolerance).astype(float),
                np.full(len(b), weights @ self.at_cap / weights.sum()),
            ]
        )
        if denominator and (
            np.min(values[:, :4]) < -tolerance
            or not np.allclose(values[:, :4].sum(axis=1), 1, rtol=0, atol=tolerance)
        ):
            raise ValueError("Repairability identity or nonnegative components failed")
        return values


def build_run(
    predictions: list[ImagePrediction],
    targets: list[ImageTarget],
    *,
    seed: int,
    threshold: float,
    evaluation: dict,
    floor: float,
) -> RepairRun:
    """Keep all images and cache geometry without reading pixels or loading models."""
    predictions, targets = aligned_records(predictions, targets)
    cap, iou = evaluation["max_detections_per_image"], evaluation["matching_iou_threshold"]
    if any(len(p.scores) > cap for p in predictions):
        raise ValueError("Input population exceeds the frozen detection cap")
    cache = build_froc_cache(
        predictions,
        targets,
        class_ids=tuple(evaluation["class_ids"]),
        floor=floor,
        iou=iou,
        cap=cap,
    )
    geometry = np.asarray(
        [maximum_coverage(p, t, iou) for p, t in zip(predictions, targets, strict=True)],
        dtype=np.int64,
    )
    return RepairRun(
        seed,
        cache,
        geometry,
        operating_counts(cache, threshold),
        np.asarray([len(p.scores) == cap for p in predictions], dtype=np.int64),
    )


def validate_domains(domains: list, clusters: Any) -> None:
    """Require exact seed pairing and shared reference populations before resampling."""
    if len(domains) != 2 or any(len(domain) != 2 for domain in domains):
        raise ValueError("Two cohorts and two detector families are required")
    for detector in range(2):
        seeds = [[run.seed for run in domain[detector]] for domain in domains]
        if not seeds[0] or seeds[0] != seeds[1] or len(set(seeds[0])) != len(seeds[0]):
            raise ValueError("Run identity/order differs across cohorts")
    for domain in domains:
        reference = domain[0][0].froc
        for family in domain:
            for run in family:
                if (
                    run.froc.image_ids != reference.image_ids
                    or not np.array_equal(run.froc.target_counts, reference.target_counts)
                    or run.primary.shape != (len(reference.image_ids), 2)
                    or run.geometry.shape != reference.target_counts.shape
                    or np.any(run.geometry > reference.target_counts)
                ):
                    raise ValueError("Reference population differs between runs")
    if clusters.image_ids != domains[0][0][0].froc.image_ids:
        raise ValueError("Internal patient order differs")


def evaluate_domains(
    domains: list,
    observations: list[np.ndarray],
    run_weights: tuple,
    budgets: list[float],
    tolerance: float,
) -> np.ndarray:
    """Couple each cohort's observations and reuse checkpoint weights across domains."""
    values = np.empty((len(domains), len(run_weights), len(budgets), len(METRICS)))
    for d, domain in enumerate(domains):
        for model, runs in enumerate(domain):
            selected = np.flatnonzero(run_weights[model])
            metrics = np.asarray(
                [runs[k].evaluate(observations[d], budgets, tolerance) for k in selected]
            )
            values[d, model] = np.average(metrics, axis=0, weights=run_weights[model][selected])
    return values


def bootstrap(
    domains: list,
    clusters: Any,
    budgets: list[float],
    settings: dict,
    tolerance: float,
    label: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Joint percentile draws; retain undefined metrics and all infeasible policies."""
    validate_domains(domains, clusters)
    sizes = [len(domain[0][0].froc.image_ids) for domain in domains]
    run_ones = tuple(np.ones(len(runs), dtype=np.int64) for runs in domains[0])
    point = evaluate_domains(
        domains, [np.ones(n, dtype=np.int64) for n in sizes], run_ones, budgets, tolerance
    )
    draws = np.empty((settings["bootstrap_resamples"], *point.shape))
    rng = np.random.default_rng(stable_rng_seed(settings["bootstrap_seed"], label))
    started = perf_counter()
    for index in range(len(draws)):
        observations = [
            draw_observations(rng, sizes[0], clusters),
            draw_observations(rng, sizes[1], None),
        ]
        weights = draw_independent_run_bootstrap_multiplicities(
            rng,
            detector_a_run_count=len(run_ones[0]),
            detector_b_run_count=len(run_ones[1]),
        )
        draws[index] = evaluate_domains(domains, observations, weights, budgets, tolerance)
        if settings["progress_every"] and (index + 1) % settings["progress_every"] == 0:
            print(f"Joint repairability bootstrap {index + 1}/{len(draws)}", flush=True)
            projected = (perf_counter() - started) * len(draws) / (index + 1)
            if projected > settings["runtime_limit_seconds"]:
                raise ValueError("Projected bootstrap runtime exceeds the configured limit")
    return point, draws


def compatible_masks(
    predictions: list[ImagePrediction], targets: list[ImageTarget], iou: float
) -> list[np.ndarray]:
    """Mark individual same-class compatibility without declaring a clinical finding."""
    masks = []
    for prediction, target in zip(predictions, targets, strict=True):
        if not len(target.labels):
            masks.append(np.zeros(len(prediction.scores), dtype=bool))
        else:
            overlap = box_iou(prediction.boxes_xyxy, target.boxes_xyxy)
            masks.append(
                np.any(
                    (overlap >= iou) & (prediction.labels[:, None] == target.labels[None, :]),
                    axis=1,
                )
            )
    return masks


def transform(
    predictions: list[ImagePrediction],
    compatible: list[np.ndarray],
    *,
    family: str,
    level: float,
    rng: np.random.Generator,
) -> tuple[list[ImagePrediction], int]:
    """Change scores or membership in copies; preserve targets and every image entry."""
    scores = np.concatenate([p.scores for p in predictions])
    mask = np.concatenate(compatible)
    keep = np.ones(len(scores), dtype=bool)
    modified = scores.copy()
    if family == "power":
        if level <= 0:
            raise ValueError("A strictly increasing score power must be positive")
        modified = scores**level
        if len(np.unique(modified)) != len(np.unique(scores)):
            raise ValueError("Monotone control lost score resolution")
        selected_count = len(scores)
    else:
        if not 0 <= level <= 1:
            raise ValueError("Perturbation fraction outside [0, 1]")
        if family == "permute_scores":
            eligible = np.arange(len(scores))
        elif family == "remove_compatible":
            eligible = np.flatnonzero(mask)
        elif family == "remove_incompatible":
            eligible = np.flatnonzero(~mask)
        else:
            raise ValueError("Unknown perturbation family")
        selected = rng.permutation(eligible)[: int(np.floor(level * len(eligible)))]
        selected_count = len(selected)
        if family == "permute_scores":
            modified[selected] = scores[rng.permutation(selected)]
        else:
            keep[selected] = False
    output, offset = [], 0
    for prediction in predictions:
        size = len(prediction.scores)
        local = keep[offset : offset + size]
        output.append(
            ImagePrediction(
                prediction.image_id,
                prediction.image_size,
                prediction.boxes_xyxy[local],
                prediction.labels[local],
                modified[offset : offset + size][local],
            )
        )
        offset += size
    return output, selected_count


def verify_control(
    base: RepairRun, changed: RepairRun, family: str, level: float, tol: float
) -> None:
    """Check control invariants without requiring a favorable empirical score direction."""
    ones = np.ones(len(base.froc.image_ids), dtype=np.int64)
    original_fp, original_r = base.froc.curve(ones)
    changed_fp, changed_r = changed.froc.curve(ones)
    if family in ("power", "permute_scores", "remove_incompatible") and not np.array_equal(
        base.geometry, changed.geometry
    ):
        raise ValueError("Geometry-preserving control changed maximum matching")
    if family == "power" and not (
        np.array_equal(original_fp, changed_fp) and np.array_equal(original_r, changed_r)
    ):
        raise ValueError("Strictly monotone control changed the exact frontier")
    if family == "remove_compatible" and (
        np.any(changed.geometry > base.geometry) or (level == 1 and np.any(changed.geometry))
    ):
        raise ValueError("Compatible-removal ceiling invariant failed")
    if family == "remove_incompatible":
        # Compare every original FP coordinate, not only selected presentation budgets.
        indices = np.searchsorted(changed_fp, original_fp + tol, side="right") - 1
        if np.any(changed_r[indices] < original_r - tol):
            raise ValueError("Removing impossible matches worsened the frontier")
