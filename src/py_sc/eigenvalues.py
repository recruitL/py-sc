"""第十章示例中使用的特征值迭代算法。"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EigenIterationResult:
    """特征值迭代结果。"""

    eigenvalue: float
    eigenvector: np.ndarray
    iterations: int
    converged: bool
    residual_norm: float
    eigenvalue_history: np.ndarray
    residual_history: np.ndarray


def rayleigh_quotient(
    matrix: np.ndarray | list[list[float]] | tuple[tuple[float, ...], ...],
    vector: np.ndarray | list[float] | tuple[float, ...],
) -> float:
    """计算 Rayleigh 商 ``(x^T A x)/(x^T x)``。"""

    a = _as_square_matrix(matrix)
    x = _as_vector(vector, "vector")
    _validate_matrix_vector_dimension(a, x)
    denominator = float(np.dot(x, x))
    if denominator == 0.0:
        raise ValueError("vector must be nonzero")
    return float(np.dot(x, a @ x) / denominator)


def eigen_residual_norm(
    matrix: np.ndarray | list[list[float]] | tuple[tuple[float, ...], ...],
    eigenvalue: float,
    eigenvector: np.ndarray | list[float] | tuple[float, ...],
) -> float:
    """计算特征对残差 ``||A x - lambda x||_2``。"""

    a = _as_square_matrix(matrix)
    x = _as_vector(eigenvector, "eigenvector")
    _validate_matrix_vector_dimension(a, x)
    return float(np.linalg.norm(a @ x - float(eigenvalue) * x, ord=2))


def normalize_vector(vector: np.ndarray | list[float] | tuple[float, ...]) -> np.ndarray:
    """返回二范数归一化后的向量。"""

    x = _as_vector(vector, "vector")
    norm = float(np.linalg.norm(x, ord=2))
    if norm == 0.0:
        raise ValueError("vector must be nonzero")
    return x / norm


def power_method(
    matrix: np.ndarray | list[list[float]] | tuple[tuple[float, ...], ...],
    initial: np.ndarray | list[float] | tuple[float, ...] | None = None,
    tolerance: float = 1e-10,
    max_iterations: int = 100,
) -> EigenIterationResult:
    """用幂法近似模最大特征值及其特征向量。"""

    a = _as_square_matrix(matrix)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x = _initial_vector(a.shape[0], initial)
    matrix_scale = max(1.0, float(np.linalg.norm(a, ord=2)))
    eigenvalue = rayleigh_quotient(a, x)
    residual = eigen_residual_norm(a, eigenvalue, x)
    eigenvalue_history = [eigenvalue]
    residual_history = [residual]
    converged = residual <= tolerance * matrix_scale
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        y = a @ x
        x = normalize_vector(y)
        eigenvalue = rayleigh_quotient(a, x)
        residual = eigen_residual_norm(a, eigenvalue, x)
        eigenvalue_history.append(eigenvalue)
        residual_history.append(residual)
        iterations = k
        if residual <= tolerance * matrix_scale:
            converged = True
            break

    return EigenIterationResult(
        eigenvalue=float(eigenvalue),
        eigenvector=x.copy(),
        iterations=iterations,
        converged=bool(converged),
        residual_norm=float(residual),
        eigenvalue_history=np.array(eigenvalue_history, dtype=float),
        residual_history=np.array(residual_history, dtype=float),
    )


def inverse_power_method(
    matrix: np.ndarray | list[list[float]] | tuple[tuple[float, ...], ...],
    shift: float = 0.0,
    initial: np.ndarray | list[float] | tuple[float, ...] | None = None,
    tolerance: float = 1e-10,
    max_iterations: int = 100,
) -> EigenIterationResult:
    """用带位移的反幂法近似最接近 ``shift`` 的特征值。"""

    a = _as_square_matrix(matrix)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x = _initial_vector(a.shape[0], initial)
    shifted = a - float(shift) * np.eye(a.shape[0])
    matrix_scale = max(1.0, float(np.linalg.norm(a, ord=2)))
    eigenvalue = rayleigh_quotient(a, x)
    residual = eigen_residual_norm(a, eigenvalue, x)
    eigenvalue_history = [eigenvalue]
    residual_history = [residual]
    converged = residual <= tolerance * matrix_scale
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        try:
            y = np.linalg.solve(shifted, x)
        except np.linalg.LinAlgError as exc:
            raise ValueError("shifted matrix is singular") from exc
        x = normalize_vector(y)
        eigenvalue = rayleigh_quotient(a, x)
        residual = eigen_residual_norm(a, eigenvalue, x)
        eigenvalue_history.append(eigenvalue)
        residual_history.append(residual)
        iterations = k
        if residual <= tolerance * matrix_scale:
            converged = True
            break

    return EigenIterationResult(
        eigenvalue=float(eigenvalue),
        eigenvector=x.copy(),
        iterations=iterations,
        converged=bool(converged),
        residual_norm=float(residual),
        eigenvalue_history=np.array(eigenvalue_history, dtype=float),
        residual_history=np.array(residual_history, dtype=float),
    )


def rayleigh_quotient_iteration(
    matrix: np.ndarray | list[list[float]] | tuple[tuple[float, ...], ...],
    initial: np.ndarray | list[float] | tuple[float, ...] | None = None,
    tolerance: float = 1e-12,
    max_iterations: int = 30,
) -> EigenIterationResult:
    """Rayleigh 商迭代，用动态位移快速逼近对称矩阵的特征对。"""

    a = _as_square_matrix(matrix)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x = _initial_vector(a.shape[0], initial)
    matrix_scale = max(1.0, float(np.linalg.norm(a, ord=2)))
    eigenvalue = rayleigh_quotient(a, x)
    residual = eigen_residual_norm(a, eigenvalue, x)
    eigenvalue_history = [eigenvalue]
    residual_history = [residual]
    converged = residual <= tolerance * matrix_scale
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        shifted = a - eigenvalue * np.eye(a.shape[0])
        try:
            y = np.linalg.solve(shifted, x)
        except np.linalg.LinAlgError as exc:
            x = _smallest_singular_vector(shifted)
            eigenvalue = rayleigh_quotient(a, x)
            residual = eigen_residual_norm(a, eigenvalue, x)
            eigenvalue_history.append(eigenvalue)
            residual_history.append(residual)
            iterations = k
            if residual <= tolerance * matrix_scale:
                converged = True
                break
            raise ValueError("Rayleigh shifted matrix is singular") from exc
        x = normalize_vector(y)
        eigenvalue = rayleigh_quotient(a, x)
        residual = eigen_residual_norm(a, eigenvalue, x)
        eigenvalue_history.append(eigenvalue)
        residual_history.append(residual)
        iterations = k
        if residual <= tolerance * matrix_scale:
            converged = True
            break

    return EigenIterationResult(
        eigenvalue=float(eigenvalue),
        eigenvector=x.copy(),
        iterations=iterations,
        converged=bool(converged),
        residual_norm=float(residual),
        eigenvalue_history=np.array(eigenvalue_history, dtype=float),
        residual_history=np.array(residual_history, dtype=float),
    )


def _as_square_matrix(matrix: np.ndarray | list[list[float]] | tuple[tuple[float, ...], ...]) -> np.ndarray:
    a = np.array(matrix, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("matrix must be square")
    return a


def _as_vector(vector: np.ndarray | list[float] | tuple[float, ...], name: str) -> np.ndarray:
    x = np.array(vector, dtype=float)
    if x.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    return x


def _initial_vector(
    size: int,
    initial: np.ndarray | list[float] | tuple[float, ...] | None,
) -> np.ndarray:
    if initial is None:
        x = np.ones(size, dtype=float)
    else:
        x = _as_vector(initial, "initial")
    if x.size != size:
        raise ValueError("initial vector dimension must match matrix")
    return normalize_vector(x)


def _validate_matrix_vector_dimension(matrix: np.ndarray, vector: np.ndarray) -> None:
    if matrix.shape[1] != vector.size:
        raise ValueError("matrix and vector dimensions do not match")


def _validate_tolerance(tolerance: float) -> float:
    tolerance = float(tolerance)
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    return tolerance


def _validate_positive_int(value: int, name: str) -> int:
    value = int(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _smallest_singular_vector(matrix: np.ndarray) -> np.ndarray:
    _, _, vh = np.linalg.svd(matrix)
    return normalize_vector(vh[-1, :])
