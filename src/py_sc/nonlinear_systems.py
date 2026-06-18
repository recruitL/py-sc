"""第九章示例中使用的非线性方程组算法。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


VectorFunction = Callable[[np.ndarray], np.ndarray]
MatrixFunction = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class NonlinearSystemResult:
    """非线性方程组迭代结果。"""

    solution: np.ndarray
    iterations: int
    converged: bool
    residual_norm: float
    history: np.ndarray
    residual_history: np.ndarray


def fixed_point_system_iteration(
    iteration_func: VectorFunction,
    initial: np.ndarray | list[float] | tuple[float, ...],
    tolerance: float = 1e-10,
    max_iterations: int = 100,
    residual_func: VectorFunction | None = None,
) -> NonlinearSystemResult:
    """用向量不动点迭代求解 ``x = iteration_func(x)``。"""

    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_old = _as_vector(initial, "initial")
    history = [x_old.copy()]
    residual_history = [_system_residual_norm(iteration_func, residual_func, x_old)]
    converged = residual_history[-1] <= tolerance
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        x_new = _as_vector(iteration_func(x_old), "iteration result")
        if x_new.shape != x_old.shape:
            raise ValueError("iteration_func must preserve the vector dimension")
        step = np.linalg.norm(x_new - x_old, ord=2)
        residual_norm = _system_residual_norm(iteration_func, residual_func, x_new)
        history.append(x_new.copy())
        residual_history.append(residual_norm)
        iterations = k
        if step <= tolerance * max(1.0, np.linalg.norm(x_new, ord=2)) or residual_norm <= tolerance:
            converged = True
            x_old = x_new
            break
        x_old = x_new

    return NonlinearSystemResult(
        solution=x_old.copy(),
        iterations=iterations,
        converged=bool(converged),
        residual_norm=float(residual_history[-1]),
        history=np.vstack(history),
        residual_history=np.array(residual_history, dtype=float),
    )


def newton_system_method(
    func: VectorFunction,
    jacobian: MatrixFunction,
    initial: np.ndarray | list[float] | tuple[float, ...],
    tolerance: float = 1e-10,
    max_iterations: int = 50,
) -> NonlinearSystemResult:
    """Newton 法求解非线性方程组 ``F(x)=0``。"""

    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_old = _as_vector(initial, "initial")
    residual = _as_vector(func(x_old), "function value")
    _validate_system_dimension(x_old, residual)
    history = [x_old.copy()]
    residual_history = [float(np.linalg.norm(residual, ord=2))]
    converged = residual_history[-1] <= tolerance
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        jac = _as_matrix(jacobian(x_old), "jacobian")
        if jac.shape != (x_old.size, x_old.size):
            raise ValueError("jacobian must be square with shape (n, n)")
        try:
            step = np.linalg.solve(jac, -residual)
        except np.linalg.LinAlgError as exc:
            raise ValueError("Newton linear system is singular") from exc
        x_new = x_old + step
        residual = _as_vector(func(x_new), "function value")
        _validate_system_dimension(x_new, residual)
        residual_norm = float(np.linalg.norm(residual, ord=2))
        history.append(x_new.copy())
        residual_history.append(residual_norm)
        iterations = k
        if residual_norm <= tolerance or np.linalg.norm(step, ord=2) <= tolerance * max(1.0, np.linalg.norm(x_new, ord=2)):
            converged = True
            x_old = x_new
            break
        x_old = x_new

    return NonlinearSystemResult(
        solution=x_old.copy(),
        iterations=iterations,
        converged=bool(converged),
        residual_norm=float(residual_history[-1]),
        history=np.vstack(history),
        residual_history=np.array(residual_history, dtype=float),
    )


def finite_difference_jacobian(
    func: VectorFunction,
    x: np.ndarray | list[float] | tuple[float, ...],
    step: float | None = None,
) -> np.ndarray:
    """用前向差分近似非线性方程组 Jacobian。"""

    x = _as_vector(x, "x")
    f0 = _as_vector(func(x), "function value")
    _validate_system_dimension(x, f0)
    jac = np.empty((x.size, x.size), dtype=float)
    for j in range(x.size):
        h = _finite_difference_step(x[j], step)
        x_step = x.copy()
        x_step[j] += h
        f_step = _as_vector(func(x_step), "function value")
        _validate_system_dimension(x, f_step)
        jac[:, j] = (f_step - f0) / h
    return jac


def damped_newton_system_method(
    func: VectorFunction,
    jacobian: MatrixFunction,
    initial: np.ndarray | list[float] | tuple[float, ...],
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    damping_factor: float = 0.5,
    min_damping: float = 1e-4,
) -> NonlinearSystemResult:
    """带残差回溯的非线性方程组 Newton 法。"""

    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    damping_factor, min_damping = _validate_damping(damping_factor, min_damping)
    x_old = _as_vector(initial, "initial")
    residual = _as_vector(func(x_old), "function value")
    _validate_system_dimension(x_old, residual)
    residual_norm = float(np.linalg.norm(residual, ord=2))
    history = [x_old.copy()]
    residual_history = [residual_norm]
    converged = residual_norm <= tolerance
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        jac = _as_matrix(jacobian(x_old), "jacobian")
        if jac.shape != (x_old.size, x_old.size):
            raise ValueError("jacobian must be square with shape (n, n)")
        try:
            step = np.linalg.solve(jac, -residual)
        except np.linalg.LinAlgError as exc:
            raise ValueError("Newton linear system is singular") from exc
        x_new, residual, residual_norm = _backtracking_system_step(
            func,
            x_old,
            step,
            residual_norm,
            damping_factor,
            min_damping,
        )
        history.append(x_new.copy())
        residual_history.append(residual_norm)
        iterations = k
        if residual_norm <= tolerance or np.linalg.norm(x_new - x_old, ord=2) <= tolerance * max(1.0, np.linalg.norm(x_new, ord=2)):
            converged = True
            x_old = x_new
            break
        x_old = x_new

    return NonlinearSystemResult(
        solution=x_old.copy(),
        iterations=iterations,
        converged=bool(converged),
        residual_norm=float(residual_history[-1]),
        history=np.vstack(history),
        residual_history=np.array(residual_history, dtype=float),
    )


def chord_newton_system_method(
    func: VectorFunction,
    jacobian: MatrixFunction,
    initial: np.ndarray | list[float] | tuple[float, ...],
    tolerance: float = 1e-10,
    max_iterations: int = 50,
) -> NonlinearSystemResult:
    """弦 Newton 法：固定初始 Jacobian 反复求解线性修正。"""

    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_old = _as_vector(initial, "initial")
    fixed_jacobian = _as_matrix(jacobian(x_old), "jacobian")
    if fixed_jacobian.shape != (x_old.size, x_old.size):
        raise ValueError("jacobian must be square with shape (n, n)")
    residual = _as_vector(func(x_old), "function value")
    _validate_system_dimension(x_old, residual)
    history = [x_old.copy()]
    residual_history = [float(np.linalg.norm(residual, ord=2))]
    converged = residual_history[-1] <= tolerance
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        try:
            step = np.linalg.solve(fixed_jacobian, -residual)
        except np.linalg.LinAlgError as exc:
            raise ValueError("chord Newton linear system is singular") from exc
        x_new = x_old + step
        residual = _as_vector(func(x_new), "function value")
        _validate_system_dimension(x_new, residual)
        residual_norm = float(np.linalg.norm(residual, ord=2))
        history.append(x_new.copy())
        residual_history.append(residual_norm)
        iterations = k
        if residual_norm <= tolerance or np.linalg.norm(step, ord=2) <= tolerance * max(1.0, np.linalg.norm(x_new, ord=2)):
            converged = True
            x_old = x_new
            break
        x_old = x_new

    return NonlinearSystemResult(
        solution=x_old.copy(),
        iterations=iterations,
        converged=bool(converged),
        residual_norm=float(residual_history[-1]),
        history=np.vstack(history),
        residual_history=np.array(residual_history, dtype=float),
    )


def _as_vector(values: np.ndarray | list[float] | tuple[float, ...], name: str) -> np.ndarray:
    vector = np.asarray(values, dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be a one-dimensional vector")
    if vector.size == 0:
        raise ValueError(f"{name} must not be empty")
    return vector


def _as_matrix(values: np.ndarray, name: str) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.ndim != 2:
        raise ValueError(f"{name} must be a matrix")
    return matrix


def _validate_system_dimension(x: np.ndarray, residual: np.ndarray) -> None:
    if residual.shape != x.shape:
        raise ValueError("function value must have the same dimension as x")


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


def _system_residual_norm(
    iteration_func: VectorFunction,
    residual_func: VectorFunction | None,
    x: np.ndarray,
) -> float:
    if residual_func is None:
        return float(np.linalg.norm(_as_vector(iteration_func(x), "iteration result") - x, ord=2))
    return float(np.linalg.norm(_as_vector(residual_func(x), "residual value"), ord=2))


def _finite_difference_step(value: float, step: float | None) -> float:
    if step is not None:
        step = float(step)
        if step <= 0:
            raise ValueError("step must be positive")
        return step
    return float(np.sqrt(np.finfo(float).eps) * max(1.0, abs(value)))


def _validate_damping(damping_factor: float, min_damping: float) -> tuple[float, float]:
    damping_factor = float(damping_factor)
    min_damping = _validate_tolerance(min_damping)
    if not 0.0 < damping_factor < 1.0:
        raise ValueError("damping_factor must be in (0, 1)")
    if min_damping > 1.0:
        raise ValueError("min_damping must be no larger than 1")
    return damping_factor, min_damping


def _backtracking_system_step(
    func: VectorFunction,
    x_old: np.ndarray,
    step: np.ndarray,
    current_residual_norm: float,
    damping_factor: float,
    min_damping: float,
) -> tuple[np.ndarray, np.ndarray, float]:
    damping = 1.0
    while damping >= min_damping:
        x_trial = x_old + damping * step
        residual = _as_vector(func(x_trial), "function value")
        _validate_system_dimension(x_old, residual)
        residual_norm = float(np.linalg.norm(residual, ord=2))
        if residual_norm < current_residual_norm:
            return x_trial, residual, residual_norm
        damping *= damping_factor
    raise ValueError("damped Newton failed to reduce residual")
