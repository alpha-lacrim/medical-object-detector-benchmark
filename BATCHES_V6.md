Yes. I’d use **three separate Codex sessions/batches**, with a review between each. That reduces the chance that Codex “improves” the experiment by changing frozen analyses you deliberately want to preserve.

I tailored these to the repository’s actual hierarchy: `report/paper_draft.md` is canonical, `results/` is the numerical source of truth, `report/report.md` is historical, and the repo already has claim/audit machinery.  The current manuscript still contains the three wording problems we identified—“threshold-free ranking,” “calibration was descriptively higher,” and the unqualified abstract “3-fold throughput”—while the detailed limitations already correctly document the FROC lower-bound and timing asymmetry. 

### Batch 1 — surgical manuscript fixes

This is the one I would run first. It should change **no results, no analysis, no experiment configuration**.

You are working in my local `medical-object-detector-benchmark` repository.

This task is a SURGICAL MANUSCRIPT/REPORTING CORRECTION. Do not expand the research project, do not add experiments, do not retrain models, do not rerun GPU inference, and do not change numerical results merely to make the narrative cleaner.

## 0. Read local project instructions before doing anything

Before editing:

1. Run `git status --short`.
2. Locate and read, in this order where applicable:
   - `AGENTS.md`
   - any nested `AGENTS.md` relevant to files you will edit
   - `CODEX.md`
   - `HANDOFF` or any clearly corresponding HANDOFF file/directory
3. These files may intentionally be UNTRACKED and absent from GitHub.
4. Treat them as local project instructions/context.
5. DO NOT add, stage, commit, rename, delete, or publish those untracked instruction/handoff files.
6. Do not copy private/local-only contents from those files into tracked repository files unless they explicitly instruct you to do so.
7. Follow their project conventions and precedence rules.

Do not commit or stage anything at the end. I want to review the diff myself.

## 1. Understand the repository's evidence hierarchy

Before changing prose, inspect:

- `README.md`, especially the canonical-document hierarchy
- `report/paper_draft.md`
- `report/paper_claim_sources.yaml`
- `docs/LIMITATIONS.md`
- `docs/REPORTING_CHECKLIST.md`
- relevant threshold/FROC/calibration/compute documentation under `docs/`
- relevant frozen numerical artifacts in `results/`

Important constraints:

- `report/paper_draft.md` is the current manuscript.
- `results/` is the numerical source of truth.
- `report/report.md` is historical/full technical documentation and must NOT be rewritten merely to mirror the current paper.
- Existing frozen/historical n=3 artifacts must not be silently converted into n=5 artifacts.
- Do not modify result files unless you discover an actual provenance/integrity mismatch. If you discover one, STOP and report it before changing scientific evidence.

## 2. Fix the following manuscript issues

Make the smallest defensible edits necessary.

### A. Replace "threshold-free" terminology

The manuscript currently contains wording equivalent to:

"threshold-free ranking still favored Faster R-CNN"

That wording is too absolute because AP is computed from the retained prediction population and the detector/evaluation pipeline has a low score floor/post-processing boundary.

Replace it with scientifically precise language conveying:

- COCO AP is not dependent on the chosen single deployment operating threshold such as 0.25, 0.69, or 0.05;
- but AP is still conditional on the retained predictions and evaluation/post-processing protocol;
- therefore avoid the terms "threshold-free" and "completely threshold-independent."

A concise wording such as the following is acceptable if it fits the surrounding prose:

"COCO AP ranking, which does not depend on the selected single deployment operating threshold, still favored Faster R-CNN."

If necessary, add a short qualifier elsewhere that the AP analysis is conditional on the retained prediction floor and common evaluation protocol.

Do NOT imply that AP is independent of all filtering or inference decisions.

Search the ENTIRE tracked repository for other uses of "threshold-free", "threshold independent", or equivalent claims and repair any scientifically equivalent overstatement in manuscript-facing documentation.

### B. Correct the D-ECE/calibration wording

The abstract currently describes calibration as "higher" for YOLO11s while reporting a larger D-ECE.

D-ECE is an error quantity, so larger D-ECE means larger calibration error, not "better/higher calibration."

Change the abstract wording to something unambiguous, for example:

"Detection-specific calibration error was descriptively higher for YOLO11s (mean D-ECE 0.0990 versus 0.0320)..."

or, if stylistically better:

"Faster R-CNN had descriptively lower detection-specific calibration error..."

