"""第七章示例中使用的线性方程组迭代算法。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LinearIterationResult:
    """线性迭代法的结果和残差历史。"""

    value: np.ndarray
    iterations: int
    converged: bool
    residual_norms: np.ndarray


def relative_residual(A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
    """计算相对残差 ``||b - A x||_2 / ||b||_2``。"""

    A, b = _as_linear_system(A, b)
    x = _as_vector(x, "x")
    if x.size != b.size:
        raise ValueError("x and b must have the same length")
    denominator = np.linalg.norm(b)
    if denominator == 0:
        denominator = 1.0
    return float(np.linalg.norm(b - A @ x) / denominator)


def spectral_radius(matrix: np.ndarray) -> float:
    """返回矩阵谱半径。"""

    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    return float(np.max(np.abs(np.linalg.eigvals(matrix))))


def jacobi_iteration_matrix(A: np.ndarray) -> np.ndarray:
    """Jacobi 迭代矩阵 ``B_J = -D^{-1}(L+U)``。"""

    A = _as_square_matrix(A)
    diagonal = np.diag(A)
    if np.any(diagonal == 0):
        raise ValueError("Jacobi iteration requires nonzero diagonal entries")
    remainder = A - np.diag(diagonal)
    return -remainder / diagonal[:, None]


def gauss_seidel_iteration_matrix(A: np.ndarray) -> np.ndarray:
    """Gauss-Seidel 迭代矩阵 ``B_GS = -(D+L)^{-1}U``。"""

    A = _as_square_matrix(A)
    lower = np.tril(A)
    upper = np.triu(A, 1)
    if np.any(np.diag(lower) == 0):
        raise ValueError("Gauss-Seidel iteration requires nonzero diagonal entries")
    return -np.linalg.solve(lower, upper)


def jacobi_iteration(
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray | None = None,
    tolerance: float = 1e-8,
    max_iterations: int = 500,
) -> LinearIterationResult:
    """Jacobi 迭代法求解 ``Ax=b``。"""

    A, b = _as_linear_system(A, b)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    diagonal = np.diag(A)
    if np.any(diagonal == 0):
        raise ValueError("Jacobi iteration requires nonzero diagonal entries")
    x = _initial_guess(b, x0)
    remainder = A - np.diag(diagonal)

    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0
    for k in range(1, max_iterations + 1):
        x = (b - remainder @ x) / diagonal
        residuals.append(relative_residual(A, x, b))
        iterations = k
        if residuals[-1] <= tolerance:
            converged = True
            break

    return LinearIterationResult(
        value=x,
        iterations=iterations,
        converged=converged,
        residual_norms=np.array(residuals, dtype=float),
    )


def gauss_seidel_iteration(
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray | None = None,
    tolerance: float = 1e-8,
    max_iterations: int = 500,
) -> LinearIterationResult:
    """Gauss-Seidel 迭代法求解 ``Ax=b``。"""

    A, b = _as_linear_system(A, b)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    if np.any(np.diag(A) == 0):
        raise ValueError("Gauss-Seidel iteration requires nonzero diagonal entries")
    x = _initial_guess(b, x0)

    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0
    for k in range(1, max_iterations + 1):
        x_old = x.copy()
        for i in range(b.size):
            left = A[i, :i] @ x[:i]
            right = A[i, i + 1 :] @ x_old[i + 1 :]
            x[i] = (b[i] - left - right) / A[i, i]
        residuals.append(relative_residual(A, x, b))
        iterations = k
        if residuals[-1] <= tolerance:
            converged = True
            break

    return LinearIterationResult(
        value=x,
        iterations=iterations,
        converged=converged,
        residual_norms=np.array(residuals, dtype=float),
    )


def is_strictly_diagonally_dominant(A: np.ndarray) -> bool:
    """判断矩阵是否严格行对角占优。"""

    A = _as_square_matrix(A)
    diagonal = np.abs(np.diag(A))
    off_diagonal = np.sum(np.abs(A), axis=1) - diagonal
    return bool(np.all(diagonal > off_diagonal))


def is_symmetric_positive_definite(A: np.ndarray, tolerance: float = 1e-12) -> bool:
    """用对称性和 Cholesky 分解检查小规模矩阵是否为 SPD。"""

    A = _as_square_matrix(A)
    if not np.allclose(A, A.T, atol=tolerance, rtol=0.0):
        return False
    try:
        np.linalg.cholesky(A)
    except np.linalg.LinAlgError:
        return False
    return True


def _iterate_fixed_point(
    step: Callable[[np.ndarray], np.ndarray],
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray,
    tolerance: float,
    max_iterations: int,
) -> LinearIterationResult:
    """内部通用迭代器，供后续方法复用。"""

    x = x0.astype(float, copy=True)
    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0
    for k in range(1, max_iterations + 1):
        x = np.asarray(step(x), dtype=float)
        residuals.append(relative_residual(A, x, b))
        iterations = k
        if residuals[-1] <= tolerance:
            converged = True
            break
    return LinearIterationResult(
        value=x,
        iterations=iterations,
        converged=converged,
        residual_norms=np.array(residuals, dtype=float),
    )


def _as_linear_system(A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    A = _as_square_matrix(A)
    b = _as_vector(b, "b")
    if A.shape[0] != b.size:
        raise ValueError("A and b dimensions do not match")
    return A, b


def _as_square_matrix(A: np.ndarray) -> np.ndarray:
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be a square matrix")
    return A


def _as_vector(value: np.ndarray, name: str) -> np.ndarray:
    value = np.asarray(value, dtype=float)
    if value.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    return value


def _initial_guess(b: np.ndarray, x0: np.ndarray | None) -> np.ndarray:
    if x0 is None:
        return np.zeros_like(b, dtype=float)
    x0 = _as_vector(x0, "x0")
    if x0.size != b.size:
        raise ValueError("x0 and b must have the same length")
    return x0.copy()


def _validate_tolerance(tolerance: float) -> float:
    tolerance = float(tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    return tolerance


def _validate_positive_int(value: int, name: str) -> int:
    value = int(value)
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value
