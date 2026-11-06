"""Publication registration is append-only and rejects tampering before writing."""

import json
from pathlib import Path

import pytest
import yaml
from PIL import Image

from scripts import register_threshold_repairability as maintenance
from src.stats.run_vindr_statistics import artifact


def test_registration_preserves_old_records_and_rejects_tampering_and_repeat(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(maintenance, "__file__", str(tmp_path / "scripts/register.py"))
    for name in (
        "scripts/report_threshold_repairability.py",
        "src/stats/run_threshold_repairability.py",
    ):
        path = Path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# synthetic source\n")
    root = Path("results/repairability")
    root.mkdir(parents=True)
    table = root / "counts.csv"
    table.write_text("detector,count\na,1\n")
    report = Path("report.md")
    report.write_text("synthetic report\n")
    figure = root / "figure.png"
    Image.new("RGB", (10, 10)).save(figure)
    summary = root / "summary.json"
    summary.write_text(
        json.dumps(dict(status="completed_exploratory", inputs=[], artifacts=[artifact(table)]))
    )
    build = root / "report_build.json"
    build.write_text(
        json.dumps(dict(inputs=[artifact(summary)], outputs=[artifact(report), artifact(figure)]))
    )
    analysis = Path("analysis.yaml")
    analysis.write_text(
        yaml.safe_dump(
            dict(
                analysis_id="synthetic", outputs=dict(public_root=str(root), summary="summary.json")
            )
        )
    )
    config = Path("config.yaml")
    config.write_text(
        yaml.safe_dump(dict(analysis_config=str(analysis), outputs=dict(receipt=str(build))))
    )
    manifest = Path("manifest.json")
    original = dict(path="original.csv", sha256="unchanged", nested=dict(evidence=[1, 2]))
    before = json.dumps(dict(artifacts=[original], publication_extension={}))
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
