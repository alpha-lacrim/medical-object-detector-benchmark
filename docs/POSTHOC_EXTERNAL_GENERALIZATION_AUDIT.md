# Research audit: external generalization v1

Audit begun 2026-10-28; resumed 2026-10-29 at unchanged baseline
`801a6c90afa480351a9e0d72ca7709b47da95e2e`. Pre-existing README Wget edits,
untracked project/orchestration files and local-only state are preserved.
The complete pasted task is the authorization; this is not Batch 54.

## Evidence baseline and implementation map

| Component | Actual implementation | Verified contract / remaining scope |
|---|---|---|
| Internal preparation | `src/data/prepare.py`, canonical COCO targets through `src/stats/run_statistics.py:load_coco_targets` | Frozen annotations/split hashes; patient grouping from NIH mapping. No new raw RSNA conversion. |
| External annotation/preprocessing | `src/data/prepare_vindr.py:build_targets`, `targets_to_coco`, `decode_image`, `geometry_check` | Exact local `Lung Opacity`, all official images, source xyxy without +1, native-size min-max PNG. New preflight exactly reconciles strict geometry from source CSV. |
| Native inference and coordinates | `src/evaluate_vindr_external.py`, including `restore_native_bounds` and `verify_boundary_repairs`; frozen operation config | Native detector preprocessing/NMS, mandatory AMP, bounded one-ULP correction with raw evidence. Existing receipts/hash bindings checked; no new GPU inference. |
| Shared AP | `src/meddet_benchmark/coco_evaluation.py:evaluate_coco` | Official COCO matches, all areas, common 0.001 floor, cap 100; target ties are COCO's own convention. |
| Operating-point matching | `src/meddet_benchmark/evaluation.py:match_image` | Stable descending score, highest-IoU available same-class target, >= score/IoU, no reuse. |
| Exact FROC | `src/analyze_exact_score_froc.py`; `src/stats/transportability.py:FrocCache` | Distinct score groups enter together; fixed-budget observed sensitivity, no interpolation or extrapolation, 0.00001 floor. |
| Threshold transport | `src/evaluate_vindr_external.py:compute_metrics`, frozen `threshold_transport` config | Historical 0.69/0.05 primary; 0.70/0.01 five-validation-run sensitivity. No external tuning. |
| Five-run aggregation | `src/stats/run_vindr_statistics.py:prepare_dataset`, `summarize_values` | Five retained runs per detector, equal run means, explicit undefined values. |
| Resampling | `src/stats/paired.py`; `src/stats/transportability.py:bootstrap` | Shared observations within cohort; known internal patient clusters, external images; independently sampled detector runs. Canonical caches tested against explicit copies. |
| Existing transport inference | `src/stats/run_vindr_statistics.py:verify` | Separate dataset intervals. No existing interval for cross-domain change; therefore new same-checkpoint dependence handling is necessary. |
| Freeze/editorial archive | `scripts/verify_frozen_external.py:historical_editorial_view` | Redirects only two editorial baseline records to their exact archived bytes, never scientific inputs. |
| Claim/artifact provenance | `scripts/verify_paper_claims.py`, `scripts/verify_scientific_artifacts.py` | Claims bound to generated cells/JSON and semantic guards; original scientific and later publication inventories are distinct. |

Independently executed before new outcomes: 38-file freeze, original 72-artifact
inventory (346 present inputs, zero unavailable, 201 references), 427 claims and
all semantic guards, and original statistical hash/saved-draw replay (130
bindings, 44 interval rows). Detailed commands are in the checkpoint; execution
logs are under `tmp/external-generalization-v1/`. These checks do not claim new
training, raw-image decoding or full original bootstrap recomputation.

## Confirmed prior analyses and scientific limitations

Original external matching, threshold definitions and canonical coordinate
contracts match internal definitions. Preprocessing policy is shared but image
appearance, resolution, source population and target semantics differ. Native
model transforms differ by detector. Score supports are matched by endpoint;
AP and lower-floor FROC intentionally use different retained populations.
Historical internal YOLO FP32 versus external bfloat16 is already investigated
in the separately retained five-run numerical-path sensitivity. That evidence
narrows the precision concern without proving equivalence or a dataset-only
effect. Do not repeat that inference or replace historical internal values.

Original separate-dataset bootstrap respects observation/run dependence for
its declared estimand. It cannot be subtracted as independent intervals to
obtain a valid same-checkpoint cross-domain interval. The new analysis uses
one within-detector run draw across domains, separate cohort observation draws,
and independent draws between detector families. Unknown external patient
dependence remains unresolved.

Candidate-floor exhaustion for an external YOLO run and substantial Faster
R-CNN cap saturation constrain the observed frontier. Existing conservative
missing-support bounds do not cover cap effects and are not confidence bounds.
New retained-output diagnostics cannot observe proposals hidden by native
NMS, floors or caps. No causal attribution follows from an error category.

The release documentation distinguishes local patterns and global diagnoses.
It supplies no validated cross-dataset instance-equivalence rule for merging
Lung Opacity, Consolidation and Infiltration. Non-target overlap accounting is
executable; broader-target AP remains pending expert review. This is a
scientific limitation, not an implementation blocker for the authorized work.

## Bugs distinguished from limitations

The first draft of the **new** annotation loader incorrectly joined raw IDs
to canonical PNG filenames and attempted to treat `No finding` sentinels as
localized boxes. The resumed implementation explicitly applies the frozen
filename convention and validates/excludes nonlocal sentinel rows. Original
source bytes, frozen adapter and historical outputs are untouched. Preflight
now passes 138 input bindings, exact strict geometry, every localized box,
and sentinel/duplicate checks. No historical scientific bug has been found.

Synthetic tests independently exercise exact boundaries, assignment competition,
FP/reference reconciliation, duplicate predictions/annotations, alternative
class overlaps, empty outputs, negatives, candidate limits, weighted AP,
patient multiplicities, cross-domain run coupling and undefined draws.
Initial focused suite (new tests plus existing transportability) passes 50
tests. Final execution/test outcomes will be recorded in the verification
record, not inferred from this baseline audit.

## Executable work and remaining prerequisites

All required retained bundles, annotations, checkpoint hashes and patient keys
are locally available under the recorded access authorization. CPU error,
overlap, weighting, joint-bootstrap and support analyses are executable.
No large download or new model is needed. Primary original artifacts remain
immutable; new versioned outputs carry their own inputs and hashes.

Expert instance/ontology adjudication is required before alternative-task AP.
Expanded candidate collection needs the separate post-hoc inference proposal,
authorization, retained checkpoints and an 8GB GPU resource gate. Neither is
silently substituted for the frozen experiment. Literature and interpretation
are completed only after actual new results are checked.
