from __future__ import annotations

import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import NaturalCubicSpline


def main() -> None:
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 0.0, 4.0])
    x_eval = np.linspace(0.0, 3.0, 7)
    spline = NaturalCubicSpline.fit(x, y)
    y_eval = spline(x_eval)

    for xi, yi in zip(x_eval, y_eval):
        print(f"x={xi:.2f}, spline(x)={yi:.6f}")


if __name__ == "__main__":
    main()
