from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from refmotion_gs_mvp.src.feature_matching import softmax_negative, topk_reflected_ray_candidates
from refmotion_gs_mvp.src.reflection_geometry import normalize, reflect
from refmotion_gs_mvp.src.synthetic_scene import AnalyticDataset


@dataclass(frozen=True)
class PixelBakeResult:
    baked_albedo: np.ndarray
    route_to_texture: np.ndarray
    fill_color: np.ndarray


@dataclass(frozen=True)
class SphereUVBakeResult:
    texture: np.ndarray
    visibility_count: np.ndarray
    projected_albedo: np.ndarray
    route_to_texture: np.ndarray
    fill_color: np.ndarray


def sphere_points_to_uv(points: np.ndarray) -> np.ndarray:
    points = normalize(points)
    u = (np.arctan2(points[..., 2], points[..., 0]) / (2.0 * np.pi) + 1.0) % 1.0
    v = np.arccos(np.clip(points[..., 1], -1.0, 1.0)) / np.pi
    return np.stack([u, v], axis=-1)


def _uv_to_texel(uv: np.ndarray, resolution: int) -> tuple[np.ndarray, np.ndarray]:
    height = int(resolution)
    width = int(2 * resolution)
    x = np.clip((uv[..., 0] * width).astype(int), 0, width - 1)
    y = np.clip((uv[..., 1] * height).astype(int), 0, height - 1)
    return y, x


def make_noisy_reflective_mask(
    reflective_mask: np.ndarray,
    false_negative_rate: float = 0.25,
    false_positive_rate: float = 0.05,
    seed: int = 0,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    noisy = np.asarray(reflective_mask, dtype=bool).copy()
    false_negative = noisy & (rng.random(noisy.shape) < false_negative_rate)
    false_positive = (~noisy) & (rng.random(noisy.shape) < false_positive_rate)
    noisy[false_negative] = False
    noisy[false_positive] = True
    return noisy


def bake_pixels_with_routing(dataset: AnalyticDataset, route_to_texture: np.ndarray) -> PixelBakeResult:
    route_to_texture = np.asarray(route_to_texture, dtype=bool) & dataset.object_mask
    if np.any(route_to_texture):
        fill_color = np.mean(dataset.images[route_to_texture], axis=0)
    else:
        fill_color = np.array([0.0, 0.0, 0.0], dtype=float)
    baked = np.zeros_like(dataset.images)
    baked[dataset.object_mask] = fill_color
    baked[route_to_texture] = dataset.images[route_to_texture]
    return PixelBakeResult(baked_albedo=baked, route_to_texture=route_to_texture, fill_color=fill_color)


def bake_sphere_uv_texture(
    dataset: AnalyticDataset,
    route_to_texture: np.ndarray,
    resolution: int = 64,
) -> SphereUVBakeResult:
    route_to_texture = np.asarray(route_to_texture, dtype=bool) & dataset.object_mask
    height = int(resolution)
    width = int(2 * resolution)
    texture_sum = np.zeros((height, width, 3), dtype=float)
    count = np.zeros((height, width), dtype=int)

    if np.any(route_to_texture):
        fill_color = np.mean(dataset.images[route_to_texture], axis=0)
        routed_points = dataset.surface_points[route_to_texture]
        routed_uv = sphere_points_to_uv(routed_points)
        tex_y, tex_x = _uv_to_texel(routed_uv, resolution)
        routed_colors = dataset.images[route_to_texture]
        np.add.at(texture_sum, (tex_y, tex_x), routed_colors)
        np.add.at(count, (tex_y, tex_x), 1)
    else:
        fill_color = np.array([0.0, 0.0, 0.0], dtype=float)

    texture = np.zeros_like(texture_sum)
    filled = count > 0
    texture[filled] = texture_sum[filled] / count[filled, None]
    texture[~filled] = fill_color

    projected = np.zeros_like(dataset.images)
    object_points = dataset.surface_points[dataset.object_mask]
    object_uv = sphere_points_to_uv(object_points)
    obj_y, obj_x = _uv_to_texel(object_uv, resolution)
    projected[dataset.object_mask] = texture[obj_y, obj_x]
    return SphereUVBakeResult(
        texture=texture,
        visibility_count=count,
        projected_albedo=projected,
        route_to_texture=route_to_texture,
        fill_color=fill_color,
    )


def _view_reflected_directions(dataset: AnalyticDataset, normals: np.ndarray, view_idx: int, mask: np.ndarray) -> np.ndarray:
    points = dataset.surface_points[view_idx][mask]
    outgoing = normalize(dataset.cameras[view_idx].center - points)
    return reflect(outgoing, normals[view_idx][mask])


def reflection_confidence_mask(
    dataset: AnalyticDataset,
    normals: np.ndarray,
    k: int = 5,
    tau: float = 0.03,
    beta: float = 0.0,
    max_feature_mse: float = 0.008,
    max_distance: float = 0.04,
    seed: int = 0,
) -> np.ndarray:
    del seed
    confidence = np.zeros(dataset.object_mask.shape, dtype=bool)
    num_views = dataset.images.shape[0]
    for view_i in range(num_views):
        view_j = (view_i + 1) % num_views
        mask_i = dataset.object_mask[view_i]
        mask_j = dataset.object_mask[view_j]
        pixels_i = np.argwhere(mask_i)
        candidate_points = dataset.surface_points[view_j][mask_j]
        candidate_dirs = _view_reflected_directions(dataset, normals, view_j, mask_j)
        candidate_features = dataset.images[view_j][mask_j]
        for y, x in pixels_i:
            point_i = dataset.surface_points[view_i, y, x]
            outgoing = normalize(dataset.cameras[view_i].center - point_i)
            query_dir = reflect(outgoing, normals[view_i, y, x])
            indices, distances = topk_reflected_ray_candidates(
                point_i,
                query_dir,
                candidate_points,
                candidate_dirs,
                k=k,
                beta=beta,
            )
            weights = softmax_negative(distances, tau=tau)
            predicted = np.sum(candidate_features[indices] * weights[:, None], axis=0)
            feature_mse = float(np.mean((dataset.images[view_i, y, x] - predicted) ** 2))
            if feature_mse < max_feature_mse and distances[0] < max_distance:
                confidence[view_i, y, x] = True
    return confidence
