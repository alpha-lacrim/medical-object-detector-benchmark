"""Bounded paired GPU experiments for the post-hoc external-failure diagnostic."""

from __future__ import annotations

import argparse
import gc
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pydicom
from PIL import Image
from pydicom.pixels import apply_modality_lut, apply_windowing

from scripts.verify_frozen_external import historical_editorial_view
from src.analyze_external_failure import retained, same_predictions, select_indices
from src.analyze_yolo_numerical_path import inference_only
from src.benchmark_inference import Predictor
from src.data.prepare import scale_radiograph_to_uint8
from src.data.prepare_vindr import ensure_private, resolve_root
from src.evaluate import _serialize_prediction
from src.evaluate_vindr_external import deserialize, dump_gzip, read_gzip, restore_native_bounds
from src.evaluate_vindr_external import preflight as inference_preflight
from src.meddet_benchmark.evaluation import ImagePrediction
from src.meddet_benchmark.reproducibility import configure_reproducibility
from src.stats.run_external_generalization import preflight as baseline_preflight
from src.stats.run_vindr_statistics import (
    artifact,
    read_json,
    read_yaml,
    require,
    verify_artifact,
    write_json,
)


def window_pixels(dataset: pydicom.Dataset, pixels: np.ndarray, settings: dict) -> np.ndarray:
    """DICOM LINEAR window followed by display-range scaling and polarity handling."""
    require(
        dataset.PhotometricInterpretation in {"MONOCHROME1", "MONOCHROME2"},
        "Unsupported photometric interpretation",
    )
    require(int(dataset.PixelRepresentation) == 0, "Unsigned storage required")
    require(
        float(getattr(dataset, "RescaleSlope", 1)) == 1
        and float(getattr(dataset, "RescaleIntercept", 0)) == 0,
        "Unexpected rescale",
    )
    require(
        not hasattr(dataset, "ModalityLUTSequence") and not hasattr(dataset, "VOILUTSequence"),
        "LUT sequence needs a separate protocol",
    )
    require(getattr(dataset, "VOILUTFunction", "LINEAR") == "LINEAR", "Unsupported VOI function")
    present = [hasattr(dataset, key) for key in ("WindowCenter", "WindowWidth")]
    require(present[0] == present[1], "Incomplete window pair")
    if not all(present):
        require(
            settings["missing"] == "identical_canonical_pixels", "Missing-window policy differs"
        )
        return scale_radiograph_to_uint8(
            pixels,
            photometric_interpretation=dataset.PhotometricInterpretation,
            invert_monochrome1=True,
        )
    displayed = apply_windowing(
        apply_modality_lut(pixels, dataset), dataset, index=settings["index"]
    ) / (2 ** int(dataset.BitsStored) - 1)
    if dataset.PhotometricInterpretation == "MONOCHROME1":
        displayed = 1 - displayed
    return np.clip(np.rint(displayed * settings["output_max"]), 0, settings["output_max"]).astype(
        np.uint8
    )


