Yes — here is the full **`BATCHES_V5_RESEARCH_REPAIR.md`** content directly in chat so you can copy it into your repository.

# BATCHES_V5_RESEARCH_REPAIR.md — Independent Audit Remediation, Statistical Clarification, and Manuscript Hardening

For `Alpha-lacrim/medical-object-detector-benchmark`.

This sequence is intentionally conservative. It is designed to repair research-validity and reporting issues identified after the V4 paper-drafting pass **without silently changing the frozen experimental protocol, hiding adverse runs, tuning on the test set, or rewriting historical artifacts as if they never existed**.

## Global rules for every batch

Before doing anything in each batch:

1. Read `AGENTS.md`, `CODEX.md`, and `HANDOFF.md` completely if present. Follow repository-local instructions over assumptions in this prompt.
2. Read `docs/DECISION_LOG.md`, `docs/LIMITATIONS.md`, `docs/HYPOTHESES.md`, and the current `report/paper_draft.md`.
3. Record the current Git commit, branch, working-tree status, and any uncommitted files relevant to the batch.
4. Treat committed numerical artifacts as evidence to be checked, not prose to be defended. Never change a result merely to make the manuscript internally consistent.
5. Do not tune any threshold, calibration mapping, model, preprocessing parameter, or hypothesis on the held-out test set.
6. Preserve superseded analyses as historical/provenance artifacts. If an analysis is corrected, write a new versioned output or clearly mark the old artifact as superseded; do not silently overwrite history.
7. Keep YOLO11s seed 271 unless a metric is mathematically undefined for that run. Never replace it after observing its behavior. If a metric is undefined, report `NA` with the reason; do not impute zero unless zero is the metric's actual defined value.
8. Do not add clinical/deployment language that the data cannot support. This is an internal retrospective controlled comparison on a hardware-scoped subset from one source.
9. Any new script must have tests for the scientific logic it introduces. Any new result table must include enough metadata/provenance to reproduce it from the frozen inputs.
10. Update `CODEX.md` and `HANDOFF.md` after every completed batch. Update `docs/DECISION_LOG.md` whenever the batch changes an inferential target, analysis interpretation, or canonical-document status.
11. Stop at the end of each batch for review. Do not continue automatically into the next batch.
12. If the current repository contradicts any premise below, **do not force the requested conclusion**. Document the contradiction, show the evidence, and stop for review.

The intended order is Batches 27–38. Batches 28–34 address validity/reporting concerns first; Batches 35–36 strengthen consistency/reproducibility; Batch 37 rewrites the manuscript only after the evidence is settled; Batch 38 is the final adversarial gate.

---

## BATCH 27 — Re-audit the Current Repository and Adjudicate the External Review

```text
Read AGENTS.md, CODEX.md, HANDOFF.md, docs/DECISION_LOG.md, docs/LIMITATIONS.md,
docs/HYPOTHESES.md, report/paper_draft.md, and report/report.md first.

This is an audit-only batch. Do not modify scientific results or manuscript claims yet.

PURPOSE
The previous external review identified several real-looking problems, but it must not be treated as
ground truth. Reproduce the audit from the repository itself and explicitly adjudicate every issue
before we change anything.

1. Record:
   - current branch and HEAD commit;
   - whether the working tree is clean;
   - current CI workflow files and latest locally verifiable test status;
   - which repo-local files are canonical according to current documentation.

2. Create `docs/REVIEW_REMEDIATION_AUDIT.md` with one row per issue below:
   - CONFIRMED;
   - PARTLY CONFIRMED / OVERSTATED;
   - NOT CONFIRMED;
   - CANNOT VERIFY.
   For each row cite exact repository file(s), line/section names, source table(s), and code path(s).

3. Re-audit all findings from the previous review:
   a. primary CI and permutation p-values target different sources of randomness;
   b. fixed-threshold precision has a seed-aware CI crossing zero while a checkpoint-conditional
      Holm-adjusted permutation p-value is small;
   c. existing DCA uses raw detector confidence as the numerical threshold probability;
   d. REPORTING_CHECKLIST.md was generated against an older manuscript state;
   e. README/canonical-document hierarchy is ambiguous or stale;
   f. D-ECE support may be sparse;
   g. exact trained checkpoints are not committed/released;
   h. CI is software QA rather than end-to-end scientific regeneration;
   i. external validity, subgroup/fairness, and prospective validation are absent;
   j. PR/FROC/Pareto/threshold analyses use different seed counts from the five-seed clean analysis.

4. Add the following issues that the previous review did not adequately test:
   a. THRESHOLD CALIBRATION: verify whether `beta = sqrt(C_FN/C_FP)` is being presented as an
      actual false-negative:false-positive clinical cost ratio. F_beta weights recall relative to
      precision; that mapping is not automatically a calibrated clinical cost function.
   b. XAI SANITY: verify whether the so-called "data-randomization" test merely shuffled input
      pixels at inference. If yes, it is not the Adebayo et al. training-label data-randomization
      sanity test.
   c. SEED RESAMPLING: determine whether same-number seeds across Faster R-CNN and YOLO11s are
      genuine matched stochastic blocks or simply labels for independent training runs. Do not
      assume a paired seed bootstrap is valid just because the integers match.
   d. ACQUISITION SHIFTS: inspect the DICOM tags and preprocessing path to determine whether
      Poisson noise was applied to values that can legitimately be treated as proportional to
      X-ray beam intensity. If not, "dose reduction" must be a synthetic proxy, not a physical
      simulation claim.
   e. CALIBRATION EXPECTATION BIAS: inspect the calibration implementation and documentation for
      any logic or narrative that presupposed seed 271 "should" be a severe calibration outlier.
      Verify the result was computed generically for all seeds with no seed-specific code path.
   f. HYPOTHESIS COVERAGE: map every H1–Hn entry to a specific manuscript section and artifact.
   g. CITATION COVERAGE: identify every citation used for a methodological or standards claim and
      note whether its claimed support has actually been verified.

5. Re-check at least 12 numerical manuscript claims across distinct sections against committed
   tables, including:
   - dataset size/patient count;
   - five-seed clean AP;
   - fixed-threshold recall/precision/F1;
   - seed-271 maximum score and AP;
   - selected thresholds;
   - FROC;
   - D-ECE;
   - a primary CI and adjusted p-value;
   - common-corruption retention;
   - an acquisition-shift DSI;
   - Grad-CAM localization;
   - XAI sanity statistic.
   Do not rely on prose summaries if the underlying table is available.

6. End `docs/REVIEW_REMEDIATION_AUDIT.md` with:
   - BLOCKING BEFORE SUBMISSION;
   - SHOULD FIX;
   - OPTIONAL STRENGTHENING;
   - CLAIMS THAT SURVIVE UNCHANGED.

No scientific code changes in this batch.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 28 — Define the Inferential Target and Audit the Training-Seed Bootstrap

```text
Read the files required by the global rules, then read every primary-statistics implementation,
test, table, and provenance file before editing.

