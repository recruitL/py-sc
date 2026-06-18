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


def sor_iteration(
    A: np.ndarray,
    b: np.ndarray,
    omega: float,
    x0: np.ndarray | None = None,
    tolerance: float = 1e-8,
    max_iterations: int = 500,
) -> LinearIterationResult:
    """逐次超松弛（SOR）迭代法求解 ``Ax=b``。"""

    A, b = _as_linear_system(A, b)
    omega = _validate_omega(omega)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    if np.any(np.diag(A) == 0):
        raise ValueError("SOR iteration requires nonzero diagonal entries")
    x = _initial_guess(b, x0)

    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0
    for k in range(1, max_iterations + 1):
        x_old = x.copy()
        for i in range(b.size):
            left = A[i, :i] @ x[:i]
            right = A[i, i + 1 :] @ x_old[i + 1 :]
            gs_value = (b[i] - left - right) / A[i, i]
            x[i] = (1.0 - omega) * x_old[i] + omega * gs_value
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


def sor_iteration_matrix(A: np.ndarray, omega: float) -> np.ndarray:
    """SOR 迭代矩阵。"""

    A = _as_square_matrix(A)
    omega = _validate_omega(omega)
    D = np.diag(np.diag(A))
    L = np.tril(A, -1)
    U = np.triu(A, 1)
    left = D + omega * L
    right = (1.0 - omega) * D - omega * U
    return np.linalg.solve(left, right)


def scan_sor_omega(
    A: np.ndarray,
    b: np.ndarray,
    omega_values: np.ndarray,
    tolerance: float = 1e-8,
    max_iterations: int = 500,
) -> list[tuple[float, int, bool, float]]:
    """扫描一组 SOR 松弛因子，返回 ``(omega, iterations, converged, residual)``。"""

    rows: list[tuple[float, int, bool, float]] = []
    for omega in np.asarray(omega_values, dtype=float):
        result = sor_iteration(A, b, omega, tolerance=tolerance, max_iterations=max_iterations)
        rows.append((float(omega), result.iterations, result.converged, float(result.residual_norms[-1])))
    return rows


def block_jacobi_iteration(
    A: np.ndarray,
    b: np.ndarray,
    block_sizes: list[int] | tuple[int, ...],
    x0: np.ndarray | None = None,
    tolerance: float = 1e-8,
    max_iterations: int = 500,
) -> LinearIterationResult:
    """块 Jacobi 迭代法。"""

    A, b = _as_linear_system(A, b)
    blocks = _block_slices(block_sizes, b.size)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x = _initial_guess(b, x0)

    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0
    for k in range(1, max_iterations + 1):
        old = x.copy()
        new = old.copy()
        for block in blocks:
            rhs = b[block] - A[block, :] @ old + A[block, block] @ old[block]
            new[block] = np.linalg.solve(A[block, block], rhs)
        x = new
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


def block_gauss_seidel_iteration(
    A: np.ndarray,
    b: np.ndarray,
    block_sizes: list[int] | tuple[int, ...],
    x0: np.ndarray | None = None,
    tolerance: float = 1e-8,
    max_iterations: int = 500,
) -> LinearIterationResult:
    """块 Gauss-Seidel 迭代法。"""

    A, b = _as_linear_system(A, b)
    blocks = _block_slices(block_sizes, b.size)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x = _initial_guess(b, x0)

    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0
    for k in range(1, max_iterations + 1):
        old = x.copy()
        for block in blocks:
            rhs = b[block] - A[block, :] @ x + A[block, block] @ x[block]
            # 尚未更新的后续块仍应使用上一轮值。
            stop = block.stop
            if stop < b.size:
                tail = slice(stop, b.size)
                rhs -= A[block, tail] @ (old[tail] - x[tail])
            x[block] = np.linalg.solve(A[block, block], rhs)
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


