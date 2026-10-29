# BATCHES_V7_Q2_VINDR.md — Q2 Manuscript Consolidation and VinDr-CXR External Transportability

For `Alpha-lacrim/medical-object-detector-benchmark`.

This sequence continues the completed V5 research-repair work and the subsequent release/manuscript maintenance sessions.

It is intentionally conservative.

The objective is NOT to expand the repository into a larger detector benchmark.

The objective is:

> Convert the existing internally rigorous RSNA comparison into a focused Q2-journal candidate, repair the few remaining high-value methodological/reporting issues using frozen artifacts wherever possible, and add exactly one major new scientific experiment: frozen zero-fine-tuning external transportability on VinDr-CXR.

The intended order is **Batches 41–52**.

Do not automatically execute more than one batch per Codex session.

---

# GLOBAL RULES FOR EVERY BATCH

## A. Standalone-session rule

Every batch will normally be pasted into a NEW Codex session in VS Code.

Therefore:

- Do not assume access to any previous Codex/chat session.
- Reconstruct the current project state from the repository.
- Do not assume an earlier batch succeeded merely because its number is lower.
- Execute only the batch pasted into the current session.
- Stop at the batch's review gate.

---

## B. Required startup sequence

Before doing scientific or manuscript work:

1. Read `AGENTS.md`.

2. Read the newest entry in `HANDOFF.md` first.
   Read older HANDOFF entries only when needed to resolve provenance/history.

3. Read `CODEX.md`, especially:
   - newest decisions;
   - current phase;
   - canonical files;
   - current risks;
   - relevant historical decisions.

4. Read the relevant section(s) of `PROJECT_SPEC.md`.
   `PROJECT_SPEC.md` remains the static source of truth.
   Do not edit it unless the user explicitly asks.

5. Read:
   - `docs/DECISION_LOG.md`
   - `docs/LIMITATIONS.md`
   - `docs/HYPOTHESES.md`
   - `docs/FINAL_SUBMISSION_AUDIT.md`
   where relevant to the batch.

6. Read the current:
   - `report/paper_draft.md`

7. Read every additional batch-specific file named in that batch.

8. Record:
   - current branch;
   - current HEAD;
   - working-tree status;
   - staged files;
   - relevant uncommitted changes.

9. Never destroy, reset, stash, stage, commit, or overwrite unrelated user changes without explicit authorization.

---

## C. Prerequisite gate

Before executing the substantive work of each batch:

Verify all prerequisite earlier-batch state from ACTUAL repository evidence.

Do not rely only on:
- HANDOFF prose;
- CODEX prose;
- batch numbering.

Where relevant, verify:
- required artifacts exist;
- hashes/provenance match;
- expected configs/scripts exist;
- relevant tests pass;
- the decision-log entry exists;
- canonical/superseded status is consistent.

If prerequisites are missing, incomplete, contradictory, or represented only by prose when artifacts should exist:

1. do not continue;
2. document the discrepancy;
3. add a HANDOFF entry;
4. stop for user review.

---

## D. Existing scientific boundary

Preserve the completed V5 corrections.

Do not redo or reverse them unless a genuine error is found.

In particular, the repository already contains work addressing:
- training-procedure versus checkpoint-conditional estimands;
- independent detector-run resampling;
- F-beta terminology;
- invalid conventional raw-score DCA;
- XAI sanity terminology;
- acquisition/DICOM interpretation;
- D-ECE support/sensitivity;
- five-run operating-regime sensitivity;
- scientific-artifact verification;
- manuscript-claim verification;
- reporting/citation/hypothesis audits.

New V7 work must build on these results rather than duplicating them.

---

## E. Model/training scope

Do NOT automatically:

- retrain Faster R-CNN;
- retrain YOLO11s;
- add additional training seeds;
- replace any existing checkpoint;
- remove seed 271;
- add additional detector families;
- run canonical-YOLO retraining;
- add new augmentation experiments.

All five attempted runs per detector remain part of the study.

If an endpoint is mathematically undefined for a run:
- report `NA`;
- explain why;
- do not remove the run;
- do not impute zero unless zero is the metric's defined value.

---

## F. Test-set integrity

Never use RSNA internal-test labels for:
- model selection;
- threshold selection;
- calibration fitting;
- preprocessing tuning;
- NMS tuning;
- parameter selection.

Never use VinDr test annotations for:
- model fine-tuning;
- threshold selection;
- calibration fitting;
- model selection;
- ontology optimization after seeing model results;
- endpoint selection after seeing model results.

---

## G. Historical artifact preservation

Committed/frozen artifacts are evidence, not prose to be defended.

If an analysis is extended or corrected:
- preserve the historical artifact;
- create a new versioned artifact/config;
- mark historical/superseded status explicitly where needed.

Never silently overwrite historical numerical provenance.

---

## H. Configuration/no-hardcoding rule

Follow the existing repository rule that:
- dataset roots;
- class names;
- thresholds;
- metric parameters;
- hyperparameters;
- file paths

must be configuration-driven where appropriate.

Do not introduce publication-critical values only as inline constants.

Prefer versioned `configs/*.yaml` files consistent with existing repository conventions.

External dataset roots should use configuration/environment indirection such as:

`VINDR_CXR_ROOT`

rather than tracked machine-specific paths.

---

## I. Reproducibility command rule

For every new scientific result that may enter the manuscript:

- provide a deterministic repository command;
- document it in `README.md` or the canonical reproducibility command index;
- bind it to the appropriate config;
- record inputs/provenance;
- add tests for newly introduced scientific logic.

Do not imply that standard CI regenerates GPU/data-dependent experiments when it does not.

A new manuscript number is not final until it has a traceable source or deterministic verification path.

---

## J. Scientific interpretation rules

Do not make architecture-family causal claims.

The comparison remains between:
- the disclosed Faster R-CNN pipeline;
- the disclosed YOLO11s pipeline.

Use:
- `lung-opacity localization`

rather than:
- `pneumonia diagnosis`

when describing the model target.

Do not add unsupported:
- clinical deployment;
- clinical safety;
- clinical workflow utility;
- prospective validation;
- state-of-the-art
claims.

---

## K. CODEX.md update rule

At the end of a completed batch, update `CODEX.md` only with durable project state, including where relevant:

- completed scientific decision;
- new canonical/superseded artifact;
- new config/script/result;
- updated phase;
- durable limitation/risk.

Preserve superseded decisions.

Do not copy the full session narrative into CODEX.md.

---

## L. HANDOFF.md update rule

`HANDOFF.md` remains append-only.

At the end of every batch:

- prepend exactly one new session entry below the existing template;
- use the repository's existing HANDOFF format;
- do not rewrite, summarize, reorder, compact, or delete older entries.

The entry must state:
- what was done;
- what remains incomplete/next;
- what requires user review;
- files touched.

Include important Git/test/artifact state required by the next standalone session.

---

## M. Local-only orchestration files

Preserve the repository's existing local-only policy.

Do not automatically stage, commit, push, untrack, or alter Git policy for:

- `AGENTS.md`
- `CODEX.md`
- `HANDOFF.md`
- `PROJECT_SPEC.md`
- `BATCHES*.md`
- established local audits/logs

unless the user explicitly requests it.

Do not rewrite `.gitignore` or `.git/info/exclude` merely to implement this batch if the existing local policy already works.

---

## N. Decision log

Update `docs/DECISION_LOG.md` whenever a batch changes:
- canonical-document status;
- primary/secondary analysis status;
- inferential interpretation;
- external ontology;
- frozen external protocol;
- threshold policy;
- external estimand.

---

## O. Commit/push rule

Do not commit, push, tag, or publish unless explicitly instructed in the current session.

Leave reviewed changes available for the user to inspect.

---

# CURRENT CANONICAL HIERARCHY TO VERIFY IN BATCH 41

Expected current hierarchy:

- `report/paper_draft.md`
  = canonical editable journal manuscript.

- `report/Manuscript_FasterRCNN_vs_YOLO11s_LungOpacity.md`
  = newly available historical/detail-rich manuscript candidate/reference, not automatically canonical.

- `report/report.md`
  = historical technical report.

- `report/A_Controlled_Comparative_Study___article.pdf`
  = rendered article artifact/submission preview.

- `results/`
  = numerical source of truth.

- `docs/`
  = methodology/audit/provenance record.

Batch 41 must verify this from the current repository rather than assuming it.

---

# EXPLICIT V7 NON-GOALS

Do not automatically add:

- additional detectors;
- additional seeds;
- new training;
- canonical YOLO retraining;
- larger XAI experiments;
- more corruption experiments;
- a large new calibration study;
- prospective clinical testing;
- reader studies.

The only major new V7 experiment is VinDr-CXR frozen external transportability.

---

# BATCH 41 — Current-State Re-Audit and Manuscript Adjudication

This is a standalone Codex session.

Follow all Global Rules above.

## PURPOSE

Establish the exact post-V5/current repository state before changing any scientific analysis.

Adjudicate the newly available long manuscript and rendered article against the current canonical paper.

No numerical scientific result may be changed in this batch.

## PREREQUISITE GATE

Verify:
- V5 Batch 38/final-audit artifacts exist;
- current scientific and paper verifiers are present;
- current Git state is identifiable;
- all local-only orchestration files are preserved.

## INPUTS

Read at minimum:

