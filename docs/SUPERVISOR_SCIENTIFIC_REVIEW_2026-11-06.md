# Scientific review and gap assessment

6 November 2026; baseline `0b5e1dd`. Reviewed canonical manuscript, S1-S12
index, frozen external protocols/results, generalization and controlled-diagnostic
tables, prior verification records, claim bindings and publication inventories.
This is scientific/editorial review of existing evidence; no new experiments.

## Findings and justified corrections

| Priority | Location and issue | Disposition |
|---|---|---|
| High | Sections 3.5, 4.8 and 4.10 used blanket statements about no later floor/preprocessing changes although 3.10/4.11 describe separate exploratory interventions. | Scoped the prohibition and unchanged floor/cap to the original frozen analysis; explicitly separated the later diagnostic. No original settings or results changed. |
| High | Section 4.10 described other-label overlap as evidence of reference-definition sensitivity, which could suggest that an alternative ontology's performance had been evaluated. | Replaced with a precise statement of disagreement with the strict definition. No expert-adjudicated alternative task has been scored. |
| Medium | Table 3 says "Unconditional", while intervals condition on fixed training data, recipes, thresholds and support. | Added a local explanation: this label only removes conditioning on a matched detection. Preserved the numeric table and its bindings. |
| Medium | Discussion could suggest numerical-path harmonization apportions a causal fraction of the collapse. | Described the observed magnitude of the tested change; retained the explicit inability to assign the remaining gap to a dataset factor. |
| Medium | Abstract omitted the latest controlled diagnostic and access restrictions. | Added the tested-control scope and public code/aggregate versus restricted-data/unpublished-checkpoint availability. |
| Medium | The PDF support revision predates S12, while the current manuscript cites S12. | Updated the build pin to the existing committed diagnostic evidence, rebuilt the canonical PDF, and checked source/output hashes and link targets. This pin is not a final submission release. |
| Medium | Checklist/PDF prose and current manuscript pointers mixed historical and current snapshots. | Refreshed the current crosswalk and entry points; dated historical audits remain historical. |

No new causal, novelty or clinical-effect claim is supported. Existing strengths
include the explicit absence of public preregistration, preservation of adverse
runs, fixed historical thresholds, target-ontology mismatch, independent
between-detector run resampling and checkpoint coupling across domains.

## Statistical and methodological distinctions that must survive editing

- Clinical correctness is not established by exact replay, source hashes, unit
  tests, reference overlap, geometric coverage or matched-box IoU.
- Canonical operating metrics use score-ordered one-to-one matching. Per-box
  candidate availability ignores competition. The controlled diagnostic's
  bipartite maximum-cardinality coverage is an annotation-informed geometric
  ceiling. These are three different quantities.
- The original three-run validation threshold policy remains primary. The
  five-run validation policy is post-hoc; neither was selected on VinDr labels.
- AP evaluation filtering, the native collection floor and detection cap are
  different controls. Lowering an evaluation filter on saved outputs cannot
  retrieve candidates absent from the collection.
- Population weighting holds internal conditional case mix fixed. Its custom
  AP is not official COCO AP, and an arithmetic change is not a prevalence
  contribution to the causal domain gap.
- Difference-in-change intervals share a checkpoint across domains and sample
  detector families independently. They are not differences of confidence
  limits. Larger absolute loss from a higher baseline does not rank inherent
  robustness. Marginal intervals and selected endpoint contrasts do not support
  a simultaneous ordering or a multiple-testing-adjusted discovery claim.
- Original patient/run intervals, checkpoint-conditional permutation p-values,
  technical timing repeats and paired diagnostic-arm intervals answer different
  questions. Zero-containing intervals do not establish equivalence.
- The negative-control diagnostic sample does not estimate the full cohort's
  FP/image. Its enriched composition cannot support population AP or precision.

## Expanded-candidate inference: NO-GO for the current paper

**Scientific decision:** defer the [full-cohort proposal](POSTHOC_CANDIDATE_SUPPORT_V2_PROPOSAL.md).
This is a prioritization decision, not a claim that additional collection would
be useless, infeasible or incapable of changing the curves.

| Potential gain | Existing evidence and remaining uncertainty | Value to current central claim |
|---|---|---|
| Recover missing high-budget external FROC support | YOLO seed 137 stops at 0.793333 FP/image; the upper-budget ordering can reverse under missing-support bounds. Faster R-CNN often reaches cap 100. | Useful if the paper claims an unrestricted frontier. The current paper explicitly does not. |
| Estimate expanded candidates' FP burden over all negatives | Current retention experiment includes all 84 positive images but only 84 negatives. | Full collection would materially strengthen an expanded-support FROC/AP sensitivity, which is a narrower secondary question. Negative-only expansion cannot substitute for the proposed matched complete-cohort comparison without its own protocol. |
| Explain failure at historical thresholds | Every strict positive has already been tested under the factorial retention arms across all runs, with unchanged historical recall. | Low incremental value for this question. This observation does not imply every full-cohort metric is unchanged. |
| Resolve the broad external collapse | Even full-cohort collection leaves reference standards, acquisition, site/population and optimization confounded. The AP-floor control remains very low. | Does not supply the missing clinical or causal evidence. |

Reconsider a GO only if authors/reviewers make expanded-support ranking or
upper-budget behavior an explicit primary question, or identify a reproducible
support defect that undermines a retained-support claim. Before authorization,
freeze a new namespace, factorial controls, complete cohort/run inventory,
paired estimands and all outcomes to report. Keep cap-100 official AP separate
from any cap-300 sensitivity. Set stopping rules on resource or integrity
failures, not favorable performance. Never promise an unrestricted frontier:
lower floors, finite caps and native NMS still limit support. No new threshold,
clinical policy or ontology is to be selected from those outcomes.

## Supplementary material: reduce reading burden without deleting provenance

The supplement is an evidence index rather than one coherent journal appendix.
It currently mixes current results, historical analyses and engineering audits.
Added a reading guide; retained every scientific artifact and S1-S12 anchor.

| Route for review | Material | Reason |
|---|---|---|
| Essential scientific support | S1-S3, current uncertainty in S7, matched timing in S8, external evidence in S9-S12 | Supports the main estimands, adverse runs, uncertainty and domain-change claims. |
| Optional secondary appendix | S4 calibration/raw-score utility; S5 synthetic stresses; S6 explanation controls | Adds separate questions with narrower samples; avoid making these evidence of transportability or clinical benefit. |
| Repository provenance, not repeated journal narrative | Historical asymmetric timing/Pareto panels, superseded audits, legacy report and repeated numerical traces | Retain for accountability but do not submit as parallel current results. |

The author-facing briefing summarizes decisions; the technical review explains
their basis; the checklist tracks reporting gaps. These should not all be
appended verbatim to the paper. A journal-specific supplement should keep one
authoritative table per result and link to the versioned raw aggregate files.

## Unresolved evidence versus reporting work

Expert review can investigate concept/instance comparability and reader
disagreement. It cannot turn source boxes into a clinical diagnosis or identify
all causes of shift. Acquisition and clinical metadata, unknown external patient
dependence, five-run uncertainty and one-machine timing remain design limits.
Their absence is not repaired by polishing prose. Ethics and data-use
determinations, journal fit, author approval and release selection require
author decisions; no checklist score or successful test suite substitutes.
