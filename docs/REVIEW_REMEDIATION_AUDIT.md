# Review Remediation Audit

Audit date: 2026-08-28  
Audit boundary: repository state at `main` / `df2f35f43170699cca32540a283a50caa1764aee`, plus read-only inspection of the local ignored data/checkpoints and the public GitHub v1.0.0 release.  
Change boundary: audit only. No scientific code, result table, figure, checkpoint, or manuscript claim was changed.

## Post-audit calibration addendum (2026-08-30)

The historical R6/R15 rows below describe the repository at the audit boundary.
They are now remediated by the uniform Batch 33 v2 calibration path. The source
contains no seed-value branch; the Phase 5 run grid is discovered dynamically;
and every run uses the same matching, class-stratified binning, weighting,
minimum-cell, and floor logic. The prospective-sounding seed-271 expectation
was removed from H6; the manuscript reports only the observed result.

R6 now has explicit versioned per-run support diagnostics and a predeclared
3/5/7-bin by 1/4/8/16-minimum sensitivity grid. The original 5-bin/minimum-8
setting remains flagged. Confidence-floor sensitivity is also reported because
the 0.001 floor materially determines the emitted population. Canonical current
evidence is `calibration_summary_v2.csv`, `calibration_support_v2.csv`,
`calibration_sensitivity_v2.csv`, the four v2 figures, and
`results/logs/phase33_calibration_support_v2/summary.json`. The D-ECE comparison
is descriptive and expressly excludes missed-target, exam-level, and clinical-
risk calibration; it remains separate from any valid probability-based DCA.

## Adjudication summary

The labels below judge the issue as stated, not the authority of the previous review. A confirmed observation may already be disclosed adequately in the manuscript; the final column distinguishes an error requiring remediation from a limitation that is already bounded correctly.

