from __future__ import annotations

import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import (
    NaturalCubicSpline,
    lagrange_interpolate,
    newton_divided_differences,
    newton_interpolate,
    piecewise_linear_interpolate,
)


def main() -> None:
    x = np.array([0.0, 0.7, 1.5, 2.4, 3.0, 4.0])
    y = np.sin(x) + 0.15 * x
    x_eval = np.linspace(x.min(), x.max(), 300)

    polynomial = lagrange_interpolate(x, y, x_eval)
    nodes, coefficients = newton_divided_differences(x, y)
    newton = newton_interpolate(nodes, coefficients, x_eval)
    piecewise = piecewise_linear_interpolate(x, y, x_eval)
    spline = NaturalCubicSpline.fit(x, y)(x_eval)

    plt.figure(figsize=(8, 5))
    plt.plot(x_eval, polynomial, label="Lagrange polynomial")
    plt.plot(x_eval, newton, "--", label="Newton polynomial")
    plt.plot(x_eval, piecewise, label="Piecewise linear")
    plt.plot(x_eval, spline, label="Natural cubic spline")
    plt.scatter(x, y, color="black", zorder=3, label="Data")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Chapter 2: interpolation comparison")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
