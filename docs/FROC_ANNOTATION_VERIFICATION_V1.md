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

## Manuscript integration and PDF completion, 16 November 2026

- Scientific checkpoint `ee4f354f9b742bf22dfa464b363c6240ca631aa9` was pushed;
  [its exact-commit CI](https://github.com/alpha-lacrim/medical-object-detector-benchmark/actions/runs/43713326808)
  passed on Windows and Ubuntu.
- Integrated the method and two propositions into Sections 2.6/3.12, results in
  Section 4.13, Table 10, Figures 6-7 and Supplement S14; revised the question,
  title, abstract, discussion and conclusion with explicit scope limitations.
- Added 41 numerical bindings and five semantic guards: 579 values / 52 guards
  pass. Three old abstract-count regexes were narrowed after shortening the
  prose; their sources, values and tolerances are unchanged. The numerical trace
  was regenerated from the verified manifest.
- Added nine publication entries while preserving the original 121 records
  exactly by value. All 130 public artifacts and the original 72-artifact
  inventory pass verification; the 38-file external freeze is unchanged.
- All 574 portable tests and nine licensed-data tests passed (583 total, one
  expected metadata-only skip). The added registration test verifies preservation
  of earlier entries and refusal of duplicate registration. After preserving
  JSON key order in the writer, the three annotation-artifact tests passed again.
- Ruff check/format passed for 169 Python files. AST graph updates include the
  new code; the graph tool's optional PDF text extractor is unavailable, so the
  graph is not evidence of semantic PDF review. PDF extraction/rendering used
  the separate document environment and Poppler successfully.
- Built the 25-page article with the prescribed marker, Pandoc/citeproc and
  three TeX passes. All 25 pages were visually inspected at 120 dpi. Shortening
  the abstract kept it on the title page; a table-space adjustment fixed an
  empty repeated Table 9 header. Only pages 17-19 changed in the final layout
  pass, and all three were reinspected. Automated QA reports zero errors.
- Verified 18 supporting PDF links against files in the pinned scientific
  commit and checked the new numerical strings in extracted PDF text. Source,
  figure, bibliography and output hashes match the build receipt.

Final PDF SHA-256:
`3bc53b11a95b8c66bdb5d2f8f54a81c05dc2852d9bad3efe774d825dbd5ec922`.
The [article](../output/pdf/rsna_vindr_article.pdf) is an author-review derivative,
not a final submission release. The research assessment's GO verdict concerns
a bounded methodological addition; priority, clinical causality and ontology
equivalence are still not established.
