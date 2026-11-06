# External failure isolation v1: controlled diagnostic protocol

Designed 2026-10-30 after all original outcomes and the first post-hoc analysis
were known. This is exploratory intervention on two implementation factors,
not causal identification of the entire RSNA-to-VinDr performance difference.
The user requested trying to isolate causes and resumed the task. The scope
here is bounded diagnostic GPU inference plus full-cohort CPU evaluation.
Original v1 artifacts and the separately proposed full-cohort candidate-support
v2 experiment are unchanged. This diagnostic is not execution of that proposal.

## Questions and scope

1. Does the fixed DICOM window recorded in each image change strict-target
   localization/confidence when checkpoint, image identity, geometry and
   postprocessing are held fixed?
2. Do the collection score floor and detection cap independently hide suitable
   candidates? Use their 2-by-2 factorial, with no image or NMS change.
3. How much does the AP evaluation floor alone affect the observed external AP
   when applied to the complete, existing prediction population?

Use all ten frozen checkpoints, retaining every adverse run. The diagnostic
cohort contains all 84 strict-positive images (95 boxes) and 84 uniformly
selected strict negatives, chosen once from sorted IDs using the configured
seed, without replacement. Selection does not use predictions. Report cohort
counts; keep identifiers and all image-level evidence private. The negative
sample is a background-control sample, not the full external population.
Its enriched positive frequency prohibits interpreting diagnostic-cohort AP,
precision or FP/image as the original population performance; do not report
such AP/precision. Negative-control FP/image is explicitly conditional on the
sample. No threshold tuning, target merging, training or checkpoint selection.

## Interventions fixed before new outcomes

The baseline collection floor/cap is 1e-5/100. The retention factorial compares
floors 1e-5 and 1e-6 with caps 100 and 300. Collect baseline and expanded
predictions with unchanged native NMS and precision. Derive lower-floor-only
and higher-cap-only arms from expanded score-ordered outputs. This is accepted
only if truncating expanded outputs to baseline reproduces actual baseline
outputs exactly on every diagnostic image/run. This validates the nested
postprocessing interpretation rather than assuming it. Stop on disagreement.

The window arm changes only the input display mapping. Apply the first header
WindowCenter/WindowWidth using pydicom's DICOM windowing, after modality
rescale, then map the defined display output range to uint8 and invert
MONOCHROME1. Missing window pairs use exactly the canonical pixels. Reject
unsupported LUTs, nonidentity rescale, non-unsigned storage or non-LINEAR VOI
functions; the existing metadata audit reports none. Retain native dimensions,
geometry, checkpoint, native resize, AMP, TF32 policy, NMS, floor and cap.
Use the same native file-loading boundary for baseline and windowed PNGs.
Validate synthetic window/polarity boundaries against pydicom and independently
recompute canonical pixels for every selected image before inference.

The original transform deliberately uses per-image min-max, not header
windowing. This test estimates the effect of the selected display mapping on
these outputs. Improvement would not prove that windowing caused the original
domain gap, nor establish a clinically correct vendor display or a deployable
new preprocessing policy. No choice among windows based on outcomes.

Primary technical references: [pydicom apply_windowing](https://pydicom.github.io/pydicom/stable/reference/generated/pydicom.pixels.apply_windowing.html)
and [DICOM VOI LUT Module](https://dicom.nema.org/medical/Dicom/2024c/output/chtml/part03/sect_C.11.2.html).

## Measurement and inference

First require exact baseline prediction replay for every selected image/run.
Keep the original source/checkpoint hashes and independently verified original
freeze. Measure historical-threshold strict recall and false positives among
the sampled strict negatives. Measure maximum one-to-one candidate coverage
at IoU 0.25 and 0.50 using bipartite matching; these are annotation-informed
geometric upper bounds, not achievable operating-point recall or AP.

Each arm uses its own declared cap/floor. Baseline comparisons use paired
images and the same checkpoint. Report all per-run values, equal-run means,
changes and marginal 95% percentile intervals. Use 2,000 bootstrap draws:
sample five runs with replacement within each detector, positive images with
replacement, and negative-control images separately with replacement. Use
the same draws across arms. Positive-image sampling keeps all boxes on an
image together. These intervals condition on the sampled diagnostic cohort,
five trained checkpoints and observed target definitions. They are not
simultaneous coverage or uncertainty over alternative training cohorts.
The factorial interaction is expanded - higher_cap - lower_floor + baseline.

The separate full-cohort CPU check recomputes COCO AP50 at the original
evaluation floor 0.001 and the saved collection floor 1e-5, with maxDets 100,
all 3,000 images, unchanged predictions and exact original AP reconciliation.
It isolates an evaluation-filter effect on saved output, not the root cause
of poor model scores. No external threshold is selected for deployment.

## Resource, integrity and reporting gates

Use the existing pinned CUDA environment, RTX 4060 Laptop, batch one and
mandatory detector-specific AMP. Time four images before full diagnostic
collection; refuse projected duration above the configured one-hour budget
or reserved CUDA memory above 7 GiB. Stream images and release each model.
Incomplete collections remain private; do not publish partial successful arms.
Freeze new source/config/protocol hashes before collection, verify them again
at completion, and refuse overwriting outputs. Existing scientific inputs must
remain unchanged. Save private prediction/selection/pixel/draw evidence and
public aggregates with hashes and reproducible commands. Verify analysis by
replaying saved predictions, without requiring duplicate GPU collection.

Annotation equivalence, acquisition/population differences, native proposals
discarded upstream of the tested controls and causal attribution of the total
domain gap remain unresolved. A null effect narrows the tested explanation;
it does not establish equivalence or prove another explanation true.
