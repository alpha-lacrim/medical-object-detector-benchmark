# V7 Q2 / VinDr Baseline Audit

**Audit date:** 2026-09-05  
**Batch:** 41 — Current-State Re-Audit and Manuscript Adjudication  
**Disposition:** prerequisite gate passed; stop for owner review before Batch 42  
**Scientific-change status:** no numerical result, threshold, prediction,
checkpoint, scientific claim, configuration, figure, or analysis was changed or
regenerated in this batch.

## 1. Executive adjudication

`report/paper_draft.md` remains the canonical editable journal manuscript.
Neither the greater length of
`report/Manuscript_FasterRCNN_vs_YOLO11s_LungOpacity.md` nor the existence of a
rendered PDF changes that decision. The current hierarchy is:

1. `report/paper_draft.md` — canonical editable journal manuscript and the only
   manuscript bound by `report/paper_claim_sources.yaml` and the current paper
   verifier.
2. `report/Manuscript_FasterRCNN_vs_YOLO11s_LungOpacity.md` — noncanonical long
   alternate manuscript; useful only as a possible later source of prose or
   Methods/Supplement detail after evidence review.
3. `report/A_Controlled_Comparative_Study___article.pdf` — read-only rendered
   article artifact derived overwhelmingly from the long alternate manuscript;
   it is not an editable or authoritative scientific source.
4. `report/report.md` — preserved historical/full technical report; it is not
   the current journal manuscript.

This agrees with the README document hierarchy, the canonical-manuscript field
in `results/scientific_artifact_manifest.json`, the manuscript path in
`report/paper_claim_sources.yaml`, and the scope of
`docs/REPORTING_CHECKLIST.md` and `docs/FINAL_SUBMISSION_AUDIT.md`.

No uniquely useful, verified technical detail was found in the long manuscript
that requires migration now. Its extra detail is predominantly expanded prose.
Any later migration must be selective, source-checked, and performed in a
manuscript-editing batch rather than copied wholesale.

## 2. Repository baseline and prerequisite gate

| Item | Observed state |
|---|---|
| Branch | `main` |
| HEAD | `42826df37468a1c0b28439a7120cc5f3d83f9168` (`add paper pdf file`) |
| Remote alignment | `origin/main` is the same SHA; ahead/behind is `0/0` |
| Tracked worktree at audit start | Clean |
| Staged state at audit start | Empty |
| Change from the latest handoff SHA | One later, PDF-only commit after `9d0c4789ac0776cca6aa67280d5fa4d8ce87300b`; no scientific result changed |
| V5 final-audit artifact | `docs/FINAL_SUBMISSION_AUDIT.md` present |
| Scientific verifier | `scripts/verify_scientific_artifacts.py` present and passing |
| Paper verifier | `scripts/verify_paper_claims.py` present and passing |
| Scientific manifest | `results/scientific_artifact_manifest.json` present |
| Checkpoint/release manifest | `results/checkpoint_release_manifest.json` present |
| Stop-gate result | No checkpoint missing, no checkpoint hash failure, and no material conflict with the completed V5 state |

The untracked publication/state/orchestration files present at the start were
preserved exactly:

- `AGENTS.md`, `BATCHES.md`, `BATCHES_V2.md`, `BATCHES_V3.md`,
  `BATCHES_V4.md`, `BATCHES_V5.md`, `BATCHES_V6.md`,
  `BATCHES_V7_Q2_VINDR.md`, `PROJECT_SPEC.md`, `CODEX.md`, and `HANDOFF.md`;
- `CHAT_RESPONSE_AUDIT&PRIORITY.md` and
  `docs/REVIEW_REMEDIATION_AUDIT.md`;
