import numpy as np

from refmotion_gs_mvp.src.dense_normal_optimization import make_initial_perturbed_normals
from refmotion_gs_mvp.src.losses import reflection_cycle_loss
from refmotion_gs_mvp.src.near_object_scene import (
    ReflectorPrimitive,
    generate_near_object_reflection_dataset,
    trace_reflector_color,
)


def test_trace_reflector_color_return_order_and_hit_identity():
    colors, hit_mask, reflector_id = trace_reflector_color(
        surface_points=np.array([[0.0, 0.0, 0.0]], dtype=float),
        reflected_dirs=np.array([[1.0, 0.0, 0.0]], dtype=float),
        reflectors=(
            ReflectorPrimitive(
                center=np.array([2.0, 0.0, 0.0], dtype=float),
                radius=0.5,
                color=np.array([0.9, 0.2, 0.1], dtype=float),
            ),
        ),
        fallback_color=np.array([0.01, 0.02, 0.03], dtype=float),
    )

    assert colors.shape == (1, 3)
    assert hit_mask.tolist() == [True]
    assert reflector_id.tolist() == [0]
    np.testing.assert_allclose(colors[0], np.array([0.9, 0.2, 0.1], dtype=float))


def test_near_object_scene_is_deterministic_and_has_reflector_hits():
    first = generate_near_object_reflection_dataset()
    second = generate_near_object_reflection_dataset()

    for field in (
        "images",
        "normals",
        "albedo",
        "roughness",
        "reflective_mask",
        "object_mask",
        "surface_points",
        "reflected_color",
    ):
        np.testing.assert_allclose(
            getattr(first.dataset, field),
            getattr(second.dataset, field),
            equal_nan=True,
        )
    np.testing.assert_array_equal(first.reflector_hit_mask, second.reflector_hit_mask)
    np.testing.assert_array_equal(first.reflector_id, second.reflector_id)

    reflective_pixels = first.dataset.reflective_mask
    hit_fraction = float(np.mean(first.reflector_hit_mask[reflective_pixels]))
    assert hit_fraction >= 0.15
    assert first.train_view_indices == [0, 1, 2, 3]
    assert first.test_view_indices == [4, 5]


def test_near_object_loss_prefers_ground_truth_normals():
    scene = generate_near_object_reflection_dataset()
    perturbed = make_initial_perturbed_normals(scene.dataset, degrees=8.0)

    gt_loss = reflection_cycle_loss(
        scene.dataset,
        scene.dataset.normals,
        sample_count=80,
        seed=19,
    ).mean_loss
    perturbed_loss = reflection_cycle_loss(
        scene.dataset,
        perturbed,
        sample_count=80,
        seed=19,
    ).mean_loss

    assert gt_loss < perturbed_loss