def steepest_descent(
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray | None = None,
    tolerance: float = 1e-8,
    max_iterations: int = 500,
) -> LinearIterationResult:
    """最速下降法求解 SPD 线性系统。"""

    A, b = _as_linear_system(A, b)
    _require_spd(A)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x = _initial_guess(b, x0)
    r = b - A @ x
    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0

    for k in range(1, max_iterations + 1):
        Ar = A @ r
        alpha = float((r @ r) / (r @ Ar))
        x = x + alpha * r
        r = b - A @ x
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


def conjugate_gradient(
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray | None = None,
    tolerance: float = 1e-8,
    max_iterations: int | None = None,
) -> LinearIterationResult:
    """共轭梯度法求解 SPD 线性系统。"""

    A, b = _as_linear_system(A, b)
    _require_spd(A)
    tolerance = _validate_tolerance(tolerance)
    if max_iterations is None:
        max_iterations = b.size
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x = _initial_guess(b, x0)
    r = b - A @ x
    p = r.copy()
    rr_old = float(r @ r)

    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0
    for k in range(1, max_iterations + 1):
        Ap = A @ p
        denom = float(p @ Ap)
        if denom <= 0:
            raise ValueError("conjugate gradient requires a positive curvature direction")
        alpha = rr_old / denom
        x = x + alpha * p
        r = r - alpha * Ap
        residuals.append(relative_residual(A, x, b))
        iterations = k
        if residuals[-1] <= tolerance:
            converged = True
            break
        rr_new = float(r @ r)
        beta = rr_new / rr_old
        p = r + beta * p
        rr_old = rr_new

    return LinearIterationResult(
        value=x,
        iterations=iterations,
        converged=converged,
        residual_norms=np.array(residuals, dtype=float),
    )


def jacobi_preconditioner(A: np.ndarray) -> np.ndarray:
    """返回 Jacobi 对角预处理器的逆对角向量。"""

    A = _as_square_matrix(A)
    diagonal = np.diag(A)
    if np.any(diagonal == 0):
        raise ValueError("Jacobi preconditioner requires nonzero diagonal entries")
    return 1.0 / diagonal


def preconditioned_conjugate_gradient(
    A: np.ndarray,
    b: np.ndarray,
    preconditioner: np.ndarray | Callable[[np.ndarray], np.ndarray] | None = None,
    x0: np.ndarray | None = None,
    tolerance: float = 1e-8,
    max_iterations: int | None = None,
) -> LinearIterationResult:
    """预处理共轭梯度法。

    ``preconditioner`` 可以是逆对角向量，也可以是执行 ``z=M^{-1}r`` 的函数。
    若为 ``None``，使用 Jacobi 对角预处理。
    """

    A, b = _as_linear_system(A, b)
    _require_spd(A)
    tolerance = _validate_tolerance(tolerance)
    if max_iterations is None:
        max_iterations = b.size
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    apply_preconditioner = _preconditioner_solver(A, preconditioner)

    x = _initial_guess(b, x0)
    r = b - A @ x
    z = apply_preconditioner(r)
    p = z.copy()
    rz_old = float(r @ z)

    residuals = [relative_residual(A, x, b)]
    converged = residuals[-1] <= tolerance
    iterations = 0
    for k in range(1, max_iterations + 1):
        Ap = A @ p
        denom = float(p @ Ap)
        if denom <= 0:
            raise ValueError("PCG requires a positive curvature direction")
        alpha = rz_old / denom
        x = x + alpha * p
        r = r - alpha * Ap
        residuals.append(relative_residual(A, x, b))
        iterations = k
        if residuals[-1] <= tolerance:
            converged = True
            break
        z = apply_preconditioner(r)
        rz_new = float(r @ z)
        beta = rz_new / rz_old
        p = z + beta * p
        rz_old = rz_new

    return LinearIterationResult(
        value=x,
        iterations=iterations,
        converged=converged,
        residual_norms=np.array(residuals, dtype=float),
    )


