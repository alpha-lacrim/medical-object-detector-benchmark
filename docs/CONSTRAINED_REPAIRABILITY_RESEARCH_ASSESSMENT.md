# Constrained detector repairability: research assessment

Exploration started 7 November 2026; assessment finalized 12 November 2026.
Exploratory follow-up on branch
`research/constrained-repairability-v1`, based on `cc00ae5`. This assessment is
separate from the canonical article and its frozen evidence. The user has no
radiologist access; none of the work below depends on clinical adjudication.

## Decision and purpose

**NO-GO for presenting this proposal as a new theorem-driven method paper.**
The two proposed mathematical results hold under the stated restrictions, but
validity alone does not establish originality. More decisively, uniform edit
costs admit a closed form in three familiar matching counts. Thus the proposed
cost surface adds no independent information beyond these counts. Heterogeneous
costs do yield a distinct optimization problem, but this study has no validated
candidate-level effort or harm measurements to justify such costs. Inventing
weights would not solve that research problem.

The implementation, proofs, counterexamples and complete exploratory analysis
are preserved for inspection. The canonical manuscript, PDF, numerical claim
bindings and frozen scientific/publication inventories remain unchanged. This
verdict concerns the proposed novelty claim, not the value of the existing
cross-dataset empirical study or an editorial decision about publication.

## 1. Formal problem and intervention classes

Let C be the retained candidates and G the reference boxes in a fixed image
universe. Candidate/reference labels and geometry are fixed. An edge exists
exactly when both vertices belong to the same image, have the same canonical
class, and meet the specified IoU cutoff. Let I be the historical selected set,
including all scores equal to the historical threshold. For S subset C, let
nu(S,G) be maximum one-to-one bipartite matching cardinality. Define

```
oracle TP(S) = nu(S,G)
oracle FP(S) = |S| - nu(S,G)
c(S) = sum_{i in S\I} p_i + sum_{i in I\S} q_i
C*(K,B) = min c(S) subject to nu(S,G) >= K and |S|-nu(S,G) <= B.
```

Here K and B are nonnegative integers; p_i and q_i are nonnegative additive
promotion/suppression costs. Optional nonnegative candidate weights can be
absorbed into these costs. Infeasibility is represented by positive infinity.
Suppression changes membership; it does not move or reclassify a box. No cost is
charged for reassignment by the oracle. Charging for assignment changes would be
a different optimization problem requiring additional definitions.

| Intervention | Permitted action | Information used here | Relation to deployment |
|---|---|---|---|
| Global cutoff | Choose one exact score prefix, preserving ties | FROC test-set envelope | Retrospective envelope, not a newly validated threshold |
| Candidate membership | Promote/suppress individual retained candidates | References may choose the subset | More permissive than one cutoff; oracle selection |
| Oracle assignment | Match selected compatible boxes in any one-to-one way | Full reference compatibility | May be unrealizable by score-ordered evaluation |
| Geometry/creation | Move boxes, change labels, add candidates or rerun collection | Outside the fixed graph | Neither covered nor ruled out by these certificates |

For n images and N references, the experiment uses B=floor(b*n) and
K=ceil(q*N), calculated with exact decimal-rational arithmetic. Target fractions
are exploratory coverage levels, not clinically acceptable sensitivity levels.
When N=0, the count problem remains defined for K=0, but recall-based summaries
are undefined. The experiment retains such bootstrap draws without replacement.

## 2. Integral minimum-cost-flow theorem

**Theorem 1.** For fixed C,G,I and additive candidate costs, C*(K,B) equals the
optimum of an integral minimum-cost circulation plus a known constant. The
statement holds for real costs mathematically; the implementation accepts exact
integers, or externally scaled rational costs, to avoid floating-point flow
ambiguity. If K exceeds nu(C,G), the problem is infeasible for every B>=0.
Conversely, if K<=nu(C,G), it is feasible for every B>=0.

**Construction.** Use source s, sink t, FP collector f and TP collector u, one
vertex per candidate and one per reference. All omitted arc costs are zero.

| Arc | Lower capacity | Upper capacity | Cost |
|---|---:|---:|---|
| s -> candidate i | 0 | 1 | p_i if i not in I; -q_i otherwise |
| candidate i -> compatible reference j | 0 | 1 | 0 |
| candidate i -> f | 0 | 1 | 0 |
| reference j -> u | 0 | 1 | 0 |
| u -> t | K | number of references | 0 |
| f -> t | 0 | B | 0 |
| t -> s | 0 | number of candidates | 0 |

