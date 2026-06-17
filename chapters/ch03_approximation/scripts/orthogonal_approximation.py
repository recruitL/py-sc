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

from py_sc import (
    chebyshev_fit_function,
    chebyshev_series_eval,
    legendre_fit_function,
    legendre_series_eval,
)


def target(x: np.ndarray) -> np.ndarray:
    return np.exp(x) * np.cos(3 * x)


def main() -> None:
    x_eval = np.linspace(-1.0, 1.0, 500)
    y_true = target(x_eval)
    degree = 12

    cheb_coefficients = chebyshev_fit_function(target, degree=degree, sample_count=40)
    leg_coefficients = legendre_fit_function(target, degree=degree, quadrature_order=80)
    y_cheb = chebyshev_series_eval(cheb_coefficients, x_eval)
    y_leg = legendre_series_eval(leg_coefficients, x_eval)

    print(f"Chebyshev 最大误差: {np.max(np.abs(y_true - y_cheb)):.3e}")
    print(f"Legendre 最大误差: {np.max(np.abs(y_true - y_leg)):.3e}")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(x_eval, y_true, label="目标函数")
    axes[0].plot(x_eval, y_cheb, "--", label="Chebyshev 逼近")
    axes[0].plot(x_eval, y_leg, ":", label="Legendre 逼近")
    axes[0].set_title("正交多项式逼近")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("函数值")
    axes[0].legend()

    axes[1].semilogy(x_eval, np.abs(y_true - y_cheb) + 1e-16, label="Chebyshev 误差")
    axes[1].semilogy(x_eval, np.abs(y_true - y_leg) + 1e-16, label="Legendre 误差")
    axes[1].set_title("逐点误差")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("绝对误差")
    axes[1].legend()

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
