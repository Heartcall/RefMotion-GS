from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from refmotion_gs_mvp.src.feature_matching import softmax_negative, topk_reflected_ray_candidates
from refmotion_gs_mvp.src.reflection_geometry import normalize, reflect
from refmotion_gs_mvp.src.synthetic_scene import AnalyticDataset


@dataclass(frozen=True)
class CycleLossResult:
    mean_loss: float
    valid_pairs: int


def _reflected_direction(camera_center: np.ndarray, point: np.ndarray, normal: np.ndarray) -> np.ndarray:
    outgoing = normalize(camera_center - point)
    return reflect(outgoing, normal)


def _valid_pixel_indices(mask: np.ndarray) -> np.ndarray:
    return np.argwhere(mask)


def reflection_cycle_loss(
    dataset: AnalyticDataset,
    normals: np.ndarray,
    sample_count: int = 500,
    k: int = 8,
    tau: float = 0.03,
    beta: float = 0.0,
    seed: int = 0,
) -> CycleLossResult:
    rng = np.random.default_rng(seed)
    losses: list[float] = []
    num_views = dataset.images.shape[0]

    for view_i in range(num_views):
        view_j = (view_i + 1) % num_views
        mask_i = dataset.object_mask[view_i] & dataset.reflective_mask[view_i]
        mask_j = dataset.object_mask[view_j] & dataset.reflective_mask[view_j]
        pixels_i = _valid_pixel_indices(mask_i)
        pixels_j = _valid_pixel_indices(mask_j)
        if len(pixels_i) == 0 or len(pixels_j) == 0:
            continue

        chosen = pixels_i[rng.choice(len(pixels_i), size=min(sample_count, len(pixels_i)), replace=False)]
        candidate_points = dataset.surface_points[view_j][mask_j]
        candidate_normals = normals[view_j][mask_j]
        candidate_dirs = reflect(normalize(dataset.cameras[view_j].center - candidate_points), candidate_normals)
        candidate_features = dataset.images[view_j][mask_j]

        for y, x in chosen:
            point_i = dataset.surface_points[view_i, y, x]
            normal_i = normals[view_i, y, x]
            query_dir = _reflected_direction(dataset.cameras[view_i].center, point_i, normal_i)
            indices, distances = topk_reflected_ray_candidates(
                query_point=point_i,
                query_direction=query_dir,
                candidate_points=candidate_points,
                candidate_directions=candidate_dirs,
                k=k,
                beta=beta,
            )
            weights = softmax_negative(distances, tau=tau)
            predicted_feature = np.sum(candidate_features[indices] * weights[:, None], axis=0)
            observed_feature = dataset.images[view_i, y, x]
            losses.append(float(np.mean((observed_feature - predicted_feature) ** 2)))

    if not losses:
        return CycleLossResult(mean_loss=float("inf"), valid_pairs=0)
    return CycleLossResult(mean_loss=float(np.mean(losses)), valid_pairs=len(losses))
