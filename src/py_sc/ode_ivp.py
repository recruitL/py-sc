"""第十一章示例中使用的常微分方程初值问题算法。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


RHSFunction = Callable[[float, np.ndarray], np.ndarray]
StepFunction = Callable[[RHSFunction, float, np.ndarray, float], np.ndarray]
ExactSolution = Callable[[float], np.ndarray | list[float] | tuple[float, ...] | float]


@dataclass(frozen=True)
class ODEResult:
    """固定步长初值问题求解结果。"""

    times: np.ndarray
    values: np.ndarray
    method: str
    step_size: float


def euler_step(rhs: RHSFunction, time: float, state: np.ndarray | list[float] | tuple[float, ...] | float, step_size: float) -> np.ndarray:
    """显式 Euler 单步。"""

    y = _as_state(state)
    h = _validate_step_size(step_size)
    f0 = _as_rhs_value(rhs(float(time), y), y.size)
    return y + h * f0


def heun_step(rhs: RHSFunction, time: float, state: np.ndarray | list[float] | tuple[float, ...] | float, step_size: float) -> np.ndarray:
    """改进 Euler/Heun 单步。"""

    y = _as_state(state)
    h = _validate_step_size(step_size)
    f0 = _as_rhs_value(rhs(float(time), y), y.size)
    predictor = y + h * f0
    f1 = _as_rhs_value(rhs(float(time) + h, predictor), y.size)
    return y + 0.5 * h * (f0 + f1)


def midpoint_step(rhs: RHSFunction, time: float, state: np.ndarray | list[float] | tuple[float, ...] | float, step_size: float) -> np.ndarray:
    """显式中点法单步。"""

    y = _as_state(state)
    h = _validate_step_size(step_size)
    f0 = _as_rhs_value(rhs(float(time), y), y.size)
    midpoint = y + 0.5 * h * f0
    f_mid = _as_rhs_value(rhs(float(time) + 0.5 * h, midpoint), y.size)
    return y + h * f_mid


def rk4_step(rhs: RHSFunction, time: float, state: np.ndarray | list[float] | tuple[float, ...] | float, step_size: float) -> np.ndarray:
    """经典四阶 Runge-Kutta 单步。"""

    y = _as_state(state)
    h = _validate_step_size(step_size)
    t = float(time)
    k1 = _as_rhs_value(rhs(t, y), y.size)
    k2 = _as_rhs_value(rhs(t + 0.5 * h, y + 0.5 * h * k1), y.size)
    k3 = _as_rhs_value(rhs(t + 0.5 * h, y + 0.5 * h * k2), y.size)
    k4 = _as_rhs_value(rhs(t + h, y + h * k3), y.size)
    return y + h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0


def solve_ivp_fixed_step(
    rhs: RHSFunction,
    t_span: tuple[float, float],
    initial: np.ndarray | list[float] | tuple[float, ...] | float,
    step_size: float,
    method: str | StepFunction = "rk4",
) -> ODEResult:
    """用固定步长显式方法求解初值问题 ``y'=f(t,y)``。"""

    t0, t_end = _validate_time_span(t_span)
    h = _validate_step_size(step_size)
    y = _as_state(initial)
    stepper, method_name = _resolve_step_method(method)
    times = [t0]
    values = [y.copy()]
    time = t0

    while time < t_end - 10.0 * np.finfo(float).eps * max(1.0, abs(t_end)):
        actual_step = min(h, t_end - time)
        y = stepper(rhs, time, y, actual_step)
        time = min(t_end, time + actual_step)
        times.append(time)
        values.append(y.copy())

    return ODEResult(
        times=np.array(times, dtype=float),
        values=np.vstack(values),
        method=method_name,
        step_size=h,
    )


def global_error(
    times: np.ndarray | list[float] | tuple[float, ...],
    values: np.ndarray | list[list[float]],
    exact_solution: ExactSolution,
    norm_ord: int | float = 2,
) -> np.ndarray:
    """计算每个网格点的全局误差范数。"""

    t = np.array(times, dtype=float)
    y = np.array(values, dtype=float)
    if t.ndim != 1:
        raise ValueError("times must be one-dimensional")
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    if y.ndim != 2 or y.shape[0] != t.size:
        raise ValueError("values must have one row per time point")
    errors = []
    for time, value in zip(t, y, strict=True):
        exact = _as_state(exact_solution(float(time)))
        if exact.size != y.shape[1]:
            raise ValueError("exact solution dimension must match values")
        errors.append(float(np.linalg.norm(value - exact, ord=norm_ord)))
    return np.array(errors, dtype=float)


def estimate_convergence_order(
    step_sizes: np.ndarray | list[float] | tuple[float, ...],
    errors: np.ndarray | list[float] | tuple[float, ...],
) -> float:
    """用 ``log(error)`` 对 ``log(step_size)`` 的斜率估计收敛阶。"""

    h = np.array(step_sizes, dtype=float)
    err = np.array(errors, dtype=float)
    if h.ndim != 1 or err.ndim != 1 or h.size != err.size:
        raise ValueError("step_sizes and errors must be one-dimensional arrays of the same length")
    if h.size < 2:
        raise ValueError("at least two data points are required")
    if np.any(h <= 0.0) or np.any(err <= 0.0):
        raise ValueError("step sizes and errors must be positive")
    slope, _ = np.polyfit(np.log(h), np.log(err), deg=1)
    return float(slope)


def _as_state(state: np.ndarray | list[float] | tuple[float, ...] | float) -> np.ndarray:
    y = np.array(state, dtype=float)
    if y.ndim == 0:
        y = y.reshape(1)
    if y.ndim != 1:
        raise ValueError("state must be scalar or one-dimensional")
    return y


def _as_rhs_value(value: np.ndarray | list[float] | tuple[float, ...] | float, size: int) -> np.ndarray:
    f = _as_state(value)
    if f.size != size:
        raise ValueError("right-hand side dimension must match state")
    return f


def _validate_step_size(step_size: float) -> float:
    h = float(step_size)
    if h <= 0.0:
        raise ValueError("step_size must be positive")
    return h


def _validate_time_span(t_span: tuple[float, float]) -> tuple[float, float]:
    if len(t_span) != 2:
        raise ValueError("t_span must contain exactly two values")
    t0, t_end = float(t_span[0]), float(t_span[1])
    if not t_end > t0:
        raise ValueError("t_span must satisfy t_end > t0")
    return t0, t_end


def _resolve_step_method(method: str | StepFunction) -> tuple[StepFunction, str]:
    methods: dict[str, StepFunction] = {
        "euler": euler_step,
        "heun": heun_step,
        "midpoint": midpoint_step,
        "rk4": rk4_step,
    }
    if callable(method):
        return method, getattr(method, "__name__", "custom")
    key = str(method).lower()
    if key not in methods:
        raise ValueError(f"unknown method: {method}")
    return methods[key], key
