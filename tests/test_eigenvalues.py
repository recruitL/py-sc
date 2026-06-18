from __future__ import annotations

import numpy as np
import pytest

from py_sc import (
    eigen_residual_norm,
    inverse_power_method,
    normalize_vector,
    power_method,
    rayleigh_quotient,
    rayleigh_quotient_iteration,
)


def test_rayleigh_quotient_matches_known_vector_value() -> None:
    matrix = np.diag([2.0, 4.0])
    vector = np.array([1.0, 1.0])

    assert rayleigh_quotient(matrix, vector) == pytest.approx(3.0)


def test_power_method_finds_dominant_symmetric_eigenpair() -> None:
    matrix = np.array([[4.0, 1.0], [1.0, 3.0]])

    result = power_method(matrix, initial=[1.0, 0.5], tolerance=1e-12)
    expected = max(np.linalg.eigvalsh(matrix))

    assert result.converged
    assert result.eigenvalue == pytest.approx(expected, rel=1e-10, abs=1e-10)
    assert result.residual_norm < 1e-10
    assert np.linalg.norm(result.eigenvector) == pytest.approx(1.0)
    assert result.eigenvalue_history.size == result.residual_history.size


def test_power_method_rejects_zero_initial_vector() -> None:
    with pytest.raises(ValueError):
        power_method(np.eye(2), initial=[0.0, 0.0])


def test_inverse_power_method_finds_eigenvalue_near_shift() -> None:
    matrix = np.diag([5.0, 2.0, -1.0])

    result = inverse_power_method(matrix, shift=1.7, initial=[1.0, 1.0, 1.0], tolerance=1e-12)

    assert result.converged
    assert result.eigenvalue == pytest.approx(2.0, abs=1e-10)
    assert result.residual_norm < 1e-10


def test_inverse_power_method_reports_singular_shift() -> None:
    with pytest.raises(ValueError):
        inverse_power_method(np.diag([1.0, 2.0]), shift=1.0, initial=[1.0, 1.0])


def test_rayleigh_quotient_iteration_converges_quickly_for_symmetric_matrix() -> None:
    matrix = np.array([[2.0, 1.0], [1.0, 2.0]])

    result = rayleigh_quotient_iteration(matrix, initial=[0.9, 1.0], tolerance=1e-13)

    assert result.converged
    assert result.eigenvalue == pytest.approx(3.0, abs=1e-12)
    assert result.residual_norm < 1e-12
    assert result.iterations <= 5


def test_eigen_residual_norm_is_small_for_exact_eigenpair() -> None:
    matrix = np.array([[0.0, 1.0], [1.0, 0.0]])
    vector = normalize_vector([1.0, 1.0])

    assert eigen_residual_norm(matrix, 1.0, vector) < 1e-14


def test_eigenvalue_routines_validate_square_matrix() -> None:
    with pytest.raises(ValueError):
        rayleigh_quotient(np.ones((2, 3)), [1.0, 1.0, 1.0])
