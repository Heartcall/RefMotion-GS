from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import sys

os.environ.setdefault("MPLCONFIGDIR", "/tmp/refmotion_gs_mvp_mpl")

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from refmotion_gs_mvp.scripts.run_phase3_milestone33 import _baking_metrics, _loss_landscape, _normal_metrics
from refmotion_gs_mvp.src.decision_checks import compute_routing_decision_checks
from refmotion_gs_mvp.src.dense_normal_optimization import (
    make_initial_perturbed_normals,
    optimize_dense_tangent_normals,
    run_dense_no_cycle_ablation,
)
from refmotion_gs_mvp.src.near_object_scene import generate_near_object_reflection_dataset
from refmotion_gs_mvp.src.phase3_revision_diagnostics import (
    active_texel_hit_fraction_map,
    compute_reflector_hit_coverage_by_texel,
    rank_reflective_active_texels,
    replay_dense_updates_for_diagnostics,
)


def _plot_objective_vs_normal_error(path: Path, trajectory: dict) -> None:
    x = np.arange(len(trajectory["reflective_error_history"]))
    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(x, trajectory["reflective_error_history"], marker="o", color="tab:red", label="reflective error")
    ax1.set_xlabel("Accepted dense update state")
    ax1.set_ylabel("Reflective normal error (deg)", color="tab:red")
    ax1.tick_params(axis="y", labelcolor="tab:red")
    ax2 = ax1.twinx()
    ax2.plot(x, trajectory["objective_history"], marker="s", color="tab:blue", label="objective")
    ax2.set_ylabel("Dense objective", color="tab:blue")
    ax2.tick_params(axis="y", labelcolor="tab:blue")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _plot_hit_coverage(path: Path, hit_fraction_map: np.ndarray) -> None:
    masked = np.ma.masked_invalid(hit_fraction_map)
    plt.figure(figsize=(7, 4))
    plt.imshow(masked, interpolation="nearest", vmin=0.0, vmax=1.0, cmap="viridis")
    plt.xlabel("UV texel x")
    plt.ylabel("UV texel y")
    plt.colorbar(label="finite reflector hit fraction")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def _recommendation(
    checks: dict[str, bool],
    trajectory: dict,
    routing: dict,
) -> str:
    corr = trajectory["objective_reflective_error_correlation"]
    if not checks["loss_correlated_near_gt"]:
        return "stop: reflection-cycle loss is not correlated with normal correctness"
    if corr is not None and corr < 0.0:
        return "pivot: dense objective descent is anti-correlated with reflective normal correctness"
    if trajectory["reflective_improvement_history"][-1] < 10.0:
        return "revise: dense trajectory diagnostics explain the failed 10 percent normal gate"
    if not routing["normal_refinement_beats_noisy_mask"]:
        return "revise: normal-refinement routing does not beat noisy-mask routing"
    return "continue to short audit"