| ID | Issue | Status | Repository adjudication and exact evidence |
|---|---|---|---|
| R1 | Primary confidence intervals and permutation p-values target different randomness | **CONFIRMED** | The clean bootstrap resamples NIH patient groups and paired seed indices (`docs/STATISTICAL_ANALYSIS.md:L40-L55`; `src/stats/paired.py:L160-L192`, `L681-L701`). The permutation test swaps detector labels by patient group while holding the observed checkpoints fixed (`docs/STATISTICAL_ANALYSIS.md:L66-L76`; `src/stats/paired.py:L703-L725`, `L743-L749`). These are deliberately different estimands: the CI includes empirical training-seed variation; the p-value is checkpoint-conditional. The methods document already says so, but tables and prose should never imply that they are two interchangeable summaries of one null distribution. |
| R2 | Fixed-threshold precision has a seed-aware CI crossing zero while its checkpoint-conditional Holm p-value is small | **CONFIRMED** | The source row is `results/tables/statistical_clean_comparison.csv:L2`: Faster R-CNN minus YOLO11s `-0.102426`, 95% CI `[-0.252889, 0.080165]`, raw p `0.00039992`, Holm p `0.00199960`. The manuscript reproduces it at `report/paper_draft.md:L700` and explains the differing randomness at `L708-L715`. This is not an arithmetic contradiction; it is a consequence of R1. It is nevertheless easy to misread, and the seed-aware interval is additionally affected by R13. |
| R3 | Existing DCA uses raw detector confidence as the numerical threshold probability | **CONFIRMED** | An exam is flagged by maximum emitted box score (`src/clinical/decision_curve.py:L300-L326`), and net benefit uses `tau/(1-tau)` (`L257-L278`). `results/tables/dca_summary.csv:L1-L3` records `raw_detector_score_used_as_nominal_threshold_probability`. The limitation is explicit in `docs/DCA_ANALYSIS.md:L112-L123`, `docs/LIMITATIONS.md:L165-L175`, and `report/paper_draft.md:L395-L414`, `L906-L912`. Therefore the numerical calculation is real, but the manuscript already limits it to nominal internal scenario analysis rather than calibrated clinical utility. |
| R4 | `REPORTING_CHECKLIST.md` was generated against an older manuscript state | **CONFIRMED** | `docs/REPORTING_CHECKLIST.md:L4-L5`, `L35-L36`, `L89`, and `L150-L151` say the paper draft/abstract does not exist. `report/paper_draft.md:L7-L35` contains an abstract. Git history dates the checklist commit `d992cf8` at 04:02 and the paper commit `ce166a5` at 04:40 on 2026-08-28. This is stale documentation, not a scientific-result error. |
| R5 | README/canonical-document hierarchy is ambiguous or stale | **CONFIRMED** | Governance is clear for project memory: `PROJECT_SPEC.md` is the static source of truth, `CODEX.md` the living state, `HANDOFF.md` the append-only log, and `BATCHES.md` the sequence (`AGENTS.md:L22-L25`; `CODEX.md:L1046-L1051`). Scientific-document precedence is not: README still calls `report/report.md` the completed 12-section study (`README.md:L8-L12`), while `CODEX.md:L1074` calls it the final course report and `CODEX.md:L1106` calls `report/paper_draft.md` the publication-style manuscript “without replacing” it. The checklist also routes only to the older report. Dependency authority is similarly split between `README.md:L85` (`requirements.txt`) and the CI's `uv.lock`/`pyproject.toml` path. Results remain traceable, but the submission-facing hierarchy is stale/ambiguous. |
| R6 | D-ECE support may be sparse | **PARTLY CONFIRMED / OVERSTATED** | The full grid has `5^5 = 3,125` possible cells and excludes cells with fewer than eight detections (`src/stats/calibration.py:L310-L380`; Küppers settings are recorded in `configs/calibration.yaml`). Per-seed source rows `results/tables/calibration_summary.csv:L2-L11` contain only 68-354 nonempty and 15-169 contributing cells. YOLO11s seed 137 is the material edge case: 394 predictions, 214 included (54.3%), and 15 contributing cells (`L9`). Other seeds retain 81.9%-98.3% of predictions. Thus multivariate cell occupancy is sparse, especially for seed 137, but “D-ECE has little support everywhere” is overstated; counts and inclusion fractions are already emitted. |
| R7 | Exact trained checkpoints are not committed or released | **CONFIRMED** | Git tracks only `results/checkpoints/.gitkeep`; `.gitignore:L43-L50` excludes `*.pt`, `*.pth`, `*.ckpt`, and checkpoint directories. `README.md:L60-L67` says checkpoints are intentionally ignored/regenerable, and `docs/REPORTING_CHECKLIST.md:L77`, `L131` identifies the availability gap. The ten final best checkpoints are present locally at ignored paths, so the issue is distribution rather than local absence. A read-only `gh release view v1.0.0 --repo Alpha-lacrim/medical-object-detector-benchmark --json assets,...` query returned `"assets":[]`; the public release exists but contains no attached model asset. |
| R8 | CI is software QA rather than end-to-end scientific regeneration | **CONFIRMED** | The sole workflow is `.github/workflows/ci.yml`. It runs lock validation, CPU dependency sync, Ruff, unit tests, and deterministic smoke on Ubuntu/Windows (`L18-L33`). It does not acquire DICOM data, train ten models, run GPU inference, regenerate tables/figures, or compare artifact hashes. README documents those operations as manual commands. CI is appropriate software QA, not proof of end-to-end scientific reproduction. |
| R9 | External validity, subgroup/fairness analysis, and prospective validation are absent | **CONFIRMED** | `docs/LIMITATIONS.md:L291-L303`, `report/paper_draft.md:L839`, `L853-L866`, `L953-L958`, and checklist rows `docs/REPORTING_CHECKLIST.md:L67`, `L71-L72`, `L92`, `L116`, `L185`, `L191` explicitly record these absences. This is a real scope limitation that is already disclosed, not a hidden omission or a reason to reinterpret the internal estimates as external evidence. |
| R10 | PR/FROC/Pareto/threshold analyses use different seed counts from the five-seed clean analysis | **CONFIRMED** | The manuscript's protocol ledger says clean nonconditional endpoints use five seeds, PR/threshold/FROC/Pareto remain frozen to seeds 17/42/137 (`n=3`), and robustness/acquisition/Grad-CAM use seed 17 (`report/paper_draft.md:L268-L281`). `docs/HYPOTHESES.md:L14-L19`, `docs/PARETO_ANALYSIS.md:L5-L10`, `results/tables/selected_operating_points.csv:L2-L3`, and `results/tables/froc_operating_points.csv:L2-L11` agree. The difference is disclosed; it limits cross-analysis synthesis but is not a numerical inconsistency. |
| R11 | Threshold calibration presents `beta = sqrt(C_FN/C_FP)` as an actual clinical FN:FP cost mapping | **CONFIRMED** | `docs/DECISION_LOG.md:L118-L131`, `docs/THRESHOLD_CALIBRATION.md:L24-L31`, `src/stats/threshold_calibration.py:L218-L238`, `L659`, and `report/paper_draft.md:L307-L324` label `beta^2` as an assumed FN:FP cost ratio. F-beta is a weighted harmonic mean in which beta controls recall relative to precision; it does not by itself define expected clinical loss, incorporate prevalence, or calibrate patient outcome/treatment utility. The repository correctly calls the scenarios hypothetical and nonclinical (`docs/THRESHOLD_CALIBRATION.md:L84-L98`; manuscript `L549-L551`, `L772-L774`), but that caveat does not validate the exact cost-ratio identity. Relabel as recall-weight scenarios unless a decision-theoretic derivation is supplied. |
| R12 | The XAI “data-randomization” test is input-pixel shuffling, not the Adebayo training-label test | **CONFIRMED** | Config says `spatial_pixel_vector_permutation_without_replacement` (`configs/xai_sanity.yaml:L35-L36`); code permutes pixel vectors within each image (`src/explainability/sanity_checks.py:L443-L452`); trained weights remain unchanged (`docs/XAI_SANITY.md:L48-L52`; manuscript `report/paper_draft.md:L429-L435`). Adebayo et al.'s data-randomization test permutes training labels and retrains the model. The result remains a valid input-structure perturbation check, but it must not be named or credited as the Adebayo data-randomization sanity test. The project's all-weights-at-once parameter test is also narrower than Adebayo's cascading/independent variants. |
| R13 | Same-number seeds across detectors are not demonstrated matched stochastic blocks | **CONFIRMED** | `configs/evaluation.yaml:L4`, `L82-L136` applies the same integer labels. Each training program separately seeds its own process: Faster R-CNN at `src/models/train_faster_rcnn.py:L1243-L1252` plus its PyTorch loader at `L205-L223`; YOLO at `src/models/train_yolo.py:L475-L482` and Ultralytics args at `src/models/yolo_training.py:L358-L405`. The architectures, optimizers, data loaders, initialization shapes, and RNG-consumption paths differ. No code establishes a shared stochastic draw or matched block. Nevertheless, `src/stats/paired.py:L160-L192`, `L681-L701` resamples a common seed index for both detectors. Patient pairing is genuine; seed pairing is not established by equal integer names. The seed component of the primary bootstrap needs justification or independent/crossed resampling before submission. |
| R14 | Poisson acquisition shifts operate on values verifiably proportional to X-ray beam intensity | **CANNOT VERIFY** | The shift normalizes stored 8-bit values and samples `Poisson(normalized * expected_full_scale)` (`src/robustness/radiography_shifts.py:L298-L304`). A fresh read-only audit of all 300 manifest DICOM headers found CR/MONOCHROME2, 8-bit unsigned, but zero instances of Pixel Intensity Relationship/Sign, Presentation Intent Type, Rescale Type, KVP, Exposure, Exposure in uAs, Exposure Time, X-ray Tube Current, or Detector Type; `ConversionType=WSD` in all 300. Repository docs already record absent VOI/modality/rescale/exposure metadata (`docs/ACQUISITION_SHIFTS.md:L12-L25`; `docs/LIMITATIONS.md:L205-L216`). Proportionality to incident quanta therefore cannot be established. The current “synthetic dose-reduction proxy” wording (`configs/acquisition_shifts.yaml:L26-L27`, `L49-L67`; manuscript `L378-L390`, `L914-L922`) is the strongest defensible claim and survives. |
| R15 | Calibration logic or narrative presupposed that seed 271 should be a severe outlier | **PARTLY CONFIRMED / OVERSTATED** | Narrative expectation bias exists: retrospective H6 explicitly predicts seed 271 will be worst (`docs/HYPOTHESES.md:L77-L95`), and plotting/summary code hard-codes a seed-271 highlight (`src/stats/calibration.py:L597-L607`, `L627-L635`, `L732`, `L802-L813`). The numerical computation is generic: every detector/seed is enumerated (`L449-L526`), all D-ECE values are calculated by the same function, and rankings are assigned only after all rows exist (`L538-L563`). No seed-specific binning, matching, exclusion, or D-ECE formula was found. Thus the result itself is generic, but H6 is retrospective and the presentation is explicitly result-linked rather than prespecified. |
| R16 | H1-H6 lack manuscript/artifact coverage | **NOT CONFIRMED** | Every hypothesis maps to a manuscript results section and committed artifact; see the hypothesis crosswalk below. `docs/HYPOTHESES.md:L1-L19` correctly says the hypotheses are retrospective rather than preregistered, so coverage does not convert them into prospective confirmatory hypotheses. |
| R17 | Methodological/standards citations have not been verified | **PARTLY CONFIRMED / OVERSTATED** | All 24 BibTeX keys used anywhere in repository Markdown resolve to primary papers or official implementation sources, and the three reporting standards plus DICOM standard links resolve to authoritative sources. The citation crosswalk below records support claim by claim. The material exception is conceptual rather than bibliographic: Adebayo supports the warning about saliency randomization and its own label-randomization method, but does not support calling this repository's pixel shuffle a “data-randomization” test. Ultralytics sources support implementation facts, not peer-reviewed architecture-level evidence. |

