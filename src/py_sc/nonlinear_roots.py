"""第八章示例中使用的标量非线性方程求根算法。"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


ScalarFunction = Callable[[float], float]


@dataclass(frozen=True)
class ScalarRootResult:
    """标量方程求根结果。"""

    root: float
    iterations: int
    converged: bool
    residual: float
    history: np.ndarray


@dataclass(frozen=True)
class QuadraticFactorResult:
    """多项式二次因子迭代结果。"""

    factor: np.ndarray
    roots: np.ndarray
    iterations: int
    converged: bool
    residual_norm: float
    history: np.ndarray


@dataclass(frozen=True)
class PolynomialRootsResult:
    """多项式全部根计算结果。"""

    roots: np.ndarray
    iterations: int
    converged: bool
    residual_norm: float


def find_sign_change_brackets(
    func: ScalarFunction,
    a: float,
    b: float,
    subintervals: int,
) -> list[tuple[float, float]]:
    """在区间上扫描变号子区间。"""

    a, b = _validate_interval(a, b)
    n = _validate_positive_int(subintervals, "subintervals")
    x = np.linspace(a, b, n + 1)
    values = np.array([_call_scalar(func, xi) for xi in x], dtype=float)
    brackets: list[tuple[float, float]] = []
    for i in range(n):
        f_left = values[i]
        f_right = values[i + 1]
        if f_left == 0:
            brackets.append((float(x[i]), float(x[i])))
        elif f_left * f_right < 0:
            brackets.append((float(x[i]), float(x[i + 1])))
    if values[-1] == 0:
        brackets.append((float(x[-1]), float(x[-1])))
    return brackets


def bisection_method(
    func: ScalarFunction,
    a: float,
    b: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100,
) -> ScalarRootResult:
    """二分法求解有变号括区间内的根。"""

    a, b = _validate_interval(a, b)
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    fa = _call_scalar(func, a)
    fb = _call_scalar(func, b)
    if fa == 0:
        return ScalarRootResult(a, 0, True, 0.0, np.array([a], dtype=float))
    if fb == 0:
        return ScalarRootResult(b, 0, True, 0.0, np.array([b], dtype=float))
    if fa * fb > 0:
        raise ValueError("bisection requires a sign-changing interval")

    history = []
    left = a
    right = b
    f_left = fa
    converged = False
    root = 0.5 * (left + right)
    iterations = 0
    for k in range(1, max_iterations + 1):
        root = 0.5 * (left + right)
        f_mid = _call_scalar(func, root)
        history.append(root)
        iterations = k
        if abs(f_mid) <= tolerance or 0.5 * (right - left) <= tolerance:
            converged = True
            break
        if f_left * f_mid < 0:
            right = root
        else:
            left = root
            f_left = f_mid

    residual = abs(_call_scalar(func, root))
    return ScalarRootResult(
        root=float(root),
        iterations=iterations,
        converged=converged,
        residual=float(residual),
        history=np.array(history, dtype=float),
    )


def fixed_point_iteration(
    iteration_func: ScalarFunction,
    initial: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100,
    residual_func: ScalarFunction | None = None,
) -> ScalarRootResult:
    """用简单不动点迭代求解 ``x = iteration_func(x)``。"""

    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_old = float(initial)
    history = [x_old]
    converged = False
    iterations = 0

    for k in range(1, max_iterations + 1):
        x_new = _call_scalar(iteration_func, x_old)
        history.append(x_new)
        iterations = k
        step = abs(x_new - x_old)
        residual = _fixed_point_residual(iteration_func, residual_func, x_new)
        if step <= tolerance * max(1.0, abs(x_new)) or residual <= tolerance:
            converged = True
            x_old = x_new
            break
        x_old = x_new

    root = float(x_old)
    residual = _fixed_point_residual(iteration_func, residual_func, root)
    return ScalarRootResult(
        root=root,
        iterations=iterations,
        converged=converged,
        residual=float(residual),
        history=np.array(history, dtype=float),
    )


def aitken_delta_squared(
    sequence: np.ndarray | list[float] | tuple[float, ...],
    denominator_tolerance: float = 1e-14,
) -> np.ndarray:
    """对一维序列应用 Aitken ``delta^2`` 加速。"""

    denominator_tolerance = _validate_tolerance(denominator_tolerance)
    values = np.asarray(sequence, dtype=float)
    if values.ndim != 1:
        raise ValueError("sequence must be one-dimensional")
    if values.size < 3:
        raise ValueError("sequence must contain at least three values")
    first_delta = values[1:-1] - values[:-2]
    second_delta = values[2:] - 2.0 * values[1:-1] + values[:-2]
    accelerated = np.full(values.size - 2, np.nan, dtype=float)
    stable = np.abs(second_delta) > denominator_tolerance
    accelerated[stable] = values[:-2][stable] - first_delta[stable] ** 2 / second_delta[stable]
    return accelerated


def steffensen_method(
    iteration_func: ScalarFunction,
    initial: float,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    residual_func: ScalarFunction | None = None,
    denominator_tolerance: float = 1e-14,
) -> ScalarRootResult:
    """用 Steffensen 方法加速不动点迭代。"""

    tolerance = _validate_tolerance(tolerance)
    denominator_tolerance = _validate_tolerance(denominator_tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_old = float(initial)
    history = [x_old]
    converged = False
    iterations = 0

    for k in range(1, max_iterations + 1):
        x1 = _call_scalar(iteration_func, x_old)
        x2 = _call_scalar(iteration_func, x1)
        denominator = x2 - 2.0 * x1 + x_old
        if abs(denominator) <= denominator_tolerance:
            raise ValueError("Steffensen denominator is too small")
        x_new = x_old - (x1 - x_old) ** 2 / denominator
        history.append(x_new)
        iterations = k
        step = abs(x_new - x_old)
        residual = _fixed_point_residual(iteration_func, residual_func, x_new)
        if step <= tolerance * max(1.0, abs(x_new)) or residual <= tolerance:
            converged = True
            x_old = x_new
            break
        x_old = x_new

    root = float(x_old)
    residual = _fixed_point_residual(iteration_func, residual_func, root)
    return ScalarRootResult(
        root=root,
        iterations=iterations,
        converged=converged,
        residual=float(residual),
        history=np.array(history, dtype=float),
    )


def newton_method(
    func: ScalarFunction,
    derivative: ScalarFunction,
    initial: float,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    derivative_tolerance: float = 1e-14,
) -> ScalarRootResult:
    """Newton 法求解标量非线性方程。"""

    tolerance = _validate_tolerance(tolerance)
    derivative_tolerance = _validate_tolerance(derivative_tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_old = float(initial)
    return _newton_core(
        func,
        derivative,
        x_old,
        tolerance,
        max_iterations,
        derivative_tolerance,
        multiplicity=1.0,
        use_damping=False,
    )


def damped_newton_method(
    func: ScalarFunction,
    derivative: ScalarFunction,
    initial: float,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    derivative_tolerance: float = 1e-14,
    damping_factor: float = 0.5,
    min_damping: float = 1e-4,
) -> ScalarRootResult:
    """带回溯阻尼的 Newton 法。"""

    tolerance = _validate_tolerance(tolerance)
    derivative_tolerance = _validate_tolerance(derivative_tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    damping_factor = float(damping_factor)
    min_damping = _validate_tolerance(min_damping)
    if not 0.0 < damping_factor < 1.0:
        raise ValueError("damping_factor must be in (0, 1)")
    if min_damping > 1.0:
        raise ValueError("min_damping must be no larger than 1")
    return _newton_core(
        func,
        derivative,
        float(initial),
        tolerance,
        max_iterations,
        derivative_tolerance,
        multiplicity=1.0,
        use_damping=True,
        damping_factor=damping_factor,
        min_damping=min_damping,
    )


def modified_newton_method(
    func: ScalarFunction,
    derivative: ScalarFunction,
    initial: float,
    multiplicity: int,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    derivative_tolerance: float = 1e-14,
) -> ScalarRootResult:
    """已知根重数时的修正 Newton 法。"""

    tolerance = _validate_tolerance(tolerance)
    derivative_tolerance = _validate_tolerance(derivative_tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    multiplicity = _validate_positive_int(multiplicity, "multiplicity")
    return _newton_core(
        func,
        derivative,
        float(initial),
        tolerance,
        max_iterations,
        derivative_tolerance,
        multiplicity=float(multiplicity),
        use_damping=False,
    )


def secant_method(
    func: ScalarFunction,
    x0: float,
    x1: float,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    denominator_tolerance: float = 1e-14,
) -> ScalarRootResult:
    """弦截法求解标量非线性方程。"""

    tolerance = _validate_tolerance(tolerance)
    denominator_tolerance = _validate_tolerance(denominator_tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    x_prev = float(x0)
    x_curr = float(x1)
    f_prev = _call_scalar(func, x_prev)
    f_curr = _call_scalar(func, x_curr)
    history = [x_prev, x_curr]
    converged = abs(f_curr) <= tolerance
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        denominator = f_curr - f_prev
        if abs(denominator) <= denominator_tolerance:
            raise ValueError("secant denominator is too small")
        x_next = x_curr - f_curr * (x_curr - x_prev) / denominator
        f_next = _call_scalar(func, x_next)
        history.append(x_next)
        iterations = k
        step = abs(x_next - x_curr)
        if abs(f_next) <= tolerance or step <= tolerance * max(1.0, abs(x_next)):
            converged = True
            x_curr = x_next
            f_curr = f_next
            break
        x_prev, f_prev = x_curr, f_curr
        x_curr, f_curr = x_next, f_next

    return ScalarRootResult(
        root=float(x_curr),
        iterations=iterations,
        converged=converged,
        residual=float(abs(f_curr)),
        history=np.array(history, dtype=float),
    )


def muller_method(
    func: ScalarFunction,
    x0: float,
    x1: float,
    x2: float,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    denominator_tolerance: float = 1e-14,
) -> ScalarRootResult:
    """实数 Müller 抛物线法求解标量非线性方程。"""

    tolerance = _validate_tolerance(tolerance)
    denominator_tolerance = _validate_tolerance(denominator_tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    history = [float(x0), float(x1), float(x2)]
    x_prev2, x_prev1, x_curr = history
    f_curr = _call_scalar(func, x_curr)
    converged = abs(f_curr) <= tolerance
    iterations = 0

    for k in range(1, max_iterations + 1):
        if converged:
            break
        x_next = _muller_next(
            func,
            x_prev2,
            x_prev1,
            x_curr,
            denominator_tolerance,
        )
        f_next = _call_scalar(func, x_next)
        history.append(x_next)
        iterations = k
        step = abs(x_next - x_curr)
        if abs(f_next) <= tolerance or step <= tolerance * max(1.0, abs(x_next)):
            converged = True
            x_curr = x_next
            f_curr = f_next
            break
        x_prev2, x_prev1, x_curr = x_prev1, x_curr, x_next
        f_curr = f_next

    return ScalarRootResult(
        root=float(x_curr),
        iterations=iterations,
        converged=converged,
        residual=float(abs(f_curr)),
        history=np.array(history, dtype=float),
    )


def polynomial_value_and_derivative(
    coefficients: np.ndarray | list[complex] | tuple[complex, ...],
    x: complex,
) -> tuple[complex, complex]:
    """用 Horner 格式同时计算多项式及其导数。"""

    coeffs = _validate_polynomial_coefficients(coefficients)
    point = complex(x)
    value = complex(coeffs[0])
    derivative = 0.0j
    for coefficient in coeffs[1:]:
        derivative = derivative * point + value
        value = value * point + complex(coefficient)
    return value, derivative


def synthetic_division(
    coefficients: np.ndarray | list[complex] | tuple[complex, ...],
    root: complex,
) -> tuple[np.ndarray, complex]:
    """用综合除法将多项式除以 ``x - root``。"""

    coeffs = _validate_polynomial_coefficients(coefficients)
    root = complex(root)
    quotient = np.empty(coeffs.size - 1, dtype=complex)
    quotient[0] = coeffs[0]
    for i in range(1, quotient.size):
        quotient[i] = coeffs[i] + root * quotient[i - 1]
    remainder = coeffs[-1] + root * quotient[-1]
    return quotient, complex(remainder)


def newton_polynomial_roots(
    coefficients: np.ndarray | list[complex] | tuple[complex, ...],
    initial_guesses: np.ndarray | list[complex] | tuple[complex, ...] | None = None,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
    derivative_tolerance: float = 1e-14,
) -> PolynomialRootsResult:
    """用 Newton 法和逐次压缩计算多项式全部根。"""

    coeffs = _validate_polynomial_coefficients(coefficients)
    tolerance = _validate_tolerance(tolerance)
    derivative_tolerance = _validate_tolerance(derivative_tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    degree = coeffs.size - 1
    guesses = _initial_polynomial_guesses(coeffs, initial_guesses)
    current = coeffs.astype(complex)
    roots: list[complex] = []
    total_iterations = 0
    converged = True

    for root_index in range(degree):
        z = complex(guesses[root_index])
        local_converged = False
        for _ in range(max_iterations):
            value, derivative = polynomial_value_and_derivative(current, z)
            if abs(value) <= tolerance:
                local_converged = True
                break
            if abs(derivative) <= derivative_tolerance:
                raise ValueError("polynomial Newton derivative is too small")
            z -= value / derivative
            total_iterations += 1
            if abs(value) <= tolerance:
                local_converged = True
                break
        value, _ = polynomial_value_and_derivative(current, z)
        if abs(value) <= tolerance:
            local_converged = True
        roots.append(z)
        current, remainder = synthetic_division(current, z)
        if abs(remainder) > tolerance * max(1.0, np.linalg.norm(coeffs)):
            local_converged = False
        converged = converged and local_converged

    roots_array = np.array(roots, dtype=complex)
    residual_norm = _polynomial_roots_residual_norm(coeffs, roots_array)
    converged = converged and residual_norm <= tolerance * max(1.0, np.linalg.norm(coeffs))
    return PolynomialRootsResult(
        roots=roots_array,
        iterations=total_iterations,
        converged=bool(converged),
        residual_norm=float(residual_norm),
    )


def bairstow_quadratic_factor(
    coefficients: np.ndarray | list[complex] | tuple[complex, ...],
    linear_coefficient: float,
    constant_coefficient: float,
    tolerance: float = 1e-10,
    max_iterations: int = 50,
) -> QuadraticFactorResult:
    """用 Bairstow 型 Newton 迭代寻找实二次因子。"""

    coeffs = _validate_polynomial_coefficients(coefficients)
    if coeffs.size < 3:
        raise ValueError("polynomial degree must be at least two")
    tolerance = _validate_tolerance(tolerance)
    max_iterations = _validate_positive_int(max_iterations, "max_iterations")
    u = complex(linear_coefficient)
    v = complex(constant_coefficient)
    history: list[tuple[complex, complex, float]] = []
    converged = False
    residual_norm = float("inf")
    iterations = 0

    for k in range(1, max_iterations + 1):
        residual = _quadratic_factor_remainder(coeffs, u, v)
        residual_norm = float(np.linalg.norm(residual))
        history.append((u, v, residual_norm))
        if residual_norm <= tolerance * max(1.0, np.linalg.norm(coeffs)):
            converged = True
            iterations = k - 1
            break
        jacobian = _quadratic_remainder_jacobian(coeffs, u, v)
        try:
            delta = np.linalg.solve(jacobian, -residual)
        except np.linalg.LinAlgError as exc:
            raise ValueError("Bairstow Jacobian is singular") from exc
        u += delta[0]
        v += delta[1]
        iterations = k
        if np.linalg.norm(delta) <= tolerance * max(1.0, abs(u), abs(v)):
            residual = _quadratic_factor_remainder(coeffs, u, v)
            residual_norm = float(np.linalg.norm(residual))
            history.append((u, v, residual_norm))
            converged = residual_norm <= tolerance * max(1.0, np.linalg.norm(coeffs))
            break

    factor = np.array([1.0 + 0.0j, u, v], dtype=complex)
    roots = np.roots(factor)
    return QuadraticFactorResult(
        factor=np.real_if_close(factor),
        roots=np.real_if_close(roots),
        iterations=iterations,
        converged=bool(converged),
        residual_norm=float(residual_norm),
        history=np.array(history, dtype=object),
    )


def _validate_interval(a: float, b: float) -> tuple[float, float]:
    a = float(a)
    b = float(b)
    if not a < b:
        raise ValueError("expected a < b")
    return a, b


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


def _call_scalar(func: ScalarFunction, x: float) -> float:
    return float(np.asarray(func(float(x)), dtype=float))


def _fixed_point_residual(
    iteration_func: ScalarFunction,
    residual_func: ScalarFunction | None,
    x: float,
) -> float:
    if residual_func is None:
        return abs(_call_scalar(iteration_func, x) - x)
    return abs(_call_scalar(residual_func, x))


def _newton_core(
    func: ScalarFunction,
    derivative: ScalarFunction,
    initial: float,
    tolerance: float,
    max_iterations: int,
    derivative_tolerance: float,
    multiplicity: float,
    use_damping: bool,
    damping_factor: float = 0.5,
    min_damping: float = 1e-4,
) -> ScalarRootResult:
    x_old = float(initial)
    history = [x_old]
    converged = False
    iterations = 0

    for k in range(1, max_iterations + 1):
        fx = _call_scalar(func, x_old)
        if abs(fx) <= tolerance:
            converged = True
            break
        dfx = _call_scalar(derivative, x_old)
        if abs(dfx) <= derivative_tolerance:
            raise ValueError("Newton derivative is too small")

        direction = -multiplicity * fx / dfx
        x_new = x_old + direction
        if use_damping:
            x_new = _backtracking_newton_step(
                func,
                x_old,
                direction,
                abs(fx),
                damping_factor,
                min_damping,
            )

        history.append(x_new)
        iterations = k
        step = abs(x_new - x_old)
        residual = abs(_call_scalar(func, x_new))
        if residual <= tolerance or step <= tolerance * max(1.0, abs(x_new)):
            converged = True
            x_old = x_new
            break
        x_old = x_new

    root = float(x_old)
    residual = abs(_call_scalar(func, root))
    return ScalarRootResult(
        root=root,
        iterations=iterations,
        converged=converged,
        residual=float(residual),
        history=np.array(history, dtype=float),
    )


def _backtracking_newton_step(
    func: ScalarFunction,
    x_old: float,
    direction: float,
    current_residual: float,
    damping_factor: float,
    min_damping: float,
) -> float:
    damping = 1.0
    while damping >= min_damping:
        x_trial = x_old + damping * direction
        trial_residual = abs(_call_scalar(func, x_trial))
        if trial_residual < current_residual:
            return x_trial
        damping *= damping_factor
    raise ValueError("damped Newton failed to reduce residual")


def _muller_next(
    func: ScalarFunction,
    x0: float,
    x1: float,
    x2: float,
    denominator_tolerance: float,
) -> float:
    f0 = _call_scalar(func, x0)
    f1 = _call_scalar(func, x1)
    f2 = _call_scalar(func, x2)
    h0 = x1 - x0
    h1 = x2 - x1
    if abs(h0) <= denominator_tolerance or abs(h1) <= denominator_tolerance:
        raise ValueError("Muller nodes must be distinct")
    delta0 = (f1 - f0) / h0
    delta1 = (f2 - f1) / h1
    a = (delta1 - delta0) / (h1 + h0)
    b = a * h1 + delta1
    c = f2
    if abs(a) <= denominator_tolerance:
        if abs(b) <= denominator_tolerance:
            raise ValueError("Muller linear denominator is too small")
        return float(x2 - c / b)
    discriminant = b * b - 4.0 * a * c
    if discriminant < 0.0:
        raise ValueError("real Muller method encountered a negative discriminant")
    sqrt_discriminant = float(np.sqrt(discriminant))
    denominator = b + np.copysign(sqrt_discriminant, b if b != 0.0 else 1.0)
    alternate = b - np.copysign(sqrt_discriminant, b if b != 0.0 else 1.0)
    if abs(denominator) <= denominator_tolerance:
        denominator = alternate
    if abs(denominator) <= denominator_tolerance:
        raise ValueError("Muller denominator is too small")
    return float(x2 - 2.0 * c / denominator)


def _validate_polynomial_coefficients(
    coefficients: np.ndarray | list[complex] | tuple[complex, ...],
) -> np.ndarray:
    coeffs = np.asarray(coefficients, dtype=complex)
    if coeffs.ndim != 1:
        raise ValueError("coefficients must be one-dimensional")
    if coeffs.size < 2:
        raise ValueError("polynomial degree must be at least one")
    if abs(coeffs[0]) == 0:
        raise ValueError("leading coefficient must be nonzero")
    return coeffs


def _initial_polynomial_guesses(
    coefficients: np.ndarray,
    initial_guesses: np.ndarray | list[complex] | tuple[complex, ...] | None,
) -> np.ndarray:
    degree = coefficients.size - 1
    if initial_guesses is not None:
        guesses = np.asarray(initial_guesses, dtype=complex)
        if guesses.ndim != 1 or guesses.size != degree:
            raise ValueError("initial_guesses must contain one guess per root")
        return guesses
    radius = 1.0 + float(np.max(np.abs(coefficients[1:] / coefficients[0])))
    angles = 2.0 * np.pi * np.arange(degree) / degree
    return radius * np.exp(1j * angles)


def _polynomial_roots_residual_norm(coefficients: np.ndarray, roots: np.ndarray) -> float:
    residuals = [abs(polynomial_value_and_derivative(coefficients, root)[0]) for root in roots]
    return float(max(residuals, default=0.0))


def _quadratic_factor_remainder(coefficients: np.ndarray, u: complex, v: complex) -> np.ndarray:
    _, remainder = np.polydiv(coefficients, np.array([1.0 + 0.0j, u, v], dtype=complex))
    remainder = np.asarray(remainder, dtype=complex)
    if remainder.size < 2:
        remainder = np.pad(remainder, (2 - remainder.size, 0))
    elif remainder.size > 2:
        remainder = remainder[-2:]
    return remainder


def _quadratic_remainder_jacobian(coefficients: np.ndarray, u: complex, v: complex) -> np.ndarray:
    residual = _quadratic_factor_remainder(coefficients, u, v)
    step_u = np.sqrt(np.finfo(float).eps) * max(1.0, abs(u))
    step_v = np.sqrt(np.finfo(float).eps) * max(1.0, abs(v))
    residual_u = _quadratic_factor_remainder(coefficients, u + step_u, v)
    residual_v = _quadratic_factor_remainder(coefficients, u, v + step_v)
    return np.column_stack(((residual_u - residual) / step_u, (residual_v - residual) / step_v))
