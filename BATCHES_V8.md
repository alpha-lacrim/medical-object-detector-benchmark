# BATCH 53 — YOLO Numerical-Inference-Path Transport Sensitivity

This is a standalone Codex session.

Use Extra High reasoning.

Follow AGENTS.md and all established repository scientific/provenance rules.

Before substantive work:

1. Read AGENTS.md.
2. Read the newest HANDOFF.md entry first.
3. Read CODEX.md, especially newest decisions/current phase/canonical files/current risks.
4. Read the relevant PROJECT_SPEC.md sections. Do not edit PROJECT_SPEC.md.
5. Read as relevant:
   - docs/DECISION_LOG.md
   - docs/LIMITATIONS.md
   - docs/HYPOTHESES.md
   - docs/FINAL_MANUSCRIPT_AUDIT.md
   - docs/REPORTING_CHECKLIST.md
   - docs/REPRODUCIBILITY.md
6. Read report/paper_draft.md.
7. Record current:
   - branch
   - HEAD
   - working-tree status
   - staged files
   - relevant uncommitted changes.
8. Never destroy/reset/stash/stage/commit/overwrite unrelated user changes.

Execute ONLY Batch 53 in this session.

Do not commit, push, tag, publish, release, or upload anything.

Stop at the batch review gate.

---

## PURPOSE

Resolve, as a controlled secondary sensitivity analysis, the current numerical
inference-path asymmetry in the manuscript:

- historical/internal YOLO11s accuracy inference used FP32;
- frozen external VinDr YOLO11s inference used explicit bfloat16 AMP.

The current manuscript correctly states that this prevents attributing all
internal-to-external score/performance changes solely to dataset differences.

The goal is to determine whether harmonising the INTERNAL YOLO numerical path
to the external bfloat16 path materially changes:

- internal ranking metrics;
- frozen operating-point behaviour;
- score distributions/emissions;
- exact-score FROC;
- the interpretation of external transportability.

No training is allowed.

This analysis is SECONDARY SENSITIVITY unless a later explicit human decision
changes its status.

The historical FP32 internal analysis remains frozen provenance.

---

## PREREQUISITE GATE

Before implementing anything, verify from actual repository evidence:

1. The current canonical manuscript is report/paper_draft.md.
2. All five retained YOLO11s frozen checkpoints exist or are accessible through
   the established local checkpoint mechanism.
3. Their hashes match the existing checkpoint/release manifest.
4. The immutable RSNA internal-test split and canonical annotations exist.
5. The historical internal YOLO prediction/evaluation artifacts remain intact.
6. The frozen external VinDr inference implementation/config/provenance clearly
   identifies the explicit bfloat16 pathway.
7. Current exact-score FROC implementation/config and historical threshold
   policies are identifiable.
8. No existing completed dtype-harmonisation sensitivity already answers this
   question.

If any prerequisite is missing, contradictory, hash-invalid, or only asserted
in prose where an artifact should exist:

- do not continue;
- document the discrepancy;
- prepend one HANDOFF entry;
- stop for user review.

---

## SCIENTIFIC INVARIANTS

Do NOT change:

- training;
- checkpoint selection;
- checkpoint bytes;
- seeds;
- RSNA train/validation/test membership;
- RSNA annotations;
- preprocessing semantics except the intended numerical inference dtype path;
- image resolution;
- NMS IoU;
- detection cap;
- evaluator matching;
- AP definitions;
- FROC budgets;
- candidate floors except where required to reproduce the already frozen FROC
  protocol;
- historical validation-selected thresholds;
- external VinDr ontology;
- external VinDr results;
- primary manuscript estimands.

Do NOT overwrite:

- historical FP32 internal YOLO prediction bundles;
- historical internal tables/figures;
- frozen VinDr outputs;
- historical threshold/FROC artifacts.

Create NEW VERSIONED artifacts/config/provenance.

Do not pair same-number detector seeds as stochastic replicates.

Do not remove seed 271.

---

## PHASE 1 — FORENSIC PATH AUDIT

Before GPU inference, determine exactly:

1. Which code path produced historical internal YOLO predictions.
2. Which code path produced external VinDr YOLO predictions.
3. Where autocast/dtype differs.
4. Whether there are any OTHER material differences between the relevant YOLO
   internal and external inference paths, including:
   - loader;
   - preprocessing;
   - resize/letterbox;
   - postprocessing;
   - coordinate restoration;
   - NMS;
   - candidate filtering;
   - score comparison semantics;
   - detection cap;
   - model fusion;
   - native API usage.

Create a concise path-comparison table in a new documentation/provenance file.

The intended scientific intervention is NUMERICAL INFERENCE PRECISION, not an
opportunistic rewrite of the adapter.

If substantial non-dtype differences prevent a clean sensitivity experiment:

- do not improvise;
- document them;
- propose the smallest defensible design;
- stop for user review.

---

## PHASE 2 — VERSIONED PROTOCOL

Create a new versioned sensitivity protocol following existing repository
naming conventions.

Likely concept:

`YOLO internal FP32-versus-bfloat16 inference-path sensitivity`

but follow existing naming/config conventions rather than forcing this exact
filename.

The config/protocol must bind:

- all five YOLO checkpoint hashes;
- internal-test manifest/hash;
- evaluator settings;
- preprocessing;
- resolution;
- NMS;
- cap;
- AP floor;
- FROC candidate floor;
- historical thresholds;
- explicit bfloat16 autocast;
- relevant software/environment identity;
- output locations.

Add a preflight mode that:

- verifies hashes;
- verifies immutable split/annotation identity;
- refuses output overwrite;
- confirms CUDA/device capability;
- records actual convolution activation dtype if technically feasible;
- confirms no training code path is reachable;
- confirms expected five-run scope.

Do not hardcode publication-critical parameters that belong in config.

---

## PHASE 3 — REVIEW GATE BEFORE SUBSTANTIAL GPU WORK

Estimate:

- number of checkpoints;
- number of images;
- expected prediction artifacts;
- approximate GPU workload;
- expected output size.

If the active environment is not the intended compatible NVIDIA environment:

- finish config/code/tests/preflight;
- provide the exact execution command;
- update HANDOFF;
- STOP.

If the environment is compatible and the workload is ordinary inference-only
rather than a major new computational campaign, proceed after successful
preflight.

Do not run any external re-inference in this batch unless required by an
unexpected technical issue and explicitly approved.

The minimal intended experiment is INTERNAL RSNA bfloat16 inference for the
five frozen YOLO checkpoints so that internal and external transport can be
examined under the same YOLO numerical inference precision.

---

## PHASE 4 — INFERENCE COLLECTION

Run all five frozen YOLO11s checkpoints on the immutable RSNA internal-test set
using the harmonised explicit bfloat16 path.

Preserve historical FP32 predictions unchanged.

For each run record:

- checkpoint SHA256;
- config hash;
- source split/annotation hashes;
- environment;
- Torch/Ultralytics/CUDA/cuDNN versions;
- explicit dtype/autocast evidence;
- execution timestamp;
- candidate floor;
- NMS;
- cap;
- prediction bundle hash.

Use versioned output paths.

No result-dependent parameter changes are allowed.

---

## PHASE 5 — PAIRED FP32 vs BFLOAT16 SENSITIVITY

Using the SAME checkpoint and SAME images, compare historical FP32 versus new
bfloat16 YOLO predictions.

Compute at minimum per run and aggregate:

### Ranking
- AP@0.50
- AP@0.50:0.95

### Historical transported/internal operating point
Using the EXISTING frozen historical RSNA YOLO threshold unchanged:
- precision
- recall
- F1
- FP/image
- detections/image
- percentage of images with detections

### Post-hoc n=5 threshold policy
If it exists, apply the existing n=5 RSNA threshold unchanged:
- precision
- recall
- F1
- FP/image
- detections/image

Do NOT re-select either threshold.

### Score/emission behaviour
- total retained candidate detections
- detections/image
- image-level zero-detection fraction
- per-run min/quantiles/median/mean/max score
- maximum score for seed 271
- number/proportion of detections crossing key frozen thresholds

### Exact-score FROC
Using the existing exact-score FROC definitions and candidate support:
- same prespecified FP/image budgets
- per-run sensitivity
- equal-run aggregate

Do not lower floors or raise caps based on these results.

If the historical FP32 bundle lacks support required for an exactly matched
comparison, report that boundary rather than manufacturing support.

---

## PHASE 6 — NUMERICAL AGREEMENT CHARACTERISATION

