"""Independent brute-force checks of greedy edit and operational certificates."""

from itertools import combinations, permutations, product

import numpy as np
import pytest

from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget, match_image
from src.stats.froc_annotation import (
    CountCurve,
    allocations,
    bounds_by_allocation,
    count_curve,
    deletion_endpoints,
    deletion_losses,
    deletion_sets,
    family_bounds,
    paired_bounds,
)
from src.stats.transportability import build_froc_cache


def _serial(preferences, available):
    remaining = set(available)
    bits = []
    for choices in preferences:
        selected = next((g for g in choices if g in remaining), None)
        bits.append(selected is not None)
        remaining.discard(selected)
    return np.array(bits, dtype=int)


def _record(boxes, scores=None, image_id="synthetic"):
    boxes = np.array(boxes, dtype=float).reshape(-1, 4)
    labels = np.zeros(len(boxes), dtype=int)
    if scores is None:
        return ImageTarget(image_id, (100, 100), boxes, labels)
    return ImagePrediction(image_id, (100, 100), boxes, labels, np.asarray(scores))


def _cache(predictions, targets, cap=100):
    return build_froc_cache(predictions, targets, class_ids=(0,), floor=0, iou=0.5, cap=cap)


def _brute_endpoint(cache, budget):
    # Enumerate actual score thresholds, never interpolate or split a tie.
    curve = count_curve(cache, np.ones(len(cache.image_ids), dtype=int))
    return max(t for t, f in zip(curve.tp, curve.fp, strict=True) if f <= budget)


def test_exhaustive_serial_matching_single_edit_changes_at_most_one_tp_bit():
    choices = [p for k in range(4) for p in permutations(range(3), k)]
    for prefs in product(choices, repeat=3):
        full = _serial(prefs, range(3))
        for removed in range(3):
            smaller = _serial(prefs, set(range(3)) - {removed})
            assert np.all(smaller <= full)
            assert (full - smaller).sum() <= 1


def test_exhaustive_relaxed_bit_edits_are_inside_recall_envelopes():
    for bits in product((0, 1), repeat=4):
        bits = np.asarray(bits)
        n = int(bits.sum()) + 2
        curve = CountCurve(np.r_[0, bits.cumsum()], np.r_[0, (1 - bits).cumsum()], n)
        for a, d in product(range(3), repeat=2):
            if n + a - d == 0:
                with pytest.raises(ValueError):
                    bounds_by_allocation(curve, np.arange(5), np.array([a]), np.array([d]))
                continue
            lo, hi = bounds_by_allocation(curve, np.arange(5), np.array([a]), np.array([d]))
            for ups in range(a + 1):
                for up in combinations(np.flatnonzero(bits == 0), ups):
                    for downs in range(d + 1):
                        for down in combinations(np.flatnonzero(bits), downs):
                            edited = bits.copy()
                            edited[list(up)], edited[list(down)] = 1, 0
                            if edited.sum() > n + a - d:
                                continue
                            c = CountCurve(
                                np.r_[0, edited.cumsum()],
                                np.r_[0, (1 - edited).cumsum()],
                                n + a - d,
                            )
                            truth = c.endpoint(np.arange(5))[0] / c.references
                            assert np.all(truth >= lo[:, 0] - 1e-12)
                            assert np.all(truth <= hi[:, 0] + 1e-12)


def test_frontier_allocations_equal_exhaustive_at_most_budget_search():
    curves = [CountCurve(np.array([0, 1, 1, 3]), np.array([0, 0, 2, 4]), 4)]
    for k in range(7):
        pairs = [(a, d) for a in range(k + 1) for d in range(min(k - a, 4) + 1) if 4 + a - d]
        a, d = np.array(pairs).T
        lo, hi = bounds_by_allocation(curves[0], np.arange(6), a, d)
        actual = family_bounds(curves, np.ones(1, dtype=int), np.arange(6), [k])[:, 0]
        np.testing.assert_allclose(actual[:, 0], lo.min(axis=1))
        np.testing.assert_allclose(actual[:, 1], hi.max(axis=1))


