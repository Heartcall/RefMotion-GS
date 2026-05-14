from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from refmotion_gs_mvp.src.cameras import Camera
from refmotion_gs_mvp.src.reflection_geometry import normalize, reflect


@dataclass(frozen=True)
class AnalyticDataset:
    images: np.ndarray
    normals: np.ndarray
    albedo: np.ndarray
    roughness: np.ndarray
    reflective_mask: np.ndarray
    object_mask: np.ndarray
    surface_points: np.ndarray
    reflected_color: np.ndarray
    cameras: list[Camera]


def _ray_sphere(origin: np.ndarray, direction: np.ndarray, radius: float = 1.0) -> tuple[bool, float]:
    b = 2.0 * float(np.dot(origin, direction))
    c = float(np.dot(origin, origin) - radius**2)
    disc = b * b - 4.0 * c
    if disc < 0.0:
        return False, np.inf
    root = np.sqrt(disc)
    t0 = (-b - root) / 2.0
    t1 = (-b + root) / 2.0
    t = t0 if t0 > 1e-6 else t1
    return bool(t > 1e-6), float(t)


def _environment_reflection_color(direction: np.ndarray) -> np.ndarray:
    direction = normalize(direction)
    color = np.array(
        [
            0.05 + 0.28 * max(float(direction[0]), 0.0),
            0.05 + 0.28 * max(float(direction[1]), 0.0),
            0.06 + 0.28 * max(float(direction[2]), 0.0),
        ],
        dtype=float,
    )
    lobes = [
        (np.array([1.0, 0.15, 0.1]), normalize(np.array([0.8, -0.2, 0.45])), 10.0),
        (np.array([0.1, 0.9, 0.25]), normalize(np.array([-0.65, 0.35, 0.55])), 9.0),
        (np.array([0.15, 0.25, 1.0]), normalize(np.array([0.1, 0.9, 0.35])), 10.0),
    ]
    for lobe_color, lobe_dir, sharpness in lobes:
        weight = max(float(np.dot(direction, lobe_dir)), 0.0) ** sharpness
        color += weight * lobe_color
    return np.clip(color, 0.0, 1.0)


def _make_camera(view_idx: int, num_views: int, width: int, height: int) -> Camera:
    angle = 2.0 * np.pi * view_idx / num_views
    center = np.array([3.0 * np.cos(angle), 0.35, 3.0 * np.sin(angle)], dtype=float)
    return Camera.look_at(
        center=center,
        target=np.array([0.0, 0.0, 0.0], dtype=float),
        up=np.array([0.0, 1.0, 0.0], dtype=float),
        focal=0.9 * min(width, height),
        width=width,
        height=height,
    )


def generate_analytic_dataset(
    num_views: int = 12,
    width: int = 64,
    height: int = 48,
    seed: int = 0,
) -> AnalyticDataset:
    rng = np.random.default_rng(seed)
    cameras = [_make_camera(i, num_views, width, height) for i in range(num_views)]
    images = np.zeros((num_views, height, width, 3), dtype=float)
    normals = np.zeros_like(images)
    albedo = np.zeros_like(images)
    roughness = np.ones((num_views, height, width), dtype=float)
    reflective_mask = np.zeros((num_views, height, width), dtype=bool)
    object_mask = np.zeros((num_views, height, width), dtype=bool)
    surface_points = np.full((num_views, height, width, 3), np.nan, dtype=float)
    reflected_color = np.zeros_like(images)

    base_albedo = np.array([0.12, 0.12, 0.11], dtype=float)
    light_dir = normalize(np.array([0.2, 0.8, 0.55], dtype=float))
    jitter = rng.normal(0.0, 0.003, size=images.shape)

    for view_idx, camera in enumerate(cameras):
        for y in range(height):
            for x in range(width):
                origin, direction = camera.pixel_ray(np.array([x + 0.5, y + 0.5], dtype=float))
                hit, t = _ray_sphere(origin, direction)
                if not hit:
                    images[view_idx, y, x] = np.array([0.015, 0.018, 0.022])
                    continue
                point = origin + t * direction
                normal = normalize(point)
                outgoing = normalize(camera.center - point)
                refl_dir = reflect(outgoing, normal)
                refl_color = _environment_reflection_color(refl_dir)
                diffuse = base_albedo * (0.22 + 0.55 * max(float(np.dot(normal, light_dir)), 0.0))
                is_reflective = normal[1] > -0.25
                specular_weight = 0.78 if is_reflective else 0.0
                color = (1.0 - specular_weight) * diffuse + specular_weight * refl_color

                images[view_idx, y, x] = np.clip(color + jitter[view_idx, y, x], 0.0, 1.0)
                normals[view_idx, y, x] = normal
                albedo[view_idx, y, x] = base_albedo
                roughness[view_idx, y, x] = 0.05 if is_reflective else 0.85
                reflective_mask[view_idx, y, x] = is_reflective
                object_mask[view_idx, y, x] = True
                surface_points[view_idx, y, x] = point
                reflected_color[view_idx, y, x] = refl_color

    return AnalyticDataset(
        images=images,
        normals=normals,
        albedo=albedo,
        roughness=roughness,
        reflective_mask=reflective_mask,
        object_mask=object_mask,
        surface_points=surface_points,
        reflected_color=reflected_color,
        cameras=cameras,
    )
