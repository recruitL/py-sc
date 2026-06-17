from __future__ import annotations

import math
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

from py_sc import pade_eval, pade_from_taylor, polynomial_eval


def exp_taylor_coefficients(order: int) -> np.ndarray:
    return np.array([1.0 / math.factorial(k) for k in range(order + 1)], dtype=float)


def main() -> None:
    x_eval = np.linspace(-2.0, 2.0, 500)
    y_true = np.exp(x_eval)

    taylor_coefficients = exp_taylor_coefficients(6)
    taylor_3 = polynomial_eval(taylor_coefficients[:4], x_eval)
    numerator, denominator = pade_from_taylor(taylor_coefficients, 3, 3)
    y_pade = pade_eval(numerator, denominator, x_eval)

    print("Padé [3/3] 分子系数:", numerator)
    print("Padé [3/3] 分母系数:", denominator)
    print(f"三次 Taylor 最大误差: {np.max(np.abs(y_true - taylor_3)):.3e}")
    print(f"Padé [3/3] 最大误差: {np.max(np.abs(y_true - y_pade)):.3e}")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(x_eval, y_true, label="exp(x)")
    axes[0].plot(x_eval, taylor_3, "--", label="三次 Taylor")
    axes[0].plot(x_eval, y_pade, ":", label="Padé [3/3]")
    axes[0].set_title("Taylor 与 Padé 逼近")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("函数值")
    axes[0].legend()

    axes[1].semilogy(x_eval, np.abs(y_true - taylor_3) + 1e-16, label="Taylor 误差")
    axes[1].semilogy(x_eval, np.abs(y_true - y_pade) + 1e-16, label="Padé 误差")
    axes[1].set_title("误差对比")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("绝对误差")
    axes[1].legend()

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
