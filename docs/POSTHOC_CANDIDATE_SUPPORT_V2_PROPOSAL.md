# Proposed retained-candidate sensitivity v2 — NOT EXECUTED

This is a separately versioned post-hoc proposal, not an amendment to v1 and
not authorization to start inference. Its purpose is to test sensitivity to
candidate truncation after the external results are known.

Proposed changes: collection floor from 0.00001 to 0.000001; maximum retained
detections per image from 100 to 300. Keep exact checkpoints, complete internal
and external cohorts, preprocessing, numerical paths, NMS, target ontology,
thresholds and matching conventions fixed. Maintain v1 AP at maxDets 100 as a
reference; any cap-300 AP is a separately named task/metric sensitivity. The
two changes together cannot distinguish floor from cap effects; if separate
attribution is needed, declare the factorial arms before collecting outcomes.

All five checkpoints per detector and both authorized complete cohorts are
required. New bundles, source provenance, runtime identity and aggregate
reports must use new namespaces. A small inference timing/memory preflight
on the RTX 4060 Laptop 8GB GPU is required; use AMP, batch one and streamed
data. Measure disk/memory/elapsed requirements rather than inventing estimates.
Preserve all previous outputs and adverse runs; do not select improved seeds,
external thresholds or target combinations after seeing v2 performance.

The scientific reason is concrete: v1's upper external budgets lack support
for YOLO seed 137, and many Faster R-CNN images hit the cap. Extra candidates
could change the high-budget observations. It cannot establish a full frontier
or repair ontology/population mismatch, and it might not change conclusions.
The v1 low-budget joint change results remain conditional on v1 support.
Separate user authorization is required before any GPU collection, as stated
in the research request's Phase Six execution rule.