Preserve:
- the descriptive/non-inferential status of this comparison;
- the exact numerical values;
- sparse-cell/protocol-sensitivity qualifications.

Audit the Discussion/Conclusion/README and other manuscript-facing text for any other wording that could confuse "higher D-ECE" with "better calibration."

Do not change the calibration implementation or results in this batch.

### C. Bound the FROC claim to the actually evaluated score sweep

The project evaluates the relevant threshold sweep over 0.01--0.99, and the manuscript already correctly notes that YOLO11s reaches the 0.01 lower sweep boundary and that the observed plateau is a grid boundary rather than a global asymptote.

The abstract/headline wording should be equally careful.

Where the abstract currently says Faster R-CNN had higher sensitivity at all five reported false-positive budgets, qualify it so a reviewer cannot interpret the claim as a statement about an unrestricted/global FROC frontier.

Use wording equivalent to:

"Within the evaluated 0.01--0.99 score sweep, Faster R-CNN had higher observed sensitivity at all five reported false-positive budgets."

or another concise scientifically equivalent version.

Also inspect:
- Results
- Discussion
- Conclusion
- README headline result
- figure captions
- supplementary index text
- any claim-binding/audit prose

Make sure none of them turns the bounded observation into a global asymptotic/dominance claim.

Preserve the existing statement that the YOLO plateau at the lower boundary is NOT a demonstrated global asymptote.

Do NOT extend the score grid in this batch.

### D. Qualify the throughput claim

The manuscript Methods/limitations already document an implementation asymmetry:

- Faster R-CNN resizing occurs inside the timed model forward;
- YOLO tensor resizing occurs before the timed forward-plus-NMS region.

Therefore the approximately threefold FPS result is a valid measurement of the documented implementations on the measured hardware, but must not read like an architecture-general end-to-end throughput law.

Revise the abstract wording currently equivalent to:

"YOLO11s delivered approximately 3-fold throughput"

to something equivalent to:

"Under the documented detector-specific profiling procedure on the measured laptop, YOLO11s achieved approximately threefold higher measured throughput..."

Keep it concise enough for an abstract.

Likewise inspect the Discussion and Conclusion for statements like:
- "three times faster"
- "3-fold throughput"
- "YOLO is faster"
- architecture-general efficiency claims

Where necessary, qualify them as:
- measured on the stated hardware/software stack;
- implementation-specific;
- not a universal architecture-family comparison.

Do NOT alter the existing FPS/latency numbers.

### E. Preserve the statistical claim boundaries

While editing, check that surrounding prose continues to make these distinctions correctly:

- five training runs per detector remain a coarse sample of training-seed variation;
- the primary bootstrap and checkpoint-conditional permutation analyses answer different questions;
- the fixed-threshold precision primary interval crosses zero;
- conditional IoU/Dice inference is not conclusive;
- retrospective hypotheses are not described as preregistered or confirmatory;
- exploratory test threshold sweeps are not described as validation-selected deployment rules;
- robustness and Grad-CAM analyses remain single-checkpoint/condition-specific where applicable.

Do not strengthen claims just because the point estimates favor one detector.

### F. Do not fabricate declarations

Inspect Section 8 and `docs/AUTHOR_DECLARATIONS_TODO.md`.

Do NOT invent:
- funding status;
- ethics approval/exemption;
- institution determinations;
- consent status;
- author contributions;
- conflicts;
- checkpoint release URLs;
- patient/public involvement.

If these remain unresolved, leave explicit author-action placeholders intact.

You may improve wording/consistency of the placeholders only if doing so does not infer any unknown fact.

## 3. Keep provenance machinery synchronized

After prose edits:

1. Inspect `report/paper_claim_sources.yaml`.
2. If edits invalidate textual anchors, claim IDs, line expectations, or manuscript claim-verification rules, update ONLY the necessary metadata.
3. Do not alter numerical source cells or tolerances unless there is a demonstrated existing error.
4. Inspect `docs/REPORTING_CHECKLIST.md` and `docs/LIMITATIONS.md`.
5. Update them only where necessary to keep the manuscript and audits consistent.
6. Prefer existing project mechanisms over introducing a new documentation system.

## 4. Validation

Run the project's normal lightweight verification commands according to local `AGENTS.md`/`CODEX.md`.

At minimum, where compatible with the repository:

- manuscript/scientific artifact verification scripts
- paper claim verification
- relevant unit tests
- `ruff` on files covered by the project
- `git diff --check`

