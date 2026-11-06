# Threshold repairability v2: execution and verification

6 November 2026. Exploratory follow-up to the public-table pilot, explicitly
authorized by the user. Baseline: `8ceb55ebc47306a33655d23f1b2a262b2dfb813c`.
No new model inference, training, external threshold fit or ontology change.

## Scientific evidence

The [protocol](THRESHOLD_REPAIRABILITY_PROTOCOL_V2.md) was written before the
new computation, with earlier outcomes already known. All original saved runs
and both full cohorts passed baseline replay. Internal historical counts also
match the lower-floor prediction sets exactly; external geometric coverage
matches the preceding census-positive diagnostic. No images were excluded.

- 20 baseline run/cohort combinations and 100 run/budget rows.
- 2,000 joint draws; internal patient clusters and external images, independently
  sampled detector runs, shared observations and checkpoint coupling across domains.
- 240 component/endpoint interval rows and 300 coupled contrast rows.
- 580 imposed interventions / 2,900 run/budget intervention rows, including
  40 global score-power controls. All declared invariants passed.
- 220 replicate-averaged control rows; replicates are not independent training runs.
- All endpoint intervals have 2,000 finite draws and zero undefined draws in
  this realized analysis. Undefined handling remains tested and reported.

Analysis summary SHA-256:
`d86a45febb465c2513e5fd9d788484ef1697c87137519158faa14fe6ba4ab040`.

Full execution took 140.90 seconds; a fresh computation took 141.63 seconds and
reproduced all five tables exactly and every point/joint draw numerically
exactly, with no overwriting. Source verification checks 139 inputs and six
outputs. Two figures and the generated report reproduce byte-exactly from
public tables and were visually inspected. Private draw/prediction arrays and
identifiers remain outside Git. Commands are in the
[README](../README.md#threshold-repairability-v2).

## Independent and software checks

Synthetic tests cover score ties, greedy assignment competition, absent
geometry, empty outputs, zero-target resampling, infeasible historical policies,
image-copy reconstruction of weighted counts, deterministic coupled draws,
replicate averaging, immutable source copies and overwrite rejection. Publication
registration tests protect old records and reject changed evidence and repeats.

The complete portable suite passed: **534 passed, one expected metadata-only
skip, seven licensed-data checks deselected**. The seven licensed-data tests
then passed separately, giving 541 passing tests across both scopes.
Independent public-table checks confirmed row counts, nonnegative accounting,
integer geometric counts, finite-draw counts and unchanged old records.
Ruff check/format passed for all source/tests and the new report/registration scripts. Original freeze:
38 files verified. Publication inventory: 121 artifacts, 1,185 present input
bindings and 212 referenced results; all 112 previous records are preserved.
Bibliography: 47 unique entries, including explicit primary TIDE/LRP positioning.
The graph was updated using AST-only extraction.

## Manuscript and review status

The draft integrates the narrower question in its title, abstract and
Introduction, with Methods 3.11, Results 4.12, Table 9, Figure 5, Discussion,
Limitations and S13. All 478 prior numerical bindings remain, with 60 added
bindings and five semantic scope guards: **538 claims / 47 guards**. The
numerical trace is regenerated from the verified bindings.

The scientific evidence checkpoint precedes the PDF refresh. Final build,
page-level visual review and Git publication details will be recorded below
when complete; the earlier PDF should not yet be treated as this revision.

## Scientific interpretation

At the stated budget, cutoff adjustment alone cannot recover most external
reference lesions within original support. Internal/external maximum matching
shows a substantial contraction in usable retained geometry. The smaller
external FP-budget barrier does not indicate better ranking: less geometry
remains to be blocked. The assignment gap is zero for these baseline outputs,
not assumed universally; synthetic competing matches exercise a nonzero gap.

The controls distinguish the consequences of score-order and geometry changes
but do not identify which real acquisition, population, annotation or training
factor produced external failure. Monotone invariance and the accounting
identity are elementary, and FROC already supplies the budget envelope.
Incremental value is the empirical, reproducible repair audit with joint
uncertainty and controlled verification; there is no TIDE/LRP superiority claim,
new calibration model, deployable repaired policy or clinical validation.

The user has no access to radiologists. No expert review is presented as
available or completed. A third independent cohort, generality across recipes
and direct evidence on clinical ontology remain outside this completed scope.
Final publication novelty and author/journal decisions remain unresolved.
