"""第五章示例中使用的数值微分算法。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import math

import numpy as np

from .interpolation import NaturalCubicSpline


ArrayFunc = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class RichardsonDerivativeResult:
    """Richardson 外推微分的结果和外推表。"""

    value: float
    table: np.ndarray
    step_sizes: np.ndarray


def forward_difference(func: ArrayFunc, x: np.ndarray | float, h: float) -> np.ndarray:
    """前向差分近似一阶导数。"""

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    return (_evaluate_array(func, x + h) - _evaluate_array(func, x)) / h


def backward_difference(func: ArrayFunc, x: np.ndarray | float, h: float) -> np.ndarray:
    """后向差分近似一阶导数。"""

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    return (_evaluate_array(func, x) - _evaluate_array(func, x - h)) / h


def central_difference(func: ArrayFunc, x: np.ndarray | float, h: float) -> np.ndarray:
    """中心差分近似一阶导数。"""

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    return (_evaluate_array(func, x + h) - _evaluate_array(func, x - h)) / (2.0 * h)


def midpoint_difference(func: ArrayFunc, x_mid: np.ndarray | float, h: float) -> np.ndarray:
    """用区间两端函数值近似中点处的一阶导数。"""

    return central_difference(func, x_mid, h)


def three_point_endpoint_derivative(
    func: ArrayFunc,
    x: np.ndarray | float,
    h: float,
    side: str = "left",
) -> np.ndarray:
    """三点端点一阶导数公式。

    ``side="left"`` 使用 ``x, x+h, x+2h`` 近似左端点导数；
    ``side="right"`` 使用 ``x, x-h, x-2h`` 近似右端点导数。
    """

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    side = _validate_side(side)
    if side == "left":
        return (
            -3.0 * _evaluate_array(func, x)
            + 4.0 * _evaluate_array(func, x + h)
            - _evaluate_array(func, x + 2.0 * h)
        ) / (2.0 * h)
    return (
        3.0 * _evaluate_array(func, x)
        - 4.0 * _evaluate_array(func, x - h)
        + _evaluate_array(func, x - 2.0 * h)
    ) / (2.0 * h)


def five_point_center_derivative(func: ArrayFunc, x: np.ndarray | float, h: float) -> np.ndarray:
    """五点中心一阶导数公式，截断误差为 O(h^4)。"""

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    return (
        _evaluate_array(func, x - 2.0 * h)
        - 8.0 * _evaluate_array(func, x - h)
        + 8.0 * _evaluate_array(func, x + h)
        - _evaluate_array(func, x + 2.0 * h)
    ) / (12.0 * h)


def five_point_endpoint_derivative(
    func: ArrayFunc,
    x: np.ndarray | float,
    h: float,
    side: str = "left",
) -> np.ndarray:
    """五点单边一阶导数公式，适合端点。"""

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    side = _validate_side(side)
    if side == "left":
        return (
            -25.0 * _evaluate_array(func, x)
            + 48.0 * _evaluate_array(func, x + h)
            - 36.0 * _evaluate_array(func, x + 2.0 * h)
            + 16.0 * _evaluate_array(func, x + 3.0 * h)
            - 3.0 * _evaluate_array(func, x + 4.0 * h)
        ) / (12.0 * h)
    return (
        25.0 * _evaluate_array(func, x)
        - 48.0 * _evaluate_array(func, x - h)
        + 36.0 * _evaluate_array(func, x - 2.0 * h)
        - 16.0 * _evaluate_array(func, x - 3.0 * h)
        + 3.0 * _evaluate_array(func, x - 4.0 * h)
    ) / (12.0 * h)


def second_derivative_three_point(func: ArrayFunc, x: np.ndarray | float, h: float) -> np.ndarray:
    """三点中心二阶导数公式。"""

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    return (
        _evaluate_array(func, x - h)
        - 2.0 * _evaluate_array(func, x)
        + _evaluate_array(func, x + h)
    ) / h**2


def second_derivative_endpoint_three_point(
    func: ArrayFunc,
    x: np.ndarray | float,
    h: float,
    side: str = "left",
) -> np.ndarray:
    """三点单边二阶导数公式，截断误差为 O(h)。"""

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    side = _validate_side(side)
    if side == "left":
        return (
            _evaluate_array(func, x)
            - 2.0 * _evaluate_array(func, x + h)
            + _evaluate_array(func, x + 2.0 * h)
        ) / h**2
    return (
        _evaluate_array(func, x)
        - 2.0 * _evaluate_array(func, x - h)
        + _evaluate_array(func, x - 2.0 * h)
    ) / h**2


def second_derivative_five_point(func: ArrayFunc, x: np.ndarray | float, h: float) -> np.ndarray:
    """五点中心二阶导数公式，截断误差为 O(h^4)。"""

    h = _validate_positive_step(h)
    x = np.asarray(x, dtype=float)
    return (
        -_evaluate_array(func, x - 2.0 * h)
        + 16.0 * _evaluate_array(func, x - h)
        - 30.0 * _evaluate_array(func, x)
        + 16.0 * _evaluate_array(func, x + h)
        - _evaluate_array(func, x + 2.0 * h)
    ) / (12.0 * h**2)


def finite_difference_weights(
    nodes: np.ndarray,
    x0: float,
    derivative_order: int,
) -> np.ndarray:
    """由局部插值多项式构造非等距节点有限差分权重。"""

    nodes = np.asarray(nodes, dtype=float)
    if nodes.ndim != 1:
        raise ValueError("nodes must be one-dimensional")
    if nodes.size < 1:
        raise ValueError("at least one node is required")
    if np.unique(nodes).size != nodes.size:
        raise ValueError("nodes must be distinct")
    derivative_order = int(derivative_order)
    if derivative_order < 0:
        raise ValueError("derivative_order must be non-negative")
    if derivative_order >= nodes.size:
        raise ValueError("derivative_order must be smaller than the number of nodes")

    shifted = nodes - float(x0)
    matrix = np.vander(shifted, N=nodes.size, increasing=True).T
    rhs = np.zeros(nodes.size, dtype=float)
    rhs[derivative_order] = math.factorial(derivative_order)
    return np.linalg.solve(matrix, rhs)


def differentiate_discrete(
    x: np.ndarray,
    y: np.ndarray,
    derivative_order: int = 1,
    stencil_size: int = 3,
) -> np.ndarray:
    """在离散数据节点上用局部有限差分权重估计导数。

    该函数允许非等距节点。每个节点附近选取 ``stencil_size`` 个点，
    再由局部插值多项式求导得到权重。
    """

    x, y = _as_sorted_points(x, y)
    derivative_order = int(derivative_order)
    stencil_size = int(stencil_size)
    if derivative_order < 1:
        raise ValueError("derivative_order must be positive")
    if stencil_size <= derivative_order:
        raise ValueError("stencil_size must be larger than derivative_order")
    if stencil_size > x.size:
        raise ValueError("stencil_size cannot exceed the number of data points")

    half = stencil_size // 2
    result = np.empty_like(y, dtype=float)
    for i, x0 in enumerate(x):
        start = min(max(i - half, 0), x.size - stencil_size)
        stop = start + stencil_size
        weights = finite_difference_weights(x[start:stop], x0, derivative_order)
        result[i] = np.dot(weights, y[start:stop])
    return result


def richardson_extrapolate(
    approximations: np.ndarray,
    base_order: int,
    order_step: int = 2,
) -> np.ndarray:
    """根据按 ``h, h/2, h/4, ...`` 排列的近似值构造 Richardson 表。"""

    approximations = np.asarray(approximations, dtype=float)
    if approximations.ndim != 1 or approximations.size < 1:
        raise ValueError("approximations must be a non-empty one-dimensional array")
    base_order = _validate_positive_int(base_order, "base_order")
    order_step = _validate_positive_int(order_step, "order_step")

    n = approximations.size
    table = np.full((n, n), np.nan, dtype=float)
    table[:, 0] = approximations
    for col in range(1, n):
        power = base_order + (col - 1) * order_step
        factor = 2.0**power
        for row in range(col, n):
            table[row, col] = table[row, col - 1] + (
                table[row, col - 1] - table[row - 1, col - 1]
            ) / (factor - 1.0)
    return table


def richardson_derivative(
    func: ArrayFunc,
    x: float,
    h: float,
    levels: int = 4,
    method: str = "central",
) -> RichardsonDerivativeResult:
    """对一阶差分公式做 Richardson 外推。"""

    h = _validate_positive_step(h)
    levels = _validate_positive_int(levels, "levels")
    x = float(x)
    method = method.lower()
    if method == "central":
        base_order = 2
        order_step = 2
        difference = central_difference
    elif method == "forward":
        base_order = 1
        order_step = 1
        difference = forward_difference
    elif method == "backward":
        base_order = 1
        order_step = 1
        difference = backward_difference
    else:
        raise ValueError("method must be 'central', 'forward', or 'backward'")

    step_sizes = h / (2.0 ** np.arange(levels, dtype=float))
    approximations = np.array([float(difference(func, x, step)) for step in step_sizes])
    table = richardson_extrapolate(approximations, base_order=base_order, order_step=order_step)
    return RichardsonDerivativeResult(
        value=float(table[levels - 1, levels - 1]),
        table=table,
        step_sizes=step_sizes,
    )


def compact_first_derivative_periodic(y: np.ndarray, h: float) -> np.ndarray:
    """周期边界上的四阶紧致差分一阶导数。

    离散方程为

    (1/4)d_{i-1} + d_i + (1/4)d_{i+1}
    = (3/(4h))(f_{i+1} - f_{i-1}).
    """

    h = _validate_positive_step(h)
    y = np.asarray(y, dtype=float)
    if y.ndim != 1:
        raise ValueError("y must be one-dimensional")
    if y.size < 3:
        raise ValueError("at least three values are required")

    n = y.size
    matrix = np.eye(n, dtype=float)
    for i in range(n):
        matrix[i, (i - 1) % n] = 0.25
        matrix[i, (i + 1) % n] = 0.25
    rhs = 0.75 * (np.roll(y, -1) - np.roll(y, 1)) / h
    return np.linalg.solve(matrix, rhs)


def natural_cubic_spline_derivative(
    x: np.ndarray,
    y: np.ndarray,
    x_eval: np.ndarray | None = None,
    derivative_order: int = 1,
) -> np.ndarray:
    """构造自然三次样条后，对分段三次多项式解析求导。"""

    x, y = _as_sorted_points(x, y)
    derivative_order = int(derivative_order)
    if derivative_order not in {1, 2}:
        raise ValueError("derivative_order must be 1 or 2")
    if x_eval is None:
        x_eval = x
    x_eval = np.asarray(x_eval, dtype=float)

    spline = NaturalCubicSpline.fit(x, y)
    indices = np.searchsorted(spline.x, x_eval, side="right") - 1
    indices = np.clip(indices, 0, spline.a.size - 1)
    dx = x_eval - spline.x[indices]
    if derivative_order == 1:
        return spline.b[indices] + 2.0 * spline.c[indices] * dx + 3.0 * spline.d[indices] * dx**2
    return 2.0 * spline.c[indices] + 6.0 * spline.d[indices] * dx


def cubic_uniform_b_spline_basis_derivative(
    x: np.ndarray | float,
    derivative_order: int = 1,
) -> np.ndarray:
    """三次均匀 B 样条基函数的一阶或二阶导数。"""

    x = np.asarray(x, dtype=float)
    derivative_order = int(derivative_order)
    if derivative_order == 1:
        return (
            _truncated_power(x, 2)
            - 4.0 * _truncated_power(x - 1.0, 2)
            + 6.0 * _truncated_power(x - 2.0, 2)
            - 4.0 * _truncated_power(x - 3.0, 2)
            + _truncated_power(x - 4.0, 2)
        ) / 2.0
    if derivative_order == 2:
        return (
            _truncated_power(x, 1)
            - 4.0 * _truncated_power(x - 1.0, 1)
            + 6.0 * _truncated_power(x - 2.0, 1)
            - 4.0 * _truncated_power(x - 3.0, 1)
            + _truncated_power(x - 4.0, 1)
        )
    raise ValueError("derivative_order must be 1 or 2")


def uniform_b_spline_curve_derivative(
    control_values: np.ndarray,
    t_eval: np.ndarray | float,
    spacing: float = 1.0,
    derivative_order: int = 1,
) -> np.ndarray:
    """计算一维三次均匀 B 样条曲线的一阶或二阶导数。"""

    spacing = _validate_positive_step(spacing)
    control_values = np.asarray(control_values, dtype=float)
    if control_values.ndim != 1:
        raise ValueError("control_values must be one-dimensional")
    t_eval = np.asarray(t_eval, dtype=float)
    result = np.zeros_like(t_eval, dtype=float)
    scaled_t = t_eval / spacing
    for j, coefficient in enumerate(control_values):
        result += coefficient * cubic_uniform_b_spline_basis_derivative(
            scaled_t - j,
            derivative_order=derivative_order,
        )
    return result / spacing**derivative_order


def observed_order(errors: np.ndarray, refinement_factor: float = 2.0) -> np.ndarray:
    """由相邻误差估计实验收敛阶。"""

    errors = np.asarray(errors, dtype=float)
    if errors.ndim != 1 or errors.size < 2:
        raise ValueError("errors must be a one-dimensional array with at least two values")
    if refinement_factor <= 1:
        raise ValueError("refinement_factor must be greater than 1")
    with np.errstate(divide="ignore", invalid="ignore"):
        orders = np.log(errors[:-1] / errors[1:]) / np.log(refinement_factor)
    orders[~np.isfinite(orders)] = np.nan
    return orders


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


def _validate_positive_step(h: float) -> float:
    h = float(h)
    if h <= 0:
        raise ValueError("step size must be positive")
    return h


def _validate_positive_int(value: int, name: str) -> int:
    value = int(value)
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


def _validate_side(side: str) -> str:
    side = side.lower()
    if side not in {"left", "right"}:
        raise ValueError("side must be 'left' or 'right'")
    return side


def _truncated_power(x: np.ndarray, power: int) -> np.ndarray:
    return np.maximum(np.asarray(x, dtype=float), 0.0) ** power