Where technically meaningful, compare FP32 and bfloat16 predictions before
thresholding:

- detection-count agreement;
- matched box-coordinate differences;
- score differences;
- rank-order stability where measurable;
- proportion of candidates appearing/disappearing;
- threshold-crossing counts.

Do not force one-to-one candidate matching where native inference genuinely
changes candidate composition.

Document the matching rule.

---

## PHASE 7 — INTERPRETATION

Answer narrowly:

1. Does bfloat16 materially change internal YOLO AP?
2. Does it materially change score scale?
3. Does it materially change frozen-threshold emissions/recall?
4. Does it materially change FROC?
5. Does seed 271 remain a low-score but nonzero-AP run?
6. Does harmonising the numerical path change any major INTERNAL detector
   comparison conclusion?
7. Does it materially alter the interpretation of the severe RSNA-to-VinDr
   transport failure?

Do NOT claim that a small dtype effect proves all remaining change is due to
dataset shift.

Dataset/site/population/annotation/preprocessing differences remain confounded.

Classify conclusions as:
- unchanged;
- strengthened;
- weakened;
- reversed.

These labels describe observed conclusions, not causal significance.

---

## PHASE 8 — MANUSCRIPT INTEGRATION

Only after all sensitivity outputs pass verification:

If the bfloat16 sensitivity is small and does not alter conclusions:
- add a concise secondary-sensitivity result;
- revise the existing FP32/bfloat16 limitation so it is no longer an
  unresolved confound to the same degree;
- retain appropriate caution.

If differences are meaningful:
- report them explicitly;
- revise Discussion/Limitations accordingly;
- do not minimize them.

Do not replace historical primary internal numbers unless explicitly required
for factual consistency.

Prefer placing detailed dtype results in Supplementary material and keeping the
main manuscript concise.

Update as applicable:
- docs/LIMITATIONS.md
- docs/REPRODUCIBILITY.md
- relevant analysis documentation
- docs/DECISION_LOG.md
- Supplementary documentation
- scientific/publication artifact manifests
- report/paper_claim_sources.yaml
- report/paper_draft.md

Any change in canonical/primary/secondary status must be recorded in
docs/DECISION_LOG.md.

---

## TESTS

Add focused tests for at least:

- all five intended YOLO runs included;
- seed 271 cannot be excluded;
- historical artifacts cannot be overwritten;
- dtype sensitivity config is explicit;
- inference-only code cannot enter training;
- evaluator constants match frozen definitions;
- threshold-selection code is not invoked;
- deterministic output schema;
- versioned output refusal on overwrite.

Run:

- focused new tests;
- relevant existing tests;
- full portable pytest if feasible;
- Ruff format/check for changed Python;
- scientific artifact verifier;
- manuscript claim verifier if manuscript changes;
- git diff --check.

Do not imply CI regenerates GPU inference.

---

## COMPLETION

Create/update durable project state only.

Update CODEX.md with:
- completed dtype sensitivity decision;
- new canonical secondary artifacts;
- durable interpretation;
- remaining limitation if any.

Prepend exactly one new HANDOFF.md entry stating:
- what was done;
- whether GPU inference completed;
- files/artifacts created;
- tests/verifiers run;
- key observed conclusion;
- what remains;
- what requires user review.

Leave AGENTS.md, CODEX.md, HANDOFF.md, PROJECT_SPEC.md and BATCHES*.md local-only
according to existing policy.

Do not stage/commit/push/tag/publish.

STOP FOR USER REVIEW.
BATCH 54 — Publication Study/Data-Flow Figure
# BATCH 54 — Publication Study/Data-Flow Figure

This is a standalone Codex session.

Use Extra High reasoning.

Follow AGENTS.md and the repository's established standalone-session,
provenance, local-orchestration and scientific-artifact rules.

Before substantive work:

1. Read AGENTS.md.
2. Read the newest HANDOFF.md entry.
3. Read CODEX.md.
4. Read relevant PROJECT_SPEC.md sections without editing PROJECT_SPEC.md.
5. Read:
   - docs/DECISION_LOG.md
   - docs/LIMITATIONS.md
   - docs/REPORTING_CHECKLIST.md
   - docs/FINAL_MANUSCRIPT_AUDIT.md
   - docs/REPRODUCIBILITY.md
6. Read report/paper_draft.md.
7. Record branch, HEAD, status, staged files and uncommitted changes.
8. Protect unrelated user changes.

Execute ONLY Batch 54.

Do not commit, push, tag, publish or upload.

---

## PURPOSE

Create a publication-quality retrospective study/data-flow figure that addresses
the current reporting gap for a participant/study flow diagram WITHOUT
inventing a clinical recruitment process.

The figure must be generated deterministically from verified canonical
repository counts.

No scientific result may be changed.

---

## PREREQUISITE GATE

Verify from actual artifacts:

### RSNA source/subset
- source study count;
- source box count if used;
- deterministic selected 5,000-study cohort;
- 2,136 patient groups;
- train/validation/internal-test study counts;
- patient-group counts;
- patient-disjointness;
- internal-test positive-study count;
- internal-test reference-box count.

### Training
- five retained Faster R-CNN runs;
- five retained YOLO11s runs;
- no accepted attempt removed.

### External
- complete official 3,000-image VinDr test release;
- strict-target-positive image count;
- strict Lung Opacity box count;
- number of zero-strict-target images;
- all ten frozen RSNA checkpoints applied without adaptation;
- no VinDr model/checkpoint/threshold selection;
- no defensible VinDr patient linkage.

Verify each value from numerical/provenance artifacts, not manuscript prose
alone.

If any count is inconsistent across canonical artifacts:
- stop;
- document;
- HANDOFF;
- user review.

---

## FIGURE DESIGN

The figure should communicate DATA/ANALYSIS FLOW, not CONSORT-like prospective
recruitment.

Preferred conceptual structure:

### Left / upper branch — RSNA internal development/testing

Official RSNA Stage 2 source
↓
Deterministic compute-scoped selected cohort
- 5,000 studies
- 2,136 patient groups

↓ split by patient group

Training
- 3,500 studies
- 1,492 patient groups

Validation
- 750 studies
- 321 patient groups

Internal testing
- 750 studies
- 323 patient groups
- 169 strict opacity-positive studies
- 268 reference boxes

↓
Two disclosed pipelines
- Faster R-CNN: five retained runs
- YOLO11s: five retained runs

↓
Internal evaluation:
- ranking
- frozen operating points
- exact-score FROC
- run/patient uncertainty
- timing

### Right / lower branch — frozen external transport

Official VinDr-CXR v1.0.0 test release
- 3,000 released images
- 84 strict Lung Opacity-positive images
- 95 strict target boxes
- 2,916 images without a strict target box

↓
same ten frozen RSNA-trained checkpoints
↓
no adaptation
no VinDr threshold selection
no VinDr calibration fitting
no ontology tuning
↓
external ranking / FROC / transported operating points

Include a concise note:
"VinDr patient linkage unavailable; external observational unit = released
image."

Do NOT call 3,000 images 3,000 independent patients.

---

## VISUAL REQUIREMENTS

Create the figure through repository code.

Do NOT manually draw/edit a publication-critical SVG/PDF/PNG.

Use the repository's existing plotting stack and style conventions where
possible.

Requirements:

- journal-clean;
- grayscale-safe;
- readable in print;
- no decorative illustration;
- no excessive colour dependence;
- legible at likely double-column width;
- concise labels;
- consistent typography;
- no clipped elements;
- vector output if supported, plus the repository's normal raster publication
  format if applicable.

Do not add icons requiring external licensing.

No specific colour palette should be introduced unless the repository already
has one for publication figures.

---

## IMPLEMENTATION

1. Identify canonical source artifacts for every displayed count.
2. Create a versioned deterministic generation script/config if needed.
3. Do not duplicate values as arbitrary hardcoded constants if they can be read
   from canonical artifacts.
4. Fail loudly if expected counts drift.
5. Produce source/provenance metadata binding:
   - generator hash;
   - config hash if applicable;
   - input artifact hashes;
   - output hash.
6. Add tests checking the important counts and figure input schema.
7. Add the figure to the publication artifact inventory if appropriate.
8. Add reproduction command to README/docs/REPRODUCIBILITY.md.

---

## MANUSCRIPT INTEGRATION

Determine the most natural location, likely near cohort/Methods.

Add a concise caption that makes clear:

- retrospective secondary analysis;
- internal patient-disjoint split;
- external full released test cohort;
- external checkpoints were frozen and applied without adaptation;
- VinDr image is the external resampling unit because defensible patient linkage
  was unavailable.

Do not overload the caption with methodology already in Methods.

Update:
- report/paper_draft.md;
- supplement/cross-references as needed;
- docs/REPORTING_CHECKLIST.md.

If CLAIM item 35 was previously "No" solely because a single flow diagram was
absent, reassess that item carefully against the exact final reporting content.

Do NOT automatically change other CLAIM "No" items.

---

## TESTS / VERIFICATION

Run:

- figure-generation tests;
- relevant count/provenance tests;
- artifact verifier;
- manuscript claim verifier if numerical manuscript content changes;
- link/cross-reference checks;
- git diff --check.

Visually inspect the generated figure for:
- clipping;
- font size;
- arrow clarity;
- mistaken implication of prospective enrolment;
- mistaken patient counts;
- inconsistent numbers.

---

## COMPLETION

Update CODEX.md only with durable state:
- new canonical flow figure;
- generation source;
- reporting-gap change if applicable.

Prepend exactly one HANDOFF.md entry:
- source counts verified;
- files changed;
- figure path;
- tests/verifiers;
- remaining issue if any.

Do not commit/push/tag/publish.

STOP FOR USER REVIEW.
BATCH 55 — Numerical Presentation and Significant-Digit Audit
# BATCH 55 — Numerical Presentation and Significant-Digit Audit

This is a standalone Codex session.

Use Extra High reasoning.

Follow AGENTS.md and existing repository rules.

Before substantive work read:
- AGENTS.md;
- newest HANDOFF.md entry;
- CODEX.md;
- relevant PROJECT_SPEC.md sections;
- docs/DECISION_LOG.md;
- docs/REPRODUCIBILITY.md;
- docs/FINAL_MANUSCRIPT_AUDIT.md;
- report/paper_draft.md;
- report/paper_claim_sources.yaml;
- publication figure/table generation code relevant to manuscript numbers.

Record branch/HEAD/status/staged/uncommitted state.

Protect unrelated changes.

Execute ONLY Batch 55.

No scientific analysis changes are authorized.

Do not commit, push, tag, publish or upload.

---

## PURPOSE

Improve human-facing numerical presentation by removing unjustified/excessive
decimal precision while preserving:

- exact underlying source results;
- scientific interpretation;
- confidence-interval zero-crossing interpretation;
- exact thresholds;
- artifact traceability;
- manuscript claim verification.

This is an EDITORIAL PRESENTATION batch.

It must NOT modify scientific source values.

---

## PREREQUISITE GATE

Verify:

1. Canonical numerical sources live under results/ and/or the existing
   publication artifact manifest.
2. report/paper_claim_sources.yaml currently verifies central manuscript
   numbers.
3. No unresolved scientific result discrepancy exists.
4. Batch 53 outputs, if completed and manuscript-integrated, are already in a
   verified state.

If any manuscript number disagrees with its canonical source beyond existing
rounding policy:
- do not conceal it by rounding;
- classify as scientific inconsistency;
- document;
- stop for review if material.

---

## PRESENTATION POLICY

Derive a coherent policy rather than blindly applying one decimal count
everywhere.

Use the following as guidance, not inflexible rules:

### Counts
Exact integers.

### Thresholds / protocol constants
Retain exact selected/configured values:
- e.g. 0.69, 0.05, 0.01;
- candidate floors as required to identify actual protocol.

### Ordinary proportions/metrics in narrative prose
Usually 3–4 significant digits.

### Very small external AP/metric values
Use enough digits to avoid rounding meaningful nonzero values to zero.

Examples:
- 0.002505 may reasonably become 0.0025;
- 0.000501 may reasonably remain around 0.00050.

Do not use scientific notation unless it improves readability.

### Confidence intervals
Usually 3–4 significant digits, but always preserve:
- sign;
- inclusion/exclusion of zero;
- interpretation.

### Means ± SD in main human-facing tables
Use precision appropriate to the metric scale, not raw computation precision.

### Timing
Usually 2 decimal places for ms/FPS where meaningful.
Retain enough digits for total elapsed values if provenance requires them in
technical documentation.

### Ratios
Usually 2 decimal places unless there is a scientific reason for more.

### Percentages
Use a coherent number of decimal places based on denominator/support.

---

## TASKS

1. Audit ALL narrative numerical claims in:
   - title if any;
   - abstract;
   - Introduction;
   - Methods;
   - Results;
   - Discussion;
   - Limitations;
   - Conclusion;
   - figure captions;
   - manuscript tables.

2. Identify:
   - gratuitous six-decimal output;
   - inconsistent rounding of the same endpoint;
   - mixed AP scales;
   - percentages whose apparent precision exceeds support;
   - CI formatting inconsistencies;
   - timing formatting inconsistencies.

3. Audit publication figures for:
   - excessive legend precision;
   - axis/annotation precision;
   - misleading rounding.

4. Audit manuscript-facing generated tables.

5. DO NOT alter raw/source CSV/JSON numerical result artifacts merely for
   presentation.

6. If table/figure generator formatting must change:
   - change formatting only;
   - preserve numeric source values.

7. Update report/paper_claim_sources.yaml ONLY where manuscript rounding or
   regex patterns require it.

8. Never loosen a claim tolerance more than necessary.

9. Ensure all new manuscript values deterministically map to exact canonical
   values.

10. Prefer recording the final presentation policy in an EXISTING suitable
    methodology/reproducibility/editorial documentation file.

Create a new dedicated numerical-style document only if there is no natural
existing home.

Avoid documentation proliferation.

---

## SPECIAL FOCUS — ABSTRACT

The abstract should be readable as a scientific abstract rather than a dump of
machine precision.

Review values such as internal/external AP and frozen-threshold metrics.

Preserve the magnitude and scientific contrast while reducing meaningless
digits.

Do NOT alter the actual conclusion.

---

## SPECIAL FOCUS — SMALL EXTERNAL VALUES

The external results are genuinely close to zero.

Do not over-round in a way that:
- converts nonzero results to 0;
- hides detector differences;
- changes CI interpretation.

Explicitly verify every rounded external headline value against source.

---

## TESTS

Run:

- manuscript claim verifier;
- relevant table/figure generation tests;
- artifact verifier if generated publication files change;
- bibliography/link checks only if affected;
- git diff --check.

Create a machine-readable or documented before/after sample showing at least:
- one AP value;
- one CI;
- one threshold;
- one timing metric;
- one small external value.

---

## COMPLETION

Report in HANDOFF:
- presentation rules adopted;
- main places changed;
- whether any suspicious source/manuscript mismatch was found;
- verifier status.

Update CODEX.md only if a durable publication numerical-presentation policy was
established.

Do not commit/push/tag/publish.

STOP FOR USER REVIEW.
BATCH 56 — Final Scientific-Concision and Positioning Pass
# BATCH 56 — Final Scientific-Concision and Positioning Pass

This is a standalone Codex session.

Use Extra High reasoning.

Follow AGENTS.md and established project rules.

Read before editing:
- AGENTS.md;
- newest HANDOFF.md;
- CODEX.md;
- relevant PROJECT_SPEC.md;
- docs/DECISION_LOG.md;
- docs/LIMITATIONS.md;
- docs/FINAL_MANUSCRIPT_AUDIT.md;
- docs/REPORTING_CHECKLIST.md;
- docs/SUPPLEMENTARY.md;
- report/paper_draft.md;
- report/paper_claim_sources.yaml;
- current bibliography/citation audit.

Record branch/HEAD/status/staged/uncommitted state.

Execute ONLY Batch 56.

This is an EDITORIAL batch.

No new scientific result is authorized.

Do not commit, push, tag, publish or upload.

---

## PURPOSE

Perform a high-level journal-editor pass on the already focused final manuscript.

The goal is NOT to rewrite the scientific study.

The goal is to:

1. make the central methodological contribution unmistakable;
2. reduce repeated defensive caveats;
3. shorten the main text where possible;
4. preserve every scientifically necessary limitation;
5. keep detailed forensic/provenance material in supplement/docs rather than
   repeatedly in the central narrative.

The paper should NOT read primarily as:

"Faster R-CNN versus YOLO11s for pneumonia detection."

It should read as a controlled empirical study showing that distinct detector
evaluation objects need not transport together.

---

## CENTRAL THESIS LOCK

Preserve approximately this conceptual thesis:

"Preserved detector ranking does not imply preserved absolute performance or
transportable operating points."

The methodological objects that should remain conceptually distinct are:

- ranking performance;
- raw score scale;
- shared numerical thresholds;
- detector-specific validation-selected operating points;
- false-positive-budget/FROC behaviour;
- stochastic training variability;
- implementation efficiency;
- external cross-dataset/cross-annotation-ontology transportability.

Do not claim that score-scale mismatch itself is newly discovered.

Do not claim universal architecture superiority.

---

## PREREQUISITE GATE

Verify:

1. Batch 53, if completed, has settled the YOLO dtype sensitivity and any
   manuscript wording is verified.
2. Batch 54 figure integration is stable if completed.
3. Batch 55 numerical formatting has passed claim verification.
4. No unverified scientific outputs are pending manuscript integration.
5. Canonical manuscript remains report/paper_draft.md.

If a scientific inconsistency is discovered:
- do not editorially "fix" it;
- document it;
- stop if material.

---

## TASK 1 — WORD-COUNT BASELINE

Measure current word counts for at least:

- Abstract;
- Introduction;
- Methods;
- Results;
- Discussion;
- Limitations;
- Introduction-through-Discussion combined.

Record baseline before editing.

Target a meaningful but conservative reduction.

A useful target is approximately 8–15% reduction in central prose IF it can be
achieved without scientific loss.

Do not chase a quota.

---

## TASK 2 — REDUNDANCY MAP

Before rewriting, identify repeated explanations of:

- "does not establish";
- "does not imply";
- clinical non-validation;
- candidate-floor support;
- detection-cap support;
- FROC finite-frontier limitations;
- checkpoint-conditional vs training-procedure inference;
- D-ECE non-clinical calibration;
- timing not being clinical workflow speed;
- architecture/optimization confounding;
- external ontology mismatch;
- dtype sensitivity if now resolved;
- post-hoc n=5 threshold status.

For each repeated caveat decide its proper primary home:

### Methods
Protocol/estimand definition.

### Results
Immediate consequence necessary to interpret the result.

### Discussion
Scientific meaning.

### Limitations
Consolidated limitation.

Avoid restating the full qualification in all four.

---

## TASK 3 — FRONT-LOAD CONTRIBUTION

Review:

- title;
- abstract Background/Conclusions;
- final Introduction paragraph;
- opening Discussion paragraph;
- Conclusion.

Ensure the contribution is framed as evaluation methodology/transportability,
not a routine architecture contest.

Do not change the title merely for novelty if the current title is already
stronger and accurate.

Any title change must be demonstrably better and neutral.

---

## TASK 4 — MOVE DETAIL, DO NOT DELETE EVIDENCE

Candidates for compacting or moving into Supplementary material include:

- one-ULP coordinate-correction detail;
- low-level timing implementation provenance;
- repeated FROC floor/cap arithmetic already available in supplement;
- detailed D-ECE implementation caveats;
- secondary corruption/XAI details;
- detailed post-hoc threshold-sensitivity machinery;
- lengthy explanations of already-defined statistical targets.

Keep enough in the main text for reproducibility and correct interpretation.

Do not hide limitations merely to shorten the paper.

---

## TASK 5 — PRESERVE ESSENTIAL LIMITATIONS

The following must remain clearly visible somewhere appropriate in the main
paper:

- compute-scoped 5,000-study RSNA subset;
- no formal sample-size/power calculation;
- only two disclosed pipelines;
- five training runs per detector;
- training/optimization/normalization/precision asymmetry;
- disabled augmentation;
- historical n=3 threshold selection provenance;
- post-hoc n=5 sensitivity status;
- non-identical VinDr opacity ontology;
- low external positive-target support;
- unavailable defensible VinDr patient grouping;
- finite FROC support/floor/cap limitations;
- no prospective evaluation;
- no reader study;
- no validated clinical deployment;
- no complete subgroup/fairness assessment;
- checkpoint/reproducibility boundary as currently true.

Do not convert any genuine limitation into euphemistic language.

---

## TASK 6 — SENTENCE-LEVEL QUALITY

Improve:

- long nested clauses;
- repeated parentheticals;
- unnecessary implementation nouns;
- paragraph openings;
- transitions between internal and external results;
- distinction between "ranking transported" and "performance transported".

Prefer precise active scientific prose.

Do not use promotional language:
- superior;
- definitive;
- decisive;
- revolutionary;
- state-of-the-art;
- clinically useful;
unless directly and narrowly justified.

---

## TASK 7 — SUPPLEMENT CROSS-REFERENCES

Where detail is moved:
- ensure the supplement contains it;
- add accurate cross-reference;
- do not create phantom sections;
- do not duplicate entire paragraphs unnecessarily.

---

## TASK 8 — REFERENCES

Do not perform a new literature-expansion project.

But if editing changes the scope of a claim:
- verify its citation still supports it;
- update citation audit if necessary.

No uncited novelty claims.

---

## TASK 9 — CLAIM-STRENGTH AUDIT

After editing, specifically search:

- superior;
- significant;
- robust;
- generalize/generalizes/generalizable;
- validate/validated/validation;
- clinical;
- diagnosis/pneumonia diagnosis;
- architecture;
- causal;
- independent;
- patient;
- full frontier;
- exhaustive;
- threshold-independent.

Confirm every use remains scientifically bounded.

---

## TASK 10 — WORD-COUNT RESULT

Record before/after section word counts.

Explain major reductions.

Do not count bibliography/repository documentation as manuscript concision.

---

## VERIFICATION

Run:

- manuscript claim verifier;
- scientific artifact verifier;
- bibliography/citation checks;
- manuscript link/cross-reference checks;
- relevant tests;
- git diff --check.

If any claim verifier requires a tolerance change merely because prose changed,
make the narrowest justified update.

No scientific source artifacts should change in this batch.

---

## COMPLETION

Update CODEX.md only if a durable manuscript-positioning decision changed.

Prepend exactly one HANDOFF entry with:
- before/after word counts;
- key editorial changes;
- scientific content deliberately preserved;
- tests/verifiers.

Do not commit/push/tag/publish.

STOP FOR USER REVIEW.
BATCH 57 — Ethics and Consent Determination Packet
# BATCH 57 — Ethics and Consent Determination Packet

This is a standalone Codex session.

Use Extra High reasoning.

Follow AGENTS.md and repository rules.

Read first:
- AGENTS.md;
- newest HANDOFF.md;
- CODEX.md;
- relevant PROJECT_SPEC.md;
- docs/AUTHOR_DECLARATIONS_TODO.md;
- docs/REPORTING_CHECKLIST.md;
- docs/FINAL_MANUSCRIPT_AUDIT.md;
- docs/DECISION_LOG.md;
- report/paper_draft.md;
- repository-held/cited RSNA/NIH data-use documentation;
- repository-held/cited PhysioNet/VinDr documentation relevant to access,
  de-identification, source-study ethics and consent.

Record Git state before changing anything.

Execute ONLY Batch 57.

Do not contact any institution.

Do not send email.

Do not fabricate an ethics determination.

Do not commit, push, tag or publish.

---

## PURPOSE

Prepare a complete, concise packet enabling the human authors to obtain the
responsible institution's actual determination for this retrospective secondary
analysis.

The repository/manuscript must continue to distinguish:

1. ethics approval/consent for the ORIGINAL RSNA/VinDr source studies;
2. data-use/access permission;
3. the institutional ethics/IRB/research-governance determination for THIS
   secondary analysis.

Source-study approval does NOT automatically establish the determination for
the present study.

Public/de-identified data do NOT by themselves establish "no ethics review
required."

Codex must never make that legal/institutional decision.

---

## PREREQUISITE GATE

Verify the current manuscript/declaration state.

Identify every location that currently says or implies:

- no separate institutional approval was obtained;
- ethics determination is unresolved;
- consent applicability is unresolved;
- source-study approval/waiver information;
- author action required.

Do not assume the latest prose is correct merely because it exists.

---

## TASK 1 — FACTUAL STUDY SYNOPSIS

Create:

`docs/ETHICS_DETERMINATION_PACKET.md`

or use an existing dedicated ethics document if one already exists and is
clearly canonical.

Include a concise factual synopsis based only on repository evidence:

### Study design
- retrospective secondary computational analysis;
- no participant recruitment;
- no participant contact;
- no clinical intervention;
- no treatment allocation;
- research object-localization benchmark/transportability study;
- no clinical deployment.