## Repository and verification snapshot

### Git state

- Branch: `main`.
- HEAD: `df2f35f43170699cca32540a283a50caa1764aee` (`Complete final consistency pass`, 2026-08-28T16:23:55+03:30).
- Baseline working tree before this audit file: **not clean**. `git status --porcelain` contained 37 untracked entries and zero tracked modifications. These were the local protocol/memory files (`AGENTS.md`, `BATCHES*.md`, `PROJECT_SPEC.md`, `CODEX.md`, `HANDOFF.md`, review notes) plus ignored/historical run logs. This audit did not treat them as changes to scientific evidence.
- Public release check: GitHub release `v1.0.0` exists and freezes commit `df81f713...`; its API-visible custom asset list is empty. Current HEAD is later than that frozen release.

### CI and latest local verification

Current workflow inventory: one file, `.github/workflows/ci.yml`, named `foundation-ci` (`L1`). It runs on push and pull request (`L3-L5`) with Ubuntu and Windows runners (`L18-L20`) and performs the commands at `L27-L33`.

Latest locally verifiable status during this audit:

```text
uv lock --check                                            PASS
uv run --no-sync ruff format --check src tests             PASS (89 files already formatted)
uv run --no-sync ruff check src tests                      PASS
uv run --no-sync python -m pytest -q                       PASS (257 passed, 1 skipped, 5.35 s)
uv run --no-sync python -m meddet_benchmark smoke ...      PASS (status=smoke; CPU/no CUDA)
```

