# Post-hoc external generalization v1 — execution and verification

Date: 2026-10-29. Status: **VERIFIED execution; EXPLORATORY scientific findings**.
The user resumed the paused standalone research request and subsequently
authorized Git commits and pushes. This is not a new numbered batch.

## Evidence and preservation

Initial baseline: `801a6c90afa480351a9e0d72ca7709b47da95e2e` on `main`.
During integration, a separate commit `40a272cdde64007795b2a2324963b834760121bb`
appeared locally and on GitHub main, including the new analysis and previously
untracked project files. It is preserved; the final integration follows it.
No source experiment, checkpoint, target definition, threshold, candidate
floor/cap, seed inclusion rule or historical result was rewritten.

The original 38-file external freeze and 72-artifact inventory passed before
new analysis and again afterward. All previous 88 publication records are
structurally identical to the initial baseline. The new manifest adds 18
records: summary, 15 CSVs and two figures. All 427 earlier numerical claims
and 36 semantic guards remain identical; 41 claims and four guards were added.
The current trace exports all 468 claims. No historical tolerance was relaxed.

Accepted summary:
`results/external_generalization_v1/summary.json`, SHA-256
`a8f39dd5b22683f35e2363b39e9415d41b580c85bfd5af389eab1647df999106`.
It binds 138 inputs, including source annotations, frozen prediction bundles,
checkpoint identities, code, tests, config and protocol. Full replay reproduced
every new table, point and all 2,000 saved bootstrap draws exactly. All 20
cohort/checkpoint point estimates were reconciled with the canonical evaluator.

## Executed commands and outcomes

Commands used `.venv/Scripts/python.exe` in the repository root. For authorized
checks, PowerShell set
`$env:VINDR_CXR_ROOT = (Resolve-Path data/raw/vindr-cxr).Path`.
The pinned environment and derived RNG seed are recorded in the summary.

| Command after Python executable | Executed outcome |
|---|---|
| `-m src.stats.run_external_generalization --config configs/external_generalization_v1.yaml --mode preflight` | PASS: 138 bindings; source/local-box validation and strict geometry reconciliation |
| `-m src.stats.run_external_generalization --config configs/external_generalization_v1.yaml --mode run` | PASS: accepted write-once analysis; 15 tables, two figures, private draws and summary |
| `-m src.stats.run_external_generalization --config configs/external_generalization_v1.yaml --mode verify` | PASS: hashes and saved-draw intervals |
| `-m src.stats.run_external_generalization --config configs/external_generalization_v1.yaml --mode replay` | PASS: full recomputation, exact equality, `full_replay: true` |
| `-m pytest tests/test_external_generalization.py tests/test_transportability.py -q` | PASS: 50 tests |
| `-m pytest tests/test_external_generalization_manifest.py -q` | PASS: two tests, including refusal of repeat registration and tampered input |
| `-m pytest -q` | PASS: 488 passed, one skipped, seven scientific tests deselected |
| `-m pytest -q --run-scientific` | PASS: 495 passed, one skipped |
| `-m ruff check src tests scripts` | PASS |
| `-m ruff format --check src tests scripts` | PASS: 140 files already formatted |
| `-m scripts.verify_paper_claims` | PASS: 468 numerical claims, all 40 semantic guards |
| `-m scripts.verify_scientific_artifacts` | PASS: original 72 artifacts, 346 present inputs, zero missing, 201 referenced results |
| `-m scripts.verify_scientific_artifacts --manifest results/publication_artifact_manifest.json` | PASS: 106 artifacts, 820 present inputs, zero missing, 212 referenced results |
| `-m scripts.verify_frozen_external --mode freeze` | PASS: original 38 frozen files |
| `-m scripts.verify_frozen_external --mode statistics` | PASS: 130 bindings and 44 interval rows reconstructed from saved draws; **not** a fresh original bootstrap |
| `-m scripts.export_paper_trace --manifest report/paper_claim_sources.yaml --output docs/SUBMISSION_NUMERICAL_TRACE.csv` | PASS: 468 verified rows exported |
| `-m scripts.check_bibliography --bibliography report/references.bib --manuscripts report/paper_draft.md report/report.md report/Manuscript_FasterRCNN_vs_YOLO11s_LungOpacity.md` | PASS: 45 unique entries; 24/19/27 cited keys resolve |

The one skipped test applies only to metadata-only environments; authorized
data are present here. Portable tests do not substitute for full scientific
execution. The legacy wrapper exposes archived editorial baseline reads only;
it does not temporarily overwrite the live paper or claim file. Original
statistics summary remains SHA-256
`a5267d223102c2312e0b568e06c7e4bf2f6157175e989d070afc943a23942f0b`.

