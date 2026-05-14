from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _normalize(vector: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    norm = np.linalg.norm(vector, axis=-1, keepdims=True)
    return vector / np.maximum(norm, eps)


@dataclass(frozen=True)
class Camera:
    center: np.ndarray
    right: np.ndarray
    up: np.ndarray
    forward: np.ndarray
    focal: float
    width: int
    height: int

    @classmethod
    def look_at(
        cls,
        center: np.ndarray,
        target: np.ndarray,
        up: np.ndarray,
        focal: float,
        width: int,
        height: int,
    ) -> "Camera":
        center = np.asarray(center, dtype=float)
        target = np.asarray(target, dtype=float)
        up = np.asarray(up, dtype=float)
        forward = _normalize(target - center)
        right = _normalize(np.cross(forward, up))
        true_up = _normalize(np.cross(right, forward))
        return cls(
            center=center,
            right=right,
            up=true_up,
            forward=forward,
            focal=float(focal),
            width=int(width),
            height=int(height),
        )

    @property
    def principal_point(self) -> np.ndarray:
        return np.array([self.width / 2.0, self.height / 2.0], dtype=float)

    def world_to_camera(self, point: np.ndarray) -> np.ndarray:
        point = np.asarray(point, dtype=float)
        rel = point - self.center
        return np.array(
            [
                np.dot(rel, self.right),
                np.dot(rel, self.up),
                np.dot(rel, self.forward),
            ],
            dtype=float,
        )

    def camera_to_world(self, point_cam: np.ndarray) -> np.ndarray:
        point_cam = np.asarray(point_cam, dtype=float)
        return (
            self.center
            + point_cam[0] * self.right
            + point_cam[1] * self.up
            + point_cam[2] * self.forward
        )

    def project(self, point: np.ndarray) -> tuple[np.ndarray, float]:
        cam = self.world_to_camera(point)
        if cam[2] <= 0:
            raise ValueError("Point projects behind the camera.")
        cx, cy = self.principal_point
        pixel = np.array(
            [
                self.focal * cam[0] / cam[2] + cx,
                cy - self.focal * cam[1] / cam[2],
            ],
            dtype=float,
        )
        return pixel, float(cam[2])

    def unproject(self, pixel: np.ndarray, depth: float) -> np.ndarray:
        pixel = np.asarray(pixel, dtype=float)
        cx, cy = self.principal_point
        x = (pixel[0] - cx) * depth / self.focal
        y = (cy - pixel[1]) * depth / self.focal
        return self.camera_to_world(np.array([x, y, depth], dtype=float))

    def pixel_ray(self, pixel: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        point = self.unproject(pixel, depth=1.0)
        direction = _normalize(point - self.center)
        return self.center.copy(), direction

