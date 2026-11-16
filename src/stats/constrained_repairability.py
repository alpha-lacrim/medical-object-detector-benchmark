"""Retrospective fixed-candidate repair oracles; never a deployment policy."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching


@dataclass(frozen=True)
class RepairProblem:
    """An image-disjoint compatibility graph and integer candidate edit costs."""

    neighbors: tuple[tuple[int, ...], ...]
    references: int
    initial: tuple[bool, ...]
    promotion: tuple[int, ...]
    suppression: tuple[int, ...]

    def __post_init__(self) -> None:
        n = len(self.neighbors)
        if not isinstance(self.references, int) or self.references < 0:
            raise ValueError("Reference count must be a nonnegative integer")
        if any(len(v) != n for v in (self.initial, self.promotion, self.suppression)):
            raise ValueError("Candidate arrays must have identical lengths")
        if any(type(v) is not bool for v in self.initial):
            raise ValueError("Initial membership must be boolean")
        if any(type(v) is not int or v < 0 for v in (*self.promotion, *self.suppression)):
            raise ValueError("Costs must be nonnegative integers; scale rational costs first")
        for row in self.neighbors:
            if tuple(sorted(set(row))) != row or any(
                type(j) is not int or not 0 <= j < self.references for j in row
            ):
                raise ValueError("Neighbors must be unique sorted reference indices")


@dataclass(frozen=True)
class RepairSolution:
    """An optimal integer cost with a verifiable selected set and assignment."""

    cost: int
    selected: tuple[int, ...]
    assignment: tuple[tuple[int, int], ...]
    promotions: int
    suppressions: int


def cardinality(neighbors: tuple, references: int) -> int:
    """Maximum matching cardinality, independent of candidate order and scores."""
    rows, cols = [], []
    for i, adjacent in enumerate(neighbors):
        rows.extend([i] * len(adjacent))
        cols.extend(adjacent)
    if not rows:
        return 0
    graph = csr_matrix(
        (np.ones(len(rows), dtype=np.int8), (rows, cols)), shape=(len(neighbors), references)
    )
    return int(np.count_nonzero(maximum_bipartite_matching(graph, perm_type="column") >= 0))


def validate_goal(target: int, budget: int) -> None:
    """Reject fractional or negative count constraints rather than rounding them."""
    if any(type(v) is not int or v < 0 for v in (target, budget)):
        raise ValueError("Target and FP budget must be nonnegative integers")


def solve(problem: RepairProblem, target: int, budget: int) -> RepairSolution | None:
    """Exact integral minimum-cost circulation, grouping interchangeable candidates.

    Network simplex uses integer costs/capacities and deterministic insertion order.
    Candidates group only when neighbors, initial membership and active cost agree.
    Inactive incompatible candidates need never be promoted at nonnegative cost.
    """
    validate_goal(target, budget)
    if target > problem.references:
        return None
    groups: dict[tuple, list[int]] = {}
    constant = 0
    for i, (adjacent, initial, p, q) in enumerate(
        zip(problem.neighbors, problem.initial, problem.promotion, problem.suppression, strict=True)
    ):
        constant += q if initial else 0
        if initial or adjacent:
            groups.setdefault((adjacent, initial, -q if initial else p), []).append(i)
    graph = nx.DiGraph()
    graph.add_nodes_from(["s", "t", "fp", "tp"], demand=0)
    # Remove the lower bound K on tp -> t and adjust inflow-minus-outflow demands.
    graph.nodes["tp"]["demand"] = target
    graph.nodes["t"]["demand"] = -target
    graph.add_edge("tp", "t", capacity=problem.references - target, weight=0)
    graph.add_edge("fp", "t", capacity=budget, weight=0)
    graph.add_edge("t", "s", capacity=len(problem.neighbors), weight=0)
    for j in range(problem.references):
        graph.add_edge(("r", j), "tp", capacity=1, weight=0)
    for g, ((adjacent, _, cost), members) in enumerate(groups.items()):
        node = ("c", g)
        graph.add_edge("s", node, capacity=len(members), weight=cost)
        graph.add_edge(node, "fp", capacity=len(members), weight=0)
        for j in adjacent:
            graph.add_edge(node, ("r", j), capacity=1, weight=0)
    try:
        flow_cost, flow = nx.network_simplex(graph)
    except nx.NetworkXUnfeasible:
        return None
    selected, assignment = [], []
    for g, ((adjacent, _, _), members) in enumerate(groups.items()):
        node = ("c", g)
        count = flow["s"][node]
        selected.extend(members[:count])
        matched_refs = [j for j in adjacent if flow[node][("r", j)]]
        assignment.extend(zip(members[: len(matched_refs)], matched_refs, strict=True))
    chosen = set(selected)
    promotions = sum(not problem.initial[i] for i in chosen)
    suppressions = sum(v and i not in chosen for i, v in enumerate(problem.initial))
    cost = sum(problem.promotion[i] for i in chosen if not problem.initial[i]) + sum(
        q for i, q in enumerate(problem.suppression) if problem.initial[i] and i not in chosen
    )
    if (
        cost != flow_cost + constant
        or len(assignment) < target
        or (len(selected) - len(assignment) > budget)
    ):
        raise AssertionError("Flow witness does not satisfy the intervention contract")
    return RepairSolution(
        cost, tuple(sorted(selected)), tuple(sorted(assignment)), promotions, suppressions
    )


def exhaustive(problem: RepairProblem, target: int, budget: int) -> int | None:
    """Independent tiny reference: enumerate selections and all partial assignments."""
    validate_goal(target, budget)
    if len(problem.neighbors) > 12:
        raise ValueError("Exhaustive reference is restricted to at most 12 candidates")

    def rank(rows: tuple, used: frozenset = frozenset()) -> int:
        if not rows:
            return 0
        return max(
            [
                rank(rows[1:], used),
                *[1 + rank(rows[1:], used | {j}) for j in rows[0] if j not in used],
            ]
        )

    best = None
    for selected in product((False, True), repeat=len(problem.neighbors)):
        matched = rank(
            tuple(row for row, keep in zip(problem.neighbors, selected, strict=True) if keep)
        )
        if matched < target or sum(selected) - matched > budget:
            continue
        cost = sum(
            p if keep else q
            for keep, old, p, q in zip(
                selected, problem.initial, problem.promotion, problem.suppression, strict=True
            )
            if keep != old
        )
        best = cost if best is None else min(best, cost)
    return best


def uniform_cost(
    initial_count: int,
    initial_rank: int,
    full_rank: int,
    target: int,
    budget: int,
    promotion: int = 1,
    suppression: int = 1,
) -> int | None:
    """Closed form proved in the research assessment; None means infeasible."""
    validate_goal(target, budget)
    if not 0 <= initial_rank <= min(initial_count, full_rank) or min(promotion, suppression) < 0:
        raise ValueError("Inconsistent ranks or negative costs")
    if target > full_rank:
        return None
    return promotion * max(0, target - initial_rank) + suppression * max(
        0, initial_count - initial_rank - budget
    )


def count_constraint(value: float, denominator: int, *, ceiling: bool) -> int:
    """Exact ceil/floor of a decimal-configured ratio times an integer count."""
    if not np.isfinite(value) or value < 0 or denominator < 0:
        raise ValueError("Ratio and denominator must be nonnegative and finite")
    f = Fraction(str(value)) * int(denominator)
    return -(-f.numerator // f.denominator) if ceiling else f.numerator // f.denominator