- `report/paper_draft.md`
- `report/Manuscript_FasterRCNN_vs_YOLO11s_LungOpacity.md`
- `report/report.md`
- `report/A_Controlled_Comparative_Study___article.pdf` if available locally
- `README.md`
- `docs/FINAL_SUBMISSION_AUDIT.md`
- `docs/DECISION_LOG.md`
- `docs/REPORTING_CHECKLIST.md`
- `report/paper_claim_sources.yaml`
- current scientific/checkpoint manifests.

## TASKS

1. Record:
   - branch;
   - HEAD;
   - tracked status;
   - staged state;
   - untracked publication/orchestration files.

2. Compare the three manuscript/article forms for:
   - title;
   - abstract;
   - research question;
   - contribution framing;
   - Methods detail;
   - Results;
   - statistical interpretation;
   - limitations;
   - declarations;
   - references;
   - overclaiming;
   - stale internal process terminology.

3. Determine which file should remain the canonical editable journal manuscript.

4. Default expectation:
   `report/paper_draft.md`.

5. Do not promote the long manuscript merely because it contains more detail.

6. If useful technical detail exists only in the long manuscript:
   record it as material that may later migrate into Methods/Supplement;
   do not copy it automatically in this batch.

7. Inspect the PDF as a rendered article artifact:
   - determine its source/provenance if possible;
   - determine whether it represents paper_draft or another source;
   - do not manually edit the PDF.

8. Verify all ten checkpoint references and hashes from the existing release/checkpoint manifest.

9. Inventory:
   - five Faster R-CNN test prediction bundles;
   - five YOLO11s test prediction bundles;
   - validation prediction bundles for all five intended seeds.

10. Specifically determine whether validation predictions exist for seeds 271 and 314 for both pipelines.

11. Verify the historical n=3 threshold-selection artifact and current n=5 operating-regime sensitivity artifact.

12. Verify current FROC threshold/grid implementation and retained candidate score floor.

13. Create:
   `docs/V7_Q2_VINDR_BASELINE_AUDIT.md`

14. Include:
   - canonical manuscript decision;
   - existing analyses that are already complete;
   - V7 analyses genuinely still needed;
   - frozen artifacts;
   - inference-only work;
   - external work;
   - human-author blockers.

15. Add a DECISION_LOG entry confirming the V7 canonical manuscript hierarchy if needed.

## SCIENTIFIC RULES

Do not:
- modify results;
- regenerate analyses;
- alter thresholds;
- change manuscript scientific claims.

This is an adjudication/baseline batch.

## USER ACTION REQUIRED

Stop if:
- a checkpoint is missing;
- a recorded checkpoint hash fails;
- current repository state conflicts materially with the assumed completed V5 state.

Report exact evidence.

## COMPLETION

Run existing lightweight:
- scientific verifier;
- paper verifier;
- relevant integrity checks.

Update CODEX.md and prepend one HANDOFF entry.

Stop for review.

---

# BATCH 42 — Exact-Score FROC Lower-Bound Repair

This is a standalone Codex session.

Follow all Global Rules above.

## PURPOSE

Repair the remaining operating-frontier weakness without repeating the already completed five-run operating-regime analysis.

Historical FROC used a fixed score grid bounded at 0.01.

Because YOLO reaches that boundary, the paper must not treat the historical grid as the complete low-score frontier.

No retraining is allowed.

## PREREQUISITE GATE

Verify Batch 41 baseline artifacts.

Verify the existing Batch-35 five-run FROC/operating-regime artifacts remain intact.

## INPUTS

Read:
- FROC implementation;
- FROC configs;
- FROC tests;
- `docs/FROC_ANALYSIS.md`;
- `docs/THRESHOLD_ANALYSIS.md`;
- n=3 and n=5 FROC artifacts;
- prediction-bundle provenance;
- manuscript FROC claims.

## TASKS

1. Reproduce/verify the historical grid-based result before implementing anything new.

2. Record:
   - threshold grid;
   - lower/upper limits;
   - candidate-score floor;
   - matching IoU;
   - max detections/image;
   - seed scope;
   - FROC budgets.

3. Create a new versioned config for exact-score FROC following current repository naming conventions.

4. Do not hardcode publication parameters in the new script.

5. Implement exact empirical operating thresholds using the unique emitted confidence scores from each frozen prediction bundle.

6. Include appropriate endpoint/sentinel behavior.

7. Keep unchanged:
   - images;
   - annotations;
   - matching;
   - class;
   - NMS;
   - max detections;
   - prediction bundles.

8. Compute:
   - per-run exact-score FROC;
   - five-run aggregate sensitivity;
   - the same prespecified FP/image budgets already used in the manuscript.

9. Produce a comparison:
   - historical 0.01–0.99 grid;
   - exact-score frontier.

10. Determine whether the frozen prediction floor, expected around 0.001, still truncates the observable low-score frontier.

11. If the candidate floor itself becomes the limiting boundary:
    - do not silently rerun checkpoint inference;
    - document the issue;
    - determine a technically safe lower candidate floor supported by both adapters;
    - prepare a proposed inference-only sensitivity protocol;
    - stop for user approval before performing substantial new inference.

12. Add tests for:
    - deterministic threshold ordering;
    - all five runs included;
    - seed 271 retained;
    - endpoint behavior;
    - expected sensitivity monotonicity as threshold relaxes;
    - expected FP/image monotonicity as threshold relaxes.

13. Investigate any monotonicity failure.

14. Create versioned outputs and provenance.

15. Update:
    - `docs/FROC_ANALYSIS.md`;
    - `docs/THRESHOLD_ANALYSIS.md`;
    - `docs/LIMITATIONS.md`;
    - artifact/claim manifests as applicable;
    - only those manuscript sentences made factually stale.

16. Replace wording such as:
    - “full continuum”;
    - “exhaustive continuum”;
    - “threshold-independent FROC.”

17. Prefer:
    - “observed exact-score frontier”;
    - “prespecified FP/image operating budgets.”

18. Add the exact reproduction command to README/reproducibility documentation.

## SCIENTIFIC RULES

If results below 0.01 weaken or reverse a previous conclusion, report that.

Never select a new candidate floor because it favors either detector.

## USER ACTION REQUIRED

Only if lower-floor checkpoint inference is genuinely necessary.

Report:
- proposed floor;
- exact models/images;
- expected generated artifacts;
- reason.

Stop before running it.

## COMPLETION

Run:
- focused FROC tests;
- full relevant tests;
- artifact verifier;
- paper verifier where claims changed.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 43 — Five-Run Validation Threshold-Selection Sensitivity

This is a standalone Codex session.

Follow all Global Rules above.

## PURPOSE

Do NOT repeat the existing five-run test-side operating-regime sensitivity.

The missing question is specifically:

> If threshold selection itself uses validation evidence from all five retained runs rather than the historical three runs, does the selected operating point or test interpretation materially change?

The historical n=3 selection remains frozen provenance.

No training is allowed.

## PREREQUISITE GATE

Verify:
- historical n=3 selected thresholds exist;
- Batch-35 n=5 test-side operating analysis exists;
- required checkpoints exist;
- Batch 41 identified validation prediction availability correctly.

## TASKS

1. Reproduce the historical selection rule exactly:
   - validation only;
   - seeds 17, 42, 137;
   - original threshold grid;
   - original objective;
   - averaging method;
   - tie rule.

2. Verify the historical detector thresholds before continuing.

3. Determine whether validation predictions exist for seeds 271 and 314 for each detector.

4. If they do not:
   run validation inference only using:
   - exact frozen best checkpoint;
   - original validation split;
   - original preprocessing;
   - original adapter;
   - original candidate floor;
   - original NMS;
   - original max detections;
   - original coordinate logic.

5. Store/hash/provenance-bind new validation prediction bundles.

6. Do not use test labels to validate or alter them.

7. Create a versioned config for:
   `post-hoc n=5 validation threshold-selection sensitivity`.

8. Use the SAME historical selection rule/grid initially.
   The intended change is run coverage, not a simultaneous objective redesign.

9. Select a detector-specific threshold from all five validation runs.

10. Apply the resulting thresholds unchanged to all five internal-test prediction bundles.

11. Compare:
    - historical n=3 threshold;
    - post-hoc n=5 threshold;
    - test precision;
    - recall;
    - F1;
    - FP/image;
    - detection count;
    - run-level variability.

12. Explicitly classify each conclusion:
    - unchanged;
    - strengthened;
    - weakened;
    - reversed.

13. Keep the existing historical n=3 artifacts unchanged.

14. Add tests preventing:
    - test-set threshold selection;
    - seed-271 exclusion;
    - historical artifact overwrite.

15. Update:
    - `docs/THRESHOLD_ANALYSIS.md`;
    - `docs/DECISION_LOG.md`;
    - `docs/LIMITATIONS.md`;
    - relevant manuscript sensitivity wording;
    - provenance/manifests.

16. Add exact reproduction command(s) to README/reproducibility documentation.

## SCIENTIFIC RULES

Never call the n=5 threshold prospectively frozen.

Use:
> post-hoc validation sensitivity.

## USER ACTION REQUIRED

If any required checkpoint or validation source data are missing:
stop.

Do not retrain.

## COMPLETION

Run relevant tests/verifiers.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 44 — RSNA Cohort Characteristics

This is a standalone Codex session.

Follow all Global Rules above.

## PURPOSE

Improve medical-AI cohort reporting with existing RSNA metadata.

This is NOT intended to become a new fairness paper.

