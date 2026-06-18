from __future__ import annotations

import numpy as np
import pytest

from py_sc import (
    gauss_seidel_iteration,
    gauss_seidel_iteration_matrix,
    is_strictly_diagonally_dominant,
    is_symmetric_positive_definite,
    jacobi_iteration,
    jacobi_iteration_matrix,
    relative_residual,
    spectral_radius,
)


def test_jacobi_and_gauss_seidel_solve_diagonally_dominant_system() -> None:
    A = np.array(
        [
            [4.0, -1.0, 0.0],
            [-1.0, 4.0, -1.0],
            [0.0, -1.0, 4.0],
        ]
    )
    b = np.array([2.0, 4.0, 6.0])
    exact = np.linalg.solve(A, b)

    jacobi = jacobi_iteration(A, b, tolerance=1e-10, max_iterations=200)
    gauss_seidel = gauss_seidel_iteration(A, b, tolerance=1e-10, max_iterations=200)

    assert jacobi.converged
    assert gauss_seidel.converged
    np.testing.assert_allclose(jacobi.value, exact, atol=1e-9)
    np.testing.assert_allclose(gauss_seidel.value, exact, atol=1e-9)
    assert gauss_seidel.iterations < jacobi.iterations
    assert relative_residual(A, jacobi.value, b) < 1e-10


def test_iteration_matrices_have_expected_spectral_radius() -> None:
    A = np.array([[4.0, -1.0], [-1.0, 4.0]])

    rho_j = spectral_radius(jacobi_iteration_matrix(A))
    rho_gs = spectral_radius(gauss_seidel_iteration_matrix(A))

    assert abs(rho_j - 0.25) < 1e-14
    assert abs(rho_gs - 0.0625) < 1e-14


def test_matrix_condition_helpers() -> None:
    A = np.array([[3.0, -1.0], [-1.0, 3.0]])
    B = np.array([[1.0, 3.0], [2.0, 1.0]])

    assert is_strictly_diagonally_dominant(A)
    assert is_symmetric_positive_definite(A)
    assert not is_strictly_diagonally_dominant(B)
    assert not is_symmetric_positive_definite(B)


def test_jacobi_rejects_zero_diagonal() -> None:
    A = np.array([[0.0, 1.0], [1.0, 2.0]])
    b = np.array([1.0, 2.0])

    with pytest.raises(ValueError):
        jacobi_iteration(A, b)