Do NOT run:
- model training;
- checkpoint inference;
- GPU robustness generation;
- any expensive reproduction pipeline;
unless local project instructions explicitly show that a lightweight command is required and does not change scientific evidence.

## 5. Final response to me

When finished, report:

1. exact files changed;
2. each scientific wording issue fixed;
3. whether ANY numerical value changed — expected answer should be "no";
4. whether ANY frozen result artifact changed — expected answer should be "no";
5. tests/audits run and outcomes;
6. unresolved author-controlled declaration items;
7. any issue you found that might require actual scientific recomputation.

Do not stage or commit the changes.

I would inspect that diff manually before proceeding. In particular, there should be essentially no reason for Batch 1 to touch `src/`, `configs/`, or numerical `results/`.

### Batch 2 — audit the code underneath those claims

This one is intentionally more conservative: I want Codex to verify that the manuscript corrections actually describe what the implementation does. **If it finds a real scientific bug, it must stop instead of silently “fixing” and regenerating the paper.**

Work in my local `medical-object-detector-benchmark` repository.

This is an IMPLEMENTATION AUDIT AND REGRESSION-GUARD task. It follows a previous manuscript-only correction batch.

The purpose is to verify that the code, configs, frozen artifacts, and manuscript now tell the same scientific story.

Do NOT expand the experiment.
Do NOT retrain models.
Do NOT run new GPU inference.
Do NOT silently regenerate or overwrite frozen scientific artifacts.

## 0. Local instructions and git safety

First:

1. Run `git status --short`.
2. Read all applicable local instructions:
   - root/nested `AGENTS.md`
   - `CODEX.md`
   - `HANDOFF` or corresponding handoff material
3. These may be intentionally untracked.
4. Do not add/stage/commit/modify/delete those local instruction files.
5. Do not stage or commit any changes made by this task.

Review the current working diff from the prior batch so you understand what changed.

## 1. Audit four specific scientific interfaces

### A. COCO AP / prediction-floor semantics

Trace the complete path used for the headline COCO AP values:

- detector inference/export adapters
- frozen prediction bundles
- shared evaluator
- pycocotools invocation
- score floors
- per-image detection caps
- NMS/post-processing boundaries
- any explicit threshold filtering before COCO evaluation

Confirm precisely:

1. whether the prediction bundles retain detections at score >= 0.001;
2. whether headline COCO AP uses all retained predictions rather than the selected single operating thresholds;
3. whether any additional threshold/filter is applied before COCO AP;
4. whether the 100-detection cap or equivalent is used;
5. why wording such as "independent of the selected deployment operating threshold" is accurate;
6. why "threshold-free" would be too absolute.

Do not rely on manuscript prose alone. Trace code/config/artifacts.

If the implementation contradicts the manuscript, STOP and report the contradiction before changing scientific code or results.

### B. FROC lower-bound behavior

Trace:

- threshold sweep configs
- threshold sweep implementation
- n=3 archive path
- n=5 sensitivity path
- FROC construction code
- FROC operating-point extraction
- associated tests and documentation

Confirm precisely:

1. that the relevant exploratory score grid is 0.01--0.99;
2. whether it contains 99 common threshold values and exactly how those values are generated;
3. that frozen predictions may contain scores below 0.01;
4. how the best sensitivity at each FP/image budget is selected;
5. whether interpolation is used;
6. whether extrapolation below 0.01 is ever performed;
7. whether a boundary-hit flag/provenance field exists;
8. whether YOLO's reported plateau at larger FP budgets is correctly recognized as a lower-grid-boundary observation rather than a global asymptote.

Do NOT extend the threshold grid in this task.

If current code extrapolates beyond observed points, labels a boundary result as a global maximum, or otherwise contradicts the manuscript, STOP and report it as a potentially material scientific issue.

### C. Compute profiling boundary

Trace the actual profiling code for both detectors.

Confirm:

- CUDA synchronization behavior;
- warm-up count;
- timed-image count;
- batch size;
- AMP/mixed precision behavior;
- what preprocessing is inside/outside the timer;
- NMS/postprocessing inclusion;
- Faster R-CNN resize timing;
- YOLO resize timing;
- how FPS and latency are derived.

Verify that the manuscript statement describing Faster R-CNN resizing inside the timed model forward and YOLO tensor resizing before timed forward-plus-NMS is literally supported by code.

If not, stop and report the mismatch.

Do not redesign the benchmark or rerun timing in this task.

### D. D-ECE interpretation

Trace the D-ECE implementation and its configuration.

