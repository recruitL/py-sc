from __future__ import annotations

import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import piecewise_cubic_hermite_interpolate, piecewise_linear_interpolate


def main() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])
    slopes = np.gradient(y, x)
    x_eval = np.linspace(0.0, 3.0, 7)
    linear = piecewise_linear_interpolate(x, y, x_eval)
    hermite = piecewise_cubic_hermite_interpolate(x, y, slopes, x_eval)

    for xi, yi_linear, yi_hermite in zip(x_eval, linear, hermite):
        print(f"x={xi:.2f}, 分段线性={yi_linear:.6f}, 分段三次 Hermite={yi_hermite:.6f}")


if __name__ == "__main__":
    main()
