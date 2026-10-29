"""Independent synthetic oracles for post-hoc diagnostics and resampling."""

import json
from dataclasses import replace

import numpy as np
import pytest

from src.meddet_benchmark.coco_evaluation import evaluate_coco
from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget, evaluate_operating_point
from src.stats import external_generalization as analysis_module
from src.stats.external_generalization import (
    ap_events,
    error_decomposition,
    joint_bootstrap,
    local_annotations,
    prevalence_metrics,
    prevalence_weights,
    weighted_ap,
)
from src.stats.paired import build_patient_clusters, json_number
from src.stats.run_external_generalization import aggregate, intervals
from src.stats.transportability import (
    RunEvidence,
    build_ap_cache,
    build_froc_cache,
    operating_counts,
)


def settings():
    return {
        "partial_iou": 0.25,
        "overlap_iou": 0.5,
        "iou_grid": [0.25, 0.5, 0.75],
        "canonical_image_suffix": ".png",
        "no_finding_label": "No finding",
        "global_labels_excluded": ["No finding", "Pneumonia"],
        "bootstrap_seed": 5,
        "bootstrap_resamples": 20,
        "progress_every": 0,
        "change_froc_budget": 0.25,
        "prevalence_recall_points": 101,
        "change_endpoints": ["ap50", "froc_0.25", "primary_recall"],
        "confidence_level": 0.95,
    }


def contract():
    return {
        "candidate_score_floor": 0.01,
        "max_detections_per_image": 100,
        "matching_iou_threshold": 0.5,
        "class_ids": (1,),
    }


def decompose(ps, ts, other=None, **overrides):
    return error_decomposition(
        ps,
        ts,
        other or {},
        threshold=0.5,
        evaluation=contract() | overrides,
        analysis=settings(),
        strict_label="Lung Opacity",
    )


def target(boxes, key="a.png"):
    return ImageTarget(key, (100, 100), boxes, [1] * len(boxes))


def prediction(boxes, scores, key="a.png"):
    return ImagePrediction(key, (100, 100), boxes, [1] * len(boxes), scores)


def test_reference_precedence_reconciles_competition_threshold_partial_and_absence():
    ts = [
        target([[0, 0, 10, 10], [0, 1, 10, 11], [20, 0, 30, 10], [40, 0, 50, 10], [60, 0, 70, 10]])
    ]
    ps = [prediction([[0, 0, 10, 10], [20, 0, 30, 10], [40, 0, 43, 10]], [0.5, 0.2, 0.9])]
    result = decompose(ps, ts)
    assert {r["category"]: r["count"] for r in result["reference_errors"]} == {
        "matched": 1,
        "high_score_assignment": 1,
        "below_threshold": 1,
        "partial_localization": 1,
        "no_relevant_retained": 1,
    }
    canonical = evaluate_operating_point(ps, ts, class_ids=(1,), score_threshold=0.5)["overall"]
    historical = result["operating"][0]
    assert (historical["tp"], historical["fp"]) == (canonical["tp"], canonical["fp"])
    assert sum(r["count"] for r in result["reference_errors"]) == 5


@pytest.mark.parametrize(
    "width,expected",
    [
        (5, "matched"),
        (4.999, "partial_localization"),
        (2.5, "partial_localization"),
        (2.499, "no_relevant_retained"),
    ],
)
def test_exact_iou_boundaries(width, expected):
    result = decompose([prediction([[0, 0, width, 10]], [0.5])], [target([[0, 0, 10, 10]])])
    assert next(r["count"] for r in result["reference_errors"] if r["category"] == expected) == 1


def test_fp_precedence_and_overlapping_class_flags_do_not_inflate_counts():
    ts = [target([[0, 0, 10, 10]])]
    ps = [
        prediction(
            [[0, 0, 10, 10], [0, 0, 10, 10], [20, 0, 30, 10], [40, 0, 43, 10], [80, 0, 90, 10]],
            [0.9, 0.8, 0.7, 0.6, 0.5],
        )
    ]
    other = {
        "a.png": {
            "Consolidation": [[0, 0, 10, 10], [20, 0, 30, 10], [40, 0, 50, 10]],
            "ILD": [[20, 0, 30, 10], [21, 0, 31, 10]],
        }
    }
    result = decompose(ps, ts, other)
    for support in ("historical", "retained"):
        rows = [r for r in result["false_positives"] if r["support"] == support]
        assert [r["count"] for r in rows] == [1, 1, 1, 1]
        assert sum(r["count"] for r in rows) == 4
        flags = {
            r["class_name"]: r["count"]
            for r in result["non_target_overlaps"]
            if r["support"] == support
        }
        assert flags == {"Consolidation": 2, "ILD": 1}


