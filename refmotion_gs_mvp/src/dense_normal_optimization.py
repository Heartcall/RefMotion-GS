from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from refmotion_gs_mvp.src.losses import reflection_cycle_loss
from refmotion_gs_mvp.src.reflection_geometry import normalize, rotate_vectors
from refmotion_gs_mvp.src.synthetic_scene import AnalyticDataset
from refmotion_gs_mvp.src.uv_baking import sphere_points_to_uv


@dataclass(frozen=True)
class DenseNormalOptimizationResult:
    normals: np.ndarray
    normal_delta_uv: np.ndarray
    loss_history: list[float]
    accepted_updates: list[dict[str, float | int]]
    active_texels: int
    final_step: float
    uses_reflection_cycle_loss: bool


def make_initial_perturbed_normals(dataset: AnalyticDataset, degrees: float = 8.0) -> np.ndarray:
    """Rotate object normals around the x axis for the Milestone 3.2 diagnostic."""
    normals = dataset.normals.copy()
    normals[dataset.object_mask] = normalize(
        rotate_vectors(
            normals[dataset.object_mask],
            axis=np.array([1.0, 0.0, 0.0], dtype=float),
            degrees=degrees,
        )
    )
    return normals


def _uv_to_grid_indices(points: np.ndarray, uv_height: int, uv_width: int) -> tuple[np.ndarray, np.ndarray]:
    uv = sphere_points_to_uv(points)
    tex_x = np.clip((uv[..., 0] * uv_width).astype(int), 0, uv_width - 1)
    tex_y = np.clip((uv[..., 1] * uv_height).astype(int), 0, uv_height - 1)
    return tex_y, tex_x