PURPOSE
The manuscript currently risks treating two different inferential targets as one generic statement
of "statistical significance." Fix the estimand/reporting problem first, and verify whether the
training-seed resampling scheme itself is justified.

1. Add a DECISION_LOG entry defining two distinct estimands:

   A. CHECKPOINT-CONDITIONAL ESTIMAND
      - conditions on the already-trained checkpoints;
      - uncertainty is from held-out patient sampling;
      - patient-cluster permutation p-values belong here.

   B. TRAINING-PROCEDURE ESTIMAND
      - includes held-out patient uncertainty AND stochastic retraining/run variability;
      - seed/run-aware bootstrap intervals belong here.

   Make one of these explicitly PRIMARY for the paper. Default to the training-procedure estimand
   for broad "pipeline" claims unless repository evidence gives a stronger reason otherwise.
   The checkpoint-conditional permutation analysis should then be labeled a secondary sensitivity
   analysis, not a second interchangeable proof of the same population claim.

2. Audit the seed dimension of the current bootstrap.
   Answer explicitly:
   - Are seed 17 for Faster R-CNN and seed 17 for YOLO11s a scientifically meaningful matched
     stochastic block?
   - Are the data-ordering, augmentation RNG, initialization RNG, and training frameworks coupled
     in a way that creates a common-random-number design?
   - Or are the two detectors' five trained runs effectively independent realizations that only
     happen to share seed labels?

3. If paired seed resampling is NOT justified:
   - implement a training-procedure bootstrap that resamples patient clusters and resamples trained
     runs independently within each detector;
   - recompute the nonlinear metrics from the resampled predictions, rather than bootstrapping only
     precomputed summary means;
   - keep the same frozen prediction bundles and test set;
   - do not retrain;
   - preserve the old paired-seed result as a clearly labeled historical/sensitivity artifact.

4. If paired seed resampling IS justified:
   - document the exact coupling mechanism;
   - add a sensitivity analysis using independent detector-run resampling anyway;
   - report whether pairing materially changes each CI.

5. For every endpoint, report:
   - point estimate;
   - 95% training-procedure bootstrap CI;
   - number of detector runs contributing;
   - number of patient clusters;
   - whether the endpoint is unconditional or conditional on a matched detection;
   - whether seed 271 contributes and how;
   - the checkpoint-conditional Holm-adjusted permutation p-value in a separate column explicitly
     labeled "conditional on observed checkpoints."

6. Add seed-influence diagnostics:
   - per-seed detector metrics;
   - leave-one-training-run-out summary for each detector;
   - a leave-one-seed-label-out comparison only as a descriptive influence check;
   - explicitly show the effect of seed 271 without presenting its exclusion as a corrected result.

7. Do NOT invent a new "seed-aware p-value" just to make the CI and p-value agree.
   If you implement a new hierarchical hypothesis test, it must have a defensible null, resampling
   scheme, and reference, and must be clearly secondary until reviewed.

8. Manuscript correction:
   - remove generic wording such as "five of seven endpoints were significant" unless every number
     in that sentence refers to one named inferential target;
   - for fixed-threshold precision, state separately what the checkpoint-conditional permutation
     test says and what the training-procedure CI says;
   - do not describe a CI crossing zero as robust evidence of a training-procedure difference;
   - preserve the strong positive seed-aware conclusions for endpoints whose intervals remain
     wholly above zero.

9. Add unit/regression tests that catch:
   - accidental image-level rather than patient-cluster resampling;
   - accidental exclusion of seed 271;
   - accidental pairing of seeds when independent resampling is configured;
   - duplicated patient IDs causing AP/IoU matching collisions in bootstrap replicates.

10. Write/update `docs/STATISTICAL_ANALYSIS.md` with a dedicated "Inferential targets" subsection
    and a plain-language explanation of why CI and p-value can differ without either arithmetic
    result being wrong.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 29 — Correct the “Cost-Weighted” F-beta Threshold Analysis

