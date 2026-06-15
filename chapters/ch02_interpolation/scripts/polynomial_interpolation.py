from __future__ import annotations

import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import lagrange_interpolate, newton_divided_differences, newton_interpolate


def main() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])
    x_eval = np.linspace(0.0, 3.0, 7)
    y_eval = lagrange_interpolate(x, y, x_eval)
    nodes, coefficients = newton_divided_differences(x, y)
    newton_eval = newton_interpolate(nodes, coefficients, x_eval)

    for xi, yi, ni in zip(x_eval, y_eval, newton_eval):
        print(f"x={xi:.2f}, 拉格朗日={yi:.6f}, 牛顿={ni:.6f}")


if __name__ == "__main__":
    main()