def poisson_2d_dirichlet_matrix(grid_size: int) -> tuple[np.ndarray, float]:
    """构造二维 Poisson 方程零 Dirichlet 边界的五点差分矩阵。

    ``grid_size`` 是每个方向上的内部网格点数量。本函数返回小规模教学验证用的
    稠密矩阵和网格步长；大规模问题应使用稀疏矩阵或矩阵-向量乘法。
    """

    n = _validate_positive_int(grid_size, "grid_size")
    h = 1.0 / (n + 1)
    size = n * n
    A = np.zeros((size, size), dtype=float)
    for i in range(n):
        for j in range(n):
            row = i * n + j
            A[row, row] = 4.0 / h**2
            if i > 0:
                A[row, (i - 1) * n + j] = -1.0 / h**2
            if i + 1 < n:
                A[row, (i + 1) * n + j] = -1.0 / h**2
            if j > 0:
                A[row, i * n + (j - 1)] = -1.0 / h**2
            if j + 1 < n:
                A[row, i * n + (j + 1)] = -1.0 / h**2
    return A, h


def poisson_2d_matvec(vector: np.ndarray, grid_size: int) -> np.ndarray:
    """零 Dirichlet 边界五点差分矩阵的矩阵-向量乘法。"""

    n = _validate_positive_int(grid_size, "grid_size")
    vector = _as_vector(vector, "vector")
    if vector.size != n * n:
        raise ValueError("vector length must be grid_size**2")
    h = 1.0 / (n + 1)
    u = vector.reshape(n, n)
    result = 4.0 * u.copy()
    result[:-1, :] -= u[1:, :]
    result[1:, :] -= u[:-1, :]
    result[:, :-1] -= u[:, 1:]
    result[:, 1:] -= u[:, :-1]
    return (result / h**2).reshape(-1)


def poisson_2d_rhs(
    grid_size: int,
    source: Callable[[np.ndarray, np.ndarray], np.ndarray],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """在内部网格上采样 Poisson 方程右端项。"""

    n = _validate_positive_int(grid_size, "grid_size")
    h = 1.0 / (n + 1)
    points = np.linspace(h, 1.0 - h, n)
    x, y = np.meshgrid(points, points, indexing="ij")
    values = np.asarray(source(x, y), dtype=float)
    if values.shape != (n, n):
        raise ValueError("source must return an array with shape (grid_size, grid_size)")
    return values.reshape(-1), x, y


def reshape_poisson_solution(vector: np.ndarray, grid_size: int) -> np.ndarray:
    """把 Poisson 内部点向量还原为二维网格数组。"""

    n = _validate_positive_int(grid_size, "grid_size")
    vector = _as_vector(vector, "vector")
    if vector.size != n * n:
        raise ValueError("vector length must be grid_size**2")
    return vector.reshape(n, n)


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


def _validate_omega(omega: float) -> float:
    omega = float(omega)
    if not 0.0 < omega < 2.0:
        raise ValueError("omega must satisfy 0 < omega < 2 for SOR")
    return omega


def _block_slices(block_sizes: list[int] | tuple[int, ...], n: int) -> list[slice]:
    if not block_sizes:
        raise ValueError("block_sizes must be non-empty")
    sizes = [int(size) for size in block_sizes]
    if any(size < 1 for size in sizes):
        raise ValueError("all block sizes must be positive")
    if sum(sizes) != n:
        raise ValueError("block sizes must sum to the system dimension")
    blocks = []
    start = 0
    for size in sizes:
        stop = start + size
        blocks.append(slice(start, stop))
        start = stop
    return blocks


def _require_spd(A: np.ndarray) -> None:
    if not is_symmetric_positive_definite(A):
        raise ValueError("method requires a symmetric positive definite matrix")


def _preconditioner_solver(
    A: np.ndarray,
    preconditioner: np.ndarray | Callable[[np.ndarray], np.ndarray] | None,
) -> Callable[[np.ndarray], np.ndarray]:
    if preconditioner is None:
        inverse_diagonal = jacobi_preconditioner(A)
        return lambda r: inverse_diagonal * r
    if callable(preconditioner):
        return lambda r: np.asarray(preconditioner(r), dtype=float)
    inverse_diagonal = _as_vector(preconditioner, "preconditioner")
    if inverse_diagonal.size != A.shape[0]:
        raise ValueError("preconditioner vector length must match A")
    return lambda r: inverse_diagonal * r
