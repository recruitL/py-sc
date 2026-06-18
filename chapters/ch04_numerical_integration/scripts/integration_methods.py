"""第四章数值积分示例脚本。

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
    adaptive_simpson,
    composite_simpson,
    composite_trapezoid,
    gauss_legendre_integrate,
    monte_carlo_integrate,
    romberg_integrate,
)


def convergence_table() -> list[tuple[int, float, float]]:
    """返回复合梯形和复合 Simpson 对一个光滑函数的误差表。"""

    exact = 2.0
    rows = []
    for n in [8, 16, 32, 64, 128]:
        trap_error = abs(composite_trapezoid(np.sin, 0.0, math.pi, n) - exact)
        simp_error = abs(composite_simpson(np.sin, 0.0, math.pi, n) - exact)
        rows.append((n, trap_error, simp_error))
    return rows


def compare_gauss_and_simpson() -> list[tuple[int, float, float]]:
    """比较 Gauss-Legendre 与复合 Simpson 的误差。"""

    exact = math.e - 1.0 / math.e
    rows = []
    for n in [2, 4, 8, 16]:
        gauss_error = abs(gauss_legendre_integrate(np.exp, -1.0, 1.0, n) - exact)
        simpson_error = abs(composite_simpson(np.exp, -1.0, 1.0, 2 * n) - exact)
        rows.append((n, gauss_error, simpson_error))
    return rows


def main() -> None:
    print("复合求积误差：")
    print("n    trapezoid_error      simpson_error")
    for n, trap_error, simp_error in convergence_table():
        print(f"{n:<4d} {trap_error: .6e}      {simp_error: .6e}")

    print("\nRomberg 求积表：")
    romberg = romberg_integrate(math.sin, 0.0, math.pi, max_order=5)
    print(np.array2string(romberg.table, precision=10, suppress_small=False))

    print("\n自适应 Simpson：")
    adaptive = adaptive_simpson(lambda x: 1.0 / (1.0 + 100.0 * (x - 0.25) ** 2), 0.0, 1.0, tolerance=1e-8)
    print(f"value={adaptive.value:.12f}, intervals={adaptive.intervals.shape[0]}, evaluations={adaptive.evaluations}")

    print("\nGauss-Legendre 与 Simpson 对比：")
    print("n    gauss_error          simpson_error")
    for n, gauss_error, simpson_error in compare_gauss_and_simpson():
        print(f"{n:<4d} {gauss_error: .6e}      {simpson_error: .6e}")

    print("\nMonte Carlo：")
    bounds = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
    mc = monte_carlo_integrate(lambda points: np.exp(-np.sum(points**2, axis=1)), bounds, 20_000, seed=2026)
    print(f"value={mc.value:.8f}, standard_error={mc.standard_error:.3e}, samples={mc.sample_count}")


if __name__ == "__main__":
    main()
