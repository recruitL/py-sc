"""第十二章示例中使用的偏微分方程有限差分算法。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


Source1D = Callable[[float, np.ndarray], np.ndarray]


@dataclass(frozen=True)
class Advection1DResult:
    """一维对流方程数值结果。"""

    grid: np.ndarray
    times: np.ndarray
    values: np.ndarray
    method: str
    courant: float


@dataclass(frozen=True)
class Advection2DResult:
    """二维对流方程数值结果。"""

    x_grid: np.ndarray
    y_grid: np.ndarray
    times: np.ndarray
    values: np.ndarray
    method: str
    courant_x: float
    courant_y: float


@dataclass(frozen=True)
class Wave1DResult:
    """一维波动方程数值结果。"""

    grid: np.ndarray
    times: np.ndarray
    values: np.ndarray
    courant: float
    energy_history: np.ndarray


def periodic_grid_1d(start: float, stop: float, points: int) -> np.ndarray:
    """生成不重复终点的一维周期网格。"""

    points = _validate_positive_int(points, "points")
    if not stop > start:
        raise ValueError("stop must be greater than start")
    return np.linspace(float(start), float(stop), points, endpoint=False)


def advection_cfl(velocity: float, dt: float, dx: float) -> float:
    """计算一维对流方程的 Courant 数。"""

    return float(velocity) * _validate_step_size(dt, "dt") / _validate_step_size(dx, "dx")


def upwind_advection_1d(
    initial: np.ndarray | list[float] | tuple[float, ...],
    velocity: float,
    dx: float,
    dt: float,
    steps: int,
) -> Advection1DResult:
    """周期边界一维常系数对流方程的上风格式。"""

    u = _as_vector(initial, "initial")
    dx = _validate_step_size(dx, "dx")
    dt = _validate_step_size(dt, "dt")
    steps = _validate_nonnegative_int(steps, "steps")
    courant = advection_cfl(velocity, dt, dx)
    values = [u.copy()]
    for _ in range(steps):
        if velocity >= 0.0:
            u = u - courant * (u - np.roll(u, 1))
        else:
            u = u - courant * (np.roll(u, -1) - u)
        values.append(u.copy())
    grid = np.arange(u.size, dtype=float) * dx
    times = np.arange(steps + 1, dtype=float) * dt
    return Advection1DResult(grid, times, np.vstack(values), "upwind", float(courant))


def lax_friedrichs_advection_1d(
    initial: np.ndarray | list[float] | tuple[float, ...],
    velocity: float,
    dx: float,
    dt: float,
    steps: int,
) -> Advection1DResult:
    """周期边界一维常系数对流方程的 Lax-Friedrichs 格式。"""

    u = _as_vector(initial, "initial")
    dx = _validate_step_size(dx, "dx")
    dt = _validate_step_size(dt, "dt")
    steps = _validate_nonnegative_int(steps, "steps")
    courant = advection_cfl(velocity, dt, dx)
    values = [u.copy()]
    for _ in range(steps):
        u = 0.5 * (np.roll(u, -1) + np.roll(u, 1)) - 0.5 * courant * (np.roll(u, -1) - np.roll(u, 1))
        values.append(u.copy())
    grid = np.arange(u.size, dtype=float) * dx
    times = np.arange(steps + 1, dtype=float) * dt
    return Advection1DResult(grid, times, np.vstack(values), "lax_friedrichs", float(courant))


def lax_wendroff_advection_1d(
    initial: np.ndarray | list[float] | tuple[float, ...],
    velocity: float,
    dx: float,
    dt: float,
    steps: int,
) -> Advection1DResult:
    """周期边界一维常系数对流方程的 Lax-Wendroff 格式。"""

    u = _as_vector(initial, "initial")
    dx = _validate_step_size(dx, "dx")
    dt = _validate_step_size(dt, "dt")
    steps = _validate_nonnegative_int(steps, "steps")
    courant = advection_cfl(velocity, dt, dx)
    values = [u.copy()]
    for _ in range(steps):
        u = (
            u
            - 0.5 * courant * (np.roll(u, -1) - np.roll(u, 1))
            + 0.5 * courant * courant * (np.roll(u, -1) - 2.0 * u + np.roll(u, 1))
        )
        values.append(u.copy())
    grid = np.arange(u.size, dtype=float) * dx
    times = np.arange(steps + 1, dtype=float) * dt
    return Advection1DResult(grid, times, np.vstack(values), "lax_wendroff", float(courant))


def upwind_advection_2d(
    initial: np.ndarray | list[list[float]],
    velocity_x: float,
    velocity_y: float,
    dx: float,
    dy: float,
    dt: float,
    steps: int,
) -> Advection2DResult:
    """周期边界二维常系数对流方程的直接上风格式。"""

    u = _as_matrix(initial, "initial")
    dx = _validate_step_size(dx, "dx")
    dy = _validate_step_size(dy, "dy")
    dt = _validate_step_size(dt, "dt")
    steps = _validate_nonnegative_int(steps, "steps")
    cx = float(velocity_x) * dt / dx
    cy = float(velocity_y) * dt / dy
    values = [u.copy()]
    for _ in range(steps):
        if velocity_x >= 0.0:
            x_diff = u - np.roll(u, 1, axis=0)
        else:
            x_diff = np.roll(u, -1, axis=0) - u
        if velocity_y >= 0.0:
            y_diff = u - np.roll(u, 1, axis=1)
        else:
            y_diff = np.roll(u, -1, axis=1) - u
        u = u - cx * x_diff - cy * y_diff
        values.append(u.copy())
    x_grid = np.arange(u.shape[0], dtype=float) * dx
    y_grid = np.arange(u.shape[1], dtype=float) * dy
    times = np.arange(steps + 1, dtype=float) * dt
    return Advection2DResult(x_grid, y_grid, times, np.stack(values), "upwind_2d", float(cx), float(cy))


def wave_cfl(speed: float, dt: float, dx: float) -> float:
    """计算一维波动方程的 Courant 数。"""

    return float(speed) * _validate_step_size(dt, "dt") / _validate_step_size(dx, "dx")


def solve_wave_1d_dirichlet(
    initial_displacement: np.ndarray | list[float] | tuple[float, ...],
    initial_velocity: np.ndarray | list[float] | tuple[float, ...],
    speed: float,
    dx: float,
    dt: float,
    steps: int,
    source: Source1D | None = None,
) -> Wave1DResult:
    """用中心差分求解一维波动方程，端点为齐次 Dirichlet 边界。"""

    u0 = _as_vector(initial_displacement, "initial_displacement")
    v0 = _as_vector(initial_velocity, "initial_velocity")
    if u0.size != v0.size:
        raise ValueError("initial displacement and velocity must have the same size")
    if u0.size < 3:
        raise ValueError("at least three grid points are required")
    dx = _validate_step_size(dx, "dx")
    dt = _validate_step_size(dt, "dt")
    steps = _validate_nonnegative_int(steps, "steps")
    courant = wave_cfl(speed, dt, dx)
    r2 = courant * courant
    grid = np.arange(u0.size, dtype=float) * dx
    times = np.arange(steps + 1, dtype=float) * dt
    values = [u0.copy()]
    if steps == 0:
        return Wave1DResult(grid, times, np.vstack(values), float(courant), np.array([wave_discrete_energy(u0, v0, speed, dx)]))

    u_prev = u0.copy()
    u_prev[0] = 0.0
    u_prev[-1] = 0.0
    source0 = _source_values(source, 0.0, grid, u0.size)
    u_curr = u_prev.copy()
    u_curr[1:-1] = (
        u_prev[1:-1]
        + dt * v0[1:-1]
        + 0.5 * r2 * (u_prev[2:] - 2.0 * u_prev[1:-1] + u_prev[:-2])
        + 0.5 * dt * dt * source0[1:-1]
    )
    u_curr[0] = 0.0
    u_curr[-1] = 0.0
    values.append(u_curr.copy())
    energies = [wave_discrete_energy(u_prev, v0, speed, dx), wave_discrete_energy(u_curr, (u_curr - u_prev) / dt, speed, dx)]

    for step in range(1, steps):
        time = step * dt
        forcing = _source_values(source, time, grid, u0.size)
        u_next = u_curr.copy()
        u_next[1:-1] = (
            2.0 * u_curr[1:-1]
            - u_prev[1:-1]
            + r2 * (u_curr[2:] - 2.0 * u_curr[1:-1] + u_curr[:-2])
            + dt * dt * forcing[1:-1]
        )
        u_next[0] = 0.0
        u_next[-1] = 0.0
        values.append(u_next.copy())
        energies.append(wave_discrete_energy(u_next, (u_next - u_prev) / (2.0 * dt), speed, dx))
        u_prev, u_curr = u_curr, u_next

    return Wave1DResult(grid, times, np.vstack(values), float(courant), np.array(energies, dtype=float))


def wave_discrete_energy(
    displacement: np.ndarray | list[float] | tuple[float, ...],
    velocity: np.ndarray | list[float] | tuple[float, ...],
    speed: float,
    dx: float,
) -> float:
    """计算一维波动方程的离散能量近似。"""

    u = _as_vector(displacement, "displacement")
    v = _as_vector(velocity, "velocity")
    if u.size != v.size:
        raise ValueError("displacement and velocity must have the same size")
    dx = _validate_step_size(dx, "dx")
    gradient = np.diff(u) / dx
    kinetic = 0.5 * dx * float(np.sum(v * v))
    potential = 0.5 * float(speed) ** 2 * dx * float(np.sum(gradient * gradient))
    return kinetic + potential


def _as_vector(values: np.ndarray | list[float] | tuple[float, ...], name: str) -> np.ndarray:
    array = np.array(values, dtype=float)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    return array


def _as_matrix(values: np.ndarray | list[list[float]], name: str) -> np.ndarray:
    array = np.array(values, dtype=float)
    if array.ndim != 2:
        raise ValueError(f"{name} must be two-dimensional")
    return array


def _validate_step_size(value: float, name: str) -> float:
    value = float(value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def _validate_positive_int(value: int, name: str) -> int:
    value = int(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _validate_nonnegative_int(value: int, name: str) -> int:
    value = int(value)
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _source_values(source: Source1D | None, time: float, grid: np.ndarray, size: int) -> np.ndarray:
    if source is None:
        return np.zeros(size, dtype=float)
    values = _as_vector(source(float(time), grid), "source values")
    if values.size != size:
        raise ValueError("source values must match grid size")
    return values
