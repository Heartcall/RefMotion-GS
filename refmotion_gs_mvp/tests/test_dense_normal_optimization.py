import numpy as np

from refmotion_gs_mvp.src.dense_normal_optimization import (
    compose_dense_normals,
    make_initial_perturbed_normals,
    optimize_dense_tangent_normals,
    run_dense_no_cycle_ablation,
)
from refmotion_gs_mvp.src.metrics import normal_angular_error_degrees
from refmotion_gs_mvp.src.synthetic_scene import generate_analytic_dataset


def test_tangent_delta_normals_are_unit_length():
    dataset = generate_analytic_dataset(num_views=4, width=28, height=22, seed=101)
    init = make_initial_perturbed_normals(dataset, degrees=8.0)
    delta = np.zeros((8, 16, 2), dtype=float)
    delta[2, 3] = np.array([0.12, -0.08], dtype=float)

    normals = compose_dense_normals(dataset, init, delta)
    object_norms = np.linalg.norm(normals[dataset.object_mask], axis=1)

    assert np.all(np.isfinite(normals[dataset.object_mask]))
    assert np.allclose(object_norms, 1.0, atol=1e-6)


def test_dense_cycle_optimizer_reduces_reflective_error():
    dataset = generate_analytic_dataset(num_views=5, width=30, height=24, seed=103)
    init = make_initial_perturbed_normals(dataset, degrees=8.0)

    result = optimize_dense_tangent_normals(
        dataset,
        init,
        uv_height=4,
        uv_width=8,
        iterations=8,
        initial_step=0.08,
        max_active_texels=32,
        sample_count=40,
        seed=107,
        loss_seed=109,
    )
    init_error = normal_angular_error_degrees(
        init,
        dataset.normals,
        dataset.reflective_mask,
    ).mean()
    final_error = normal_angular_error_degrees(
        result.normals,
        dataset.normals,
        dataset.reflective_mask,
    ).mean()

    assert final_error < 0.9 * init_error
    assert result.loss_history[-1] <= result.loss_history[0]
    assert result.uses_reflection_cycle_loss is True


def test_no_cycle_dense_ablation_does_not_use_reflection_cycle_loss():
    dataset = generate_analytic_dataset(num_views=4, width=28, height=22, seed=111)
    init = make_initial_perturbed_normals(dataset, degrees=8.0)

    result = run_dense_no_cycle_ablation(
        dataset,
        init,
        uv_height=8,
        uv_width=16,
        iterations=2,
        max_active_texels=6,
        seed=113,
    )
    object_norms = np.linalg.norm(result.normals[dataset.object_mask], axis=1)

    assert result.uses_reflection_cycle_loss is False
    assert np.all(np.isfinite(result.normals[dataset.object_mask]))
    assert np.allclose(object_norms, 1.0, atol=1e-6)
