from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from refmotion_gs_mvp.src.losses import reflection_cycle_loss
from refmotion_gs_mvp.src.reflection_geometry import normalize, rotate_vectors
from refmotion_gs_mvp.src.synthetic_scene import AnalyticDataset


@dataclass(frozen=True)
class NormalOptimizationResult:
    normals: np.ndarray
    loss_history: list[float]
    accepted_steps: list[tuple[str, float]]


def _rotate_object_normals(normals: np.ndarray, object_mask: np.ndarray, axis: np.ndarray, degrees: float) -> np.ndarray:
    updated = normals.copy()
    updated[object_mask] = normalize(rotate_vectors(updated[object_mask], axis=axis, degrees=degrees))
    return updated


def optimize_global_normal_rotation(
    dataset: AnalyticDataset,
    initial_normals: np.ndarray,
    iterations: int = 8,
    initial_step_degrees: float = 4.0,
    sample_count: int = 300,
    seed: int = 0,
) -> NormalOptimizationResult:
    axes = {
        "x": np.array([1.0, 0.0, 0.0], dtype=float),
        "y": np.array([0.0, 1.0, 0.0], dtype=float),
        "z": np.array([0.0, 0.0, 1.0], dtype=float),
    }
    current = normalize(initial_normals)
    current_loss = reflection_cycle_loss(dataset, current, sample_count=sample_count, seed=seed).mean_loss
    history = [current_loss]
    accepted: list[tuple[str, float]] = []
    step = float(initial_step_degrees)

    for _ in range(iterations):
        best_normals = current
        best_loss = current_loss
        best_step: tuple[str, float] | None = None
        for axis_name, axis in axes.items():
            for sign in (-1.0, 1.0):
                trial_step = sign * step
                trial = _rotate_object_normals(current, dataset.object_mask, axis=axis, degrees=trial_step)
                trial_loss = reflection_cycle_loss(dataset, trial, sample_count=sample_count, seed=seed).mean_loss
                if trial_loss < best_loss:
                    best_loss = trial_loss
                    best_normals = trial
                    best_step = (axis_name, trial_step)

        if best_step is None:
            step *= 0.5
        else:
            current = best_normals
            current_loss = best_loss
            accepted.append(best_step)
        history.append(current_loss)

    return NormalOptimizationResult(normals=current, loss_history=history, accepted_steps=accepted)

