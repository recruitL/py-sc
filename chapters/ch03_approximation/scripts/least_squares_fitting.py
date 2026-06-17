from __future__ import annotations

import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = [
    "Arial Unicode MS",
    "PingFang SC",
    "Heiti SC",
    "SimHei",
    "Noto Sans CJK SC",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from py_sc import polynomial_eval, polynomial_least_squares


def main() -> None:
    rng = np.random.default_rng(2026)
    x = np.linspace(-1.0, 1.0, 35)
    y_clean = np.sin(2 * np.pi * x)
    y_noisy = y_clean + 0.15 * rng.normal(size=x.size)
    x_eval = np.linspace(-1.0, 1.0, 500)

    degrees = [3, 7, 14]
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y_noisy, color="black", s=25, label="含噪声数据")
    plt.plot(x_eval, np.sin(2 * np.pi * x_eval), color="gray", linewidth=2, label="真实函数")

    for degree in degrees:
        coefficients = polynomial_least_squares(x, y_noisy, degree=degree)
        y_fit = polynomial_eval(coefficients, x_eval)
        residual = np.linalg.norm(polynomial_eval(coefficients, x) - y_noisy)
        print(f"{degree:2d} 次多项式残差二范数: {residual:.3e}")
        plt.plot(x_eval, y_fit, label=f"{degree} 次拟合")

    plt.title("多项式最小二乘拟合与过拟合")
    plt.xlabel("x")
    plt.ylabel("函数值")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
