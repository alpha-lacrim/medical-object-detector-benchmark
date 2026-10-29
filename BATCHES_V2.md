# BATCHES_V2.md — Research Paper Track

Continues from `BATCHES.md` (Batches 0-8, the completed course deliverable). Do not run any
of these before Batch 9. Same protocol as before: paste one at a time, read `HANDOFF.md` and
`CODEX.md` at the start of each, update both at the end, stop at every review checkpoint.

**Priority order, if you don't run all of them:** Batch 9 (housekeeping) → Batch 10
(threshold sweep — highest value, lowest cost) → Batch 11 (Pareto — cheap) → Batch 13
(reframing — cheap, writing only) → Batch 14 (paper draft) → Batch 12 (more seeds — the
expensive one) → Batch 16 (final pass). Batch 15 (third detector) is optional and should be
run last, only if reviewer feedback specifically calls for it.

---

## BATCH 9 — Freeze V1, Resolve Decision-Log Inconsistency, GFLOPs Sanity Check

```
Read HANDOFF.md and CODEX.md first.

This repository's course-project deliverable (Batches 0-8) is complete. Before starting any
new research-track work, freeze it:

1. Create an annotated git tag `v1-course-submission` on the current HEAD commit, with a
   message summarizing what it contains (two detectors, unified evaluator, robustness,
   Grad-CAM, statistics, 12-section report). Do not rewrite history to create this tag.

2. Resolve the loose end in docs/DECISION_LOG.md: entry D-001 proposes a two-track design
   (Track A: assignment-aligned controlled comparison; Track B: a separately-tuned,
   architecture-optimized comparison), but only Track A was ever delivered. Add a new entry
   D-002 to the log (do not edit D-001) that formally supersedes the Track B portion, stating
   it was descoped for hardware/time budget reasons and that the research-paper direction
   this project is now taking reframes the contribution around controlled comparison and
   multi-axis trade-off analysis rather than best-effort leaderboard performance — so Track B
   is not needed. If you think Track B should instead be revived, stop and ask before writing
   D-002.

3. Sanity-check the GFLOPs estimates in results/tables/faster_rcnn_compute.csv and
   yolo_compute.csv (currently ~450.76 vs ~21.42, a ~21x gap) against typical literature-
   reported values for fasterrcnn_resnet50_fpn_v2 and YOLO11s at comparable input resolution.
   Document the counting methodology used (which ops are registered/counted, whether RPN+RoI
   heads are included, proposal count assumptions) in docs/QUANTITATIVE_COMPARISON.md so the
   number is defensible even if it isn't directly comparable to other papers' reported FLOPs.
   Do not change the measured numbers — only document/verify the methodology behind them.

Do not modify any existing results/, report/, or docs/ content beyond what's specified above.

When done: update CODEX.md's Decisions Log with the D-002 resolution and the v1 tag, and
append a HANDOFF.md entry. Stop for my review — this batch is housekeeping, not new
experiments, so it should be fast.
```

---

## BATCH 10 — Precision-Recall / Threshold Sweep Analysis

```
Read HANDOFF.md and CODEX.md first.

This is the single highest-value addition for the research-paper direction: it requires no
retraining, only reprocessing the frozen prediction bundles already produced in
results/logs/phase5_evaluation/ (six frozen clean bundles) — do not retrain or re-infer
anything.

Add src/evaluate_threshold_sweep.py (or extend src/evaluate.py with a new mode) that, for
each of the six frozen prediction bundles (Faster R-CNN and YOLO11s, seeds 17/42/137):

1. Sweeps confidence threshold from 0.01 to 0.99 (e.g. 50-99 steps) and recomputes precision,
   recall, and F1 at each threshold using the SAME matching/IoU logic already implemented in
   the unified evaluator (src/evaluate.py) — do not reimplement matching from scratch, import
   and reuse the existing matcher.
2. Also expose the full precision-recall curve underlying AP (this already exists inside the
   pycocotools computation — expose it rather than recomputing).
3. Produces, per detector (averaged/aggregated across the three seeds with a shaded band or
   mean ± std, consistent with how Table 4a/4b were built):
   - results/tables/threshold_sweep.csv (threshold, precision, recall, F1 per detector)
   - results/figures/precision_recall_curves.png (both detectors on one plot)
   - results/figures/f1_vs_threshold.png
4. Compute and report, per detector: recall at fixed precision (e.g. at precision=0.5 and
   precision=0.9, if reachable) and precision at fixed recall (e.g. at recall=0.3 and 0.5).
   Report "not reachable at any threshold" honestly if a detector never hits a target level
   rather than extrapolating.

Write docs/THRESHOLD_ANALYSIS.md summarizing what this shows: does YOLO11s's apparent
low-recall/high-precision profile persist across the whole operating curve, or was it an
artifact of the fixed 0.25 threshold used in the main comparison? State the finding plainly,
whichever way it comes out — this is meant to test, not confirm, the headline result.

When done: update CODEX.md (new files, one-line summary of the finding) and append a
HANDOFF.md entry. Stop for my review of the PR curves before Batch 11 — this result will
shape how confidently later batches can claim the detectors occupy "distinct operating
regimes" rather than just "different results at one threshold."
```