No model training is allowed.

## PREREQUISITE GATE

Verify the immutable 5,000-study split and patient mapping.

## TASKS

1. Locate the original RSNA DICOM root without hardcoding a local path.

2. Prefer an environment/config mechanism such as:
   `RSNA_DICOM_ROOT`.

3. Map source DICOMs to the existing selected-study/split manifests without changing membership.

4. Inspect actual DICOM tags.

5. Extract, where reliable:
   - age;
   - sex;
   - AP/PA projection.

6. Validate:
   - age syntax/units;
   - impossible/out-of-range ages;
   - missing age;
   - sex categories/missingness;
   - projection categories/missingness.

7. Produce aggregate publication-safe characteristics for:
   - train;
   - validation;
   - internal test;
   - total.

8. Include:
   - studies;
   - patient groups;
   - opacity-positive studies;
   - bounding boxes;
   - age summary;
   - age missingness;
   - sex counts/percentages;
   - sex missingness;
   - AP/PA counts/percentages;
   - projection missingness.

9. Do not commit:
   - DICOMs;
   - raw patient rows;
   - patient identifiers;
   - patient-level demographic records.

10. Only aggregate publication-safe outputs may be tracked.

11. Do not add inferential fairness claims.

12. If easy and adequately supported, optional descriptive subgroup summaries may be produced, but keep them supplementary/descriptive unless separately justified.

13. Correct manuscript language saying demographics were unavailable if successful.

14. Update:
   - cohort table;
   - Methods;
   - cohort Results;
   - Limitations;
   - reporting checklist where relevant.

15. Add reproducible aggregate-generation command to README/reproducibility documentation.

## USER ACTION REQUIRED

If Codex cannot locate the original RSNA DICOMs:

stop and ask the user to set/provide:

`RSNA_DICOM_ROOT`

Do not guess the path.

## COMPLETION

Verify aggregate totals against the immutable split.

Run tests.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 45 — Standardized End-to-End Inference Timing

This is a standalone Codex session.

Follow all Global Rules above.

## PURPOSE

Replace the manuscript's main asymmetric implementation-timing comparison with a matched timing boundary.

Preserve historical compute profiling.

No training.

## PREREQUISITE GATE

Verify historical timing code/results and the intended publication hardware recorded in project state.

## TASKS

1. Reproduce/document the historical timing boundary.

2. Preserve historical artifacts.

3. Implement a versioned standardized timing protocol beginning from the same conceptual state for both models.

Primary boundary should include for BOTH detectors:

- decoded source image already in host memory;
- resize/letterbox;
- tensor conversion;
- host-to-device transfer as applicable;
- model forward;
- postprocessing/NMS;
- coordinate restoration.

Exclude disk I/O from both.

4. Use config-driven:
   - image subset;
   - warm-up count;
   - batch size;
   - repetitions.

5. Use batch size 1.

6. Use explicit CUDA synchronization around timed boundaries.

7. Use an identical deterministic image subset.

8. Perform at least three complete repetitions.

9. Report:
   - total elapsed time;
   - FPS;
   - median image latency;
   - IQR or similarly robust dispersion;
   - hardware;
   - CUDA/framework versions;
   - warm-up;
   - subset size.

10. Do not treat timing repetitions as independent biological/training replicates.

11. Verify timing-path predictions agree with ordinary inference for:
    - detection count;
    - box coordinates;
    - scores
    within appropriate deterministic/numerical tolerances.

12. Keep parameter counts.

13. Retain profiler GFLOPs only as clearly incomplete profiler-registered operations.

14. Do not headline the historical approximate 21× operation count as an architecture-level fact.

15. Update:
    - compute docs;
    - table/figure;
    - manuscript;
    - Limitations;
    - provenance.

16. Add the exact timing command to README.

## USER ACTION REQUIRED

Publication timing must be produced on the intended reporting hardware.

If the active Codex environment is NOT the project's RTX 4060 Laptop GPU environment:

- finish the code/tests/config;
- give the user the exact command;
- do NOT generate final publication timing values;
- stop.

The user runs the command locally and leaves/returns the generated artifacts for the next session.

## COMPLETION

Run timing tests and relevant verifiers.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 46 — Focus the Internal Q2 Manuscript and Update Related Work

This is a standalone Codex session.

Follow all Global Rules above.

## PURPOSE

Create the clean internal-paper state before external VinDr integration.

The goal is to make the paper SMALLER and more focused.

## PREREQUISITE GATE

Verify scientific outputs from Batches 42–45 or document why an optional item remains incomplete.

## CANONICAL MANUSCRIPT

Use:
`report/paper_draft.md`

unless Batch 41 explicitly proved another file should be canonical.

Do not rewrite `report/report.md`.

Do not use the long Manuscript file as the editing base.

## CENTRAL INTERNAL THESIS

Frame the paper around:

> Cross-detector conclusions can depend materially on operating-point definition. Under a leakage-aware common evaluation protocol, ranking performance, shared raw thresholds, detector-specific validation-selected operating points, stochastic training variability, false-positive operating regimes, and measured implementation efficiency describe different properties of the evaluated pipelines.

Do not claim that this paper first discovered detector score-scale mismatch.

## TASKS

1. Update Introduction/Related Work using current primary/authoritative sources.

2. Verify literature rather than trusting old prose.

3. Include relevant modern work on:
   - detector calibration/threshold pitfalls;
   - recent direct RSNA modern-detector comparisons;
   - CLAIM 2024;
   - primary RSNA dataset/challenge methodology.

4. Prefer DOI/publisher/official sources.

5. Keep central:
   - patient-disjoint split;
   - common evaluator;
   - five retained runs;
   - AP/PR;
   - shared-threshold behavior;
   - validation-selected thresholds;
   - exact-score FROC;
   - training-procedure uncertainty;
   - standardized compute.

6. Demote to secondary/supplement:
   - D-ECE;
   - Grad-CAM;
   - common corruptions;
   - acquisition-shift stress;
   - F-beta;
   - hypothetical loss;
   - internal project decision archaeology.

7. Do NOT launch another calibration research project.

8. Describe D-ECE as:
   - detection-level;
   - emitted-detection population;
   - support/binning dependent;
   - descriptive;
   - not clinical-risk calibration.

9. Remove journal prose containing:
   - Batch numbers;
   - D-xxx internal project IDs;
   - course-project language;
   - definitive/decisive/overwhelming/fundamental-fallacy style language;
   - architecture-family causal claims.

10. Preserve repository provenance documents unchanged where they legitimately use batch/decision IDs.

11. Keep unresolved declarations as:
    `AUTHOR ACTION REQUIRED`.

12. Never invent:
    - ethics approval/waiver;
    - consent;
    - funding;
    - COI;
    - CRediT roles;
    - patient/public involvement.

13. Leave title/abstract somewhat provisional because external results are not yet known.

14. Update claim bindings when manuscript wording changes.

15. Update citation/reporting audits as necessary.

## USER ACTION REQUIRED

Only for factual author declarations if the user chooses to resolve them now.

Otherwise keep placeholders.

## COMPLETION

Run:
- paper verifier;
- scientific verifier;
- bibliography checks;
- tests affected by editing.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 47 — Freeze the VinDr-CXR External Protocol

This is a standalone Codex session.

Follow all Global Rules above.

NO full detector inference is allowed in this batch.

## PURPOSE

Pre-specify the external experiment before seeing VinDr performance.

This batch is the scientific firewall against post-hoc ontology/threshold/endpoint tuning.

## PREREQUISITE GATE

Verify Batch 46 manuscript state and current internal analysis definitions.

Verify VinDr access is lawful/authorized before accessing restricted files.

## DATASET POLICY

Use the official VinDr-CXR release.

Primary external population:
the official 3,000-image test set with consensus annotations, subject to verification from the actual release documentation.

Do not use VinDr training data for:
- fine-tuning;
- threshold selection;
- calibration fitting;
- model selection;
- hyperparameter tuning.

## PRIMARY EXTERNAL TARGET

Use the exact local VinDr finding:

`Lung opacity`

Do not automatically merge:
- Consolidation;
- Infiltration;
- Atelectasis;
- ILD;
- global Pneumonia;
- other findings.

## TERMINOLOGY

Use:
- `external testing`;
- `cross-dataset transportability`;
- `cross-annotation-ontology transportability`.

Do not call it:
- identical-task external validation.

## TASKS

1. Verify:
   - dataset version;
   - official test definition;
   - annotation schema;
   - redistribution/derived-artifact constraints.

2. Create versioned config:
   `configs/...vindr_external...yaml`
   following existing naming conventions.

3. Dataset root must come from configuration/environment indirection such as:
   `VINDR_CXR_ROOT`.

4. Create:
   `docs/VINDR_EXTERNAL_PROTOCOL.md`.

5. Pre-specify:
   - dataset version;
   - split;
   - strict ontology;
   - DICOM preprocessing;
   - candidate-score floor;
   - max detections/image;
   - NMS;
   - IoU matching;
   - AP endpoints;
   - FROC budgets;
   - threshold-transport endpoints;
   - score-distribution summaries;
   - statistical observational unit;
   - run aggregation;
   - planned tables/figures;
   - prohibited tuning.

6. Primary external endpoints:
   - AP@0.50;
   - AP@0.50:0.95;
   - exact-score FROC;
   - sensitivity at the same prespecified internal FP/image budgets.

