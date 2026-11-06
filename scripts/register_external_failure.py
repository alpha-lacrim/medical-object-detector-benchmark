"""Append verified diagnostic aggregates to the publication inventory exactly once."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image

from scripts.extend_external_generalization_manifest import binding
from src.stats.run_vindr_statistics import artifact, read_json, read_yaml, require, verify_artifact


def register(config_path: Path, manifest_path: Path) -> int:
    """Preserve every old record and reject repeats or changed collection/report inputs."""
    config = read_yaml(config_path)
    root = Path(config["outputs"]["public_root"])
    summary_path, build_path = root / "summary.json", root / "report_build.json"
    summary, build = read_json(summary_path), read_json(build_path)
    require(summary["status"] == "complete_exploratory_diagnostic", "Incomplete diagnostic")
    for item in [*summary["inputs"], *summary["artifacts"], *build["inputs"], *build["outputs"]]:
        verify_artifact(item)
    paths = [
        summary_path,
        *[Path(r["path"]) for r in summary["artifacts"] if Path(r["path"]).is_relative_to(root)],
        *[Path(r["path"]) for r in build["outputs"] if Path(r["path"]).suffix == ".png"],
        build_path,
    ]
    manifest = read_json(manifest_path)
    previous = {item["path"] for item in manifest["artifacts"]}
    require(
        len(set(paths)) == len(paths) and not previous.intersection(p.as_posix() for p in paths),
        "Diagnostic already registered or duplicate paths; do not refresh hashes",
    )
    for path in paths:
        report_artifact = path.suffix == ".png" or path == build_path
        source = Path(
            "scripts/report_external_failure.py"
            if report_artifact
            else "src/analyze_external_failure.py"
        )
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
        dependencies = (
            summary["inputs"] + summary["artifacts"]
            if path == summary_path
            else [artifact(summary_path)]
        )
        if report_artifact:
            dependencies += build["inputs"] + build["outputs"]
        manifest["artifacts"].append(
            {
                "path": path.as_posix(),
                "sha256": artifact(path)["sha256"],
                "generating_script": source.as_posix(),
                "generating_script_sha256": artifact(source)["sha256"],
                "config": {
                    "path": config_path.as_posix(),
                    "sha256": artifact(config_path)["sha256"],
                },
                "input_artifacts": [binding(item) for item in dependencies],
                "expected_schema": schema,
                "study_phase": "Post-hoc controlled external failure diagnostic v1",
                "reproduction_tier": "authorized_data_replay",
                "gpu_required": False,
                "training_required": False,
                "referenced_results": [],
            }
        )
    manifest["manuscript_critical_paths"] = [r["path"] for r in manifest["artifacts"]]
    manifest["publication_extension"]["external_failure_isolation"] = {
        "analysis_id": config["analysis_id"],
        "maintenance_script": Path(__file__).resolve().relative_to(Path.cwd()).as_posix(),
        "note": "CPU analysis replay requires private collected bundles; "
        "initial paired collection requires GPU. All prior entries unchanged.",
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    return len(paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    print(f"Registered {register(args.config, args.manifest)} diagnostic artifacts")
