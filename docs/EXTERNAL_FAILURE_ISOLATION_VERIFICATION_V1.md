# Controlled external failure diagnostic: interpretation and verification

2026-11-05. **VERIFIED execution; EXPLORATORY findings; overall causes UNRESOLVED.**

## Baseline and continuation boundary

The resumed checkout was `main` at
`b49569d6b7d87e38674d42769ea2412d504b3e84`, with the existing upstream unchanged.
README and graph outputs were already modified, and the diagnostic config,
protocol, collector, analyzer, renderer, registration script and tests were
already untracked. Their completed private collection was present even though
the local handoff still described collection as in progress. No new GPU
inference, training, download, commit or push was performed in this continuation.

The earlier [generalization package](POSTHOC_EXTERNAL_GENERALIZATION_VERIFICATION.md)
already implemented the original research request. A fresh complete CPU replay
reproduced its 15 tables, all point estimates and all 2,000 joint bootstrap
draws exactly. Its summary remains SHA-256
`a8f39dd5b22683f35e2363b39e9415d41b580c85bfd5af389eab1647df999106`.
That result is independently rechecked here, not inferred from the handoff.

The [subsequent diagnostic protocol](EXTERNAL_FAILURE_ISOLATION_V1.md) was
written before its collection but after the original external outcomes were
known. The collector's receipt records completion of all ten runs in about
762 seconds on the pinned CUDA environment. This is an existing execution
record, not a new timing measurement. Its source/config/protocol/test bytes
remain hash-bound and were not edited during this continuation.

## What was executed and independently checked

Completed the existing CPU analyzer and renderer, then replayed all three CSVs
and all 2,000 paired draws per detector exactly. The accepted diagnostic summary
is [summary.json](../results/external_failure_isolation_v1/summary.json), SHA-256
`2cced016913cf2c75e89f77cf435ac18c9b358b228679340f8ddbaf2d827945a`.
The [generated report](EXTERNAL_FAILURE_ISOLATION_RESULTS_V1.md) contains every
arm, including unchanged and adverse outcomes. The aggregate figure was
visually inspected: labels, intervals and legends are legible and unobscured.

Added [a read-only verifier](../scripts/verify_external_failure.py) and
[seven synthetic checks](../tests/test_external_failure_verification.py).
The verifier checks exact detector/seed and arm inventories, observation order,
class IDs, strict native collection floors, caps, stable score order and actual
saved arrays. It independently reproduced 1,680 historical-baseline image/run
comparisons and 5,040 nested-retention comparisons and checked 504 private pixel
artifact hashes. This avoids treating receipt success flags as independent
evidence. It loads no model and exposes only aggregate check counts.

The first new test run had three fixture failures because synthetic prediction
arrays are read-only. Copying those synthetic fixtures before deliberate
tampering resolved them; no scientific source, result or assertion was weakened.
The focused verifier/diagnostic/registration suite then passed all 22 tests.

## Scientific findings and interpretation

All numerical values below come from the generated paired-change and AP-floor
tables. Equal-run means include all five checkpoints per detector. Diagnostic
recall and coverage use all 84 strict-positive images / 95 boxes. Negative
controls are a fixed random sample of 84 strict-negative images.

| Question | Executed evidence | What follows and what does not |
|---|---|---|
| Does collection hide geometrically suitable candidates? | Lowering the floor from 1e-5 to 1e-6 increases YOLO maximum one-to-one IoU-0.50 coverage from 0.181053 to 0.324211; paired change 0.143158 [0.082605, 0.210538]. Increasing its cap alone changes neither coverage endpoint. | Some absence in the originally retained set is collection-dependent. This is an annotation-informed geometric ceiling, not score-ranked recall or clinical correctness. |
| Do the tested retention changes rescue historical recall? | Historical recall is identical across baseline, lower-floor, higher-cap and combined arms for both detectors. Faster R-CNN combined changes increase IoU-0.50 coverage by 0.025263 [0.006186, 0.052002]. | Added low-score geometry does not rescue the frozen operating thresholds on this cohort. This does not identify the source of low scores or exclude upstream proposal/NMS failures. |
| Does the fixed header window establish improved recall? | Faster R-CNN recall changes by 0.006316 [0.000000, 0.024742]; YOLO by 0.000000 [-0.008791, 0.008696]. Faster R-CNN geometric coverage changes by 0.031579 [0.002149, 0.065997]. | Geometry can change while recall evidence remains inconclusive. Zero-containing intervals are not equivalence tests; this particular header mapping is not validated vendor display processing. |
| Does the AP evaluation floor explain the collapse? | On all 3,000 images with unchanged saved predictions, lowering evaluation floor from 0.001 to 0.00001 changes mean AP50 from 0.002505098 to 0.002697961 (Faster R-CNN), and 0.000500694 to 0.000887913 (YOLO). | Evaluation filtering affects reported AP, but these absolute values remain very low. This isolates a filter effect on saved outputs, not a causal fraction of the domain gap. |