def prepare(config_path: Path) -> dict:
    """Verify historical evidence and create private, immutable diagnostic inputs."""
    config = read_yaml(config_path)
    gate = baseline_preflight(Path(config["baseline_analysis_config"]))
    protocol = gate["baseline"]["protocol"]
    private = Path(config["outputs"]["private_root"])
    ensure_private(private / "prepared.json", Path(protocol["outputs"]["private_root"]))
    require(not private.exists(), "Diagnostic inputs exist; never overwrite")
    require(
        list(config["arms"])
        == ["baseline", "lower_floor", "higher_cap", "expanded", "dicom_window"],
        "Unexpected intervention arms",
    )
    evaluation = protocol["evaluation"]
    base = config["arms"]["baseline"]
    require(
        base["floor"] == evaluation["candidate_score_floor"]
        and base["cap"] == evaluation["max_detections_per_image"],
        "Baseline contract differs",
    )
    inputs = [
        *gate["inputs"],
        *[
            artifact(p)
            for p in [
                config_path,
                config["protocol"],
                config["private_audit"],
                *config["source_files"],
            ]
        ],
    ]
    targets = gate["targets"]
    selected = select_indices(targets, config["selection"])
    audit = read_json(config["private_audit"])
    records = {r["file_name"]: r for r in audit["records"]}
    adapter = read_yaml(config["adapter_config"])
    canonical_root = Path(protocol["outputs"]["private_root"]) / adapter["images_directory_name"]
    raw_root = resolve_root(protocol) / protocol["dataset"]["paths"]["images"]
    private.mkdir(parents=True)
    window_root = private / "window_images"
    window_root.mkdir()
    image_records = []
    for i in selected:
        target = targets[i]
        raw = raw_root / (Path(target.image_id).stem + protocol["dataset"]["extension"])
        png = canonical_root / target.image_id
        raw_receipt, png_receipt = artifact(raw), artifact(png)
        require(
            raw_receipt["sha256"] == records[target.image_id]["source_sha256"]
            and png_receipt["sha256"] == records[target.image_id]["png_sha256"],
            "Image hash differs",
        )
        ds = pydicom.dcmread(raw)
        pixels = ds.pixel_array
        canonical = scale_radiograph_to_uint8(
            pixels, photometric_interpretation=ds.PhotometricInterpretation, invert_monochrome1=True
        )
        with Image.open(png) as source:
            require(np.array_equal(np.asarray(source), canonical), "Canonical pixel replay differs")
        windowed = window_pixels(ds, pixels, config["window"])
        require(windowed.shape == canonical.shape == target.image_size, "Native dimensions differ")
        path = window_root / target.image_id
        Image.fromarray(windowed).save(path, compress_level=adapter["png_compress_level"])
        with Image.open(path) as image:
            require(np.array_equal(np.asarray(image), windowed), "Window PNG round-trip differs")
        image_records.append(
            {
                "image_id": target.image_id,
                "source": raw_receipt,
                "canonical": png_receipt,
                "window": artifact(path),
                "window_present": hasattr(ds, "WindowCenter"),
                "monochrome1": ds.PhotometricInterpretation == "MONOCHROME1",
                "changed_fraction": float(np.mean(canonical != windowed)),
                "mean_absolute_pixel_change": float(
                    np.abs(canonical.astype(float) - windowed).mean()
                ),
            }
        )
    prepared = {
        "inputs": inputs,
        "image_ids": [targets[i].image_id for i in selected],
        "images": image_records,
        "cohort": {
            "images": len(selected),
            "positive_images": sum(bool(len(targets[i].labels)) for i in selected),
            "negative_images": config["selection"]["negative_images"],
            "target_boxes": sum(len(targets[i].labels) for i in selected),
        },
        "aggregate_pixel_audit": {
            "canonical_pixel_exact_replays": len(selected),
            "window_present": sum(r["window_present"] for r in image_records),
            "monochrome1": sum(r["monochrome1"] for r in image_records),
            "mean_changed_fraction": float(np.mean([r["changed_fraction"] for r in image_records])),
            "mean_absolute_pixel_change": float(
                np.mean([r["mean_absolute_pixel_change"] for r in image_records])
            ),
        },
    }
    for entry in inputs:
        verify_artifact(entry)
    write_json(private / "prepared.json", prepared)
    return {"status": "prepared", **prepared["cohort"], **prepared["aggregate_pixel_audit"]}


class WindowDataset:
    """Keep the original loader's metadata with a new, native-resolution PNG source."""

    def __init__(self, original: object, root: Path) -> None:
        self.original, self.root = original, root

    def __getattr__(self, name: str) -> object:
        return getattr(self.original, name)

    def image_path(self, index: int) -> Path:
        return self.root / self.original.records[index].file_name

    def __getitem__(self, index: int) -> tuple:
        import torch

        with Image.open(self.image_path(index)) as image:
            pixels = np.array(image.convert("RGB"), dtype=np.float32) / np.float32(255)
        return torch.from_numpy(np.ascontiguousarray(pixels.transpose(2, 0, 1))), None


