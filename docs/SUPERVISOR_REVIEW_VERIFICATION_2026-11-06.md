# Supervisor-review preparation: execution and verification

6 November 2026. **Completed editorial/review preparation and existing-evidence
verification. Expert adjudication and new inference were not executed.**

## Baseline and preservation

Repository `medical-object-detector-benchmark`, branch `main`, commit
`0b5e1dd4b7ff1cd94072ebc981d18c3cea2d9c2b`; initial working tree clean and aligned
with its configured upstream. This task authorizes local preparation only.
No training, GPU inference, threshold selection, ontology merge, commit, push
or release designation occurred. The CUDA environment was used solely for the
existing saved-inference verifier, not prediction collection.

The original claim bindings, scientific/publication inventories and original,
generalization and controlled-diagnostic summaries are byte-identical to HEAD.
No manifest hash was refreshed to conceal changed inputs. All five runs per
detector remain represented. New prose is supported by existing evidence;
the 478-value trace was regenerated only to update manuscript locations.

## Delivered review documents

- [Supervisor briefing](SUPERVISOR_BRIEFING_2026-11-06.md): contribution,
  verified versus exploratory evidence, scientific decisions and author gates.
- [Scientific review](SUPERVISOR_SCIENTIFIC_REVIEW_2026-11-06.md): corrected
  scope ambiguities, remaining limits, supplementary reading plan and a NO-GO
  recommendation for full-cohort expanded inference for the current paper.
- [Adjudication protocol v1](CLINICAL_ANNOTATION_ADJUDICATION_V1.md): future
  blinded expert reads, fixed selection and endpoints, instance ambiguity,
  missingness/agreement and private-data controls. No reader recruitment,
  approval, sampling or clinical judgment is represented as completed.
- [Updated CLAIM 2024 crosswalk](REPORTING_CHECKLIST.md): all 44 items with
  Yes/No/NA and evidence; separate author-only ethics, compliance, authorship,
  journal, model-access and final-release decisions.

## Actual scientific and software checks

Commands ran from the repository root with `VINDR_CXR_ROOT` set to the existing
authorized `data/raw/vindr-cxr` directory. The following table gives exact
arguments after `.venv/Scripts/python.exe`, except the explicitly identified
CUDA-environment verifier. The subprocess execution record, outputs and elapsed
times are retained locally in `tmp/supervisor-review-20261106/verification.json`.

| Executed arguments | Result |
|---|---|
| `-m scripts.verify_frozen_external --mode freeze` | PASS: 38 frozen files |
| `-m scripts.verify_scientific_artifacts` | PASS: 72 artifacts, 346 present inputs, zero unavailable |
| `-m scripts.verify_scientific_artifacts --manifest results/publication_artifact_manifest.json` | PASS: 112 artifacts, 996 present inputs, zero unavailable |
| `-m scripts.verify_frozen_external --mode inference` using `C:\Users\Pouyan\.conda\envs\torch-gpu\python.exe` | PASS: saved source/checkpoint/prediction/metric checks for ten runs, 3,000 images each; no inference |
| `-m scripts.verify_frozen_external --mode statistics` | PASS: 130 bindings and 44 saved-draw interval rows |
| `-m scripts.verify_frozen_external --mode replay` | PASS: fresh full deterministic original-statistics bootstrap replay, including both 2,000-draw cohort analyses |
| `-m src.stats.run_external_generalization --config configs/external_generalization_v1.yaml --mode verify` | PASS: 138 inputs, 15 tables |
| `-m src.stats.run_external_generalization --config configs/external_generalization_v1.yaml --mode replay` | PASS: fresh full 2,000-draw joint replay and exact table/point equality |
| `-m scripts.verify_external_failure --config configs/external_failure_isolation_v1.yaml` | PASS: 1,680 baseline and 5,040 nested-retention comparisons; 504 pixel hashes |
| `-m src.analyze_external_failure --config configs/external_failure_isolation_v1.yaml --replay` | PASS: three tables, 2,000 paired draws per detector |
| `-m pytest -q --basetemp=tmp/pytest-supervisor-portable-20261106 -p no:cacheprovider` | PASS: 510 passed, one expected skip, seven scientific tests deselected |
| `-m pytest -q --run-scientific --basetemp=tmp/pytest-supervisor-scientific-20261106 -p no:cacheprovider` | PASS: 517 passed, one expected skip |
| `-m ruff check src tests scripts` | PASS |
| `-m ruff format --check src tests scripts` | PASS: 148 files |
| `-m scripts.verify_paper_claims` | PASS: 478 claims and all 42 existing semantic guards |
| `-m scripts.check_bibliography --bibliography report/references.bib --manuscripts report/paper_draft.md report/report.md report/Manuscript_FasterRCNN_vs_YOLO11s_LungOpacity.md` | PASS: 45 entries, 24/19/27 cited keys resolve |
| `-m scripts.export_paper_trace --manifest report/paper_claim_sources.yaml --output docs/SUBMISSION_NUMERICAL_TRACE.csv` | PASS: 478 verified current-location rows |

The skip applies only to a metadata-only environment; authorized data are
present here. Portable tests are distinguished from the separately executed
licensed-data verification. The frozen wrapper resolves the two archived
editorial baseline files without overwriting the living manuscript or weakening
scientific hash checks. These results establish implementation/provenance
consistency, not reference-standard validity or clinical correctness.

## PDF build and exact-source checks

Used the existing separate document environment and unchanged builder/filter/
header. Updated only build work directory and the supporting evidence pin to
`0b5e1dd4b7ff1cd94072ebc981d18c3cea2d9c2b`, which contains S12. This is the
already committed evidence revision, not the unpublished review's final release.

