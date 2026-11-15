# FROC annotation sensitivity: exploratory protocol v1

13 November 2026. This continues the user's request to investigate a useful
original contribution after the constrained-repairability NO-GO. It is written
before running the new analyses, after observing the original study. It is not
a preregistration or a claim that novelty has been established.

## Question and candidate contribution

How robust are an operating-budget conclusion, a between-detector ranking and
an internal-to-external sensitivity gap to a bounded number of reference-box
insertions/deletions? The previous geometric edit bound does not answer this
question for FROC: one edit can unlock a long score prefix at the FP budget.

Investigate a matching-aware certificate for the actual noninterpolated FROC,
with whole score ties, the original per-image cap, fixed predictions and the
canonical score-ordered best-available-reference matcher. Separate:

1. Universal conservative envelopes for unknown insertions/deletions.
2. Exact worst/best sensitivity over shared sets of one or two deleted existing
   references, rematching the affected image and reusing a sparse loss trace.
3. Sampling/run uncertainty of these functionals, distinct from annotation
   uncertainty. No edit budget is estimated or asserted clinically plausible.

The candidate method must add operational conclusions beyond the existing
geometric bound and bootstrap intervals. The primary literature comparison must
include WACV 2025 Noise-Aware Evaluation, annotation-agreement work and recent
incompleteness benchmarks, not just TIDE/OC-cost. No publication-level priority
claim is permitted based on a few unsuccessful keyword searches.

## Fixed evidence and analysis

Use both complete saved cohorts, both detectors, all five seeds and all five
original FP/image budgets. Preserve the original strict ontology, native NMS,
candidate floor, per-image caps, stable score/reference ties and matching IoU.
Replay the baseline against v2. No inference, model fitting or exported policy.

Compute universal envelopes for edit counts 0 through the configured maximum,
including insertions only, deletions only and unknown mixtures. References may
be inserted into previously negative images, but the image universe is fixed.
A box relocation or class change costs one deletion plus one insertion. The
surviving original references keep their relative tie order. No crowd/ignore
rules, retuned IoU, changed preprocessing or annotation-dependent NMS are allowed.
N=0 recall is undefined, not zero. For mixtures, optimize a common edit-type
allocation after averaging runs; do not give each seed unrelated annotations.

Enumerate every single/pair deletion on the observed reference set, using the
same deleted references for all runs and detectors. These are hypothetical
stress tests in memory, never corrected clinical labels. Publish aggregates
only. Exact shared-reference extrema can be compared with independent-seed
extrema to measure how much the latter exaggerate uncertainty. Do not claim
exactness for arbitrary insertions, larger deletion sets or box relocations.

Use the original internal patient clusters and external image units, independent
run resampling between detector families, and the same run multiplicities across
domains. Recompute the nonlinear envelopes in each of 2,000 joint draws. The
bootstrap edit budget counts edits to observation copies in each sampled cohort;
it is not a guarantee about editing one original image repeated many times.
Keep zero-reference draws undefined. Use marginal percentile intervals only,
and couple domain differences within each draw. No subtraction of separate CIs.

## Validation and decision

Prove the canonical greedy matching insertion/deletion lemma and the operational
envelopes. Test exhaustive small match/score/reference configurations, random
geometric examples, exact-deletion replay against full canonical rematching,
ties, empty predictions/references, zero FP budgets, cap preservation, negative
images, monotone scores, and the earlier FROC cliff counterexample. Include a
case where the same geometric counts give different annotation-sensitive FROC
conclusions. A solver agreeing with itself is not independent validation.

The analysis and generated outputs use a new namespace and hash receipts.
Record all exploratory design changes before freezing results. Preserve the
prior NO-GO research and frozen study evidence. Integrate a bounded contribution
into the manuscript only if mathematical correctness, implementation checks and
nonredundant empirical utility hold. A useful certificate still does not identify
clinical causes, establish label equivalence or guarantee journal acceptance.