Confirm:

- lower D-ECE represents lower calibration error;
- dimensions/strata actually used;
- bin count;
- minimum supported-cell population;
- weighting denominator;
- treatment of unsupported cells;
- IoU correctness definition;
- score floor;
- handling of no-detection runs/settings;
- sensitivity-grid behavior.

Verify that the revised manuscript language says "higher calibration error" rather than implying that a numerically higher D-ECE means better calibration.

If there is a discrepancy between implementation and Methods equations/prose, stop and report it before changing results.

## 2. Add only lightweight regression safeguards where justified

After the audit, if all four implementations match the intended methods, inspect the existing project verification architecture.

Prefer strengthening EXISTING:
- tests;
- scientific artifact verifiers;
- manuscript claim verifiers;
- reporting checklist assertions;
- provenance checks.

Do not create a completely new framework if the repository already has mechanisms for this.

Useful safeguards, only if consistent with project conventions, may include tests/checks that prevent future regressions such as:

- manuscript reintroducing the literal phrase "threshold-free ranking";
- manuscript saying "calibration was higher" where D-ECE is being compared without the word "error";
- an unqualified claim that the measured FROC plateau is a global asymptote;
- an architecture-general throughput claim that contradicts the documented timer boundary;
- loss of the 0.01-grid-boundary caveat from the relevant reporting audit.

Avoid brittle tests tied to exact prose if a semantic/checklist mechanism already exists.

Do not change any numerical scientific result simply to satisfy a regression test.

## 3. Verify frozen scientific evidence

Inspect hashes/manifests and verify that this batch has NOT modified:

- prediction bundles;
- checkpoint manifests;
- generated metric CSVs;
- frozen n=3 archives;
- n=5 sensitivity result tables;
- figures derived from frozen scientific evidence;
- scientific artifact manifest contents,

unless an existing verification file itself legitimately needs a textual/reference update.

If any frozen artifact changes unexpectedly, stop.

## 4. Run lightweight verification

Use the commands specified by local project instructions.

Where applicable run:

- `python scripts/verify_scientific_artifacts.py` or the repository-equivalent invocation;
- `python scripts/verify_paper_claims.py` or equivalent;
- relevant targeted tests;
- full CPU test suite if reasonably lightweight;
- `ruff` for modified Python;
- `git diff --check`.

Do not train or infer.

## 5. Final report

Give me a structured report with:

### Confirmed implementation facts
- AP/prediction floor
- FROC/grid boundary
- profiling timer boundary
- D-ECE semantics

### Changes made
For every changed file, explain why.

### Scientific integrity
Explicitly state:
- whether numerical results changed;
- whether frozen artifacts changed;
- whether a potentially material implementation bug was found.

### Verification
List commands and pass/fail status.

### Remaining caveats
List only genuine unresolved caveats; do not suggest new experiments unless required to correct an actual error.

Do not stage or commit.

This is the batch most likely to catch something we missed. The repo already states that AP uses the unified evaluator, FROC is based on the bounded sweep, D-ECE uses detections retained at `>=0.001`, and the timing boundary differs between detectors.  The prompt forces Codex to prove those facts from implementation rather than trusting the paper.

### Batch 3 — final submission-readiness and overclaim audit

This one is less about “editing for style” and more about making sure the final paper presents exactly the study you actually performed.

Work in my local `medical-object-detector-benchmark` repository after the prior manuscript-correction and implementation-audit batches.

This is the FINAL SCIENTIFIC REPORTING / SUBMISSION-READINESS PASS.

My priorities are:

1. preserve the existing project scope;
2. do not add experiments;
3. do not retrain or rerun expensive analyses;
4. make the manuscript defensible under peer review;
5. avoid both overclaiming and unnecessary self-undermining;
6. keep the manuscript suitable for an international biomedical image-analysis / biomedical signal-processing journal such as Biomedical Signal Processing and Control or Journal of Imaging Informatics in Medicine;
7. do NOT reformat it into a specific publisher template yet.

## 0. Read project-local instructions first

Before editing:

- run `git status --short`;
- read applicable `AGENTS.md`;
- read `CODEX.md`;
- read `HANDOFF`/handoff material;
- inspect previous-batch diffs/history available in the working tree.

These local instruction files may intentionally be untracked.

Do not stage, commit, modify, delete, or publish them.

## 1. Read the complete evidence/reporting chain

At minimum inspect:

