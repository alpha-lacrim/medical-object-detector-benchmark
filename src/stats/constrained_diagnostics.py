"""Saved-output adapters and independent correction-cost comparison."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linear_sum_assignment

from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget, box_iou
from src.stats.constrained_repairability import RepairProblem, cardinality, count_constraint
from src.stats.transportability import aligned_records, validate_weights

METRICS = ("feasible_fraction", "cost", "cost_per_reference", "cost_per_image")


def oc_cost(
    prediction: ImagePrediction,
    target: ImageTarget,
    *,
    localization_weight: float,
    dummy_cost: float,
    empty_empty_cost: float,
) -> float:
    """Otani et al. equations 5-9 with authors' dummy-to-dummy beta during solving.

    Expanded unit-capacity assignment equals their transport problem. Remove
    dummy-to-dummy transport only AFTER optimization, as in the authors' code.
    This float64 reimplementation is a diagnostic, not a COCO benchmark replay.
    """
    if not 0 <= localization_weight <= 1 or dummy_cost < 0:
        raise ValueError("Invalid OC-cost weights")
    p, g = prediction.boxes_xyxy, target.boxes_xyxy
    m, n = len(p), len(g)
    if not m and not n:
        return empty_empty_cost
    if not m or not n:
        return dummy_cost
    intersection = np.prod(
        np.maximum(
            np.minimum(p[:, None, 2:], g[None, :, 2:]) - np.maximum(p[:, None, :2], g[None, :, :2]),
            0,
        ),
        axis=2,
    )
    union = (
        np.prod(p[:, 2:] - p[:, :2], axis=1)[:, None]
        + np.prod(g[:, 2:] - g[:, :2], axis=1)[None, :]
        - intersection
    )
    hull = np.prod(
        np.maximum(p[:, None, 2:], g[None, :, 2:]) - np.minimum(p[:, None, :2], g[None, :, :2]),
        axis=2,
    )
    giou = intersection / union - (hull - union) / hull
    same = prediction.labels[:, None] == target.labels[None, :]
    classification = (1 + np.where(same, -1, 1) * prediction.scores[:, None]) / 2
    pair_cost = localization_weight * (1 - giou) / 2 + (1 - localization_weight) * classification
    costs = np.full((m + n, m + n), dummy_cost)
    costs[:m, :n] = pair_cost
    rows, cols = linear_sum_assignment(costs)
    real = (rows < m) & (cols < n)
    matched = int(real.sum())
    numerator = pair_cost[rows[real], cols[real]].sum() + dummy_cost * (m + n - 2 * matched)
    return float(numerator / (m + n - matched))


def problem_from_outputs(
    predictions: list[ImagePrediction],
    targets: list[ImageTarget],
    *,
    threshold: float,
    iou: float,
    promotion: int,
    suppression: int,
) -> tuple[RepairProblem, np.ndarray]:
    """Construct a disjoint graph; prune only unselected, incompatible candidates.

    Columns of per-image counts: historical selected H, historical rank r,
    full rank M, reference count N, retained candidates C. Pruning cannot lower
    the optimum because costs are nonnegative; full C is still reported.
    """
    predictions, targets = aligned_records(predictions, targets)
    neighbors, initial, counts = [], [], []
    offset = 0
    for p, t in zip(predictions, targets, strict=True):
        compatible = (box_iou(p.boxes_xyxy, t.boxes_xyxy) >= iou) & (
            p.labels[:, None] == t.labels[None, :]
        )
        rows = tuple(tuple(map(int, np.flatnonzero(row))) for row in compatible)
        selected = p.scores >= threshold
        full = cardinality(rows, len(t.labels))
        historical = cardinality(
            tuple(row for row, keep in zip(rows, selected, strict=True) if keep), len(t.labels)
        )
        counts.append([int(selected.sum()), historical, full, len(t.labels), len(p.scores)])
        for row, keep in zip(rows, selected, strict=True):
            if keep or row:
                neighbors.append(tuple(j + offset for j in row))
                initial.append(bool(keep))
        offset += len(t.labels)
    count = len(neighbors)
    return RepairProblem(
        tuple(neighbors), offset, tuple(initial), (promotion,) * count, (suppression,) * count
    ), np.asarray(counts, dtype=np.int64)


@dataclass
class CountRun:
    """Sufficient per-image counts for exact unit-cost observation resampling."""

    seed: int
    counts: np.ndarray

    def evaluate(
        self,
        weights: np.ndarray,
        budgets: list[float],
        targets: list[float],
        promotion: int,
        suppression: int,
    ) -> np.ndarray:
        """Recompute integer constraints; retain infeasibility as positive infinity."""
        validate_weights(weights, len(self.counts))
        h, r, full, references, _ = map(int, weights @ self.counts)
        images = int(weights.sum())
        values = np.full((len(budgets), len(targets), len(METRICS)), np.nan)
        if not references:
            return values
        for b, budget in enumerate(budgets):
            bound = count_constraint(budget, images, ceiling=False)
            for t, target in enumerate(targets):
                k = count_constraint(target, references, ceiling=True)
                feasible = k <= full
                cost = (
                    promotion * max(0, k - r) + suppression * max(0, h - r - bound)
                    if feasible
                    else np.inf
                )
                values[b, t] = [float(feasible), cost, cost / references, cost / images]
        return values


def extended_interval(point: float, draws: np.ndarray, confidence: float) -> dict:
    """Inverse empirical-CDF percentiles retain infinite draws without interpolation."""
    defined = draws[~np.isnan(draws)]
    bounds = (
        np.quantile(defined, [(1 - confidence) / 2, (1 + confidence) / 2], method="inverted_cdf")
        if len(defined)
        else [np.nan, np.nan]
    )

    def encode(value: float) -> float | str | None:
        return None if np.isnan(value) else "infinite" if np.isinf(value) else float(value)

    return dict(
        point=encode(point),
        lower=encode(bounds[0]),
        upper=encode(bounds[1]),
        finite=int(np.isfinite(draws).sum()),
        infinite=int(np.isinf(draws).sum()),
        undefined=int(np.isnan(draws).sum()),
    )