```text
Read the global-rule files, then inspect:
- src/stats/threshold_calibration.py
- docs/THRESHOLD_CALIBRATION.md
- docs/THRESHOLD_ANALYSIS.md
- the D-004 decision-log entry
- all threshold-calibration tables/figures
- every manuscript sentence that uses "cost", "clinical cost", "false-negative cost",
  "false-positive cost", "cost ratio", or beta.

PURPOSE
F_beta is a recall-vs-precision weighting metric. The identity
    beta = sqrt(C_FN / C_FP)
does NOT, by itself, make F_beta optimization equivalent to minimizing a clinically measured
false-negative/false-positive loss. Repair the terminology and, only if justified, add a genuinely
cost-sensitive sensitivity analysis.

1. Re-derive the current objective from the implementation and document exactly what beta does.

2. Unless there is a repository citation and derivation that supports the current clinical-cost
   interpretation, rename the analysis everywhere from:
   - "cost-weighted threshold calibration"
   to something like:
   - "recall-weighted F_beta threshold sensitivity"
   or another technically accurate term.

3. Remove or rewrite statements that equate beta^2 directly with an empirical clinical harm ratio.
   The beta sweep may still be retained as a hypothetical preference/sensitivity analysis.

4. Keep threshold selection validation-only.
   No threshold may be selected or altered using test-set outcomes.

5. Preserve the existing beta sweep {1, 3, 5, 10} if it was frozen before test evaluation, but
   label these as preference weights, not measured clinical costs.

6. Add threshold-stability diagnostics on validation:
   - width of the near-optimal plateau;
   - bootstrap distribution of selected tau;
   - frequency with which each candidate threshold is selected.
   This is descriptive and should not tune the test result.

7. OPTIONAL SEPARATE ANALYSIS, only if scientifically useful:
   implement a true hypothetical misclassification-loss sweep:
       L(tau; r) = r * FN(tau)/N + FP(tau)/N
   for explicitly hypothetical FN:FP loss ratios r.
   If added:
   - do not call r a measured clinical cost;
   - select on validation only;
   - keep it separate from F_beta;
   - report the assumed ratios prominently;
   - do not imply deployment utility.

8. Update:
   - docs/DECISION_LOG.md;
   - docs/HYPOTHESES.md if the operational wording currently claims clinical cost;
   - docs/THRESHOLD_CALIBRATION.md;
   - docs/LIMITATIONS.md;
   - report/paper_draft.md;
   - figure/table titles and column names.

9. Add tests ensuring no test labels enter the selection path and no code silently converts beta
   into a clinical-cost assertion.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 30 — Remove or Rebuild Conventional Decision-Curve Analysis

```text
Read the global-rule files, then inspect the complete DCA implementation, tests, tables, figures,
provenance summaries, references, and every manuscript DCA sentence.

Scientific references to verify before editing:
- Vickers & Elkin, Medical Decision Making, 2006, decision-curve analysis;
- Vickers et al., BMC Medical Informatics and Decision Making, 2008, extensions to diagnostic
  tests/markers and conversion of a continuous marker to predicted probability.

PURPOSE
Conventional DCA uses a threshold probability p_t that represents a decision-maker's harm/benefit
trade-off. A raw detector confidence threshold is not automatically that probability. The existing
raw-score curves must not be presented as standard clinical net-benefit evidence.

MANDATORY STEP 1 — classify the current analysis
1. Verify whether the current code uses:
      max detector confidence >= tau
   to define action and simultaneously uses:
      tau/(1-tau)
   as the false-positive harm weight.
2. If yes, mark the existing analysis as NON-STANDARD for conventional DCA interpretation.

MANDATORY STEP 2 — preserve provenance
3. Do not delete the existing arithmetic or pretend it was never run.
   Keep it as a historical/exploratory artifact, but rename/relabel it as a raw-score threshold
   utility/sensitivity curve if retained anywhere.
4. Remove conventional clinical wording such as:
   - "net benefit from threshold probability X to Y";
   - "clinical utility";
   - "beneficial decision range";
   unless a valid probability-based DCA is produced below.

PREFERRED PAPER PATH
5. The safest default for this manuscript is:
   - remove raw-score DCA from the main Results;
   - mention in Supplementary/Limitations that an exploratory raw-score utility calculation was
     performed but is not interpretable as standard DCA because detector scores are not validated
     outcome probabilities.

OPTIONAL SALVAGE PATH — only if the required validation data exist
6. If frozen validation predictions and exam-level binary outcomes are available, implement an
   exam-level probability mapping using VALIDATION DATA ONLY:
   - define the exam-level marker exactly (e.g. maximum emitted detection score; score 0 when none);
   - fit a monotonic or logistic probability calibration mapping separately for each detector/run;
   - freeze the mapping before test evaluation;
   - apply it to the test set once;
   - define actions by calibrated predicted probability >= p_t;
   - compute conventional DCA using p_t as the same probability scale used in the harm weighting.

7. Do not choose the calibrator family or hyperparameters based on test DCA performance.
   Any choice among logistic/isotonic/etc. must be justified and frozen from validation behavior.

8. Explicitly address prevalence:
   - the test set is enriched/internal and is not a deployment prevalence sample;
   - any DCA is therefore internal to this study population;
   - do not translate it into external clinical utility or deployment readiness.

9. If probability calibration is unstable, underpowered, or invalid for one or more runs, DO NOT
   force a DCA. Use the preferred removal/demotion path instead.

