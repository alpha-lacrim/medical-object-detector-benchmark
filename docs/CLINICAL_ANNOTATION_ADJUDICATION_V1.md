# Clinical annotation-adjudication protocol v1

Date: 6 November 2026. **Specified for future expert review; NOT EXECUTED and
not clinically approved.** Detector outcomes were known when this document was
written. This is prospective specification of future reader observations,
not preregistration of the completed benchmark. The original source labels,
strict `Lung Opacity` mapping, predictions and reported metrics remain immutable.

## Purpose, hypotheses and decision boundary

Investigate whether source annotation concepts and lesion-instance boundaries
are sufficiently comparable to support a separately defined future opacity
task. The questions are whether strict-source boxes correspond to the agreed
radiographic construct, and whether overlaps with other localized categories
refer to the same finding, another finding, or an indeterminate relationship.
The hypothesis is that class-name agreement and spatial overlap alone do not
establish construct or instance equivalence. No direction or minimum magnitude
of metric improvement is an objective.

This is not a pneumonia-diagnosis study, reader-versus-AI competition, deployment
evaluation, relabeling of v1 or permission to compute merged-target AP. A future
alternative-reference evaluation would require its own approved protocol and
authorization after reference decisions are locked.

## People, permissions and pre-read lock

Appoint two independent, qualified radiologists experienced in adult chest
radiographs, at least one with thoracic specialization, and a third senior
radiologist for disagreements. Proposed minimum experience is five years of
independent practice; record actual qualifications, conflicts and prior exposure
to these datasets/results. A methodologist/data custodian manages masking and
provenance and cannot override clinical decisions. No reader identity or
qualification is assumed to have been secured.

Before case selection or reading, the clinical lead and both readers must sign
off the construct rubric, sampling, viewer, forms, ambiguity handling and
analysis plan. Authors must establish the applicable institutional/consent and
data-access conditions for the new reader activity; original data-collection
approval and a recorded DUA do not determine these requirements. Every reader
must have authorized access; no restricted image or identifier is sent to an
external service or placed in the public repository.

Freeze a dated protocol/config/form version and SHA-256 receipt before the first
study read. Store approvals privately. An amendment is versioned with rationale
and timing; changes after any study reads require explicit accounting and cannot
be represented as the original prespecified rule. No outcome-driven stopping.

## Construct workshop and rubric, before study images

Experts inspect the published RSNA/VinDr definitions, not detector examples,
and agree an operational radiographic opacity construct. For each released
localized category, record whether the wording could describe that construct,
why, and which distinctions require image-level review. Consider `Lung Opacity`,
`Consolidation`, `Infiltration`, `Atelectasis` and `ILD` individually. The latter
four are questions for assessment, not an approved merged class list. Exclude
global `Pneumonia` from localization; do not invent its boxes. Do not infer that
all ILD/atelectasis or every overlapping region is equivalent to an RSNA lesion.

For each assessed source region use: **compatible**, **incompatible**, or
**indeterminate**, plus an ungradable flag and reason. Record focal/diffuse or
multifocal pattern, uncertainty in boundaries, and whether a localized box is
an appropriate representation. Do not infer etiology or a clinical diagnosis
from the image alone. Experts must approve the actual rubric rather than being
asked to endorse categories as medically validated by this document.

Train the reader workflow on 20 authorized non-study practice cases, with no
overlap with the official external test cohort and no predictions. If suitable
cases are unavailable, postpone reading; do not silently use study cases for
rubric development. Record training feedback before the final protocol lock.

## Population and sampling

Sampling uses only frozen released annotations and image availability, never
detector scores, successes or failures. Partition all 3,000 official VinDr test
images into mutually exclusive strata, in the following priority order:

| Stratum | Definition | Prespecified allocation |
|---|---|---|
| A | At least one exact local `Lung Opacity` box | Census: all 84 images / 95 strict boxes |
| B | No strict box; at least one local box in Consolidation, Infiltration, Atelectasis or ILD | 80 images, or census if fewer are available |
| C | No A/B box; at least one other valid localized finding | 80 images, or census if fewer are available |
| D | No valid localized finding | 80 images, or census if fewer are available |

`No finding` sentinel rows and global labels are not local boxes. Keep all
other classes visible in the private annotation inventory; stratum priority
prevents double sampling. The maximum workload is 324 unique study images,
read twice independently, plus masked repeat reads. This is a bounded
exploratory audit, not a powered clinical-equivalence sample.

For each sampled stratum, order UTF-8 source image IDs by SHA-256 of the exact
string `adjudication-v1:20261106:<stratum>:<image_id>`; choose the first allocation,
breaking an impossible hash tie lexically by image ID. Freeze the complete
eligible counts, selected IDs, selection hashes and image hashes privately.
Replace source IDs with random review codes using a separately stored mapping.
Report aggregate stratum counts publicly. Selection is not executed in this
preparation task. Do not reuse the outcome-enriched diagnostic negatives as a
convenience sample.

If a selected image is corrupt, inaccessible or ungradable, retain it in the
flow and intended denominator; record the reason rather than replace it with a
more convenient case. Halt for integrity/access failures. An assessment of
VinDr alone cannot establish equivalence to RSNA image interpretation. The
workshop can compare definitions; a future cross-dataset reader study needs a
separate RSNA sampling plan before claiming empirical cross-dataset equivalence.

## Blinding and reading sequence

