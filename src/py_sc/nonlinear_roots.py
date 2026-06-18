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