The geometric matching is deliberately a maximum-cardinality bipartite bound.
It does not replace the original score-ordered greedy operating matcher or
official COCO matching. Consequently it must not be equated to the earlier
per-target availability diagnostic, which ignores assignment competition.

Positive and negative images are resampled separately, with the same image and
checkpoint multiplicities across arms within each detector. All sampled
positive images have targets, so recall/coverage denominators remain positive
in every draw; the fixed-size negative sample also has a positive denominator.
The two detector analyses report marginal within-detector effects only. Their
RNG streams must not be repurposed as independently sampled between-detector
contrasts. No such contrast or simultaneous interval claim is made here.

Negative-control FP/image is conditional on the chosen sample. The enriched
diagnostic cohort is not used to report full-population AP or precision.
Only the separate AP-floor control uses all official external images.
Changing external controls after known outcomes remains exploratory and does
not validate a deployment rule. No class merge, recalibration, threshold
selection, run exclusion or primary-artifact replacement occurred.

## Reproduction and actual check outcomes

Run in the repository root using `.venv/Scripts/python.exe`; set the authorized
dataset location in PowerShell before commands that require it:

```powershell
$env:VINDR_CXR_ROOT = (Resolve-Path data/raw/vindr-cxr).Path
```

The table lists arguments after that Python executable. Test invocations used
fresh `--basetemp=tmp/pytest-...-20261105` paths and `-p no:cacheprovider`.
These CPU commands do not collect predictions or overwrite the frozen study.
The first diagnostic analysis refuses existing output; use `--replay` now.

| Executed command | Actual result |
|---|---|
| `-m src.stats.run_external_generalization --config configs/external_generalization_v1.yaml --mode verify` | PASS: 138 inputs, 15 tables, saved-draw intervals |
| Same command with `--mode replay` | PASS: complete recomputation, all 2,000 draws exactly equal |
| `-m src.analyze_external_failure --config configs/external_failure_isolation_v1.yaml` | PASS: first accepted CPU analysis; three CSVs, summary, private draws/counts |
| Same command with `--replay` | PASS: three tables and 2,000 draws per detector exactly equal |
| `-m scripts.verify_external_failure --config configs/external_failure_isolation_v1.yaml` | PASS: ten runs, 168 images, 1,680 baseline / 5,040 retention comparisons, 504 pixel hashes |
| `-m scripts.report_external_failure --config configs/external_failure_isolation_v1.yaml` | PASS: generated report, figure and build receipt; figure visually inspected |
| `-m pytest tests/test_external_failure_verification.py tests/test_external_failure.py tests/test_external_failure_manifest.py -q` | PASS: 22 tests after the synthetic-fixture correction |
| `-m pytest -q` | PASS: 510 passed, one expected metadata-only skip, seven licensed-data tests deselected |
| `-m pytest -q --run-scientific` | PASS: 517 passed, one expected skip |
| `-m ruff check src tests scripts` | PASS |
| `-m ruff format --check src tests scripts` | PASS: 148 files already formatted |
| `-m scripts.verify_paper_claims` | PASS: 478 claims and all 42 semantic guards |
| `-m scripts.export_paper_trace --manifest report/paper_claim_sources.yaml --output docs/SUBMISSION_NUMERICAL_TRACE.csv` | PASS: 478 verified bindings |
| `-m scripts.verify_scientific_artifacts` | PASS: original 72 artifacts, 346 inputs present, zero unavailable, 201 result references |
| `-m scripts.verify_scientific_artifacts --manifest results/publication_artifact_manifest.json` | PASS: 112 artifacts, 996 inputs present, zero unavailable, 212 result references |
| `-m scripts.verify_frozen_external --mode freeze` | PASS: all 38 original frozen files |
| `-m scripts.verify_frozen_external --mode statistics` | PASS: 130 bindings and 44 saved-draw interval rows; not fresh original-cohort bootstrapping |
| `-m scripts.check_bibliography --bibliography report/references.bib --manuscripts report/paper_draft.md report/report.md report/Manuscript_FasterRCNN_vs_YOLO11s_LungOpacity.md` | PASS: 45 entries; 24/19/27 cited keys resolve |