10. If valid DCA is retained:
    - use patient-cluster bootstrap CIs on test;
    - keep calibrators frozen within bootstrap replicates;
    - report the test population, patient clusters, positives, prevalence, and all assumptions;
    - compare detectors on calibrated probability thresholds, never the same raw confidence scale.

11. Update:
    - docs/DCA_ANALYSIS.md;
    - docs/LIMITATIONS.md;
    - docs/HYPOTHESES.md if applicable;
    - report/paper_draft.md;
    - references.bib;
    - table/figure captions and provenance metadata.

12. Add tests that fail if raw detector confidence is accidentally passed directly as p_t in the
    standard-DCA code path.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 31 — Correct the XAI “Sanity Check” Terminology and Method

```text
Read the global-rule files, then inspect:
- src/explainability/sanity_checks.py
- docs/XAI_SANITY.md
- docs/EXPLAINABILITY.md
- Grad-CAM tables/figures
- the manuscript XAI section
- the exact Adebayo et al. reference in references.bib.

Reference to verify:
Adebayo et al., "Sanity Checks for Saliency Maps", NeurIPS 2018.

PURPOSE
The canonical Adebayo data-randomization test randomizes the relationship between training inputs
and labels and retrains a model. Shuffling test-image pixels is an input perturbation, not that test.
Also, a single full-weight reinitialization is not the same as the canonical cascading randomization
analysis. Correct the claims without discarding useful historical controls.

1. Determine exactly what the current implementation does.

2. If "data randomization" currently shuffles input pixel matrices at inference:
   - rename it everywhere to "input-pixel randomization control" or similarly accurate terminology;
   - explicitly state that it is NOT the Adebayo training-label data-randomization test;
   - do not claim that it establishes sensitivity to the learned data-label relationship.

3. Reclassify the existing all-weights reinitialization as:
   - a full model-parameter randomization control.
   Do not call it a full reproduction of Adebayo cascading randomization unless it actually is.

4. Add a proper cascading model-parameter randomization test if feasible without retraining:
   - randomize detector head/output layers first, then progressively deeper blocks/backbone groups;
   - define detector-specific layer groups transparently for Faster R-CNN and YOLO11s;
   - use the same frozen 50-image subset;
   - never mutate the original checkpoints on disk.

5. Improve similarity metrics.
   Do not rely on one Pearson correlation alone.
   At minimum report:
   - Spearman/rank correlation on normalized maps;
   - SSIM or another spatial structural similarity metric;
   - the existing correlation for continuity if desired.
   Explain metric preprocessing and degenerate-map handling.

6. Do NOT add the canonical Adebayo data-randomization test unless we explicitly accept new
   retraining. For object detection it would require training an identical architecture on randomized
   training annotations/label relationships and demonstrating that the randomized task was actually
   fit. If that experiment is not run, state "not performed."

7. Reinterpret the results conservatively:
   - low similarity after parameter randomization supports parameter sensitivity of the explanation;
   - it does NOT prove anatomical correctness, causal faithfulness, or clinical reasoning;
   - input-pixel randomization is a perturbation stress control, not evidence of data-label
     dependence.

8. Audit the existing localization values (energy-in-box, pointing game, box-area reference).
   Keep them descriptive unless a valid inferential analysis exists.
   Do not describe small absolute overlaps as strong localization merely because they exceed a
   box-area baseline slightly.

9. Produce versioned outputs, e.g.:
   - results/tables/gradcam_sanity_v2_summary.csv
   - results/figures/gradcam_sanity_v2_panel.png
   and retain the old table as historical.

10. Update docs/XAI_SANITY.md, docs/EXPLAINABILITY.md, docs/LIMITATIONS.md,
    report/paper_draft.md, references.bib, and provenance hashes.

11. Add tests for:
    - checkpoint immutability;
    - deterministic layer-group randomization under a fixed audit RNG;
    - correlation/SSIM handling;
    - correct labeling of input-randomization versus training-data randomization.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 32 — Re-audit the “Radiography-Physics-Aware” Acquisition-Shift Claims

```text
Read the global-rule files, then inspect the raw-DICOM audit path, preprocessing code,
src/robustness/radiography_shifts.py, docs/ACQUISITION_SHIFTS.md, results, and manuscript wording.

Use the current DICOM standard as the primary technical reference, especially:
- Photometric Interpretation;
- Pixel Intensity Relationship / Sign;
- Modality LUT / Rescale;
- VOI LUT and Window Center/Width;
- whether pixels are approximately linear, logarithmic, display-ready, or otherwise processed.

PURPOSE
The current transformations may be useful stress tests, but "dose simulation" or
"acquisition-physics-aware" language is too strong unless the stored pixel values support the
required physical interpretation.

1. Build a DICOM metadata audit table for every image in the acquisition-shift subset, including:
   - SOP Class / modality;
   - Photometric Interpretation;
   - Pixel Intensity Relationship and Sign, if present;
   - Rescale Slope/Intercept/Type;
   - VOI LUT / Window Center/Width / VOI function;
   - Presentation Intent Type or processing-related fields if present;
   - missingness of each field.

2. Confirm the existing MONOCHROME handling and DICOM LINEAR window implementation against the
   standard. Add regression tests using known numeric examples from the standard.

