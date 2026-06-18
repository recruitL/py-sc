"""第五章数值微分示例脚本。

本脚本是 Notebook 实验的紧凑版本，用于快速检查核心算法是否能运行。
Notebook 中仍保留教学式推导和实现。
"""

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
    central_difference,
    compact_first_derivative_periodic,
    differentiate_discrete,
    five_point_center_derivative,
    forward_difference,
    natural_cubic_spline_derivative,
    observed_order,
    richardson_derivative,
    second_derivative_five_point,
)


def convergence_table() -> list[tuple[float, float, float, float]]:
    """返回前向、中心和五点公式对 sin(x) 的误差表。"""

    x0 = 0.7
    exact = math.cos(x0)
    rows = []
    for h in [2.0**(-k) for k in range(3, 10)]:
        forward_error = abs(float(forward_difference(np.sin, x0, h)) - exact)
        central_error = abs(float(central_difference(np.sin, x0, h)) - exact)
        five_error = abs(float(five_point_center_derivative(np.sin, x0, h)) - exact)
        rows.append((h, forward_error, central_error, five_error))
    return rows


def roundoff_table() -> list[tuple[float, float]]:
    """返回中心差分在极小步长下的误差，用于观察 U 形曲线。"""

    x0 = 1.0
    exact = math.exp(x0)
    rows = []
    for exponent in range(1, 17):
        h = 10.0 ** (-exponent)
        error = abs(float(central_difference(np.exp, x0, h)) - exact)
        rows.append((h, error))
    return rows


def spline_noise_demo() -> tuple[float, float]:
    """比较有限差分和样条微分在含噪声数据上的平均绝对误差。"""

    rng = np.random.default_rng(2026)
    x = np.linspace(0.0, 2.0 * math.pi, 41)
    clean = np.sin(x)
    noisy = clean + 0.02 * rng.normal(size=x.size)
    exact = np.cos(x)

    finite_diff = differentiate_discrete(x, noisy, stencil_size=5)
    spline_diff = natural_cubic_spline_derivative(x, noisy, x)
    return float(np.mean(np.abs(finite_diff - exact))), float(np.mean(np.abs(spline_diff - exact)))


def main() -> None:
    print("一阶差分收敛误差：")
    print("h          forward_error      central_error      five_point_error")
    rows = convergence_table()
    for h, forward_error, central_error, five_error in rows:
        print(f"{h: .6e} {forward_error: .6e}      {central_error: .6e}      {five_error: .6e}")

    central_errors = np.array([row[2] for row in rows])
    five_errors = np.array([row[3] for row in rows])
    print("\n实验收敛阶：")
    print("central:", np.array2string(observed_order(central_errors), precision=3))
    print("five_point:", np.array2string(observed_order(five_errors), precision=3))

    print("\n中心差分 U 形步长误差：")
    print("h          error")
    for h, error in roundoff_table():
        print(f"{h: .1e} {error: .6e}")

    print("\nRichardson 外推表：")
    result = richardson_derivative(np.sin, 0.7, h=0.25, levels=5)
    print(np.array2string(result.table, precision=10, suppress_small=False))
    print(f"value={result.value:.12f}, exact={math.cos(0.7):.12f}")

    print("\n二阶五点公式：")
    second = second_derivative_five_point(np.sin, 0.7, 0.05)
    print(f"value={float(second):.12f}, exact={-math.sin(0.7):.12f}")

    print("\n周期紧致差分：")
    n = 64
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    h = x[1] - x[0]
    compact_error = np.max(np.abs(compact_first_derivative_periodic(np.sin(x), h) - np.cos(x)))
    print(f"max_error={compact_error:.6e}")

    print("\n含噪声数据平均绝对误差：")
    finite_error, spline_error = spline_noise_demo()
    print(f"finite_difference={finite_error:.6e}, natural_spline={spline_error:.6e}")


if __name__ == "__main__":
    main()
