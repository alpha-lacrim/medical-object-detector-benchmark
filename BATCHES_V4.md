# BATCHES_V4.md — Q1-Direction Extensions (Phases 9-14), Solo Track

For `Alpha-lacrim/medical-object-detector-benchmark`. Continues from `BATCHES_V3.md` — Batches
0-17 are done and verified real (checked directly against this repo's committed data before
writing this file: `detector_comparison.csv`, `DECISION_LOG.md` through D-003,
`HYPOTHESES.md`, `PARETO_ANALYSIS.md`, `FROC_ANALYSIS.md`, `statistical_clean_comparison.csv`
and its image-level archive all present and internally consistent with each other and with
the README).

**Why these six phases go before the paper draft:** all six reuse the frozen prediction
bundles you already have — no retraining, and only two of them (XAI sanity, radiography
shifts) touch the GPU at all, both for light inference passes over existing checkpoints on
subsets you already defined. That makes this materially cheaper than the seed-count batch you
already ran. Since all six produce Results-section content, drafting the paper before them
would mean revising the draft substantially once they land — better to do them first and
draft once.

Same discipline as every batch file so far: read `HANDOFF.md`/`CODEX.md` first if this repo
keeps them (check before assuming either way), update both after, stop at every review
checkpoint, no exceptions for a batch "seeming small."

---

## BATCH 18 — Detection-Specific Probability Calibration

```
Read HANDOFF.md and CODEX.md first (if present in this repo — check before assuming).

Implement docs/HYPOTHESES.md's calibration hypothesis (add it now as H6 if it isn't already
there — see step 4). No retraining: this operates on the frozen five-seed prediction bundles
already in results/logs/.

1. Create src/stats/calibration.py implementing multivariate detection calibration following
   Küppers et al., "Multivariate Confidence Calibration for Object Detection" (CVPR
   Workshops, 2020). A public reference implementation exists at
   github.com/fabiankueppers/calibration-framework — check its license against this repo's
   license before depending on it directly; reimplement the relevant method if it isn't
   compatible, citing the paper either way.
2. Compute a detection-appropriate calibration error for Faster R-CNN and YOLO11s, all five
   seeds each — not naive classifier-style ECE. A detector emits a variable number of scored
   boxes per image; calibration here means assessing whether a matched detection's confidence
   corresponds to its empirical correctness rate, following the cited framework's approach.
3. Quantify YOLO11s seed 271's confidence-score pathology explicitly as part of this analysis
   — it should appear as a severe outlier in calibration terms. Do not impute or exclude it;
   it's an observed, already-documented finding (see docs/LIMITATIONS.md), not missing data.
4. Add an H6 entry to docs/HYPOTHESES.md if calibration isn't already covered there, following
   the file's existing format (operational check, which artifact it's tested against).
5. Output results/tables/calibration_summary.csv and results/figures/reliability_diagrams.png
   (mean predicted probability vs. fraction of true positives, both detectors).
6. Write docs/CALIBRATION_ANALYSIS.md: method, finding, and an explicit statement that this
   measures calibration — distinct from the score-scale/selectivity mismatch already
   established in docs/THRESHOLD_ANALYSIS.md. Don't conflate the two findings; they're
   complementary, not the same claim restated.

When done: update CODEX.md and HANDOFF.md if present. Stop for review.
```

---

## BATCH 19 — Patient-Cluster-Aware Threshold Calibration

```
Read HANDOFF.md and CODEX.md first.

No retraining — reuses frozen predictions.

RECONCILE WITH EXISTING WORK FIRST: you already have a validation-selected operating
threshold per detector (results/tables/selected_operating_points_per_seed.csv,
docs/THRESHOLD_ANALYSIS.md). This batch adds a more sophisticated, cost-weighted
alternative. Before writing code, add a docs/DECISION_LOG.md entry (D-004) stating explicitly
whether this batch's output SUPERSEDES the existing threshold selection for downstream use
(e.g. in the eventual paper draft), or stands alongside it as a distinct cost-sensitivity
extension reported separately. Don't let two threshold-selection documents coexist without a
stated relationship between them — that's exactly the kind of contradiction already fixed
once in this project's history.

1. Create src/stats/threshold_calibration.py implementing:
   F1_β(τ) = (1+β²)·P(τ)·R(τ) / (β²·P(τ) + R(τ)), where β = √(C_FN/C_FP)
2. Outer loop over τ ∈ [0.01, 0.99]; inner loop of patient-cluster bootstrap — reuse the
   patient-cluster resampling code already built for the statistics module, don't
   reimplement it.
3. Select τ* optimizing the lower 95% CI bound, for β ∈ {1, 3, 5, 10}. Report the full
   sensitivity sweep rather than picking one β as definitive — the cost ratio is an
   assumption, not something measured from data, and the sweep is what makes that honest.
4. Output results/tables/threshold_calibration_summary.csv and
   results/figures/threshold_calibration_sensitivity.png (the β sweep).
5. Write docs/THRESHOLD_CALIBRATION.md: the math, the method, the D-004 reconciliation
   decision, and the finding.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 20 — Decision Curve Analysis

```
Read HANDOFF.md and CODEX.md first.