3. Reclassify each synthetic shift:
   A. DICOM display-transform sensitivity;
   B. generic intensity perturbation;
   C. physics-motivated proxy;
   D. physically unsupported for these stored values.
   Do not use one umbrella label if the transformations have different levels of physical validity.

4. Poisson/dose claim:
   - only call a transform a dose/quantum-noise proxy if the pixel representation used for noise
     is demonstrably approximately proportional to the relevant X-ray signal, or is validly mapped
     back to such a scale;
   - if Pixel Intensity Relationship is LOG/DISP/OTHER/missing and cannot be inverted reliably,
     rename the experiment to signal-dependent Poisson-like noise sensitivity;
   - explicitly state that it is NOT a validated low-dose acquisition simulation.

5. Gaussian blur:
   - call it blur/spatial-resolution sensitivity unless a scanner/reconstruction-specific model is
     justified;
   - do not imply a particular detector or reconstruction process without evidence.

6. Quantify the effect of the canonical per-image min-max preprocessing:
   - compute image-space perturbation magnitude before and after min-max scaling;
   - identify transforms that are partly or almost completely cancelled by normalization;
   - include this diagnostic in the table or supplement.

7. Keep DSI as a descriptive performance-retention/domain-sensitivity index.
   Do not imply that DSI estimates real inter-site transportability.

8. If the current names are too strong, update titles/captions/manuscript to something like:
   "radiography-motivated synthetic acquisition/display sensitivity"
   rather than "clinical acquisition robustness."

9. Do not rerun GPU inference unless the audit shows the implementation itself was scientifically
   wrong or the transformation must be corrected. If rerunning is required, preserve old outputs as
   superseded and hash all new inputs/outputs.

10. Update docs/ACQUISITION_SHIFTS.md, docs/LIMITATIONS.md, report/paper_draft.md, provenance,
    and tests.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 33 — Harden Detection Calibration Reporting and Sensitivity

```text
Read the global-rule files, then inspect the full calibration implementation, D-ECE tables,
reliability diagrams, score-floor handling, matching rules, and manuscript claims.

Reference to verify:
Küppers et al., "Multivariate Confidence Calibration for Object Detection", CVPR Workshops 2020.

PURPOSE
D-ECE is detection-specific and useful here, but a high-dimensional histogram can be sparse and
the metric evaluates emitted detections rather than missed targets or exam-level risk.

1. Verify the implementation against the cited D-ECE definition:
   - confidence;
   - class;
   - box position/scale dimensions actually used;
   - TP/FP matching rule and IoU threshold;
   - binning;
   - weighting;
   - minimum-cell rule;
   - confidence floor.

2. Confirm there is no seed-271 special case in code.
   The same pipeline must process every detector/run.
   If prose previously said seed 271 "should" be an outlier before the analysis, remove that
   expectation from method wording and report only what the result actually shows.

3. Add support/occupancy diagnostics per detector/run:
   - total detections entering calibration;
   - total possible multidimensional cells;
   - occupied cells;
   - cells meeting minimum support;
   - fraction of detections contributing to supported cells;
   - median/min/max supported-cell size.

4. Add a predeclared descriptive sensitivity grid over reasonable bin counts and/or minimum-cell
   thresholds.
   The purpose is robustness of the D-ECE estimate, not selecting the setting that favors a model.
   Keep the original setting clearly identified.

5. Add confidence-floor sensitivity if the 0.001 floor materially determines the population.
   Do not remove seed 271 or low-confidence detections merely to stabilize the metric.

6. Label reliability diagrams accurately:
   - if they are confidence-only marginal plots, say so;
   - do not present a 1-D reliability diagram as a visualization of all five D-ECE dimensions.

7. Manuscript wording:
   - call D-ECE comparison descriptive unless a defensible patient/run-level inferential analysis
     is added;
   - do not infer clinical-risk calibration from detection confidence calibration;
   - explicitly note that missed ground-truth objects have no emitted confidence and are outside
     D-ECE's emitted-detection calibration population.

8. Keep the exam-level probability calibration used for any valid DCA, if created in Batch 30,
   conceptually and programmatically separate from detection-level D-ECE.

9. Output versioned calibration-support tables/figures and update provenance.

10. Add tests for binning edge cases, empty/sparse cells, score-floor behavior, and absence of
    seed-specific branches.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 34 — Rebuild Reporting Standards, Hypothesis Traceability, and Citation Verification

```text
Read all global-rule files and the current manuscript after Batches 28–33.

PURPOSE
The old reporting checklist was created before the paper draft and is stale. The earlier external
review also did not provide the requested complete hypothesis and methodological-citation audit.

1. Make the canonical document hierarchy explicit in README.md:
   - report/paper_draft.md = current manuscript;
   - report/report.md = historical/full technical report;
   - docs/ = analysis/methodology/audit record;
   - results/ = numerical source of truth.
   Preserve report/report.md; do not rewrite it as if it were the current paper.

2. Regenerate `docs/REPORTING_CHECKLIST.md` AGAINST THE CURRENT paper_draft.md, not report.md.

3. CLAIM:
   - use CLAIM 2024 as the primary medical-imaging AI checklist;
   - use the official Yes / No / Not Applicable structure;
   - for Yes, cite manuscript section/line or exact repo artifact;
   - for No/NA, explain why;
   - use "internal testing" and "external testing" terminology where appropriate;
   - do not claim official compliance merely because an internal crosswalk exists.