---

## BATCH 11 — Pareto Accuracy-Efficiency Frontier

```
Read HANDOFF.md and CODEX.md first.

This reuses existing data — no retraining, no new inference. Combine
results/tables/detector_comparison.csv (accuracy) with results/tables/*_compute.csv
(FPS/latency/params/GFLOPs) and, since Batch 10 is done, threshold_sweep.csv.

Produce results/figures/pareto_frontier.png: a 2x2 panel figure with:
   (a) mAP@0.5:0.95 vs FPS, both detectors, all three (or five, if Batch 12 has run) seeds
       plotted individually, not just the mean, so seed spread is visible;
   (b) recall vs latency;
   (c) mAP@0.5:0.95 vs parameters;
   (d) recall vs estimated GFLOPs.
Mark which detector is Pareto-dominant in each panel, or state neither dominates if the
points aren't strictly ordered.

Write docs/PARETO_ANALYSIS.md with 3-4 sentences per panel on what it shows, avoiding
"winner" language — frame it as which detector is preferable under which resource
constraint, consistent with the rest of the project's scenario-conditional framing (see
report.md §11.3 for the tone to match).

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review before Batch 13
(or Batch 12, if you're doing the extra seeds first).
```

---

## BATCH 12 — Additional Seeds for the Clean Headline Comparison (3 → 5)

```
Read HANDOFF.md and CODEX.md first.

This is the expensive batch — budget for it accordingly on this hardware (RTX 4060 8GB,
16GB RAM; see PROJECT_SPEC.md §3 for the original timing/scoping approach, reuse the same
preflight/benchmark/train gate pattern used for seeds 42 and 137 in the original BATCHES.md
Batch 4 flow). Target n=5 total, not more — see the reasoning in HANDOFF.md if you want it,
but don't chase 10 seeds on this hardware for a marginal statistical gain.

Train two additional seeds (e.g. 271 and 314 — pick and document any two new seeds distinct
from 17/42/137) for BOTH Faster R-CNN and YOLO11s, using the exact same configs as the
existing seed-42/137 runs (same augmentation-disabled policy, same hyperparameter
asymmetries already disclosed in docs/LIMITATIONS.md — do not silently change anything about
the training recipe here, this batch only adds seed count, it does not re-litigate the
protocol).

Before running the full training: derive timing approvals the same way Batch 4 did
originally (reuse/extend the seed-gates mode in src/evaluate.py), get a time estimate, and
stop for my sign-off before committing to the runs — four more full trainings (2 seeds x 2
detectors) at the measured ~1.7-2h/seed for Faster R-CNN and ~30min/seed for YOLO11s is a
non-trivial chunk of wall-clock time on this laptop.

Once approved and trained: re-run the unified evaluator (src/evaluate.py --mode evaluate)
and the statistics module (src/stats/run_statistics.py) with n=5 seeds instead of n=3 for
the CLEAN comparison only — do NOT re-run robustness or explainability at 5 seeds, those
stay scoped to seed 17 as already documented in docs/LIMITATIONS.md's seed-scoping section.

Update results/tables/detector_comparison.csv, detector_comparison_mean_std.csv,
detector_comparison_per_seed.csv, and results/tables/statistical_clean_comparison.csv to
reflect n=5. Do not delete the n=3 versions — archive them as
results/tables/detector_comparison_n3_archive.csv etc. so the numbers tagged
v1-course-submission remain traceable.

When done: update CODEX.md (new seed count, whether conclusions changed materially) and
append a HANDOFF.md entry. Stop for my review — specifically flag whether the Holm-corrected
significance pattern from the n=3 analysis held up at n=5, since that's the number a
reviewer will scrutinize most.
```

---

## BATCH 13 — Literature Review Reframing + Research Questions/Hypotheses

```
Read HANDOFF.md and CODEX.md first.

This is a writing/reasoning batch, not an experiment — no training or inference.

1. Revise docs/LITERATURE_REVIEW.md to argue a specific gap rather than only describe the
   two architectures. Add a paragraph (with real citations, following this project's
   existing citation discipline in references.bib — do not fabricate references) making the
   case that prior medical-detector comparisons typically vary dataset splits, preprocessing,
   augmentation, thresholds, and metric implementations simultaneously, which prevents
   attributing results to detector architecture alone — and that this project's contribution
   is isolating that comparison under one controlled, patient-safe, unified-evaluation
   protocol.

2. Add docs/HYPOTHESES.md stating:
   - One primary research question about how contrasting detector paradigms trade off
     accuracy, operating-point behavior, computational cost, and corruption robustness under
     a controlled protocol.
   - 4-5 sub-hypotheses covering: detection coverage/AP, precision/efficiency, whether the
     PR-curve (Batch 10) shows the operating-point difference persists across thresholds,
     whether robustness degradation is corruption-specific rather than uniform, and whether
     Grad-CAM attribution differs systematically between the two without claiming clinical
     validity.
   Each hypothesis must be checkable against a specific table or figure already in results/
   or produced in Batches 10-12 — no untestable claims.

3. Do a terminology pass over docs/ and report/report.md: the target is a radiographic
   "Lung Opacity," not confirmed pneumonia. Make sure "lung-opacity detection" (or equivalent
   precise phrasing) is used wherever a claim could otherwise sound diagnostic. Do not change
   the underlying dataset/task, just the terminology precision.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review of the reframed
research questions before Batch 14 — get these right before restructuring the report around
them.
```

