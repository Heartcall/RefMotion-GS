import numpy as np

from refmotion_gs_mvp.src.feature_matching import topk_reflected_ray_candidates
from refmotion_gs_mvp.src.losses import reflection_cycle_loss
from refmotion_gs_mvp.src.reflection_geometry import rotate_vectors
from refmotion_gs_mvp.src.synthetic_scene import generate_analytic_dataset


def test_topk_reflected_ray_candidates_returns_best_direction_match():
    query_direction = np.array([0.0, 0.0, 1.0])
    candidate_directions = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.1, 0.995],
            [0.0, -1.0, 0.0],
        ],
        dtype=float,
    )
    candidate_points = np.zeros((3, 3), dtype=float)

    indices, distances = topk_reflected_ray_candidates(
        query_point=np.zeros(3),
        query_direction=query_direction,
        candidate_points=candidate_points,
        candidate_directions=candidate_directions,
        k=1,
        beta=0.0,
    )

    assert indices.tolist() == [1]
    assert distances[0] < 0.02


def test_reflection_cycle_loss_is_lower_for_ground_truth_normals_than_perturbed_normals():
    dataset = generate_analytic_dataset(num_views=6, width=36, height=28, seed=11)
    gt_loss = reflection_cycle_loss(dataset, normals=dataset.normals, sample_count=220, seed=5)
    perturbed = dataset.normals.copy()
    perturbed[dataset.object_mask] = rotate_vectors(
        perturbed[dataset.object_mask],
        axis=np.array([1.0, 0.0, 0.0]),
        degrees=8.0,
    )

    perturbed_loss = reflection_cycle_loss(dataset, normals=perturbed, sample_count=220, seed=5)

    assert gt_loss.mean_loss < perturbed_loss.mean_loss
    assert gt_loss.valid_pairs > 100