def predict_arm(
    predictor: Predictor,
    index: int,
    target: object,
    arm: dict,
    original: object,
    windowed: WindowDataset,
) -> ImagePrediction:
    """Change only the explicitly named input and postprocessing controls."""
    evaluation = predictor.phase.evaluation.model_copy(
        update={"coco_minimum_score": arm["floor"], "max_detections": arm["cap"]}
    )
    predictor.phase = predictor.phase.model_copy(update={"evaluation": evaluation})
    predictor.dataset = windowed if arm["image"] == "dicom_window" else original
    if predictor.run.detector == "faster_rcnn":
        predictor.model.roi_heads.score_thresh = arm["floor"]
        predictor.model.roi_heads.detections_per_img = arm["cap"]
    values = predictor.predict(index, None)
    boxes, _ = restore_native_bounds(values["boxes"], target.image_size, predictor.run.detector)
    return ImagePrediction(
        target.image_id, target.image_size, boxes, values["labels"], values["scores"]
    )


def collect(config_path: Path) -> dict:
    """Replay baseline, collect three forward arms and validate the factorial."""
    import torch

    config = read_yaml(config_path)
    private = Path(config["outputs"]["private_root"])
    prepared = read_json(private / "prepared.json")
    for entry in prepared["inputs"]:
        verify_artifact(entry)
    for record in prepared["images"]:
        for field in ("source", "canonical", "window"):
            verify_artifact(record[field])
    require(not (private / "collection.json").exists(), "Collection exists; never overwrite")
    with historical_editorial_view(Path.cwd()):
        protocol, _, phase, models, dataset, _ = inference_preflight(
            Path(config["external_config"]), Path(config["operation_config"])
        )
    require(torch.cuda.is_available(), "CUDA is unavailable")
    require(torch.cuda.get_device_name(0) == config["runtime"]["required_gpu_name"], "Wrong GPU")
    for package, expected in protocol["runtime"]["versions"].items():
        actual = torch.version.cuda if package == "cuda" else version(package)
        require(actual == expected, f"Pinned package differs: {package}")
    from src.stats.run_statistics import load_coco_targets

    all_targets, _ = load_coco_targets(Path(protocol["outputs"]["local_annotations"]))
    indices = select_indices(all_targets, config["selection"])
    require(prepared["image_ids"] == [all_targets[i].image_id for i in indices], "Cohort differs")
    external = read_json(
        read_yaml(read_yaml(config["baseline_analysis_config"])["statistics_config"])[
            "external_summary"
        ]
    )
    windows = WindowDataset(dataset, private / "window_images")
    settings = protocol["runtime"]
    torch.set_num_threads(settings["torch_threads"])
    receipt = {
        "status": "running",
        "inputs": [*prepared["inputs"], artifact(private / "prepared.json")],
        "environment": {
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "gpu": torch.cuda.get_device_name(0),
            "cudnn": torch.backends.cudnn.version(),
        },
        "runs": [],
    }
    write_json(private / "collection.json", receipt)
    start = time.perf_counter()
    with inference_only():
        for spec in phase.runs:
            configure_reproducibility(
                spec.seed,
                deterministic=settings["deterministic"],
                allow_tf32=settings["allow_tf32"],
            )
            source = next(
                r
                for r in external["runs"]
                if r["metadata"]["detector"] == spec.detector and r["metadata"]["seed"] == spec.seed
            )
            saved = {
                p.image_id: p
                for p in deserialize(read_gzip(Path(source["artifacts"][0]["path"]))["predictions"])
            }
            predictor = Predictor(
                spec, phase.model_copy(deep=True), models[(spec.detector, spec.seed)], dataset
            )
            if spec.detector == "faster_rcnn":
                predictor.model.roi_heads.score_thresh = config["arms"]["baseline"]["floor"]
            predictor.predict(indices[0], None)
            dtype = predictor.verify_amp(indices[0])
            require(dtype == "torch." + settings["amp_dtype"][spec.detector], "AMP dtype differs")
            require(
                torch.are_deterministic_algorithms_enabled()
                and not torch.backends.cudnn.benchmark
                and not torch.backends.cuda.matmul.allow_tf32
                and not torch.backends.cudnn.allow_tf32,
                "Numerical runtime controls differ",
            )
            torch.cuda.reset_peak_memory_stats()
            arms = {name: [] for name in config["arms"]}
            probe_start = time.perf_counter()
            for position, index in enumerate(indices):
                target = all_targets[index]
                baseline = predict_arm(
                    predictor, index, target, config["arms"]["baseline"], dataset, windows
                )
                require(
                    same_predictions(baseline, saved[target.image_id]),
                    "Exact baseline replay differs",
                )
                expanded = predict_arm(
                    predictor, index, target, config["arms"]["expanded"], dataset, windows
                )
                nested = retained(
                    expanded, config["arms"]["baseline"]["floor"], config["arms"]["baseline"]["cap"]
                )
                require(same_predictions(nested, baseline), "Retention is not exactly nested")
                window = predict_arm(
                    predictor, index, target, config["arms"]["dicom_window"], dataset, windows
                )
                for name, prediction in [
                    ("baseline", baseline),
                    ("expanded", expanded),
                    ("dicom_window", window),
                ]:
                    arms[name].append(_serialize_prediction(prediction))
                for name in ("lower_floor", "higher_cap"):
                    arm = config["arms"][name]
                    arms[name].append(
                        _serialize_prediction(retained(expanded, arm["floor"], arm["cap"]))
                    )
                if position + 1 == config["runtime"]["probe_images"]:
                    projected = (
                        (time.perf_counter() - probe_start)
                        / (position + 1)
                        * len(indices)
                        * len(phase.runs)
                    )
                    require(
                        projected < config["runtime"]["max_seconds"],
                        "Projected diagnostic exceeds time budget",
                    )
                    print(
                        f"Probe {spec.detector} seed {spec.seed}: "
                        f"projected all-run seconds {projected:.0f}",
                        flush=True,
                    )
                require(
                    torch.cuda.max_memory_reserved() / 2**30
                    < config["runtime"]["max_reserved_memory_gib"],
                    "Reserved CUDA memory exceeds diagnostic budget",
                )
                require(
                    time.perf_counter() - start < config["runtime"]["max_seconds"],
                    "Diagnostic time budget exceeded",
                )
                if (position + 1) % config["runtime"]["progress_every"] == 0:
                    print(
                        f"{spec.detector} seed {spec.seed}: "
                        f"{position + 1}/{len(indices)} paired images",
                        flush=True,
                    )
            bundle = private / f"{spec.detector}_{spec.seed}.json.gz"
            dump_gzip(bundle, {"detector": spec.detector, "seed": spec.seed, "arms": arms})
            receipt["runs"].append(
                {
                    "detector": spec.detector,
                    "seed": spec.seed,
                    "artifact": artifact(bundle),
                    "activation_dtype": dtype,
                    "elapsed_seconds": time.perf_counter() - probe_start,
                    "peak_reserved_bytes": torch.cuda.max_memory_reserved(),
                    "baseline_exact_replay": True,
                    "nested_retention_exact_replay": True,
                }
            )
            write_json(private / "collection.json", receipt)
            del predictor, saved, arms
            gc.collect()
            torch.cuda.empty_cache()
    for entry in receipt["inputs"]:
        verify_artifact(entry)
    receipt["status"] = "complete"
    receipt["elapsed_seconds"] = time.perf_counter() - start
    write_json(private / "collection.json", receipt)
    return {
        "status": "complete",
        "runs": len(receipt["runs"]),
        "seconds": receipt["elapsed_seconds"],
    }


def main() -> None:
    """Keep preparation and GPU collection explicit and independently executable."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--mode", choices=["prepare", "collect"], required=True)
    args = parser.parse_args()
    print((prepare if args.mode == "prepare" else collect)(args.config))


if __name__ == "__main__":
    main()
