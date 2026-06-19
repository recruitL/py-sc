"""第六章示例中使用的线性方程组直接求解算法。"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PLUFactorization:
    """带部分选主元的 LU 分解结果。

    ``permutation`` 是行置换向量，并满足 ``A[permutation, :] = L @ U``。
    """

    permutation: np.ndarray
    L: np.ndarray
    U: np.ndarray


def forward_substitution(L: np.ndarray, b: np.ndarray, unit_diagonal: bool = False, tol: float = 1e-14) -> np.ndarray:
    """求解下三角方程组 ``L x = b``。

    ``b`` 可以是一维向量，也可以是多个右端项组成的二维数组。
    """

    L = _as_square_matrix(L)
    rhs, was_vector = _as_rhs(b, L.shape[0])
    n = L.shape[0]
    x = np.zeros_like(rhs, dtype=float)

    for i in range(n):
        pivot = 1.0 if unit_diagonal else L[i, i]
        if abs(pivot) <= tol:
            raise ValueError("zero or tiny diagonal entry in forward substitution")
        x[i] = (rhs[i] - L[i, :i] @ x[:i]) / pivot

    return _restore_rhs_shape(x, was_vector)


def backward_substitution(U: np.ndarray, b: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """求解上三角方程组 ``U x = b``。"""

    U = _as_square_matrix(U)
    rhs, was_vector = _as_rhs(b, U.shape[0])
    n = U.shape[0]
    x = np.zeros_like(rhs, dtype=float)

    for i in range(n - 1, -1, -1):
        pivot = U[i, i]
        if abs(pivot) <= tol:
            raise ValueError("zero or tiny diagonal entry in backward substitution")
        x[i] = (rhs[i] - U[i, i + 1 :] @ x[i + 1 :]) / pivot

    return _restore_rhs_shape(x, was_vector)


def gaussian_elimination(A: np.ndarray, b: np.ndarray, pivoting: bool = False, tol: float = 1e-14) -> np.ndarray:
    """用高斯消元求解 ``A x = b``。

    当 ``pivoting=True`` 时使用部分选主元。函数会复制输入，不会原地修改 ``A`` 或 ``b``。
    """

    U = _as_square_matrix(A).copy()
    rhs, was_vector = _as_rhs(b, U.shape[0])
    rhs = rhs.copy()
    n = U.shape[0]

    for k in range(n - 1):
        if pivoting:
            pivot_row = k + int(np.argmax(np.abs(U[k:, k])))
            if abs(U[pivot_row, k]) <= tol:
                raise ValueError("matrix is singular to working precision")
            if pivot_row != k:
                U[[k, pivot_row], :] = U[[pivot_row, k], :]
                rhs[[k, pivot_row], :] = rhs[[pivot_row, k], :]
        elif abs(U[k, k]) <= tol:
            raise ValueError("zero or tiny pivot encountered; use pivoting")

        for i in range(k + 1, n):
            multiplier = U[i, k] / U[k, k]
            U[i, k:] -= multiplier * U[k, k:]
            rhs[i] -= multiplier * rhs[k]

    return _restore_rhs_shape(backward_substitution(U, rhs, tol=tol), was_vector)


def gaussian_elimination_partial_pivoting(A: np.ndarray, b: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """部分选主元高斯消元。"""

    return gaussian_elimination(A, b, pivoting=True, tol=tol)


def lu_doolittle(A: np.ndarray, tol: float = 1e-14) -> tuple[np.ndarray, np.ndarray]:
    """Doolittle LU 分解，不选主元，返回 ``(L, U)``。

    ``L`` 的对角元为 1。若主元为零或过小，函数会失败。
    """

    A = _as_square_matrix(A)
    n = A.shape[0]
    L = np.eye(n, dtype=float)
    U = np.zeros_like(A, dtype=float)

    for k in range(n):
        U[k, k:] = A[k, k:] - L[k, :k] @ U[:k, k:]
        if abs(U[k, k]) <= tol:
            raise ValueError("zero or tiny pivot encountered in LU factorization")
        for i in range(k + 1, n):
            L[i, k] = (A[i, k] - L[i, :k] @ U[:k, k]) / U[k, k]

    return L, U


def plu_factorization(A: np.ndarray, tol: float = 1e-14) -> PLUFactorization:
    """部分选主元 LU 分解，满足 ``A[p, :] = L @ U``。"""

    U = _as_square_matrix(A).copy()
    n = U.shape[0]
    L = np.eye(n, dtype=float)
    permutation = np.arange(n)

    for k in range(n - 1):
        pivot_row = k + int(np.argmax(np.abs(U[k:, k])))
        if abs(U[pivot_row, k]) <= tol:
            raise ValueError("matrix is singular to working precision")
        if pivot_row != k:
            U[[k, pivot_row], k:] = U[[pivot_row, k], k:]
            if k > 0:
                L[[k, pivot_row], :k] = L[[pivot_row, k], :k]
            permutation[[k, pivot_row]] = permutation[[pivot_row, k]]

        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]

    if abs(U[-1, -1]) <= tol:
        raise ValueError("matrix is singular to working precision")

    return PLUFactorization(permutation=permutation, L=L, U=U)


def lu_solve(L: np.ndarray, U: np.ndarray, b: np.ndarray, permutation: np.ndarray | None = None, tol: float = 1e-14) -> np.ndarray:
    """由 LU 或 PLU 分解结果求解线性方程组。"""

    L = _as_square_matrix(L)
    U = _as_square_matrix(U)
    if L.shape != U.shape:
        raise ValueError("L and U must have the same shape")
    rhs, was_vector = _as_rhs(b, L.shape[0])
    if permutation is not None:
        permutation = np.asarray(permutation, dtype=int)
        if permutation.shape != (L.shape[0],):
            raise ValueError("permutation must have shape (n,)")
        rhs = rhs[permutation]

    y = forward_substitution(L, rhs, unit_diagonal=True, tol=tol)
    x = backward_substitution(U, y, tol=tol)
    return _restore_rhs_shape(np.asarray(x, dtype=float), was_vector)


def cholesky_factorization(A: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """对称正定矩阵的 Cholesky 分解，返回 ``L``，满足 ``A = L @ L.T``。"""

    A = _as_symmetric_matrix(A)
    n = A.shape[0]
    L = np.zeros_like(A, dtype=float)

    for j in range(n):
        diagonal = A[j, j] - np.dot(L[j, :j], L[j, :j])
        if diagonal <= tol:
            raise ValueError("matrix is not positive definite")
        L[j, j] = np.sqrt(diagonal)
        for i in range(j + 1, n):
            L[i, j] = (A[i, j] - np.dot(L[i, :j], L[j, :j])) / L[j, j]

    return L


def cholesky_solve(L: np.ndarray, b: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """由 Cholesky 因子求解 ``L L.T x = b``。"""

    y = forward_substitution(L, b, tol=tol)
    return backward_substitution(np.asarray(L, dtype=float).T, y, tol=tol)


def ldlt_factorization(A: np.ndarray, tol: float = 1e-14) -> tuple[np.ndarray, np.ndarray]:
    """对称正定矩阵的 ``L D L.T`` 分解。

    返回单位下三角矩阵 ``L`` 和一维对角数组 ``D``。
    """

    A = _as_symmetric_matrix(A)
    n = A.shape[0]
    L = np.eye(n, dtype=float)
    D = np.zeros(n, dtype=float)

    for j in range(n):
        if j == 0:
            correction = 0.0
        else:
            correction = np.sum((L[j, :j] ** 2) * D[:j])
        D[j] = A[j, j] - correction
        if D[j] <= tol:
            raise ValueError("matrix is not positive definite")
        for i in range(j + 1, n):
            numerator = A[i, j] - np.sum(L[i, :j] * L[j, :j] * D[:j])
            L[i, j] = numerator / D[j]

    return L, D


def ldlt_solve(L: np.ndarray, D: np.ndarray, b: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """由 ``L D L.T`` 分解求解线性方程组。"""

    D = np.asarray(D, dtype=float)
    if D.ndim != 1:
        raise ValueError("D must be a one-dimensional diagonal array")
    y = forward_substitution(L, b, unit_diagonal=True, tol=tol)
    y2, was_vector = _as_rhs(y, D.size)
    if np.any(np.abs(D) <= tol):
        raise ValueError("zero or tiny diagonal entry in D")
    z = y2 / D[:, None]
    x = backward_substitution(np.asarray(L, dtype=float).T, z, tol=tol)
    return _restore_rhs_shape(np.asarray(x, dtype=float), was_vector)


def thomas_algorithm(
    lower: np.ndarray,
    diagonal: np.ndarray,
    upper: np.ndarray,
    rhs: np.ndarray,
    tol: float = 1e-14,
) -> np.ndarray:
    """三对角方程组的追赶法。

    ``lower`` 和 ``upper`` 长度为 ``n-1``，``diagonal`` 长度为 ``n``。
    """

    lower = np.asarray(lower, dtype=float)
    diagonal = np.asarray(diagonal, dtype=float)
    upper = np.asarray(upper, dtype=float)
    n = diagonal.size
    if lower.shape != (n - 1,) or upper.shape != (n - 1,):
        raise ValueError("lower and upper must have length n-1")
    rhs_matrix, was_vector = _as_rhs(rhs, n)

    c_prime = np.zeros(n - 1, dtype=float)
    d_prime = np.zeros_like(rhs_matrix, dtype=float)
    pivot = diagonal[0]
    if abs(pivot) <= tol:
        raise ValueError("zero or tiny pivot in Thomas algorithm")
    if n > 1:
        c_prime[0] = upper[0] / pivot
    d_prime[0] = rhs_matrix[0] / pivot

    for i in range(1, n):
        pivot = diagonal[i] - lower[i - 1] * c_prime[i - 1]
        if abs(pivot) <= tol:
            raise ValueError("zero or tiny pivot in Thomas algorithm")
        if i < n - 1:
            c_prime[i] = upper[i] / pivot
        d_prime[i] = (rhs_matrix[i] - lower[i - 1] * d_prime[i - 1]) / pivot

    x = np.zeros_like(rhs_matrix, dtype=float)
    x[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]

    return _restore_rhs_shape(x, was_vector)


def classical_gram_schmidt(A: np.ndarray, tol: float = 1e-14) -> tuple[np.ndarray, np.ndarray]:
    """经典 Gram-Schmidt QR 分解。"""

    A = _as_2d_array(A)
    m, n = A.shape
    Q = np.zeros((m, n), dtype=float)
    R = np.zeros((n, n), dtype=float)

    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            R[i, j] = np.dot(Q[:, i], A[:, j])
            v -= R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        if R[j, j] <= tol:
            raise ValueError("columns are linearly dependent to working precision")
        Q[:, j] = v / R[j, j]

    return Q, R


def modified_gram_schmidt(A: np.ndarray, tol: float = 1e-14) -> tuple[np.ndarray, np.ndarray]:
    """修正 Gram-Schmidt QR 分解。"""

    A = _as_2d_array(A)
    m, n = A.shape
    V = A.copy()
    Q = np.zeros((m, n), dtype=float)
    R = np.zeros((n, n), dtype=float)

    for i in range(n):
        R[i, i] = np.linalg.norm(V[:, i])
        if R[i, i] <= tol:
            raise ValueError("columns are linearly dependent to working precision")
        Q[:, i] = V[:, i] / R[i, i]
        for j in range(i + 1, n):
            R[i, j] = np.dot(Q[:, i], V[:, j])
            V[:, j] -= R[i, j] * Q[:, i]

    return Q, R


def householder_qr(A: np.ndarray, tol: float = 1e-14) -> tuple[np.ndarray, np.ndarray]:
    """Householder QR 分解，返回完整 ``Q`` 和 ``R``。"""

    A = _as_2d_array(A)
    m, n = A.shape
    R = A.copy()
    Q = np.eye(m, dtype=float)

    for k in range(min(m, n)):
        x = R[k:, k]
        norm_x = np.linalg.norm(x)
        if norm_x <= tol:
            continue
        sign = -1.0 if x[0] < 0 else 1.0
        v = x.copy()
        v[0] += sign * norm_x
        v_norm = np.linalg.norm(v)
        if v_norm <= tol:
            continue
        v /= v_norm

        R[k:, k:] -= 2.0 * np.outer(v, v @ R[k:, k:])
        Q[:, k:] -= 2.0 * np.outer(Q[:, k:] @ v, v)

    R[np.abs(R) < 10 * tol] = 0.0
    return Q, R


def givens_qr(A: np.ndarray, tol: float = 1e-14) -> tuple[np.ndarray, np.ndarray]:
    """Givens 旋转 QR 分解，返回完整 ``Q`` 和 ``R``。"""

    A = _as_2d_array(A)
    m, n = A.shape
    R = A.copy()
    Q = np.eye(m, dtype=float)

    for j in range(n):
        for i in range(m - 1, j, -1):
            a = R[j, j]
            b = R[i, j]
            if abs(b) <= tol:
                continue
            radius = np.hypot(a, b)
            c = a / radius
            s = b / radius
            G = np.eye(m, dtype=float)
            G[j, j] = c
            G[i, i] = c
            G[j, i] = s
            G[i, j] = -s
            R = G @ R
            Q = Q @ G.T

    R[np.abs(R) < 10 * tol] = 0.0
    return Q, R


def qr_solve(Q: np.ndarray, R: np.ndarray, b: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """由 QR 分解求解方阵线性方程组。"""

    Q = _as_2d_array(Q)
    R = _as_2d_array(R)
    if Q.shape[0] != Q.shape[1]:
        raise ValueError("Q must be square")
    n = R.shape[1]
    rhs, was_vector = _as_rhs(b, Q.shape[0])
    y = Q.T @ rhs
    x = backward_substitution(R[:n, :], y[:n], tol=tol)
    return _restore_rhs_shape(np.asarray(x, dtype=float), was_vector)


def relative_residual(A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
    """计算相对残差 ``||b - A x||_2 / ||b||_2``。"""

    A = _as_2d_array(A)
    x = np.asarray(x, dtype=float)
    b = np.asarray(b, dtype=float)
    residual = b - A @ x
    denominator = np.linalg.norm(b)
    if denominator == 0:
        return float(np.linalg.norm(residual))
    return float(np.linalg.norm(residual) / denominator)


def relative_forward_error(x_computed: np.ndarray, x_exact: np.ndarray) -> float:
    """计算相对前向误差 ``||x_hat - x||_2 / ||x||_2``。"""

    x_computed = np.asarray(x_computed, dtype=float)
    x_exact = np.asarray(x_exact, dtype=float)
    denominator = np.linalg.norm(x_exact)
    if denominator == 0:
        return float(np.linalg.norm(x_computed - x_exact))
    return float(np.linalg.norm(x_computed - x_exact) / denominator)


def orthogonality_error(Q: np.ndarray) -> float:
    """计算 ``||Q.T Q - I||_F``。"""

    Q = _as_2d_array(Q)
    return float(np.linalg.norm(Q.T @ Q - np.eye(Q.shape[1]), ord="fro"))


def _as_square_matrix(A: np.ndarray) -> np.ndarray:
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("expected a square matrix")
    return A


def _as_symmetric_matrix(A: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    A = _as_square_matrix(A)
    if not np.allclose(A, A.T, atol=tol, rtol=tol):
        raise ValueError("expected a symmetric matrix")
    return A


def _as_2d_array(A: np.ndarray) -> np.ndarray:
    A = np.asarray(A, dtype=float)
    if A.ndim != 2:
        raise ValueError("expected a two-dimensional array")
    return A


def _as_rhs(b: np.ndarray, n: int) -> tuple[np.ndarray, bool]:
    b = np.asarray(b, dtype=float)
    if b.ndim == 1:
        if b.shape[0] != n:
            raise ValueError("right-hand side has incompatible length")
        return b.reshape(n, 1), True
    if b.ndim == 2 and b.shape[0] == n:
        return b, False
    raise ValueError("right-hand side must have shape (n,) or (n, m)")


def _restore_rhs_shape(x: np.ndarray, was_vector: bool) -> np.ndarray:
    return x[:, 0] if was_vector else x