def test_one_added_reference_unlocks_many_froc_tps_and_bounds_cover_it():
    boxes = [[0, 0, 10, 10], [20, 0, 30, 10], [40, 0, 50, 10]]
    p = _record(boxes, [0.9, 0.8, 0.7])
    old, new = _record(boxes[1:]), _record(boxes)
    c = count_curve(_cache([p], [old]), np.ones(1, dtype=int))
    assert _brute_endpoint(_cache([p], [old]), 0) == 0
    assert _brute_endpoint(_cache([p], [new]), 0) == 3
    lo, hi = bounds_by_allocation(c, np.array([0]), np.array([1]), np.array([0]))
    assert lo[0, 0] == 0 and hi[0, 0] == 1


def test_identical_full_froc_curves_can_have_different_shared_annotation_risks():
    boxes = [[0, 0, 10, 10], [20, 0, 30, 10]]
    t = _record(boxes)
    a, b = _record(boxes, [0.9, 0.8]), _record(boxes[::-1], [0.9, 0.8])
    subsets = deletion_sets(2, 1)
    results = []
    for p in (a, b):
        cache = _cache([p], [t])
        c = count_curve(cache, np.ones(1, dtype=int))
        np.testing.assert_array_equal(c.tp, [0, 1, 2])
        np.testing.assert_array_equal(c.fp, [0, 0, 0])
        losses = deletion_losses([p], [t], cache, floor=0, iou=0.5, cap=100, subsets=subsets)
        results.append(deletion_endpoints(c, losses, np.array([0]))[:, 0])
    np.testing.assert_array_equal(results[0] - results[1], [-1, 1])
    # A comparison with the same geometry/order in both detectors has zero risk,
    # although both individual baseline FROC curves and matching ranks are identical.
    np.testing.assert_array_equal(results[0] - results[0], [0, 0])


def test_paired_envelopes_cover_shared_geometric_deletions_and_nested_budgets():
    rng = np.random.default_rng(71)
    boxes = [[0, 0, 10, 10], [5, 0, 15, 10], [40, 0, 50, 10], [65, 0, 75, 10]]
    targets = [_record(boxes)]
    for _ in range(30):
        families, exact = [], []
        for _model in range(2):
            curves, outcomes = [], []
            for _run in range(2):
                p = _record([*boxes, [85, 85, 95, 95]], rng.choice([0.2, 0.5, 0.9], 5))
                cache = _cache([p], targets)
                curve = count_curve(cache, np.ones(1, dtype=int))
                lost = deletion_losses(
                    [p], targets, cache, floor=0, iou=0.5, cap=100, subsets=deletion_sets(4, 2)
                )
                outcomes.append(deletion_endpoints(curve, lost, np.arange(4)) / 2)
                curves.append(curve)
            families.append(curves)
            exact.append(outcomes)
        weights = (np.array([1, 2]), np.array([2, 1]))
        bounds = paired_bounds(families, weights, np.arange(4), [0, 1, 2], "deletions")
        actual = np.average(exact[0], axis=0, weights=weights[0]) - np.average(
            exact[1], axis=0, weights=weights[1]
        )
        assert np.all(actual >= bounds[2, :, 2, 0] - 1e-12)
        assert np.all(actual <= bounds[2, :, 2, 1] + 1e-12)
        assert np.all(np.diff(bounds[..., 0], axis=2) <= 1e-12)
        assert np.all(np.diff(bounds[..., 1], axis=2) >= -1e-12)
        np.testing.assert_array_equal(bounds[:, :, 0, 0], bounds[:, :, 0, 1])


def test_independent_observation_copies_match_integer_cache_weights():
    from src.stats.run_froc_annotation import evaluate

    p = [_record([[0, 0, 10, 10]], [0.9], "a"), _record([[20, 0, 30, 10]], [0.5], "b")]
    t = [_record([[0, 0, 10, 10]], image_id="a"), _record([], image_id="b")]
    c = _cache(p, t)
    domains = [[[c], [c]], [[c], [c]]]
    weights = (np.array([1]), np.array([1]))
    weighted = evaluate(domains, [np.array([2, 1]), np.array([1, 2])], weights, [0, 0.5], [0, 1])
    for d, counts in enumerate(([2, 1], [1, 2])):
        pp, tt = [], []
        for i, count in enumerate(counts):
            for j in range(count):
                name = f"{i}:{j}"
                pp.append(_record(p[i].boxes_xyxy, p[i].scores, name))
                tt.append(_record(t[i].boxes_xyxy, image_id=name))
        copy_cache = _cache(pp, tt)
        curves = [[count_curve(copy_cache, np.ones(3, dtype=int))]] * 2
        truth = paired_bounds(curves, weights, np.array([0, 1]), [0, 1])
        np.testing.assert_allclose(weighted[d], truth)