- pre-existing local aborted, failed, rejected, smoke, and orchestration records
  under `results/logs/faster_rcnn_rsna_seed17_benchmark_aborted-*`,
  `results/logs/faster_rcnn_rsna_seed17_smoke_pre-worker-adjustment/`,
  `results/logs/faster_rcnn_rsna_seed42_benchmark_aborted-redundant-timing/`,
  `results/logs/phase5_orchestration/`,
  `results/logs/phase16_orchestration/`,
  `results/logs/phase21_xai_sanity/`,
  `results/logs/phase22_acquisition_shifts/`, and the
  `results/logs/yolo11s_rsna_seed17_{benchmark,full,smoke}_*` directories.

The long manuscript and PDF are tracked at HEAD, not untracked. No file was
staged or committed during this audit.

## 3. Manuscript and article comparison

| Dimension | Canonical `paper_draft.md` | Long alternate manuscript | Rendered article PDF | Historical `report.md` |
|---|---|---|---|---|
| Title | Current controlled-study title | Same title | Same rendered title | Older “Controlled Comparison” report title |
| Abstract | Concise, numerically bound, and qualified | Same core results but uses stronger rhetoric such as “rigorously,” “substantially,” and “in stark contrast” | Follows the long version | No journal abstract |
| Research question | Current internal controlled-comparison question | Substantively the same question | Follows the long version | Older, broader question includes scenario preference and point-of-care framing |
| Contribution framing | Pipeline-level, multi-axis, and explicitly bounded | Inflates the same contribution with field-advancement and architecture-paradigm language | Inherits the long framing | Coursework/full-report framing |
| Methods detail | Sufficient current protocol and scope; linked to canonical artifacts | Mostly verbose paraphrase, with no uniquely necessary verified detail identified in this audit | Dense rendering of the long Methods | Contains useful historical implementation narrative, but also obsolete run-era details |
| Results | Current five-run/eligible-run results with explicit scope separation | Mostly reproduces current numbers, but mixes them with stronger claims | Reproduces the long Results | Partly stale: principal threshold/PR/FROC/Pareto presentation remains historical n=3 and lacks the full current synthesis |
| Statistical interpretation | Separates training-procedure bootstrap intervals from checkpoint-conditional permutation sensitivity | States the distinction initially, then overreaches with “statistically significant,” “minuscule,” “robust superiority,” and “definitively established” language | Inherits those overstatements | Preserves useful estimand discussion but belongs to an older evidence scope |
| Limitations | Most complete: dataset, reference, preprocessing, sampling, pipeline, metrics, calibration, DCA, robustness, XAI, statistics, compute, and governance | Compressed; omits several support/floor, DICOM, reproducibility, and release details | Inherits the compressed limitations | Shorter historical limitations |
| Declarations | Seven explicit `AUTHOR ACTION REQUIRED` placeholders, correctly unresolved | Improperly asserts no funding, no conflicts, waivers, contributor roles, PPI status, and availability; includes `[Professor's Name]` | Renders those unsupported declarations and author placeholders | No journal declaration section |
| References | 29 cited keys resolve against 32 bibliography entries; previously audited | Body uses 27 unique keys and omits both Vickers DCA citations used by the canonical paper | Renders 30 numbered references, including uncited/injected-looking entries relative to the long body | 19-key historical citation scope |
| Overclaiming | Best bounded of the four, while still provisional pending human review | Repeated “superiority,” “definitive,” “diagnostic coverage,” and architecture-family generalization; calls bounded FROC “threshold-independent” | Inherits the long overclaiming | Includes scenario recommendations that the canonical manuscript intentionally removed |
| Stale process terminology | Still contains internal `Batch`, `D-00x`, `Phase`, and course-project language scheduled for later cleanup | Contains `Batch 35`, `D-006`, and `D-008` process language | Inherits that process language | Contains older Batch/Phase/course-project language |

Additional defects in the long/PDF line include a Discussion subsection numbered
`4.4` after section 5.3, the false implication that grid-based FROC is
threshold-independent, and an availability hyperlink whose Markdown target is
a Google Search URL rather than the repository URL. These are reasons not to
promote the long manuscript; they are not repaired in this adjudication batch.

