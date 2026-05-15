from __future__ import annotations

import argparse
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

from refmotion_gs_mvp.src.decision_checks import compute_routing_decision_checks
from refmotion_gs_mvp.src.dense_normal_optimization import (
    make_initial_perturbed_normals,
    optimize_dense_tangent_normals,
    run_dense_no_cycle_ablation,
)
from refmotion_gs_mvp.src.losses import reflection_cycle_loss
from refmotion_gs_mvp.src.metrics import (
    albedo_rmse,
    normal_angular_error_degrees,
    specular_leakage_score,
)
from refmotion_gs_mvp.src.near_object_scene import generate_near_object_reflection_dataset
from refmotion_gs_mvp.src.normal_optimization import optimize_global_normal_rotation
from refmotion_gs_mvp.src.reflection_geometry import normalize, rotate_vectors
from refmotion_gs_mvp.src.uv_baking import (
    bake_pixels_with_routing,
    bake_sphere_uv_texture,
    make_noisy_reflective_mask,
    reflection_confidence_mask,
)


def _perturb_normals(normals: np.ndarray, object_mask: np.ndarray, degrees: float) -> np.ndarray:
    updated = normals.copy()
    updated[object_mask] = normalize(
        rotate_vectors(
            updated[object_mask],
            axis=np.array([1.0, 0.0, 0.0], dtype=float),
            degrees=degrees,
        )
    )
    return updated


def _normal_metrics(dataset, init_normals: np.ndarray, final_normals: np.ndarray) -> dict[str, float]:
    init_ref = float(
        normal_angular_error_degrees(
            init_normals,
            dataset.normals,
            dataset.reflective_mask,
        ).mean()
    )
    final_ref = float(
        normal_angular_error_degrees(
            final_normals,
            dataset.normals,
            dataset.reflective_mask,
        ).mean()
    )
    init_nonref = float(
        normal_angular_error_degrees(
            init_normals,
            dataset.normals,
            dataset.object_mask & ~dataset.reflective_mask,
        ).mean()
    )
    final_nonref = float(
        normal_angular_error_degrees(
            final_normals,
            dataset.normals,
            dataset.object_mask & ~dataset.reflective_mask,
        ).mean()
    )
    return {
        "init_reflective_error_deg": init_ref,
        "final_reflective_error_deg": final_ref,
        "reflective_error_improvement_percent": 100.0 * (init_ref - final_ref) / init_ref,
        "init_nonreflective_error_deg": init_nonref,
        "final_nonreflective_error_deg": final_nonref,
    }


def _loss_landscape(dataset, sample_count: int = 140, seed: int = 31) -> dict[str, float]:
    perturbations = {
        "0deg": dataset.normals,
        "5deg": _perturb_normals(dataset.normals, dataset.object_mask, 5.0),
        "10deg": _perturb_normals(dataset.normals, dataset.object_mask, 10.0),
    }
    return {
        name: reflection_cycle_loss(dataset, normals, sample_count=sample_count, seed=seed).mean_loss
        for name, normals in perturbations.items()
    }