Add the constant Q=sum_{i in I} q_i to the flow objective. If K>|G|, reject
immediately. Replacing the lower bound on u->t by residual capacity |G|-K
requires residual inflow-minus-outflow demand +K at u and -K at t.

**Proof of correspondence.** In an integral feasible flow, select precisely the
candidates receiving a unit from s. Flow conservation routes each selected
candidate either to one compatible reference or to f. Reference capacity one
makes the reference-routed units a matching, of cardinality m>=K. At most B
selected candidates are routed through f. The maximum matching on that same
selected set can only improve m, so nu(S,G)>=K and |S|-nu(S,G)<=B. The objective
plus Q is exactly c(S), including the cost of suppressing each initial candidate
not selected.

Conversely, for every feasible S, route a maximum matching through the reference
vertices and the remaining selected candidates through f, then return all flow
through t->s. All capacities and the K lower bound hold, and its objective plus
Q equals c(S). These two directions prove equality of optimal values. This is
an exact correspondence **after projection onto selected sets**, not a bijection:
one selected set may admit many flows, and some flows deliberately under-match
it while still satisfying the constraints.

For completeness, the integrality argument is the standard network-matrix
argument. The directed incidence matrix has a +1 and -1 in each column. Any
square submatrix either has a column with at most one nonzero, allowing induction
on determinant size, or has zero column sums and determinant zero. Its square
minors are therefore 0 or +/-1. Appending identity rows for bounds preserves this
property. Integral demands and capacities imply integral extreme points. The
feasible circulation polytope is bounded here, so a nonempty feasible instance
has an integral optimal extreme point. This is established network-flow theory,
not a new integrality result. See the
[MIT network-flow notes](https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/687225c151d8cc8254dcb8b07e5f9ce2_MIT15_053S13_lec16.pdf).

Finally, every matching on S is also a matching on C; therefore K>nu(C,G) is
impossible. If K<=nu(C,G), select only K candidates from any maximum matching.
They yield K matches and zero FPs, proving the converse. This does not say a real
policy can discover that subset or obtain that assignment. QED.

**Policy lower bound.** Any real policy restricted to the same membership edits,
whose one-to-one evaluation yields at least K TPs and at most B FPs, selects an
oracle-feasible S: maximum matching is at least its actual TP count. It therefore
pays at least C*(K,B). This is a pathwise lower bound, also valid per realization
of a randomized policy. It is not a guarantee of deployable repair, expected
future sensitivity, or a bound on methods allowed to create/move candidates.

**Greedy counterexample.** In one image, take references [0,0,10,10] and
[5,0,15,10]. Candidate boxes [2,0,12,10] and [0,0,7,10] have scores .9 and .8.
At IoU .5, the first is compatible with both references but greedily prefers the
first; the second is compatible only with the first. With I containing both,
K=2,B=0, the oracle has cost zero. Score-ordered greedy matching yields one TP
and one FP. No subset of these candidates yields two greedy TPs at the fixed
order. Reversing their scores would work, but changes a different intervention
class. All four subsets are checked by the canonical evaluator in tests.

## 3. The simplification that limits the novelty claim

**Theorem 2 (uniform-cost reduction).** Write H=|I|, r=nu(I,G), M=nu(C,G). For
constant promotion price p>=0 and suppression price q>=0,

```
C*(K,B) = p*max(0,K-r) + q*max(0,H-r-B),  if K<=M;
C*(K,B) = infinity,                     if K>M.
```

**Proof, lower bound.** Adding a candidate raises matching rank by at most one,
and deleting a candidate cannot raise it. At least max(0,K-r) promotions are
needed. The nullity |S|-nu(S,G) cannot decrease on insertion and decreases by at
most one on deletion. Starting from nullity H-r, at least max(0,H-r-B)
suppressions are needed. Nonnegative prices give the stated cost lower bound.

**Proof, simultaneous attainment.** Choose r initially selected candidates that
can all be matched. These are a basis of I in the transversal matroid of
matchable candidate sets. Extend this independent set to size max(r,K) within
C; this is possible because its rank is M. None of the added elements needs to
come from I: all of I is in the closure of the initial basis, and closure only
grows on extension. Thus exactly d=max(0,K-r) initially unselected candidates
suffice. Equivalently, augmenting paths can extend a matching without losing any
previously matched left vertex; an unmatched vertex in I cannot augment after
d additions because rank(I plus those d candidates)<=r+d. Each necessary next
augmentation can therefore start outside I and the previous additions.