def test_empty_runs_and_negative_images_are_retained_with_undefined_fp_fraction():
    ts = [target([[0, 0, 10, 10]]), target([], "b.png")]
    ps = [prediction([], []), prediction([], [], "b.png")]
    result = decompose(ps, ts)
    assert result["reference_errors"][-1]["count"] == 1
    assert all(r["fraction"] is None for r in result["false_positives"])
    assert result["operating"][0]["images"] == 2
    assert result["distributions"][1]["median"] is None
    assert decompose(ps[::-1], ts[::-1]) == result


def test_floor_cap_and_stable_score_ties():
    ts = [target([[0, 0, 10, 10]])]
    ps = [prediction([[0, 0, 10, 10]], [0.01])]
    assert decompose(ps, ts, max_detections_per_image=1)["operating"][1]["tp"] == 1
    with pytest.raises(ValueError, match="support"):
        decompose(ps, ts, candidate_score_floor=0.02)
    ps = [prediction([[0, 0, 10, 10]] * 2, [0.5, 0.5])]
    assert decompose(ps, ts)["operating"][0]["tp"] == 1
    with pytest.raises(ValueError, match="support"):
        decompose(ps, ts, max_detections_per_image=1)


def annotation_protocol():
    return {
        "ontology": {
            "source_exact_class_name": "Lung Opacity",
            "canonical_classes": {1: "Lung Opacity"},
        },
        "dataset": {
            "annotation_columns": ["image_id", "class_name", "x_min", "y_min", "x_max", "y_max"],
            "image_id_column": "image_id",
            "class_name_column": "class_name",
        },
    }


def source_row(label="Lung Opacity", key="a", box=(0, 0, 10, 10)):
    return dict(
        zip(
            ("image_id", "class_name", "x_min", "y_min", "x_max", "y_max"),
            (key, label, *map(str, box)),
            strict=True,
        )
    )


def test_source_suffix_sentinels_and_cross_class_duplicates_are_explicit():
    rows = [source_row(), source_row("Consolidation"), source_row("No finding", "b", ("",) * 4)]
    ts = [target([[0, 0, 10, 10]]), target([], "b.png")]
    mapping, audit = local_annotations(rows, ts, annotation_protocol(), settings())
    assert audit["cross_class_coincident_geometries"] == 1
    assert audit["no_finding_sentinel_images"] == 1
    assert "No finding" not in audit["local_box_counts"]
    assert mapping["a.png"]["Lung Opacity"] == [(0.0, 0.0, 10.0, 10.0)]


@pytest.mark.parametrize(
    "bad",
    [
        source_row(key="unknown"),
        source_row(box=(0, 0, 0, 10)),
        source_row(box=(0, 0, 101, 10)),
        source_row(box=(0, 0, "nan", 10)),
        source_row("Pneumonia"),
        source_row("No finding"),
    ],
)
def test_invalid_source_annotations_fail_closed(bad):
    with pytest.raises(ValueError):
        local_annotations([bad], [target([[0, 0, 10, 10]])], annotation_protocol(), settings())


def test_duplicate_conflicting_and_missing_annotations_fail():
    ts = [target([[0, 0, 10, 10]])]
    for rows in ([source_row()] * 2, [], [source_row(), source_row("No finding", box=("",) * 4)]):
        with pytest.raises(ValueError):
            local_annotations(rows, ts, annotation_protocol(), settings())


def evidence(seed=17, hit=True):
    ts = [target([[0, 0, 10, 10]]), target([], "b.png"), target([], "c.png")]
    ps = [
        prediction([[0, 0, 10, 10]] if hit else [[20, 0, 30, 10]], [0.5]),
        prediction([[0, 0, 10, 10]], [0.6], "b.png"),
        prediction([], [], "c.png"),
    ]
    ap = build_ap_cache(
        ps,
        ts,
        class_ids=(1,),
        minimum_score=0.01,
        max_dets=[1, 10, 100],
        iou_thresholds=[0.5],
        recall_points=101,
    )
    froc = build_froc_cache(ps, ts, class_ids=(1,), floor=0.01, iou=0.5, cap=100)
    return RunEvidence(seed, ap, froc, operating_counts(froc, 0.5)), ps, ts


