from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

os.environ.setdefault("MPLCONFIGDIR", "/tmp/refmotion_gs_mvp_mpl")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from refmotion_gs_mvp.src.losses import reflection_cycle_loss
from refmotion_gs_mvp.src.metrics import albedo_rmse, normal_angular_error_degrees, specular_leakage_score
from refmotion_gs_mvp.src.normal_optimization import optimize_global_normal_rotation
from refmotion_gs_mvp.src.reflection_geometry import normalize, rotate_vectors
from refmotion_gs_mvp.src.synthetic_scene import generate_analytic_dataset
from refmotion_gs_mvp.src.uv_baking import (
    bake_sphere_uv_texture,
    bake_pixels_with_routing,
    make_noisy_reflective_mask,
    reflection_confidence_mask,
)


def _save_image(path: Path, image: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    array = np.clip(image * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(array).save(path)


def _perturb_normals(normals: np.ndarray, object_mask: np.ndarray, degrees: float) -> np.ndarray:
    perturbed = normals.copy()
    perturbed[object_mask] = normalize(
        rotate_vectors(perturbed[object_mask], axis=np.array([1.0, 0.0, 0.0]), degrees=degrees)
    )
    return perturbed


def _smooth_random_perturbation(normals: np.ndarray, object_mask: np.ndarray, seed: int, scale: float = 0.14) -> np.ndarray:
    rng = np.random.default_rng(seed)
    updated = normals.copy()
    noise = rng.normal(0.0, scale, size=updated[object_mask].shape)
    updated[object_mask] = normalize(updated[object_mask] + noise)
    return updated


def _plot_loss_landscape(out_dir: Path, loss_landscape: dict[str, float]) -> None:
    numeric_keys = [key for key in loss_landscape if key.endswith("deg")]
    numeric_keys.sort(key=lambda name: float(name.replace("deg", "")))
    labels = numeric_keys + [key for key in loss_landscape if key not in numeric_keys]
    values = [loss_landscape[key] for key in labels]
    plt.figure(figsize=(7, 4))
    plt.plot(labels, values, marker="o")
    plt.ylabel("Reflection-cycle loss")
    plt.xlabel("Normal perturbation")
    plt.tight_layout()
    plt.savefig(out_dir / "loss_landscape.png", dpi=160)
    plt.close()


def _plot_leakage(out_dir: Path, leakage: dict[str, float]) -> None:
    labels = list(leakage)
    values = [leakage[key] for key in labels]
    plt.figure(figsize=(8, 4))
    plt.bar(labels, values)
    plt.ylabel("Specular leakage score")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(out_dir / "leakage_bars.png", dpi=160)
    plt.close()


def _plot_normal_history(out_dir: Path, history: list[float]) -> None:
    plt.figure(figsize=(7, 4))
    plt.plot(np.arange(len(history)), history, marker="o")
    plt.ylabel("Optimization loss")
    plt.xlabel("Coordinate-search iteration")
    plt.tight_layout()
    plt.savefig(out_dir / "normal_optimization_loss.png", dpi=160)
    plt.close()


def run(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    dataset = generate_analytic_dataset(num_views=8, width=48, height=36, seed=23)
    _save_image(out_dir / "synthetic_view0.png", dataset.images[0])
    _save_image(out_dir / "synthetic_view0_reflective_mask.png", np.repeat(dataset.reflective_mask[0][..., None], 3, axis=2))

    perturbations = {
        "0deg": dataset.normals,
        "1deg": _perturb_normals(dataset.normals, dataset.object_mask, 1.0),
        "3deg": _perturb_normals(dataset.normals, dataset.object_mask, 3.0),
        "5deg": _perturb_normals(dataset.normals, dataset.object_mask, 5.0),
        "10deg": _perturb_normals(dataset.normals, dataset.object_mask, 10.0),
        "smooth_random": _smooth_random_perturbation(dataset.normals, dataset.object_mask, seed=29),
    }
    loss_landscape = {
        name: reflection_cycle_loss(dataset, normals, sample_count=350, seed=31).mean_loss
        for name, normals in perturbations.items()
    }

    init_normals = _perturb_normals(dataset.normals, dataset.object_mask, 8.0)
    optimization = optimize_global_normal_rotation(
        dataset,
        init_normals,
        iterations=7,
        initial_step_degrees=4.0,
        sample_count=300,
        seed=37,
    )
    init_ref_error = float(normal_angular_error_degrees(init_normals, dataset.normals, dataset.reflective_mask).mean())
    final_ref_error = float(normal_angular_error_degrees(optimization.normals, dataset.normals, dataset.reflective_mask).mean())
    init_nonref_error = float(
        normal_angular_error_degrees(init_normals, dataset.normals, dataset.object_mask & ~dataset.reflective_mask).mean()
    )
    final_nonref_error = float(
        normal_angular_error_degrees(
            optimization.normals,
            dataset.normals,
            dataset.object_mask & ~dataset.reflective_mask,
        ).mean()
    )

    noisy_reflective = make_noisy_reflective_mask(dataset.reflective_mask, false_negative_rate=0.35, seed=41)
    all_pixels = bake_pixels_with_routing(dataset, route_to_texture=dataset.object_mask)
    oracle_mask = bake_pixels_with_routing(dataset, route_to_texture=dataset.object_mask & ~dataset.reflective_mask)
    noisy_mask = bake_pixels_with_routing(dataset, route_to_texture=dataset.object_mask & ~noisy_reflective)
    init_confidence = reflection_confidence_mask(dataset, init_normals)
    final_confidence = reflection_confidence_mask(dataset, optimization.normals)
    proposed_init = bake_pixels_with_routing(
        dataset,
        route_to_texture=dataset.object_mask & ~noisy_reflective & ~init_confidence,
    )
    proposed_final = bake_pixels_with_routing(
        dataset,
        route_to_texture=dataset.object_mask & ~noisy_reflective & ~final_confidence,
    )

    baking = {
        "all_pixels": all_pixels,
        "oracle_mask_exclusion": oracle_mask,
        "noisy_mask_only": noisy_mask,
        "reflection_confidence_routing": proposed_init,
        "normal_refinement_plus_routing": proposed_final,
    }
    leakage = {
        name: specular_leakage_score(result.baked_albedo, dataset.albedo, dataset.reflected_color, dataset.reflective_mask)
        for name, result in baking.items()
    }
    albedo = {
        name: albedo_rmse(result.baked_albedo, dataset.albedo, dataset.object_mask)
        for name, result in baking.items()
    }
    for name, result in baking.items():
        _save_image(out_dir / f"baked_{name}.png", result.baked_albedo[0])

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
    uv_leakage = {
        name: specular_leakage_score(result.projected_albedo, dataset.albedo, dataset.reflected_color, dataset.reflective_mask)
        for name, result in uv_baking.items()
    }
    uv_albedo = {
        name: albedo_rmse(result.projected_albedo, dataset.albedo, dataset.object_mask)
        for name, result in uv_baking.items()
    }
    for name, result in uv_baking.items():
        _save_image(out_dir / f"uv_texture_{name}.png", result.texture)

    _plot_loss_landscape(out_dir, loss_landscape)
    _plot_leakage(out_dir, uv_leakage)
    _plot_normal_history(out_dir, optimization.loss_history)

    metrics = {
        "dataset": {
            "num_views": int(dataset.images.shape[0]),
            "height": int(dataset.images.shape[1]),
            "width": int(dataset.images.shape[2]),
            "object_pixels": int(dataset.object_mask.sum()),
            "reflective_pixels": int(dataset.reflective_mask.sum()),
        },
        "loss_landscape": loss_landscape,
        "normal_optimization": {
            "init_reflective_error_deg": init_ref_error,
            "final_reflective_error_deg": final_ref_error,
            "reflective_error_improvement_percent": 100.0 * (init_ref_error - final_ref_error) / init_ref_error,
            "init_nonreflective_error_deg": init_nonref_error,
            "final_nonreflective_error_deg": final_nonref_error,
            "loss_history": optimization.loss_history,
            "accepted_steps": optimization.accepted_steps,
        },
        "texture_baking": {
            "specular_leakage_score": leakage,
            "albedo_rmse": albedo,
            "noisy_mask_false_negative_rate_observed": float(
                np.mean((dataset.reflective_mask == 1) & (noisy_reflective == 0))
                / np.mean(dataset.reflective_mask == 1)
            ),
        },
        "uv_texture_baking": {
            "specular_leakage_score": uv_leakage,
            "albedo_rmse": uv_albedo,
            "atlas_resolution": [64, 128],
        },
        "decision_checks": {
            "loss_correlated_near_gt": bool(
                loss_landscape["0deg"] < loss_landscape["5deg"] < loss_landscape["10deg"]
            ),
            "normal_error_improves_10_percent": bool(final_ref_error < 0.9 * init_ref_error),
            "routing_beats_all_pixels": bool(
                uv_leakage["normal_refinement_plus_routing"] < uv_leakage["all_pixels"]
            ),
            "routing_beats_noisy_mask": bool(
                uv_leakage["normal_refinement_plus_routing"] < uv_leakage["noisy_mask_only"]
            ),
            "routing_beats_oracle_mask": bool(
                uv_leakage["normal_refinement_plus_routing"] < uv_leakage["oracle_mask_exclusion"]
            ),
        },
    }
    with (out_dir / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="refmotion_gs_mvp/outputs/run_latest")
    args = parser.parse_args()
    metrics = run(Path(args.out_dir))
    print(json.dumps(metrics["decision_checks"], indent=2))


if __name__ == "__main__":
    main()
