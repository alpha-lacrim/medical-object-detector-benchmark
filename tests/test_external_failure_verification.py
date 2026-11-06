"""Reject altered diagnostic evidence without reading restricted clinical data."""

from copy import deepcopy

import pytest

from scripts.verify_external_failure import verify_arms
from src.analyze_external_failure import retained
from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget


def evidence():
    """A capped baseline, tied scores, low-score candidates and an empty image."""
    targets = [ImageTarget("a", (10, 10), [[0, 0, 2, 2]], [1]), ImageTarget("b", (10, 10), [], [])]
    expanded = [
        ImagePrediction(
            "a", (10, 10), [[0, 0, 2, 2], [3, 3, 5, 5], [6, 6, 8, 8]], [1, 1, 1], [0.8, 0.8, 0.1]
        ),
        ImagePrediction("b", (10, 10), [], [], []),
    ]
    settings = {
        "baseline": {"floor": 0.2, "cap": 1},
        "lower_floor": {"floor": 0.05, "cap": 1},
        "higher_cap": {"floor": 0.2, "cap": 3},
        "expanded": {"floor": 0.05, "cap": 3},
        "dicom_window": {"floor": 0.2, "cap": 1},
    }
    arms = {
        name: [retained(p, s["floor"], s["cap"]) for p in expanded] for name, s in settings.items()
    }
    original = {p.image_id: deepcopy(p) for p in arms["baseline"]}
    return arms, targets, original, settings


def test_complete_evidence_replays_including_empty_predictions():
    assert verify_arms(*evidence(), {1}) == 2


@pytest.mark.parametrize("change", ["missing", "order", "score", "floor", "class", "nested"])
def test_diagnostic_verifier_rejects_semantic_tampering(change):
    arms, targets, original, settings = evidence()
    arms = deepcopy(arms)
    if change == "missing":
        arms.pop("dicom_window")
    elif change == "order":
        arms["dicom_window"].reverse()
    elif change == "score":
        original["a"].scores[0] = 0.7
    elif change == "floor":
        arms["expanded"][0].scores[-1] = settings["expanded"]["floor"]
    elif change == "class":
        arms["dicom_window"][0].labels[0] = 2
    elif change == "nested":
        arms["higher_cap"][0].boxes_xyxy[0] = [1, 1, 3, 3]
    with pytest.raises(ValueError):
        verify_arms(arms, targets, original, settings, {1})
