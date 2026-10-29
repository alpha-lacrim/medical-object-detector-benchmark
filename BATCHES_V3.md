# BATCHES_V3.md — Correctness Fixes, Then Research Paper Track (continued)

Supersedes `BATCHES_V2.md` Batch 12 onward. Batches 9-11 from V2 stand (9 and 10 are
published on main; 11 is done locally, unreviewed — its Pareto figure gets partially revised
in Batch 14 below once the threshold-selection fix lands, so hold off on a separate review
pass for it and just review the revised version instead).

**Why this ordering:** three independent reviews converged on real correctness issues — a
red CI, image-level statistics that don't account for patient clustering, and a test-set
threshold-selection contamination already present in Batch 11's Pareto plot. All three get
fixed before any further seeds get trained (Batch 16) or the paper draft gets written (Batch
18), so nothing downstream has to be redone a second time.

---

## BATCH 12 — CI Green + Decision Log D-003

```
Read HANDOFF.md and CODEX.md first.

Two housekeeping items, no experiments.

1. CI has been red since 2026-08-12 (foundation-ci fails at `ruff format --check src tests`
   on both ubuntu-latest and windows-latest, before pytest ever runs). Run
   `uv run --locked ruff format src tests` locally, commit the formatting fixes, push, and
   confirm the next foundation-ci run is fully green (formatting + lint + pytest) on both
   platforms before proceeding. Do not loosen the CI config to force a pass — fix the actual
   formatting. If a specific ruff rule seems wrong for this codebase, say so explicitly and
   ask before changing the config.

2. Add docs/DECISION_LOG.md entry D-003, worded as follows (adapt lightly for house style,
   keep the substance):

   ## D-003 — Decline to revive a Track-B-style native/best-practice comparison

   - Date: <today>
   - Status: Accepted; does not reopen D-002

   ### Context
   An independent technical review recommended reviving a second, architecture-optimized
   comparison (each detector under its own best-practice recipe, equal tuning budget) to
   isolate "one-stage vs two-stage detectors" from "this Faster R-CNN pipeline vs this
   YOLO11s pipeline."

   ### Decision
   D-002's descoping is reaffirmed. The project's current claims do not depend on isolating
   architecture family in the abstract — they depend on the already-disclosed comparison of
   two specific, documented pipelines under shared constraints, which remains scientifically
   sound. A full Track B under an equal-opportunity tuning budget would multiply training
   compute substantially on the project's fixed hardware (RTX 4060 Laptop, 8GB VRAM), for a
   claim-strengthening addition rather than a correctness fix, while several correctness
   fixes (patient-cluster statistics, threshold-selection methodology, CI) are still
   outstanding and higher priority.

   ### Consequences
   - A much cheaper partial alternative remains available as optional future work: a single
     native-defaults run per detector (not a tuning search), explicitly framed as an
     exploratory robustness-of-conclusion check rather than a formal second track. This is
     not committed work and should only be considered after Batches 13-15 are complete and
     if compute time remains.
   - The paper's contribution stays framed around the controlled comparison, the multi-axis
     trade-off characterization, and the threshold/score-scale mismatch finding — not an
     architecture-family claim.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review — confirm CI is
actually green (describe or link the passing run) before Batch 13.
```

---

## BATCH 13 — Patient-Cluster Statistical Rework

