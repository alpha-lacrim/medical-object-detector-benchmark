"""Render the shared-annotation audit from verified public aggregate tables."""

from __future__ import annotations

import argparse
import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.stats.run_vindr_statistics import (
    artifact,
    read_json,
    read_yaml,
    require,
    verify_artifact,
    write_json,
)


def build(config_path: Path, *, replay: bool = False) -> dict:
    """Render deterministic figures and text; never overwrite a published output."""
    config = read_yaml(config_path)
    settings = read_yaml(config["analysis_config"])["analysis"]
    summary = read_json(config["analysis_summary"])
    root = Path(config["output_root"])
    for entry in summary["artifacts"]:
        if Path(entry["path"]).suffix == ".csv":
            verify_artifact(entry)
    sources = [
        artifact(p)
        for p in (config_path, __file__, config["analysis_config"], config["analysis_summary"])
    ]
    baseline = (
        pd.read_csv(root / "per_run.csv").groupby(["dataset", "detector", "budget"]).recall.mean()
    )
    envelope = pd.read_csv(root / "envelopes.csv")
    exact = pd.read_csv(root / "exact_deletions.csv")
    contrasts = pd.read_csv(root / "contrasts.csv")
    budget = settings["primary_budget"]
    detectors = summary["detectors"]
    labels = {detectors[0]: "Faster R-CNN", detectors[1]: "YOLO11s"}
    colors = config["colors"]
    plt.rcParams.update({"font.size": config["font_size"], "font.family": "DejaVu Sans"})
    outputs = {}

    def save(figure, name):
        buffer = io.BytesIO()
        figure.savefig(
            buffer,
            format="png",
            dpi=config["dpi"],
            bbox_inches="tight",
            metadata={"Software": "froc-annotation-v1"},
        )
        outputs[root / config["figures"][name]] = buffer.getvalue()
        plt.close(figure)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
    radii = {}
    for ax, detector, color in zip(axes, detectors, colors, strict=True):
        data = envelope[
            (envelope.dataset == "external")
            & (envelope.entity == detector)
            & (envelope["mode"] == "mixed")
            & (envelope.budget == budget)
        ].sort_values("edits")
        gap = baseline.loc["internal", detector, budget] - data.upper
        interval = contrasts[
            (contrasts.detector == detector)
            & (contrasts.budget == budget)
            & (contrasts.endpoint == "lower")
        ].sort_values("external_edits")
        radii[detector] = int(data.loc[gap > 0, "edits"].max())
        ax.plot(data.edits, gap * 100, color=color, lw=2, label="Conditional gap lower bound")
        ax.fill_between(
            interval.external_edits,
            interval.lower * 100,
            interval.upper * 100,
            color=color,
            alpha=0.15,
            label="Marginal 95% bootstrap interval",
        )
        ax.scatter(interval.external_edits, interval.point * 100, color=color, s=17)
        ax.axhline(0, color="#444444", lw=1)
        ax.set_title(labels[detector])
        ax.set_xlabel("Maximum external reference-box edits")
        ax.grid(alpha=0.16)
        ax.legend(fontsize=8, loc="upper right")
    axes[0].set_ylabel("Internal minus external recall (percentage points)")
    fig.suptitle(f"External shortfall under bounded annotation changes | {budget:g} FP/image")
    fig.text(
        0.5,
        0.01,
        "Fixed predictions; internal annotations unchanged. "
        "Shading describes sampling variation of the bound.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.045, 1, 0.96))
    save(fig, "domain_gap")

    fig, ax = plt.subplots(figsize=(8, 4.2))
    selected = exact[
        (exact.dataset == "external")
        & (exact.entity == f"{detectors[0]}-{detectors[1]}")
        & (exact.budget == budget)
    ].sort_values("deletions")
    for i, row in enumerate(selected.itertuples()):
        for offset, lower, upper, color, label in (
            (-0.12, row.lower, row.upper, colors[0], "Same edits for every run and detector"),
            (
                0.12,
                row.independent_lower,
                row.independent_upper,
                colors[1],
                "Independent edits: relaxed comparison",
            ),
        ):
            y = i + offset
            ax.plot(
                [lower * 100, upper * 100],
                [y, y],
                color=color,
                lw=5,
                solid_capstyle="butt",
                label=label if i == 0 else None,
            )
            ax.scatter([lower * 100, upper * 100], [y, y], color=color, s=15)
    original_gap = (
        baseline.loc["external", detectors[0], budget]
        - baseline.loc["external", detectors[1], budget]
    )
    ax.axvline(original_gap * 100, color="#666666", ls="--", lw=1, label="Original mean difference")
    ax.set_yticks(
        range(len(selected)), [f"Exactly {d} deleted reference(s)" for d in selected.deletions]
    )
    ax.set_ylim(-0.6, len(selected) - 0.4)
    ax.invert_yaxis()
    ax.set_xlabel("Faster R-CNN minus YOLO recall (percentage points)")
    ax.set_title(f"Shared annotations narrow the external comparison | {budget:g} FP/image")
    ax.grid(axis="x", alpha=0.16)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.23), fontsize=9)
    fig.text(
        0.5,
        0.01,
        "Ranges are finite-scenario extrema, not confidence intervals. "
        "All observed runs are included.",
        ha="center",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "shared_deletions")

    text = [
        "# Shared-annotation FROC audit: results v1",
        "",
        "Generated from hash-verified public aggregates. This is a retrospective "
        "sensitivity analysis, not clinical relabeling or a deployed repair.",
        "",
        "See the [method and proofs](FROC_ANNOTATION_METHOD_V1.md) "
        "and [protocol](FROC_ANNOTATION_PROTOCOL_V1.md).",
        "",
        "All five seeds per detector, both complete cohorts and all five original "
        f"budgets were analyzed. The primary display uses **{budget:g} FP/image**.",
        "",
        "## Conditional domain-gap certificates",
        "",
        "Only external references may change here; internal annotations, images and "
        "all detector candidates remain fixed. The maximum tested count is not an "
        "estimated error rate.",
        "",
        "| Detector | Internal recall | External recall | "
        "Largest tested edit budget with positive gap lower bound |",
        "|---|---:|---:|---:|",
    ]
    for detector in detectors:
        text.append(
            f"| {labels[detector]} | {baseline.loc['internal', detector, budget]:.6f} | "
            f"{baseline.loc['external', detector, budget]:.6f} | {radii[detector]} |"
        )
    text.extend(
        [
            "",
            "The next edit count loses the conservative certificate; it does not "
            "demonstrate an attainable explanation or recovery. Sampling uncertainty "
            "is more restrictive than these point certificates.",
            "",
            "| Detector | External edit budget | Gap lower bound | "
            "Marginal 95% interval for that bound |",
            "|---|---:|---:|---|",
        ]
    )
    for detector in detectors:
        for k in (0, 10, 20, 30, 40):
            row = contrasts[
                (contrasts.detector == detector)
                & (contrasts.budget == budget)
                & (contrasts.external_edits == k)
                & (contrasts.endpoint == "lower")
            ].iloc[0]
            text.append(
                f"| {labels[detector]} | {k} | {row.point:.6f} | "
                f"[{row.lower:.6f}, {row.upper:.6f}] |"
            )
    text.extend(
        [
            "",
            f"![Domain gap certificates](../{(root / config['figures']['domain_gap']).as_posix()})",
            "",
            "Intervals use 2,000 joint patient/image/run draws. The edit units are "
            "resampled observation copies. These are marginal percentile intervals "
            "for conditional bound endpoints, not finite-sample or clinical-error guarantees.",
            "",
            "## Exact shared-reference deletion census",
            "",
            "Every subset of one/two existing references was evaluated: 268/35,778 internal "
            "subsets and 95/4,465 external subsets. Each subset is shared across both "
            "detectors and every seed before averaging and comparing.",
            "",
            "| External deletions | Shared difference range | Independent-edit range | "
            "Width reduction |",
            "|---:|---|---|---:|",
        ]
    )
    for row in selected.itertuples():
        reduction = 1 - (row.upper - row.lower) / (row.independent_upper - row.independent_lower)
        text.append(
            f"| {row.deletions} | [{row.lower:.6f}, {row.upper:.6f}] | "
            f"[{row.independent_lower:.6f}, {row.independent_upper:.6f}] | {reduction:.1%} |"
        )
    text.extend(
        [
            "",
            "![Shared deletion ranges]"
            f"(../{(root / config['figures']['shared_deletions']).as_posix()})",
            "",
            "These are exact extrema for the declared finite deletion set, not confidence "
            "intervals. Independent edits can require contradictory annotation sets "
            "across runs/detectors; that relaxation is shown only as a comparator. "
            "No annotation is asserted incorrect, and no corrected labels are exported.",
            "",
            "## Interpretation and limits",
            "",
            "The exact shared-subset result adds information absent from complete marginal "
            "FROC curves; the method includes a constructive proof. It also distinguishes "
            "annotation sensitivity from sampling uncertainty. It does not identify clinical "
            "causes, prove label equivalence or establish publication priority. Bounds are "
            "conditional on fixed scores, geometry, caps, image population and the canonical "
            "one-to-one matcher; crowd/ignore protocols are outside scope.",
            "",
            "Full values for every original budget are in the public `envelopes.csv`, "
            "`exact_deletions.csv`, `intervals.csv` and `contrasts.csv` beside the figures. "
            "Observation-linked arrays remain private.",
            "",
        ]
    )
    outputs[Path(config["report"])] = "\n".join(text).encode("utf-8")
    receipt = root / config["receipt"]
    if replay:
        stored = read_json(receipt)
        for item in stored["inputs"] + stored["artifacts"]:
            verify_artifact(item)
        for path, content in outputs.items():
            require(path.read_bytes() == content, f"Report replay differs: {path}")
        return dict(status="byte_exact_report_replay_passed", outputs=len(outputs))
    require(
        not receipt.exists() and not any(p.exists() for p in outputs),
        "Report output exists; use replay",
    )
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    write_json(receipt, dict(inputs=sources, artifacts=[artifact(p) for p in outputs]))
    return dict(status="report_created", receipt=artifact(receipt))


def main() -> None:
    """Generate or exactly replay the aggregate-only report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    print(build(args.config, replay=args.replay))


if __name__ == "__main__":
    main()
