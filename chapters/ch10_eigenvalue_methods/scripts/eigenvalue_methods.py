"""第十章特征值计算示例脚本。"""

from __future__ import annotations

import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import (  # noqa: E402
    eigen_residual_norm,
    inverse_power_method,
    jacobi_eigenvalue_method,
    power_method,
    qr_eigenvalue_iteration,
    rayleigh_quotient,
    rayleigh_quotient_iteration,
)


def main() -> None:
    symmetric = np.array(
        [
            [4.0, 1.0, 0.0],
            [1.0, 3.0, 1.0],
            [0.0, 1.0, 2.0],
        ]
    )
    probe = np.array([1.0, 1.0, 0.0])
    print("Rayleigh quotient:", f"{rayleigh_quotient(symmetric, probe):.12f}")

    dominant = power_method(symmetric, initial=[1.0, 0.5, 0.25], tolerance=1e-12)
    print(
        "power method:",
        f"lambda={dominant.eigenvalue:.12f}",
        f"iterations={dominant.iterations}",
        f"residual={dominant.residual_norm:.3e}",
    )

    near_middle = inverse_power_method(symmetric, shift=2.8, initial=[1.0, 1.0, 1.0], tolerance=1e-12)
    print(
        "inverse power near shift 2.8:",
        f"lambda={near_middle.eigenvalue:.12f}",
        f"iterations={near_middle.iterations}",
        f"residual={near_middle.residual_norm:.3e}",
    )

    rayleigh = rayleigh_quotient_iteration(symmetric, initial=[0.2, 1.0, 0.4], tolerance=1e-13)
    print(
        "Rayleigh quotient iteration:",
        f"lambda={rayleigh.eigenvalue:.12f}",
        f"iterations={rayleigh.iterations}",
        f"residual={rayleigh.residual_norm:.3e}",
    )

    exact_values = np.linalg.eigvalsh(symmetric)
    print("numpy eigvalsh:", np.array2string(exact_values, precision=12))
    print(
        "dominant residual recomputed:",
        f"{eigen_residual_norm(symmetric, dominant.eigenvalue, dominant.eigenvector):.3e}",
    )

    jacobi = jacobi_eigenvalue_method(symmetric, tolerance=1e-12)
    print("Jacobi eigenvalues:", np.array2string(jacobi.eigenvalues, precision=12))
    print(
        "Jacobi:",
        f"rotations={jacobi.iterations}",
        f"offdiag={jacobi.off_diagonal_norm:.3e}",
    )

    qr = qr_eigenvalue_iteration(symmetric[:2, :2], tolerance=1e-12)
    print("QR iteration eigenvalues:", np.array2string(np.sort(qr.eigenvalues), precision=12))
    print(
        "QR iteration:",
        f"iterations={qr.iterations}",
        f"offdiag={qr.off_diagonal_norm:.3e}",
    )


if __name__ == "__main__":
    main()