def _baking_metrics(dataset, init_normals: np.ndarray, final_normals: np.ndarray) -> tuple[dict, dict]:
    noisy_reflective = make_noisy_reflective_mask(
        dataset.reflective_mask,
        false_negative_rate=0.35,
        seed=41,
    )
    init_confidence = reflection_confidence_mask(dataset, init_normals)
    final_confidence = reflection_confidence_mask(dataset, final_normals)

    pixel_baking = {
        "all_pixels": bake_pixels_with_routing(dataset, route_to_texture=dataset.object_mask),
        "oracle_mask_exclusion": bake_pixels_with_routing(
            dataset,
            route_to_texture=dataset.object_mask & ~dataset.reflective_mask,
        ),
        "noisy_mask_only": bake_pixels_with_routing(
            dataset,
            route_to_texture=dataset.object_mask & ~noisy_reflective,
        ),
        "reflection_confidence_routing": bake_pixels_with_routing(
            dataset,
            route_to_texture=dataset.object_mask & ~noisy_reflective & ~init_confidence,
        ),
        "normal_refinement_plus_routing": bake_pixels_with_routing(
            dataset,
            route_to_texture=dataset.object_mask & ~noisy_reflective & ~final_confidence,
        ),
    }
    uv_baking = {
        "all_pixels": bake_sphere_uv_texture(dataset, route_to_texture=dataset.object_mask, resolution=64),
        "oracle_mask_exclusion": bake_sphere_uv_texture(
            dataset,
            route_to_texture=dataset.object_mask & ~dataset.reflective_mask,
            resolution=64,
        ),
        "noisy_mask_only": bake_sphere_uv_texture(
            dataset,
            route_to_texture=dataset.object_mask & ~noisy_reflective,
            resolution=64,
        ),
        "reflection_confidence_routing": bake_sphere_uv_texture(
            dataset,
            route_to_texture=dataset.object_mask & ~noisy_reflective & ~init_confidence,
            resolution=64,
        ),
        "normal_refinement_plus_routing": bake_sphere_uv_texture(
            dataset,
            route_to_texture=dataset.object_mask & ~noisy_reflective & ~final_confidence,
            resolution=64,
        ),
    }

    pixel_metrics = {
        "specular_leakage_score": {
            name: specular_leakage_score(
                result.baked_albedo,
                dataset.albedo,
                dataset.reflected_color,
                dataset.reflective_mask,
            )
            for name, result in pixel_baking.items()
        },
        "albedo_rmse": {
            name: albedo_rmse(result.baked_albedo, dataset.albedo, dataset.object_mask)
            for name, result in pixel_baking.items()
        },
    }
    uv_metrics = {
        "specular_leakage_score": {
            name: specular_leakage_score(
                result.projected_albedo,
                dataset.albedo,
                dataset.reflected_color,
                dataset.reflective_mask,
            )
            for name, result in uv_baking.items()
        },
        "albedo_rmse": {
            name: albedo_rmse(result.projected_albedo, dataset.albedo, dataset.object_mask)
            for name, result in uv_baking.items()
        },
        "atlas_resolution": [64, 128],
    }
    return pixel_metrics, uv_metrics


def _plot_dense_loss(path: Path, loss_history: list[float]) -> None:
    plt.figure(figsize=(7, 4))
    plt.plot(np.arange(len(loss_history)), loss_history, marker="o")
    plt.xlabel("Coordinate-search iteration")
    plt.ylabel("Dense reflection-cycle objective")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def _plot_reflector_hit_map(path: Path, reflector_id: np.ndarray, object_mask: np.ndarray, view_idx: int = 0) -> None:
    image = np.full(reflector_id[view_idx].shape, -1, dtype=float)
    image[object_mask[view_idx]] = reflector_id[view_idx][object_mask[view_idx]]
    plt.figure(figsize=(5, 4))
    plt.imshow(image, cmap="viridis", interpolation="nearest", vmin=-1, vmax=max(2, int(np.max(reflector_id))))
    plt.xticks([])
    plt.yticks([])
    plt.colorbar(label="reflector id")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def _recommendation(checks: dict[str, bool], dense: dict[str, float]) -> str:
    if not checks["loss_correlated_near_gt"]:
        return "stop: reflection-cycle loss is not correlated with normal correctness"
    if not checks["reflector_hit_fraction_sufficient"]:
        return "revise: reflector hit fraction is below the finite-object visibility gate"
    if not checks["dense_normal_error_improves_10_percent"] and dense["reflective_error_improvement_percent"] > 0.0:
        return "revise: dense normal improvement is positive but below the 10 percent gate"
    if not checks["dense_normal_error_improves_10_percent"]:
        return "pivot: dense normal optimization did not improve reflective-region normal error"
    if not checks["dense_beats_no_cycle_ablation"]:
        return "pivot: dense no-cycle ablation explains the normal result"
    if checks["routing_beats_all_pixels"] and checks["routing_beats_noisy_mask"]:
        return "continue to post-result xhigh audit"
    return "revise: routing did not beat required non-oracle baselines"