The phrase “internal testing” in the canonical paper is intentional CLAIM-safe
scope terminology, not stale process language. Removing actual Batch/decision-ID/
course terminology belongs to the later focused manuscript rewrite.

## 4. PDF rendering and provenance

The PDF was inspected as a rendered artifact and was not edited.

- File: `report/A_Controlled_Comparative_Study___article.pdf`
- SHA-256: `02d69dcafcd6cb81a069d7c6237750ba632641fc02dd480d2e32fc11d8ddcfc8`
- Git provenance: added alone by commit
  `42826df37468a1c0b28439a7120cc5f3d83f9168` on 2026-09-05.
- PDF metadata: 25 A4 pages, PDF 1.5, produced by
  `pdfTeX-1.40.29` with `LaTeX with hyperref`; creation/modification timestamp
  2026-09-04 18:05:43 Iran Standard Time; no author, title, subject, or keyword
  metadata; no forms, JavaScript, or embedded source files.
- Visual QA: all 25 rendered pages were reviewed. No obvious clipping,
  overlapping elements, broken glyphs, or missing-page defect was found. The
  article is dense and uses relatively small text; page 23 visibly contains the
  declaration/author placeholders.
- Text provenance: five-word-shingle comparison gives about 79.94% PDF-text
  containment in the long manuscript and only 11.43% in `paper_draft.md`
  (Jaccard about 71.64% versus 6.75%). The PDF therefore represents the long
  manuscript line, not the canonical paper or historical report.

Exact source provenance cannot be reconstructed from the repository: no LaTeX
source, conversion command, or build recipe is committed, and the PDF contains
no embedded source. It also adds page-one author text not present in the long
Markdown front matter. It must therefore remain a noncanonical rendered
artifact until a controlled build is supplied.

## 5. Checkpoint manifest audit

All ten checkpoint references in `results/checkpoint_release_manifest.json`
exist locally, remain Git-ignored/untracked as intended, match their recorded
SHA-256 values and byte sizes, match their bound config hashes, and agree with
`results/logs/phase5_evaluation/summary.json`. The manifest total is
962,924,817 bytes and its distribution state remains
`manifest_ready_binaries_not_published` with a null public URL.

| Detector | Seed | Bytes | Verified SHA-256 |
|---|---:|---:|---|
| Faster R-CNN | 17 | 173,412,170 | `9ec35c5d761f8e4bf7a43f7999f388ac1ffc0d533f62746409db280706dffab4` |
| Faster R-CNN | 42 | 173,412,170 | `c97813cf5dfe50b6eb074fe50cd4a870bb24e5a667bfaf8b94b37a844fd2b83d` |
| Faster R-CNN | 137 | 173,412,170 | `0d651d620c4106de296648960424326980ff13dd631a9baa120997590abc2a78` |
| Faster R-CNN | 271 | 173,412,170 | `fa7ef259b30d5ce19c954e3e30ddecf3c6d74d05e82c5d525eb499a2db2c998f` |
| Faster R-CNN | 314 | 173,412,170 | `e2147d0c45b1c7e369270a2d737e08b564fedd37cd88e2456ec13df03e4591a7` |
| YOLO11s | 17 | 19,172,819 | `65909164e82c1ef53c0d38e0d898d37bbbec5f46cb9f5cd029e76ba486c0371c` |
| YOLO11s | 42 | 19,172,691 | `7710372489e96c547aebd4c868663c33a8cf62f8ec48557049b7de8b2a6ab1c0` |
| YOLO11s | 137 | 19,173,331 | `b7677b5343b5d3930616f1b5a530f6005ded88dfc54f7e8fdecbe93e3a04fa19` |
| YOLO11s | 271 | 19,172,435 | `d89651bf4e94e1d0067b7b7e287cb95b58c5cd136b654a3a1b3a8a8147b3bd53` |
| YOLO11s | 314 | 19,172,691 | `9d4dfb4b6d5338aa3bd4d9eca8be47cd6d50481d575d4d6dc7b2e979351d86b9` |

## 6. Prediction-bundle inventory

