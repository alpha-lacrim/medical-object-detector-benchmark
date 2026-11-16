# Graph Report - DP_Final_Project  (2026-11-16)

## Corpus Check
- 397 files · ~2,958,304 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 375 file(s) not represented in the graph (top: .csv 185, .gz 157, (none) 15)

## Summary
- 4845 nodes · 13572 edges · 204 communities (184 shown, 20 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 496 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ee4f354f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- prepare.py
- analyze_yolo_numerical_path.py
- CocoDetectionDataset
- threshold_calibration.py
- download.py
- run_statistics.py
- train_faster_rcnn.py
- calibration.py
- faster_rcnn_reporting.py
- evaluate_vindr_external.py
- analyze_validation_threshold_sensitivity.py
- analyze_threshold_repairability.py
- test_external_generalization.py
- evaluation.py
- analyze_yolo_seed_stability.py
- evaluate_threshold_sweep.py
- run_vindr_statistics.py
- verify_scientific_artifacts.py
- run_explainability.py
- meddet_benchmark/corruptions.py
- Shared-annotation certificates for operating-budget detection comparisons
- radiography_shifts.py
- YoloConfig
- decision_curve_pre_batch30_nonstandard.py
- numpy
- faster_rcnn_config.py
- evaluate_threshold_selection.py
- run_robustness.py
- sanity_checks.py
- meddet_benchmark/config.py
- analyze_operating_regime_sensitivity.py
- test_train_faster_rcnn.py
- report_transportability.py
- os
- train_yolo.py
- visualize.py
- 3. Materials and Methods
- plot_pareto_frontier.py
- dataclasses
- argparse
- test_transportability.py
- Medical Object Detector Benchmark
- raw_score_utility.py
- analyze_external_failure.py
- README.md
- test_statistics.py
- CocoDetectionDataset
- math
- test_radiography_shifts.py
- batch52/paper_draft.md
- Any
- numpy
- artifact
- Float32DetectionLoss
- StrictModel
- yolo_data.py
- decision_curve.py
- PROJECT_PLAN.md
- json
- batch46/paper_draft.md
- build_faster_rcnn
- load_yolo_config
- test_exact_score_froc.py
- cohort_characteristics.py
- StrictModel
- Project plan: controlled lung-opacity detector comparison
- collections_abc
- load_pareto_points
- report.md
- StrictModel
- test_threshold_calibration.py
- Research direction: limits of threshold repair under external shift
- numpy
- sha256_file
- run_timing
- COMPUTE_TIMING.md
- V7 Q2 / VinDr Baseline Audit
- test_evaluate_vindr_external.py
- load_faster_rcnn_config
- test_inference_timing.py
- evaluate_coco
- Grad-CAM Sensitivity Controls (v2)
- Constrained detector repairability: research assessment
- Clinical annotation-adjudication protocol v1
- explainability/config.py
- Supervisor briefing: transportability evidence and publication decision
- Supervisor-review preparation: execution and verification
- StrictModel
- test_raw_score_utility.py
- StrictModel
- ActivationCapture
- test_check_bibliography.py
- Final adversarial submission audit
- Scientific review and gap assessment
- VinDr-CXR adapter preflight — Batch 48
- plot_raincloud_metrics.py
- aggregate_hybrid
- Review Remediation Audit
- seed.py
- test_cohort_characteristics.py
- yolo_reporting.py
- collect
- Statistical analysis
- Supplementary Materials Index
- Medical Object Detector Benchmark v2.0.0 — Research Artifact Release
- ImagePrediction
- External failure isolation v1: controlled diagnostic protocol
- Final manuscript evidence and verification audit
- Unified quantitative comparison
- 4. Results
- AgeSettings
- Focused Internal Manuscript Audit
- .image_path
- StrictModel
- StrictModel
- Literature Review
- Post-hoc external generalization results v1
- TimingConfig
- generate_cohort_characteristics
- csv
- Hypothesis Traceability
- load_config
- OutputSettings
- External failure isolation v1: executed diagnostic results
- Datasheet: RSNA Pneumonia Detection Challenge 2018
- Final Submission Audit
- Limitations
- holm_adjust
- StrictModel
- load_phase5_config
- StrictModel
- Controlled external failure diagnostic: interpretation and verification
- Radiography-Motivated Synthetic Acquisition/Display Sensitivity
- Author Declarations — Action Required
- Dataset choice
- VinDr-CXR external testing protocol v1
- benchmark_inference.py
- 3. Materials and Methods
- SelectionSettings
- Threshold repairability v2: execution and verification
- analyze_exact_score_froc.py
- conftest.py
- Detection-Confidence Calibration
- test_xai_sanity.py
- Research Question and Hypotheses
- Post-hoc external generalization protocol v1
- Reproducibility contract
- Recall-Weighted F-beta Threshold Sensitivity
- VinDr statistics and cross-dataset transportability — Batch 50
- load_robustness_config
- analyze_pair
- analyze_training_procedure
- draw_hierarchical_bootstrap_multiplicities
- _aggregate_row
- [2.0.0] — Research Artifact Release
- Post-hoc external generalization v1 — execution and verification
- Exploratory Raw-Score Threshold Utility/Sensitivity (Non-Standard DCA)
- Decision log
- Final submission audit and author-declaration follow-up
- Reporting Checklist Crosswalk
- Frozen VinDr-CXR inference results — Batch 49
- run_statistics.py
- 2. Related Work
- Threshold repairability v2: computational protocol
- Threshold repairability v2: complete computational results
- PatientClusters
- Citation Audit
- Frozen VinDr statistics and cross-dataset transportability
- Scientific interpretation of post-hoc external generalization v1
- Citation Verification Audit
- Dataset workspace
- test_timer_brackets_the_whole_prediction_with_cuda_completion
- Frozen VinDr-CXR inference — Batch 49
- YOLO numerical inference-path sensitivity, v1
- Research audit: external generalization v1
- main
- D-002 — Descope Track B and reframe the research contribution
- D-004 — Keep later validation-threshold sensitivity separate from the primary thresholds
- D-005 — Separate inferential targets and resample detector runs independently
- D-006 — Treat beta as an F-beta preference parameter and separate linear loss
- D-007 — Remove raw detector-score curves from conventional DCA interpretation
- D-008 — Use n=5 as the principal operating-regime sensitivity display
- D-009 — Use one version for software and research-artifact releases
- D-010 — Keep `paper_draft.md` as the canonical editable journal manuscript
- D-011 — Use the observed exact-score frontier and retain the candidate-floor boundary
- D-012 — Adopt the approved 0.0001 FROC sensitivity and retain the residual boundary
- D-013 — Adopt the approved 0.00001 FROC sensitivity and stop at the residual bound
- D-014 — Retain n=3 threshold provenance and report n=5 selection only as post-hoc sensitivity
- D-015 — Report aggregate DICOM-header cohort characteristics with an age-unit caveat
- D-003 — Decline to revive a Track-B-style native/best-practice comparison
- D-001 — Two-track detector comparison design
- D-019 — Separate observed ranking transport from frozen operating-point transport
- VINDR_WGET_WINDOWS.md
- build_parser
- batch52/README.md
- meddet-benchmark

## God Nodes (most connected - your core abstractions)
1. `ImagePrediction` - 146 edges
2. `sha256_file()` - 115 edges
3. `ImageTarget` - 114 edges
4. `require()` - 53 edges
5. `artifact()` - 49 edges
6. `load_phase5_config()` - 46 edges
7. `verify_artifact()` - 45 edges
8. `CocoDetectionDataset` - 44 edges
9. `read_yaml()` - 44 edges
10. `read_json()` - 43 edges

## Surprising Connections (you probably didn't know these)
- `Prerequisite and implementation checks` --references--> `Predictor`  [INFERRED]
  docs/VINDR_INFERENCE.md → src/benchmark_inference.py
- `Actual DICOM semantics and preprocessing` --references--> `scale_radiograph_to_uint8()`  [INFERRED]
  docs/VINDR_ADAPTER_PREFLIGHT.md → src/data/prepare.py
- `4. Frozen DICOM and model execution contract` --references--> `scale_radiograph_to_uint8()`  [INFERRED]
  docs/VINDR_EXTERNAL_PROTOCOL.md → src/data/prepare.py
- `Implementation and efficiency audit` --references--> `restore_native_bounds()`  [INFERRED]
  docs/FINAL_SUBMISSION_AUDIT_2026-09-24.md → src/evaluate_vindr_external.py
- `One prediction-to-metric path` --references--> `ImagePrediction`  [INFERRED]
  docs/QUANTITATIVE_COMPARISON.md → src/meddet_benchmark/evaluation.py

## Import Cycles
- None detected.

## Communities (204 total, 20 thin omitted)

### Community 0 - "prepare.py"
Cohesion: 0.05
Nodes (46): _add_issue(), _allocate_exact_counts(), _audit_summary(), AuditIssue, AuditResult, _balanced_group_order(), BoundingBox, build_coco() (+38 more)

### Community 1 - "analyze_yolo_numerical_path.py"
Cohesion: 0.05
Nodes (42): binding(), main(), main(), number(), render(), candidate_agreement(), canonical_bytes(), check_inputs() (+34 more)

### Community 2 - "CocoDetectionDataset"
Cohesion: 0.09
Nodes (18): CocoAnnotation, CocoCategory, CocoImageRecord, CocoValidationError, _configured_path(), _ImageMetadata, _load_coco_payload(), _parse_annotations() (+10 more)

### Community 3 - "threshold_calibration.py"
Cohesion: 0.12
Nodes (24): _artifact(), _atomic_bytes(), _atomic_csv(), _atomic_json(), _atomic_sensitivity_figure(), _deserialize_predictions(), FrozenValidationData, _hypothetical_loss_summary_rows() (+16 more)

### Community 4 - "download.py"
Cohesion: 0.05
Nodes (41): build_parser(), _child_environment(), ConfigurationError, _credential_file_path(), CredentialError, CredentialSource, download_competition_files(), _download_failure_message() (+33 more)

### Community 5 - "run_statistics.py"
Cohesion: 0.18
Nodes (22): _artifact_hash(), _atomic_bytes(), _atomic_csv(), _atomic_csv_fields(), _atomic_json(), _bundle_hash_map(), compare_holm_significance(), compare_paired_and_independent_run_intervals() (+14 more)

### Community 6 - "train_faster_rcnn.py"
Cohesion: 0.07
Nodes (26): config_fingerprint(), FasterRCNNConfig, apply_training_mode(), _approved_benchmark(), _atomic_torch_save(), _available_subset(), _checkpoint_payload(), _completed_artifacts_intact() (+18 more)

### Community 7 - "calibration.py"
Cohesion: 0.05
Nodes (47): _add_detector_summaries(), _atomic_binning_sensitivity_figure(), _atomic_bytes(), _atomic_csv(), _atomic_floor_sensitivity_figure(), _atomic_json(), _atomic_reliability_figure(), _atomic_support_figure() (+39 more)

### Community 8 - "faster_rcnn_reporting.py"
Cohesion: 0.07
Nodes (34): append_epoch_metrics(), _atomic_write_text(), build_benchmark_projection(), _csv_cell(), _csv_text(), _json_text(), _load_epoch_csv(), _load_epoch_jsonl() (+26 more)

### Community 9 - "evaluate_vindr_external.py"
Cohesion: 0.08
Nodes (31): Evidence baseline and implementation map, main(), build_targets(), decode_image(), geometry_check(), main(), PreflightError, read_csv() (+23 more)

### Community 10 - "analyze_validation_threshold_sensitivity.py"
Cohesion: 0.09
Nodes (37): _aggregate_test_rows(), _artifact(), build_conclusion_rows(), build_parser(), _bundle_record(), classify_margin_change(), collect_validation_predictions(), _compare_reference_operating_point() (+29 more)

### Community 11 - "analyze_threshold_repairability.py"
Cohesion: 0.12
Nodes (14): binding(), calculate(), components(), require(), run(), unique_runs(), maximum_coverage(), evaluate() (+6 more)

### Community 12 - "test_external_generalization.py"
Cohesion: 0.10
Nodes (32): ap_events(), joint_bootstrap(), evaluate(), local_annotations(), prevalence_metrics(), prevalence_weights(), validate_domains(), weighted_ap() (+24 more)

### Community 13 - "evaluation.py"
Cohesion: 0.09
Nodes (26): box_iou(), _boxes(), evaluate_operating_point(), combine(), _image_size(), ImageMatchResult, _labels(), Match (+18 more)

### Community 14 - "analyze_yolo_seed_stability.py"
Cohesion: 0.14
Nodes (22): _artifact(), _atomic_bytes(), _atomic_csv(), build_parser(), classify_convergence(), classify_operational(), InputSettings, load_config() (+14 more)

### Community 15 - "evaluate_threshold_sweep.py"
Cohesion: 0.07
Nodes (33): aggregate_threshold_rows(), _artifact(), _atomic_bytes(), _atomic_csv(), _atomic_figure(), _atomic_json(), build_parser(), _deserialize_predictions() (+25 more)

### Community 16 - "run_vindr_statistics.py"
Cohesion: 0.07
Nodes (36): verify(), analyze(), main(), select_indices(), ensure_private(), deserialize(), read_gzip(), count_constraint() (+28 more)

### Community 17 - "verify_scientific_artifacts.py"
Cohesion: 0.08
Nodes (32): ArtifactSpec, build_manifest(), committed(), external(), _input_payload(), InputSpec, main(), _schema() (+24 more)

### Community 18 - "run_explainability.py"
Cohesion: 0.10
Nodes (34): ExplainabilityConfig, load_explainability_config(), aggregate_localization(), _atomic_bytes(), _atomic_csv(), _atomic_json(), _best_candidate_index(), build_parser() (+26 more)

### Community 19 - "meddet_benchmark/corruptions.py"
Cohesion: 0.07
Nodes (23): apply_corruption(), build_transform(), corruption_fingerprint(), CorruptionApplier, CorruptionCondition, CorruptionConfig, CorruptionDefinition, _derived_seed() (+15 more)

### Community 20 - "Shared-annotation certificates for operating-budget detection comparisons"
Cohesion: 0.07
Nodes (27): 10. What this can and cannot establish for the professor, 1. The problem that the previous proposal did not solve, 2. Contract and definitions, 3. Lemma: a reference edit changes at most one greedy TP indicator, 4. Theorem: FP-budget transport bounds, 5. Run means, paired rankings and domain gaps, 6. Exact shared-reference deletion audit, 7. Nonredundancy theorem (+19 more)

### Community 21 - "radiography_shifts.py"
Cohesion: 0.10
Nodes (29): AcquisitionShiftConfig, _audit_raw_files(), _audit_value(), build_parser(), _bundle_identity(), _bundle_path(), _condition_payload(), _dataset_contract() (+21 more)

### Community 22 - "YoloConfig"
Cohesion: 0.05
Nodes (22): load_yolo_config(), StrictModel, YoloAugmentationConfig, YoloBenchmarkConfig, YoloDataConfig, YoloEarlyStoppingConfig, YoloEvaluationConfig, YoloLossConfig (+14 more)

### Community 23 - "decision_curve_pre_batch30_nonstandard.py"
Cohesion: 0.09
Nodes (25): _artifact(), _atomic_csv(), _atomic_figure(), _atomic_json(), compute_decision_curves(), contiguous_ranges(), DecisionCurveConfig, _display_name() (+17 more)

### Community 24 - "numpy"
Cohesion: 0.08
Nodes (32): draw_independent_run_bootstrap_multiplicities(), draw_patient_cluster_bootstrap_multiplicities(), stable_rng_seed(), controls(), bootstrap(), summarize(), controls(), interval() (+24 more)

### Community 25 - "faster_rcnn_config.py"
Cohesion: 0.11
Nodes (31): BenchmarkSettings, _channel_values(), DataPaths, EarlyStoppingSettings, EvaluationSettings, _mapping(), _non_negative_int(), OptimizerSettings (+23 more)

### Community 27 - "evaluate_threshold_selection.py"
Cohesion: 0.10
Nodes (29): _artifact(), _atomic_bytes(), _atomic_csv(), _atomic_json(), build_parser(), collect_validation_predictions(), _frozen_faster_config_sha256(), InputSettings (+21 more)

### Community 28 - "run_robustness.py"
Cohesion: 0.10
Nodes (32): _atomic_bytes(), _atomic_csv(), _atomic_json(), build_parser(), _bundle_identity(), _bundle_path(), _cached_result(), _clean_predictions() (+24 more)

### Community 29 - "sanity_checks.py"
Cohesion: 0.14
Nodes (21): assert_checkpoint_immutability(), _atomic_bytes(), _atomic_csv(), _atomic_json(), build_parser(), checkpoint_hashes(), _draw_candidate(), _historical_artifact_identity() (+13 more)

### Community 30 - "meddet_benchmark/config.py"
Cohesion: 0.05
Nodes (43): assert_run_allowed(), canonical_json(), config_fingerprint(), DataConfig, EvaluationConfig, ExperimentConfig, load_experiment(), Manifests (+35 more)

### Community 31 - "analyze_operating_regime_sensitivity.py"
Cohesion: 0.10
Nodes (26): _artifact(), _atomic_csv(), _atomic_json(), build_conclusion_rows(), build_fixed_threshold_tables(), build_inventory_rows(), build_parser(), classify_margin_change() (+18 more)

### Community 32 - "test_train_faster_rcnn.py"
Cohesion: 0.14
Nodes (12): build_parser(), _dataset_summary(), split_summary(), _load_datasets(), main(), _coco_payload(), test_approved_benchmark_binds_data_execution_and_implementation(), test_complete_finalization_is_a_noop_only_while_artifacts_are_intact() (+4 more)

### Community 33 - "report_transportability.py"
Cohesion: 0.10
Nodes (13): render(), table(), number(), plot_froc(), plot_scores(), plot_thresholds(), render(), report() (+5 more)

### Community 34 - "os"
Cohesion: 0.08
Nodes (28): aggregate_froc_curve(), AnalysisSettings, _artifact(), _atomic_csv(), _atomic_figure(), _atomic_json(), build_parser(), DetectorSettings (+20 more)

### Community 35 - "train_yolo.py"
Cohesion: 0.08
Nodes (19): build_parser(), _copy_checkpoint(), _driver_version(), _execution_identity(), _finalize(), _git_commit(), _guard_new_run(), _implementation_identity() (+11 more)

### Community 36 - "visualize.py"
Cohesion: 0.14
Nodes (14): _balanced_sample(), build_parser(), _draw_centered_text(), _font(), _load_coco_records(), load_dataset_config(), main(), plot_annotation_samples() (+6 more)

### Community 37 - "3. Materials and Methods"
Cohesion: 0.05
Nodes (39): 1. Introduction, 2.1 Two-stage and one-stage detector organization, 2.2 The comparability gap in medical detection studies, 2.3 Robustness, calibration, and explanation, 2. Related Work, 3.10 Inferential targets and patient-cluster protocol, 3.11 Retrospective hypothesis and reporting status, 3.1 Dataset, target, and patient-disjoint split (+31 more)

### Community 38 - "plot_pareto_frontier.py"
Cohesion: 0.10
Nodes (17): aggregate_pareto_points(), _artifact(), _assert_close(), _atomic_csv(), _atomic_figure(), _atomic_json(), _float(), _integer() (+9 more)

### Community 39 - "dataclasses"
Cohesion: 0.06
Nodes (32): CountRun, extended_interval(), problem_from_outputs(), cardinality(), exhaustive(), rank(), RepairProblem, RepairSolution (+24 more)

### Community 40 - "argparse"
Cohesion: 0.12
Nodes (23): main(), _artifact_paths(), evaluate_source(), _filtered_csv_rows(), _json_pointer(), _load_yaml(), main(), _number() (+15 more)

### Community 41 - "test_transportability.py"
Cohesion: 0.06
Nodes (30): _percentile_interval(), aligned_records(), APCache, bootstrap(), build_ap_cache(), build_froc_cache(), classify_change(), FrocCache (+22 more)

### Community 42 - "Medical Object Detector Benchmark"
Cohesion: 0.05
Nodes (44): 1. Create the pinned environment, 2. Acquire and prepare the dataset, 2a. Generate aggregate cohort characteristics, 3. Train and finalize the primary Faster R-CNN run, 4. Train and finalize the primary YOLO11s run, 5. Train the additional seeds and run the five-seed unified test evaluator, 5a. Reprocess the frozen bundles across confidence thresholds, 5b.1 Run the post-hoc five-validation-run selection sensitivity (+36 more)

### Community 43 - "raw_score_utility.py"
Cohesion: 0.16
Nodes (25): _atomic_bytes(), AnalysisSettings, _artifact(), _atomic_csv(), _atomic_figure(), _atomic_json(), _audit_archives(), _display_name() (+17 more)

### Community 44 - "analyze_external_failure.py"
Cohesion: 0.13
Nodes (17): image_counts(), paired_summary(), window_pixels(), dicom(), prediction(), target(), test_bootstrap_preserves_a_known_constant_paired_intervention(), test_incomplete_window_is_not_silently_ignored() (+9 more)

### Community 45 - "README.md"
Cohesion: 0.11
Nodes (10): Constrained repairability v1: exploratory computational protocol, Proposed retained-candidate sensitivity v2 — NOT EXECUTED, Prerequisite evidence, YOLO numerical inference-path audit (Batch 53, v1), 1. Introduction, 5. Discussion, 6. Limitations, 7. Conclusion (+2 more)

### Community 46 - "test_statistics.py"
Cohesion: 0.14
Nodes (22): evaluate_prediction_records(), EvaluationSettings, build_patient_clusters(), load_statistics_config(), _merge_clean_endpoint_rows(), test_coco_ap_uses_retained_predictions_below_the_operating_threshold(), test_unified_metrics_include_conditional_iou_and_dice(), _evidence() (+14 more)

### Community 47 - "CocoDetectionDataset"
Cohesion: 0.23
Nodes (16): CocoDetectionDataset, detection_collate_fn(), _canonical_coco(), test_actual_image_dimensions_are_checked_during_preflight(), test_coco_filename_cannot_escape_processed_images_dir(), test_complete_modes_list_every_missing_file(), test_duplicate_ids_are_rejected(), test_getitem_reports_clear_missing_torch_dependency() (+8 more)

### Community 48 - "math"
Cohesion: 0.16
Nodes (11): EarlyStopObservation, EarlyStopper, estimate_training_seconds(), test_early_stopper_records_initial_and_later_improvements(), test_early_stopper_rejects_nonfinite_metrics(), test_early_stopper_requires_improvement_strictly_above_min_delta(), test_early_stopper_stops_at_patience_boundary(), test_early_stopper_tie_is_not_an_improvement() (+3 more)

### Community 49 - "test_radiography_shifts.py"
Cohesion: 0.10
Nodes (19): scale_radiograph_to_uint8(), apply_radiography_shift(), _derived_seed(), dicom_linear_window(), _normalized_error_metrics(), RadiographyShift, _dicom_metadata(), _shift_metadata() (+11 more)

### Community 50 - "batch52/paper_draft.md"
Cohesion: 0.06
Nodes (30): 1. Introduction, 2.1 Detector scores and operating-point assessment, 2.2 RSNA methodology and direct detector comparisons, 2.3 Implementation and reporting context, 2.4 External testing under a different annotation ontology, 2. Related Work, 3.1 Dataset, target, and patient-disjoint split, 3.2 Detector pipelines and controlled training factors (+22 more)

### Community 51 - "Any"
Cohesion: 0.16
Nodes (19): _artifact(), _atomic_csv(), _atomic_figure(), _atomic_json(), _candidate_floor_assessment(), _deserialize_predictions(), ExactFrocConfig, _inference_sensitivity_proposal() (+11 more)

### Community 52 - "numpy"
Cohesion: 0.12
Nodes (27): allocations(), bounds_by_allocation(), count_curve(), CountCurve, deletion_endpoints(), deletion_losses(), deletion_sets(), family_bounds() (+19 more)

### Community 53 - "artifact"
Cohesion: 0.06
Nodes (30): binding(), register(), register(), register(), figures(), number(), report(), run() (+22 more)

### Community 55 - "StrictModel"
Cohesion: 0.06
Nodes (18): CascadingParameterRandomizationSettings, ClaimBoundaries, DetectorLayerGroups, HistoricalArtifacts, InputPixelRandomizationSettings, LayerGroup, OutputSettings, PanelSettings (+10 more)

### Community 56 - "yolo_data.py"
Cohesion: 0.15
Nodes (10): _atomic_json(), _atomic_text(), _balanced_smoke(), CocoImageRecord, _ensure_hardlink(), _image_manifest_sha256(), _label_text(), _load_coco() (+2 more)

### Community 57 - "decision_curve.py"
Cohesion: 0.15
Nodes (13): CalibratedOutcomeProbabilities, DecisionThresholdProbability, RawDetectorConfidenceScores, RawDetectorConfidenceThreshold, _require_decision_threshold_probability(), standard_dca_actions(), standard_dca_net_benefit(), _validated_threshold_probability() (+5 more)

### Community 58 - "PROJECT_PLAN.md"
Cohesion: 0.07
Nodes (23): Artifacts and reproduction, Current interpretation, Exact-score method and endpoint behavior, Free-Response ROC Analysis, Historical-grid reproduction and fixed protocol, Historical grid versus approved lower-floor exact-score frontier, Residual candidate-floor boundary and conservative bound, Scientific value of another lower-floor run (+15 more)

### Community 59 - "json"
Cohesion: 0.07
Nodes (22): main(), sha256(), digest(), main(), add(), binding(), main(), render() (+14 more)

### Community 60 - "batch46/paper_draft.md"
Cohesion: 0.07
Nodes (26): 1. Introduction, 2.1 Detector scores and operating-point assessment, 2.2 RSNA methodology and direct detector comparisons, 2.3 Implementation and reporting context, 2. Related Work, 3.1 Dataset, target, and patient-disjoint split, 3.2 Detector pipelines and controlled training factors, 3.3 Five retained runs and common evaluation (+18 more)

### Community 61 - "build_faster_rcnn"
Cohesion: 0.13
Nodes (9): ModelSettings, count_parameters(), enforce_backbone_trainability(), freeze_batch_norm_statistics(), FakeBody, FakeParameter, test_all_backbone_stages_include_stem_batch_norm_at_five_layers(), test_configured_three_layer_freeze_mask_is_enforced_without_torchvision() (+1 more)

### Community 62 - "load_yolo_config"
Cohesion: 0.06
Nodes (9): _atomic_json(), ComparableEarlyStopping, Float32DetectionLoss, _floating_tensors_to_float32(), YoloRunTracker, test_comparable_early_stopping_enforces_minimum_and_delta(), test_loss_prediction_cast_is_float32_and_preserves_gradient(), test_tracker_ignores_ultralytics_final_eval_callback() (+1 more)

### Community 63 - "test_exact_score_froc.py"
Cohesion: 0.18
Nodes (19): audit_exact_score_monotonicity(), exact_score_froc_rows(), load_exact_froc_config(), select_exact_operating_points(), frozen_exact_inputs(), frozen_exact_rows(), lower_floor_exact_inputs(), lower_floor_exact_rows() (+11 more)

### Community 64 - "cohort_characteristics.py"
Cohesion: 0.14
Nodes (8): AgeObservation, _build_parser(), main(), ManifestColumns, _read_manifest(), _resolved_dataset_config(), _safe_relative_name(), _update_accumulator()

### Community 65 - "StrictModel"
Cohesion: 0.13
Nodes (5): AnalysisSettings, InputSettings, OutputSettings, PlotSettings, StrictModel

### Community 66 - "Project plan: controlled lung-opacity detector comparison"
Cohesion: 0.08
Nodes (25): 10. Explainability plan as delivered, 11. Statistical analysis, 12. Implementation sequence and completion status, 13. Actual repository architecture, 14. Final report mapping, 15. Major risks and mitigations, 1. Aim and research questions, 2. Definition of success (+17 more)

### Community 67 - "collections_abc"
Cohesion: 0.19
Nodes (7): gradcam_for_score(), gradcam_from_tensors(), resolve_module(), restore_letterboxed_heatmap(), test_gradcam_uses_global_average_gradient_weights(), test_letterbox_restoration_removes_centered_padding(), test_module_resolution_supports_attributes_and_indices()

### Community 68 - "load_pareto_points"
Cohesion: 0.16
Nodes (14): _directed(), dominance_by_panel(), load_pareto_config(), load_pareto_points(), main(), ParetoPoint, strict_detector_dominance(), _validate_seed_grid() (+6 more)

### Community 69 - "report.md"
Cohesion: 0.08
Nodes (23): 10. Statistical Analysis, 11.1 Accuracy and operating-point behavior, 11.2 Robustness and explanation evidence, 11.3 Scenario-specific recommendation, 11.4 Limitations and scope of claims, 11. Discussion, 12. Conclusions and Future Work, 1. Introduction (+15 more)

### Community 70 - "StrictModel"
Cohesion: 0.09
Nodes (9): ArtifactBinding, ComparisonSettings, FrozenEvaluationSettings, InputSettings, OutputSettings, ProtectionSettings, ScopeSettings, SelectionSettings (+1 more)

### Community 71 - "test_threshold_calibration.py"
Cohesion: 0.15
Nodes (15): BootstrapPlan, compute_calibration_curve(), compute_hypothetical_loss_curve(), f_beta(), _ratios_from_counts(), summarize_hypothetical_detection_error_loss(), summarize_threshold_counts(), _summarize_threshold_counts_with_distribution() (+7 more)

### Community 72 - "Research direction: limits of threshold repair under external shift"
Cohesion: 0.29
Nodes (7): A concrete feasibility result from existing evidence, Closest literature and the novelty boundary, Exact scope of the score-cutoff limit, Recommendation and question, Research direction: limits of threshold repair under external shift, Short pitch for the professor, Work completed here and what would strengthen the paper

### Community 74 - "numpy"
Cohesion: 0.18
Nodes (8): BoxAttentionResult, evaluate_box_attention(), pixel_center_box_mask(), _validated_box(), _validated_heatmap(), test_box_mask_rejects_out_of_bounds_boxes(), test_energy_and_pointing_use_pixel_center_box_mask(), test_zero_energy_is_explicitly_invalid()

### Community 75 - "sha256_file"
Cohesion: 0.12
Nodes (40): _aggregate_boundaries(), _artifact(), build_parser(), main(), preflight(), _read_bundle(), _read_json(), _relative() (+32 more)

### Community 76 - "run_timing"
Cohesion: 0.16
Nodes (7): render(), run_timing(), synchronize(), telemetry(), time_call(), write_csv(), write_json()

### Community 77 - "COMPUTE_TIMING.md"
Cohesion: 0.06
Nodes (32): Accepted laptop measurements, Claim limits and artifact provenance, Matched boundary and configuration, Parameter counts and incomplete operation profiles, Prediction agreement and timing statistics, Reporting hardware and reproducibility, Standardized inference timing v1, Artifacts (+24 more)

### Community 78 - "V7 Q2 / VinDr Baseline Audit"
Cohesion: 0.10
Nodes (20): 10. Verification record, 11. Review checkpoint, 1. Executive adjudication, 2. Repository baseline and prerequisite gate, 3. Manuscript and article comparison, 4. PDF rendering and provenance, 5. Checkpoint manifest audit, 6. Prediction-bundle inventory (+12 more)

### Community 79 - "test_evaluate_vindr_external.py"
Cohesion: 0.08
Nodes (30): extend(), main(), aggregate_metrics(), flatten(), artifact(), compute_metrics(), dump_gzip(), main() (+22 more)

### Community 80 - "load_faster_rcnn_config"
Cohesion: 0.32
Nodes (17): load_faster_rcnn_config(), test_aggregation_excludes_zero_maps_and_reports_status(), _config_payload(), test_batch_size_outside_hardware_scope_is_rejected(), test_coco_minimum_score_must_match_model_output_threshold(), test_loader_persistence_settings_require_booleans(), test_non_amp_runtime_is_rejected(), test_output_artifact_paths_reject_project_escape() (+9 more)

### Community 81 - "test_inference_timing.py"
Cohesion: 0.19
Nodes (11): Agreement, compare_predictions(), summarize(), prediction(), test_empty_prediction_parity_is_valid(), test_invalid_timings_fail(), test_prediction_parity_allows_order_and_bounded_numerical_error(), test_prediction_parity_fails_on_scientifically_different_output() (+3 more)

### Community 82 - "evaluate_coco"
Cohesion: 0.17
Nodes (12): _empty_results_dataset(), evaluate_coco(), _precision_curve(), _safe_average(), prediction(), target(), test_all_negative_dataset_returns_null_ap(), test_class_without_ground_truth_has_null_ap() (+4 more)

### Community 83 - "Grad-CAM Sensitivity Controls (v2)"
Cohesion: 0.12
Nodes (15): Explainability Analysis, Grad-CAM protocol, Qualitative selection and caveats, Quantitative results, Reproduction, Scope and provenance, Where are the models looking?, Cascading model-parameter randomization (+7 more)

### Community 84 - "Constrained detector repairability: research assessment"
Cohesion: 0.08
Nodes (21): 1. Formal problem and intervention classes, 2. Integral minimum-cost-flow theorem, 3. The simplification that limits the novelty claim, 4. Annotation-edit stability theorem, 5. Implementation and computational limits, 6. Prior work and novelty comparison, 7. Real study results and uncertainty, 8. Relationship to the professor's requirements (+13 more)

### Community 85 - "Clinical annotation-adjudication protocol v1"
Cohesion: 0.22
Nodes (9): Blinding and reading sequence, Clinical annotation-adjudication protocol v1, Construct workshop and rubric, before study images, Instance relations and duplicate annotations, Outcomes and statistical plan, People, permissions and pre-read lock, Population and sampling, Purpose, hypotheses and decision boundary (+1 more)

### Community 86 - "explainability/config.py"
Cohesion: 0.12
Nodes (7): DetectorLayerSettings, GradCamSettings, MetricSettings, OutputSettings, QualitativeSettings, RuntimeSettings, StrictModel

### Community 88 - "Supervisor briefing: transportability evidence and publication decision"
Cohesion: 0.25
Nodes (8): Central contribution, Decisions for the supervisor, Direct answers to the professor's four requests, Label mapping and evaluation, in concrete terms, Publication barriers, Suggested reply in Persian, Supervisor briefing: transportability evidence and publication decision, What the evidence establishes

### Community 89 - "Supervisor-review preparation: execution and verification"
Cohesion: 0.25
Nodes (8): Actual scientific and software checks, Baseline and preservation, Boundaries of completion, Current location map for the reporting crosswalk, Delivered review documents, Final privacy and document checks, PDF build and exact-source checks, Supervisor-review preparation: execution and verification

### Community 90 - "StrictModel"
Cohesion: 0.11
Nodes (7): AnalysisSettings, DetectorSettings, InferenceSensitivityProposal, InputSettings, OutputSettings, PlotSettings, StrictModel

### Community 91 - "test_raw_score_utility.py"
Cohesion: 0.31
Nodes (5): maximum_scores_by_image(), raw_score_utility_index(), test_exam_marker_is_maximum_emitted_box_confidence(), test_project_config_declares_nonstandard_interpretation_and_archives(), test_raw_score_utility_matches_historical_hand_calculation()

### Community 92 - "StrictModel"
Cohesion: 0.11
Nodes (6): AnalysisSettings, DetectorSettings, InputSettings, OutputSettings, PlotSettings, StrictModel

### Community 93 - "ActivationCapture"
Cohesion: 0.13
Nodes (13): ActivationCapture, audit_layer_group_partition(), _detail_row(), _extract_reference_map(), _faster_reference_score(), _missing_reference_result(), _module_matches_prefix(), _pil_to_tensor() (+5 more)

### Community 94 - "test_check_bibliography.py"
Cohesion: 0.15
Nodes (10): citation_keys(), main(), parse_bibliography(), literal(), token(), verify(), test_duplicate_doi_rejected_even_with_different_keys(), test_literal_fields_and_metric_notation() (+2 more)

### Community 96 - "Final adversarial submission audit"
Cohesion: 0.11
Nodes (18): ANALYSIS-SCOPE SUMMARY, AUTHOR ACTION REQUIRED, BLOCKING FAILURES, CLEAN-CHECKOUT CI STATUS, COMMANDS / TESTS EXECUTED, EXTERNAL FROC SUPPORT / CAP STATUS, Final adversarial submission audit, Final rendered PDF (+10 more)

### Community 97 - "Scientific review and gap assessment"
Cohesion: 0.33
Nodes (6): Expanded-candidate inference: NO-GO for the current paper, Findings and justified corrections, Scientific review and gap assessment, Statistical and methodological distinctions that must survive editing, Supplementary material: reduce reading burden without deleting provenance, Unresolved evidence versus reporting work

### Community 98 - "VinDr-CXR adapter preflight — Batch 48"
Cohesion: 0.33
Nodes (6): Actual DICOM semantics and preprocessing, Cohort and annotation conversion, Frozen evaluator contract, Prerequisite and publication boundaries, Verification and review gate, VinDr-CXR adapter preflight — Batch 48

### Community 99 - "plot_raincloud_metrics.py"
Cohesion: 0.07
Nodes (27): _assert_close(), build_parser(), DetectorConfig, _finite_or_none(), InputConfig, load_and_audit_observations(), load_config(), main() (+19 more)

### Community 100 - "aggregate_hybrid"
Cohesion: 0.28
Nodes (8): aggregate_hybrid(), aggregate_prepared_hybrid(), _aggregate_single(), _average_precision(), DetectionEvidence, _operating_ratios(), _selected(), _weighted_average_precision()

### Community 101 - "Review Remediation Audit"
Cohesion: 0.12
Nodes (16): Adjudication summary, BibTeX citations used in repository Markdown, BLOCKING BEFORE SUBMISSION, Canonical repo-local hierarchy found in current documentation, CI and latest local verification, Citation-support audit, CLAIMS THAT SURVIVE UNCHANGED, Git state (+8 more)

### Community 102 - "seed.py"
Cohesion: 0.08
Nodes (23): _collect_nvidia_smi(), _collect_package_versions(), _collect_torch_environment(), _determinism_note(), _fallback_freeze(), initialize_reproducibility(), log_run_environment(), make_torch_generator() (+15 more)

### Community 103 - "test_cohort_characteristics.py"
Cohesion: 0.21
Nodes (10): load_cohort_characteristics_config(), parse_patient_age(), resolve_dicom_root(), test_committed_outputs_are_aggregate_only_and_match_the_immutable_total(), test_config_freezes_the_immutable_5000_study_cohort(), test_environment_dicom_root_overrides_dataset_config(), test_missing_dicom_root_requests_the_named_environment_variable(), test_patient_age_parser_distinguishes_standard_units_and_dataset_caveat() (+2 more)

### Community 104 - "yolo_reporting.py"
Cohesion: 0.08
Nodes (11): Historical boundary reconstruction and preservation, ParameterLike, summarize_parameter_counts(), evaluate_yolo_checkpoint(), plot_yolo_training_curves(), _profile_tensor(), profile_yolo_checkpoint(), summarize_yolo_artifact() (+3 more)

### Community 105 - "collect"
Cohesion: 0.09
Nodes (12): Path comparison, verify_arms(), retained(), same_predictions(), Predictor, collect(), predict_arm(), WindowDataset (+4 more)

### Community 106 - "Statistical analysis"
Cohesion: 0.12
Nodes (16): Checkpoint-conditional patient-cluster permutation and effect, Clean training-procedure results, Corruption-grid results, Endpoints, Inference protocol, Inferential targets, Interpretation limits, Pairing sensitivity and seed influence (+8 more)

### Community 107 - "Supplementary Materials Index"
Cohesion: 0.06
Nodes (32): Reading guide for supervisor review (2026-11-06), S10. YOLO numerical inference-path sensitivity, S11. Post-hoc external generalization analysis, S12. Controlled external failure diagnostic, S13. Fixed-output threshold repairability, S14. Shared-annotation FROC certificates, S1. Cohort, split, and provenance records, S2. Full clean seed-level comparison (+24 more)

### Community 108 - "Medical Object Detector Benchmark v2.0.0 — Research Artifact Release"
Cohesion: 0.12
Nodes (15): Citation, Data availability, Documentation and infrastructure changes, Known limitations, License, Major changes since v1.0.0, Manuscript status, Medical Object Detector Benchmark v2.0.0 — Research Artifact Release (+7 more)

### Community 110 - "ImagePrediction"
Cohesion: 0.11
Nodes (26): _best_proxy(), operating_evidence(), _quantile_unique(), select_qualitative_cases(), _unique_top(), _record_maps(), ImagePrediction, ImageTarget (+18 more)

### Community 111 - "External failure isolation v1: controlled diagnostic protocol"
Cohesion: 0.40
Nodes (5): External failure isolation v1: controlled diagnostic protocol, Interventions fixed before new outcomes, Measurement and inference, Questions and scope, Resource, integrity and reporting gates

### Community 112 - "Final manuscript evidence and verification audit"
Cohesion: 0.40
Nodes (5): Final manuscript evidence and verification audit, Manuscript traceability and claim boundaries, Portable CI and authorized scientific verification, Remaining author and submission work, Scientific prerequisite gate

### Community 113 - "Unified quantitative comparison"
Cohesion: 0.20
Nodes (9): Across-seed summary, Compute measurements, GFLOP counting contract and sanity check, Held-out results, One prediction-to-metric path, Operational confidence-score instability, Reproduction, Scope and freeze point (+1 more)

### Community 114 - "4. Results"
Cohesion: 0.14
Nodes (14): 4.10 Post-hoc failure decomposition and domain-change sensitivity, 4.11 Controlled retention and display diagnostic, 4.12 Limits of threshold repair on retained outputs, 4.13 Shared-annotation sensitivity, 4.1 Clean internal-testing performance, 4.2 Shared thresholds and validation-selected operating points, 4.3 Internal exact-score false-positive regimes, 4.4 Training-procedure uncertainty and conditional tests (+6 more)

### Community 115 - "AgeSettings"
Cohesion: 0.09
Nodes (7): AgeSettings, CategoricalTagSettings, ExpectedCohort, ExpectedCounts, InputSettings, OutputSettings, StrictModel

### Community 116 - "Focused Internal Manuscript Audit"
Cohesion: 0.40
Nodes (5): Completion checks and review boundary, Editorial changes, Focused Internal Manuscript Audit, Literature and claim bindings, Prerequisite gate

### Community 118 - "StrictModel"
Cohesion: 0.11
Nodes (9): Hardware, Outputs, Versions, OutputSettings, RuntimeSettings, StrictModel, TimingReuseReview, TimingReuseReviews (+1 more)

### Community 119 - "StrictModel"
Cohesion: 0.12
Nodes (6): AnalysisSettings, HypotheticalLossSettings, InputSettings, OutputSettings, PlotSettings, StrictModel

### Community 120 - "Literature Review"
Cohesion: 0.17
Nodes (12): Alternatives and planned fallback order, Common-corruption robustness, Comparability gap and contribution of the present study, Detector selection: Ultralytics YOLO11s, Explainability for object detection, Grad-CAM, Implications for the experimental design, Literature Review (+4 more)

### Community 121 - "Post-hoc external generalization results v1"
Cohesion: 0.25
Nodes (8): Candidate availability (assignment ignored), Candidate support, Cross-domain changes with shared checkpoint resampling, Interpretation boundary, Post-hoc external generalization results v1, Prevalence standardization, Reference-box error decomposition, Strict false positives and non-target findings

### Community 122 - "TimingConfig"
Cohesion: 0.21
Nodes (5): preflight(), TimingConfig, verify_history(), verify_results(), test_historical_overwrite_namespace_is_rejected()

### Community 123 - "generate_cohort_characteristics"
Cohesion: 0.18
Nodes (7): _atomic_csv(), _atomic_json(), CohortCharacteristicsConfig, _dicom_value_and_vr(), generate_cohort_characteristics(), _immutable_gate(), sha256_file()

### Community 124 - "csv"
Cohesion: 0.07
Nodes (9): csv_bytes(), figure_bytes(), read_rows(), main(), prepare(), test_manifest_extension_preserves_existing_entries_and_rejects_repeat(), test_run_eda_creates_distribution_samples_and_summary(), _write_manifest() (+1 more)

### Community 125 - "Hypothesis Traceability"
Cohesion: 0.25
Nodes (8): H1 — Detection coverage and average precision, H2 — A shared threshold does not define a shared operating regime, H3 — Accuracy-compute Pareto trade-off, H4 — Corruption degradation is type- and severity-specific, H5 — Grad-CAM is a failure-analysis tool, not clinical-reasoning evidence, H6 — Detection confidence calibration, Hypothesis Traceability, Interpretation rule

### Community 126 - "load_config"
Cohesion: 0.18
Nodes (5): hardware_snapshot(), load_config(), main(), test_hardware_gate_refuses_cpu_before_any_measurement(), test_history_tampering_is_detected()

### Community 129 - "External failure isolation v1: executed diagnostic results"
Cohesion: 0.29
Nodes (7): External failure isolation v1: executed diagnostic results, False positives per negative-control image, Full-cohort evaluation-floor control, Historical-threshold recall, Limits, One-to-one geometric coverage (IoU 0.25), One-to-one geometric coverage (IoU 0.50)

### Community 130 - "Datasheet: RSNA Pneumonia Detection Challenge 2018"
Cohesion: 0.18
Nodes (11): Acquisition provenance, Annotation conversion and image processing, Collection and annotation, Datasheet: RSNA Pneumonia Detection Challenge 2018, Hardware-scoped benchmark subset, Integrity checks, Known biases and risks, License and access conditions (+3 more)

### Community 131 - "Final Submission Audit"
Cohesion: 0.18
Nodes (11): Analysis-scope table, BLOCKING FAILURES, Exact commands/tests run and results, Final statement, Final Submission Audit, Language-search audit, Numerical traceability (29 manuscript numbers), Recorded repository and CI state (+3 more)

### Community 132 - "Limitations"
Cohesion: 0.14
Nodes (14): Annotation and preprocessing scope, Compute and sampling scope, Controlled diagnostic update (2026-11-05), Dataset, population, and target scope, Deployment and regulatory scope, Detector-comparison validity, Explainability scope, Fixed-output repairability extension (+6 more)

### Community 133 - "holm_adjust"
Cohesion: 0.22
Nodes (7): holm_adjust(), apply_clean_holm(), apply_grid_holm(), test_clean_holm_fails_closed_if_an_endpoint_is_missing(), test_clean_holm_uses_exact_seven_endpoint_family(), test_grid_holm_excludes_explicitly_non_estimable_hypotheses(), test_holm_adjustment_is_monotone_in_sorted_p_values()

### Community 134 - "StrictModel"
Cohesion: 0.18
Nodes (4): AnalysisSettings, InputSettings, OutputSettings, StrictModel

### Community 135 - "load_phase5_config"
Cohesion: 0.19
Nodes (15): validate_protocol_contract(), aggregate_rows(), load_phase5_config(), _aggregation_row(), test_aggregation_rejects_invalid_missingness_contract(), test_aggregation_rejects_partially_defined_conditional_metrics(), test_aggregation_rejects_undefined_reason_that_disagrees_with_counts(), test_aggregation_retains_all_attempts_but_uses_defined_conditional_n() (+7 more)

### Community 136 - "StrictModel"
Cohesion: 0.15
Nodes (6): DiagnosticSettings, InputSettings, MetadataContract, OutputSettings, RuntimeSettings, StrictModel

### Community 137 - "Controlled external failure diagnostic: interpretation and verification"
Cohesion: 0.33
Nodes (6): Baseline and continuation boundary, Controlled external failure diagnostic: interpretation and verification, Manuscript, prior art and remaining limits, Reproduction and actual check outcomes, Scientific findings and interpretation, What was executed and independently checked

### Community 138 - "Radiography-Motivated Synthetic Acquisition/Display Sensitivity"
Cohesion: 0.20
Nodes (10): Condition-by-condition scientific classification, Current DICOM-standard interpretation, Descriptive performance sensitivity, Distinction from post-conversion digital corruptions, Effect of canonical per-image min-max preprocessing, MONOCHROME polarity and DICOM `LINEAR` implementation, Question, frozen scope, and Batch 32 correction, Radiography-Motivated Synthetic Acquisition/Display Sensitivity (+2 more)

### Community 139 - "Author Declarations — Action Required"
Cohesion: 0.20
Nodes (10): Author contributions, Author Declarations — Action Required, Authorship and journal — supplied facts, Competing interests, Consent applicability, Data and code availability, Ethics and data-use determination, Final insertion checklist (+2 more)

### Community 140 - "Dataset choice"
Cohesion: 0.20
Nodes (9): Annotation quality, Balance and task definition, Dataset choice, Decision, Hardware-scoped subset, Inspection method, Licensing, Suitability for the comparison (+1 more)

### Community 141 - "VinDr-CXR external testing protocol v1"
Cohesion: 0.20
Nodes (10): 1. Scientific question and prerequisite gate, 2. Release, access, provenance and sharing, 3. Population and strict target ontology, 4. Frozen DICOM and model execution contract, 5. Endpoints and candidate support, 6. Frozen threshold transport and score summaries, 7. Observational unit, aggregation and uncertainty, 8. Planned outputs and prohibited tuning (+2 more)

### Community 142 - "benchmark_inference.py"
Cohesion: 0.28
Nodes (3): select_indices(), Subset, test_subset_is_order_invariant_and_changes_with_seed()

### Community 143 - "3. Materials and Methods"
Cohesion: 0.14
Nodes (14): 3.10 Subsequent controlled implementation diagnostic, 3.11 Fixed-output threshold repairability, 3.12 Shared-annotation FROC certificates, 3.1 Dataset, target, and patient-disjoint split, 3.2 Detector pipelines and controlled training factors, 3.3 Five retained runs and common evaluation, 3.4 Operating-point protocols and exact-score FROC, 3.5 Frozen VinDr external testing (+6 more)

### Community 145 - "Threshold repairability v2: execution and verification"
Cohesion: 0.40
Nodes (5): Independent and software checks, Manuscript and review status, Scientific evidence, Scientific interpretation, Threshold repairability v2: execution and verification

### Community 146 - "analyze_exact_score_froc.py"
Cohesion: 0.11
Nodes (10): aggregate_exact_frontier(), audit_selected_points_against_canonical_matcher(), build_run_reachability(), compare_historical_and_exact(), compare_prior_and_current_exact(), compare_prior_and_current_runs(), conservative_frontier_bounds(), _sample_std() (+2 more)

### Community 148 - "Detection-Confidence Calibration"
Cohesion: 0.22
Nodes (8): Definition and verified implementation, Descriptive finding, Detection-Confidence Calibration, Population and decision-analysis boundary, Predeclared descriptive sensitivity, Primary support and occupancy, Reliability-diagram scope, Versioned artifacts and reproduction

### Community 149 - "test_xai_sanity.py"
Cohesion: 0.09
Nodes (20): aggregate_sanity(), load_xai_sanity_config(), map_similarity_metrics(), normalize_map_for_similarity(), pearson_map_correlation(), _pearson_values(), select_nested_stratified_rows(), shuffle_pixel_vectors() (+12 more)

### Community 150 - "Research Question and Hypotheses"
Cohesion: 0.22
Nodes (9): H1 - Detection coverage and average precision, H2 - A shared threshold does not define a shared operating regime, H3 - Accuracy-compute Pareto trade-off, H4 - Corruption degradation is type- and severity-specific, H5 - Grad-CAM is a failure-analysis tool, not clinical-reasoning evidence, H6 - Detection confidence calibration, Primary research question, Research Question and Hypotheses (+1 more)

### Community 151 - "Post-hoc external generalization protocol v1"
Cohesion: 0.25
Nodes (8): Inputs and common contracts, Outputs and verification, Post-hoc external generalization protocol v1, RQ1: observable external error structure, RQ2: ontology sensitivity and expert gate, RQ3: population weighting sensitivity, RQ4: cross-domain changes, RQ5: candidate support

### Community 152 - "Reproducibility contract"
Cohesion: 0.22
Nodes (9): Aggregate RSNA cohort-characteristics reproduction, Environment and dependency locks, Exact checkpoint audit and release boundary, Exact-score FROC committed-analysis reproduction, Five-run validation threshold-selection sensitivity, Machine-checkable committed evidence, Release-candidate verification, Reproducibility contract (+1 more)

### Community 153 - "Recall-Weighted F-beta Threshold Sensitivity"
Cohesion: 0.22
Nodes (8): Artifacts and reproduction, F-beta findings and threshold stability, Recall-Weighted F-beta Threshold Sensitivity, Relationship to the primary operating points, Scope and limitations, Separate hypothetical detection-error loss, Validation-only method, What beta does

### Community 154 - "VinDr statistics and cross-dataset transportability — Batch 50"
Cohesion: 0.22
Nodes (9): A. Ranking and B. false-positive-regime transport, C. Score scale and detection counts, Candidate support remains incomplete, Central question, Checkpoint-conditional sensitivity and complete provenance, D. Frozen operating points and n=3 versus n=5 sensitivity, Population and estimands, Primary uncertainty on VinDr (+1 more)

### Community 155 - "load_robustness_config"
Cohesion: 0.23
Nodes (7): draw_stratified_subsample(), _largest_remainder_allocation(), load_robustness_config(), SamplingSettings, test_largest_remainder_allocation_is_exact_and_proportional(), test_phase6_config_is_primary_seed_and_matches_required_grid(), test_stratified_sample_is_reproducible_and_preserves_allocations()

### Community 156 - "analyze_pair"
Cohesion: 0.21
Nodes (8): estimate_pair(), EvidencePair, HybridEvidence, prepare_hybrid(), _build_and_validate_evidence(), _phase5_pairs(), _seed_influence_diagnostics(), _validate_clean_seed_eligibility()

### Community 157 - "analyze_training_procedure"
Cohesion: 0.27
Nodes (4): analyze_training_procedure(), estimate_independent_runs(), estimate(), IndependentEvidenceRuns

### Community 158 - "draw_hierarchical_bootstrap_multiplicities"
Cohesion: 0.31
Nodes (5): analyze_pair(), draw_hierarchical_bootstrap_multiplicities(), expand_patient_group_choices(), expand_patient_group_multiplicities(), test_patient_group_draws_and_swaps_move_complete_clusters()

### Community 159 - "_aggregate_row"
Cohesion: 0.25
Nodes (5): _aggregate_row(), AggregateAccumulator, MetadataSettings, _percent(), test_aggregate_row_contains_counts_percentages_and_no_identifier_fields()

### Community 160 - "[2.0.0] — Research Artifact Release"
Cohesion: 0.25
Nodes (7): [1.0.0], [2.0.0] — Research Artifact Release, Changelog, Documentation, Infrastructure, Reproducibility and verification, Scientific analysis

### Community 161 - "Post-hoc external generalization v1 — execution and verification"
Cohesion: 0.29
Nodes (7): Evidence and preservation, Executed commands and outcomes, Figures, manuscript, privacy and remaining work, Implementation corrections and preserved attempts, Post-hoc external generalization v1 — execution and verification, Publication gate, Subsequent PDF follow-up — 2026-10-29

### Community 162 - "Exploratory Raw-Score Threshold Utility/Sensitivity (Non-Standard DCA)"
Cohesion: 0.25
Nodes (8): Exploratory Raw-Score Threshold Utility/Sensitivity (Non-Standard DCA), Method references, Population and prevalence boundary, Preserved and relabeled artifacts, Reproduction, Status and corrective decision, Verified historical construction, Why probability-based salvage was not performed

### Community 163 - "Decision log"
Cohesion: 0.17
Nodes (12): D-016 — Matched decoded-host timing v1 supersedes primary asymmetric timing, D-017 — Freeze VinDr-CXR external testing v1 before performance, D-018 — Retain complete frozen VinDr external inference and adverse results, D-020 — Integrate frozen external evidence and preserve the verification boundary, D-021 — Audit the final science and derive the author-review article, D-022 — Incorporate supplied author declarations and preserve the audited snapshot, D-023 — Retain numerical-path harmonisation as secondary sensitivity, D-024 — Post-hoc external generalization diagnostics (2026-10-29) (+4 more)

### Community 164 - "Final submission audit and author-declaration follow-up"
Cohesion: 0.18
Nodes (11): 2026-09-27 declaration wording and PDF refresh, 2026-10-29 post-hoc PDF refresh and visual review, 2026-11-06 supervisor-review preparation and current PDF, 2026-11-07 threshold-repairability revision and current PDF, Final submission audit and author-declaration follow-up, Historical author-review record: 2026-09-25, PDF inspection at 2026-09-25, Remaining author/submission actions (+3 more)

### Community 166 - "Reporting Checklist Crosswalk"
Cohesion: 0.20
Nodes (10): Author-only release gates, Authoritative guideline sources, CLAIM 2024 primary crosswalk, Preserved earlier context, Publication readiness and CLAIM 2024 crosswalk, Required sample-size and subset-selection row, STARD-AI 2025 selected reporting crosswalk by analogy, Submission blockers and linked audits (+2 more)

### Community 167 - "Frozen VinDr-CXR inference results — Batch 49"
Cohesion: 0.25
Nodes (8): Achieved FP/image and candidate-floor limits, AP and prespecified FROC sensitivities, Equal-run AP summaries, Execution and numerical handoff audit, Frozen VinDr-CXR inference results — Batch 49, Historical n=3 RSNA threshold transport — PRIMARY, Post-hoc n=5 RSNA threshold transport — SECONDARY sensitivity, Score distributions at the four prespecified supports

### Community 168 - "run_statistics.py"
Cohesion: 0.16
Nodes (10): AnalysisSettings, build_parser(), CleanSeedEligibility, _expected_metric_vector(), ExpectedUndefinedConditional, InputSettings, main(), OutputSettings (+2 more)

### Community 169 - "2. Related Work"
Cohesion: 0.29
Nodes (7): 2.1 Detector scores and operating-point assessment, 2.2 RSNA methodology and direct detector comparisons, 2.3 Implementation and reporting context, 2.4 External testing under a different annotation ontology, 2.5 Error diagnostics and the incremental contribution, 2.6 Annotation sensitivity and the scope of the method, 2. Related Work

### Community 171 - "Threshold repairability v2: computational protocol"
Cohesion: 0.33
Nodes (6): Controlled output perturbations, Joint uncertainty, Main estimands and invariance scope, Scope and fixed evidence, Threshold repairability v2: computational protocol, Verification, runtime and interpretation gates

### Community 172 - "Threshold repairability v2: complete computational results"
Cohesion: 0.40
Nodes (5): Components at 0.25 FP/image, Controlled output changes, Coupled contrasts, Scope and audit trail, Threshold repairability v2: complete computational results

### Community 174 - "Citation Audit"
Cohesion: 0.29
Nodes (7): Architecture, software, and evaluation methods, Bibliography entries not cited by the current manuscript, Calibration, XAI, statistics, DICOM, and decision analysis, Citation Audit, Corrections made during this audit, Dataset and domain-background sources, Reporting-standard sources used by the audit

### Community 175 - "Frozen VinDr statistics and cross-dataset transportability"
Cohesion: 0.29
Nodes (7): Artifacts and replay, Estimands and conditioning, Exact reconstruction and technical verification, Frozen VinDr statistics and cross-dataset transportability, Internal comparison and support limits, Observation units and joint resampling, Preserved rendering-order correction

### Community 176 - "Scientific interpretation of post-hoc external generalization v1"
Cohesion: 0.40
Nodes (5): Competing explanations remain unresolved, Contribution and relation to primary literature, Recommendation to the supervising professor, Scientific interpretation of post-hoc external generalization v1, What the retained evidence establishes

### Community 177 - "Citation Verification Audit"
Cohesion: 0.50
Nodes (4): Citation Verification Audit, Current final manuscript — 2026-09-25, Historical audit retained verbatim (through 2026-09-07), Post-hoc extension — 2026-10-29

### Community 178 - "Dataset workspace"
Cohesion: 0.33
Nodes (5): Acquire and prepare, Credentials and competition access, Dataset workspace, Locally inspected source files, Selected source

### Community 181 - "Frozen VinDr-CXR inference — Batch 49"
Cohesion: 0.33
Nodes (6): Evidence and replay, Frozen VinDr-CXR inference — Batch 49, Interpretation boundaries, Observed findings and adverse results, Prerequisite and implementation checks, Preserved initial implementation failure

### Community 182 - "YOLO numerical inference-path sensitivity, v1"
Cohesion: 0.33
Nodes (6): Candidate agreement, Completed result and interpretation, Frozen design and execution gate, Reproduction, Verification and review gate, YOLO numerical inference-path sensitivity, v1

### Community 193 - "Research audit: external generalization v1"
Cohesion: 0.50
Nodes (4): Bugs distinguished from limitations, Confirmed prior analyses and scientific limitations, Executable work and remaining prerequisites, Research audit: external generalization v1

### Community 198 - "D-002 — Descope Track B and reframe the research contribution"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-002 — Descope Track B and reframe the research contribution, Decision

### Community 199 - "D-004 — Keep later validation-threshold sensitivity separate from the primary thresholds"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-004 — Keep later validation-threshold sensitivity separate from the primary thresholds, Decision

### Community 200 - "D-005 — Separate inferential targets and resample detector runs independently"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-005 — Separate inferential targets and resample detector runs independently, Decision

### Community 201 - "D-006 — Treat beta as an F-beta preference parameter and separate linear loss"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-006 — Treat beta as an F-beta preference parameter and separate linear loss, Decision

### Community 202 - "D-007 — Remove raw detector-score curves from conventional DCA interpretation"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-007 — Remove raw detector-score curves from conventional DCA interpretation, Decision

### Community 203 - "D-008 — Use n=5 as the principal operating-regime sensitivity display"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-008 — Use n=5 as the principal operating-regime sensitivity display, Decision

### Community 204 - "D-009 — Use one version for software and research-artifact releases"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-009 — Use one version for software and research-artifact releases, Decision

### Community 205 - "D-010 — Keep `paper_draft.md` as the canonical editable journal manuscript"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-010 — Keep `paper_draft.md` as the canonical editable journal manuscript, Decision

### Community 206 - "D-011 — Use the observed exact-score frontier and retain the candidate-floor boundary"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-011 — Use the observed exact-score frontier and retain the candidate-floor boundary, Decision

### Community 207 - "D-012 — Adopt the approved 0.0001 FROC sensitivity and retain the residual boundary"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-012 — Adopt the approved 0.0001 FROC sensitivity and retain the residual boundary, Decision

### Community 208 - "D-013 — Adopt the approved 0.00001 FROC sensitivity and stop at the residual bound"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-013 — Adopt the approved 0.00001 FROC sensitivity and stop at the residual bound, Decision

### Community 209 - "D-014 — Retain n=3 threshold provenance and report n=5 selection only as post-hoc sensitivity"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-014 — Retain n=3 threshold provenance and report n=5 selection only as post-hoc sensitivity, Decision

### Community 210 - "D-015 — Report aggregate DICOM-header cohort characteristics with an age-unit caveat"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-015 — Report aggregate DICOM-header cohort characteristics with an age-unit caveat, Decision

### Community 211 - "D-003 — Decline to revive a Track-B-style native/best-practice comparison"
Cohesion: 0.50
Nodes (4): Consequences, Context, D-003 — Decline to revive a Track-B-style native/best-practice comparison, Decision

### Community 212 - "D-001 — Two-track detector comparison design"
Cohesion: 0.50
Nodes (4): Context, D-001 — Two-track detector comparison design, Outcome, Proposal

### Community 215 - "D-019 — Separate observed ranking transport from frozen operating-point transport"
Cohesion: 0.67
Nodes (3): Context and decision, D-019 — Separate observed ranking transport from frozen operating-point transport, Interpretation and boundaries

## Knowledge Gaps
- **1 isolated node(s):** `meddet-benchmark`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 2135 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Path comparison` connect `collect` to `sha256_file`, `README.md`, `CocoDetectionDataset`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ImagePrediction` (e.g. with `One prediction-to-metric path` and `exact_score_froc_rows()`) actually correct?**
  _`ImagePrediction` has 42 INFERRED edges - model-reasoned connections that need verification._
- **What connects `meddet-benchmark` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `prepare.py` be split into smaller, more focused modules?**
  _Cohesion score 0.051287128712871284 - nodes in this community are weakly interconnected._
- **Why does `YOLO numerical inference-path audit (Batch 53, v1)` connect `README.md` to `collect`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Should `analyze_yolo_numerical_path.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05209397344228805 - nodes in this community are weakly interconnected._
- **Why does `ImagePrediction` connect `ImagePrediction` to `analyze_yolo_numerical_path.py`, `threshold_calibration.py`, `run_statistics.py`, `calibration.py`, `load_phase5_config`, `evaluate_vindr_external.py`, `analyze_threshold_repairability.py`, `test_external_generalization.py`, `evaluation.py`, `analyze_yolo_seed_stability.py`, `evaluate_threshold_sweep.py`, `run_vindr_statistics.py`, `analyze_exact_score_froc.py`, `run_explainability.py`, `numpy`, `evaluate_threshold_selection.py`, `run_robustness.py`, `meddet_benchmark/config.py`, `dataclasses`, `run_statistics.py`, `test_transportability.py`, `analyze_external_failure.py`, `test_statistics.py`, `Any`, `numpy`, `test_exact_score_froc.py`, `sha256_file`, `test_evaluate_vindr_external.py`, `evaluate_coco`, `yolo_reporting.py`, `collect`, `Unified quantitative comparison`, `csv`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._