7. Pre-specify score summaries:
   - detection count;
   - min;
   - quantiles;
   - median;
   - mean;
   - max.

8. Primary threshold transport:
   apply the HISTORICAL RSNA validation-selected detector thresholds unchanged to VinDr.

9. Secondary threshold transport:
   if Batch 43 produced n=5 validation-selected thresholds, apply them unchanged as a post-hoc sensitivity.

10. Never select a VinDr-specific threshold.

11. Determine whether a defensible patient-group identifier exists.

12. If patient identity cannot be established:
    pre-specify study/image-level resampling;
    do not invent patient grouping.

13. Add a DECISION_LOG entry freezing:
    - target ontology;
    - endpoints;
    - no-tuning rule;
    - threshold policy;
    - observational unit.

14. Hash/version the protocol/config before full inference.

15. Add planned commands to README, but do not run the full experiment.

## USER ACTION REQUIRED

The user must personally obtain authorized VinDr-CXR access and download the official release.

Codex must not:
- accept DUAs on behalf of the user;
- bypass authentication/access controls;
- download unauthorized restricted data.

The user should expose the local path, for example:

`VINDR_CXR_ROOT=/local/path/to/vindr-cxr`

The user must review `docs/VINDR_EXTERNAL_PROTOCOL.md` before Batch 49.

## COMPLETION

No full detector results may have been inspected.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 48 — Build and Validate the VinDr External Adapter

This is a standalone Codex session.

Follow all Global Rules above.

Do NOT change the frozen Batch-47 protocol based on detector performance.

Do NOT run the complete ten-checkpoint study.

## PURPOSE

Create and validate deterministic VinDr ingestion and annotation conversion compatible with the existing common evaluator.

## PREREQUISITE GATE

Verify:
- frozen Batch-47 protocol/config;
- its hash/version;
- authorized local dataset path;
- no full external performance analysis has been run.

## TASKS

1. Load VinDr root through config/environment, never a hardcoded personal path.

2. Verify the official test-set file inventory.

3. Verify the annotation schema.

4. Build a deterministic official-test manifest.

5. Count:
   - total test studies;
   - strict `Lung opacity` positive studies;
   - strict `Lung opacity` boxes;
   - strict-target zero-box studies.

6. Treat every test study without a strict `Lung opacity` box as a negative for this exact target, even when other VinDr findings are present.

7. Implement deterministic DICOM ingestion consistent with the repository's validated preprocessing principles.

8. Do not assume VinDr DICOM semantics are identical to RSNA.

9. Audit actual:
   - Photometric Interpretation;
   - dimensions;
   - pixel representation;
   - relevant rescale/window fields;
   - orientation/projection where needed.

10. Convert official boxes into the canonical evaluator format.

11. Validate:
    - IDs;
    - dimensions;
    - x/y coordinate order;
    - bounds;
    - positive box area;
    - duplicates;
    - resize mapping;
    - inverse coordinate restoration.

12. Add unit/integration tests for:
    - ontology filtering;
    - negative-study behavior;
    - DICOM polarity;
    - coordinate conversion;
    - deterministic preprocessing.

13. Do not commit DICOMs.

14. Do not redistribute restricted annotation data if prohibited.

15. Commit/track only permitted derived artifacts.

16. A tiny technical smoke inference is allowed only to verify execution.

17. Do not interpret performance from that smoke run.

18. Do not alter the frozen protocol because predictions appear unexpectedly good/bad.

19. Add exact adapter/preflight command to README.

## USER ACTION REQUIRED

Stop if:
- dataset version is wrong;
- files are incomplete;
- authorization is missing;
- annotation schema differs materially from the frozen protocol.

## COMPLETION

Produce a preflight summary with:
- test count;
- positive count;
- box count;
- ontology;
- preprocessing;
- candidate floor;
- evaluator parameters.

Update CODEX.md and prepend one HANDOFF entry.

STOP FOR USER REVIEW.

Do not proceed to Batch 49 automatically.

---

# BATCH 49 — Frozen Ten-Checkpoint VinDr External Inference

This is a standalone Codex session.

Follow all Global Rules above.

No training.

No fine-tuning.

No external threshold tuning.

## PURPOSE

Run the sole major new V7 scientific experiment:

> all ten frozen RSNA-trained checkpoints evaluated without adaptation on the official VinDr-CXR test set.

## PREREQUISITE GATE

Before any full inference verify:

1. Batch-47 protocol exists and is frozen/hash-bound.

2. Batch-48 adapter tests/preflight pass.

3. The user has reviewed/approved proceeding.

4. All ten checkpoint hashes match expected identities.

5. Dataset version/test set matches the frozen protocol.

If any condition fails:
stop.

## CHECKPOINTS

Use all retained best checkpoints for seeds:

- 17
- 42
- 137
- 271
- 314

for both:
- Faster R-CNN;
- YOLO11s.

Never exclude seed 271.

## TASKS

1. Run all ten checkpoints under the frozen protocol.

2. Do not modify after seeing results:
   - input size;
   - preprocessing;
   - candidate floor;
   - NMS;
   - max detections;
   - target ontology;
   - checkpoint;
   - thresholds.

3. Save run-level predictions where permitted.

4. Record:
   - checkpoint hash;
   - config hash;
   - protocol hash;
   - dataset version;
   - software environment;
   - execution metadata.

5. Compute per run:
   - AP@0.50;
   - AP@0.50:0.95;
   - exact-score FROC;
   - prespecified FROC sensitivities;
   - confidence/score-distribution summaries.

6. Apply historical RSNA detector-specific validation thresholds unchanged.

7. Report:
   - precision;
   - recall;
   - F1;
   - FP/image;
   - detections/image;
   - percentage of studies producing detections.

8. If available, apply Batch-43 n=5 RSNA thresholds unchanged as SECONDARY sensitivity.

9. Clearly distinguish:
   - historical n=3 threshold transport;
   - post-hoc n=5 threshold transport.

10. Never create a VinDr-optimized threshold.

11. Preserve adverse results.

12. If:
    - YOLO overtakes Faster R-CNN;
    - ranking reverses;
    - both collapse;
    - threshold transport fails;
    - seed 271 behaves unusually;
    report exactly that.

13. If a technical implementation bug is found:
    - stop;
    - document;
    - correct only the bug;
    - preserve superseded external artifacts;
    - do not opportunistically change protocol choices.

14. Add exact execution command to README.

## USER ACTION REQUIRED

If Codex cannot run the full GPU workload on the intended local machine:

- prepare exact config/command;
- user runs it locally;
- do not manually edit result artifacts;
- next session verifies generated hashes/provenance before interpretation.

## COMPLETION

Run artifact verification.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 50 — VinDr Statistics and Internal-vs-External Transportability

This is a standalone Codex session.

Follow all Global Rules above.

No ontology or threshold tuning is allowed.

## PURPOSE

Determine whether ranking and internally selected operating points transport in the same way.

## PREREQUISITE GATE

Verify complete ten-checkpoint external artifacts from Batch 49.

Verify protocol/config hashes match Batch 47.

## CENTRAL QUESTION

> Do detector ranking and RSNA-selected operating points show the same transport behavior on VinDr?

## TASKS

1. Define external estimands explicitly.

2. Reuse the project's existing inferential principles rather than creating a competing statistical framework.

3. For common external observations:
   resample observation units jointly across detectors.

4. For training-procedure uncertainty:
   resample trained runs independently within each detector.

5. Do not pair same-number seeds.

6. If defensible patient groups exist:
   use them.

7. If not:
   use study/image-level resampling;
   state the limitation.

8. Avoid unnecessary hypothesis-test proliferation.

9. Construct internal-vs-external comparison for:

### A. Ranking transportability
- AP@0.50;
- AP@0.50:0.95.

### B. False-positive-regime transportability
- exact-score FROC;
- same FP/image budgets.

### C. Score-scale transportability
- confidence distributions/detection counts.

### D. Operating-point transportability
- RSNA-frozen threshold recall;
- precision;
- F1;
- FP/image.

10. Compare historical n=3 threshold transport and Batch-43 n=5 sensitivity when both exist.

11. Do not pool RSNA and VinDr into a single AP/FROC estimate.

12. Explicitly classify changes:
    - unchanged;
    - strengthened;
    - weakened;
    - reversed.

13. Produce only high-information figures, preferably:
    - internal vs external FROC;
    - internal vs external score distributions;
    - frozen-threshold transport summary.

14. Avoid decorative figures.

15. Add tests for external resampling/statistical logic.

16. Create/update external statistical documentation and provenance.

17. Add exact commands to README.

## SCIENTIFIC RULES

Do not attribute external performance differences specifically to:
- scanners;
- institution;
- country;
- patient population;
- ontology

unless separately demonstrated.

These factors are confounded.

Use:
`cross-dataset transportability`.

## COMPLETION

Run tests/verifiers.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 51 — Final Q2 Manuscript Rewrite With External Evidence

This is a standalone Codex session.

Follow all Global Rules above.

## PURPOSE

Produce the final focused journal manuscript using all settled internal and external evidence.

## PREREQUISITE GATE

Verify Batches 42–50 results and provenance.

Do not rewrite the manuscript if external artifacts are incomplete or unverified.

## CANONICAL SOURCE

Use:
`report/paper_draft.md`.

Do not independently maintain:
- historical report;
- long historical manuscript;
- PDF
as competing scientific sources.

## TARGET PAPER STORY

