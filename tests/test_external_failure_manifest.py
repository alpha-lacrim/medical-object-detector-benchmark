"""Protect existing evidence and immutable diagnostic registration."""

import json
from pathlib import Path

import pytest
import yaml
from PIL import Image

from scripts import register_external_failure as maintenance
from src.stats.run_vindr_statistics import artifact


def test_registration_preserves_old_records_rejects_tampering_and_repeat(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(maintenance, "__file__", str(tmp_path / "scripts/register.py"))
    for name in ("scripts/report_external_failure.py", "src/analyze_external_failure.py"):
        path = Path(name)
        path.parent.mkdir(exist_ok=True)
        path.write_text("# synthetic source\n")
    root = Path("results/diagnostic")
    root.mkdir(parents=True)
    table = root / "counts.csv"
    table.write_text("detector,count\na,1\n")
    report = Path("report.md")
    report.write_text("synthetic report\n")
    figure = root / "paired_changes.png"
    Image.new("RGB", (10, 10)).save(figure)
    summary = root / "summary.json"
    summary.write_text(
        json.dumps(
            {
                "status": "complete_exploratory_diagnostic",
                "inputs": [],
                "artifacts": [artifact(table)],
            }
        )
    )
    build = root / "report_build.json"
    build.write_text(
        json.dumps({"inputs": [artifact(summary)], "outputs": [artifact(report), artifact(figure)]})
    )
    config = Path("config.yaml")
    config.write_text(
        yaml.safe_dump({"analysis_id": "synthetic", "outputs": {"public_root": str(root)}})
    )
    manifest = Path("manifest.json")
    original = {"path": "original.csv", "sha256": "untouched", "nested": {"evidence": [1, 2]}}
    before = json.dumps({"artifacts": [original], "publication_extension": {}})
    manifest.write_text(before)
    table.write_text("tampered\n")
    with pytest.raises(ValueError, match="Hash mismatch"):
        maintenance.register(config, manifest)
    assert manifest.read_text() == before
    table.write_text("detector,count\na,1\n")
    assert maintenance.register(config, manifest) == 4
    assert json.loads(manifest.read_text())["artifacts"][0] == original
    registered = manifest.read_bytes()
    with pytest.raises(ValueError, match="already registered"):
        maintenance.register(config, manifest)
    assert manifest.read_bytes() == registered