`UV_CACHE_DIR` was redirected to repository-local `.uv-cache`. The exact workflow-style `uv run --locked --extra cpu` environment could not be newly synchronized in the restricted audit sandbox because a missing seaborn wheel required network access; `uv lock --check` passed and the already-created project environment ran the checks with `--no-sync`. `CODEX.md:L1128-L1130` also records GitHub Actions run `33173026686` passing both operating-system jobs for this HEAD.

This validates software behavior only. It is not a rerun of training or scientific artifact generation (R8).

### Canonical repo-local hierarchy found in current documentation

| Scope | Canonical/current files according to repository documentation | Audit note |
|---|---|---|
| Static requirements and batch governance | `PROJECT_SPEC.md`, `BATCHES.md`, `AGENTS.md` (`AGENTS.md:L22-L25`; `CODEX.md:L1046`) | Explicit and unambiguous. |
| Living project state and session continuity | `CODEX.md`, then newest `HANDOFF.md` entry (`AGENTS.md:L9-L16`, `L23-L24`) | Explicit; both were untracked local files at the baseline snapshot. |
| Numerical scientific evidence | Committed `results/tables/*.csv`, provenance JSON, figures, configs, and their generating code; README says paper/report values are rounded from committed artifacts (`README.md:L542-L544`; `CODEX.md:L1084-L1114`) | Source tables, not prose summaries, were used for the numerical audit below. |
| Reproduction commands | `README.md` and domain documents (`CODEX.md:L1050`) | Commands are extensive but end-to-end execution is manual, not CI. |
| Technical/course report | `report/report.md` plus `report/references.bib` (`CODEX.md:L1074`; `README.md:L8-L12`) | Called final/completed by README and CODEX. |
| Submission-style manuscript | `report/paper_draft.md` plus the same bibliography (`CODEX.md:L1106`) | Called the publication-style draft, but current docs do not say it supersedes `report/report.md`; this is R5. |
| Dependencies | `README.md:L85` names `requirements.txt` authoritative; CI uses `pyproject.toml` and `uv.lock` (`.github/workflows/ci.yml:L28-L32`) | Exact dependency precedence should be stated once. |

## Numerical manuscript-claim recheck

All checks below use committed tables/manifests rather than prose summaries. Values are shown at manuscript precision; every checked claim matched its underlying artifact.

