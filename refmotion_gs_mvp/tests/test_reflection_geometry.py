import numpy as np

from refmotion_gs_mvp.src.reflection_geometry import (
    angular_error_degrees,
    plucker_line,
    reflected_ray_distance,
    reflect,
    rotate_vectors,
)


def test_reflect_known_plane_normal():
    outgoing_to_camera = np.array([0.0, 0.0, 1.0])
    normal = np.array([0.0, 1.0, 1.0])
    normal = normal / np.linalg.norm(normal)

    reflected = reflect(outgoing_to_camera, normal)

    assert np.allclose(np.linalg.norm(reflected), 1.0)
    assert reflected[1] > 0.99
    assert abs(reflected[2]) < 1e-6


def test_plucker_reflected_ray_distance_is_symmetric():
    line_a = plucker_line(np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))
    line_b = plucker_line(np.array([-1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))

    ab = reflected_ray_distance(line_a, line_b, beta=0.25)
    ba = reflected_ray_distance(line_b, line_a, beta=0.25)

    assert np.isclose(ab, ba)
    assert ab > 0.0


def test_reflected_ray_distance_increases_with_normal_perturbation():
    point = np.array([0.0, 0.0, 0.0])
    outgoing = np.array([0.0, 0.0, 1.0])
    normal = np.array([0.0, 0.0, 1.0])
    gt_line = plucker_line(point, reflect(outgoing, normal))
    normal_5 = rotate_vectors(normal[None, :], axis=np.array([1.0, 0.0, 0.0]), degrees=5.0)[0]
    normal_10 = rotate_vectors(normal[None, :], axis=np.array([1.0, 0.0, 0.0]), degrees=10.0)[0]

    dist_5 = reflected_ray_distance(gt_line, plucker_line(point, reflect(outgoing, normal_5)), beta=0.25)
    dist_10 = reflected_ray_distance(gt_line, plucker_line(point, reflect(outgoing, normal_10)), beta=0.25)

    assert dist_10 > dist_5 > 0.0
    assert angular_error_degrees(normal[None, :], normal_10[None, :])[0] > 9.9

