"""Geometric/greedy separation, output controls and observation/run resampling."""

from dataclasses import replace
from itertools import product

import numpy as np
import pytest

from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget, match_image
from src.stats.constrained_diagnostics import (
    CountRun,
    extended_interval,
    oc_cost,
    problem_from_outputs,
)
from src.stats.constrained_repairability import solve
from src.stats.paired import build_patient_clusters
from src.stats.run_constrained_repairability import bootstrap, evaluate
from src.stats.threshold_repairability import build_run, compatible_masks, transform

EVALUATION = dict(class_ids=[1], max_detections_per_image=100, matching_iou_threshold=0.5)
SETTINGS = dict(
    target_recalls=[0.25, 0.75, 1.0],
    promotion_cost=1,
    suppression_cost=1,
    bootstrap_resamples=40,
    bootstrap_seed=12,
    progress_every=0,
    runtime_limit_seconds=60,
)


def fixture():
    t = [
        ImageTarget("a", (20, 20), [[0, 0, 10, 10], [5, 0, 15, 10]], [1, 1]),
        ImageTarget("b", (20, 20), np.empty((0, 4)), []),
    ]
    p = [
        ImagePrediction("a", (20, 20), [[2, 0, 12, 10], [0, 0, 7, 10]], [1, 1], [0.9, 0.8]),
        ImagePrediction("b", (20, 20), [[0, 0, 10, 10]], [1], [0.9]),
    ]
    return p, t


def build(p, t, threshold=0.5):
    return problem_from_outputs(p, t, threshold=threshold, iou=0.5, promotion=1, suppression=1)


def test_oracle_assignment_not_achievable_by_any_membership_policy_in_fixed_order():
    p, t = fixture()
    graph, _ = build(p[:1], t[:1])
    assert solve(graph, 2, 0).cost == 0
    for keep in product((False, True), repeat=2):
        mask = np.array(keep)
        changed = replace(
            p[0],
            boxes_xyxy=p[0].boxes_xyxy[mask],
            labels=p[0].labels[mask],
            scores=p[0].scores[mask],
        )
        actual = match_image(
            changed, t[0], score_threshold=0, iou_threshold=0.5, max_detections=100
        )
        assert len(actual.matches) <= 1


def test_score_ties_are_whole_threshold_groups_and_monotone_maps_transport_cutoff():
    p, t = fixture()
    p = [replace(row, scores=np.full(len(row.scores), 0.8)) for row in p]
    original, original_counts = build(p, t, 0.8)
    masks = compatible_masks(p, t, 0.5)
    for power in (0.5, 2):
        changed, _ = transform(p, masks, family="power", level=power, rng=np.random.default_rng(2))
        graph, counts = build(changed, t, 0.8**power)
        np.testing.assert_array_equal(counts, original_counts)
        assert solve(graph, 2, 0).cost == solve(original, 2, 0).cost
        before = build_run(p, t, seed=1, threshold=0.8, evaluation=EVALUATION, floor=0)
        after = build_run(changed, t, seed=1, threshold=0.8**power, evaluation=EVALUATION, floor=0)
        for a, b in zip(
            before.froc.curve(np.ones(2, int)), after.froc.curve(np.ones(2, int)), strict=True
        ):
            np.testing.assert_array_equal(a, b)


def test_reference_insertion_on_negative_image_can_break_froc_count_bound():
    p = [
        ImagePrediction(str(i), (20, 20), [[0, 0, 10, 10]], [1], [0.9 - 0.1 * i]) for i in range(3)
    ]
    targets = [ImageTarget(str(i), (20, 20), [[0, 0, 10, 10]], [1]) for i in range(3)]
    original = [replace(targets[0], boxes_xyxy=np.empty((0, 4)), labels=[]), *targets[1:]]
    before = build_run(p, original, seed=1, threshold=0, evaluation=EVALUATION, floor=0)
    after = build_run(p, targets, seed=1, threshold=0, evaluation=EVALUATION, floor=0)
    assert before.evaluate(np.ones(3, int), [0], 0)[0, 0] == 0
    assert after.evaluate(np.ones(3, int), [0], 0)[0, 0] == 1
    assert after.geometry.sum() - before.geometry.sum() == 1
    # One reference insertion unlocks three TPs at FP budget zero, not at most one.


