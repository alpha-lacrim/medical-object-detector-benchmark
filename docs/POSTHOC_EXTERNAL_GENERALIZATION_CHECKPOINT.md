# External generalization work checkpoint — paused by user

Date: 2026-10-28. **IMPLEMENTATION INCOMPLETE; NO NEW SCIENTIFIC RESULTS.**
User explicitly requested a safe pause because of token limits. Resume this
standalone pasted request only after the user says to resume; it is not Batch 54.

## Request and starting state

Full request is locally preserved at
`C:/Users/Pouyan/.codex/attachments/3efe3994-0be1-4bab-b172-2a29a1fcb1a4/Pasted text.txt`.
It requests a research audit, versioned post-hoc protocol, error decomposition,
non-target annotation overlap, defensible ontology sensitivity, prevalence
standardization, checkpoint-paired domain-change bootstrap, candidate-support
audit, literature assessment, manuscript integration and full verification.
It explicitly permits leaving broader ontology merging pending expert review
and requires separate authorization for new GPU inference. No commit/push.

Baseline HEAD remains `801a6c90afa480351a9e0d72ca7709b47da95e2e` on main.
Existing README Wget addition and unrelated untracked files are preserved.
No tracked scientific artifacts, original configs, predictions or manuscript
were changed. CODEX/HANDOFF are local-only and must never be staged.

## Independently checked baseline

Commands used `.venv/Scripts/python.exe` from the repository root:

- `-m scripts.verify_frozen_external --mode freeze`: PASS, 38 frozen files.
- `-m scripts.verify_scientific_artifacts`: PASS, 72 original artifacts,
  346 present inputs, zero unavailable inputs, 201 referenced result files.
- `-m scripts.verify_paper_claims`: PASS, 427 numerical claims and configured
  semantic guards. The current publication inventory is checked by that gate.
- `-m scripts.verify_frozen_external --mode statistics`: PASS, 130 input
  bindings and 44 interval rows; saved-draw reconstruction, NOT full bootstrap
  recomputation. Log: `tmp/external-generalization-v1/baseline-statistics.log`.
- `-m py_compile` on the three new modules: PASS.
- `git diff --check`: PASS for tracked diff at pause; the new files are untracked.

Authorized local raw data, annotations, original prediction bundles and
checkpoints are present. Set `VINDR_CXR_ROOT` explicitly to resolved
`data/raw/vindr-cxr`; access attestation already exists in frozen v1 config.
Full GPU/source inference replay and full baseline bootstrap replay have NOT
been run this session. Portable/full-data pytest suites have NOT been run.

## New files and their status

- `configs/external_generalization_v1.yaml`: draft post-hoc choices/paths.
- `docs/POSTHOC_EXTERNAL_GENERALIZATION_PROTOCOL.md`: written before new
  outcome calculations. Preserve that chronology; later corrections must be
  recorded honestly. Broader target merging is explicitly not executed.
- `src/stats/external_generalization.py`: untested diagnostic/weighting/joint
  bootstrap implementation. Uses canonical matcher, official COCO match caches,
  independent detector-run draws reused across domains.
- `src/stats/run_external_generalization.py`: untested orchestration,
  source/provenance gates, write-once outputs, verify/replay modes.
- `src/stats/report_external_generalization.py`: untested aggregate plots/report.

No new output directory, bootstrap draws, aggregate result or generated report
has been created. No outcome analysis has run; no result interpretation or
manuscript edit is warranted yet. No new tests exist yet.

## Immediate resume issues

1. New `--mode preflight` FAILED in `local_annotations` with
   `ValueError: Unknown source annotation image or empty class`. Log:
   `tmp/external-generalization-v1/preflight.log`. Diagnose source ID versus
   canonical target ID representation (inspect `load_coco_targets` and
   `prepare_vindr.build_targets`) without printing restricted IDs/rows. This
   is not evidence of corrupt annotations or a historical scientific bug.
   Do not weaken hash, identity, duplicate or geometry checks to pass it.