The final paper should communicate:

> A leakage-aware, multi-run comparison of two lung-opacity detector pipelines separates ranking performance from raw-score operating behavior, quantifies uncertainty from held-out patients and stochastic retraining, and tests whether internally selected operating rules transport to an independent external dataset under a non-identical opacity annotation ontology.

## TASKS

### 1. Title

Create a neutral journal title emphasizing:
- operating points;
- controlled multi-run evaluation;
- lung-opacity localization;
- external transportability.

Do not imply universal architecture superiority.

### 2. Abstract

Include only the most important:
- retrospective design;
- 5,000 RSNA studies;
- patient-disjoint split;
- five attempted runs/detector;
- internal AP result;
- operating-point finding;
- exact-score FROC finding;
- principal training-procedure uncertainty result;
- standardized implementation efficiency;
- VinDr external ranking result;
- frozen-threshold transport result.

Remove detailed:
- Grad-CAM;
- corruption;
- D-ECE support;
- profiler GFLOPs.

### 3. Introduction

Do not claim:
- no prior YOLO/Faster R-CNN RSNA comparisons exist;
- confidence-scale mismatch is newly discovered.

Frame novelty as the combined methodology:
- leakage-aware split;
- common evaluator;
- all attempted runs;
- ranking versus operating point;
- run/patient uncertainty;
- external threshold transport.

### 4. Methods

Include compact subsections for:
- cohort/patient grouping;
- preprocessing;
- training pipelines/asymmetry;
- run design;
- common evaluator;
- ranking metrics;
- validation-selected thresholds;
- exact-score FROC;
- inferential targets;
- standardized timing;
- descriptive calibration;
- VinDr protocol;
- strict external ontology;
- frozen threshold transport;
- external statistics.

### 5. Results

Separate clearly:
1. internal benchmark;
2. score/operating-point behavior;
3. exact-score FROC;
4. statistical uncertainty;
5. accuracy-efficiency;
6. external ranking;
7. external FROC;
8. frozen-threshold transport;
9. score-scale transport.

### 6. Discussion

Emphasize:
- ranking;
- confidence scale;
- fixed threshold;
- detector-specific validation threshold;
- FROC;
- calibration;
- external transport
are different evaluation objects.

Do not turn seed 271 into a universal YOLO statement.

### 7. Supplementary emphasis

Move most:
- Grad-CAM;
- synthetic corruptions;
- acquisition shifts;
- F-beta;
- hypothetical loss;
- D-ECE sensitivity
out of the central narrative.

### 8. Limitations

Include at minimum:
- hardware-scoped 5,000-study subset;
- two pipelines;
- five runs;
- detector-specific training asymmetry;
- disabled augmentation;
- historical n=3 threshold provenance;
- post-hoc n=5 selection sensitivity;
- D-ECE limitations;
- secondary-analysis scope;
- VinDr ontology mismatch;
- external positive-support/sample limitations;
- external observational-unit limitation if relevant;
- no prospective evaluation;
- no reader study;
- no validated clinical deployment;
- no complete fairness analysis.

### 9. Terminology

Use:
- internal testing;
- external testing;
- cross-dataset transportability.

Do not call VinDr:
- identical-task external validation.

### 10. Declarations

Keep:
`AUTHOR ACTION REQUIRED`

for unresolved human facts.

Do not invent any declaration.

### 11. Reporting

Regenerate CLAIM 2024 crosswalk against THIS final manuscript.

Do not use certification language.

### 12. References

Run complete methodological citation audit and current-source verification.

### 13. Claim traceability

Every final numerical claim must map to exact verified artifacts.

Update paper claim manifest.

## COMPLETION

Run:
- full tests;
- lint/format;
- artifact verifier;
- paper claim verifier;
- bibliography/citation audit;
- reporting-checklist regeneration.

Update CODEX.md and prepend one HANDOFF entry.

Stop.

---

# BATCH 52 — Final Adversarial Q2 Submission Gate and PDF

This is a standalone Codex session.

Follow all Global Rules above.

This is an audit batch.

Do not assume earlier batches succeeded merely because they completed.

## PURPOSE

Determine whether the project is genuinely ready for author review/journal submission.

Regenerate the article PDF from the canonical manuscript only after the audit evidence is settled.

## 1. REPOSITORY STATE

Record:
- branch;
- HEAD;
- Git status;
- staged state;
- CI configuration;
- current canonical files.

## 2. FULL VERIFICATION

Run:
- full pytest;
- Ruff/format/lint;
- package smoke;
- scientific-artifact verifier;
- manuscript-claim verifier;
- checkpoint hashes;
- bibliography checks;
- link checks;
- any new VinDr artifact verifier.

## 3. NUMERICAL TRACEABILITY

Trace at least 20 manuscript numbers across:
- Abstract;
- cohort;
- internal clean results;
- thresholds;
- FROC;
- statistics;
- efficiency;
- calibration;
- external results;
- threshold transport;
- Discussion/Limitations.

For each report:
- manuscript value;
- exact source;
- row/column/calculation;
- rounding;
- PASS/FAIL.

## 4. ANALYSIS-SCOPE TABLE

For every major analysis list:
- dataset;
- sample size;
- patient/study units;
- detector runs;
- seed count;
- seed 271 status;
- historical/post-hoc/external classification;
- inferential/descriptive status.

Verify captions/text against it.

## 5. FROC LANGUAGE

Search:
- continuum;
- exhaustive;
- threshold-independent;
- full range;
- FROC.

Confirm every statement respects the observed exact-score/candidate-floor boundary.

## 6. THRESHOLD LANGUAGE

Confirm:
- historical thresholds selected from RSNA validation only;
- n=5 threshold selection is labeled post-hoc;
- no VinDr threshold optimization occurred.

## 7. STATISTICAL LANGUAGE

Search:
- significant;
- confidence interval;
- p-value;
- robust;
- superior;
- seed;
- checkpoint;
- population.

Confirm consistency with the established inferential targets.

## 8. CALIBRATION LANGUAGE

Confirm:
- D-ECE is detection-level/descriptive;
- no exam-level clinical-risk calibration claim;
- sparse-support limitations remain visible.

## 9. EXTERNAL LANGUAGE

Search:
- external validation;
- validated;
- generalizes;
- generalizable;
- transportability;
- domain;
- site.

Confirm:
- VinDr is external testing/cross-dataset transport;
- ontology mismatch is explicit;
- no identical-task claim.

## 10. ONTOLOGY AUDIT

Verify:
- strict VinDr `Lung opacity` is the primary box target;
- no silent merging of other findings;
- global Pneumonia was not treated as the same bounding-box class.

## 11. EFFICIENCY AUDIT

Confirm:
- matched timing boundaries;
- intended GPU;
- explicit synchronization;
- proper dispersion;
- no universal architecture-level runtime claim;
- incomplete GFLOPs appropriately demoted.

## 12. COHORT AUDIT

Confirm:
- age;
- sex;
- projection;
- missingness
are correctly reported if recovered.

Confirm no unsupported fairness conclusion.

## 13. REFERENCES

Verify every methodological citation supports its associated claim.

Ensure recent relevant literature is included.

## 14. REPORTING

Regenerate/verify CLAIM 2024 against the final manuscript.

No certification language.

## 15. DECLARATIONS

Update:
`docs/AUTHOR_DECLARATIONS_TODO.md`

Never fill unresolved author-controlled facts by inference.

## 16. REPRODUCIBILITY

Verify every new manuscript-critical V7 analysis has:
- config;
- generation command;
- provenance;
- verification path.

Confirm README commands actually exist and match current files.

## 17. PHANTOM-ARTIFACT CHECK

Verify existence/status of every manuscript-mentioned:
- table;
- figure;
- script;
- config;
- checkpoint;
- supplement;
- external artifact.

## 18. FINAL PDF

Regenerate the final article PDF from the canonical manuscript/build process.

Do not manually edit scientific content in the PDF.

Visually inspect:
- title;
- abstract;
- figures;
- tables;
- equations;
- captions;
- bibliography;
- cross-references;
- page breaks;
- clipped material;
- missing glyphs;
- unresolved placeholders;
- broken links.

## 19. FINAL SUBMISSION AUDIT

Rewrite/update:
`docs/FINAL_SUBMISSION_AUDIT.md`

with:

### BLOCKING FAILURES

### AUTHOR ACTION REQUIRED

### SHOULD-FIX

### VERIFIED CLEAN AREAS

### 20-NUMBER TRACEABILITY TABLE

### ANALYSIS-SCOPE TABLE

### INTERNAL VS EXTERNAL PROTOCOL TABLE

### COMMANDS / TESTS EXECUTED

### FINAL STATUS

Allowed statuses:

- `NOT READY FOR SUBMISSION`
- `READY FOR AUTHOR REVIEW`
- `READY FOR JOURNAL SUBMISSION`

Do not use `READY FOR JOURNAL SUBMISSION` while factual author declarations or required publication decisions remain unresolved.

## USER ACTION REQUIRED

The author must personally finalize:

1. author names/order;
2. CRediT contributions;
3. supervisor details if applicable;
4. funding;
5. competing interests;
6. institutional ethics/data-use determination;
7. consent wording;
8. patient/public involvement;
9. RSNA/VinDr use-compliance confirmation;
10. checkpoint release policy;
11. archive/DOI if desired;
12. target journal;
13. journal-specific formatting/declaration requirements.

