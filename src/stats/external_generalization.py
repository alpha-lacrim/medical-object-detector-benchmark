"""Post-hoc diagnostics of frozen predictions; no clinical relabeling or inference."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import replace
from typing import Any

import numpy as np

from src.meddet_benchmark.evaluation import ImageTarget, box_iou, match_image
from src.stats.paired import draw_independent_run_bootstrap_multiplicities, stable_rng_seed
from src.stats.transportability import aligned_records, draw_observations

TARGET_CATEGORIES = (
    "matched",
    "high_score_assignment",
    "below_threshold",
    "partial_localization",
    "no_relevant_retained",
)
FP_CATEGORIES = (
    "claimed_strict_target",
    "other_local_finding",
    "ambiguous_partial",
    "no_local_overlap",
)


def local_annotations(
    rows: list[dict], targets: list[ImageTarget], protocol: dict, analysis: dict
) -> tuple:
    """Validate source local boxes and exactly reconcile strict source/canonical geometry."""
    sizes = {t.image_id: t.image_size for t in targets}
    strict = protocol["ontology"]["source_exact_class_name"]
    category = next(k for k, v in protocol["ontology"]["canonical_classes"].items() if v == strict)
    columns = protocol["dataset"]["annotation_columns"][2:]
    no_finding = set()
    by_image: dict = defaultdict(lambda: defaultdict(list))
    seen = set()
    cross_class: dict = defaultdict(set)
    for row in rows:
        key = row[protocol["dataset"]["image_id_column"]] + analysis["canonical_image_suffix"]
        label = row[protocol["dataset"]["class_name_column"]]
        if key not in sizes or not label:
            raise ValueError("Unknown source annotation image or empty class")
        if label == analysis["no_finding_label"]:
            if key in no_finding or any(row[k] and not np.isnan(float(row[k])) for k in columns):
                raise ValueError("Invalid or duplicate no-finding sentinel")
            no_finding.add(key)
            continue
        if label in analysis["global_labels_excluded"]:
            raise ValueError("Global diagnosis cannot supply a localization box")
        box = tuple(float(row[k]) for k in columns)
        # ImageTarget is the shared finite, area and native-bounds validator.
        ImageTarget(key, sizes[key], [box], [category])
        if (key, label, box) in seen:
            raise ValueError("Duplicate same-class source annotation; review required")
        seen.add((key, label, box))
        cross_class[key, box].add(label)
        by_image[key][label].append(box)
    if no_finding & set(by_image):
        raise ValueError("No-finding sentinel conflicts with a localized annotation")
    for target in targets:
        actual = sorted(by_image[target.image_id].get(strict, []))
        expected = sorted(map(tuple, target.boxes_xyxy))
        if actual != expected:
            raise ValueError("Strict source/canonical annotation disagreement")
    counts = Counter(label for _, label, _ in seen)
    return by_image, {
        "local_box_counts": dict(sorted(counts.items())),
        "cross_class_coincident_geometries": sum(len(v) > 1 for v in cross_class.values()),
        "same_class_duplicates": 0,
        "invalid_boxes": 0,
        "strict_geometry_reconciled": True,
        "no_finding_sentinel_images": len(no_finding),
    }


def distribution(values: list | np.ndarray) -> dict:
    """Nonidentifying linear quartiles; missing populations stay explicitly undefined."""
    a = np.asarray(values, dtype=float)
    names = ("minimum", "q25", "median", "q75", "maximum")
    quantiles = np.quantile(a, [0, 0.25, 0.5, 0.75, 1]) if len(a) else [None] * 5
    return {"count": len(a), **dict(zip(names, quantiles, strict=True))}


def error_decomposition(
    predictions: list,
    targets: list,
    annotations: dict,
    *,
    threshold: float,
    evaluation: dict,
    analysis: dict,
    strict_label: str,
) -> dict[str, list[dict]]:
    """Assign exclusive reference/FP categories using the unchanged canonical matcher."""
    ps, ts = aligned_records(predictions, targets)
    floor, cap = evaluation["candidate_score_floor"], evaluation["max_detections_per_image"]
    required, partial = evaluation["matching_iou_threshold"], analysis["partial_iou"]
    overlap = analysis["overlap_iou"]
    categories = Counter(dict.fromkeys(TARGET_CATEGORIES, 0))
    fp_counts = {s: Counter(dict.fromkeys(FP_CATEGORIES, 0)) for s in ("historical", "retained")}
    overlaps = {s: Counter() for s in fp_counts}
    totals = {s: Counter() for s in fp_counts}
    available = Counter({str(v): 0 for v in analysis["iou_grid"]})
    best_values, matchable_scores, unmatchable_scores = [], [], []
    classes = sorted({c for image in annotations.values() for c in image if c != strict_label})
    for p, t in zip(ps, ts, strict=True):
        if len(p.scores) > cap or np.any(p.scores < floor):
            raise ValueError("Prediction support differs from the frozen cap/floor")
        if not set(p.labels).issubset(evaluation["class_ids"]) or not set(t.labels).issubset(
            evaluation["class_ids"]
        ):
            raise ValueError("Unexpected foreground label")
        ious = box_iou(p.boxes_xyxy, t.boxes_xyxy)
        best = ious.max(axis=0) if len(p.scores) else np.zeros(len(t.labels))
        best_values.extend(best)
        compatible = (
            ious.max(axis=1) >= required if len(t.labels) else np.zeros(len(p.scores), bool)
        )
        matchable_scores.extend(p.scores[compatible])
        unmatchable_scores.extend(p.scores[~compatible])
        for v in analysis["iou_grid"]:
            available[str(v)] += int(np.count_nonzero(best >= v))
        historical = match_image(
            p, t, score_threshold=threshold, iou_threshold=required, max_detections=cap
        )
        hits = {m.target_index for m in historical.matches}
        for j, value in enumerate(best):
            if j in hits:
                category = "matched"
            elif np.any((ious[:, j] >= required) & (p.scores >= threshold)):
                category = "high_score_assignment"
            elif value >= required:
                category = "below_threshold"
            elif value >= partial:
                category = "partial_localization"
            else:
                category = "no_relevant_retained"
            categories[category] += 1
        others = annotations.get(t.image_id, {})
        other_iou = {
            name: box_iou(p.boxes_xyxy, boxes).max(axis=1)
            for name, boxes in others.items()
            if name != strict_label and len(boxes)
        }
        other_max = (
            np.maximum.reduce(list(other_iou.values())) if other_iou else np.zeros(len(p.scores))
        )
        strict_max = ious.max(axis=1) if len(t.labels) else np.zeros(len(p.scores))
        for support, cutoff in (("historical", threshold), ("retained", floor)):
            result = (
                historical
                if support == "historical"
                else match_image(
                    p, t, score_threshold=cutoff, iou_threshold=required, max_detections=cap
                )
            )
            claimed = [m.target_index for m in result.matches]
            totals[support].update(
                {
                    "tp": len(result.matches),
                    "fp": len(result.unmatched_prediction_indices),
                    "detections": len(result.prediction_indices),
                    "emitting_images": int(bool(result.prediction_indices)),
                }
            )
            for i in result.unmatched_prediction_indices:
                if claimed and np.any(ious[i, claimed] >= overlap):
                    category = "claimed_strict_target"
                elif other_max[i] >= overlap:
                    category = "other_local_finding"
                elif max(strict_max[i], other_max[i]) >= partial:
                    category = "ambiguous_partial"
                else:
                    category = "no_local_overlap"
                fp_counts[support][category] += 1
                for name, values in other_iou.items():
                    overlaps[support][name] += int(values[i] >= overlap)
    n = sum(len(t.labels) for t in ts)
    if sum(categories.values()) != n:
        raise AssertionError("Reference error categories do not reconcile")
    fp_rows, overlap_rows, operating = [], [], []
    for support in fp_counts:
        total = totals[support]
        if sum(fp_counts[support].values()) != total["fp"]:
            raise AssertionError("False-positive categories do not reconcile")
        fp_rows.extend(
            {
                "support": support,
                "category": k,
                "count": v,
                "denominator": total["fp"],
                "fraction": v / total["fp"] if total["fp"] else None,
            }
            for k, v in fp_counts[support].items()
        )
        overlap_rows.extend(
            {
                "support": support,
                "class_name": k,
                "count": overlaps[support][k],
                "denominator": total["fp"],
                "fraction": overlaps[support][k] / total["fp"] if total["fp"] else None,
            }
            for k in classes
        )
        operating.append(
            {
                "support": support,
                **total,
                "images": len(ts),
                "target_boxes": n,
                "sensitivity": total["tp"] / n if n else None,
                "fp_per_image": total["fp"] / len(ts),
            }
        )
    return {
        "reference_errors": [
            {"category": k, "count": v, "denominator": n, "fraction": v / n if n else None}
            for k, v in categories.items()
        ],
        "false_positives": fp_rows,
        "non_target_overlaps": overlap_rows,
        "availability": [
            {"iou": float(k), "count": v, "denominator": n, "fraction": v / n if n else None}
            for k, v in available.items()
        ],
        "distributions": [
            {"population": k, **distribution(v)}
            for k, v in (
                ("best_target_iou", best_values),
                ("matchable_candidate_score", matchable_scores),
                ("unmatchable_candidate_score", unmatchable_scores),
            )
        ],
        "operating": operating,
    }


def ap_events(cache: Any) -> tuple[np.ndarray, np.ndarray]:
    """Expand only original detection events from official COCO matches, never sampled copies."""
    owners = np.repeat(cache.group_images, cache.group_lengths)
    matches = np.zeros(len(owners), bool)
    groups, counts, offsets = cache.positives[0]
    starts = np.cumsum(cache.group_lengths) - cache.group_lengths
    matches[starts[np.repeat(groups, counts)] + offsets] = True
    return owners, matches


def weighted_ap(
    events: tuple[np.ndarray, np.ndarray],
    target_counts: np.ndarray,
    weights: np.ndarray,
    recall_points: int,
) -> float:
    """Custom weighted 101-position AP; unit weights recover official cached AP50."""
    if (
        weights.shape != target_counts.shape
        or np.any(weights < 0)
        or not np.isfinite(weights).all()
    ):
        raise ValueError("Invalid observation weights")
    target_mass = weights @ target_counts
    if target_mass <= 0:
        return float("nan")
    owners, matches = events
    masses = weights[owners]
    keep = masses > 0
    masses, matches = masses[keep], matches[keep]
    if not len(masses):
        return 0.0
    tp = np.cumsum(masses * matches)
    precision = tp / np.cumsum(masses)
    envelope = np.maximum.accumulate(precision[::-1])[::-1]
    idx = np.searchsorted(tp / target_mass, np.linspace(0, 1, recall_points), side="left")
    values = np.zeros(recall_points)
    valid = idx < len(envelope)
    values[valid] = envelope[idx[valid]]
    return float(values.mean())


def prevalence_weights(counts: np.ndarray, observations: np.ndarray, q: float) -> np.ndarray:
    """Standardize image-positive frequency, retaining patient multiplicities."""
    if not 0 < q < 1 or observations.shape != counts.shape or np.any(observations < 0):
        raise ValueError("Invalid prevalence or observation weights")
    if not observations.sum():
        return np.full(len(counts), np.nan)
    positive = counts > 0
    p = observations[positive].sum() / observations.sum()
    if p in (0, 1):
        return np.full(len(counts), np.nan)
    return observations * np.where(positive, q / p, (1 - q) / (1 - p))


def prevalence_metrics(
    run: Any, events: tuple, weights: np.ndarray, recall_points: int
) -> np.ndarray:
    """Weighted AP and frozen-threshold precision; undefined strata propagate."""
    if not np.isfinite(weights).all():
        return np.full(2, np.nan)
    tp, fp = weights @ run.primary_counts
    precision = tp / (tp + fp) if tp + fp else 0.0
    return np.array([weighted_ap(events, run.ap.target_counts, weights, recall_points), precision])


def validate_domains(internal: tuple, external: tuple, clusters: Any) -> None:
    """Require exact within-detector checkpoint/run pairing and consistent observation order."""
    if len(internal) != 2 or len(external) != 2:
        raise ValueError("Exactly two detector families required")
    for a, b in zip(internal, external, strict=True):
        if (
            not a
            or [r.seed for r in a] != [r.seed for r in b]
            or len({r.seed for r in a}) != len(a)
        ):
            raise ValueError("Run identity/order differs across domains")
    for domain in (internal, external):
        ref = domain[0][0].ap
        for family in domain:
            for run in family:
                if (
                    run.ap.image_ids != ref.image_ids
                    or run.froc.image_ids != ref.image_ids
                    or not np.array_equal(run.ap.target_counts, ref.target_counts)
                ):
                    raise ValueError("Inconsistent observations or targets within domain")
    if clusters.image_ids != internal[0][0].ap.image_ids:
        raise ValueError("Internal cluster order differs")


def joint_bootstrap(
    internal: tuple,
    external: tuple,
    clusters: Any,
    analysis: dict,
    label: str,
    tolerance: float,
) -> tuple[dict, dict]:
    """Independent cohorts/families; identical checkpoint multiplicities across domains."""
    validate_domains(internal, external, clusters)
    domains = (internal, external)
    q = float(np.mean(external[0][0].ap.target_counts > 0))
    events = [[ap_events(r.ap) for r in runs] for runs in internal]
    # Reuse exact AP logic but evaluate only the declared IoU-0.50 endpoint.
    aps = [
        [[replace(r.ap, positives=r.ap.positives[:1]) for r in runs] for runs in domain]
        for domain in domains
    ]
    count = analysis["bootstrap_resamples"]
    changes = np.full((count, 2, 3), np.nan)
    prevalence = np.full((count, 2, 2, 2), np.nan)
    limited = np.zeros((count, 2, 2), dtype=int)
    rng = np.random.default_rng(stable_rng_seed(analysis["bootstrap_seed"], label))

    def evaluate(observations: list, run_weights: tuple) -> tuple:
        values = np.full((2, 2, 3), np.nan)
        prev = np.full((2, 2, 2), np.nan)
        support = np.zeros((2, 2), dtype=int)
        for domain_index, domain in enumerate(domains):
            w = observations[domain_index]
            for detector, runs in enumerate(domain):
                metrics = []
                for j, run in enumerate(runs):
                    ap = aps[domain_index][detector][j].evaluate(w)[0]
                    sens, flag = run.froc.budgets(w, [analysis["change_froc_budget"]], tolerance)
                    targets = w @ run.ap.target_counts
                    recall = (w @ run.primary_counts)[0] / targets if targets else np.nan
                    metrics.append([ap, sens[0], recall])
                    support[domain_index, detector] += int(flag[0]) * run_weights[detector][j]
                selected = run_weights[detector] > 0
                values[domain_index, detector] = np.average(
                    np.asarray(metrics)[selected], axis=0, weights=run_weights[detector][selected]
                )
                if domain_index == 0:
                    standardized = prevalence_weights(runs[0].ap.target_counts, w, q)
                    for mode, weights in enumerate((w, standardized)):
                        ms = np.asarray(
                            [
                                prevalence_metrics(
                                    r, e, weights, analysis["prevalence_recall_points"]
                                )
                                for r, e in zip(runs, events[detector], strict=True)
                            ]
                        )
                        prev[mode, detector] = np.average(
                            ms[selected], axis=0, weights=run_weights[detector][selected]
                        )
        return values[1] - values[0], prev, support, values

    ones = [np.ones(len(d[0][0].ap.image_ids), dtype=int) for d in domains]
    run_ones = tuple(np.ones(len(runs), dtype=int) for runs in internal)
    point, prev_point, support_point, domain_points = evaluate(ones, run_ones)
    for i in range(count):
        observations = [
            draw_observations(rng, len(ones[0]), clusters),
            draw_observations(rng, len(ones[1]), None),
        ]
        run_weights = draw_independent_run_bootstrap_multiplicities(
            rng, detector_a_run_count=len(internal[0]), detector_b_run_count=len(internal[1])
        )
        changes[i], prevalence[i], limited[i], _ = evaluate(observations, run_weights)
        if analysis["progress_every"] and (i + 1) % analysis["progress_every"] == 0:
            print(f"Joint change/prevalence bootstrap {i + 1}/{count}", flush=True)
    return {"changes": changes, "prevalence": prevalence, "floor_limited_selected_runs": limited}, {
        "change": point.tolist(),
        "prevalence": prev_point.tolist(),
        "domain_points": domain_points.tolist(),
        "observed_floor_limited_runs": support_point.tolist(),
        "target_positive_frequency": q,
        "rng_seed": stable_rng_seed(analysis["bootstrap_seed"], label),
    }
