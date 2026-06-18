from __future__ import annotations

import numpy as np
import pytest

from py_sc import (
    block_gauss_seidel_iteration,
    block_jacobi_iteration,
    conjugate_gradient,
    gauss_seidel_iteration,
    gauss_seidel_iteration_matrix,
    is_strictly_diagonally_dominant,
    is_symmetric_positive_definite,
    jacobi_preconditioner,
    jacobi_iteration,
    jacobi_iteration_matrix,
    poisson_2d_dirichlet_matrix,
    poisson_2d_matvec,
    poisson_2d_rhs,
    preconditioned_conjugate_gradient,
    relative_residual,
    reshape_poisson_solution,
    scan_sor_omega,
    sor_iteration,
    sor_iteration_matrix,
    steepest_descent,
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


def test_sor_solves_system_and_matches_gauss_seidel_when_omega_is_one() -> None:
    A = np.array(
        [
            [4.0, -1.0, 0.0],
            [-1.0, 4.0, -1.0],
            [0.0, -1.0, 4.0],
        ]
    )
    b = np.array([2.0, 4.0, 6.0])
    exact = np.linalg.solve(A, b)

    sor = sor_iteration(A, b, omega=1.15, tolerance=1e-10, max_iterations=200)
    gs = gauss_seidel_iteration(A, b, tolerance=1e-10, max_iterations=200)
    sor_as_gs = sor_iteration(A, b, omega=1.0, tolerance=1e-10, max_iterations=200)

    assert sor.converged
    np.testing.assert_allclose(sor.value, exact, atol=1e-9)
    np.testing.assert_allclose(sor_as_gs.value, gs.value, atol=1e-12)
    assert spectral_radius(sor_iteration_matrix(A, 1.0)) == pytest.approx(
        spectral_radius(gauss_seidel_iteration_matrix(A))
    )


def test_sor_omega_scan_returns_convergence_rows() -> None:
    A = np.array([[4.0, -1.0], [-1.0, 4.0]])
    b = np.array([1.0, 2.0])

    rows = scan_sor_omega(A, b, np.array([0.8, 1.0, 1.2]), tolerance=1e-10, max_iterations=100)

    assert len(rows) == 3
    assert all(row[2] for row in rows)
    assert all(row[3] < 1e-10 for row in rows)


def test_block_iterations_solve_system() -> None:
    A = np.array(
        [
            [5.0, -1.0, 0.0, 0.0],
            [-1.0, 5.0, -1.0, 0.0],
            [0.0, -1.0, 5.0, -1.0],
            [0.0, 0.0, -1.0, 5.0],
        ]
    )
    b = np.array([1.0, 2.0, 3.0, 4.0])
    exact = np.linalg.solve(A, b)

    block_j = block_jacobi_iteration(A, b, [2, 2], tolerance=1e-10, max_iterations=200)
    block_gs = block_gauss_seidel_iteration(A, b, [2, 2], tolerance=1e-10, max_iterations=200)

    assert block_j.converged
    assert block_gs.converged
    np.testing.assert_allclose(block_j.value, exact, atol=1e-9)
    np.testing.assert_allclose(block_gs.value, exact, atol=1e-9)


def test_sor_rejects_invalid_omega() -> None:
    A = np.eye(2)
    b = np.ones(2)

    with pytest.raises(ValueError):
        sor_iteration(A, b, omega=2.0)


def test_steepest_descent_cg_and_pcg_solve_spd_system() -> None:
    A = np.array(
        [
            [6.0, 2.0, 0.0],
            [2.0, 5.0, 1.0],
            [0.0, 1.0, 4.0],
        ]
    )
    b = np.array([1.0, 2.0, 3.0])
    exact = np.linalg.solve(A, b)

    sd = steepest_descent(A, b, tolerance=1e-10, max_iterations=200)
    cg = conjugate_gradient(A, b, tolerance=1e-12, max_iterations=10)
    pcg = preconditioned_conjugate_gradient(A, b, tolerance=1e-12, max_iterations=10)

    assert sd.converged
    assert cg.converged
    assert pcg.converged
    np.testing.assert_allclose(sd.value, exact, atol=1e-9)
    np.testing.assert_allclose(cg.value, exact, atol=1e-11)
    np.testing.assert_allclose(pcg.value, exact, atol=1e-11)
    assert cg.iterations <= A.shape[0]


def test_jacobi_preconditioner_returns_inverse_diagonal() -> None:
    A = np.diag([2.0, 4.0, 5.0])

    np.testing.assert_allclose(jacobi_preconditioner(A), np.array([0.5, 0.25, 0.2]))


def test_cg_rejects_non_spd_matrix() -> None:
    A = np.array([[1.0, 2.0], [3.0, 1.0]])
    b = np.ones(2)

    with pytest.raises(ValueError):
        conjugate_gradient(A, b)


def test_poisson_matrix_matches_matvec() -> None:
    A, _ = poisson_2d_dirichlet_matrix(4)
    vector = np.arange(16, dtype=float)

    np.testing.assert_allclose(poisson_2d_matvec(vector, 4), A @ vector, atol=1e-12)


def test_poisson_manufactured_solution_with_cg() -> None:
    n = 8
    A, _ = poisson_2d_dirichlet_matrix(n)
    rhs, x, y = poisson_2d_rhs(
        n,
        lambda xx, yy: 2.0 * np.pi**2 * np.sin(np.pi * xx) * np.sin(np.pi * yy),
    )
    exact_grid = np.sin(np.pi * x) * np.sin(np.pi * y)

    result = conjugate_gradient(A, rhs, tolerance=1e-10, max_iterations=n * n)
    numerical = reshape_poisson_solution(result.value, n)

    assert result.converged
    assert np.max(np.abs(numerical - exact_grid)) < 1.5e-2


def test_poisson_matvec_rejects_wrong_length() -> None:
    with pytest.raises(ValueError):
        poisson_2d_matvec(np.ones(3), 2)
