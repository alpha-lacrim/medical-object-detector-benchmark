# Supervisor briefing: transportability evidence and publication decision

6 November 2026. Review baseline: `main`, `0b5e1dd4b7ff1cd94072ebc981d18c3cea2d9c2b`;
working tree initially clean. This briefing concerns the current canonical
[manuscript](../report/paper_draft.md), not the historical long report.
Follow-up review at `85269e5` checked the completed diagnostic, refreshed PDF
and pushed review package before refining the answers below. No new experiment
is represented by this update.

## Direct answers to the professor's four requests

**Ready for reassessment; the analysis does not establish a complete causal
explanation or clinical equivalence of the two reference standards.**

| Request | Current answer | What remains open |
|---|---|---|
| Explain the external collapse | Partly addressed by measured failure categories and controlled retention/display tests. More retained low-score boxes did not improve recall at the original operating thresholds; relaxing the AP evaluation filter left absolute AP very low. | The tested controls narrow particular implementation explanations. They do not partition the total loss among annotation, acquisition, population, training or other pipeline differences. |
| Clarify label mapping and evaluation | Addressed at the implementation/protocol level: exact local-label mapping, native coordinates, common evaluator, all official test images and frozen RSNA-selected thresholds. Details below. | Matching class IDs does not establish that RSNA and VinDr boxes represent the same clinical construct or lesion instances. Expert review is specified but unexecuted. |
| Establish statistical stability | Quantified across all five runs per detector and resampled observations. Severe degradation is supported; the AP contrast and historical-threshold contrasts have different uncertainty conclusions. | Five runs, few positive external images, unavailable external patient linkage and marginal intervals limit generalization. A reproducible result is not automatically a precise or confirmatory result. |
| Define the scientific contribution | A focused empirical transportability study separating detector ranking, absolute performance, transported thresholds and finite candidate support, with paired uncertainty and bounded failure diagnostics. | This is not a new detector or proof of a new causal mechanism. The professor and authors must judge whether the evidence and positioning meet a journal's contribution threshold. |

## Central contribution

**Research question:** When fixed RSNA-trained pipelines are transported to
VinDr's strict opacity target, do relative detector rankings, absolute detection
performance and validation-selected operating rules remain consistent, and
which observed failure patterns change under specified implementation controls?

The defensible contribution is an empirical demonstration that detector ranking,
absolute performance, transported operating thresholds and finite false-positive
frontiers answer different questions. Five retained runs per pipeline, shared
evaluation, explicit candidate limits and observation/run uncertainty make this
more informative than an accuracy/speed comparison. It contributes neither a
new detector nor a causal account of domain shift. Its external task also has a
different annotation ontology, and its training recipes are not interchangeable.

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
work plan. A [proposed computational focus](THRESHOLD_REPAIRABILITY_RESEARCH_DIRECTION.md)
asks what a confidence cutoff can and cannot repair within a fixed FP budget.
It includes an executed public-table feasibility analysis and a Persian pitch.
The potential contribution needs further joint uncertainty/controlled-output
validation and comparison with existing methods; novelty is not established by
the new framing. The current manuscript has not been replaced by this proposal.

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

استاد گرامی، بر اساس نکات شما، تحلیل‌های تکمیلی انجام شده و متن مقاله و نسخهٔ
PDF به‌روز شده‌اند. پرسش اصلی اکنون این است که آیا حفظ رتبهٔ نسبی دو مدل روی
دیتاست خارجی با حفظ عملکرد واقعی و اعتبار آستانه‌های انتخاب‌شده روی دیتاست
داخلی همراه است یا خیر. نتایج نشان می‌دهند این موارد لزوماً همراه نیستند.

برای بررسی افت عملکرد، الگوهای خطا را تفکیک کردیم و اثر حداقل امتیاز ذخیرهٔ
پیش‌بینی‌ها، سقف تعداد کادرها و یک روش مشخص نمایش تصویر را به‌صورت کنترل‌شده
بررسی کردیم. افزایش کادرهای کم‌امتیاز، حساسیت را در آستانه‌های اصلی بهبود نداد؛
کاهش فیلتر ارزیابی نیز عملکرد خارجی را به سطح داخلی برنگرداند. بنابراین برخی
توضیحات فنی محدودتر شده‌اند، اما هنوز نمی‌توان علت کل افت یا سهم هر عامل را
به‌طور علّی تعیین کرد.

تطبیق برچسب‌ها و پروتکل ارزیابی اکنون صریح و قابل بازبینی است: فقط کادرهای
دارای برچسب محلی دقیق «Lung Opacity» هدف هستند، سایر یافته‌ها ادغام نشده‌اند و
آستانه‌ها با دادهٔ خارجی تنظیم نشده‌اند. بااین‌حال، برابری بالینی تعریف ضایعه
در دو دیتاست اثبات نشده است. برای بررسی این مسئله پروتکل داوری متخصص تهیه
شده، ولی این داوری هنوز اجرا نشده است.

پایداری نتایج با حفظ هر پنج اجرای هر مدل و تحلیل عدم‌قطعیت بررسی شده است.
افت شدید عملکرد پشتیبانی آماری دارد، اما برتری بین مدل‌ها به شاخص ارزیابی
وابسته است و همهٔ اختلاف‌ها قطعی نیستند. سهم علمی پیشنهادی، یک مطالعهٔ تجربی
و بازتولیدپذیر دربارهٔ تعمیم‌پذیری و محدودیت‌های ارزیابی است؛ ادعای معماری جدید
یا توضیح کامل علل شکست نداریم. شواهد برای بازبینی مجدد شما آماده است؛ کفایت
نوآوری و انتخاب مجله همچنان نیازمند قضاوت علمی شما و تصمیم نویسندگان است.
