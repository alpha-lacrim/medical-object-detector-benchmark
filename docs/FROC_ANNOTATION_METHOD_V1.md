# Shared-annotation certificates for operating-budget detection comparisons

Exploratory method, 13 November 2026. Research branch:
`research/froc-annotation-certificates-v1`. This is a candidate methodological
contribution, not a declaration of publication priority or clinical validity.
See the [protocol](FROC_ANNOTATION_PROTOCOL_V1.md).

## 1. The problem that the previous proposal did not solve

Maximum matching answers whether candidate geometry exists. A minimum-cost
candidate oracle can select favorable boxes using ground truth. Neither answers
whether the actual FROC conclusion survives uncertainty in the *same reference
annotations used for every detector and trained run*.

This method supplies two different outputs: a conservative envelope over a
declared insertion/deletion budget, and exact finite-set extrema over one/two
deletions of existing references. The second retains cross-detector and cross-run
dependence that is lost by perturbing each evaluation independently. It is an
evaluation audit, not a new detector, annotation cleaner or deployable repair.

## 2. Contract and definitions

Fix the image universe, detector outputs, classes, scores, score ties, native
postprocessing, retained-candidate floor and cap. Within each image, process
candidates in the canonical stable descending-score order. A candidate selects
the available same-class reference with greatest IoU, resolving equal IoU by
the stable reference order; it matches only if IoU reaches the fixed cutoff.
Surviving references retain their relative order after edits. There are no
crowd, ignored-region, many-to-one or annotation-dependent candidate rules.

Let j index whole-score prefixes, including reject-all. Let T(j) and F(j) be
the integer cumulative TP and FP counts, and N the reference count. At an
integer FP budget B, define

    C(B) = max{T(j): F(j) <= B},       R(B) = C(B)/N.

For B<0 set C(B)=0 only as a lower-bound convention; reject-all is the operational
policy at nonnegative budgets. Use B=floor(b*n_images) for FP/image budget b.
N=0 recall is undefined. Whole ties enter together; no interpolation is allowed.
Both T and F are nondecreasing in j. Define j_b as the last prefix with F<=b.

An edit scenario inserts a references and deletes d original references, with
a+d<=k, d<=N and N'=N+a-d>0. New references may occur on previously negative
images. A relocation or class change costs a deletion plus an insertion. These
are hypothetical scenarios, not asserted corrections to clinical ground truth.

## 3. Lemma: a reference edit changes at most one greedy TP indicator

Under the contract above, one reference insertion changes at most one candidate
from unmatched to matched and never changes a matched candidate to unmatched.
A deletion has the reverse property. The candidate-to-reference assignments
themselves may change along a long chain.

**Proof.** Consider the baseline and insertion-augmented matchers at the same
step. Until a formerly unmatched candidate becomes matched, the augmented set
of available references equals the baseline set plus one extra reference e.
If the next candidate does not prefer e to its baseline choice, both make the
same choice and preserve this invariant. If it selects e instead of a baseline
reference g, both candidates are matched; the new extra available reference is
g. If the baseline candidate is unmatched and accepts e, exactly one TP bit is
gained, the remaining available sets become identical, and all later decisions
are identical. If e is never accepted by an unmatched candidate, no TP bit
changes. Fixed preferences and stable tie orders make these cases exhaustive.
An edit affects only one image; the other images' bits are unchanged. Reversing
the insertion proves deletion. Repetition gives at most a upward and d downward
bit changes under a edits and d deletions. This proof applies at every prefix
simultaneously, including endpoints of score ties. QED.