### Data
RSNA/NIH:
- source used;
- de-identified/challenge context as documented;
- local subset role;
- patient grouping mechanism as actually used.

VinDr:
- credentialed PhysioNet access;
- official test release;
- strict local Lung Opacity target;
- restricted derivatives remain private where required;
- no defensible patient linkage found locally.

### Processing
- model training on RSNA;
- inference/evaluation;
- frozen external testing;
- aggregate statistical analysis;
- no attempt to re-identify subjects.

Do not add facts not supported by the repository/source documentation.

---

## TASK 2 — DATA-HANDLING SUMMARY

Document, at a high level:

- what source files were accessed;
- whether direct identifiers were available;
- whether any patient-level linkage keys were used;
- whether local source images are redistributed;
- whether restricted VinDr predictions/derivatives are public;
- what aggregate outputs are public;
- whether checkpoints contain source images (they should not, but do not infer
  beyond evidence);
- access/control boundary.

This is for ethics-office context, not for making the decision.

---

## TASK 3 — QUESTIONS FOR THE RESPONSIBLE INSTITUTION

Prepare a short structured request asking the institution to determine, using
THEIR terminology:

1. Whether the present secondary analysis requires ethics/IRB review.
2. Whether it qualifies as:
   - approved research;
   - exempt research;
   - not-human-subjects research;
   - review not required;
   - or another local category.
3. Whether informed consent for the present secondary analysis is:
   - required;
   - waived;
   - not applicable;
   - or governed by another determination.
4. Which institution/committee/office should be named in publication.
5. Whether a reference/decision number exists.
6. Date of determination.
7. Any wording the institution requires in manuscripts.
8. Whether the use of credentialed VinDr data changes the institutional review
   requirement.

Do not suggest which answer the institution "should" give.

---

## TASK 4 — AUTHOR EMAIL TEMPLATE

Create a concise professional email template the corresponding author can
PERSONALLY send.

The email should:

- identify authors/institutions;
- explain the retrospective secondary computational nature;
- identify RSNA/NIH and credentialed VinDr-CXR;
- state no participant contact/intervention;
- ask for a written determination suitable for journal reporting;
- offer the study synopsis/manuscript if needed.

Do not send it.

---

## TASK 5 — FORM-READY SUMMARY

Prepare a compact approximately 150–250 word study description suitable for a
research-governance/ethics enquiry form.

No claims beyond evidence.

---

## TASK 6 — MANUSCRIPT DECLARATION TEMPLATES

Prepare publication-ready templates with explicit placeholders:

### Ethics template
"[Responsible institution/board] determined that [actual determination] for
this retrospective secondary analysis ([reference], [date])."

### Consent template
"[Actual consent determination and responsible body/rationale]."

Create variants only for plausible structural formatting, such as:
- formal approval;
- exemption;
- not-human-subjects/review-not-required.

Mark every variant:

`TEMPLATE ONLY — INVALID FOR SUBMISSION UNTIL REPLACED BY ACTUAL INSTITUTIONAL DETERMINATION.`

Do not insert any unconfirmed variant into the paper as fact.

---

## TASK 7 — CURRENT MANUSCRIPT SAFETY AUDIT

Review the current ethics/consent prose.

Correct only wording that wrongly implies:
- original-source ethics = present-study ethics;
- source consent waiver = present-study consent determination;
- de-identification automatically removes all institutional requirements.

Maintain `AUTHOR ACTION REQUIRED` until real facts are provided.

Do not weaken factual source-study reporting.

---

## TASK 8 — AUTHOR CHECKLIST

End the packet with exactly what the author needs to return for a later
declarations batch:

- responsible institution/board;
- determination type/verbatim wording;
- decision/reference number if any;
- date;
- consent determination;
- any institution-required publication wording;
- confirmation of RSNA/VinDr terms compliance if separately required.

---

## VERIFICATION

Run:
- link/reference checks for cited repository/source documents;
- manuscript claim verifier if manuscript text changes;
- reporting checklist consistency check;
- git diff --check.

No numerical scientific artifact should change.

---

## COMPLETION

Update CODEX.md only with durable state:
"ethics packet prepared; actual determination remains human/institutional."

Prepend one HANDOFF entry:
- packet path;
- manuscript changes if any;
- exact outstanding human facts.

Do not mark ethics resolved.

Do not commit/push/tag/publish.

STOP FOR USER REVIEW.
BATCH 58 — Publication Release Identity and Checkpoint Availability Preparation
# BATCH 58 — Publication Release Identity and Checkpoint Availability Preparation

This is a standalone Codex session.

Use Extra High reasoning.

Follow AGENTS.md and repository rules.

Read first:
- AGENTS.md;
- newest HANDOFF.md;
- CODEX.md;
- relevant PROJECT_SPEC.md;
- README.md;
- pyproject.toml;
- CITATION.cff;
- CHANGELOG.md;
- release notes files;
- docs/REPRODUCIBILITY.md;
- docs/AUTHOR_DECLARATIONS_TODO.md;
- docs/FINAL_MANUSCRIPT_AUDIT.md;
- docs/DECISION_LOG.md;
- report/paper_draft.md;
- results/checkpoint_release_manifest.json;
- results/publication_artifact_manifest.json;
- .gitignore and relevant release/package scripts.

Record:
- current branch;
- HEAD;
- tags;
- status;
- staged/uncommitted files.

Execute ONLY Batch 58.

DO NOT:
- create/push a tag;
- create a GitHub Release;
- upload checkpoints;
- upload archives;
- mint/register a DOI;
- publish to Zenodo/Hugging Face/OSF;
- change repository visibility.

Prepare only.

---

## PURPOSE

Resolve the remaining PUBLICATION-STATE ambiguity by preparing:

1. a reproducible immutable submission release process;
2. accurate data/code/model availability language;
3. a technically verified checkpoint-release package IF the human author later
   chooses and is legally permitted to release checkpoints.

This batch must distinguish clearly between:

- what already exists;
- what is locally prepared;
- what is publicly released;
- what still requires explicit human action.

Never claim a release/tag/DOI/public checkpoint URL exists unless verified.

---

## PREREQUISITE GATE

Determine from actual repository/Git state:

1. Current project/package version.
2. Current HEAD.
3. Existing local tags.
4. Existing remote tags if accessible without mutation.
5. Whether the repository currently claims `v2.0.0`.
6. Whether `v2.0.0` actually exists as a tag.
7. Whether any GitHub Release exists, if queryable read-only.
8. Whether a Zenodo/archive DOI already exists.
9. Current CITATION.cff state.
10. Current release notes/changelog state.
11. Current manuscript availability wording.
12. Current exact checkpoint availability/public URL status.

If documentation claims an artifact exists when it does not:
- fix the wording;
- do not fabricate the artifact.

---

# PART A — IMMUTABLE SUBMISSION RELEASE PREPARATION

## A1. RELEASE MODEL

Use the repository's existing version/release philosophy unless a genuine
inconsistency exists.

Preserve distinction between:
- living manuscript;
- frozen scientific evidence boundary;
- exact submitted snapshot.

Determine the cleanest final submission identifier strategy, preferably:
- exact commit SHA;
- annotated Git tag;
- GitHub Release;
- optional archival DOI.

Do not create them yet.

---

## A2. RELEASE METADATA AUDIT

Synchronize as appropriate:

- pyproject.toml version;
- package version;
- CITATION.cff;
- CHANGELOG;
- release notes;
- README;
- reproducibility docs.

Do not bump a version merely because this batch exists if current release policy
says otherwise.

If a version bump is warranted, explain and stop for user approval before
making a semantic release-policy change.

---

## A3. FINAL RELEASE CHECKLIST

Create or update a concise publication-release checklist giving exact commands
for the HUMAN author to run after final review.

It must include:

1. verify clean/expected Git state;
2. run lock/environment checks;
3. run tests;
4. run Ruff/format;
5. run artifact verifier;
6. run manuscript claim verifier;
7. run package smoke;
8. run git diff --check;
9. confirm final manuscript/PDF;
10. commit reviewed tracked changes;
11. create annotated tag;
12. push commit/tag;
13. create GitHub Release;
14. optionally create archival DOI;
15. insert final commit/tag/DOI into manuscript;
16. re-run manuscript verifier after insertion if relevant.

Use repository-real commands, not generic placeholders where actual commands are
available.

---

## A4. RELEASE-IDENTIFIER GUARD

