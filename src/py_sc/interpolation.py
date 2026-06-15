"""Interpolation algorithms used in Chapter 2 examples."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _as_sorted_points(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x and y must be one-dimensional arrays")
    if x.size != y.size:
        raise ValueError("x and y must have the same length")
    if x.size < 2:
        raise ValueError("at least two data points are required")

    order = np.argsort(x)
    x_sorted = x[order]
    y_sorted = y[order]
    if np.any(np.diff(x_sorted) == 0):
        raise ValueError("x values must be distinct")

    return x_sorted, y_sorted


def lagrange_interpolate(x: np.ndarray, y: np.ndarray, x_eval: np.ndarray) -> np.ndarray:
    """Evaluate the Lagrange interpolation polynomial."""

    x, y = _as_sorted_points(x, y)
    x_eval = np.asarray(x_eval, dtype=float)
    result = np.zeros_like(x_eval, dtype=float)

    for j, xj in enumerate(x):
        basis = np.ones_like(x_eval, dtype=float)
        for m, xm in enumerate(x):
            if m != j:
                basis *= (x_eval - xm) / (xj - xm)
        result += y[j] * basis

    return result


def newton_divided_differences(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute Newton divided-difference coefficients.

    Returns the sorted nodes and the coefficients in Newton form:

    p(x) = c_0 + c_1(x-x_0) + c_2(x-x_0)(x-x_1) + ...
    """

    x, y = _as_sorted_points(x, y)
    coefficients = y.copy()
    n = x.size

    for order in range(1, n):
        coefficients[order:n] = (
            coefficients[order:n] - coefficients[order - 1 : n - 1]
        ) / (x[order:n] - x[: n - order])

    return x, coefficients


def newton_interpolate(
    x: np.ndarray,
    coefficients: np.ndarray,
    x_eval: np.ndarray,
) -> np.ndarray:
    """Evaluate a Newton interpolation polynomial."""

    x = np.asarray(x, dtype=float)
    coefficients = np.asarray(coefficients, dtype=float)
    x_eval = np.asarray(x_eval, dtype=float)

    if x.ndim != 1 or coefficients.ndim != 1:
        raise ValueError("x and coefficients must be one-dimensional arrays")
    if x.size != coefficients.size:
        raise ValueError("x and coefficients must have the same length")

    result = np.full_like(x_eval, coefficients[-1], dtype=float)
    for k in range(coefficients.size - 2, -1, -1):
        result = coefficients[k] + (x_eval - x[k]) * result

    return result


def chebyshev_nodes(a: float, b: float, n: int) -> np.ndarray:
    """Return n Chebyshev nodes on the interval [a, b]."""

    if n < 1:
        raise ValueError("n must be at least 1")
    if b <= a:
        raise ValueError("expected a < b")

    k = np.arange(n)
    nodes = np.cos((2 * k + 1) * np.pi / (2 * n))
    mapped = 0.5 * (a + b) + 0.5 * (b - a) * nodes
    return np.sort(mapped)


def piecewise_linear_interpolate(
    x: np.ndarray,
    y: np.ndarray,
    x_eval: np.ndarray,
) -> np.ndarray:
    """Evaluate piecewise linear interpolation."""

    x, y = _as_sorted_points(x, y)
    return np.interp(np.asarray(x_eval, dtype=float), x, y)


@dataclass(frozen=True)
class NaturalCubicSpline:
    """Natural cubic spline interpolant with zero endpoint second derivatives."""

    x: np.ndarray
    a: np.ndarray
    b: np.ndarray
    c: np.ndarray
    d: np.ndarray

    @classmethod
    def fit(cls, x: np.ndarray, y: np.ndarray) -> "NaturalCubicSpline":
        x, y = _as_sorted_points(x, y)
        n = x.size
        h = np.diff(x)

        alpha = np.zeros(n)
        for i in range(1, n - 1):
            alpha[i] = 3 * (y[i + 1] - y[i]) / h[i] - 3 * (y[i] - y[i - 1]) / h[i - 1]

        lower = np.zeros(n)
        diag = np.ones(n)
        upper = np.zeros(n)
        rhs = np.zeros(n)

        for i in range(1, n - 1):
            lower[i] = h[i - 1]
            diag[i] = 2 * (x[i + 1] - x[i - 1])
            upper[i] = h[i]
            rhs[i] = alpha[i]

        c = _solve_tridiagonal(lower, diag, upper, rhs)
        a = y[:-1]
        b = np.zeros(n - 1)
        d = np.zeros(n - 1)

        for i in range(n - 1):
            b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3
            d[i] = (c[i + 1] - c[i]) / (3 * h[i])

        return cls(x=x, a=a, b=b, c=c[:-1], d=d)

    def __call__(self, x_eval: np.ndarray) -> np.ndarray:
        x_eval = np.asarray(x_eval, dtype=float)
        indices = np.searchsorted(self.x, x_eval, side="right") - 1
        indices = np.clip(indices, 0, self.a.size - 1)
        dx = x_eval - self.x[indices]
        return self.a[indices] + self.b[indices] * dx + self.c[indices] * dx**2 + self.d[indices] * dx**3


def cubic_spline_coefficients(x: np.ndarray, y: np.ndarray) -> dict[str, np.ndarray]:
    """Return natural cubic spline coefficients for teaching inspection."""

    spline = NaturalCubicSpline.fit(x, y)
    return {
        "x": spline.x,
        "a": spline.a,
        "b": spline.b,
        "c": spline.c,
        "d": spline.d,
    }


def _solve_tridiagonal(
    lower: np.ndarray,
    diag: np.ndarray,
    upper: np.ndarray,
    rhs: np.ndarray,
) -> np.ndarray:
    """Solve a tridiagonal linear system with the Thomas algorithm."""

    n = diag.size
    c_prime = np.zeros(n)
    d_prime = np.zeros(n)

    c_prime[0] = upper[0] / diag[0]
    d_prime[0] = rhs[0] / diag[0]

    for i in range(1, n):
        denom = diag[i] - lower[i] * c_prime[i - 1]
        c_prime[i] = upper[i] / denom if i < n - 1 else 0.0
        d_prime[i] = (rhs[i] - lower[i] * d_prime[i - 1]) / denom

    solution = np.zeros(n)
    solution[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        solution[i] = d_prime[i] - c_prime[i] * solution[i + 1]

    return solution