```
Read HANDOFF.md and CODEX.md first.

This is the most important correctness fix identified across three independent reviews. No
retraining or new inference — this reprocesses the frozen Phase 5 clean prediction bundles
and existing robustness/threshold outputs already on disk.

Problem: the test split is patient-safe (no patient crosses train/validation/test), but
within the 750-image test set some patients have multiple images/exams. The current
bootstrap resampling and paired permutation test (Phase 8) resample/exchange at the IMAGE
level, treating correlated observations from the same patient as independent. This overstates
precision — tighter CIs and smaller p-values than are actually justified.

Fix, using the existing patient-group mapping from Batch 1 (locate it in
data/splits/rsna-pneumonia-5000/ or wherever the NIH patient-group IDs for the test split are
recorded — reuse it, don't rebuild it):

1. Bootstrap: resample PATIENT GROUPS from the test split with replacement, not individual
   images. For each resampled patient group, include every image belonging to that group.
   Recompute the dataset-level metric on the resulting pooled image set. Keep the existing
   number of bootstrap replicates unless there's a documented reason to change it.

2. Paired permutation test: adapt the exchange unit to respect patient clusters — the label
   swap (which detector's result counts as "A" vs "B" under a given permutation) happens at
   the patient-cluster level, so all images from one patient move together.

3. Recompute every primary and secondary CI, p-value, and Holm correction currently in
   docs/STATISTICAL_ANALYSIS.md using this corrected method. Archive the old image-level
   results (e.g. results/tables/statistical_clean_comparison_image_level_archive.csv) rather
   than deleting them, and note why the patient-cluster version is now primary.

4. Explicitly report whether the significance pattern changes: does anything Holm-significant
   under image-level resampling become non-significant under patient-cluster resampling, or
   vice versa? This is the single most important thing to flag back to me.

5. If jackknife Cohen's d isn't clearly valid once resampling is cluster-based, flag it rather
   than guessing — a simpler paired raw-difference-with-CI effect size is an acceptable
   fallback if you're not confident the jackknife formulation still holds.

Do not touch report/report.md or docs/QUANTITATIVE_COMPARISON.md's prose here — that
reconciliation happens in Batch 15, once Batch 14's methodology fixes also land. Just fix the
statistics module and its outputs in this batch.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review — specifically
tell me whether any conclusion actually changed once clustering is accounted for correctly.
```

---

## BATCH 14 — Threshold Selection on Validation, Terminology Fix, FROC Addition

```
Read HANDOFF.md and CODEX.md first.

Three related fixes, all reusing already-frozen predictions — no retraining.

1. TEST-SET CONTAMINATION FIX: Batch 10's threshold sweep ran on the TEST set, which is fine
   as a descriptive, exploratory analysis (already labeled as such in
   docs/THRESHOLD_ANALYSIS.md). But Batch 11's Pareto plot used the "peak observed mean-F1
   threshold" from that TEST-set sweep (0.63 for Faster R-CNN, 0.01 for YOLO11s) as if it
   were a selected operating point for the recall axis — that's test-set-derived threshold
   selection being presented as a result. Fix it:
   - Run the same sweep protocol from Batch 10, but on the 750-image VALIDATION split, both
     detectors, all three seeds.
   - Select each detector's operating threshold on validation only (e.g. peak mean F1, or
     another predeclared rule — state which and why).
   - Freeze those thresholds. Apply each exactly once to TEST for the final operating-point
     precision/recall/F1 reported anywhere a single chosen threshold is used.
   - Update the Pareto frontier's recall panel (results/figures/pareto_frontier.png,
     docs/PARETO_ANALYSIS.md) to use these validation-selected, test-evaluated thresholds.
     The AP-based panels are threshold-free and unaffected — leave them as-is.
   - The full PR curves (results/figures/precision_recall_curves.png) describe the whole
     curve, not a selected point, and were never a contamination risk — leave unchanged.

2. TERMINOLOGY FIX: docs/THRESHOLD_ANALYSIS.md currently describes the finding as a
   "selectivity/calibration effect." Replace every instance of "calibration" describing this
   finding with "score-scale/selectivity mismatch" (or equivalent) across
   THRESHOLD_ANALYSIS.md, PARETO_ANALYSIS.md, and anywhere else it appears this way — a PR
   sweep shows the two detectors' score distributions aren't interchangeable at a shared
   threshold; it does not demonstrate probabilistic calibration (whether a score of 0.8
   corresponds to ~80% empirical correctness). Do not claim calibration was measured anywhere
   it wasn't.

3. FROC ADDITION: reparametrize the existing threshold-sweep data (no new experiment) as a
   free-response ROC curve — sensitivity (recall) vs. average false positives per image, both
   detectors, using the frozen test-set sweep data from Batch 10 (threshold-free
   redescription of existing data, not a new selection, so item 1's contamination concern
   doesn't apply here). Report sensitivity at a small set of clinically-plausible FP/image
   points (e.g. 0.125, 0.25, 0.5, 1, 2 — state and justify the set used). Add
   results/figures/froc_curves.png, results/tables/froc_operating_points.csv, and
   docs/FROC_ANALYSIS.md explaining the protocol and finding.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review.
```