4. STARD-AI:
   - use the final 2025 STARD-AI guideline, not an old protocol/pre-publication placeholder;
   - assess whether the study is sufficiently diagnostic-accuracy-centered for the checklist to be
     applicable;
   - if used, label it a reporting crosswalk unless the official submission checklist is completed.

5. TRIPOD+AI:
   - assess applicability carefully;
   - this is not primarily an individualized clinical prediction-model study;
   - use by analogy only where informative unless the manuscript truly falls within scope.

6. Create `docs/HYPOTHESIS_TRACEABILITY.md`:
   for every H1–Hn include:
   - exact hypothesis wording;
   - retrospective/preregistered status;
   - operational endpoint;
   - dataset/split;
   - seed count;
   - source artifact;
   - manuscript section;
   - result status;
   - whether multiplicity control applies;
   - limitations.
   Do not retroactively relabel retrospective hypotheses as preregistered.

7. Create `docs/CITATION_AUDIT.md`.
   For EVERY reference used to support a methodological, standards, dataset, DICOM, statistical,
   calibration, DCA, or XAI claim:
   - citation key;
   - full title/authors/year;
   - DOI/PMID/arXiv or authoritative standard section where available;
   - whether the source exists;
   - exact manuscript claim it supports;
   - VERIFIED / PARTIAL / UNSUPPORTED / WRONG ATTRIBUTION.
   Correct references.bib and manuscript claims for any failed rows.
   Background citations may be sampled only if clearly labeled background; methodological claims
   are not sampled.

8. Submission declarations:
   create a section or `docs/AUTHOR_DECLARATIONS_TODO.md` listing:
   - funding;
   - competing interests;
   - ethics/data-use determination;
   - consent applicability;
   - author contributions;
   - data/code availability;
   - patient/public involvement if applicable.
   NEVER invent these facts. Use explicit `AUTHOR ACTION REQUIRED` placeholders where only the
   human author can answer.

9. Add a sample-size/subset-selection reporting row:
   explain the 5,000-study hardware-scoped subset, how it was selected, whether a formal sample-size
   calculation existed, and what that means for generalizability.

10. Update docs/LIMITATIONS.md to ensure all newly clarified limitations from Batches 28–33 are
    represented.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 35 — Five-Seed Sensitivity for PR/FROC/Pareto and Operating-Regime Claims

```text
Read global-rule files and the current decision log.

No retraining. Use only frozen prediction bundles already present.

PURPOSE
The clean comparison uses five attempted runs, while several operating-regime analyses were frozen
earlier at n=3. The paper can keep that history, but the central score-scale/threshold conclusion
should have a five-run sensitivity analysis if the required predictions already exist.

1. Inventory which analyses can be recomputed from all five frozen prediction bundles without:
   - retraining;
   - changing validation-selected thresholds;
   - test-set tuning.

2. For each of PR, FROC, Pareto, and fixed validation-selected-threshold performance:
   - retain the original n=3 artifact as historical/pre-specified;
   - create a new n=5 sensitivity artifact;
   - include seed 271 exactly as observed;
   - do not reselect the old threshold using test data or the new test results.

3. For FROC/PR:
   - compute per-run curves where appropriate;
   - report aggregate summaries with explicit run count;
   - show how seed 271 changes score-scale behavior and threshold-free ranking.

4. For Pareto:
   - define exactly what is being aggregated;
   - do not mix n=3 and n=5 metrics in one frontier without visible labels;
   - if hardware metrics exist only for certain runs, keep sample-size labels explicit.

5. Compare n=3 versus n=5 conclusions in a dedicated table:
   - unchanged;
   - strengthened;
   - weakened;
   - reversed.
   Report all changes, not only favorable ones.

6. Decide via DECISION_LOG whether the manuscript's principal operating-regime figure remains the
   originally frozen n=3 analysis with n=5 sensitivity, or is replaced by n=5 with the original
   retained as provenance. Justify the choice based on design/provenance, not aesthetics.

7. Update docs/THRESHOLD_ANALYSIS.md, docs/FROC_ANALYSIS.md, docs/PARETO_ANALYSIS.md,
   docs/LIMITATIONS.md, manuscript captions/text, and provenance.

8. Add regression tests ensuring all five runs are included in the n=5 path and seed 271 is not
   automatically filtered for having no detections at 0.25.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 36 — Strengthen Reproducibility Without Pretending CI Retrains the Study

```text
Read global-rule files, README.md, docs/REPRODUCIBILITY.md, CI workflows, artifact manifests,
checkpoint references, and all current provenance summaries.

PURPOSE
Current CI is useful software QA but does not retrain ten models or regenerate all scientific
evidence. Strengthen artifact-level verification and make the exact reproducibility boundary
machine-checkable.

1. Add a machine-readable scientific artifact manifest, e.g.
   `results/scientific_artifact_manifest.json`, containing for each manuscript-critical artifact:
   - path;
   - SHA256;
   - generating script;
   - config path/hash;
   - input artifact hashes;
   - expected schema;
   - study phase;
   - whether GPU/training is required to regenerate it.

2. Add `scripts/verify_scientific_artifacts.py` that:
   - verifies hashes;
   - validates CSV schemas and required columns;
   - verifies referenced result files exist;
   - fails on stale/missing manuscript-critical artifacts.

3. Add a claim-to-source manifest, e.g.
   `report/paper_claim_sources.yaml`, for key numerical claims.
   Each entry should point to an exact table/row/column or deterministic calculation.
   Add `scripts/verify_paper_claims.py` to check these values against the manuscript within the
   stated rounding tolerance.

