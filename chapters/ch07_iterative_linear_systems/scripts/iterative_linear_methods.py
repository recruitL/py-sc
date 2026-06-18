"""第七章线性方程组迭代法示例脚本。"""

from __future__ import annotations

import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import (  # noqa: E402
    gauss_seidel_iteration,
    gauss_seidel_iteration_matrix,
    jacobi_iteration,
    jacobi_iteration_matrix,
    spectral_radius,
)


def main() -> None:
    A = np.array(
        [
            [4.0, -1.0, 0.0],
            [-1.0, 4.0, -1.0],
            [0.0, -1.0, 4.0],
        ]
    )
    b = np.array([2.0, 4.0, 6.0])
    exact = np.linalg.solve(A, b)

    jacobi = jacobi_iteration(A, b, tolerance=1e-10, max_iterations=200)
    gs = gauss_seidel_iteration(A, b, tolerance=1e-10, max_iterations=200)

    print("Jacobi:")
    print(f"iterations={jacobi.iterations}, residual={jacobi.residual_norms[-1]:.3e}")
    print(f"error={np.linalg.norm(jacobi.value - exact):.3e}")
    print(f"spectral_radius={spectral_radius(jacobi_iteration_matrix(A)):.6f}")

    print("\nGauss-Seidel:")
    print(f"iterations={gs.iterations}, residual={gs.residual_norms[-1]:.3e}")
    print(f"error={np.linalg.norm(gs.value - exact):.3e}")
    print(f"spectral_radius={spectral_radius(gauss_seidel_iteration_matrix(A)):.6f}")


if __name__ == "__main__":
    main()
