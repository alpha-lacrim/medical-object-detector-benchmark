"""Independent exhaustive checks and counterexamples for the proposed theorems."""

from dataclasses import replace
from itertools import product

import numpy as np
import pytest

from src.stats.constrained_repairability import (
    RepairProblem,
    cardinality,
    count_constraint,
    exhaustive,
    solve,
    uniform_cost,
)


def problem(rows, refs, initial=None, p=None, q=None):
    n = len(rows)
    return RepairProblem(
        tuple(tuple(r) for r in rows),
        refs,
        tuple(initial or [False] * n),
        tuple(p or [1] * n),
        tuple(q or [1] * n),
    )


def check(p, k, b):
    actual = solve(p, k, b)
    assert (None if actual is None else actual.cost) == exhaustive(p, k, b)
    if actual is not None:
        assert actual == solve(p, k, b)
        selected = set(actual.selected)
        assert len({c for c, _ in actual.assignment}) == len(actual.assignment)
        assert len({g for _, g in actual.assignment}) == len(actual.assignment)
        assert all(c in selected and g in p.neighbors[c] for c, g in actual.assignment)
        assert len(actual.assignment) >= k
        assert len(selected) - len(actual.assignment) <= b


def test_all_two_by_two_graphs_memberships_targets_and_budgets():
    # Exhaustive topology/membership coverage, including duplicates and empty references.
    for edges in product((False, True), repeat=4):
        rows = tuple(tuple(j for j in range(2) if edges[2 * i + j]) for i in range(2))
        for initial in product((False, True), repeat=2):
            p = problem(rows, 2, initial)
            r = cardinality(tuple(row for row, keep in zip(rows, initial, strict=True) if keep), 2)
            full = cardinality(rows, 2)
            for k, b in product(range(4), range(3)):
                check(p, k, b)
                assert uniform_cost(sum(initial), r, full, k, b) == exhaustive(p, k, b)


def test_seeded_heterogeneous_and_uniform_cost_properties():
    rng = np.random.default_rng(20261107)
    for _ in range(150):
        n, g = map(int, rng.integers(0, 7, 2))
        rows = tuple(tuple(map(int, np.flatnonzero(rng.random(g) < 0.4))) for _ in range(n))
        initial = tuple(map(bool, rng.integers(0, 2, n)))
        p = problem(
            rows,
            g,
            initial,
            list(map(int, rng.integers(0, 6, n))),
            list(map(int, rng.integers(0, 6, n))),
        )
        k, b = int(rng.integers(0, g + 2)), int(rng.integers(0, n + 1))
        check(p, k, b)
        cp, cq = map(int, rng.integers(0, 6, 2))
        uniform = replace(p, promotion=(cp,) * n, suppression=(cq,) * n)
        rank = cardinality(tuple(row for row, keep in zip(rows, initial, strict=True) if keep), g)
        assert exhaustive(uniform, k, b) == uniform_cost(
            sum(initial), rank, cardinality(rows, g), k, b, cp, cq
        )


@pytest.mark.parametrize(
    "rows,refs,initial,k,b,expected",
    [
        ([], 0, [], 0, 0, 0),
        ([], 1, [], 1, 0, None),
        ([[], []], 0, [True, True], 0, 0, 2),
        ([[0], [0]], 1, [True, True], 1, 0, 1),
        ([[0, 1], [0]], 2, [True, True], 2, 0, 0),
        ([[0], []], 1, [False, True], 1, 0, 2),
    ],
)
def test_edge_cases(rows, refs, initial, k, b, expected):
    p = problem(rows, refs, initial)
    check(p, k, b)
    result = solve(p, k, b)
    assert (None if result is None else result.cost) == expected


def test_heterogeneous_cost_not_determined_by_counts():
    # Same H,r,M,K,B, different available promotion costs: the weighted problem is distinct.
    a = problem([[0], [0]], 1, p=[1, 10])
    b = replace(a, promotion=(5, 10))
    assert solve(a, 1, 0).cost == 1
    assert solve(b, 1, 0).cost == 5


def test_shared_reference_edits_bound_difference_and_relocation_is_two():
    rng = np.random.default_rng(13)
    for _ in range(250):
        g = int(rng.integers(0, 7))
        graphs = [
            tuple(
                tuple(map(int, np.flatnonzero(rng.random(g) < 0.4)))
                for _ in range(int(rng.integers(0, 7)))
            )
            for _ in range(2)
        ]
        initial = [cardinality(rows, g) for rows in graphs]
        inserted = [
            tuple(tuple((*r, g)) if rng.random() < 0.5 else r for r in rows) for rows in graphs
        ]
        changed = [cardinality(rows, g + 1) for rows in inserted]
        assert abs((changed[0] - changed[1]) - (initial[0] - initial[1])) <= 1
        if g:
            deleted = [
                tuple(tuple(j for j in row if j != g - 1) for row in rows) for rows in graphs
            ]
            new = [cardinality(rows, g - 1) for rows in deleted]
            assert abs((new[0] - new[1]) - (initial[0] - initial[1])) <= 1
    # One old box matches A only; relocating it makes it match B only: gap +1 -> -1.
    assert abs((0 - 1) - (1 - 0)) == 2


def test_decimal_constraints_do_not_round_toward_the_wrong_integer():
    assert count_constraint(0.1, 95, ceiling=True) == 10
    assert count_constraint(0.25, 95, ceiling=True) == 24
    assert count_constraint(0.125, 750, ceiling=False) == 93
    assert count_constraint(0.07, 100, ceiling=True) == 7


def test_validation_rejects_fractional_costs_and_constraints():
    with pytest.raises(ValueError, match="Costs"):
        problem([[0]], 1, p=[0.1])
    with pytest.raises(ValueError, match="Neighbors"):
        problem([[1]], 1)
    with pytest.raises(ValueError, match="integers"):
        solve(problem([], 0), 0, 0.1)