def test_random_geometric_deletions_match_full_canonical_rematching():
    rng = np.random.default_rng(20261113)
    for _ in range(80):
        xy = rng.uniform(0, 35, size=(4, 2))
        boxes = np.c_[xy, xy + rng.uniform(10, 35, size=(4, 2))]
        t = _record(boxes)
        pb = np.concatenate([boxes, boxes[:2], [[70, 70, 80, 80]]])
        p = _record(pb, rng.choice([0.1, 0.3, 0.8, 0.9], size=len(pb)))
        cap = int(rng.integers(1, len(pb) + 1))
        cache = _cache([p], [t], cap)
        c = count_curve(cache, np.ones(1, dtype=int))
        for d in (1, 2):
            subsets = deletion_sets(4, d)
            lost = deletion_losses([p], [t], cache, floor=0, iou=0.5, cap=cap, subsets=subsets)
            actual = deletion_endpoints(c, lost, np.arange(5))
            lo, hi = bounds_by_allocation(c, np.arange(5), np.array([0]), np.array([d]))
            for j, subset in enumerate(subsets):
                keep = np.ones(4, dtype=bool)
                keep[subset] = False
                changed = _record(boxes[keep])
                baseline_hits = {
                    m.prediction_index
                    for m in match_image(p, t, score_threshold=0, max_detections=cap).matches
                }
                changed_hits = {
                    m.prediction_index
                    for m in match_image(p, changed, score_threshold=0, max_detections=cap).matches
                }
                assert changed_hits <= baseline_hits
                for b in range(5):
                    expected = _brute_endpoint(_cache([p], [changed], cap), b)
                    assert actual[j, b] == expected
                    assert lo[b, 0] <= expected / (4 - d) <= hi[b, 0]


def test_same_image_two_deletions_cannot_be_summed_from_singleton_effects():
    boxes = [[0, 0, 10, 10], [5, 0, 15, 10], [60, 0, 70, 10]]
    p = _record([[2, 0, 12, 10]], [0.9])
    t = _record(boxes)
    cache = _cache([p], [t])
    singles = deletion_losses(
        [p], [t], cache, floor=0, iou=0.5, cap=100, subsets=np.array([[0], [1]])
    )
    pair = deletion_losses([p], [t], cache, floor=0, iou=0.5, cap=100, subsets=np.array([[0, 1]]))
    assert np.all(singles == -1)
    np.testing.assert_array_equal(pair, [[1, -1]])


def test_empty_predictions_and_zero_reference_draws():
    p, t = _record([], []), _record([])
    c = count_curve(_cache([p], [t]), np.ones(1, dtype=int))
    assert np.isnan(family_bounds([c], np.ones(1, dtype=int), np.array([0]), [0, 2])).all()
    c = CountCurve(np.array([0]), np.array([0]), 3)
    np.testing.assert_array_equal(
        family_bounds([c], np.ones(1, dtype=int), np.array([0]), [0, 1, 2]), 0
    )


def test_observation_copies_and_monotone_scores_preserve_curves():
    p = _record([[0, 0, 10, 10], [20, 0, 30, 10]], [0.5, 0.5])
    t = _record([[0, 0, 10, 10]])
    base = count_curve(_cache([p], [t]), np.array([3]))
    transformed = _record(p.boxes_xyxy, p.scores**2)
    other = count_curve(_cache([transformed], [t]), np.array([3]))
    np.testing.assert_array_equal(base.tp, other.tp)
    np.testing.assert_array_equal(base.fp, other.fp)
    assert base.references == 3
    assert base.endpoint(np.array([2]))[0][0] == 0  # Whole ties cannot be split.
    assert base.endpoint(np.array([3]))[0][0] == 3


@pytest.mark.parametrize("k,n,mode", [(-1, 4, "mixed"), (1, -1, "mixed"), (1, 4, "bogus")])
def test_invalid_edit_allocations(k, n, mode):
    with pytest.raises(ValueError):
        allocations(k, n, mode)
