import numpy as np

from refmotion_gs_mvp.src.synthetic_scene import generate_analytic_dataset


def test_analytic_dataset_has_expected_shapes_and_finite_values():
    dataset = generate_analytic_dataset(num_views=5, width=32, height=24, seed=7)

    assert dataset.images.shape == (5, 24, 32, 3)
    assert dataset.normals.shape == (5, 24, 32, 3)
    assert dataset.albedo.shape == (5, 24, 32, 3)
    assert dataset.reflective_mask.shape == (5, 24, 32)
    assert len(dataset.cameras) == 5
    assert np.isfinite(dataset.images).all()
    assert np.isfinite(dataset.normals[dataset.object_mask]).all()


def test_reflective_pixels_have_view_dependent_color_variation():
    dataset = generate_analytic_dataset(num_views=8, width=40, height=30, seed=3)
    mask_any = dataset.reflective_mask & dataset.object_mask

    per_view_mean = []
    for view_idx in range(dataset.images.shape[0]):
        mask = mask_any[view_idx]
        assert mask.sum() > 20
        per_view_mean.append(dataset.images[view_idx][mask].mean(axis=0))
    per_view_mean = np.asarray(per_view_mean)

    assert per_view_mean.std(axis=0).max() > 0.02

