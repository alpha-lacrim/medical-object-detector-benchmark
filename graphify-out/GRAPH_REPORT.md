# Graph Report - DP_Final_Project  (2026-11-06)

## Corpus Check
- 360 files · ~2,877,675 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 362 file(s) not represented in the graph (top: .csv 170, .gz 157, (none) 17)

## Summary
- 4506 nodes · 12338 edges · 190 communities (168 shown, 22 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 484 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `31942439`
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
- test_statistics.py
- radiography_shifts.py
- YoloConfig
- decision_curve_pre_batch30_nonstandard.py
- seed_everything
- faster_rcnn_config.py
- hashlib
- evaluate_threshold_selection.py
- run_robustness.py
- sanity_checks.py
- meddet_benchmark/config.py
- analyze_operating_regime_sensitivity.py
- test_train_faster_rcnn.py
- report_transportability.py
- os
- train_yolo.py
- test_xai_sanity.py
- 3. Materials and Methods
- plot_pareto_frontier.py
- StrictModel
- argparse
- test_transportability.py
- Medical Object Detector Benchmark
- raw_score_utility.py
- test_external_failure.py
- README.md
- paired.py
- visualize.py
- math
- test_radiography_shifts.py
- batch52/paper_draft.md
- Any
- StrictModel
- build_scientific_artifact_manifest.py
- Float32DetectionLoss
- StrictModel
- test_threshold_repairability.py
- decision_curve.py
- PROJECT_PLAN.md
- json
- batch46/paper_draft.md
- build_faster_rcnn
- YoloRunTracker
- test_exact_score_froc.py
- cohort_characteristics.py
- retained
- Project plan: controlled lung-opacity detector comparison
- collections_abc
- load_pareto_points
- report.md
- SelectionSettings
- pytest
- MatchedDetectionTrainer
- evaluate_vindr_external.py
- numpy
- sha256_file
- configure_reproducibility
- window_pixels
- V7 Q2 / VinDr Baseline Audit
- test_check_bibliography.py
- load_faster_rcnn_config
- test_inference_timing.py
- evaluate_coco
- Grad-CAM Sensitivity Controls (v2)
- ComparableEarlyStopping
- Clinical annotation-adjudication protocol v1
- explainability/config.py
- load_robustness_config
- Supervisor briefing: transportability evidence and publication decision
- Supervisor-review preparation: execution and verification
- StrictModel
- _parse_outputs
- StrictModel
- Research direction: limits of threshold repair under external shift
- faster_rcnn_reporting.py
- analyze_exact_score_froc.py
- Final adversarial submission audit
- Scientific review and gap assessment
- VinDr-CXR adapter preflight — Batch 48
- plot_raincloud_metrics.py
- 2. Related Work
- Review Remediation Audit
- csv
- test_cohort_characteristics.py
- yolo_training.py
- Statistical analysis
- YOLO numerical-path sensitivity: results v1
- Medical Object Detector Benchmark v2.0.0 — Research Artifact Release
- External failure isolation v1: controlled diagnostic protocol
- Final manuscript evidence and verification audit
- Unified quantitative comparison
- 4. Results
- AgeSettings
- Focused Internal Manuscript Audit
- Citation Verification Audit
- Literature Review
- Post-hoc external generalization results v1
- StrictModel
- generate_cohort_characteristics
- RuntimeSettings
- Hypothesis Traceability
- AggregateAccumulator
- External failure isolation v1: executed diagnostic results
- Datasheet: RSNA Pneumonia Detection Challenge 2018
- Final Submission Audit
- Limitations
- Supplementary Materials Index
- StrictModel
- load_phase5_config
- model_validator
- Controlled external failure diagnostic: interpretation and verification
- Radiography-Motivated Synthetic Acquisition/Display Sensitivity
- Author Declarations — Action Required
- Dataset choice
- VinDr-CXR external testing protocol v1
- 3. Materials and Methods
- draw_independent_run_bootstrap_multiplicities
- conftest.py
- Detection-Confidence Calibration
- map_similarity_metrics
- Research Question and Hypotheses
- Post-hoc external generalization protocol v1
- Reproducibility contract
- Recall-Weighted F-beta Threshold Sensitivity
- VinDr statistics and cross-dataset transportability — Batch 50
- [2.0.0] — Research Artifact Release
- Post-hoc external generalization v1 — execution and verification
- Exploratory Raw-Score Threshold Utility/Sensitivity (Non-Standard DCA)
- Decision log
- Final submission audit and author-declaration follow-up
- Reporting Checklist Crosswalk
- Frozen VinDr-CXR inference results — Batch 49
- Citation Audit
- Frozen VinDr statistics and cross-dataset transportability
- Scientific interpretation of post-hoc external generalization v1
- Dataset workspace
- COMPUTE_TIMING.md
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
- conservative_frontier_bounds
- meddet-benchmark

## God Nodes (most connected - your core abstractions)
1. `ImagePrediction` - 121 edges
2. `sha256_file()` - 115 edges
3. `ImageTarget` - 94 edges
4. `load_phase5_config()` - 46 edges
5. `CocoDetectionDataset` - 44 edges
6. `load_faster_rcnn_config()` - 41 edges
7. `evaluate_operating_point()` - 38 edges
8. `_run_training()` - 37 edges
9. `evaluate_coco()` - 35 edges
10. `run_statistics()` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Prerequisite and implementation checks` --references--> `Predictor`  [INFERRED]
  docs/VINDR_INFERENCE.md → src/benchmark_inference.py
- `VinDr-CXR frozen external testing (Batches 47–49)` --references--> `prepare()`  [INFERRED]
  README.md → src/collect_external_failure.py
- `Actual DICOM semantics and preprocessing` --references--> `scale_radiograph_to_uint8()`  [INFERRED]
  docs/VINDR_ADAPTER_PREFLIGHT.md → src/data/prepare.py
- `4. Frozen DICOM and model execution contract` --references--> `scale_radiograph_to_uint8()`  [INFERRED]
  docs/VINDR_EXTERNAL_PROTOCOL.md → src/data/prepare.py
- `Implementation and efficiency audit` --references--> `restore_native_bounds()`  [INFERRED]
  docs/FINAL_SUBMISSION_AUDIT_2026-09-24.md → src/evaluate_vindr_external.py

## Import Cycles
- None detected.

## Communities (190 total, 22 thin omitted)

### Community 0 - "prepare.py"
Cohesion: 0.05
Nodes (45): _add_issue(), _allocate_exact_counts(), _audit_summary(), AuditIssue, AuditResult, _balanced_group_order(), BoundingBox, build_coco() (+37 more)

### Community 1 - "analyze_yolo_numerical_path.py"
Cohesion: 0.07
Nodes (33): main(), number(), render(), candidate_agreement(), canonical_bytes(), check_inputs(), digest(), distribution() (+25 more)

### Community 2 - "CocoDetectionDataset"
Cohesion: 0.06
Nodes (36): CocoAnnotation, CocoCategory, CocoDetectionDataset, CocoImageRecord, CocoValidationError, _configured_path(), DatasetPreflight, detection_collate_fn() (+28 more)

### Community 3 - "threshold_calibration.py"
Cohesion: 0.09
Nodes (40): _artifact(), _atomic_bytes(), _atomic_csv(), _atomic_json(), _atomic_sensitivity_figure(), BootstrapPlan, compute_calibration_curve(), compute_hypothetical_loss_curve() (+32 more)

### Community 4 - "download.py"
Cohesion: 0.05
Nodes (41): build_parser(), _child_environment(), ConfigurationError, _credential_file_path(), CredentialError, CredentialSource, download_competition_files(), _download_failure_message() (+33 more)

### Community 5 - "run_statistics.py"
Cohesion: 0.10
Nodes (38): holm_adjust(), apply_clean_holm(), apply_grid_holm(), _artifact_hash(), _atomic_bytes(), _atomic_csv(), _atomic_csv_fields(), _atomic_json() (+30 more)

### Community 6 - "train_faster_rcnn.py"
Cohesion: 0.07
Nodes (25): config_fingerprint(), FasterRCNNConfig, serializable_config(), _approved_benchmark(), _atomic_torch_save(), _available_subset(), _checkpoint_payload(), _completed_artifacts_intact() (+17 more)

### Community 7 - "calibration.py"
Cohesion: 0.05
Nodes (49): _add_detector_summaries(), _atomic_binning_sensitivity_figure(), _atomic_bytes(), _atomic_csv(), _atomic_floor_sensitivity_figure(), _atomic_json(), _atomic_reliability_figure(), _atomic_support_figure() (+41 more)

### Community 8 - "faster_rcnn_reporting.py"
Cohesion: 0.09
Nodes (25): append_epoch_metrics(), build_benchmark_projection(), _csv_cell(), _csv_text(), _json_text(), _load_epoch_csv(), _load_epoch_jsonl(), load_epoch_metrics() (+17 more)

### Community 9 - "evaluate_vindr_external.py"
Cohesion: 0.08
Nodes (31): Evidence baseline and implementation map, main(), build_targets(), decode_image(), ensure_private(), geometry_check(), main(), PreflightError (+23 more)

### Community 10 - "analyze_validation_threshold_sensitivity.py"
Cohesion: 0.07
Nodes (44): _aggregate_test_rows(), _artifact(), ArtifactBinding, build_conclusion_rows(), build_parser(), _bundle_record(), classify_margin_change(), collect_validation_predictions() (+36 more)

### Community 11 - "analyze_threshold_repairability.py"
Cohesion: 0.15
Nodes (9): binding(), calculate(), csv_bytes(), figure_bytes(), read_rows(), require(), run(), unique_runs() (+1 more)

### Community 12 - "test_external_generalization.py"
Cohesion: 0.09
Nodes (33): ap_events(), distribution(), error_decomposition(), joint_bootstrap(), evaluate(), local_annotations(), prevalence_metrics(), prevalence_weights() (+25 more)

### Community 13 - "evaluation.py"
Cohesion: 0.08
Nodes (33): _best_proxy(), operating_evidence(), _quantile_unique(), select_qualitative_cases(), _unique_top(), box_iou(), _boxes(), evaluate_operating_point() (+25 more)

### Community 14 - "analyze_yolo_seed_stability.py"
Cohesion: 0.14
Nodes (22): _artifact(), _atomic_bytes(), _atomic_csv(), build_parser(), classify_convergence(), classify_operational(), InputSettings, load_config() (+14 more)

### Community 15 - "evaluate_threshold_sweep.py"
Cohesion: 0.07
Nodes (32): aggregate_threshold_rows(), _artifact(), _atomic_bytes(), _atomic_csv(), _atomic_figure(), _atomic_json(), build_parser(), _deserialize_predictions() (+24 more)

### Community 16 - "run_vindr_statistics.py"
Cohesion: 0.05
Nodes (42): binding(), extend(), main(), register(), render(), verify(), analyze(), main() (+34 more)

### Community 17 - "verify_scientific_artifacts.py"
Cohesion: 0.13
Nodes (22): ArtifactVerificationError, _load_json(), main(), _parser(), _png_dimensions(), _relative_path(), sha256_file(), _valid_sha256() (+14 more)

### Community 18 - "run_explainability.py"
Cohesion: 0.09
Nodes (38): ExplainabilityConfig, load_explainability_config(), ActivationCapture, aggregate_localization(), _atomic_bytes(), _atomic_csv(), _atomic_json(), _best_candidate_index() (+30 more)

### Community 19 - "meddet_benchmark/corruptions.py"
Cohesion: 0.07
Nodes (23): apply_corruption(), build_transform(), corruption_fingerprint(), CorruptionApplier, CorruptionCondition, CorruptionConfig, CorruptionDefinition, _derived_seed() (+15 more)

### Community 20 - "test_statistics.py"
Cohesion: 0.11
Nodes (31): evaluate_prediction_records(), EvaluationSettings, _record_maps(), ImagePrediction, ImageTarget, evaluate_yolo_checkpoint(), _target(), build_evidence() (+23 more)

### Community 21 - "radiography_shifts.py"
Cohesion: 0.11
Nodes (29): sha256_file(), AcquisitionShiftConfig, _audit_raw_files(), _audit_value(), build_parser(), _bundle_identity(), _bundle_path(), _condition_payload() (+21 more)

### Community 22 - "YoloConfig"
Cohesion: 0.08
Nodes (17): load_yolo_config(), StrictModel, YoloBenchmarkConfig, YoloConfig, YoloDataConfig, YoloEarlyStoppingConfig, YoloEvaluationConfig, YoloLossConfig (+9 more)

### Community 23 - "decision_curve_pre_batch30_nonstandard.py"
Cohesion: 0.06
Nodes (29): AnalysisSettings, _artifact(), _atomic_csv(), _atomic_figure(), _atomic_json(), compute_decision_curves(), contiguous_ranges(), DecisionCurveConfig (+21 more)

### Community 24 - "seed_everything"
Cohesion: 0.22
Nodes (9): _random_sample(), test_initialization_can_defer_environment_writes_until_after_a_gate(), test_initialize_reproducibility_seeds_torch_and_writes_run_metadata(), test_nvidia_smi_parser_tolerates_quoted_and_unavailable_values(), test_package_logging_falls_back_when_pip_is_unavailable(), test_seed_everything_accepts_only_valid_cublas_workspace_settings(), test_seed_everything_rejects_out_of_range_values(), test_seed_everything_repeats_python_and_numpy_streams() (+1 more)

### Community 25 - "faster_rcnn_config.py"
Cohesion: 0.14
Nodes (27): BenchmarkSettings, _channel_values(), DataPaths, EarlyStoppingSettings, EvaluationSettings, _mapping(), _non_negative_int(), OptimizerSettings (+19 more)

### Community 26 - "hashlib"
Cohesion: 0.12
Nodes (12): _atomic_json(), _atomic_text(), _balanced_smoke(), _ensure_hardlink(), _image_manifest_sha256(), _label_text(), _load_coco(), prepare_yolo_dataset() (+4 more)

### Community 27 - "evaluate_threshold_selection.py"
Cohesion: 0.09
Nodes (29): _artifact(), _atomic_bytes(), _atomic_csv(), _atomic_json(), build_parser(), collect_validation_predictions(), _frozen_faster_config_sha256(), InputSettings (+21 more)

### Community 28 - "run_robustness.py"
Cohesion: 0.12
Nodes (29): _atomic_bytes(), _atomic_csv(), _atomic_json(), build_parser(), _bundle_identity(), _bundle_path(), _cached_result(), _clean_predictions() (+21 more)

### Community 29 - "sanity_checks.py"
Cohesion: 0.16
Nodes (22): _atomic_bytes(), _atomic_csv(), _atomic_json(), build_parser(), checkpoint_hashes(), _detail_row(), _draw_candidate(), _historical_artifact_identity() (+14 more)

### Community 30 - "meddet_benchmark/config.py"
Cohesion: 0.06
Nodes (34): assert_run_allowed(), canonical_json(), config_fingerprint(), DataConfig, EvaluationConfig, ExperimentConfig, load_experiment(), Manifests (+26 more)

### Community 31 - "analyze_operating_regime_sensitivity.py"
Cohesion: 0.10
Nodes (26): _artifact(), _atomic_csv(), _atomic_json(), build_conclusion_rows(), build_fixed_threshold_tables(), build_inventory_rows(), build_parser(), classify_margin_change() (+18 more)

### Community 32 - "test_train_faster_rcnn.py"
Cohesion: 0.13
Nodes (13): sha256_file(), build_parser(), _dataset_summary(), split_summary(), _load_datasets(), main(), _coco_payload(), test_approved_benchmark_binds_data_execution_and_implementation() (+5 more)

### Community 33 - "report_transportability.py"
Cohesion: 0.10
Nodes (13): render(), table(), number(), plot_froc(), plot_scores(), plot_thresholds(), render(), report() (+5 more)

### Community 34 - "os"
Cohesion: 0.08
Nodes (29): _atomic_bytes(), aggregate_froc_curve(), AnalysisSettings, _artifact(), _atomic_csv(), _atomic_figure(), _atomic_json(), build_parser() (+21 more)

### Community 35 - "train_yolo.py"
Cohesion: 0.12
Nodes (10): _execution_identity(), _guard_new_run(), _implementation_identity(), main(), _preflight(), _register_tracker(), _require_benchmark(), _run_ultralytics() (+2 more)

### Community 36 - "test_xai_sanity.py"
Cohesion: 0.07
Nodes (27): aggregate_sanity(), assert_checkpoint_immutability(), audit_layer_group_partition(), DetectorLayerGroups, LayerGroup, load_xai_sanity_config(), _module_matches_prefix(), ParameterInitializationSettings (+19 more)

### Community 37 - "3. Materials and Methods"
Cohesion: 0.05
Nodes (39): 1. Introduction, 2.1 Two-stage and one-stage detector organization, 2.2 The comparability gap in medical detection studies, 2.3 Robustness, calibration, and explanation, 2. Related Work, 3.10 Inferential targets and patient-cluster protocol, 3.11 Retrospective hypothesis and reporting status, 3.1 Dataset, target, and patient-disjoint split (+31 more)

### Community 38 - "plot_pareto_frontier.py"
Cohesion: 0.10
Nodes (17): aggregate_pareto_points(), _artifact(), _assert_close(), _atomic_csv(), _atomic_figure(), _atomic_json(), _float(), _integer() (+9 more)

### Community 39 - "StrictModel"
Cohesion: 0.12
Nodes (6): AnalysisSettings, HypotheticalLossSettings, InputSettings, OutputSettings, PlotSettings, StrictModel

### Community 40 - "argparse"
Cohesion: 0.13
Nodes (23): main(), _artifact_paths(), evaluate_source(), _filtered_csv_rows(), _json_pointer(), _load_yaml(), main(), _number() (+15 more)

### Community 41 - "test_transportability.py"
Cohesion: 0.06
Nodes (29): aligned_records(), APCache, bootstrap(), build_froc_cache(), classify_change(), draw_observations(), FrocCache, operating_counts() (+21 more)

### Community 42 - "Medical Object Detector Benchmark"
Cohesion: 0.05
Nodes (41): 1. Create the pinned environment, 2. Acquire and prepare the dataset, 2a. Generate aggregate cohort characteristics, 3. Train and finalize the primary Faster R-CNN run, 4. Train and finalize the primary YOLO11s run, 5. Train the additional seeds and run the five-seed unified test evaluator, 5a. Reprocess the frozen bundles across confidence thresholds, 5b.1 Run the post-hoc five-validation-run selection sensitivity (+33 more)

### Community 43 - "raw_score_utility.py"
Cohesion: 0.11
Nodes (31): load_decision_curve_config(), AnalysisSettings, _artifact(), _atomic_csv(), _atomic_figure(), _atomic_json(), _audit_archives(), _display_name() (+23 more)

### Community 44 - "test_external_failure.py"
Cohesion: 0.17
Nodes (12): image_counts(), maximum_coverage(), paired_summary(), prediction(), target(), test_bootstrap_preserves_a_known_constant_paired_intervention(), test_intervention_preserves_frozen_original_evaluation_settings(), test_maximum_coverage_is_one_to_one_and_handles_assignment_competition() (+4 more)

### Community 45 - "README.md"
Cohesion: 0.12
Nodes (9): Proposed retained-candidate sensitivity v2 — NOT EXECUTED, Prerequisite evidence, YOLO numerical inference-path audit (Batch 53, v1), 1. Introduction, 5. Discussion, 6. Limitations, 7. Conclusion, 8. Declarations (+1 more)

### Community 46 - "paired.py"
Cohesion: 0.08
Nodes (30): aggregate_hybrid(), aggregate_prepared_hybrid(), _aggregate_single(), analyze_pair(), analyze_training_procedure(), _average_precision(), _coco_image_matches(), DetectionEvidence (+22 more)

### Community 47 - "visualize.py"
Cohesion: 0.14
Nodes (14): _balanced_sample(), build_parser(), _draw_centered_text(), _font(), _load_coco_records(), load_dataset_config(), main(), plot_annotation_samples() (+6 more)

### Community 48 - "math"
Cohesion: 0.15
Nodes (11): EarlyStopObservation, EarlyStopper, estimate_training_seconds(), test_early_stopper_records_initial_and_later_improvements(), test_early_stopper_rejects_nonfinite_metrics(), test_early_stopper_requires_improvement_strictly_above_min_delta(), test_early_stopper_stops_at_patience_boundary(), test_early_stopper_tie_is_not_an_improvement() (+3 more)

### Community 49 - "test_radiography_shifts.py"
Cohesion: 0.11
Nodes (21): scale_radiograph_to_uint8(), apply_radiography_shift(), _derived_seed(), dicom_linear_window(), _normalized_error_metrics(), RadiographyShift, RadiographyShiftSubsetDataset, test_constant_and_nonfinite_reference_contract() (+13 more)

### Community 50 - "batch52/paper_draft.md"
Cohesion: 0.06
Nodes (30): 1. Introduction, 2.1 Detector scores and operating-point assessment, 2.2 RSNA methodology and direct detector comparisons, 2.3 Implementation and reporting context, 2.4 External testing under a different annotation ontology, 2. Related Work, 3.1 Dataset, target, and patient-disjoint split, 3.2 Detector pipelines and controlled training factors (+22 more)

### Community 51 - "Any"
Cohesion: 0.16
Nodes (19): _artifact(), _atomic_csv(), _atomic_figure(), _atomic_json(), _candidate_floor_assessment(), _deserialize_predictions(), ExactFrocConfig, _inference_sensitivity_proposal() (+11 more)

### Community 52 - "StrictModel"
Cohesion: 0.11
Nodes (9): Hardware, Outputs, Versions, OutputSettings, RuntimeSettings, StrictModel, TimingReuseReview, TimingReuseReviews (+1 more)

### Community 53 - "build_scientific_artifact_manifest.py"
Cohesion: 0.21
Nodes (10): ArtifactSpec, build_manifest(), committed(), external(), _input_payload(), InputSpec, main(), _schema() (+2 more)

### Community 55 - "StrictModel"
Cohesion: 0.07
Nodes (11): CascadingParameterRandomizationSettings, ClaimBoundaries, HistoricalArtifacts, InputPixelRandomizationSettings, OutputSettings, PanelSettings, RuntimeSettings, SamplingSettings (+3 more)

### Community 56 - "test_threshold_repairability.py"
Cohesion: 0.24
Nodes (7): components(), evaluate(), test_invalid_or_infeasible_decompositions_fail(), test_missing_geometry_and_assignment_competition_are_distinct(), test_monotone_transform_preserves_entire_frontier_and_ties(), test_reranking_can_repair_budget_barrier_without_changing_geometry(), test_source_hash_mismatch_stops_before_output()

### Community 57 - "decision_curve.py"
Cohesion: 0.15
Nodes (13): CalibratedOutcomeProbabilities, DecisionThresholdProbability, RawDetectorConfidenceScores, RawDetectorConfidenceThreshold, _require_decision_threshold_probability(), standard_dca_actions(), standard_dca_net_benefit(), _validated_threshold_probability() (+5 more)

### Community 58 - "PROJECT_PLAN.md"
Cohesion: 0.07
Nodes (23): Artifacts and reproduction, Current interpretation, Exact-score method and endpoint behavior, Free-Response ROC Analysis, Historical-grid reproduction and fixed protocol, Historical grid versus approved lower-floor exact-score frontier, Residual candidate-floor boundary and conservative bound, Scientific value of another lower-floor run (+15 more)

### Community 59 - "json"
Cohesion: 0.06
Nodes (26): main(), sha256(), digest(), main(), add(), binding(), main(), binding() (+18 more)

### Community 60 - "batch46/paper_draft.md"
Cohesion: 0.07
Nodes (26): 1. Introduction, 2.1 Detector scores and operating-point assessment, 2.2 RSNA methodology and direct detector comparisons, 2.3 Implementation and reporting context, 2. Related Work, 3.1 Dataset, target, and patient-disjoint split, 3.2 Detector pipelines and controlled training factors, 3.3 Five retained runs and common evaluation (+18 more)

### Community 61 - "build_faster_rcnn"
Cohesion: 0.13
Nodes (11): ModelSettings, apply_training_mode(), build_faster_rcnn(), count_parameters(), enforce_backbone_trainability(), freeze_batch_norm_statistics(), FakeBody, FakeParameter (+3 more)

### Community 62 - "YoloRunTracker"
Cohesion: 0.13
Nodes (3): _atomic_json(), YoloRunTracker, test_tracker_ignores_ultralytics_final_eval_callback()

### Community 63 - "test_exact_score_froc.py"
Cohesion: 0.18
Nodes (19): audit_exact_score_monotonicity(), exact_score_froc_rows(), load_exact_froc_config(), select_exact_operating_points(), frozen_exact_inputs(), frozen_exact_rows(), lower_floor_exact_inputs(), lower_floor_exact_rows() (+11 more)

### Community 64 - "cohort_characteristics.py"
Cohesion: 0.18
Nodes (6): _aggregate_row(), _build_parser(), main(), MetadataSettings, _percent(), _safe_relative_name()

### Community 65 - "retained"
Cohesion: 0.29
Nodes (5): verify_arms(), retained(), evidence(), test_complete_evidence_replays_including_empty_predictions(), test_diagnostic_verifier_rejects_semantic_tampering()

### Community 66 - "Project plan: controlled lung-opacity detector comparison"
Cohesion: 0.08
Nodes (25): 10. Explainability plan as delivered, 11. Statistical analysis, 12. Implementation sequence and completion status, 13. Actual repository architecture, 14. Final report mapping, 15. Major risks and mitigations, 1. Aim and research questions, 2. Definition of success (+17 more)

### Community 67 - "collections_abc"
Cohesion: 0.14
Nodes (7): gradcam_for_score(), gradcam_from_tensors(), resolve_module(), restore_letterboxed_heatmap(), test_gradcam_uses_global_average_gradient_weights(), test_letterbox_restoration_removes_centered_padding(), test_module_resolution_supports_attributes_and_indices()

### Community 68 - "load_pareto_points"
Cohesion: 0.16
Nodes (14): _directed(), dominance_by_panel(), load_pareto_config(), load_pareto_points(), main(), ParetoPoint, strict_detector_dominance(), _validate_seed_grid() (+6 more)

### Community 69 - "report.md"
Cohesion: 0.08
Nodes (23): 10. Statistical Analysis, 11.1 Accuracy and operating-point behavior, 11.2 Robustness and explanation evidence, 11.3 Scenario-specific recommendation, 11.4 Limitations and scope of claims, 11. Discussion, 12. Conclusions and Future Work, 1. Introduction (+15 more)

### Community 71 - "pytest"
Cohesion: 0.30
Nodes (9): validate_contract(), test_clean_holm_fails_closed_if_an_endpoint_is_missing(), test_grid_holm_excludes_explicitly_non_estimable_hypotheses(), test_dtype_explicit(), test_forbidden_actions(), test_frozen_evaluator_constants(), test_historical_output_paths_refused(), test_no_run_can_be_excluded() (+1 more)

### Community 73 - "evaluate_vindr_external.py"
Cohesion: 0.06
Nodes (37): Path comparison, same_predictions(), Predictor, collect(), predict_arm(), WindowDataset, _serialize_prediction(), aggregate_metrics() (+29 more)

### Community 74 - "numpy"
Cohesion: 0.17
Nodes (8): BoxAttentionResult, evaluate_box_attention(), pixel_center_box_mask(), _validated_box(), _validated_heatmap(), test_box_mask_rejects_out_of_bounds_boxes(), test_energy_and_pointing_use_pixel_center_box_mask(), test_zero_energy_is_explicitly_invalid()

### Community 75 - "sha256_file"
Cohesion: 0.10
Nodes (41): _aggregate_boundaries(), _artifact(), build_parser(), main(), preflight(), _read_bundle(), _read_json(), _relative() (+33 more)

### Community 76 - "configure_reproducibility"
Cohesion: 0.21
Nodes (9): configure_reproducibility(), _optional_torch(), ReproducibilityReport, seed_worker(), sample_random_values(), test_cli_smoke_emits_strict_json(), test_invalid_seed_is_rejected(), test_reseeding_repeats_python_and_numpy_streams() (+1 more)

### Community 77 - "window_pixels"
Cohesion: 0.25
Nodes (7): window_pixels(), dicom(), test_incomplete_window_is_not_silently_ignored(), test_missing_window_reuses_exact_canonical_transform(), test_window_has_fixed_display_scale_and_correct_polarity(), test_window_rejects_semantics_outside_protocol(), test_window_width_one_is_a_threshold()

### Community 78 - "V7 Q2 / VinDr Baseline Audit"
Cohesion: 0.10
Nodes (20): 10. Verification record, 11. Review checkpoint, 1. Executive adjudication, 2. Repository baseline and prerequisite gate, 3. Manuscript and article comparison, 4. PDF rendering and provenance, 5. Checkpoint manifest audit, 6. Prediction-bundle inventory (+12 more)

### Community 79 - "test_check_bibliography.py"
Cohesion: 0.15
Nodes (10): citation_keys(), main(), parse_bibliography(), literal(), token(), verify(), test_duplicate_doi_rejected_even_with_different_keys(), test_literal_fields_and_metric_notation() (+2 more)

### Community 80 - "load_faster_rcnn_config"
Cohesion: 0.32
Nodes (16): load_faster_rcnn_config(), _config_payload(), test_batch_size_outside_hardware_scope_is_rejected(), test_coco_minimum_score_must_match_model_output_threshold(), test_loader_persistence_settings_require_booleans(), test_non_amp_runtime_is_rejected(), test_output_artifact_paths_reject_project_escape(), test_path_escape_is_rejected() (+8 more)

### Community 81 - "test_inference_timing.py"
Cohesion: 0.05
Nodes (32): Agreement, compare_predictions(), hardware_snapshot(), load_config(), main(), preflight(), render(), run_timing() (+24 more)

### Community 82 - "evaluate_coco"
Cohesion: 0.12
Nodes (16): _empty_results_dataset(), evaluate_coco(), _precision_curve(), _safe_average(), evaluate_model(), _records_for_image(), _remap_labels(), _scalar_image_id() (+8 more)

### Community 83 - "Grad-CAM Sensitivity Controls (v2)"
Cohesion: 0.12
Nodes (15): Explainability Analysis, Grad-CAM protocol, Qualitative selection and caveats, Quantitative results, Reproduction, Scope and provenance, Where are the models looking?, Cascading model-parameter randomization (+7 more)

### Community 85 - "Clinical annotation-adjudication protocol v1"
Cohesion: 0.22
Nodes (9): Blinding and reading sequence, Clinical annotation-adjudication protocol v1, Construct workshop and rubric, before study images, Instance relations and duplicate annotations, Outcomes and statistical plan, People, permissions and pre-read lock, Population and sampling, Purpose, hypotheses and decision boundary (+1 more)

### Community 86 - "explainability/config.py"
Cohesion: 0.13
Nodes (7): DetectorLayerSettings, GradCamSettings, MetricSettings, OutputSettings, QualitativeSettings, RuntimeSettings, StrictModel

### Community 87 - "load_robustness_config"
Cohesion: 0.13
Nodes (10): draw_stratified_subsample(), _largest_remainder_allocation(), load_robustness_config(), OutputSettings, RuntimeSettings, SamplingSettings, StrictModel, test_largest_remainder_allocation_is_exact_and_proportional() (+2 more)

### Community 88 - "Supervisor briefing: transportability evidence and publication decision"
Cohesion: 0.25
Nodes (8): Central contribution, Decisions for the supervisor, Direct answers to the professor's four requests, Label mapping and evaluation, in concrete terms, Publication barriers, Suggested reply in Persian, Supervisor briefing: transportability evidence and publication decision, What the evidence establishes

### Community 89 - "Supervisor-review preparation: execution and verification"
Cohesion: 0.25
Nodes (8): Actual scientific and software checks, Baseline and preservation, Boundaries of completion, Current location map for the reporting crosswalk, Delivered review documents, Final privacy and document checks, PDF build and exact-source checks, Supervisor-review preparation: execution and verification

### Community 90 - "StrictModel"
Cohesion: 0.11
Nodes (7): AnalysisSettings, DetectorSettings, InferenceSensitivityProposal, InputSettings, OutputSettings, PlotSettings, StrictModel

### Community 91 - "_parse_outputs"
Cohesion: 0.25
Nodes (4): OutputSettings, _parse_outputs(), _portable_path(), _run_name()

### Community 92 - "StrictModel"
Cohesion: 0.11
Nodes (6): AnalysisSettings, DetectorSettings, InputSettings, OutputSettings, PlotSettings, StrictModel

### Community 93 - "Research direction: limits of threshold repair under external shift"
Cohesion: 0.29
Nodes (7): A concrete feasibility result from existing evidence, Closest literature and the novelty boundary, Exact scope of the score-cutoff limit, Recommendation and question, Research direction: limits of threshold repair under external shift, Short pitch for the professor, Work completed here and what would strengthen the paper

### Community 94 - "faster_rcnn_reporting.py"
Cohesion: 0.06
Nodes (19): Historical boundary reconstruction and preservation, _atomic_write_text(), _normalize_flat_rows(), ParameterLike, _percentile(), _require_finite_non_negative_float(), summarize_inference_timings(), summarize_model_artifact() (+11 more)

### Community 95 - "analyze_exact_score_froc.py"
Cohesion: 0.12
Nodes (8): aggregate_exact_frontier(), audit_selected_points_against_canonical_matcher(), build_run_reachability(), compare_historical_and_exact(), compare_prior_and_current_exact(), compare_prior_and_current_runs(), _sample_std(), _selection_key()

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

### Community 100 - "2. Related Work"
Cohesion: 0.40
Nodes (5): 2.1 Detector scores and operating-point assessment, 2.2 RSNA methodology and direct detector comparisons, 2.3 Implementation and reporting context, 2.4 External testing under a different annotation ontology, 2. Related Work

### Community 101 - "Review Remediation Audit"
Cohesion: 0.12
Nodes (16): Adjudication summary, BibTeX citations used in repository Markdown, BLOCKING BEFORE SUBMISSION, Canonical repo-local hierarchy found in current documentation, CI and latest local verification, Citation-support audit, CLAIMS THAT SURVIVE UNCHANGED, Git state (+8 more)

### Community 102 - "csv"
Cohesion: 0.05
Nodes (23): build_parser(), _copy_checkpoint(), _driver_version(), _finalize(), _git_commit(), _load_result_rows(), sha256_file(), plot_yolo_training_curves() (+15 more)

### Community 103 - "test_cohort_characteristics.py"
Cohesion: 0.19
Nodes (11): _dicom_value_and_vr(), load_cohort_characteristics_config(), parse_patient_age(), resolve_dicom_root(), test_aggregate_row_contains_counts_percentages_and_no_identifier_fields(), test_config_freezes_the_immutable_5000_study_cohort(), test_environment_dicom_root_overrides_dataset_config(), test_missing_dicom_root_requests_the_named_environment_variable() (+3 more)

### Community 104 - "yolo_training.py"
Cohesion: 0.16
Nodes (4): build_ultralytics_train_args(), _floating_tensors_to_float32(), test_loss_prediction_cast_is_float32_and_preserves_gradient(), test_ultralytics_arguments_explicitly_disable_augmentation_and_match_batch()

### Community 106 - "Statistical analysis"
Cohesion: 0.12
Nodes (16): Checkpoint-conditional patient-cluster permutation and effect, Clean training-procedure results, Corruption-grid results, Endpoints, Inference protocol, Inferential targets, Interpretation limits, Pairing sensitivity and seed influence (+8 more)

### Community 107 - "YOLO numerical-path sensitivity: results v1"
Cohesion: 0.12
Nodes (16): Candidate agreement at retained support, Exact-score FROC, Exact-score FROC by checkpoint, Historical RSNA threshold, unchanged at 0.05, Historical RSNA threshold, unchanged at 0.05 by checkpoint, Historical shared 0.25 cutoff, Post-hoc n=5 RSNA threshold, unchanged at 0.01, Post-hoc n=5 RSNA threshold, unchanged at 0.01 by checkpoint (+8 more)

### Community 108 - "Medical Object Detector Benchmark v2.0.0 — Research Artifact Release"
Cohesion: 0.12
Nodes (15): Citation, Data availability, Documentation and infrastructure changes, Known limitations, License, Major changes since v1.0.0, Manuscript status, Medical Object Detector Benchmark v2.0.0 — Research Artifact Release (+7 more)

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
Cohesion: 0.17
Nodes (12): 4.10 Post-hoc failure decomposition and domain-change sensitivity, 4.11 Controlled retention and display diagnostic, 4.1 Clean internal-testing performance, 4.2 Shared thresholds and validation-selected operating points, 4.3 Internal exact-score false-positive regimes, 4.4 Training-procedure uncertainty and conditional tests, 4.5 Standardized inference timing, 4.6 External cohort and ranking performance (+4 more)

### Community 115 - "AgeSettings"
Cohesion: 0.09
Nodes (7): AgeSettings, CategoricalTagSettings, ExpectedCohort, ExpectedCounts, InputSettings, OutputSettings, StrictModel

### Community 116 - "Focused Internal Manuscript Audit"
Cohesion: 0.40
Nodes (5): Completion checks and review boundary, Editorial changes, Focused Internal Manuscript Audit, Literature and claim bindings, Prerequisite gate

### Community 119 - "Citation Verification Audit"
Cohesion: 0.50
Nodes (4): Citation Verification Audit, Current final manuscript — 2026-09-25, Historical audit retained verbatim (through 2026-09-07), Post-hoc extension — 2026-10-29

### Community 120 - "Literature Review"
Cohesion: 0.17
Nodes (12): Alternatives and planned fallback order, Common-corruption robustness, Comparability gap and contribution of the present study, Detector selection: Ultralytics YOLO11s, Explainability for object detection, Grad-CAM, Implications for the experimental design, Literature Review (+4 more)

### Community 121 - "Post-hoc external generalization results v1"
Cohesion: 0.25
Nodes (8): Candidate availability (assignment ignored), Candidate support, Cross-domain changes with shared checkpoint resampling, Interpretation boundary, Post-hoc external generalization results v1, Prevalence standardization, Reference-box error decomposition, Strict false positives and non-target findings

### Community 122 - "StrictModel"
Cohesion: 0.15
Nodes (6): DiagnosticSettings, InputSettings, MetadataContract, OutputSettings, RuntimeSettings, StrictModel

### Community 123 - "generate_cohort_characteristics"
Cohesion: 0.17
Nodes (8): _atomic_csv(), _atomic_json(), CohortCharacteristicsConfig, generate_cohort_characteristics(), _immutable_gate(), _read_manifest(), _resolved_dataset_config(), sha256_file()

### Community 125 - "Hypothesis Traceability"
Cohesion: 0.25
Nodes (8): H1 — Detection coverage and average precision, H2 — A shared threshold does not define a shared operating regime, H3 — Accuracy-compute Pareto trade-off, H4 — Corruption degradation is type- and severity-specific, H5 — Grad-CAM is a failure-analysis tool, not clinical-reasoning evidence, H6 — Detection confidence calibration, Hypothesis Traceability, Interpretation rule

### Community 128 - "AggregateAccumulator"
Cohesion: 0.25
Nodes (4): AgeObservation, AggregateAccumulator, ManifestColumns, _update_accumulator()

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
Cohesion: 0.15
Nodes (13): Annotation and preprocessing scope, Compute and sampling scope, Controlled diagnostic update (2026-11-05), Dataset, population, and target scope, Deployment and regulatory scope, Detector-comparison validity, Explainability scope, Frozen external testing and transportability (+5 more)

### Community 133 - "Supplementary Materials Index"
Cohesion: 0.14
Nodes (14): Reading guide for supervisor review (2026-11-06), S10. YOLO numerical inference-path sensitivity, S11. Post-hoc external generalization analysis, S12. Controlled external failure diagnostic, S1. Cohort, split, and provenance records, S2. Full clean seed-level comparison, S3. Operating-point and threshold evidence, S4. Calibration and exploratory raw-score utility (+6 more)

### Community 134 - "StrictModel"
Cohesion: 0.18
Nodes (4): AnalysisSettings, InputSettings, OutputSettings, StrictModel

### Community 135 - "load_phase5_config"
Cohesion: 0.19
Nodes (15): validate_protocol_contract(), aggregate_rows(), load_phase5_config(), _aggregation_row(), test_aggregation_rejects_invalid_missingness_contract(), test_aggregation_rejects_partially_defined_conditional_metrics(), test_aggregation_rejects_undefined_reason_that_disagrees_with_counts(), test_aggregation_retains_all_attempts_but_uses_defined_conditional_n() (+7 more)

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

### Community 143 - "3. Materials and Methods"
Cohesion: 0.17
Nodes (12): 3.10 Subsequent controlled implementation diagnostic, 3.1 Dataset, target, and patient-disjoint split, 3.2 Detector pipelines and controlled training factors, 3.3 Five retained runs and common evaluation, 3.4 Operating-point protocols and exact-score FROC, 3.5 Frozen VinDr external testing, 3.6 Estimands and uncertainty, 3.7 Standardized implementation timing (+4 more)

### Community 148 - "Detection-Confidence Calibration"
Cohesion: 0.22
Nodes (8): Definition and verified implementation, Descriptive finding, Detection-Confidence Calibration, Population and decision-analysis boundary, Predeclared descriptive sensitivity, Primary support and occupancy, Reliability-diagram scope, Versioned artifacts and reproduction

### Community 149 - "map_similarity_metrics"
Cohesion: 0.26
Nodes (6): map_similarity_metrics(), normalize_map_for_similarity(), pearson_map_correlation(), _pearson_values(), spearman_map_correlation(), ssim_map_similarity()

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
Cohesion: 0.18
Nodes (11): D-016 — Matched decoded-host timing v1 supersedes primary asymmetric timing, D-017 — Freeze VinDr-CXR external testing v1 before performance, D-018 — Retain complete frozen VinDr external inference and adverse results, D-020 — Integrate frozen external evidence and preserve the verification boundary, D-021 — Audit the final science and derive the author-review article, D-022 — Incorporate supplied author declarations and preserve the audited snapshot, D-023 — Retain numerical-path harmonisation as secondary sensitivity, D-024 — Post-hoc external generalization diagnostics (2026-10-29) (+3 more)

### Community 164 - "Final submission audit and author-declaration follow-up"
Cohesion: 0.20
Nodes (10): 2026-09-27 declaration wording and PDF refresh, 2026-10-29 post-hoc PDF refresh and visual review, 2026-11-06 supervisor-review preparation and current PDF, Final submission audit and author-declaration follow-up, Historical author-review record: 2026-09-25, PDF inspection at 2026-09-25, Remaining author/submission actions, Repository and author state at 2026-09-25 (+2 more)

### Community 166 - "Reporting Checklist Crosswalk"
Cohesion: 0.20
Nodes (10): Author-only release gates, Authoritative guideline sources, CLAIM 2024 primary crosswalk, Preserved earlier context, Publication readiness and CLAIM 2024 crosswalk, Required sample-size and subset-selection row, STARD-AI 2025 selected reporting crosswalk by analogy, Submission blockers and linked audits (+2 more)

### Community 167 - "Frozen VinDr-CXR inference results — Batch 49"
Cohesion: 0.25
Nodes (8): Achieved FP/image and candidate-floor limits, AP and prespecified FROC sensitivities, Equal-run AP summaries, Execution and numerical handoff audit, Frozen VinDr-CXR inference results — Batch 49, Historical n=3 RSNA threshold transport — PRIMARY, Post-hoc n=5 RSNA threshold transport — SECONDARY sensitivity, Score distributions at the four prespecified supports

### Community 174 - "Citation Audit"
Cohesion: 0.29
Nodes (7): Architecture, software, and evaluation methods, Bibliography entries not cited by the current manuscript, Calibration, XAI, statistics, DICOM, and decision analysis, Citation Audit, Corrections made during this audit, Dataset and domain-background sources, Reporting-standard sources used by the audit

### Community 175 - "Frozen VinDr statistics and cross-dataset transportability"
Cohesion: 0.29
Nodes (7): Artifacts and replay, Estimands and conditioning, Exact reconstruction and technical verification, Frozen VinDr statistics and cross-dataset transportability, Internal comparison and support limits, Observation units and joint resampling, Preserved rendering-order correction

### Community 176 - "Scientific interpretation of post-hoc external generalization v1"
Cohesion: 0.40
Nodes (5): Competing explanations remain unresolved, Contribution and relation to primary literature, Recommendation to the supervising professor, Scientific interpretation of post-hoc external generalization v1, What the retained evidence establishes

### Community 178 - "Dataset workspace"
Cohesion: 0.33
Nodes (5): Acquire and prepare, Credentials and competition access, Dataset workspace, Locally inspected source files, Selected source

### Community 180 - "COMPUTE_TIMING.md"
Cohesion: 0.06
Nodes (32): Accepted laptop measurements, Claim limits and artifact provenance, Matched boundary and configuration, Parameter counts and incomplete operation profiles, Prediction agreement and timing statistics, Reporting hardware and reproducibility, Standardized inference timing v1, Artifacts (+24 more)

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1969 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `prepare()` connect `run_vindr_statistics.py` to `VinDr-CXR adapter preflight — Batch 48`, `threshold_calibration.py`, `evaluate_vindr_external.py`, `Medical Object Detector Benchmark`, `evaluate_vindr_external.py`, `window_pixels`, `test_radiography_shifts.py`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `ImagePrediction` (e.g. with `One prediction-to-metric path` and `exact_score_froc_rows()`) actually correct?**
  _`ImagePrediction` has 37 INFERRED edges - model-reasoned connections that need verification._
- **What connects `meddet-benchmark` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `prepare.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05277262420119563 - nodes in this community are weakly interconnected._
- **Why does `VinDr-CXR adapter preflight — Batch 48` connect `VinDr-CXR adapter preflight — Batch 48` to `run_vindr_statistics.py`, `README.md`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Should `analyze_yolo_numerical_path.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06572769953051644 - nodes in this community are weakly interconnected._
- **Why does `Decision log` connect `Decision log` to `D-002 — Descope Track B and reframe the research contribution`, `D-004 — Keep later validation-threshold sensitivity separate from the primary thresholds`, `D-005 — Separate inferential targets and resample detector runs independently`, `D-006 — Treat beta as an F-beta preference parameter and separate linear loss`, `D-007 — Remove raw detector-score curves from conventional DCA interpretation`, `D-008 — Use n=5 as the principal operating-regime sensitivity display`, `D-009 — Use one version for software and research-artifact releases`, `README.md`, `D-010 — Keep `paper_draft.md` as the canonical editable journal manuscript`, `D-011 — Use the observed exact-score frontier and retain the candidate-floor boundary`, `D-012 — Adopt the approved 0.0001 FROC sensitivity and retain the residual boundary`, `D-013 — Adopt the approved 0.00001 FROC sensitivity and stop at the residual bound`, `D-014 — Retain n=3 threshold provenance and report n=5 selection only as post-hoc sensitivity`, `D-003 — Decline to revive a Track-B-style native/best-practice comparison`, `D-001 — Two-track detector comparison design`, `D-015 — Report aggregate DICOM-header cohort characteristics with an age-unit caveat`, `D-019 — Separate observed ranking transport from frozen operating-point transport`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._