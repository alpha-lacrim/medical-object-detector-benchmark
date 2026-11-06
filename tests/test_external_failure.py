"""Synthetic intervention tests without restricted data or GPU execution."""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest
from pydantic import BaseModel, ConfigDict
from pydicom.dataset import Dataset

from src.analyze_external_failure import (
    image_counts,
    maximum_coverage,
    paired_summary,
    retained,
    same_predictions,
    select_indices,
)
from src.collect_external_failure import predict_arm, window_pixels
from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget


def prediction(boxes, scores, labels=None, name="synthetic"):
    return ImagePrediction(
        name,
        (20, 20),
        np.asarray(boxes).reshape(-1, 4),
        np.ones(len(scores), dtype=int) if labels is None else labels,
        scores,
    )


def target(boxes, name="synthetic"):
    return ImageTarget(
        name, (20, 20), np.asarray(boxes).reshape(-1, 4), np.ones(len(boxes), dtype=int)
    )


def dicom(polarity="MONOCHROME2"):
    ds = Dataset()
    ds.PhotometricInterpretation = polarity
    ds.PixelRepresentation = 0
    ds.BitsStored = 12
    ds.WindowCenter = 5
    ds.WindowWidth = 5
    return ds


WINDOW = {"index": 0, "missing": "identical_canonical_pixels", "output_max": 255}


def test_intervention_preserves_frozen_original_evaluation_settings():
    class Evaluation(BaseModel):
        model_config = ConfigDict(frozen=True)
        coco_minimum_score: float = 0.00001
        max_detections: int = 100

    class Phase(BaseModel):
        model_config = ConfigDict(frozen=True)
        evaluation: Evaluation

    original = Phase(evaluation=Evaluation())
    detector = SimpleNamespace(
        phase=original,
        run=SimpleNamespace(detector="faster_rcnn"),
        model=SimpleNamespace(roi_heads=SimpleNamespace()),
    )

    def native_predict(index, rgb):
        assert detector.phase.evaluation.max_detections == 300
        assert detector.phase.evaluation.coco_minimum_score == 0.000001
        assert detector.model.roi_heads.detections_per_img == 300
        return {
            "boxes": np.empty((0, 4)),
            "labels": np.array([], dtype=int),
            "scores": np.array([]),
        }

    detector.predict = native_predict
    predict_arm(
        detector,
        0,
        target([]),
        {"floor": 0.000001, "cap": 300, "image": "canonical"},
        object(),
        object(),
    )
    assert original.evaluation.max_detections == 100
    assert original.evaluation.coco_minimum_score == 0.00001


def test_window_has_fixed_display_scale_and_correct_polarity():
    pixels = np.array([[2, 3, 4, 5, 6, 7]], dtype=np.uint16)
    # DICOM LINEAR: low boundary 2.5, high boundary 6.5, not sample min/max.
    expected = np.rint(np.array([[0, 0.125, 0.375, 0.625, 0.875, 1]]) * 255).astype(np.uint8)
    assert np.array_equal(window_pixels(dicom(), pixels, WINDOW), expected)
    assert np.array_equal(window_pixels(dicom("MONOCHROME1"), pixels, WINDOW), 255 - expected)
    narrow = np.array([[4, 5]], dtype=np.uint16)
    assert np.array_equal(window_pixels(dicom(), narrow, WINDOW), expected[:, 2:4])


def test_window_width_one_is_a_threshold():
    ds = dicom()
    ds.WindowWidth = 1
    assert window_pixels(ds, np.array([[4, 5]], dtype=np.uint16), WINDOW).tolist() == [[0, 255]]


def test_missing_window_reuses_exact_canonical_transform():
    ds = dicom("MONOCHROME1")
    del ds.WindowCenter
    del ds.WindowWidth
    pixels = np.array([[2, 4, 6], [2, 4, 6]], dtype=np.uint16)
    assert window_pixels(ds, pixels, WINDOW).tolist() == [[255, 128, 0], [255, 128, 0]]


@pytest.mark.parametrize(
    "field,value", [("RescaleSlope", 2), ("PixelRepresentation", 1), ("VOILUTFunction", "SIGMOID")]
)
def test_window_rejects_semantics_outside_protocol(field, value):
    ds = dicom()
    setattr(ds, field, value)
    with pytest.raises(ValueError):
        window_pixels(ds, np.array([[1, 2]], dtype=np.uint16), WINDOW)


