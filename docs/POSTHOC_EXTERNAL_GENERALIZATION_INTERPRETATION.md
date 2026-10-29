# Scientific interpretation of post-hoc external generalization v1

These are exploratory measurements designed after the original VinDr results
were known. Numerical sources are the generated CSVs and summary under
`results/external_generalization_v1/`; methods are in the versioned protocol.
Verification outcomes are recorded separately. The strict original target,
all checkpoints and adverse runs remain unchanged.

## What the retained evidence establishes

| Question | Executed evidence | Interpretation and limits |
|---|---|---|
| RQ1: observable errors | Equal-run reference fractions: matched 1.895%/0.421%, compatible only below historical threshold 54.947%/17.684%, partial localization 25.053%/21.684%, no retained IoU >=0.25 candidate 18.105%/60.211% (Faster R-CNN/YOLO11s). High-score assignment category is zero for both. | The retained failure profiles differ. Low scores account for many geometrically compatible Faster R-CNN candidates; YOLO has more targets without a sufficiently overlapping retained box. These are descriptions of outputs, not causal mechanisms or evidence about hidden proposals. The partial/absent boundary is exploratory. |
| RQ2: annotation sensitivity | At historical thresholds, 53.656%/37.795% of strict FPs overlap another localized class at IoU >=0.50, using equal-run fractions over five/four nonempty FP populations. | Strict FP accounting includes substantial spatial agreement with other annotations. YOLO's fifth, zero-output run remains in counts/metrics and has undefined FP proportions. This supports an annotation-disagreement caveat, not corrected clinical labels. No merged-target AP or validated clinical equivalence is established. |
| RQ3: population weighting | Internal custom weighted AP50 becomes 0.108684/0.055072 from canonical 0.304224/0.162612; historical precision becomes 0.086639/0.062173 from 0.362419/0.252403. | Weighting the internal positive-image frequency to 0.028 materially changes precision/ranking summaries. It does not reproduce observed external AP 0.002505/0.000501 or precision 0.010830/0.004271. Recall is unchanged by construction. Do not interpret any arithmetic fraction of the observed drop as a causal explained fraction. |
| RQ4: cross-domain change | Both detectors have negative marginal intervals for AP50, FROC at 0.25 FP/image and historical recall. Difference-in-change AP50 is -0.139607 [-0.179174, -0.101154]; recall -0.141233 [-0.250947, -0.051971]; FROC -0.047368 [-0.105416, 0.023884]. | Absolute degradation is supported under this resampling model. Faster R-CNN has the larger absolute AP/recall decrease from its higher internal baseline. The FROC degradation difference is unresolved. This is not a relative robustness or architecture-superiority claim. AP changes cross non-equivalent reference ontologies. |
| RQ5: finite candidate support | Replayed original budget flags/bounds; external YOLO seed 137 ends below 1/2 FP/image, while Faster R-CNN cap counts remain 3000/2635/3000/3000/209 and YOLO counts remain zero. No bootstrap draw is floor-limited at the selected 0.25 budget. | The selected low-budget interval is conditional on retained support. The existing upper-budget missing-support reversal possibility and cap limitation remain. No new collection was done and no full-frontier ranking is claimed. |

The full per-run reference/FP/availability/score tables retain all runs and
denominators. Class-specific overlap flags are nonexclusive: summing them
would double count predictions. Geometry alone cannot distinguish an
appropriate broader opacity detection from a chance or clinically irrelevant
overlap. Clinical expert adjudication is needed to answer that question.

The 2,000 joint bootstrap draws preserve known internal patient clusters and
shared observation sampling within each cohort. The same selected checkpoint
has the same multiplicity across domains, while detector families are sampled
independently. All selected change endpoints have 2,000 valid and zero undefined
draws. These marginal intervals condition on fixed training data, the empirical
five-run recipes, thresholds, target definitions and retained candidates.
They do not include new-training-cohort uncertainty, unknown repeated external
patients or simultaneous endpoint coverage. The weighting intervals additionally
condition on the observed external positive-image frequency. No p-value family
was introduced.

## Competing explanations remain unresolved

An image can contain a broad pulmonary finding with a different local label,
but the present data cannot demonstrate that replacing its annotation would
make it equivalent to an RSNA reference object. Likewise, low score can follow
many changes in image appearance or pipeline behavior. We did not manipulate
acquisition, reference standards, population and preprocessing independently.
The prior five-run YOLO numerical-path sensitivity narrows one implementation
concern but does not isolate remaining causes. Substantial reweighted internal
performance also does not validate a label-shift model for VinDr: weighting
holds the internal within-stratum case mix fixed by assumption.

## Contribution and relation to primary literature

| Established work | Verified primary source | Relationship to this study |
|---|---|---|
| Variable external chest-radiograph performance and site/population confounding | Zech et al., PLOS Medicine 15(11):e1002683 (2018), [DOI](https://doi.org/10.1371/journal.pmed.1002683) | External failure is not a newly discovered phenomenon. This study adds evidence for the particular frozen detector/ontology/threshold setting. |
| Distinct local and global radiographic annotation concepts | Nguyen et al., Scientific Data 9:429 (2022), [DOI](https://doi.org/10.1038/s41597-022-01498-w) | The release's annotation taxonomy motivates auditing other-class overlap, but does not validate merged lesion instances. |
| Detector calibration and evaluation-population pitfalls | Kuzucu et al., ECCV 2024, pp.185–204, [official paper](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/03148.pdf) | Separating ranking, score populations and thresholds uses established concerns. No calibrator was fitted here. |
| Free-response localization and multiple marks/lesions | Chakraborty, Radiation Protection Dosimetry 139(1–3):20–25 (2010), [author article](https://pmc.ncbi.nlm.nih.gov/articles/PMC2868098/), DOI 10.1093/rpd/ncp305 | Fixed-budget localization differs from exam-level ROC and diagnosis. This study does not introduce FROC or JAFROC. |
| Reference, population, output and aggregation pitfalls | Reinke et al., Nature Methods 21:182–194 (2024), [DOI](https://doi.org/10.1038/s41592-023-02150-0) | Explicit denominators, empty populations and reference mismatch are established validation principles, implemented here for this benchmark. |
| Variation in trained-model comparisons | Bouthillier et al., MLSys (2021), [official paper](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf) | The finite trained-run resampling is conditional on the studied recipes and fixed training cohort, not comprehensive benchmark uncertainty. |
| Marginal label-frequency changes require conditional-distribution assumptions | Lipton, Wang and Smola, ICML/PMLR 80:3122–3130 (2018), [official proceedings](https://proceedings.mlr.press/v80/lipton18a.html) | The present weighting is a labeled, post-hoc arithmetic sensitivity; it is not BBSE, unlabeled shift estimation, adaptation or evidence that label shift holds. |

The contribution is empirical: reproducible separation of ranking,
absolute-performance and historical-operating-point transport, supported by
retained-candidate diagnostics and correctly paired checkpoint change
uncertainty. The implementation is a useful auditable combination of existing
methods; it does not substantiate a new detector, novel statistical framework,
first discovery of domain shift, causal explanation or clinical utility.

## Recommendation to the supervising professor

The additional evidence strengthens the paper by replacing a vague explanation
of external collapse with measured output categories, a bounded annotation
accounting analysis, a transparent population-weight sensitivity and explicit
uncertainty in degradation itself. Its defensible claim is a careful empirical
transportability study. Expert reference-standard review would strengthen any
broader ontology claim; further candidate collection can address support but
requires separate authorization. Authors should retain the adverse findings
and complete ethics/journal decisions and final manuscript review before
submission. A new architecture is not necessary to make this contribution.
