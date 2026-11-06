"""Independent small cases for repair accounting, resampling and imposed controls."""

from dataclasses import replace

import numpy as np
import pytest

from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget
from src.stats.paired import build_patient_clusters
from src.stats.run_threshold_repairability import interval, run, summarize, summarize_controls
from src.stats.threshold_repairability import (
    METRICS,
    bootstrap,
    build_run,
    compatible_masks,
    evaluate_domains,
    transform,
    validate_domains,
    verify_control,
)

EVALUATION = dict(class_ids=[1], max_detections_per_image=100, matching_iou_threshold=0.5)
BUDGETS = [0.0, 0.25, 0.5, 1.0, 2.0]


def fixture():
    targets = [
        ImageTarget("a", (20, 20), [[0, 0, 10, 10], [5, 0, 15, 10]], [1, 1]),
        ImageTarget("b", (20, 20), np.empty((0, 4)), []),
        ImageTarget("c", (20, 20), [[0, 0, 10, 10]], [1]),
    ]
    predictions = [
        ImagePrediction(
            "a",
            (20, 20),
            [[2, 0, 12, 10], [0, 0, 7, 10], [12, 12, 20, 20]],
            [1, 1, 1],
            [0.9, 0.8, 0.9],
        ),
        ImagePrediction("b", (20, 20), [[12, 12, 20, 20]], [1], [0.9]),
        ImagePrediction("c", (20, 20), np.empty((0, 4)), [], []),
    ]
    return predictions, targets


def make(predictions=None, targets=None, seed=17):
    if predictions is None:
        predictions, targets = fixture()
    return build_run(predictions, targets, seed=seed, threshold=0.5, evaluation=EVALUATION, floor=0)


def test_components_separate_competition_absence_and_infeasible_history():
    values = make().evaluate(np.ones(3, int), BUDGETS, 1e-12)
    np.testing.assert_allclose(values[0, :4], [0, 1 / 3, 1 / 3, 1 / 3])
    assert values[0, METRICS.index("signed_cutoff_difference")] == -1 / 3
    assert values[0, METRICS.index("historical_feasible_fraction")] == 0
    np.testing.assert_allclose(values[:, :4].sum(axis=1), 1)


def test_weighted_counts_equal_direct_image_copy_reconstruction():
    predictions, targets = fixture()
    weights = np.array([2, 1, 0])
    duplicated_p, duplicated_t = [], []
    for p, t, count in zip(predictions, targets, weights, strict=True):
        for k in range(count):
            identifier = f"{p.image_id}_{k}"
            duplicated_p.append(
                ImagePrediction(identifier, p.image_size, p.boxes_xyxy, p.labels, p.scores)
            )
            duplicated_t.append(ImageTarget(identifier, t.image_size, t.boxes_xyxy, t.labels))
    actual = make().evaluate(weights, BUDGETS, 1e-12)
    expected = make(duplicated_p, duplicated_t).evaluate(np.ones(3, int), BUDGETS, 1e-12)
    np.testing.assert_array_equal(actual, expected)


def test_zero_target_draw_stays_undefined_without_losing_fp_flags():
    values = make().evaluate(np.array([0, 3, 0]), BUDGETS, 1e-12)
    assert np.isnan(values[:, :8]).all()
    assert np.isfinite(values[:, 8:]).all()
    assert interval(0.2, np.array([np.nan, 0.1, 0.3]), 0.95)["undefined"] == 1


@pytest.mark.parametrize(
    "family,level",
    [
        ("power", 0.5),
        ("power", 2),
        ("permute_scores", 1),
        ("remove_compatible", 1),
        ("remove_incompatible", 1),
    ],
)
def test_control_invariants_and_source_immutability(family, level):
    predictions, targets = fixture()
    original = [p.scores.copy() for p in predictions]
    masks = compatible_masks(predictions, targets, 0.5)
    changed, _ = transform(
        predictions, masks, family=family, level=level, rng=np.random.default_rng(4)
    )
    verify_control(make(), make(changed, targets), family, level, 1e-12)
    assert [p.image_id for p in changed] == [p.image_id for p in predictions]
    for before, after in zip(original, predictions, strict=True):
        np.testing.assert_array_equal(before, after.scores)
    if family == "permute_scores":
        np.testing.assert_array_equal(
            np.sort(np.concatenate(original)), np.sort(np.concatenate([p.scores for p in changed]))
        )


