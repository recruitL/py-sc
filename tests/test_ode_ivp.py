from __future__ import annotations

import math

import numpy as np
import pytest

from py_sc import (
    AdaptiveODEResult,
    estimate_convergence_order,
    euler_step,
    global_error,
    heun_euler_embedded_step,
    heun_step,
    midpoint_step,
    rk4_step,
    solve_ivp_adaptive_heun,
    solve_ivp_fixed_step,
)


def exponential_rhs(_time: float, state: np.ndarray) -> np.ndarray:
    return state


def test_euler_step_matches_forward_tangent() -> None:
    actual = euler_step(exponential_rhs, 0.0, 1.0, 0.1)

    assert actual.shape == (1,)
    assert actual[0] == pytest.approx(1.1)


def test_second_order_steps_are_more_accurate_than_euler() -> None:
    exact = math.exp(0.1)
    euler_error = abs(euler_step(exponential_rhs, 0.0, 1.0, 0.1)[0] - exact)
    heun_error = abs(heun_step(exponential_rhs, 0.0, 1.0, 0.1)[0] - exact)
    midpoint_error = abs(midpoint_step(exponential_rhs, 0.0, 1.0, 0.1)[0] - exact)

    assert heun_error < euler_error
    assert midpoint_error < euler_error


def test_rk4_step_is_high_accuracy_for_exponential_growth() -> None:
    actual = rk4_step(exponential_rhs, 0.0, 1.0, 0.1)

    assert actual[0] == pytest.approx(math.exp(0.1), abs=1e-7)


def test_solve_ivp_fixed_step_solves_scalar_problem() -> None:
    result = solve_ivp_fixed_step(exponential_rhs, (0.0, 1.0), 1.0, 0.1, method="rk4")

    assert result.method == "rk4"
    assert result.times[0] == pytest.approx(0.0)
    assert result.times[-1] == pytest.approx(1.0)
    assert result.values.shape == (11, 1)
    assert result.values[-1, 0] == pytest.approx(math.e, abs=3e-6)


def test_solve_ivp_fixed_step_handles_vector_system() -> None:
    def oscillator(_time: float, state: np.ndarray) -> np.ndarray:
        return np.array([state[1], -state[0]])

    result = solve_ivp_fixed_step(oscillator, (0.0, math.pi / 2.0), [1.0, 0.0], math.pi / 200.0, method="rk4")

    assert result.values.shape[1] == 2
    assert np.allclose(result.values[-1], [0.0, -1.0], atol=1e-8)


def test_global_error_compares_against_exact_solution() -> None:
    result = solve_ivp_fixed_step(exponential_rhs, (0.0, 0.5), 1.0, 0.25, method="euler")
    errors = global_error(result.times, result.values, lambda time: math.exp(time))

    assert errors[0] == pytest.approx(0.0)
    assert errors[-1] > 0.0


def test_estimate_convergence_order_detects_euler_order() -> None:
    step_sizes = np.array([0.2, 0.1, 0.05])
    errors = []
    for step_size in step_sizes:
        result = solve_ivp_fixed_step(exponential_rhs, (0.0, 1.0), 1.0, step_size, method="euler")
        errors.append(abs(result.values[-1, 0] - math.e))

    order = estimate_convergence_order(step_sizes, errors)

    assert order == pytest.approx(1.0, rel=0.15)


def test_solve_ivp_fixed_step_rejects_unknown_method() -> None:
    with pytest.raises(ValueError):
        solve_ivp_fixed_step(exponential_rhs, (0.0, 1.0), 1.0, 0.1, method="bogus")


def test_solve_ivp_fixed_step_rejects_invalid_span() -> None:
    with pytest.raises(ValueError):
        solve_ivp_fixed_step(exponential_rhs, (1.0, 0.0), 1.0, 0.1)


def test_heun_euler_embedded_step_returns_error_estimate() -> None:
    high, low, error = heun_euler_embedded_step(exponential_rhs, 0.0, 1.0, 0.1)

    assert high[0] == pytest.approx(1.105)
    assert low[0] == pytest.approx(1.1)
    assert error[0] == pytest.approx(0.005)


def test_solve_ivp_adaptive_heun_solves_scalar_problem() -> None:
    result = solve_ivp_adaptive_heun(
        exponential_rhs,
        (0.0, 1.0),
        1.0,
        initial_step=0.25,
        absolute_tolerance=1e-7,
        relative_tolerance=1e-5,
    )

    assert isinstance(result, AdaptiveODEResult)
    assert result.method == "adaptive_heun"
    assert result.times[-1] == pytest.approx(1.0)
    assert result.values[-1, 0] == pytest.approx(math.e, abs=2e-4)
    assert result.accepted_steps == result.step_sizes.size
    assert np.max(result.error_estimates) <= 1.0


def test_solve_ivp_adaptive_heun_rejects_too_large_initial_step() -> None:
    def fast_rhs(_time: float, state: np.ndarray) -> np.ndarray:
        return 10.0 * state

    result = solve_ivp_adaptive_heun(
        fast_rhs,
        (0.0, 0.2),
        1.0,
        initial_step=0.2,
        absolute_tolerance=1e-8,
        relative_tolerance=1e-6,
    )

    assert result.rejected_steps >= 1
    assert result.values[-1, 0] == pytest.approx(math.exp(2.0), rel=5e-4)


def test_solve_ivp_adaptive_heun_rejects_invalid_tolerances() -> None:
    with pytest.raises(ValueError):
        solve_ivp_adaptive_heun(exponential_rhs, (0.0, 1.0), 1.0, 0.1, absolute_tolerance=0.0)