def test_weighted_counts_equal_distinct_image_copy_flow():
    p, t = fixture()
    _, counts = build(p, t)
    weights = np.array([2, 1])
    copies_p, copies_t = [], []
    for a, b, w in zip(p, t, weights, strict=True):
        for j in range(w):
            identifier = f"{a.image_id}_{j}"
            copies_p.append(replace(a, image_id=identifier))
            copies_t.append(replace(b, image_id=identifier))
    graph, copied = build(copies_p, copies_t)
    actual = CountRun(1, counts).evaluate(weights, [0, 0.25], [0.5, 1], 1, 1)
    expected = CountRun(1, copied).evaluate(np.ones(3, int), [0, 0.25], [0.5, 1], 1, 1)
    np.testing.assert_array_equal(actual, expected)
    assert actual[0, 1, 1] == solve(graph, 4, 0).cost


def test_joint_bootstrap_keeps_infeasible_and_undefined_draws():
    p, t = fixture()
    _, counts = build(p, t)
    first = CountRun(1, counts)
    second_counts = counts.copy()
    second_counts[:, :3] = 0
    second = CountRun(2, second_counts)
    domains = [[[first, second], [first]], [[first, second], [first]]]
    clusters = build_patient_clusters(("a", "b"), {"a": "p1", "b": "p2"})
    point, draws = bootstrap(domains, clusters, SETTINGS, [0, 0.25], "test")
    np.testing.assert_array_equal(
        draws, bootstrap(domains, clusters, SETTINGS, [0, 0.25], "test")[1]
    )
    assert np.isnan(draws).any()
    assert np.isinf(point[..., 1]).any()
    both = evaluate(
        domains, [np.ones(2, int)] * 2, (np.array([2, 0]), np.array([1])), SETTINGS, [0, 0.25]
    )
    np.testing.assert_array_equal(both[0], both[1])
    assert np.isfinite(both).all()  # Unselected infeasible run must not cause 0 * inf.
    interval = extended_interval(np.inf, np.array([1, np.inf, np.nan]), 0.95)
    assert interval == dict(
        point="infinite", lower=1, upper="infinite", finite=1, infinite=1, undefined=1
    )


@pytest.mark.parametrize("family", ["permute_scores", "remove_compatible", "remove_incompatible"])
def test_output_controls_keep_geometry_contracts(family):
    p, t = fixture()
    original, old = build(p, t)
    changed, _ = transform(
        p, compatible_masks(p, t, 0.5), family=family, level=1, rng=np.random.default_rng(5)
    )
    problem, counts = build(changed, t)
    if family == "remove_compatible":
        assert counts[:, 2].sum() == 0 and solve(problem, 1, 0) is None
    else:
        np.testing.assert_array_equal(counts[:, 2], old[:, 2])
    if family == "remove_incompatible":
        assert solve(problem, 2, 0).cost <= solve(original, 2, 0).cost


def test_oc_cost_hand_computed_and_dummy_transport_convention():
    kwargs = dict(localization_weight=0.5, dummy_cost=0.6, empty_empty_cost=0)
    target = ImageTarget("a", (20, 20), [[0, 0, 1, 1]], [1])
    p = ImagePrediction("a", (20, 20), [[0, 0, 1, 1]], [1], [1])
    assert oc_cost(p, target, **kwargs) == 0
    assert oc_cost(replace(p, scores=[0]), target, **kwargs) == 0.25
    empty_p = replace(p, boxes_xyxy=np.empty((0, 4)), labels=[], scores=[])
    empty_t = replace(target, boxes_xyxy=np.empty((0, 4)), labels=[])
    assert oc_cost(empty_p, empty_t, **kwargs) == 0
    assert oc_cost(empty_p, target, **kwargs) == 0.6
    assert oc_cost(p, empty_t, **kwargs) == 0.6
    far = replace(p, boxes_xyxy=[[10, 0, 11, 1]])
    # Authors' beta on dummy-dummy makes c>beta remain unmatched, not c>2*beta.
    assert oc_cost(far, target, **dict(kwargs, localization_weight=1)) == 0.6
    duplicate = replace(p, boxes_xyxy=[[0, 0, 1, 1], [0, 0, 1, 1]], labels=[1, 1], scores=[1, 1])
    assert oc_cost(duplicate, target, **kwargs) == 0.3
