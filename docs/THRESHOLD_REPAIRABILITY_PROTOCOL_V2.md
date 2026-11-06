# Threshold repairability v2: computational protocol

6 November 2026. Exploratory follow-up authorized by the user's request to
implement the repairability direction and update the paper. The external v1
point estimates and original study outcomes were already known. This protocol
specifies new computations and output interventions before executing them; it
is not public preregistration of the original study or a confirmatory analysis.

## Scope and fixed evidence

Use both complete saved test cohorts, all five original checkpoints per detector
and every original FROC budget. Inherit the exact target mapping, matching IoU,
native NMS, candidate floor/cap and primary historical cutoffs from the frozen
external protocol. Internal candidates are the existing exact-score v4 bundles;
external candidates are the existing original external bundles. No new model
execution, training, threshold selection, calibrated model, ontology expansion
or image interpretation is authorized or needed by this analysis.

Replay the baseline FROC endpoints, retained-floor recall/FP burden and source
historical counts. Check that the historical cutoff on the lower-floor bundles
reproduces the source operating counts before describing that point as part of
the same prediction set. External geometric counts must reproduce the previous
diagnostic census-positive results. Preserve v1 and all original artifacts.
Keep identifiers, prediction arrays and bootstrap draws in the ignored private
tree. Public outputs contain only aggregate run/budget/perturbation statistics.

## Main estimands and invariance scope

For each fixed candidate set, `Rb` is maximal greedy-matched recall over exact
score cutoffs satisfying FP/image <= b; `Rall` admits all retained predictions;
`G` is maximum-cardinality same-class bipartite matching at the same IoU, divided
by reference-box count. Report the identity

```
1 = Rb + (Rall - Rb) + (G - Rall) + (1 - G).
```

The four terms are the cutoff ceiling, current-order FP-budget barrier,
assignment gap and unavailable retained geometry. They are an aggregate recall
accounting identity, not causal fractions of the cross-domain loss. The
candidate geometry ceiling is an annotation-informed bound, not deployed recall.
`Rb` is a per-run optimistic test-set envelope; its mean is not performance of
one common threshold or an ensemble. No maximizing score coordinate is exported.

A strictly increasing global score map preserves prediction prefixes and ties,
so cannot raise `Rb` when the candidate set, matching, tie handling and all other
postprocessing are held fixed. Feature-dependent rescoring, changed ties, NMS,
boxes, ontology or collection settings are outside that statement. No new
mathematical theorem or universal impossibility of calibration is claimed.

Also report historical recall/FP burden, the signed difference `Rb - R0`, and
the fraction of selected runs for which the historical policy satisfies the
budget. Infeasible historical policies and resampling draws stay included;
signed differences are not automatically nonnegative recovery opportunities.
Report floor limitation and cap saturation. No extrapolation beyond retained
candidates or clinically acceptable FP tolerance is claimed.

## Joint uncertainty

Use 2,000 percentile bootstrap draws with the configured seed and marginal 95%
intervals. Sample known internal patient clusters and external released images
independently by cohort. Share each cohort's observation weights across all
detectors, runs, budgets and components. Sample runs independently within each
detector; reuse the selected checkpoint multiplicities across internal and
external cohorts. Recompute each nonlinear budget endpoint before averaging
selected runs. Preserve within-image lesion competition and all source boxes.

Save the joint draws privately. Estimate per-cohort endpoints, within-cohort
detector contrasts, each detector's external-minus-internal changes and their
difference from the same draws. Do not subtract independently calculated CI
limits. Record finite/undefined draw counts without retrying or imputing. No
p-value family, simultaneous ordering or equivalence test is introduced. The
primary presentation budget is 0.25 FP/image, as in the prior post-hoc analysis;
all original budgets remain available. Intervals condition on the training
cohort, recipes, five checkpoints, source references and retained support.
Unknown external patient dependence remains a limitation.

## Controlled output perturbations

Apply the following separately to each complete saved run/cohort. Never rerun
NMS, apply an old numerical score floor after transforming scores, or change
the source files. Keep image membership, targets and native coordinates fixed.
Re-evaluate transformed outputs at floor zero with the original cap; their
membership was already fixed before transformation.

1. Global score powers 0.5 and 2.0. Require identical full FP/recall curves and
   geometry, including tied-score groups. Historical numeric-cutoff behavior
   may change. Any lost score-order resolution or invariant violation fails
   the integrity gate; it is not silently treated as a valid monotone control.
2. Permute scores among 25%, 50% and 100% of retained candidates. Preserve the
   global score multiset and every box. Use three fixed replicates per level,
   with identities/seeds determining the RNG, never performance. Require
   unchanged geometric coverage. Do not require a particular FROC direction.
3. Remove 25%, 50% and 100% of individually compatible candidates (same-class
   IoU >= canonical match IoU with any reference). Use three nested removal
   orders per run. Maximum geometric coverage cannot increase; complete removal
   must leave zero geometric coverage. Ranked recall need not decline at every
   level because redundancy and greedy assignment can change.
4. Remove individually incompatible candidates with the same levels/replicates.
   They cannot match any reference under the fixed rules. Require unchanged
   geometry and nondecreasing budget recall. This is a label-informed positive
   control for FP removal, not an implementable prediction filter.

Use the same observation denominators throughout. Report every run, budget,
strength and replicate, including zero effects and improvements under score
permutation. Select floor(fraction * eligible candidate count) candidates;
derive each random order without the strength in its seed so removal sets nest.
Aggregate replicate outcomes within each trained run before
equal-run averaging. Replicates are imposed software perturbations, not new
patients or training runs. The controls receive descriptive changes and
invariant checks, not clinical significance claims or bootstrap CIs. None
identifies which acquisition, population or annotation factor caused real shift.

## Verification, runtime and interpretation gates

Require original input hashes, complete run identities, exact baseline replay,
the accounting identity for points and finite draws, and all specified control
invariants. Use synthetic unit cases including score ties, competing matches,
infeasible historical policies, empty outputs and zero-target resampling.
Compare with a direct image-copy reconstruction on small fixtures. Require
fresh exact numerical replay of tables/arrays before manuscript integration.

Use CPU-only execution and process perturbations one run at a time. The smoke
mode checks both cohorts with the configured small draw count and only the first
run's controls; it writes no accepted results. The full run stops on a projected
one-hour computational overrun or integrity failure rather than selecting a
favorable subset. Source/config/protocol bytes are bound before computation and
checked at the end. Output namespaces refuse overwrite.

Compare interpretation with exact FROC and published TIDE/LRP concepts. FROC
already gives `Rb` and `Rall`; the audit organizes their implications and adds
the geometric ceiling, paired uncertainty and controlled validation. It is
not a new leaderboard metric or an empirical claim of superiority over those
methods. Report this incremental contribution honestly, retain the original
clinical/ontology limitations, and leave final publication novelty to review.