- `README.md`
- `report/paper_draft.md`
- `report/paper_claim_sources.yaml`
- `docs/LIMITATIONS.md`
- `docs/REPORTING_CHECKLIST.md`
- `docs/AUTHOR_DECLARATIONS_TODO.md`
- `docs/SUPPLEMENTARY.md` if present
- threshold/FROC/calibration/statistics/compute/robustness/XAI methodology docs relevant to manuscript claims
- frozen numerical sources referenced by major headline claims

Do not treat `report/report.md` as the current paper.

## 2. Perform a claim-by-claim overstatement audit

Search the manuscript and manuscript-facing tracked documentation for potentially dangerous wording, including variants of:

- prove / proven
- demonstrate / demonstrated
- establish / established
- superior
- robust / robustness
- generalize / generalization
- clinically
- diagnostic
- deployment
- threshold-free
- threshold-independent
- optimal
- asymptote
- dominates
- significant / significantly
- faster / 3-fold / threefold
- calibrated / better calibrated
- architecture
- one-stage versus two-stage
- all thresholds
- all operating points
- external validity

Do NOT mechanically remove these words.

For every occurrence, determine whether the evidence actually supports it.

Preserve strong wording where justified.
Narrow it where the study design does not justify the broader interpretation.

## 3. Enforce the actual study identity

The final manuscript should consistently describe this as:

- a controlled multi-axis characterization/benchmark of two disclosed detector pipelines;
- on a patient-disjoint internal RSNA benchmark;
- with five attempted training seeds per detector for the primary clean all-attempt comparison;
- using one common evaluator;
- including ranking, operating-point, calibration, compute, robustness, and XAI analyses;
- NOT a causal proof that the Faster R-CNN architecture is universally superior to YOLO;
- NOT a pneumonia diagnostic-validation study;
- NOT evidence of clinical utility;
- NOT an external/site/population validation;
- NOT a universal hardware benchmark.

Do not weaken legitimate empirical results merely because the study is bounded.

The goal is precise scope, not timid prose.

## 4. Check the following specific claim boundaries

### Clean metrics/statistics
Make sure:
- all five attempted seeds are retained where defined;
- YOLO11s seed 271 is not described as a failed run that should have been excluded;
- its zero precision/recall/F1 at frozen thresholds and nonzero AP are distinguished correctly;
- conditional matched-box IoU/Dice sample-size asymmetry is visible where needed;
- primary training-procedure bootstrap and checkpoint-conditional permutation results are not conflated;
- precision is not declared method-level different when the primary interval crosses zero;
- retrospective hypotheses are not called preregistered or confirmatory.

### Threshold analysis
Make sure:
- 0.25 is a protocol-sensitivity/common-cutoff result, not a chosen deployment threshold;
- detector-specific thresholds were selected on validation using the frozen n=3 procedure and subsequently applied unchanged;
- n=5 test sensitivity does not get rewritten as n=5 threshold selection;
- exploratory internal-testing threshold optima are not presented as selected deployment settings;
- AP is described as independent of the selected single operating threshold, not literally "threshold-free";
- FROC claims are bounded to the evaluated 0.01--0.99 sweep where necessary;
- lower-bound hits are described as observed grid boundaries, not global optima/asymptotes.

### Calibration
Make sure:
- D-ECE is explicitly a calibration ERROR measure;
- lower D-ECE is described correctly;
- comparisons remain descriptive where no inferential test was performed;
- D-ECE is conditional on emitted detections;
- missed targets are outside that estimand;
- the test-set evaluation is not described as post-hoc fitted calibration;
- detection calibration is not relabeled as patient-level probability calibration.

### Compute
Make sure:
- the approximate threefold throughput result is tied to the measured laptop/software stack and detector-specific profiling implementation;
- the Faster R-CNN/YOLO resize-timing difference is disclosed;
- registered-operation GFLOPs are described as estimates with unsupported operations omitted;
- no architecture-general speed law is claimed.

### Robustness
Make sure:
- digital common corruptions are not called scanner/site/population shift;
- DICOM-derived intensity perturbations are not called validated dose simulation;
- single seed-17 robustness evidence is clearly condition/checkpoint-specific;
- "robustness" is used as controlled stress-test robustness, not clinical safety.

### Grad-CAM / XAI
Make sure:
- weak localization results are reported rather than hidden;
- parameter randomization sensitivity is not treated as proof of clinical explanation validity;
- model-randomization and input-randomization controls are described accurately;
- absence of the Adebayo label-randomization/retraining test remains clear;
- saliency is not presented as causal reasoning.