This is a specialization of familiar resource monotonicity in serial allocation,
not a claim of a new general matching principle. See, for example, the
[resource-monotonic serial-allocation analysis](https://people.duke.edu/~aa88/matchingconference/Klaus.pdf).
The important application is that reference edits have a *sparse TP-loss trace*
even when their assignment chain is long.

## 4. Theorem: FP-budget transport bounds

For the fixed detector, any allowed scenario satisfies

    max(0, C(B-d)-d) / N' <= R'(B)
                              <= min(N', T(j_(B+a)) + min(a,F(j_(B+a)))) / N'.

The left side is zero when B-d<0. These are conservative bounds, not guaranteed
attainable endpoints for the observed geometry.

**Proof.** At every fixed prefix, the lemma gives T-d<=T'<=T+a and
F-a<=F'<=F+d. A baseline prefix feasible at B-d remains feasible at B, and its
changed TP count is at least max(0,T-d); selecting the baseline optimum proves
the lower bound. Conversely, a changed prefix feasible at B must have baseline
F<=B+a. At that prefix at most min(a,F) old FP indicators can become TP, so
T'<=T+min(a,F), also T'<=N'. Both T and F increase along the baseline curve,
therefore the last eligible baseline prefix maximizes this upper expression.
Dividing by the common positive N' proves the claim. QED.

The horizontal budget change is essential. Take a high-score FP followed by
two lower-score TPs on different references. At B=0 the original ceiling is
zero. Insert a matching reference for the leading FP: the entire three-candidate
prefix becomes feasible and sensitivity becomes one. A vertical k/N adjustment
alone is not a valid FROC guarantee.

## 5. Run means, paired rankings and domain gaps

Let L_mr(a,d;B) and U_mr(a,d;B) be the bounds for detector m, run r. Use fixed
nonnegative run weights summing to one within each detector. For a declared
(a,d), average the lower/upper endpoints over runs *before* minimizing or
maximizing over edit-type allocations. All runs see the same reference count
N' and the same a,d. Every actual shared annotation scenario is then inside
the resulting family envelope by termwise inequalities.

For A-B, a valid paired envelope is

    min_(a,d) [mean_r L_Ar(a,d;B) - mean_s U_Bs(a,d;B)],
    max_(a,d) [mean_r U_Ar(a,d;B) - mean_s L_Bs(a,d;B)].

Again a,d are shared across detectors. The unknown edit locations are still
relaxed, so this is not a sharp joint-geometry optimizer. A strictly positive
lower endpoint certifies the observed mean ordering under the declared budget.
Losing a certificate does not demonstrate that a reversal can occur.

For an external-only annotation perturbation, subtract the external upper
endpoint from the unchanged internal mean recall to obtain a lower bound on
the domain gap. A positive value rules out explanations of that gap requiring
only the allowed number/type of external annotation edits, conditional on all
other fixed aspects of the evaluation. It does not estimate how many errors the
annotations actually contain or identify the mechanism of acquisition shift.

## 6. Exact shared-reference deletion audit

For each reference subset S of size q in {1,2}, delete S in a temporary in-memory
copy and rematch its affected images with the canonical matcher. Never edit
the original annotations. By the lemma, record at most q lost TP score-group
indices; a padding value denotes no loss. For prefix j, let ell_S(j) count lost
indices at or before j. The changed cumulative counts are exactly

    T_S(j)=T(j)-ell_S(j),       F_S(j)=F(j)+ell_S(j).

Binary search the last prefix with F_S<=B and return T_S/(N-q). For subsets
spanning distinct images, combine cached local losses. For two references in
one image, rematch them jointly: singleton effects are not generally additive.
For example, one candidate compatible with either of two references loses
nothing when either alone is removed, but loses its TP when both are removed.

Use exactly the same S for all runs and both detectors. Average the run-specific
endpoints for that S, subtract detector means if needed, and only then take
the minimum/maximum over S. Enumeration covers the entire declared finite
scenario set, so these endpoints are attainable *within that hypothetical
deletion model*. Independent per-run extrema form a relaxation; their endpoint
differences need not correspond to any common annotation set. Combining the
baseline with q=1,2 extrema yields the corresponding at-most-two-deletion set.

The protocol changes labels only for a diagnostic calculation in memory. An
extremizing scenario is not a proposed clinical relabeling, and no patient or
image identifier from the subset census is published.

## 7. Nonredundancy theorem

Even the two complete marginal FROC curves do not determine the exact shared
annotation sensitivity of their difference.

**Construction and proof.** Let an image have disjoint references g1,g2.
Detector A scores exact copies of g1,g2 at 0.9,0.8. Detector B scores exact
copies of g2,g1 at 0.9,0.8. At B=0 both full FROC curves have successive
(TP,FP)=(0,0),(1,0),(2,0), and both geometric matching ranks equal two.
Deleting g1 gives A zero budget-feasible TPs and B one; deleting g2 reverses
this. Since N'=1, the exact paired sensitivity difference ranges from -1 to 1.
In the comparison A versus an identical copy of A, all marginal FROC curves,
geometry ranks and historical count summaries are the same, but the paired
difference is zero under every common deletion. Thus marginal curves and
matching counts cannot recover the shared-subset audit. QED.

This establishes information beyond the quantities that made the previous
uniform-cost proposal redundant. It establishes neither priority over all
prior literature nor clinical utility by itself; the real-data comparison and
related-work assessment remain necessary.

## 8. Complexity and statistical limits

With U score groups, J operating budgets, R runs and S_q=binomial(N,q) subsets,
endpoint reconstruction costs O(R*S_q*J*q*log U) after the loss traces are known.
The current implementation stores O(R*S_q*J) endpoint values privately.
Local matching is memoized by image and deleted local subset, reducing repeated
work on cross-image pairs. This is exhaustive enumeration with a reusable
sparse trace, not a polynomial-time solver for unbounded q; S_q is combinatorial.
The implementation deliberately supports only q=1,2 for the exact census.

Universal envelopes enumerate O(k^2) insertion/deletion allocations for each
k. Each allocation uses binary search of existing integer count curves, without
image inference or new assignment optimization. The current implementation
preserves every allocation rather than relying on an unproved reduction.

Joint observation/run bootstrap intervals describe sampling variation of the
universal envelope endpoints. Internal sampling units are known patients;
external units are images because patient linkage is unavailable. The same
checkpoint multiplicities are used across cohorts, independent between detector
families. Nonlinear envelopes and paired domain contrasts are recomputed within
each draw. Edit units in a draw are observation copies, not original subjects.
Undefined zero-reference draws are retained and counted. Intervals are marginal,
not simultaneous, and are not finite-sample coverage or clinical-error guarantees.
The exact deletion census is conditional on the observed cohort/runs and has
no claimed observation-sampling CI in this version.

## 9. Closest primary literature and scope of the novelty claim

Searches on 13 and 15 November 2026 covered annotation-aware FROC, annotation robustness,
shared-label ranking, adversarial label errors, targeted case removal and serial
matching. Search absence does not prove originality. Relevant overlaps include:

| Primary work | Established contribution | Difference investigated here |
|---|---|---|
| [TIDE, ECCV 2020](https://arxiv.org/abs/2008.08115) | Diagnoses object-detection error contributions | Shared reference edits and an operating-budget ranking certificate |
| [OC-cost, CVPR 2022](https://arxiv.org/abs/2203.14438) | Image-level correction cost via transport | Fixed predictions; changes to reference membership and FROC feasibility |
| [Noise-Aware Evaluation, WACV 2025](https://openaccess.thecvf.com/content/WACV2025/html/Llerena_Noise-Aware_Evaluation_of_Object_Detectors_WACV_2025_paper.html) | Annotation-noise-aware bounds, focusing on corner discrepancies and AP | Discrete presence edits, budget transport and exact common-subset extrema; no claim to the first noise-aware evaluation bound |
| [Annotation agreement via OT, ACCV 2026](https://arxiv.org/abs/2610.19912) | Quantifies agreement between annotation sources | Bounds an actual operating-budget comparison without another annotation source |
| [Benchmark incompleteness, 2026 preprint](https://arxiv.org/abs/2609.21822) | Reannotation, ambiguity-aware benchmarks and real label-error analysis | No new adjudication; conditional sensitivity rather than estimated annotation accuracy |
| [AMIP, Broderick et al.](https://arxiv.org/abs/2011.14999) | Sensitivity of conclusions to influential sample removal, with approximation bounds | Deletes reference objects while retaining images and predictions; exact small-budget nonlinear FROC audit |
| [Decision Reliability Profiles, 2026](https://www.mdpi.com/1999-4893/19/8/676) | Targeted case-removal comparison under additive metrics | Rematching and a discrete FP constraint make this object-level problem nonadditive |
| [Serial-allocation resource monotonicity](https://people.duke.edu/~aa88/matchingconference/Klaus.pdf) | Established matching monotonicity | Domain specialization and sparse endpoint reconstruction, not a new general allocation theorem |
| [Lampert et al., IEEE TIP 2016](https://arxiv.org/abs/1307.0426) | Detector rankings depend on how annotators' references are combined | Conditional certificates from one reference set; not the first recognition of annotation-dependent rankings |
| [Cost-sensitive failure recognition, UAI 2024](https://arxiv.org/abs/2404.17427) | Budgeted uncertainty thresholding to recognize detector failures | No policy fitting; bounds on an evaluation conclusion under shared reference edits |

The primary WACV PDF was obtained on 15 November after the web viewer failed.
Sections 3.1-3.4, equations (3)-(4) and (10), bound box similarity via the triangle
inequality and use an estimated expected corner-noise discrepancy to adjust IoU
and AP. Section 3.3 explicitly restricts its analysis to localization noise.
Our membership edits leave surviving geometry fixed, alter the reference
denominator and FP-budget feasibility, and retain a common scenario across runs.
We did not execute the authors' implementation; this is an equation-level scope
comparison, not an empirical superiority claim over their noise model.
The method is a bounded contribution in shared-annotation FROC auditing, not the
first robustness theorem or an established publication-priority claim. The
[assessment](FROC_ANNOTATION_RESEARCH_ASSESSMENT.md) records the integration verdict.

## 10. What this can and cannot establish for the professor

The method can strengthen the answer to whether evaluation/annotation uncertainty
could undermine the observed collapse or detector ordering. It preserves the
explicit label mapping and evaluation protocol and separates statistical from
annotation sensitivity. Its exact shared-subset component is demonstrably
nonredundant with complete marginal FROC curves.

Saved predictions and one reference set cannot identify latent clinical truth
or causal acquisition mechanisms: different latent label conventions and failure
mechanisms can produce the same observed predictions and references. No theorem
about those observations can distinguish such mechanisms without further
information or assumptions. Thus sufficient publication novelty, clinical label
equivalence and a complete causal explanation remain separate claims requiring
evidence; they must not be described as solved by passing tests.
