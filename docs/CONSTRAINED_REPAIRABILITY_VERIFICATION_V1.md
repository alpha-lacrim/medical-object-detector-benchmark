# Constrained repairability v1: verification record

Completed 12 November 2026; analysis/protocol originated 7 November 2026.
Branch `research/constrained-repairability-v1`, from clean, pushed baseline
`cc00ae5a53187d23ba87262b76f025ccbd9de983`. The latest task explicitly requested
a new research branch; this takes precedence over the earlier main-only workflow.

## Evidence and execution

- Original v2 work was committed/pushed at `c29f863`, with final PDF at `cc00ae5`.
  Fresh v2 replay passed: five tables, all 2,000 joint draws, baseline and control
  gates; elapsed 297.62 seconds in this session. Runtime differs from the earlier
  host measurement without changing the deterministic outputs.
- New smoke: both complete cohorts/all 20 runs, 500 flow/formula cells,
  one run's 11 controls and eight bootstrap draws; 21.69 seconds, no output writes.
- Full execution: 98.72 seconds; 500 per-run grid rows, 400 marginal interval rows,
  220 control rows, 40 OC-cost comparison rows, 202 annotation sensitivity rows
  and all 2,000 joint observation/run draws. All flow/formula and control gates pass.
- Fresh full replay: 102.25 seconds, all five CSV tables and every saved point/draw
  exactly reproduced, including infinite costs. Report replay reproduces both
  figures and generated Markdown byte-for-byte. Both figures were visually
  inspected: labels, infinity cells, axes and deterministic-bound captions are legible.
- Analysis receipt SHA-256:
  `f3a91252ec313806cb7d666930c97a5482db75921b6a2d31502fa5a9d7f7038a`.
  It binds 149 inputs and six outputs, including the private bootstrap archive.
- Report receipt SHA-256:
  `841f57a37ea24425cdd5d0d88d584e3e3fb98e8477ce3efc42ec26433bc79067`.
  It binds three report inputs and three generated outputs.

Commands are documented in the [README](../README.md#constrained-repairability-research-assessment).
The strict external ontology, score floor/cap, native NMS, historical cutoffs,
IoU compatibility, exact tied-score FROC and image populations were inherited.
No models were run and no source annotations or prediction bundles were edited.

## Tests and review

Twenty-five new tests include exhaustive two-candidate/two-reference topology,
membership, target and budget combinations (768 instances), 150 seeded weighted
small instances and their uniform-price counterparts, 250 synthetic paired
reference-edit cases, and 30 independent transport-LP checks of the OC-cost
assignment implementation. These are finite software tests, not substitutes for
the mathematical proofs. Edge tests cover no detections/references, duplicates,
many-to-one and one-to-many compatibility, ties, zero budgets, unreachable
targets, monotone maps, ranking/removal controls, greedy non-achievability,
reference additions on negative images, observation-copy reconstruction,
independent run resampling and retained infinite/undefined outcomes.

The original paper's 538 numerical bindings and semantic guards pass, the
publication inventory verifies all 121 artifacts, and all 38 original frozen
files match. All 559 portable tests and seven licensed-data integration tests
pass (566 total; one expected metadata-only test skipped). Ruff format/check
passes on all 142 checked source, test and reporting files. Graphify AST update
completed with 4,729 nodes and 13,146 edges. Its PDF parser extra is absent;
the graph rebuild is for code, and PDF inspection used the existing rendered
artifact instead.

The canonical paper SHA-256 remains
`39d265d9380f9855292da0d94fbdd113bbdd1586605bbd1927acb32888519a2f`;
the current 22-page PDF remains
`f0044daf1f99572d28e57105c4644a08a5201ff230e05cfafe1e72b134acde82`.
Its existing rendered repairability page was inspected for context. No new PDF
was built because the assessment is NO-GO for manuscript integration. The prior
full visual review remains recorded in the v2 verification note.

## Scientific conclusion

The flow/oracle theorem, uniform-cost reduction and annotation-edit bound have
explicit proofs in the [assessment](CONSTRAINED_REPAIRABILITY_RESEARCH_ASSESSMENT.md).
No new minimum-cost-flow algorithm or integrality theorem is claimed. Every
uniform-cost result is determined by quantities already recoverable from the
study's v2 results. The conditional annotation ranking certificate is useful
sensitivity analysis but is not a causal explanation, FROC theorem, clinical
label validation, conformal guarantee or established publication-level novelty.
The experimental code and results are retained separately, with all primary
scientific and manuscript records preserved.
