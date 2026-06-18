"""第四章示例中使用的数值积分算法。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.polynomial import hermite as H
from numpy.polynomial import laguerre as La

from .interpolation import NaturalCubicSpline


ArrayFunc = Callable[[np.ndarray], np.ndarray]
ScalarFunc = Callable[[float], float]


@dataclass(frozen=True)
class RombergResult:
    """Romberg 求积的结果和外推表。"""

    value: float
    table: np.ndarray
    iterations: int
    converged: bool


@dataclass(frozen=True)
class AdaptiveSimpsonResult:
    """自适应 Simpson 求积的结果和接受区间信息。"""

    value: float
    error_estimate: float
    intervals: np.ndarray
    local_errors: np.ndarray
    depths: np.ndarray
    evaluations: int
    converged: bool


@dataclass(frozen=True)
class MonteCarloResult:
    """Monte Carlo 积分估计结果。"""

    value: float
    standard_error: float
    sample_count: int
    sample_mean: float
    sample_variance: float


def midpoint_rule(func: ScalarFunc, a: float, b: float) -> float:
    """单区间中点公式。"""

    a, b = _validate_interval(a, b)
    return (b - a) * _call_scalar(func, 0.5 * (a + b))


def trapezoid_rule(func: ScalarFunc, a: float, b: float) -> float:
    """单区间梯形公式。"""

    a, b = _validate_interval(a, b)
    return 0.5 * (b - a) * (_call_scalar(func, a) + _call_scalar(func, b))


def simpson_rule(func: ScalarFunc, a: float, b: float) -> float:
    """单区间 Simpson 公式。"""

    a, b = _validate_interval(a, b)
    mid = 0.5 * (a + b)
    return (b - a) * (
        _call_scalar(func, a) + 4.0 * _call_scalar(func, mid) + _call_scalar(func, b)
    ) / 6.0


def simpson_three_eighths_rule(func: ScalarFunc, a: float, b: float) -> float:
    """单区间 Simpson 3/8 公式。"""

    a, b = _validate_interval(a, b)
    h = (b - a) / 3.0
    x0 = a
    x1 = a + h
    x2 = a + 2.0 * h
    x3 = b
    return 3.0 * h * (
        _call_scalar(func, x0)
        + 3.0 * _call_scalar(func, x1)
        + 3.0 * _call_scalar(func, x2)
        + _call_scalar(func, x3)
    ) / 8.0


def closed_newton_cotes_weights(order: int) -> tuple[np.ndarray, np.ndarray]:
    """返回标准区间 [0, 1] 上闭型 Newton-Cotes 节点和权重。

    ``order`` 表示插值多项式次数，因此会有 ``order + 1`` 个节点。
    """

    if order < 0:
        raise ValueError("order must be non-negative")
    nodes = np.linspace(0.0, 1.0, order + 1)
    weights = _interpolatory_weights(nodes, 0.0, 1.0)
    return nodes, weights


def open_newton_cotes_weights(node_count: int) -> tuple[np.ndarray, np.ndarray]:
    """返回标准区间 [0, 1] 上开型 Newton-Cotes 节点和权重。"""

    if node_count < 1:
        raise ValueError("node_count must be at least 1")
    nodes = np.arange(1, node_count + 1, dtype=float) / (node_count + 1.0)
    weights = _interpolatory_weights(nodes, 0.0, 1.0)
    return nodes, weights


def newton_cotes_integrate(
    func: ScalarFunc,
    a: float,
    b: float,
    nodes: np.ndarray,
    weights: np.ndarray,
) -> float:
    """用给定标准节点和权重在 [a, b] 上积分。"""

    a, b = _validate_interval(a, b)
    nodes = np.asarray(nodes, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if nodes.ndim != 1 or weights.ndim != 1 or nodes.size != weights.size:
        raise ValueError("nodes and weights must be one-dimensional arrays of the same length")

    x = a + (b - a) * nodes
    values = np.array([_call_scalar(func, xi) for xi in x], dtype=float)
    return float((b - a) * np.dot(weights, values))


def composite_midpoint(func: ArrayFunc, a: float, b: float, subintervals: int) -> float:
    """复合中点公式。"""

    a, b = _validate_interval(a, b)
    n = _validate_positive_int(subintervals, "subintervals")
    h = (b - a) / n
    nodes = a + (np.arange(n, dtype=float) + 0.5) * h
    return float(h * np.sum(_evaluate_array(func, nodes)))


def composite_trapezoid(func: ArrayFunc, a: float, b: float, subintervals: int) -> float:
    """复合梯形公式。"""

    a, b = _validate_interval(a, b)
    n = _validate_positive_int(subintervals, "subintervals")
    x = np.linspace(a, b, n + 1)
    y = _evaluate_array(func, x)
    return float((b - a) / n * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1]))


def composite_simpson(func: ArrayFunc, a: float, b: float, subintervals: int) -> float:
    """复合 Simpson 公式，``subintervals`` 必须为偶数。"""

    a, b = _validate_interval(a, b)
    n = _validate_positive_int(subintervals, "subintervals")
    if n % 2 != 0:
        raise ValueError("subintervals must be even for composite Simpson rule")
    x = np.linspace(a, b, n + 1)
    y = _evaluate_array(func, x)
    h = (b - a) / n
    return float(h / 3.0 * (y[0] + y[-1] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-1:2])))


def romberg_integrate(
    func: ScalarFunc,
    a: float,
    b: float,
    max_order: int = 8,
    tolerance: float | None = None,
) -> RombergResult:
    """用梯形递推和 Richardson 外推构造 Romberg 求积表。"""

    a, b = _validate_interval(a, b)
    if max_order < 1:
        raise ValueError("max_order must be at least 1")
    if tolerance is not None and tolerance <= 0:
        raise ValueError("tolerance must be positive")

    table = np.full((max_order, max_order), np.nan, dtype=float)
    table[0, 0] = trapezoid_rule(func, a, b)
    converged = False
    iterations = 1

    for k in range(1, max_order):
        panel_count = 2**k
        h = (b - a) / panel_count
        new_nodes = a + (np.arange(1, panel_count, 2, dtype=float) * h)
        new_values = np.array([_call_scalar(func, x) for x in new_nodes], dtype=float)
        table[k, 0] = 0.5 * table[k - 1, 0] + h * np.sum(new_values)

        for j in range(1, k + 1):
            factor = 4**j
            table[k, j] = table[k, j - 1] + (table[k, j - 1] - table[k - 1, j - 1]) / (factor - 1)

        iterations = k + 1
        if tolerance is not None and abs(table[k, k] - table[k - 1, k - 1]) <= tolerance:
            converged = True
            break

    value = float(table[iterations - 1, iterations - 1])
    return RombergResult(value=value, table=table[:iterations, :iterations], iterations=iterations, converged=converged)


def adaptive_simpson(
    func: ScalarFunc,
    a: float,
    b: float,
    tolerance: float = 1e-8,
    max_depth: int = 20,
) -> AdaptiveSimpsonResult:
    """自适应 Simpson 求积，返回接受区间和局部误差估计。"""

    a, b = _validate_interval(a, b)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")

    evaluations = 0
    accepted: list[tuple[float, float, float, float, int]] = []
    reached_max_depth = False

    def f(x: float) -> float:
        nonlocal evaluations
        evaluations += 1
        return _call_scalar(func, x)

    def simpson_from_values(left: float, right: float, f_left: float, f_mid: float, f_right: float) -> float:
        return (right - left) * (f_left + 4.0 * f_mid + f_right) / 6.0

    def refine(
        left: float,
        right: float,
        f_left: float,
        f_mid: float,
        f_right: float,
        whole: float,
        local_tol: float,
        depth: int,
    ) -> tuple[float, float]:
        nonlocal reached_max_depth
        mid = 0.5 * (left + right)
        left_mid = 0.5 * (left + mid)
        right_mid = 0.5 * (mid + right)
        f_left_mid = f(left_mid)
        f_right_mid = f(right_mid)
        left_value = simpson_from_values(left, mid, f_left, f_left_mid, f_mid)
        right_value = simpson_from_values(mid, right, f_mid, f_right_mid, f_right)
        refined = left_value + right_value
        error = abs(refined - whole) / 15.0

        if error <= local_tol or depth >= max_depth:
            if depth >= max_depth and error > local_tol:
                reached_max_depth = True
            corrected = refined + (refined - whole) / 15.0
            accepted.append((left, right, corrected, error, depth))
            return corrected, error

        left_result, left_error = refine(
            left,
            mid,
            f_left,
            f_left_mid,
            f_mid,
            left_value,
            0.5 * local_tol,
            depth + 1,
        )
        right_result, right_error = refine(
            mid,
            right,
            f_mid,
            f_right_mid,
            f_right,
            right_value,
            0.5 * local_tol,
            depth + 1,
        )
        return left_result + right_result, left_error + right_error

    mid = 0.5 * (a + b)
    f_a = f(a)
    f_mid = f(mid)
    f_b = f(b)
    initial = simpson_from_values(a, b, f_a, f_mid, f_b)
    value, error_estimate = refine(a, b, f_a, f_mid, f_b, initial, tolerance, 0)

    if accepted:
        data = np.array(accepted, dtype=float)
        intervals = data[:, :2]
        local_errors = data[:, 3]
        depths = data[:, 4].astype(int)
    else:
        intervals = np.empty((0, 2), dtype=float)
        local_errors = np.empty(0, dtype=float)
        depths = np.empty(0, dtype=int)

    return AdaptiveSimpsonResult(
        value=float(value),
        error_estimate=float(error_estimate),
        intervals=intervals,
        local_errors=local_errors,
        depths=depths,
        evaluations=evaluations,
        converged=not reached_max_depth,
    )


def gauss_legendre_nodes_weights(order: int) -> tuple[np.ndarray, np.ndarray]:
    """用 Golub-Welsch 思想构造 Gauss-Legendre 节点和权重。"""

    n = _validate_positive_int(order, "order")
    diagonal = np.zeros(n, dtype=float)
    k = np.arange(1, n, dtype=float)
    off_diagonal = k / np.sqrt(4.0 * k**2 - 1.0)
    jacobi = np.diag(diagonal)
    if n > 1:
        jacobi += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
    nodes, eigenvectors = np.linalg.eigh(jacobi)
    weights = 2.0 * eigenvectors[0, :] ** 2
    return nodes, weights


def gauss_legendre_integrate(func: ArrayFunc, a: float, b: float, order: int) -> float:
    """Gauss-Legendre 求积，支持一般区间 [a, b]。"""

    a, b = _validate_interval(a, b)
    nodes, weights = gauss_legendre_nodes_weights(order)
    x = 0.5 * (a + b) + 0.5 * (b - a) * nodes
    values = _evaluate_array(func, x)
    return float(0.5 * (b - a) * np.dot(weights, values))


def gauss_chebyshev_integrate(func: ArrayFunc, order: int) -> float:
    """第一类 Gauss-Chebyshev 求积。

    计算 ``int_{-1}^{1} f(x) / sqrt(1 - x^2) dx``。
    """

    n = _validate_positive_int(order, "order")
    k = np.arange(1, n + 1, dtype=float)
    nodes = np.cos((2.0 * k - 1.0) * np.pi / (2.0 * n))
    return float(np.pi / n * np.sum(_evaluate_array(func, nodes)))


def gauss_laguerre_integrate(func: ArrayFunc, order: int) -> float:
    """Gauss-Laguerre 求积。

    计算 ``int_0^inf exp(-x) f(x) dx``。
    """

    n = _validate_positive_int(order, "order")
    nodes, weights = La.laggauss(n)
    return float(np.dot(weights, _evaluate_array(func, nodes)))


def gauss_hermite_integrate(func: ArrayFunc, order: int) -> float:
    """Gauss-Hermite 求积。

    计算 ``int_{-inf}^{inf} exp(-x^2) f(x) dx``。
    """

    n = _validate_positive_int(order, "order")
    nodes, weights = H.hermgauss(n)
    return float(np.dot(weights, _evaluate_array(func, nodes)))


def discrete_trapezoid(x: np.ndarray, y: np.ndarray) -> float:
    """离散数据的梯形积分，允许非等距节点。"""

    x, y = _as_sorted_points(x, y)
    return float(np.sum(0.5 * (y[:-1] + y[1:]) * np.diff(x)))


def discrete_simpson(x: np.ndarray, y: np.ndarray) -> float:
    """离散数据的局部二次插值积分。

    节点数必须为奇数。若节点等距，该函数退化为复合 Simpson 公式。
    """

    x, y = _as_sorted_points(x, y)
    if x.size < 3:
        raise ValueError("at least three points are required")
    if x.size % 2 == 0:
        raise ValueError("Simpson integration requires an odd number of points")

    total = 0.0
    for i in range(0, x.size - 2, 2):
        total += _quadratic_integral(x[i : i + 3], y[i : i + 3], x[i], x[i + 2])
    return float(total)


def average_parabolic_integral(x: np.ndarray, y: np.ndarray) -> float:
    """平均抛物线插值积分，适合展示局部二次近似的平滑效果。"""

    x, y = _as_sorted_points(x, y)
    if x.size < 3:
        raise ValueError("at least three points are required")

    total = 0.0
    for i in range(x.size - 1):
        estimates = []
        if i >= 1:
            estimates.append(_quadratic_integral(x[i - 1 : i + 2], y[i - 1 : i + 2], x[i], x[i + 1]))
        if i + 2 < x.size:
            estimates.append(_quadratic_integral(x[i : i + 3], y[i : i + 3], x[i], x[i + 1]))
        total += float(np.mean(estimates))
    return float(total)


def natural_cubic_spline_integral(x: np.ndarray, y: np.ndarray) -> float:
    """先构造自然三次样条，再对每段三次多项式精确积分。"""

    x, y = _as_sorted_points(x, y)
    spline = NaturalCubicSpline.fit(x, y)
    h = np.diff(spline.x)
    values = (
        spline.a * h
        + 0.5 * spline.b * h**2
        + spline.c * h**3 / 3.0
        + spline.d * h**4 / 4.0
    )
    return float(np.sum(values))


def tensor_product_gauss_legendre(
    func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
    x_order: int,
    y_order: int,
) -> float:
    """矩形区域上的张量积 Gauss-Legendre 求积。"""

    ax, bx = _validate_interval(*x_bounds)
    ay, by = _validate_interval(*y_bounds)
    tx, wx = gauss_legendre_nodes_weights(x_order)
    ty, wy = gauss_legendre_nodes_weights(y_order)
    x = 0.5 * (ax + bx) + 0.5 * (bx - ax) * tx
    y = 0.5 * (ay + by) + 0.5 * (by - ay) * ty
    xx, yy = np.meshgrid(x, y, indexing="ij")
    values = np.asarray(func(xx, yy), dtype=float)
    if values.shape != xx.shape:
        raise ValueError("func must return an array with the broadcast mesh shape")
    scale = 0.25 * (bx - ax) * (by - ay)
    return float(scale * np.sum((wx[:, None] * wy[None, :]) * values))


def composite_simpson_2d_rectangle(
    func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    x_bounds: tuple[float, float],
    y_bounds: tuple[float, float],
    x_subintervals: int,
    y_subintervals: int,
) -> float:
    """矩形区域上的张量积复合 Simpson 公式。"""

    ax, bx = _validate_interval(*x_bounds)
    ay, by = _validate_interval(*y_bounds)
    nx = _validate_positive_int(x_subintervals, "x_subintervals")
    ny = _validate_positive_int(y_subintervals, "y_subintervals")
    if nx % 2 != 0 or ny % 2 != 0:
        raise ValueError("Simpson subinterval counts must be even")

    x = np.linspace(ax, bx, nx + 1)
    y = np.linspace(ay, by, ny + 1)
    wx = _simpson_weights(nx)
    wy = _simpson_weights(ny)
    xx, yy = np.meshgrid(x, y, indexing="ij")
    values = np.asarray(func(xx, yy), dtype=float)
    if values.shape != xx.shape:
        raise ValueError("func must return an array with the broadcast mesh shape")

    hx = (bx - ax) / nx
    hy = (by - ay) / ny
    return float(hx * hy / 9.0 * np.sum((wx[:, None] * wy[None, :]) * values))


def variable_limit_integral(
    func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    x_bounds: tuple[float, float],
    y_lower: Callable[[np.ndarray], np.ndarray],
    y_upper: Callable[[np.ndarray], np.ndarray],
    x_order: int = 16,
    y_order: int = 16,
) -> float:
    """一般区域上的变限积分，内部使用张量化 Gauss-Legendre。"""

    ax, bx = _validate_interval(*x_bounds)
    tx, wx = gauss_legendre_nodes_weights(x_order)
    ty, wy = gauss_legendre_nodes_weights(y_order)
    x = 0.5 * (ax + bx) + 0.5 * (bx - ax) * tx
    lower = np.asarray(y_lower(x), dtype=float)
    upper = np.asarray(y_upper(x), dtype=float)
    if lower.shape != x.shape or upper.shape != x.shape:
        raise ValueError("y_lower and y_upper must return arrays with the same shape as x")
    if np.any(upper <= lower):
        raise ValueError("expected y_upper(x) > y_lower(x)")

    y = 0.5 * (upper[:, None] + lower[:, None]) + 0.5 * (upper[:, None] - lower[:, None]) * ty[None, :]
    xx = x[:, None] * np.ones_like(y)
    values = np.asarray(func(xx, y), dtype=float)
    if values.shape != y.shape:
        raise ValueError("func must return an array with the transformed mesh shape")
    inner = 0.5 * (upper - lower) * np.sum(values * wy[None, :], axis=1)
    return float(0.5 * (bx - ax) * np.dot(wx, inner))


def monte_carlo_integrate(
    func: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    sample_count: int,
    seed: int | None = None,
) -> MonteCarloResult:
    """高维超矩形区域上的均匀 Monte Carlo 积分。"""

    bounds = _validate_bounds(bounds)
    n = _validate_positive_int(sample_count, "sample_count")
    rng = np.random.default_rng(seed)
    lower = bounds[:, 0]
    upper = bounds[:, 1]
    points = rng.uniform(lower, upper, size=(n, bounds.shape[0]))
    values = np.asarray(func(points), dtype=float)
    if values.shape != (n,):
        raise ValueError("func must return a one-dimensional array with sample_count values")

    volume = float(np.prod(upper - lower))
    sample_mean = float(np.mean(values))
    sample_variance = float(np.var(values, ddof=1)) if n > 1 else 0.0
    standard_error = volume * np.sqrt(sample_variance / n)
    return MonteCarloResult(
        value=volume * sample_mean,
        standard_error=float(standard_error),
        sample_count=n,
        sample_mean=sample_mean,
        sample_variance=sample_variance,
    )


def rejection_monte_carlo_integrate(
    func: Callable[[np.ndarray], np.ndarray],
    indicator: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    sample_count: int,
    seed: int | None = None,
) -> MonteCarloResult:
    """用指示函数处理一般区域上的 Monte Carlo 积分。"""

    def masked_func(points: np.ndarray) -> np.ndarray:
        inside = np.asarray(indicator(points), dtype=bool)
        values = np.asarray(func(points), dtype=float)
        if inside.shape != (points.shape[0],) or values.shape != (points.shape[0],):
            raise ValueError("func and indicator must return one-dimensional arrays")
        return np.where(inside, values, 0.0)

    return monte_carlo_integrate(masked_func, bounds, sample_count, seed=seed)


def _validate_interval(a: float, b: float) -> tuple[float, float]:
    a = float(a)
    b = float(b)
    if not a < b:
        raise ValueError("expected a < b")
    return a, b


def _validate_positive_int(value: int, name: str) -> int:
    value = int(value)
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


def _call_scalar(func: ScalarFunc, x: float) -> float:
    return float(np.asarray(func(float(x)), dtype=float))


def _evaluate_array(func: ArrayFunc, x: np.ndarray) -> np.ndarray:
    values = np.asarray(func(np.asarray(x, dtype=float)), dtype=float)
    if values.shape == ():
        values = np.full_like(x, float(values), dtype=float)
    if values.shape != x.shape:
        raise ValueError("func must return an array with the same shape as x")
    return values


def _as_sorted_points(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x and y must be one-dimensional arrays")
    if x.size != y.size:
        raise ValueError("x and y must have the same length")
    if x.size < 2:
        raise ValueError("at least two points are required")
    order = np.argsort(x)
    x_sorted = x[order]
    if np.any(np.diff(x_sorted) <= 0):
        raise ValueError("x values must be distinct")
    return x_sorted, y[order]


def _interpolatory_weights(nodes: np.ndarray, a: float, b: float) -> np.ndarray:
    nodes = np.asarray(nodes, dtype=float)
    if nodes.ndim != 1 or nodes.size < 1:
        raise ValueError("nodes must be a non-empty one-dimensional array")
    if np.unique(nodes).size != nodes.size:
        raise ValueError("nodes must be distinct")

    vandermonde = np.vander(nodes, N=nodes.size, increasing=True).T
    powers = np.arange(nodes.size, dtype=float)
    moments = (b ** (powers + 1.0) - a ** (powers + 1.0)) / (powers + 1.0)
    return np.linalg.solve(vandermonde, moments)


def _quadratic_integral(x: np.ndarray, y: np.ndarray, left: float, right: float) -> float:
    coefficients = np.linalg.solve(np.vander(x, 3, increasing=True), y)
    powers_left = np.array([left, left**2 / 2.0, left**3 / 3.0])
    powers_right = np.array([right, right**2 / 2.0, right**3 / 3.0])
    return float(np.dot(coefficients, powers_right - powers_left))


def _simpson_weights(subintervals: int) -> np.ndarray:
    weights = np.ones(subintervals + 1, dtype=float)
    weights[1:-1:2] = 4.0
    weights[2:-1:2] = 2.0
    return weights


def _validate_bounds(bounds: np.ndarray) -> np.ndarray:
    bounds = np.asarray(bounds, dtype=float)
    if bounds.ndim != 2 or bounds.shape[1] != 2:
        raise ValueError("bounds must have shape (dimension, 2)")
    if np.any(bounds[:, 1] <= bounds[:, 0]):
        raise ValueError("each bound must satisfy lower < upper")
    return bounds