## COMPLETION

Update CODEX.md.

Prepend one HANDOFF entry.

Stop.

---

# USER ACTION CHECKPOINTS — QUICK REFERENCE

## Before Batch 41

- Create/switch to your V7 working branch.
- Make sure local orchestration files remain local.
- Add the small pasted-batch amendment to AGENTS.md.
- Create this local `BATCHES_V7_Q2_VINDR.md`.

## Batch 44

If requested, provide/set:
`RSNA_DICOM_ROOT`.

## Batch 45

Run final standardized timing on the intended RTX 4060 Laptop GPU if Codex is not executing on that hardware.

## Batch 47

Personally obtain lawful/authorized VinDr-CXR access.

Set/provide:
`VINDR_CXR_ROOT`.

Review the frozen protocol.

## Batch 48

Review adapter/preflight counts and ontology before allowing full external inference.

## Batch 49

If required, run the exact provided ten-checkpoint inference command on your local machine.

Do not change settings after seeing results.

## Batch 52

Personally finalize factual declarations and target-journal details.

---

# RECOMMENDED COMMIT BOUNDARIES

After reviewing each successful tracked diff, one commit per batch is preferred:

- Batch 41 — baseline/canonical manuscript adjudication
- Batch 42 — exact-score FROC
- Batch 43 — n=5 validation threshold-selection sensitivity
- Batch 44 — cohort characteristics
- Batch 45 — standardized timing
- Batch 46 — internal manuscript consolidation
- Batch 47 — frozen VinDr protocol
- Batch 48 — VinDr adapter
- Batch 49 — frozen external inference
- Batch 50 — external statistics
- Batch 51 — final manuscript
- Batch 52 — final audit/PDF

Do not include local orchestration files in those commits unless explicitly intended.

The most scientifically important freeze point is:

> Commit/review Batch 47 before running Batch 49.

This establishes that the external ontology, thresholds, endpoints, and analysis policy existed before the external performance results were inspected.

---

# FINAL V7 PUBLICATION TARGET

The final manuscript should NOT merely say:

> Faster R-CNN was more accurate and YOLO11s was faster.

It should NOT claim:

> We discovered for the first time that detector confidence thresholds differ.

The intended contribution is:

> A leakage-aware, multi-run medical object-detection evaluation that separates ranking performance, raw confidence scale, validation-selected operating points, false-positive operating regimes, stochastic retraining variability, and measured implementation efficiency, and then evaluates whether ranking and internally selected operating rules transport to an independent external dataset under a different annotation context.


---

# UPDATED BATCHES 51-52:

# BATCH 51 — Final Q2 Manuscript Rewrite With External Evidence

This is a standalone Codex session.

Follow all Global Rules above.

Execute only Batch 51 in this session.

Stop at the end for user review.

---

## PURPOSE

Produce the final focused journal manuscript using all settled internal and external evidence.

The manuscript must now reflect the actual frozen VinDr results rather than the provisional pre-external story.

The paper is not simply a Faster R-CNN-versus-YOLO winner comparison.

Its central contribution is the controlled separation of:

- ranking performance;
- raw-score and operating-point behavior;
- false-positive operating regimes;
- stochastic training variability;
- measured implementation efficiency;
- internal performance;
- external transportability.

The final manuscript should make clear that these are different evaluation objects and need not transport in the same way.

---

## PREREQUISITE GATE

Reconstruct the current project state from the repository.

Read the required project/orchestration files under the Global Rules, including the newest HANDOFF entry, CODEX, PROJECT_SPEC where relevant, decision/limitations/audit documents, and the canonical manuscript.

Verify from actual artifacts rather than prose that Batches 42–50 are scientifically complete enough to support the final manuscript.

At minimum verify:

- the canonical internal results used by the paper;
- the exact-score FROC repair;
- five-run threshold-selection sensitivity;
- cohort characteristics;
- standardized timing;
- the frozen VinDr protocol;
- VinDr adapter/preflight;
- all ten external checkpoint runs;
- Batch-50 external statistics/transportability;
- checkpoint/config/protocol identity and provenance where applicable.

All five runs per detector must remain represented, including seed 271.

Do not continue if a manuscript-critical external result exists only as prose when its expected numerical/provenance artifact should exist.

---

## CLEAN-CHECKOUT / CI REQUIREMENT

Before finalizing the manuscript, verify the repository's normal clean-checkout test/CI path.

Portable CI must not require private or machine-local RSNA/VinDr data.

If the current test layout incorrectly mixes portable tests with authorized-data scientific integration tests:

- repair that boundary in the smallest appropriate way;
- preserve the full-data scientific verification;
- keep an explicit way to run those tests in an authorized local environment;
- do not weaken scientific checks merely to obtain a green CI result.

Use your judgment to implement the cleanest repository-consistent solution.

If fixing CI would require changing scientific definitions, results, thresholds, frozen external settings, or other substantive methodology, stop for user review instead.

---

## CANONICAL SOURCE

Use:

`report/paper_draft.md`

as the only canonical editable journal manuscript.

Historical reports, historical manuscript versions, and rendered PDFs are not competing scientific sources.

Preserve them where required for provenance, but do not independently maintain their scientific content.

---

## TARGET PAPER STORY

The manuscript should communicate approximately this scientific story:

> A leakage-aware, multi-run comparison of two lung-opacity detector pipelines separates ranking performance from operating-point behavior, quantifies uncertainty from held-out observations and stochastic retraining, evaluates implementation efficiency under a matched protocol, and tests whether internally established detector ranking and operating rules transport to an independent external dataset under a non-identical opacity annotation ontology.

The external result should be interpreted around the distinction:

> Preserved ordering is not preserved performance.

This phrase is useful only if qualified correctly.

The paper must not imply that:
- every external endpoint establishes the same detector ordering;
- the full external FROC frontier was observed;
- preserved relative ranking means successful external generalization.

---

## SCIENTIFIC INVARIANTS

These are non-negotiable.

### Test-set integrity

Do not use RSNA internal-test labels for model/threshold/calibration/preprocessing/NMS tuning.

Do not use VinDr test annotations for:
- training;
- fine-tuning;
- model selection;
- checkpoint selection;
- threshold selection;
- calibration fitting;
- ontology optimization after seeing results;
- endpoint selection after seeing results.

No new VinDr-optimized threshold may be created.

### Run integrity

Retain all five attempted runs per detector.

Do not remove or downweight an inconvenient run simply because its behavior differs.

Do not treat same-number detector seeds as paired stochastic replicates.

### External ontology

The primary VinDr box target remains the exact local finding:

`Lung opacity`

Do not silently merge other findings such as:
- Consolidation;
- Infiltration;
- Atelectasis;
- ILD;
- global Pneumonia;
- other labels.

### Historical analysis integrity

Preserve:
- historical n=3 threshold provenance;
- post-hoc n=5 threshold sensitivity as secondary;
- historical/superseded artifacts where they are evidence.

Do not rewrite history to make the final paper cleaner.

---

## MANUSCRIPT PRIORITIES

Use your judgment to structure the paper cleanly, but keep the central narrative focused on the following.

### Internal benchmark

Present the internal comparison accurately and concisely, including:

- patient-disjoint design;
- common evaluator;
- five-run behavior;
- AP/ranking;
- validation-selected operating points;
- exact-score FROC;
- principal uncertainty;
- matched timing.

Do not reduce the study to one AP number.

### Ranking versus operating point

Make this distinction central.

Explain that:
- detector confidence scales are not directly interchangeable;
- ranking performance and fixed-threshold behavior answer different questions;
- detector-specific thresholds can materially alter precision/recall/FP behavior.

Do not claim that score-scale mismatch itself is newly discovered.

### Training variability

Make clear that one checkpoint does not represent the entire training procedure.

Keep the primary training-procedure interpretation separate from checkpoint-conditional sensitivity analyses.

### Efficiency

Report the standardized timing experiment as measured implementation performance on the stated hardware/protocol.

Do not generalize the timing result to all Faster R-CNN or YOLO implementations.

Keep incomplete profiler GFLOPs appropriately demoted.

---

## EXTERNAL EVIDENCE

The external experiment is now central to the manuscript.

Accurately report the verified VinDr cohort and strict target support.

Make clear that:
- the RSNA-trained checkpoints were applied without adaptation;
- the external protocol was frozen before full inference;
- no VinDr threshold optimization occurred.

### External AP / ranking

The external result must clearly communicate both facts:

1. the observed equal-run AP ordering remains in the same direction as internally;
2. absolute AP collapses for both pipelines.

Do not allow the first fact to obscure the second.

### Frozen-threshold transport

Treat the failure of the internally selected operating points to transport well as a major scientific result.

Report the external:
- precision;
- recall;
- F1;
- FP/image;
- detection/emission behavior

without softening adverse values.

Do not interpret low FP/image as improvement when recall/emission also collapse.

### External FROC

Handle support limits conservatively.

The manuscript must preserve the fact that:

- FROC is based on retained exact-score candidates;
- candidate support is finite;
- one external YOLO run is floor-limited at the upper 1 and 2 FP/image budgets;
- the conservative missing-support bound does not rule out an ordering reversal beyond retained support at those upper budgets;
- substantial Faster R-CNN max-detection-cap saturation is also part of the support limitation.

Do not describe external FROC ordering as an unrestricted/full-frontier conclusion.

Do not change the frozen candidate floor or detection cap after seeing the result.