def test_power_does_not_reapply_original_score_floor():
    p = [ImagePrediction("a", (20, 20), [[0, 0, 10, 10]], [1], [1e-5])]
    t = [ImageTarget("a", (20, 20), [[0, 0, 10, 10]], [1])]
    changed, _ = transform(
        p, [np.array([True])], family="power", level=2, rng=np.random.default_rng(1)
    )
    assert changed[0].scores[0] < 1e-5
    assert make(changed, t).evaluate(np.ones(1, int), [0], 1e-12)[0, 0] == 1


def test_empty_outputs_leave_all_reference_geometry_unavailable():
    p, t = fixture()
    changed = [ImagePrediction(a.image_id, a.image_size, np.empty((0, 4)), [], []) for a in p]
    values = make(changed, t).evaluate(np.ones(3, int), BUDGETS, 1e-12)
    np.testing.assert_array_equal(values[:, :4], np.tile([0, 0, 0, 1], (len(BUDGETS), 1)))


def test_same_checkpoint_weights_reused_across_domains():
    first = make()
    p, t = fixture()
    empty = [ImagePrediction(a.image_id, a.image_size, np.empty((0, 4)), [], []) for a in p]
    second = make(empty, t, seed=42)
    domains = [[[first, second], [first]], [[first, second], [first]]]
    observations = [np.ones(3, int), np.ones(3, int)]
    result = evaluate_domains(
        domains, observations, (np.array([0, 2]), np.array([1])), BUDGETS, 1e-12
    )
    np.testing.assert_array_equal(result[0], result[1])
    assert result[0, 0, 0, 3] == 1
    groups = build_patient_clusters(first.froc.image_ids, {"a": "p1", "b": "p1", "c": "p2"})
    validate_domains(domains, groups)
    invalid = [domains[0], [[first, replace(second, seed=137)], [first]]]
    with pytest.raises(ValueError, match="Run identity"):
        validate_domains(invalid, groups)


def test_bootstrap_preserves_identity_is_deterministic_and_keeps_null_draws():
    base = make()
    domains = [[[base], [base]], [[base], [base]]]
    clusters = build_patient_clusters(base.froc.image_ids, {"a": "p1", "b": "p2", "c": "p3"})
    settings = dict(
        bootstrap_resamples=60, bootstrap_seed=12, progress_every=0, runtime_limit_seconds=60
    )
    point, draws = bootstrap(domains, clusters, BUDGETS, settings, 1e-12, "test")
    np.testing.assert_array_equal(
        draws, bootstrap(domains, clusters, BUDGETS, settings, 1e-12, "test")[1]
    )
    finite = np.isfinite(draws[..., 0])
    assert not finite.all()
    np.testing.assert_allclose(draws[..., :4].sum(axis=-1)[finite], 1)
    intervals, contrasts = summarize(
        point, draws, ["internal", "external"], ["a", "b"], BUDGETS, 0.95
    )
    assert len(intervals) == 4 * len(BUDGETS) * len(METRICS)
    for row in contrasts:
        if row["contrast"].startswith(("internal:", "external:")):
            assert row["point"] == row["lower"] == row["upper"] == 0


def test_imposed_replicates_are_not_extra_training_runs():
    rows = []
    for seed, replicates, value in [(17, 3, 1.0), (42, 1, 0.0)]:
        for rep in range(replicates):
            rows.append(
                dict(
                    dataset="internal",
                    detector="a",
                    family="test",
                    level=1,
                    budget=0.25,
                    seed=seed,
                    replicate=rep,
                    **{k: value for m in METRICS for k in [m, f"delta_{m}"]},
                )
            )
    result = summarize_controls(rows)[0]
    assert result["runs"] == 2 and result["interventions"] == 4
    assert result["threshold_ceiling"] == 0.5


def test_namespace_refuses_overwrite_before_loading_private_evidence(tmp_path):
    root = tmp_path / "accepted"
    root.mkdir()
    config = tmp_path / "config.yaml"
    config.write_text(
        f"outputs:\n  public_root: {root.as_posix()}\n"
        f"  private_root: {tmp_path.as_posix()}/private\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="never overwrite"):
        run(config)
