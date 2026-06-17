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

from py_sc import adaptive_piecewise_linear, piecewise_linear_interpolate


def target(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + 25.0 * x**2)


def main() -> None:
    x_adapt, y_adapt = adaptive_piecewise_linear(target, -1.0, 1.0, tolerance=2e-3, max_depth=12)
    x_uniform = np.linspace(-1.0, 1.0, x_adapt.size)
    y_uniform = target(x_uniform)
    x_eval = np.linspace(-1.0, 1.0, 600)

    y_true = target(x_eval)
    y_adapt_eval = piecewise_linear_interpolate(x_adapt, y_adapt, x_eval)
    y_uniform_eval = piecewise_linear_interpolate(x_uniform, y_uniform, x_eval)

    print(f"自适应节点数: {x_adapt.size}")
    print(f"同节点数等距分段线性最大误差: {np.max(np.abs(y_true - y_uniform_eval)):.3e}")
    print(f"自适应分段线性最大误差: {np.max(np.abs(y_true - y_adapt_eval)):.3e}")

    plt.figure(figsize=(8, 5))
    plt.plot(x_eval, y_true, label="目标函数")
    plt.plot(x_eval, y_uniform_eval, "--", label="等距分段线性")
    plt.plot(x_eval, y_adapt_eval, ":", label="自适应分段线性")
    plt.scatter(x_adapt, y_adapt, s=18, color="black", label="自适应节点")
    plt.title("自适应分段线性逼近")
    plt.xlabel("x")
    plt.ylabel("函数值")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
