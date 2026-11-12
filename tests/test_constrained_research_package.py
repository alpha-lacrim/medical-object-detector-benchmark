"""Public research receipts and an independent transport-formulation comparison."""

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from src.meddet_benchmark.evaluation import ImagePrediction, ImageTarget
from src.stats.constrained_diagnostics import oc_cost
from src.stats.constrained_repairability import cardinality

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results/constrained_repairability_v1"


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_public_research_outputs_match_receipts_and_keep_private_draws_local():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    report = json.loads((RESULTS / "report_build.json").read_text(encoding="utf-8"))
    private = []
    for record in [
        *summary["inputs"],
        *summary["artifacts"],
        *report["inputs"],
        *report["artifacts"],
    ]:
        path = ROOT / record["path"]
        if path.exists():
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
    for record in [*summary["artifacts"], *report["artifacts"]]:
        if record["path"].startswith("data/processed/"):
            private.append(record["path"])
        else:
            assert (ROOT / record["path"]).is_file()
    assert len(private) == 1 and private[0].endswith("joint_draws.npz")
    assert summary["formula_verified_all_cells"] and summary["controls_passed"]
    assert {r["invariants_passed"] for r in rows(RESULTS / "perturbations.csv")} == {"True"}


def test_new_study_costs_are_reconstructible_from_published_v2_counts():
    old = {
        (r["dataset"], r["detector"], r["seed"], r["budget"]): r
        for r in rows(ROOT / "results/threshold_repairability_v2/per_run.csv")
    }
    values = rows(RESULTS / "per_run.csv")
    assert len(values) == 500
    for r in values:
        v2 = old[r["dataset"], r["detector"], r["seed"], r["budget"]]
        n, images = int(r["references"]), int(r["images"])
        rank = round(float(v2["historical_recall"]) * n)
        fp = round(float(v2["historical_fp_per_image"]) * images)
        full = round(float(v2["geometry_ceiling"]) * n)
        assert rank == int(r["historical_rank"]) == int(r["historical_greedy_tp"])
        assert rank + fp == int(r["historical_selected"])
        assert full == int(r["full_rank"])
        if int(r["target_count"]) > full:
            assert r["cost"] == "infinite" and r["feasible"] == "False"
        else:
            expected = max(0, int(r["target_count"]) - rank) + max(
                0, fp - int(r["fp_budget_count"])
            )
            assert float(r["cost"]) == expected
            assert math.isclose(float(r["cost_per_reference"]), expected / n, abs_tol=1e-15)
            assert math.isclose(float(r["cost_per_image"]), expected / images, abs_tol=1e-15)
            if r["dataset"] == "external":
                assert int(r["suppressions"]) == 0
    intervals = rows(RESULTS / "intervals.csv")
    assert all(
        int(r["finite"]) + int(r["infinite"]) + int(r["undefined"]) == 2000 for r in intervals
    )
    unstable = next(
        r
        for r in intervals
        if r["dataset"] == "external"
        and r["detector"] == "faster_rcnn"
        and float(r["target_recall"]) == 0.5
        and float(r["budget"]) == 0.25
        and r["metric"] == "cost"
    )
    assert unstable["upper"] == "infinite" and int(unstable["infinite"]) > 0


def test_annotation_unit_bound_requires_normalized_runs_and_unit_edit_weights():
    # One original reference inserted with three observation copies changes rank by three.
    before = cardinality(((), (), ()), 0)
    after = cardinality(((0,), (1,), (2,)), 3)
    assert after - before == 3
    # For three fixed run graphs, normalized averaging restores the unit bound.
    increments = [cardinality(((0,),), 1) - cardinality(((),), 0) for _ in range(3)]
    assert sum(increments) == 3 and np.mean(increments) == 1


def test_oc_assignment_equals_independent_explicit_transport_linear_program():
    rng = np.random.default_rng(32)
    for _ in range(30):
        m, n = map(int, rng.integers(1, 5, 2))
        left = rng.uniform(0, 10, m)
        right = rng.uniform(0, 10, n)
        scores = rng.uniform(0, 1, m)
        # Unit-width boxes with a shared y range permit an independent 1-D GIoU calculation.
        boxes_p = [[x, 0, x + 1, 1] for x in left]
        boxes_t = [[x, 0, x + 1, 1] for x in right]
        p = ImagePrediction("a", (20, 20), boxes_p, [1] * m, scores)
        t = ImageTarget("a", (20, 20), boxes_t, [1] * n)
        matrix = np.full((m + 1, n + 1), 0.6)
        for i, x in enumerate(left):
            for j, y in enumerate(right):
                overlap = max(0, 1 - abs(x - y))
                union, hull = 2 - overlap, 1 + abs(x - y)
                giou = overlap / union - (hull - union) / hull
                matrix[i, j] = 0.5 * (1 - giou) / 2 + 0.5 * (1 - scores[i]) / 2
        equality, demands = [], []
        for i in range(m + 1):
            constraint = np.zeros_like(matrix)
            constraint[i, :] = 1
            equality.append(constraint.ravel())
            demands.append(1 if i < m else n)
        for j in range(n + 1):
            constraint = np.zeros_like(matrix)
            constraint[:, j] = 1
            equality.append(constraint.ravel())
            demands.append(1 if j < n else m)
        lp = linprog(matrix.ravel(), A_eq=equality, b_eq=demands, bounds=(0, None), method="highs")
        assert lp.success
        flow = lp.x.reshape(matrix.shape)
        flow[-1, -1] = 0
        expected = (flow * matrix).sum() / flow.sum()
        actual = oc_cost(p, t, localization_weight=0.5, dummy_cost=0.6, empty_empty_cost=0)
        np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-12)