### External interpretation

Use:
- external testing;
- cross-dataset transportability;
- cross-annotation-ontology transportability.

Do not call VinDr identical-task external validation.

Do not attribute the external performance change specifically to:
- scanners;
- hospital/site;
- country;
- population;
- annotation ontology;
- preprocessing;
- another single factor

unless separately demonstrated.

Those factors are confounded.

---

## NUMERICAL IMPLEMENTATION CAVEATS

Incorporate the implementation caveats proportionately.

### Inference precision

Historical internal YOLO accuracy inference used FP32, whereas the external YOLO inference used the verified bfloat16 AMP path.

Therefore do not attribute internal/external score or performance shifts solely to dataset differences.

Describe this clearly in Methods/Limitations without allowing it to dominate the paper.

### Faster R-CNN coordinate repair

The Batch-49 one-ULP inverse-coordinate upper-bound repair should be documented as a narrow numerical implementation correction.

Preserve the important facts:

- it concerns the tiny documented floating-point upper-bound overshoot;
- invalid lower-bound/materially out-of-range coordinates still fail;
- it did not alter the frozen scientific protocol;
- it did not become an opportunity for post-hoc external tuning.

Place detailed debugging/provenance in supplementary/reproducibility material rather than the main Results narrative unless needed for clarity.

---

## STATISTICAL LANGUAGE

Use the established inferential framework.

Do not invent a new competing statistical analysis merely for the final manuscript.

Keep clear distinctions between:

- training-procedure uncertainty;
- checkpoint-conditional uncertainty;
- descriptive cross-dataset comparisons.

The Batch-50 terms:

- unchanged;
- strengthened;
- weakened;
- reversed

are descriptive classifications.

Do not turn them into significance statements unless a corresponding inferential test genuinely exists.

Do not imply:
- familywise/simultaneous coverage from marginal intervals;
- an unperformed cross-dataset interaction test;
- a robust detector difference merely because a point estimate is positive.

---

## SECONDARY MATERIAL

Keep the journal story focused.

Most of the following should remain secondary/supplementary unless a specific item materially helps the central argument:

- D-ECE details;
- Grad-CAM;
- common corruptions;
- acquisition stress analyses;
- F-beta;
- hypothetical loss;
- detailed internal decision history;
- low-level debugging records.

D-ECE must remain described as:
- detection-level;
- emitted-population dependent;
- binning/support dependent;
- descriptive;
- not patient-level clinical-risk calibration.

---

## LIMITATIONS

Ensure the final Limitations section accurately covers the limitations that materially affect interpretation.

At minimum this includes:

- hardware-scoped 5,000-study RSNA subset;
- only two disclosed detector pipelines;
- five runs as a coarse sample of training variability;
- training asymmetries;
- disabled augmentation where applicable;
- historical versus post-hoc threshold provenance;
- calibration/XAI/secondary-analysis scope;
- non-identical VinDr ontology;
- low external positive/box support;
- lack of defensible VinDr patient grouping;
- possibility that image-level external intervals are too narrow if repeat patients exist;
- external FROC candidate-floor limitations;
- Faster R-CNN detection-cap saturation;
- internal/external YOLO inference-precision difference;
- no prospective evaluation;
- no reader study;
- no validated clinical deployment;
- no complete fairness analysis.

Do not use Limitations merely as a dumping ground for caveats that should also qualify the Results/Discussion where relevant.

---

## CLAIM BOUNDARIES

The final manuscript must not claim or imply:

- Faster R-CNN is universally superior to YOLO;
- YOLO is universally inferior;
- lung-opacity localization equals pneumonia diagnosis;
- a confidence score has the same meaning across detectors;
- higher AP means better performance at every operating point;
- one checkpoint represents the full training procedure;
- preserved ranking means successful external performance transport;
- VinDr constitutes identical-task validation;
- a specific external factor caused the performance collapse;
- the models are clinically validated or deployment-ready;
- the study establishes diagnostic utility or patient benefit;
- external FROC superiority exists beyond the support actually observed.

Use your judgment to audit the entire manuscript for equivalent overclaims, not merely these exact phrases.

---

## REPORTING / REFERENCES / TRACEABILITY

Update all manuscript-supporting publication artifacts against the final paper.

This includes as appropriate:

- CLAIM 2024 crosswalk;
- bibliography/citation audit;
- claim manifest;
- relevant limitation/provenance documentation.

Use current authoritative/primary references where available.

Every final numerical manuscript claim must have a traceable canonical source or deterministic verification path.

Do not source final manuscript numbers only from:
- HANDOFF;
- CODEX;
- memory;
- obsolete prose reports

when numerical artifacts exist.

---

## COMPLETION

Perform the verification reasonably required to establish that the final manuscript is internally consistent with the repository and settled evidence.

This must include:

- portable tests/CI-equivalent verification;
- relevant authorized/local scientific verification;
- lint/format;
- artifact/result verification;
- manuscript-claim verification;
- bibliography/reporting verification.

If a manuscript-critical result fails verification:
- do not conceal it with wording;
- do not casually alter the methodology;
- document the discrepancy and stop for user review.

Update `CODEX.md` locally.

Prepend one `HANDOFF.md` entry locally.

---

## LOCAL ORCHESTRATION / GIT SAFETY

The established Codex/orchestration files are LOCAL working files unless the user explicitly names a specific file and explicitly asks for that file itself to be committed/pushed.

This includes, where present:

- `AGENTS.md`
- `CODEX.md`
- `HANDOFF.md`
- `PROJECT_SPEC.md`
- `BATCHES.md`
- `BATCHES_V*.md`
- established local audit/session/orchestration files.

You may read and update them as required by the batch.

However:

- do NOT stage them;
- do NOT commit them;
- do NOT push them;
- do NOT discard their working-tree contents.

Before any commit/push, inspect the staged set.

If a local orchestration file is staged, unstage it non-destructively while preserving its local contents.

Generic user instructions such as:
- `commit the batch`;
- `commit everything`;
- `push the changes`;
- `push to GitHub`

do NOT authorize inclusion of these local orchestration files.

Avoid broad staging if it would include them.

Stage intended public/scientific files selectively.

Do not push anything unless explicitly authorized by the user in the current session.

Stop for user review.

---

# BATCH 52 — Final Adversarial Q2 Submission Gate and PDF

This is a standalone Codex session.

Follow all Global Rules above.

Execute only Batch 52 in this session.

This is an audit batch.

Do not assume earlier batches succeeded merely because their batch numbers are complete.

Do not launch new major experiments or casually redesign settled methodology.

If the final audit exposes a substantive scientific defect that requires more than a narrow correction:

- classify it as blocking;
- document it;
- stop for user review.

---

## PURPOSE

Determine whether the project is genuinely ready for author review and eventual journal submission.

This is an adversarial audit of:

- scientific claims;
- numerical provenance;
- statistical interpretation;
- external evidence;
- reproducibility;
- repository/CI state;
- manuscript/reporting consistency;
- final rendered PDF.

Challenge both favorable and unfavorable results equally.

Do not relax the standard because the external results are inconvenient.

---

## STARTUP / REPOSITORY STATE

Reconstruct the full current project state.

Record enough repository state to make the audit reproducible, including:

- branch;
- HEAD;
- Git status;
- staged state;
- current canonical manuscript;
- current canonical scientific artifacts;
- current CI configuration/status where available;
- relevant public/private artifact boundaries.

Verify that the final Batch-49 and Batch-50 artifacts intended to support the manuscript actually exist in the state being audited.

Do not rely solely on HANDOFF/CODEX claims.

---

## CLEAN-CHECKOUT CI / TEST BOUNDARY

Verify the repository's portable clean-checkout CI/test path.

It must not fail simply because:
- private RSNA data are absent;
- private VinDr data are absent;
- ignored processed datasets are absent;
- machine-specific local artifacts are absent.

Full-data scientific integration/replay tests may legitimately require authorized local data, but this must be explicit and separated cleanly from portable CI.

If this boundary is still broken, treat it as a publication-blocking repository defect.

Do not obtain a green result by deleting or weakening meaningful scientific verification.

Use repository-consistent judgment to distinguish:
- portable validation;
- authorized local full-data validation;
- GPU-dependent reproduction.

---

## FULL SCIENTIFIC VERIFICATION

Run the relevant final verification stack.

This should include, where applicable:

- portable pytest;
- lint/format;
- package smoke;
- scientific artifact verification;
- VinDr artifact verification;
- manuscript-claim verification;
- checkpoint/config/protocol verification;
- bibliography/link/reporting checks;
- authorized local scientific integration/replay verification.

Record the meaningful commands/results in the final submission audit.

---

## NUMERICAL TRACEABILITY

Perform a fresh adversarial trace of at least 20 manuscript numbers.

Choose numbers across the major scientific claims rather than simply the easiest values to verify.

The trace must cover a representative set from:

- cohort;
- internal AP;
- operating-point metrics;
- internal FROC;
- uncertainty;
- timing/efficiency;
- external cohort;
- external AP;
- external FROC;
- external uncertainty;
- frozen-threshold transport;
- score/detection behavior;
- important support-limit statements.

For every checked value, record enough information to recover:
- manuscript value;
- source artifact/calculation;
- relevant row/column or derivation;
- rounding;
- PASS/FAIL.

A manuscript-critical number without an exact provenance path is a failure.

---

## ANALYSIS-SCOPE AUDIT

