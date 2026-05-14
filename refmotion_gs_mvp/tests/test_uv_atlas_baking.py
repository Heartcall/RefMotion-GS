import numpy as np

from refmotion_gs_mvp.src.metrics import specular_leakage_score
from refmotion_gs_mvp.src.synthetic_scene import generate_analytic_dataset
from refmotion_gs_mvp.src.uv_baking import bake_sphere_uv_texture, make_noisy_reflective_mask


def test_sphere_uv_bake_has_texture_and_projected_pixel_albedo():
    dataset = generate_analytic_dataset(num_views=4, width=32, height=24, seed=19)
    result = bake_sphere_uv_texture(dataset, route_to_texture=dataset.object_mask, resolution=32)

    assert result.texture.shape == (32, 64, 3)
    assert result.visibility_count.shape == (32, 64)
    assert result.projected_albedo.shape == dataset.images.shape
    assert np.isfinite(result.texture).all()


def test_sphere_uv_routing_reduces_leakage_against_all_pixel_and_noisy_mask():
    dataset = generate_analytic_dataset(num_views=5, width=34, height=26, seed=21)
    noisy_reflective = make_noisy_reflective_mask(dataset.reflective_mask, false_negative_rate=0.35, seed=3)
    all_uv = bake_sphere_uv_texture(dataset, route_to_texture=dataset.object_mask, resolution=40)
    noisy_uv = bake_sphere_uv_texture(dataset, route_to_texture=dataset.object_mask & ~noisy_reflective, resolution=40)
    oracle_uv = bake_sphere_uv_texture(dataset, route_to_texture=dataset.object_mask & ~dataset.reflective_mask, resolution=40)

    all_leakage = specular_leakage_score(all_uv.projected_albedo, dataset.albedo, dataset.reflected_color, dataset.reflective_mask)
    noisy_leakage = specular_leakage_score(noisy_uv.projected_albedo, dataset.albedo, dataset.reflected_color, dataset.reflective_mask)
    oracle_leakage = specular_leakage_score(oracle_uv.projected_albedo, dataset.albedo, dataset.reflected_color, dataset.reflective_mask)

    assert oracle_leakage < all_leakage
    assert oracle_leakage < noisy_leakage

