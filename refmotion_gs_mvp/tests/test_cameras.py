import numpy as np

from refmotion_gs_mvp.src.cameras import Camera


def test_camera_projection_unprojection_round_trip():
    camera = Camera.look_at(
        center=np.array([0.0, 0.0, 3.0]),
        target=np.array([0.0, 0.0, 0.0]),
        up=np.array([0.0, 1.0, 0.0]),
        focal=80.0,
        width=64,
        height=48,
    )
    world_point = np.array([0.2, -0.1, 0.5])

    pixel, depth = camera.project(world_point)
    reconstructed = camera.unproject(pixel, depth)

    assert np.allclose(reconstructed, world_point, atol=1e-6)


def test_camera_center_ray_points_toward_target():
    camera = Camera.look_at(
        center=np.array([0.0, 0.0, 3.0]),
        target=np.array([0.0, 0.0, 0.0]),
        up=np.array([0.0, 1.0, 0.0]),
        focal=80.0,
        width=64,
        height=48,
    )

    origin, direction = camera.pixel_ray(np.array([32.0, 24.0]))

    assert np.allclose(origin, camera.center)
    assert np.allclose(direction, np.array([0.0, 0.0, -1.0]), atol=1e-6)

