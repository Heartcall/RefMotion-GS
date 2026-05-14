from __future__ import annotations

import numpy as np

from refmotion_gs_mvp.src.reflection_geometry import plucker_line, reflected_ray_distance
from refmotion_gs_mvp.src.reflection_geometry import normalize


def topk_reflected_ray_candidates(
    query_point: np.ndarray,
    query_direction: np.ndarray,
    candidate_points: np.ndarray,
    candidate_directions: np.ndarray,
    k: int = 8,
    beta: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    distances = reflected_ray_distances(query_point, query_direction, candidate_points, candidate_directions, beta)
    order = np.argsort(distances)[:k]
    return order, distances[order]


def reflected_ray_distances(
    query_point: np.ndarray,
    query_direction: np.ndarray,
    candidate_points: np.ndarray,
    candidate_directions: np.ndarray,
    beta: float = 0.0,
) -> np.ndarray:
    query_direction = normalize(query_direction)
    candidate_directions = normalize(candidate_directions)
    query_moment = np.cross(np.asarray(query_point, dtype=float), query_direction)
    candidate_moments = np.cross(np.asarray(candidate_points, dtype=float), candidate_directions)
    dir_term = np.sum((candidate_directions - query_direction) ** 2, axis=1)
    moment_term = np.sum((candidate_moments - query_moment) ** 2, axis=1)
    return dir_term + beta * moment_term


def softmax_negative(distances: np.ndarray, tau: float) -> np.ndarray:
    scaled = -np.asarray(distances, dtype=float) / tau
    scaled -= np.max(scaled)
    weights = np.exp(scaled)
    return weights / np.maximum(np.sum(weights), 1e-12)
