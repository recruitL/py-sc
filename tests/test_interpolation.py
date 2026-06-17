from __future__ import annotations

import numpy as np

from py_sc import (
    NaturalCubicSpline,
    bilinear_interpolate_cell,
    chebyshev_nodes,
    cubic_uniform_b_spline_basis,
    cubic_spline_coefficients,
    divided_difference_table,
    lagrange_interpolate,
    newton_divided_differences,
    newton_interpolate,
    pchip_interpolate,
    pchip_slopes,
    piecewise_cubic_hermite_interpolate,
    piecewise_linear_interpolate,
    triangle_linear_interpolate,
)


def test_lagrange_interpolates_training_points() -> None:
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.0, 2.0])

    np.testing.assert_allclose(lagrange_interpolate(x, y, x), y)


def test_piecewise_linear_interpolates_midpoint() -> None:
    x = np.array([0.0, 1.0])
    y = np.array([2.0, 4.0])

    np.testing.assert_allclose(piecewise_linear_interpolate(x, y, np.array([0.5])), np.array([3.0]))


def test_piecewise_cubic_hermite_matches_cubic_with_exact_slopes() -> None:
    x = np.array([-1.0, 0.0, 1.0, 2.0])
    y = x**3 - 2 * x + 1
    slopes = 3 * x**2 - 2
    x_eval = np.linspace(-1.0, 2.0, 17)

    np.testing.assert_allclose(
        piecewise_cubic_hermite_interpolate(x, y, slopes, x_eval),
        x_eval**3 - 2 * x_eval + 1,
    )


def test_pchip_interpolates_nodes_and_preserves_monotone_range() -> None:
    x = np.array([0.0, 1.0, 2.0, 4.0])
    y = np.array([0.0, 0.4, 0.9, 1.2])
    x_eval = np.linspace(0.0, 4.0, 41)
    values = pchip_interpolate(x, y, x_eval)

    np.testing.assert_allclose(pchip_interpolate(x, y, x), y)
    assert np.all(values >= y.min() - 1e-12)
    assert np.all(values <= y.max() + 1e-12)
    assert np.all(np.diff(values) >= -1e-12)


def test_pchip_sets_slope_zero_at_local_extremum() -> None:
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 0.0])

    _, _, slopes = pchip_slopes(x, y)

    assert slopes[1] == 0.0


def test_cubic_uniform_b_spline_basis_known_values() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])

    np.testing.assert_allclose(
        cubic_uniform_b_spline_basis(x),
        np.array([0.0, 1.0 / 6.0, 2.0 / 3.0, 1.0 / 6.0, 0.0]),
    )


def test_bilinear_interpolate_cell_matches_linear_function() -> None:
    values = np.array([[1.0, 3.0], [4.0, 6.0]])

    result = bilinear_interpolate_cell((0.0, 1.0), (0.0, 1.0), values, np.array([0.5]), np.array([0.5]))

    np.testing.assert_allclose(result, np.array([3.5]))


def test_triangle_linear_interpolate_matches_linear_function() -> None:
    vertices = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    values = 1.0 + 2.0 * vertices[:, 0] + 3.0 * vertices[:, 1]
    points = np.array([[0.25, 0.5], [0.2, 0.3]])

    np.testing.assert_allclose(
        triangle_linear_interpolate(vertices, values, points),
        1.0 + 2.0 * points[:, 0] + 3.0 * points[:, 1],
    )


def test_newton_interpolation_matches_lagrange() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])
    x_eval = np.linspace(0.0, 3.0, 9)
    nodes, coefficients = newton_divided_differences(x, y)

    np.testing.assert_allclose(
        newton_interpolate(nodes, coefficients, x_eval),
        lagrange_interpolate(x, y, x_eval),
    )


def test_divided_difference_table_first_row_matches_coefficients() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])

    nodes, coefficients = newton_divided_differences(x, y)
    table_nodes, table = divided_difference_table(x, y)

    np.testing.assert_allclose(table_nodes, nodes)
    np.testing.assert_allclose(table[0], coefficients)


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
