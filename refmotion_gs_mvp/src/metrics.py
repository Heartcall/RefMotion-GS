from __future__ import annotations

import numpy as np

from refmotion_gs_mvp.src.reflection_geometry import angular_error_degrees


def normal_angular_error_degrees(pred: np.ndarray, gt: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    error = angular_error_degrees(pred, gt)
    if mask is None:
        return error
    return error[np.asarray(mask, dtype=bool)]


def albedo_rmse(pred: np.ndarray, gt: np.ndarray, mask: np.ndarray | None = None) -> float:
    pred = np.asarray(pred, dtype=float)
    gt = np.asarray(gt, dtype=float)
    residual = pred - gt
    if mask is not None:
        residual = residual[np.asarray(mask, dtype=bool)]
    return float(np.sqrt(np.mean(residual**2)))


def specular_leakage_score(
    baked_albedo: np.ndarray,
    gt_albedo: np.ndarray,
    reflected_color: np.ndarray,
    mask: np.ndarray,
    eps: float = 1e-12,
) -> float:
    residual = (np.asarray(baked_albedo, dtype=float) - np.asarray(gt_albedo, dtype=float))[mask]
    reflected_delta = (np.asarray(reflected_color, dtype=float) - np.asarray(gt_albedo, dtype=float))[mask]
    if residual.size == 0:
        return 0.0
    residual_norm = residual.reshape(-1, 3)
    reflected_norm = reflected_delta.reshape(-1, 3)
    numerator = np.sum(residual_norm * reflected_norm, axis=1)
    denom = np.linalg.norm(residual_norm, axis=1) * np.linalg.norm(reflected_norm, axis=1) + eps
    return float(np.mean(np.maximum(numerator / denom, 0.0)))
