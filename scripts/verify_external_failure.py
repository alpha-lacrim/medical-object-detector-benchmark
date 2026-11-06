"""Independently replay diagnostic membership, native support and baseline identities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.analyze_external_failure import retained, same_predictions, select_indices
from src.evaluate_vindr_external import deserialize, read_gzip
from src.stats.run_external_generalization import preflight
from src.stats.run_vindr_statistics import read_json, read_yaml, require, verify_artifact


def verify_arms(arms: dict, targets: list, original: dict, settings: dict, class_ids: set) -> int:
    """Recheck actual saved arrays rather than trusting collection success flags."""
    require(set(arms) == set(settings), "Diagnostic arm inventory differs")
    for name, predictions in arms.items():
        require(len(predictions) == len(targets), "Diagnostic arm is incomplete")
        for prediction, target in zip(predictions, targets, strict=True):
            require(
                prediction.image_id == target.image_id
                and prediction.image_size == target.image_size,
                "Diagnostic observation identity or order differs",
            )
            require(set(prediction.labels).issubset(class_ids), "Diagnostic class differs")
            require(
                len(prediction.scores) <= settings[name]["cap"]
                and np.all(prediction.scores > settings[name]["floor"])
                and np.all(np.diff(prediction.scores) <= 0),
                "Diagnostic native support differs",
            )
    for index, target in enumerate(targets):
        require(
            same_predictions(arms["baseline"][index], original[target.image_id]),
            "Historical baseline prediction replay differs",
        )
        for name in ("baseline", "lower_floor", "higher_cap"):
            expected = retained(
                arms["expanded"][index], settings[name]["floor"], settings[name]["cap"]
            )
            require(same_predictions(arms[name][index], expected), "Nested retention differs")
    return len(targets)


def verify(config_path: Path) -> dict:
    """Read-only verification; no model loading, inference or scientific artifact writes."""
    config = read_yaml(config_path)
    private = Path(config["outputs"]["private_root"])
    receipt = read_json(private / "collection.json")
    require(receipt["status"] == "complete", "Diagnostic collection is incomplete")
    for item in receipt["inputs"]:
        verify_artifact(item)
    prepared = read_json(private / "prepared.json")
    # Pixel provenance is nested in the private receipt, not exposed in public output.
    for record in prepared["images"]:
        for field in ("source", "canonical", "window"):
            verify_artifact(record[field])
    gate = preflight(Path(config["baseline_analysis_config"]))
    protocol = gate["baseline"]["protocol"]
    targets = [gate["targets"][i] for i in select_indices(gate["targets"], config["selection"])]
    require(prepared["image_ids"] == [t.image_id for t in targets], "Diagnostic cohort differs")
    expected = {
        (detector, seed)
        for detector in protocol["models"]["detectors"]
        for seed in protocol["models"]["seeds"]
    }
    actual = [(r["detector"], r["seed"]) for r in receipt["runs"]]
    require(len(actual) == len(expected) and set(actual) == expected, "Run inventory differs")
    image_runs = 0
    for run in receipt["runs"]:
        verify_artifact(run["artifact"])
        bundle = read_gzip(Path(run["artifact"]["path"]))
        key = (run["detector"], run["seed"])
        require((bundle["detector"], bundle["seed"]) == key, "Bundle identity differs")
        source = next(
            r
            for r in gate["baseline"]["external"]["runs"]
            if (r["metadata"]["detector"], r["metadata"]["seed"]) == key
        )
        original = {
            p.image_id: p
            for p in deserialize(read_gzip(Path(source["artifacts"][0]["path"]))["predictions"])
        }
        arms = {name: deserialize(values) for name, values in bundle["arms"].items()}
        image_runs += verify_arms(
            arms, targets, original, config["arms"], set(protocol["ontology"]["canonical_classes"])
        )
    return {
        "status": "verified",
        "runs": len(actual),
        "images": len(targets),
        "image_run_baseline_replays": image_runs,
        "nested_retention_replays": 3 * image_runs,
        "pixel_artifact_hashes": 3 * len(prepared["images"]),
        "new_inference": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    print(json.dumps(verify(parser.parse_args().config), indent=2))
