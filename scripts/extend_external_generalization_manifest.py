"""Register reviewed post-hoc aggregates without replacing existing scientific evidence."""

from __future__ import annotations

import argparse
import csv
import inspect
import json
from pathlib import Path

from PIL import Image

from src.stats import run_external_generalization as analysis
from src.stats.run_vindr_statistics import artifact, read_json, read_yaml, verify_artifact


def binding(entry: dict) -> dict:
    """Preserve exact hashes and explicitly distinguish private external prerequisites."""
    verify_artifact(entry)
    return {
        "path": entry["path"],
        "sha256": entry["sha256"],
        "availability": "external_or_ignored"
        if entry["path"].startswith(("data/processed/", "data/raw/", "results/checkpoints/"))
        else "committed",
    }


def extend(config_path: Path, manifest_path: Path) -> int:
    """Add one version exactly once; retain every prior record byte-for-value."""
    analysis.verify(config_path)
    config = read_yaml(config_path)
    root = Path(config["outputs"]["public_root"])
    summary_path = root / config["outputs"]["summary"]
    summary = read_json(summary_path)
    manifest = read_json(manifest_path)
    previous = {entry["path"] for entry in manifest["artifacts"]}
    paths = [summary_path] + [
        Path(e["path"]) for e in summary["artifacts"] if Path(e["path"]).is_relative_to(root)
    ]
    if len(set(paths)) != len(paths) or any(p.as_posix() in previous for p in paths):
        raise ValueError("Analysis already registered or duplicate outputs; do not refresh hashes")
    source = Path(inspect.getfile(analysis)).resolve().relative_to(Path.cwd()).as_posix()
    inputs = [binding(e) for e in summary["inputs"] + summary["artifacts"]]
    for path in paths:
        if path.suffix == ".csv":
            with path.open(encoding="utf-8", newline="") as stream:
                reader = csv.DictReader(stream)
                rows = list(reader)
                columns = reader.fieldnames
            schema = {
                "type": "csv",
                "required_columns": columns,
                "exact_columns": columns,
                "row_count": len(rows),
            }
        elif path.suffix == ".png":
            with Image.open(path) as image:
                schema = {"type": "png", "width": image.width, "height": image.height}
        else:
            schema = {
                "type": "json",
                "top_level_type": "object",
                "required_keys": list(read_json(path)),
            }
        manifest["artifacts"].append(
            {
                "path": path.as_posix(),
                "sha256": artifact(path)["sha256"],
                "generating_script": source,
                "generating_script_sha256": artifact(source)["sha256"],
                "config": {
                    "path": config_path.as_posix(),
                    "sha256": artifact(config_path)["sha256"],
                },
                "input_artifacts": inputs
                if path == summary_path
                else [binding(artifact(summary_path))],
                "expected_schema": schema,
                "study_phase": "Post-hoc external generalization v1",
                "reproduction_tier": "authorized_data_replay",
                "gpu_required": False,
                "training_required": False,
                "referenced_results": [],
            }
        )
    manifest["manuscript_critical_paths"] = [e["path"] for e in manifest["artifacts"]]
    manifest["publication_extension"]["posthoc_external_generalization"] = {
        "analysis_id": config["analysis_id"],
        "maintenance_script": Path(__file__).resolve().relative_to(Path.cwd()).as_posix(),
        "note": "All previous entries unchanged; exploratory evidence does not replace v1.",
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    return len(paths)


def main() -> None:
    """Require explicit config/destination; this maintenance command is never run by CI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    print(f"Added {extend(args.config, args.manifest)} post-hoc aggregate records")


if __name__ == "__main__":
    main()