Keep this matched set and remove s=max(0,H-r-B) of the H-r remaining initial
candidates. This is possible since B>=0 implies s<=H-r. The surviving set has
rank exactly r+d: it contains that many independently matched candidates and
adding d candidates to I cannot raise its rank further. Its nullity is H-r-s,
at most B, and its cost attains both lower bounds simultaneously. QED.

Consequently, the entire uniform-cost surface is a deterministic transformation
of H,r,M. Changing the global promotion/suppression price ratio does not remove
this redundancy. Moreover, B changes only the necessary removal of historical
excess FPs; it does not constrain oracle promotions of correctly assigned boxes.
The framework cannot capture the operational difficulty of finding those boxes.

With heterogeneous costs, counts no longer suffice. For example, two initially
unselected candidates compatible with one reference have costs (1,10) or (5,10).
Both instances have H=r=0,M=1,K=1,B=0, but optimum costs 1 and 5. This validates
the weighted solver's distinct functionality, not the clinical relevance of
unmeasured weights or a new optimization algorithm.

## 4. Annotation-edit stability theorem

**Theorem 3.** Fix the candidates of detectors A and B and a common reference set
G. If G' is obtained by at most k shared reference insertions/deletions, then

```
abs([nu_A(G')-nu_B(G')] - [nu_A(G)-nu_B(G)]) <= k.
```

**Proof.** One insertion changes each maximum matching count by either zero or
one. It cannot decrease rank; removing the inserted vertex from any matching
loses at most one edge. Thus the two detectors' changes lie in the SAME interval
[0,1], and their difference lies in [-1,1]. For one deletion, both changes lie
in [-1,0], with the same conclusion. Telescope over the k edits and apply the
triangle inequality. The shared edit direction is why the bound is k, not 2k.
It is tight when one inserted reference is compatible only with A. QED.

A relocated box counts as two edits; this is necessary. A reference initially
matching only A and relocated to match only B changes the gap from +1 to -1.
Replacing a class-labelled reference also needs deletion plus insertion under
this definition. An ontology change affecting many boxes cannot be charged as
a single edit.

The graph is the disjoint union of per-image graphs, so the proof holds for a
new reference on a previously negative image. The image universe and both
detectors' retained candidates must stay fixed. Each detector's fixed weighted
mean over runs also obeys the theorem if its weights are nonnegative and sum to
one: every mean increment lies in [0,1], or every decrement in [-1,0]. Equal run
counts and seed pairing are unnecessary. Sums of run counts without normalization
do not obey the same unit bound. Weights selected again after seeing the edits
are outside this result.

**Conditional ranking certificate.** For the equal-run mean count gap D>0,
D>k guarantees a strictly positive geometric gap after any k allowed edits.
D>=k guarantees only a nonnegative gap. When both detectors share the same
edited denominator N'>0, dividing by N' preserves the sign. It does not preserve
the magnitude bound: one valid normalized bound is

```
|D'/N' - D/N| <= k/N' + |D|*|N'-N|/(N*N'),  for N,N'>0.
```

The numerical sensitivity curves show [D-k,D+k], not attainable extrema or
probabilities of annotation error. They neither infer which references are
wrong nor modify medical ground truth. An original reference repeated w times
by a bootstrap draw has edit weight w; the unit bound cannot silently be applied
to original-reference edits in that weighted sample. Conditional edit bounds
and observation/run sampling intervals are therefore reported separately.

**Why this is not a FROC theorem.** At budget zero, let A have one highest-score
FP on a negative image, followed by two correct boxes on two positive images.
Initially no nonempty score prefix is feasible, so its FROC TP count is zero.
Insert one reference compatible with that first box: all three become feasible
TPs. One edit changes the budget-constrained TP count by three, while maximum
matching rises only from two to three. A second detector with no candidates
makes this a counterexample for the between-detector FROC count gap too. This
case is checked against the canonical evaluator.

## 5. Implementation and computational limits

The implementation is in
[constrained_repairability.py](../src/stats/constrained_repairability.py), with
saved-output adapters and an independent OC-cost diagnostic in
[constrained_diagnostics.py](../src/stats/constrained_diagnostics.py).