| # | Manuscript claim and location | Underlying committed source and exact row/selector | Audit result |
|---:|---|---|---|
| 1 | Source has 26,684 labeled radiographs and 9,555 valid boxes; subset has 5,000 studies from 2,136 patient groups (`report/paper_draft.md:L194-L214`) | `data/manifests/rsna-pneumonia-5000-audit.json:L22`, `L32`, `L108-L112`; split rows `L71-L99` | **MATCH**: 26,684; 9,555; 5,000; 2,136. |
| 2 | Five-seed clean mAP@0.5 is 0.3042 +/- 0.0189 vs 0.1626 +/- 0.0162 (`L481`) | `results/tables/detector_comparison.csv:L7` | **MATCH**: 0.3042238 +/- 0.0188960 vs 0.1626119 +/- 0.0161740, n=5 each. |
| 3 | Five-seed clean mAP@0.5:0.95 is 0.0995 +/- 0.0067 vs 0.0542 +/- 0.0060 (`L482`) | `results/tables/detector_comparison.csv:L8` | **MATCH**. |
| 4 | Fixed-threshold precision is 0.1959 vs 0.2983 (`L476`) | `results/tables/detector_comparison.csv:L2` | **MATCH**: 0.1958907 vs 0.2983169. |
| 5 | Fixed-threshold recall is 0.5799 vs 0.0955 (`L477`) | `results/tables/detector_comparison.csv:L3` | **MATCH**: 0.5798507 vs 0.0955224. |
| 6 | Fixed-threshold F1 is 0.2845 vs 0.1427 (`L478`) | `results/tables/detector_comparison.csv:L4` | **MATCH**: 0.2845263 vs 0.1426614. |
| 7 | YOLO11s seed 271 maximum score is 0.0412735 (`L487`) | `results/tables/detector_comparison_per_seed.csv:L10` | **MATCH**: 0.04127352312207222. |
| 8 | YOLO11s seed 271 AP@0.5/AP@0.5:0.95 are 0.15872/0.05558 (`L486`) | `results/tables/detector_comparison_per_seed.csv:L10` | **MATCH**: 0.1587217376 / 0.0555798883. |
| 9 | Validation-selected thresholds are 0.69 and 0.05, with reported test P/R/F1 (`L521-L525`) | `results/tables/selected_operating_points.csv:L2-L3` | **MATCH**: Faster 0.69 -> 0.354308/0.360697/0.349225; YOLO 0.05 -> 0.309561/0.243781/0.271750. |
| 10 | FROC sensitivity at 0.5 FP/image is 0.4801 vs 0.3321 and Faster is higher at all five budgets (`L528-L532`) | `results/tables/froc_operating_points.csv:L2-L11`, specifically `L4` and `L9` | **MATCH**: 0.4800995 vs 0.3320896; all five comparisons agree. |
| 11 | Five-seed descriptive mean D-ECE is 0.0320 +/- 0.0058 vs 0.0990 +/- 0.0232 | `results/tables/calibration_summary_v2.csv` detector-summary rows; support and sensitivity in the adjacent v2 tables | **MATCH**: 0.0320433 +/- 0.0057606 vs 0.0990267 +/- 0.0231603; no D-ECE inference claimed. |
| 12 | Primary mAP@0.5:0.95 difference is 0.0453, CI 0.0325-0.0595, Holm p 0.0342 (`L706`) | `results/tables/statistical_clean_comparison.csv:L8` | **MATCH**: 0.0453332, CI 0.0324699-0.0595062, p=0.0341932. |
| 13 | Fixed-threshold precision difference/CI/Holm p is -0.1024, -0.2529 to 0.0802, 0.0020 (`L700`) | `results/tables/statistical_clean_comparison.csv:L2` | **MATCH**; interpretation governed by R1/R2/R13. |
| 14 | Across 35 declared common-corruption/severity conditions, raw mAP is 0.112898 vs 0.054099 and retention 0.763846 vs 0.709083 (`L622-L625`) | Recomputed directly from `results/tables/robustness_curves.csv`, selector `metric=map_50_95`, severities 1-5, 35 rows/detector: arithmetic means of `corrupted_performance` and `relative_performance` | **MATCH**: 0.112898102/0.763845712 vs 0.054099313/0.709083127. |
| 15 | Severity-5 salt-and-pepper retention is 0.2025 vs 0.0570; Gaussian-blur retention is 0.6936 vs 0.6949 (`L627-L633`) | `results/tables/robustness_curves.csv:L141`, `L176`, `L386`, `L421` (detector/corruption/severity/metric row keys) | **MATCH**: 0.2024958/0.0570137 and 0.6936158/0.6948661. |
| 16 | Poisson 12.5% proxy DSI is 0.314529 vs 0.436641 (`L652-L654`) | `results/tables/acquisition_shift_results.csv:L8`, `L18` | **MATCH**: shifted mAP 0.1013142/0.0429813; DSI 0.3145287/0.4366408. |
| 17 | Grad-CAM all-target mean energy-in-box is 0.0869 vs 0.0975 and pointing accuracy 0.1091 vs 0.1261 (`L667-L670`) | `results/tables/gradcam_localization_summary.csv:L2`, `L5` | **MATCH**: energy 0.0868949/0.0974910; pointing 0.1090909/0.1261261. |
| 18 | XAI sanity correlations are 0.0014/-0.0159 and 0.0234/-0.0034 (`L679-L684`) | `results/tables/gradcam_sanity_summary.csv:L2-L5` | **MATCH**: 0.00136015, -0.01585896, 0.02344169, -0.00335679. Test-name correction remains required under R12. |