def _write_summary(path: Path, metrics: dict) -> None:
    dataset = metrics["dataset"]
    dense = metrics["dense_normal_optimization"]
    ablation = metrics["dense_no_cycle_ablation"]
    checks = metrics["decision_checks"]
    uv_leakage = metrics["uv_texture_baking"]["specular_leakage_score"]
    phase3 = metrics["phase3"]
    lines = [
        "# Phase 3 Milestone 3.3 Near-Object Scene Summary",
        "",
        "## Scene Path",
        "",
        "- renderer_path: analytic_near_object_fallback",
        "- reason: Blender/Cycles is unavailable on PATH, so the audited analytic fallback is the current implementation path.",
        f"- reflector_hit_fraction: {dataset['reflector_hit_fraction']}",
        f"- reflector_hit_fraction_sufficient: {str(checks['reflector_hit_fraction_sufficient']).lower()}",
        "",
        "## Loss Landscape",
        "",
        f"- 0deg: {metrics['loss_landscape']['0deg']}",
        f"- 5deg: {metrics['loss_landscape']['5deg']}",
        f"- 10deg: {metrics['loss_landscape']['10deg']}",
        f"- loss_correlated_near_gt: {str(checks['loss_correlated_near_gt']).lower()}",
        "",
        "## Dense Reflection-Cycle Optimizer",
        "",
        f"- method_name: {dense['method_name']}",
        f"- reflective_error_improvement_percent: {dense['reflective_error_improvement_percent']}",
        f"- dense_normal_error_improves_10_percent: {str(checks['dense_normal_error_improves_10_percent']).lower()}",
        f"- dense_beats_no_cycle_ablation: {str(checks['dense_beats_no_cycle_ablation']).lower()}",
        f"- dense final reflective error: {dense['final_reflective_error_deg']}",
        f"- no-cycle final reflective error: {ablation['final_reflective_error_deg']}",
        "",
        "## Texture And Mask Baselines",
        "",
        f"- routing_beats_all_pixels: {str(checks['routing_beats_all_pixels']).lower()}",
        f"- routing_beats_noisy_mask: {str(checks['routing_beats_noisy_mask']).lower()}",
        f"- routing_beats_oracle_mask: {str(checks['routing_beats_oracle_mask']).lower()}",
        f"- oracle mask exclusion leakage: {uv_leakage['oracle_mask_exclusion']}",
        f"- normal refinement plus routing leakage: {uv_leakage['normal_refinement_plus_routing']}",
        "",
        "## Scope Flags",
        "",
        f"- used_blender_cycles: {str(phase3['used_blender_cycles']).lower()}",
        f"- implements_learned_near_field_reflection_field: {str(phase3['implements_learned_near_field_reflection_field']).lower()}",
        f"- implements_inter_reflection_residual: {str(phase3['implements_inter_reflection_residual']).lower()}",
        f"- implements_full_pbr_optimization: {str(phase3['implements_full_pbr_optimization']).lower()}",
        f"- claims_relighting_or_material_editing: {str(phase3['claims_relighting_or_material_editing']).lower()}",
        f"- claims_representation_novelty: {str(phase3['claims_representation_novelty']).lower()}",
        "",
        "## Recommendation",
        "",
        f"- {metrics['recommendation']}",
        "",
        "## Reviewer Risk Boundary",
        "",
        "- Evidence remains controlled synthetic analytic evidence, not a paper-level success claim.",
        "- MaterialRefGS / photometric-variation risk is not fully closed because this is not a MaterialRefGS baseline.",
        "- TextureSplat / texture-only risk is addressed only through retained texture-only, mask-only, and routing baselines.",
        "- SpecTRe-GS and Ref-DGS overlap is avoided because no learned near-field reflection field or local reflection Gaussian is implemented.",
        "- Mask-only threat remains binding; oracle mask exclusion is reported even when stronger.",
    ]
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
    loss_landscape = _loss_landscape(dataset, sample_count=140, seed=31)
    init_normals = make_initial_perturbed_normals(dataset, degrees=8.0)

    global_reference = optimize_global_normal_rotation(
        dataset,
        init_normals,
        iterations=7,
        initial_step_degrees=4.0,
        sample_count=120,
        seed=37,
    )
    global_metrics = _normal_metrics(dataset, init_normals, global_reference.normals)
    global_metrics["loss_history"] = global_reference.loss_history
    global_metrics["accepted_steps"] = [
        [axis, float(step)] for axis, step in global_reference.accepted_steps
    ]

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
    dense_metrics.update(
        {
            "method_name": "dense_reflection_cycle_optimizer",
            "parameterization": "sphere_uv_tangent_delta_grid",
            "uv_height": int(uv_height),
            "uv_width": int(uv_width),
            "active_texels": int(dense.active_texels),
            "uses_reflection_cycle_loss": True,
            "loss_history": dense.loss_history,
            "accepted_updates": dense.accepted_updates,
            "lambda_smooth": 0.02,
            "lambda_l2": 0.001,
            "sample_count": int(sample_count),
            "seed": 67,
            "loss_seed": 71,
            "update_radius": int(update_radius),
        }
    )
    no_cycle_metrics = _normal_metrics(dataset, init_normals, no_cycle.normals)
    no_cycle_metrics.update(
        {
            "method_name": "dense_no_cycle_ablation",
            "uses_reflection_cycle_loss": False,
            "loss_history": no_cycle.loss_history,
        }
    )

    pixel_metrics, uv_metrics = _baking_metrics(dataset, init_normals, dense.normals)
    routing_checks = compute_routing_decision_checks(uv_metrics["specular_leakage_score"])
    reflective_pixels = dataset.reflective_mask
    reflector_hit_fraction = float(np.mean(scene.reflector_hit_mask[reflective_pixels]))
    decision_checks = {
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
    metrics = {
        "dataset": {
            "scene_type": "analytic_near_object_reflection",
            "num_views": int(dataset.images.shape[0]),
            "width": int(dataset.images.shape[2]),
            "height": int(dataset.images.shape[1]),
            "seed": 173,
            "train_view_indices": scene.train_view_indices,
            "test_view_indices": scene.test_view_indices,
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
        "loss_landscape": loss_landscape,
        "global_rotation_reference": global_metrics,
        "dense_normal_optimization": dense_metrics,
        "dense_no_cycle_ablation": no_cycle_metrics,
        "pixel_baking": pixel_metrics,
        "uv_texture_baking": uv_metrics,
        "decision_checks": decision_checks,
        "phase3": {
            "milestone": "3.3",
            "purpose": "stricter_scene_or_renderer_validation",
            "renderer_path": "analytic_near_object_fallback",
            "used_blender_cycles": False,
            "implements_learned_near_field_reflection_field": False,
            "implements_inter_reflection_residual": False,
            "implements_full_pbr_optimization": False,
            "claims_relighting_or_material_editing": False,
            "claims_representation_novelty": False,
        },
    }
    metrics["recommendation"] = _recommendation(decision_checks, dense_metrics)

    with (out_dir / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    _plot_dense_loss(out_dir / "dense_loss_history.png", dense.loss_history)
    _plot_reflector_hit_map(out_dir / "reflector_hit_map.png", scene.reflector_id, dataset.object_mask)
    _write_summary(out_dir / "summary.md", metrics)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        default="refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene",
    )
    args = parser.parse_args()
    metrics = run(Path(args.out_dir))
    print(json.dumps(metrics["decision_checks"], indent=2))


if __name__ == "__main__":
    main()
