# Supervisor briefing: transportability evidence and publication decision

6 November 2026. Review baseline: `main`, `0b5e1dd4b7ff1cd94072ebc981d18c3cea2d9c2b`;
working tree initially clean. This briefing concerns the current canonical
[manuscript](../report/paper_draft.md), not the historical long report.
Follow-up review at `85269e5` checked the completed diagnostic, refreshed PDF
and pushed review package before refining the answers below. The subsequent
threshold-repairability v2 update adds an executed CPU analysis and controlled
changes to copies of saved outputs; it runs no new model inference.

## Direct answers to the professor's four requests

**Ready for reassessment; the analysis does not establish a complete causal
explanation or clinical equivalence of the two reference standards.**

| Request | Current answer | What remains open |
|---|---|---|
| Explain the external collapse | Now bounded more directly: changing a global cutoff alone cannot restore recall under a fixed FP budget. Internal/external geometric coverage and controlled output changes distinguish score-order limitations from missing retained geometry. | This isolates limits of proposed computational repairs, not the medical or dataset mechanisms that produced the errors. Annotation, acquisition, population and training effects remain confounded. |
| Clarify label mapping and evaluation | Addressed at the implementation/protocol level: exact local-label mapping, native coordinates, common evaluator, all official test images and frozen RSNA-selected thresholds. Details below. | Matching class IDs does not establish that RSNA and VinDr boxes represent the same clinical construct or lesion instances. Expert review is specified but unexecuted. |
| Establish statistical stability | Joint 2,000-draw uncertainty now covers repairability components and paired domain changes, sharing observations and reusing the same checkpoints across domains. Both geometric losses have negative intervals. | Five runs, few positive external images, unavailable external patient linkage and marginal intervals limit generalization. The between-detector difference in cutoff-ceiling loss still includes zero. |
| Define the scientific contribution | A reproducible audit of which failures global confidence-cutoff repair can and cannot address, combining full-cohort bounds, maximum matching, coupled uncertainty and controlled output checks. | FROC and error diagnostics already exist. This is an empirical diagnostic contribution, not a new detector, theorem, clinical cause or demonstrated improvement over TIDE/LRP. |

## Central contribution

**Research question:** After external detection failure, how much recall can a
global confidence cutoff recover under a fixed false-positive budget, and how
much remains limited by score ordering or unavailable retained geometry?

The completed computational audit answers this on both full saved cohorts.
At 0.25 FP/image, even an optimistic per-run cutoff reaches only 8.63% / 3.37%
external recall for Faster R-CNN / YOLO11s. Missing retained geometry accounts
for 43.16% / 81.89% of external reference boxes, compared with 2.69% / 21.42%
internally. Score-power controls leave whole frontiers unchanged; reranking can
change budget recall without changing geometry; annotation-informed removals
separate these limits. All 580 imposed interventions and 2,000 joint draws
are reported, without selecting favorable arms. See the
[complete v2 results](THRESHOLD_REPAIRABILITY_RESULTS_V2.md).

These are limits within original retained candidates and source labels, not
causal percentages of the external loss. Missing geometry may still depend on
floor, cap, NMS, localisation and reference definition. No radiologist access
is assumed. Publication novelty must be judged against existing FROC, TIDE,
LRP and calibration research; the paper now states its incremental scope.

## Label mapping and evaluation, in concrete terms

Only the exact local VinDr box label `Lung Opacity` is a target. It maps to
canonical category 1, Faster R-CNN foreground 1 and YOLO foreground 0. These
numeric IDs are adapter conventions, not a claim of clinical equivalence.
Consolidation, Infiltration, Atelectasis and ILD are not merged; global Pneumonia
labels do not become boxes. An image without a strict-target box remains a
strict-target negative even if it contains another finding. Consequently,
overlap with another annotated finding can still count as a strict false
positive; it cannot be called a clinically incorrect detection without review.

