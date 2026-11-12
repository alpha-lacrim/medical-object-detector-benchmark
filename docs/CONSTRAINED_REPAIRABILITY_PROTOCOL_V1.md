# Constrained repairability v1: exploratory computational protocol

7 November 2026. Written after inspecting the completed v2 results and deriving
candidate theorems, before the new real-data analysis. This is exploratory work,
not preregistration. Branch: `research/constrained-repairability-v1`, based on
`cc00ae5`. Preserve all primary, v1/v2, manuscript and PDF bytes.

Use both complete saved cohorts, all five seeds per detector, and every original
FP/image budget. Inherit classes, strict external ontology, candidate floor, cap,
native NMS, historical cutoffs and IoU from the frozen external protocol. No model
execution, radiologist review, label changes or fitted operating policy. Replay
v2 first and check its hash-bound inputs; replay FROC and geometry per run.

Evaluate K=ceil(q*N) for q in {0.10,0.25,0.50,0.75,0.90}, spanning low through high
coverage, without suggesting these are clinical requirements. B=floor(b*n_images)
for every original budget, including negative images in n_images. Unit promotion
and suppression costs count membership edits, not minutes, risk or clinical
benefit. Do not manufacture heterogeneous clinical weights. The general solver
supports integer weights, tested synthetically. Rational costs can be scaled.

Distinguish membership changes from score-threshold changes, optimal assignment,
and changed/new geometry. All optimum costs and selected subsets are retrospective
annotation-informed oracles. No candidate identities or fitted cutoffs are public.
Compare exact circulation with the uniform-cost formula on every real grid cell,
and with exhaustive selection/assignment enumeration on small synthetic graphs.
Use synthetic score-order counterexamples to delimit deployability.

Report costs as counts, per reference and per image; expose infeasibility as an
infinite extended cost, never drop unsuccessful runs. Report FROC ceiling, full
geometry, historical selected count/rank, promotions, suppressions and fraction
of feasible runs. Equal-run mean cost is infinite if any run is infeasible.

Joint uncertainty uses 2,000 draws: resample internal patient clusters and external
released images independently, share each cohort's observations across all runs,
and independently resample runs within each family. Reuse checkpoint weights
across cohorts. Recompute N,K,B and costs per draw before averaging runs. Report
infinite and undefined draws explicitly. Use inverse empirical-CDF percentiles
so infinite costs are retained without invalid interpolation. Undefined draws
(no reference boxes) remain undefined, without retries. Do not interpret fractions
of feasible resampled runs as deployment success probabilities. The count formula
makes full resampling feasible without repeated large flow solves.

Annotation sensitivity is a deterministic worst-case bound on the difference of
equal-run mean maximum matching COUNTS under shared insertions/deletions. It is
not a measured error rate of the labels, not a FROC bound, and does not edit any
medical reference. Show integer budgets 0 through 100 and k/N for context. Keep
these conditional certificates separate from observation/run uncertainty: an edit
to an original box with bootstrap multiplicity w has weight w, not one.

Controls on every run: two monotone powers (transport the historical cutoff with
the same function), plus score permutation, compatible removal and incompatible
removal at 25/50/100%, one fixed replicate each. Preserve the retained population
before transformations, use evaluation floor zero, and never rerun NMS. Require
power invariance of ranks/membership/cost and FROC; permutation preserves full
geometry but may change initial membership/cost; removals cannot increase full
rank; incompatible removal preserves full/initial rank and cannot increase unit
cost. Reference-edit properties are checked on synthetic graphs only.

Compare with standard FROC/v2 geometry and an independently implemented OC-cost
diagnostic using published equations (lambda=.5,beta=.6), without parameter
optimization. Describe empty-image conventions and numerical implementation
differences explicitly; do not assert a faithful benchmark replication without
checking authors' equations/code. TIDE/LRP/calibration/conformal methods receive
a primary-source comparison matrix; no unsupported cross-method superiority.

Public outputs contain aggregate CSV/JSON/figures only. Source, protocol, config,
private input and output hashes form a separate research receipt. Exact fresh
replay is required. No overwrite of accepted results. Smoke mode writes nothing.
The assessment must record full proofs, counterexamples, complexity, literature,
results, limitations and GO/REVISE/NO-GO before any canonical manuscript change.
GO requires demonstrated nonredundant information and credible novelty, not just
a true theorem or passing tests.
