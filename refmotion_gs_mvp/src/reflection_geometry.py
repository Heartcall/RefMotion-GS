from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def normalize(vectors: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    vectors = np.asarray(vectors, dtype=float)
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    return vectors / np.maximum(norms, eps)


def reflect(outgoing_to_camera: np.ndarray, normal: np.ndarray) -> np.ndarray:
    outgoing_to_camera = normalize(outgoing_to_camera)
    normal = normalize(normal)
    dot = np.sum(normal * outgoing_to_camera, axis=-1, keepdims=True)
    return normalize(2.0 * dot * normal - outgoing_to_camera)


@dataclass(frozen=True)
class PluckerLine:
    direction: np.ndarray
    moment: np.ndarray


def plucker_line(point: np.ndarray, direction: np.ndarray) -> PluckerLine:
    direction = normalize(direction)
    point = np.asarray(point, dtype=float)
    return PluckerLine(direction=direction, moment=np.cross(point, direction))


def reflected_ray_distance(line_a: PluckerLine, line_b: PluckerLine, beta: float = 0.1) -> float:
    dir_term = np.sum((line_a.direction - line_b.direction) ** 2)
    moment_term = np.sum((line_a.moment - line_b.moment) ** 2)
    return float(dir_term + beta * moment_term)


def rotate_vectors(vectors: np.ndarray, axis: np.ndarray, degrees: float) -> np.ndarray:
    vectors = np.asarray(vectors, dtype=float)
    axis = normalize(np.asarray(axis, dtype=float))
    theta = np.deg2rad(degrees)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return (
        vectors * cos_t
        + np.cross(axis, vectors) * sin_t
        + axis * np.sum(vectors * axis, axis=-1, keepdims=True) * (1.0 - cos_t)
    )


def angular_error_degrees(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = normalize(a)
    b = normalize(b)
    cos = np.clip(np.sum(a * b, axis=-1), -1.0, 1.0)
    return np.rad2deg(np.arccos(cos))

