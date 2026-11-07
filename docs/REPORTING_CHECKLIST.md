# Publication readiness and CLAIM 2024 crosswalk

Current review: **6 November 2026**, against canonical `report/paper_draft.md`
and the rebuilt author-review PDF. This supersedes the dated primary crosswalk;
older secondary-framework discussion below is historical context. It is not a
compliance certificate, clinical validation, or journal submission approval.

The [official 44-item checklist](https://rsna.github.io/claim/checklist.html)
and [2024 publication](https://doi.org/10.1148/ryai.240300) were checked for this
review. Short topic labels below are navigation aids, not reproduced checklist
text. Use the publisher's exact form for submission. Yes denotes available
reporting evidence, not absence of methodological limitations. No identifies an
incomplete applicable item; NA explains an inapplicable item. Current page/line
locations are provided in the review verification record; final journal
pagination and author attestations must be reconfirmed.

## Author-only release gates

The subsequent threshold-repairability extension is documented in the
[v2 verification record](THRESHOLD_REPAIRABILITY_VERIFICATION_V2.md).
Methods 3.11, Results 4.12 and S13 add coupled uncertainty and controlled-output
evidence; no clinical adjudication, deployment evidence or author-only release
decision follows from that computational work.

| Gate | Current evidence | Decision and owner |
|---|---|---|
| Ethics and consent | Authors previously reported no separate institutional determination; source-study approval and consent waiver are described separately in Section 8. | Responsible authors must establish applicable institutional/journal requirements and retain any written determination. Do not invent exemption or retrospective approval. |
| Data-use compliance | Authorized local access and private-derivative boundaries are recorded; this review checks file exposure only. | Authors/data custodian must confirm current RSNA/NIH and VinDr/PhysioNet terms, permitted secondary use and reader access. A Git privacy scan is not a legal compliance determination. |
| Authorship and approval | Two named authors, affiliations, CRediT roles, funding/conflict and no-PPI facts were supplied previously. | Both authors must confirm contribution accuracy, accountability, final text and journal forms; consider any subsequent expert contributions without promising authorship. |
| Journal selection | No journal is selected. | Supervisor/authors choose fit for an empirical methods/transportability paper, then check scope, word/figure limits, supplement format, fees, AI-use disclosure and data/model-access policy. No journal acceptance is implied. |
| Final release | The repairability PDF pins evidence to pushed commit c29f863; its 22 pages and artifact bindings are verified. | Authors choose the exact final commit/archive and designate it after all accepted edits. No tag, archive, commit or push is created here. |
| Model access | All ten checkpoint binaries remain unpublished by the existing author decision, explicitly disclosed. | Authors decide whether the chosen journal accepts this restriction and whether an approved access mechanism is possible. Do not promise availability on request without a real process. |
| Expert study | Future adjudication protocol is specified, without approvals, recruited readers or reader results. | Clinical lead and authors must approve before executing it. Preserve overlap-only claims if it is not undertaken. |

## CLAIM 2024 primary crosswalk

All manuscript references below are to the current canonical paper; S1-S13 are
sections of [the supplementary index](SUPPLEMENTARY.md). The exact manuscript,
PDF hashes and verification outcomes are in
[the review record](SUPERVISOR_REVIEW_VERIFICATION_2026-11-06.md).

| Item | Topic | Response | Current evidence and remaining action |
|---:|---|---|---|
| 1 | AI identification | Yes | Abstract identifies deep-learning detection and both pipelines. |
| 2 | Abstract scope | Yes | Abstract reports retrospective design, cohorts, splits, runs, uncertainty, results, bounded conclusions and current access restrictions. Final journal length remains author action. |
| 3 | Rationale/use | Yes | Sections 1-2 and 5 state the research comparison and exclude diagnostic use. |
| 4 | Objectives/hypotheses | Yes | Section 1 states the scientific questions and distinguishes retrospective internal aims, locally frozen external settings and subsequent exploratory analyses. This is transparent aim/design reporting, not evidence that internal hypotheses were prospective. |
| 5 | Study timing | Yes | Abstract and Sections 1/8 identify retrospective secondary analysis. |
| 6 | Study goal | Yes | Sections 1 and 3.1 define object localization and methodological comparison. |
| 7 | Data provenance | Yes | Sections 3.1/3.5 identify RSNA/NIH and official VinDr test data and research-only applicability; S1/S9 bind provenance. |
| 8 | Eligibility/sampling | No | Section 3.1 reports deterministic hardware-scoped selection and 3.5 complete external inclusion. Detailed source accrual/clinical eligibility and local external clinical descriptors are unavailable. |
| 9 | Preprocessing | Yes | Sections 3.1/3.5 describe conversion/native transforms; 3.10 separates the exploratory display intervention. S1/S9/S12 retain exact settings. |
| 10 | Subset selection | Yes | Sections 3.1/3.8/3.10 and S1/S5/S6/S12 identify primary and secondary samples. Complete official external testing is distinct from the enriched diagnostic cohort. |
| 11 | De-identification | No | Section 8 cites de-identified source releases; complete upstream RSNA processes are not locally documented. Local private-file controls do not fill that gap. |
| 12 | Missingness | Yes | Section 3.1/Table 1 records available-field missingness and age caveats; Sections 3.3/3.6 state undefined-metric handling; absent clinical variables remain absent. |
| 13 | Acquisition | No | Section 6 discloses missing acquisition/processing history. Neither scanner-level comparability nor a clinical display pipeline is established. |
| 14 | Reference definition | No | Sections 3.1/3.5 specify released boxes and strict mapping, but complete original reader instructions and case-level adjudication details are unavailable. Future protocol approval is not present evidence. |
| 15 | Reference rationale | Yes | Sections 1/3.1/3.5/6 and S1 explain opacity-localization scope, dataset choice and reference limitations. |
| 16 | Reader provenance | No | Published source workflows are cited in Sections 2.2/3.5 and DATASHEET.md, but complete per-case original reader assignments/instructions are not reported. |
| 17 | Test annotation | No | Both test cohorts reuse source references; conversion is verified. Complete source annotation/display procedures for these subsets and a local independent rereading are unavailable. |
| 18 | Reader variability | No | No executed local inter/intrarater study. CLINICAL_ANNOTATION_ADJUDICATION_V1.md specifies future measurement only. |
| 19 | Partition allocation | Yes | Section 3.1/Table 1 and S1 give grouped RSNA allocation; Sections 3.5/4.6 give complete external inclusion without adaptation. |
| 20 | Partition independence | Yes | Section 3.1 documents internal patient grouping; 3.5/6 explicitly disclose unknown within-VinDr patient linkage. Reporting does not establish independent external patients. |
| 21 | Sample rationale | Yes | Section 3.1 reports the hardware-scoped sample and no formal power calculation; 3.5 reports the full official external set. Adequate power is not inferred. |
| 22 | Model definition | Yes | Sections 2.3/3.2 and S8 identify exact Faster R-CNN and YOLO11s implementations. |
| 23 | Software | Yes | Sections 3.2/3.7 and S8 record pinned environments and implementation settings. |
| 24 | Initialization | Yes | Section 3.2 states pretrained COCO initialization; configs/checkpoint manifests are linked in S8/S9. |
| 25 | Training | Yes | Section 3.2 records budgets, augmentation, optimizer/normalization/precision asymmetries and selection. Full configs are available. |
| 26 | Model selection | Yes | Sections 3.2-3.4 preserve validation checkpoint selection and all five runs; no external seed selection. |
| 27 | Ensemble | NA | Section 3.3 averages per-run metrics, not detections from an ensemble. |
| 28 | Metric choice | Yes | Sections 3.3-3.6/3.9-3.10 define metrics and scientific rationale for comparing two established pipelines. Section 2.2 supplies contextual prior comparisons while explaining why their published scores are not interchangeable. This does not reproduce their experiments. |
| 29 | Statistical methods | Yes | Sections 3.6/3.9/3.10 distinguish original intervals, later joint change intervals and paired diagnostic effects, with dependence and conditioning stated. Table 3's conditioning label is clarified. |
| 30 | Sensitivity | Yes | Sections 3.4/3.8-3.10 and 4.2/4.7-4.11 report completed sensitivities, all runs and finite support; S3-S6/S9-S12 give detail. |
| 31 | Explanation | Yes | Section 3.8 and S6 describe Grad-CAM targets and controls with an explicit noncausal/secondary scope. |
| 32 | Internal testing | Yes | Sections 3.1/3.3/4.1-4.4 and S1-S3/S7 document held-out patients and all runs. |
| 33 | External testing | Yes | Sections 3.5/4.6-4.8 and S9 report all official images/checkpoints and the non-identical reference task. |
| 34 | Trial registration | NA | Sections 1/8 describe retrospective computational research without a clinical intervention or participant enrollment. Local protocol freezing is not trial registration. |
| 35 | Cohort flow | No | Sections 3.1/4.6 and Table 1 disclose source, selected/excluded and split counts. A consolidated source-to-analysis flow diagram is still absent; this is a fixable presentation gap, not missing observations. |
| 36 | Case characteristics | No | Table 1 supplies limited internal header descriptors with caveats. External clinical/demographic characterization and many acquisition fields are unavailable. |
| 37 | Performance coverage | No | Sections 4.1-4.11 cover all retained runs and primary test endpoints; demographic/clinical subgroup performance is absent. Counts are not fairness evidence. |
| 38 | Diagnostic classification | NA | This study evaluates localization, not an exam-level diagnostic classifier. Detection uncertainty appears under 28/29/37; D-ECE is not clinical-risk calibration. |
| 39 | Error analysis | Yes | Sections 4.1/4.7/4.10/4.11 and S11/S12 report adverse runs, candidate categories, reference overlap and controls, without clinical relabeling. |
| 40 | Limitations | Yes | Section 6 states confounding, missing fields, few runs/positives, image dependence, selection/support and clinical boundaries. |
| 41 | Implications | Yes | Sections 5/7 frame an empirical transportability contribution and exclude deployment benefit/universal superiority. |
| 42 | Protocol access | Yes | S1-S12 and README identify frozen protocols, exploratory versions, code and provenance. Future adjudication is explicitly unexecuted. |
| 43 | Resource access | Yes | Abstract/Section 8 state public code/aggregates, licensed data, unpublished checkpoints and their consequences. The final immutable submission revision remains a separate author gate. |
| 44 | Funding | Yes | Section 8 states previously supplied no-external-funding/support facts; authors must reconfirm current disclosures. |

Item 43 now distinguishes completeness of the access statement from release
selection. Item 2 includes the added availability sentence. These reporting
changes do not mean checkpoint access improved or a final release was chosen.
This review treats items 4 and 28 as reporting checks: the aims and metric
comparison are explicit, while retrospective design and literature-score
noncomparability remain limitations. A Yes does not invent prospective
hypotheses or require another training campaign to reproduce every comparator.
See the official explanations for
[objectives](https://rsna.github.io/claim/item-04.html),
[metrics](https://rsna.github.io/claim/item-28.html),
[cohort flow](https://rsna.github.io/claim/item-35.html) and
[resource access](https://rsna.github.io/claim/item-43.html).

## Submission disposition

**Ready for supervisor/author scientific review; not cleared for submission.**
The PDF is current and technically reviewed when the linked execution record
reports completion. Authors should resolve the gates above, decide which
reporting gaps the journal will accept as disclosed limitations, supply the
final cohort-flow presentation, and complete the publisher's form against the
accepted paginated revision. No overall compliance percentage is calculated.
Clinical-adjudication conclusions and expanded-candidate results cannot be
included as if executed. Passing tests verifies implementation and provenance,
not medical truth, ethics approval or legal compliance.

## Preserved earlier context

The sections below preserve the earlier sample-size and secondary-framework
review. References to an earlier snapshot, source audit or unresolved flow
remain historical; the 44-item table and author gates above control this review.

## Required sample-size and subset-selection row

| Reporting point | Current disclosure | Consequence |
|---|---|---|
| Source, selected size, method, formal calculation, and generalizability | The source has 26,684 labeled studies. A deterministic, seed-17, SHA-256-ordered procedure selected 5,000 studies while tracking three label strata and keeping complete NIH patient groups together; it then assigned 3,500/750/750 studies to training/model optimization/internal testing. The other 21,684 studies were excluded for the stated 8-GB-VRAM laptop compute scope, not because they failed the annotation audit. **No formal statistical sample-size or power calculation existed.** Evidence: [`paper_draft.md` §3.1](../report/paper_draft.md#31-dataset-target-and-patient-disjoint-split), [`configs/dataset.yaml`](../configs/dataset.yaml), [`DATASET_CHOICE.md`](DATASET_CHOICE.md), and [`DATASHEET.md`](DATASHEET.md). | Determinism, stratification, and patient grouping support reproducibility and leakage control, but do not establish adequate power, prevalence representativeness, or equivalence to the complete challenge cohort. Sampling uncertainty is larger and generalizability is limited before any external-population shift is considered. |

## STARD-AI 2025 selected reporting crosswalk by analogy

The source is the **final version of record**, not the 2020 announcement or
2021 protocol: Sounderajah, Guni, Liu, et al., *The STARD-AI reporting guideline
for diagnostic accuracy studies using artificial intelligence*, *Nature
Medicine* 31, 3283--3289 (2025), DOI
[10.1038/s41591-025-03953-8](https://doi.org/10.1038/s41591-025-03953-8).
The final paper describes a minimum reporting set for AI-centered diagnostic
test-accuracy studies.

This manuscript is not sufficiently diagnostic-accuracy-centered for an
official STARD-AI completion: it does not define a participant-level index-test
result, clinical diagnostic target, diagnostic threshold, or 2-by-2 reference-
standard comparison. The following are selected useful concepts only.

| STARD-AI concept used by analogy | Current mapping | Boundary/gap |
|---|---|---|
| Data source, eligibility, sampling, and participant flow | [`paper_draft.md` §3.1](../report/paper_draft.md#31-dataset-target-and-patient-disjoint-split) reports source/split counts and partition-wise DICOM-header age, sex, and AP/PA projection. | Accrual dates, detailed eligibility, broader clinical/demographic variables, and a flow diagram remain unavailable. |
| Reference standard | Challenge bounding boxes are described in [`paper_draft.md` §§2--3.1](../report/paper_draft.md#31-dataset-target-and-patient-disjoint-split). | Boxes are object-localization annotations, not a participant-level clinical diagnosis; original reader instructions and local agreement assessment are unavailable. |
| Internal versus external testing | Patient-disjoint held-out evaluation is explicitly called internal testing in [`paper_draft.md` §3.3](../report/paper_draft.md#33-five-retained-runs-and-common-evaluation). | Frozen VinDr external testing is now reported in §§3.5 and 4.6--4.8; non-identical ontology and absent patient linkage limit interpretation. |
| Sample-size rationale | The dedicated row above reports the hardware-driven 5,000-study subset and absence of formal calculation. | This is not a diagnostic-accuracy power calculation. |
| Uncertainty, indeterminate outputs, and failures | [`paper_draft.md` §§3.6, 4.1, 4.4, and 4.6--4.8](../report/paper_draft.md#36-estimands-and-uncertainty) report intervals, the zero-detection YOLO run, and endpoint-specific undefinedness. | Multiple boxes/false positives and conditional localization do not reduce to one diagnostic result per participant. |
| Generalizability and clinical role | [`paper_draft.md` §§5--6](../report/paper_draft.md#5-discussion) explicitly limit use. | External testing is complete but confounds dataset, ontology and numerical differences. No diagnostic utility, prospective benefit or complete fairness assessment is established. |

## TRIPOD+AI 2024 selected reporting crosswalk by analogy

Source: Collins, Moons, Dhiman, et al., *TRIPOD+AI statement: updated guidance for
reporting clinical prediction models that use regression or machine learning
methods*, *BMJ* 385:e078378 (2024), DOI
[10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378).
TRIPOD+AI addresses development and evaluation of models that combine
predictors to estimate an individualized outcome. This study instead evaluates
object detections; it is not primarily a clinical prediction-model study.

| TRIPOD+AI concept used by analogy | Current mapping | Boundary/gap |
|---|---|---|
| Clear objectives and analysis populations | [`paper_draft.md` §§1 and 3.1](../report/paper_draft.md#31-dataset-target-and-patient-disjoint-split) states the comparison and partitions. | Hypotheses are retrospective, not preregistered. |
| Model specification and reproducibility | [`paper_draft.md` §§3.2--3.3](../report/paper_draft.md#32-detector-pipelines-and-controlled-training-factors), configs, source, and [`SUPPLEMENTARY.md`](SUPPLEMENTARY.md) record the pipelines. | Outputs are boxes/scores, not individualized diagnostic/prognostic probabilities. |
| Sample size and missing data | The dedicated row above reports the subset; annotation/conversion and age/sex/projection missingness audits are traceable. | No formal sample-size calculation exists, and uncollected broader clinical variables cannot be assessed or imputed. |
| Model performance and calibration | Detection metrics, uncertainty, and emitted-detection D-ECE are in [`paper_draft.md` §§3.3, 3.8, and 4](../report/paper_draft.md#33-five-retained-runs-and-common-evaluation). | D-ECE is not exam-level outcome-probability calibration; decision-curve analysis was correctly not performed. |
| Open science, declarations, and patient/public involvement | Code/config/artifact provenance is indexed in [`README.md`](../README.md) and [`SUPPLEMENTARY.md`](SUPPLEMENTARY.md). [`paper_draft.md` §8](../report/paper_draft.md#8-declarations) incorporates supplied funding/conflict/contribution/no-PPI facts. | No separate institutional ethics/consent determination exists. Applicable requirements and the exact public submission revision remain open. Initial-submission checkpoints stay unpublished by author decision. |

## Submission blockers and linked audits

- Resolve the ethics/consent and submission-version decisions stated in
  [`paper_draft.md` §8](../report/paper_draft.md#8-declarations) and tracked in
  [`AUTHOR_DECLARATIONS_TODO.md`](AUTHOR_DECLARATIONS_TODO.md).
- Use [`HYPOTHESIS_TRACEABILITY.md`](HYPOTHESIS_TRACEABILITY.md) to retain the historical
  H1--H6 provenance and endpoint/artifact bindings. These labels are no longer
  journal prose; this does not make the focused research question prospective.
- Use [`CITATION_AUDIT.md`](CITATION_AUDIT.md) for the current 19-key
  manuscript source audit and the explicitly archived broader source review.
- Re-complete the journal's official checklist after formatting the final
  submission. This crosswalk must not be submitted as proof of compliance.

## Authoritative guideline sources

- Ali S. Tejani, Michail E. Klontzas, Anthony A. Gatti, John T. Mongan,
  Linda Moy, Seong Ho Park, and Charles E. Kahn Jr., for the CLAIM 2024 Update
  Panel. *Checklist for Artificial Intelligence in Medical Imaging (CLAIM):
  2024 Update*. *Radiology: Artificial Intelligence* 6(4), e240300 (2024).
  DOI [10.1148/ryai.240300](https://doi.org/10.1148/ryai.240300); PMID 38809149.
- Viknesh Sounderajah, Ahmad Guni, Xiaoxuan Liu, et al., for the STARD-AI
  Steering Committee. *The STARD-AI reporting guideline for diagnostic
  accuracy studies using artificial intelligence*. *Nature Medicine* 31,
  3283--3289 (2025). DOI
  [10.1038/s41591-025-03953-8](https://doi.org/10.1038/s41591-025-03953-8);
  PMID 40954311. The publisher page includes the July 2026 author correction.
- Gary S. Collins, Karel G. M. Moons, Paula Dhiman, et al. *TRIPOD+AI statement: updated
  guidance for reporting clinical prediction models that use regression or
  machine learning methods*. *BMJ* 385:e078378 (2024). DOI
  [10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378).
