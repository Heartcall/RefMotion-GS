from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from refmotion_gs_mvp.src.dense_normal_optimization import (
    _apply_trial_step,
    compose_dense_normals,
    texel_observation_counts,
)
from refmotion_gs_mvp.src.metrics import normal_angular_error_degrees
from refmotion_gs_mvp.src.near_object_scene import NearObjectSceneResult
from refmotion_gs_mvp.src.synthetic_scene import AnalyticDataset
from refmotion_gs_mvp.src.uv_baking import sphere_points_to_uv


@dataclass(frozen=True)
class DenseTrajectoryDiagnostics:
    objective_history: list[float]
    reflective_error_history: list[float]
    nonreflective_error_history: list[float]
    reflective_improvement_history: list[float]
    objective_reflective_error_correlation: float | None
    accepted_update_count: int
    worsened_reflective_update_count: int


@dataclass(frozen=True)
class CoverageDiagnostics:
    reflector_hit_fraction: float
    active_texel_count: int
    active_texel_hit_fraction_mean: float
    active_texel_hit_fraction_min: float
    active_texels_without_finite_hits: int


def rank_reflective_active_texels(
    dataset: AnalyticDataset,
    uv_height: int,
    uv_width: int,
    max_active_texels: int,
) -> list[tuple[int, int]]:
    counts = texel_observation_counts(dataset, uv_height, uv_width, mask=dataset.reflective_mask)
    ranked = np.argwhere(counts > 0)
    if len(ranked) == 0:
        return []
    order = np.argsort(counts[ranked[:, 0], ranked[:, 1]])[::-1]
    selected = ranked[order[:max_active_texels]]
    return [(int(y), int(x)) for y, x in selected]


def _mean_normal_error(dataset: AnalyticDataset, normals: np.ndarray, mask: np.ndarray) -> float:
    errors = normal_angular_error_degrees(normals, dataset.normals, mask)
    return float(np.mean(errors))


def _objective_history_from_updates(
    accepted_updates: list[dict],
    accepted_state_count: int,
    objective_history: list[float] | None,
) -> list[float]:
    if objective_history is not None and len(objective_history) >= accepted_state_count:
        return [float(value) for value in objective_history[:accepted_state_count]]
    update_losses = [float(update["loss"]) for update in accepted_updates]
    if objective_history:
        initial = float(objective_history[0])
    else:
        initial = update_losses[0] if update_losses else 0.0
    return [initial, *update_losses[: max(0, accepted_state_count - 1)]]


def _safe_correlation(x_values: list[float], y_values: list[float]) -> float | None:
    x = np.asarray(x_values, dtype=float)
    y = np.asarray(y_values, dtype=float)
    finite = np.isfinite(x) & np.isfinite(y)
    if int(finite.sum()) < 3:
        return None
    x = x[finite]
    y = y[finite]
    if float(np.std(x)) == 0.0 or float(np.std(y)) == 0.0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def replay_dense_updates_for_diagnostics(
    dataset: AnalyticDataset,
    initial_normals: np.ndarray,
    accepted_updates: list[dict],
    uv_height: int,
    uv_width: int,
    objective_history: list[float] | None = None,
) -> DenseTrajectoryDiagnostics:
    delta = np.zeros((uv_height, uv_width, 2), dtype=float)
    reflective_mask = dataset.reflective_mask
    nonreflective_mask = dataset.object_mask & ~dataset.reflective_mask

    reflective_errors = [_mean_normal_error(dataset, initial_normals, reflective_mask)]
    nonreflective_errors = [_mean_normal_error(dataset, initial_normals, nonreflective_mask)]

    for update in accepted_updates:
        delta = _apply_trial_step(
            delta,
            tex_y=int(update["texel_y"]),
            tex_x=int(update["texel_x"]),
            channel=int(update["channel"]),
            step=float(update["step"]),
            update_radius=int(update.get("update_radius", 0)),
        )
        normals = compose_dense_normals(dataset, initial_normals, delta)
        reflective_errors.append(_mean_normal_error(dataset, normals, reflective_mask))
        nonreflective_errors.append(_mean_normal_error(dataset, normals, nonreflective_mask))

    init_reflective = reflective_errors[0]
    if init_reflective == 0.0:
        improvement_history = [0.0 for _ in reflective_errors]
    else:
        improvement_history = [
            float(100.0 * (init_reflective - error) / init_reflective)
            for error in reflective_errors
        ]

    worsened_count = sum(
        1
        for previous, current in zip(reflective_errors, reflective_errors[1:])
        if current > previous
    )
    objectives = _objective_history_from_updates(
        accepted_updates,
        accepted_state_count=len(reflective_errors),
        objective_history=objective_history,
    )
    return DenseTrajectoryDiagnostics(
        objective_history=objectives,
        reflective_error_history=reflective_errors,
        nonreflective_error_history=nonreflective_errors,
        reflective_improvement_history=improvement_history,
        objective_reflective_error_correlation=_safe_correlation(objectives, reflective_errors),
        accepted_update_count=len(accepted_updates),
        worsened_reflective_update_count=int(worsened_count),
    )


def _reflective_texel_indices(
    scene: NearObjectSceneResult,
    uv_height: int,
    uv_width: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    dataset = scene.dataset
    reflective = dataset.object_mask & dataset.reflective_mask
    points = dataset.surface_points[reflective]
    uv = sphere_points_to_uv(points)
    tex_x = np.clip((uv[..., 0] * uv_width).astype(int), 0, uv_width - 1)
    tex_y = np.clip((uv[..., 1] * uv_height).astype(int), 0, uv_height - 1)
    hit_mask = scene.reflector_hit_mask[reflective]
    return tex_y, tex_x, hit_mask


def active_texel_hit_fraction_map(
    scene: NearObjectSceneResult,
    uv_height: int,
    uv_width: int,
    active_texels: list[tuple[int, int]],
) -> np.ndarray:
    hit_fraction = np.full((uv_height, uv_width), np.nan, dtype=float)
    tex_y, tex_x, hit_mask = _reflective_texel_indices(scene, uv_height, uv_width)
    for y, x in active_texels:
        selected = (tex_y == int(y)) & (tex_x == int(x))
        if np.any(selected):
            hit_fraction[int(y), int(x)] = float(np.mean(hit_mask[selected]))
    return hit_fraction


def compute_reflector_hit_coverage_by_texel(
    scene: NearObjectSceneResult,
    uv_height: int,
    uv_width: int,
    active_texels: list[tuple[int, int]],
) -> CoverageDiagnostics:
    dataset = scene.dataset
    reflective = dataset.object_mask & dataset.reflective_mask
    reflector_hit_fraction = float(np.mean(scene.reflector_hit_mask[reflective]))
    hit_fraction_map = active_texel_hit_fraction_map(scene, uv_height, uv_width, active_texels)
    active_values = np.asarray(
        [
            hit_fraction_map[int(y), int(x)]
            for y, x in active_texels
            if np.isfinite(hit_fraction_map[int(y), int(x)])
        ],
        dtype=float,
    )
    if active_values.size == 0:
        mean_fraction = 0.0
        min_fraction = 0.0
        empty_count = len(active_texels)
    else:
        mean_fraction = float(np.mean(active_values))
        min_fraction = float(np.min(active_values))
        empty_count = int(np.sum(active_values == 0.0))

    return CoverageDiagnostics(
        reflector_hit_fraction=reflector_hit_fraction,
        active_texel_count=len(active_texels),
        active_texel_hit_fraction_mean=mean_fraction,
        active_texel_hit_fraction_min=min_fraction,
        active_texels_without_finite_hits=empty_count,
    )