---

## BATCH 15 — Report/Docs Reconciliation

```
Read HANDOFF.md and CODEX.md first.

Now that Batches 13-14 corrected the statistics (patient-cluster) and the threshold
methodology (validation-selected, FROC-reframed, calibration language fixed), reconcile every
document describing the headline findings so nothing on main contradicts anything else.

- report/report.md: retire "the two paradigms occupy meaningfully different operating
  regimes" and the "recall-heavy proposal detector versus a selective, compact dense
  detector" framing (§11, around lines 457-465). Replace with the corrected finding: Faster
  R-CNN dominates the precision-recall frontier at nearly every point; YOLO11s's apparent
  precision advantage at the original fixed threshold is a score-scale/selectivity artifact,
  not a genuine frontier advantage; the defensible trade-off is detection quality vs.
  computational cost (cite the Pareto frontier and, now, the FROC curves). Also correct any
  language implying the original bootstrap/permutation was already patient-cluster-aware.
- docs/QUANTITATIVE_COMPARISON.md: same correction to its summary paragraph.
- docs/PARETO_ANALYSIS.md: confirm it reflects Batch 14's validation-selected thresholds.
- docs/STATISTICAL_ANALYSIS.md: confirm the patient-cluster results are presented as primary,
  with the image-level version clearly marked superseded/archived.
- docs/LIMITATIONS.md: remove the now-resolved image-level-clustering limitation (replace
  with a note that it was identified and corrected in Batch 13), and fold in the "digital
  robustness not clinical robustness" and "implementation-specific, not architecture-general,
  compute comparison" wording precision if not already present.

Read report.md, QUANTITATIVE_COMPARISON.md, THRESHOLD_ANALYSIS.md, PARETO_ANALYSIS.md,
STATISTICAL_ANALYSIS.md, and FROC_ANALYSIS.md together afterward and confirm no two of them
describe the same finding in contradictory language.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review — this is the
point where the repository's narrative should be fully internally consistent for the first
time since Batch 10 was added.
```

---

## BATCH 16 — Additional Seeds for the Clean Headline Comparison (3 → 5)

```
Read HANDOFF.md and CODEX.md first.

Same as previously planned, now running after the methodology fixes so the n=5 statistics
are computed correctly the first time. Budget for this on the RTX 4060 8GB/16GB RAM hardware
per PROJECT_SPEC.md §3 — this remains the expensive batch in the sequence.

Train two additional seeds (e.g. 271 and 314) for BOTH Faster R-CNN and YOLO11s, using the
exact same configs as seeds 42/137 (same augmentation-disabled policy, same disclosed
asymmetries — do not change the training recipe here). Get a time estimate and my sign-off
before committing to the runs.

Once approved and trained: re-run the unified evaluator and the (now patient-cluster-aware,
per Batch 13) statistics module with n=5 for the CLEAN comparison only. Do not re-run
robustness or explainability at 5 seeds — those stay scoped to seed 17 as documented. Archive
the n=3 tables rather than deleting them.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review — flag whether
the Holm-corrected significance pattern held at n=5, now under the corrected clustering
methodology.
```

---

## BATCH 17 — Literature Review Reframing + Hypotheses

