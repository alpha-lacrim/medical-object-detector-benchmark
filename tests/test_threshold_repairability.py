"""Known synthetic failures test the scope of the proposed recall ceilings."""

from __future__ import annotations

import numpy as np
import pytest

from scripts.analyze_threshold_repairability import components, run, unique_runs
from src.analyze_external_failure import maximum_coverage
from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget
from src.stats.transportability import build_froc_cache


def evaluate(boxes, scores, targets, budget=0.25):
    """Small exact-score examples with one image and no private data."""
    prediction = ImagePrediction(
        "synthetic", (20, 20), np.asarray(boxes).reshape(-1, 4), np.ones(len(scores), int), scores
    )
    target = ImageTarget(
        "synthetic", (20, 20), np.asarray(targets).reshape(-1, 4), np.ones(len(targets), int)
    )
    cache = build_froc_cache([prediction], [target], class_ids=(1,), floor=0, iou=0.5, cap=100)
    fp, recall = cache.curve(np.ones(1, dtype=int))
    ceiling = float(cache.budgets(np.ones(1, dtype=int), [budget], 1e-12)[0][0])
    geometry = maximum_coverage(prediction, target, 0.5) / len(targets)
    return fp, recall, ceiling, geometry


def test_monotone_transform_preserves_entire_frontier_and_ties():
    boxes = [[0, 0, 10, 10], [12, 12, 20, 20], [12, 0, 20, 8]]
    scores = np.array([0.2, 0.9, 0.9])
    original = evaluate(boxes, scores, [[0, 0, 10, 10]])
    transformed = evaluate(boxes, scores**2, [[0, 0, 10, 10]])
    for a, b in zip(original, transformed, strict=True):
        np.testing.assert_array_equal(a, b)
    assert original[2] == 0 and original[3] == 1


def test_reranking_can_repair_budget_barrier_without_changing_geometry():
    boxes = [[0, 0, 10, 10], [12, 12, 20, 20]]
    original = evaluate(boxes, [0.2, 0.9], [[0, 0, 10, 10]])
    reranked = evaluate(boxes, [0.9, 0.2], [[0, 0, 10, 10]])
    assert original[2:] == (0, 1)
    assert reranked[2:] == (1, 1)


def test_missing_geometry_and_assignment_competition_are_distinct():
    missing = evaluate([[12, 12, 20, 20]], [0.9], [[0, 0, 10, 10]])
    assert missing[2:] == (0, 0)
    _, recall, ceiling, geometry = evaluate(
        [[2, 0, 12, 10], [0, 0, 7, 10]], [0.9, 0.8], [[0, 0, 10, 10], [5, 0, 15, 10]]
    )
    assert recall[-1] == 0.5 and geometry == 1
    parts = components(0, ceiling, recall[-1], geometry, 0, 0.25, 1e-12)
    assert parts["assignment_gap"] == 0.5 and parts["unavailable_geometry"] == 0
    assert sum(parts.values()) == 1


@pytest.mark.parametrize(
    "values, reason",
    [
        ((0.1, 0.2, 0.6, 0.7, 0.3, 0.25, 1e-12), "exceeds budget"),
        ((0.1, 0.2, 0.6, 0.5, 0.1, 0.25, 1e-12), "not nested"),
        ((0.1, np.nan, 0.6, 0.7, 0.1, 0.25, 1e-12), "Nonfinite"),
        ((0.1, 0.2, 0.6, 1.1, 0.1, 0.25, 1e-12), "outside"),
    ],
)
def test_invalid_or_infeasible_decompositions_fail(values, reason):
    with pytest.raises(ValueError, match=reason):
        components(*values)


def test_duplicate_seed_cannot_silently_replace_a_run():
    with pytest.raises(ValueError, match="Duplicate"):
        unique_runs([{"detector": "a", "seed": "17"}] * 2)


def test_source_hash_mismatch_stops_before_output(tmp_path):
    source = tmp_path / "source.csv"
    source.write_text("changed source", encoding="utf-8")
    config = tmp_path / "config.yaml"
    config.write_text(
        f"sources:\n  table:\n    path: {source.as_posix()}\n    sha256: wrong\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Source hash mismatch"):
        run(config)
