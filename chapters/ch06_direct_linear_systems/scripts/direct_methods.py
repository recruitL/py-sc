"""第六章线性方程组直接方法示例脚本。

本脚本是 Notebook 实验的紧凑版本，用于快速检查核心算法是否能运行。
Notebook 中仍保留教学式推导和实现。
"""

from __future__ import annotations

import pathlib
import sys
import time

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import (  # noqa: E402
    cholesky_factorization,
    cholesky_solve,
    classical_gram_schmidt,
    gaussian_elimination,
    gaussian_elimination_partial_pivoting,
    householder_qr,
    ldlt_factorization,
    ldlt_solve,
    lu_solve,
    modified_gram_schmidt,
    orthogonality_error,
    plu_factorization,
    thomas_algorithm,
)
from py_sc.direct_linear import relative_forward_error, relative_residual  # noqa: E402


def pivoting_demo() -> tuple[np.ndarray, np.ndarray]:
    """返回不选主元和选主元在小主元例子上的解。"""

    A = np.array([[1e-16, 1.0], [1.0, 1.0]])
    b = np.array([1.0, 2.0])
    try:
        no_pivot = gaussian_elimination(A, b, tol=0.0)
    except ValueError:
        no_pivot = np.array([np.nan, np.nan])
    pivot = gaussian_elimination_partial_pivoting(A, b)
    return no_pivot, pivot


def plu_demo() -> float:
    """返回 PLU 分解重构误差。"""

    A = np.array([[0.0, 2.0, 1.0], [2.0, 2.0, 3.0], [4.0, -1.0, 2.0]])
    factorization = plu_factorization(A)
    return float(np.linalg.norm(A[factorization.permutation, :] - factorization.L @ factorization.U))


def spd_demo() -> tuple[float, float]:
    """比较 Cholesky 和 LDLT 解的残差。"""

    rng = np.random.default_rng(2026)
    R = rng.normal(size=(5, 5))
    A = R.T @ R + np.eye(5)
    x_exact = rng.normal(size=5)
    b = A @ x_exact
    L = cholesky_factorization(A)
    x_chol = cholesky_solve(L, b)
    L_ldlt, D = ldlt_factorization(A)
    x_ldlt = ldlt_solve(L_ldlt, D, b)
    return relative_residual(A, x_chol, b), relative_residual(A, x_ldlt, b)


def tridiagonal_timing() -> list[tuple[int, float, float]]:
    """粗略比较追赶法和 dense solve 的运行时间。"""

    rows = []
    for n in [200, 500, 1000]:
        lower = -np.ones(n - 1)
        diagonal = 4.0 * np.ones(n)
        upper = -np.ones(n - 1)
        b = np.ones(n)
        A = np.diag(diagonal) + np.diag(lower, -1) + np.diag(upper, 1)

        t0 = time.perf_counter()
        thomas_algorithm(lower, diagonal, upper, b)
        thomas_time = time.perf_counter() - t0

        t0 = time.perf_counter()
        np.linalg.solve(A, b)
        dense_time = time.perf_counter() - t0
        rows.append((n, thomas_time, dense_time))
    return rows


def qr_demo() -> dict[str, tuple[float, float]]:
    """返回不同 QR 方法的重构误差和正交性误差。"""

    A = np.array([[1.0, 1.0, 1.0], [1.0, 1.0 + 1e-8, 2.0], [1.0, 2.0, 3.0], [1.0, 3.0, 5.0]])
    results = {}
    for name, factor in [
        ("classical_gs", classical_gram_schmidt),
        ("modified_gs", modified_gram_schmidt),
        ("householder", householder_qr),
    ]:
        Q, R = factor(A)
        results[name] = (float(np.linalg.norm(Q @ R - A)), orthogonality_error(Q))
    return results


def hilbert_demo() -> tuple[float, float, float]:
    """返回 Hilbert 矩阵上的条件数、相对残差和前向误差。"""

    n = 10
    i = np.arange(1, n + 1)
    H = 1.0 / (i[:, None] + i[None, :] - 1.0)
    x_exact = np.ones(n)
    b = H @ x_exact
    x = gaussian_elimination_partial_pivoting(H, b)
    return float(np.linalg.cond(H)), relative_residual(H, x, b), relative_forward_error(x, x_exact)


def main() -> None:
    no_pivot, pivot = pivoting_demo()
    print("小主元例子：")
    print("不选主元：", no_pivot)
    print("部分选主元：", pivot)

    print("\nPLU 重构误差:", f"{plu_demo():.3e}")

    chol_residual, ldlt_residual = spd_demo()
    print("\nSPD 求解残差：")
    print("Cholesky:", f"{chol_residual:.3e}")
    print("LDLT:", f"{ldlt_residual:.3e}")

    print("\n三对角系统时间比较：")
    print("n      Thomas(s)       dense solve(s)")
    for n, thomas_time, dense_time in tridiagonal_timing():
        print(f"{n:<6d} {thomas_time: .3e}      {dense_time: .3e}")

    print("\nQR 重构误差和正交性误差：")
    for name, (reconstruct, orthogonal) in qr_demo().items():
        print(f"{name:14s} reconstruct={reconstruct:.3e}, orthogonality={orthogonal:.3e}")

    condition, residual, forward = hilbert_demo()
    print("\nHilbert 病态矩阵：")
    print(f"cond={condition:.3e}, relative residual={residual:.3e}, relative forward error={forward:.3e}")


if __name__ == "__main__":
    main()
