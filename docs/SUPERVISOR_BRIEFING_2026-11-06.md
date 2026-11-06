# Supervisor briefing: transportability evidence and publication decision

6 November 2026. Review baseline: `main`, `0b5e1dd4b7ff1cd94072ebc981d18c3cea2d9c2b`;
working tree initially clean. This briefing concerns the current canonical
[manuscript](../report/paper_draft.md), not the historical long report.

## Central contribution

The defensible contribution is an empirical demonstration that detector ranking,
absolute performance, transported operating thresholds and finite false-positive
frontiers answer different questions. Five retained runs per pipeline, shared
evaluation, explicit candidate limits and observation/run uncertainty make this
more informative than an accuracy/speed comparison. It contributes neither a
new detector nor a causal account of domain shift. Its external task also has a
different annotation ontology, and its training recipes are not interchangeable.

## What the evidence establishes

Execution status and scientific status are separate: a replayed exploratory
result remains exploratory. Software verification does not establish clinical
correctness. Exact commands and this review's outcomes are in the
[verification record](SUPERVISOR_REVIEW_VERIFICATION_2026-11-06.md).

| Evidence status | Finding | Meaning and boundary |
|---|---|---|
| VERIFIED frozen study | Mean AP50: Faster R-CNN 0.304224 to 0.002505; YOLO11s 0.162612 to 0.000501. Historical recall: 0.350746/0.194776 to 0.018947/0.004211. | Observed AP ordering survives severe absolute failure. This does not establish useful clinical performance. Sources: manuscript Tables 5-6 and [transport table](../results/vindr_external_v1/statistics/transport_comparison.csv). |
| VERIFIED uncertainty | External AP contrast intervals are positive; historical operating-point contrast intervals contain zero. The post-hoc difference in FROC degradation also contains zero. | Conclusions depend on endpoint and estimand. Intervals are marginal, conditional on five retained runs and fixed training data; external patient dependence is unknown. Sources: Tables 5-8. |
| EXPLORATORY, replayed | Below-threshold compatible candidates account for 54.95%/17.68% of strict boxes; absent retained IoU-0.25 candidates account for 18.11%/60.21%. | Different observable failure profiles, not explanations of hidden proposal failure. Source: [generalization interpretation](POSTHOC_EXTERNAL_GENERALIZATION_INTERPRETATION.md), with bound per-run tables. |
| EXPLORATORY, replayed | Other local annotations overlap 53.656%/37.795% of historical strict false positives in defined run populations. Prevalence-weighted internal AP50 remains 0.108684/0.055072. | Annotation overlap is not clinical validation; custom weighted AP neither reproduces external performance nor assigns a causal fraction to prevalence. The zero-emission run remains included. |
| EXPLORATORY, replayed | YOLO geometric coverage rises from 0.181053 to 0.324211 under the lower floor; historical recall is unchanged under all retention arms. Header-window recall change intervals include zero. | Collection affects retained geometry. Geometry is not score-ranked recall, and inconclusive window effects do not establish equivalence. Source: [complete controlled results](EXTERNAL_FAILURE_ISOLATION_RESULTS_V1.md). |

## Decisions for the supervisor

**Recommend proceeding to substantive author review of a methods/transportability
paper, with a NO-GO for full-cohort expanded-candidate inference at present.**
The current claims expressly condition on retained support. A larger collection
could resolve selected FROC/false-positive questions, but it would not adjudicate
labels or identify the total domain-gap cause. The [scientific review](SUPERVISOR_SCIENTIFIC_REVIEW_2026-11-06.md)
gives the decision rationale and conditions for reconsideration.

Prioritize expert scrutiny of the opacity construct over additional performance
curves. The [annotation-adjudication protocol](CLINICAL_ANNOTATION_ADJUDICATION_V1.md)
is specified for future independent reads, with predictions withheld until
reference assessments are locked. No reader has approved or executed it. A
review could support a future separate annotation-sensitivity task; it cannot
retroactively validate a merged target or replace the frozen study.

## Publication barriers

The available analysis can support the bounded paper without a new experiment.
It cannot support clinical utility, architecture-family superiority, an
unrestricted FROC ordering or a complete causal explanation. Expert review is
required if authors wish to go beyond descriptive annotation overlap; it is not
to be represented as completed evidence in the present paper.

Before submission, authors must resolve institutional ethics/consent
applicability and data-use conditions; both authors must approve contributions,
disclosures and the final text; a journal and immutable submission release must
be designated. The decision to withhold checkpoints is disclosed and limits
independent exact-model reproduction. Missing acquisition/clinical descriptors,
limited external positives and unknown external patient linkage must remain
limitations. The rebuilt PDF is an author-review derivative, not submission
clearance. See the current [CLAIM 2024 readiness crosswalk](REPORTING_CHECKLIST.md).