## Hypothesis coverage crosswalk

Coverage exists for every retrospective H1-H6 entry. This is an artifact/narrative traceability finding, not evidence of preregistration (`docs/HYPOTHESES.md:L1-L19`).

| Hypothesis | Manuscript section | Primary artifacts/code | Coverage verdict |
|---|---|---|---|
| H1: coverage and AP | `report/paper_draft.md` Section 4.1 (`L465-L498`) and statistical synthesis 4.10 (`L691-L715`) | `results/tables/detector_comparison.csv`; `results/tables/statistical_clean_comparison.csv`; `src/stats/paired.py` | Complete. |
| H2: shared threshold does not create a shared regime | Section 4.2 (`L500-L535`) | `detector_comparison_n3_archive.csv`; `precision_recall_curves.csv`; `selected_operating_points.csv`; `froc_operating_points.csv`; threshold/FROC plotting code | Complete at disclosed n=3. |
| H3: accuracy-compute Pareto trade-off | Section 4.5 (`L572-L590`) | `detector_comparison_per_seed_n3_archive.csv`; `selected_operating_points_per_seed.csv`; `results/figures/pareto_frontier.png`; `src/plot_pareto_frontier.py` | Complete at disclosed n=3. |
| H4: corruption-specific degradation | Section 4.7 (`L618-L646`) and 4.10 | `robustness_curves.csv`; `robustness_family_mean_curves.csv`; `statistical_robustness_comparison.csv`; robustness figures/code | Complete at seed 17 / 300 images. |
| H5: Grad-CAM as failure analysis | Section 4.9 (`L665-L689`) | `gradcam_localization_summary.csv`; `gradcam_localization_per_target.csv`; qualitative figures; `src/explainability/gradcam.py`; sanity artifact is secondary | Complete, with R12 naming correction. |
| H6: confidence calibration | Section 4.4 | `calibration_summary_v2.csv`; `calibration_support_v2.csv`; `calibration_sensitivity_v2.csv`; confidence-only marginal reliability and sensitivity figures; `src/stats/calibration.py`; `configs/calibration.yaml` | Complete as a retrospective descriptive audit; R6/R15 remediated by the post-audit addendum. |

## Citation-support audit

### BibTeX citations used in repository Markdown

There are 24 unique citation keys used across tracked/local repository Markdown and 24 corresponding entries in `report/references.bib:L1-L236`. The two manuscripts use 21 unique keys in union (20 in `paper_draft.md`, 19 in `report.md`); three additional keys are used by `docs/LITERATURE_REVIEW.md`. “Verified” below means the linked primary paper or official implementation source supports the specific nearby repository claim, not that the current study independently reproduces that source.