```
Read HANDOFF.md and CODEX.md first.

Writing/reasoning only, no experiments.

1. Revise docs/LITERATURE_REVIEW.md to argue a specific gap: prior medical-detector
   comparisons typically vary dataset splits, preprocessing, augmentation, thresholds, and
   metric implementations simultaneously, preventing clean attribution to architecture. This
   project's contribution is isolating that comparison under one controlled, patient-safe,
   unified-evaluation protocol — plus the finding that a shared nominal threshold does not
   guarantee a shared operating regime. Use real citations from references.bib; don't
   fabricate any.

2. Add docs/HYPOTHESES.md with a primary research question and 4-6 sub-hypotheses covering:
   detection coverage/AP, the corrected precision-recall/FROC finding (Batches 13-14), the
   accuracy-compute Pareto trade-off, corruption-specific (not uniform) robustness
   degradation, and Grad-CAM as failure-analysis rather than evidence of clinical reasoning.
   Each must be checkable against a specific existing table or figure.

3. Terminology pass: use "lung-opacity detection" (not "pneumonia detection") wherever a
   claim could otherwise sound diagnostic, across docs/ and report/report.md.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review before Batch 18.
```

---

## BATCH 18 — Paper Draft (IMRaD Restructure)

```
Read HANDOFF.md and CODEX.md first.

Do NOT edit report/report.md in place — it stays as the complete technical/reproducibility
report. Create report/paper_draft.md, pulling from report.md, docs/HYPOTHESES.md, and every
Batch 10-17 artifact (threshold sweep, FROC, Pareto, patient-cluster statistics).

Structure: Title (avoid "pneumonia detection," avoid "benchmark" as an unqualified claim —
scope it explicitly as a controlled comparative study of two detector families) → Abstract
(~250 words, state the contribution as the controlled-comparison methodology plus the
threshold/score-scale mismatch finding, not "Faster R-CNN is better") → Introduction →
Related Work (the gap argument from Batch 17) → Materials and Methods (dataset, patient-safe
split, both detectors, the disclosed training-recipe asymmetry as an explicit factor, unified
evaluation, validation-selected threshold protocol, FROC protocol, patient-cluster
statistical protocol) → Results (clean performance; PR/FROC operating regimes; Pareto
frontier; robustness; explainability/failure analysis; statistical synthesis) → Discussion
(trade-offs, not a winner; explicitly note the comparison is of two disclosed pipelines, not
an architecture-family claim, per D-002/D-003) → Limitations (pull from docs/LIMITATIONS.md
verbatim in spirit — do not soften the hedging) → Conclusion.

Target ~8-12 pages, two-column-equivalent length. Move exhaustive implementation detail to a
Supplementary Material pointer back to report.md and the repository.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review.
```

---

## BATCH 19 — (Optional) Single Native-Defaults Run Per Detector

```
Read HANDOFF.md and CODEX.md first.

OPTIONAL — only run if explicitly told to, and only after Batches 13-18 are done. This is
the cheap compromise from D-003: ONE run per detector using each framework's sensible
best-practice defaults (YOLO11s with its native augmentation stack re-enabled; Faster R-CNN
with any reasonably-defaulted equivalent), NOT a tuning search or equal-opportunity trial
budget — that would be a full Track B, which D-003 declined. Frame this explicitly in
docs/ as an exploratory robustness-of-conclusion check: does the controlled-comparison
ranking hold when each detector gets its own natural recipe? Report the result plainly
either way, and do not let this single run's outcome override the primary controlled-protocol
result — it's a secondary check, not a replacement.

Before training: report a time estimate and get my sign-off first.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 20 — Final Consistency Pass

```
Read HANDOFF.md and CODEX.md first.

1. Confirm every number in paper_draft.md traces to a committed results/ artifact.
2. Confirm docs/LIMITATIONS.md reflects: n=5 seeds, patient-cluster statistics, the
   validation-selected threshold protocol, FROC, and (if run) the Batch 19 native-defaults
   check.
3. Confirm references.bib has no missing/duplicate entries and every citation resolves.
4. Regenerate README.md's reproduction command index to include every script added since
   Batch 12.
5. Run the full test suite, linter, and confirm CI is still green on the final commit.

When done: update CODEX.md to mark this iteration complete, and write a final HANDOFF.md
entry summarizing the full delta from Batch 9 through Batch 20.
```
