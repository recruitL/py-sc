"""第九章非线性方程组示例脚本。"""

from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import (  # noqa: E402
    broyden_system_method,
    chord_newton_system_method,
    damped_newton_system_method,
    finite_difference_jacobian,
    fixed_point_system_iteration,
    newton_system_method,
    parameter_continuation,
)


def main() -> None:
    def iteration(x: np.ndarray) -> np.ndarray:
        return np.array([0.5 * math.cos(x[1]), 0.5 * math.sin(x[0])])

    def fixed_point_residual(x: np.ndarray) -> np.ndarray:
        return x - iteration(x)

    fixed_point = fixed_point_system_iteration(
        iteration,
        [0.3, 0.2],
        tolerance=1e-12,
        residual_func=fixed_point_residual,
    )
    print(
        "fixed point system:",
        f"solution={np.array2string(fixed_point.solution, precision=12)}",
        f"iterations={fixed_point.iterations}",
        f"residual={fixed_point.residual_norm:.3e}",
    )

    def func(x: np.ndarray) -> np.ndarray:
        return np.array([x[0] ** 2 + x[1] ** 2 - 1.0, x[0] - x[1]])

    def jacobian(x: np.ndarray) -> np.ndarray:
        return np.array([[2.0 * x[0], 2.0 * x[1]], [1.0, -1.0]])

    newton = newton_system_method(func, jacobian, [0.8, 0.6], tolerance=1e-12)
    chord = chord_newton_system_method(func, jacobian, [0.8, 0.6], tolerance=1e-10)
    finite_diff = finite_difference_jacobian(func, np.array([0.8, 0.6]))
    print(
        "Newton system:",
        f"solution={np.array2string(newton.solution, precision=12)}",
        f"iterations={newton.iterations}",
        f"residual={newton.residual_norm:.3e}",
    )
    print("finite-difference Jacobian at [0.8, 0.6]:")
    print(np.array2string(finite_diff, precision=8))
    print(
        "chord Newton:",
        f"solution={np.array2string(chord.solution, precision=12)}",
        f"iterations={chord.iterations}",
        f"residual={chord.residual_norm:.3e}",
    )

    damped = damped_newton_system_method(
        lambda x: np.array([x[0] ** 3 - 1.0, x[1]]),
        lambda x: np.array([[3.0 * x[0] ** 2, 0.0], [0.0, 1.0]]),
        [0.1, 0.5],
        tolerance=1e-12,
    )
    print(
        "damped Newton:",
        f"solution={np.array2string(damped.solution, precision=12)}",
        f"iterations={damped.iterations}",
        f"residual={damped.residual_norm:.3e}",
    )

    broyden = broyden_system_method(func, [0.8, 0.6], tolerance=1e-10)
    print(
        "Broyden:",
        f"solution={np.array2string(broyden.solution, precision=12)}",
        f"iterations={broyden.iterations}",
        f"residual={broyden.residual_norm:.3e}",
    )

    continuation = parameter_continuation(
        lambda parameter, x: np.array([x[0] ** 2 - parameter, x[1] - parameter]),
        parameters=[1.0, 1.5, 2.0],
        initial=[1.0, 1.0],
        tolerance=1e-10,
    )
    print("continuation parameters:", continuation.parameters)
    print("continuation solutions:")
    print(np.array2string(continuation.solutions, precision=8))


if __name__ == "__main__":
    main()
