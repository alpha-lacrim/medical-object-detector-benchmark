"""Verify the complete public grid and independently reconstruct private summaries."""

import json
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.stats.run_vindr_statistics import verify_artifact

ROOT = Path("results/froc_annotation_v1")


def test_public_annotation_receipts_and_complete_design():
    summary = json.loads((ROOT / "summary.json").read_text())
    report = json.loads((ROOT / "report_build.json").read_text())
    for entry in [*summary["artifacts"], *report["inputs"], *report["artifacts"]]:
        if not entry["path"].startswith("data/"):
            verify_artifact(entry)
    for name, count in summary["rows"].items():
        table = pd.read_csv(ROOT / f"{name}.csv")
        assert len(table) == count
        assert set(table.budget) == set(summary["budgets"])
    exact = pd.read_csv(ROOT / "exact_deletions.csv")
    for row in exact.itertuples():
        assert row.cases == comb(row.original_references, row.deletions)
        assert row.remaining_references == row.original_references - row.deletions
        assert row.independent_lower <= row.lower + 1e-12
        assert row.upper <= row.independent_upper + 1e-12


@pytest.mark.scientific_data
def test_joint_intervals_and_shared_extrema_from_saved_arrays():
    summary = json.loads((ROOT / "summary.json").read_text())
    archive = next(e for e in summary["artifacts"] if e["path"].endswith(".npz"))
    verify_artifact(archive)
    detectors, budgets = summary["detectors"], summary["budgets"]
    entities = [*detectors, "-".join(detectors)]
    edits = summary["bootstrap_edits"]
    alpha = (1 - summary["confidence_level"]) / 2
    with np.load(archive["path"]) as arrays:
        for row in pd.read_csv(ROOT / "contrasts.csv").itertuples():
            m, b, j = (
                detectors.index(row.detector),
                budgets.index(row.budget),
                edits.index(row.external_edits),
            )
            side = 1 if row.endpoint == "lower" else 0
            samples = (
                arrays["draws"][:, 0, m, b, edits.index(0), 0]
                - arrays["draws"][:, 1, m, b, j, side]
            )
            finite = samples[np.isfinite(samples)]
            assert row.valid == len(finite)
            assert row.undefined == len(samples) - len(finite)
            np.testing.assert_allclose(
                [row.lower, row.upper], np.quantile(finite, [alpha, 1 - alpha]), atol=1e-12
            )
        for row in pd.read_csv(ROOT / "exact_deletions.csv").itertuples():
            means = arrays[f"{row.dataset}_delete_{row.deletions}"].mean(axis=1)
            m, b = entities.index(row.entity), budgets.index(row.budget)
            values = (means[m] if m < 2 else means[0] - means[1])[:, b]
            np.testing.assert_allclose([row.lower, row.upper], [values.min(), values.max()])


@pytest.mark.scientific_data
def test_registration_preserves_prior_inventory_and_refuses_duplicates(tmp_path):
    from scripts.register_froc_annotation import register

    original = json.loads(Path("results/publication_artifact_manifest.json").read_text())
    earlier = [e for e in original["artifacts"] if not e["path"].startswith(ROOT.as_posix())]
    original["artifacts"] = earlier
    original["manuscript_critical_paths"] = [e["path"] for e in earlier]
    original["publication_extension"].pop("froc_annotation_v1")
    destination = tmp_path / "inventory.json"
    destination.write_text(json.dumps(original), encoding="utf-8")
    report_config = Path("configs/froc_annotation_v1_report.yaml")
    added = register(report_config, destination)
    updated = json.loads(destination.read_text())
    assert updated["artifacts"][: len(earlier)] == earlier
    assert added == len(updated["artifacts"]) - len(earlier)
    before = destination.read_bytes()
    with pytest.raises(ValueError, match="Already registered"):
        register(report_config, destination)
    assert destination.read_bytes() == before