---

## BATCH 14 — Paper Draft (IMRaD Restructure)

```
Read HANDOFF.md and CODEX.md first.

Do NOT edit report/report.md in place — that stays as the complete technical/reproducibility
report. Create report/paper_draft.md: a tighter, publication-style manuscript pulling from
report.md, docs/HYPOTHESES.md, and the Batch 10-12 artifacts — not report.md renamed.

Structure:
1. Title — reflect the reframed contribution, not "Faster R-CNN vs YOLO comparison." Use
   "lung-opacity detection" per Batch 13's terminology pass.
2. Abstract (~250 words) — state the contribution as characterizing accuracy/efficiency/
   robustness trade-offs under a controlled protocol, not "we found Faster R-CNN is better."
3. Introduction — problem, the literature gap from Batch 13, the research questions.
4. Related Work — reorganize docs/LITERATURE_REVIEW.md's content into: detector paradigms;
   robustness/corruption benchmarking; explainability in detection; evaluation/reproducibility
   in medical AI. Keep it argumentative, not descriptive.
5. Materials and Methods — dataset, patient-grouped split, preprocessing, both detectors,
   controlled training protocol (foreground the augmentation/precision asymmetries as an
   explicit documented experimental factor, not a footnote), unified evaluation, threshold
   sweep protocol, robustness protocol, explainability protocol, statistical protocol.
6. Results — reorganize around: (a) clean detection performance at fixed threshold; (b)
   precision-recall operating regimes (Batch 10 figure); (c) accuracy-efficiency Pareto
   frontier (Batch 11 figure); (d) robustness; (e) explainability/failure analysis; (f)
   statistical synthesis. Pull numbers only from committed results/ artifacts.
7. Discussion — organize around trade-offs, not a winner: coverage vs selectivity, the
   scenario-conditional recommendation already in report.md §11.3 (keep that framing), what
   the PR-curve/Pareto results add or change, explainability as failure-analysis not clinical
   evidence.
8. Limitations — pull directly from docs/LIMITATIONS.md. Do not soften or shorten the
   hedging language — carry it over faithfully.
9. Conclusion — the trade-off framing, explicit future work (external validation, additional
   architecture families, full-cohort scale-up).

Target roughly 8-12 pages in typical two-column conference format (don't worry about exact
LaTeX yet, write it at that length in Markdown) — move exhaustive implementation detail,
full seed-level tables, and command listings to a "Supplementary Material" pointer back to
report.md and the repository rather than inlining them here.

When done: update CODEX.md and append a HANDOFF.md entry. Stop for my review — this is the
first full draft, expect another editing pass after I read it.
```

---

## BATCH 15 — (Optional) Third Detector Baseline

```
Read HANDOFF.md and CODEX.md first.

OPTIONAL — only run this batch if explicitly told to proceed. It genuinely strengthens the
architecture-level claim (right now the study can only say "this Faster R-CNN vs this
YOLO11s," not "two-stage vs one-stage" in general), but it's expensive: a full third
training + evaluation pipeline at roughly the same order of compute as the Faster R-CNN arm.

If proceeding: add RetinaNet (torchvision `retinanet_resnet50_fpn_v2`) as a second one-stage
reference, following the exact same pattern as src/models/faster_rcnn.py — same dataset,
same disabled-augmentation policy, same evaluation harness, start with seed 17 only, extend
to the full seed count only after confirming it's worth repeating a third time. Update
src/evaluate.py to handle three detectors, and update every downstream table/figure
generator from Batches 10-11 to plot three lines instead of two.

Before training: run the same preflight/benchmark/approval gate pattern as the other
detectors and report the time estimate for my sign-off first.

When done: update CODEX.md and HANDOFF.md. Stop for review.
```

---

## BATCH 16 — Final Consistency Pass

```
Read HANDOFF.md and CODEX.md first.

Do a full consistency pass across report/paper_draft.md, report/report.md, and all of docs/:

1. Confirm every number cited in paper_draft.md traces to a committed results/ artifact.
2. Confirm docs/LIMITATIONS.md reflects the n=5 seed count (Batch 12), the threshold-sweep
   and Pareto additions (Batches 10-11), and the third detector if Batch 15 ran.
3. Confirm references.bib has no missing or duplicate entries and every citation in
   paper_draft.md resolves.
4. Regenerate the README.md reproduction command index to include the new scripts from
   Batches 10-12 (and 15 if applicable), following the existing "report item -> generated
   source -> regenerating command" table format.
5. Run the full test suite and linter (as in the README's verification section) and confirm
   everything still passes after all the new code added in Batches 9-15.

When done: update CODEX.md to mark the research-paper track complete for this iteration, and
write a final HANDOFF.md entry summarizing the full V1 -> V2 delta.
```
