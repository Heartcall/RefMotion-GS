import numpy as np

from refmotion_gs_mvp.src.metrics import normal_angular_error_degrees, specular_leakage_score
from refmotion_gs_mvp.src.normal_optimization import optimize_global_normal_rotation
from refmotion_gs_mvp.src.reflection_geometry import rotate_vectors
from refmotion_gs_mvp.src.synthetic_scene import generate_analytic_dataset
from refmotion_gs_mvp.src.uv_baking import (
    bake_pixels_with_routing,
    make_noisy_reflective_mask,
    reflection_confidence_mask,
)


def test_normal_only_optimization_reduces_reflective_normal_error():
    dataset = generate_analytic_dataset(num_views=6, width=36, height=28, seed=13)
    init = dataset.normals.copy()
    init[dataset.object_mask] = rotate_vectors(
        init[dataset.object_mask],
        axis=np.array([1.0, 0.0, 0.0]),
        degrees=8.0,
    )

    result = optimize_global_normal_rotation(dataset, init, iterations=5, initial_step_degrees=4.0, sample_count=180)
    init_error = normal_angular_error_degrees(init, dataset.normals, dataset.reflective_mask).mean()
    final_error = normal_angular_error_degrees(result.normals, dataset.normals, dataset.reflective_mask).mean()

    assert final_error < 0.9 * init_error
    assert result.loss_history[-1] <= result.loss_history[0]


def test_reflection_confidence_routing_reduces_noisy_mask_leakage():
    dataset = generate_analytic_dataset(num_views=5, width=34, height=26, seed=17)
    noisy_reflective = make_noisy_reflective_mask(dataset.reflective_mask, false_negative_rate=0.35, seed=1)
    all_pixels = bake_pixels_with_routing(dataset, route_to_texture=dataset.object_mask)
    noisy_mask = bake_pixels_with_routing(dataset, route_to_texture=dataset.object_mask & ~noisy_reflective)
    confidence = reflection_confidence_mask(dataset, dataset.normals, seed=2)
    proposed = bake_pixels_with_routing(
        dataset,
        route_to_texture=dataset.object_mask & ~noisy_reflective & ~confidence,
    )

    mask = dataset.reflective_mask
    all_leakage = specular_leakage_score(all_pixels.baked_albedo, dataset.albedo, dataset.reflected_color, mask)
    noisy_leakage = specular_leakage_score(noisy_mask.baked_albedo, dataset.albedo, dataset.reflected_color, mask)
    proposed_leakage = specular_leakage_score(proposed.baked_albedo, dataset.albedo, dataset.reflected_color, mask)

    assert proposed_leakage < all_leakage
    assert proposed_leakage < noisy_leakage

