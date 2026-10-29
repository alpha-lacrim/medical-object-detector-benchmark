# Post-hoc external generalization protocol v1

Written 2026-10-28 before computing the new outcome-dependent summaries.
The original external outcomes were already known. This is exploratory work,
not preregistration. Baseline: `801a6c90afa480351a9e0d72ca7709b47da95e2e`.
The original 38-file freeze, checkpoints, bundles, primary thresholds and
scientific inventory remain unchanged. Configuration:
`configs/external_generalization_v1.yaml`. No training or new inference.

## Inputs and common contracts

Use the hash-gated Batch 50 loader and its canonical point replay, including
the explicit archived-editorial read context. Internal AP/operating points
use original Phase 5 bundles; internal FROC uses Batch 42 lower-floor bundles.
External endpoints use original Batch 49 bundles. Compare the complete five
run identities within each detector across domains. All official images stay.
Original coordinates, single canonical class, native NMS/caps, >= threshold
and >= IoU boundaries, stable score order and canonical `match_image` apply.
COCO AP retains official COCO matching, which has its own target-tie rule;
error decomposition uses the operating-point matcher, not a surrogate AP.

Only exact local `Lung Opacity` remains a reference target. Source CSV hashes
must match v1. Rebuild strict targets from source and compare every coordinate
and image to the canonical COCO file. Validate all localized annotation
geometry and duplicate same-class rows. Cross-class coincident boxes are
allowed but flagged and never summed into an alternative target population.
Global labels never generate boxes. Restricted identifiers/rows never appear
in public outputs. Private bootstrap arrays stay in the ignored hierarchy.

Implementation clarification (2026-10-29, before new outcome calculations):
the canonical loader uses PNG filenames; source annotation identifiers omit
the `.png` suffix. The explicit configured suffix follows the frozen adapter.
The source box CSV also contains `No finding` sentinel rows with missing box
coordinates. Validate these separately, reject duplicate/conflicting sentinels,
and exclude them from local-box geometry, overlap and object counts. Other
global diagnoses cannot supply boxes. This corrects the draft loader only;
the historical adapter/evaluations are unaffected.

## RQ1: observable external error structure

Each reference box receives exactly one category, in this order:

1. `matched`: canonical match at the historical threshold.
2. `high_score_assignment`: unmatched, but at least one retained candidate
   with score >= historical threshold and IoU >= canonical match IoU exists.
   This includes competition for another target, not necessarily a bug.
3. `below_threshold`: no such high-score candidate, but a retained candidate
   has IoU >= canonical match IoU. Availability is not a promise of a match.
4. `partial_localization`: no compatible candidate; best retained IoU >=0.25.
5. `no_relevant_retained`: best IoU <0.25, including empty predictions.

Counts must sum to the reference count separately for every run. Secondary
overlapping flags describe availability at IoU 0.25/0.50/0.75; best-IoU and
matchable/unmatchable candidate-score quantiles use linear interpolation.
Candidate availability is an upper envelope ignoring assignment competition.
Missing retained candidates do not establish missing pre-NMS/proposal output.

For each unmatched prediction, separately at the historical threshold and
full retained support, use exclusive precedence:

1. `claimed_strict_target`: IoU >=0.50 with a strict target already matched.
2. `other_local_finding`: IoU >=0.50 with any non-target local annotation.
3. `ambiguous_partial`: no preceding match, but IoU >=0.25 with any local box.
4. `no_local_overlap`: none of these conditions.

Ambiguous here is an operational geometric category, not a radiologist's
judgment. Report overlapping flags for every source non-target local class,
including Consolidation, Infiltration, Atelectasis and ILD. Each flag counts
a prediction once per class regardless of overlapping/duplicate cross-class
boxes. Denominator is all strict FPs on that run/support; zero FP gives an
undefined proportion, not zero. No overlapping FP becomes a TP.
All summaries first operate per run; detector summaries are equal-run means
and sample SD with defined/attempted counts, never pooled detections.

## RQ2: ontology sensitivity and expert gate