### Held-out test bundles

All ten intended tracked test bundles are present under
`results/logs/phase5_evaluation/predictions/`, and each hash matches the Phase 5
summary.

| Detector | Seed | Bytes | Verified SHA-256 |
|---|---:|---:|---|
| Faster R-CNN | 17 | 730,551 | `d7dfecb06bf57008cc4b6a392e309e5101c723c66d86d796a38c358d04568c66` |
| Faster R-CNN | 42 | 336,469 | `83b6222c4cece06f8e25dfbb75df2b1d1b6ba44fd171ae6508ed68893f470b3b` |
| Faster R-CNN | 137 | 974,602 | `f9c4b18e57790b0751ae30487e7fddf0b9e3fded3a528a6a47be50a991c1d163` |
| Faster R-CNN | 271 | 295,192 | `0f8c5d2e615f65d337b74126c0226f2bd3f5fd069660b47756d2461d22e04a44` |
| Faster R-CNN | 314 | 187,058 | `b0d11508dd7319ea3524f0c05658df95bdf81c28d169592a22eeb98ea964e316` |
| YOLO11s | 17 | 83,158 | `1a5876f9f8ace7c5af8b3bf81f79ed3b38d9b55d8591d1da27e24be1bef8d384` |
| YOLO11s | 42 | 72,969 | `8d3804eb35f5ff1927c07cc35c246badb548f60d3d1475b9a643b6d34ed8323d` |
| YOLO11s | 137 | 56,926 | `3e62b8220181da56c0663defebf745ead5c0d56e7dba082a94adde0bec355b0b` |
| YOLO11s | 271 | 79,326 | `8790c679b7da1cbab0598f79a5e690aa764acacf2885a10379ff201f1047da5b` |
| YOLO11s | 314 | 78,010 | `ddd75b4d1b6b493bd0e53a384e58509a8b0cf0217abf323cd802b26661df33e4` |

### Validation bundles

Six tracked validation bundles are present under
`results/logs/phase14_threshold_selection/validation_predictions/`; their
hashes match the Phase 14 manifest.

| Detector | Seed | Bytes | Verified SHA-256 | State |
|---|---:|---:|---|---|
| Faster R-CNN | 17 | 750,230 | `355413196476a14d87865ea20edc946f1e1b56e8320200d072a516d622160763` | Present |
| Faster R-CNN | 42 | 347,446 | `6cc4b57a1cf7a789b5bb1a0af7d726db6417a024b65c1dea3b7bb1e69653afde` | Present |
| Faster R-CNN | 137 | 991,777 | `14142327d8482e5cb8700d02bc293011c43a6191755d72db729bea3170467966` | Present |
| Faster R-CNN | 271 | — | — | **Absent; validation inference needed** |
| Faster R-CNN | 314 | — | — | **Absent; validation inference needed** |
| YOLO11s | 17 | 89,165 | `7e42737d2d664acfb47a1bbb3552e4a21d0c44f44bde4b571e97d5e6b91cdab3` | Present |
| YOLO11s | 42 | 75,157 | `2b3431029e208040f9e41c5a2865f260cf987e03f1424e289e0adc96a2e91478` | Present |
| YOLO11s | 137 | 58,718 | `8d2caef6eb29cec81788ca3b9facf48c7bd6e44776074601a87df3dbcca38b89` | Present |
| YOLO11s | 271 | — | — | **Absent; validation inference needed** |
| YOLO11s | 314 | — | — | **Absent; validation inference needed** |

Thus seeds 271 and 314 lack validation predictions for both pipelines. This is
the expected D-007/n=3-selection boundary, not a lost frozen artifact. Creating
the four missing bundles is checkpoint inference only and belongs to Batch 43.

## 7. Historical n=3 and current n=5 operating-regime artifacts

The historical Phase 14 threshold-selection artifact is intact:

- validation seeds 17, 42, and 137 per detector;
- 99 thresholds from 0.01 through 0.99;
- maximum equal-run mean validation F1 with exact ties resolved toward the
  higher threshold;