Add or extend verification so final submission cannot silently retain an
unresolved release identifier.

Do NOT make ordinary development fail solely because an AUTHOR ACTION REQUIRED
placeholder still exists before the human release step unless that matches
existing verifier architecture.

Prefer a dedicated final-submission gate/check.

---

# PART B — CHECKPOINT AVAILABILITY

## B1. CURRENT STATE

Verify:

- ten expected checkpoint identities;
- whether each file currently exists locally;
- exact SHA256;
- size;
- detector/seed mapping;
- whether a public URL exists;
- whether repository docs accurately state current availability.

Do not print or expose credentials/local secrets.

---

## B2. REDISTRIBUTION / LICENSING AUDIT

Inspect repository-held licenses/terms for:

- repository-authored code;
- pretrained model sources/framework terms;
- RSNA source-data restrictions;
- VinDr/PhysioNet terms;
- any relevant checkpoint redistribution constraints already documented.

Do NOT invent a legal conclusion.

Classify each question as:
- clearly supported;
- clearly prohibited;
- unclear / requires human/legal/provider confirmation.

If redistribution rights are unclear, produce a concise human checklist.

Do not upload anything.

---

## B3. CHECKPOINT PACKAGER

If not already present, implement a safe LOCAL packaging/verification tool that:

1. loads expected checkpoint manifest;
2. verifies all ten exact hashes;
3. verifies sizes/identities;
4. refuses mismatched/missing files;
5. creates a clean release staging directory/archive;
6. includes:
   - checksums;
   - model/seed mapping;
   - software/config references;
   - README describing purpose;
7. excludes:
   - source images;
   - restricted VinDr derivatives;
   - credentials;
   - local paths;
   - caches;
   - unrelated predictions;
   - environment secrets;
8. writes a package manifest;
9. never uploads.

Use deterministic/archive-safe behaviour where feasible.

Add tests using synthetic/small fake files rather than real checkpoint binaries.

---

## B4. AVAILABILITY TEXT — TWO AUTHOR OPTIONS

Prepare two polished variants.

### OPTION A — CHECKPOINTS RELEASED

Text must state:
- exact public release/archive identifier placeholder;
- all ten frozen checkpoints;
- hashes/manifest;
- what reproduction they enable;
- source data still require provider access;
- license/terms only if confirmed.

### OPTION B — CHECKPOINTS NOT PUBLICLY RELEASED

Text must state:
- code/configs/aggregate artifacts are public;
- exact frozen checkpoint binaries are not public;
- exact inference reproduction therefore requires access to those exact files;
- retraining reproduction is distinct from exact inference reproduction;
- source data require provider access.

Do not make Option B sound more reproducible than it is.

Do not insert either option as final manuscript fact until the human author
chooses.

---

## B5. SINGLE HUMAN DECISION POINT

Where possible, eliminate multiple contradictory checkpoint placeholders.

Centralize the unresolved decision in:
- docs/AUTHOR_DECLARATIONS_TODO.md;
- one clearly identified manuscript placeholder;
- release checklist.

Do not scatter alternatives throughout the paper.

---

## B6. README / REPRODUCIBILITY CONSISTENCY

Ensure all documentation distinguishes four levels:

1. software verification;
2. committed-analysis reproduction;
3. exact inference reproduction;
4. exact retraining reproducibility.

Do not let a GitHub badge/green CI imply exact GPU reproduction.

---

## TESTS / VERIFICATION

Run:

- packaging tests;
- hash-manifest checks;
- artifact verifier;
- manuscript claim verifier if wording changes;
- package smoke;
- Ruff for changed scripts;
- git diff --check.

No real binary upload.

No remote mutation.

---

## COMPLETION

Update CODEX.md with durable prepared state only.

Prepend HANDOFF with:
- exact current release state;
- exact checkpoint state;
- files/scripts prepared;
- unresolved legal/author decisions;
- exact next human actions.

Do not claim the project is publicly released unless it actually is.

Do not commit/push/tag/publish.

STOP FOR USER REVIEW.
BATCH 59 — Insert Final Human Declarations
This is the one prompt you should not run until you have the actual facts. Replace the bracketed section first.

# BATCH 59 — Insert Final Human Declarations

This is a standalone Codex session.

Use Extra High reasoning.

Follow AGENTS.md and established repository rules.

Before substantive work:
- read AGENTS.md;
- newest HANDOFF.md;
- CODEX.md;
- relevant PROJECT_SPEC.md;
- docs/AUTHOR_DECLARATIONS_TODO.md;
- docs/ETHICS_DETERMINATION_PACKET.md if present;
- docs/REPORTING_CHECKLIST.md;
- docs/FINAL_MANUSCRIPT_AUDIT.md;
- docs/REPRODUCIBILITY.md;
- report/paper_draft.md;
- current release/checkpoint availability documentation.

Record Git state.

Execute ONLY Batch 59.

Never infer a missing declaration.

If any required human fact below remains blank/ambiguous, STOP rather than guess.

Do not commit/push/tag/publish.

---

# AUTHOR-CONFIRMED FACTS

Treat ONLY this block plus verifiable repository/public release state as
authority for author-controlled declarations.

## Final author names/order
[INSERT]

## Corresponding author
[INSERT]

## Funding/support
[INSERT EXACT HUMAN-CONFIRMED FACTS]

Include funder role if applicable.

## Competing interests
[INSERT EXACT HUMAN-CONFIRMED FACTS FOR EACH AUTHOR]

## Present-study ethics determination
Responsible institution/board/office:
[INSERT]

Exact determination:
[INSERT]

Reference/identifier:
[INSERT OR "none issued" ONLY IF CONFIRMED]

Date:
[INSERT]

Institution-required wording if any:
[INSERT]

## Present-study consent determination
[INSERT EXACT CONFIRMED DETERMINATION]

## Data-use compliance confirmation
RSNA/NIH/Kaggle:
[INSERT]

VinDr/PhysioNet:
[INSERT]

## CRediT contributions
Pouyan Delivandani:
[INSERT]

Mohammad Amin Hajialirezaei:
[INSERT]

Any additional/final authors:
[INSERT OR CONFIRMED NONE]

## Patient/public involvement
[INSERT CONFIRMED FACT]

## Checkpoint release decision
Choose exactly one:
[RELEASED / NOT PUBLICLY RELEASED]

If released:
public URL:
[INSERT]
release/archive identifier:
[INSERT]
license/terms wording:
[INSERT ONLY IF CONFIRMED]

If not released:
reason/boundary:
[INSERT]

## Final code/repository release
Exact commit SHA:
[INSERT IF ALREADY CREATED]

Tag:
[INSERT IF ALREADY CREATED]

GitHub Release:
[INSERT IF ALREADY CREATED]

Archive DOI:
[INSERT IF ALREADY CREATED OR CONFIRMED NONE]

## Target journal if already chosen
[INSERT OR LEAVE "not yet chosen"]

---

## PURPOSE

Replace unresolved AUTHOR ACTION REQUIRED declaration fields with actual,
author-confirmed facts.

Do not change scientific results.

Do not infer missing information from affiliations, Git history, repository
absence, or source-study documentation.

---

## PREREQUISITE GATE

1. Verify the facts block is complete enough for the requested declaration work.
2. Verify any supplied:
   - commit SHA;
   - tag;
   - release;
   - DOI;
   - checkpoint public URL
   actually exists if technically queryable read-only.
3. Verify ethics wording does not confuse:
   - source-study approvals;
   - present-study institutional determination.
4. Verify checkpoint wording matches actual public state.

If a supplied public identifier does not resolve:
- do not insert it as fact;
- report discrepancy;
- stop.

---

## TASK 1 — DECLARATIONS

Finalize:

- funding/support;
- competing interests;
- ethics/data use;
- consent;
- CRediT;
- data/code/model availability;
- patient/public involvement;
- AI-assistance statement only if still accurate;
- corresponding-author details where needed.

Use target-journal-neutral scholarly wording unless a target journal has already
been explicitly chosen and its requirements are available.

Do not overstate ethics conclusions beyond the actual institutional wording.

---

## TASK 2 — ETHICS DISTINCTION

Keep separate:

A. present-study institutional determination;

B. original VinDr source-study IRB/consent history;

C. RSNA/NIH source-data provenance;

D. data-use/access compliance.

Do not substitute one for another.

---

## TASK 3 — CRediT

Use only human-confirmed roles.

Do not infer supervision, conceptualization, resources, validation or funding
acquisition merely from authorship/affiliation.

