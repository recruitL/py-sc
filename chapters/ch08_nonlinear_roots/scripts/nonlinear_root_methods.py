"""第八章非线性方程求根示例脚本。"""

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
    aitken_delta_squared,
    bairstow_quadratic_factor,
    bisection_method,
    damped_newton_method,
    find_sign_change_brackets,
    fixed_point_iteration,
    modified_newton_method,
    newton_method,
    newton_polynomial_roots,
    muller_method,
    secant_method,
    steffensen_method,
    synthetic_division,
)


def main() -> None:
    func = lambda x: math.cos(x) - x
    brackets = find_sign_change_brackets(func, 0.0, 2.0, subintervals=20)
    print("brackets:", brackets)
    result = bisection_method(func, brackets[0][0], brackets[0][1], tolerance=1e-12)
    print(f"root={result.root:.12f}, residual={result.residual:.3e}, iterations={result.iterations}")

    plain = fixed_point_iteration(math.cos, 0.5, tolerance=1e-12)
    accelerated = steffensen_method(math.cos, 0.5, tolerance=1e-12)
    aitken_values = aitken_delta_squared(plain.history[:8])
    print(
        "fixed point:",
        f"root={plain.root:.12f}",
        f"iterations={plain.iterations}",
        f"residual={plain.residual:.3e}",
    )
    print(
        "steffensen:",
        f"root={accelerated.root:.12f}",
        f"iterations={accelerated.iterations}",
        f"residual={accelerated.residual:.3e}",
    )
    print("first Aitken accelerated values:", np.array2string(aitken_values[:3], precision=12))

    sqrt2 = newton_method(lambda x: x**2 - 2.0, lambda x: 2.0 * x, 1.5, tolerance=1e-12)
    damped = damped_newton_method(lambda x: x**3 - 1.0, lambda x: 3.0 * x**2, 0.1, tolerance=1e-12)
    multiple_plain = newton_method(
        lambda x: (x - 2.0) ** 3,
        lambda x: 3.0 * (x - 2.0) ** 2,
        3.5,
        tolerance=1e-8,
    )
    multiple_modified = modified_newton_method(
        lambda x: (x - 2.0) ** 3,
        lambda x: 3.0 * (x - 2.0) ** 2,
        3.5,
        multiplicity=3,
        tolerance=1e-12,
    )
    print(f"Newton sqrt(2): root={sqrt2.root:.12f}, iterations={sqrt2.iterations}")
    print(f"damped Newton cubic: root={damped.root:.12f}, iterations={damped.iterations}")
    print(
        "multiple root:",
        f"plain_iterations={multiple_plain.iterations}",
        f"modified_iterations={multiple_modified.iterations}",
    )
    secant = secant_method(func, 0.0, 1.0, tolerance=1e-12)
    muller = muller_method(lambda x: x**3 - x - 2.0, 0.0, 1.0, 2.0, tolerance=1e-12)
    print(f"secant cos fixed point: root={secant.root:.12f}, iterations={secant.iterations}")
    print(f"Muller cubic: root={muller.root:.12f}, iterations={muller.iterations}")

    quotient, remainder = synthetic_division([1.0, -6.0, 11.0, -6.0], 1.0)
    polynomial_roots = newton_polynomial_roots(
        [1.0, -6.0, 11.0, -6.0],
        initial_guesses=[0.8, 2.2, 3.2],
        tolerance=1e-12,
    )
    quadratic_factor = bairstow_quadratic_factor(
        [1.0, -3.0, 3.0, -3.0, 2.0],
        linear_coefficient=-2.5,
        constant_coefficient=1.5,
        tolerance=1e-12,
    )
    print("synthetic division quotient:", np.array2string(quotient.real, precision=8), "remainder:", f"{abs(remainder):.3e}")
    print("Newton deflation roots:", np.array2string(np.sort(polynomial_roots.roots.real), precision=8))
    print("Bairstow factor:", np.array2string(np.asarray(quadratic_factor.factor, dtype=float), precision=8))

    polynomial = lambda x: (x - 1.0) * (x + 0.5) * (x - 2.0)
    print("polynomial brackets:", find_sign_change_brackets(polynomial, -1.0, 2.5, 35))

    even_root = lambda x: (x - 1.0) ** 2
    print("even root sign-change brackets:", find_sign_change_brackets(even_root, 0.0, 2.0, 19))
    print("grid min near even root:", np.min([even_root(x) for x in np.linspace(0.0, 2.0, 21)]))


if __name__ == "__main__":
    main()