| Citation key | Repository claim location | Support verification |
|---|---|---|
| `ren2015fasterrcnn` | `report/paper_draft.md:L102-L104` | **VERIFIED** against the NeurIPS primary paper: shared features, RPN, RoI-based second stage. |
| `lin2017fpn` | `L104-L106` | **VERIFIED** against the CVPR primary paper: multiscale semantic feature pyramid. |
| `redmon2016yolo` | `L109-L110` | **VERIFIED** against the CVPR primary paper: unified one-pass detector framing. |
| `li2020gfl` | `L111-L114` | **VERIFIED** against the NeurIPS primary paper: distributed bounding-box regression lineage. It supports the general DFL mechanism, not every YOLO11 implementation detail. |
| `ultralytics2024yolo11` | `L110-L120`; `docs/LITERATURE_REVIEW.md:L9` | **VERIFIED AS IMPLEMENTATION SOURCE**: official repository/model family, not peer-reviewed scientific evidence. |
| `ultralytics2026release` | `docs/LITERATURE_REVIEW.md:L9` | **VERIFIED AS IMPLEMENTATION SOURCE**: official PyPI 8.4.110 release/date; it does not identify the downloaded weight bytes, which the repository separately hashes. |
| `ultralytics2026yoloarchitecture` | `report/paper_draft.md:L111-L118` | **VERIFIED AS OFFICIAL DOCUMENTATION**, with the caveat that a live documentation page is less durable than the pinned source/config. |
| `ultralytics2026yolo11config` | `L115-L118` | **VERIFIED AS PINNED SOURCE**: tag-specific official model configuration. |
| `shih2019rsna` | `L130-L145` | **VERIFIED** against the RSNA resource paper: chest-radiograph collection and expert opacity annotations. |
| `yao2021pneumonia` | `L134-L146` | **VERIFIED** against the full primary paper (PMC8081632): modified Faster R-CNN, custom backbone/anchors and Soft-NMS. |
| `wu2024pneumonia` | `L136-L146` | **VERIFIED** against the full Scientific Reports paper (PMC10803753): anchor-free RSNA detector, augmentation/loss/post-processing and study-specific AP/AR setup. |
| `kang2023rcsyolo` | `L138-L148` | **VERIFIED** against the MICCAI paper/official conference record: 2-D brain MRI, YOLO accuracy-speed emphasis. |
| `kang2025pkyolo` | `L138-L148` | **VERIFIED** against the WACV primary paper: multiplanar MRI, domain pretraining, small-target loss. |
| `hendrycks2019corruptions` | `L160-L165` | **VERIFIED** against the ICLR/OpenReview primary paper: common corruptions and five ordered severities. The project's medical corruptions are inspired stress tests, not a claim of dataset equivalence. |
| `michaelis2019detectionrobustness` | `L162-L168` | **VERIFIED** against the primary object-detection robustness paper: detector degradation across corruption type/severity. |
| `kuppers2020calibration` | `L170-L177`, `L328-L346` | **VERIFIED** against the CVPR Workshops primary paper: multivariate D-ECE with confidence/location/scale, five bins per dimension for full K=5 D-ECE, and neglect of cells under eight samples. R6 remains an application-support issue. |
| `selvaraju2017gradcam` | `L179-L181` | **VERIFIED** against the ICCV primary paper: gradient-weighted convolutional feature maps and coarse localization. |
| `chattopadhay2018gradcampp` | `docs/LITERATURE_REVIEW.md:L59` | **VERIFIED** against the WACV primary paper: pixel-wise positive-gradient weighting and multiple-instance motivation. |
| `muhammad2020eigencam` | `docs/LITERATURE_REVIEW.md:L61` | **VERIFIED** against the IJCNN/arXiv primary paper: principal-component activation map without backpropagated class gradients. |
| `petsiuk2021drise` | `docs/LITERATURE_REVIEW.md:L63`; `report/report.md:L685` | **VERIFIED** against the CVPR primary paper: black-box detector saliency via randomized masks and detection similarity, evaluated on YOLO/Faster R-CNN. |
| `adebayo2018sanity` | `report/paper_draft.md:L182-L187` | **PARTLY VERIFIED FOR THIS REPOSITORY'S USE**: the paper supports model-dependence warnings and parameter/label-randomization sanity tests. It does **not** support naming input-pixel shuffling “data randomization” (R12). |
| `arun2021saliency` | `L182-L185` | **VERIFIED** against the Radiology: AI primary paper: medical saliency localization/trustworthiness limitations and weight-randomization sensitivity. |
| `zhang2016excitation` | `L185-L186` | **VERIFIED** against the ECCV primary paper: pointing-game localization measure. |
| `vickers2006decisioncurve` | `L395-L414` | **VERIFIED FOR THE DCA FORMULA** against the Medical Decision Making primary paper: net benefit and threshold odds. It assumes meaningful threshold probabilities; it does not validate substituting uncalibrated detector scores, which the manuscript labels nominal (R3). |

### Standards and direct methodological links

