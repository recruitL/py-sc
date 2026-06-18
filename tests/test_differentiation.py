from __future__ import annotations

import math

import numpy as np
import pytest

from py_sc import (
    central_difference,
    compact_first_derivative_periodic,
    cubic_uniform_b_spline_basis_derivative,
    differentiate_discrete,
    finite_difference_weights,
    five_point_center_derivative,
    forward_difference,
    natural_cubic_spline_derivative,
    richardson_derivative,
    second_derivative_five_point,
    three_point_endpoint_derivative,
)


def test_central_difference_is_more_accurate_than_forward_for_sine() -> None:
    x0 = 0.7
    h = 1e-3
    exact = math.cos(x0)

    forward_error = abs(float(forward_difference(np.sin, x0, h)) - exact)
    central_error = abs(float(central_difference(np.sin, x0, h)) - exact)

    assert central_error < forward_error


def test_three_and_five_point_formulas_match_polynomial_derivative() -> None:
    func = lambda x: x**4 - 2.0 * x**3 + x
    derivative = lambda x: 4.0 * x**3 - 6.0 * x**2 + 1.0
    x0 = 0.3
    h = 0.1

    np.testing.assert_allclose(five_point_center_derivative(func, x0, h), derivative(x0), atol=1e-12)

    quadratic = lambda x: 2.0 * x**2 - 3.0 * x + 1.0
    np.testing.assert_allclose(three_point_endpoint_derivative(quadratic, 0.0, h), -3.0, atol=1e-12)


def test_second_derivative_five_point_matches_quartic() -> None:
    func = lambda x: x**4 - x**2 + 2.0
    second = lambda x: 12.0 * x**2 - 2.0

    np.testing.assert_allclose(second_derivative_five_point(func, 0.4, 0.05), second(0.4), atol=1e-11)


def test_finite_difference_weights_recover_center_formula() -> None:
    h = 0.25
    weights = finite_difference_weights(np.array([-h, 0.0, h]), 0.0, derivative_order=1)

    np.testing.assert_allclose(weights, np.array([-0.5 / h, 0.0, 0.5 / h]))


def test_differentiate_discrete_is_exact_for_local_polynomial_on_nonuniform_nodes() -> None:
    x = np.array([-1.0, -0.4, 0.0, 0.35, 0.9, 1.4])
    y = x**4 - x**2 + 2.0 * x
    expected = 4.0 * x**3 - 2.0 * x + 2.0

    np.testing.assert_allclose(differentiate_discrete(x, y, stencil_size=5), expected, atol=1e-11)


def test_richardson_derivative_improves_central_difference() -> None:
    result = richardson_derivative(np.sin, 0.3, h=0.2, levels=5)

    assert abs(result.value - math.cos(0.3)) < 1e-12
    assert result.table.shape == (5, 5)
    assert np.all(np.diff(result.step_sizes) < 0)


def test_natural_cubic_spline_derivative_matches_linear_data() -> None:
    x = np.array([-1.0, 0.0, 1.0, 2.0])
    y = 2.5 * x - 1.0
    x_eval = np.linspace(-1.0, 2.0, 9)

    np.testing.assert_allclose(natural_cubic_spline_derivative(x, y, x_eval), np.full_like(x_eval, 2.5))
    np.testing.assert_allclose(
        natural_cubic_spline_derivative(x, y, x_eval, derivative_order=2),
        np.zeros_like(x_eval),
        atol=1e-14,
    )


def test_compact_periodic_derivative_for_sine() -> None:
    n = 64
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    h = x[1] - x[0]
    derivative = compact_first_derivative_periodic(np.sin(x), h)

    assert np.max(np.abs(derivative - np.cos(x))) < 1e-5


def test_b_spline_basis_derivative_known_values() -> None:
    points = np.array([0.0, 1.0, 2.0, 3.0, 4.0])

    np.testing.assert_allclose(
        cubic_uniform_b_spline_basis_derivative(points),
        np.array([0.0, 0.5, 0.0, -0.5, 0.0]),
    )


def test_invalid_step_raises() -> None:
    with pytest.raises(ValueError):
        central_difference(np.sin, 0.0, 0.0)