Ensure manuscript wording and submission-ready metadata agree.

---

## TASK 4 — DATA/CODE/MODEL AVAILABILITY

If checkpoints are RELEASED:
- verify public identifier;
- state exact scope;
- distinguish checkpoint release from source-image access.

If NOT RELEASED:
- state the limitation plainly;
- do not imply exact inference reproducibility from Git alone.

Use exact final repository commit/tag/release identifiers only when they
actually exist.

---

## TASK 5 — REMOVE RESOLVED PLACEHOLDERS

Search tracked submission-relevant files for:

- AUTHOR ACTION REQUIRED
- TODO
- TBD
- placeholder
- unresolved
- not yet
- release candidate
- manuscript-ready
- finalization required

Classify every occurrence as:

1. legitimate historical provenance;
2. local orchestration;
3. genuinely unresolved submission blocker;
4. stale wording that should be fixed.

Do not erase historical provenance merely because it contains an old warning.

---

## TASK 6 — REPORTING CHECKLIST

Regenerate/reassess CLAIM 2024 rows affected ONLY by newly resolved human facts.

For example:
- availability;
- funding;
- ethics-related reporting where applicable.

Do not convert genuine scientific-reporting gaps to "Yes" just because
declarations are resolved.

No certification language.

---

## TASK 7 — AUTHOR TODO DOCUMENT

Update docs/AUTHOR_DECLARATIONS_TODO.md to reflect actual resolved status.

Preserve useful historical/audit provenance if repository conventions require
it.

It should no longer misleadingly say an item is unresolved if the actual
confirmed fact has been inserted.

---

## TASK 8 — CONSISTENCY AUDIT

Check that declarations agree across:
- manuscript;
- README/release docs;
- CITATION.cff where relevant;
- reporting checklist;
- author todo/audit docs.

---

## VERIFICATION

Run:
- manuscript claim verifier;
- artifact verifier;
- bibliography/link checks;
- reporting-checklist checks;
- unresolved-placeholder scan;
- git diff --check.

No scientific result files should change.

---

## COMPLETION

Update CODEX.md with durable resolved declaration state.

Prepend HANDOFF with:
- declarations resolved;
- any genuinely remaining human blocker;
- public release/checkpoint state;
- tests/verifiers.

Do not commit/push/tag/publish unless separately authorized.

STOP FOR USER REVIEW.
BATCH 60 — Final Adversarial Submission Gate and Article PDF
# BATCH 60 — Final Adversarial Submission Gate and Article PDF

This is a standalone Codex session.

Use Extra High reasoning.

This is the FINAL ADVERSARIAL AUDIT.

Follow AGENTS.md and all established repository rules.

Do not assume Batches 53–59 succeeded merely because their numbers are lower.

Before substantive work:

1. Read AGENTS.md.
2. Read newest HANDOFF.md first.
3. Read CODEX.md.
4. Read relevant PROJECT_SPEC.md.
5. Read:
   - docs/DECISION_LOG.md
   - docs/LIMITATIONS.md
   - docs/REPORTING_CHECKLIST.md
   - docs/REPRODUCIBILITY.md
   - docs/AUTHOR_DECLARATIONS_TODO.md
   - docs/FINAL_MANUSCRIPT_AUDIT.md
   - docs/FINAL_SUBMISSION_AUDIT.md
   - relevant dtype/flow/release documentation created in Batches 53–59.
6. Read report/paper_draft.md.
7. Record:
   - branch;
   - HEAD;
   - working-tree status;
   - staged state;
   - local tags;
   - current canonical files.

Execute ONLY Batch 60.

Do not commit, push, tag, publish, release or upload.

---

## PURPOSE

Determine whether the current project is genuinely ready for:

- author review;
- journal submission;

after all lower-than-hard issues addressed in Batches 53–59.

Regenerate the final article PDF only after the scientific/manuscript audit
passes sufficiently to justify doing so.

This batch must be adversarial.

Do not "help" the manuscript pass by weakening the audit.

---

# 1. REPOSITORY AND CANONICAL-STATE AUDIT

Verify:

- canonical manuscript;
- historical report/manuscript/PDF status;
- results/ as numerical source of truth;
- current publication manifest;
- current claim manifest;
- checkpoint manifest;
- current release state;
- current declarations state;
- current supplementary source.

Check Git state for accidental:
- staged local orchestration files;
- machine-specific paths;
- credentials;
- source data;
- checkpoint binaries;
- restricted VinDr artifacts.

---

# 2. FULL PORTABLE VERIFICATION

Run the repository's exact current commands for:

- lock/environment verification;
- Ruff format;
- Ruff lint;
- full portable pytest;
- package smoke;
- scientific/publication artifact verifier;
- manuscript claim verifier;
- bibliography/citation checks;
- link/cross-reference checks;
- git diff --check.

If scientific-data tests require licensed local data, distinguish:
- portable suite;
- authorized-data suite.

Do not imply portable CI runs GPU inference.

Record every command and result.

---

# 3. BATCH 53 DTYPE-SENSITIVITY AUDIT

If Batch 53 completed:

Verify:
- historical FP32 artifacts preserved;
- new bfloat16 internal artifacts versioned;
- all five YOLO checkpoints represented;
- seed 271 retained;
- no threshold re-selection;
- no training;
- actual dtype recorded;
- manuscript wording agrees with sensitivity results.

Answer:
- Did dtype materially affect AP?
- score scale?
- threshold emissions?
- FROC?
- transport interpretation?

Ensure the paper does not claim dataset shift alone explains external collapse
unless actually demonstrated.

If Batch 53 did not complete:
determine whether the original FP32/bfloat16 limitation remains a submission
blocker or a defensible limitation for the target paper.

Do not pretend it disappeared.

---

# 4. DATA-FLOW FIGURE AUDIT

If Batch 54 completed:

Verify every displayed count against canonical artifacts.

Specifically:
- 26,684 RSNA source studies if displayed;
- 5,000 selected studies;
- 2,136 patient groups;
- 3,500/750/750 split;
- 1,492/321/323 patient groups;
- internal positives/boxes;
- 5 + 5 retained runs;
- 3,000 VinDr images;
- 84 strict-target-positive images;
- 95 strict boxes;
- 2,916 zero-strict-target images;
- ten frozen external checkpoints.

Ensure figure does NOT:
- call images patients;
- imply prospective enrolment;
- imply VinDr patient independence.

Visually inspect.

---

# 5. NUMERICAL-PRESENTATION AUDIT

Verify Batch 55 changes:

- source numbers unchanged;
- rounded manuscript values map to exact sources;
- no small external value rounded to misleading zero;
- CI zero-crossing preserved;
- thresholds exact;
- consistent AP scale;
- consistent precision policy.

Trace at least 25 manuscript numbers across:

- Abstract;
- cohort;
- internal AP;
- shared/frozen thresholds;
- exact-score FROC;
- uncertainty;
- timing;
- external AP;
- external threshold transport;
- external FROC;
- dtype sensitivity if present.

For each record:
- manuscript value;
- exact source;
- source row/cell/path/calculation;
- source exact value;
- manuscript rounding;
- PASS/FAIL.

---

# 6. CONCISION / CLAIM-STRENGTH AUDIT

Assess whether Batch 56 accidentally strengthened claims while shortening prose.

Search and inspect every relevant use of:

- superior;
- significant;
- robust;
- validated;
- validation;
- generalize;
- generalizable;
- generalization;
- clinical;
- diagnosis;
- pneumonia;
- architecture;
- causal;
- independent;
- full;
- exhaustive;
- threshold-independent;
- state-of-the-art.

Verify central narrative still distinguishes:

- ranking;
- absolute performance;
- raw score;
- operating point;
- false-positive budget;
- training variability;
- implementation efficiency;
- transportability.

Ensure the paper is not reduced to:
"Faster R-CNN beats YOLO."

---

# 7. DATA/SPLIT/LEAKAGE AUDIT

Verify:

- patient-disjoint internal split;
- train/validation/internal-test roles;
- checkpoint selection from validation;
- threshold selection from validation only;
- internal test not used for tuning;
- VinDr not used for:
  - training;
  - fine-tuning;
  - checkpoint selection;
  - threshold selection;
  - calibration fitting;
  - ontology tuning after results.

Confirm post-hoc n=5 threshold selection remains labeled post-hoc.

---

# 8. FROC AUDIT

Search:
- FROC;
- continuum;
- exhaustive;
- full frontier;
- threshold-independent;
- candidate;
- floor;
- cap;
- interpolation;
- extrapolation.

