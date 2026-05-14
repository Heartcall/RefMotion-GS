import numpy as np

from refmotion_gs_mvp.src.metrics import albedo_rmse, normal_angular_error_degrees, specular_leakage_score


def test_normal_angular_error_degrees_known_angles():
    gt = np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])
    pred = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])

    err = normal_angular_error_degrees(pred, gt)

    assert np.allclose(err, np.array([0.0, 90.0]), atol=1e-5)


def test_albedo_rmse_uses_mask():
    pred = np.zeros((2, 2, 3), dtype=float)
    gt = np.zeros((2, 2, 3), dtype=float)
    gt[0, 0] = 1.0
    mask = np.zeros((2, 2), dtype=bool)
    mask[0, 0] = True

    assert np.isclose(albedo_rmse(pred, gt, mask), 1.0)


def test_specular_leakage_score_increases_with_reflected_color_residual():
    baked = np.array([[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2]]], dtype=float)
    gt = np.array([[[0.2, 0.2, 0.2], [0.2, 0.2, 0.2]]], dtype=float)
    reflected = np.array([[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]], dtype=float)
    mask = np.ones((1, 2), dtype=bool)

    leakage = specular_leakage_score(baked, gt, reflected, mask)

    assert leakage > 0.9