No retraining — reuses frozen predictions.

1. Create src/clinical/decision_curve.py computing:
   NetBenefit(τ) = TP/N - (FP/N)·[τ/(1-τ)], across τ ∈ [0.01, 0.99], both detectors.
2. Compute the disease-prevalence figure used in this calculation EMPIRICALLY from the full
   750-image test split (not a generic literature number, and not incidentally reused from
   the smaller 300-image robustness subsample unless you've confirmed that's actually the
   right population for this specific claim). State the population and resulting prevalence
   explicitly in the output.
3. Apply patient-cluster bootstrap resampling (reuse the existing machinery) for 95% CIs on
   Net Benefit.
4. Output results/tables/dca_summary.csv (net benefit, CIs, treat-all/treat-none references
   at each τ) and results/figures/dca_curves.png (Net Benefit curves with confidence ribbons
   for both detectors, plus the reference lines).
5. Write docs/DCA_ANALYSIS.md: method, prevalence source, and a clinical-relevance
   interpretation — which threshold-probability ranges favor which detector, tied to the
   scenario framing already established elsewhere in this project (retrospective screening
   vs. point-of-care) rather than inventing new scenario language here.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 21 — XAI Sanity Checks

```
Read HANDOFF.md and CODEX.md first.

Light GPU use — forward/backward passes on already-trained checkpoints over a small subset,
not new training.

1. Create src/explainability/sanity_checks.py. Define a stratified 50-image subset of the
   existing robustness test pool (reuse that pool's manifest — don't draw a new sample).
2. Parameter-randomization test: clone the trained model, reinitialize all weights via
   torch.nn.init.xavier_normal_, extract Grad-CAM heatmaps.
3. Data-randomization test: shuffle input pixel matrices, extract Grad-CAM heatmaps from the
   unmodified trained model.
4. Compute C_sanity = (1/K)·Σ Corr(M_trained^(k), M_randomized^(k)) for both tests, both
   detectors.
5. Output results/tables/gradcam_sanity_summary.csv (failure rates, correlation values) and
   results/figures/gradcam_sanity_panel.png (trained-vs-randomized qualitative panels).
6. Write docs/XAI_SANITY.md: method, finding, and an explicit statement of what the result
   means for the project's existing Grad-CAM claims (which already frame it as a
   failure-analysis tool, not evidence of clinical reasoning — state whether this
   reinforces or complicates that framing; report honestly either way, this is meant to test
   the existing claim, not just support it).

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 22 — Radiography-Physics-Aware Acquisition Shifts

```
Read HANDOFF.md and CODEX.md first.

GPU inference on existing seed-17 checkpoints over the existing 300-image robustness subset —
not new training.

PREREQUISITE CHECK — do this before writing any code: confirm the raw DICOM files for the
robustness subset (or the full processed cohort) are still present on local disk. data/raw/
is gitignored, so check the filesystem directly rather than assuming from the repo. If they
were deleted after the original PNG conversion, report that back before proceeding — a
re-download changes this batch's scope and timeline.

1. Create src/robustness/radiography_shifts.py — named for "radiography," not "DICOM/CT,"
   because this targets planar-radiography physics specifically.
2. Implement DICOM VOI LUT / Window Center-Width variations on the raw pixel arrays.
   Explicitly do NOT use Hounsfield Unit terminology or CT-specific windowing logic — chest
   X-rays are planar radiographs, not CT reconstructions, and have no HU scale. Ground this in
   the actual DICOM VOI LUT standard, not an invented approximation.
3. Implement signal-dependent Poisson noise on the raw sensor-scale data (modeling dose
   reduction).
