from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from refmotion_gs_mvp.src.cameras import Camera
from refmotion_gs_mvp.src.reflection_geometry import normalize, reflect
from refmotion_gs_mvp.src.synthetic_scene import AnalyticDataset, _environment_reflection_color


@dataclass(frozen=True)
class ReflectorPrimitive:
    center: np.ndarray
    radius: float
    color: np.ndarray


@dataclass(frozen=True)
class NearObjectSceneResult:
    dataset: AnalyticDataset
    reflector_hit_mask: np.ndarray
    reflector_id: np.ndarray
    train_view_indices: list[int]
    test_view_indices: list[int]
    reflectors: tuple[ReflectorPrimitive, ...]
    scope_flags: dict[str, bool] = field(
        default_factory=lambda: {
            "implements_learned_near_field_reflection_field": False,
            "implements_inter_reflection_residual": False,
            "implements_full_pbr_optimization": False,
            "claims_relighting_or_material_editing": False,
            "claims_representation_novelty": False,
        }
    )


def _default_reflectors() -> tuple[ReflectorPrimitive, ...]:
    return (
        ReflectorPrimitive(
            center=np.array([1.75, 0.10, 1.15], dtype=float),
            radius=0.765,
            color=np.array([0.95, 0.10, 0.08], dtype=float),
        ),
        ReflectorPrimitive(
            center=np.array([-1.55, 0.35, 1.35], dtype=float),
            radius=0.68,
            color=np.array([0.08, 0.85, 0.18], dtype=float),
        ),
        ReflectorPrimitive(
            center=np.array([0.15, 1.45, -1.55], dtype=float),
            radius=0.85,
            color=np.array([0.12, 0.22, 0.95], dtype=float),
        ),
    )


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


def _fallback_colors(reflected_dirs: np.ndarray, fallback_color: np.ndarray | None) -> np.ndarray:
    dirs = normalize(np.asarray(reflected_dirs, dtype=float))
    flat_dirs = dirs.reshape(-1, 3)
    if fallback_color is None:
        colors = np.asarray([_environment_reflection_color(direction) for direction in flat_dirs], dtype=float)
    else:
        fallback = np.asarray(fallback_color, dtype=float)
        colors = np.broadcast_to(fallback, dirs.shape).reshape(-1, 3).copy()
    return colors.reshape(dirs.shape)


