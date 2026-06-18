from __future__ import annotations

import math

import numpy as np

from py_sc import (
    adaptive_simpson,
    closed_newton_cotes_weights,
    composite_simpson,
    composite_simpson_2d_rectangle,
    composite_trapezoid,
    discrete_simpson,
    discrete_trapezoid,
    gauss_chebyshev_integrate,
    gauss_hermite_integrate,
    gauss_laguerre_integrate,
    gauss_legendre_integrate,
    gauss_legendre_nodes_weights,
    monte_carlo_integrate,
    natural_cubic_spline_integral,
    newton_cotes_integrate,
    romberg_integrate,
    tensor_product_gauss_legendre,
)


def test_closed_newton_cotes_weights_match_trapezoid_and_simpson() -> None:
    nodes_1, weights_1 = closed_newton_cotes_weights(1)
    nodes_2, weights_2 = closed_newton_cotes_weights(2)

    np.testing.assert_allclose(nodes_1, np.array([0.0, 1.0]))
    np.testing.assert_allclose(weights_1, np.array([0.5, 0.5]))
    np.testing.assert_allclose(nodes_2, np.array([0.0, 0.5, 1.0]))
    np.testing.assert_allclose(weights_2, np.array([1.0 / 6.0, 4.0 / 6.0, 1.0 / 6.0]))

    value = newton_cotes_integrate(lambda x: x**2, 0.0, 1.0, nodes_2, weights_2)
    assert abs(value - 1.0 / 3.0) < 1e-14


def test_composite_rules_integrate_polynomials() -> None:
    trapezoid_value = composite_trapezoid(lambda x: x, 0.0, 2.0, subintervals=8)
    simpson_value = composite_simpson(lambda x: x**3 - 2.0 * x + 1.0, -1.0, 2.0, subintervals=10)

    assert abs(trapezoid_value - 2.0) < 1e-14
    exact = (2.0**4 - (-1.0) ** 4) / 4.0 - (2.0**2 - (-1.0) ** 2) + 3.0
    assert abs(simpson_value - exact) < 1e-14


def test_romberg_and_adaptive_simpson_integrate_sine() -> None:
    romberg = romberg_integrate(math.sin, 0.0, math.pi, max_order=7, tolerance=1e-10)
    adaptive = adaptive_simpson(math.sin, 0.0, math.pi, tolerance=1e-10, max_depth=20)

    assert romberg.converged
    assert abs(romberg.value - 2.0) < 1e-10
    assert adaptive.converged
    assert abs(adaptive.value - 2.0) < 1e-10
    assert adaptive.intervals.shape[1] == 2
    assert adaptive.evaluations >= 3


def test_gauss_legendre_exactness_for_polynomials() -> None:
    nodes, weights = gauss_legendre_nodes_weights(3)

    assert nodes.size == 3
    assert weights.size == 3
    assert abs(np.sum(weights) - 2.0) < 1e-14
    assert abs(gauss_legendre_integrate(lambda x: x**4, -1.0, 1.0, order=3) - 2.0 / 5.0) < 1e-14
    assert abs(gauss_legendre_integrate(lambda x: x**5, -1.0, 1.0, order=3)) < 1e-14


def test_weighted_gaussian_rules_match_known_moments() -> None:
    assert abs(gauss_chebyshev_integrate(lambda x: x**2, order=8) - math.pi / 2.0) < 1e-14
    assert abs(gauss_laguerre_integrate(lambda x: x, order=8) - 1.0) < 1e-14
    assert abs(gauss_hermite_integrate(lambda x: x**2, order=8) - math.sqrt(math.pi) / 2.0) < 1e-14


def test_discrete_integration_methods() -> None:
    x = np.array([-1.0, -0.2, 0.7, 1.5, 2.0])
    y = x**2 + 2.0 * x + 1.0

    exact = (2.0**3 - (-1.0) ** 3) / 3.0 + (2.0**2 - (-1.0) ** 2) + 3.0
    assert abs(discrete_simpson(x, y) - exact) < 1e-14
    assert abs(discrete_trapezoid(np.array([0.0, 1.0]), np.array([2.0, 2.0])) - 2.0) < 1e-14

    xs = np.linspace(0.0, math.pi, 17)
    ys = np.sin(xs)
    assert abs(natural_cubic_spline_integral(xs, ys) - 2.0) < 5e-4


def test_two_dimensional_quadrature() -> None:
    func = lambda x, y: x + y

    assert abs(tensor_product_gauss_legendre(func, (0.0, 1.0), (0.0, 2.0), 3, 3) - 3.0) < 1e-14
    assert abs(composite_simpson_2d_rectangle(func, (0.0, 1.0), (0.0, 2.0), 4, 4) - 3.0) < 1e-14


def test_monte_carlo_constant_integral_has_zero_standard_error() -> None:
    result = monte_carlo_integrate(lambda points: np.full(points.shape[0], 2.0), np.array([[0.0, 1.0], [0.0, 1.0]]), 128, seed=2026)

    assert result.value == 2.0
    assert result.standard_error == 0.0
    assert result.sample_count == 128