1. **Independent image review:** randomized order separately per reader;
   withhold stratum, source class/boxes, detector family, seed, confidence,
   prediction boxes, numerical results and the other reader's judgments.
   Readers mark findings under the agreed rubric and may mark no finding or
   ungradable. Lock this first-pass record before overlays are shown.
2. **Independent source-region review:** show every released localized region
   on each sampled image, in neutral styling with source class still hidden.
   Use fixed source-region units for compatibility ratings. Record completeness,
   extent/boundary uncertainty and a reader-assigned finding-instance ID; record
   relevant previously unmarked regions separately. Lock individual ratings.
3. **Adjudication:** disclose source category after independent records are
   locked. The third reader reviews discordant or indeterminate cases and the
   stated reasons. Retain both original ratings, the adjudicated judgment and
   rationale. If disagreement persists, keep indeterminate; never force agreement
   to enable a class merge. Source-category disclosure may influence this phase
   and must be reported.
4. **Prediction audit only after reference lock:** assess all
   historical-threshold detections from all five runs of each detector on the
   sampled images, as prespecified secondary work. Hide family, seed, score and
   strict TP/FP classification. Link exact duplicate marks to one display unit
   while preserving every original mark/run membership; do not collapse merely
   overlapping predictions. Source/reference decisions cannot be revised in
   response to predictions. No new inference, thresholds or diagnostic arms.

Source identity may be recognizable from acquisition appearance; report this
limitation rather than claim perfect masking. A coordinator audits accidental
unblinding. Readers do not receive the detector-comparison briefing until their
independent judgments and reference adjudication are locked.

Use an authorized local DICOM viewer with source pixel geometry and logging of
display operations. Agree the baseline rendering and permitted window/zoom
adjustments before reading, and capture viewer/version and settings. Do not
present either the benchmark min-max PNG or the tested first-header window as
validated clinical display processing. No image leaves the approved environment.

## Instance relations and duplicate annotations

For overlapping source regions, record **same finding**, **different findings**
or **uncertain**, with boundaries/diffuse involvement noted. Exact duplicate
rows are technical anomalies, reported without erasing the source. Different
class labels sharing a box are not automatically duplicates. IoU is an indexing
aid, not an expert-equivalence rule. Preserve many-to-one and one-to-many
relations in a private relational table; ambiguous relations remain unresolved.

The current task creates no deduplicated replacement reference. Any future
metric analysis must state whether it evaluates lesions, regions or images,
how instance relations define denominators, and how indeterminate cases affect
all reported results. It must retain the original strict metrics alongside a
separately named task. Do not use adjudication to remove difficult images.

## Outcomes and statistical plan

Primary outputs are the three-category compatibility counts/fractions for
strict source boxes in A, and independent-reader agreement on those fixed units.
Keep all 95 boxes in the intended denominator; report ungradable/missing
assessments separately and show complete-case denominators explicitly. Report
raw agreement, the full cross-tabulation and unweighted Cohen kappa where
defined, using jointly gradable, nonmissing reader pairs and explicitly reporting
that denominator. Missing/ungradable pairs are counted separately, never
classified as agreement. Indeterminate is a category, not an error or a negative. If kappa is
undefined under a degenerate marginal distribution, report NA with its reason.

Secondary outputs are stratum- and source-class-specific compatibility,
same/different/uncertain instance relations and the blinded mark audit.
Do not pool the enriched sample to estimate population prevalence, full-cohort
AP, clinical accuracy or the fraction of all strict false positives that is
clinically correct. A full-cohort estimate would require a separately declared
design-weighted estimand and appropriate sampling variance. The audit also
cannot estimate sensitivity to lesions that neither the source nor readers mark.

For descriptive uncertainty, use 2,000 image-cluster bootstrap draws within
each reviewed stratum, seed 20261106; carry all regions and both reader ratings
of an image together. These are marginal conditional case-resampling intervals,
not finite-population confidence intervals for the census in A, not uncertainty
over a population of radiologists, and not simultaneous guarantees. Record
undefined draws without retrying or zero imputation. Show counts even when an
interval is undefined. External image independence remains unverified.

Repeat ceil(10% of each stratum's selected images), chosen by a second fixed
hash prefix `adjudication-repeat-v1:20261106:`, after at least four weeks. Use
new masked codes and independent order, without access to original responses.
Report intrareader agreement separately; repeats are not additional cases.
No efficacy p-values, thresholds of "acceptable equivalence", data-dependent
class inclusion, multiplicity-adjusted discovery claims or model reranking.

## Records, quality checks and reporting

Private schemas must include protocol/form version, review code, source-region
key, reader ID, phase, timestamp, rating, ungradable/missing reason, instance
relations, certainty, display log and adjudication rationale. Every edit is
versioned; original independent entries remain read-only. Keep source IDs,
coordinates, images, per-image scores and reviewer correspondence under the
ignored restricted hierarchy. Export only reviewed nonidentifying aggregates.

Before analysis, check complete selected-image and source-region inventories,
valid category codes, phase ordering, missingness, locked references, repeat
mapping, and both readers' coverage. Report reader qualifications, actual
workload, departures, time separation, blinding limitations and disagreements.
Qualified experts must review interpretation before author publication approval.

Required signatures before execution: clinical lead; both readers; adjudicator;
data-access custodian; responsible authors. Dates, institutional determination,
actual reader names and approved viewer remain **unfilled author/expert decisions**.
The source definitions are documented in manuscript Sections 2.2, 2.4, 3.1 and
3.5 and the [frozen protocol](VINDR_EXTERNAL_PROTOCOL.md); this plan does not
replace those definitions or CLAIM reporting of an unperformed reader study.