4. Implement Gaussian-blur kernels modeling reconstruction/detector variation.
5. Run the shifted raw arrays through the existing per-image min-max scaling function (reuse
   it, don't reimplement) to produce valid 8-bit model inputs.
6. Run inference over the shifted 300-image subset for both detectors' seed-17 checkpoints.
   Compute Domain Shift Index: DSI = 1 - (Performance_shifted / Performance_clean).
7. Output results/tables/acquisition_shift_results.csv.
8. Write docs/ACQUISITION_SHIFTS.md, explicitly distinguishing this from the existing digital
   corruption robustness (results/tables/robustness_curves.csv): this is acquisition-physics
   motivated, that was generic digital corruption. State clearly what each does and does not
   claim, consistent with the "digital robustness, not clinical robustness" distinction
   already established in docs/LIMITATIONS.md.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 23 — Standards-Compliant Reporting & Supplementary Visualizations

```
Read HANDOFF.md and CODEX.md first. Do this after Batches 18-22 — it references their
outputs.

1. Create docs/REPORTING_CHECKLIST.md mapping this project's actual artifacts, splits,
   threshold decisions, and code files to CLAIM, TRIPOD-AI, and STARD-AI checklist items.
   Only mark an item complete if it's verifiably true of the current repository — check each
   claim against a real file or table before checking it off. Do not write anything here that
   isn't traceable.
2. Generate raincloud plots (ptitprince or seaborn) for the seven primary predictive metrics
   plus the hardware/latency metrics, from results/tables/detector_comparison.csv and its
   per-seed breakdown. If any panel mixes different sample sizes (e.g. n=5 clean vs. n=3
   robustness-era data), label that explicitly in the panel — don't let it read as one
   consistent n.
3. Save results/figures/raincloud_metrics.png.
4. Compile a Supplementary Materials section (docs/SUPPLEMENTARY.md or similar) pointing to
   full seed-level data, complete corruption grids, and the decision log — pointer-style,
   consistent with how the existing report avoids inlining exhaustive tables.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 24 — Paper Draft (IMRaD Restructure)

```
Read HANDOFF.md and CODEX.md first.

Do NOT edit report/report.md in place — it stays as the complete technical/reproducibility
report. Create report/paper_draft.md, pulling from report.md, docs/HYPOTHESES.md, and every
artifact from Batches 9-23 (threshold sweep, FROC, Pareto, patient-cluster statistics,
calibration, cost-weighted threshold calibration, DCA, XAI sanity checks, radiography-physics
robustness).

Structure: Title (avoid "pneumonia detection," scope explicitly as a controlled comparative
study of two detector families, not an unqualified "benchmark") → Abstract (~250 words,
lead with the controlled-comparison methodology and the threshold/score-scale mismatch
finding, not "Faster R-CNN is better") → Introduction → Related Work (the literature gap
already argued in docs/LITERATURE_REVIEW.md) → Materials and Methods (dataset, patient-safe
split, both detectors, the disclosed training-recipe asymmetry as an explicit factor, unified
evaluation, validation-selected and cost-weighted threshold protocols, FROC, calibration, DCA,
patient-cluster statistical protocol) → Results (clean performance; PR/FROC operating
regimes; calibration and reliability; Pareto frontier; DCA net benefit; digital and
acquisition-physics robustness; explainability plus XAI sanity findings; statistical
synthesis) → Discussion (trade-offs, not a winner; explicit that this compares two disclosed
pipelines, not an architecture-family claim, per D-002/D-003) → Limitations (pull from
docs/LIMITATIONS.md verbatim in spirit — do not soften the hedging) → Conclusion.

Target ~10-14 pages given the expanded evidence base. Move exhaustive implementation detail
to a Supplementary Material pointer (docs/SUPPLEMENTARY.md from Batch 23) rather than inlining
it.

When done: update CODEX.md and HANDOFF.md. Stop for review — this is the first full draft
incorporating everything; expect another editing pass after you read it.
```

---

## BATCH 25 — (Optional) Single Native-Defaults Run Per Detector

```
Read HANDOFF.md and CODEX.md first.

OPTIONAL — only run if you decide it's worth the time, and only after Batch 24. Per D-003,
this is deliberately NOT a full tuning search (that would be the Track B that's already been
declined twice) — just one run per detector using each framework's sensible best-practice
defaults (YOLO11s with its native augmentation stack re-enabled; Faster R-CNN with a
reasonably-defaulted equivalent), framed explicitly as an exploratory
robustness-of-conclusion check: does the controlled-comparison ranking hold when each
detector gets its own natural recipe? Report the result plainly either way, and don't let a
single run override the primary controlled-protocol result — it's a secondary check.

Before training: report a time estimate and confirm you want to spend it before committing.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 26 — Final Consistency Pass

```
Read HANDOFF.md and CODEX.md first.

1. Confirm every number in report/paper_draft.md traces to a committed results/ artifact.
2. Confirm docs/LIMITATIONS.md reflects everything from Batches 18-23 (calibration scope,
   DCA prevalence assumption, XAI sanity findings, acquisition-shift subset limitations) and,
   if run, Batch 25.
3. Confirm references.bib has no missing/duplicate entries and every citation resolves,
   including the new Küppers et al. and Vickers et al. (DCA) citations.
4. Regenerate README.md's reproduction command index to include every script added since
   Batch 18.
5. Run the full test suite and linter, and confirm CI is green on the final commit.

When done: update CODEX.md to mark this iteration complete, and write a final HANDOFF.md
entry summarizing the full delta from Batch 18 through Batch 26.
```