4. Integrate the lightweight artifact and claim checks into CI.
   Do NOT add model training or large dataset downloads to standard CI.

5. README/REPRODUCIBILITY wording must distinguish:
   - software tests pass;
   - committed-analysis reproduction from frozen predictions;
   - exact inference reproduction;
   - exact retraining reproducibility.
   Never say green CI proves all published scientific results regenerate.

6. Checkpoint release audit:
   - determine whether exact trained checkpoint files still exist locally;
   - determine license/data-policy feasibility for public release;
   - if feasible, create a release manifest/instructions and hashes, but DO NOT commit huge binaries
     automatically;
   - if not available or not releasable, document the limitation precisely.
   Never fabricate a download link.

7. Verify lockfiles, environment versions, GPU/CUDA notes, RNG settings, and known nondeterministic
   operations are accurately documented.

8. Add tests for the new verifier scripts.

When done: update README.md, docs/REPRODUCIBILITY.md, CODEX.md, and HANDOFF.md. Stop for review.
```

---

## BATCH 37 — Rewrite the Manuscript Around Only the Claims That Survive

```text
Read all outputs and decisions from Batches 27–36 before editing.

Do NOT edit report/report.md except for an optional one-line historical-status notice if the decision
log explicitly calls for it. report/paper_draft.md is the current manuscript.

PURPOSE
Now that the statistical, DCA, threshold, XAI, calibration, acquisition-shift, and reporting issues
have been adjudicated, rewrite the paper so every claim matches the corrected evidence.

1. TITLE
   Keep the scope as a controlled comparative study of two disclosed detector pipelines.
   Do not imply a universal one-stage-vs-two-stage benchmark law.
   Prefer "lung opacity" over "pneumonia diagnosis" where target semantics matter.

2. ABSTRACT
   - identify retrospective/internal-testing design;
   - state dataset size and patient-disjoint split;
   - lead with controlled evaluation and operating-score/threshold behavior, not a universal winner;
   - use the PRIMARY inferential target from Batch 28;
   - do not call precision significant under training-procedure uncertainty if its CI includes zero;
   - remove conventional DCA claims unless Batch 30 produced a valid probability-based DCA;
   - no clinical deployment claim.

3. METHODS
   Add compact but explicit subsections for:
   - canonical preprocessing;
   - two disclosed training recipes and their asymmetry;
   - seed/run design;
   - primary inferential estimand and checkpoint-conditional sensitivity;
   - validation-only threshold selection;
   - F_beta preference-weight sensitivity with corrected terminology;
   - detection-level calibration and its support limitations;
   - DCA only if valid after Batch 30;
   - digital corruptions versus radiography-motivated synthetic shifts;
   - XAI controls with corrected Adebayo terminology;
   - retrospective hypothesis status.

4. RESULTS
   - every number must come from a committed result artifact or claim manifest;
   - visibly label n=3/n=5/single-checkpoint analyses;
   - preserve seed 271;
   - separate statistical inference from descriptive secondary analyses;
   - report absolute performance as well as between-detector differences;
   - if five-seed sensitivity changes an older finding, report the change.

5. DISCUSSION
   Protect the defensible contribution:
   - nominally identical raw confidence thresholds can correspond to very different operating
     regimes across these two disclosed pipelines;
   - AP, raw score scale, fixed-threshold behavior, and calibration are different objects;
   - seed 271 is evidence of score-scale instability, not a run to hide.
   Do not generalize to all Faster R-CNN, all YOLO, all one-stage/two-stage detectors, or clinical
   populations.

6. LIMITATIONS
   Include, at minimum:
   - one historical source / no external testing;
   - hardware-scoped 5,000-study subset;
   - two model pipelines only;
   - five training attempts provide coarse run-level uncertainty;
   - secondary analyses with smaller run/sample scopes;
   - enriched/internal prevalence;
   - no subgroup/fairness analysis;
   - no prospective evaluation;
   - detection calibration is not exam-level clinical risk calibration;
   - DCA limitation/removal;
   - XAI sanity scope;
   - synthetic acquisition-shift limits;
   - exact checkpoint availability/retraining nondeterminism;
   - retrospective hypotheses.

7. REPORTING LANGUAGE
   - use "internal testing" rather than ambiguous "validation" when referring to held-out test data;
   - reserve "validation set" for the model-development split used for threshold/calibration fitting;
   - avoid "clinically useful", "safe", "deployment-ready", "diagnostic" unless directly bounded.

8. REFERENCES
   Apply all corrections from CITATION_AUDIT.md.

9. DECLARATIONS
   Keep author-only items as explicit placeholders. Do not invent ethics, funding, conflicts,
   authorship, or consent statements.

10. After editing, run:
    - full test suite;
    - lint/format checks;
    - scientific artifact verifier;
    - paper claim verifier.

11. Regenerate docs/REPORTING_CHECKLIST.md once more against THIS final manuscript state, because
    any checklist generated before this rewrite is stale by definition.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 38 — Final Adversarial Submission Gate