The frozen-statistics wrapper supplies the exact archived editorial context to
the legacy verifier. Running the legacy entry point against the living paper
would confuse editorial changes with changes to original scientific inputs.
Portable success alone is not the licensed-data replay reported separately.

The complete final suite invocations were:

```powershell
rtk .\.venv\Scripts\python.exe -m pytest -q --basetemp=tmp/pytest-portable-generalization-final-20261105 -p no:cacheprovider
rtk .\.venv\Scripts\python.exe -m pytest -q --run-scientific --basetemp=tmp/pytest-scientific-generalization-final-20261105 -p no:cacheprovider
```

Final working-tree checks found no restricted image identifiers in 30 changed
or untracked public text files, including graph outputs, using all 3,000
official external identifiers as the local comparison set. All 181 private
diagnostic files are ignored, and no files under the restricted raw/processed
VinDr roots are tracked. This targeted check supplements aggregate-output
review; it is not a claim to detect every possible privacy issue.
`rtk git diff --check` passed. The graph was refreshed with
`rtk graphify update .` after the code changes.

After exact replay and visual review, the existing one-time command
`-m scripts.register_external_failure --config configs/external_failure_isolation_v1.yaml --manifest results/publication_artifact_manifest.json`
added six public artifact records. A structural comparison with Git HEAD
confirmed that all previous 106 records, 468 claims and 40 guards are unchanged;
the original scientific manifest is byte-identical. No stale hash was refreshed.

## Manuscript, prior art and remaining limits

Added Methods 3.10, Results 4.11, bounded Discussion/Limitations text and
Supplement S12. Ten new numerical bindings and two semantic guards refer to
generated evidence. Existing scientific numbers and claims are preserved.
The current PDF/build receipts remain the reviewed 2026-10-29 snapshot; they
do not incorporate this Markdown extension and require refresh before submission.

The [earlier interpretation](POSTHOC_EXTERNAL_GENERALIZATION_INTERPRETATION.md)
provides the research-question table and primary-literature assessment.
Primary publisher/proceedings pages were revisited for external generalization
([Zech et al.](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683)),
detector calibration ([Kuzucu et al.](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/03148.pdf)),
benchmark variability ([Bouthillier et al.](https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf))
and label-shift assumptions ([Lipton et al.](https://proceedings.mlr.press/v80/lipton18a.html)).
Window semantics were checked against the
[DICOM standard](https://dicom.nema.org/medical/Dicom/2024c/output/chtml/part03/sect_C.11.2.html)
and [pydicom documentation](https://pydicom.github.io/pydicom/stable/reference/generated/pydicom.pixels.apply_windowing.html).
These establish context and implementation definitions, not novelty or clinical
validity of the present results. No new bibliographic claim was invented.

For the supervising professor: the combined package supports an empirical
transportability contribution with measured failure categories, annotation
overlap, prevalence weighting, checkpoint-coupled changes and bounded control
experiments. It does not identify the overall cause of external collapse.
Expert ontology/instance adjudication, the separate full-cohort extended-support
study, unknown repeated external patients, author ethics/journal decisions and
submission-version selection remain unresolved. All supported CPU analyses
have been executed; no new GPU experiment is claimed by this continuation.