## 5. Abstract audit

The abstract must be especially strict because editors may only read that before deciding whether to send the paper to review.

Check that it:

- states the bounded benchmark design;
- does not imply architectural causality;
- gives the headline AP result accurately;
- clearly distinguishes the raw 0.25 cutoff phenomenon from the broader AP/PR result;
- qualifies the FROC finding to the evaluated sweep where necessary;
- qualifies the approximately threefold throughput result;
- says "calibration error" for D-ECE;
- identifies descriptive versus inferential conclusions accurately;
- does not claim clinical utility.

Keep the abstract concise. Do not stuff every limitation into it.

## 6. Discussion and conclusion audit

The Discussion should explain why the project is scientifically useful:

- one common raw confidence threshold can place different detector pipelines in very different operating regimes;
- AP/ranking, raw score scale, fixed-threshold behavior, detection-level calibration, computational efficiency, corruption sensitivity, and XAI localization are different evaluation dimensions;
- reporting only one fixed threshold or only mAP can conceal important behavior.

But ensure the Discussion does NOT claim:
- a universal Faster-R-CNN-over-YOLO law;
- clinical superiority;
- external robustness;
- causal architecture effects.

The Conclusion should be concise and should not introduce any stronger claim than Results.

## 7. Declarations / author-controlled facts

Inspect every unresolved declaration.

NEVER infer author-controlled facts.

Unless explicit publishable facts are available in tracked project data or explicitly authorized by local project instructions, retain placeholders for:
- funding/support;
- conflicts;
- ethics determination;
- consent;
- CRediT contributions;
- patient/public involvement;
- final public repository/archive version;
- checkpoint release status.

Do not manufacture "Not applicable", "No funding", "No conflict", ethics exemption, or consent waiver statements.

Produce a final list for me of exactly what I must personally fill in before submission.

## 8. Consistency with README/audits

After editing the manuscript:

- synchronize only necessary claim/audit wording;
- maintain `results/` as numerical source of truth;
- preserve historical report/archive status;
- update `paper_claim_sources.yaml` only where textual references/anchors require it;
- do not alter source numerical cells or tolerances without evidence of an actual mistake.

## 9. Quality control

Run applicable lightweight repository checks according to local instructions, including where appropriate:

- paper claim verification;
- scientific artifact verification;
- reporting audits;
- relevant tests;
- `ruff` for modified Python, if any;
- `git diff --check`.

No training.
No new checkpoint inference.
No new corruption generation.
No new Grad-CAM generation.
No new statistical analysis.
No threshold-grid extension.

## 10. Give me a reviewer-style final report

After editing, respond with:

### Files changed

### Claims strengthened or clarified
List the important before/after conceptual changes, not every punctuation edit.

### Remaining scientific limitations
Only limitations that genuinely remain after these corrections.

### Author input still required
Especially declarations.

### Submission blockers
Clearly distinguish:
- scientific blocker;
- reporting blocker;
- author/declaration blocker;
- none.

### Verification
Commands and outcomes.

### Scope confirmation
Explicitly confirm whether:
- any new experiment was added;
- any model was retrained;
- any GPU inference was run;
- any frozen numerical result changed.

The desired answer for all four should be "no" unless you found an actual integrity problem, in which case explain it clearly.

Do not stage or commit.

### Why I would **not** give Codex a “fix the FROC by extending it” prompt yet

Your frozen prediction population goes down to `0.001`, while the exploratory FROC/threshold sweep starts at `0.01`; the current manuscript already acknowledges that the YOLO plateau is a lower-grid-boundary result.  Technically, you *could* design a new CPU-only low-score FROC sensitivity analysis from the frozen predictions without retraining. But that would be **new analysis**, not merely correcting an error.

Given your explicit preference—**the project is done; don't expand it**—I would first fix the claim to:

> “within the evaluated 0.01–0.99 score sweep…”

That is scientifically defensible and keeps your frozen research design intact.

The declaration issue is different: Section 8 genuinely remains a submission blocker because the manuscript explicitly still has author-action placeholders for funding, conflicts, ethics/data use, consent, contributions, availability, and patient/public involvement.  Codex should **never guess those**, which is why all three prompts explicitly protect them.

**Recommended workflow:** run Batch 1 → inspect `git diff` → commit yourself → run Batch 2 → inspect/commit → run Batch 3. If Batch 2 reports an actual implementation contradiction rather than just wording, stop there and show me its report before letting Codex modify the scientific pipeline.