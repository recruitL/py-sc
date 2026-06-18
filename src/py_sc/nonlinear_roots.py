"""第八章示例中使用的标量非线性方程求根算法。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


ScalarFunction = Callable[[float], float]


@dataclass(frozen=True)
class ScalarRootResult:
    """标量方程求根结果。"""

    root: float
    iterations: int
    converged: bool
    residual: float
    history: np.ndarray


def find_sign_change_brackets(
    func: ScalarFunction,
    a: float,
    b: float,
    subintervals: int,
) -> list[tuple[float, float]]:
    """在区间上扫描变号子区间。"""

    a, b = _validate_interval(a, b)
    n = _validate_positive_int(subintervals, "subintervals")
    x = np.linspace(a, b, n + 1)
    values = np.array([_call_scalar(func, xi) for xi in x], dtype=float)
    brackets: list[tuple[float, float]] = []
    for i in range(n):
        f_left = values[i]
        f_right = values[i + 1]
        if f_left == 0:
            brackets.append((float(x[i]), float(x[i])))
        elif f_left * f_right < 0:
            brackets.append((float(x[i]), float(x[i + 1])))
    if values[-1] == 0:
        brackets.append((float(x[-1]), float(x[-1])))
    return brackets


def bisection_method(
    func: ScalarFunction,
    a: float,
    b: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100,
) -> ScalarRootResult:
    """二分法求解有变号括区间内的根。"""

    a, b = _validate_interval(a, b)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    fa = _call_scalar(func, a)
    fb = _call_scalar(func, b)
    if fa == 0:
        return ScalarRootResult(a, 0, True, 0.0, np.array([a], dtype=float))
    if fb == 0:
        return ScalarRootResult(b, 0, True, 0.0, np.array([b], dtype=float))
    if fa * fb > 0:
        raise ValueError("bisection requires a sign-changing interval")

    history = []
    left = a
    right = b
    f_left = fa
    converged = False
    root = 0.5 * (left + right)
    iterations = 0
    for k in range(1, max_iterations + 1):
        root = 0.5 * (left + right)
        f_mid = _call_scalar(func, root)
        history.append(root)
        iterations = k
        if abs(f_mid) <= tolerance or 0.5 * (right - left) <= tolerance:
            converged = True
            break
        if f_left * f_mid < 0:
            right = root
        else:
            left = root
            f_left = f_mid

    residual = abs(_call_scalar(func, root))
    return ScalarRootResult(
        root=float(root),
        iterations=iterations,
        converged=converged,
        residual=float(residual),
        history=np.array(history, dtype=float),
    )


def fixed_point_iteration(
    iteration_func: ScalarFunction,
    initial: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100,
    residual_func: ScalarFunction | None = None,
) -> ScalarRootResult:
    """用简单不动点迭代求解 ``x = iteration_func(x)``。"""

    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_old = float(initial)
    history = [x_old]
    converged = False
    iterations = 0

    for k in range(1, max_iterations + 1):
        x_new = _call_scalar(iteration_func, x_old)
        history.append(x_new)
        iterations = k
        step = abs(x_new - x_old)
        residual = _fixed_point_residual(iteration_func, residual_func, x_new)
        if step <= tolerance * max(1.0, abs(x_new)) or residual <= tolerance:
            converged = True
            x_old = x_new
            break
        x_old = x_new

    root = float(x_old)
    residual = _fixed_point_residual(iteration_func, residual_func, root)
    return ScalarRootResult(
        root=root,
        iterations=iterations,
        converged=converged,
        residual=float(residual),
        history=np.array(history, dtype=float),
    )


def aitken_delta_squared(
    sequence: np.ndarray | list[float] | tuple[float, ...],
    denominator_tolerance: float = 1e-14,
) -> np.ndarray:
    """对一维序列应用 Aitken ``delta^2`` 加速。"""

    denominator_tolerance = _validate_tolerance(denominator_tolerance)
    values = np.asarray(sequence, dtype=float)
    if values.ndim != 1:
        raise ValueError("sequence must be one-dimensional")
    if values.size < 3:
        raise ValueError("sequence must contain at least three values")
    first_delta = values[1:-1] - values[:-2]
    second_delta = values[2:] - 2.0 * values[1:-1] + values[:-2]
    accelerated = np.full(values.size - 2, np.nan, dtype=float)
    stable = np.abs(second_delta) > denominator_tolerance
    accelerated[stable] = values[:-2][stable] - first_delta[stable] ** 2 / second_delta[stable]
    return accelerated


def steffensen_method(
    iteration_func: ScalarFunction,
    initial: float,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    residual_func: ScalarFunction | None = None,
    denominator_tolerance: float = 1e-14,
) -> ScalarRootResult:
    """用 Steffensen 方法加速不动点迭代。"""

    tolerance = _validate_tolerance(tolerance)
    denominator_tolerance = _validate_tolerance(denominator_tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_old = float(initial)
    history = [x_old]
    converged = False
    iterations = 0

    for k in range(1, max_iterations + 1):
        x1 = _call_scalar(iteration_func, x_old)
        x2 = _call_scalar(iteration_func, x1)
        denominator = x2 - 2.0 * x1 + x_old
        if abs(denominator) <= denominator_tolerance:
            raise ValueError("Steffensen denominator is too small")
        x_new = x_old - (x1 - x_old) ** 2 / denominator
        history.append(x_new)
        iterations = k
        step = abs(x_new - x_old)
        residual = _fixed_point_residual(iteration_func, residual_func, x_new)
        if step <= tolerance * max(1.0, abs(x_new)) or residual <= tolerance:
            converged = True
            x_old = x_new
            break
        x_old = x_new

    root = float(x_old)
    residual = _fixed_point_residual(iteration_func, residual_func, root)
    return ScalarRootResult(
        root=root,
        iterations=iterations,
        converged=converged,
        residual=float(residual),
        history=np.array(history, dtype=float),
    )


def _validate_interval(a: float, b: float) -> tuple[float, float]:
    a = float(a)
    b = float(b)
    if not a < b:
        raise ValueError("expected a < b")
    return a, b


def _validate_tolerance(tolerance: float) -> float:
    tolerance = float(tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    return tolerance


def _validate_positive_int(value: int, name: str) -> int:
    value = int(value)
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


def _call_scalar(func: ScalarFunction, x: float) -> float:
    return float(np.asarray(func(float(x)), dtype=float))


def _fixed_point_residual(
    iteration_func: ScalarFunction,
    residual_func: ScalarFunction | None,
    x: float,
) -> float:
    if residual_func is None:
        return abs(_call_scalar(iteration_func, x) - x)
    return abs(_call_scalar(residual_func, x))
