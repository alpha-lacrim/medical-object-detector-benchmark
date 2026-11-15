"""Annotation-edit certificates for canonical greedy, whole-tie FROC curves."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np

from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget, match_image
from src.stats.transportability import FrocCache, aligned_records, validate_weights


@dataclass(frozen=True)
class CountCurve:
    """Integer cumulative counts at all whole-score thresholds, including reject-all."""

    tp: np.ndarray
    fp: np.ndarray
    references: int

    def __post_init__(self) -> None:
        if (
            self.tp.ndim != 1
            or self.tp.shape != self.fp.shape
            or not len(self.tp)
            or self.tp[0] != 0
            or self.fp[0] != 0
            or self.references < 0
            or any(not np.issubdtype(a.dtype, np.integer) for a in (self.tp, self.fp))
            or any(np.any(np.diff(a) < 0) for a in (self.tp, self.fp))
            or self.tp[-1] > self.references
        ):
            raise ValueError("Invalid integer FROC curve")

    def endpoint(self, budgets: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return maximal whole-prefix TP and its FP count; negative budgets reject all."""
        indices = np.maximum(0, np.searchsorted(self.fp, budgets, side="right") - 1)
        return self.tp[indices], self.fp[indices]


def count_curve(cache: FrocCache, weights: np.ndarray) -> CountCurve:
    """Use integer observation copies without rounding normalized FROC values."""
    validate_weights(weights, len(cache.image_ids))
    w = weights[cache.images]
    tp = np.r_[0, np.cumsum(w * cache.matched)[cache.score_ends]]
    fp = np.r_[0, np.cumsum(w * ~cache.matched)[cache.score_ends]]
    return CountCurve(tp, fp, int(weights @ cache.target_counts))


def allocations(k: int, references: int, mode: str) -> tuple[np.ndarray, np.ndarray]:
    """Enumerate allowed (insertions, deletions), excluding undefined zero-reference sets."""
    if k < 0 or references < 0 or mode not in {"mixed", "insertions", "deletions"}:
        raise ValueError("Invalid edit budget or mode")
    pairs = [
        (a, d)
        for a in range(k + 1 if mode != "deletions" else 1)
        for d in range(min(k - a, references) + 1 if mode != "insertions" else 1)
        if references + a - d > 0
    ]
    if not pairs:
        return np.array([], dtype=int), np.array([], dtype=int)
    return tuple(np.asarray(pairs, dtype=int).T)