def test_weighted_ap_has_independent_hand_calculated_answer_and_unit_coco_oracle():
    run, ps, ts = evidence()
    events = ap_events(run.ap)
    assert weighted_ap(events, run.ap.target_counts, np.ones(3), 101) == pytest.approx(
        evaluate_coco(ps, ts, class_ids=(1,), minimum_score=0.01)["ap50"]
    )
    # One earlier FP has mass 3; one later TP has mass 1, with full recall.
    assert weighted_ap(events, run.ap.target_counts, np.array([1, 3, 0]), 101) == 0.25
    assert weighted_ap(events, run.ap.target_counts, np.array([1, 0, 0]), 101) == 1
    assert np.isnan(weighted_ap(events, run.ap.target_counts, np.array([0, 1, 1]), 101))
    with pytest.raises(ValueError):
        weighted_ap(events, run.ap.target_counts, np.array([-1, 1, 1]), 101)


def test_prevalence_weights_change_mass_not_conditional_recall_and_cluster_multiplicity():
    run, _, _ = evidence()
    obs = np.array([3, 3, 1])
    weights = prevalence_weights(run.ap.target_counts, obs, 0.1)
    assert weights.sum() == pytest.approx(obs.sum())
    assert weights[0] / weights.sum() == pytest.approx(0.1)
    tp = (weights @ run.primary_counts)[0]
    assert tp / (weights @ run.ap.target_counts) == 1
    assert np.isnan(prevalence_weights(run.ap.target_counts, np.array([0, 2, 1]), 0.1)).all()
    assert np.isnan(prevalence_metrics(run, ap_events(run.ap), np.full(3, np.nan), 101)).all()


def domains():
    runs = tuple(evidence(seed, hit)[0] for seed, hit in ((17, True), (42, False)))
    domain = (runs, runs)
    clusters = build_patient_clusters(
        runs[0].ap.image_ids, {"a.png": "p", "b.png": "p", "c.png": "q"}
    )
    return domain, clusters


def test_shared_checkpoint_weights_cancel_identical_domains_and_independent_families(monkeypatch):
    domain, clusters = domains()
    seen = []

    def observations(rng, n, grouping):
        seen.append(grouping)
        return np.ones(n, dtype=int)

    monkeypatch.setattr(analysis_module, "draw_observations", observations)
    # Deliberately different family draws; both must still cancel across domains.
    monkeypatch.setattr(
        analysis_module,
        "draw_independent_run_bootstrap_multiplicities",
        lambda *a, **kw: (np.array([2, 0]), np.array([0, 2])),
    )
    arrays, _ = joint_bootstrap(domain, domain, clusters, settings(), "test", 1e-12)
    assert np.all(arrays["changes"] == 0)
    assert seen[::2] == [clusters] * settings()["bootstrap_resamples"]
    assert seen[1::2] == [None] * settings()["bootstrap_resamples"]
    assert np.all(arrays["prevalence"][:, 0, 0, 0] == 0.5)
    assert np.all(arrays["prevalence"][:, 0, 1, 0] == 0)


def test_determinism_undefined_draws_and_run_identity():
    domain, clusters = domains()
    first, points = joint_bootstrap(domain, domain, clusters, settings(), "test", 1e-12)
    assert json.loads(json.dumps(json_number(points), allow_nan=False)) == points
    second, _ = joint_bootstrap(domain, domain, clusters, settings(), "test", 1e-12)
    for name in first:
        np.testing.assert_equal(first[name], second[name])
    assert np.isnan(first["changes"]).any()
    rows, _ = intervals(points, first, {"analysis": settings()})
    assert all(r["a_valid"] + r["a_undefined"] == 20 for r in rows)
    assert any(r["a_undefined"] > 0 for r in rows)
    with pytest.raises(ValueError, match="Run identity"):
        joint_bootstrap(domain, (domain[0][::-1], domain[1]), clusters, settings(), "test", 1e-12)
    bad = replace(domain[0][0].ap, image_ids=("bad", "b.png", "c.png"))
    with pytest.raises(ValueError, match="observations"):
        joint_bootstrap(
            ((replace(domain[0][0], ap=bad), domain[0][1]), domain[1]),
            domain,
            clusters,
            settings(),
            "test",
            1e-12,
        )


def test_equal_run_summary_preserves_undefined_zero_output_run():
    rows = [{"detector": "a", "fraction": None}, {"detector": "a", "fraction": 0.6}]
    result = aggregate(rows, ["detector"], ["fraction"])[0]
    assert result["mean"] == 0.6 and result["defined_runs"] == 1 and result["attempted_runs"] == 2