Verify:

- observed exact-score language;
- candidate-floor limits;
- detection-cap limits;
- internal bound interpretation;
- external missing-support reversal possibility;
- no unsupported unrestricted-frontier superiority claim.

---

# 9. STATISTICAL AUDIT

For every primary/secondary uncertainty statement verify:

- observational unit;
- run resampling;
- patient/image resampling;
- independent run resampling;
- same-number seeds not treated as paired stochastic replicates;
- training-procedure vs checkpoint-conditional targets;
- marginal vs simultaneous CI language;
- no threshold-selection uncertainty falsely included;
- no patient-level VinDr claim.

Search:
- confidence interval;
- CI;
- p-value;
- significant;
- population;
- seed;
- checkpoint;
- training procedure.

---

# 10. EXTERNAL TRANSPORT AUDIT

Verify all external language:

- "external testing";
- "cross-dataset transportability";
- "cross-annotation-ontology transportability".

Ensure the paper does not imply:
- identical reference standard;
- identical-task validation;
- validated diagnosis;
- scanner-specific causal explanation;
- country-specific causal explanation;
- site-specific causal explanation;
- population-shift causal attribution;
- ontology alone caused collapse.

Verify exact strict VinDr ontology:
- Lung Opacity only;
- no silent Consolidation merge;
- no Infiltration merge;
- no Atelectasis merge;
- no ILD merge;
- no global Pneumonia-as-box-target substitution.

---

# 11. TRAINING / ARCHITECTURE AUDIT

Verify the manuscript still discloses:

- Faster R-CNN vs YOLO11s are pipelines, not isolated architecture families;
- optimization differs;
- normalization behaviour differs;
- precision differs;
- losses/assignment differ;
- augmentation disabled;
- only two pipelines;
- five runs;
- compute-scoped training subset.

Ensure no causal architecture-family conclusion crept in during editing.

---

# 12. TIMING AUDIT

Verify:

- matched decoded-host boundary;
- same image subset;
- batch size 1;
- explicit synchronization;
- technical repeats not training replicates;
- hardware/software identity;
- parameter counts;
- timing ratios;
- no clinical workflow-speed claim;
- incomplete historical operation counts remain demoted.

---

# 13. ETHICS / CONSENT AUDIT

Determine current actual state from Batch 57/59.

If an institutional determination has been inserted:

Verify:
- exact wording matches human-provided fact;
- institution/board/office;
- reference if any;
- date;
- consent determination;
- source-study approvals remain distinct.

If no real institutional determination has been supplied:

`READY FOR JOURNAL SUBMISSION` is NOT permitted if the target journal/institution
requires that determination before submission.

Do not invent a resolution.

---

# 14. FUNDING / COI / CRediT / PPI AUDIT

Verify each against the Batch 59 human-confirmed facts.

No role or declaration may be inferred from repository activity alone.

Search for stale contradictory placeholders.

---

# 15. RELEASE / AVAILABILITY AUDIT

Verify actual current state:

- exact commit;
- tag if any;
- GitHub Release if any;
- DOI if any;
- code availability;
- data access boundary;
- checkpoint availability.

Never call a planned tag/release/DOI public.

If checkpoints are public:
verify URL/manifest/hashes where possible.

If not:
ensure exact inference limitation is plainly stated.

Ensure green CI is not described as end-to-end scientific reproduction.

---

# 16. CLAIM 2024 REPORTING AUDIT

Regenerate/reassess the final CLAIM 2024 crosswalk against the current
manuscript.

Do not optimize the paper merely to turn "No" into "Yes".

A genuine limitation may remain "No".

No certification language.

Check specifically whether the study-flow figure changed the flow-diagram row.

---

# 17. REFERENCES / RELATED WORK

Verify:

- every in-text citation resolves;
- no duplicate keys;
- no phantom references;
- methodological citations support claims;
- recent detector-comparison/calibration/reporting references remain current for
  the paper's scope.

Do not launch broad literature expansion unless a factual gap is discovered.

---

# 18. PHANTOM-ARTIFACT AUDIT

Verify every manuscript-mentioned:

- figure;
- table;
- supplement section;
- config;
- script;
- checkpoint reference;
- dataset artifact;
- release identifier;
- documentation file.

Classify each as:
- committed/public;
- external/licensed;
- local/private;
- generated-on-replay;
- missing.

No missing item may be implied public.

---

# 19. UNRESOLVED-PLACEHOLDER SCAN

Search submission-relevant tracked files for:

- AUTHOR ACTION REQUIRED
- TODO
- TBD
- placeholder
- unresolved
- FIXME
- XXX
- release candidate
- insert
- pending
- not yet
- manuscript-ready

Classify every occurrence.

Historical provenance/local orchestration can remain.

Submission-facing unresolved facts must be listed explicitly.

---

# 20. FINAL PDF

ONLY after the above audit is sufficiently clean:

Regenerate the article PDF using the canonical build path from the canonical
manuscript.

Do not manually edit scientific PDF content.

Visually inspect every page for:

- title;
- author names/affiliations;
- abstract;
- headings;
- equations;
- tables;
- flow figure;
- PR/FROC/timing figures;
- captions;
- references;
- cross-references;
- page breaks;
- clipping;
- missing glyphs;
- strange hyphenation;
- line overflow;
- unresolved placeholders;
- broken URLs/DOIs where rendered.

Confirm PDF scientific content matches canonical manuscript.

---

# 21. FINAL AUDIT DOCUMENT

Rewrite/update:

`docs/FINAL_SUBMISSION_AUDIT.md`

with at least:

## AUDIT DATE / HEAD

## BLOCKING FAILURES

## AUTHOR ACTION REQUIRED

## SHOULD-FIX

## DEFENSIBLE LIMITATIONS

## VERIFIED CLEAN AREAS

## 25-NUMBER TRACEABILITY TABLE

## ANALYSIS-SCOPE TABLE

For each major analysis:
- dataset;
- sample size;
- observational unit;
- detector;
- runs/seeds;
- seed 271 status;
- historical/post-hoc/external/secondary classification;
- inferential/descriptive status.

## INTERNAL VS EXTERNAL PROTOCOL TABLE

## REPRODUCIBILITY LEVEL TABLE

## DECLARATION STATUS

## RELEASE / CHECKPOINT STATUS

## COMMANDS AND TESTS EXECUTED

## FINAL STATUS

Allowed statuses:

- NOT READY FOR SUBMISSION
- READY FOR AUTHOR REVIEW
- READY FOR JOURNAL SUBMISSION

Do not use READY FOR JOURNAL SUBMISSION if any genuinely required human factual
declaration or release identifier remains unresolved.

Do not downgrade a paper merely because defensible scientific limitations remain
when they are transparently reported.

---

# 22. TARGET-JOURNAL CHECK — ONLY IF ALREADY CHOSEN

If a target journal has been explicitly chosen in the prompt/CODEX/HANDOFF:

Audit only its CURRENT official author instructions for:
- manuscript type;
- word limits;
- abstract structure;
- figures/tables;
- declarations;
- reporting checklist;
- data/code statements;
- ethics wording;
- supplementary files.

Use official publisher/journal sources.

Do not change science to fit the journal.

If no target journal has been chosen:
record this as a remaining author decision, not a scientific blocker.

---

## COMPLETION

Update CODEX.md only with durable final state.

Prepend exactly one HANDOFF.md entry containing:
- final status;
- blocker count;
- remaining human actions;
- tests/verifiers;
- final PDF path;
- exact HEAD;
- whether release/tag/publication actions remain.

Do not stage/commit/push/tag/publish/release.

STOP FOR USER REVIEW.
Recommended execution sequence
Run them exactly as:

53 → 54 → 55 → 56 → 57 → 58 → human actions → 59 → 60.

The important human interruption is between 58 and 59. At that point, you should obtain the actual ethics determination, decide the checkpoint-release policy, and create the final public release identifiers when you're ready. Batch 59 should receive those facts, not be asked to infer them.

One other important point: I would not add batches for more detector families, more seeds, full-RSNA retraining, or another external dataset at this stage. Your own V7 plan explicitly defined the objective as focusing the existing benchmark rather than expanding it into a larger detector comparison, and froze VinDr as the one major new external experiment.

BATCHES_V7_Q2_VINDR.md
MD
Those bigger changes remain possible later if peer review specifically demands them, but I would not voluntarily destabilise this paper now.