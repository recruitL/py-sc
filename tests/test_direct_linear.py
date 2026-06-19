from __future__ import annotations

import numpy as np
import pytest

from py_sc import (
    backward_substitution,
    cholesky_factorization,
    cholesky_solve,
    classical_gram_schmidt,
    forward_substitution,
    gaussian_elimination,
    gaussian_elimination_partial_pivoting,
    givens_qr,
    householder_qr,
    ldlt_factorization,
    ldlt_solve,
    lu_doolittle,
    lu_solve,
    modified_gram_schmidt,
    orthogonality_error,
    plu_factorization,
    qr_solve,
    relative_forward_error,
    thomas_algorithm,
)
from py_sc.direct_linear import relative_residual as direct_relative_residual


def test_triangular_substitution_supports_multiple_rhs() -> None:
    L = np.array([[2.0, 0.0, 0.0], [1.0, 3.0, 0.0], [-1.0, 2.0, 4.0]])
    U = np.array([[2.0, -1.0, 3.0], [0.0, 4.0, 1.0], [0.0, 0.0, -2.0]])
    x_true = np.array([[1.0, 2.0], [-1.0, 0.5], [0.25, -0.75]])

    y = forward_substitution(L, L @ x_true)
    x = backward_substitution(U, U @ x_true)

    np.testing.assert_allclose(y, x_true)
    np.testing.assert_allclose(x, x_true)


def test_gaussian_elimination_partial_pivoting_handles_zero_pivot() -> None:
    A = np.array([[0.0, 2.0], [1.0, 1.0]])
    b = np.array([2.0, 2.0])

    with pytest.raises(ValueError):
        gaussian_elimination(A, b)

    x = gaussian_elimination_partial_pivoting(A, b)
    np.testing.assert_allclose(x, np.linalg.solve(A, b))


def test_lu_and_plu_factorizations_solve_systems() -> None:
    A = np.array([[4.0, 2.0, 1.0], [2.0, 5.0, 3.0], [1.0, 3.0, 6.0]])
    b = np.array([[1.0, 0.0], [2.0, 1.0], [3.0, -1.0]])

    L, U = lu_doolittle(A)
    np.testing.assert_allclose(L @ U, A)
    np.testing.assert_allclose(lu_solve(L, U, b), np.linalg.solve(A, b))

    B = np.array([[0.0, 2.0, 1.0], [2.0, 2.0, 3.0], [4.0, -1.0, 2.0]])
    factorization = plu_factorization(B)
    np.testing.assert_allclose(factorization.L @ factorization.U, B[factorization.permutation, :])
    np.testing.assert_allclose(
        lu_solve(factorization.L, factorization.U, np.array([1.0, 2.0, 3.0]), factorization.permutation),
        np.linalg.solve(B, np.array([1.0, 2.0, 3.0])),
    )


def test_cholesky_and_ldlt_reconstruct_spd_matrix() -> None:
    R = np.array([[2.0, -1.0, 0.5], [0.0, 1.5, 2.0], [1.0, 0.0, 1.0]])
    A = R.T @ R + np.eye(3)
    b = np.array([1.0, 2.0, -1.0])

    L_chol = cholesky_factorization(A)
    np.testing.assert_allclose(L_chol @ L_chol.T, A)
    np.testing.assert_allclose(cholesky_solve(L_chol, b), np.linalg.solve(A, b))

    L_ldlt, D = ldlt_factorization(A)
    np.testing.assert_allclose(L_ldlt @ np.diag(D) @ L_ldlt.T, A)
    np.testing.assert_allclose(ldlt_solve(L_ldlt, D, b), np.linalg.solve(A, b))

    with pytest.raises(ValueError):
        cholesky_factorization(np.array([[1.0, 2.0], [2.0, 1.0]]))


def test_thomas_algorithm_matches_dense_solve() -> None:
    n = 6
    lower = -np.ones(n - 1)
    diagonal = 4.0 * np.ones(n)
    upper = -np.ones(n - 1)
    A = np.diag(diagonal) + np.diag(lower, -1) + np.diag(upper, 1)
    b = np.arange(1.0, n + 1.0)

    np.testing.assert_allclose(thomas_algorithm(lower, diagonal, upper, b), np.linalg.solve(A, b))


def test_qr_factorizations_reconstruct_and_are_orthogonal() -> None:
    A = np.array([[1.0, 1.0, 1.0], [1.0, 1.0 + 1e-8, 2.0], [1.0, 2.0, 3.0], [1.0, 3.0, 5.0]])

    for factor in [classical_gram_schmidt, modified_gram_schmidt]:
        Q, R = factor(A)
        np.testing.assert_allclose(Q @ R, A, atol=1e-8)
        assert orthogonality_error(Q) < 1e-6

    for factor in [householder_qr, givens_qr]:
        Q, R = factor(A)
        np.testing.assert_allclose(Q @ R, A, atol=1e-10)
        assert orthogonality_error(Q) < 1e-10


def test_qr_solve_and_error_helpers() -> None:
    A = np.array([[3.0, 1.0, -1.0], [2.0, 4.0, 1.0], [-1.0, 2.0, 5.0]])
    x_exact = np.array([1.0, -2.0, 0.5])
    b = A @ x_exact
    Q, R = householder_qr(A)
    x = qr_solve(Q, R, b)

    np.testing.assert_allclose(x, x_exact)
    assert direct_relative_residual(A, x, b) < 1e-14
    assert relative_forward_error(x, x_exact) < 1e-14
