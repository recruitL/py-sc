"""第三章示例中使用的函数逼近与曲线拟合算法。"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from numpy.polynomial import chebyshev as C
from numpy.polynomial import legendre as L
from numpy.polynomial import polynomial as P


def _validate_degree(degree: int) -> None:
    if degree < 0:
        raise ValueError("degree must be non-negative")


def _validate_domain(domain: tuple[float, float]) -> tuple[float, float]:
    a, b = map(float, domain)
    if not a < b:
        raise ValueError("domain must satisfy a < b")
    return a, b


def _to_standard_interval(x: np.ndarray, domain: tuple[float, float]) -> np.ndarray:
    a, b = _validate_domain(domain)
    return (2 * np.asarray(x, dtype=float) - (a + b)) / (b - a)


def _from_standard_interval(t: np.ndarray, domain: tuple[float, float]) -> np.ndarray:
    a, b = _validate_domain(domain)
    return 0.5 * (a + b) + 0.5 * (b - a) * np.asarray(t, dtype=float)


def chebyshev_fit_function(
    func: Callable[[np.ndarray], np.ndarray],
    degree: int,
    domain: tuple[float, float] = (-1.0, 1.0),
    sample_count: int | None = None,
) -> np.ndarray:
    """用 Chebyshev 多项式基拟合函数，返回 Chebyshev 系数。

    系数对应标准区间变量 ``t in [-1, 1]``：

    f(x(t)) ≈ c_0 T_0(t) + c_1 T_1(t) + ... + c_n T_n(t).
    """

    _validate_degree(degree)
    _validate_domain(domain)
    if sample_count is None:
        sample_count = degree + 1
    if sample_count < degree + 1:
        raise ValueError("sample_count must be at least degree + 1")

    k = np.arange(sample_count)
    t_nodes = np.cos((2 * k + 1) * np.pi / (2 * sample_count))
    x_nodes = _from_standard_interval(t_nodes, domain)
    y_nodes = np.asarray(func(x_nodes), dtype=float)

    vandermonde = C.chebvander(t_nodes, degree)
    coefficients, *_ = np.linalg.lstsq(vandermonde, y_nodes, rcond=None)
    return coefficients


def chebyshev_series_eval(
    coefficients: np.ndarray,
    x_eval: np.ndarray,
    domain: tuple[float, float] = (-1.0, 1.0),
) -> np.ndarray:
    """计算 Chebyshev 级数在给定点上的取值。"""

    t_eval = _to_standard_interval(np.asarray(x_eval, dtype=float), domain)
    return C.chebval(t_eval, np.asarray(coefficients, dtype=float))


def legendre_fit_function(
    func: Callable[[np.ndarray], np.ndarray],
    degree: int,
    domain: tuple[float, float] = (-1.0, 1.0),
    quadrature_order: int | None = None,
) -> np.ndarray:
    """用 Legendre 投影近似函数，返回 Legendre 系数。

    这里先把 ``domain`` 映射到标准区间，再用 Gauss-Legendre 求积近似内积。
    """

    _validate_degree(degree)
    _validate_domain(domain)
    if quadrature_order is None:
        quadrature_order = max(2 * degree + 3, 32)
    if quadrature_order < degree + 1:
        raise ValueError("quadrature_order must be at least degree + 1")

    t_nodes, weights = L.leggauss(quadrature_order)
    x_nodes = _from_standard_interval(t_nodes, domain)
    y_nodes = np.asarray(func(x_nodes), dtype=float)
    vandermonde = L.legvander(t_nodes, degree)

    coefficients = np.empty(degree + 1, dtype=float)
    for n in range(degree + 1):
        coefficients[n] = 0.5 * (2 * n + 1) * np.sum(weights * y_nodes * vandermonde[:, n])
    return coefficients


def legendre_series_eval(
    coefficients: np.ndarray,
    x_eval: np.ndarray,
    domain: tuple[float, float] = (-1.0, 1.0),
) -> np.ndarray:
    """计算 Legendre 级数在给定点上的取值。"""

    t_eval = _to_standard_interval(np.asarray(x_eval, dtype=float), domain)
    return L.legval(t_eval, np.asarray(coefficients, dtype=float))


def polynomial_least_squares(
    x: np.ndarray,
    y: np.ndarray,
    degree: int,
) -> np.ndarray:
    """在幂基下求多项式最小二乘拟合系数。

    返回升幂排列系数 ``c``，即

    p(x) = c_0 + c_1 x + ... + c_n x^n.
    """

    _validate_degree(degree)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x and y must be one-dimensional arrays")
    if x.size != y.size:
        raise ValueError("x and y must have the same length")
    if x.size < degree + 1:
        raise ValueError("at least degree + 1 points are required")

    vandermonde = np.vander(x, degree + 1, increasing=True)
    coefficients, *_ = np.linalg.lstsq(vandermonde, y, rcond=None)
    return coefficients


def polynomial_eval(coefficients: np.ndarray, x_eval: np.ndarray) -> np.ndarray:
    """计算升幂排列多项式在给定点上的取值。"""

    return P.polyval(np.asarray(x_eval, dtype=float), np.asarray(coefficients, dtype=float))


def pade_from_taylor(
    taylor_coefficients: np.ndarray,
    numerator_degree: int,
    denominator_degree: int,
) -> tuple[np.ndarray, np.ndarray]:
    """由 Taylor 系数构造 Padé 有理逼近。

    输入的 Taylor 系数采用升幂排列：

    f(x) = c_0 + c_1 x + c_2 x^2 + ...

    返回 ``(p, q)``，其中 ``q[0] = 1``，并且

    R(x) = P_m(x) / Q_n(x).
    """

    _validate_degree(numerator_degree)
    _validate_degree(denominator_degree)
    coefficients = np.asarray(taylor_coefficients, dtype=float)
    required = numerator_degree + denominator_degree + 1
    if coefficients.ndim != 1:
        raise ValueError("taylor_coefficients must be one-dimensional")
    if coefficients.size < required:
        raise ValueError("not enough Taylor coefficients for the requested Padé order")

    m = numerator_degree
    n = denominator_degree
    q = np.zeros(n + 1, dtype=float)
    q[0] = 1.0

    if n > 0:
        matrix = np.empty((n, n), dtype=float)
        rhs = np.empty(n, dtype=float)
        for row in range(n):
            power = m + 1 + row
            rhs[row] = -coefficients[power]
            for col in range(n):
                matrix[row, col] = coefficients[power - (col + 1)]
        q[1:] = np.linalg.solve(matrix, rhs)

    p = np.zeros(m + 1, dtype=float)
    for power in range(m + 1):
        total = 0.0
        for j in range(min(power, n) + 1):
            total += q[j] * coefficients[power - j]
        p[power] = total
    return p, q


def pade_eval(
    numerator_coefficients: np.ndarray,
    denominator_coefficients: np.ndarray,
    x_eval: np.ndarray,
) -> np.ndarray:
    """计算 Padé 有理函数在给定点上的取值。"""

    x_eval = np.asarray(x_eval, dtype=float)
    numerator = P.polyval(x_eval, np.asarray(numerator_coefficients, dtype=float))
    denominator = P.polyval(x_eval, np.asarray(denominator_coefficients, dtype=float))
    return numerator / denominator


def adaptive_piecewise_linear(
    func: Callable[[np.ndarray], np.ndarray],
    a: float,
    b: float,
    tolerance: float = 1e-3,
    max_depth: int = 12,
) -> tuple[np.ndarray, np.ndarray]:
    """用中点误差估计构造自适应分段线性逼近节点。"""

    if not a < b:
        raise ValueError("expected a < b")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")

    def f_scalar(x: float) -> float:
        return float(np.asarray(func(np.array([x], dtype=float)))[0])

    nodes: list[float] = []

    def refine(left: float, right: float, f_left: float, f_right: float, depth: int) -> None:
        mid = 0.5 * (left + right)
        f_mid = f_scalar(mid)
        linear_mid = 0.5 * (f_left + f_right)
        error_estimate = abs(f_mid - linear_mid)

        if error_estimate <= tolerance or depth >= max_depth:
            nodes.append(left)
            return

        refine(left, mid, f_left, f_mid, depth + 1)
        refine(mid, right, f_mid, f_right, depth + 1)

    f_a = f_scalar(a)
    f_b = f_scalar(b)
    refine(float(a), float(b), f_a, f_b, 0)
    nodes.append(float(b))

    x_nodes = np.array(nodes, dtype=float)
    y_nodes = np.asarray(func(x_nodes), dtype=float)
    return x_nodes, y_nodes
