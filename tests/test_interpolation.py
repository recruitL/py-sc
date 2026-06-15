from __future__ import annotations

import numpy as np

from py_sc import NaturalCubicSpline, lagrange_interpolate, piecewise_linear_interpolate


def test_lagrange_interpolates_training_points() -> None:
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.0, 2.0])

    np.testing.assert_allclose(lagrange_interpolate(x, y, x), y)


def test_piecewise_linear_interpolates_midpoint() -> None:
    x = np.array([0.0, 1.0])
    y = np.array([2.0, 4.0])

    np.testing.assert_allclose(piecewise_linear_interpolate(x, y, np.array([0.5])), np.array([3.0]))


def test_natural_cubic_spline_interpolates_training_points() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])
    spline = NaturalCubicSpline.fit(x, y)

    np.testing.assert_allclose(spline(x), y)

