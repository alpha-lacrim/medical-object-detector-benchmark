# Shared-annotation FROC certificates: research assessment

15 November 2026. Branch `research/froc-annotation-certificates-v1`, based on
`d27373d26325768602545d0c9aa8b170b2129d1d`. Exploratory research following the
previous constrained-repairability NO-GO; the earlier findings are preserved.

## Verdict: GO for a bounded methodological addition

Integrate the shared-annotation audit into the research-branch manuscript.
Mathematical correctness, independently checked implementation, and useful
information beyond the previous summaries have been demonstrated. This is a
recommendation to present a defensible contribution, not a guarantee of journal
novelty, clinical validity or acceptance. We have not established priority over
all prior literature, and should not describe this as a new general matching
theorem or a detector repair algorithm.

The contribution is **operating-budget sensitivity to a common reference set**:
conservative insertion/deletion certificates, exact small-budget shared-deletion
extrema using sparse greedy matching changes, and separate joint observation/run
uncertainty. Keeping the same edits across detectors and runs is essential.
The earlier uniform-price oracle was determined by existing counts. This audit
provably cannot be reconstructed even from complete marginal FROC curves.

This assessment was written after executing the exploratory protocol and before
changing the canonical manuscript. No frozen primary result is replaced.

## Evidence and mathematical status

The [method](FROC_ANNOTATION_METHOD_V1.md) gives the definitions, full proofs,
counterexamples, algorithms, complexity and assumptions. The
[protocol](FROC_ANNOTATION_PROTOCOL_V1.md) predates this analysis run but follows
the original observed study; it is not a preregistration.

| Claim | Evidence | Boundary |
|---|---|---|
| One reference insertion/deletion changes at most one greedy TP bit | Available-reference-set invariant; exhaustive serial preference checks | Fixed candidate order, best available reference, stable tie preferences; no crowd/ignore |
| Actual FROC requires horizontal budget transport as well as vertical TP bounds | Proof using feasible prefixes at B-d and B+a; explicit one-edit cliff | Conservative extrema, not necessarily attainable |
| Shared deletion sensitivity is not determined by marginal FROC curves | Two-reference construction with identical complete curves and different paired ranges | An information distinction, not a publication-priority proof |
| Sparse traces reconstruct exact small-deletion endpoints | Canonical full-rematching comparison over randomized geometry and ties | Exact census limited to one/two deletions; same-image pairs rematched jointly |
| Common edits improve the comparison in this study | Complete census across both cohorts, all runs/budgets | Hypothetical scenarios; no annotation declared wrong |
| Original scientific evidence remains intact | Baseline gates, hash receipts and exact replay | This extension makes no new independent external-test performance claim |

For N references and q deletions, enumeration has binomial(N,q) scenarios.
Endpoint reconstruction costs O(R*binomial(N,q)*J*q*log U) after local matching,
with R runs, J budgets and U score groups. It is not a polynomial solver for
arbitrary q. Unknown insertions/deletions use conservative O(k^2) allocation
enumeration for each tested k. Detailed local-rematching costs remain data
dependent; no asymptotic speed advantage over every existing method is claimed.

## Closest research and originality limits

The method document contains a primary-source comparison matrix. Three overlaps
most directly constrain the claim:

- [Noise-Aware Evaluation of Object Detectors (WACV 2025)](https://openaccess.thecvf.com/content/WACV2025/papers/Llerena_Noise-Aware_Evaluation_of_Object_Detectors_WACV_2025_paper.pdf)
  already develops annotation-noise-aware evaluation bounds. Its equations use
  box-distance inequalities and a corner-noise model for adjusted IoU/AP. Our
  different object is reference membership, whole-score FP feasibility and
  common-subset detector/run comparisons. Its code was not run here.
- [Decision Reliability Profiles (2026)](https://www.mdpi.com/1999-4893/19/8/676)
  already studies targeted deletion sensitivity of fixed-prediction comparisons.
  Its exact descending-gain calculation assumes additive case losses. Reference
  deletion here preserves images and candidates, rematches detections and can
  move the feasible score endpoint; singleton effects need not add.
- [Lampert et al. (IEEE TIP 2016)](https://arxiv.org/abs/1307.0426)
  already shows that reference construction can change detector rankings. We
  claim a specific conditional audit, not discovery of that phenomenon.

Resource monotonicity, FROC, joint bootstrap, oracle diagnostics and exhaustive
enumeration are established ideas. The proposed contribution is their specified
combination for common annotation edits with a nonredundancy proof and real
operating-budget evidence. The literature search through 15 November 2026 does
not establish worldwide priority. Independent expert review is still needed to
judge whether this is sufficiently original for a particular journal.

## Completed empirical study

The analysis used five retained seeds per detector in each complete cohort,
750 internal images with 268 references and 3,000 external images with 95
references, all five original FP/image budgets, and the original score floor,
cap, native NMS and IoU matching. No inference, training or label files changed.
All 20 cohort/run baselines matched the completed repairability v2 results.

At the primary 0.25 FP/image budget, baseline cutoff ceilings are
0.366418/0.086316 internally/externally for Faster R-CNN and
0.266418/0.033684 for YOLO11s. With only external references allowed to change,
the conservative mixed-edit bounds preserve a strictly positive internal-minus-
external gap through 41 and 29 edits respectively. These are sufficient point
certificates, not exact minimum edit distances or estimated annotation-error
rates. Losing the bound at the next count does not establish a feasible recovery.

Sampling uncertainty supports more restricted statements. At 20 external edits,
the Faster R-CNN gap lower bound is 0.119461, with marginal 95% joint-bootstrap
interval [0.025995, 0.203687]. At 10 edits the YOLO11s value is 0.140704
[0.070139, 0.211927]. At 30 edits for Faster R-CNN and 20 for YOLO11s those
intervals cross zero. All planned grid values, including these losses of
statistical resolution, are disclosed in the public tables and figures.

Every one/two-reference subset was enumerated: 268/35,778 internally and
95/4,465 externally. For the external Faster R-CNN minus YOLO11s comparison:

| Deleted references | Exact common-subset range | Independent-run/detector relaxation | Width reduction |
|---:|---|---|---:|
| 1 | [0.044681, 0.055319] | [0.042553, 0.063830] | 50% |
| 2 | [0.036559, 0.058065] | [0.032258, 0.075269] | 50% |

These are attainable extrema within the finite hypothetical deletion family,
not confidence intervals. The independent comparator may use contradictory
annotation sets for different detectors/runs. The result quantifies the benefit
of retaining the actual dependence structure; it is not a performance gain.

The [generated results](FROC_ANNOTATION_RESULTS_V1.md) and all public CSVs supply
the other budgets and endpoints. Joint uncertainty uses 2,000 patient/image/run
draws, recomputing bounds and domain contrasts within each draw. All reported
draws here were defined. The exact subset census has no sampling CI in v1.

## Validation and reproducibility

The full analysis completed in 118.09 seconds on the local CPU. A fresh replay
reproduced all five tables and every private array exactly. The analysis receipt
binds 146 inputs and six outputs; the report receipt binds four inputs and three
outputs. Both figures were visually reviewed and the report replay was byte exact.

Fourteen mathematical/algorithm tests include 12,288 exhaustive single-edit
preference comparisons, exhaustive bounded TP-bit edits, 800 random geometric
single/pair-deletion cases against full canonical rematching, paired families,
score ties, zero budgets/references, caps, monotone scores, and explicit FROC and
nonadditivity counterexamples. Additional artifact checks reconstruct uncertainty
and common-subset extrema independently from retained arrays. Final verification
and Git state are recorded in the handoff and verification document.

Authorized data had moved to `D:\vindr-rsna-dataset`. Thirty-nine missing analysis
inputs were restored as hash-verified copies to their original ignored relative
paths (56.08 MiB); no images/raw data were copied. The D-drive originals and user
Git changes were preserved. Observation-linked arrays remain ignored/private.

## Professor's requirements

| Requirement | What can now be defended | What remains unresolved |
|---|---|---|
| Explain the external decline | Cutoff versus ranking/geometry limitations, controlled output checks, and conditional exclusion of small annotation-edit explanations | A causal clinical or acquisition mechanism is not identified |
| Clarify label mapping and protocol | Frozen strict mapping, cross-ontology qualification, exact matcher/ties/caps and explicit sensitivity model | True clinical equivalence of RSNA and VinDr targets is not established |
| Establish statistical stability | All attempted runs, patient/image and run resampling, paired nonlinear contrasts, and clear separation from annotation sensitivity | Unknown external patient linkage, few training runs, and marginal rather than simultaneous coverage |
| Define a contribution beyond two-model comparison | A mathematical and computational common-annotation audit with a proof of nonredundancy and measured tightening | Publication priority and sufficient journal-level novelty require independent judgment |
| Fix a research question before choosing a venue | How much failure is cutoff-repairable, and how robust is that conclusion to shared reference uncertainty? | No final journal or submission claim is selected |

The paper can now give a much stronger answer to the professor. It should not
claim that every requirement is fully solved. Saved predictions and one reference
set cannot identify latent clinical truth or separate every acquisition/ontology
cause. This is an identifiability limit, not a missing theorem that software tests
can remove. No radiologist access, retraining or new labels are prerequisites
for presenting this bounded contribution.