def test_incomplete_window_is_not_silently_ignored():
    ds = dicom()
    del ds.WindowWidth
    with pytest.raises(ValueError, match="Incomplete"):
        window_pixels(ds, np.array([[1, 2]], dtype=np.uint16), WINDOW)


def test_selection_keeps_every_positive_and_ignores_input_order_for_negative_choices():
    ts = [target([[0, 0, 2, 2]], "a"), target([], "b"), target([], "c"), target([], "d")]
    settings = {"positive_images": "all_strict_target_positive", "negative_images": 2, "seed": 123}
    names = {ts[i].image_id for i in select_indices(ts, settings)}
    reversed_ts = list(reversed(ts))
    assert names == {reversed_ts[i].image_id for i in select_indices(reversed_ts, settings)}
    assert "a" in names and len(names) == 3
    with pytest.raises(ValueError):
        select_indices(ts, {**settings, "negative_images": 4})


def test_native_filter_is_strict_and_cap_keeps_stable_ties():
    p = prediction([[0, 0, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3]], [0.1, 0.2, 0.2])
    filtered = retained(p, 0.1, 1)
    assert filtered.boxes_xyxy.tolist() == [[1, 1, 2, 2]]
    assert len(retained(p, 0.2, 5).scores) == 0
    assert not same_predictions(p, filtered)
    assert same_predictions(p, p)


def test_maximum_coverage_is_one_to_one_and_handles_assignment_competition():
    t = target([[0, 0, 10, 10], [5, 0, 15, 10]])
    one = prediction([[0, 0, 15, 10]], [0.1])
    assert maximum_coverage(one, t, 0.5) == 1  # one candidate cannot cover two lesions
    p = prediction([[0, 0, 15, 10], [0, 0, 10, 10]], [0.9, 0.1])
    assert maximum_coverage(p, t, 0.5) == 2
    assert image_counts(p, t, 0.05, 100, [0.5], 0.5).tolist() == [1, 0, 2]
    assert maximum_coverage(prediction([], []), t, 0.5) == 0
    assert maximum_coverage(prediction([[0, 0, 10, 10]], [0.9], [2]), t, 0.5) == 0


def test_negative_control_counts_only_negative_image_false_positives():
    p = prediction([[0, 0, 3, 3]], [0.8])
    assert image_counts(p, target([]), 0.5, 100, [0.25, 0.5], 0.5).tolist() == [0, 1, 0, 0]
    assert image_counts(p, target([[10, 10, 15, 15]]), 0.5, 100, [0.25, 0.5], 0.5).tolist() == [
        0,
        0,
        0,
        0,
    ]


def test_paired_bootstrap_preserves_zero_changes_and_factorial_identity():
    arms = ["baseline", "lower_floor", "higher_cap", "expanded", "dicom_window"]
    counts = np.zeros((5, 2, 3, 4), dtype=int)
    counts[:, :, 0] = [1, 0, 1, 1]
    counts[:, :, 1] = [0, 0, 1, 0]
    counts[:, :, 2] = [0, 2, 0, 0]
    settings = {
        "support_ious": [0.25, 0.5],
        "bootstrap_seed": 123,
        "bootstrap_resamples": 100,
        "confidence_level": 0.95,
    }
    rows, runs, draws = paired_summary(
        counts, np.array([1, 1, 0]), settings, arms, "example", [17, 42]
    )
    assert all(row["delta"] == row["ci_lower"] == row["ci_upper"] == 0 for row in rows)
    assert runs[0]["historical_recall"] == 0.5
    assert runs[0]["negative_control_fp_per_image"] == 2
    again = paired_summary(counts, np.array([1, 1, 0]), settings, arms, "example", [17, 42])[2]
    assert np.array_equal(draws, again)


def test_bootstrap_preserves_a_known_constant_paired_intervention():
    arms = ["baseline", "lower_floor", "higher_cap", "expanded", "dicom_window"]
    counts = np.zeros((5, 2, 2, 4), dtype=int)
    counts[4, :, 0, 0] = 1
    settings = {
        "support_ious": [0.25, 0.5],
        "bootstrap_seed": 123,
        "bootstrap_resamples": 100,
        "confidence_level": 0.95,
    }
    rows, _, _ = paired_summary(counts, np.array([1, 0]), settings, arms, "example", [17, 42])
    row = next(
        r for r in rows if r["arm"] == "dicom_window" and r["endpoint"] == "historical_recall"
    )
    assert row["delta"] == row["ci_lower"] == row["ci_upper"] == 1