The executable sensitivity is non-target overlap accounting, preserving the
reference ontology. Candidate broader scenario: exact `Lung Opacity`,
`Consolidation`, `Infiltration`. These are separate localized radiographic
findings in VinDr; the rationale for considering them is possible overlap
with the broader pneumonia-like RSNA annotation concept, not validated
equivalence. Atelectasis/ILD and all other local/global labels are excluded
from that proposed task because they denote distinct patterns/conditions.
The release documentation alone cannot determine lesion-instance equivalence
or a clinically justified cross-class deduplication rule. Therefore no merged
AP is executed. Expert review must define instance reconciliation before any
broader task, including exact cross-class duplicates and partly overlapping
boxes. Such a task would be substantively different and cannot replace strict
AP even after review. Overlap describes numerical sensitivity of FP accounting;
it does not quantify corrected clinical accuracy or a causal annotation effect.

## RQ3: population weighting sensitivity

Hold internal detections, annotations, thresholds and within-stratum case mix
fixed. Let p be internal positive-image frequency and q the observed external
strict-positive frequency. Assign image weights q/p to positive images and
(1-q)/(1-p) to negatives. This decreases positive weight; removing negatives
would increase prevalence. Every target and detection inherits its image weight.
Report custom weighted AP50 and historical precision, plus unweighted values,
weighted recall (unchanged by construction) and Kish image-weight effective
sample size as a concentration diagnostic, not independent patient count.

Weighted AP50 uses cached official COCO per-image IoU-0.50 matches at the
original AP floor/cap. Stable global score order is retained. Cumulate weighted
TP/FP masses at detection events, take the reverse precision envelope and
sample at the configured 101 recall positions, with zero beyond achieved
recall. This is a custom weighted interpolated AP, **not official COCO AP**.
Unit weights must reproduce canonical AP; small analytical fixtures test
non-unit weights. No image is represented as a newly independent patient.

Uncertainty uses the internal patient/run draws below, re-estimating p within
each draw and holding q fixed at its observed value. Draws lacking either
stratum are undefined without retry. Report original/weighted estimates and
paired changes, marginal intervals and valid/undefined draws. These intervals
condition on q and cannot identify a causal prevalence effect. Changes in
appearance, acquisition, annotation and other population factors remain.

## RQ4: cross-domain changes

Endpoints: AP50 (cross-ontology descriptive), observed FROC sensitivity at
0.25 FP/image, historical-threshold recall. For each detector compute
VinDr minus RSNA; the contrast of changes is Faster R-CNN minus YOLO11s.
Use absolute changes. Use 2,000 deterministic draws, base seed 20261028 and
analysis-ID-derived RNG. Within a draw sample internal known patient clusters
and external released images independently; each dataset's observation draw
is shared across both detectors and all runs. Independently sample trained
runs within detector, **reuse exactly those multiplicities across domains**.
Same-number seeds across detector families are not paired. Recompute cohort
metrics, then average selected runs. Undefined selected values propagate.
Report marginal percentile 95% intervals and valid/undefined counts; no
simultaneous inference, p-values or new-training-dataset uncertainty.
Record floor-limited contributions at the chosen budget in bootstrap draws.
Unknown repeated external patients can narrow intervals improperly.

## RQ5: candidate support

Recompute per-run floor, minimum retained score, maximum FP/image, cap count
and fraction, all frozen budget support flags and observed sensitivities.
Verify canonical source agreement. Reproduce conservative mean bounds by
replacing only a limited run's sensitivity with 1; these are missing-support
bounds, not confidence intervals and do not repair cap saturation.

If extra collection is warranted, propose separately named post-hoc v2:
candidate floor 0.000001 and cap 300 on all ten checkpoints and both complete
cohorts, retaining all other v1 choices. These prospective proposal values
are not selected from new outcomes. Cost requires a bounded GPU timing/memory
gate on the 8GB RTX 4060 and authorized data; larger bundles stay private.
Selection after known results remains a limitation. **Not authorized here**:
the current request requires separate authorization for new inference.

## Outputs and verification

Nonidentifying per-run/category/overlap/score/support/prevalence tables,
equal-run summaries, cross-domain intervals and figures; a source-bound JSON
summary and private draw archive; reproducible preflight/run/verify/replay CLI.
Run refuses existing output. Verify checks hashes and reconstructs intervals
from saved draws; replay recomputes the analysis from original bundles.
Tests cover matching boundaries/ties/competition, empty/negative inputs,
invalid/duplicate annotations, weighting, shared checkpoint resampling,
patient multiplicities, undefined draws and reconciliation. Historical tests
remain unchanged. Manuscript additions describe only executed evidence.