2. Ruff formatting was applied only to the new files. `ruff check` still
   reports 20 issues, all in the report module: one unused loop variable and
   long string lines. Fix before execution; run formatting then lint.
3. Review/test all new logic. In particular, weighted AP uses weighted
   detection events, which has a different tie interpretation from canonical
   distinct-copy COCO AP for non-unit observation weights. It must remain
   clearly custom weighted AP. Verify unit-weight equality and independently
   hand-calculated non-unit examples. Document the bootstrap convention.
4. Replace the geometry validator's temporary literal category with the
   configured canonical category. Validate config/label assumptions as needed.
5. Add synthetic tests covering the complete request's edge cases, including
   IoU/score equality, competing assignments, duplicate predictions,
   overlapping alternative classes, invalid/duplicate annotations, empty
   outputs/negatives, ties, cap/floor limits, deterministic ordering, patient
   multiplicities, same checkpoints across domains, independent families,
   undefined draws, FP/reference count reconciliation and provenance failures.
6. Then rerun preflight; execute the priority error/overlap analysis followed
   by prevalence/change bootstrap only after tests pass. Use write-once output
   protection and archive failed evidence instead of silently overwriting it.
   Verify/replay actual results and visually inspect aggregate figures.

## Remaining work after implementation validation

- Complete the research audit mapping actual source functions and remaining
  methodological gaps; distinguish read code, hash checks and actual replays.
- Compare candidate-support audit against original per-run and conservative
  bounds; no further inference under this request.
- Write interpretation and source-verified contribution assessment. Existing
  Batch 53 numerical-path sensitivity already addresses one concern; reuse it.
- Precisely update canonical manuscript only for completed results, preserving
  original primary values/adverse runs. Extend claim bindings/semantic guards
  and publication inventory without altering the original 72-artifact inventory
  or any prior publication entries. Do not blindly run
  `scripts.build_publication_manifest`: its currently inspected code builds
  the earlier extension and may omit the later five Batch 53 records.
- Add exact README commands, tests, aggregate artifact registrations and
  relevant supplementary/limitations/decision records. Keep the unrelated
  README Wget hunk. If PDF remains unchanged, clearly label it the prior
  reviewed snapshot; do not claim it renders new Markdown evidence.
- Run requested portable/full authorized checks and original frozen statistics
  via `scripts.verify_frozen_external`, which resolves only two archived
  editorial baseline reads. Direct legacy statistics commands would compare
  live rewritten manuscript bytes against the original freeze.
- Record all actual outcomes and update CODEX/HANDOFF before final review.
  Full request specifies a seven-part final answer with VERIFIED,
  IMPLEMENTED BUT NOT EXECUTED, EXPLORATORY FINDING and UNRESOLVED distinctions.

## Literature located and verified online this session

Use primary sources and verify details when integrating; no bibliography has
yet changed. These support context, not claims about this study's new results:

- Zech et al. (2018), *Variable generalization performance of a deep learning
  model to detect pneumonia in chest radiographs: A cross-sectional study*,
  PLOS Medicine 15(11):e1002683, DOI
  [10.1371/journal.pmed.1002683](https://doi.org/10.1371/journal.pmed.1002683).
- Nguyen et al. (2022), *VinDr-CXR: An open dataset of chest X-rays with
  radiologist's annotations*, Scientific Data,
  [10.1038/s41597-022-01498-w](https://doi.org/10.1038/s41597-022-01498-w).
  Distinct local categories/global diagnoses do not validate their merging.
- Reinke et al. (2024), *Understanding metric-related pitfalls in image
  analysis validation*, Nature Methods 21:182–194,
  [10.1038/s41592-023-02150-0](https://www.nature.com/articles/s41592-023-02150-0).
- Bouthillier et al. (2021), *Accounting for Variance in Machine Learning
  Benchmarks*, MLSys; [official proceedings paper](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf).

Existing bibliography includes calibration/COCO/RSNA/CLAIM references; inspect
and reuse rather than adding duplicate entries. Additional primary FROC and
calibration literature checks remain. No claim of a first or causal discovery.