Construct or update a compact scope table for every major analysis.

Use it to verify that the manuscript and figure captions correctly distinguish:

- dataset;
- observation unit;
- sample size;
- positive/box support where relevant;
- run/seed inclusion;
- historical/post-hoc/external status;
- inferential versus descriptive status;
- threshold policy;
- candidate/score support where relevant.

Pay particular attention to accidental scope drift between:
- one checkpoint and five-run results;
- validation selection and test evaluation;
- patient-level internal resampling and image-level external resampling;
- observed FROC support and hypothetical unobserved support.

---

## ADVERSARIAL FROC AUDIT

Audit all FROC claims rather than merely checking the reported numbers.

The final paper must remain consistent with:

- exact retained scores;
- finite candidate floor;
- no interpolation/extrapolation where not performed;
- tied-score handling;
- fixed FP/image budgets;
- floor-limited observations;
- max-detection cap behavior.

Explicitly verify that:

- the external YOLO support limitation at the upper budgets remains visible;
- the conservative missing-support bound is correctly characterized;
- an ordering reversal beyond retained support at 1 and 2 FP/image is not ruled out where the bound does not permit that conclusion;
- substantial Faster R-CNN detection-cap saturation is not hidden.

Reject any wording that turns observed support-limited FROC results into a full/unrestricted detector frontier comparison.

---

## THRESHOLD / OPERATING-POINT AUDIT

Verify:

- historical thresholds came only from RSNA validation;
- historical policy remains historical/primary;
- n=5 validation selection remains post-hoc/secondary;
- all test analyses retain all five runs;
- no VinDr threshold was optimized;
- no VinDr calibration fitting occurred.

Make sure the manuscript does not mistake:
- lower FP/image;
- fewer emitted detections

for improvement when recall collapses.

The failure of frozen operating-point transport should remain visible.

---

## STATISTICAL INTERPRETATION AUDIT

Challenge the manuscript for improper inferential wording.

Verify the distinction between:

- training-procedure uncertainty;
- fixed-checkpoint uncertainty;
- descriptive cross-dataset change classifications.

Confirm the manuscript does not imply:

- same-number seed pairing;
- unperformed interaction tests;
- familywise/simultaneous guarantees;
- resolved detector differences where intervals do not support that conclusion.

Terms such as:
- strengthened;
- weakened;
- reversed;
- unchanged

must remain descriptive unless separately supported by an inferential procedure.

---

## EXTERNAL TRANSPORTABILITY AUDIT

Audit the manuscript's external story as a whole.

Verify:

- strict VinDr `Lung opacity` target;
- no silent ontology broadening;
- correct external image/positive/box counts;
- correct use of image/study as the external statistical unit;
- explicit lack of defensible patient grouping;
- no conversion of image counts into patient claims;
- no identical-task external-validation language;
- no causal attribution to one external factor.

The main scientific conclusion should distinguish:

- preserved observed relative ordering on some ranking endpoints;
- severe absolute performance degradation;
- poor frozen-threshold transport.

Ensure the phrase:

> Preserved ordering is not preserved performance.

is used only in a way consistent with the actual support and uncertainty.

---

## IMPLEMENTATION-CAVEAT AUDIT

Verify relevant numerical implementation facts have not been lost during manuscript simplification.

In particular:

- historical internal YOLO accuracy inference was FP32;
- external YOLO inference used the verified bfloat16 AMP path;
- external Faster R-CNN used its verified configured AMP path;
- internal/external differences are not attributed solely to dataset factors.

Verify the Faster R-CNN coordinate canonicalization remains:
- narrow;
- tested;
- provenance-preserved;
- scientifically non-opportunistic.

Do not allow a technical implementation repair to become a hidden protocol change.

---

## EFFICIENCY AUDIT

Verify the final timing claims against the actual standardized experiment.

Confirm the paper accurately states the important experimental boundary and hardware context.

Do not permit:
- universal architecture speed claims;
- theoretical operation counts to replace measured timing;
- incomplete profiler GFLOPs to become headline evidence.

---

## SECONDARY ANALYSIS / CALIBRATION AUDIT

Ensure secondary analyses remain proportionate to their evidential strength.

In particular:

- D-ECE remains detection-level/descriptive;
- no patient-risk calibration claim;
- XAI is not presented as proof of clinically meaningful reasoning;
- synthetic corruptions/acquisition stress are not generalized beyond their defined scope.

---

## CLAIM-BOUNDARY REVIEW

Read the final manuscript as a skeptical reviewer.

Identify and correct any wording that implies, explicitly or indirectly:

- universal Faster R-CNN superiority;
- universal YOLO inferiority;
- pneumonia diagnosis rather than opacity localization;
- directly comparable confidence scales;
- AP as a complete description of detector usefulness;
- one checkpoint as the training procedure;
- successful external generalization merely from preserved ranking;
- successful threshold transport despite very low external recall;
- unrestricted FROC superiority beyond retained support;
- causation from one external domain factor;
- clinical validation;
- deployment readiness;
- patient benefit;
- state-of-the-art status without defensible evidence.

Use judgment rather than limiting the audit to exact keywords.

If correcting an overclaim would require changing the underlying science rather than the wording, classify it as blocking.

---

## REFERENCES / REPORTING / DECLARATIONS

Verify the final manuscript against:

- current relevant methodological references;
- CLAIM 2024 crosswalk;
- final claim manifest;
- declaration TODOs;
- data/code availability statements.

Do not invent author-controlled facts.

Unresolved factual declarations remain author action.

Do not use certification language for reporting checklists.

---

## REPRODUCIBILITY / ARTIFACT AUDIT

Verify every manuscript-critical analysis has a defensible reproduction or verification path appropriate to its data restrictions.

Check for phantom or stale references to:

- figures;
- tables;
- scripts;
- configs;
- checkpoints;
- result files;
- supplements;
- protocols;
- external artifacts.

A public manuscript must not imply that a restricted/private artifact is publicly accessible when it is not.

Likewise, private raw data need not be published merely to make the repository look complete.

Preserve lawful data-access boundaries.

---

## FINAL PDF

Only after the scientific/repository audit is settled, regenerate the final article PDF from the canonical manuscript/build process.

Do not manually alter scientific content in the rendered PDF.

Visually inspect the finished article for:

- title/author placeholders;
- abstract;
- figures;
- tables;
- captions;
- equations;
- bibliography;
- cross-references;
- page/layout problems;
- clipped material;
- missing glyphs;
- unresolved placeholders;
- broken links.

Ensure external FROC/table/figure captions preserve the necessary support-limit language.

---

## FINAL SUBMISSION AUDIT

Rewrite/update:

`docs/FINAL_SUBMISSION_AUDIT.md`

as an evidence-based final status report.

It should clearly distinguish at least:

### BLOCKING FAILURES

### AUTHOR ACTION REQUIRED

### SHOULD-FIX

### VERIFIED CLEAN AREAS

### CLEAN-CHECKOUT CI STATUS

### FULL-DATA SCIENTIFIC VERIFICATION STATUS

### NUMERICAL TRACEABILITY

### ANALYSIS-SCOPE SUMMARY

### INTERNAL VS EXTERNAL PROTOCOL SUMMARY

### EXTERNAL FROC SUPPORT / CAP STATUS

### FROZEN-THRESHOLD TRANSPORT STATUS

### COMMANDS / TESTS EXECUTED

### FINAL STATUS

Allowed final statuses:

- `NOT READY FOR SUBMISSION`
- `READY FOR AUTHOR REVIEW`
- `READY FOR JOURNAL SUBMISSION`

Use `NOT READY FOR SUBMISSION` if:
- manuscript-critical science remains unverified;
- portable clean-checkout CI is still broken;
- required scientific/public artifacts are missing;
- material claim/provenance inconsistencies remain.

Do not use `READY FOR JOURNAL SUBMISSION` while required author-controlled declarations or journal-specific decisions remain unresolved.

---

## USER-CONTROLLED ITEMS

Do not invent or finalize on the author's behalf:

- author names/order;
- CRediT roles;
- supervisor details;
- funding;
- conflicts;
- ethics/data-use determination;
- consent wording;
- patient/public involvement;
- checkpoint-release policy;
- archive/DOI;
- target journal;
- journal-specific declarations/formatting.

Clearly identify any such remaining items.

---

## LOCAL ORCHESTRATION / GIT SAFETY

The established Codex/orchestration files remain local unless the user explicitly names a specific file and explicitly requests that file itself to be committed/pushed.

This includes, where present:

- `AGENTS.md`
- `CODEX.md`
- `HANDOFF.md`
- `PROJECT_SPEC.md`
- `BATCHES.md`
- `BATCHES_V*.md`
- established local audit/session/orchestration files.

They may be read and updated locally where required.

Do NOT:
- stage them;
- commit them;
- push them;
- discard their local changes.

Before any commit or push, inspect the staged/commit contents and non-destructively unstage any local orchestration file.

Generic instructions such as:
- `commit everything`;
- `commit the batch`;
- `push the changes`

do not authorize inclusion of these files.

Prefer selective staging of public/scientific changes.

Do not push anything unless the user explicitly authorizes a push in the current session.

---

## COMPLETION

Update `CODEX.md` locally.

Prepend one `HANDOFF.md` entry locally.

Ensure local orchestration files remain unstaged.

Do not commit, push, tag, publish, release, or submit unless explicitly instructed.

Stop.