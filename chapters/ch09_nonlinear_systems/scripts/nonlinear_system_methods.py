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

from py_sc import fixed_point_system_iteration, newton_system_method  # noqa: E402


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
    print(
        "Newton system:",
        f"solution={np.array2string(newton.solution, precision=12)}",
        f"iterations={newton.iterations}",
        f"residual={newton.residual_norm:.3e}",
    )


if __name__ == "__main__":
    main()