def bounds_by_allocation(
    curve: CountCurve, budgets: np.ndarray, additions: np.ndarray, deletions: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Conservative recall bounds, indexed [FP budget, shared edit allocation]."""
    a, d = additions[None, :], deletions[None, :]
    b = np.asarray(budgets)[:, None]
    n = curve.references + a - d
    if np.any(b < 0) or np.any(a < 0) or np.any(d < 0) or np.any(n <= 0):
        raise ValueError("Invalid FP budget, edits or changed reference count")
    lo, _ = curve.endpoint(b - d)
    lo = np.maximum(0, lo - d)
    # If b-d<0, reject-all remains a valid lower guarantee.
    lo = np.where(b >= d, lo, 0)
    hi, fp = curve.endpoint(b + a)
    hi = np.minimum(n, hi + np.minimum(a, fp))
    return lo / n, hi / n


def family_bounds(
    curves: list[CountCurve],
    run_weights: np.ndarray,
    budgets: np.ndarray,
    edit_counts: list[int],
    mode: str = "mixed",
) -> np.ndarray:
    """Average runs before optimizing a common annotation edit-type allocation."""
    if not curves or len({c.references for c in curves}) != 1:
        raise ValueError("Runs must share a reference set")
    validate_weights(run_weights, len(curves))
    result = np.full((len(budgets), len(edit_counts), 2), np.nan)
    if not curves[0].references:
        return result
    for j, k in enumerate(edit_counts):
        a, d = allocations(k, curves[0].references, mode)
        lows, highs = [], []
        for i in np.flatnonzero(run_weights):
            lo, hi = bounds_by_allocation(curves[i], budgets, a, d)
            lows.append(lo)
            highs.append(hi)
        weights = run_weights[run_weights > 0]
        result[:, j, 0] = np.average(lows, axis=0, weights=weights).min(axis=1)
        result[:, j, 1] = np.average(highs, axis=0, weights=weights).max(axis=1)
    return result


def paired_bounds(
    families: list[list[CountCurve]],
    run_weights: tuple[np.ndarray, np.ndarray],
    budgets: np.ndarray,
    edit_counts: list[int],
    mode: str = "mixed",
) -> np.ndarray:
    """Bound two run means and their difference under common edit-type counts.

    Output axes: detector A / detector B / A-B, budget, edits, lower/upper.
    Unknown edit locations are relaxed; only exact deletion enumeration certifies
    geometrically attainable extrema for a shared subset of reference boxes.
    """
    if len(families) != 2 or not all(families):
        raise ValueError("Exactly two nonempty detector families are required")
    references = {c.references for family in families for c in family}
    if len(references) != 1:
        raise ValueError("Detector families must share reference counts")
    for curves, weights in zip(families, run_weights, strict=True):
        validate_weights(weights, len(curves))
    n = next(iter(references))
    output = np.full((3, len(budgets), len(edit_counts), 2), np.nan)
    if not n:
        return output
    for j, k in enumerate(edit_counts):
        a, d = allocations(k, n, mode)
        means = []
        for curves, weights in zip(families, run_weights, strict=True):
            selected = np.flatnonzero(weights)
            values = [bounds_by_allocation(curves[i], budgets, a, d) for i in selected]
            means.append(np.average(values, axis=0, weights=weights[selected]))
        for m, (lo, hi) in enumerate(means):
            output[m, :, j, 0] = lo.min(axis=1)
            output[m, :, j, 1] = hi.max(axis=1)
        output[2, :, j, 0] = (means[0][0] - means[1][1]).min(axis=1)
        output[2, :, j, 1] = (means[0][1] - means[1][0]).max(axis=1)
    return output


def deletion_sets(references: int, count: int) -> np.ndarray:
    """Stable common reference-subset order for exact one/two-deletion diagnostics."""
    if count not in (1, 2) or references < count:
        raise ValueError("Exact deletion diagnostics require one/two existing references")
    return np.asarray(list(combinations(range(references), count)), dtype=int)


def deletion_losses(
    predictions: list[ImagePrediction],
    targets: list[ImageTarget],
    cache: FrocCache,
    *,
    floor: float,
    iou: float,
    cap: int,
    subsets: np.ndarray,
) -> np.ndarray:
    """Find lost greedy TP score groups, rematching only affected images.

    -1 is padding. A deleted reference changes at most one TP bit; matches may
    cascade to different references. Same-image pair losses must be rematched
    jointly rather than summed from singleton deletion effects.
    """
    predictions, targets = aligned_records(predictions, targets)
    n = sum(len(t.labels) for t in targets)
    if cache.image_ids != tuple(t.image_id for t in targets) or not np.array_equal(
        cache.target_counts, [len(t.labels) for t in targets]
    ):
        raise ValueError("Deletion cache uses different reference observations")
    if (
        subsets.ndim != 2
        or not np.issubdtype(subsets.dtype, np.integer)
        or np.any(subsets < 0)
        or np.any(subsets >= n)
        or any(len(set(row)) != len(row) for row in subsets)
    ):
        raise ValueError("Invalid reference subsets")
    groups = cache.scores[cache.score_ends]
    owners = [(i, j) for i, t in enumerate(targets) for j in range(len(t.labels))]
    baseline, memo = {}, {}
    losses = np.full(subsets.shape, -1, dtype=int)
    for row_index, subset in enumerate(subsets):
        per_image: dict[int, list[int]] = {}
        for reference in subset:
            i, j = owners[reference]
            per_image.setdefault(i, []).append(j)
        row_losses = []
        for i, removed in per_image.items():
            key = (i, tuple(sorted(removed)))
            if key not in memo:
                p, t = predictions[i], targets[i]
                if i not in baseline:
                    baseline[i] = {
                        m.prediction_index
                        for m in match_image(
                            p, t, score_threshold=floor, iou_threshold=iou, max_detections=cap
                        ).matches
                    }
                keep = np.ones(len(t.labels), dtype=bool)
                keep[removed] = False
                changed = ImageTarget(t.image_id, t.image_size, t.boxes_xyxy[keep], t.labels[keep])
                after = {
                    m.prediction_index
                    for m in match_image(
                        p, changed, score_threshold=floor, iou_threshold=iou, max_detections=cap
                    ).matches
                }
                if not after.issubset(baseline[i]) or len(baseline[i] - after) > len(removed):
                    raise ValueError("Canonical greedy deletion lemma violated")
                memo[key] = [
                    int(np.searchsorted(-groups, -p.scores[j])) + 1
                    for j in sorted(baseline[i] - after)
                ]
            row_losses.extend(memo[key])
        losses[row_index, : len(row_losses)] = sorted(row_losses)
    return losses


def deletion_endpoints(curve: CountCurve, losses: np.ndarray, budgets: np.ndarray) -> np.ndarray:
    """Exact whole-tie TP endpoints after each supplied sparse TP-loss trace.

    Vectorized binary search costs O(subsets * budgets * deletions * log(prefixes)).
    The loss trace is computed by canonical rematching, not a label-flip surrogate.
    """
    losses = np.asarray(losses)
    budgets = np.asarray(budgets)
    if (
        losses.ndim != 2
        or not np.issubdtype(losses.dtype, np.integer)
        or np.any(losses < -1)
        or np.any(losses >= len(curve.tp))
        or np.any(losses == 0)
        or np.any(budgets < 0)
    ):
        raise ValueError("Invalid deletion losses or budgets")
    lo = np.zeros((len(losses), len(budgets)), dtype=int)
    hi = np.full_like(lo, len(curve.tp))
    valid_losses = np.where(losses < 0, len(curve.tp), losses)
    while np.any(lo + 1 < hi):
        mid = (lo + hi) // 2
        lost = np.sum(valid_losses[:, :, None] <= mid[:, None, :], axis=1)
        feasible = curve.fp[mid] + lost <= budgets[None, :]
        lo = np.where(feasible, mid, lo)
        hi = np.where(feasible, hi, mid)
    lost = np.sum(valid_losses[:, :, None] <= lo[:, None, :], axis=1)
    return curve.tp[lo] - lost