def _tangent_frame(surface_points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    radial = normalize(surface_points)
    up = np.array([0.0, 1.0, 0.0], dtype=float)
    side = np.array([1.0, 0.0, 0.0], dtype=float)
    reference = np.broadcast_to(up, radial.shape).copy()
    near_pole = np.abs(np.sum(radial * up, axis=-1)) >= 0.95
    reference[near_pole] = side
    t1 = normalize(np.cross(reference, radial))
    t2 = normalize(np.cross(radial, t1))
    return t1, t2


def texel_observation_counts(
    dataset: AnalyticDataset,
    uv_height: int,
    uv_width: int,
    mask: np.ndarray | None = None,
) -> np.ndarray:
    """Count object observations per sphere-UV normal texel."""
    active_mask = dataset.object_mask if mask is None else (dataset.object_mask & mask)
    counts = np.zeros((uv_height, uv_width), dtype=int)
    if not np.any(active_mask):
        return counts
    tex_y, tex_x = _uv_to_grid_indices(dataset.surface_points[active_mask], uv_height, uv_width)
    np.add.at(counts, (tex_y, tex_x), 1)
    return counts


def compose_dense_normals(
    dataset: AnalyticDataset,
    initial_normals: np.ndarray,
    normal_delta_uv: np.ndarray,
) -> np.ndarray:
    """Compose per-pixel normals from a shared sphere-UV tangent delta grid."""
    delta = np.asarray(normal_delta_uv, dtype=float)
    if delta.ndim != 3 or delta.shape[-1] != 2:
        raise ValueError("normal_delta_uv must have shape (uv_height, uv_width, 2)")

    uv_height, uv_width = delta.shape[:2]
    normals = normalize(np.asarray(initial_normals, dtype=float)).copy()
    mask = dataset.object_mask
    if not np.any(mask):
        return normals

    points = dataset.surface_points[mask]
    tex_y, tex_x = _uv_to_grid_indices(points, uv_height, uv_width)
    t1, t2 = _tangent_frame(points)
    coeff = delta[tex_y, tex_x]
    composed = normals[mask] + coeff[:, 0, None] * t1 + coeff[:, 1, None] * t2
    normals[mask] = normalize(composed)
    return normals


def _regularization_terms(delta: np.ndarray, observed_counts: np.ndarray) -> tuple[float, float]:
    valid = observed_counts > 0
    if not np.any(valid):
        return 0.0, 0.0

    l2 = float(np.mean(np.sum(delta[valid] ** 2, axis=-1)))
    smooth_terms: list[float] = []
    height, width = valid.shape
    for y in range(height):
        for x in range(width):
            if not valid[y, x]:
                continue
            right = (x + 1) % width
            if valid[y, right]:
                smooth_terms.append(float(np.sum((delta[y, x] - delta[y, right]) ** 2)))
            if y + 1 < height and valid[y + 1, x]:
                smooth_terms.append(float(np.sum((delta[y, x] - delta[y + 1, x]) ** 2)))
    smooth = float(np.mean(smooth_terms)) if smooth_terms else 0.0
    return smooth, l2


def _rank_active_texels(
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


def _objective(
    dataset: AnalyticDataset,
    initial_normals: np.ndarray,
    delta: np.ndarray,
    observed_counts: np.ndarray,
    lambda_smooth: float,
    lambda_l2: float,
    sample_count: int,
    loss_seed: int,
    uses_reflection_cycle_loss: bool,
) -> tuple[float, np.ndarray]:
    normals = compose_dense_normals(dataset, initial_normals, delta)
    cycle = 0.0
    if uses_reflection_cycle_loss:
        cycle = reflection_cycle_loss(
            dataset,
            normals,
            sample_count=sample_count,
            seed=loss_seed,
        ).mean_loss
    smooth, l2 = _regularization_terms(delta, observed_counts)
    total = cycle + lambda_smooth * smooth + lambda_l2 * l2
    return float(total), normals


def _apply_trial_step(
    delta: np.ndarray,
    tex_y: int,
    tex_x: int,
    channel: int,
    step: float,
    update_radius: int,
) -> np.ndarray:
    trial = delta.copy()
    height, width = delta.shape[:2]
    radius = max(0, int(update_radius))
    for dy in range(-radius, radius + 1):
        yy = tex_y + dy
        if yy < 0 or yy >= height:
            continue
        for dx in range(-radius, radius + 1):
            xx = (tex_x + dx) % width
            trial[yy, xx, channel] = np.clip(
                trial[yy, xx, channel] + step,
                -0.35,
                0.35,
            )
    return trial


def optimize_dense_tangent_normals(
    dataset: AnalyticDataset,
    initial_normals: np.ndarray,
    uv_height: int = 16,
    uv_width: int = 32,
    iterations: int = 8,
    initial_step: float = 0.08,
    step_decay: float = 0.5,
    min_step: float = 0.01,
    max_active_texels: int = 64,
    lambda_smooth: float = 0.02,
    lambda_l2: float = 0.001,
    sample_count: int = 250,
    seed: int = 53,
    loss_seed: int = 59,
    uses_reflection_cycle_loss: bool = True,
    update_radius: int = 0,
) -> DenseNormalOptimizationResult:
    del seed
    delta = np.zeros((uv_height, uv_width, 2), dtype=float)
    observed_counts = texel_observation_counts(dataset, uv_height, uv_width)
    active_texels = _rank_active_texels(dataset, uv_height, uv_width, max_active_texels)

    current_loss, current_normals = _objective(
        dataset,
        initial_normals,
        delta,
        observed_counts,
        lambda_smooth,
        lambda_l2,
        sample_count,
        loss_seed,
        uses_reflection_cycle_loss,
    )
    loss_history = [current_loss]
    accepted_updates: list[dict[str, float | int]] = []
    step = float(initial_step)

    for iteration in range(iterations):
        best_loss = current_loss
        best_delta: np.ndarray | None = None
        best_update: dict[str, float | int] | None = None
        for tex_y, tex_x in active_texels:
            for channel in (0, 1):
                for sign in (-1.0, 1.0):
                    trial_delta = _apply_trial_step(
                        delta,
                        tex_y,
                        tex_x,
                        channel,
                        sign * step,
                        update_radius,
                    )
                    trial_loss, _ = _objective(
                        dataset,
                        initial_normals,
                        trial_delta,
                        observed_counts,
                        lambda_smooth,
                        lambda_l2,
                        sample_count,
                        loss_seed,
                        uses_reflection_cycle_loss,
                    )
                    if trial_loss < best_loss:
                        best_loss = trial_loss
                        best_delta = trial_delta
                        best_update = {
                            "iteration": int(iteration),
                            "texel_y": int(tex_y),
                            "texel_x": int(tex_x),
                            "channel": int(channel),
                            "step": float(sign * step),
                            "update_radius": int(update_radius),
                            "loss": float(trial_loss),
                        }

        if best_delta is None or best_update is None:
            step *= step_decay
        else:
            delta = best_delta
            current_loss = best_loss
            current_normals = compose_dense_normals(dataset, initial_normals, delta)
            accepted_updates.append(best_update)

        loss_history.append(float(current_loss))
        if step < min_step:
            break

    final_loss, final_normals = _objective(
        dataset,
        initial_normals,
        delta,
        observed_counts,
        lambda_smooth,
        lambda_l2,
        sample_count,
        loss_seed,
        uses_reflection_cycle_loss,
    )
    if final_loss != loss_history[-1]:
        loss_history[-1] = float(final_loss)

    return DenseNormalOptimizationResult(
        normals=final_normals,
        normal_delta_uv=delta,
        loss_history=loss_history,
        accepted_updates=accepted_updates,
        active_texels=len(active_texels),
        final_step=float(step),
        uses_reflection_cycle_loss=uses_reflection_cycle_loss,
    )


def run_dense_no_cycle_ablation(
    dataset: AnalyticDataset,
    initial_normals: np.ndarray,
    uv_height: int = 16,
    uv_width: int = 32,
    iterations: int = 8,
    initial_step: float = 0.08,
    step_decay: float = 0.5,
    min_step: float = 0.01,
    max_active_texels: int = 64,
    lambda_smooth: float = 0.02,
    lambda_l2: float = 0.001,
    seed: int = 53,
    update_radius: int = 0,
) -> DenseNormalOptimizationResult:
    return optimize_dense_tangent_normals(
        dataset,
        initial_normals,
        uv_height=uv_height,
        uv_width=uv_width,
        iterations=iterations,
        initial_step=initial_step,
        step_decay=step_decay,
        min_step=min_step,
        max_active_texels=max_active_texels,
        lambda_smooth=lambda_smooth,
        lambda_l2=lambda_l2,
        sample_count=1,
        seed=seed,
        loss_seed=0,
        uses_reflection_cycle_loss=False,
        update_radius=update_radius,
    )
