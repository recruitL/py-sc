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

from py_sc import bisection_method, find_sign_change_brackets  # noqa: E402


def main() -> None:
    func = lambda x: math.cos(x) - x
    brackets = find_sign_change_brackets(func, 0.0, 2.0, subintervals=20)
    print("brackets:", brackets)
    result = bisection_method(func, brackets[0][0], brackets[0][1], tolerance=1e-12)
    print(f"root={result.root:.12f}, residual={result.residual:.3e}, iterations={result.iterations}")

    polynomial = lambda x: (x - 1.0) * (x + 0.5) * (x - 2.0)
    print("polynomial brackets:", find_sign_change_brackets(polynomial, -1.0, 2.5, 35))

    even_root = lambda x: (x - 1.0) ** 2
    print("even root sign-change brackets:", find_sign_change_brackets(even_root, 0.0, 2.0, 20))
    print("grid min near even root:", np.min([even_root(x) for x in np.linspace(0.0, 2.0, 21)]))


if __name__ == "__main__":
    main()
