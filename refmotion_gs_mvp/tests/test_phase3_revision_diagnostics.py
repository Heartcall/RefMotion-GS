import numpy as np

from refmotion_gs_mvp.src.dense_normal_optimization import (
    make_initial_perturbed_normals,
    optimize_dense_tangent_normals,
)
from refmotion_gs_mvp.src.near_object_scene import generate_near_object_reflection_dataset
from refmotion_gs_mvp.src.phase3_revision_diagnostics import (
    compute_reflector_hit_coverage_by_texel,
    rank_reflective_active_texels,
    replay_dense_updates_for_diagnostics,
)


def test_dense_update_replay_reports_error_trajectory():
    scene = generate_near_object_reflection_dataset(num_views=4, width=18, height=16)
    dataset = scene.dataset
    init_normals = make_initial_perturbed_normals(dataset, degrees=8.0)
    dense = optimize_dense_tangent_normals(
        dataset,
        init_normals,
        uv_height=8,
        uv_width=16,
        iterations=2,
        max_active_texels=8,
        sample_count=20,
        seed=67,
        loss_seed=71,
        update_radius=1,
    )

    diagnostics = replay_dense_updates_for_diagnostics(
        dataset,
        init_normals,
        dense.accepted_updates,
        uv_height=8,
        uv_width=16,
        objective_history=dense.loss_history,
    )

    assert len(diagnostics.reflective_error_history) == diagnostics.accepted_update_count + 1
    assert len(diagnostics.nonreflective_error_history) == diagnostics.accepted_update_count + 1
    assert len(diagnostics.reflective_improvement_history) == diagnostics.accepted_update_count + 1
    assert np.all(np.isfinite(diagnostics.reflective_error_history))
    assert np.all(np.isfinite(diagnostics.nonreflective_error_history))
    assert isinstance(diagnostics.worsened_reflective_update_count, int)
    assert diagnostics.worsened_reflective_update_count >= 0


def test_reflector_hit_coverage_reports_active_texel_support():
    scene = generate_near_object_reflection_dataset()
    active_texels = rank_reflective_active_texels(
        scene.dataset,
        uv_height=16,
        uv_width=32,
        max_active_texels=64,
    )

    diagnostics = compute_reflector_hit_coverage_by_texel(
        scene,
        uv_height=16,
        uv_width=32,
        active_texels=active_texels,
    )

    assert diagnostics.reflector_hit_fraction >= 0.15
    assert diagnostics.active_texel_count > 0
    assert 0.0 <= diagnostics.active_texel_hit_fraction_min
    assert diagnostics.active_texel_hit_fraction_min <= diagnostics.active_texel_hit_fraction_mean
    assert diagnostics.active_texel_hit_fraction_mean <= 1.0