All 3,000 official external test images are retained, including 84 strict-positive
images with 95 boxes. Coordinates are restored to native image space. AP uses
the shared COCO evaluator; historical operating metrics use score-ordered
one-to-one matching at IoU 0.50. The original validation-selected cutoffs
(0.69 for Faster R-CNN and 0.05 for YOLO11s) were transported without selection
on external labels. The later diagnostic is explicitly exploratory and does
not replace those primary results. The [frozen protocol](VINDR_EXTERNAL_PROTOCOL.md#3-population-and-strict-target-ontology)
and [machine-readable contract](../configs/vindr_external_v1.yaml) specify these
rules. The experiment tests transport across both datasets and annotation
definitions; it does not isolate a change of hospital under an identical task.

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

The controlled diagnostic includes every strict-positive image and a fixed
random sample of 84 strict negatives. Its negative-sample false-positive rate
is not the whole-cohort rate. Lowering the AP evaluation filter is a separate
saved-output control on all 3,000 images; it is not new candidate collection
or external threshold tuning. The [protocol](EXTERNAL_FAILURE_ISOLATION_V1.md)
specifies the floors, caps and window intervention; the
[full results](EXTERNAL_FAILURE_ISOLATION_RESULTS_V1.md) retain all outcomes,
including unchanged results.

Statistical support should be stated by endpoint: the cross-domain-change
analysis supports substantial deterioration for both pipelines, while the
between-detector difference in FROC deterioration remains uncertain. Shared
observations and the same checkpoint across domains are coupled in the change
bootstrap; the two detector families' runs are sampled independently. The
paired diagnostic uses the same image/run draws across its intervention arms.
These intervals condition on the existing training data and runs. They neither
cover unknown external patient clustering nor establish simultaneous claims
across all exploratory comparisons. No post-hoc result becomes confirmatory
because its computation was replayed exactly.

## Decisions for the supervisor

**Follow-up constraint:** the user reports no access to radiologists. Expert
adjudication therefore remains an unresolved evidence gap, not the immediate
work plan. The [computational focus](THRESHOLD_REPAIRABILITY_RESEARCH_DIRECTION.md)
has now been implemented with internal comparison, joint uncertainty and
controlled outputs. Methods 3.11, Results 4.12, Table 9, Figure 5 and S13
incorporate the evidence. Novelty is not established merely by this framing.

**Recommend proceeding to substantive author review of a methods/transportability
paper, with a NO-GO for full-cohort expanded-candidate inference at present.**
The current claims expressly condition on retained support. A larger collection
could resolve selected FROC/false-positive questions, but it would not adjudicate
labels or identify the total domain-gap cause. The [scientific review](SUPERVISOR_SCIENTIFIC_REVIEW_2026-11-06.md)
gives the decision rationale and conditions for reconsideration.

Expert scrutiny of the opacity construct would be needed to support a broader
ontology claim. The [annotation-adjudication protocol](CLINICAL_ANNOTATION_ADJUDICATION_V1.md)
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

## Suggested reply in Persian

استاد گرامی، بر اساس نکات شما، تمرکز مقاله را مشخص‌تر کرده‌ایم: آیا افت عملکرد
خارجی با تغییر آستانهٔ اطمینان قابل جبران است، یا محدودیت در رتبه‌بندی و جعبه‌های
باقی‌مانده اجازهٔ این جبران را نمی‌دهد؟ این تحلیل اکنون روی هر دو مجموعه و تمام
اجراهای اصلی انجام شده، همراه با بازنمونه‌گیری مشترک برای عدم‌قطعیت و آزمون‌های
کنترل‌شده روی خروجی‌های ذخیره‌شده.

در بودجهٔ ۰٫۲۵ مثبت کاذب به ازای هر تصویر، حتی بهترین آستانهٔ ممکن روی خروجی‌های
موجود فقط حدود ۸٫۶٪ و ۳٫۴٪ از ضایعات مرجع خارجی را برای Faster R-CNN و YOLO11s
بازیابی می‌کند. برای حدود ۴۳٪ و ۸۲٪ از ضایعات مرجع خارجی نیز جعبهٔ باقی‌مانده با
هم‌پوشانی کافی وجود ندارد؛ این محدودیت نسبت به مجموعهٔ داخلی بسیار شدیدتر است.
بنابراین مشکل صرفاً انتخاب نامناسب آستانه نیست. البته این اعداد سهم علّی عوامل
بالینی، جمعیتی یا تفاوت برچسب‌گذاری را تعیین نمی‌کنند.

نگاشت دقیق برچسب‌ها و پروتکل ارزیابی حفظ شده و عدم‌قطعیت مؤلفه‌ها و تغییرات بین
دو مجموعه گزارش شده است. سهم علمی پیشنهادی، یک تحلیل تجربی و بازتولیدپذیر از
محدودیت‌های اصلاح با آستانه است، نه معماری جدید یا قضیهٔ ریاضی جدید. بدون بازخوانی
رادیولوژی نیز ادعای هم‌ارزی بالینی دو تعریف برچسب نداریم. اکنون شواهد برای ارزیابی
این سهم مشخص‌تر است؛ کفایت نوآوری برای مقاله همچنان نیازمند نظر علمی شماست.