| Source | Repository use | Verification |
|---|---|---|
| CLAIM 2024, DOI `10.1148/ryai.240300` | `docs/REPORTING_CHECKLIST.md:L9`, Section starting `L31` | **VERIFIED** against the official RSNA 2024 update. Checklist is stale relative to the paper, not sourced from the wrong standard. |
| TRIPOD+AI 2024, DOI `10.1136/bmj-2023-078378` | `L10-L11`, Section starting `L80` | **VERIFIED** against the BMJ statement and expanded checklist. It is a reporting guideline, not a risk-of-bias or study-quality instrument. |
| STARD-AI 2025, DOI `10.1038/s41591-025-03953-8` | `L12-L14`, Section starting `L141` | **VERIFIED** against the Nature Medicine consensus statement and 2026 correction note. |
| DICOM PS3.3 C.11.2.1.2.1 | `docs/ACQUISITION_SHIFTS.md:L29-L43`; `configs/acquisition_shifts.yaml:L26-L28` | **VERIFIED** against the current NEMA standard for LINEAR window behavior. It does not establish detector stored values as proportional photon counts (R14). |
| F-beta interpretation used to adjudicate R11 | Repository has no supporting citation for the cost identity | External method documentation defines beta as recall importance relative to precision; clinical utility literature requires prevalence/outcome/decision consequences. **NO VERIFIED SOURCE FOUND FOR `C_FN/C_FP = beta^2` AS AN AUTOMATIC CLINICAL COST CALIBRATION.** |

## BLOCKING BEFORE SUBMISSION

1. Rework or explicitly justify the seed-level resampling in the primary CIs. Same-number seeds are not demonstrated matched stochastic blocks (R13). Patient-cluster pairing can remain; the seed layer needs independent/crossed resampling or a defensible block argument. Recompute affected intervals if the method changes before altering manuscript claims.
2. Stop describing `beta^2` as a calibrated false-negative:false-positive clinical cost ratio. Preserve the existing numerical sensitivity analysis, but relabel it as recall-weighted F-beta scenarios unless a valid expected-utility derivation is added (R11).
3. Rename the XAI pixel-shuffle experiment as an input/pixel-structure perturbation test and separate it explicitly from Adebayo et al.'s training-label data-randomization sanity test (R12). Do not claim that the canonical Adebayo data-randomization test was performed.

## SHOULD FIX

1. Regenerate `docs/REPORTING_CHECKLIST.md` against `report/paper_draft.md`, retaining genuine missing items (R4).
2. Publish one canonical-document map: governance sources, source tables, technical report, submission manuscript, bibliography, and dependency authority (R5).
3. Make the CI scope explicit in README/status badges: software QA, not end-to-end scientific regeneration (R8).
4. Report D-ECE contributing-cell counts/fractions or at least their ranges in the submission-facing calibration text, especially YOLO11s seed 137 (R6).
5. Archive the ten exact final checkpoints as release/DOI assets with hashes, licenses, and config/run identity, or state clearly that third parties must retrain (R7).
6. Keep the CI-versus-permutation estimands adjacent anywhere both are reported, particularly the precision row (R1-R2).

## OPTIONAL STRENGTHENING

1. Add an actual Adebayo label-randomization/retraining experiment and cascading parameter-randomization analysis if compute/time allow; do not make it a prerequisite for accurately naming the current test.
2. Add external multi-site, demographic subgroup/fairness, and prospective/workflow validation in future work; the current single-source internal study cannot supply these retrospectively (R9).
3. Add an artifact-level reproducibility job that regenerates a small hash-bound scientific slice. Full ten-checkpoint GPU training is not suitable for ordinary CI but could be released as a scheduled/manual workflow (R8).
4. If acquisition physics is a future claim, obtain raw detector data with calibrated exposure/intensity metadata or a validated forward model. The current DICOMs support only synthetic proxy language (R14).
5. Replace retrospective H6 wording with an explicitly post hoc research question or label all H1-H6 consistently as retrospective analysis statements (R15-R16).

## CLAIMS THAT SURVIVE UNCHANGED

- All 18 numerical checks in this audit match their committed source tables/manifests at the stated precision.
- Dataset construction, patient-disjoint split counts, five-seed clean AP, fixed-threshold P/R/F1, seed-271 score/AP values, n=3 selected thresholds and FROC values, D-ECE point estimates, common-corruption retention, acquisition-proxy DSI, Grad-CAM localization, and XAI correlation statistics survive numerically.
- The clean patient-level pairing and checkpoint-conditional permutation results survive as calculations. Only the seed-resampling interpretation/interval layer requires adjudication before final inferential claims.
- DCA survives only as an internal, same-test, raw-score **nominal** scenario analysis; it does not become calibrated clinical utility.
- Acquisition-shift results survive only as synthetic stored-value sensitivity proxies, not physical dose simulations.
- The absence of external, subgroup/fairness, and prospective validation is already stated accurately and should remain unchanged.
- The conclusion that the results compare two measured pipelines rather than detector families remains supported by the repository evidence and limitations.
