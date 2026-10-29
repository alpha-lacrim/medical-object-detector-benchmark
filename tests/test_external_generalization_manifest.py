"""Portable protection against silently refreshing pre-existing evidence."""

import json
from pathlib import Path

import pytest
import yaml

from scripts import extend_external_generalization_manifest as maintenance
from src.stats.run_vindr_statistics import artifact


def test_manifest_extension_preserves_existing_entries_and_rejects_repeat(tmp_path, monkeypatch):
    original_root = Path.cwd()
    generator = Path(maintenance.analysis.__file__).resolve().relative_to(original_root)
    (tmp_path / generator).parent.mkdir(parents=True)
    (tmp_path / generator).write_text("# synthetic generator\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(maintenance.inspect, "getfile", lambda obj: str(tmp_path / generator))
    monkeypatch.setattr(maintenance.analysis, "verify", lambda path: {"status": "verified"})
    root = Path("results/synthetic")
    root.mkdir(parents=True)
    csv_path = root / "counts.csv"
    csv_path.write_text("detector,count\na,2\n")
    summary_path = root / "summary.json"
    summary_path.write_text(json.dumps({"inputs": [], "artifacts": [artifact(csv_path)]}))
    config_path = Path("config.yaml")
    config_path.write_text(
        yaml.safe_dump(
            {
                "analysis_id": "synthetic",
                "outputs": {"public_root": root.as_posix(), "summary": summary_path.name},
            }
        )
    )
    manifest = Path("manifest.json")
    prior = {"path": "original.json", "sha256": "must-not-change", "metadata": {"a": [1, 2]}}
    manifest.write_text(json.dumps({"artifacts": [prior], "publication_extension": {}}))
    # Keep the maintenance-script path inside the synthetic workspace as well.
    monkeypatch.setattr(maintenance, "__file__", str(tmp_path / "scripts/maintenance.py"))
    assert maintenance.extend(config_path, manifest) == 2
    result = json.loads(manifest.read_text())
    assert result["artifacts"][0] == prior
    before = manifest.read_bytes()
    with pytest.raises(ValueError, match="already registered"):
        maintenance.extend(config_path, manifest)
    assert manifest.read_bytes() == before


def test_binding_rejects_changed_source(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = Path("source.txt")
    path.write_text("before")
    entry = artifact(path)
    path.write_text("after")
    with pytest.raises(ValueError, match="Hash mismatch"):
        maintenance.binding(entry)
