# Shared-annotation audit verification

15 November 2026. Analysis namespace `froc_annotation_v1`.

| Check | Observed result |
|---|---|
| Completed v2 baseline reproduction | All 20 cohort/run gates passed |
| New full run | Five public tables, complete subset census, 2,000 joint draws; 118.09 s |
| Fresh full replay | All tables and private arrays exact; 210.86 s |
| Analysis receipt | 146 inputs / six outputs verified |
| Report receipt and replay | Four inputs / three outputs; byte exact |
| Visual review | Both PNG figures inspected; readable axes, captions and legends |
| Portable suite | 574 passed, one expected metadata-only skip |
| Licensed-data suite | Eight passed with `--run-scientific` |
| Static checks | Ruff check and format passed for src/tests/scripts |
| Preserved manuscript checks before integration | 538 numerical bindings and all semantic guards passed |
| Preserved publication manifest | 121 artifacts verified |
| Original external freeze | 38 files verified unchanged |
| Staged receipt contents | 110 public bindings match Git index bytes; 49 authorized ignored dependencies |
| Privacy | All 3,000 private external image identifiers absent from staged text; no data/checkpoints staged |
| Graph | AST update completed: 4,803 nodes / 13,490 edges |

The theorem/algorithm suite includes exhaustive preference checks, independently
rematched random geometry, whole-score ties, caps, empty sets, zero budgets,
monotone scores, nonadditive same-image deletions and a marginal-FROC
nonredundancy construction. The additional saved-array test independently
reconstructs every domain-contrast interval and shared-deletion extremum.

The original seven scientific tests and the additional annotation-artifact test
ran with the explicit licensed-data option. A preliminary invocation using only
the marker selected no tests, because the repository deselects scientific tests
without that option; it is not counted as a validation pass.

The primary and prior exploratory artifacts remain unchanged. No image inference,
retraining, operational threshold selection, clinical relabeling or unrestricted
data publication occurred. Manuscript integration and its PDF checks follow this
verified scientific checkpoint and are separately recorded in the session handoff.

See [README commands](../README.md#shared-annotation-froc-certificates-exploratory-v1),
[assessment](FROC_ANNOTATION_RESEARCH_ASSESSMENT.md), and
[results](FROC_ANNOTATION_RESULTS_V1.md). These checks establish implementation
and reproduction evidence, not publication priority or clinical truth.
