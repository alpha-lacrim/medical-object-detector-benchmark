# Threshold repairability v2: execution and verification

6-7 November 2026. Exploratory follow-up to the public-table pilot, explicitly
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

The scientific/manuscript checkpoint is committed and pushed as
`c29f86374b545d5a6abd10ff034a7edb68109a9e`. Its GitHub Actions run
[42281988247](https://github.com/alpha-lacrim/medical-object-detector-benchmark/actions/runs/42281988247)
completed successfully. The PDF pins its supporting links to that exact commit;
this is evidence provenance, not designation of a final scientific release.

The refreshed [author-review PDF](../output/pdf/rsna_vindr_article.pdf) has
**22 pages**, all rendered with Poppler at 120 dpi and visually inspected.
Direct S13 links were added during review; only pages 8 and 17 changed on a
second render, and both were reinspected. Every other rendered page was
byte-identical to its inspected predecessor. No clipping, overlap, broken
equations, missing captions or bibliography-layout defects were observed.
The final TeX log contains no overfull boxes, undefined citations or missing
characters. Automated PDF QA reports zero errors.

- Final PDF SHA-256:
  `f0044daf1f99572d28e57105c4644a08a5201ff230e05cfafe1e72b134acde82`.
- Canonical Markdown SHA-256:
  `39d265d9380f9855292da0d94fbdd113bbdd1586605bbd1927acb32888519a2f`.
- All 12 build inputs and the output match the build receipt; 38 internal links
  are valid, and all 12 distinct pinned supporting links resolve to committed
  paths. The S13 anchor exists at the pinned revision.
- All 60 added numerical values are present in extracted PDF text; the 36
  Table 9 values agree in order with the canonical table. New methods appear
  on page 8, Table 9/Figure 5 on page 16, and controls on page 17.
- [Build receipt](../report/paper_build_manifest.json),
  [automated QA](../report/paper_pdf_qa.json) and
  [numerical trace](SUBMISSION_NUMERICAL_TRACE.csv) identify this derivative.

The earlier 19-page PDF is superseded. Original scientific artifacts and all
prior numerical bindings remain unchanged. The PDF and review records form
the final Git checkpoint for this task; no author submission approval is implied.

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