- selected thresholds 0.69 for Faster R-CNN and 0.05 for YOLO11s;
- selection uses validation data only, followed by one-shot held-out-test
  application.

The current Phase 35 operating-regime sensitivity is also intact:

- test seeds 17, 42, 137, 271, and 314 per detector;
- the same frozen n=3-selected thresholds are applied unchanged;
- the analysis performs no training, inference, or threshold reselection;
- the versioned n=5 threshold, PR, FROC, fixed-threshold, and Pareto artifacts
  remain complete and hash-consistent with their frozen scientific inputs.

Three expected historical provenance snapshots point at mutable documentation
or routing paths whose current bytes have since changed:

1. Phase 14 records `configs/threshold_selection.yaml` as
   `f7ba5bae...`; those exact bytes survive in
   `configs/threshold_selection_n3_frozen.yaml`, while the live file now routes
   through the n=3 archive and hashes to `273e0cf2...`.
2. Phase 14 records `configs/threshold_sweep.yaml` as `6f472d17...`; those exact
   bytes survive in `configs/threshold_sweep_n3_frozen.yaml`, while the live
   archive-routed file hashes to `1343056a...`.
3. Phase 35 snapshots the then-current `docs/DECISION_LOG.md` as `ddb0fdf...`;
   the append-only log has legitimately changed since that run.

These are historical-generation snapshot semantics, not result or checkpoint
failures. All referenced n=3 outputs and prediction inputs and all current n=5
scientific artifacts pass the repository verifier. Frozen copies preserve the
exact historical config bytes; no old summary is rewritten.

## 8. Current FROC implementation and retained score floor

The current grid implementation is explicit and internally guarded:

- `configs/threshold_sweep_n5_sensitivity.yaml` defines the inclusive
  0.01–0.99 grid with 99 steps.
- `configs/froc_n5_sensitivity.yaml` defines FP/image budgets 0.125, 0.25, 0.5,
  1.0, and 2.0 with tolerance `1e-12`.
- `src/plot_froc_curves.py` validates complete/equal detector seed sets,
  threshold-table hashes and row counts, image/target counts, and recall
  consistency. At each seed and budget it chooses the maximum *observed*
  sensitivity among grid rows satisfying the budget. Ties prefer fewer false
  positives per image and then the higher threshold. It does not interpolate or
  extrapolate; aggregation is equal-run mean and sample SD.
- Regression tests require 594 historical n=3 rows, 990 current n=5 rows, all
  five seeds including 271, nonzero seed-271 behavior below 0.05, and the
  YOLO11s lower-grid-boundary status at threshold 0.01.
- `configs/evaluation.yaml` and the Phase 5 prediction provenance retain
  candidate scores down to `coco_minimum_score: 0.001`.

Consequently the current FROC artifact is valid only on the observed 0.01–0.99
grid, while the saved bundles retain candidates down to 0.001. Batch 42 is
still needed to construct exact-score FROC from unique emitted scores and test
whether the retained 0.001 floor truncates the observable frontier. No
lower-floor inference is authorized unless that offline audit first establishes
that the floor is limiting and the user approves the resulting protocol.

## 9. Work classification after this audit

### Analyses already complete

- five-run clean internal comparison with estimand-separated uncertainty;
- historical n=3 validation threshold selection and fixed test application;
- n=5 held-out-test grid threshold, official PR, FROC, fixed-threshold, and
  Pareto sensitivity;
- detection ECE/support sensitivity, recall-weighted F-beta sensitivity, and
  explicitly hypothetical raw-score loss analysis;
- detector-specific historical compute profiling;
- digital-corruption and acquisition/display sensitivity analyses;
- Grad-CAM localization and randomization/control analyses;
- scientific-artifact, claim-source, reporting, citation, checkpoint-release,
  and V5 final-submission audits.

### V7 analyses genuinely still needed

