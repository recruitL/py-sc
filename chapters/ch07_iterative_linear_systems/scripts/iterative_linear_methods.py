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
    block_gauss_seidel_iteration,
    block_jacobi_iteration,
    conjugate_gradient,
    gauss_seidel_iteration,
    gauss_seidel_iteration_matrix,
    jacobi_preconditioner,
    jacobi_iteration,
    jacobi_iteration_matrix,
    poisson_2d_dirichlet_matrix,
    poisson_2d_rhs,
    preconditioned_conjugate_gradient,
    reshape_poisson_solution,
    scan_sor_omega,
    sor_iteration,
    steepest_descent,
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

    print("\nSOR omega scan:")
    rows = scan_sor_omega(A, b, np.array([0.8, 1.0, 1.15, 1.4]), tolerance=1e-10, max_iterations=200)
    for omega, iterations, converged, residual in rows:
        print(f"omega={omega:.2f}, iterations={iterations}, converged={converged}, residual={residual:.3e}")

    print("\nBlock iterations:")
    A4 = np.array(
        [
            [5.0, -1.0, 0.0, 0.0],
            [-1.0, 5.0, -1.0, 0.0],
            [0.0, -1.0, 5.0, -1.0],
            [0.0, 0.0, -1.0, 5.0],
        ]
    )
    b4 = np.array([1.0, 2.0, 3.0, 4.0])
    block_j = block_jacobi_iteration(A4, b4, [2, 2], tolerance=1e-10, max_iterations=200)
    block_gs = block_gauss_seidel_iteration(A4, b4, [2, 2], tolerance=1e-10, max_iterations=200)
    sor = sor_iteration(A4, b4, omega=1.1, tolerance=1e-10, max_iterations=200)
    print(f"block_jacobi_iterations={block_j.iterations}, block_gs_iterations={block_gs.iterations}, sor_iterations={sor.iterations}")

    print("\nCG and PCG:")
    A_spd = np.array(
        [
            [6.0, 2.0, 0.0],
            [2.0, 5.0, 1.0],
            [0.0, 1.0, 4.0],
        ]
    )
    b_spd = np.array([1.0, 2.0, 3.0])
    sd = steepest_descent(A_spd, b_spd, tolerance=1e-10, max_iterations=200)
    cg = conjugate_gradient(A_spd, b_spd, tolerance=1e-12)
    pcg = preconditioned_conjugate_gradient(
        A_spd,
        b_spd,
        preconditioner=jacobi_preconditioner(A_spd),
        tolerance=1e-12,
    )
    print(f"steepest_descent_iterations={sd.iterations}, cg_iterations={cg.iterations}, pcg_iterations={pcg.iterations}")

    print("\n2D Poisson:")
    n = 8
    A_p, _ = poisson_2d_dirichlet_matrix(n)
    rhs, x_grid, y_grid = poisson_2d_rhs(
        n,
        lambda x, y: 2.0 * np.pi**2 * np.sin(np.pi * x) * np.sin(np.pi * y),
    )
    exact_grid = np.sin(np.pi * x_grid) * np.sin(np.pi * y_grid)
    poisson_cg = conjugate_gradient(A_p, rhs, tolerance=1e-10, max_iterations=n * n)
    error = np.max(np.abs(reshape_poisson_solution(poisson_cg.value, n) - exact_grid))
    print(f"cg_iterations={poisson_cg.iterations}, residual={poisson_cg.residual_norms[-1]:.3e}, max_error={error:.3e}")


if __name__ == "__main__":
    main()
