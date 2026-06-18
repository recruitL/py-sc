from __future__ import annotations

import math

import numpy as np
import pytest

from py_sc import (
    broyden_system_method,
    chord_newton_system_method,
    parameter_continuation,
    damped_newton_system_method,
    finite_difference_jacobian,
    fixed_point_system_iteration,
    newton_system_method,
)


def test_fixed_point_system_iteration_solves_contraction() -> None:
    def iteration(x: np.ndarray) -> np.ndarray:
        return np.array([0.5 * math.cos(x[1]), 0.5 * math.sin(x[0])])

    def residual(x: np.ndarray) -> np.ndarray:
        return x - iteration(x)

    result = fixed_point_system_iteration(iteration, [0.3, 0.2], tolerance=1e-12, residual_func=residual)

    assert result.converged
    assert result.residual_norm < 1e-11
    assert result.history.shape[1] == 2
    assert result.residual_history[-1] <= result.residual_history[0]


def test_newton_system_method_solves_circle_line_system() -> None:
    def func(x: np.ndarray) -> np.ndarray:
        return np.array([x[0] ** 2 + x[1] ** 2 - 1.0, x[0] - x[1]])

    def jacobian(x: np.ndarray) -> np.ndarray:
        return np.array([[2.0 * x[0], 2.0 * x[1]], [1.0, -1.0]])

    result = newton_system_method(func, jacobian, [0.8, 0.6], tolerance=1e-12)
    expected = np.array([1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)])

    assert result.converged
    assert np.allclose(result.solution, expected, atol=1e-12)
    assert result.residual_norm < 1e-12
    assert result.iterations <= 6


def test_newton_system_method_rejects_singular_jacobian() -> None:
    def func(x: np.ndarray) -> np.ndarray:
        return np.array([x[0] ** 2 + 1.0, x[1]])

    def jacobian(x: np.ndarray) -> np.ndarray:
        return np.array([[2.0 * x[0], 0.0], [0.0, 1.0]])

    with pytest.raises(ValueError):
        newton_system_method(func, jacobian, [0.0, 0.0])


def test_finite_difference_jacobian_matches_analytic_jacobian() -> None:
    def func(x: np.ndarray) -> np.ndarray:
        return np.array([x[0] ** 2 + x[1] ** 2 - 1.0, x[0] - x[1]])

    point = np.array([0.7, 0.6])
    expected = np.array([[1.4, 1.2], [1.0, -1.0]])

    actual = finite_difference_jacobian(func, point)

    assert np.allclose(actual, expected, atol=1e-7)


def test_damped_newton_system_method_backtracks_and_converges() -> None:
    def func(x: np.ndarray) -> np.ndarray:
        return np.array([x[0] ** 3 - 1.0, x[1]])

    def jacobian(x: np.ndarray) -> np.ndarray:
        return np.array([[3.0 * x[0] ** 2, 0.0], [0.0, 1.0]])

    result = damped_newton_system_method(func, jacobian, [0.1, 0.5], tolerance=1e-12)

    assert result.converged
    assert np.allclose(result.solution, [1.0, 0.0], atol=1e-10)
    assert result.residual_norm < 1e-10
    assert result.residual_history[1] < result.residual_history[0]


def test_chord_newton_system_method_uses_fixed_jacobian() -> None:
    def func(x: np.ndarray) -> np.ndarray:
        return np.array([x[0] ** 2 + x[1] ** 2 - 1.0, x[0] - x[1]])

    def jacobian(x: np.ndarray) -> np.ndarray:
        return np.array([[2.0 * x[0], 2.0 * x[1]], [1.0, -1.0]])

    result = chord_newton_system_method(func, jacobian, [0.8, 0.6], tolerance=1e-10, max_iterations=40)
    expected = np.array([1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)])

    assert result.converged
    assert np.allclose(result.solution, expected, atol=1e-8)
    assert result.iterations >= 2


def test_broyden_system_method_solves_circle_line_system() -> None:
    def func(x: np.ndarray) -> np.ndarray:
        return np.array([x[0] ** 2 + x[1] ** 2 - 1.0, x[0] - x[1]])

    result = broyden_system_method(func, [0.8, 0.6], tolerance=1e-10, max_iterations=30)
    expected = np.array([1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)])

    assert result.converged
    assert np.allclose(result.solution, expected, atol=1e-8)
    assert result.residual_norm < 1e-8


def test_parameter_continuation_tracks_solution_branch() -> None:
    def system(parameter: float, x: np.ndarray) -> np.ndarray:
        return np.array([x[0] ** 2 - parameter, x[1] - parameter])

    parameters = np.array([1.0, 1.5, 2.0, 2.5])
    result = parameter_continuation(system, parameters, initial=[1.0, 1.0], tolerance=1e-10)

    assert result.converged
    assert np.allclose(result.solutions[:, 0], np.sqrt(parameters), atol=1e-8)
    assert np.allclose(result.solutions[:, 1], parameters, atol=1e-8)
    assert np.max(result.residual_norms) < 1e-8
