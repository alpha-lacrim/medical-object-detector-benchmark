"""Append verified repairability artifacts while preserving every previous record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from scripts.extend_external_generalization_manifest import binding
from src.stats.run_threshold_repairability import read_csv
from src.stats.run_vindr_statistics import artifact, read_json, read_yaml, require, verify_artifact


def register(config_path: Path, manifest_path: Path) -> int:
    report = read_yaml(config_path)
    config = read_yaml(report["analysis_config"])
    root = Path(config["outputs"]["public_root"])
    summary_path = root / config["outputs"]["summary"]
    build_path = Path(report["outputs"]["receipt"])
    summary, build = read_json(summary_path), read_json(build_path)
    require(summary["status"] == "completed_exploratory", "Analysis is incomplete")
    for item in [*summary["inputs"], *summary["artifacts"], *build["inputs"], *build["outputs"]]:
        verify_artifact(item)
    paths = [
        summary_path,
        *[Path(e["path"]) for e in summary["artifacts"] if Path(e["path"]).is_relative_to(root)],
        *[Path(e["path"]) for e in build["outputs"] if Path(e["path"]).suffix == ".png"],
        build_path,
    ]
    manifest = read_json(manifest_path)
    previous = {e["path"] for e in manifest["artifacts"]}
    require(
        len(set(paths)) == len(paths) and not previous.intersection(p.as_posix() for p in paths),
        "Analysis already registered or duplicate output; do not refresh hashes",
    )
    for path in paths:
        is_report = path.suffix == ".png" or path == build_path
        source = Path(
            "scripts/report_threshold_repairability.py"
            if is_report
            else "src/stats/run_threshold_repairability.py"
        )
        source_config = config_path if is_report else Path(report["analysis_config"])
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
            dependencies += build["inputs"] + build["outputs"]
        manifest["artifacts"].append(
            dict(
                path=path.as_posix(),
                sha256=artifact(path)["sha256"],
                generating_script=source.as_posix(),
                generating_script_sha256=artifact(source)["sha256"],
                config=dict(
                    path=source_config.as_posix(), sha256=artifact(source_config)["sha256"]
                ),
                input_artifacts=[binding(e) for e in dependencies],
                expected_schema=schema,
                study_phase="Exploratory fixed-output threshold repairability v2",
                reproduction_tier="authorized_data_replay",
                gpu_required=False,
                training_required=False,
                referenced_results=[],
            )
        )
    manifest["manuscript_critical_paths"] = [e["path"] for e in manifest["artifacts"]]
    manifest["publication_extension"]["threshold_repairability_v2"] = dict(
        analysis_id=config["analysis_id"],
        maintenance_script=Path(__file__).resolve().relative_to(Path.cwd()).as_posix(),
        note="Original records preserved. Public reporting replays from aggregate tables; "
        "full CPU replay requires authorized saved predictions. No inference or training.",
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
    print(f"Registered {register(args.config, args.manifest)} repairability artifacts")
