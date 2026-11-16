"""Append verified annotation-audit artifacts without refreshing prior bindings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from scripts.extend_external_generalization_manifest import binding
from src.stats.run_threshold_repairability import read_csv
from src.stats.run_vindr_statistics import (
    artifact,
    read_json,
    read_yaml,
    require,
    verify_artifact,
)


def register(config_path: Path, manifest_path: Path) -> int:
    """Register once, preserving every original publication record."""
    config = read_yaml(config_path)
    root = Path(config["output_root"])
    summary_path = Path(config["analysis_summary"])
    report_path = root / config["receipt"]
    summary, report = read_json(summary_path), read_json(report_path)
    require(summary["status"] == "completed_exploratory", "Incomplete analysis")
    for record in (summary, report):
        for item in record["inputs"] + record["artifacts"]:
            verify_artifact(item)
    paths = [summary_path, report_path] + [
        Path(e["path"])
        for record in (summary, report)
        for e in record["artifacts"]
        if Path(e["path"]).is_relative_to(root)
    ]
    manifest = read_json(manifest_path)
    previous = list(manifest["artifacts"])
    existing = {e["path"] for e in previous}
    require(len(set(paths)) == len(paths), "Duplicate output")
    require(not existing.intersection(p.as_posix() for p in paths), "Already registered")
    for path in paths:
        is_report = path.suffix == ".png" or path == report_path
        source = (
            "scripts/report_froc_annotation.py" if is_report else "src/stats/run_froc_annotation.py"
        )
        source_config = config_path if is_report else Path(config["analysis_config"])
        if path.suffix == ".csv":
            rows = read_csv(path)
            columns = list(rows[0])
            schema = dict(
                type="csv", required_columns=columns, exact_columns=columns, row_count=len(rows)
            )
        elif path.suffix == ".png":
            with Image.open(path) as image:
                schema = dict(type="png", width=image.width, height=image.height)
        else:
            schema = dict(type="json", top_level_type="object", required_keys=list(read_json(path)))
        dependencies = (
            summary["inputs"] + summary["artifacts"]
            if path == summary_path
            else [artifact(summary_path)]
        )
        if is_report:
            dependencies += report["inputs"] + report["artifacts"]
        manifest["artifacts"].append(
            dict(
                path=path.as_posix(),
                sha256=artifact(path)["sha256"],
                generating_script=source,
                generating_script_sha256=artifact(source)["sha256"],
                config=dict(
                    path=source_config.as_posix(), sha256=artifact(source_config)["sha256"]
                ),
                input_artifacts=[binding(e) for e in dependencies],
                expected_schema=schema,
                study_phase="Exploratory shared-annotation FROC sensitivity v1",
                reproduction_tier="authorized_data_replay",
                gpu_required=False,
                training_required=False,
                referenced_results=[],
            )
        )
    require(manifest["artifacts"][: len(previous)] == previous, "Prior entries changed")
    manifest["manuscript_critical_paths"] = [e["path"] for e in manifest["artifacts"]]
    manifest["publication_extension"]["froc_annotation_v1"] = dict(
        analysis_id=summary["analysis_id"],
        maintenance_script=Path(__file__).resolve().relative_to(Path.cwd()).as_posix(),
        note="Prior records preserved; retrospective conditional sensitivity, no label correction.",
    )
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    return len(paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    print(f"Registered {register(args.config, args.manifest)} annotation-audit artifacts")