- **Batch 42:** exact-score FROC from the ten frozen test bundles; offline first.
- **Batch 43:** post-hoc five-run validation-threshold sensitivity after the
  four missing validation bundles are produced.
- **Batch 44:** aggregate publication-safe RSNA cohort age/sex and AP/PA
  characterization from authorized local original DICOMs.
- **Batch 45:** standardized repeated end-to-end timing on the intended RTX
  4060 laptop.
- **Batch 46:** focused canonical-manuscript rewrite/literature refresh,
  including removal of internal Batch/decision-ID/course language and stronger
  overclaiming controls.
- **Batches 47–48:** freeze and preflight the official VinDr-CXR external
  protocol and adapter, with only an explicitly bounded smoke evaluation.
- **Batch 49:** the sole major new experiment—run all ten frozen checkpoints on
  the official VinDr-CXR test set without training, fine-tuning, or threshold
  tuning.
- **Batch 50:** internal/external statistical and transportability synthesis.

### Frozen artifacts

The ten validation-selected checkpoints; all ten Phase 5 test prediction
bundles; the six Phase 14 validation bundles; selected thresholds 0.69/0.05;
historical n=3 artifacts and frozen configs; current n=5 operating-regime
artifacts; all completed calibration, robustness, acquisition, XAI, statistics,
and scientific/claim manifests remain frozen. They may be read or independently
verified but not silently overwritten or relabeled.

### Inference-only work

- four RSNA validation bundles for seeds 271 and 314 across both pipelines;
- repeated standardized timing with existing checkpoints;
- only if separately approved after the offline floor audit, lower-floor RSNA
  prediction export;
- tiny VinDr adapter smoke inference, followed later by the approved ten-model
  official VinDr test inference.

None requires or authorizes retraining.

### External work and data dependencies

- A human must personally obtain and authorize the official VinDr-CXR release
  and expose `VINDR_CXR_ROOT`; the agent cannot accept a data-use agreement or
  substitute an unofficial mirror.
- Batch 44 needs the authorized original RSNA DICOM root.
- Batch 45 needs the intended RTX 4060 laptop/software environment; external
  VinDr inference likewise needs suitable checkpoint-capable hardware.

### Human-author blockers

- funding/support;
- competing interests;
- ethics/data-use review and the correct institutional wording;
- consent applicability/waiver wording;
- final author list and CRediT contributions;
- final code/data/checkpoint availability statement and checkpoint publication
  decision/URL;
- patient/public involvement statement;
- later review of the frozen VinDr protocol before full external inference,
  plus final venue/citation metadata.

No declaration may be inferred from the long manuscript or rendered PDF.

## 10. Verification record

The following lightweight checks were run against the current repository:

```text
.venv\Scripts\python.exe scripts/verify_scientific_artifacts.py
Scientific artifact verification passed: 46 artifacts, 110 present inputs,
0 unavailable external/ignored inputs, 159 referenced result files.

.venv\Scripts\python.exe scripts/verify_paper_claims.py
Paper claim verification passed: 35 numerical claims and all configured
semantic guards.

.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
  --basetemp C:\Users\Pouyan\AppData\Local\Temp\codex-batch41-pytest-20260905
  tests/test_verify_scientific_artifacts.py
  tests/test_verify_paper_claims.py
  tests/test_threshold_selection.py tests/test_threshold_sweep.py
  tests/test_froc.py
21 passed.
```

The explicit temporary root avoids the known managed-Windows ACL on the
repository's configured `.pytest-tmp`; the initial collection using that
directory produced setup permission errors rather than test assertion
failures. The production verifiers and focused suite were repeated after the
documentation edits and passed with the same counts. `git diff --check` and an
explicit changed-path guard also passed; no manuscript, report, PDF, README,
result, config, source, or test path has a tracked diff.

## 11. Review checkpoint

Stop here for owner review. The next authorized batch is Batch 42; this audit
does not authorize manuscript rewriting, analysis regeneration, threshold
changes, new inference, external-data acquisition, or publication actions.
