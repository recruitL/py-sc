from __future__ import annotations

import math

import numpy as np
import pytest

from py_sc import (
    aitken_delta_squared,
    bisection_method,
    damped_newton_method,
    find_sign_change_brackets,
    fixed_point_iteration,
    modified_newton_method,
    muller_method,
    newton_method,
    secant_method,
    steffensen_method,
)


def test_find_sign_change_brackets_finds_multiple_roots() -> None:
    func = lambda x: (x - 1.0) * (x + 0.5) * (x - 2.0)

    brackets = find_sign_change_brackets(func, -1.0, 2.5, subintervals=35)

    assert any(left <= -0.5 <= right for left, right in brackets)
    assert any(left <= 1.0 <= right for left, right in brackets)
    assert any(left <= 2.0 <= right for left, right in brackets)


def test_bisection_solves_cos_fixed_point_equation() -> None:
    result = bisection_method(lambda x: math.cos(x) - x, 0.0, 1.0, tolerance=1e-12)

    assert result.converged
    assert abs(result.root - 0.7390851332151607) < 1e-11
    assert result.residual < 1e-11
    assert result.history.size == result.iterations


def test_bisection_rejects_interval_without_sign_change() -> None:
    with pytest.raises(ValueError):
        bisection_method(lambda x: x**2 + 1.0, -1.0, 1.0)


def test_even_multiplicity_root_has_no_sign_change() -> None:
    brackets = find_sign_change_brackets(lambda x: (x - 1.0) ** 2, 0.0, 2.0, subintervals=19)

    assert brackets == []


def test_fixed_point_iteration_solves_cos_fixed_point() -> None:
    result = fixed_point_iteration(math.cos, 0.5, tolerance=1e-12, max_iterations=100)

    assert result.converged
    assert abs(result.root - 0.7390851332151607) < 1e-10
    assert result.residual < 1e-10
    assert result.history.size == result.iterations + 1


def test_aitken_delta_squared_accelerates_linear_sequence() -> None:
    exact = 2.0
    sequence = np.array([exact + 0.8**k for k in range(8)], dtype=float)

    accelerated = aitken_delta_squared(sequence)

    assert np.allclose(accelerated, exact, atol=1e-12)


def test_steffensen_method_converges_faster_than_plain_fixed_point() -> None:
    plain = fixed_point_iteration(math.cos, 0.5, tolerance=1e-12, max_iterations=100)
    accelerated = steffensen_method(math.cos, 0.5, tolerance=1e-12, max_iterations=20)

    assert accelerated.converged
    assert abs(accelerated.root - 0.7390851332151607) < 1e-12
    assert accelerated.iterations < plain.iterations


def test_steffensen_rejects_zero_aitken_denominator() -> None:
    with pytest.raises(ValueError):
        steffensen_method(lambda x: x + 1.0, 0.0)


def test_newton_method_solves_quadratic_equation() -> None:
    result = newton_method(lambda x: x**2 - 2.0, lambda x: 2.0 * x, 1.5, tolerance=1e-12)

    assert result.converged
    assert abs(result.root - math.sqrt(2.0)) < 1e-12
    assert result.iterations <= 5


def test_damped_newton_backtracks_large_initial_step() -> None:
    func = lambda x: x**3 - 1.0
    derivative = lambda x: 3.0 * x**2

    result = damped_newton_method(func, derivative, 0.1, tolerance=1e-12, max_iterations=50)

    assert result.converged
    assert abs(result.root - 1.0) < 1e-10
    assert abs(func(result.history[1])) < abs(func(result.history[0]))


def test_modified_newton_handles_known_multiple_root() -> None:
    func = lambda x: (x - 2.0) ** 3
    derivative = lambda x: 3.0 * (x - 2.0) ** 2

    plain = newton_method(func, derivative, 3.5, tolerance=1e-8, max_iterations=100)
    modified = modified_newton_method(func, derivative, 3.5, multiplicity=3, tolerance=1e-12)

    assert plain.converged
    assert modified.converged
    assert abs(modified.root - 2.0) < 1e-12
    assert modified.iterations < plain.iterations


def test_newton_rejects_zero_derivative() -> None:
    with pytest.raises(ValueError):
        newton_method(lambda x: x**3 + 1.0, lambda x: 3.0 * x**2, 0.0)


def test_secant_method_solves_cos_fixed_point_equation() -> None:
    result = secant_method(lambda x: math.cos(x) - x, 0.0, 1.0, tolerance=1e-12)

    assert result.converged
    assert abs(result.root - 0.7390851332151607) < 1e-12
    assert result.iterations < 10


def test_secant_rejects_repeated_function_values() -> None:
    with pytest.raises(ValueError):
        secant_method(lambda x: x**2 + 1.0, -1.0, 1.0)


def test_muller_method_solves_cubic_equation() -> None:
    result = muller_method(lambda x: x**3 - x - 2.0, 0.0, 1.0, 2.0, tolerance=1e-12)

    assert result.converged
    assert abs(result.root - 1.5213797068045676) < 1e-11
    assert result.residual < 1e-11


def test_real_muller_rejects_negative_discriminant() -> None:
    with pytest.raises(ValueError):
        muller_method(lambda x: x**2 + 1.0, -1.0, 0.0, 1.0)