```text
Read AGENTS.md, CODEX.md, HANDOFF.md and all current canonical documents.

This is the final audit. Do not assume earlier batches succeeded merely because they completed.

1. Record current HEAD, git status, test status, and CI configuration.

2. Re-run:
   - full pytest;
   - Ruff/format/lint;
   - package smoke test;
   - scientific artifact verifier;
   - manuscript claim verifier.

3. NUMERICAL TRACEABILITY
   Trace at least 15 manuscript numbers from abstract, methods, results, discussion, and limitations
   to exact committed source cells/calculations.
   Report every mismatch, including rounding errors beyond the declared tolerance.

4. STATISTICAL LANGUAGE
   Search the manuscript for:
   significant, significance, robust, superior, better, uncertainty, confidence interval, p-value,
   seed, checkpoint.
   Verify every use is consistent with the estimand definitions from Batch 28.

5. DCA / UTILITY LANGUAGE
   Search for:
   DCA, decision curve, net benefit, threshold probability, clinical utility.
   Confirm no raw detector score is represented as a clinical threshold probability.
   If standard DCA was removed, confirm no stale figure/table/citation still implies otherwise.

6. THRESHOLD LANGUAGE
   Search for:
   cost, cost-weighted, C_FN, C_FP, beta.
   Confirm F_beta preference weighting is not falsely presented as measured clinical cost.

7. XAI LANGUAGE
   Search for:
   data randomization, sanity, faithful, attention, reasoning, localization.
   Confirm input-pixel shuffling is not called Adebayo data randomization and that no sanity test is
   interpreted as proof of clinical faithfulness.

8. RADIOGRAPHY/DICOM LANGUAGE
   Search for:
   CT, HU, Hounsfield, dose, quantum, acquisition, windowing, VOI, Modality LUT, Rescale.
   Confirm all statements match planar radiography and the actual inspected DICOM metadata.

9. CALIBRATION LANGUAGE
   Search for:
   calibrated, calibration, D-ECE, reliability, probability.
   Confirm detection-level D-ECE is not described as exam-level clinical-risk calibration and that
   sparse-support diagnostics are disclosed.

10. SEED/SCOPE CONSISTENCY
    Build one table listing every major analysis and:
    - dataset/sample size;
    - patient clusters;
    - detector runs/seeds;
    - whether seed 271 is included;
    - whether inference is population-level, checkpoint-conditional, or descriptive.
    Compare this table to every manuscript caption/claim.

11. HYPOTHESES
    Verify every H1–Hn is represented accurately and retrospective hypotheses are never described
    as preregistered.

12. REFERENCES
    Re-run the full methodological citation audit and ensure every manuscript citation key resolves.

13. REPORTING CHECKLIST
    Confirm the CLAIM 2024 checklist points to the final manuscript, not the historical report.
    Confirm STARD-AI/TRIPOD+AI applicability is not overstated.

14. README / DOCUMENT HIERARCHY
    Confirm README names paper_draft.md as current manuscript and report.md as historical technical
    report, and reproduction commands match files that actually exist.

15. PHANTOM-ARTIFACT CHECK
    For every manuscript-mentioned table, figure, script, config, checkpoint reference, supplement,
    and documentation file, verify existence or explicitly label external/unavailable items.

16. Write `docs/FINAL_SUBMISSION_AUDIT.md` with:
    - BLOCKING FAILURES;
    - SHOULD-FIX;
    - VERIFIED CLEAN AREAS;
    - 15-number traceability table;
    - analysis-scope table;
    - exact commands/tests run and results;
    - final statement: READY FOR AUTHOR REVIEW or NOT READY FOR SUBMISSION.

17. Do not declare the project "submission ready" if any blocking item remains or any human-only
    declaration is unresolved. Use "ready for author review" where appropriate.

When done: update CODEX.md and HANDOFF.md with the final state and stop.
```

---

# Optional follow-up experiments — do not run automatically

These are not required to repair the manuscript's internal validity, but they would materially strengthen a later journal submission.

## OPTIONAL A — External testing

Design a genuinely external-site/data-source evaluation only after confirming annotation-target compatibility. Do not treat a dataset with a different clinical label definition as a direct drop-in validation set. Pre-specify mapping, inclusion criteria, threshold policy, and primary endpoints before seeing results.

## OPTIONAL B — Subgroup/fairness analysis

Only if reliable demographic/acquisition metadata exist. Pre-specify subgroups, minimum support, multiplicity policy, and whether the analysis is descriptive or inferential. Do not infer fairness from missing or low-quality metadata.

## OPTIONAL C — Broader detector coverage

If the paper is to claim general one-stage/two-stage behavior, two implementations are insufficient. Add detector families only under a new pre-specified protocol; do not retrofit architecture-family claims onto the current two-pipeline experiment.

## OPTIONAL D — Exact checkpoint release

If licenses and storage allow, release frozen checkpoint binaries with SHA256 hashes, environment metadata, and an inference reproduction command. This improves exact inference reproducibility but does not remove GPU nondeterminism from retraining.

---

# Priority if compute/time is limited

Run these first, in this order:

1. Batch 27 — current-state audit.
2. Batch 28 — inferential target + seed-resampling audit.
3. Batch 29 — F_beta/cost-language correction.
4. Batch 30 — DCA removal or proper probability-based rebuild.
5. Batch 31 — XAI sanity correction.
6. Batch 32 — acquisition-physics claim correction.
7. Batch 33 — calibration support/sensitivity.
8. Batch 34 — reporting/citations/hypotheses.
9. Batch 37 — manuscript rewrite.
10. Batch 38 — final gate.

Batches 35–36 are high-value strengthening passes but should not delay correction of the validity and interpretation issues above.

This is the **Codex batch file** I was referring to. I also created the separate `CHATGPT_RESPONSE_AUDIT_AND_PRIORITY.md`; I can paste that entire `.md` into the chat as well.