```powershell
rtk .\.tools\paper-build\Scripts\python.exe -m scripts.build_paper_pdf --config configs/paper_build.yaml
rtk .\.tools\paper-build\Scripts\python.exe -m scripts.check_paper_pdf --pdf output/pdf/rsna_vindr_article.pdf --output report/paper_pdf_qa.json --text tmp/pdfs/supervisor-review-20261106/final/extracted-final.txt
rtk pdftoppm -r 120 -png output/pdf/rsna_vindr_article.pdf tmp/pdfs/supervisor-review-20261106/final/page
```

All commands passed. The configured three pdfLaTeX passes completed; the final
log contains no overfull/underfull, missing-character, undefined-reference or
rerun warnings. An `rg` search returned exit 1 because there were no matches,
not because the build failed. Automated QA reports **19 pages, zero errors**.
All 11 build inputs and the output hash were independently checked against the
build receipt. All 34 internal PDF links have valid destinations; 11 pinned
repository URIs resolve to existing paths at the pinned Git revision. This is
not an assertion that every external publisher URL was tested over HTTP.

- Manuscript SHA-256: `c7c83a98cfd48674e726f93d3fcfc9e4e4a787eca5dc5400287b56f8f53455bd`.
- PDF SHA-256: `06d3d38b36f2eaa9a04920ab28e39ad5a4ba7136d2dcfb3224172cd830a22215`.
- Build receipt: [paper_build_manifest.json](../report/paper_build_manifest.json).
- Automated QA: [paper_pdf_qa.json](../report/paper_pdf_qa.json).
- Final derivative: [rsna_vindr_article.pdf](../output/pdf/rsna_vindr_article.pdf).

Visually inspected **every page individually** from the 120-dpi PNG rendering.
No clipping, overlap, missing glyphs, obscured labels or broken captions were
observed. Table 1 continues on page 4 with a repeated header; reference entries
remain intact. All ten numerical values in Section 4.11 and all 27 Table 8
values were checked against extracted PDF text. This targeted PDF check is
separate from all 478 source-manuscript bindings.

| Pages | Visual/content review |
|---|---|
| 1-4 | Title/authors, updated abstract/access statement, rationale, related work and Table 1 |
| 5-7 | Frozen-experiment scope, uncertainty distinctions, Methods 3.9 and 3.10, S11/S12 pointers |
| 8-11 | Internal tables and PR/F1/FROC/timing figures; Table 3 conditioning clarification |
| 12-14 | External Tables 5-7, frozen floor/cap caveat, numerical-path results and Table 8 |
| 15-17 | Results 4.11, bounded Discussion/Limitations, conclusion and unresolved declarations |
| 18-19 | Complete references, readable URLs and page transitions |

## Current location map for the reporting crosswalk

Source lines refer to this exact Markdown hash, not numbered PDF lines. This
map supplies page and source-line locations for the section references in all
44 checklist rows; authors must transfer them to the journal's final form.

| Section | Source starting line | PDF pages |
|---|---:|---|
| Abstract | 20 | 1 |
| 1 Introduction | 65 | 1-2 |
| 2.1 / 2.2 Related work | 109 / 122 | 2 |
| 2.3 / 2.4 Reporting/external context | 145 / 161 | 3 |
| 3.1 Cohort/Table 1 | 187 | 3-4 |
| 3.2 / 3.3 Training/evaluation | 241 / 261 | 4 |
| 3.4 Threshold/FROC methods | 282 | 4-5 |
| 3.5 Frozen external methods | 311 | 5 |
| 3.6 Uncertainty | 366 | 5-6 |
| 3.7 Timing | 411 | 6 |
| 3.8 Secondary methods | 441 | 6-7 |
| 3.9 / 3.10 Post-hoc/controlled methods | 465 / 504 | 7 |
| 4.1 / 4.2 Internal results | 526 / 565 | 7-9 |
| 4.3 / 4.4 Internal FROC/uncertainty | 594 / 612 | 9-11 |
| 4.5 Timing results | 646 | 11 |
| 4.6 / 4.7 External ranking/operating points | 677 / 701 | 12-13 |
| 4.8 External FROC | 749 | 13-14 |
| 4.9 / 4.10 Numerical path/post-hoc results | 795 / 813 | 14 |
| 4.11 Controlled diagnostic | 856 | 15 |
| 5 / 6 Discussion/Limitations | 871 / 943 | 15-16 |
| 7 / 8 Conclusion/declarations | 1020 / 1034 | 17 |

## Boundaries of completion

The expert protocol, supervisor recommendation and checklist are completed
documents, not executed expert evidence or author approvals. Full-cohort
expanded-candidate inference remains a deferred proposal. Missing clinical/
acquisition information, unknown external patient dependence, cohort-flow
presentation and author/journal/release decisions remain explicitly identified.
No new CI run on GitHub or cross-platform release export is claimed for this
uncommitted local review. Existing private data were used only for authorized
verification and remain private.


## Final privacy and document checks

The targeted local scan checked all 14 changed/untracked public text files
and extracted final PDF text against all 3,000 restricted external image
identifiers: zero matches. No files under the restricted raw/processed VinDr
roots are tracked. Local context files and execution logs remain ignored.
All relative links in the new review documents and current checklist resolve;
all 44 checklist item numbers occur exactly once in order. No source, test,
script or scientific-results files changed. `rtk git diff --check` passed.
These checks do not certify legal compliance or detect every possible privacy
issue. No graph rebuild was required because no analysis/build code changed.

The unexecuted expert-protocol draft reviewed here has SHA-256
`63a538e00b94b0af56d20ff3f7e7f4f7469367d6615c1023bdeb3ba11ec0400e`. This identifies the document supplied for expert review;
it is not the signed pre-read protocol lock or evidence of expert approval.