One-time registration used
`-m scripts.extend_external_generalization_manifest --config configs/external_generalization_v1.yaml --manifest results/publication_artifact_manifest.json`.
It added 18 entries and refuses a second registration. Do not regenerate the
older publication manifest builder or refresh hashes to conceal changed inputs.
Reproduction commands and input restrictions are also in the README.

`git diff --check` passed. `graphify update .` completed with AST extraction;
two files supplied no symbols (`pyproject.toml` and an existing orchestration
PowerShell script). No paid/LLM graph-labeling step was needed. The graph update
does not alter analysis code or source bindings.

## Implementation corrections and preserved attempts

The paused draft's source/canonical identity mismatch was confined to the new
loader. Explicit PNG suffix mapping and validation of `No finding` sentinel
rows resolved it; the frozen adapter and data were unchanged. Synthetic tests
cover source identity, invalid/duplicate geometry, sentinels, assignment and
boundary behavior, overlapping classes, negatives, empty outputs, undefined
fractions, candidate limits, canonical AP reconciliation, custom weighted AP,
patient multiplicities and cross-domain checkpoint resampling.

The first complete computation failed during final JSON serialization of
array-valued point estimates. A conversion fix and regression test resolved
it. The next completed result passed verification, but visual review found
a legend obscuring an interval. During the following render iteration, an
in-flight renderer edit caused final source-hash verification to reject that
attempt. No hash was refreshed to accept the mismatch. After source edits
stopped, a new complete run passed, followed by the independent full replay.

Those attempts, logs and archive hash receipts remain private under
`data/processed/vindr-cxr-external-v1/superseded/`, in
`generalization_v1_serialization_failure`, `generalization_v1_layout_review`
and `generalization_v1_render_receipt`. The latter deliberately retains its
failed provenance status. A direct comparison confirms all 15 CSVs, scientific
points and bootstrap arrays in the accepted result equal those from the
earlier completed layout-review snapshot. Only serialization/rendering
corrections were involved; no outcome-dependent scientific setting changed.

## Figures, manuscript, privacy and remaining work

Both accepted PNGs were visually inspected: labels, legends, values and
intervals are legible with no covered points or clipped text. The manuscript
adds Abstract/Introduction context, primary prior art in Section 2.4, methods
in Section 3.9, results and Table 8 in Section 4.10, and bounded discussion,
limitations and conclusion. Section 3.6 now dates the original absence of
cross-domain contrasts; Supplement S11 links the new evidence. The existing
PDF and build/QA receipts initially remained the prior 16-page reviewed
snapshot. The subsequent user-requested PDF follow-up below resolves that
remaining formatting task without changing scientific content.

A local integrity check compared the current manifests/claims with the exact
initial Git revision and compared science across the archived/accepted runs.
A scan of 667 changed/public text files before this final record found no
released VinDr image identifiers. Restricted source annotations, images,
prediction bundles and bootstrap draws remain untracked in ignored paths;
only nonidentifying aggregates enter the release. Original scientific and
restricted data were neither uploaded nor modified by this analysis.

**IMPLEMENTED BUT NOT EXECUTED:** none of the core CPU analyses; all were
executed and replayed. **UNRESOLVED / NOT EXECUTED:** broader ontology scoring
requires expert instance adjudication, and expanded candidate-support inference
requires separate authorization and an 8GB GPU resource gate. The proposal
does not constitute an implemented or executed GPU experiment. Ethics/journal
decisions, final author review and a submission release identifier remain
author responsibilities. No causal, clinical or novel-detector claim follows.

## Publication gate

The final staged integration contains 39 files, including the updated knowledge
graph. Exact Git-index bytes match 275 distinct public artifact, generator,
config and input bindings. Staged whitespace checks pass. A final scan including
the rebuilt graph checks 686 changed/public text files with zero released VinDr
image-ID matches. CODEX.md, HANDOFF.md and all private data are excluded.
The user authorized committing and pushing this follow-up to the existing
GitHub main branch; no history rewrite or new inference is part of that action.
The Git commit containing this record identifies the completed integration.

## Subsequent PDF follow-up — 2026-10-29

The user requested a refresh and visual review. The canonical PDF now contains
all post-hoc manuscript additions and spans 19 pages. All pages were visually
reviewed; a split bibliography entry was corrected, and the final two reference
pages were reviewed again. The other 17 pages are pixel-identical to the reviewed
render. Three configured TeX passes complete a fresh build without warnings.
The automated check reports zero errors, 34 internal links and 39 URI targets.
Build/QA receipts match exact inputs/output; the manuscript, scientific values
and 468-row numerical trace are unchanged. Exact commands, hashes and remaining
author decisions are in [the submission audit](FINAL_SUBMISSION_AUDIT.md).
Core CPU analyses were reverified rather than recomputed: all 138 input bindings
and 15 tables still pass, following the already completed full bootstrap replay.