For c candidates, g references and e compatibility edges, the uncompressed flow
network has exactly c+g+4 vertices and e+2c+g+3 arcs. It uses O(c+g+e) storage.
The solver groups candidates only if their neighbor sets, initial membership
and active cost agree, using group capacities; each integral group flow can be
expanded onto distinct identical candidates. Initially unselected candidates
with no compatibility edges can be omitted at nonnegative promotion cost.
Their removal from the optimization does not remove them from reported retained
candidate counts or change FROC. These reductions preserve the optimum.

NetworkX 3.6.1 network simplex uses exact integer arithmetic and a cycling-avoidance
rule. Node/edge insertion and witness expansion are deterministic. With P pivots,
a conservative arithmetic-operation bound is O(P*(V+E)+V+E); P has no polynomial
bound promised here. Network simplex is not a new or claimed strongly polynomial
algorithm. Polynomial minimum-cost-flow algorithms exist, but their complexity
must not be attributed to this implementation. Rational scaling can increase
integer bit lengths. Different library versions can choose different optimal
witnesses; exact costs, rather than witness identity across versions, matter.
See the [NetworkX algorithm documentation](https://networkx.org/documentation/3.6/reference/algorithms/generated/networkx.algorithms.flow.network_simplex.html).

The independent exhaustive reference enumerates all 2^c selected sets and all
partial injective assignments. A loose worst-case bound is
O(c*[2*(g+1)]^c), with a hard guard c<=12; even that guard is not a promise that
dense worst cases are practical. The test suite uses genuinely tiny graphs.
SciPy's Hopcroft-Karp cardinality routine takes O(e*sqrt(c+g)) time after sparse
construction. Building geometry takes O(sum_image c_i*g_i) IoU comparisons.
After H,r,M are available, each uniform-cost grid cell is O(1). Bootstrap costs
therefore need weighted count sums, not thousands of large flow optimizations.

The exact solver is for membership oracles, not score-ordered matching, NMS
optimization, adding boxes, spatial cost optimization, or universal clinical
repair. All retained support limitations survive. Five seeds do not identify
architecture-wide laws or variability over new training datasets.

## 6. Prior work and novelty comparison

Primary-source scoping was performed on 7 November and refreshed on 12 November
2026, including searches for
the exact proposed title, minimum-cost detection correction, matching stability,
and conformal/risk-controlled detection through that date. This is targeted
scoping, not an exhaustive systematic review or proof that a formulation has
never appeared. Mathematical validity is established by the proofs above;
originality is not established by failing to find an exact title.

| Prior work | Existing contribution relevant here | Difference and novelty limit |
|---|---|---|
| [TIDE, Bolya et al., ECCV 2020](https://arxiv.org/abs/2008.08115) | Output-based detection error taxonomy and oracle error corrections assessed through AP | Our constraints concern K and FP counts with fixed geometry, not AP. Oracle error diagnosis is already established; we do not claim to introduce it. |
| [LRP/oLRP, Oksuz et al., TPAMI](https://arxiv.org/abs/2011.10772) | Combines localization, FP and FN errors; oLRP minimizes across score thresholds | A K/B membership oracle has a different feasible set. Threshold optimization and decomposed error interpretation are not new. |
| [OC-cost, Otani et al., CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/html/Otani_Optimal_Correction_Cost_for_Object_Detection_Evaluation_CVPR_2022_paper.html) | Optimal transport for image-level detection correction cost, including dummy FP/FN assignments | Closest predecessor. We fix geometry and constrain partial coverage/FP counts relative to historical membership; OC-cost allows pairwise localization/classification correction. Integral cost optimization itself is not a novel contribution. |
| [Kuzucu et al., ECCV 2024](https://arxiv.org/abs/2405.20459) | Critiques calibration evaluation and develops effective post-hoc detector calibration baselines | Our oracle is not a calibrator. Strictly increasing global maps preserve prefixes; this does not rule out broader calibration or feature-dependent reranking. |
| [Andeol et al., 2025 SeqCRC](https://arxiv.org/abs/2505.24038) | Sequential risk control for confidence/localization/classification with calibrated prediction sets; discusses matching and FP limitations | Provides prospective statistical guarantees under sampling assumptions. Our finite-data certificate is annotation-informed and has no future-risk guarantee. Do not claim FP-constrained oracle optimization supplies conformal validity. |
| [Ries et al., COPA 2026](https://proceedings.mlr.press/v329/ries26a.html) | Conformal class/box prediction sets with uncertainty-scaled intervals, including cross-domain experiments | Changes the uncertainty representation and geometry; outside fixed-candidate membership. It is a relevant contemporary alternative, not an evaluated comparator here. |
| [Lee et al., Algorithms 2026](https://doi.org/10.3390/a19050409) | Cost-sensitive LRP with a local threshold-stability objective for deployment decisions | Cost-aware, stable operating-point assessment is also active prior art. Our oracle does not recommend a validated operating threshold. |
| [Prokhorov and Kalinin, October 2026 preprint](https://arxiv.org/abs/2610.19912) (authors report ACCV 2026 acceptance) | Optimal-transport comparison of annotation sets with graded matched/unmatched costs and perturbation analysis | Annotation disagreement and transport-based diagnostics already overlap with the proposed framing. Their agreement metric differs from our conditional matching-count ranking bound; this is not evidence that our elementary bound is original. |
| Standard FROC and current v2 | Exact threshold ceiling, retained recall, geometric matching ceiling and joint uncertainty | New unit costs reduce to H,r,M. They reorganize existing information; the edit-count stability statement adds a conditional sensitivity interpretation. |

We independently implemented the published OC-cost equations using expanded
assignment, checked the authors' public
[implementation](https://github.com/mayu-ot/oc-cost/blob/main/src/extensions/metrics/ot_cost.py),
and used their illustrated lambda=.5,beta=.6 without tuning. The authors assign
beta to dummy-to-dummy flow during optimization, then exclude that flow and
normalize by remaining transported mass. We preserve that detail: setting its
optimization cost to zero would change assignments. Empty/empty images cost zero,
one-sided empty images beta. We use float64 geometry and SciPy assignment rather
than their float32 geometry/MMDetection/POT stack. This is an equation-based
comparison on our cohorts, not a bitwise reproduction of their COCO benchmark.
No superiority claim is made, and TIDE/LRP/SeqCRC were not newly executed.

## 7. Real study results and uncertainty

The [generated numerical report](CONSTRAINED_REPAIRABILITY_RESULTS_V1.md) contains
all target summaries, normalized costs, FROC/geometry comparisons, OC-cost results
and two figures. The [analysis receipt](../results/constrained_repairability_v1/summary.json)
binds the independently versioned inputs and outputs. The original completed v2
analysis was freshly reproduced, including all five tables and all 2,000 joint
draws. The new run used 750 internal images/268 reference boxes and 3,000 external
images/95 reference boxes, five seeds per detector, and budgets
0.125,0.25,0.5,1,2 FP/image. No prediction bundle or annotation was modified.

**Redundancy test:** all 500 run/cohort/target/budget flow optima exactly equal
the closed form; 180 cells are infeasible. Historical maximum matching equals
historical greedy TP in all 20 baseline runs. Thus H,r,M are all recoverable
from already published v2 counts on this study: the new unit-cost surface
introduces no independently measured quantity.

At 0.25 FP/image, equal-run results are:

| Cohort / detector | Target recall | Feasible seeds | Mean minimum edits [marginal 95% interval] | Mean edits/reference |
|---|---:|---:|---|---:|
| RSNA / Faster R-CNN | 25% | 5/5 | 18.8 [0.0,67.2] | 0.070 |
| RSNA / YOLO11s | 25% | 5/5 | 16.0 [0.0,48.8] | 0.060 |
| VinDr / Faster R-CNN | 25% | 5/5 | 22.2 [17.2,27.8] | 0.234 |
| VinDr / YOLO11s | 25% | 1/5 | infinity [infinity,infinity] | infinity |
| VinDr / Faster R-CNN | 50% | 5/5 | 46.2 [36.8,infinity] | 0.486 |
| VinDr / YOLO11s | 50% | 0/5 | infinity [infinity,infinity] | infinity |

The external Faster R-CNN 50% point is feasible in every observed run but has
630/2,000 infinite-cost bootstrap draws. Reporting a finite-only interval would
hide this instability. For external YOLO11s at 25%, 1,993/2,000 draws have infinite
cost. The extended equal-run mean is infinite whenever any selected run is
infeasible; a finite lower bound can coexist with an infinite point for some
other targets. No undefined draws arose in the real cohorts; synthetic draws
with no references explicitly remain undefined. These exploratory percentile
intervals describe the specified resampling procedure, not a finite-sample
coverage theorem for an extended-real population parameter. They are marginal,
not simultaneous, and do not imply a clinical probability of repair.

All external historical FP counts fit even the smallest original budget.
Consequently every feasible external optimum requires zero suppression and its
cost is just the target count minus historical rank. The cost is identical
across all five FP budgets. This is a substantive limitation: unlike a threshold
policy, the oracle can select only reference-compatible low-score boxes and
avoid their surrounding FPs for free. Raw counts across cohorts also reflect
different reference totals and historical feasibility, so lower edit counts
must not be interpreted as better generalization.

**Annotation sensitivity:** the equal-run geometric count gaps are 50.2
internally (260.8 versus 210.6 matches) and 36.8 externally (54.0 versus 17.2).
The theorem guarantees the observed geometric ordering under any at most
50 internal or 36 external shared insertion/deletion edits. For example, after
36 external edits the lower bound on the mean count gap remains 0.8. At 37 edits
the bound ceases to certify the sign; this does not prove that 37 geometrically
realizable edits can reverse it. These are sensitivity budgets, not estimates
that the annotations contain that many errors, and not FROC guarantees.

**Existing correction-cost comparison:** with the published illustrative weights,
mean historical OC-cost is 0.146773/0.148507 internally and 0.039319/0.028291
externally (Faster R-CNN/YOLO11s). All-retained OC-cost is 0.598524/0.532369 and
0.599920/0.518704 respectively. Its different image-weighted objective explains
why low external historical cost can coexist with almost no lesion sensitivity:
the many empty/empty images contribute zero. These are descriptive results,
not new uncertainty estimates or a claim that one metric dominates another.

**Controls and scope:** all 220 imposed output interventions passed their
specified invariants. Monotone powers preserve membership after transporting the
cutoff, FROC and repair cost; permutation preserves full geometry but may change
historical membership; incompatible removal preserves matching ranks and cannot
increase cost. Synthetic tests cover shared reference insertions/deletions,
empty cases, ties, competing assignments, score perturbations, exact-vs-brute
force costs and observation-copy/bootstrap consistency. Neither these controls
nor the mathematical bounds identify the clinical cause of real external shift.

## 8. Relationship to the professor's requirements

| Requirement | What this work can answer | What remains unresolved |
|---|---|---|
| Explain external collapse | Separates limits of cutoff changes, oracle membership/assignment and missing retained geometry | Does not causally identify acquisition, disease population, annotation practice or training factors |
| Explain labels/protocol | Inherits and verifies strict ontology, matching, budgets, floor/cap and original historical policies | Does not establish clinical equivalence between the two datasets' target labels |
| Statistical stability | Joint observation/run bootstrap, explicit infeasibility, all five seeds and all budgets | External patient dependence and new-training-sample variation remain unmeasured |
| Clear scientific contribution beyond comparison | Tests a precise repairability hypothesis and provides falsifiable limitations and a deterministic annotation sensitivity bound | Does not establish sufficient methodological originality for a theorem-centered paper |

The strongest honest framing remains an empirical study of the limits of
threshold transport under a fixed annotation protocol. A theoretical appendix
could eventually clarify the limits, but appending elementary results as a
headline innovation would overstate the contribution. A future weighted repair
study would need an independently motivated action/cost model and evidence of
usefulness beyond matching counts and OC-cost, not merely a more elaborate solver.
No new work is made dependent on radiologists, retraining or relabeling.

## 9. Evidence categories and remaining questions

- **Mathematically proved:** flow/oracle equivalence, geometric infeasibility,
  policy lower bound, uniform-cost closed form, shared-edit count stability and
  its fixed-weight run-average extension.
- **Software validated:** exact-vs-exhaustive costs on small graphs, deterministic
  witnesses, canonical greedy counterexamples, score/tie controls, output removal,
  observation-copy reconstruction and resampling treatment of infinity/undefined.
- **Empirical:** only the saved study's cohort/run/target/budget results and
  imposed output controls; these are not independent external repair tests.
- **Not established:** a new flow algorithm, new integrality mathematics,
  clinical correction costs, causal domain-shift mechanisms, conformal guarantees,
  or publication-level novelty of the theorem package.
- **Research-dependent:** whether a defensible restricted policy/action space or
  independently justified heterogeneous cost model yields useful information that
  existing diagnostics miss. The present work deliberately does not manufacture
  that evidence or claim the question is solved.
