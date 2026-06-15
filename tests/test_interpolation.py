from __future__ import annotations

import numpy as np

from py_sc import (
    NaturalCubicSpline,
    chebyshev_nodes,
    cubic_spline_coefficients,
    lagrange_interpolate,
    newton_divided_differences,
    newton_interpolate,
    piecewise_linear_interpolate,
)


def test_lagrange_interpolates_training_points() -> None:
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.0, 2.0])

    np.testing.assert_allclose(lagrange_interpolate(x, y, x), y)


def test_piecewise_linear_interpolates_midpoint() -> None:
    x = np.array([0.0, 1.0])
    y = np.array([2.0, 4.0])

    np.testing.assert_allclose(piecewise_linear_interpolate(x, y, np.array([0.5])), np.array([3.0]))


def test_newton_interpolation_matches_lagrange() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])
    x_eval = np.linspace(0.0, 3.0, 9)
    nodes, coefficients = newton_divided_differences(x, y)

    np.testing.assert_allclose(
        newton_interpolate(nodes, coefficients, x_eval),
        lagrange_interpolate(x, y, x_eval),
    )


def test_chebyshev_nodes_are_inside_interval() -> None:
    nodes = chebyshev_nodes(-2.0, 3.0, 8)

    assert np.all(nodes >= -2.0)
    assert np.all(nodes <= 3.0)
    assert np.all(np.diff(nodes) > 0)


def test_natural_cubic_spline_interpolates_training_points() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])
    spline = NaturalCubicSpline.fit(x, y)

    np.testing.assert_allclose(spline(x), y)


def test_cubic_spline_coefficients_have_interval_length() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])
    coefficients = cubic_spline_coefficients(x, y)

    assert coefficients["a"].size == x.size - 1
    assert coefficients["b"].size == x.size - 1
    assert coefficients["c"].size == x.size - 1
    assert coefficients["d"].size == x.size - 1