def _write_summary(path: Path, metrics: dict) -> None:
    trajectory = metrics["dense_trajectory_diagnostics"]
    coverage = metrics["coverage_diagnostics"]
    routing = metrics["routing_diagnostics"]
    reflectors = metrics["reflectors"]
    lines = [
        "# Phase 3 Milestone 3.3 Revision Diagnostics Summary",
        "",
        "## Evidence",
        "",
        f"- reflector_hit_fraction: {coverage['reflector_hit_fraction']}",
        f"- active_texel_count: {coverage['active_texel_count']}",
        f"- active_texel_hit_fraction_mean: {coverage['active_texel_hit_fraction_mean']}",
        f"- active_texels_without_finite_hits: {coverage['active_texels_without_finite_hits']}",
        f"- accepted_update_count: {trajectory['accepted_update_count']}",
        f"- worsened_reflective_update_count: {trajectory['worsened_reflective_update_count']}",
        f"- objective_reflective_error_correlation: {trajectory['objective_reflective_error_correlation']}",
        f"- final_reflective_improvement_percent: {trajectory['reflective_improvement_history'][-1]}",
        f"- normal_refinement_improves_over_reflection_confidence: {str(routing['normal_refinement_improves_over_reflection_confidence']).lower()}",
        f"- normal_refinement_beats_noisy_mask: {str(routing['normal_refinement_beats_noisy_mask']).lower()}",
        f"- normal_refinement_beats_oracle_mask: {str(routing['normal_refinement_beats_oracle_mask']).lower()}",
        "",
        "## Reflector Primitive Reconciliation",
        "",
        "- The implemented Milestone 3.3 radii are treated as the recorded diagnostic scene for this revision.",
        "- Larger radii were used to obtain a minimum finite-reflector hit fraction in the low-resolution smoke scene.",
        "- The hit fraction is barely above the gate, so it is not a strong realism claim.",
    ]
    for idx, reflector in enumerate(reflectors):
        lines.append(
            f"- reflector {idx}: center={reflector['center']}, radius={reflector['radius']}, color={reflector['color']}"
        )
    lines.extend(
        [
            "",
            "## Routing Diagnostics",
            "",
            f"- all-pixel leakage: {routing['uv_leakage']['all_pixels']}",
            f"- noisy-mask leakage: {routing['uv_leakage']['noisy_mask_only']}",
            f"- reflection-confidence routing leakage: {routing['uv_leakage']['reflection_confidence_routing']}",
            f"- normal-refinement-plus-routing leakage: {routing['uv_leakage']['normal_refinement_plus_routing']}",
            f"- oracle mask exclusion leakage: {routing['uv_leakage']['oracle_mask_exclusion']}",
            "- oracle mask exclusion remains an honest comparator and is still reported even when stronger.",
            "",
            "## Inference",
            "",
            "- The diagnostic output measures whether objective descent aligns with reflective-region normal correctness.",
            "- Normal-refinement-plus-routing is explicitly compared with reflection-confidence routing, noisy-mask-only, and oracle mask exclusion.",
            "- The revision remains controlled synthetic evidence and does not support paper-level claims by itself.",
            "",
            "## Decision",
            "",
            f"- recommendation: {metrics['recommendation']}",
            "",
            "## Next Action",
            "",
            "- Run a short audit before treating this revision state as accepted.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    out_dir: Path,
    num_views: int = 6,
    width: int = 28,
    height: int = 24,
    uv_height: int = 16,
    uv_width: int = 32,
    dense_iterations: int = 8,
    max_active_texels: int = 64,
    sample_count: int = 50,
    update_radius: int = 1,
) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    scene = generate_near_object_reflection_dataset(
        num_views=num_views,
        width=width,
        height=height,
        seed=173,
    )
    dataset = scene.dataset
    init_normals = make_initial_perturbed_normals(dataset, degrees=8.0)
    loss_landscape = _loss_landscape(dataset, sample_count=140, seed=31)
    dense = optimize_dense_tangent_normals(
        dataset,
        init_normals,
        uv_height=uv_height,
        uv_width=uv_width,
        iterations=dense_iterations,
        initial_step=0.08,
        max_active_texels=max_active_texels,
        sample_count=sample_count,
        seed=67,
        loss_seed=71,
        update_radius=update_radius,
    )
    no_cycle = run_dense_no_cycle_ablation(
        dataset,
        init_normals,
        uv_height=uv_height,
        uv_width=uv_width,
        iterations=dense_iterations,
        initial_step=0.08,
        max_active_texels=max_active_texels,
        seed=67,
        update_radius=update_radius,
    )

    dense_metrics = _normal_metrics(dataset, init_normals, dense.normals)
    no_cycle_metrics = _normal_metrics(dataset, init_normals, no_cycle.normals)
    pixel_metrics, uv_metrics = _baking_metrics(dataset, init_normals, dense.normals)
    del pixel_metrics
    routing_checks = compute_routing_decision_checks(uv_metrics["specular_leakage_score"])
    reflective_pixels = dataset.reflective_mask
    reflector_hit_fraction = float(np.mean(scene.reflector_hit_mask[reflective_pixels]))
    checks = {
        "loss_correlated_near_gt": bool(
            loss_landscape["0deg"] < loss_landscape["5deg"] < loss_landscape["10deg"]
        ),
        "reflector_hit_fraction_sufficient": bool(reflector_hit_fraction >= 0.15),
        "dense_normal_error_improves_10_percent": bool(
            dense_metrics["final_reflective_error_deg"]
            < 0.9 * dense_metrics["init_reflective_error_deg"]
        ),
        "dense_beats_no_cycle_ablation": bool(
            dense_metrics["final_reflective_error_deg"]
            < no_cycle_metrics["final_reflective_error_deg"]
        ),
        **routing_checks,
    }

    active_texels = rank_reflective_active_texels(
        dataset,
        uv_height=uv_height,
        uv_width=uv_width,
        max_active_texels=max_active_texels,
    )
    trajectory = asdict(
        replay_dense_updates_for_diagnostics(
            dataset,
            init_normals,
            dense.accepted_updates,
            uv_height=uv_height,
            uv_width=uv_width,
            objective_history=dense.loss_history,
        )
    )
    coverage = asdict(
        compute_reflector_hit_coverage_by_texel(
            scene,
            uv_height=uv_height,
            uv_width=uv_width,
            active_texels=active_texels,
        )
    )
    uv_leakage = uv_metrics["specular_leakage_score"]
    routing = {
        "uv_leakage": uv_leakage,
        "normal_refinement_improves_over_reflection_confidence": bool(
            uv_leakage["normal_refinement_plus_routing"] < uv_leakage["reflection_confidence_routing"]
        ),
        "normal_refinement_beats_noisy_mask": bool(
            uv_leakage["normal_refinement_plus_routing"] < uv_leakage["noisy_mask_only"]
        ),
        "normal_refinement_beats_oracle_mask": bool(
            uv_leakage["normal_refinement_plus_routing"] < uv_leakage["oracle_mask_exclusion"]
        ),
    }
    metrics = {
        "dataset": {
            "scene_type": "analytic_near_object_reflection",
            "num_views": int(dataset.images.shape[0]),
            "width": int(dataset.images.shape[2]),
            "height": int(dataset.images.shape[1]),
            "seed": 173,
            "object_pixels": int(dataset.object_mask.sum()),
            "reflective_pixels": int(dataset.reflective_mask.sum()),
            "reflector_hit_fraction": reflector_hit_fraction,
        },
        "reflectors": [
            {
                "center": np.asarray(reflector.center, dtype=float).tolist(),
                "radius": float(reflector.radius),
                "color": np.asarray(reflector.color, dtype=float).tolist(),
            }
            for reflector in scene.reflectors
        ],
        "baseline_milestone33_decision_checks": checks,
        "dense_trajectory_diagnostics": trajectory,
        "coverage_diagnostics": coverage,
        "routing_diagnostics": routing,
        "phase3": {
            "milestone": "3.3_revision",
            "purpose": "dense_normal_gate_failure_diagnostics",
            "renderer_path": "analytic_near_object_fallback",
            "used_blender_cycles": False,
            "implements_learned_near_field_reflection_field": False,
            "implements_inter_reflection_residual": False,
            "implements_full_pbr_optimization": False,
            "claims_relighting_or_material_editing": False,
            "claims_representation_novelty": False,
        },
    }
    metrics["recommendation"] = _recommendation(checks, trajectory, routing)

    with (out_dir / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    _write_summary(out_dir / "summary.md", metrics)
    _plot_objective_vs_normal_error(out_dir / "objective_vs_normal_error.png", trajectory)
    hit_fraction_map = active_texel_hit_fraction_map(scene, uv_height, uv_width, active_texels)
    _plot_hit_coverage(out_dir / "reflector_hit_coverage_by_texel.png", hit_fraction_map)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        default="refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics",
    )
    args = parser.parse_args()
    metrics = run(Path(args.out_dir))
    print(json.dumps(metrics["recommendation"], indent=2))


if __name__ == "__main__":
    main()
