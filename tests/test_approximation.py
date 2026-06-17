from __future__ import annotations

import math

import numpy as np

from py_sc import (
    adaptive_piecewise_linear,
    chebyshev_fit_function,
    chebyshev_series_eval,
    legendre_fit_function,
    legendre_series_eval,
    pade_eval,
    pade_from_taylor,
    polynomial_eval,
    polynomial_least_squares,
)


def test_chebyshev_fit_reconstructs_polynomial() -> None:
    def target(x: np.ndarray) -> np.ndarray:
        return 1.0 - 2.0 * x + 0.5 * x**2

    coefficients = chebyshev_fit_function(target, degree=2)
    x_eval = np.linspace(-1.0, 1.0, 21)

    np.testing.assert_allclose(chebyshev_series_eval(coefficients, x_eval), target(x_eval), atol=1e-12)


def test_legendre_fit_reconstructs_x_squared() -> None:
    coefficients = legendre_fit_function(lambda x: x**2, degree=2, quadrature_order=8)

    np.testing.assert_allclose(coefficients, np.array([1.0 / 3.0, 0.0, 2.0 / 3.0]), atol=1e-12)
    x_eval = np.linspace(-1.0, 1.0, 11)
    np.testing.assert_allclose(legendre_series_eval(coefficients, x_eval), x_eval**2, atol=1e-12)


def test_polynomial_least_squares_recovers_quadratic() -> None:
    x = np.linspace(-2.0, 2.0, 9)
    y = 2.0 - 3.0 * x + 0.25 * x**2

    coefficients = polynomial_least_squares(x, y, degree=2)

    np.testing.assert_allclose(coefficients, np.array([2.0, -3.0, 0.25]), atol=1e-12)
    np.testing.assert_allclose(polynomial_eval(coefficients, x), y, atol=1e-12)


def test_pade_exp_11_matches_known_formula() -> None:
    taylor = np.array([1.0, 1.0, 1.0 / 2.0])

    numerator, denominator = pade_from_taylor(taylor, numerator_degree=1, denominator_degree=1)

    np.testing.assert_allclose(numerator, np.array([1.0, 0.5]), atol=1e-12)
    np.testing.assert_allclose(denominator, np.array([1.0, -0.5]), atol=1e-12)
    x_eval = np.array([0.1, 0.2])
    np.testing.assert_allclose(
        pade_eval(numerator, denominator, x_eval),
        (1.0 + 0.5 * x_eval) / (1.0 - 0.5 * x_eval),
    )


def test_adaptive_piecewise_linear_refines_curved_function() -> None:
    coarse_x, _ = adaptive_piecewise_linear(np.sin, 0.0, math.pi, tolerance=0.5, max_depth=8)
    fine_x, _ = adaptive_piecewise_linear(np.sin, 0.0, math.pi, tolerance=0.02, max_depth=8)

    assert coarse_x.size >= 2
    assert fine_x.size > coarse_x.size
    assert np.all(np.diff(fine_x) > 0)