def trace_reflector_color(
    surface_points: np.ndarray,
    reflected_dirs: np.ndarray,
    reflectors: tuple[ReflectorPrimitive, ...],
    fallback_color: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return `(colors, hit_mask, reflector_id)` for finite analytic reflector hits."""
    points = np.asarray(surface_points, dtype=float)
    dirs = normalize(np.asarray(reflected_dirs, dtype=float))
    if points.shape != dirs.shape or points.shape[-1] != 3:
        raise ValueError("surface_points and reflected_dirs must have matching shape (..., 3)")

    colors = _fallback_colors(dirs, fallback_color)
    hit_mask = np.zeros(points.shape[:-1], dtype=bool)
    reflector_id = np.full(points.shape[:-1], -1, dtype=int)
    best_t = np.full(points.shape[:-1], np.inf, dtype=float)

    for idx, reflector in enumerate(reflectors):
        center = np.asarray(reflector.center, dtype=float)
        radius = float(reflector.radius)
        oc = points - center
        b = 2.0 * np.sum(oc * dirs, axis=-1)
        c = np.sum(oc * oc, axis=-1) - radius**2
        disc = b * b - 4.0 * c
        valid_disc = disc >= 0.0
        sqrt_disc = np.zeros_like(disc)
        sqrt_disc[valid_disc] = np.sqrt(disc[valid_disc])
        t0 = (-b - sqrt_disc) / 2.0
        t1 = (-b + sqrt_disc) / 2.0
        t = np.where(t0 > 1e-6, t0, np.where(t1 > 1e-6, t1, np.inf))
        hit = valid_disc & (t < best_t) & np.isfinite(t)
        if np.any(hit):
            colors[hit] = np.asarray(reflector.color, dtype=float)
            hit_mask[hit] = True
            reflector_id[hit] = int(idx)
            best_t[hit] = t[hit]

    return colors, hit_mask, reflector_id


def _split_indices(num_views: int) -> tuple[list[int], list[int]]:
    if num_views >= 6:
        return list(range(4)), list(range(4, num_views))
    split = max(1, num_views - 1)
    return list(range(split)), list(range(split, num_views))


def generate_near_object_reflection_dataset(
    num_views: int = 6,
    width: int = 28,
    height: int = 24,
    seed: int = 173,
) -> NearObjectSceneResult:
    rng = np.random.default_rng(seed)
    reflectors = _default_reflectors()
    cameras = [_make_camera(i, num_views, width, height) for i in range(num_views)]

    images = np.zeros((num_views, height, width, 3), dtype=float)
    normals = np.zeros_like(images)
    albedo = np.zeros_like(images)
    roughness = np.ones((num_views, height, width), dtype=float)
    reflective_mask = np.zeros((num_views, height, width), dtype=bool)
    object_mask = np.zeros((num_views, height, width), dtype=bool)
    surface_points = np.full((num_views, height, width, 3), np.nan, dtype=float)
    reflected_color = np.zeros_like(images)
    reflector_hit_mask = np.zeros((num_views, height, width), dtype=bool)
    reflector_id = np.full((num_views, height, width), -1, dtype=int)

    base_albedo = np.array([0.11, 0.115, 0.105], dtype=float)
    light_dir = normalize(np.array([0.2, 0.8, 0.55], dtype=float))
    jitter = rng.normal(0.0, 0.002, size=images.shape)

    for view_idx, camera in enumerate(cameras):
        for y in range(height):
            for x in range(width):
                origin, direction = camera.pixel_ray(np.array([x + 0.5, y + 0.5], dtype=float))
                hit, t = _ray_sphere(origin, direction)
                if not hit:
                    images[view_idx, y, x] = np.array([0.012, 0.015, 0.019], dtype=float)
                    continue

                point = origin + t * direction
                normal = normalize(point)
                outgoing = normalize(camera.center - point)
                refl_dir = reflect(outgoing, normal)
                refl_color, refl_hit, refl_id = trace_reflector_color(
                    point[None, :],
                    refl_dir[None, :],
                    reflectors,
                )
                diffuse = base_albedo * (0.20 + 0.58 * max(float(np.dot(normal, light_dir)), 0.0))
                is_reflective = normal[1] > -0.25
                specular_weight = 0.82 if is_reflective else 0.0
                color = (1.0 - specular_weight) * diffuse + specular_weight * refl_color[0]

                images[view_idx, y, x] = np.clip(color + jitter[view_idx, y, x], 0.0, 1.0)
                normals[view_idx, y, x] = normal
                albedo[view_idx, y, x] = base_albedo
                roughness[view_idx, y, x] = 0.05 if is_reflective else 0.85
                reflective_mask[view_idx, y, x] = is_reflective
                object_mask[view_idx, y, x] = True
                surface_points[view_idx, y, x] = point
                reflected_color[view_idx, y, x] = refl_color[0]
                reflector_hit_mask[view_idx, y, x] = bool(refl_hit[0])
                reflector_id[view_idx, y, x] = int(refl_id[0])

    train_view_indices, test_view_indices = _split_indices(num_views)
    return NearObjectSceneResult(
        dataset=AnalyticDataset(
            images=images,
            normals=normals,
            albedo=albedo,
            roughness=roughness,
            reflective_mask=reflective_mask,
            object_mask=object_mask,
            surface_points=surface_points,
            reflected_color=reflected_color,
            cameras=cameras,
        ),
        reflector_hit_mask=reflector_hit_mask,
        reflector_id=reflector_id,
        train_view_indices=train_view_indices,
        test_view_indices=test_view_indices,
        reflectors=reflectors,
    )
